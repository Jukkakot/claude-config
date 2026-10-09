#!/usr/bin/env bash
# Installs the global Claude config into ~/.claude: CLAUDE.md, hooks, skills, and the hook entries
# in settings.json (other settings are kept). Safe to run again; used by cloud sessions' setup
# script and locally after editing this repo (Git Bash on Windows).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dest="${CLAUDE_HOME:-$HOME/.claude}"
# First Python that really runs (on Windows python3 may be the Microsoft Store stub).
py=""
for candidate in python3 python /c/Python313/python.exe; do
  if "$candidate" -c "" >/dev/null 2>&1; then py="$candidate"; break; fi
done
[ -n "$py" ] || { echo "No working Python found" >&2; exit 1; }

mkdir -p "$dest/hooks" "$dest/skills"
cp "$here/CLAUDE.md" "$dest/CLAUDE.md"
cp "$here"/hooks/*.py "$dest/hooks/"
for skill in "$here"/skills/*/; do
  name="$(basename "$skill")"
  rm -rf "$dest/skills/$name"
  cp -r "$skill" "$dest/skills/$name"
done
"$py" "$here/tools/install_settings.py" "$dest"
echo "claude-config installed into $dest"
