"""Skill smokes for learn pack (no quiz HTML path)."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestLearnPackSkill(unittest.TestCase):
    def test_skill_pack_not_quiz_html(self) -> None:
        skill = (ROOT / "skills/gsuper-learn-pack/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("gsuper-pack-", skill)
        self.assertIn("mermaid flow", skill)
        self.assertIn("Overview first", skill)
        self.assertIn("mermaid", skill)
        self.assertIn("verbatim", skill.lower())
        self.assertIn("Quiz", skill)
        self.assertIn(".agent-workflow/learn/", skill)
        self.assertIn("gsuper-learn-material", skill)
        self.assertNotIn("quiz-data.js", skill)
        self.assertNotIn("overview-data.js", skill)
        self.assertNotIn("need-to-know.md + self-report", skill)
        self.assertNotIn("gsuper-learn-self", skill)

    def test_pack_shape_unique_name(self) -> None:
        shape = (
            ROOT / "skills/gsuper-learn-pack/references/pack-shape.md"
        ).read_text(encoding="utf-8")
        self.assertIn("gsuper-pack-<repo>-<ticket-id>.md", shape)
        self.assertIn("after-brainstorm", shape)
        self.assertIn("Per-unit", shape)
        self.assertIn("Quiz", shape)
        self.assertIn("mermaid", shape)
        self.assertNotIn("quiz.html", shape)


if __name__ == "__main__":
    unittest.main()
