---
name: github-templates
description: Install gsuper GitHub parent issue, sub-issue, and PR templates into a project. Use on /workflow-init (optional) or when the user wants GitHub templates.
---

# GitHub templates (gsuper)

## Copy into project

From plugin `templates/github/`:

```text
.github/ISSUE_TEMPLATE/feature-parent.yml
.github/ISSUE_TEMPLATE/phase-sub-issue.yml
.github/ISSUE_TEMPLATE/config.yml
.github/pull_request_template.md
```

Do not overwrite without asking if files already exist.

## Sub-issue rules (enforce in skills that create issues)

Body sections (5):

1. Parent (`#<parent_id>`)
2. What to build
3. Impacted range
4. Acceptance criteria
5. Blocked by — **`#<issue_id>` only** (GitHub-linkable); nest via `addSubIssue` under the parent

## Parent

Use feature-parent template (PRD-style): Problem, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes.
