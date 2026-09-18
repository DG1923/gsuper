# Project conventions

**Not project law.** Do not put must/must-not here.

Project rules live in one spec file per concept:

```text
.agent-workflow/specs/<kind>/<id>.md
```

(`architecture`, `system`, `feature`, `algorithm`, `srs` — Constraints section.)

This file exists so `memory.py init` can migrate leftover `learn/invariants.json`. Leave it empty of product rules.
