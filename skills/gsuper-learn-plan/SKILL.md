---
name: gsuper-learn-plan
description: >
  Human overview HTML after spec or plan, before implement. Mentor walkthrough
  (mermaid, lecture under charts, widgets for the user). Agent reads only
  .agent-workflow Markdown. Use after gsuper-write-spec, gsuper-write-plan, or
  /gsuper-workflow-learn. Not gsuper-learn-self. Not implement.
---

# Learn plan (gsuper) — mentor overview for the human

**Stage:** spec and/or plan — **before** `gsuper-implement`.  
**Not** `gsuper-learn-self` (after the plan work is done).

Offer after spec/plan, or run when the user asks / `/gsuper-workflow-learn`. Not during brainstorm (no seams yet).

## Who reads what

| Reader | Artifact |
|--------|----------|
| Agent (this skill, then implement) | `.agent-workflow/specs/…` and `.agent-workflow/plans/…` only |
| Human | `docs/<ticket-id>-slug/overview.html` |

Implement uses spec `Done when`, not the HTML. Widgets and Q&A exist so the **user** can try a path a chart cannot teach.

Shape, catalogs, thin vs fat, Unverified, voice: [references/overview-shape.md](references/overview-shape.md).

## Steps

1. **Read the workflow Markdown.** Spec always. Plan too if it exists and the user just finished `gsuper-write-plan`. Extract Purpose, seams, now vs after, out of scope. **Done when:** those four are named from the files, not from memory.

2. **Verify now against the repo.** File-backed or tag **Unverified**. **Done when:** every now-claim has a path or sits in the Unverified box.

3. **Pick by question.** Chart catalog and widget catalog in overview-shape. One of each kind that has a question. Thin ticket: one mermaid. **Done when:** each block on the page answers a question you can say aloud; extras are cut.

4. **Write the HTML.** Path in overview-shape. Voice: mentor tech lead leveling the user. Under every chart: lecture text (why this picture, what to copy, what not to copy). Widgets for the user. Q&A answers collapsed. **Tích lũy / Accumulate last** — carry-forward cards + Unverified. Mermaid (CDN) is enough. **Done when:** a new hire can fail a Q&A, open it, and name one thing they will not put in the next PR.

5. **Point the spec at the HTML.** One `**Overview (human):**` line. Do not paste the lecture into the spec. **Done when:** the spec links the file; implement still has `Done when` in Markdown.

6. **Hand the path to the user.** Stay pre-implement. **Done when:** they have the file path; implement has not started in this skill.

## Guardrails (pair)

Write the overview as a mentor lecture with mermaid and user widgets. Spec/plan stay the implement source. Unverified stays labeled and out of spec.
