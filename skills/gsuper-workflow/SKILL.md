---
name: gsuper-workflow
description: >
  Orchestrate gsuper phases gsuper-brainstorm → gsuper-write-spec →
  gsuper-write-plan → gsuper-implement → gsuper-review. gsuper-learn-pack at
  brainstorm/spec/plan/implement; gsuper-learn-material after implement.
  Use when /gsuper-workflow, gsuper, or full code workflow.
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
spec / plan / after brainstorm     →  gsuper-learn-pack       # unique pack + quiz
plan done (after implement)        →  gsuper-learn-material   # one-concept lesson + sample
```

Neither blocks the next ship step if declined.

## Paths

```text
.agent-workflow/specs/
.agent-workflow/plans/
.agent-workflow/scratch/<ticket>/
.agent-workflow/learn/             # pack + material lessons + samples + invariants.json
```

Missing -> **gsuper-init-project**.

## Phase map

| gsuper | ≈ your phase | Skill | Gate |
|--------|--------------|-------|------|
| gsuper-brainstorm | `/clarify` | `gsuper-brainstorm` | Intent + design approved |
| gsuper-write-spec | `/specify` | `gsuper-write-spec` | Spec approved; optional **gsuper-learn-pack** |
| gsuper-write-plan | SP plans + Matt slices | `gsuper-write-plan` | Plan saved; optional **gsuper-learn-pack** |
| gsuper-implement | `/build` | `gsuper-implement` | Evidence; then pack + **gsuper-learn-material** (review not blocked) |
| gsuper-review | `/review` | `gsuper-review` | Defect + Spec + Standards; read-only |

| Side track | When | Skill |
|------------|------|-------|
| Human learn pack | After brainstorm, spec/plan, or implement | `gsuper-learn-pack` |
| Lesson + sample | **After** implement verified | `gsuper-learn-material` |
| Repo closure | Ticket end | phase `/learn` (optional later) |

## Offers

After **gsuper-write-spec** / **gsuper-write-plan** (and after brainstorm intent):

> Unique learn pack Markdown (read + upload ChatGPT/Claude)? → `gsuper-learn-pack`

After **gsuper-implement** (plan done):

> Pack + quiz? → `gsuper-learn-pack` (after-implement). Lesson + sample? → `gsuper-learn-material`

Commands: `/gsuper-workflow-learn` (pack), `/gsuper-workflow-learn-pack`, `/gsuper-workflow-learn-material`.

## Review after implement

`gsuper-review` skill. Three axes. No edit in review. P0 -> back to gsuper-implement.

## GitHub

**gsuper-github-templates**. Sub-issue **Blocked by** = `#<issue_id>`. Nest under parent.

## Related

Rules: `pep8-python`, `small-diffs`, `ponytail`, `python-objects`, `testing-seams`.
Review refs: `skills/gsuper-review/references/github-defect.md`, `standards-bar.md`.
Learn pack: `skills/gsuper-learn-pack/` (mermaid; see `references/diagram-design.md`).
Lesson + sample: `skills/gsuper-learn-material/`.
