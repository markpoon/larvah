#!/usr/bin/env bash
# The Stagehand: re-states the core lines on each message. Off unless the
# person switches it on (larvahctl.py settings stagehand true). Never fails a prompt.
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
python3 "$ROOT/scripts/larvahctl.py" hook stagehand 2>/dev/null
exit 0
