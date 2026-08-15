# Symptom / confusion gate (gsuper)

Stop and clarify **before** any product fix when the ask looks like:

| Signal | Example |
|--------|---------|
| **Symptom-only (“sửa ngọn”)** | “Thêm if null”, “đổi message lỗi”, “hotfix cho qua CI” — no root cause or Done when |
| **User (or prior chat) confuses cause** | Blames the wrong layer; contradicts repo facts; “hallucinated” API/behavior |
| **Problem not understood** | Can’t state what hurts, who, or how we’ll know it’s fixed |
| **Patch fights the design** | Local hack that violates seams / intent already locked |

## What to do

1. **Stop** — no implement, no drive-by patch.
2. **Remind** (short, direct):

```markdown
## Pause: clarify before fixing

This looks like a **symptom fix** / **unclear problem**, not a locked root cause.

What I see: <1–2 sentences — symptom vs missing cause>
Risk if we patch now: <wrong layer / mask bug / fight design>

Call next: **gsuper-brainstorm** (or diagnose facts first, then gsuper-brainstorm)
```

3. **Facts first** — look up repo/logs/tests yourself; correct wrong assumptions gently with evidence.
4. **Grill** — problem → success → whether they want root fix vs explicit temporary workaround.
5. Only after user confirms direction → **gsuper-write-spec** (thin OK) → **gsuper-implement**.

## Explicit workaround exception

User says clearly: “temporary workaround only / accept debt / don’t dig root” → record that in intent (`Deferred` / `Constraints`), thin Done when, then implement the **named** workaround. Do not silently treat a vague “just fix it” as that exception.

## Not this gate

- Clear bug with reproducible evidence + obvious one-line fix at the right seam → can go thin **gsuper-write-spec** → **gsuper-implement**.
- Already approved spec/plan matching the ask → follow implement; use **Drift** if the new ask leaves the spec.
