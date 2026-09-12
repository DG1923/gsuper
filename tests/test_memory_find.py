"""find() hides superseded and evidence=doc unless old=True."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-memory/scripts"))

from store import connect, find, init_schema, upsert_node, upsert_note


def _db() -> sqlite3.Connection:
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    init_schema(conn)
    upsert_node(conn, slug="worker", kind="part", title="Worker", blurb="highlight worker")
    upsert_note(
        conn,
        kind="decision",
        node="worker",
        body="must: ack after handle. must_not: ack before generate.",
        evidence="spec",
        status="live",
    )
    upsert_note(
        conn,
        kind="decision",
        node="worker",
        body="must: Redis lease is a claim marker.",
        evidence="spec",
        status="superseded",
    )
    upsert_note(
        conn,
        kind="decision",
        node="worker",
        body="SRS tennis timeout numbers",
        evidence="doc",
        status="live",
    )
    return conn


class TestFind(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = _db()

    def tearDown(self) -> None:
        self.conn.close()

    def test_find_hides_superseded_and_doc(self) -> None:
        rows = find(self.conn, q="lease")
        self.assertEqual(rows, [])
        old = find(self.conn, q="lease", old=True)
        self.assertTrue(any("Redis" in r["body"] for r in old))

    def test_find_ack_on_worker(self) -> None:
        rows = find(self.conn, kind="decision", node="worker", q="ack")
        self.assertEqual(len(rows), 1)
        self.assertIn("ack after handle", rows[0]["body"])
        self.assertEqual(rows[0]["status"], "live")


if __name__ == "__main__":
    unittest.main()
