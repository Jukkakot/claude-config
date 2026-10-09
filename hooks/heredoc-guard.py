"""PreToolUse hook for Bash: deny long heredoc commands (they break on quotes/backticks).

Kept after a trial (2026-09-27 to 2026-10-08; logging dropped then, the user's decision).
"""
import json
import sys

MAX_LINES = 30


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    command = (data.get("tool_input") or {}).get("command") or ""
    if "<<" not in command:
        return
    lines = command.count("\n") + 1
    if lines > MAX_LINES:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"heredoc-guard: this command has a heredoc and {lines} lines (limit {MAX_LINES}). "
                    "Long heredocs break on quotes/backticks. Write file contents with the Write tool, "
                    "or write the script to the scratchpad with Write and run the file."
                ),
            }
        }))


main()
