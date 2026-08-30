# Plan task shape (vendored)

**From Superpowers `writing-plans`:** bite-sized TDD steps, exact paths/commands, Interfaces consume/produce, no placeholders, self-review.  
**From Matt `to-tickets`:** vertical tracer slices; blocking edges; expand–contract for wide refactors.  
**gsuper:** soft ~500 LOC/task; path `.agent-workflow/plans/`; after save → ask learn; handoff → **gsuper-implement** (not SP subagents).

---

## Header (required)

```markdown
# <Feature> Implementation Plan

> For agentic workers: execute task-by-task via gsuper **gsuper-implement**. Steps use `- [ ]`.

**Goal:** …
**Architecture:** …
**Tech Stack:** …

## Global Constraints

- … (verbatim from spec: versions, naming, platform — one line each)
```

## Before tasks

1. **Scope** — if spec spans independent subsystems, prefer separate plans (or say so and split).
2. **File map** — list create/modify/test paths and one-line responsibility each. Lock decomposition here.
3. Prefer small focused files; follow existing layout; only plan a split if a file is already unwieldy **and** this work needs it.

## Task sizing

- Smallest unit with its **own** test cycle and reviewer gate.
- Fold setup/scaffold/docs into the task that needs them.
- Soft-cap **~<500 lines** intended diff — split if larger.
- Prefer **vertical** slices (demoable path) over horizontal layers.
- Give **Blocked by:** prior task ids, or `None`.
- Wide mechanical blast radius → **expand → migrate batches → contract**, not one mega vertical ticket.

## Task template

````markdown
### Task N: <name>

**Blocked by:** None | Task K, …

**Files:**
- Create: `exact/path.py`
- Modify: `exact/existing.py`
- Test: `tests/exact/test.py`

**Interfaces:**
- Consumes: … (signatures from earlier tasks)
- Produces: … (names/types later tasks rely on)

- [ ] **Step 1: Write the failing test**

```python
def test_behavior() -> None:
    assert port.do(x) == expected
```

- [ ] **Step 2: Run — expect RED**

Run: `pytest tests/…::test_behavior -v`  
Expected: FAIL (feature missing — not import typo)

- [ ] **Step 3: Minimal implementation**

```python
# only what GREEN needs
```

- [ ] **Step 4: Run — expect GREEN**

Run: same command  
Expected: PASS

- [ ] **Step 5: Commit** (only if user asked for commits in this session)

```bash
git add …
git commit -m "…"
```
````

Infra-only tasks: smoke command at real boundary instead of red-green.

## Plan failures (never ship)

- TBD / TODO / “implement later” / “add validation” without how
- “Write tests for the above” with no test code
- “Similar to Task N” — repeat the needed code
- Steps that say what without showing how (code steps need code)
- Types/names in later tasks that don’t match earlier **Produces**

## Self-review (before ask user)

1. **Spec coverage** — each Done when / requirement → a task (list gaps → fix)
2. **Placeholder scan** — fix red flags above
3. **Type consistency** — signatures match across tasks

## After save

1. Offer learn pack Markdown → **gsuper-learn-pack** (spec/plan stage)
2. Offer execution: inline (**gsuper-implement**) vs later — no SP `subagent-driven` / `executing-plans` required
3. Do **not** offer **gsuper-learn-material** until the plan work is done
