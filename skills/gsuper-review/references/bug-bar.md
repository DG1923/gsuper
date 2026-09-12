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

```text
## Issue: [title]
**File:** abs/path.py:12
**Severity:** Critical | High | Medium
**Problem:** …
**Evidence:** command + output, or fault line
**Suggested fix:** … (do not implement)
```

None: `No significant issues found in the reviewed changes.`
