---
name: praxis-browser-editor-workflows
description: Author or reconstruct Praxis pages by operating visible browser editors, including their free JSON fields, and prepare repeatable timed demonstrations with real data. Use for human-style Page Builder exercises; use component authoring skills instead when implementing editor code.
---

# Praxis Browser Editor Workflows

Produce an editable page through controls a person can operate. Keep runtime
correctness, fidelity, usability and elapsed time separate in the evidence.
Authorization comes from the user's request, not this skill. Necessary Save of
the requested page can include its configured remote persistence; this does not
authorize domain-record mutations, source changes, publication or recording.
Preparing a video does not itself request a recording.

## Inspect the baseline

Distinguish exploration, a prepared rehearsal and recording. For preparation and
timing read [rehearsal.md](references/rehearsal.md); for collection screens also
read [collection-screen.md](references/collection-screen.md).

Inspect applicable AGENTS, the host route/providers, package lock, actual palette,
editor and reference screen. Canonical sources in `praxis-ui-angular` are:

- `projects/praxis-page-builder/src/lib/`: dynamic builder/config editor, widget
  shell editor, component palette and connection editor.
- `projects/praxis-core/src/lib/`: widget page/state/data-source/composition models,
  data-source runtime, dynamic widget page and registry metadata.
- Child component metadata, authoring document, renderer, editor and focused specs.

The installed package proves installed capability. A newer main or closed issue
does not prove adoption; an old-release defect does not prove a current gap.
Record these baselines separately.

Use `praxis-page-builder-authoring` and `praxis-page-builder-composition` for
semantics, plus the owning child skill for components actually used. For issue
triage use `praxis-product-evolution`; for authorized host changes load
`praxis-angular-host-project`. Backend metadata and config persistence remain
owned by their starters, not by this browser procedure.

## Operate the editors

1. Identify route, persona and disposable page scope. Preserve a checkpoint before
   an authorized reset. Reset through product controls; distinguish widgets,
   connections, data sources and device/layout overrides.
2. Stabilize before timing: official origin/port, real reads, known persistence
   and one save/reopen/reload. Use an existing authorized storage adapter. Do not
   create a config protocol or undisclosed mock to make a demo pass.
3. Inspect native ResourcePage/CRUD/Table, scope/KPI and insertion presets before
   manually composing Lists and connections. Prefer the simplest registered
   composition that satisfies the job. A recipe does not permit importing a
   finished page when the user requested creation through individual editors.
4. Use the browser's documented APIs and fresh visible state. Wait for panel
   transitions, validation, data and capabilities; do not assume a click worked.
   Resolve or close an obstructing overlay and confirm the intended enabled
   control and focus before keyboard activation. Never force disabled actions
   or use fixed sleeps to conceal incomplete work.
5. Configure data/behavior before polishing. Use visual controls first; when
   insufficient, edit the child's **visible free JSON field**, validate, use its
   Apply JSON command when present, then save. Preserve unrelated fields. The
   graph's Praxis JSON view may be an inspector/export, not an import editor.
   For a page-owned reconstruction, set each child's configuration origin to the
   page before editing content; JSON envelopes need not carry persistence policy.
6. Configure shell and canvas through their controls. Natural content height,
   occupied rows and fixed pixels are different. `kind: none` removes the shell;
   a frameless preset can preserve its content inset. Do not enlarge cards to
   conceal unresolved bindings.
7. Wire declared ports, shared state and transforms. Verify each connection's
   saved path immediately before creating the next; input text alone is not proof.
   If filling leaves the pipeline unchanged, use focused native typing and blur,
   then inspect again. Test native clear before adding a feedback link.
8. Preview desktop/mobile and exercise the journey. Save/reopen/reload proves
   persistence; screenshots alone do not. Preserve authorization and read-only
   scope, including denied Create/Edit.

Explore metadata, other registered components, native composition and JSON before
declaring a limitation. JSON cannot register an absent Angular class, implement
missing runtime behavior or override permission.

## Evidence and follow-up

For a limitation retain the smallest accepted/rejected JSON, before/after result,
editor path and baseline. Separate editor-authored configuration, transport-only
diagnosis and source inspection. A transport experiment is not human authoring.
For a UX issue, show the existing JSON/runtime capability and the unnecessary
work; do not invent a missing contract to justify improving its presentation.

Check duplicates and newer fixes before opening contextual owner issues. Include
job, reproduction, JSON result, owner, consumers, accessibility/mobile,
round-trip acceptance and validation limits. Prefer adoption/materialization
improvements to new public contracts.

On success finish with a saved page/checkpoint, screenshots, real-read evidence,
interactions and persistence boundary. If the official API remains unavailable,
preserve the draft, logs and elapsed time and report the blocked proof; do not
claim a continuous demonstration. For timed runs disclose preparation and
interruptions. Reconcile guidance with the canonical skill source; do not teach
version-specific workarounds as permanent product requirements.
