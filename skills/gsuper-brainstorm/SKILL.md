---
name: gsuper-brainstorm
description: >
  MUST use when the user wants a new feature, capability, behavior change, unclear
  product idea, or a symptom-only / confused “just fix it” ask — lock intent by grilling
  before gsuper-write-spec or any code. Maps to phase clarify.
---

# Brainstorm (gsuper) ≈ clarify

Lock **what the user wants** and the **chosen direction**. No product implementation.

**Entry (always):** User asks to build / add / change a product feature (or the goal is fuzzy) → run this skill first. Do **not** jump to gsuper-write-plan, implement, or code. Only skip when user explicitly says intent is already locked and points at an existing approved intent/spec.

**Also enter when:** prompt is **sửa ngọn** (symptom patch), user seems to **misunderstand the problem**, or chat/assumptions look **hallucinated** vs repo facts → [references/symptom-gate.md](references/symptom-gate.md). Remind + clarify; do not ship the patch yet.

Self-contained. **No** runtime Matt/Superpowers/`clarify` skill.

## Vendored cores

| Source | Kept |
|--------|------|
| Phase `clarify` | Intent lock; Decision needed on trade-offs; no silent pick; handoff to specify |
| Matt `grilling` | Design tree; **frontier rounds**; Q + recommended answer; facts≠decisions |
| Superpowers `brainstorming` | Hard gate; scope decompose; 2–3 approaches; section approval; “too simple” still needs short approval |
| Matt `prototype` | Optional throwaway **only** when one design Q needs a proof — then fold verdict back |

Detail: [references/grilling.md](references/grilling.md)

## What “clarify ý user” means here

You must learn, by asking (not guessing):

1. **Problem** — what hurts / who cares
2. **Success** — how we’ll know it worked (observable)
3. **Scope** — in vs out / deferred
4. **Direction** — chosen approach among alternatives

Until those are settled with the user → no spec, no plan, no implement.

## Symptom / confusion gate

If the ask is only a surface fix or the problem isn’t understood → follow [symptom-gate.md](references/symptom-gate.md): **pause, remind, grill**, then continue this checklist. Do not implement “just to unblock” unless they explicitly accept a temporary workaround.

## Hard gate

Do not implement, scaffold production code, or call **gsuper-implement** until design is approved (short design OK for tiny work — skip approval is not).

## Checklist

1. **Context** — enough repo/docs/commits to ask well (facts = you look up).
2. **Scope** — multiple independent subsystems → decompose first; gsuper-brainstorm one slice.
3. **Grill** — [grilling.md](references/grilling.md): frontier rounds until tree empty. **Wait for answers** each round — do not invent decisions.
4. **Strategic gates** — multiple viable directions, YAGNI cuts, large trade-offs → stop; put options + recommendation; do not pick silently.
5. **2–3 approaches** — trade-offs; recommend one with reasons; user picks / confirms.
6. **Present design** — scale to complexity; prefer **short code samples** for seams/APIs; approve section-by-section if large.
7. **Intent artifact** — write `.agent-workflow/scratch/<ticket>/intent.md` from [intent-template.md](references/intent-template.md) (ask ticket id once if missing). Tiny work: intent can be 5 lines.
8. **Hand off** — on **user** approval → **gsuper-write-spec** (not plan, not implement).

Optional visual: only when a Q is clearer shown than told; own message; decline → don’t re-offer.

Optional prototype: one design question needs throwaway proof → mark `PROTOTYPE`; capture verdict into intent; delete or leave out of main path.

## Design content (as needed)

Architecture, components, interfaces, data flow, errors, testing — **samples over abstract prose**.

```python
def enqueue(job: Job, *, idempotency_key: str) -> EnqueueResult:
    """Return accepted or duplicate; never raise on duplicate key."""
    ...
```

### Isolation

Each unit: one purpose, clear interface, independently testable.

### Existing codebases

Follow local patterns. Refactors only if they serve this goal.

## Principles

- Frontier grilling (not endless one-by-one when Qs are independent)
- Decisions = user; facts = agent
- YAGNI ruthlessly
- Alternatives before lock
- “Too simple for design” is an anti-pattern — still get short approval

## After approval

→ **gsuper-write-spec** → `.agent-workflow/specs/…`  
Do **not** jump to implement. Plan only after the written spec is approved.

Optional: uniquely named learn **pack** Markdown (read + upload ChatGPT/Claude)? → **gsuper-learn-pack** (stage `after-brainstorm`).
