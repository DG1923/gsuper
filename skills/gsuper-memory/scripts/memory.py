"""CLI: init / node / lock / find / around / note. No project-specific seed."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from store import (
    around,
    connect,
    find,
    init_schema,
    live_spec_id,
    upsert_node,
    upsert_note,
    upsert_spec_lock,
)


def _default_db() -> Path:
    return Path.cwd() / ".agent-workflow" / "memory.sqlite"


def _cli_text(s: str) -> str:
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    return s.encode(enc, errors="replace").decode(enc)


def _print_line(s: str) -> None:
    print(_cli_text(s))


def _lock_decisions(musts: list[str], must_nots: list[str]) -> list[dict[str, str]]:
    n = max(len(musts), len(must_nots))
    if n == 0:
        raise ValueError("lock needs at least one --must or --must-not")
    rows: list[dict[str, str]] = []
    for i in range(n):
        rows.append(
            {
                "must": musts[i] if i < len(musts) else "",
                "must_not": must_nots[i] if i < len(must_nots) else "",
            }
        )
    return rows


def _print_rows(rows: list[dict]) -> None:
    for r in rows:
        symbol = r.get("symbol") or ""
        body = (r.get("body") or "").replace("\t", " ").replace("\n", " ")
        _print_line(
            f"{r.get('row_kind', '')}\t{r.get('status', '')}\t"
            f"{r.get('evidence', '')}\t{r.get('path', '')}\t{symbol}\t{body}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="memory.py")
    parser.add_argument("--db", type=Path, default=_default_db())
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    p_node = sub.add_parser("node")
    p_node.add_argument("--slug", required=True)
    p_node.add_argument("--kind", required=True)
    p_node.add_argument("--title", required=True)
    p_node.add_argument("--blurb", default="")

    p_lock = sub.add_parser("lock")
    p_lock.add_argument("--ticket", required=True)
    p_lock.add_argument("--node", required=True)
    p_lock.add_argument("--path", required=True)
    p_lock.add_argument("--summary", required=True)
    p_lock.add_argument("--must", action="append", default=[])
    p_lock.add_argument("--must-not", action="append", default=[])
    p_lock.add_argument("--supersede", type=int, default=None)

    p_find = sub.add_parser("find")
    p_find.add_argument("--kind")
    p_find.add_argument("--node")
    p_find.add_argument("--ticket")
    p_find.add_argument("--q")
    p_find.add_argument("--old", action="store_true")

    p_around = sub.add_parser("around")
    p_around.add_argument("node")

    p_note = sub.add_parser("note")
    p_note.add_argument("--kind", required=True)
    p_note.add_argument("--node", required=True)
    p_note.add_argument("--body", required=True)
    p_note.add_argument("--path", default="")
    p_note.add_argument("--evidence", default="spec")

    args = parser.parse_args(argv)
    existed = args.db.exists()
    conn = connect(args.db)
    init_schema(conn)

    try:
        if args.cmd == "init":
            _print_line("ok" if existed else "created")
            return 0

        if args.cmd == "node":
            upsert_node(
                conn,
                slug=args.slug,
                kind=args.kind,
                title=args.title,
                blurb=args.blurb,
            )
            print("ok")
            return 0

        if args.cmd == "lock":
            sid = args.supersede
            if sid is None:
                sid = live_spec_id(conn, args.ticket)
            artifact_id = upsert_spec_lock(
                conn,
                ticket=args.ticket,
                node=args.node,
                path=args.path,
                summary=args.summary,
                decisions=_lock_decisions(args.must, args.must_not),
                supersede_id=sid,
            )
            _print_line(f"ok\t{artifact_id}")
            return 0

        if args.cmd == "find":
            rows = find(
                conn,
                kind=args.kind,
                node=args.node,
                ticket=args.ticket,
                q=args.q,
                old=args.old,
            )
            _print_rows(rows)
            return 0

        if args.cmd == "around":
            out = around(conn, args.node)
            for n in out["neighbors"]:
                _print_line(f"neighbor\t{n['rel']}\t\t\t{n['slug']}\t")
            _print_rows(out["seams"])
            _print_rows(out["notes"])
            _print_rows(out["artifacts"])
            return 0

        if args.cmd == "note":
            upsert_note(
                conn,
                kind=args.kind,
                node=args.node,
                body=args.body,
                path=args.path,
                evidence=args.evidence,
            )
            print("ok")
            return 0
    except ValueError as exc:
        _print_line(str(exc))
        return 2

    return 2


if __name__ == "__main__":
    sys.exit(main())
