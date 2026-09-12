"""CLI find prints live rows, not Redis."""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-memory/scripts"))

from memory import _print_rows, main
from store import connect, init_schema, upsert_node, upsert_note


class _CharmapStdout:
    """Windows console: encode fails on arrows (review P0)."""

    encoding = "cp1258"

    def __init__(self) -> None:
        self.chunks: list[str] = []

    def write(self, s: str) -> int:
        s.encode("cp1258")
        self.chunks.append(s)
        return len(s)

    def flush(self) -> None:
        return None


class TestCli(unittest.TestCase):
    def test_cli_find_ack(self) -> None:
        tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        tmp.close()
        db = Path(tmp.name)
        conn = connect(db)
        init_schema(conn)
        upsert_node(conn, slug="worker", kind="part", title="Worker")
        upsert_note(
            conn,
            kind="decision",
            node="worker",
            body="must: ack after handle.",
            evidence="spec",
        )
        upsert_note(
            conn,
            kind="decision",
            node="worker",
            body="must: Redis lease.",
            evidence="spec",
            status="superseded",
        )
        conn.close()

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(db), "find", "--node", "worker", "--q", "ack"])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("ack after handle", out)
        self.assertNotIn("Redis", out)

    def test_print_rows_survives_cp1258(self) -> None:
        fake = _CharmapStdout()
        old = sys.stdout
        sys.stdout = fake  # type: ignore[assignment]
        try:
            _print_rows(
                [
                    {
                        "row_kind": "decision",
                        "status": "live",
                        "evidence": "spec",
                        "path": "spec.md",
                        "symbol": "",
                        "body": "timeout/kill → stopped",
                    }
                ]
            )
        finally:
            sys.stdout = old
        text = "".join(fake.chunks)
        self.assertIn("stopped", text)
        self.assertNotIn("\u2192", text)

    def test_cli_around_unknown_node(self) -> None:
        tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        tmp.close()
        db = Path(tmp.name)
        conn = connect(db)
        init_schema(conn)
        conn.close()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(db), "around", "nosuch"])
        self.assertEqual(rc, 2)
        self.assertIn("unknown node", buf.getvalue())

    def test_cli_around_no_duplicate_seam(self) -> None:
        tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        tmp.close()
        db = Path(tmp.name)
        conn = connect(db)
        init_schema(conn)
        upsert_node(conn, slug="worker", kind="part", title="Worker")
        from store import upsert_seam

        upsert_seam(
            conn,
            node="worker",
            symbol="Worker.handle",
            path="worker.py",
            inputs="payload",
            outputs="status",
            does="Run highlight; ack after handle",
        )
        conn.close()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(db), "around", "worker"])
        self.assertEqual(rc, 0)
        self.assertEqual(buf.getvalue().count("Worker.handle"), 1)

    def test_cli_init_creates_schema_when_missing(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "sub" / "memory.sqlite"
        self.assertFalse(tmp.exists())
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(tmp), "init"])
        self.assertEqual(rc, 0)
        self.assertTrue(tmp.exists())
        self.assertIn("created", buf.getvalue())
        conn = connect(tmp)
        names = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table', 'virtual')"
            )
        }
        self.assertIn("node", names)
        conn.close()
        buf2 = io.StringIO()
        with redirect_stdout(buf2):
            rc2 = main(["--db", str(tmp), "init"])
        self.assertEqual(rc2, 0)
        self.assertIn("ok", buf2.getvalue())

    def test_cli_node_then_note(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "memory.sqlite"
        self.assertEqual(main(["--db", str(tmp), "init"]), 0)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(
                [
                    "--db",
                    str(tmp),
                    "node",
                    "--slug",
                    "worker",
                    "--kind",
                    "part",
                    "--title",
                    "Worker",
                ]
            )
        self.assertEqual(rc, 0)
        self.assertIn("ok", buf.getvalue())
        rc = main(
            [
                "--db",
                str(tmp),
                "note",
                "--kind",
                "decision",
                "--node",
                "worker",
                "--body",
                "must: ack after handle.",
            ]
        )
        self.assertEqual(rc, 0)

    def test_cli_rejects_seed_xproject(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "memory.sqlite"
        with self.assertRaises(SystemExit):
            main(["--db", str(tmp), "seed-xproject"])

    def test_cli_lock_then_supersede(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "memory.sqlite"
        self.assertEqual(main(["--db", str(tmp), "init"]), 0)
        self.assertEqual(
            main(
                [
                    "--db",
                    str(tmp),
                    "node",
                    "--slug",
                    "worker",
                    "--kind",
                    "part",
                    "--title",
                    "Worker",
                ]
            ),
            0,
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(
                [
                    "--db",
                    str(tmp),
                    "lock",
                    "--ticket",
                    "61",
                    "--node",
                    "worker",
                    "--path",
                    "specs/old.md",
                    "--summary",
                    "Redis era",
                    "--must",
                    "Redis lease",
                    "--must-not",
                    "ignore lease",
                ]
            )
        self.assertEqual(rc, 0)
        self.assertRegex(buf.getvalue(), r"ok\t\d+")
        self.assertEqual(
            main(
                [
                    "--db",
                    str(tmp),
                    "lock",
                    "--ticket",
                    "61",
                    "--node",
                    "worker",
                    "--path",
                    "specs/new.md",
                    "--summary",
                    "PGMQ",
                    "--must",
                    "send/read/delete",
                    "--must-not",
                    "fail()",
                ]
            ),
            0,
        )
        live = io.StringIO()
        with redirect_stdout(live):
            main(["--db", str(tmp), "find", "--kind", "spec", "--ticket", "61"])
        self.assertIn("new.md", live.getvalue())
        self.assertNotIn("old.md", live.getvalue())
        hidden = io.StringIO()
        with redirect_stdout(hidden):
            main(["--db", str(tmp), "find", "--q", "Redis"])
        self.assertEqual(hidden.getvalue().strip(), "")
        old = io.StringIO()
        with redirect_stdout(old):
            main(["--db", str(tmp), "find", "--q", "Redis", "--old"])
        self.assertIn("Redis", old.getvalue())

    def test_cli_lock_needs_decision(self) -> None:
        tmp = Path(tempfile.mkdtemp()) / "memory.sqlite"
        main(["--db", str(tmp), "init"])
        main(
            [
                "--db",
                str(tmp),
                "node",
                "--slug",
                "worker",
                "--kind",
                "part",
                "--title",
                "Worker",
            ]
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(
                [
                    "--db",
                    str(tmp),
                    "lock",
                    "--ticket",
                    "61",
                    "--node",
                    "worker",
                    "--path",
                    "specs/a.md",
                    "--summary",
                    "empty",
                ]
            )
        self.assertEqual(rc, 2)
        self.assertIn("must", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
