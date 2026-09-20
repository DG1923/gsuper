---
name: gsuper-workflow
description: >
  Orchestrate gsuper phases gsuper-brainstorm → gsuper-write-plan →
  gsuper-implement → gsuper-review. gsuper-write-spec is on-demand project
  docs (algorithm / SRS / architecture / large feature). gsuper-learn-pack at
  brainstorm/plan/implement; gsuper-learn-material after implement.
  Use when /gsuper-workflow, gsuper, or full code workflow.
---

# gsuper workflow

Hard order (ship only):

```text
gsuper-brainstorm → gsuper-write-plan → gsuper-implement → gsuper-review
```

**gsuper-write-spec** is **not** on this path. Run it when the user asks to write or update algorithm / SRS / large feature / architecture / system design docs.

No skip of brainstorm/plan unless user skip.

## Entry routing (feature requests)

When the user wants a **new/changed product capability** and there is no approved intent/plan for it:

```text
→ gsuper-brainstorm first (grill / lock intent)
→ then gsuper-write-plan → gsuper-implement → gsuper-review
```

Do **not** start coding, scaffolding, or gsuper-write-plan from a vague “làm chức năng X”.  
If they already point at an approved `.agent-workflow/plans/…` (or explicit skip clarify) → start at the matching later phase.

Fuzzy mid-flight (implement without clear Done when) → stop → **gsuper-brainstorm** or **gsuper-write-plan**.

**Symptom / hallucination / chưa hiểu vấn đề:** User asks only to patch the surface (“sửa ngọn”) or their framing contradicts facts / doesn’t name the real problem → **stop**, remind them, run **gsuper-brainstorm** (see `skills/gsuper-brainstorm/references/symptom-gate.md`). Do **not** implement first. Explicit temporary workaround only if they accept the debt in intent.

**Project docs:** “viết SRS / thuật toán / kiến trúc / core / update spec / **sync spec** / project có sẵn” → **gsuper-write-spec**. Large existing repo → **gsuper-write-spec-sync** then one kind. Each kind has its own shape (not one template). On demand; **not after every implement**. New feature: write that kind only; **suggest** sibling drift, never auto-update system/architecture/algorithm. Doc flow: system → architecture → algorithm → feature → plan.

## Side tracks (timing locked)

```text
plan / after brainstorm          →  gsuper-learn-pack       # unique pack + quiz
plan done (after implement)      →  gsuper-learn-material   # one-concept lesson + sample
```

Neither blocks the next ship step if declined.

## Paths

```text
.agent-workflow/plans/<feature>/           # ticket AC (Done when)
.agent-workflow/specs/<kind>/<feature>/    # algorithm|feature|architecture; system/ flat
.agent-workflow/specs/_legacy/             # optional leftover dated ticket specs
.agent-workflow/scratch/<ticket>/
.agent-workflow/learn/<feature>/           # pack + material + samples
.agent-workflow/conventions.md     # not project law (init/migrate stub); must/must-not live in specs/<kind>/
.agent-workflow/memory.sqlite      # local find index — gitignore; memory.py find first
```

Missing -> **gsuper-init-project**.

## Phase map

| gsuper | ≈ your phase | Skill | Gate |
|--------|--------------|-------|------|
| gsuper-brainstorm | `/clarify` | `gsuper-brainstorm` | Intent + design approved |
| gsuper-write-plan | ticket AC | `gsuper-write-plan` | Plan approved + `lock --kind plan`; optional **gsuper-learn-pack** |
| gsuper-write-spec | project docs | `gsuper-write-spec` | User asked for algorithm/SRS/architecture/feature/system; `lock --kind spec` |
| gsuper-implement | `/build` | `gsuper-implement` | Evidence vs plan Done when; then pack + **gsuper-learn-material** (review not blocked) |
| gsuper-review | `/review` | `gsuper-review` | Bug + Performance + plan Done when + Standards; one pass |

| Side track | When | Skill |
|------------|------|-------|
| Human learn pack | After brainstorm, plan, or implement | `gsuper-learn-pack` |
| Lesson + sample | **After** implement verified | `gsuper-learn-material` |
| Repo closure | Ticket end | phase `/learn` (optional later) |

## Offers

After **gsuper-write-plan** (and after brainstorm intent; after spec-docs if written):

> Unique learn pack Markdown (read + upload ChatGPT/Claude)? → `gsuper-learn-pack`

After **gsuper-implement** (plan done):

> Pack + quiz? → `gsuper-learn-pack` (after-implement). Lesson + sample? → `gsuper-learn-material`

Commands: `/gsuper-workflow-learn` (pack), `/gsuper-workflow-learn-pack`, `/gsuper-workflow-learn-material`.

## Review after implement

`gsuper-review` skill. Three axes (Spec axis = plan Done when). No edit in review. P0 -> back to gsuper-implement.

## Migration (0.8)

Do **not** rewrite existing `specs/YYYY-MM-DD-*.md` or old fat plans. New tickets: plan only. Implement/review: plan first; legacy dated spec if no plan. `memory.py sync --plans` and `sync --specs` (subfolders + dated root).

## GitHub

**gsuper-github-templates**. Sub-issue **Blocked by** = `#<issue_id>`. Nest under parent.

## Related

Rules: `pep8-python`, `small-diffs`, `ponytail`, `python-objects`, `testing-seams`, `source-ladder` (`So sánh:` / `Raise:`; `find --ticket` / `--q` / `around`; `seam.does` only).
Review refs: `skills/gsuper-review/references/github-defect.md`, `standards-bar.md`.
Learn pack: `skills/gsuper-learn-pack/` (mermaid; see `references/diagram-design.md`).
Lesson + sample: `skills/gsuper-learn-material/`.
