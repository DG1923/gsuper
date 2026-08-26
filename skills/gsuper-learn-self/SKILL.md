---
name: gsuper-learn-self
description: >
  Personal skill upgrade AFTER a plan is fully done (implemented + verified). Concept
  cards for YOU. Not the learn pack (gsuper-learn-plan). Use after implement done or /gsuper-workflow-learn-self.
---

# Learn self (gsuper) — personal skill track

**Not** in the ship chain. **Not** `gsuper-learn-plan` (Markdown pack). **Not** phase `/learn` (repo outcomes).

Purpose: after a **plan is done** (all tasks implemented + evidence), extract concepts so **you** level up from what you just shipped.

## When

- After **gsuper-implement** claims the plan/ticket done (evidence in hand) — offer; user may decline
- Optionally after **review** if they deferred
- Or `/gsuper-workflow-learn-self` with a completed plan
- Input: plan path (+ what actually landed), or latest under `.agent-workflow/plans/`

**Do not** offer this right after `gsuper-write-plan` — that stage is for **gsuper-learn-plan** pack Markdown.

Do **not** start more product work here. Do **not** edit repo standards unless user promotes a note to ADR.

## Process

1. Read the finished plan (+ spec; skim review notes if any).
2. Prefer concepts you **touched while building**, not abstract plan prose alone.
3. Pick **2–4** cards (see [references/concept-card.md](references/concept-card.md)):
   - Pattern / decision the work hinged on
   - Something new or easy to fake-know
   - One trap you hit or avoided
4. Save:

```text
.agent-workflow/learning/YYYY-MM-DD-<plan-slug>.md
```

5. Teach lightly: one card (or pick-one); **explain-back** each.
6. Stop when done. Next ticket → gsuper-brainstorm / clarify as usual.

## Rules

- Short > essay. No full Matt `teach` unless a teaching workspace.
- Ground in this plan’s Task N / real paths — not generic blog.
- Primary facts from repo/docs when claiming tools/APIs.

## Vs other learns

| Skill | Stage | For |
|-------|--------|-----|
| `gsuper-learn-plan` | Spec / plan **before** implement | Understand to ship (human overview HTML) |
| `gsuper-learn-self` | **After** plan done | Upgrade **you** (concept cards) |
| phase `/learn` | Ticket close | Repo Outcome / ADR |
