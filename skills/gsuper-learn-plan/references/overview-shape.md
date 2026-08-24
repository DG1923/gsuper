# Overview shape (human HTML)

Agent input: `.agent-workflow` Markdown (+ `learn/invariants.json` and `learn/<ticket-id>/gaps.json` if present). Implement never uses the HTML as AC.

## Path

```text
.agent-workflow/learn/<ticket-id>/quiz.html           # copy from templates/quiz.html — do not edit
.agent-workflow/learn/<ticket-id>/quiz-data.js        # agent writes this only
.agent-workflow/learn/<ticket-id>/gaps.json           # user export; gitignored; Read+check before overview
.agent-workflow/learn/<ticket-id>/overview.html       # copy from templates/overview.html — do not edit
.agent-workflow/learn/<ticket-id>/overview-data.js    # agent writes this only
.agent-workflow/learn/invariants.json                 # must / must not + spec path; init empty
.agent-workflow/learn/profile.json                    # merge_profile after each gaps; gitignored
```

Not `docs/`. One scrolling overview page. Spec: `**Overview (human):**` → the HTML.

Data files are `window.OVERVIEW_DATA = { … }` / `window.QUIZ_DATA = { … }` so `file://` works (no fetch). Schema: [templates/overview-data.example.js](../templates/overview-data.example.js), [templates/quiz-data.example.js](../templates/quiz-data.example.js).

## Voice

Mid or senior engineer talking to a peer who already codes. Identifiers in `<code>`. Lecture language = the user’s language. Not junior onboarding.

## Quiz

12-20 questions. Topic ids match overview section `topic` fields. First pick locks; show `why_right` / `why_wrong` then Next. Submit exports `gaps.json` (`score`, `strong`, `weak`, `not_understood`) via copy/download. Missing gaps → STOP, no overview-data.

## Overview page order

1. Role strip — spec decides · code is now · overview reports
2. **Owns** — each component: phụ trách / không phụ trách / lỗi hay mắc
3. Charts — question → mermaid and/or widget → **lecture or recap** (`depth` from gaps) → short code if it earns it
4. 80/20 Q&A — question visible, answer in `<details>`
5. **Accumulate last** — cards + **Unverified**

`depth[topic] === "recap"` → `section.recap`; else `section.lecture`. Widgets/mermaid still render.

## Thin vs fat

| Ticket | Ship |
|--------|------|
| Thin | Role strip · owns · one mermaid · lecture · Q&A · accumulate |
| Fat | Add only a chart/widget that answers a new question |

## Chart / widget catalogs

| Question | Chart |
|----------|--------|
| What talks to what | flowchart |
| Who sends what, in time | sequence |
| Allowed statuses / events | state |
| Ordered stages in one box | flowchart (process) |
| List, Q&A | no chart |

| Question | Widget |
|----------|--------|
| Who owns what / typical miss | `owns` chips |
| Same parts, one move | `arch` now/after |
| Time, one arrow at a time | `seq` stepper |
| From this status, this event | `state` fire-event |
| If this world, then what | `die` what-if |
| What this stage owns | `process` click-stage |
| Try to answer first | Q&A details |

Mermaid is enough. Omit a key in `OVERVIEW_DATA` to skip that block.

## Unverified

Repo-backed or tagged Unverified. Unverified does not enter spec/plan/implement. Amber box at accumulate.
