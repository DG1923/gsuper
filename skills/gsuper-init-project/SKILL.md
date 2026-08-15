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
```

Copy text from plugin `templates/agent-workflow/` when present.

## Gitignore

Append if missing:

```gitignore
# gsuper workflow artifacts (remove this line to commit specs/plans)
.agent-workflow/
```

Tell the user they can delete that ignore line to version artifacts.

## Optional

Ask whether to also install GitHub templates via **gsuper-github-templates**.

## Idempotent

Do not overwrite existing non-empty specs/plans; only create missing dirs/files.
