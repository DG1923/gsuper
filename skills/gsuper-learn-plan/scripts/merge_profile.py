"""Merge a quiz gaps object into learn/profile.json."""

from __future__ import annotations

from typing import Any


def merge_profile(profile: dict[str, Any], gaps: dict[str, Any]) -> dict[str, Any]:
    topics: dict[str, dict[str, str]] = {
        key: dict(value) for key, value in (profile.get("topics") or {}).items()
    }
    strong = list(gaps.get("strong") or [])
    weak = list(gaps.get("weak") or [])
    misses = {
        item["id"]: item.get("miss") or ""
        for item in gaps.get("not_understood") or []
    }

    for topic_id in strong:
        topics[topic_id] = {"status": "strong"}

    for topic_id in weak:
        current = topics.get(topic_id) or {}
        if topic_id in strong:
            continue
        if current.get("status") == "not_understood":
            if topic_id in misses:
                topics[topic_id] = {
                    "status": "not_understood",
                    "miss": misses[topic_id],
                }
            continue
        if topic_id in misses:
            topics[topic_id] = {
                "status": "not_understood",
                "miss": misses[topic_id],
            }
        else:
            topics[topic_id] = {"status": "weak"}

    for topic_id, miss in misses.items():
        if topic_id not in strong:
            topics[topic_id] = {"status": "not_understood", "miss": miss}

    return {"topics": topics}
