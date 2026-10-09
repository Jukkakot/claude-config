---
name: ui
description: UI principles, light/dark theme rules and cheap UI checks for the user's projects. Load before any UI change (a screen, component, layout, style or copy), a UI audit or polish, or a theme decision.
---

# UI work

## Theme

- Every project has a clear theme (a visual concept: materials, palette, shapes), agreed early and
  recorded in the project's docs/specs; new UI and copy stay consistent with it. Don't imitate the
  look of an existing commercial product.
- Every project has a **light and a dark theme**. By default the UI follows the system
  (`prefers-color-scheme`); a light/dark/system choice in settings overrides it.
- Use the platform's base theme first when it brings a good light/dark one (Material 3 on Android,
  a component library's theme) and add only what the project needs. A custom theme with mockups
  (both variants) is worth it mainly for web apps and games.

## Principles

Apply these on every UI change; for an audit or polish, run through them before and after.

- **Consistency:** the same concept is always shown the same way. Never re-implement inline what
  already has a shared component; flag inconsistencies when spotted.
- **State legibility:** the user can always answer: what is happening, what can I do, what
  happened last.
- **Feedback:** every action gets immediate visual feedback. Unusable buttons are disabled, not
  hidden. Show loading while waiting for a backend.
- **Hierarchy:** the most important element is the most prominent; the primary action stands out.
- **Mobile:** check mobile portrait, mobile landscape and desktop narrow (a project may narrow
  this). Touch targets at least 44×44 px. Nothing clips out of view.
- **Overflow:** never clip elements at container edges unless the clipping is intentional.

## Checking cheaply

Screenshots cost many tokens. Verify facts (text shown, button enabled, no horizontal scroll,
sizes) with an accessibility snapshot or a short DOM query; take a screenshot only where the look
needs judging (a new screen, a layout change), usually one per state.
