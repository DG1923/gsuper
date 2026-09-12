"""x-project seed: PGMQ live, Redis lease hidden."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-memory/scripts"))

from seed_xproject import seed
from store import around, connect, find, init_schema


def _db() -> sqlite3.Connection:
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    init_schema(conn)
    return conn


class TestSeed(unittest.TestCase):
    def test_seed_pgmq_live_lease_hidden(self) -> None:
        conn = _db()
        seed(conn)
        self.assertEqual(find(conn, q="lease"), [])
        self.assertTrue(find(conn, node="queue", q="pgmq"))
        self.assertTrue(find(conn, kind="seam", q="enqueue"))
        slugs = {n["slug"] for n in around(conn, "worker")["neighbors"]}
        self.assertIn("queue", slugs)
        conn.close()


if __name__ == "__main__":
    unittest.main()
