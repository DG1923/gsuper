"""Plan vs spec locks: find prefers plan; sync subfolders; --id alias."""

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
from store import connect, find, init_schema, upsert_node, upsert_spec_lock


class TestPlanLock(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.db = self.tmp / "memory.sqlite"
        self.assertEqual(main(["--db", str(self.db), "init"]), 0)
        self.assertEqual(
            main(
                [
                    "--db",
                    str(self.db),
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

    def test_lock_plan_and_find_kind_plan(self) -> None:
        rc = main(
            [
                "--db",
                str(self.db),
                "lock",
                "--kind",
                "plan",
                "--ticket",
                "EL-9",
                "--node",
                "worker",
                "--path",
                "plans/el9.md",
                "--summary",
                "plan ac",
                "--must",
                "done when on plan",
                "--must-not",
                "require spec",
            ]
        )
        self.assertEqual(rc, 0)
        plans = find(connect(self.db), kind="plan", ticket="EL-9")
        specs = find(connect(self.db), kind="spec", ticket="EL-9")
        self.assertEqual(len(plans), 1)
        self.assertTrue(plans[0]["path"].endswith("el9.md"))
        self.assertEqual(specs, [])

    def test_find_ticket_lists_plan_before_legacy_spec(self) -> None:
        conn = connect(self.db)
        init_schema(conn)
        upsert_node(conn, slug="worker", kind="part", title="Worker")
        upsert_spec_lock(
            conn,
            ticket="EL-8-clean-layers",
            node="worker",
            path="specs/2026-09-13-EL-8-clean-layers.md",
            summary="legacy ticket spec",
            decisions=[{"must": "old ac", "must_not": ""}],
            kind="spec",
        )
        upsert_spec_lock(
            conn,
            ticket="EL-8-clean-layers",
            node="worker",
            path="plans/2026-09-13-EL-8-clean-layers.md",
            summary="new plan ac",
            decisions=[{"must": "plan wins", "must_not": ""}],
            kind="plan",
        )
        rows = find(conn, ticket="EL-8")
        kinds = [r["row_kind"] for r in rows if r["row_kind"] in ("plan", "spec")]
        self.assertEqual(kinds[0], "plan")
        self.assertIn("spec", kinds)

    def test_lock_spec_via_id(self) -> None:
        rc = main(
            [
                "--db",
                str(self.db),
                "lock",
                "--kind",
                "spec",
                "--id",
                "captions",
                "--node",
                "worker",
                "--path",
                "specs/architecture/captions.md",
                "--summary",
                "caption architecture",
                "--must",
                "cache sentence in application",
                "--must-not",
                "domain import share",
            ]
        )
        self.assertEqual(rc, 0)
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["--db", str(self.db), "find", "--kind", "spec", "--q", "caption"])
        self.assertIn("captions.md", buf.getvalue())

    def test_sync_specs_subfolder_and_skip_unknown(self) -> None:
        specs = self.tmp / "specs"
        (specs / "architecture").mkdir(parents=True)
        (specs / "unknown-kind").mkdir()
        (specs / "architecture" / "captions.md").write_text(
            "# Captions architecture\n\nCache first.\n", encoding="utf-8"
        )
        (specs / "unknown-kind" / "nope.md").write_text("# Nope\n", encoding="utf-8")
        (specs / "2026-09-13-EL-7-two-facades.md").write_text(
            "# EL-7 two facades\n", encoding="utf-8"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(self.db), "sync", "--specs", str(specs)])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("lock\tcaptions", out)
        self.assertIn("lock\tEL-7-two-facades", out)
        self.assertIn("skip-kind\tnope", out)

    def test_sync_specs_nested_feature_index(self) -> None:
        specs = self.tmp / "specs"
        pack = specs / "feature" / "custom-course"
        pack.mkdir(parents=True)
        (pack / "index.md").write_text("# Custom course\n", encoding="utf-8")
        (pack / "doc-ingest.md").write_text("# Doc ingest\n", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(self.db), "sync", "--specs", str(specs)])
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("lock\tcustom-course", out)
        self.assertIn("lock\tdoc-ingest", out)

    def test_sync_plans_dated_file(self) -> None:
        plans = self.tmp / "plans"
        nested = plans / "gsuper"
        nested.mkdir(parents=True)
        (nested / "2026-09-19-gsuper-plan-as-ticket.md").write_text(
            "# gsuper-plan-as-ticket — Plan\n", encoding="utf-8"
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(self.db), "sync", "--plans", str(plans)])
        self.assertEqual(rc, 0)
        self.assertIn("lock\tgsuper-plan-as-ticket", buf.getvalue())
        found = io.StringIO()
        with redirect_stdout(found):
            main(["--db", str(self.db), "find", "--kind", "plan", "--ticket", "gsuper-plan-as-ticket"])
        self.assertIn("gsuper-plan-as-ticket", found.getvalue())

    def test_store_sync_helpers_defined_once(self) -> None:
        src = (ROOT / "skills/gsuper-memory/scripts/store.py").read_text(
            encoding="utf-8"
        )
        self.assertEqual(src.count("def sync_plan_dir"), 1)
        self.assertEqual(src.count("def sync_spec_dir"), 1)
        self.assertEqual(src.count("def _rel_to_parent"), 1)
        self.assertEqual(src.count("def _lock_sync_file"), 1)


if __name__ == "__main__":
    unittest.main()
