"""Build gaps.json from quiz questions and chosen answers.

Per topic: all correct → strong; any wrong → weak + not_understood miss.
A topic is never in both strong and weak.
"""

from __future__ import annotations

from typing import Any


def build_gaps(
    ticket: str,
    questions: list[dict[str, Any]],
    chosen: dict[str, int],
) -> dict[str, Any]:
    by_topic: dict[str, list[dict[str, Any]]] = {}
    for question in questions:
        by_topic.setdefault(question["topic"], []).append(question)

    correct = 0
    strong: list[str] = []
    weak: list[str] = []
    not_understood: list[dict[str, str]] = []

    for topic, topic_questions in by_topic.items():
        all_ok = True
        for question in topic_questions:
            pick = chosen.get(question["id"])
            ok = pick == question["answer"]
            if ok:
                correct += 1
            else:
                all_ok = False
                not_understood.append(
                    {"id": topic, "miss": question.get("miss_if_wrong") or ""}
                )
        if all_ok:
            strong.append(topic)
        else:
            weak.append(topic)

    return {
        "ticket": ticket,
        "score": {"correct": correct, "total": len(questions)},
        "strong": strong,
        "weak": weak,
        "not_understood": not_understood,
    }
