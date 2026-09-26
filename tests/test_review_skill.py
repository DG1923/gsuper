"""gsuper-review: one pass, evidence gate, no mode menu."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills/gsuper-review/SKILL.md").read_text(encoding="utf-8")
BUG = ROOT / "skills/gsuper-review/references/bug-bar.md"
PERF = ROOT / "skills/gsuper-review/references/performance-bar.md"


class TestReviewSkill(unittest.TestCase):
    def test_router_runs_both_skills_in_parallel(self) -> None:
        self.assertTrue(BUG.is_file())
        self.assertTrue(PERF.is_file())
        self.assertIn("## Performance", SKILL)
        self.assertIn("bug-bar.md", SKILL)
        self.assertIn("performance-bar.md", SKILL)
        self.assertIn("Do not apply", SKILL)
        self.assertIn("verified-bug-hunt", SKILL)
        self.assertIn("code-review", SKILL)
        self.assertIn("in parallel", SKILL)
        self.assertIn("Do not paraphrase", SKILL)
        self.assertIn("Do not offer a mode menu", SKILL)
        self.assertIn("Do not start a second review pass", SKILL)
        self.assertIn("Kết luận cho bạn", SKILL)
        self.assertIn("Do not drop a hunt finding", SKILL)
        self.assertIn("skills/verified-bug-hunt/SKILL.md", SKILL)
        self.assertIn("skills/code-review/SKILL.md", SKILL)
        hunt = (ROOT / "skills/verified-bug-hunt/SKILL.md").read_text(encoding="utf-8")
        review = (ROOT / "skills/code-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: verified-bug-hunt", hunt)
        self.assertIn("name: code-review", review)
        self.assertIn("if you didn't run it and see the output, it isn't a finding", hunt)
        self.assertIn("## Standards", review)
        self.assertIn("## Spec", review)

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
