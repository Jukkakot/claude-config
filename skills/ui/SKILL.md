---
name: ui
description: UI principles, default taste, light/dark theme rules, design process and a design-pass checklist for the user's projects. Load before any UI change (a screen, component, layout, style or copy), a UI audit or polish, or a theme decision.
---

# UI work

For a new screen or flow also read `references/guidelines.md` (conventions table, evidence with
sources, competitor patterns, common mistakes).

## Theme

- Every project has a clear theme (a visual concept: materials, palette, shapes), agreed early and
  recorded in the project's docs/specs; new UI and copy stay consistent with it. Don't imitate the
  look of an existing commercial product.
- Every project has a **light and a dark theme**. By default the UI follows the system
  (`prefers-color-scheme`); a light/dark/system choice in settings overrides it.
- Use the platform's base theme first when it brings a good light/dark one (Material 3 on Android,
  a component library's theme) and add only what the project needs. A custom theme with mockups
  (both variants) is worth it mainly for web apps and games.

## Default taste (the user's recurring wishes; a project may override)

- **Dense by default** for reading, list and overview screens on mobile: more visible at once, no
  airy "demo UI". Roomier only where the user acts on the move or one-handed (e.g. a shopping
  mode); density is a per-project/per-screen decision, raise it when unsure.
- **Visual, not generic:** colour and character from the first proposal; never a grey stack of
  equal cards. Readability before decoration (no hard-to-read display fonts).
- **Symbols over prose, lazy readers:** navigation and rare actions get icon + short label;
  repeated row actions (tick, star, ⋯) icon only, with an accessible name. Status shows as text or
  shape too, not colour alone.
- **Few taps in daily use:** a tap does the thing, no "Add to list" step; stay on the current tab.
  But never lose clarity: no destructive action without Undo, no hidden auto-choice (show the
  value), no gesture without a visible alternative.
- **Undo, not confirmation or popups.** Confirm only the irreversible and large, naming the
  consequence on the buttons.
- **Rare things hidden but findable** (settings, stats, technical info, maintenance modes off by
  default) behind a visible, named opener.
- **Thumb reach:** daily actions low or central, input at the bottom, primary "+" bottom right.
- **Quiet help:** suggestions appear when relevant, each dismissible; nothing interrupts.
- **Consistent:** the same concept looks the same everywhere. New patterns must match existing
  ones in the app; prefer extending an existing pattern over adding a new one. One word, one
  meaning across features (keep a short glossary in the project's context when words collide).
- **Modern, minimal, no clutter** (no gimmicks like emoji reactions).

## Principles

Apply on every UI change; for an audit or polish, run through them before and after.

- **State legibility:** the user can always answer: what is happening, what can I do, what happened
  last. Never clip elements at container edges unless intended; check mobile portrait, landscape
  and desktop narrow.
- **Findability:** 3-5 main destinations visible (bottom bar/tabs), no hamburger for daily use;
  hiding max 2 levels; names predict content (not "More"/"Other"); one home for a secondary item;
  home answers "what do I do now" (no menu page); state is saved, the user returns to the same
  place.
- **Conventions:** use the platform's expected pattern for add, delete, undo, reorder, back,
  close, settings, share (table in the reference); deviate only when clearly better, and then
  explain. A familiar gesture keeps its meaning everywhere; swipe only for deleting/revealing,
  same direction everywhere. Familiar icons keep their meaning (⋯ more, gear settings, ≡ drag).
- **Few taps, clear result:** feedback within 100-150 ms (pressed state), result visible at once;
  wait indicator by duration (<100 ms none, 0.1-1 s hint, 1-10 s spinner, >10 s progress bar);
  button names state the result; do not disable without reason (explain what is missing);
  no silent changes (say when another user or the system changed something).
- **Focus/hierarchy:** one primary action per screen (filled primary colour only there); max 3
  size levels and 2 big elements; text in 2-3 shades and 2 weights; most important word first in
  a row; rare/maintenance actions visually quiet; one banner at a time.
- **Visual craft:** spacing scale 4/8/12/16/24/32/48, smaller gap inside a group than between
  groups; 5-6 type sizes, body 16 px, secondary 14, min 12; weights 400/600; no ALL CAPS in
  tabs/buttons; colours as roles/tokens with predefined scales (no lighten()/darken()); one colour
  = one meaning; no grey text on coloured backgrounds; depth by surface tone, shadow only for
  floating elements; dark theme is dark grey not #000, with its own contrast check; do not enlarge
  small icons (put them in a coloured tile).
- **Mobile:** touch targets >= 44x44 px (absolute floor 24x24 CSS px), >= 8 px between them,
  larger in corners and for the primary action; input font >= 16 px, right `inputmode`,
  keyboard must not cover the field; `env(safe-area-inset-*)`, `100dvh`; no targets in system
  gesture zones; sheets for short contextual tasks only, never sheet on sheet, with a visible
  close button plus back, drag down and backdrop tap.
- **Layers:** a modal layer (sheet, dialog) covers or hides persistent chrome (tab bar, FAB, undo
  line); `inert` alone hides the bug from tests while taps still land on the chrome, so hit-test
  the topmost element at the sheet's last row.
- **No nested targets in a moving context:** never put a secondary button (star, chip, toggle)
  inside a whole-row tap target where the user acts on the move; give it a fixed column at the
  row edge or make it a non-interactive marker.
- **Accessibility:** contrast 4.5:1 text, 3:1 large text, icons and states, in both themes; state
  never by colour alone; visible focus ring; focus moves sensibly after delete; add/remove
  announced via `role="status"`; row buttons named with the item ("Delete milk"), always visible;
  reduced motion honoured; every gesture has a keyboard/visible alternative.

## Design process

1. Mood/style board (3 moods: colour, font, shapes) before the first screens: **ask per project,
   every time**; never start it automatically.
2. Per new screen show **2-3 clearly different alternatives** (different layout, density or
   visual approach, not variations of one), recommendation marked with a one-line reason; name
   1-2 real apps the pattern comes from and what was taken (do not copy the look).
3. Mockups use real content: realistic names, 15+ rows, longest name, empty state, both themes,
   360x780 first, then the smallest and largest width.
4. Ask about look only with a picture. Judge by what users can do, not by how nice it looks.
   Before asking, check the mockup's fidelity: one frame per theme against a screenshot of the
   built app (same controls, tiles, cards in light and dark), or the user chooses on a wrong
   picture.
5. Run the design pass below, fix, and tell the user in one short line ("korjattu
   itsekritiikissä: ..."), not the whole list.
6. After implementing, compare a screenshot of each new screen with the mockup.

## Design pass (before every mockup or UI change)

1. Daily actions visible (not in a menu); 3-5 main items; hiding <= 2 levels, opener named.
2. Each ordinary task follows the conventions table; any deviation justified.
3. Names predict content; no "More"/"Other".
4. Core-path taps counted; extra ones removed; auto-chosen values shown.
5. Every button has a result-telling name or a universal icon with accessible name.
6. Pressed state, immediate result, wait indicator matching duration.
7. Undo instead of confirmation, Undo stays visible long enough; confirm only irreversible.
8. No silent changes; every gesture has a visible alternative.
9. One primary action, filled only there; rare actions quieter.
10. <= 3 size levels, <= 2 big elements; key word first; squint test passes with real content.
11. Main content central, daily action low/central, dangerous action apart.
12. Spacing, type sizes and colours from scales/tokens.
13. Colour and icons purposeful, one colour one meaning; not a grey card stack.
14. Density fits the screen's use (>= ~10 list rows visible on a reading/list screen).
15. Depth by surface tone, shadow only on floating elements.
16. Targets >= 44 px, gaps >= 8 px, input font >= 16 px, safe area, no gesture-zone targets.
17. Sheets: close button + back + drag down; none on top of another; nothing persistent drawn
    over them.
17b. No secondary button nested in a whole-row tap target on move-heavy screens.
18. Contrast and state cues in both themes; focus visible and moved sensibly.
19. States covered: empty, loading, error, offline, long name, long list, pressed, selected, disabled.
20. Seen in both themes, at 360 px and at 200 % text size: no mid-word breaks, titles keep ~8+
    characters, header actions wrap or turn icon-only, fixed chrome (checkbox, tile) does not
    grow with rem. Automate it so a test fails on these, not only on clipping.
21. New patterns match existing ones in the app (extend before adding).

## Checking cheaply

Screenshots cost many tokens. Verify facts (text shown, button enabled, no horizontal scroll,
sizes) with an accessibility snapshot or a short DOM query; take a screenshot only where the look
needs judging (a new screen, a layout change), usually one per state.
