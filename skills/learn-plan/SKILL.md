---
name: learn-plan
description: >
  Diagram walkthrough of a gsuper spec or plan BEFORE implement. Use after write-spec
  or write-plan offer, or /workflow-learn. Not for personal skill cards (learn-self).
---

# Learn plan (gsuper) — pre-implement diagrams

**Stage:** spec and/or plan — **before** `implement`.  
**Not** `learn-self` (that runs after the plan work is done).

Only when the user asks (offer after spec/plan, or `/workflow-learn`).

## Goal

Understand design/plan visually before coding: seams, data flow, task order — short prose + 1–2 diagrams.

## Input

- Spec: `.agent-workflow/specs/…` (architecture / seams)
- and/or Plan: `.agent-workflow/plans/…` (tasks / sequence)  
Prefer plan if both exist and user just finished `write-plan`. Prefer spec if still pre-plan.

## How

1. Read the chosen artifact(s).
2. Prefer [diagram-design](https://github.com/cathrynlavery/diagram-design) (architecture / flowchart / sequence / data-flow) as self-contained HTML+SVG.
3. Follow `references/diagram-design.md` (style-guide gate on first use).
4. Low density; one idea per diagram; split if crowded.
5. Narrate short bullets tied to spec seams or plan Task IDs.

## Do not

- Start **implement** during this skill
- Run **learn-self** here (wrong stage)
- Regenerate the whole plan/spec unless asked
- Spam diagram types — pick 1–2
