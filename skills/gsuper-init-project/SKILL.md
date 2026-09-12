---
name: gsuper-init-project
description: Initialize .agent-workflow/ storage and gitignore for gsuper. Use on /gsuper-workflow-init or when artifact paths are missing.
---

# Init project (gsuper)

## Create

```text
.agent-workflow/
  README.md
  conventions.md
  specs/
  plans/
  scratch/
  learning/
  learn/
    .gitignore
```

Copy text from plugin `templates/agent-workflow/` when present, including `learn/` and root `conventions.md`.

`conventions.md` is user-owned project conventions. Create it if missing (from the template). Do not overwrite a non-empty `conventions.md`. Do not create a JSON conventions store.

Do not scan the repo.

## Gitignore

Append if missing:

```gitignore
# gsuper workflow artifacts (remove this line to commit specs/plans)
.agent-workflow/
.agent-workflow/memory.sqlite
```

`memory.sqlite` stays gitignored even if the rest of `.agent-workflow/` is committed.

On **new or existing** projects, run (safe upgrade — does not drop sqlite rows or overwrite specs/plans):

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite init
```

`init` creates schema if missing, writes `conventions.md` if missing, and **migrates** leftover `learn/invariants.json` into `conventions.md` (appends missing `## id` only). It deletes that JSON only after every rule id is in the md. Bad JSON → exit 2; files stay.

Do not seed project-specific nodes. The project adds its own map with `memory.py node`.

Tell the user they can delete the `.agent-workflow/` ignore line to version artifacts (never commit `memory.sqlite`).

## Optional

Ask whether to also install GitHub templates via **gsuper-github-templates**.

## Idempotent

Do not overwrite existing non-empty specs/plans. Re-run `memory.py init` on old trees to upgrade layout. Do not replace a non-empty `conventions.md` body (migrate only appends missing rules).
