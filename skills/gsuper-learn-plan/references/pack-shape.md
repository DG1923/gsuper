# Pack + need-to-know shape

Implement never uses these files as AC. Spec `Done when` stays in Markdown.

## Paths

```text
.agent-workflow/learn/gsuper-pack-<repo>-<ticket-id>.md
.agent-workflow/learn/need-to-know-<repo>-<ticket-id>.md   # after implement
.agent-workflow/learn/self-report-<ticket-id>.md           # gitignored
.agent-workflow/learn/invariants.json
.agent-workflow/learn/profile.json                         # gitignored
```

Never name the pack `pack.md`. Helpers: `scripts/names.py`.

## Pack header (required)

```markdown
# Pack: <repo> / <ticket-id>
- stage: after-brainstorm | after-spec | after-implement
- generated: YYYY-MM-DD
```

Then: purpose, seams / now vs after, must / must-not (from invariants + spec), cited excerpts (`path` + fenced code). Unverified labeled. Voice: mid/senior to a peer who codes.

Self-contained: upload this file alone to ChatGPT/Claude.

## Need-to-know

Short. After implement. Same topics as spec seams. `render_need_to_know`: known → recap; unknown or missing self-report → full. Still much shorter than the pack.

## Self-report

```markdown
## <topic-id>
status: known
how: …
```

`status:` `known` or `unknown` (or biết / không biết). No answer key. Not AC. Does not truncate the pack.

## Stages

| When | Write |
|------|--------|
| After brainstorm | pack, stage `after-brainstorm` |
| After spec or plan | pack, stage `after-spec` |
| After implement | pack `after-implement` + need-to-know + self-report stub |
