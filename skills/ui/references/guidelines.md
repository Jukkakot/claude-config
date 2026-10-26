# UI guidelines: reference

Read when designing a new screen or flow. Rules are in `../SKILL.md`; this file holds the
conventions table, evidence with sources and common mistakes. Source tags in [brackets] are listed
at the end. Numbers marked * come from memory or secondary sources.

Jakob's law: users spend most of their time in other apps, so expectations come from there; use a
new pattern only when clearly better, and explain it [NNg-mental]. Fluent: use platform patterns
~80 % of the time, save originality for signature features [Fluent-principles].

## Conventions table

| Task | Conventional pattern | Source |
|---|---|---|
| Add new | Android: FAB bottom right, 16 dp margin. iOS: "+" in toolbar or row at list end. Web/PWA: fixed field at the bottom or "+" | [M3-FAB] [HIG-layout]* |
| Add several in a row | Field stays open and clears on Enter; suggestions above/below the field | [Sweet-AnyList] [Inclusive-todo] |
| Tick done | Tap the checkbox/row; strike-through and move to a "done" section at the bottom | [Inclusive-todo] [Keep-jefftk] |
| Delete | Swipe left + visible alternative (⋯ or edit mode); Undo snackbar at once | [HIG-gestures] [NNg-swipe] [M3-snackbar] |
| Undo | Snackbar at the bottom, single "Undo" action, above FAB/bottom bar, a new one replaces the old | [M3-snackbar] [NNg-control] |
| Reorder | Drag handle (≡) at row end or edit mode; long-press + drag as shortcut | [HIG-lists] [HIG-gestures] |
| Row extras | Long-press as shortcut; visible ⋯ on the row or in the detail view | [HIG-gestures] [NNg-contextmenu] |
| Switch list/space | Bottom bar 3-5 items (icon + name); other lists via one list view or a dropdown in the header | [M3-navbar] [NNg-navi] |
| Settings | Own view, gear or "Settings"; grouped list, switches apply at once (no Save button) | [HIG-color]* [NNg-control] |
| Share/invite | System share sheet (Web Share API) with a link; sharing per account, revocable | [Sweet-AnyList] [MUO-Bring] |
| Search | Magnifier is one of the few universal icons; one search field per view | [NNg-ikonit] [NNg-mental] |
| Back | Android back closes the topmost layer (dialog, panel, view); at root it exits; never jumps up the hierarchy | [Android-back] [NNg-mental] [NNg-control] |
| Close a sheet | Drag down, backdrop tap, back AND a visible "×"/"Close" | [NNg-sheet] [HIG-sheets] [M3-sheet] |
| Refresh | Pull down at the list top (if data does not sync by itself) | * |
| Cancel a form | "Cancel" left, "Done" right (iOS); ask about unsaved changes | [HIG-sheets] |

Gestures and icons: do not give a familiar gesture a private meaning (tap = select/open, swipe =
scroll/close/reveal actions); swipe for delete only, same direction everywhere, no horizontal
swipe from the screen edge (collides with back) [HIG-gestures] [NNg-swipe] [Android-back]. Icons:
⋯ more, gear settings, ≡ drag/menu, heart or star = favourite (not both with different meanings)
[NNg-ikonit]. Context menu (⋯): only this item's actions, most used on top, under ~10 entries, one
submenu level, inactive entries dimmed not hidden; ⋯ or ▾, not gear or hamburger [NNg-contextmenu].

## Evidence and numbers

**Findability**
- Hidden navigation measurably hurts discoverability [NNg-hamburger]; usage collapsed when hidden
  and rose when made visible in LukeW's cases (Polar, Zeebox, Facebook, Redbooth) [LukeW-hidden].
  Hamburger only for browse-heavy apps with many destinations.
- Progressive disclosure: max 2 levels; the opener's name says what is behind it [NNg-progressive].
- Home as a "navigation hub" (front page = menu) only when one session = one task [NNg-navi].
- Mobile sessions are short and interrupted (~72 s vs. 150 s on desktop): always save state
  [NNg-mobileUX]. Names: information scent [NNg-scent] [NNg-tabs].
- Autocomplete on mobile: 4-8 suggestions, predicted part highlighted [Baymard-autocomplete].

**Feedback and control**
- Feedback < 100-150 ms with a pressed state [NNg-buttonstates] [NNg-status]. Wait indicators
  by duration (none / hint / spinner / progress bar at 10 s) [Strom-density].
- Undo before confirmation; confirm only the irreversible and large, name the object and the
  consequence on the buttons ("Delete list" / "Keep"), no default choice [NNg-confirm]
  [GOVUK-button]. Destructive Undo should stay until the next action or move, not vanish in
  seconds; not shake-only [NNg-control] [M3-snackbar].
- Flat, text-like targets took 22 % longer to find and 25 % more fixations: buttons look like
  buttons, links differ from text [NNg-flat].
- Icons: if meaning needs > 5 s of thought, add text ("5-second rule") [NNg-ikonit].
- Where fewer taps hurts understanding (do not trim): destructive without Undo; effects visible
  elsewhere (other user, notification); gesture-only; invisible auto-choice [NNg-swipe]
  [NNg-status] [HIG-gestures]. Preview before committing when the outcome is unclear ("Add 6
  ingredients" shows which) [NNg-status] [Sweet-AnyList].
- Disabled buttons have low contrast and confuse; prefer active + explain; if dimmed use
  `aria-disabled`, do not hide [GOVUK-button] [NNg-buttonstates] [NNg-contextmenu].
- No self-vanishing views that hold an action (except Undo) [HIG-a11y]. The screen should not
  require remembering what is not visible [NNg-mobileUX].

**Attention and hierarchy**
- Primary: filled; secondary: outline/tinted; tertiary: text button; red only when destructive
  is the screen's primary action [RUI-7tips] [GOVUK-button] [HIG-layout].
- Max 3 size/contrast levels, <= 2 big elements, 2 main + 2 secondary colours in a simple view
  [NNg-hierarchy]. De-emphasise competitors: 2-3 text shades, 2 weights, none under 400 [RUI-7tips].
- Labels last: "12 left" not "Quantity: 12"; obvious data without label; label smaller/lighter
  [RUI-labels].
- Order by importance from the top/left; indent = subordinate, alignment = same group
  [HIG-layout]. Users look at and touch the screen centre: main content central, secondary
  actions top/bottom, third-level in a corner, dangerous far from others [Hoober-2017].
- F-pattern is the default without strong cues; on mobile also "marking". First words of a row
  decide: key word first [NNg-F]. Squint test: blur a mockup 5-10 px, the right thing must still
  stand out; test with real content [NNg-hierarchy].
- One banner at a time, only when it concerns the user; success message only when confirmation
  is expected [GOVUK-banner]. Accent edge or coloured icon tile guides the eye without big
  surfaces [RUI-7tips].

**Visual foundation**
- Spacing 4/8/12/16/24/32/48 [RUI*] [M3-layout*]. Type: body 16 (M3 Body Large 16, iOS Body
  17 pt), secondary 14, min 12 (iOS absolute min 11 pt), headings 20-24, large 28-34, line height
  1.4-1.5 [M3-type] [HIG-a11y] [Fluent-type].
- Weights 400 and 600/500; no ALL CAPS in tabs/buttons; sentence case [Fluent-type] [NNg-tabs]
  [HIG-a11y].
- Palettes defined up front: 8-10 greys, 5-10 shades of primary (start from a button-ready 500,
  then 100/900, then between), accents and semantic colours (red destructive, yellow warning,
  green ok) in a few shades [RUI-palette]. Radix 12-step roles: 1-2 background, 3-5 component
  background (rest/hover/pressed), 6-8 borders (subtle/interactive/focus), 9-10 solid fill and
  hover, 11 low-contrast text, 12 high-contrast text [Radix-scale]. Tint greys toward the primary
  (blue -> slate, green -> sage) unless a quiet look is wanted [Radix-compose]. Tailwind uses 11
  steps 50-950 [Tailwind-colors].
- Colour roles not hex: primary/on-primary, primary-container/on-primary-container, surface + 5
  surface-container levels, outline, outline-variant; contrast holds when a pair changes
  together; light theme primary tone 40, dark 80; container 90/30 [M3-color].
- Depth with surface tone; shadow for floating elements, offset downward (light from above), no
  big blurry halo [M3-color] [RUI-7tips]. Colour means one thing; accent = clickable, not used
  for non-clickable text [HIG-color].
- Dark theme: dark grey (M3 neutral 6, ~#121212 class, not #000), lighter tones (80), contrast
  checked separately [M3-color] [HIG-color].
- Personality chosen on purpose (colour, font, rounding, language), else generic [RUI*]
  [Fluent-principles]. Beauty is perceived as easier and forgives small problems, not serious
  ones; decoration that lowers density too much turns into annoyance [NNg-aesthetic]. Judge by
  what users do, not by praise.
- Density = value / (time + space); frequent users prefer dense; empty space only where it
  groups; load speed raises effective density more than cramming [Strom-density].
- Optional: 3 rounding values and 2 shadows; motion short 50-200 ms (fade in 150, out 75), medium
  250-400 ms (view transitions ~300 ms), decelerate in, accelerate out; tabs fade through; list ->
  detail container transform [M3-motion].

**Mobile and touch**
- Targets >= 44x44 px (Apple 44 pt; NN/g ~1 cm), absolute minimum 24x24 CSS px (WCAG 2.5.8);
  the visible part may be smaller [HIG-a11y] [NNg-target] [WCAG-258].
- Spacing: Apple ~12 pt around a bordered button, ~24 pt around a borderless icon's visible edge;
  at least 2 mm (~8 px); corners/edges ~12 mm, centre ~7 mm [HIG-a11y] [NNg-target] [Hoober-2017].
  Larger targets when moving (walking in a store), for the primary action, when few elements.
- Grip: ~49 % one hand, 36 % cradled, 15 % two hands; 75 % tap with the thumb; left-handed ~1/3.
  Daily actions low or central; do not assume the top is "safe for dangerous" (cradle grip
  reaches it) [Hoober-2013] [Hoober-2017].
- Bottom sheet: not justified by reach; for short contextual tasks, not persistent info, no sheet
  on sheet, no multi-page flows [NNg-sheet] [HIG-sheets]. Handle (>= 48 px free zone) + visible
  close + back + drag down + backdrop tap; max width ~640 px on large screens; ask about unsaved
  changes [M3-sheet] [NNg-sheet] [HIG-sheets].
- Bottom bar 3-5 items, always icon + name, active indicator (pill behind icon) plus a second cue
  (weight or colour); height 64-80 px + safe area [M3-navbar] [NNg-tabs]. Snackbar above bar/FAB,
  one at a time, one action, swipe-dismissable [M3-snackbar].
- Inputs: font >= 16 px (iOS zooms otherwise), never block zoom, correct `inputmode` and
  `enterkeyhint`; typing is slow, minimise it and offer choices [NNg-mobileUX].
- Safe areas `env(safe-area-inset-*)`, `100dvh`; no targets in system gesture zones [HIG-layout]
  [Android-back]. Panels: `overscroll-behavior: contain`.
- Widths 360, 390 px and narrow desktop; long Finnish words must not break the row; 200 % text
  size must not break layout (rows grow, not clip) [HIG-layout] [HIG-a11y]. Light haptics on tick,
  off with reduced motion [HIG-a11y].

**Accessibility**
- Contrast: text <= 17 pt 4.5:1, large (>= 18 pt or bold) 3:1, icons/borders/states 3:1, both
  themes [HIG-a11y] [Fluent-type]. State not by colour alone (red-green and blue-orange confuse)
  [HIG-a11y] [HIG-color].
- Focus ring visible within 150 ms for keyboard use, not just a colour change; focus not hidden
  under a sticky bar (WCAG 2.4.11) [NNg-buttonstates]. After delete move focus to the next row or
  list heading; announce add/remove in a `role="status"` region ("Milk added") [Inclusive-todo].
- Row delete button named with the item, always visible (not hover-only); placeholder is not a
  label [Inclusive-todo]. Reduced motion: slides and zooms become fades, no depth animation, no
  flashing [HIG-a11y]. Core works with touch, keyboard and screen reader [HIG-a11y] [HIG-gestures].

## Competitor patterns (shopping/list apps, generalised)

Sources are reviews and vendor pages; user feedback from comparison blogs (some are competitors'
own) is indicative only.

- **Visual tiles (Bring!):** items as coloured illustrated tiles, recognised at a glance; tap =
  bought. A "recently used" strip under the list re-adds with one tap (frequently-bought without
  a separate view). Catalogue by category with search; custom items by typing. Urgency badges
  ("urgent", "offer", "if convenient") cut household messaging. Tiles/list view choice, themes,
  light/dark; personalisation is a selling point. Recipe templates add all ingredients at once.
  Complaints: offers/ads feel intrusive, wrong automatic icon guess hard to undo, unreliable
  notifications [TapSmart-Bring] [MUO-Bring] [Bring-blog].
- **Per-list identity (AnyList, To Do):** each list has its own header colour and icon on the home
  view; lists in folders; emoji at the start of a name becomes the list icon. To Do has a daily
  "My Day" view that starts empty and suggests unfinished items [Sweet-AnyList] [MSToDo-help].
- **Add flow (AnyList, Todoist):** "+", type, suggestions under the field (built-in, favourites,
  recent), Enter keeps typing; item notes remembered; "add all favourites" = weekly base list in
  one tap; the "recent" list grows too big to use, so cap and order it. One quick-add field that
  takes everything at once (Todoist: natural language, `#project`, `p1`) [Sweet-AnyList]
  [Todoist-help].
- **Order and shopping flow (AnyList, OurGroceries, Paprika):** automatic category headings, shelf
  order editable by store layout, per-store filtering (users' favourite feature), same ingredient
  from several recipes merged, "already at home" tick before the trip. Change visible to the
  other person in the store at once [Sweet-AnyList] [OG-overview] [Paprika-reviews*].
- **Done items (Keep):** ticked items move down and stay, forming a "what we usually buy" list
  for re-adding [Keep-help] [Keep-jefftk].
- **Sharing:** per account, manageable, revocable; immediate notification of changes. Complaints
  across apps: sync problems, accidental ticks, much behind a paywall, ads where a tap added an
  item, sharing that needs a shared account [Sweet-AnyList] [OG-overview] [vertailut*].

## Common mistakes

Avoid
- Generic grey stack of equal cards; too much air on mobile (little visible), but also a large
  image that costs density [NNg-aesthetic].
- Several filled primary buttons in one view; red button other than as the primary action.
- Confirmation dialogs for routine actions ("Are you sure?" + OK/Cancel, default "Yes").
- A daily action in a hamburger or ⋯ menu; a third disclosure level; vague names ("Add", "More",
  "Manage") in navigation.
- Icon without text when the meaning is not universal; gear or hamburger as a context-menu icon;
  one icon with two meanings; text-like button/link in text colour.
- Long-press as the only route to an escape hatch ("don't suggest" on a chip, remove a
  suggestion): it recurs; give it a visible control too.
- Swipe or long-press as the only route; swipe whose meaning changes by direction or state;
  horizontal swipe colliding with back.
- Sheet on sheet; handle without a Close button; back that skips a panel or jumps up.
- Snackbar gone before Undo can be tapped; many banners at once; silent deletion or change
  (other user changed, system cleaned up).
- Dimmed button without explanation; hidden non-working button.
- Grey text on coloured background; colour-only state; ALL CAPS names; enlarged small icon; big
  blurry shadow; borders everywhere.
- Layout shift on load; spinner for < 1 s; animation for < 100 ms.
- Dark theme as inverted colours, #000 background, over-saturated colours.
- Keyboard covering the field; input font < 16 px; target in a gesture zone.

Often forgotten
- States: empty (say what goes here + one action; not "no results" while loading), loading,
  error, offline, long name, long list, pressed, selected, disabled [NNg-empty].
- Pressed state 100-150 ms; keyboard focus; selected with two cues.
- Back and browser history work as in an app; back closes the topmost layer.
- Focus after delete; screen-reader status message on add/remove.
- First launch: no tour, empty views teach.
- Same words and icons mean the same in every view (glossary).
- Maskable app icon, `theme-color` for both themes, splash.
- Short human copy; number before explanation ("3 left").
- Done rows do not vanish: they are the base for re-adding [Keep-jefftk].
- One delightful small moment (done state), no clutter.

## Sources

Design systems
- [HIG-layout] https://developer.apple.com/design/human-interface-guidelines/layout
- [HIG-a11y] https://developer.apple.com/design/human-interface-guidelines/accessibility
- [HIG-lists] https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
- [HIG-gestures] https://developer.apple.com/design/human-interface-guidelines/gestures
- [HIG-color] https://developer.apple.com/design/human-interface-guidelines/color
- [HIG-sheets] https://developer.apple.com/design/human-interface-guidelines/sheets
- [M3-color] https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md
- [M3-type] .../docs/theming/Typography.md
- [M3-motion] .../docs/theming/Motion.md
- [M3-sheet] .../docs/components/BottomSheet.md
- [M3-navbar] .../docs/components/BottomNavigation.md
- [M3-FAB] .../docs/components/FloatingActionButton.md
- [M3-snackbar] .../docs/components/Snackbar.md
- [M3-layout]* https://m3.material.io/foundations/layout/understanding-layout/spacing (from memory)
- [Android-back] https://developer.android.com/design/ui/mobile/guides/patterns/predictive-back
- [Fluent-principles] https://fluent2.microsoft.design/design-principles
- [Fluent-type] https://fluent2.microsoft.design/typography
- [GOVUK-button] https://design-system.service.gov.uk/components/button/
- [GOVUK-banner] https://design-system.service.gov.uk/components/notification-banner/
- [WCAG-258] https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- [Radix-scale] https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale
- [Radix-compose] https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette
- [Tailwind-colors] https://tailwindcss.com/docs/colors

Usability research (nngroup.com/articles/<slug>)
- [NNg-navi] mobile-navigation-patterns; [NNg-hamburger] find-navigation-mobile-even-hamburger;
  [NNg-ikonit] icon-usability; [NNg-swipe] contextual-swipe; [NNg-confirm] confirmation-dialog;
  [NNg-mental] mental-models; [NNg-F] f-shaped-pattern-reading-web-content;
  [NNg-hierarchy] visual-hierarchy-ux-definition; [NNg-mobileUX] mobile-ux;
  [NNg-progressive] progressive-disclosure; [NNg-flat] flat-ui-less-attention-cause-uncertainty;
  [NNg-sheet] bottom-sheet; [NNg-control] user-control-and-freedom;
  [NNg-status] visibility-system-status; [NNg-buttonstates] button-states-communicate-interaction;
  [NNg-scent] information-scent; [NNg-tabs] tabs-used-right; [NNg-contextmenu] contextual-menus;
  [NNg-target] touch-target-size; [NNg-empty] empty-state-interface-design;
  [NNg-aesthetic] aesthetic-usability-effect
- [Hoober-2013] https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php
- [Hoober-2017] https://www.uxmatters.com/mt/archives/2017/03/design-for-fingers-touch-and-people-part-1.php
- [LukeW-hidden] https://www.lukew.com/ff/entry.asp?1945
- [Baymard-autocomplete] https://baymard.com/blog/autocomplete-design
- [Inclusive-todo] https://inclusive-components.design/a-todo-list/
- [Strom-density] https://mattstromawn.com/writing/ui-density

Visual craft
- [RUI-7tips] https://medium.com/refactoring-ui/7-practical-tips-for-cheating-at-design-40c736799886
- [RUI-palette] https://www.refactoringui.com/previews/building-your-color-palette
- [RUI-labels] https://www.refactoringui.com/previews/labels-are-a-last-resort
- [RUI*] Refactoring UI book (spacing scale, personality), from memory

Competitors
- [Bring-blog] https://getbring.com/blog-posts/out-now-your-whole-new-shopping-experience-with-bring
- [TapSmart-Bring] https://www.tapsmart.com/apps/review-bring-shopping-lists-made-easy/
- [MUO-Bring] https://www.makeuseof.com/organize-family-shopping-with-bring-grocery-app/
- [Sweet-AnyList] https://thesweetsetup.com/apps/anylist-favorite-grocery-shopping-app/
- [OG-overview] https://www.ourgroceries.com/overview
- [Keep-help] https://support.google.com/keep/answer/6358550
- [Keep-jefftk] https://www.jefftk.com/p/keep-move-checked-items-to-bottom
- [MSToDo-help] https://support.microsoft.com/en-us/todo/customize-your-lists
- [Todoist-help] https://www.todoist.com/help/articles/use-task-quick-add-in-todoist-va4Lhpzz
- [Paprika-reviews*] https://plantoeat.com/?p=38013 and App Store reviews (search summary only)
- [vertailut*] fango.fi, getbuybye.com, smartcartfamily.com, listonic.com comparisons (some are
  competitors' blogs; indicative only)
