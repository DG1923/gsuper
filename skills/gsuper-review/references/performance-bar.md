# Performance leak bar (gsuper-review)

Code in the **diff** only. Not agent token use. Not “could be faster”.

**No Bound → omit.** Each finding needs Now / Better / Bound.

## Leak types

| Leak | Now → Better | Bound |
|------|----------------|-------|
| Wasted work on a path that runs | compute then discard | this function runs when … |
| Serial await/IO, no data dependency | `gather` / parallel | loop or ≥ 3 sibling calls |
| Per-item instead of batch | one `IN` / bulk | N items |

Never-run dead code is **not** this axis (Standards / ponytail).

Correct-but-slow → Performance only. Crash / OOM / wrong result → Bug only. Do not copy a finding into both.

## Output

```text
## Perf: [title]
**File:** abs/path.py:88
**Now:** for q in queues: await consume(q)
**Better:** gather — results are independent
**Bound:** len(queues) ≥ 3
```

None: `No performance leaks found in the diff.`
