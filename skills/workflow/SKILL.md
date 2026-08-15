---
name: workflow
description: Orchestrate gsuper phases brainstorm → spec → plan → implement → review. learn-plan at spec/plan before implement; learn-self after plan done. Use when /workflow, gsuper, or full code workflow.
---

# gsuper workflow

Hard order (ship only):

```text
brainstorm → write-spec → write-plan → implement → review
```

No skip unless user skip.

## Entry routing (feature requests)

When the user wants a **new/changed product capability** and there is no approved intent/spec for it:

```text
→ brainstorm first (grill / lock intent)
→ then write-spec → write-plan → implement → review
```

Do **not** start coding, scaffolding, or write-plan from a vague “làm chức năng X”.  
If they already point at an approved `.agent-workflow/specs/…` (or explicit skip clarify) → start at the matching later phase.

Fuzzy mid-flight (implement without clear Done when) → stop → **brainstorm** or **write-spec**.

**Symptom / hallucination / chưa hiểu vấn đề:** User asks only to patch the surface (“sửa ngọn”) or their framing contradicts facts / doesn’t name the real problem → **stop**, remind them, run **brainstorm** (see `skills/brainstorm/references/symptom-gate.md`). Do **not** implement first. Explicit temporary workaround only if they accept the debt in intent.

## Side tracks (timing locked)

```text
spec / plan (before implement)  →  learn-plan   # diagrams — understand to ship
plan done (after implement)     →  learn-self   # personal skill cards
```

Neither blocks the next ship step if declined.

## Paths

```text
.agent-workflow/specs/
.agent-workflow/plans/
.agent-workflow/scratch/<ticket>/
.agent-workflow/learning/          # learn-self only
```

Missing -> **init-project**.

## Phase map

| gsuper | ≈ your phase | Skill | Gate |
|--------|--------------|-------|------|
| brainstorm | `/clarify` | `brainstorm` | Intent + design approved |
| write-spec | `/specify` | `write-spec` | Spec approved; optional **learn-plan** |
| write-plan | SP plans + Matt slices | `write-plan` | Plan saved; optional **learn-plan** |
| implement | `/build` | `implement` | Evidence; then offer **learn-self** |
| review | `/review` | `review` | Defect + Spec + Standards; read-only |

| Side track | When | Skill |
|------------|------|-------|
| Diagram | Spec or plan, **before** implement | `learn-plan` |
| Personal skill | **After** plan done | `learn-self` |
| Repo closure | Ticket end | phase `/learn` (optional later) |

## Offers

After **write-spec** / **write-plan**:

> Diagram walkthrough? → `learn-plan`

After **implement** (plan done):

> Personal skill concepts? → `learn-self`

Commands: `/workflow-learn`, `/workflow-learn-self`.

## Review after implement

`review` skill. Three axes. No edit in review. P0 -> back to implement.

## GitHub

**github-templates**. Sub-issue **Blocked by** = `#<issue_id>`. Nest under parent.

## Related

Rules: `pep8-python`, `small-diffs`, `ponytail`, `python-objects`, `testing-seams`.
Review refs: `skills/review/references/github-defect.md`, `standards-bar.md`.
Diagrams: `references/diagram-design.md`.
Personal cards: `skills/learn-self/`.
