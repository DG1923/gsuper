---
name: gsuper-brainstorm
description: >
  MUST use when the user wants a new feature, capability, behavior change, unclear
  product idea, or a symptom-only / confused “just fix it” ask — lock intent by grilling
  before gsuper-write-plan or any code. Maps to phase clarify. Spec-docs are a
  separate ask (algorithm / SRS / architecture).
---

# Brainstorm (gsuper) ≈ clarify

Lock **what the user wants** and the **chosen direction**. No product implementation.

**Entry (always):** User asks to build / add / change a product feature (or the goal is fuzzy) → run this skill first. Do **not** jump to gsuper-write-plan, implement, or code. Only skip when user explicitly says intent is already locked and points at an existing approved intent/spec.

**Also enter when:** prompt is **sửa ngọn** (symptom patch), user seems to **misunderstand the problem**, or chat/assumptions look **hallucinated** vs repo facts → [references/symptom-gate.md](references/symptom-gate.md). Remind + clarify; do not ship the patch yet.

Self-contained. **No** runtime Matt/Superpowers/`clarify` skill.

## Vendored cores

| Source | Kept |
|--------|------|
| Phase `clarify` | Intent lock; Decision needed on trade-offs; no silent pick; handoff to plan |
| Matt `grilling` | Design tree; **frontier rounds**; Q + recommended answer; facts≠decisions |
| Superpowers `brainstorming` | Hard gate; scope decompose; 2–3 approaches; section approval; “too simple” still needs short approval |
| Matt `prototype` | Optional throwaway **only** when one design Q needs a proof — then fold verdict back |

Detail: [references/grilling.md](references/grilling.md)

## What “clarify ý user” means here

**Teach first, then ask.** Do not open a frontier round until the user has seen how it works now and what extra steps their idea would add.

Then lock, by asking (not guessing):

1. **Problem** — what hurts / who cares
2. **Success** — how we’ll know it worked (observable)
3. **Scope** — in vs out / deferred
4. **Direction** — chosen approach among alternatives

Until those are settled with the user → no spec, no plan, no implement.

## Symptom / confusion gate

If the ask is only a surface fix or the problem isn’t understood → follow [symptom-gate.md](references/symptom-gate.md): **pause, remind, Teach + Flow, then grill**. Do not implement “just to unblock” unless they explicitly accept a temporary workaround.

## Hard gate

Do not implement, scaffold production code, or call **gsuper-implement** until design is approved (short design OK for tiny work — skip approval is not).

## Checklist

1. **Context** — enough repo/docs/commits to ask well (facts = you look up). Run `memory.py find --q <topic>` (or `around <node>`). Empty → index miss; Read `.agent-workflow/plans/` and linked `.agent-workflow/specs/` on disk. Do not assume the ticket was never locked. **Tell the user those facts** — do not keep the mechanism only in your head. **source-ladder:** each technical claim **`So sánh:`** (test / must / Done when / `seam.does`) or **`Raise:`**. Do not invent.
2. **Scope** — multiple independent subsystems → decompose first; gsuper-brainstorm one slice.
3. **Teach** — current mechanism; map the user’s idea onto it; **Flow** (mermaid in a ` ```mermaid ` fence in **chat** and files + table: step / input / uses / output). Never a bare `flowchart` without that fence. User-visible steps only. Extra steps vs their sentence **must** be on the chart. **Plain language** (words the user already used; one short gloss if you keep a term). Do **not** grill yet.
4. **Grill** — [grilling.md](references/grilling.md): frontier rounds until tree empty. Each Q: Why + If yes, extra steps. **Wait for answers** each round — do not invent decisions.
5. **Strategic gates** — multiple viable directions, YAGNI cuts, large trade-offs → stop; put options + recommendation; do not pick silently.
6. **2–3 approaches** — trade-offs; recommend one with reasons; user picks / confirms. Update Flow if the pick adds or drops steps.
7. **Present design** — Flow already shown; adjust if answers changed. Prefer **short code samples** for seams/APIs; approve section-by-section if large.
8. **Intent artifact** — write `.agent-workflow/scratch/<ticket>/intent.md` from [intent-template.md](references/intent-template.md) (ask ticket id once if missing). Tiny work: intent can be 5 lines.
9. **Hand off** — on **user** approval → **gsuper-write-plan** (not implement). Plan must reuse the same Flow. **gsuper-write-spec** only if the user asked for algorithm / SRS / feature / architecture / system docs.

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

→ **gsuper-write-plan** → `.agent-workflow/plans/…`  
Do **not** jump to implement.

User asked for SRS / algorithm / architecture / large-feature docs → **gsuper-write-spec** (can run beside the ticket, not instead of the plan).

Optional: uniquely named learn **pack** Markdown (read + upload ChatGPT/Claude)? → **gsuper-learn-pack** (stage `after-brainstorm`).
