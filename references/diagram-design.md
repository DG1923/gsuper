# diagram-design (for gsuper-learn-plan)

Upstream: [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)

## Purpose in gsuper

After a plan is saved, if the user wants a walkthrough, use diagram-design to explain the plan with 1–2 clear diagrams (architecture, flowchart, sequence, or data flow) plus short narration tied to plan tasks.

## Setup

Install or enable the diagram-design skill/plugin so the agent can load `skills/diagram-design/SKILL.md`.

Examples:

- Clone/add the repo as a Cursor plugin or copy its `skills/diagram-design` into an available skills path
- Or `/add-plugin` / marketplace install if published for your Cursor version

## First diagram in a project

Honor diagram-design’s **style-guide gate**: ask before shipping default tokens into a branded project.

## gsuper constraints

- Teach the **plan**, do not start implement
- Low density; split overcrowded graphs
- Prefer HTML+SVG self-contained output as the skill specifies
- Link plan task IDs in the narration
