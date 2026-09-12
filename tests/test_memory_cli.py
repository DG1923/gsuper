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

from memory import main
from store import connect, init_schema, upsert_node, upsert_note


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


if __name__ == "__main__":
    unittest.main()
