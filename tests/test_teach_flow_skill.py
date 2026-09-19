"""Brainstorm teaches + Flow before grill; spec template has Flow."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAIN = (ROOT / "skills/gsuper-brainstorm/SKILL.md").read_text(encoding="utf-8")
GRILL = (ROOT / "skills/gsuper-brainstorm/references/grilling.md").read_text(
    encoding="utf-8"
)
TEMPLATE = (
    ROOT / "skills/gsuper-write-spec/references/spec-template.md"
).read_text(encoding="utf-8")
FEATURE_SHAPE = (
    ROOT / "skills/gsuper-write-spec/references/feature-shape.md"
).read_text(encoding="utf-8")
SYSTEM_SHAPE = (
    ROOT / "skills/gsuper-write-spec/references/system-shape.md"
).read_text(encoding="utf-8")
ARCH_SHAPE = (
    ROOT / "skills/gsuper-write-spec/references/architecture-shape.md"
).read_text(encoding="utf-8")
ALGO_SHAPE = (
    ROOT / "skills/gsuper-write-spec/references/algorithm-shape.md"
).read_text(encoding="utf-8")


class TestTeachFlow(unittest.TestCase):
    def test_teach_before_grill(self) -> None:
        check = BRAIN.split("## Checklist")[-1]
        self.assertIn("Teach", check)
        self.assertIn("Flow", check)
        self.assertLess(check.find("Teach"), check.find("Grill"))

    def test_symptom_gate_teaches_before_grill(self) -> None:
        gate = (
            ROOT / "skills/gsuper-brainstorm/references/symptom-gate.md"
        ).read_text(encoding="utf-8")
        what = gate.split("## What to do")[-1]
        self.assertIn("Teach", what)
        self.assertIn("Flow", what)
        self.assertLess(what.find("Teach"), what.find("Grill"))
        self.assertIn("plain language", what.lower())

    def test_grill_q_has_why_and_extra_steps(self) -> None:
        self.assertIn("Why", GRILL)
        self.assertIn("extra steps", GRILL.lower())

    def test_review_issue_has_step_and_why(self) -> None:
        bug = (
            ROOT / "skills/gsuper-review/references/bug-bar.md"
        ).read_text(encoding="utf-8")
        self.assertIn("**Step:**", bug)
        self.assertIn("Why a bug", bug)

    def test_plain_language_in_teach_spec_review(self) -> None:
        bug = (
            ROOT / "skills/gsuper-review/references/bug-bar.md"
        ).read_text(encoding="utf-8")
        spec_skill = (ROOT / "skills/gsuper-write-spec/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("plain language", BRAIN.lower())
        self.assertIn("plain language", TEMPLATE.lower())
        self.assertIn("plain language", spec_skill.lower())
        self.assertIn("plain language", bug.lower())
        self.assertIn("plain language", GRILL.lower())

    def test_spec_template_has_flow(self) -> None:
        self.assertIn("mermaid", TEMPLATE)
        self.assertIn("```mermaid", TEMPLATE)
        self.assertIn("system-shape", TEMPLATE)
        self.assertIn("## Flow", FEATURE_SHAPE)
        self.assertIn("## Requirements", FEATURE_SHAPE)
        self.assertIn("shall", FEATURE_SHAPE.lower())
        self.assertIn("## Problem", FEATURE_SHAPE)
        self.assertIn("index.md", FEATURE_SHAPE)
        self.assertIn("Why", FEATURE_SHAPE)
        self.assertIn("## Actors", SYSTEM_SHAPE)
        self.assertIn("## Context", SYSTEM_SHAPE)
        self.assertNotIn("## Requirements", SYSTEM_SHAPE)
        self.assertIn("## Stores", ARCH_SHAPE)
        self.assertIn("## Layers", ARCH_SHAPE)
        self.assertIn("## Happy", ALGO_SHAPE)
        self.assertIn("## Fallback", ALGO_SHAPE)
        self.assertIn("không dùng", TEMPLATE.lower())
        self.assertIn("đích", TEMPLATE.lower())
        self.assertIn("suy ra", TEMPLATE.lower())
        self.assertIn("SRS-lite", TEMPLATE)

    def test_flow_skills_fence_mermaid_including_chat(self) -> None:
        fence = "```mermaid"
        for rel in (
            "skills/gsuper-brainstorm/SKILL.md",
            "skills/gsuper-brainstorm/references/symptom-gate.md",
            "skills/gsuper-write-plan/SKILL.md",
            "skills/gsuper-write-plan/references/plan-shape.md",
            "skills/gsuper-write-spec/SKILL.md",
            "skills/gsuper-learn-pack/SKILL.md",
            "skills/gsuper-learn-pack/references/pack-shape.md",
            "skills/gsuper-learn-material/SKILL.md",
            "skills/gsuper-learn-material/references/material-shape.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(fence, text, msg=rel)
        for rel in (
            "skills/gsuper-brainstorm/SKILL.md",
            "skills/gsuper-write-plan/SKILL.md",
            "skills/gsuper-write-spec/SKILL.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("chat", text.lower(), msg=rel)


if __name__ == "__main__":
    unittest.main()
