"""Puts this repo's hooks into <claude home>/settings.json, keeping every other setting.

Hook entries pointing at a script of the same name are replaced, so running it again is safe.
The interpreter is the one running this script (python3 in the cloud, C:/Python313 locally).
"""
import json
import os
import sys

HOOKS = [
    ("Bash", "heredoc-guard.py"),
    ("Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell", "openspec-guard.py"),
]


def main(dest: str) -> None:
    path = os.path.join(dest, "settings.json")
    settings = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            settings = json.load(f)
    python = sys.executable.replace("\\", "/")
    pre = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    names = {script for _, script in HOOKS}

    def ours(entry: dict) -> bool:
        text = json.dumps(entry)
        return any(name in text for name in names)

    pre[:] = [e for e in pre if not ours(e)]
    for matcher, script in HOOKS:
        hook_path = os.path.join(dest, "hooks", script).replace("\\", "/")
        pre.append({
            "matcher": matcher,
            "hooks": [{"type": "command", "command": python, "args": [hook_path], "timeout": 10}],
        })
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1])
