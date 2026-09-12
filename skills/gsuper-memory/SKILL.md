---
name: gsuper-memory
description: >
  Project sqlite memory. Run memory.py find (or around) before dumping
  specs/plans/packs/SRS. Not implement AC. Not Codegraph.
---

# Memory (gsuper)

CLI (plugin):

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite find [--node] [--kind] [--ticket] [--q] [--old]
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite around <node>
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite note --kind decision|run|bug|verify --node <node> --body "..." --path ...
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite seed-xproject
```

Default `--db` is `<cwd>/.agent-workflow/memory.sqlite`. Schema is created on first run. The sqlite file is **local / gitignored**. Plugin code is what you commit.

`find` default hides `status=superseded` and `evidence=doc`. Then Codegraph one matching symbol. Do not ingest spec/pack bodies into SQL.
