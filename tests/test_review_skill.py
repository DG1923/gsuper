"""gsuper-review: one pass, evidence gate, no mode menu."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills/gsuper-review/SKILL.md").read_text(encoding="utf-8")
BUG = ROOT / "skills/gsuper-review/references/bug-bar.md"
PERF = ROOT / "skills/gsuper-review/references/performance-bar.md"


class TestReviewSkill(unittest.TestCase):
    def test_one_pass_has_bug_and_performance(self) -> None:
        self.assertTrue(BUG.is_file())
        self.assertTrue(PERF.is_file())
        self.assertIn("## Performance", SKILL)
        self.assertIn("bug-bar.md", SKILL)
        self.assertIn("performance-bar.md", SKILL)
        self.assertIn("Do not offer a mode menu", SKILL)
        self.assertIn("Do not start a second review pass", SKILL)
        self.assertIn("Kết luận cho bạn", SKILL)

    def test_evidence_gate_in_bars(self) -> None:
        bug = BUG.read_text(encoding="utf-8")
        perf = PERF.read_text(encoding="utf-8")
        self.assertIn("No finding without evidence", bug)
        self.assertIn("Bound", perf)
        self.assertIn("No Bound → omit", perf)
        self.assertIn("omit", bug.lower())
        self.assertIn("**Step:**", bug)
        self.assertIn("Why a bug", bug)


if __name__ == "__main__":
    unittest.main()
