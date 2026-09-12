"""Spec lock inserts live spec + decisions; can supersede."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-memory/scripts"))

from store import connect, find, init_schema, upsert_node, upsert_spec_lock


def _db() -> sqlite3.Connection:
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    init_schema(conn)
    upsert_node(conn, slug="worker", kind="part", title="Worker")
    return conn


class TestSpecLock(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = _db()

    def tearDown(self) -> None:
        self.conn.close()

    def test_spec_lock_then_supersede(self) -> None:
        a1 = upsert_spec_lock(
            self.conn,
            ticket="61",
            node="worker",
            path="specs/old.md",
            summary="Redis era",
            decisions=[{"must": "Redis lease", "must_not": "ignore lease"}],
        )
        upsert_spec_lock(
            self.conn,
            ticket="61",
            node="worker",
            path="specs/new.md",
            summary="PGMQ",
            decisions=[{"must": "send/read/delete", "must_not": "fail()"}],
            supersede_id=a1,
        )
        live = find(self.conn, kind="spec", ticket="61")
        self.assertEqual(len(live), 1)
        self.assertTrue(live[0]["path"].endswith("new.md"))
        self.assertEqual(find(self.conn, q="Redis"), [])
        self.assertTrue(find(self.conn, q="Redis", old=True))
        self.assertTrue(find(self.conn, kind="decision", q="delete"))


if __name__ == "__main__":
    unittest.main()
