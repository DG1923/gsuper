"""CLI: find / around / note / seed-xproject."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from store import around, connect, find, init_schema, upsert_note


def _default_db() -> Path:
    return Path.cwd() / ".agent-workflow" / "memory.sqlite"


def _cli_text(s: str) -> str:
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    return s.encode(enc, errors="replace").decode(enc)


def _print_line(s: str) -> None:
    print(_cli_text(s))


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

    sub.add_parser("seed-xproject")

    args = parser.parse_args(argv)
    conn = connect(args.db)
    init_schema(conn)

    try:
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

        if args.cmd == "seed-xproject":
            from seed_xproject import seed

            seed(conn)
            print("seeded")
            return 0
    except ValueError as exc:
        _print_line(str(exc))
        return 2

    return 2


if __name__ == "__main__":
    sys.exit(main())
