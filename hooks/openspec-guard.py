"""PreToolUse hook: keep OpenSpec ahead of the code in repos that use it.

Applies only inside a repo that has an openspec/changes/ directory.

- Edit/Write/MultiEdit/NotebookEdit of a code file is denied while no OpenSpec change is active
  (a folder in openspec/changes/ other than archive/ with a proposal.md), unless a fresh
  quick-fix marker exists: ~/.claude/hooks/openspec-quick-fix, younger than QUICK_FIX_MINUTES.
- Bash `git commit` is denied when the working tree has code changes but no changed openspec/
  file and no active change, unless the command carries a "Quick-fix: yes" trailer.

Every denial is logged to openspec-guard.log (JSON lines).
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

QUICK_FIX_MINUTES = 30
CODE_EXT = {
    ".kt", ".kts", ".java", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".go", ".rs",
    ".swift", ".cs", ".vue", ".svelte", ".css", ".scss", ".html",
}
FREE_DIRS = ("openspec/", "docs/", ".claude/", ".github/")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openspec-guard.log")
MARKER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openspec-quick-fix").replace("\\", "/")


def repo_root(start: str):
    d = os.path.abspath(start)
    if not os.path.isdir(d):
        d = os.path.dirname(d)
    while True:
        if os.path.isdir(os.path.join(d, "openspec", "changes")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def active_changes(root: str):
    changes = os.path.join(root, "openspec", "changes")
    return [
        name for name in os.listdir(changes)
        if name != "archive" and os.path.isfile(os.path.join(changes, name, "proposal.md"))
    ]


def is_code(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    if rel.startswith(FREE_DIRS) or rel.endswith(".md"):
        return False
    ext = os.path.splitext(rel)[1].lower()
    return ext in CODE_EXT or (ext == ".xml" and "/src/" in "/" + rel)


def quick_fix_marker() -> bool:
    marker = MARKER
    return os.path.isfile(marker) and time.time() - os.path.getmtime(marker) < QUICK_FIX_MINUTES * 60


def deny(reason: str, data: dict, root: str) -> None:
    try:
        with open(LOG, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({
                "ts": datetime.now().isoformat(timespec="seconds"),
                "session": data.get("session_id"),
                "repo": root,
                "tool": data.get("tool_name"),
                "reason": reason[:160],
            }) + "\n")
    except Exception:
        pass
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


def check_edit(data: dict) -> None:
    path = (data.get("tool_input") or {}).get("file_path") or (data.get("tool_input") or {}).get("notebook_path")
    if not path:
        return
    root = repo_root(path)
    if not root:
        return
    rel = os.path.relpath(os.path.abspath(path), root).replace("\\", "/")
    if rel.startswith("..") or not is_code(rel):
        return
    if active_changes(root) or quick_fix_marker():
        return
    deny(
        f"openspec-guard: {rel} is code, and this repo has no active OpenSpec change. "
        "Create the change first (/opsx:propose <name>) and edit after its proposal exists. "
        f"If this really is a quick fix (see CLAUDE.md), touch {MARKER} "
        f"(valid {QUICK_FIX_MINUTES} min) and say so to the user.",
        data, root,
    )


def check_commit(data: dict) -> None:
    command = (data.get("tool_input") or {}).get("command") or ""
    if not re.search(r"\bgit\b[^\n;&|]*\bcommit\b", command):
        return
    if re.search(r"quick-fix:\s*yes", command, re.IGNORECASE):
        return
    root = repo_root(data.get("cwd") or os.getcwd())
    m = re.search(r"\bgit\s+-C\s+(\"[^\"]+\"|'[^']+'|\S+)", command)
    if m:
        root = repo_root(m.group(1).strip("\"'")) or root
    if not root or active_changes(root):
        return
    try:
        out = subprocess.run(
            ["git", "-C", root, "status", "--porcelain", "-uall"],
            capture_output=True, text=True, timeout=5,
        ).stdout
    except Exception:
        return
    paths = [line[3:].split(" -> ")[-1].strip('"') for line in out.splitlines() if len(line) > 3]
    code = [p for p in paths if is_code(p)]
    spec = [p for p in paths if p.replace("\\", "/").startswith("openspec/")]
    if code and not spec:
        deny(
            "openspec-guard: this commit has code changes (" + ", ".join(code[:3])
            + ("…" if len(code) > 3 else "") + ") but no OpenSpec change. Write the change "
            "(/opsx:propose) and commit it with the code, or, for a quick fix (see CLAUDE.md), "
            "add the trailer line 'Quick-fix: yes' to the commit message.",
            data, root,
        )


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    tool = data.get("tool_name")
    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        check_edit(data)
    elif tool in ("Bash", "PowerShell"):
        check_commit(data)


if __name__ == "__main__":
    main()
