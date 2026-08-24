"""String smokes for learn-plan templates, skills, and init artifacts."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "skills/gsuper-learn-plan/templates/overview.html"
EX = ROOT / "skills/gsuper-learn-plan/templates/overview-data.example.js"
QUIZ = ROOT / "skills/gsuper-learn-plan/templates/quiz.html"
QUIZ_EX = ROOT / "skills/gsuper-learn-plan/templates/quiz-data.example.js"


class TestLearnTemplates(unittest.TestCase):
    def test_overview_template_missing_data_message(self) -> None:
        text = TPL.read_text(encoding="utf-8")
        self.assertIn("overview-data.js", text)
        self.assertIn("OVERVIEW_DATA", text)
        self.assertTrue("Missing" in text or "missing" in text)

    def test_example_data_assigns_global(self) -> None:
        text = EX.read_text(encoding="utf-8")
        self.assertIn("window.OVERVIEW_DATA", text)
        self.assertIn("accumulate", text)

    def test_skill_phase1_path_and_copy(self) -> None:
        skill = (ROOT / "skills/gsuper-learn-plan/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".agent-workflow/learn/", skill)
        self.assertIn("overview-data.js", skill)
        self.assertNotIn("docs/<ticket", skill)
        shape = (ROOT / "skills/gsuper-learn-plan/references/overview-shape.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("learn/<ticket-id>", shape)

    def test_init_learn_artifacts(self) -> None:
        inv = ROOT / "templates/agent-workflow/learn/invariants.json"
        gi = ROOT / "templates/agent-workflow/learn/.gitignore"
        data = inv.read_text(encoding="utf-8")
        self.assertIn('"rules"', data)
        g = gi.read_text(encoding="utf-8")
        self.assertIn("gaps.json", g)
        self.assertIn("profile.json", g)
        self.assertIn("result.json", g)
        init = (ROOT / "skills/gsuper-init-project/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("learn/", init)
        self.assertIn("do not scan", init.lower())

    def test_workflow_mentions_learn_dir(self) -> None:
        wf = (ROOT / "skills/gsuper-workflow/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".agent-workflow/learn/", wf)
        impl = (ROOT / "skills/gsuper-implement/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("invariants.json", impl)

    def test_quiz_template_and_example(self) -> None:
        html = QUIZ.read_text(encoding="utf-8")
        self.assertIn("quiz-data.js", html)
        self.assertIn("QUIZ_DATA", html)
        self.assertIn("gaps.json", html)
        self.assertIn("why_right", html)
        self.assertIn("locked", html)
        data = QUIZ_EX.read_text(encoding="utf-8")
        self.assertIn("window.QUIZ_DATA", data)
        self.assertIn("miss_if_wrong", data)

    def test_skill_gaps_hard_gate(self) -> None:
        skill = (ROOT / "skills/gsuper-learn-plan/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("gaps.json", skill)
        self.assertIn("quiz-data.js", skill)
        self.assertTrue("STOP" in skill or "stop" in skill.lower())

    def test_template_supports_depth(self) -> None:
        html = TPL.read_text(encoding="utf-8")
        self.assertIn("recap", html)
        self.assertIn("depth", html)
        example = EX.read_text(encoding="utf-8")
        self.assertIn("recap", example)
        self.assertIn("lecture", example)

    def test_skill_profile_merge(self) -> None:
        skill = (ROOT / "skills/gsuper-learn-plan/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("profile.json", skill)
        self.assertIn("merge_profile", skill)


if __name__ == "__main__":
    unittest.main()
