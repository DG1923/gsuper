# Plan task shape (gsuper)

Ticket AC lives here. User **approves** this file; agent **implements** from it.  
Each heading: a few plain-language sentences (user), then a table or list (agent).

**Not** a pre-written program: no test function bodies, no impl bodies, no pytest -v scripts.

---

## Header (required)

```markdown
# <Feature> — Plan

**Date:** …
**Status:** Draft for review | Approved
**Ticket / parent:** …

## Purpose
<One job — 1–3 sentences, words the user already used>

## Constraints
- <Hard limits>

## Do
- …

## Do not
- …

## Out of scope
- …
```

## Impacted range

Main files that change — not a dump of the repo.

| Touches | Does not touch |
|---------|----------------|
| … | … |

## Flow

**Chuyện gì xảy ra** (2–4 câu, lời user) — học viên / hệ thống làm gì, ra cái gì — **trước** mermaid. Chat and files: always a ` ```mermaid ` fence.

User-visible steps. Mermaid **and** I/O table (one-step ticket: table only is OK). Table columns in **everyday words** (what goes in, what comes out), not only file/API names.

```mermaid
flowchart LR
  a[A] --> b[B]
```

| Step | Input | Uses | Output |
|------|--------|------|--------|
| A | … | … | … |
| B | output of A | … | … |

## Implementation

Numbered slices so the user can follow the order. Each slice: **one sentence of what changes**, then files, **Blocked by**.

1. <việc gì, bằng lời thường> — `path/a.py`, `path/b.py` — Blocked by: None
2. …

Soft-cap **~<500 lines** intended diff per slice. Vertical slices over horizontal layers. Wide refactor → expand → migrate → contract.

## Testing

How we will prove each slice — **not** the test source.

- TDD new seam: `<Name>` → `tests/exact/test.py` (behavior in one line)
- Update existing: `tests/old.py` — what to change (imports / assertion); what stays (HTTP URL, …)

Infra-only: name the smoke command at the real boundary.

## Quality

**Security:** <trust + AC> | N/A  
**Perf:** <metric> | Non-goal  

**Ponytail:** smallest behavior that proves Purpose.

## Done when

Observable checkboxes. This is implement AC.

- [ ] …
- [ ] Security/Perf line satisfied (AC or N/A / Non-goal)

## Open questions

1. …

---

## Plan failures (never ship)

- Test or impl **function bodies** in the plan
- Copy-paste pytest commands as the plan's main content
- TBD / “implement later” / “add tests” with no seam/file
- “Similar to slice N” without repeating the files
- File-path dump of the whole tree
- Gold-plating the intent did not ask for

## Self-review (before ask user)

1. User can read Purpose + chuyện gì xảy ra + Flow + Implementation **without** opening the repo
2. Agent can pick files + TDD vs update-test from Testing + slices
3. Each Done when maps to a slice
4. No code bodies
5. I/O table is understandable without knowing internal function names

## After save

1. User approves this file
2. `memory.py lock --kind plan --ticket <id> …` (path + summary + must/must-not; no body ingest)
3. Offer learn pack Markdown → **gsuper-learn-pack**
4. Offer **gsuper-implement**
5. Do **not** offer **gsuper-learn-material** until the plan work is done
