"""Self-report parse and need-to-know render. No quiz answers."""

from __future__ import annotations

from typing import Any

KNOWN = frozenset({"known", "yes", "biet", "biết"})
UNKNOWN = frozenset({"unknown", "no", "khong", "không", "khong biet", "không biết"})


def parse_self_report(markdown: str) -> dict[str, dict[str, str]]:
    """Parse ## topic blocks with status: and how: lines."""
    result: dict[str, dict[str, str]] = {}
    topic = ""
    status = "unknown"
    how_lines: list[str] = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            if topic:
                result[topic] = {"status": status, "how": "\n".join(how_lines).strip()}
            topic = line[3:].strip()
            status = "unknown"
            how_lines = []
            continue
        if not topic:
            continue
        lower = line.lower()
        if lower.startswith("status:"):
            value = line.split(":", 1)[1].strip().lower()
            if value in KNOWN:
                status = "known"
            else:
                status = "unknown"
        elif lower.startswith("how:"):
            how_lines.append(line.split(":", 1)[1].strip())
        elif line and not lower.startswith("#"):
            how_lines.append(line)
    if topic:
        result[topic] = {"status": status, "how": "\n".join(how_lines).strip()}
    return result


def self_report_template(ticket: str, topic_ids: list[str]) -> str:
    lines = [
        f"# Self-report — {ticket}",
        "",
        "Per topic: `status: known` or `status: unknown`. `how:` is your words — no quiz answers live here.",
        "",
    ]
    for topic_id in topic_ids:
        lines.extend(
            [
                f"## {topic_id}",
                "status: unknown",
                "how:",
                "",
            ]
        )
    return "\n".join(lines)


def render_need_to_know(
    title: str,
    sections: list[dict[str, Any]],
    report: dict[str, dict[str, str]] | None,
) -> str:
    """Unknown or missing topic → full; known → recap."""
    report = report or {}
    lines = [f"# {title}", "", "Short. Pack file is the full upload.", ""]
    for section in sections:
        topic_id = str(section["id"])
        status = (report.get(topic_id) or {}).get("status", "unknown")
        body_key = "recap" if status == "known" else "full"
        body = str(section.get(body_key) or section.get("full") or "")
        lines.append(f"## {section.get('title') or topic_id}")
        if status == "known":
            lines.append("_recap — marked known_")
        else:
            lines.append("_full — unknown or not reported_")
        lines.append("")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
