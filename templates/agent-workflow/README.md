# `.agent-workflow` (gsuper)

Project-local storage for the gsuper plugin workflow.

| Path | Contents |
|------|----------|
| `plans/<feature>/` | Ticket AC. Plugin tickets → `plans/gsuper/`. |
| `specs/<kind>/<feature>/` | Project docs. `system/` stays flat. Dated root `YYYY-MM-DD-*` = leftover. |
| `scratch/<ticket>/` | Intent, AC, state while working a ticket |
| `learning/` | Unused. Do not write new files here. |
| `learn/<feature>/` | `gsuper-pack-*.md`, `gsuper-material-*.md`, `samples/`. |
| `conventions.md` | **Not project law.** Init/migrate stub only. Must/must-not live in `specs/<kind>/`. |
| `memory.sqlite` | Local find index (nodes, seams, decisions). **Never commit.** `memory.py init` if missing; `find --ticket` / `--q` / `around` before dumping plans/specs (never bare `find`). `lock --kind plan` after plan approve; `lock --kind spec` after spec-doc approve. Technical answers: **So sánh** or **Raise** (`rules/source-ladder.mdc`). |

By default this directory is **gitignored**. Remove `.agent-workflow/` from `.gitignore` if you want to commit artifacts. Always keep `memory.sqlite` ignored. Projects that version `.agent-workflow/` still ignore personal learn JSON via `learn/.gitignore`.
