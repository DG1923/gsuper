---
name: gsuper-write-plan
description: >
  Bite-sized implementation plan under .agent-workflow/plans/ after approved spec.
  Vendors Superpowers writing-plans + Matt vertical slices. Soft ~500 LOC/task;
  after save: offer gsuper-learn-plan overview HTML only (pre-implement). gsuper-learn-self is after plan done.
---

# Write plan (gsuper)

Self-contained. **No** runtime Superpowers `writing-plans` or Matt `to-tickets`.

Gate: approved spec with `Done when:` (`.agent-workflow/specs/` or fallback `.scratch/`). Missing → **gsuper-write-spec**.

## Vendored cores

| Source | Kept |
|--------|------|
| SP `writing-plans` | Header; file map; bite-size TDD steps; Interfaces; no placeholders; self-review; exact cmds |
| Matt `to-tickets` | Vertical slices; Blocked by; expand–contract for wide refactors; quiz granularity if unclear |
| gsuper | `.agent-workflow/plans/`; soft 500 LOC; offer **gsuper-learn-plan** only; handoff **gsuper-implement**; commits optional |

Dropped: worktrees; REQUIRED SP subagent skills; “announce skill name”; forced commit every task.

Detail: [references/plan-shape.md](references/plan-shape.md)

## Output

```text
.agent-workflow/plans/YYYY-MM-DD-<feature>.md
```

Missing dir → **gsuper-init-project**.

## Process

1. Read approved spec (and intent if present).
2. Scope / file map / task breakdown per [plan-shape.md](references/plan-shape.md).
3. If granularity unclear → short quiz (too coarse/fine? blocking edges?) then write.
4. Write full plan — real code in steps, not outlines.
5. Self-review (coverage / placeholders / types).
6. Save file.
7. **After save — overview HTML only (pre-implement):**

   > Mentor overview of this plan? → **gsuper-learn-plan**

   Do **not** offer **gsuper-learn-self** here (that is after the plan is **done**).

8. Exit → user runs **gsuper-implement** when ready.

## Rules while writing

- Samples readable; Python PEP 8
- Align steps with implement loop: test → RED → fill → GREEN
- Ponytail: don’t plan gold-plating the spec didn’t ask for
- No silent scope expand — gap → ask or note Open in plan
