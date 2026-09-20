---
name: gsuper-implement
description: >
  Implement against approved plan (Done when) — TDD at seams (test→RED→frame→fill→GREEN),
  Ponytail, Python objects. Use after gsuper-write-plan or /gsuper-workflow implement.
  Legacy ticket spec is fallback only when no plan exists.
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

Plan with `Done when:` (`.agent-workflow/plans/` or `.scratch/<ticket>/`).  
No plan → **gsuper-write-plan**. Fuzzy → **gsuper-brainstorm**.  
**Dual-read:** if `find --ticket` has a live **plan**, that is AC. A live legacy **spec** (dated file in `specs/` root) is AC only when there is no plan. Spec-docs in `specs/algorithm|srs|feature|architecture|system/` are project docs — follow them when the plan points at them; they are not ticket Done when.

Do **not** treat a JSON conventions file as live law. `.agent-workflow/conventions.md` is **not project law** (stub / JSON migrate only). Approved spec-docs hold must/must-not; do not write the same bullets into conventions.md.

Before Glob of `.agent-workflow/` specs/plans/packs or `docs/system`, run **`memory.py find --ticket <id>`** (or `find --q <topic>` / `around <node>` if the ticket is unknown). See **source-ladder** (`rules/source-ladder.mdc`): **`So sánh:`** or **`Raise:`**; do not invent.

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite find --ticket <id>
```

Empty → index miss; Read the plan file on disk (then legacy spec if no plan). Pack is not AC. After a useful run/bug/verify, `memory.py note --kind run|bug|verify --node … --body … --path …`. After an expensive explore that yields a **new** one-line meaning and a Bên B (test / must / Done when) exists:

```text
memory.py seam --node <slug> --symbol <Name> --path <file> --does "one line"
```

Write tests and production code from the plan's Testing + slices. **Do not** expect function bodies in the plan.

**Symptom / confusion:** User pushes a local patch, wrong-layer fix, or “just make it work” while the problem/root is unclear (or contradicts repo facts) → **stop**. Remind + send to **gsuper-brainstorm** ([symptom-gate](../gsuper-brainstorm/references/symptom-gate.md)). Do not implement the ngọn fix first. Exception: user explicitly accepts a temporary workaround recorded in intent/plan.

## 1. While coding

- Plan only. Linked spec-docs if the plan names them. No scope fat.
- Rules: **ponytail**, **python-objects**, **testing-seams**, **pep8-python**, **small-diffs**, **source-ladder**
- Loop: [tdd-loop.md](references/tdd-loop.md) — **test → RED → frame → fill → GREEN**
- Soft ~500 LOC / task
- Typecheck / single test file often; full suite once at end
- Ask before: new dep, break public contract, rewrite vs expand-contract, expand AC

## 2. Each plan task

1. In progress
2. Seam for this slice (from plan Testing) — confirmed
3. Write **one** failing test (sample API in the test)
4. **Run** → confirm RED (right reason)
5. Thin **frame** (stub / signatures) if needed
6. **Fill** only what GREEN needs
7. **Run** → GREEN
8. Plan verify command if any
9. Next task

Infra-only: smoke at real boundary. No fake seams.

## 3. Drift

Leaves plan → **stop**. Tell user. No silent adopt.

## 4. Blocked

Stop + ask: missing dep, RED never correct, verify flaky, instruction unclear.  
No implement on `main`/`master` unless user says so.

## 5. Done (evidence)

Before claiming task/ticket done:

1. Name the verify command (plan or tests for this slice)
2. **Run it now** (this turn)
3. Claim only with that output (exit 0 / pass count)

Every `Done when` (on the **plan**) has evidence.  
Call next: **gsuper-review** (read-only). Fix P0 later back in this skill.

**After plan done** (all plan tasks verified):

> Learn pack + quiz Markdown? → **gsuper-learn-pack** (stage `after-implement`)

> Lesson + runnable sample from shipped behavior? → **gsuper-learn-material** (does not block review)

No commit unless user asked.
