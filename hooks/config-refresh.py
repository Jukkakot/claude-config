"""SessionStart hook (cloud only): reinstall the newest claude-config at every session start.

A cloud environment's setup script runs only when its container is built fresh; cached containers
keep the config of that build, so sessions can start with weeks-old instructions (seen
2026-11-14). This hook clones the repo again and runs install.sh. If the global CLAUDE.md changed,
it tells the model to read it again, since the copy loaded at start may be the old one.
Never fails the session: any error prints one line and exits 0.
"""
import filecmp
import os
import shutil
import subprocess
import sys
import tempfile

REPO = "https://github.com/Jukkakot/claude-config"


def cloud() -> bool:
    return os.environ.get("CLAUDE_CODE_REMOTE") == "true" or os.path.isdir("/root/.ccr")


def main() -> None:
    sys.stdin.read()  # hook input, unused
    if not cloud():
        return  # locally the user runs install.sh after editing the repo
    home = os.environ.get("CLAUDE_HOME", os.path.expanduser("~/.claude"))
    installed = os.path.join(home, "CLAUDE.md")
    work = tempfile.mkdtemp(prefix="claude-config-")
    try:
        src = os.path.join(work, "repo")
        subprocess.run(["git", "clone", "-q", "--depth", "1", REPO, src], check=True, timeout=60,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        old = os.path.exists(installed) and filecmp.cmp(installed, os.path.join(src, "CLAUDE.md"), shallow=False)
        subprocess.run(["bash", os.path.join(src, "install.sh")], check=True, timeout=60,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        rev = subprocess.run(["git", "-C", src, "rev-parse", "--short", "HEAD"], capture_output=True,
                             text=True, timeout=10).stdout.strip()
        if not old:
            print(f"claude-config refreshed to {rev}: the global instructions changed at session start. "
                  f"Read {installed} now and follow it instead of any older copy loaded earlier.")
    except Exception as e:  # noqa: BLE001 - a hook must never block the session
        print(f"claude-config refresh failed ({type(e).__name__}); global instructions may be stale.")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
