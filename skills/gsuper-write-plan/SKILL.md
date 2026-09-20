---
name: gsuper-write-plan
description: >
  Ticket plan under .agent-workflow/plans/ after approved intent (spec-docs optional).
  Same fields as the old ticket spec, plus impacted files, testing approach, and
  a user-readable implementation story. No test/impl bodies. Soft ~500 LOC/slice.
---

# Write plan (gsuper)

Self-contained. **No** runtime Superpowers `writing-plans`.

Gate: approved **intent** (and this plan). Project **spec-docs** (`specs/algorithm|srs|feature|architecture|system/`) are optional — Read if the plan should follow them.  
Legacy: if an old ticket spec exists and there is **no** plan yet, you may turn that spec into this plan shape (do not rewrite other EL-* files unless asked).

Missing `.agent-workflow/` → **gsuper-init-project**.

If the user jumped here with a fuzzy feature and no intent → **gsuper-brainstorm** first.

## Output

```text
.agent-workflow/plans/<feature>/YYYY-MM-DD-<ticket>.md
```

`<feature>` = cùng id folder với `specs/feature/<feature>/` (vd. `shadowing`, `custom-course`). Ticket plugin/workflow → `plans/gsuper/`. Không để mọi plan cùng cấp `plans/*.md`.

Shape: [references/plan-shape.md](references/plan-shape.md). Layout **B**: each heading is plain language first, then a table/list for the agent.

## Process

1. Run `memory.py find --ticket <id>` (empty → index miss; Read intent / plan / linked spec-doc on disk). Prefer a live **plan** pointer over a legacy ticket spec. **source-ladder:** **`So sánh:`** to that plan/intent or **`Raise:`** if none — do not invent AC.
2. Write the plan for the **user who approves it**, in **natural language** they already used: Purpose, chuyện gì xảy ra, Flow, slices (việc rồi file), how we will test.
3. **Do not** paste test function bodies or implementation bodies.
4. Self-review per plan-shape.md.
5. Save file. Ask the user to approve.
6. After **approve**, lock (no body ingest):

```text
python <gsuper>/skills/gsuper-memory/scripts/memory.py --db .agent-workflow/memory.sqlite lock --kind plan --ticket <id> --node <node> --path .agent-workflow/plans/<feature>/<file>.md --summary "..." --must "..." --must-not "..."
```

If `lock` cannot run (unknown node), `node` first, or `sync --plans .agent-workflow/plans` then `lock`.

7. Offer learn pack → **gsuper-learn-pack**. Do **not** offer **gsuper-learn-material** here.
8. Exit → **gsuper-implement** when the user is ready.

Do **not** append a JSON conventions store. `.agent-workflow/conventions.md` is **not project law**. Project must/must-not live in the matching spec-doc. Propose spec edits; do not write the same bullets into conventions.md.

## Rules while writing

- Samples in the plan are **signatures or one-liners**, not full tests
- Before mermaid: 2–4 sentences **chuyện gì xảy ra** in the user's words
- Every chart (chat and `.md`) is a ` ```mermaid ` fence — never a bare `flowchart`
- Each slice: what the user will see change, **then** files
- I/O table columns in everyday words, not only function names
- Ponytail: don’t plan gold-plating the intent didn’t ask for
- No silent scope expand — gap → ask or Open questions
