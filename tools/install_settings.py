"""Puts this repo's hooks into <claude home>/settings.json, keeping every other setting.

Hook entries pointing at a script of the same name are replaced, so running it again is safe.
The interpreter is the one running this script (python3 in the cloud, C:/Python313 locally).
"""
import json
import os
import sys

HOOKS = [
    ("PreToolUse", "Bash", "heredoc-guard.py", 10),
    ("PreToolUse", "Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell", "openspec-guard.py", 10),
    ("SessionStart", "startup", "config-refresh.py", 120),
]


def main(dest: str) -> None:
    path = os.path.join(dest, "settings.json")
    settings = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            settings = json.load(f)
    python = sys.executable.replace("\\", "/")
    hooks = settings.setdefault("hooks", {})
    names = {script for _, _, script, _ in HOOKS}

    def ours(entry: dict) -> bool:
        text = json.dumps(entry)
        return any(name in text for name in names)

    for event in {event for event, _, _, _ in HOOKS}:
        hooks[event] = [e for e in hooks.get(event, []) if not ours(e)]
    for event, matcher, script, timeout in HOOKS:
        hook_path = os.path.join(dest, "hooks", script).replace("\\", "/")
        hooks[event].append({
            "matcher": matcher,
            "hooks": [{"type": "command", "command": python, "args": [hook_path], "timeout": timeout}],
        })
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1])
