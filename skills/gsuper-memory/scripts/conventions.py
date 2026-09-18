"""Move leftover learn/invariants.json into conventions.md. Never drop sqlite."""

from __future__ import annotations

import json
from pathlib import Path

HEADER = """# Project conventions

**Not project law.** Do not put must/must-not here.

Project rules live in one spec file per concept:

```text
.agent-workflow/specs/<kind>/<id>.md
```

(`architecture`, `system`, `feature`, `algorithm`, `srs` — Constraints section.)

This file exists so `memory.py init` can migrate leftover `learn/invariants.json`. Leave it empty of product rules.
"""


def upgrade_workflow(workflow: Path) -> str:
    workflow.mkdir(parents=True, exist_ok=True)
    md_path = workflow / "conventions.md"
    json_path = workflow / "learn" / "invariants.json"

    created = False
    if not md_path.exists():
        md_path.write_text(HEADER, encoding="utf-8")
        created = True

    if not json_path.exists():
        return "created" if created else "ok"

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"bad conventions json: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        raise ValueError("bad conventions json: missing rules list")

    rules = data["rules"]
    text = md_path.read_text(encoding="utf-8")
    appended = False
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError("bad conventions json: rule not an object")
        rid = str(rule.get("id") or "").strip()
        if not rid:
            raise ValueError("bad conventions json: rule missing id")
        if f"## {rid}" in text:
            continue
        if not text.endswith("\n"):
            text += "\n"
        text += (
            f"\n## {rid}\n"
            f"- must: {rule.get('must', '')}\n"
            f"- must_not: {rule.get('must_not', '')}\n"
            f"- spec: {rule.get('spec', '')}\n"
        )
        appended = True

    if appended:
        md_path.write_text(text, encoding="utf-8")

    final = md_path.read_text(encoding="utf-8")
    missing = [
        str(rule.get("id") or "").strip()
        for rule in rules
        if isinstance(rule, dict) and f"## {str(rule.get('id') or '').strip()}" not in final
    ]
    missing = [m for m in missing if m]
    if missing:
        raise ValueError("migrate incomplete: " + ",".join(missing))
    json_path.unlink()
    if appended:
        return "migrated"
    return "created" if created else "ok"
