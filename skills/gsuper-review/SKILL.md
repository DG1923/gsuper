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
| **Spec** | Each plan `Done when` + OOS / Impacted (legacy ticket spec only if no plan) |
| **Standards** | [references/standards-bar.md](references/standards-bar.md) — sure + in-diff |

Style nits: still forbidden ([github-defect.md](references/github-defect.md) “NEVER Comment On”). Unsure on Bug or Standards → omit.

## 0. Memory then diff

Run `memory.py find --ticket <id>` or `find --q <topic>` first. Empty → index miss; use the **plan** file on disk (legacy ticket spec only if no plan). Do not treat empty find as “no plan”. **source-ladder:** **`So sánh:`** each finding to a Flow step / Done when / test, or omit (**`Raise:`** is not a Bug rank — skip the finding).

## 0b. Diff

```bash
git --no-pager status
# staged -> git --no-pager diff --staged
# unstaged -> git --no-pager diff
# clean tree -> git --no-pager diff main...HEAD
git --no-pager log --oneline -10
```

Empty diff -> blocked. Call next: implement / build.

## 1. Plan file (AC)

Order: user path -> `.agent-workflow/plans/` + `scratch/<ticket>/` -> legacy `.agent-workflow/specs/YYYY-MM-DD-<ticket>.md` if **no** plan -> `.scratch/<ticket>/ac.md`.

Spec-docs under `specs/algorithm|srs|feature|architecture|system/` are not ticket AC.

None + user says none -> Spec axis = `no plan available`. Do not invent AC.

Diff no map to plan -> **drift**. Stop. Ask which phase.

## 2. Bug

Follow **bug-bar.md**. Walk all six boxes. Verify this turn. Absolute paths. Never modify.

Each Issue must name the **Flow step** (from the plan, or a user-visible step if no Flow) and **Why a bug** in **plain language** (expected I/O vs what happened; why that breaks Purpose — no jargon-only sentence). Omit the finding if you cannot say that.

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

The user **reads and decides** this file. Lead with natural language. Axes stay; they do not replace the summary.

```markdown
# Review — <ticket>
Diff: <staged | unstaged | main...HEAD>

## Kết luận cho bạn
<5–10 câu lời thường: ship được không; chỗ nào hỏng (bước user thấy); bạn cần quyết gì. Không mở đầu bằng P0/file:line.>
So sánh: <Done when / test / seam> → khớp | lệch | thiếu (Raise, không bịa).

## Bug
(Issue blocks with Step + Why a bug, or: No significant issues found in the reviewed changes.)

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

- P0 open -> implement (or gsuper-write-plan if AC itself wrong)
- else -> learn / done

Do not apply P0 yourself in this skill.
