---
name: gsuper-write-spec
description: Write locked gsuper spec (Purpose, Impacted, Seams, Sec/Perf line, Done when) to .agent-workflow/specs/. Use after gsuper-brainstorm approval.
---

# Write spec (gsuper)

Design **locked** (gsuper-brainstorm / intent approved). If the user jumped here with a fuzzy feature request → **gsuper-brainstorm** first. Fill [references/spec-template.md](references/spec-template.md). No Matt/to-spec at runtime.

## Output

```text
.agent-workflow/specs/YYYY-MM-DD-<topic>.md
```

Missing dir -> **gsuper-init-project**. Thin ticket: same fields, short. Multi-phase: one block per phase.

## Must have

- Purpose, Constraints, Do / Do not / Out of scope
- Impacted range
- Seams & Testing (or N/A — no app logic)
- Quality: **Security** + **Perf** always one line each (AC/budget **or** N/A / Non-goal)
- Done when (observable)
- Open questions if any

No file-path dump. No “code must be clean”. Ponytail: cut over-scope here.

## Self-review

Placeholders, contradictions, two-way ambiguity -> fix before ask user.

## Exit

User reviews file. Approved → optional ask:

> Mentor overview of this spec (HTML for you, not for implement)? → **gsuper-learn-plan** (before plan/implement)

Then → **gsuper-write-plan**.  
Do **not** offer **gsuper-learn-self** here.
