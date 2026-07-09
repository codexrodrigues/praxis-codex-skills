---
name: praxis-table-filter-actions
description: Use when Codex must work on @praxisui/table filters, dynamic filter payloads, filter settings, filter drawer adapter, inline filters, toolbar actions, row actions, bulk actions, global actions, CRUD actions, export operations, or action/surface capability grounding.
---

# Praxis Table Filter Actions

Use this skill for table filters and action surfaces. The table must materialize governed capabilities, `_links`, `/schemas/filtered`, resource actions, global action catalogs, and filter DTO metadata. Do not solve filter/action gaps by adding host-specific keyword routing, local command parsing, or private adapters.

## Source Audit

Inspect the affected source:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/src/lib/components/praxis-filter/**`
- `projects/praxis-table/src/lib/filter-settings/**`
- `projects/praxis-table/src/lib/filter-drawer.adapter.ts`
- `projects/praxis-table/filter-drawer-adapter/**`
- `projects/praxis-table/src/lib/services/filter-config.service.ts`
- `projects/praxis-table/src/lib/toolbar-actions-editor/**`
- `projects/praxis-table/src/lib/table-global-action-adapter.ts`
- `projects/praxis-table/src/lib/crud-integration-editor/**`
- `projects/praxis-table/docs/dynamic-filter-payload-contract.md`
- `projects/praxis-table/docs/dynamic-filter-host-integration-guide.md`
- `projects/praxis-table/docs/dynamic-filter-architecture-overview.md`
- `projects/praxis-table/docs/dynamic-inline-filter-catalog.md`
- `projects/praxis-table/docs/dynamic-filter-range-filters-guide.md`

For backend grounding, inspect `praxis-metadata-starter` filter DTO and resource controller docs/source when the change touches `GenericFilterDTO`, `/filter`, `/filter/cursor`, `/locate`, `/options/filter`, or range normalization.

## Filter Contract Rules

- `PraxisFilter` emits filter payload snapshots; the host sends them to the canonical backend endpoint.
- The final HTTP payload must remain mappable to backend `GenericFilterDTO`.
- Ranges, aliases, and entity lookup collection payloads must respect the documented normalizers and `payloadMode`.
- Inline aliases and UI metadata can help materialize controls, but they must not create arbitrary HTTP contracts.
- Use `@praxisui/dynamic-fields` option sources, async selects, entity lookup, descriptors, and field metadata before creating local filter controls.

If a field, range, or lookup cannot be represented, classify the gap. Most problems are `ja-suportado-mal-nomeado-ou-mal-materializado` or `suportado-parcialmente`, not a new table-only contract.

## Action Contract Rules

- Toolbar, row, and bulk actions must resolve from declared table config, global action catalog, resource actions, record surfaces, capabilities, and `_links`.
- For global actions, use `GLOBAL_ACTION_CATALOG`, `PRAXIS_GLOBAL_ACTION_CATALOG`, validation helpers, and effect preservation; do not write one-off action payloads.
- For row actions that open declared record surfaces, preserve the canonical `recordSurface.id`; do not overwrite it with a row action id.
- For CRUD actions, respect `crudContext`, `resourcePath`, `idField`, open mode, and canonical CRUD integration editor behavior.
- For export, honor configured formats/scopes and the collection export service; selection and filtered scopes must come from runtime state, not guessed IDs.

Do not route user intent by local keywords. The AI or backend contract chooses the canonical operation; table metadata can then rank fields, actions, and surfaces.

## Validation

- Filter payload or inline controls: `praxis-filter*.spec.ts`, filter settings specs, and relevant docs.
- Host/backend contract: validate against `dynamic-filter-payload-contract.md` and a focal host/E2E when payload shape changes.
- Filter drawer adapter: include `filter-drawer-adapter/public-api.ts` and adapter specs.
- Toolbar/row/bulk/global actions: `table-global-action-adapter.spec.ts`, toolbar editor specs, config editor integration, and AI operation specs when assistant behavior changes.
- CRUD action integration: `crud-integration-editor` plus config editor integration specs.
- Browser-visible filter/action UX: relevant Playwrights such as `funcionarios-inline-filters`, filter demo interactions, table connections, or surface-open demos.

## Companion Skills

- Use `praxis-table-runtime-data` for runtime data modes, selection state, exports, renderers, and analytics.
- Use `praxis-table-authoring-settings` when filters/actions are edited through Settings Panel or config editors.
- Use `praxis-table-ai-validation` when action/filter behavior is available to table assistant or component edit plans.
- Use `praxis-core-resource-runtime` for resource schemas, actions, surfaces, capabilities, `_links`, option sources, and CRUD operation resolution.
- Use `praxis-dynamic-fields-editorial` for filter controls backed by dynamic fields or option sources.
