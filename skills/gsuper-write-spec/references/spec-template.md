# Spec template (locked)

```markdown
# <Topic> — Spec

**Date:** …
**Status:** Draft for review | Approved
**Ticket / parent:** #… (optional)

## Purpose
<One job — 1–3 sentences>

## Constraints
- <Hard limits>

## Do
- …

## Do not
- …

## Out of scope
- …

## Impacted range

| Touches | Does not touch |
|---------|----------------|
| …       | …              |

## Seams & Testing
**Seams under test (confirmed):**
- `<Name>` — observe `<behavior>` via `<how>`

**Out of test (intentional):**
- …

**Testing decisions:**
- External behavior only
- Modules this ticket: …
- Prior art: …

Infra-only / no app logic -> `Seams: N/A — no app logic`

## Quality

**Security:** <trust boundaries + AC> | N/A — no auth/secrets/untrusted input
**Perf:** <metric + how to measure> | Non-goal — no scale/latency claim

**Ponytail:** smallest behavior that proves Purpose; no speculative API.

## Done when
- [ ] …
- [ ] Security/Perf line satisfied (AC or explicit N/A / Non-goal)

## Open questions
1. …
```
