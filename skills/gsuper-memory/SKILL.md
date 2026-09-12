---
name: gsuper-memory
description: >
  Project sqlite memory. Run memory.py find (or around) before dumping
  specs/plans/packs/SRS. Not implement AC. Not Codegraph.
---

# Memory (gsuper)

CLI (plugin). Same commands on every project — no project-specific seed.

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite init
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite node --slug <slug> --kind part|layer|domain --title "..." [--blurb "..."]
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite lock --ticket <id> --node <node> --path <spec.md> --summary "..." --must "..." --must-not "..."
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite find [--node] [--kind] [--ticket] [--q] [--old]
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite around <node>
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite note --kind decision|run|bug|verify --node <node> --body "..." --path ...
```

Default `--db` is `<cwd>/.agent-workflow/memory.sqlite`. **`init`** creates the file + schema if missing; second run is `ok` (still applies `CREATE IF NOT EXISTS`). The sqlite file is **local / gitignored**. Plugin code is what you commit.

Do not invent a project map. Add nodes with `node` when the project names its parts. `note` / `around` / `lock` need a node that already exists.

After the user **approves** a spec, `lock` writes the path + summary + must/must-not only. Do **not** ingest the spec body. Repeat `--must` / `--must-not` in pairs. A second `lock` on the same ticket supersedes the live artifact (or pass `--supersede <id>`).

`find` default hides `status=superseded` and `evidence=doc`. Then Codegraph one matching symbol. Do not ingest spec/pack bodies into SQL.
