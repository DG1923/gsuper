"""Project memory sqlite — find / around / upserts. No spec-body ingest."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

_SPEC_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")
_TICKET_BOUNDARY_RE = re.compile(r"[^A-Za-z0-9]")
ARTIFACT_KINDS = frozenset({"plan", "spec"})
SPEC_DOC_FOLDERS = frozenset(
    {"algorithm", "srs", "feature", "architecture", "system"}
)


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS node (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            kind TEXT NOT NULL,
            title TEXT NOT NULL,
            blurb TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS edge (
            id INTEGER PRIMARY KEY,
            from_id INTEGER NOT NULL REFERENCES node(id),
            to_id INTEGER NOT NULL REFERENCES node(id),
            rel TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS artifact (
            id INTEGER PRIMARY KEY,
            kind TEXT NOT NULL,
            ticket TEXT NOT NULL,
            node_id INTEGER REFERENCES node(id),
            path TEXT NOT NULL,
            summary TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'live',
            superseded_by INTEGER,
            evidence TEXT NOT NULL DEFAULT 'spec'
        );
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY,
            kind TEXT NOT NULL,
            node_id INTEGER REFERENCES node(id),
            artifact_id INTEGER REFERENCES artifact(id),
            body TEXT NOT NULL,
            path TEXT NOT NULL DEFAULT '',
            evidence TEXT NOT NULL DEFAULT 'spec',
            status TEXT NOT NULL DEFAULT 'live',
            verify_when TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS seam (
            id INTEGER PRIMARY KEY,
            node_id INTEGER NOT NULL REFERENCES node(id),
            symbol TEXT NOT NULL,
            path TEXT NOT NULL,
            inputs TEXT NOT NULL,
            outputs TEXT NOT NULL,
            does TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'live',
            evidence TEXT NOT NULL DEFAULT 'code'
        );
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
            text,
            source_kind UNINDEXED,
            source_id UNINDEXED,
            tokenize = 'unicode61'
        );
        """
    )
    conn.commit()


def _node_id(conn: sqlite3.Connection, slug: str) -> int:
    row = conn.execute("SELECT id FROM node WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise ValueError(f"unknown node: {slug}")
    return int(row["id"])


def _fts_add(conn: sqlite3.Connection, source_kind: str, source_id: int, text: str) -> None:
    conn.execute(
        "INSERT INTO memory_fts(text, source_kind, source_id) VALUES (?, ?, ?)",
        (text, source_kind, source_id),
    )


def upsert_node(
    conn: sqlite3.Connection,
    *,
    slug: str,
    kind: str,
    title: str,
    blurb: str = "",
) -> int:
    existing = conn.execute("SELECT id FROM node WHERE slug = ?", (slug,)).fetchone()
    if existing:
        conn.execute(
            "UPDATE node SET kind = ?, title = ?, blurb = ? WHERE id = ?",
            (kind, title, blurb, existing["id"]),
        )
        conn.commit()
        return int(existing["id"])
    cur = conn.execute(
        "INSERT INTO node (slug, kind, title, blurb) VALUES (?, ?, ?, ?)",
        (slug, kind, title, blurb),
    )
    conn.commit()
    return int(cur.lastrowid)


def upsert_note(
    conn: sqlite3.Connection,
    *,
    kind: str,
    node: str,
    body: str,
    path: str = "",
    evidence: str = "spec",
    artifact_id: int | None = None,
    status: str = "live",
    verify_when: str = "",
) -> int:
    node_id = _node_id(conn, node)
    cur = conn.execute(
        """
        INSERT INTO note (kind, node_id, artifact_id, body, path, evidence, status, verify_when)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (kind, node_id, artifact_id, body, path, evidence, status, verify_when),
    )
    note_id = int(cur.lastrowid)
    _fts_add(conn, "note", note_id, body)
    conn.commit()
    return note_id


def _live_clause(old: bool) -> str:
    if old:
        return "1=1"
    return "r.status = 'live' AND r.evidence != 'doc'"


def ticket_matches(stored: str, query: str) -> bool:
    """Exact or hyphen/underscore prefix: EL-6 matches EL-6-domain, not EL-60."""
    if not query:
        return True
    if stored == query:
        return True
    return stored.startswith(f"{query}-") or stored.startswith(f"{query}_")


def ticket_in_text(text: str, query: str) -> bool:
    """True when query sits on a non-alnum boundary (avoids EL-6 matching EL-60)."""
    if not query or not text:
        return False
    start = 0
    while True:
        i = text.find(query, start)
        if i < 0:
            return False
        before_ok = i == 0 or _TICKET_BOUNDARY_RE.match(text[i - 1])
        after = i + len(query)
        after_ok = after == len(text) or _TICKET_BOUNDARY_RE.match(text[after])
        if before_ok and after_ok:
            return True
        start = i + 1


def _ids_for_ticket(
    conn: sqlite3.Connection, ticket: str, old: bool
) -> tuple[set[int], set[int]]:
    live_a = _live_clause(old).replace("r.", "a.")
    live_n = _live_clause(old).replace("r.", "n.")
    artifacts: set[int] = set()
    for r in conn.execute(
        f"SELECT a.id, a.ticket FROM artifact a WHERE {live_a} "
        f"AND a.kind IN ('spec', 'plan')"
    ):
        if ticket_matches(str(r["ticket"]), ticket):
            artifacts.add(int(r["id"]))
    notes: set[int] = set()
    for r in conn.execute(
        f"SELECT n.id, n.artifact_id, n.path, n.body FROM note n WHERE {live_n}"
    ):
        aid = r["artifact_id"]
        if aid is not None and int(aid) in artifacts:
            notes.add(int(r["id"]))
        elif aid is None and (
            ticket_in_text(r["path"] or "", ticket)
            or ticket_in_text(r["body"] or "", ticket)
        ):
            notes.add(int(r["id"]))
    return artifacts, notes


def _fts_query(q: str) -> str:
    tokens = q.split()
    if not tokens:
        return '""'
    quoted = ['"' + token.replace('"', '""') + '"' for token in tokens]
    return " AND ".join(quoted)


def _match_ids(conn: sqlite3.Connection, q: str) -> tuple[set[int], set[int], set[int]]:
    notes: set[int] = set()
    artifacts: set[int] = set()
    seams: set[int] = set()
    try:
        matched = conn.execute(
            "SELECT source_kind, source_id FROM memory_fts WHERE memory_fts MATCH ?",
            (_fts_query(q),),
        )
    except sqlite3.OperationalError:
        return notes, artifacts, seams
    for row in matched:
        if row["source_kind"] == "note":
            notes.add(int(row["source_id"]))
        elif row["source_kind"] == "artifact":
            artifacts.add(int(row["source_id"]))
        elif row["source_kind"] == "seam":
            seams.add(int(row["source_id"]))
    return notes, artifacts, seams


def _artifact_rows(
    conn: sqlite3.Connection,
    *,
    artifact_kind: str,
    live: str,
    node_id: int | None,
    artifact_ids: set[int] | None,
) -> list[dict[str, Any]]:
    sql = f"""
        SELECT a.id, a.kind, a.summary, a.path, a.evidence, a.status, a.ticket,
               nd.slug AS node
        FROM artifact a
        LEFT JOIN node nd ON nd.id = a.node_id
        WHERE {live.replace('r.', 'a.')} AND a.kind = ?
    """
    args: list[Any] = [artifact_kind]
    if node_id is not None:
        sql += " AND a.node_id = ?"
        args.append(node_id)
    if artifact_ids is not None:
        if artifact_ids:
            placeholders = ",".join("?" * len(artifact_ids))
            sql += f" AND a.id IN ({placeholders})"
            args.extend(artifact_ids)
        else:
            sql += " AND 1=0"
    rows: list[dict[str, Any]] = []
    for r in conn.execute(sql, args):
        rows.append(
            {
                "row_kind": artifact_kind,
                "status": r["status"],
                "evidence": r["evidence"],
                "path": r["path"],
                "body": r["summary"],
                "symbol": "",
                "ticket": r["ticket"],
                "node": r["node"] or "",
            }
        )
    return rows


def find(
    conn: sqlite3.Connection,
    *,
    kind: str | None = None,
    node: str | None = None,
    ticket: str | None = None,
    q: str | None = None,
    old: bool = False,
) -> list[dict[str, Any]]:
    note_ids: set[int] | None = None
    artifact_ids: set[int] | None = None
    seam_ids: set[int] | None = None
    if q:
        note_ids, artifact_ids, seam_ids = _match_ids(conn, q)

    node_id = _node_id(conn, node) if node else None
    live = _live_clause(old)
    rows: list[dict[str, Any]] = []

    ticket_art_ids: set[int] | None = None
    ticket_note_ids: set[int] | None = None
    if ticket:
        ticket_art_ids, ticket_note_ids = _ids_for_ticket(conn, ticket, old)
        if note_ids is not None:
            note_ids = note_ids & ticket_note_ids
        else:
            note_ids = ticket_note_ids
        if artifact_ids is not None:
            artifact_ids = artifact_ids & ticket_art_ids
        else:
            artifact_ids = ticket_art_ids

    want_notes = kind in (None, "decision", "note")
    want_plans = kind in (None, "plan")
    want_specs = kind in (None, "spec")
    want_seams = kind in (None, "seam")

    if want_notes:
        sql = f"""
            SELECT n.id, n.kind, n.body, n.path, n.evidence, n.status, nd.slug AS node,
                   COALESCE(a.ticket, '') AS ticket
            FROM note n
            JOIN node nd ON nd.id = n.node_id
            LEFT JOIN artifact a ON a.id = n.artifact_id
            WHERE {live.replace('r.', 'n.')}
        """
        args: list[Any] = []
        if kind == "decision":
            sql += " AND n.kind = 'decision'"
        elif kind == "note":
            sql += " AND n.kind != 'decision'"
        if node_id is not None:
            sql += " AND n.node_id = ?"
            args.append(node_id)
        if note_ids is not None:
            if not note_ids:
                sql += " AND 1=0"
            else:
                placeholders = ",".join("?" * len(note_ids))
                sql += f" AND n.id IN ({placeholders})"
                args.extend(note_ids)
        for r in conn.execute(sql, args):
            rows.append(
                {
                    "row_kind": "decision" if r["kind"] == "decision" else "note",
                    "status": r["status"],
                    "evidence": r["evidence"],
                    "path": r["path"],
                    "body": r["body"],
                    "symbol": "",
                    "ticket": r["ticket"] or "",
                    "node": r["node"],
                }
            )

    if want_plans:
        rows.extend(
            _artifact_rows(
                conn,
                artifact_kind="plan",
                live=live,
                node_id=node_id,
                artifact_ids=artifact_ids,
            )
        )
    if want_specs:
        rows.extend(
            _artifact_rows(
                conn,
                artifact_kind="spec",
                live=live,
                node_id=node_id,
                artifact_ids=artifact_ids,
            )
        )

    if want_seams:
        sql = f"""
            SELECT s.id, s.symbol, s.path, s.inputs, s.outputs, s.does,
                   s.evidence, s.status, nd.slug AS node
            FROM seam s
            JOIN node nd ON nd.id = s.node_id
            WHERE {live.replace('r.', 's.')}
        """
        args = []
        if node_id is not None:
            sql += " AND s.node_id = ?"
            args.append(node_id)
        if seam_ids is not None:
            if seam_ids:
                placeholders = ",".join("?" * len(seam_ids))
                sql += f" AND s.id IN ({placeholders})"
                args.extend(seam_ids)
            else:
                sql += " AND 1=0"
        for r in conn.execute(sql, args):
            rows.append(
                {
                    "row_kind": "seam",
                    "status": r["status"],
                    "evidence": r["evidence"],
                    "path": r["path"],
                    "body": r["does"],
                    "symbol": r["symbol"],
                    "ticket": "",
                    "node": r["node"],
                    "inputs": r["inputs"],
                    "outputs": r["outputs"],
                }
            )

    return rows


def upsert_edge(conn: sqlite3.Connection, src: str, dst: str, rel: str) -> int:
    src_id = _node_id(conn, src)
    dst_id = _node_id(conn, dst)
    existing = conn.execute(
        "SELECT id FROM edge WHERE from_id = ? AND to_id = ? AND rel = ?",
        (src_id, dst_id, rel),
    ).fetchone()
    if existing:
        return int(existing["id"])
    cur = conn.execute(
        "INSERT INTO edge (from_id, to_id, rel) VALUES (?, ?, ?)",
        (src_id, dst_id, rel),
    )
    conn.commit()
    return int(cur.lastrowid)


def upsert_seam(
    conn: sqlite3.Connection,
    *,
    node: str,
    symbol: str,
    path: str,
    inputs: str,
    outputs: str,
    does: str,
    status: str = "live",
    evidence: str = "code",
) -> int:
    if "\n" in does.strip():
        raise ValueError("seam.does must be a single line")
    node_id = _node_id(conn, node)
    existing = conn.execute(
        "SELECT id FROM seam WHERE node_id = ? AND symbol = ?",
        (node_id, symbol),
    ).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE seam SET path = ?, inputs = ?, outputs = ?, does = ?,
                   status = ?, evidence = ? WHERE id = ?
            """,
            (path, inputs, outputs, does, status, evidence, existing["id"]),
        )
        conn.execute(
            "DELETE FROM memory_fts WHERE source_kind = 'seam' AND source_id = ?",
            (existing["id"],),
        )
        _fts_add(conn, "seam", int(existing["id"]), f"{symbol} {does}")
        conn.commit()
        return int(existing["id"])
    cur = conn.execute(
        """
        INSERT INTO seam (node_id, symbol, path, inputs, outputs, does, status, evidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (node_id, symbol, path, inputs, outputs, does, status, evidence),
    )
    seam_id = int(cur.lastrowid)
    _fts_add(conn, "seam", seam_id, f"{symbol} {does}")
    conn.commit()
    return seam_id


def live_artifact_id(
    conn: sqlite3.Connection, ticket: str, kind: str
) -> int | None:
    row = conn.execute(
        "SELECT id FROM artifact WHERE kind = ? AND ticket = ? AND status = 'live'",
        (kind, ticket),
    ).fetchone()
    if row is None:
        return None
    return int(row["id"])


def live_spec_id(conn: sqlite3.Connection, ticket: str) -> int | None:
    return live_artifact_id(conn, ticket, "spec")


def upsert_spec_lock(
    conn: sqlite3.Connection,
    *,
    ticket: str,
    node: str,
    path: str,
    summary: str,
    decisions: list[dict[str, str]],
    supersede_id: int | None = None,
    kind: str = "spec",
) -> int:
    if kind not in ARTIFACT_KINDS:
        raise ValueError(f"lock kind must be plan or spec, got {kind}")
    node_id = _node_id(conn, node)
    cur = conn.execute(
        """
        INSERT INTO artifact (kind, ticket, node_id, path, summary, status, evidence)
        VALUES (?, ?, ?, ?, ?, 'live', ?)
        """,
        (kind, ticket, node_id, path, summary, kind),
    )
    artifact_id = int(cur.lastrowid)
    _fts_add(conn, "artifact", artifact_id, f"{ticket} {summary}")
    if supersede_id is not None:
        conn.execute(
            "UPDATE artifact SET status = 'superseded', superseded_by = ? WHERE id = ?",
            (artifact_id, supersede_id),
        )
        conn.execute(
            "UPDATE note SET status = 'superseded' WHERE artifact_id = ?",
            (supersede_id,),
        )
    for item in decisions:
        must = item.get("must", "")
        must_not = item.get("must_not", "")
        body = f"must: {must}. must_not: {must_not}."
        upsert_note(
            conn,
            kind="decision",
            node=node,
            body=body,
            path=path,
            evidence=kind,
            artifact_id=artifact_id,
        )
    conn.commit()
    return artifact_id


def around(conn: sqlite3.Connection, node_slug: str) -> dict[str, Any]:
    nid = _node_id(conn, node_slug)
    neighbors: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    q = """
        SELECT n.slug, e.rel
        FROM edge e
        JOIN node n ON n.id = e.to_id
        WHERE e.from_id = ?
        UNION
        SELECT n.slug, e.rel
        FROM edge e
        JOIN node n ON n.id = e.from_id
        WHERE e.to_id = ? AND n.id != ?
    """
    for r in conn.execute(q, (nid, nid, nid)):
        key = (r["slug"], r["rel"])
        if key in seen:
            continue
        seen.add(key)
        neighbors.append({"slug": r["slug"], "rel": r["rel"]})
    rows = find(conn, node=node_slug)
    return {
        "neighbors": neighbors,
        "seams": [r for r in rows if r["row_kind"] == "seam"],
        "notes": [r for r in rows if r["row_kind"] in ("decision", "note")],
        "artifacts": [r for r in rows if r["row_kind"] in ARTIFACT_KINDS],
    }


def _first_heading(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    except OSError:
        return ""
    return ""


def _rel_to_parent(path: Path, parent: Path) -> str:
    try:
        return path.resolve().relative_to(parent.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _live_tickets_of(conn: sqlite3.Connection, kind: str) -> list[str]:
    rows = conn.execute(
        "SELECT ticket FROM artifact WHERE kind = ? AND status = 'live'",
        (kind,),
    )
    return [str(r["ticket"]) for r in rows]


def _ticket_already_live(live_tickets: list[str], ticket: str) -> bool:
    return any(
        ticket_matches(existing, ticket) or ticket_matches(ticket, existing)
        for existing in live_tickets
    )


def _ensure_sync_node(conn: sqlite3.Connection, ticket: str, blurb: str) -> None:
    try:
        _node_id(conn, ticket)
    except ValueError:
        upsert_node(conn, slug=ticket, kind="part", title=ticket, blurb=blurb)


def _lock_sync_file(
    conn: sqlite3.Connection,
    *,
    path: Path,
    ticket: str,
    kind: str,
    parent: Path,
    live_tickets: list[str],
    pointer_must: str,
) -> dict[str, str]:
    rel = _rel_to_parent(path, parent)
    if _ticket_already_live(live_tickets, ticket):
        return {"action": "skip", "ticket": ticket, "path": str(path)}
    _ensure_sync_node(conn, ticket, f"sync from {kind}")
    summary = _first_heading(path) or ticket
    upsert_spec_lock(
        conn,
        ticket=ticket,
        node=ticket,
        path=rel,
        summary=summary,
        decisions=[{"must": pointer_must, "must_not": ""}],
        kind=kind,
    )
    live_tickets.append(ticket)
    return {"action": "lock", "ticket": ticket, "path": rel}


def sync_spec_dir(conn: sqlite3.Connection, specs_dir: Path) -> list[dict[str, str]]:
    """Register missing spec pointers. Does not ingest must/body. Skips tickets already live."""
    results: list[dict[str, str]] = []
    if not specs_dir.is_dir():
        raise ValueError(f"not a directory: {specs_dir}")
    live_tickets = _live_tickets_of(conn, "spec")
    parent = specs_dir.resolve().parent
    for path in sorted(specs_dir.glob("*.md")):
        matched = _SPEC_FILE_RE.match(path.name)
        if not matched:
            continue
        ticket = matched.group(2)
        results.append(
            _lock_sync_file(
                conn,
                path=path,
                ticket=ticket,
                kind="spec",
                parent=parent,
                live_tickets=live_tickets,
                pointer_must="spec pointer (sync)",
            )
        )
    for folder in sorted(SPEC_DOC_FOLDERS):
        doc_dir = specs_dir / folder
        if not doc_dir.is_dir():
            continue
        for path in sorted(doc_dir.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            matched = _SPEC_FILE_RE.match(path.name)
            if matched:
                ticket = matched.group(2)
            elif path.name == "index.md":
                ticket = path.parent.name
            else:
                ticket = path.stem
            results.append(
                _lock_sync_file(
                    conn,
                    path=path,
                    ticket=ticket,
                    kind="spec",
                    parent=parent,
                    live_tickets=live_tickets,
                    pointer_must="spec pointer (sync)",
                )
            )
    for child in sorted(specs_dir.iterdir()):
        if not child.is_dir() or child.name in SPEC_DOC_FOLDERS or child.name.startswith("."):
            continue
        for path in sorted(child.glob("*.md")):
            rel = _rel_to_parent(path, parent)
            results.append({"action": "skip-kind", "ticket": path.stem, "path": rel})
    return results


def sync_plan_dir(conn: sqlite3.Connection, plans_dir: Path) -> list[dict[str, str]]:
    """Register missing plan pointers. Dated filenames only. No body ingest."""
    results: list[dict[str, str]] = []
    if not plans_dir.is_dir():
        raise ValueError(f"not a directory: {plans_dir}")
    live_tickets = _live_tickets_of(conn, "plan")
    parent = plans_dir.resolve().parent
    for path in sorted(plans_dir.rglob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        matched = _SPEC_FILE_RE.match(path.name)
        if not matched:
            continue
        ticket = matched.group(2)
        results.append(
            _lock_sync_file(
                conn,
                path=path,
                ticket=ticket,
                kind="plan",
                parent=parent,
                live_tickets=live_tickets,
                pointer_must="plan pointer (sync)",
            )
        )
    return results
