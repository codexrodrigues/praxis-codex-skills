# Design A Composition Of Existing Widgets

Start with the operator's task, primary decision/action and information flow.
Choose native component capabilities and relationships before arranging a grid.
The same page can combine filters, editable forms, records, charts and editorial
content; its label does not prescribe four KPI cards or a particular widget count.

## Choose Responsibilities Before Appearance

- Page canvas: reading order, spans, grouping, occupied space and device layout.
- Widget shell: optional title/status/chrome, body surface, supported size and
  actions. Avoid duplicating a title already owned by the child without purpose.
- Child: internal hierarchy, typography, fields, chart legend, list slots, card
  content and query controls. Stacking the outer widget does not fix its internals.
- Runtime state: loading, invalid, selected, empty, error, denied and saved. Style
  these actual states; a visual badge must not fabricate freshness or permission.

For a proposed clickable card decide whether it navigates, selects a record,
filters a collection or only presents a value. Ground the interaction in the
owner's actual events/actions and make the selected/disabled state legible.
Use the filter-actions skill for query cards and the composition skill for links.

## Work With The Editor's Actual Capabilities

Prefer registered presets, inherited theme/shell and native density/spacing/layout
controls. Resolve explicit overrides before deciding a page preset failed to
apply. Do not patch host CSS to compensate for a shared editor/component defect.
If a visual control is missing, inspect the owner's installed editor/document
before claiming either a JSON-only limitation or a missing platform contract.

Keep one clear hierarchy for the task: the form's primary Submit, the collection's
query action and the editor's Apply/Save have different purposes. Query ownership
must remain understandable across inline filters, cards and chart selection.
Use compactness where it supports scanning; do not make tiny controls or tall
empty cards merely to equalize rows. Resolve missing data/bindings first.

## Compare More Than One Screen Type

For analytical views check scale, units, period, provenance, zero/error values,
legend and the effect of selection/clear. For custom registration check section
grouping, required/invalid fields, keyboard order, cancellation and the authorized
submit boundary. For collection/detail check search/clear, selection identity,
empty selection and return to the collection.

At desktop and narrow widths inspect the actual runtime and an open editor,
including overlays and footer controls. Record viewport and state; a screenshot
proves appearance at that point, not save/reopen or backend enforcement. Use the
owning component's functional checks alongside the visual rubrics.
