---
name: gsuper-learn-pack
description: >
  Human learn pack (Markdown) after brainstorm, spec, or implement. Unique
  gsuper-pack-<repo>-<ticket>.md for reading and ChatGPT/Claude upload.
  Overview then per-unit flows (both required). Open quiz in the pack, no answer key.
  Path .agent-workflow/learn/. Not gsuper-learn-material. Not implement AC.
  Formerly gsuper-learn-plan.
---

# Learn pack (gsuper)

**Not** implement. **Not** `gsuper-learn-material` (one-concept lesson + sample).

Pack is for the **human** (read + upload). Implement uses spec `Done when` only.

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
| Human | `learn/gsuper-pack-<repo>-<ticket>.md` (full, upload) |
| Agent | spec/plan/intent MD, `learn/invariants.json` |
| Implement | spec `Done when` only |

Do **not** write `need-to-know-*.md` or `self-report-*.md`. Do **not** copy quiz.html or overview.html. Do **not** write `gaps.json`.

## Sources (required)

Pack is compiled from **spec + live code**, not from memory.

| Input | How it enters the pack |
|-------|------------------------|
| Spec / intent / plan | Read. Quote `Done when` / must-must-not that still match code. |
| Live code | **Verbatim excerpt** (path + fence, ~5–20 lines). Copy the function, do not paraphrase the algorithm. |
| Doc that contradicts code | One **drift** row: spec said X, file:line does Y. |

**Do not** `cat` / concat whole spec files or whole `.py` modules into the pack. That is a dump: stale SRS + 2k-line detectors, no map, no drift, ChatGPT hits context. Concat is allowed **only** for the short excerpts you chose.

## Pack steps (any stage)

1. List source paths in the header (`sources:`). Read them. **Verify every spec claim against code.** User or doc wrong → drift table, not silence.
2. Write **one** file: `gsuper-pack-<repo>-<ticket-id>.md` (overwrite same name). Header: repo, ticket, **stage**, date, sources.
3. Body is **two layers in one file**:
   - **Overview first** — purpose, **one mermaid E2E**, name table, must/must-not, jump links.
   - **Then per-unit detail** — each live detector / stage / service: **mermaid flow** (`detect()` / queues), I/O, numbers, verbatim excerpt, failures.
   - Overview-only = too thin. Detail-only = too thick. ASCII-only diagrams = rewrite as mermaid (you read the pack too).
4. **Quiz** at the end: open questions, **no answer key**.
5. Mid/senior voice. Self-contained. Hand the **full filename**.

## Guardrails

Pack = the only full-ticket learn upload. Quiz lives in the pack. Invariants JSON = Cursor agent one-pager. Spec `Done when` is unchanged.

One-concept ôn + runnable sample → **gsuper-learn-material** (after implement).
