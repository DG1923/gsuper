---
name: gsuper-learn-plan
description: >
  Human overview after spec or plan, before implement. Quiz first when
  shipping learn HTML: copy templates, write quiz-data.js / overview-data.js
  only. Path .agent-workflow/learn/. Agent reads spec/plan MD. Use after
  gsuper-write-spec, gsuper-write-plan, or /gsuper-workflow-learn.
  Not gsuper-learn-self. Not implement.
---

# Learn plan (gsuper) — quiz, gaps, overview

**Stage:** spec and/or plan — **before** `gsuper-implement`.  
**Not** `gsuper-learn-self`.

Offer after spec/plan, or `/gsuper-workflow-learn`. Not during brainstorm.

## Who reads what

| Reader | Artifact |
|--------|----------|
| Agent (this skill, then implement) | `.agent-workflow/specs/…`, `.agent-workflow/plans/…`, `.agent-workflow/learn/invariants.json`, `.agent-workflow/learn/<ticket-id>/gaps.json` |
| Human | `.agent-workflow/learn/<ticket-id>/quiz.html` then `overview.html` |

Implement uses spec `Done when`. Do not use the HTML as AC.

If `invariants.json` exists, **Read it** before writing quiz or overview data. Codegraph for code symbols, not for spec/invariants/gaps.

Shape: [references/overview-shape.md](references/overview-shape.md).

## Steps

1. **Read workflow Markdown** (and `learn/invariants.json` if present). Spec always. Plan if they just finished write-plan. If `learn/profile.json` exists, Read it — next quiz **must** include ≥1 question whose `topic` is profile `weak` or `not_understood` when profile is non-empty. **Done when:** Purpose, seams, now vs after, out of scope are named from files.

2. **Verify now against the repo.** File-backed or **Unverified**. **Done when:** every now-claim has a path or sits in Unverified.

3. **Copy quiz template, write quiz-data only.** Copy [templates/quiz.html](templates/quiz.html) → `.agent-workflow/learn/<ticket-id>/quiz.html`. Write **only** `quiz-data.js` (`window.QUIZ_DATA = {…}`). 12–20 questions. Topic ids **align** with overview section `topic` fields. Voice: mid/senior to a peer who codes. Each question: `why_right`, `why_wrong[]`, `miss_if_wrong`. HTML locks the first pick and shows those explanations before Next. **Done when:** user can open `quiz.html` and finish in one sitting.

4. **Wait for `gaps.json` on disk.** User submits → copy or download. Path: `.agent-workflow/learn/<ticket-id>/gaps.json`. If they paste JSON in chat: **write the file, then Read it again**. Never invent scores from chat memory. **Hard gate:** **Read + check** keys `score`, `strong`, `weak`, `not_understood`. Missing file or missing keys → **STOP**. Do not write overview-data. **Done when:** the file on disk has those keys.

5. **Merge profile.** After a valid gaps file, run [scripts/merge_profile.py](scripts/merge_profile.py) (`merge_profile`) into `.agent-workflow/learn/profile.json` (create if missing). `not_understood` stays until a later quiz marks that topic `strong`. **Done when:** profile on disk reflects this sitting.

6. **Copy overview template, write data only.** Copy [templates/overview.html](templates/overview.html) → `.agent-workflow/learn/<ticket-id>/overview.html`. Write **only** `overview-data.js`. Set `depth`: strong topics → `"recap"`; weak / `not_understood` → `"full"`. Mermaid/widgets always present if the section exists. Include `owns` (phụ trách / không / lỗi hay mắc). Lecture **under** each chart. Q&A collapsed. Accumulate **last**. **Done when:** a peer can open a Q&A and name one thing they will not put in the next PR.

7. **Point the spec.** One `**Overview (human):**` line to that HTML. **Done when:** spec links it; `Done when` stays in Markdown.

8. **Hand the paths to the user.** Pre-implement. **Done when:** they have quiz + overview paths; this skill has not started implement.

## Guardrails (pair)

Copy templates + fill `quiz-data.js` / `overview-data.js`. Spec/plan remain the implement source. Unverified stays labeled and out of spec. Do not treat HTML as AC. `gaps.json` / `profile.json` / `result.json` are gitignored — do not commit them.
