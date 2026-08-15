---
name: implement
description: >
  Implement against approved spec/plan — TDD at seams (test→RED→frame→fill→GREEN),
  Ponytail, Python objects. Use after write-plan or /workflow implement.
---

# Implement (gsuper)

Self-contained. **No** `Read ~/.claude/skills` or Superpowers at runtime.

## Vendored cores

| Source | What we kept |
|--------|----------------|
| Matt `tdd` + `tests`/`mocking` | Seams, anti-patterns, mock at boundaries, vertical slices |
| Matt `implement` / phase `build` | Gate Done when, typecheck/tests often, full suite end, drift stop |
| Superpowers `test-driven-development` | Watch RED; no prod code before failing test |
| Superpowers `executing-plans` | Plan first; task steps; stop+ask when blocked |
| Superpowers `verification-before-completion` | Fresh verify evidence before “done” |

Dropped: Matt auto-commit; diagnosing-bugs full; worktrees / finishing-branch / subagent orchestration.

Detail: [references/tdd-loop.md](references/tdd-loop.md)

## 0. Gate

Spec with `Done when:` (`.agent-workflow/specs/` or `.scratch/<ticket>/`).  
No spec → **write-spec**. Fuzzy → **brainstorm**.

Plan present → read; gaps → ask. Do not guess.

**Symptom / confusion:** User pushes a local patch, wrong-layer fix, or “just make it work” while the problem/root is unclear (or contradicts repo facts) → **stop**. Remind + send to **brainstorm** ([symptom-gate](../brainstorm/references/symptom-gate.md)). Do not implement the ngọn fix first. Exception: user explicitly accepts a temporary workaround recorded in intent/spec.

## 1. While coding

- Spec + plan only. No scope fat.
- Rules: **ponytail**, **python-objects**, **testing-seams**, **pep8-python**, **small-diffs**
- Loop: [tdd-loop.md](references/tdd-loop.md) — **test → RED → frame → fill → GREEN**
- Soft ~500 LOC / task
- Typecheck / single test file often; full suite once at end
- Ask before: new dep, break public contract, rewrite vs expand-contract, expand AC

## 2. Each plan task

1. In progress
2. Seam for this slice (from spec) — confirmed
3. Write **one** failing test (sample API in the test)
4. **Run** → confirm RED (right reason)
5. Thin **frame** (stub / signatures) if needed
6. **Fill** only what GREEN needs
7. **Run** → GREEN
8. Plan verify command if any
9. Next task

Infra-only: smoke at real boundary. No fake seams.

## 3. Drift

Leaves spec → **stop**. Tell user. No silent adopt.

## 4. Blocked

Stop + ask: missing dep, RED never correct, verify flaky, instruction unclear.  
No implement on `main`/`master` unless user says so.

## 5. Done (evidence)

Before claiming task/ticket done:

1. Name the verify command (plan or tests for this slice)
2. **Run it now** (this turn)
3. Claim only with that output (exit 0 / pass count)

Every `Done when` has evidence.  
Call next: **review** (read-only). Fix P0 later back in this skill.

**After plan done** (all plan tasks verified): offer side track

> Personal skill concepts from this completed plan? → **learn-self**

(Diagrams already belonged at spec/plan — do not re-offer **learn-plan** unless they ask.)

No commit unless user asked.
