---
name: gsuper-learn-material
description: >
  Implementation-grounded lesson plus a minimal runnable sample and a
  behavior-aligned quiz from completed, verified work. Extract 3–6 mental
  models, one concept per lesson. Never invent behavior to clean the lesson.
  Validate theory == sample == production (required). Use after implement
  done, or /gsuper-workflow-learn-material. Not the pack (gsuper-learn-pack).
  Not implement AC. Does not block review.
---

# Learn material (gsuper)

**Not** implement. **Not** `gsuper-learn-pack` (ticket pack). **Not** AC.

Purpose: turn **verified implementation** into one lesson you can ôn: mental model + toy code that still does the same thing + quiz.

Shape: [references/material-shape.md](references/material-shape.md).

```text
completed work
   → gsuper-learn-pack       # optional: whole-ticket map
   → gsuper-learn-material   # this skill: one concept + sample
```

Review is **not** gated on this skill. Decline is OK.

## When

- After **gsuper-implement** has evidence (plan/ticket done)
- `/gsuper-workflow-learn-material` with a ticket / unit name (e.g. BallDetector)
- Input: live code that shipped + pack/spec only as pointers — **code wins**

Do **not** run this on unshipped design. Do **not** teach a stack you did not implement.  
Do **not** offer this right after **gsuper-write-plan** — that stage is pack only (`gsuper-learn-pack`).

## Hard rules

1. **Never invent behavior to make the lesson cleaner.**  
   Production `acceleration = "fast"` stays a **speed bucket**. Do not rewrite it as Δv because the name is wrong.

2. **Sample may simplify implementation, but must preserve the behavior being taught.**  
   Drop GPU / FastAPI / CSV cache. Do not change the rule (largest **contour**, not union of all `> 0.5` cells).

3. **Validate is mandatory.** If theory, sample, and production disagree — fix or delete the claim. Do not ship the lesson.

## Four competencies (all required, in order)

| # | Competency | Question | Fail if |
|---|---|---|---|
| 1 | Reverse-engineer | Code actually does what? | Paraphrase from memory / README |
| 2 | Teach | Which 3–6 models are worth teaching? | Dump the architecture |
| 3 | Reproduce | Smallest runnable proof? | Sample needs `backend/` or GPU |
| 4 | Validate | Theory == sample == production? | Skipped or “close enough” |

## Pipeline

```text
Completed + verified implementation
        ↓
1 Reverse-engineer — list actual behaviors (path:line)
        ↓
2 Teach — 3–6 concepts; pick traps / misses / boundaries you hit
        ↓
   STOP — list the concepts; user picks ONE (or decline)
        ↓
3 Reproduce — Part A mental model; Part B one py (+ few files)
        ↓
   Production snippets + name mapping (sample name → live name)
        ↓
   Quiz from the taught behavior only
        ↓
4 Validate — theory == sample == production; run the sample
```

Do not write the lesson until the user picks. One concept per file.

## Paths

```text
.agent-workflow/learn/gsuper-material-<repo>-<ticket>-<concept>.md
.agent-workflow/learn/samples/<concept>/          # python <file>.py
```

Never `pack.md`. Never overwrite the pack. Never write `need-to-know-*.md`.

## Pedagogical chain (each lesson)

`theory → example → execution → quiz`

- **Theory** — one mermaid mental model; must/must-not; drift vs misleading names
- **Example** — production excerpt (verbatim, short) + mapping table
- **Execution** — agent **runs** the sample this turn; paste or summarize stdout
- **Quiz** — open questions, **no answer key**; only what the sample + excerpts prove

Semantic names in the sample are OK (`speed_bucket`) if the mapping table shows live `acceleration`.

## Vs pack

| Skill | Artifact | Job |
|---|---|---|
| `gsuper-learn-pack` | `gsuper-pack-<repo>-<ticket>.md` | Whole-ticket map |
| `gsuper-learn-material` | `gsuper-material-…-<concept>.md` + sample | One concept; must run |

## Guardrails

| Do | Do not |
|---|---|
| Teach only implemented + verified behavior | New tech stacks “you could have used” |
| Prefer the trap / miss / boundary you actually hit | Syntax tours |
| Stdlib (or tiny deps) toy | Import production modules |
| One concept | Whole pipeline in one lesson (that is the pack) |
| Evidence: `path:line` on every claim | Invent a cleaner algorithm |

Failed trial (do not repeat): sample used bbox of **all** cells `> 0.5`. Live is **largest contour** bbox (`_extract_ball_position_contours`). That is a Validate fail.
