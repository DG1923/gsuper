# gsuper

Portable **code workflow** skills for Cursor, Claude Code, Codex, Pi, and other agents:

```text
gsuper-brainstorm → gsuper-write-spec → gsuper-write-plan → gsuper-implement → gsuper-review
```

Side tracks: **gsuper-learn-plan** (unique pack Markdown under `.agent-workflow/learn/`) · **gsuper-learn-self** (personal skill cards after plan done).

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
| `gsuper-brainstorm` | Clarify intent (grilling + symptom-gate) before any code |
| `gsuper-write-spec` | Locked Done when / seams / Sec+Perf |
| `gsuper-write-plan` | Bite-size TDD tasks (~500 LOC soft) |
| `gsuper-implement` | test → RED → frame → fill → GREEN |
| `gsuper-review` | Defect + Spec + Standards (read-only) |
| `gsuper-learn-plan` | Unique pack Markdown after brainstorm/spec/implement; per-unit flows + quiz |
| `gsuper-learn-self` | Personal concept cards after plan done |
| `gsuper-workflow` | Orchestrator |
| `gsuper-init-project` | `.agent-workflow/` + gitignore |
| `gsuper-github-templates` | Parent / sub-issue / PR templates |

Rules (Cursor): Ponytail, Python objects, testing seams, PEP 8, small diffs.

---

## After install

In the agent, ask for `/gsuper-workflow` or “run gsuper-brainstorm” on a new feature.  
Artifact root: `.agent-workflow/` (created by `gsuper-init-project`).

---

## Docs

- [DISTRIBUTE.md](DISTRIBUTE.md) — IDE vs CLI vs other agents  
- [CHANGELOG.md](CHANGELOG.md)

## License

MIT
