"""Ship path is plan-as-ticket; spec is project docs; plan has no code bodies."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestPlanAsTicketSkills(unittest.TestCase):
    def test_workflow_ship_path_skips_spec(self) -> None:
        wf = (ROOT / "skills/gsuper-workflow/SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "gsuper-brainstorm → gsuper-write-plan → gsuper-implement → gsuper-review",
            wf,
        )
        self.assertIn("is **not** on this path", wf)

    def test_plan_shape_forbids_code_bodies(self) -> None:
        shape = (
            ROOT / "skills/gsuper-write-plan/references/plan-shape.md"
        ).read_text(encoding="utf-8")
        self.assertIn("## Done when", shape)
        self.assertIn("## Testing", shape)
        self.assertIn("Chuyện gì xảy ra", shape)
        self.assertNotIn("real code in steps", shape)
        self.assertNotIn("code steps need code", shape)
        self.assertIn("function bodies", shape)

    def test_brainstorm_hands_off_to_plan(self) -> None:
        brain = (ROOT / "skills/gsuper-brainstorm/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("gsuper-write-plan", brain)
        self.assertIn("After approval", brain)
        after = brain.split("## After approval")[-1]
        self.assertIn("gsuper-write-plan", after)

    def test_implement_gates_on_plan(self) -> None:
        impl = (ROOT / "skills/gsuper-implement/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("No plan → **gsuper-write-plan**", impl)
        self.assertNotIn("No spec → **gsuper-write-spec**", impl)

    def test_spec_is_project_docs(self) -> None:
        spec = (ROOT / "skills/gsuper-write-spec/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("gsuper-write-spec-feature", spec)
        self.assertIn("gsuper-write-spec-algorithm", spec)
        self.assertIn("gsuper-write-spec-architecture", spec)
        self.assertIn("gsuper-write-spec-system", spec)
        self.assertIn("gsuper-write-spec-sync", spec)
        self.assertIn("system-shape", spec)
        flow = (
            ROOT / "skills/gsuper-write-spec/references/spec-flow.md"
        ).read_text(encoding="utf-8")
        self.assertIn("system", flow)
        self.assertIn("algorithm", flow)
        self.assertIn("specs/<kind>/", spec)
        self.assertIn("architecture", spec)
        self.assertIn("--kind spec", spec)
        self.assertIn("--id", spec)
        self.assertIn("Mode A", spec)
        self.assertIn("Reflection", spec)
        self.assertIn("verbatim", spec.lower())
        self.assertIn("only when the user asks", spec)
        self.assertIn("Apply check", spec)
        self.assertIn("rewrite Design", spec)
        self.assertIn("Happy path vs fallback", spec)
        self.assertIn("## Technique", spec)
        self.assertIn("live", spec.lower())
        self.assertIn("suy ra", spec.lower())
        self.assertIn("2–3", spec)
        self.assertIn("Names", spec)
        self.assertIn("Boundaries", spec)
        self.assertIn("SRS-lite", spec)
        self.assertIn("SDD-lite", spec)
        self.assertIn("shall", spec)
        self.assertIn("Contract", spec)
        self.assertIn("đích", spec)
        self.assertIn("Views", spec)
        self.assertIn("Standards", spec)
        self.assertIn("NFR", spec)
        self.assertIn("guardrail", spec.lower())
        self.assertIn("tracing", spec.lower())
        self.assertIn("parent", spec.lower())
        self.assertIn("OWASP", spec)
        self.assertIn("Problem", spec)
        self.assertIn("what + why", spec.lower())
        self.assertIn("concurrent", spec.lower())
        self.assertIn("vector", spec.lower())
        self.assertIn("suggest", spec.lower())
        self.assertIn("never auto", spec.lower())
        self.assertIn("Suggest, then wait", flow)
        self.assertIn("index.md", flow)
        feat = (ROOT / "skills/gsuper-write-spec-feature/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("index.md", feat)
        self.assertIn("cùng folder", feat)
        self.assertNotIn("Do not invent a full SRS for unimplemented", spec)
        skill_lower = spec.lower()
        self.assertIn("one concept", skill_lower)
        self.assertIn("conventions.md", skill_lower)
        self.assertNotIn("treat `.agent-workflow/conventions.md` as **target**", spec.lower())

    def test_one_concept_one_spec_file(self) -> None:
        spec = (ROOT / "skills/gsuper-write-spec/SKILL.md").read_text(encoding="utf-8")
        plan = (ROOT / "skills/gsuper-write-plan/SKILL.md").read_text(encoding="utf-8")
        impl = (ROOT / "skills/gsuper-implement/SKILL.md").read_text(encoding="utf-8")
        wf = (ROOT / "skills/gsuper-workflow/SKILL.md").read_text(encoding="utf-8")
        init = (ROOT / "skills/gsuper-init-project/SKILL.md").read_text(encoding="utf-8")
        pack = (ROOT / "skills/gsuper-learn-pack/SKILL.md").read_text(encoding="utf-8")
        conv = (ROOT / "templates/agent-workflow/conventions.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "templates/agent-workflow/README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("one concept", spec.lower())
        self.assertIn("do not write the same", spec.lower())
        self.assertIn("matching spec", spec.lower())
        self.assertIn("not project law", plan.lower())
        self.assertIn("not project law", impl.lower())
        self.assertIn("not project law", wf.lower())
        self.assertIn("not project law", init.lower())
        self.assertIn("not project law", pack.lower())
        self.assertIn("not project law", conv.lower())
        self.assertIn("specs/", conv)
        self.assertIn("not project law", readme.lower())
        self.assertIn("## 0.9.4", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn('"version": "0.9.4"', (ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertIn(
            '"version": "0.9.4"',
            (ROOT / ".cursor-plugin/plugin.json").read_text(encoding="utf-8"),
        )
        plan = (ROOT / "skills/gsuper-write-plan/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("plans/<feature>/", plan)
        self.assertIn("plans/<feature>/", spec)
        pack = (ROOT / "skills/gsuper-learn-pack/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("learn/<feature>/", pack)


if __name__ == "__main__":
    unittest.main()
