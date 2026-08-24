---
name: gsuper-workflow
description: Orchestrate gsuper phases gsuper-brainstorm → gsuper-write-spec → gsuper-write-plan → gsuper-implement → gsuper-review. gsuper-learn-plan at spec/plan before implement; gsuper-learn-self after plan done. Use when /gsuper-workflow, gsuper, or full code workflow.
---

# gsuper workflow

Hard order (ship only):

```text
gsuper-brainstorm → gsuper-write-spec → gsuper-write-plan → gsuper-implement → gsuper-review
```

No skip unless user skip.

## Entry routing (feature requests)

When the user wants a **new/changed product capability** and there is no approved intent/spec for it:

```text
→ gsuper-brainstorm first (grill / lock intent)
→ then gsuper-write-spec → gsuper-write-plan → gsuper-implement → gsuper-review
```

Do **not** start coding, scaffolding, or gsuper-write-plan from a vague “làm chức năng X”.  
If they already point at an approved `.agent-workflow/specs/…` (or explicit skip clarify) → start at the matching later phase.

Fuzzy mid-flight (implement without clear Done when) → stop → **gsuper-brainstorm** or **gsuper-write-spec**.

**Symptom / hallucination / chưa hiểu vấn đề:** User asks only to patch the surface (“sửa ngọn”) or their framing contradicts facts / doesn’t name the real problem → **stop**, remind them, run **gsuper-brainstorm** (see `skills/gsuper-brainstorm/references/symptom-gate.md`). Do **not** implement first. Explicit temporary workaround only if they accept the debt in intent.

## Side tracks (timing locked)

```text
spec / plan (before implement)  →  gsuper-learn-plan   # quiz then overview HTML under .agent-workflow/learn/
plan done (after implement)     →  gsuper-learn-self   # personal skill cards
```

Neither blocks the next ship step if declined.

## Paths

```text
.agent-workflow/specs/
.agent-workflow/plans/
.agent-workflow/scratch/<ticket>/
.agent-workflow/learning/          # gsuper-learn-self only
.agent-workflow/learn/             # quiz / overview HTML + invariants.json
```

Missing -> **gsuper-init-project**.

## Phase map

| gsuper | ≈ your phase | Skill | Gate |
|--------|--------------|-------|------|
| gsuper-brainstorm | `/clarify` | `gsuper-brainstorm` | Intent + design approved |
| gsuper-write-spec | `/specify` | `gsuper-write-spec` | Spec approved; optional **gsuper-learn-plan** |
| gsuper-write-plan | SP plans + Matt slices | `gsuper-write-plan` | Plan saved; optional **gsuper-learn-plan** |
| gsuper-implement | `/build` | `gsuper-implement` | Evidence; then offer **gsuper-learn-self** |
| gsuper-review | `/review` | `gsuper-review` | Defect + Spec + Standards; read-only |

| Side track | When | Skill |
|------------|------|-------|
| Human overview | Spec or plan, **before** implement | `gsuper-learn-plan` |
| Personal skill | **After** plan done | `gsuper-learn-self` |
| Repo closure | Ticket end | phase `/learn` (optional later) |

## Offers

After **gsuper-write-spec** / **gsuper-write-plan**:

> Mentor overview (mermaid + lecture)? → `gsuper-learn-plan`

After **gsuper-implement** (plan done):

> Personal skill concepts? → `gsuper-learn-self`

Commands: `/gsuper-workflow-learn`, `/gsuper-workflow-learn-self`.

## Review after implement

`gsuper-review` skill. Three axes. No edit in review. P0 -> back to gsuper-implement.

## GitHub

**gsuper-github-templates**. Sub-issue **Blocked by** = `#<issue_id>`. Nest under parent.

## Related

Rules: `pep8-python`, `small-diffs`, `ponytail`, `python-objects`, `testing-seams`.
Review refs: `skills/gsuper-review/references/github-defect.md`, `standards-bar.md`.
Overview HTML: `skills/gsuper-learn-plan/` (mermaid; see `references/diagram-design.md` for the pointer).
Personal cards: `skills/gsuper-learn-self/`.
