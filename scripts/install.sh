#!/usr/bin/env bash
# Install gsuper skills (and optionally rules) for Cursor CLI / servers / other agents.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET=""
DEST=""

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh --target <mode> --dest <path>

  cursor-plugin   Copy/symlink whole plugin → DEST (usually ~/.cursor/plugins/local/gsuper)
  cursor-skills   Copy each skills/* → DEST/<skill-name>/  (CLI-safe: ~/.cursor/skills)
  project         Copy skills → DEST/.cursor/skills/
  project-rules   Copy rules  → DEST/.cursor/rules/
  flat-skills     Copy skills → DEST/<skill-name>/  (any agent skill root)

Examples:
  ./scripts/install.sh --target cursor-skills --dest "$HOME/.cursor/skills"
  ./scripts/install.sh --target project --dest /srv/app
  ./scripts/install.sh --target cursor-plugin --dest "$HOME/.cursor/plugins/local/gsuper"
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --dest) DEST="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1"; usage; exit 1 ;;
  esac
done

[[ -n "$TARGET" && -n "$DEST" ]] || { usage; exit 1; }

copy_skills_into() {
  local out="$1"
  mkdir -p "$out"
  for d in "$ROOT"/skills/*/; do
    [[ -f "${d}SKILL.md" ]] || continue
    name="$(basename "$d")"
    rm -rf "$out/$name"
    cp -a "$d" "$out/$name"
    echo "skill → $out/$name"
  done
}

case "$TARGET" in
  cursor-plugin)
    mkdir -p "$(dirname "$DEST")"
    rm -rf "$DEST"
    cp -a "$ROOT" "$DEST"
    echo "plugin → $DEST"
    ;;
  cursor-skills|flat-skills)
    copy_skills_into "$DEST"
    ;;
  project)
    copy_skills_into "$DEST/.cursor/skills"
    ;;
  project-rules)
    mkdir -p "$DEST/.cursor/rules"
    cp -a "$ROOT"/rules/*.mdc "$DEST/.cursor/rules/" 2>/dev/null || true
    echo "rules → $DEST/.cursor/rules"
    ;;
  *)
    echo "Unknown target: $TARGET"; usage; exit 1
    ;;
esac

echo "Done. For Cursor IDE plugin path: reload window. For CLI: restart cursor-agent."
