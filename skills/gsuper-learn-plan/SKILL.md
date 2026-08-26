---
name: gsuper-learn-plan
description: >
  Human learn pack (Markdown) after brainstorm, spec, or implement. Unique
  gsuper-pack-<repo>-<ticket>.md for reading and ChatGPT/Claude upload.
  After implement: short need-to-know.md + self-report (known/unknown, no quiz).
  Path .agent-workflow/learn/. Not gsuper-learn-self. Not implement AC.
---

# Learn pack (gsuper)

**Not** implement. **Not** `gsuper-learn-self` (concept cards).

Pack and need-to-know are for the **human**. Implement uses spec `Done when` only.

Shape: [references/pack-shape.md](references/pack-shape.md).

Filenames (do not use `pack.md`): [scripts/names.py](scripts/names.py) — `pack_filename`, `need_to_know_filename`, `self_report_filename`.

Repo slug = git toplevel directory name (or remote repo name). Ticket id = scratch folder / issue slug.

## When

- After **gsuper-brainstorm** (intent locked; spec may not exist yet)
- After **gsuper-write-spec** / **gsuper-write-plan**
- After **gsuper-implement** (regenerate pack at stage `after-implement` + need-to-know + self-report stub)

Offer; user may decline. `/gsuper-workflow-learn` runs this skill.

## Who reads what

| Reader | Artifact |
|--------|----------|
| Human | `learn/gsuper-pack-<repo>-<ticket>.md` (full, upload) and `learn/need-to-know-<repo>-<ticket>.md` (short, after implement) |
| Agent | spec/plan/intent MD, `learn/invariants.json`, `learn/self-report-<ticket>.md` if present |
| Implement | spec `Done when` only |

Do **not** copy quiz.html or overview.html. Do **not** write `gaps.json` from a scored quiz.

## Pack steps (any stage)

1. Read intent if present. Read spec/plan if they exist. Read `invariants.json` if present. Verify now-claims against the repo or tag Unverified.
2. Cite code with **path + excerpt** (codegraph for symbols). Do not dump whole files.
3. Write **one** file: `gsuper-pack-<repo>-<ticket-id>.md` (overwrite same name). Header: repo, ticket, **stage** (`after-brainstorm` | `after-spec` | `after-implement`), date. Body: purpose, seams, must/must-not, excerpts. Mid/senior voice. Self-contained — someone with no repo can ask ChatGPT/Claude from this file alone.
4. Hand the **full filename** to the user.

## After implement (extra)

5. Write `need-to-know-<repo>-<ticket-id>.md` from spec seams: each topic has `full` and `recap` in your notes. If `self-report-*.md` exists, **Read** it and run [scripts/self_report.py](scripts/self_report.py) `render_need_to_know` (known → recap, unknown/missing → full). If no self-report yet, all full (short file still — not a pack dump).
6. Write stub `self-report-<ticket-id>.md` via `self_report_template` if missing (topics, `status: unknown`, empty `how:`). Tell the user to fill it. Gitignored. Merge into `learn/profile.json` with [scripts/merge_profile.py](scripts/merge_profile.py) after they fill — unknown stays until known.
7. **Never** shrink the pack from self-report. **Never** treat these files as AC.

## Guardrails

Pack = full upload. Need-to-know = short read. Self-report = biết / không + như nào. Invariants JSON = Cursor agent one-pager.
