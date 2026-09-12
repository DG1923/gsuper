---
name: gsuper-init-project
description: Initialize .agent-workflow/ storage and gitignore for gsuper. Use on /gsuper-workflow-init or when artifact paths are missing.
---

# Init project (gsuper)

## Create

```text
.agent-workflow/
  README.md
  specs/
  plans/
  scratch/
  learning/
  learn/
    invariants.json
    .gitignore
```

Copy text from plugin `templates/agent-workflow/` when present, including `learn/`.

Each invariants rule (appended later, after a spec is approved) is `{ "id", "must", "must_not", "spec" }`. Init leaves `"rules": []`. Do not overwrite a non-empty `invariants.json`.

Do not scan the repo.

## Gitignore

Append if missing:

```gitignore
# gsuper workflow artifacts (remove this line to commit specs/plans)
.agent-workflow/
.agent-workflow/memory.sqlite
```

`memory.sqlite` stays gitignored even if the rest of `.agent-workflow/` is committed. First `memory.py find` creates the schema. Optional trial: `memory.py seed-xproject`.

Tell the user they can delete the `.agent-workflow/` ignore line to version artifacts (never commit `memory.sqlite`).

## Optional

Ask whether to also install GitHub templates via **gsuper-github-templates**.

## Idempotent

Do not overwrite existing non-empty specs/plans; only create missing dirs/files.
