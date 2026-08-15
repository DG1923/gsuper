# TDD loop (vendored — no runtime Matt/Superpowers)

**From Matt `tdd`:** seams, good test = public behavior, 3 anti-patterns, red→green, refactor ≠ loop.  
**From Superpowers `test-driven-development`:** must **watch RED** (fail for right reason); no production code before failing test.  
**From Superpowers `verification-before-completion`:** evidence before “done”.  
**From Matt `mocking.md`:** mock system boundaries only.

---

## Order (locked)

```text
1. Test — one behavior at a confirmed seam (API shape = sample in test)
2. RED  — run test; fail because feature missing (not typo)
3. Frame — thin stub / signatures / NotImplemented so test reaches the gap
4. Fill  — only code needed to pass
5. GREEN — run again; pass
6. Next slice — or light cleanup with tests still green (no new behavior)
```

Not: big frame first → tests after.  
Yes: test pulls frame; frame serves the red test.

## Good test

- Behavior through **public seam** (spec / user confirmed)
- Name = WHAT, not HOW
- Expected value = literal / Done when / worked example — not same formula as impl
- Survives internal refactor

## Anti-patterns (Matt)

- **Implementation-coupled** — mock own modules, private methods, DB peek past interface
- **Tautological** — expected recomputed like production
- **Horizontal** — all tests then all code → use **vertical** one test → min impl → repeat

## Mock (Matt)

Mock **system boundaries** only: external HTTP, sometimes DB/time/fs.  
Prefer fake **adapter** behind `Protocol`.  
Do not mock code you own inside the seam.

```python
# GOOD — assert through seam
def test_enqueue_rejects_duplicate_key(port: QueuePort) -> None:
    assert port.enqueue(job, idempotency_key="k").accepted is True
    assert port.enqueue(job, idempotency_key="k").accepted is False

# BAD — tautology
def test_total() -> None:
    items = [{"price": 10}, {"price": 5}]
    expected = sum(i["price"] for i in items)  # same as impl
    assert total(items) == expected
```

## Verify RED (Superpowers)

Mandatory. After writing the test, **run it** before filling production code.

- Fails → good (missing feature)
- Passes immediately → wrong test (testing existing behavior) → fix test
- Errors (import/typo) → fix harness until it **fails correctly**

Wrote production code first? Delete it. Restart from test. (Iron law — soft exception: infra/config/prototype with user OK.)

## Green

Minimum to pass. No extra options, no drive-by refactor, no “while we’re here”.

## Exceptions (ask user)

Throwaway prototype, generated files, compose/env-only — smoke command OK, skip red-green.
