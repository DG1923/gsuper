---
name: verified-bug-hunt
description: Self-contained bugs-and-performance review of a diff — find real issues by actually RUNNING the changed code against boundary/adversarial inputs and by profiling its hot paths, not by reading it. This is a standalone review pass, not a step that needs another skill before or after it: use it any time the user wants a diff/PR reviewed for bugs or performance, a deep bug hunt, a production-readiness pass, or says a prior review missed something — especially for code that touches external or configurable data (arrays, images, bytes, env-driven settings, network/adapter responses), async/concurrency code, or anything that runs per-request/per-item in a loop. It owns exactly two axes — correctness bugs and performance — verified by execution; it does not check spec-compliance, coding standards, or other non-functional conventions, so pair it with this repo's `code-review` skill (which owns those) when the user wants full coverage, but each runs completely on its own and neither depends on the other having run. A plain "review this diff/PR" with no axis specified should run both. Systematically catches what a reading-only review misses: dtype/shape bugs, config-boundary crashes, swallowed exceptions, exception-shape changes from concurrency primitives (e.g. asyncio.gather → TaskGroup, multi-failure `except*` re-merging), off-by-one at a guard's exact boundary, degenerate math that silently returns a plausible wrong value, bugs introduced by the fix commits themselves on a re-review, and plain inefficiency (redundant work, repeated calls that could be merged) that nobody happened to make a claim about. Every finding this skill reports must be backed by an actual command run and its actual observed output — never a speculative "this could fail" or "this could be slow."
---

# Verified Bug Hunt

`code-review` and `gsuper-review` in this repo compare the diff against documented standards and the spec — a reading exercise. This skill finds a different class of bug: the kind that only shows up when you actually execute the code with an input its author didn't picture. A validator that checks shape but not dtype, a `GRID=0` config crash, a `except: return None` with no log line, an `asyncio.TaskGroup` that silently turns a caught exception type into an uncatchable `ExceptionGroup` — none of these are visible from reading; all of them are one Python one-liner away from being *proven*.

The standing rule: **if you didn't run it and see the output, it isn't a finding.** "Likely fails on empty input" is a hypothesis, not a bug report. Run it, then report what actually happened.

The concrete examples in this file (dtype, `GRID=0`, `TaskGroup`, `np.percentile`, `cvtColor`) come from one past PR. They illustrate *shapes* of bugs — they are not the checklist. A review that only re-finds those will miss the next PR's bugs; derive candidates from the categories in step 3 applied to *this* diff.

## Division of labor with other review skills

This skill is complete on its own for what it covers: run it by itself whenever the ask is "are there bugs or performance problems in this diff" — it doesn't need `code-review` or `gsuper-review` to have run first, and it doesn't hand anything off to them.

The boundary is by axis, not by order:
- **This skill owns**: correctness bugs and performance, both proven by executing the code.
- **`code-review` owns**: spec-compliance (does the diff do what the issue/PR asked) and standards/non-functional conventions (naming, architecture, docs, everything this repo's `CLAUDE.md`/`docs/*.md` document) — a reading exercise against documented rules, not execution.

Neither is a subset or a prerequisite of the other. When the user wants full coverage of a diff, run both (in either order, or in parallel) and report their findings separately — don't merge a spec finding into this skill's report or vice versa. When the user only wants one axis, running just that skill is a complete review for what they asked, not a partial one.

## Process

### 1. Pin the diff

Same convention as `code-review`: get a fixed point (commit/branch/tag the user gives, or ask). Run `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`. If reviewing a GitHub PR, also fetch the PR body/description and any existing review comments (`gh pr view <n> --json body,comments,reviews`, `gh api repos/<owner>/<repo>/pulls/<n>/comments`) — you'll need them for step 7 (drift) and for re-review mode below.

**Re-review mode (a fix commit exists).** When the branch already had a review and later commits fix it, the fix commits are the highest-risk code in the PR: they were written fast, against a specific complaint, and nobody has attacked them yet. So:
- Review the fix commits on their own first: `git diff <last-reviewed-commit>..HEAD`. Don't let the full-branch diff dilute them.
- Every guard, `try/except`, validator, constraint, or exception-conversion the fix *added* is a target in its own right (step 2g) — attack the fix, don't just confirm the original complaint is gone.
- Confirming "the reported bug no longer reproduces" is necessary, not sufficient. The fix's own new boundary (the `N` in a new `x < N` guard, the new `except` clause) is where the next bug lives.

### 2. Enumerate targets

Walk the diff and pull out every changed function/method that does at least one of these — these are the shapes where boundary bugs hide:

- **(a) Accepts external or configurable data**: array/image input, decoded bytes, a settings/env value, a response from an adapter or network call.
- **(b) Parses or validates**: any `field_validator`, shape/type check, `isinstance`, decode step.
- **(c) Has a fallback path**: `try/except`, a function returning `None`/a default on failure, an `or` with a fallback value.
- **(d) Combines multiple fields that travel together**: two attributes that are supposed to stay consistent with each other but aren't enforced as one unit (e.g. a count and a list whose length should match it).
- **(e) Makes a concurrency or performance claim**: `asyncio.gather`/`TaskGroup`/`to_thread`, a docstring or PR description claiming something runs in parallel, off the event loop, or faster than before.
- **(f) Sits on a hot path**: runs per-request, per-image/per-item, or inside a loop — regardless of whether anyone claimed anything about its speed. Production code doesn't need a performance claim attached to it to be worth profiling; it needs to be on a path that actually runs often. Look for: repeated calls to the same expensive function that could be merged into one (two `np.percentile` calls instead of one with a list), work done at full resolution/size that's about to be downsized anyway, the same expensive input transformed more than once on independent code paths, or a blocking call sitting directly on an event loop instead of offloaded.
- **(g) Was added by a fix commit**: a new guard (`if x < N: raise`), a new `except`/`except*`, a new validator or `Field(...)` constraint, a new exception wrap/unwrap. Fix code has its own boundaries and its own error paths — treat each as a fresh target, independent of the complaint it answered.

Skip pure plumbing (re-exports, `__init__.py`, straightforward dataclass fields with no logic). You want the handful of functions where a bad input actually changes behavior, or where real request volume actually passes through.

### 3. Brainstorm adversarial inputs per target

For each target, work through the categories below and note concrete candidate inputs — don't run anything yet, just build the hit list. Not every category applies to every target; use judgement.

| Category | What to try |
|---|---|
| Type boundary | The "obviously wrong but technically accepted" type: `float32`/`uint16` where `uint8` is assumed, a `str` where a number is expected, `None` where a value is required but the type hint says `Optional` loosely |
| Shape/size boundary | Degenerate shapes: a 1-pixel-wide image, an empty array/list, a single-element collection where the code assumes ≥2, a huge value that overflows an assumption |
| At every guard / threshold | For each `x < N`, `x <= N`, `len(...) >= N` in the target: try exactly `N-1`, `N`, `N+1`. Off-by-one bugs sit *on* the boundary, not far below it — testing `1` against a `< 2` guard proves nothing about `2`. Then ask which *real entry-point input* produces that intermediate value (e.g. which source image size becomes a 2px frame after resize + crop) and run that input through the public entry point, not only the helper |
| Degenerate math — silent wrong value | Windows, normalizations, divisors, and ratios can degenerate without crashing: a window of all zeros, a `max()` of 0, a variance of 0, an `if total <= 0: return 0.0` fallback. At the boundary sizes above, check the *returned value* is still meaningful (e.g. a sharp/noisy input still scores > 0), not just that nothing raised. A plausible-looking `0.0` that flips a verdict is worse than a crash |
| Config boundary | `0`, negative, and very large values for every numeric setting touched by the diff — especially anything used as a divisor, a loop bound, or a `np.array_split`/grid argument |
| Cross-field consistency | Two fields set independently (e.g. by different call sites, or one with a default) that some downstream function assumes move together |
| Error-path / swallowed exceptions | Every bare or broad `except` — what happens to the caller when the wrapped call actually raises? Is it logged? Does the fallback value quietly change output semantics? |
| Concurrency-primitive exception shape | If the diff uses `asyncio.gather`, `TaskGroup`, `to_thread`, or similar: what exception type does a caller actually receive when an inner call raises? Does that match what upstream `except SomeType` clauses expect? Try **one** failure *and* **several at once with different types** (a domain error + an unexpected one) — `except*` semantics differ: if two `except*` clauses each raise, Python re-merges them into a new `ExceptionGroup`. Also try nested groups, `KeyboardInterrupt`/`CancelledError` (should pass through untouched), and cancellation from outside. Racing real threads is nondeterministic — to hit multi-failure deterministically, have a fake raise a pre-built `ExceptionGroup([...])` from inside one task, then separately stress real concurrent failures in a loop (e.g. 200 runs, `threading.Barrier`) and report the outcome distribution |

Cross-check against sibling code while you do this: grep for analogous existing classes/settings/adapters elsewhere in the repo (e.g. `rg 'Field\(gt=0\)'` if the diff adds an unconstrained numeric setting next to others that use it, `rg 'logger.warning'` in sibling adapters if the diff swallows an exception silently). A pattern the rest of the repo follows consistently, that this diff's new code alone skips, is a strong signal — cite the sibling file+line as evidence, not just "convention."

### 4. Run it — don't guess

For each candidate from step 3, write a minimal script that imports and calls the *real* target code with that input, and actually execute it:

```bash
cd <service-dir> && uv run python -c "
from extractor_onprem.domain.card_image_quality.models import CardImageQualityInput
import numpy as np
img = np.full((200, 200, 3), 200, np.float32)  # wrong dtype
print(CardImageQualityInput(image=img))
"
```

Rules for this step:
- Never edit real repo files to do this — a throwaway `-c` script or a file under your scratchpad directory only. Never run git commands that mutate state (`checkout`, `reset`, `stash`, `commit`, `rebase`) during this process — read and execute only.
- Record the *exact* command and the *exact* output or traceback. If it didn't crash and produced a wrong-looking value instead (the more dangerous case — a silent bad verdict, not a crash), record the actual value and, if feasible, the same input run through the "correct" dtype/shape for comparison.
- If a candidate input turns out fine, that's useful too — note it under "checked, not an issue" (step 9) rather than discarding it. A reviewer reading your report should be able to tell what you ruled out, not just what you found.
- In re-review mode, also run each confirmed candidate against the **pre-fix** code to show the fix (or its test) actually changes the outcome — without mutating the repo: `git show <commit>:<path> > <scratchpad>/old_x.py`, then load it with `types.ModuleType` + `exec`, setting `__package__` and registering it in `sys.modules` so relative imports and `@dataclass` work. A test that passes on both old and new code isn't guarding anything.
- If executing requires infra you don't have (e.g. a live Triton server), use the same fakes/mocks the repo's own tests use for that dependency — check `tests/` for an existing fake first rather than inventing a new one.

### 5. Benchmark — claims (2e) and hot paths (2f) alike

**If a target makes a claim** (step 2e), don't accept it from the docstring or PR description — measure it. **If a target just sits on a hot path** (step 2f), profile it anyway even though nobody claimed anything: production-quality review means finding the redundant `cvtColor` call or the two `np.percentile` calls that could be one, not just checking that stated claims are true.

```python
import time
N = 50
start = time.perf_counter()
for _ in range(N):
    the_function(*args)
print((time.perf_counter() - start) / N * 1000, "ms")
```

For a hot-path target, don't stop at timing the code as it stands — ask "does this do anything twice, at a bigger size than it needs to, or synchronously when it could be offloaded?" and time a rewritten version against the original. If you propose a change, verify it doesn't alter output: `np.array_equal(before, after)` or the equivalent equality check for the data type involved. Report real numbers (ms, with N runs), not "should be faster" — and if you looked at a hot path and genuinely found nothing worth changing, say so under "checked, not an issue" rather than skipping it silently, so the reader knows it was actually profiled.

### 6. Sibling-code consistency pass

For every finding candidate so far that looks like a missing constraint/validation/log line, explicitly grep 1-2 sibling modules in the same domain/layer to confirm whether this is a repo-wide gap (less severe, maybe out of scope) or a local regression against an established local pattern (worth flagging directly, cite the sibling file+line).

### 7. Commit-vs-description drift pass

Diff the latest commit's actual code against what the PR description / issue / docstring *claims* it does. Concurrency and error-handling claims drift the most (e.g. a later commit swaps `gather` for `TaskGroup` but the description still says `gather`). Flag any mismatch you find — it's often exactly where a real bug hides, since the author's mental model and the code diverged.

### 8. Only keep confirmed findings

Drop anything from your working notes that step 4 didn't actually execute and observe. A finding that survives to the report must have a reproducible command + real output attached.

### 9. Rate every finding: Priority × Complexity

Before writing the report, rate each surviving finding on two independent axes so a reader can triage without re-deriving your reasoning:

**Priority** — how bad is it in production if left unfixed:
- **High** — wrong output produced silently (no crash, no log), a crash on input real traffic will realistically hit, or error handling/observability broken so a real failure goes unnoticed (e.g. exception swallowed with no log, exception type changed so upstream can't catch it).
- **Medium** — crashes, but only on input that's rare/edge (not impossible, not everyday), or degrades a non-critical path with a recoverable failure mode.
- **Low** — no behavior change, no crash risk — pure inefficiency on a hot path, or a robustness gap with no realistic trigger yet (e.g. a config constraint missing but nothing currently sets that value).

**Complexity** — how much the fix touches:
- **Low** — one line to a few lines, single file, no contract/API change (add a `Field(gt=0)`, add a log line, swap one function call for another with identical behavior).
- **Medium** — contained to one function/class but changes its shape (add a validator, restructure a fallback path, reorder two operations) — needs a test update but not a design decision.
- **High** — crosses a file/layer boundary, changes a public contract (function signature, exception type callers must handle, ownership of a dependency between two classes) — needs a design decision, not just an edit.

Rate from what you actually observed in step 4/5 — if you're not sure an input is realistic in production, call it Medium, not High; don't inflate priority to make a finding look more important than the evidence supports.

### 10. Report format

Group findings by Priority (High → Medium → Low), bugs before performance within each group. Every row's evidence must be something you ran, not something you reasoned about.

```markdown
## Bugs

### High priority

| # | Location | Issue | Verified evidence | Fix direction | Complexity |
|---|---|---|---|---|---|
| 1 | `models.py:274` | No dtype validation — float32 in [0,1] silently flips the `dark` verdict, no exception | Ran `CardImageQualityInput` with `uint8` (p50=182.5, dark=False) vs `float32` same image (p50=0.717, dark=True), no exception raised either way | Add `value.dtype == np.uint8` to `_check_bgr_shape` | Low |

### Medium priority

| # | Location | Issue | Verified evidence | Fix direction | Complexity |
|---|---|---|---|---|---|
| 3 | `preprocessing.py:72` | 5% border crop on a 1px-wide image produces an empty frame | `np.full((1,400,3), 128, np.uint8)` → `normalize_for_analysis` returns shape `(0, 288, 3)` → `cv2.error` downstream, not a domain error | Guard minimum dimension pre-crop, raise a domain error | Medium |

### Low priority

(same shape — omit if empty)

## Performance

### High priority

| Location | Before | After | Complexity | Note |
|---|---|---|---|---|
| `text_signal_adapter.py:53` | 15.9ms (full-res `cvtColor` then resize) | 2.4ms (resize then `cvtColor`) | Low | `np.array_equal` confirms bit-identical output; runs on the event loop today, so this latency is paid synchronously per request |

### Medium / Low priority

(same shape)

## Checked, not an issue

- `service.py` fan-out via 3x `to_thread` — measured 5.6ms concurrent vs 9.8ms run sequentially by hand; parallelism has a real payoff here, no change needed.
```

Omit an empty priority group or section entirely rather than leaving a heading with nothing under it — don't pad with speculative rows just to fill every bucket.
