---
name: praxis-table-data-source-precedence
description: "Use when Codex must implement, audit, or debug @praxisui/table data-source runtime precedence: remote versus local data mode, resourcePath, document.bindings.resourcePath, queryContext, filterCriteria compatibility, pagination/sorting projection, local-data pipeline, persisted connection fallback, GenericCrudService handoff, or table authoring apply plans."
---

# Praxis Table Data Source Precedence

Use this skill when a table issue depends on how `@praxisui/table` chooses, applies, or persists its data source.

The table runtime materializes governed resource and query decisions. It must not guess user intent from text or silently switch between local and remote data modes without following the canonical precedence.

## Source Audit

Inspect before editing:

- `projects/praxis-table/AGENTS.md`
- `projects/praxis-table/docs/local-data-mode-precedence.md`
- `projects/praxis-table/src/lib/praxis-table.ts`
- `projects/praxis-table/src/lib/local-data/local-data-view-pipeline.ts`
- `projects/praxis-table/src/lib/local-data/local-data-filter-engine.ts`
- `projects/praxis-table/src/lib/table-editor-document.model.ts`
- `projects/praxis-table/src/lib/table-editor-capability.ts`
- `projects/praxis-table/src/lib/praxis-table-config-editor.ts`
- focused local-data, remote regression, config editor, and authoring document specs.

Also inspect `@praxisui/core` services when the flow uses `GenericCrudService`, `ResourceDiscoveryService`, query context models, capabilities, loading, or runtime observations.

## Canonical Precedence

Use the documented order:

1. Explicit `resourcePath` from input, quick connect, or `document.bindings.resourcePath` wins.
2. Local `data` array activates local mode only when no explicit `resourcePath` exists.
3. Persisted connection is fallback only when neither explicit `resourcePath` nor local mode applies.

`resourcePath + data` resolves to remote mode. Clearing `document.bindings.resourcePath` is the explicit authoring path for removing a remote connection.

## Runtime Rules

- Treat `queryContext` as the primary semantic query bridge for new composition. Use `filterCriteria` as compatibility input.
- Local mode belongs in `local-data/**` and must project filtering, sorting, pagination, and lookup comparison consistently.
- Remote mode must remain grounded in `GenericCrudService`, `resourcePath`, schema metadata, capabilities, HATEOAS links, and backend filter endpoints.
- In local mode, server pagination/sorting strategies should be projected to client behavior with diagnostics instead of silently behaving as remote.
- Preserve `config.meta.idField`, schema id/hash, server hash, bindings, and apply-plan diagnostics across authoring round-trip.
- Do not create host-specific data-source fallback branches when the existing precedence or core service already expresses the operation.

## Contextual Pagination and Sorting

Inspect `createDefaultTableConfig`, `TableDefaultsProvider`, `ensureConfigDefaults`,
`resolvePagingStrategy` and `resolveSortingStrategy` together. The canonical shared
defaults leave strategy properties absent: the table infers `server` for a remote
source and `client` for local data. Preserve explicit choices and existing local
constraints. Do not fix sparse host metadata by forcing a client default or adding
a host-specific server override.

The editor's Automatic option deletes the strategy property. Public values remain
`client` and `server`; never serialize `auto`. Unrelated editor changes preserve
absence. A partial authoring operation that omits strategy preserves an existing
explicit choice; omission in a patch is not a reset operation.

For remote acceptance, use the actual Material paginator/data source and wait for
deferred callbacks plus capability/action materialization. Verify a backend total
larger than the page size remains stable on page two and after reapplication or
resubscription. A transient correct range can later collapse when a client
paginator is incorrectly attached. Include local and explicit-choice controls,
core defaults/editor round-trip specs and a direct public consumer build. Keep
pre-existing unrelated suite compilation failures explicit; a focal gate is not
a full suite result.

## Aderence Inventory

Classify before adding inputs, config fields, connection models, or runtime branches:

- `ja-suportado-so-ux`: mode, binding, query, or diagnostic exists but the editor/runtime does not expose it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host field or legacy marker should normalize to `TableAuthoringDocument`, `bindings.resourcePath`, `queryContext`, or `config.meta`.
- `suportado-parcialmente`: table can choose the source but apply-plan, diagnostics, persistence, local projection, docs, or direct consumer proof is incomplete.
- `lacuna-real-de-contrato`: no table/core/config contract can represent the data-source decision.

Only real gaps justify new public contracts. Prefer fixing `@praxisui/core` for shared query/resource contracts and `praxis-table` for table-specific source precedence.

## Validation

Use focused proof:

- `local-data/*.spec.ts`
- `praxis-table.remote-regression.spec.ts`
- `praxis-table.pagination-context.spec.ts`
- `praxis-table.persistence-merge.spec.ts`
- `praxis-table.runtime-operations.spec.ts`
- `table-editor-capability.spec.ts`
- config editor or Settings Panel specs when apply/save/reset is affected.

For first-step issue resolution, audit: effective mode, chosen `resourcePath`, local data presence, query/filter merge, pagination/sorting strategy, idField/schema hash diagnostics, data reload flags, and persisted binding changes.

## Companion Skills

- Use `praxis-table-runtime-data` for the broader table runtime umbrella.
- Use `praxis-table-filter-actions` when source choice affects filter payloads or actions.
- Use `praxis-table-authoring-settings` when source choice is edited through Settings Panel.
- Use `praxis-core-resource-runtime` for `GenericCrudService`, schemas, capabilities, HATEOAS, and query context.
