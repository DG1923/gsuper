# Pack shape

Implement never uses this file as AC. Spec `Done when` stays in Markdown.

## Paths

```text
.agent-workflow/learn/gsuper-pack-<repo>-<ticket-id>.md
.agent-workflow/learn/invariants.json
```

Never name the pack `pack.md`. Helper: `scripts/names.py` `pack_filename`.

Do not write `need-to-know-*.md` or `self-report-*.md`.

## Pack header (required)

```markdown
# Pack: <repo> / <ticket-id>
- stage: after-brainstorm | after-spec | after-implement
- generated: YYYY-MM-DD
```

Then, **in this order**:

1. How to use in another chat
2. **Overview** — purpose, **one mermaid E2E**, name table, must/must-not, jump links, drift vs spec
3. **Per-unit detail** — mermaid flow per unit + verbatim excerpts
4. Quiz

A pack that is only overview, or only detail, is incomplete.

Voice: mid/senior to a peer. Self-contained: upload this file alone.

## Per-unit section (required for each live detector / stage / service)

Not a one-line summary. Each unit needs:

1. **Flow** — mermaid `flowchart` of `detect()` / `process()` (cache, callees, stages, queues). Not ASCII trees.
2. **I/O** — exact filenames and column names from code.
3. **Numbers** — thresholds, windows, weights, timeouts as in the live ctor (call out class-default vs live override).
4. **Failure / traps** — empty output, stale docs, type mismatches.
5. **Excerpt** — path + short fence. Unverified if the file is not in the tree.

Overview-only (“three detectors then three stages”) is a failed pack.  
Detail-only (no Part A map) is also a failed pack.

## Quiz (required)

Open questions that can be graded **only** from this file. No answer key, no `why_right`. Cover flows, not just names.

## Honesty

If a user claim or repo doc contradicts cited code, the pack states the contradiction. Do not paper over it.

## No dump-concat

Do not shell-concat entire specs or modules into the pack. Excerpts are copy-paste of **chosen** functions only.

## Stages

| When | Write |
|------|--------|
| After brainstorm | pack, stage `after-brainstorm` |
| After spec or plan | pack, stage `after-spec` |
| After implement | pack, stage `after-implement` |
| Unreadable spec / foreign repo | pack from **code**, mark doc drift |
