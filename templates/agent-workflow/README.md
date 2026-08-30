# `.agent-workflow` (gsuper)

Project-local storage for the gsuper plugin workflow.

| Path | Contents |
|------|----------|
| `specs/` | Approved designs / phase specs |
| `plans/` | Implementation plans |
| `scratch/<ticket>/` | Intent, AC, state while working a ticket |
| `learning/` | Unused. Do not write new files here. |
| `learn/` | `gsuper-pack-*.md`, `gsuper-material-*.md`, `samples/`, `invariants.json`. Gitignore leftover `self-report*.md` / `profile.json` / `gaps.json` |

By default this directory is **gitignored**. Remove `.agent-workflow/` from `.gitignore` if you want to commit artifacts. Projects that version `.agent-workflow/` still ignore personal learn JSON via `learn/.gitignore`.
