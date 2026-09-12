# `.agent-workflow` (gsuper)

Project-local storage for the gsuper plugin workflow.

| Path | Contents |
|------|----------|
| `specs/` | Approved designs / phase specs |
| `plans/` | Implementation plans |
| `scratch/<ticket>/` | Intent, AC, state while working a ticket |
| `learning/` | Unused. Do not write new files here. |
| `learn/` | `gsuper-pack-*.md`, `gsuper-material-*.md`, `samples/`. Gitignore leftover `self-report*.md` / `profile.json` / `gaps.json` |
| `conventions.md` | User-owned project must/must-not. Agent proposes; writes only after approval. Not implement AC. |
| `memory.sqlite` | Local find index (nodes, seams, decisions). **Never commit.** `memory.py init` if missing; `find` before dumping specs. |

By default this directory is **gitignored**. Remove `.agent-workflow/` from `.gitignore` if you want to commit artifacts. Always keep `memory.sqlite` ignored. Projects that version `.agent-workflow/` still ignore personal learn JSON via `learn/.gitignore`.
