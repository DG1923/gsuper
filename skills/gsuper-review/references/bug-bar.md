# Bug bar (gsuper-review)

Hunt in the **diff**. Still omit style, naming, and “consider X”.

**No finding without evidence.** Evidence is either:

- a command you ran **this turn** plus its output, or
- the exact file:line that *is* the fault (e.g. `print` of `→` plus the traceback you just got)

“Looks wrong” / unsure → **omit**. Medium is allowed only if reproduced.

## Walk (skip a box → Bug step is not done)

On this diff, check:

1. Crash / encode / IO
2. Wrong filter, status, or default (stale row shown as live)
3. New CLI/API path with no test — run it once
4. State / order (ack before handle)
5. Secrets or path execution
6. Race / leaked resource if the hunk is concurrent

Wrong result, crash, or OOM → Bug (not Performance).

## Output

A reader who only has the idea / Flow must see **which step** broke and **why that is a bug** (expected I/O vs what happened). File:line alone is not enough.

```text
## Issue: [title]
**Step:** <Flow box: input → uses → output> | (no Flow in spec — name the user-visible step)
**Why a bug:** <plain language: that step should …; the diff does …; that breaks Purpose / Done when because …>
**File:** abs/path.py:12
**Severity:** Critical | High | Medium
**Problem:** <plain language — what the user would notice; not only a path>
**Evidence:** command + output, or fault line
**Suggested fix:** … (do not implement)
```

No **Step** / **Why a bug** → do not publish the finding (same as no evidence).

None: `No significant issues found in the reviewed changes.`
