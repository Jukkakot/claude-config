# Global Claude Instructions

Source: the public repo `Jukkakot/claude-config` (edit there, commit, push; cloud sessions install
it with `install.sh`). A project's own instructions override these.

## Language

Talk to the user in Finnish. Common English technical terms are fine where they are the usual
vocabulary (commit, merge, hook, build …). Code, identifiers, commit messages and specs stay in
English unless a project says otherwise.

## Documentation

Docs are a map for the AI, the code is the truth. In the user's hobby projects no human reads the
docs: keep in them what the code does not tell (where things live, why, decisions, how to run,
install and debug) and point to files for detail (thresholds, constants, field lists, pipeline
steps). Update a doc only when the map changes. Do NOT create new markdown files (analyses, TODO
summaries) unless asked.

## Committing

After any code change, commit before ending the turn: only the relevant files (no debug
screenshots or temp files), English message with a conventional prefix (feat:, fix:, refactor: …).
Run the project's cheap checks first (build, lint; e.g. `npm run build` for frontend). Don't push
unless the project's instructions or the user in this session allow it.

## Quick fixes (pikakorjaus)

A quick fix goes in as is (no tests, checks, UI check or OpenSpec change), still in its own commit.

- Qualifies: typos and wording, comments, docs/instruction files, config values, a style tweak, a
  one-line fix whose effect is obvious by reading, anything the user calls "pikana".
- Not: logic in rules, commands or state handling; behaviour across several files; dependency
  changes. When unsure, it is not a quick fix.
- Say it plainly in the reply: "Pikakorjaus: ei testattu, oletettu toimivaksi."
- In a repo with `openspec/`: commit trailer `Quick-fix: yes`; code edits need
  `touch ~/.claude/hooks/openspec-quick-fix` first (valid 30 min).

## OpenSpec (repos with `openspec/`)

Every change that is not a quick fix starts with `/opsx:propose` (the skill, not hand-written
files) before code is touched, and is implemented with `/opsx:apply`; also in autopilot and for
follow-ups found while testing. The hook `openspec-guard.py` denies code edits while no change is
active and commits with code but no `openspec/` file; when it denies, write the change.

Use OpenSpec in every phase, even when the user does not mention it:

- **Questions:** read the relevant `openspec/specs/`, `openspec/context/` and active changes first
  and answer from them (say when code and specs disagree). Open-ended thinking: `/opsx:explore`.
- **Decisions in conversation:** put them where they belong (new change, `/opsx:update`, roadmap or
  backlog), not only in the chat.
- **Implementing:** follow the change's tasks and tick them; fixes found while testing go into the
  change.
- **Finishing:** `/opsx:archive`, so the specs stay true.

**Specify first, then one-shot.** Specify a new change with the user until nothing that affects
behaviour or look is open: propose, then ask (numbered questions in text; the user often answers
by voice) and fold the answers in. Implementation starts only when the user agrees the spec is
complete.

**Scale the paperwork.** Small change (one area, no real design choices, an hour or two): a short
proposal and tasks, a delta spec only when behaviour changes, no `design.md`. Bigger change or real
choices: the full set. Group small related items into one change when that is cheaper.

## Testing (hobby projects)

Test where it pays:

- Logic (algorithms, rules, state, parsing) gets real tests.
- UI gets one or two smoke tests per screen. Never assert exact copy; for translations one test
  that a text changes with the language is enough. Spec scenarios don't each need a test.
- Screenshots only when a layout's look needs judging.
- The user's own use on the device is the real UI test: list what to try in the summary.
- When something fails in real use, ask for the log, a screenshot or what happened before fixing
  on a guess.

## Talking with the user

- Questions: numbered, in plain text (the user often answers by voice, often on a phone). Use the
  AskUserQuestion picker only when the user asks for it ("kysy multa …").
- **After planning or proposing:** a short summary the user can read on a phone: what will change,
  in a few lines, then the decisions the user needs to make (numbered, at most 3–5, one line each,
  recommendation first). No file lists or links unless asked; the user reads the reply, not the
  files.
- **After implementing:** what changed (what the user will notice), every decision taken on the
  user's behalf (so it can be corrected), open items. No "how to check" section, no file-by-file
  recap.

## Session economy

Every turn re-sends the whole context. At natural boundaries (a change proposed, implemented or
archived) judge whether the session is long and recommend **/compact** (work still needs this
session's details) or **a new session** (clean boundary, the repo and memory hold what the next
step needs; usually cheaper). With a new session, give a handover of a few lines to paste: commits
done, the exact next command, open questions, only what is not in the repo or memory. Don't switch
mid-task.

## Inconveniences and better ways of working

Note whatever slows or blocks the work (missing permission, awkward tool, flaky command, a step
that costs more than it gives). Raise it only when it has happened more than once and fixing it is
clearly worth it; keep raised ones in the project memory's `open-inconveniences.md` (in the repo's
`.claude/memory/` when it has one) with the user's
reaction, and repeat open ones at the end of summaries until the user reacts ("not now" items only
at handovers). Also suggest briefly any way to use fewer tokens or drop heavy steps, with the
expected saving; don't re-propose what the user declined.

## Known tool pitfalls

- Bash heredocs over ~30 lines or with many quotes/backticks fail ("unexpected EOF"); a hook
  (`heredoc-guard.py`) denies them. Write the script to the scratchpad with Write and run it; one
  Write call per file.
- After an interruption (continue, compacted context, handover): `git status --short` and
  `git diff --stat` first, and read changed tests' names, so finished work is not redone.
- Windows: write text files with LF line endings (Python: `newline='\n'`).
- Windows: Playwright MCP saves screenshots only under the workspace (e.g. `.playwright-mcp/`).
  Close the tabs you opened when a UI check is done.
- Cloud sessions: this file, the hooks and the skills come from `install.sh`; `~/.claude/projects/…`
  memory does not carry over. A repo with `.claude/memory/` keeps its project memory there (same
  file format, index `MEMORY.md`): read the index and write project memories there instead.

## UI work

Before any UI change or audit, load the `ui` skill (principles, light/dark theme, cheap checks).
Games made from game-kit also have a `game-ui` skill.

## Reusable building blocks (low priority)

The user enjoys reusable pieces across projects (game-kit: Colyseus server, lobby, bots, CI,
logging; Claude/OpenSpec setup: `claude-config`). When something looks generally reusable, say so
briefly and suggest where it could live; keep such code free of project names where it costs
nothing. Don't build the shared thing unasked.
