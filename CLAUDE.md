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

**README for people (user, 2026-11-09):** the one exception: every project has a short, friendly
`README.md` at the repo root for a human visitor: what the app is, what it does, how it is used and
installed, the stack in a line. Light and timeless: no feature lists that go stale, no internals
(those live in the AI docs), so it rarely needs touching; update it only when the app's purpose or
the way to get it changes. Add one when a project has none (new projects from the start; existing
ones only when worked on, not as a sweep).

## Knowledge bank

Every project has a `knowledge.md` (`openspec/context/knowledge.md` in OpenSpec repos, else at the
repo root; create it with the first finding): general topic knowledge the project relies on, with
sources; no configuration, versions or other things that go stale. Knowledge that holds in any
project goes to the global bank `~/.claude/knowledge.md` (source: `knowledge.md` in claude-config;
add there, commit, push).

- **Never read either file whole.** Both start with an index; find the topic there
  (`grep -n '^## '`) and read only that section.
- **Before researching** a topic (web search, docs, trial), read its section in both files first.
- **After researching**, add what was learnt with its source to the right file and keep its index
  in step.

## Committing

After any code change, commit before ending the turn: only the relevant files (no debug
screenshots or temp files), English message with a conventional prefix (feat:, fix:, refactor: …).
Run the project's cheap checks first (build, lint; e.g. `npm run build` for frontend). Then push
to the default branch (`main`) in every session, local or cloud (user, 2026-10-09), unless the
project's instructions say otherwise. This overrides a cloud session's "develop on branch
claude/…" instruction: work on that branch if you like, but also `git push origin HEAD:main`
(fast-forward; on rejection fetch and rebase first). No pull requests unless asked.

**CI minutes (user, 2026-10-26):** no CI run without a reason. A workflow on push skips
docs-only changes (`paths-ignore` for specs, design files, `.claude/**`, `**/*.md`); add this when
creating or touching a workflow, and flag any other needless runs (duplicate triggers, jobs that
redo what another job did).

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
behaviour or look is open: propose, run the `spec-review` skill (rubber-duck review and the
question format), ask, and fold the answers in. Implementation starts only when the user agrees
the spec is complete. Don't hurry to implementation (user, 2026-11-14): the aim is a spec a
Sonnet implementer gets right in one go.

**Scale the paperwork.** Small change (one area, no real design choices, an hour or two): a short
proposal and tasks, a delta spec only when behaviour changes, no `design.md`. Bigger change or real
choices: the full set. Group small related items into one change when that is cheaper.

## Libraries first (user, 2026-11-09)

Before writing a feature yourself (a file format reader, a chart, a parser, a protocol), look for a
maintained library and use it when one exists; recommend it in the proposal. A library brings its
other features for free and is already tested; hand-written code needs its own tests and still
breaks. Size is not a reason to write it yourself: choose between libraries (lighter or fuller) on
fit, maintenance and licence. Write it yourself only when no suitable library exists, and say why.

## Testing (hobby projects)

Test where it pays:

- Logic (algorithms, rules, state, parsing) gets real tests.
- UI gets one or two smoke tests per screen. Never assert exact copy; for translations one test
  that a text changes with the language is enough. Spec scenarios don't each need a test.
- Screenshots only when a layout's look needs judging.
- The user's own use on the device is the real UI test. They ask what to try when they want to:
  no "try on the phone" lists in summaries, no phone-check tasks, and nothing waits for a
  device check (archive a change once it is merged and green) (user, 2026-10-29).
- When something fails in real use, ask for the log, a screenshot or what happened before fixing
  on a guess.

## Talking with the user

- **Phone first (user, 2026-11-14):** the user reads over 90 % of replies on a narrow phone
  screen. Short paragraphs and lines, bullets over long sentences; avoid wide tables and ASCII
  diagrams wider than about 40 characters (a list reads better). Question layout: `spec-review`.
- **Short by default (user, 2026-11-14):** the user reads little. Lead with the answer or the
  decision needed, cut background they did not ask for, prefer five lines to fifteen; detail only
  on request. Suggest any way to shorten what the user has to read.
- **Push when the user is needed (user, 2026-11-14):** whenever nothing more will happen until the
  user acts (all work done, a failure, a question that blocks), send a PushNotification (one
  line, what to act on) as the turn ends. The tool skips it while the user is active in the
  session. Not for routine progress.
- Questions: numbered, in plain text (the user often answers by voice, often on a phone). Use the
  AskUserQuestion picker only when the user asks for it ("kysy multa …").
- **After planning or proposing:** a short summary the user can read on a phone: what will change,
  in a few lines, then the decisions the user needs to make (numbered, at most 3–5, one line each,
  recommendation first). No file lists or links unless asked; the user reads the reply, not the
  files.
- **Before a round of look or design options:** ask in one line what situation it is for and what
  bothers the user in the current one, unless they already said. Options built on the real need
  land in one round (user, 2026-10-29).
- **After implementing:** what changed (what the user will notice), every decision taken on the
  user's behalf (so it can be corrected), open items. No "how to check" section, no file-by-file
  recap.
- **Version number (user, 2026-11-14):** whenever a reply says something is installed,
  released or ready to try, name the exact version it is in (e.g. "v1.19.3"), taken from the
  release or build, never guessed.

## Subagent models

Pick the cheapest model that does the task well (`model` on the Agent call; a fork always runs on
the parent's model). Say the choice in one line when spawning.

- **haiku:** mechanical work with no judgement: file searches and read-only sweeps, regenerating
  output from given data, moving rows, renames.
- **sonnet (default):** clear briefs: implementing a well-specified change from its tasks, mockups
  from a brief, folding decided answers into specs, writing tests.
- **opus:** judgement: unclear design, architecture, reviews and audits, hard logic (sync,
  offline merge, concurrency), merge conflicts, a final check before main.

If a cheaper agent fails or its report looks off, rerun that task on the next model up rather
than starting every task on the expensive one.

Weigh the price of a bug, not only of tokens (user, 2026-11-14): a bug that only shows on the
user's device costs a test round, a log share and a fix, more than the Opus-Sonnet difference.
So implementation that the session cannot test (device hardware such as Bluetooth, background
work and OS power rules, OS lifecycle, real external services) goes to **opus**; logic covered by
unit tests and plain UI from a complete spec goes to **sonnet**. Give the reason in the one line.

## Master session (user, 2026-10-25, global 2026-11-14)

Development runs from one master session that talks with the user and starts subagents; every
session is the master unless the user says otherwise. Subagents run in the background, so the
user can specify and plan with the master while they work:

- One subagent per task (an OpenSpec change to apply, a mockup round, research), started with
  `isolation: "worktree"`; it works and commits on its own worktree branch, never pushes, and
  reports back: what it did, decisions taken, questions for the user (subagents cannot ask).
- Run in parallel only tasks that touch different files; tasks on the same change, the same code
  area or the same `openspec/context/` files run one after another.
- The master merges each finished branch into `main` (rebase onto current `main` first; rerun the
  checks only when the merge needed conflict resolution), pushes, deletes the branch, and relays
  the questions to the user. This is the only exception to "commit straight to `main`".
- The master keeps its own context small: it reads reports, not transcripts, and does no
  implementation itself.
- Each worktree has its own build output; mind a cloud session's disk allowance with more than two
  at once.

After merging an agent's branch without conflicts, trust its check run and CI; rerun the checks
locally only when the merge needed conflict resolution (user, 2026-10-29). Agents commit early and
often: a crash or a usage limit loses uncommitted worktree work.

## Session economy

Every turn re-sends the whole context. At natural boundaries (a change proposed, implemented or
archived) judge whether the session is long and recommend **/compact** (work still needs this
session's details) or **a new session** (clean boundary, the repo and memory hold what the next
step needs; usually cheaper). With a new session, give a handover of a few lines to paste: commits
done, the exact next command, open questions, only what is not in the repo or memory. Don't switch
mid-task. Put the handover (and any prompt meant for another session) alone in one fenced code
block, so the app's copy button copies exactly it (user, 2026-11-09).

Once a handover is given, the old session asks nothing more: new questions go to the project's
question file (or the handover's "Huom" line), work still running in the background is named
there too, and the reply says the next session picks them up. The user can switch right away
(user, 2026-10-29).

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
