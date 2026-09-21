"""Source ladder: compare or raise; no file/func catalog."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE = ROOT / "rules" / "source-ladder.mdc"


class TestSourceLadder(unittest.TestCase):
    def test_rule_always_applies(self) -> None:
        self.assertTrue(RULE.is_file())
        text = RULE.read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", text)
        self.assertIn("So sánh", text)
        self.assertIn("Raise", text)
        self.assertIn("seam.does", text)
        self.assertIn("```mermaid", text)
        lower = text.lower()
        self.assertIn("find --ticket", lower)
        self.assertIn("find --q", lower)
        self.assertIn("do not run find with no", lower)
        self.assertIn("codegraph", lower)
        self.assertIn("insights/", lower)
        self.assertIn("embedding", lower)
        self.assertIn("do not store", lower)

    def test_rule_forbids_func_catalog(self) -> None:
        text = RULE.read_text(encoding="utf-8").lower()
        self.assertIn("do not store", text)
        self.assertTrue("func" in text or "function" in text)
        self.assertIn("depend", text)

    def test_memory_skill_filters_find_and_seam(self) -> None:
        mem = (ROOT / "skills/gsuper-memory/SKILL.md").read_text(encoding="utf-8")
        lower = mem.lower()
        self.assertIn("do not run find with no", lower)
        self.assertIn("seam.does", mem)
        self.assertIn("So sánh", mem)
        self.assertIn("Raise", mem)
        self.assertNotIn("seed-xproject", mem)

    def test_hooks_name_the_ladder(self) -> None:
        for rel in (
            "skills/gsuper-workflow/SKILL.md",
            "skills/gsuper-implement/SKILL.md",
            "skills/gsuper-brainstorm/SKILL.md",
            "skills/gsuper-review/SKILL.md",
            "skills/gsuper-write-plan/SKILL.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("So sánh", text, msg=rel)
            self.assertIn("source-ladder", text, msg=rel)

    def test_implement_writes_seam_after_explore(self) -> None:
        impl = (ROOT / "skills/gsuper-implement/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("memory.py seam", impl)
        self.assertIn("--does", impl)

    def test_version_and_changelog(self) -> None:
        plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        cursor = json.loads(
            (ROOT / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(plugin["version"], "0.9.6")
        self.assertEqual(cursor["version"], "0.9.6")
        log = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("0.9.6", log)
        self.assertIn("gsuper-explain", log)
        self.assertIn("0.9.5", log)
        self.assertIn("source ladder", log.lower())


if __name__ == "__main__":
    unittest.main()
