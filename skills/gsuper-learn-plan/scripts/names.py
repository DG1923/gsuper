"""Unique learn artifact filenames (upload-safe)."""

from __future__ import annotations

import re


def slug(part: str) -> str:
    text = part.strip().lower().replace("_", "-")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "ticket"


def pack_filename(repo: str, ticket_id: str) -> str:
    return f"gsuper-pack-{slug(repo)}-{slug(ticket_id)}.md"


def need_to_know_filename(repo: str, ticket_id: str) -> str:
    return f"need-to-know-{slug(repo)}-{slug(ticket_id)}.md"


def self_report_filename(ticket_id: str) -> str:
    return f"self-report-{slug(ticket_id)}.md"
