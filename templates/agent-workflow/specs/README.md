# specs/ — project documents

Ticket AC is **`plans/`**, not this folder.

Each kind has **its own headings** (do not copy feature shalls into system):

| Folder | Reader should see | Shape |
|--------|-------------------|--------|
| `system/` | Product in the world: actors, apps, NFR | Job, Actors, Context, Apps |
| `architecture/` | How the machine is wired (core) | Layers, Stores, Composition |
| `algorithm/` | Input → steps → output | Happy, Fallback, Limits |
| `feature/` | Job + shall. Always `feature/<feature>/index.md` | Problem, Requirements, Contract |
| `algorithm/` / `architecture/` | Nest under **same feature slug** | Happy / Layers |
| `srs/` | Optional. Skip if it only repeats system Surfaces | — |

**Existing repo** (code already there; this folder empty or stale) → **gsuper-write-spec-sync**, then one kind.

New feature: write that kind only. Agent **suggests** sibling drift; does not auto-patch system / architecture / algorithm.

Write or update only when asked (**gsuper-write-spec** → kind sub-skill). Chain: system → architecture (core) → algorithm → feature → plan. Unknown folder: ask; do not invent `core/`.

Dated files `YYYY-MM-DD-<ticket>.md` in this directory root are leftover **ticket** specs. Leave them. New tickets do not add files here.
