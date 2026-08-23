# Overview shape (human HTML)

Agent input is `.agent-workflow` Markdown. This file is how to *write* the HTML. Implement never loads the HTML as AC.

## Who it is for

A **mentor** tech lead walking the user up a level before they code. Direct. Quiz, then explain. Identifiers stay in `<code>`. Lecture language = the language the user has been using.

Widgets and Q&A toggles are for the **user** to try. They are not agent procedure.

## Path

```text
docs/<ticket-id>-slug/overview.html
```

One scrolling page. Spec gets one line: `**Overview (human):**` pointing here.

## Page order (locked)

1. Role strip — spec decides · code is now · overview reports
2. Charts the question needs — each block: question → mermaid and/or widget → **lecture text** → short code if it earns it
3. 80/20 Q&A — question visible, suggested answer collapsed (`<details>`)
4. **Tích lũy / Accumulate last** — cards to carry to the next ticket; **Unverified** labels

Lecture sits **under** the chart. A chart that needs no lecture was decoration — cut it. Text that restates the spec's Do/Do not list belongs in the spec, not here.

## Thin vs this-fat

| Ticket | Ship |
|--------|------|
| Thin | Role strip · one mermaid · lecture · Q&A · accumulate |
| Fat (new seam, now vs after, state) | Add only the extra chart/widget that answers a new question |

One of each kind. Skip a kind with no question.

## Chart catalog — pick by question

| Question | Chart |
|----------|--------|
| What talks to what | flowchart (architecture) |
| Who sends what, in time | sequence |
| Allowed statuses / events | state |
| Ordered stages in one box | flowchart (process) |
| List, glossary, Q&A | no chart |

Mermaid is enough. Understanding beats decoration.

## Widget catalog — pick by question the chart cannot teach

| Question | Widget |
|----------|--------|
| Same parts, one move | now / after toggle |
| Time, one arrow at a time | sequence stepper |
| From this status, this event | fire-event + chips |
| If this world, then what | what-if buttons |
| What this stage owns / does not | click-stage |
| Try to answer first | Q&A `<details>` |

A widget with no question is chrome. Cut it.

## Unverified

Every now-claim is repo-backed **or** tagged **Unverified**. Unverified does not enter spec, plan, or implement. Amber box at accumulate, not buried in a lecture.

## Voice test

A new hire can walk the page, fail a Q&A, open the answer, and say what they will not copy into the next PR. If they only remember colors, the lecture failed.
