# gsuper

Portable **code workflow** skills for Cursor, Claude Code, Codex, Pi, and other agents:

```text
brainstorm → write-spec → write-plan → implement → review
```

Side tracks: **learn-plan** (diagrams before implement) · **learn-self** (personal skill cards after plan done).

MIT · self-contained (no runtime Matt / Superpowers deps).

---

## Install (any agent)

Skills live under `skills/*/SKILL.md` — compatible with [Agent Skills](https://agentskills.io) and installers like [`npx skills`](https://github.com/vercel-labs/skills) / [`npx add-skill`](https://github.com/vercel-labs/add-skill).

### One-liner (recommended)

```bash
# All skills → choose agents when prompted (Claude Code, Cursor, Codex, …)
npx skills add DG1923/gsuper

# Or pin agents + global
npx skills add DG1923/gsuper -g -a cursor -a claude-code -a codex -y

# List what’s in the repo first
npx skills add DG1923/gsuper --list
```

Equivalent:

```bash
npx add-skill DG1923/gsuper
```

### Manual clone

```bash
git clone https://github.com/DG1923/gsuper.git
cd gsuper
./scripts/install.sh --target cursor-skills --dest "$HOME/.cursor/skills"   # Cursor CLI
./scripts/install.sh --target flat-skills --dest "$HOME/.claude/skills"    # Claude Code
./scripts/install.sh --target flat-skills --dest "$HOME/.codex/skills"     # Codex
# Windows: .\scripts\install.ps1 -Target cursor-skills -Dest "$env:USERPROFILE\.cursor\skills"
```

### Cursor IDE (full plugin: skills + rules + commands)

```bash
git clone https://github.com/DG1923/gsuper.git ~/.cursor/plugins/local/gsuper
# or: ln -s /path/to/gsuper ~/.cursor/plugins/local/gsuper
```

Reload Cursor. See [DISTRIBUTE.md](DISTRIBUTE.md) for Team Marketplace / server notes.

---

## What’s inside

| Skill | Role |
|-------|------|
| `brainstorm` | Clarify intent (grilling + symptom-gate) before any code |
| `write-spec` | Locked Done when / seams / Sec+Perf |
| `write-plan` | Bite-size TDD tasks (~500 LOC soft) |
| `implement` | test → RED → frame → fill → GREEN |
| `review` | Defect + Spec + Standards (read-only) |
| `learn-plan` | Diagrams at spec/plan (before implement) |
| `learn-self` | Personal concept cards after plan done |
| `workflow` | Orchestrator |
| `init-project` | `.agent-workflow/` + gitignore |
| `github-templates` | Parent / sub-issue / PR templates |

Rules (Cursor): Ponytail, Python objects, testing seams, PEP 8, small diffs.

---

## After install

In the agent, ask for `/workflow` or “run gsuper brainstorm” on a new feature.  
Artifact root: `.agent-workflow/` (created by `init-project`).

---

## Docs

- [DISTRIBUTE.md](DISTRIBUTE.md) — IDE vs CLI vs other agents  
- [CHANGELOG.md](CHANGELOG.md)

## License

MIT
