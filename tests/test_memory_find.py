"""find() hides superseded and evidence=doc unless old=True."""

from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-memory/scripts"))

from store import (
    connect,
    find,
    init_schema,
    ticket_in_text,
    ticket_matches,
    upsert_node,
    upsert_note,
    upsert_spec_lock,
)


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

    def test_find_q_and_does_not_raise(self) -> None:
        rows = find(self.conn, q="AND")
        self.assertEqual(rows, [])
        rows = find(self.conn, q="ack AND lease")
        self.assertIsInstance(rows, list)

    def test_ticket_matches_prefix_not_el60(self) -> None:
        self.assertTrue(ticket_matches("EL-6-domain-layer-refactor", "EL-6"))
        self.assertFalse(ticket_matches("EL-60-foo", "EL-6"))
        self.assertTrue(ticket_in_text("plans/2026-09-13-EL-6-domain.md", "EL-6"))
        self.assertFalse(ticket_in_text("plans/2026-09-13-EL-60-foo.md", "EL-6"))

    def test_find_ticket_scopes_notes_and_miss_is_empty(self) -> None:
        upsert_node(self.conn, slug="other", kind="part", title="Other")
        upsert_spec_lock(
            self.conn,
            ticket="EL-6-domain-layer-refactor",
            node="worker",
            path=".agent-workflow/specs/2026-09-13-EL-6-domain-layer-refactor.md",
            summary="domain move",
            decisions=[{"must": "thin application", "must_not": "domain import share.db"}],
        )
        upsert_note(
            self.conn,
            kind="verify",
            node="other",
            body="EL-0-stack verified",
            path=".agent-workflow/plans/2026-09-13-EL-0-stack.md",
        )
        scoped = find(self.conn, ticket="EL-6")
        kinds = {r["row_kind"] for r in scoped}
        self.assertIn("spec", kinds)
        self.assertIn("decision", kinds)
        self.assertFalse(any("EL-0" in (r["body"] or "") for r in scoped))
        self.assertEqual(find(self.conn, ticket="61"), [])
        self.assertEqual(find(self.conn, ticket="EL-60"), [])


if __name__ == "__main__":
    unittest.main()
