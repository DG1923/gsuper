"""around() neighbors and single-line seam.does."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-memory/scripts"))

from store import (
    around,
    connect,
    find,
    init_schema,
    upsert_edge,
    upsert_node,
    upsert_note,
    upsert_seam,
)


def _db() -> sqlite3.Connection:
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    tmp.close()
    conn = connect(Path(tmp.name))
    init_schema(conn)
    for slug, title in (
        ("queue", "Queue"),
        ("worker", "Worker"),
        ("detect", "Detect"),
        ("score", "Score"),
        ("render", "Render"),
    ):
        upsert_node(conn, slug=slug, kind="part", title=title)
    upsert_edge(conn, "queue", "worker", "next")
    upsert_edge(conn, "worker", "detect", "contains")
    upsert_edge(conn, "worker", "score", "contains")
    upsert_edge(conn, "worker", "render", "contains")
    upsert_edge(conn, "worker", "queue", "depends")
    return conn


class TestAround(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = _db()

    def tearDown(self) -> None:
        self.conn.close()

    def test_around_worker_neighbors(self) -> None:
        out = around(self.conn, "worker")
        slugs = {n["slug"] for n in out["neighbors"]}
        self.assertTrue({"detect", "score", "render", "queue"} <= slugs)

    def test_seam_does_single_line(self) -> None:
        upsert_seam(
            self.conn,
            node="queue",
            symbol="QueueClient.enqueue",
            path="backend/src/lib/queue/client.py",
            inputs="queue, payload: bytes",
            outputs="EnqueueResult",
            does="Send JSON via pgmq.send, return message_id",
        )
        row = find(self.conn, kind="seam", node="queue", q="enqueue")[0]
        self.assertEqual(row["symbol"], "QueueClient.enqueue")
        with self.assertRaises(ValueError):
            upsert_seam(
                self.conn,
                node="queue",
                symbol="bad",
                path="x.py",
                inputs="a",
                outputs="b",
                does="line1\nline2",
            )

    def test_around_notes_exclude_seams(self) -> None:
        upsert_seam(
            self.conn,
            node="worker",
            symbol="Worker.handle",
            path="worker.py",
            inputs="payload",
            outputs="status",
            does="Run highlight; ack after handle",
        )
        upsert_note(
            self.conn,
            kind="decision",
            node="worker",
            body="must: ack after handle.",
        )
        out = around(self.conn, "worker")
        self.assertEqual(len(out["seams"]), 1)
        self.assertTrue(all(r["row_kind"] in ("decision", "note") for r in out["notes"]))
        self.assertFalse(any(r.get("symbol") == "Worker.handle" for r in out["notes"]))


if __name__ == "__main__":
    unittest.main()
