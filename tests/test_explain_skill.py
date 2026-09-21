"""Skill smokes for gsuper-explain (arrow-chain, chat default, silent self-check)."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestExplainSkill(unittest.TestCase):
    def test_skill_arrow_chain_not_pack(self) -> None:
        skill = (ROOT / "skills/gsuper-explain/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: gsuper-explain", skill)
        self.assertIn("giải thích", skill)
        self.assertIn("diễn giải", skill)
        self.assertIn("->", skill)
        self.assertIn("plain language", skill.lower())
        self.assertIn("chat only", skill.lower())
        self.assertIn("Self-check before sending", skill)
        self.assertIn("silently", skill.lower())
        self.assertIn("```mermaid", skill)
        self.assertIn("flowchart TD", skill)
        self.assertIn("gsuper-learn-pack", skill)
        self.assertIn("gsuper-learn-material", skill)
        self.assertNotIn("in this project", skill)
        self.assertNotIn("gsuper-learn-self", skill)

    def test_command_points_at_skill(self) -> None:
        cmd = (ROOT / "commands/gsuper-explain.md").read_text(encoding="utf-8")
        self.assertIn("gsuper-explain", cmd)
        self.assertIn("giải thích", cmd)

    def test_workflow_lists_on_demand_side_track(self) -> None:
        wf = (ROOT / "skills/gsuper-workflow/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("gsuper-explain", wf)
        self.assertIn(
            "gsuper-brainstorm → gsuper-write-plan → gsuper-implement → gsuper-review",
            wf,
        )
        self.assertIn("is **not** on this path", wf)


if __name__ == "__main__":
    unittest.main()
