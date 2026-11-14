---
name: spec-review
description: How a change is specified with the user before any implementation, including the rubber-duck review (a fresh-context reviewer that hunts for what the spec leaves open) and the question format for the user. Use after drafting a change (e.g. /opsx:propose) and before telling the user it is ready, whenever the change adds or changes behaviour the user notices; also when an implementer reports something the spec did not settle.
---

# Spec review

Goal (user, 2026-11-14): a spec so complete that a Sonnet implementer gets it right in one go,
with as little work for the user as possible. The user is the specifier; the master drives. The
user decides what matters to them; the master decides the rest and says so. Do not hurry to
implementation: a few more minutes of specifying is cheaper than a phone test round and a fix.

## When to run the rubber duck

Run it for every change that adds or changes behaviour or look the user notices (a new feature, a
changed rule, a new screen or setting), and for any change touching what cannot be tested in the
session (device hardware, background work, OS power rules, real accounts).

Skip it for quick fixes, a bug fix that restores already specified behaviour, refactors with no
behaviour change, docs and config. When unsure, run it: it costs one review, a missed question
costs a round on the device.

## Flow

1. Draft the change (proposal, delta specs, tasks; design when there are real choices) from what
   the user said and the existing specs.
2. Rubber duck: spawn one **opus** subagent, read-only, with a fresh context. Give it only the
   paths of the change, the specs it touches and the project context files, never the chat or
   your own reasoning (it must not inherit your assumptions). Brief it to:
   - read the change as an implementer who cannot ask anything;
   - list every point where two reasonable implementers would build different things:
     edge cases, errors and failures, empty and first-run states, permissions, timing and
     lifecycle (background, restart, offline), data migration and old data, what the UI shows in
     each state, wording that is vague ("quickly", "when needed"), conflicts with existing specs,
     requirements that cannot be tested;
   - for each: the question, why it matters, a recommended answer, and whether it affects
     behaviour or look the user would notice (`user`) or is an internal choice (`internal`);
   - report as a list, at most about 15 points, most important first; no rewrite of the spec.
3. Triage the report yourself:
   - `user` points that change what the user sees or how the app behaves: ask the user.
   - `internal` points and low-impact `user` points with an obvious answer: decide, write the
     decision into the change, list it in the reply as "päätin puolestasi".
   - Points the specs already answer: drop.
4. Ask the user (format below), fold the answers into the change, and repeat step 2 only if the
   answers opened something new and big.
5. The spec is done when nothing that affects behaviour or look is open and the user agrees.
   Only then implementation starts (subagent per the model rules in the global CLAUDE.md).

## Questions to the user

The user answers by voice, often on a phone. Each round:

- At most 5 to 7 questions, numbered, one or two lines each, the most important first.
- Each question names the options with letters, the recommended one first and marked:
  `3. Mitä tehdään kun X? (a) Y, suositus (b) Z`
- Yes/no questions say the default: `4. Näytetäänkö X? kyllä/ei, suositus kyllä`
- The user may answer "1a, 2b, loput suositukset" or "kaikki suositukset".
- Before the questions: what the change does in a few lines. After: the "päätin puolestasi" list,
  one line each, so the user can correct any of them.
- No file lists or links.
- More than 7 open points: ask the most important now, decide or defer the rest, and say so.

## During implementation

The implementer does not decide what the spec left open in behaviour or look. It picks the
simplest reasonable option only to keep going, writes it into the change (design or tasks note)
and lists it in its report. The master relays such points to the user as questions in the format
above, or as "päätin puolestasi" when they are minor; the answers go into the change and, if
needed, a follow-up task.
