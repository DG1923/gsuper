"""Skill smokes for learn pack (no quiz HTML path)."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestLearnPackSkill(unittest.TestCase):
    def test_skill_pack_not_quiz(self) -> None:
        skill = (ROOT / "skills/gsuper-learn-plan/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("gsuper-pack-", skill)
        self.assertIn("need-to-know", skill)
        self.assertIn("self-report", skill)
        self.assertIn(".agent-workflow/learn/", skill)
        self.assertNotIn("quiz-data.js", skill)
        self.assertNotIn("overview-data.js", skill)

    def test_pack_shape_unique_name(self) -> None:
        shape = (
            ROOT / "skills/gsuper-learn-plan/references/pack-shape.md"
        ).read_text(encoding="utf-8")
        self.assertIn("gsuper-pack-<repo>-<ticket-id>.md", shape)
        self.assertIn("after-brainstorm", shape)
        self.assertNotIn("quiz.html", shape)


if __name__ == "__main__":
    unittest.main()
