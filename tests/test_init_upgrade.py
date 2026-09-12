"""init upgrades workflow layout without dropping sqlite rows."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/gsuper-memory/scripts"))

from memory import main
from store import connect


class TestInitUpgrade(unittest.TestCase):
    def test_init_keeps_nodes_and_migrates_json(self) -> None:
        wf = Path(tempfile.mkdtemp())
        db = wf / "memory.sqlite"
        self.assertEqual(main(["--db", str(db), "init"]), 0)
        self.assertEqual(
            main(
                [
                    "--db",
                    str(db),
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
        learn = wf / "learn"
        learn.mkdir()
        (learn / "invariants.json").write_text(
            json.dumps(
                {
                    "rules": [
                        {
                            "id": "ack-after-handle",
                            "must": "Ack after handle.",
                            "must_not": "Ack before generate.",
                            "spec": "specs/a.md",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(db), "init"])
        self.assertEqual(rc, 0)
        self.assertIn("ok", buf.getvalue())
        md = (wf / "conventions.md").read_text(encoding="utf-8")
        self.assertIn("Ack after handle.", md)
        self.assertFalse((learn / "invariants.json").exists())
        conn = connect(db)
        slugs = [r[0] for r in conn.execute("SELECT slug FROM node").fetchall()]
        conn.close()
        self.assertIn("worker", slugs)

    def test_init_keeps_user_conventions_and_appends(self) -> None:
        wf = Path(tempfile.mkdtemp())
        db = wf / "memory.sqlite"
        (wf / "conventions.md").write_text(
            "# Project conventions\n\nKeep this line.\n",
            encoding="utf-8",
        )
        learn = wf / "learn"
        learn.mkdir()
        (learn / "invariants.json").write_text(
            json.dumps(
                {
                    "rules": [
                        {
                            "id": "no-fail",
                            "must": "Do not call fail().",
                            "must_not": "Call fail().",
                            "spec": "specs/b.md",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.assertEqual(main(["--db", str(db), "init"]), 0)
        md = (wf / "conventions.md").read_text(encoding="utf-8")
        self.assertIn("Keep this line.", md)
        self.assertIn("Do not call fail().", md)
        self.assertFalse((learn / "invariants.json").exists())

    def test_init_bad_json_keeps_file(self) -> None:
        wf = Path(tempfile.mkdtemp())
        db = wf / "memory.sqlite"
        learn = wf / "learn"
        learn.mkdir()
        junk = learn / "invariants.json"
        junk.write_text("{not json", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(["--db", str(db), "init"])
        self.assertEqual(rc, 2)
        self.assertTrue(junk.exists())


if __name__ == "__main__":
    unittest.main()
