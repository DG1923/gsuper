---
name: gsuper-review
description: >
  Router for one review. Runs verified-bug-hunt and code-review in parallel,
  unchanged. Read-only. After implement / before merge. Does not hunt bugs,
  measure performance, or judge standards itself.
---

# Review (gsuper)

Read-only. No edit, no commit, no fix. One review, one `review.md`.

Do not offer a mode menu. Do not start a second review pass.

This skill is a router. It does not hunt bugs, measure performance, or judge spec/standards. Those skills already do that. Follow them as written. Do not paraphrase them. Do not edit them.

| Axis | Skill (shipped in this plugin, unchanged) |
|------|-------------------|
| **Bug + Performance** | [skills/verified-bug-hunt/SKILL.md](../verified-bug-hunt/SKILL.md) |
| **Spec + Standards** | [skills/code-review/SKILL.md](../code-review/SKILL.md) |

Read those two files and follow them. Spawn both in parallel. Neither waits on the other. Do not merge ranks. Do not add a finding either skill did not report.

Do not apply [bug-bar.md](references/bug-bar.md), [performance-bar.md](references/performance-bar.md), or [standards-bar.md](references/standards-bar.md). If either skill file is missing, stop that axis and say so. Do not fall back to those bars.

`diagnosing-bugs` is not this router. A bug that is already failing goes there, not into a second review pass.

## 0. Memory then diff

Run `memory.py find --ticket <id>` or `find --q <topic>` first. Empty → index miss; use the **plan** file on disk (legacy ticket spec only if no plan). Do not treat empty find as “no plan”.

**source-ladder:** you are not the reviewer. Spec rows that `code-review` reports already compare to the plan (`So sánh:` Done when → khớp | lệch | thiếu). Hunt rows compare to the command it ran. Do not drop a hunt finding because no `Done when` mentions it. Do not invent a finding.

## 0b. Pin one diff

Same diff for both skills.

```bash
git --no-pager status
# staged -> git --no-pager diff --staged
# unstaged -> git --no-pager diff
# clean tree -> git --no-pager diff main...HEAD
git --no-pager log --oneline -10
```

User named a ref → `git rev-parse` it, then `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`.

Empty diff → blocked. Call next: implement / build. Bad ref → stop. Do not spawn.

## 1. Plan path (hand to code-review only)

Order: user path → `.agent-workflow/plans/` + `scratch/<ticket>/` → legacy `.agent-workflow/specs/YYYY-MM-DD-<ticket>.md` if **no** plan → `.scratch/<ticket>/ac.md`.

Spec-docs under `specs/algorithm|srs|feature|architecture|system/` are not ticket AC.

None + user says none → tell `code-review` there is no spec. Do not invent AC. The hunt still runs.

Diff does not map to the plan → **drift**. Stop. Ask which phase. Do not spawn.

## 2. Spawn both

Give both the same diff command and commit list.

**verified-bug-hunt** — follow that skill. No extra bug rules from this file.

**code-review** — follow that skill. Pass the plan path as the spec argument (its step “a path the user passed”). That is the ticket AC. Do not add gsuper standards-bar on top.

## 3. Write

Prefer `.agent-workflow/scratch/<ticket>/review.md`, else `.scratch/<ticket>/review.md`.

Paste each report under its heading. `Kết luận cho bạn` only summarises what they returned: ship or not, what the user would see, what to decide. No new bug, no new smell.

```markdown
# Review — <ticket>
Diff: <staged | unstaged | main...HEAD | ref...HEAD>

## Kết luận cho bạn
<5–10 câu từ hai báo cáo. Không mở đầu bằng P0/file:line.>
So sánh: <hunt command output | Done when line> → khớp | lệch | thiếu

## Bugs
(paste verified-bug-hunt)

## Performance
(paste verified-bug-hunt)

## Spec
(paste code-review)

## Standards
(paste code-review)

## Decisions
P0: hunt High, or Spec missing/wrong
P1: hunt performance / standards judgement / user accept?
```

Call next:

- P0 open → implement (or gsuper-write-plan if AC itself is wrong)
- else → learn / done

Do not apply P0 yourself in this skill.
