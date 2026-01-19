#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

usage() {
    cat <<'EOF'
Codex helper for SocialPublisher (isolated from Claude Skill)

Usage:
  codex/run.sh status [--json] [-p platform]
  codex/run.sh login [--platform all|twitter|wechat|xiaohongshu]
  codex/run.sh init --topic "Your Topic"
  codex/run.sh search --query "Your Topic" --time-range "24h" --posts '[...]'
  codex/run.sh engage --action like --post-id "123"
  codex/run.sh distill --trends '["t1"]' --points '["p1"]'
  codex/run.sh generate --platform twitter --thread '["1/ ..."]'
  codex/run.sh publish --platform twitter --status published --count 1
  codex/run.sh verify
  codex/run.sh report
  codex/run.sh list
  codex/run.sh session-id

Notes:
  - This wrapper only calls scripts/ helpers.
  - It does not use .claude/ or Playwright MCP.
EOF
}

if [[ $# -lt 1 ]]; then
    usage
    exit 0
fi

cmd="$1"
shift

case "$cmd" in
    status)
        "$PYTHON_BIN" "$ROOT_DIR/scripts/check_login.py" "$@"
        ;;
    login)
        "$PYTHON_BIN" "$ROOT_DIR/codex/login.py" "$@"
        ;;
    init|search|engage|distill|generate|publish|verify|report|list|session-id)
        "$PYTHON_BIN" "$ROOT_DIR/scripts/content_tracker.py" "$cmd" "$@"
        ;;
    track)
        "$PYTHON_BIN" "$ROOT_DIR/scripts/content_tracker.py" "$@"
        ;;
    help|-h|--help)
        usage
        ;;
    *)
        echo "Unknown command: $cmd" >&2
        usage
        exit 1
        ;;
esac
