# Distribute gsuper

Public repo: **https://github.com/DG1923/gsuper**

## Fastest install (multi-agent)

```bash
npx skills add DG1923/gsuper
# or
npx add-skill DG1923/gsuper
```

Installers discover `skills/*/SKILL.md` and copy into Cursor / Claude Code / Codex / Pi / etc.

---

How to ship this plugin to **Cursor IDE**, **Cursor CLI / servers**, and **other agents**.

## What you already have

```text
gsuper/                          # Cursor Plugin (full)
├── .cursor-plugin/plugin.json   # Cursor manifest (rules + skills + commands)
├── skills/                      # Agent Skills (portable core)
├── rules/                       # Cursor .mdc (IDE / project rules)
├── commands/                    # Cursor slash commands
├── templates/
└── scripts/install.*            # copy/symlink helpers
```

Skills under `skills/*/SKILL.md` follow the [Agent Skills](https://agentskills.io) layout — that is the part any agent can consume.

---

## A. Cursor IDE (this machine / any desktop)

```bash
# copy or symlink the whole plugin
ln -s /path/to/gsuper ~/.cursor/plugins/local/gsuper
# Windows (Admin or Developer Mode):
# New-Item -ItemType Junction -Path "$env:USERPROFILE\.cursor\plugins\local\gsuper" -Target "E:\path\to\gsuper"
```

Reload window. Enable **Include third-party Plugins, Skills, and other configs** if needed.  
Org policy may set `userLocal=false` — then local plugins are blocked.

Or: put the repo on GitHub → Team Marketplace / [Marketplace publish](https://cursor.com/marketplace/publish).

---

## B. Cursor CLI on a server (important)

As of early 2026, **`cursor-agent` often does not load skills from plugins** (`~/.cursor/plugins/local` or marketplace cache). Skills register reliably from:

| Path | Scope |
|------|--------|
| `~/.cursor/skills/<name>/SKILL.md` | User (CLI + IDE) |
| `<repo>/.cursor/skills/<name>/SKILL.md` | Project (clone = install) |

**Recommended for headless / CI / server:**

```bash
# from the gsuper root
./scripts/install.sh --target cursor-skills --dest "$HOME/.cursor/skills"
# or into a repo
./scripts/install.sh --target project --dest /path/to/repo
```

Also install rules into the project if you want always-on style:

```bash
./scripts/install.sh --target project-rules --dest /path/to/repo
```

CLI plugin install today is mostly interactive (`cursor-agent` → `/plugin`) or user-scope sync after IDE install — there is **no** solid non-interactive `plugin install` for CI yet. Prefer **flat skills** on servers.

---

## C. Any AI agent (Claude Code, Codex, custom, …)

Same skill folders; only the **destination** changes:

| Agent | Typical skill roots |
|-------|---------------------|
| Cursor | `~/.cursor/skills/`, `.cursor/skills/` |
| Claude Code | `~/.claude/skills/`, project skills if configured |
| Generic | Point the agent at a directory of `*/SKILL.md` trees |

```bash
./scripts/install.sh --target flat-skills --dest /opt/agent-skills/gsuper
# result: /opt/agent-skills/gsuper/gsuper-brainstorm/SKILL.md, …
```

Optional portable **Agent Plugin** manifest (skills only — no Cursor rules/commands): keep a root `plugin.json` with `$schema` from [agent-plugins.org](https://agent-plugins.org) for clients that load that format.

Rules (`.mdc`) and slash `commands/` are **Cursor-specific** — other agents won’t use them unless you translate (e.g. paste into `AGENTS.md` / `CLAUDE.md`).

---

## D. Pack for transfer (tarball / release)

```bash
# from parent of gsuper
tar -czf gsuper-0.2.8.tar.gz \
  --exclude .git \
  gsuper/

# on the server
tar -xzf gsuper-0.2.8.tar.gz
cd gsuper && ./scripts/install.sh --target cursor-skills --dest "$HOME/.cursor/skills"
```

Or git clone the plugin repo and run `install.sh`.

---

## E. What to commit in an app repo (team default)

Minimal, works IDE + CLI for everyone who clones:

```text
your-app/
  .cursor/
    skills/          # copied/symlinked from gsuper/skills/*
    rules/           # optional: gsuper/rules/*
  AGENTS.md          # one line: follow gsuper workflow (gsuper-brainstorm → …)
```

Do **not** rely only on `~/.cursor/plugins/local` if teammates use CLI/CI.

---

## Quick decision

| Goal | Method |
|------|--------|
| Solo Cursor desktop | `plugins/local/gsuper` |
| Server / CLI / CI | Flat `~/.cursor/skills` or repo `.cursor/skills` via `install.sh` |
| Whole team same repo | Commit `.cursor/skills` (+ rules) in the project |
| Other agents | Flat skills dir + their skill path |
| Org-wide Cursor | Team marketplace Required/Default On |

See `scripts/install.sh` and `scripts/install.ps1`.
