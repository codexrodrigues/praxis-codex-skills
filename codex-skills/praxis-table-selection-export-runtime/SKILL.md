---
name: praxis-table-selection-export-runtime
description: Use when Codex must implement, audit, or debug @praxisui/table selection and export operations: rowClick, selectionChange, selected rows/ids context, bulk actions, export formats/scopes, PraxisCollectionExportService, filtered/currentPage/selected/all scopes, collection capabilities, toolbar export UI, or AI selected-record context.
---

# Praxis Table Selection Export Runtime

Use this skill when the issue depends on selected rows, bulk operations, row events, or governed export from `@praxisui/table`.

Selection and export are runtime evidence. They should be derived from table state, capabilities, and declared export configuration, not from DOM order, viewport text, guessed IDs, or local action labels.

## Source Audit

Inspect before editing:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/lib/praxis-table.ts`
- `projects/praxis-table/src/lib/praxis-table.metadata.ts`
- `projects/praxis-table/src/lib/table-global-action-adapter.ts`
- `projects/praxis-table/src/lib/toolbar-actions-editor/**`
- `projects/praxis-table/src/lib/praxis-table-config-editor.*`
- `projects/praxis-table/src/lib/ai/table-context-pack.ts`
- `projects/praxis-table/src/lib/ai/table-agentic-authoring-turn-flow.ts`
- focused selection, bulk, export, global action, config editor, and AI context specs.

Inspect `@praxisui/core` collection export models/services and global action payload contracts when export or actions cross package boundaries.

## Selection Rules

- Use canonical outputs: `rowClick`, `selectionChange`, `widgetEvent`, `resourceEvent`, and `recordSurfaceOpen` as applicable.
- Preserve `selectionChange` shape with trigger, selectedRows, selectedCount, optional row, and tableId.
- Use selected row snapshots and sanitized selected-record context for AI; do not expose raw internal fields unless explicitly required.
- Treat `selectedRecordsContext` as governed read-only grounding for analysis of the current selection. Questions to understand, summarize, compare, inspect, rank, or explain selected records should answer with `info` grounded in sanitized `sampleRows`; do not convert them into `componentEditPlan`, `table.filter.apply`, export, row action, navigation, or backend mutation unless the user explicitly asks to apply/configure/create/open/export.
- When a request explicitly asks to turn selected records into filters, use declared `selectedRecordsContext.filterCandidates` as the canonical bridge to advanced filters; prefer candidate labels and criteria over re-inferring values from prose, selected ids, sample rows, or visible cell text. If the shared property is ambiguous, ask a concise clarification grounded in filter-field labels or export scopes.
- When selected records also expose `recordSurfaces`, requests to open, consult, view, navigate to, or inspect a related surface should ground on the declared surface ids before considering selection-derived filters.
- Bulk actions are disabled when no rows are selected unless a governed action says otherwise.
- Reconcile selection after data refresh by stable row identity, not visual index.
- For related resource or surface actions, separate row-selection transport from authorization. Availability comes from capabilities, surfaces, actions, or `_links`.

## Export Rules

- Use `PraxisCollectionExportService` and core export request/result contracts.
- Honor declared formats and scopes: `selected`, `filtered`, `currentPage`, `all`, and `auto`.
- `selected` scope must come from selected row state or selected ids; `filtered` scope must come from effective filters/query context; `currentPage` from the current paged data.
- Do not add direct CSV/PDF/XLS generation in a host or table branch when core collection export already owns the operation.
- Treat host-declared export config as a contract. If host export config changes, reconcile persisted table config accordingly.

## Aderence Inventory

Classify before adding selection/export behavior:

- `ja-suportado-so-ux`: event/export state exists but UI, toolbar, empty state, or assistant does not expose it.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a local selected-id or export shape should map to core collection export or table selection outputs.
- `suportado-parcialmente`: selection/export exists but scope mapping, persistence, AI context, capabilities, docs, or direct consumer proof is incomplete.
- `lacuna-real-de-contrato`: no table/core event, export scope, request, or capability can express the operation.

Only real gaps justify new public contracts. Otherwise fix materialization or consumer wiring.

## Validation

Use focused proof:

- `praxis-table.events.spec.ts`
- selection, floating bulk, row action, or toolbar specs.
- `table-global-action-adapter.spec.ts`
- export/runtime operation specs and AI operation specs when assistant behavior changes.
- config editor specs when export/actions are authored.
- browser validation when selection affordances or download UX are user-visible.

For first-step issue resolution, audit: selectedRows/selectedIds source, idField, current filters/query context, export scope, requested formats, capability availability, generated request, artifact validation, and user-visible disabled/error state.

## Companion Skills

- Use `praxis-table-runtime-data` for surrounding table runtime state.
- Use `praxis-table-filter-actions` for toolbar/row/bulk action authoring and grounding.
- Use `praxis-core-global-action-payloads` for structured action refs.
- Use `praxis-core-resource-runtime` for collection export, capabilities, HATEOAS, and resource discovery.
