---
name: gsuper-review
description: >
  One-pass review — Bug (verified), Performance leaks (Now/Better/Bound),
  Spec (Done when), Standards (gsuper rules). Read-only. After implement / before merge.
---

# Review (gsuper)

Read-only. No edit, no commit, no fix. One pass, one `review.md`. Do not merge ranks.

Do not offer a mode menu. Do not start a second review pass.

| Axis | Bar |
|------|-----|
| **Bug** | [references/bug-bar.md](references/bug-bar.md) — hunt + evidence |
| **Performance** | [references/performance-bar.md](references/performance-bar.md) — leak + Bound |
| **Spec** | Each `Done when` + OOS / Impacted |
| **Standards** | [references/standards-bar.md](references/standards-bar.md) — sure + in-diff |

Style nits: still forbidden ([github-defect.md](references/github-defect.md) “NEVER Comment On”). Unsure on Bug or Standards → omit.

## 0. Diff

```bash
git --no-pager status
# staged -> git --no-pager diff --staged
# unstaged -> git --no-pager diff
# clean tree -> git --no-pager diff main...HEAD
git --no-pager log --oneline -10
```

Empty diff -> blocked. Call next: implement / build.

## 1. Spec file

Order: user path -> `.agent-workflow/specs/` + `scratch/<ticket>/` -> `.scratch/<ticket>/ac.md` or `spec.md` -> `docs/superpowers/specs/`.

None + user says none -> Spec = `no spec available`. Do not invent AC.

Diff no map to spec -> **drift**. Stop. Ask which phase.

## 2. Bug

Follow **bug-bar.md**. Walk all six boxes. Verify this turn. Absolute paths. Never modify.

## 2b. Performance

Follow **performance-bar.md**. No Bound → omit.

## 3. Spec axis

Each `Done when` line -> **evidenced** | **missing** | **partial** | **unverified**.

Scope creep vs Out of scope / Impacted. Implemented-but-wrong -> quote the line.

No PEP8 / Ponytail on this axis.

## 4. Standards

Follow **standards-bar.md**. Cite rule + rung.

## 5. Ask user

Bug vs Spec conflict (ship vs fix). Bug Critical/High security may block merge.

## 6. Write

Prefer `.agent-workflow/scratch/<ticket>/review.md`, else `.scratch/<ticket>/review.md`.

```markdown
# Review — <ticket>
Diff: <staged | unstaged | main...HEAD>

## Bug
(Issue blocks, or: No significant issues found in the reviewed changes.)

## Performance
(Perf blocks, or: No performance leaks found in the diff.)

## Spec
- [ ] <Done when> — evidenced | missing | partial | unverified
- Impacted / OOS: none | …

## Standards
(Standard blocks, or: No significant standards findings.)

## Decisions
P0: Bug Critical/High or Spec missing/wrong
P1: Performance leak with Bound / Standards / user accept?
```

Call next:

- P0 open -> implement (or gsuper-write-spec if AC itself wrong)
- else -> learn / done

Do not apply P0 yourself in this skill.
