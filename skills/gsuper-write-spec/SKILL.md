---
name: gsuper-write-spec
description: >
  Write or update project documents (algorithm, SRS, large feature, architecture,
  system design) under .agent-workflow/specs/<kind>/. Not ticket AC. Use when the
  user asks to write, update, sync existing docs, analyze docs, or improve specs.
---

# Write spec (gsuper)

**Not** the ticket lock. Ticket AC is **gsuper-write-plan**.

Run **only when the user asks** to write, update, **sync**, **analyze**, or **improve** project docs. Do **not** run after every implement.

Fuzzy “build feature X” without a locked intent → **gsuper-brainstorm**, then a **plan**, not this skill.

Fill [references/spec-template.md](references/spec-template.md). **Plain language**. Easy to read. Production-quality: a new teammate can use the file without opening the whole repo.

**One concept → one file.** Must/must-not for an area live in that matching spec-doc (`Constraints`). Do not write the same bullets into `conventions.md`. `.agent-workflow/conventions.md` is **not project law** (init/migrate stub only).

## Output

```text
.agent-workflow/specs/<kind>/<id>.md
```

`<kind>` is one of: `algorithm`, `srs`, `feature`, `architecture`, `system`.  
Unknown folder → **ask**; do not invent a kind.

Legacy dated files `specs/YYYY-MM-DD-<ticket>.md` stay put (dual-read). Do not move them unless the user asks.

Missing dir → **gsuper-init-project**. Create the kind folder if missing.

## Mode A — project already has docs (sync + analyze)

When the user asks to sync or analyze existing docs:

1. **Find sources** (do not dump): `SRS/`, `docs/`, README, leftover `.agent-workflow/conventions.md` (fold unique rules into the matching spec, then stop using that file as law), linked research. Skip ticket plans and dated `specs/YYYY-MM-DD-*` unless the user names them.
2. **Propose a map** (table: source → kind → id → keep / rewrite / skip). **Wait** if kind is unclear.
3. **Rewrite** into the spec template — **do not** copy the source file verbatim into `specs/`.
4. One **Apply check** + **Reflection** (below). If Design overclaims, **rewrite Design now**. Then ask the user to approve.

## Mode B — new project or unstable structure

When there is no durable spec, or docs fight the code:

1. Read **live code and tests** as facts. Leftover `conventions.md` is a source to fold into spec Constraints — never proof of what ships, and not a second law file.
2. Write the **smallest** set of specs that a production reader needs (usually `system` + `architecture`; add `feature` / `algorithm` / `srs` only if the user asked or the product already has that surface).
3. One **Apply check** + **Reflection** pass. Then ask the user to approve.
4. Do not invent a full SRS for unimplemented product areas.

## Apply check (one pass, then ask)

Facts from live code/tests, not conventions.md.  
If Design overclaims, **rewrite Design in this pass**. Reflection = leftover risk — **not** a place to leave a wrong Design. Do not write the same must/must-not into conventions.md.

Do **not** loop until perfect. Do **not** skip FE when Kind is `system` or `feature` in a monorepo.

- [ ] Happy path vs fallback named separately (example: json3 vs VTT)
- [ ] User Flow = click/submit that exists (not implied auto)
- [ ] Composition root vs router vs domain (who imports SQL / HTTP / domain)
- [ ] HTTP JSON fields vs domain types (synthetic `id`, …)
- [ ] FE + BE if Kind is `system` or `feature`
- [ ] Each must/must-not: a file or test that shows it

## Reflection (after Apply, still one pass)

Short **Reflection** on the draft (or in chat if tiny). Then **stop**.

| Check | Fail if |
|-------|---------|
| Drift | Design still says X while file:line does Y — fix Design, do not only note it here |
| Flow | User-visible or system flow exists but no mermaid/table |
| Readable | Jargon without a gloss; file-path dump |
| Production | Missing must/must-not, error/boundary, or “how this ships” when this doc needs it |
| Kind | Folder / Kind line mismatch |

Do not propose a parallel conventions.md body for rules that belong in this spec.

## Must have

- **Kind** matching the folder
- Purpose in plain language
- **Flow** (mermaid in a ` ```mermaid ` fence in **chat** and the spec file + input / uses / output) when the area has a user-visible or system flow. Never a bare `flowchart`.
- Design body (algorithm / architecture / SRS) — not ticket Done when
- Constraints (must / must-not for this area)
- **Sources** (paths used; not a dump)
- **Apply check** done; Design matches live code (overclaims rewritten)
- **Reflection** (one pass) on first draft / sync

No file-path dump. No “code must be clean”. Ponytail: do not turn a ticket into an SRS unless the user asked for that doc.

## Self-review

Placeholders, jargon without a gloss, Kind/folder mismatch, missing Reflection, Design still overclaiming vs code → fix before ask user.

## Exit

User reviews file. **Approved** → lock (path + summary + must/must-not; **do not** ingest the markdown body). `--id` is the doc id (not an EL-* ticket):

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite lock --kind spec --id <id> --node <node> --path .agent-workflow/specs/<kind>/<id>.md --summary "..." --must "..." --must-not "..."
```

If `lock` cannot run (unknown node), `node` first, or `sync --specs .agent-workflow/specs` then `lock`.

Optional **gsuper-learn-pack**. Do **not** append a JSON conventions store. `.agent-workflow/conventions.md` is **not project law**.

Do **not** hand off to write-plan unless the user is starting a ticket that needs one.  
Do **not** offer **gsuper-learn-material** here.
