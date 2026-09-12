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

After creating dirs, run (creates the sqlite + schema if missing; `ok` if already there):

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite init
```

Do not seed project-specific nodes. The project adds its own map with `memory.py node`.

Tell the user they can delete the `.agent-workflow/` ignore line to version artifacts (never commit `memory.sqlite`).

## Optional

Ask whether to also install GitHub templates via **gsuper-github-templates**.

## Idempotent

Do not overwrite existing non-empty specs/plans; only create missing dirs/files.
