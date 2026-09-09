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

Standalone `praxis-filter` is authorable through its projected manifest. Keep
filter-field operations selected by stable ids from the Table owner manifest;
preserve target/validator/example closure through
`projectComponentAuthoringManifest()` and generated registry ingestion.

Distinguish filter outputs when authoring connections or explaining payloads:
`change` carries filter values; `contextChange` carries `PraxisFilterViewContext`
with `filter`, `labels`, `fieldLabels` and `fields` for presentation. Only its
`filter` portion is the query payload; do not send the entire view context as
a backend filter or imply that its display labels trigger a query. Inspect
`requestSearch` separately when the workflow requires explicit search.

For localized labels, inspect
`components/praxis-filter/praxis-filter-editorial.ts` and its spec under
`projects/praxis-table/src/lib/`, owning metadata providers and i18n registration.
The official descriptors distinguish “Valores do filtro” from “Valores e
rótulos do filtro”. Consumers resolve them through
`ComponentMetadataRegistry.resolveEditorial()`; do not rename outputs or add
host label maps. Test pt-BR/en-US, fallback and host translation overrides
without changing binding identity or payload shape.

## Governed Filter Presentation

Inspect Core's `FilterPresentationConfig`, the Table JSON API's **Filter presentation** section,
`PraxisFilterComponent` and Filter Settings before adding a label, icon or local toolbar style.
The table path is `behavior.filtering.advancedFilters.settings.presentation`; standalone filters
use `FilterConfig.presentation`. Neither changes query semantics. Reuse `header.visible`,
text/icon/position/size, `advancedAction` display/position/size and the declared presentation tokens.
An absent header stays hidden; an empty icon removes it. Empty authored text restores localized
copy, and an icon-only advanced action without an icon must retain a visible text fallback.
Keep `showAdvancedButton` as the existing availability switch rather than adding another one.

Prove visible/hidden heading, authored/cleared text, icon removal, host token and translation
overrides in both embedded and standalone consumers. Preserve the complete effective FilterConfig
when editing presentation. With persistence enabled, acknowledged preferences win over authored
presentation on reload; `disablePersistence` prevents preference loading and saving. Apply alone
is not proof of that round-trip. Use `praxis-config-runtime-persistence` for remote ownership/ETag.

## Action Contract Rules

- Toolbar, row, and bulk actions must resolve from declared table config, global action catalog, resource actions, record surfaces, capabilities, and `_links`.
- Toolbar disabled explanations must materialize existing denied availability from runtime CRUD operations, discovered actions or surfaces through Core resourceDiscovery translations. An available surface does not override a denied operation. Preserve selection-only guidance when no denial exists, host locale/translation overrides, unknown-code fallback and fail-closed dispatch; do not infer permission from a configured tooltip or enable an action merely to demonstrate it. Validate the session-required path separately from authenticated open/cancel/save.
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

Add `praxis-filter-authoring-manifest.spec.ts`, widget config-editor/metadata
specs, registry projection specs, and palette/editor round-trip when standalone
Filter authoring changes.

## Companion Skills

- Use `praxis-table-data-source-precedence` when filters depend on local/remote mode, `queryContext`, `filterCriteria`, or persisted `resourcePath`.
- Use `praxis-table-selection-export-runtime` when toolbar/row/bulk actions depend on selection, export scopes, or collection export.
- Use `praxis-table-analytics-stats-runtime` when filters feed analytics stats requests or analytic-table views.
- Use `praxis-table-runtime-data` for the broader runtime umbrella.
- Use `praxis-table-authoring-settings` when filters/actions are edited through Settings Panel or config editors.
- Use `praxis-table-ai-validation` when action/filter behavior is available to table assistant or component edit plans.
- Use `praxis-core-resource-runtime` for resource schemas, actions, surfaces, capabilities, `_links`, option sources, and CRUD operation resolution.
- Use `praxis-dynamic-fields-editorial` for filter controls backed by dynamic fields or option sources.
