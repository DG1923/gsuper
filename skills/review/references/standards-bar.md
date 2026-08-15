# Standards bar (gsuper)

Separate from Defect. Do not use Copilot Issue format here.

Only report if all three hold:

1. In the **diff** (no whole-repo audit)
2. Cite **rule + rung** (`ponytail`, `python-objects`, `testing-seams`, `pep8-python`, `small-diffs`)
3. **Sure** — no "consider X"

Skip: ruff/black/isort already catch · naming/format · nicer-to-have · spec Out of scope

No Fowler smell list.

```text
## Standard: [rung / rule]
**File:** abs/path.py:12
**Rule:** python-objects #1 | ponytail #5 | testing-seams
**Problem:** …
**Evidence:** hunk / call
**Suggested:** … (do not implement)
```

None: `No significant standards findings.`
