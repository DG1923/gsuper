---
name: gsuper-write-spec-sync
description: >
  Inventory a large existing repo and propose spec map (has specs or none).
  Use when the user asks to sync or analyze docs on an existing project.
---

# Write spec — sync

For **repos that already have code**. Specs may be missing or leftover.

Follow [../gsuper-write-spec/references/sync.md](../gsuper-write-spec/references/sync.md).

1. Inventory code + docs + `specs/`.
2. Propose map (kind / id / keep|rewrite|create|skip).
3. **Wait.**
4. One approved row → `gsuper-write-spec-<kind>` and **that** shape file.
5. If nothing in `specs/system|architecture|algorithm|feature|srs/` → create **system** only, then stop.

Do not fill four kinds in one pass. Do not use feature-shape for system.
