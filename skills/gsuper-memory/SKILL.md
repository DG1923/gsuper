---
name: gsuper-memory
description: >
  Project sqlite memory. Run memory.py find (or around) before dumping
  plans/specs/packs/SRS. Ticket AC is plan. Spec is project docs. Not implement AC.
  Not Codegraph.
---

# Memory (gsuper)

CLI (plugin). Same commands on every project — no project-specific seed.

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite init
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite node --slug <slug> --kind part|layer|domain --title "..." [--blurb "..."]
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite lock --kind plan|spec [--ticket <id> | --id <id>] --node <node> --path <file.md> --summary "..." --must "..." --must-not "..."
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite find [--node] [--kind decision|note|spec|plan|seam] [--ticket] [--q] [--old]
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite around <node>
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite note --kind decision|run|bug|verify --node <node> --body "..." --path ...
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite edge --from <slug> --to <slug> --rel <rel>
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite seam --node <slug> --symbol <Name> --path <file> --does "one line"
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite sync [--specs .agent-workflow/specs] [--plans .agent-workflow/plans]
```

Default `--db` is `<cwd>/.agent-workflow/memory.sqlite`. **`init`** creates the file + schema if missing; second run is `ok` (still applies `CREATE IF NOT EXISTS`). The sqlite file is **local / gitignored**. Plugin code is what you commit.

Do not invent a project map. Add nodes with `node` when the project names its parts. `note` / `around` / `lock` need a node that already exists.

`lock` writes the path + summary + must/must-not only. Do **not** ingest the markdown body. `--kind plan` after the user approves a ticket plan. `--kind spec` after they approve a project doc (`--id` is the doc id, e.g. `captions`). Repeat `--must` / `--must-not` in pairs. A second `lock` on the same kind+id supersedes the live artifact.

`find --ticket` returns the live **plan** first, then a legacy ticket spec if both exist. Empty `find --ticket` means **index miss** → Read the plan (then dated spec) on disk; do not treat it as “ticket does not exist”.

`sync --specs` locks dated files at `specs/` root (legacy tickets) and `*.md` under `algorithm/`, `srs/`, `feature/`, `architecture/`, `system/`. Other subfolders → `skip-kind` (do not invent a kind). `sync --plans` locks dated `plans/YYYY-MM-DD-<ticket>.md`. Neither ingest bodies.

`--ticket` matches exact or prefix at `-`/`_` (`EL-6` → `EL-6-domain-…`, not `EL-60`). Unknown ticket → **zero rows**. `--kind` for find is `decision|note|spec|plan|seam`.

`edge` / `seam` fill what `around` prints. Without `edge`, neighbors stay empty.

`find` default hides `status=superseded` and `evidence=doc`. Then Codegraph one matching symbol. Do not ingest spec/plan/pack bodies into SQL.
