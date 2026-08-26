"""Merge self-report into learn/profile.json. Unknown stays until known."""

from __future__ import annotations

from typing import Any


def merge_profile(
    profile: dict[str, Any],
    report: dict[str, dict[str, str]],
) -> dict[str, Any]:
    topics: dict[str, dict[str, str]] = {
        key: dict(value) for key, value in (profile.get("topics") or {}).items()
    }
    for topic_id, entry in report.items():
        status = entry.get("status") or "unknown"
        how = entry.get("how") or ""
        current = topics.get(topic_id) or {}
        if status == "known":
            topics[topic_id] = {"status": "known", "how": how}
            continue
        if current.get("status") == "unknown" or topic_id not in topics:
            topics[topic_id] = {"status": "unknown", "how": how or current.get("how") or ""}
    return {"topics": topics}
