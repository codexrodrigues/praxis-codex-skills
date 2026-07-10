---
name: praxis-table-runtime-data
description: Use when Codex must inspect, change, or scaffold @praxisui/table runtime behavior: remote versus local data mode, TableConfig, columns, pagination, sorting, expansion, renderers, selection, CRUD resourcePath, GenericCrudService integration, export, analytics projections, or runtime observations.
---

# Praxis Table Runtime Data

Use this skill for the `@praxisui/table` runtime surface. The table is the canonical Angular runtime for enterprise table materialization, but it is not the primary source of backend semantics. Backend resource semantics come from `praxis-metadata-starter`; governed configuration and publication belong to `praxis-config-starter`; shared Angular models and services often belong to `@praxisui/core`.

## Source Audit

Inspect the real source before changing table runtime behavior:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/public-api.ts`
- `projects/praxis-table/src/lib/praxis-table.ts`
- `projects/praxis-table/src/lib/praxis-table.metadata.ts`
- `projects/praxis-table/src/lib/table-editor-document.model.ts`
- `projects/praxis-table/src/lib/table-editor-capability.ts`
- `projects/praxis-table/src/lib/local-data/**`
- `projects/praxis-table/src/lib/data-formatter/**`
- `projects/praxis-table/src/lib/analytics/**`
- `projects/praxis-table/docs/local-data-mode-precedence.md`
- `projects/praxis-table/docs/resource-events.md`

Also inspect `projects/praxis-core/src/lib/models/**`, `services/**`, and `src/public-api.ts` when the behavior depends on `TableConfig`, `GenericCrudService`, `ResourceDiscoveryService`, `RestApiLinks`, `PraxisCollectionExportService`, loading, logging, i18n, global actions, surfaces, capabilities, analytics, or runtime observations.

## Canonical Runtime Rules

Honor the official data-source precedence:

1. Explicit `resourcePath` from input, quick connect, or `document.bindings.resourcePath` wins.
2. Local `data` array activates local mode only when no explicit `resourcePath` exists.
3. Persisted connection is fallback only when neither explicit `resourcePath` nor local mode applies.

Treat `resourcePath + data` as remote mode. Clearing `document.bindings.resourcePath` is the explicit authoring path for removing a remote connection.

Do not add a local adapter, fallback, or special host branch when `GenericCrudService`, `/schemas/filtered`, `_links`, capabilities, resource surfaces, or table config already governs the operation.

## Platform Aderence Inventory

Before adding a runtime input, config field, event, service, renderer, export option, analytics shape, or public API, classify the need:

- `ja-suportado-so-ux`: the runtime has the state/operation and only needs better materialization.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the contract exists but the table labels, mapping, or defaults obscure it.
- `suportado-parcialmente`: table has part of the behavior but needs owner-aligned extension.
- `lacuna-real-de-contrato`: no canonical source can provide the data or behavior.

Only `lacuna-real-de-contrato` can justify a new public contract. Prefer fixing `@praxisui/core` for shared models/services and `praxis-metadata-starter` for backend metadata semantics.

## Runtime Change Guidance

- For remote resource flows, ground columns, filters, id fields, actions, surfaces, and availability in schema/capability discovery instead of hardcoded host lists.
- For local data mode, keep behavior contained in `src/lib/local-data/**` and preserve the documented precedence.
- For data formatting, renderers, rich content, rating, badges, links, chips, progress, avatar, media, compose, and micro-visualization, verify the renderer contract and the rich-content adapter before changing table chrome.
- For export, use `PraxisCollectionExportService` and declared export config; do not invent direct CSV/PDF generation inside a host.
- For analytics, use `analytics-table` models/services and core analytics projection contracts instead of bespoke dashboard payloads.
- For runtime observations, use the core observation registry rather than console-only diagnostics.

## Validation

Prefer the smallest reliable validation:

- local data or precedence: `local-data/*.spec.ts` plus affected `praxis-table.*.spec.ts`
- remote resource regression: `praxis-table.remote-regression.spec.ts` or a focused runtime spec
- renderers/rich content: the matching `praxis-table.*rich-content.spec.ts`
- export/global action/runtime operation: focused runtime spec plus AI/runtime operation spec when assistant behavior is involved
- public API/exported contract: `npm run build:praxis-table` plus a direct consumer or adapter validation when applicable
- browser-visible behavior: focal Playwright under `projects/praxis-table/test-dev/e2e/**`

When PowerShell is unavailable, run equivalent local manifest/frontmatter/hash checks for skill changes and state the limitation.

## Companion Skills

- Use `praxis-table-data-source-precedence` for focused local/remote data-source resolution, `resourcePath`, `queryContext`, persisted connections, local pipeline, and apply-plan diagnostics.
- Use `praxis-table-selection-export-runtime` for selected rows/ids, `selectionChange`, bulk state, export scopes, and collection export requests.
- Use `praxis-table-analytics-stats-runtime` for analytic-table projections, stats request execution, fallback rows, and dashboard table views.
- Use `praxis-table-renderer-state-diagnostics` for renderers, rich-content cells, formatting, empty/loading/error states, i18n, and runtime observations.
- Use `praxis-table-filter-actions` for filters, toolbar actions, row actions, bulk actions, filter drawer adapter, global actions, and action grounding.
- Use `praxis-table-authoring-settings` for Settings Panel, config editors, round-trip, resourcePath, idField, and editor parity.
- Use `praxis-table-ai-validation` for table AI manifest, component edit plans, runtime operations, context packs, registry ingestion, and AI E2E.
- Use `praxis-core-resource-runtime` for schemas, actions, surfaces, capabilities, HATEOAS, option sources, CRUD operation resolution, and resource discovery.
- Use `praxis-ui-product-design` for visual table UX and screenshot validation.
