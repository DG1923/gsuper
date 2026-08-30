# `.agent-workflow` (gsuper)

Project-local storage for the gsuper plugin workflow.

| Path | Contents |
|------|----------|
| `specs/` | Approved designs / phase specs |
| `plans/` | Implementation plans |
| `scratch/<ticket>/` | Intent, AC, state while working a ticket |
| `learning/` | Personal skill concept cards (`gsuper-learn-self`) — not repo docs |
| `learn/` | Unique `gsuper-pack-*.md` + `invariants.json`. Gitignore leftover `self-report*.md` / `profile.json` / `gaps.json` |

By default this directory is **gitignored**. Remove `.agent-workflow/` from `.gitignore` if you want to commit artifacts. Projects that version `.agent-workflow/` still ignore personal learn JSON via `learn/.gitignore`.
