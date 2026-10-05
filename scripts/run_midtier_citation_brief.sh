#!/bin/bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRIEF_FILE="$PROJECT_DIR/sessions/MIDTIER_CITATION_SIGNAL_BRIEF_v1.0.md"
LOG_FILE="$PROJECT_DIR/sessions/midtier_citation_brief_run_$(date +%Y%m%d_%H%M%S).log"
PLIST_LABEL="com.justinbank.midtier-citation-brief"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"

cd "$PROJECT_DIR"

CLAUDE_BIN="$(command -v claude || true)"
CLAUDE_BIN="${CLAUDE_BIN:-/opt/homebrew/bin/claude}"

"$CLAUDE_BIN" -p "$(cat "$BRIEF_FILE")" \
  --permission-mode bypassPermissions \
  --output-format text \
  > "$LOG_FILE" 2>&1

# One-shot job: unload and remove the LaunchAgent so it doesn't recur.
launchctl bootout "gui/$(id -u)" "$PLIST_PATH" 2>/dev/null || true
rm -f "$PLIST_PATH"
