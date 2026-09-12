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


if __name__ == "__main__":
    unittest.main()
