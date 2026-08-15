---
name: gsuper-review
description: >
  Three-axis review — Defect (GitHub Copilot bar, verbatim), Spec (Done when),
  Standards (gsuper rules). Read-only. Use after implement, before merge, or /review.
---

# Review (gsuper)

Read-only. No edit, no commit, no fix. Three axes. Do not merge ranks.

| Axis | Bar | Source in plugin |
|------|-----|------------------|
| **Defect** | High-confidence bugs only | [references/github-defect.md](references/github-defect.md) — copy Copilot YAML, do not paraphrase |
| **Spec** | Each `Done when` + OOS / Impacted | Spec file |
| **Standards** | gsuper rules, sure + in-diff | [references/standards-bar.md](references/standards-bar.md) |

Unsure on Defect or Standards -> do not mention.

## 0. Diff

```bash
git --no-pager status
# staged -> git --no-pager diff --staged
# unstaged -> git --no-pager diff
# clean tree -> git --no-pager diff main...HEAD   # or user base
git --no-pager log --oneline -10
```

Empty diff -> blocked. Call next: implement / build.

## 1. Spec file

Order: user path -> `.agent-workflow/specs/` + `scratch/<ticket>/` -> `.scratch/<ticket>/ac.md` or `spec.md` -> `docs/superpowers/specs/`.

None + user says none -> Spec = `no spec available`. Do not invent AC.

Diff no map to spec -> **drift**. Stop. Ask which phase. Do not continue axes as if on-spec.

## 2. Defect

Follow **github-defect.md** verbatim. Absolute paths. Verify when possible. Never modify.

## 3. Spec axis

Each `Done when` line -> exactly one: **evidenced** | **missing** | **partial** | **unverified**.

Also: scope creep vs Out of scope / Impacted range. Implemented-but-wrong -> quote the line.

No PEP8 / Ponytail / objects on this axis.

## 4. Standards

Follow **standards-bar.md**. Cite rule + rung. No Fowler dump.

## 5. Ask user

Defect vs Spec conflict (ship vs fix). Defect Critical/High security may block merge.

## 6. Write

Prefer `.agent-workflow/scratch/<ticket>/review.md`, else `.scratch/<ticket>/review.md`.

```markdown
# Review — <ticket>
Diff: <staged | unstaged | main...HEAD>

## Defect
(Copilot Issue blocks, or: No significant issues found in the reviewed changes.)

## Spec
- [ ] <Done when> — evidenced | missing | partial | unverified
- Impacted / OOS: none | …

## Standards
(Standard blocks, or: No significant standards findings.)

## Decisions
P0: Defect Critical/High or Spec missing/wrong
P1: Standards / user accept?
```

Call next:

- P0 open -> implement (or gsuper-write-spec if AC itself wrong)
- else -> learn / done

Do not apply P0 yourself in this skill.
