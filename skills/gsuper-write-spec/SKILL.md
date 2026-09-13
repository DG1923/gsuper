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
- **Flow** (mermaid + input / uses / output table) — same chart as brainstorm Teach; **plain language** (not only file/API names)
- Seams & Testing (or N/A — no app logic)
- Quality: **Security** + **Perf** always one line each (AC/budget **or** N/A / Non-goal)
- Done when (observable)
- Open questions if any

No file-path dump. No “code must be clean”. Ponytail: cut over-scope here.

## Self-review

Placeholders, contradictions, two-way ambiguity, missing Flow, jargon without a gloss, or grill-before-teach leftover → fix before ask user.

## Exit

User reviews file. Approved → optional ask:

> Unique learn pack Markdown (read + upload ChatGPT/Claude)? → **gsuper-learn-pack** (stage `after-spec`)

After the user **approves** the spec: do **not** append a JSON conventions store. Project conventions live in `.agent-workflow/conventions.md` (workflow root, not `learn/`). If that file should change, propose the exact bullets and **wait for user approval** before editing it.

If `skills/gsuper-memory/scripts/memory.py` exists, **lock the approved spec in the same turn** (path + summary + must/must-not only — do **not** ingest the markdown body). Same ticket a second time supersedes the live artifact. If `lock` cannot run (unknown node), `node` first, or `sync --specs .agent-workflow/specs` then `lock` to replace the sync pointer with real must/must-not:

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite lock --ticket <id> --node <node> --path .agent-workflow/specs/<file>.md --summary "..." --must "..." --must-not "..."
```

Then → **gsuper-write-plan**.  
Do **not** offer **gsuper-learn-material** here.
