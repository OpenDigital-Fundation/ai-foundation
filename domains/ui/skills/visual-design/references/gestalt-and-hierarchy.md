# Gestalt principles and visual hierarchy

Reference for `ui:visual-design`. Perception groups and ranks what it sees before anyone reads a word; these principles predict how a layout will be read. Use them to check that the visual structure says the same thing as the information structure.

## Gestalt principles

| Principle | Perception | Check in a layout | Common failure |
|---|---|---|---|
| Proximity | Items close together read as a group | Space inside a group is clearly smaller than space between groups | A label equidistant from two fields; even spacing everywhere |
| Similarity | Items that look alike read as having the same role | One visual treatment per role (link, button, tag, status) | Clickable and static text styled the same; two styles for one action |
| Common region | A shared container makes a group | Cards, panels and table rows enclose what belongs together | Nested boxes that compete; borders where spacing would do |
| Uniform connectedness | Connected items (lines, shared background) read as related | Steppers, timelines and related controls are visually joined | Connectors that link unrelated items |
| Closure | The eye completes incomplete shapes | Icons and partial cards stay recognisable | Truncation that hides that content continues (no fade, no "more") |
| Continuity | The eye follows lines and curves | Alignments lead the eye along the reading order | Ragged alignments that break a column |
| Figure-ground | Foreground separates from background | Modals, menus and toasts clearly sit above the page | Low-contrast overlays; content bleeding through |
| Prägnanz (simplicity) | The simplest reading of a shape wins | Layouts resolve into a few clear blocks | Many small competing shapes |
| Symmetry and order | Symmetric, ordered arrangements read as a whole | Use symmetry for stable, formal layouts; break it to draw attention | Accidental near-symmetry that looks like a mistake |
| Common fate | Elements that move together read as a group | Animate a group as one; animate separately only when items are independent | Staggered motion that splits one object into parts |

## Visual hierarchy

Hierarchy tells the user what to look at first, second and last. Its levers, roughly in order of strength:

1. **Size and scale** — the largest element is read first.
2. **Contrast and colour** — high contrast and saturated colour pull attention; keep one accent for the primary action.
3. **Weight** — bold text and filled shapes outrank light ones.
4. **Position** — top and leading side (left in LTR, right in RTL) are read first; the first and last items in a list are remembered best.
5. **Whitespace** — isolation increases importance; crowding lowers it.
6. **Motion** — movement overrides everything else; reserve it for state changes.

### Checks

- **Squint test:** blur the screen (or step back). The order in which blocks remain visible should match their importance.
- **One primary action per view.** If two elements both look primary, neither is.
- **Three levels are usually enough** for text: heading, body, secondary. More levels need a reason.
- **Scanning patterns:** text-heavy pages are often scanned in an F-shape and sparse pages in a Z-shape; put key words at the start of headings and lines. Treat these as tendencies, confirmed by testing when they matter.
- **Hierarchy must survive accessibility settings:** larger text, high contrast and dark mode should keep the same order (see `accessibility:wcag-accessibility`).

## Relation to UX heuristics

Gestalt and hierarchy implement Nielsen's "aesthetic and minimalist design" and "consistency and standards", and Norman's signifiers: a button that does not look like a button is a similarity failure. For the full set of heuristics and laws used in reviews, see `ux:usability-review` (`references/heuristics-and-laws.md`).
