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
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite find [--node] [--kind decision|note|spec|seam] [--ticket] [--q] [--old]
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite around <node>
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite note --kind decision|run|bug|verify --node <node> --body "..." --path ...
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite edge --from <slug> --to <slug> --rel <rel>
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite seam --node <slug> --symbol <Name> --path <file> --does "one line"
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite sync [--specs .agent-workflow/specs]
```

Default `--db` is `<cwd>/.agent-workflow/memory.sqlite`. **`init`** creates the file + schema if missing; second run is `ok` (still applies `CREATE IF NOT EXISTS`). The sqlite file is **local / gitignored**. Plugin code is what you commit.

Do not invent a project map. Add nodes with `node` when the project names its parts. `note` / `around` / `lock` need a node that already exists.

After the user **approves** a spec, `lock` writes the path + summary + must/must-not only. Do **not** ingest the spec body. Repeat `--must` / `--must-not` in pairs. A second `lock` on the same ticket supersedes the live artifact (or pass `--supersede <id>`).

`sync` is the safety net if `lock` was skipped: for each `YYYY-MM-DD-<ticket>.md` with no live row, create a node (slug=ticket) and a **pointer** lock (`must: spec pointer (sync)`). It does **not** ingest Done when / body and does **not** overwrite a live lock. Empty `find --ticket` means **index miss** → Read the spec on disk; do not treat it as “ticket does not exist”.

`--ticket` matches exact or prefix at `-`/`_` (`EL-6` → `EL-6-domain-…`, not `EL-60`). Unknown ticket → **zero rows** (not every note). `--kind` is `decision|note|spec|seam`, not node kinds.

`edge` / `seam` fill what `around` prints. Without `edge`, neighbors stay empty.

`find` default hides `status=superseded` and `evidence=doc`. Then Codegraph one matching symbol. Do not ingest spec/pack bodies into SQL.
