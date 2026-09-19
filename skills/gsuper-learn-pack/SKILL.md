---
name: gsuper-learn-pack
description: >
  Human learn pack (Markdown) after brainstorm, spec, or implement. Unique
  gsuper-pack-<repo>-<ticket>.md for the user to understand first (natural language,
  then flow; optional ChatGPT/Claude upload). Overview then per-unit flows (both
  required). Open quiz in the pack, no answer key.
  Path .agent-workflow/learn/. Not gsuper-learn-material. Not implement AC.
  Formerly gsuper-learn-plan.
---

# Learn pack (gsuper)

**Not** implement. **Not** `gsuper-learn-material` (one-concept lesson + sample).

Pack is for the **human to understand first** (read; optional upload). Implement uses **plan** `Done when` only.

Shape: [references/pack-shape.md](references/pack-shape.md).

Filename (do not use `pack.md`): [scripts/names.py](scripts/names.py) — `pack_filename`.

Repo slug = git toplevel directory name (or remote repo name). Ticket id = scratch folder / issue slug.

## When

- After **gsuper-brainstorm** (intent locked; spec may not exist yet)
- After **gsuper-write-spec** / **gsuper-write-plan**
- After **gsuper-implement** (regenerate pack at stage `after-implement`)
- Repo / spec is unreadable or the user has no project context — write the pack from **code** first

Offer; user may decline. `/gsuper-workflow-learn` or `/gsuper-workflow-learn-pack` runs this skill.

## Who reads what

| Reader | Artifact |
|--------|----------|
| Human | `learn/<feature>/gsuper-pack-<repo>-<ticket>.md` (full, upload) |
| Agent | plan/intent MD, optional spec-docs, `memory.py find`. `.agent-workflow/conventions.md` is **not project law** |
| Implement | plan `Done when` only |

Do **not** write `need-to-know-*.md` or `self-report-*.md`. Do **not** copy quiz.html or overview.html. Do **not** write `gaps.json`.

## Sources (required)

Pack is compiled from **plan + live code** (and spec-docs if the ticket used them), not from memory.

| Input | How it enters the pack |
|-------|------------------------|
| Plan / intent / spec-docs | Read. Restate in **plain language**; quote `Done when` / must that still match code. |
| Live code | **Explain first** (what it does in everyday words). Then a short excerpt (path + fence, ~5–20 lines) **after** the explanation. Paraphrase is allowed; if paraphrase fights the file → drift row. |
| Doc that contradicts code | One **drift** row: doc said X, file:line does Y. |

**Do not** `cat` / concat whole spec files or whole `.py` modules into the pack. That is a dump: stale SRS + 2k-line detectors, no map, no drift, ChatGPT hits context. Concat is allowed **only** for the short excerpts you chose.

## Pack steps (any stage)

1. List source paths in the header (`sources:`). Read them. **Verify every spec claim against code.** User or doc wrong → drift table, not silence.
2. Write **one** file under `learn/<feature>/`: `gsuper-pack-<repo>-<ticket-id>.md` (overwrite same name). `<feature>` = cùng slug `specs/feature/<feature>/`. Header: repo, ticket, **stage**, date, sources.
3. Body is **two layers in one file**, user-first:
   - **Giải thích + Overview first** — chuyện gì xảy ra (lời thường) + **one mermaid E2E** in a ` ```mermaid ` fence + bảng bước vào/ra bằng lời thường, must/must-not, jump links.
   - **Then per-unit** — mỗi luồng: câu chuyện ngắn + **mermaid flow** + giải thích bước; **verbatim** excerpt **sau**.
   - Overview-only = too thin. Detail-only = too thick. Excerpt-only = failed. ASCII-only diagrams = rewrite as mermaid.
4. **Quiz** at the end: open questions in plain language, **no answer key**.
5. Voice: the person who reads and decides. Self-contained. Hand the **full filename**. Optional “use in another chat” **after** the explanation, never first.

## Guardrails

Pack = the only full-ticket learn upload. Quiz lives in the pack. Invariants JSON = Cursor agent one-pager. Plan `Done when` is unchanged.

One-concept ôn + runnable sample → **gsuper-learn-material** (after implement).

After writing the pack file, if `memory.py` exists, record **path only** (no mermaid/body ingest):

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite note --kind verify --node <node> --body "pack pointer" --path .agent-workflow/learn/<feature>/<pack-filename>
```
