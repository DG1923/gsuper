# `.agent-workflow` (gsuper)

Project-local storage for the gsuper plugin workflow.

| Path | Contents |
|------|----------|
| `plans/` | Ticket AC (Purpose, Flow, slices, Testing, Done when). Agent implements from here. |
| `specs/` | Project docs — **not** ticket AC. Subfolders: `algorithm/`, `srs/`, `feature/`, `architecture/`, `system/`. Dated `YYYY-MM-DD-*.md` at root are **legacy** ticket specs (dual-read if no plan). |
| `scratch/<ticket>/` | Intent, AC, state while working a ticket |
| `learning/` | Unused. Do not write new files here. |
| `learn/` | `gsuper-pack-*.md`, `gsuper-material-*.md`, `samples/`. Gitignore leftover `self-report*.md` / `profile.json` / `gaps.json` |
| `conventions.md` | **Not project law.** Init/migrate stub only. Must/must-not live in `specs/<kind>/`. |
| `memory.sqlite` | Local find index (nodes, seams, decisions). **Never commit.** `memory.py init` if missing; `find` before dumping plans/specs. `lock --kind plan` after plan approve; `lock --kind spec` after spec-doc approve. |

By default this directory is **gitignored**. Remove `.agent-workflow/` from `.gitignore` if you want to commit artifacts. Always keep `memory.sqlite` ignored. Projects that version `.agent-workflow/` still ignore personal learn JSON via `learn/.gitignore`.
