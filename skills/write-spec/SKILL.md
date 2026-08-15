---
name: write-spec
description: Write locked gsuper spec (Purpose, Impacted, Seams, Sec/Perf line, Done when) to .agent-workflow/specs/. Use after brainstorm approval.
---

# Write spec (gsuper)

Design **locked** (brainstorm / intent approved). If the user jumped here with a fuzzy feature request → **brainstorm** first. Fill [references/spec-template.md](references/spec-template.md). No Matt/to-spec at runtime.

## Output

```text
.agent-workflow/specs/YYYY-MM-DD-<topic>.md
```

Missing dir -> **init-project**. Thin ticket: same fields, short. Multi-phase: one block per phase.

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

> Diagram walkthrough of this spec? → **learn-plan** (before plan/implement)

Then → **write-plan**.  
Do **not** offer **learn-self** here.
