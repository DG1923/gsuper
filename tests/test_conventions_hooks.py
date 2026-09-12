"""Project conventions live at .agent-workflow/conventions.md, not invariants.json."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestConventionsHooks(unittest.TestCase):
    def test_no_invariants_store(self) -> None:
        for rel in (
            "skills/gsuper-write-spec/SKILL.md",
            "skills/gsuper-implement/SKILL.md",
            "skills/gsuper-learn-pack/SKILL.md",
            "skills/gsuper-init-project/SKILL.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("conventions.md", text)
            if rel.endswith("gsuper-init-project/SKILL.md"):
                self.assertIn("migrat", text.lower())
                continue
            self.assertNotIn("invariants.json", text)
        self.assertTrue((ROOT / "templates/agent-workflow/conventions.md").is_file())
        self.assertFalse(
            (ROOT / "templates/agent-workflow/learn/invariants.json").exists()
        )
        spec = (ROOT / "skills/gsuper-write-spec/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("approv", spec.lower())


if __name__ == "__main__":
    unittest.main()
