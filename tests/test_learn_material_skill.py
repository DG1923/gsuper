"""Skill smokes for learn-material (lesson + sample + validate)."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestLearnMaterialSkill(unittest.TestCase):
    def test_skill_forbids_invented_behavior(self) -> None:
        skill = (ROOT / "skills/gsuper-learn-material/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Never invent behavior", skill)
        self.assertIn("Validate is mandatory", skill)
        self.assertIn("gsuper-material-", skill)
        self.assertIn("does not block review", skill.lower())
        self.assertIn("gsuper-learn-pack", skill)
        self.assertIn("Never write `need-to-know", skill)
        self.assertNotIn("gsuper-learn-self", skill)

    def test_shape_validate_and_contour_trap(self) -> None:
        shape = (
            ROOT / "skills/gsuper-learn-material/references/material-shape.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Validate (mandatory", shape)
        self.assertIn("python", shape)
        self.assertIn("Largest **contour**", shape)
        self.assertIn("speed bucket", shape)
        self.assertNotIn("quiz.html", shape)


if __name__ == "__main__":
    unittest.main()
