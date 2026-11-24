#!/usr/bin/env bash
# The Dresser: puts the mask on when a session starts, resumes, clears or compacts.
# Silent when there is no mask or auto_don is off. Never fails the session.
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
python3 "$ROOT/scripts/larvahctl.py" hook dresser 2>/dev/null
exit 0
