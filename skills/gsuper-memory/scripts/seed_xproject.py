"""Trial map for x-project pickleball/PGMQ. Lease decision is superseded."""

from __future__ import annotations

import sqlite3

from store import (
    upsert_edge,
    upsert_node,
    upsert_note,
    upsert_seam,
    upsert_spec_lock,
)


def seed(conn: sqlite3.Connection) -> None:
    nodes = (
        ("vibe-ui", "domain", "pickleball-vibe", "UI pickleball and football"),
        ("api", "layer", "API", "FastAPI upload + status. Not GPU."),
        ("queue", "part", "Queue", "PGMQ video.highlight. No Redis broker."),
        ("worker", "part", "Worker", "highlight_worker. Ack after handle."),
        ("detect", "part", "Detect", "TrackNet + X-CLIP + YAMNet (CPU)."),
        ("score", "part", "Score", "Rounds then highlight weights."),
        ("render", "part", "Render", "VibeGenerator + ffmpeg."),
    )
    for slug, kind, title, blurb in nodes:
        upsert_node(conn, slug=slug, kind=kind, title=title, blurb=blurb)

    upsert_edge(conn, "vibe-ui", "api", "next")
    upsert_edge(conn, "api", "queue", "next")
    upsert_edge(conn, "queue", "worker", "next")
    upsert_edge(conn, "worker", "detect", "contains")
    upsert_edge(conn, "worker", "score", "contains")
    upsert_edge(conn, "worker", "render", "contains")
    upsert_edge(conn, "worker", "queue", "depends")

    upsert_seam(
        conn,
        node="queue",
        symbol="QueueClient.enqueue",
        path="backend/src/lib/queue/client.py",
        inputs="queue: str, payload: bytes",
        outputs="EnqueueResult",
        does="Send JSON via pgmq.send, return message_id",
    )
    upsert_seam(
        conn,
        node="queue",
        symbol="QueueClient.consume",
        path="backend/src/lib/queue/client.py",
        inputs="queue: str, timeout: float",
        outputs="ClaimedMessage | None",
        does="Poll pgmq.read until a message or timeout",
    )
    upsert_seam(
        conn,
        node="queue",
        symbol="QueueClient.ack",
        path="backend/src/lib/queue/client.py",
        inputs="ClaimedMessage",
        outputs="None",
        does="pgmq.delete — message is done",
    )
    upsert_seam(
        conn,
        node="worker",
        symbol="Worker.handle",
        path="backend/src/lib/queue/worker.py",
        inputs="queue payload",
        outputs="success | stopped | error",
        does="Run highlight; ack after handle",
    )

    old = upsert_spec_lock(
        conn,
        ticket="61",
        node="worker",
        path=".agent-workflow/specs/2026-08-22-reusable-highlight-worker.md",
        summary="Worker split. Broker in this copy drifted — live is PGMQ.",
        decisions=[{"must": "Redis lease is a claim marker", "must_not": "treat missing lease as dead"}],
    )
    upsert_spec_lock(
        conn,
        ticket="61",
        node="worker",
        path=".agent-workflow/specs/2026-08-22-reusable-highlight-worker.md",
        summary="Worker split. Live broker is PGMQ send/read/delete.",
        decisions=[
            {"must": "PGMQ send/read/delete", "must_not": "RabbitMQ, Redis broker, fail()"},
            {"must": "ack after handle", "must_not": "ack before generate"},
            {"must": "GPU in worker process", "must_not": "VibeProcessor inside FastAPI"},
            {"must": "timeout/kill → stopped", "must_not": "timeout → error"},
        ],
        supersede_id=old,
    )
    upsert_note(
        conn,
        kind="decision",
        node="queue",
        body="must: PGMQ send/read/delete. must_not: RabbitMQ, Redis broker, fail().",
        path="backend/src/lib/queue/",
        evidence="code",
    )
