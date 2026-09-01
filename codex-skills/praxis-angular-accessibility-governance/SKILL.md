---
name: praxis-angular-accessibility-governance
description: Use when implementing or auditing functional accessibility across `@praxisui/*`: keyboard navigation, focus lifecycle through dialogs/drawers/editors, ARIA semantics and accessible names, live regions, chart alternatives, high contrast, reduced motion, localized assistive copy, responsive reflow, or focused accessibility/browser gates. Pair with the owning component skill; do not use only for visual polish.
---

# Praxis Angular Accessibility Governance

Use this skill for accessibility behavior that must remain coherent across
Praxis component packages and authoring surfaces. Visual taste belongs to
`praxis-ui-product-design`; the owning package still owns its component
contract. This skill owns the cross-library correctness rubric and proof.

## Source And Owner Audit

Start with root and package `AGENTS.md`, then inspect the affected component,
template, styles, i18n catalog, overlay/editor host, focused specs, and official
example. For shared behavior also inspect:

- `projects/praxis-core` focus, widget shell, i18n, and surface-host contracts
- `projects/praxis-dialog` overlay lifecycle and close affordances
- `projects/praxis-settings-panel` drawer/editor lifecycle
- Table, List, Dynamic Form, Dynamic Fields, Charts, CRUD, and Page Builder
  sources that participate in the journey

Do not fix a repeated focus, live-region, token, or overlay problem in a demo
when the shared owner is Core, Dialog, Settings Panel, or the component package.

## Functional Contract

- Every operation must be reachable and understandable without pointer input.
  Preserve logical tab order; do not encode layout order as an alternate state
  machine.
- Focus entering an overlay/editor goes to the intended first task target or
  labelled container. Closing, cancelling, applying, or failing restores focus
  to the initiating control when it still exists.
- Do not trap focus outside a modal contract or lose it during async
  materialization, table refresh, chart redraw, or component-mode switch.
- Controls require semantic roles, relationships, states, and accessible names.
  Icon-only controls need localized names; a tooltip is not the name.
- Announce material state changes such as filter result changes, column
  resize/reorder, export completion, persistence failure, loading, validation,
  and terminal authoring outcomes without repeatedly announcing transient
  implementation noise.
- Charts must expose keyboard interaction and an equivalent data/summary path.
  Semantic point identity, selection, and cross-filter state must not depend on
  pixel position or pointer-only events.
- High contrast, forced colors, reduced motion, zoom, narrow viewports, and
  reflow must retain meaning and access to primary actions.
- Assistive copy follows Praxis i18n namespaces. Stable test ids may make E2E
  deterministic but never replace accessible names or localization assertions.

Do not solve accessibility with duplicated hidden controls, hardcoded English
ARIA strings, consumer-only CSS, indiscriminate `tabindex`, or delayed focus
timers that lack lifecycle ownership.

## Workflow

1. Name the user journey and the exact accessibility failure, not only the WCAG
   label.
2. Map focus owner, keyboard owner, semantic DOM owner, i18n owner, and overlay
   owner. Classify whether the contract already exists but is under-materialized.
3. Fix the smallest canonical owner and update every projection of the same
   state: visible text, accessible name, live message, disabled/busy state, and
   diagnostics.
4. Exercise the sequence with keyboard only, including open, mutate, async
   result, error/cancel, close, and restored focus where applicable.
5. Review desktop and narrow reflow plus high-contrast/reduced-motion behavior
   when the changed surface uses color, motion, sticky/floating controls, canvas,
   charts, tables, or overlays.

## Proof

Minimum proof includes the owning focused spec and package build. Add browser
proof when behavior depends on real focus order, overlay portals, layout,
keyboard events, announcements, or chart rendering.

Prove:

1. Happy: keyboard completes the journey and focus/announcements are deliberate.
2. Risk: async loading, validation failure, unavailable action, narrow reflow,
   or destroyed initiator produces a safe result without lost focus.
3. Adversarial: no duplicate announcements, focus loop, pointer-only target,
   unlabeled icon, hidden actionable clone, or locale-dependent selector.

Use existing package commands from `praxis-angular-validation-gates`; do not
invent an E2E lane. Run registry/docs generation only when public component
metadata or assistive documentation changed. Capture screenshots for visual
contrast/reflow, but do not claim screenshots prove keyboard or screen-reader
behavior.

## Companion Skills

- Always pair with the owning functional component skill.
- `praxis-dialog-overlay-runtime`: modal/drawer focus and close lifecycle.
- `praxis-authoring-editors`: Settings Panel and config-editor round-trip.
- `praxis-charts-analytics-interactions`: chart selection and cross-filter semantics.
- `praxis-angular-i18n-governance`: localized accessible names and messages.
- `praxis-ui-product-design`: visual hierarchy, tokens, contrast, and screenshot QA.

