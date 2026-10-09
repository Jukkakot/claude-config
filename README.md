# claude-config

Jukka's global Claude Code setup, shared by the local machine and cloud sessions.

| Path | Installed to | What |
|---|---|---|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Global instructions for every project |
| `hooks/` | `~/.claude/hooks/` | `openspec-guard.py` (OpenSpec first), `heredoc-guard.py` (long heredocs) |
| `skills/` | `~/.claude/skills/` | `ui` (UI principles, theme, cheap checks), `quickshare` (Samsung Quick Share downloads) |
| `tools/install_settings.py` | `~/.claude/settings.json` | Adds the hook entries; other settings are kept |

## Install

```sh
./install.sh            # locally (Git Bash) after editing this repo
```

Cloud environment (claude.ai → Code → environment settings → Setup script):

```sh
git clone --depth 1 https://github.com/Jukkakot/claude-config /tmp/claude-config && bash /tmp/claude-config/install.sh
```

Edit here, never in `~/.claude` directly (the next install overwrites it). Per-project memory
(`~/.claude/projects/`) is not part of this repo.
