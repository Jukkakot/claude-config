#!/usr/bin/env bash
# Installs the global Claude config into ~/.claude: CLAUDE.md, knowledge.md, hooks, skills, and the hook entries
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
cp "$here/knowledge.md" "$dest/knowledge.md"
cp "$here"/hooks/*.py "$dest/hooks/"
for skill in "$here"/skills/*/; do
  name="$(basename "$skill")"
  rm -rf "$dest/skills/$name"
  cp -r "$skill" "$dest/skills/$name"
done
"$py" "$here/tools/install_settings.py" "$dest"

# Cloud containers: Maven Central answers 429 there (rubikki-solveri, terveyslappu), so Gradle and
# Robolectric try Google's mirror of it first. Builds that read `robolectricRepoUrl` pass it on as
# Robolectric's `robolectric.dependency.repo.url`. Never on the local PC.
if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || [ -d /root/.ccr ]; then
  mirror="https://maven-central.storage-download.googleapis.com/maven2/"
  mkdir -p "$HOME/.gradle/init.d"
  cat > "$HOME/.gradle/init.d/central-mirror.gradle.kts" <<EOF
// Written by claude-config install.sh (cloud only): Maven Central is rate-limited here.
beforeSettings {
    pluginManagement.repositories { maven("$mirror") }
    dependencyResolutionManagement.repositories { maven("$mirror") }
}
EOF
  props="$HOME/.gradle/gradle.properties"
  grep -q '^robolectricRepoUrl=' "$props" 2>/dev/null || echo "robolectricRepoUrl=$mirror" >> "$props"
fi
echo "claude-config installed into $dest"
