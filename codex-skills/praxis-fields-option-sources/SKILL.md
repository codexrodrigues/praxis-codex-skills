---
name: praxis-fields-option-sources
description: Use when implementing or reviewing Praxis Dynamic Fields option-source controls, async selects, searchable selects, entity lookup, `RESOURCE_ENTITY` lookup projections, selected-value reload by IDs, dependency filters, option display resolution, `GenericCrudService` option APIs, or backend `x-ui.optionSource` materialization in Angular fields.
---

# Praxis Fields Option Sources

Use this skill for select-like fields backed by canonical Praxis option sources. The goal is to prevent local autocomplete/select implementations when `x-ui.optionSource`, `RESOURCE_ENTITY`, `async-select`, `searchable-select`, or `entityLookup` already cover the workflow.

## Canonical Boundary

- Backend metadata publishes `x-ui.optionSource`.
- `@praxisui/core` owns `OptionSourceMetadata`, `GenericCrudService.filterOptionSourceOptions`, `GenericCrudService.getOptionSourceOptionsByIds`, lookup DTOs, and resource discovery contracts.
- `@praxisui/dynamic-fields` materializes option loading in `SimpleBaseSelectComponent`, `MaterialAsyncSelectComponent`, inline select variants, `InlineEntityLookupComponent`, `OptionStore`, and `OptionDisplayResolverService`.
- Backend `RESOURCE_ENTITY` semantics belong with `praxis-resource-entity-lookup-backend`; this skill owns the Angular runtime/editorial consumption.

When backend metadata is wrong or incomplete, use `praxis-metadata-domain-option-sources` to audit `@DomainGovernance`, field access, `x-ui.optionSource`, entity lookup publication, selected reload policy, invalid sort policy, and filter/by-ids endpoints before adding Angular workarounds.

Do not route field intent through keywords such as "customer" or "status". Use the semantic `optionSource` contract, declared resource, and resolved `controlType`.

## Required Inventory

Before editing, inspect:

- `src/lib/base/simple-base-select.component.ts`
- `src/lib/base/option-store.ts`
- `src/lib/components/inline-async-select/**`
- `src/lib/components/inline-entity-lookup/**`
- `src/lib/components/material-async-select/**`
- `src/lib/services/option-display-resolver.service.ts`
- affected `material-select`, `material-searchable-select`, `material-async-select`, `inline-*select`, or `inline-entity-lookup` component and spec
- `src/lib/components/**/pdx-*.json-api.md` for public runtime claims
- `src/lib/editorial/**` when the option-source field must be discoverable
- `@praxisui/core` option-source and `GenericCrudService` contracts
- `@praxisui/dynamic-form` submit/runtime skills when selected value shape enters form payloads
- `@praxisui/metadata-editor` cascade normalization skills when the editor authoring surface changes dependencies
- backend `x-ui.optionSource` producer when the Angular runtime lacks required data

## Option Source Rules

- Prefer `optionSource.key` plus `filterOptionSourceOptions(...)` over ad hoc endpoints when the backend publishes an option source.
- Use `optionSource.resourcePath` or the canonical resource path to configure the CRUD service; do not invent local routes.
- Honor `optionSource.dependsOn` and `optionSource.dependencyFilterMap`. Legacy `dependencyFields` and `dependencyFilterMap` may be runtime/manual metadata, but canonical backend-driven flows should come from `optionSource`.
- Convert dependency criteria to lookup filters through the existing option-source filter pipeline; do not encode dependency routing with local text matching.
- Honor `optionSource.includeIds`. Send `includeIds` in filter requests only when the contract allows it.
- For selected-value hydration, prefer `getOptionSourceOptionsByIds(optionSource.key, ids, options)` for option sources and `getOptionsByIds(ids)` only for generic resource options.
- Preserve `selectedReloadPolicy`, `invalidSortPolicy`, and backend waivers in UX/tooling claims. If by-ids reload is not supported, mark the scenario partial instead of pretending edit/reopen is fully supported.
- Keep categorical buckets distinct: when the source is `CATEGORICAL_BUCKET`, default loading/search behavior may intentionally differ from free-text remote search.
- Keep dynamic-form and table/filter consumers aligned: the same `optionSource` decision should drive form controls, inline filters, metadata-editor authoring, and CRUD/table lookup displays without host-local duplication.

## Entity Lookup

Use `entityLookup` / `inlineEntityLookup` for corporate entity selection when the backend publishes `RESOURCE_ENTITY` semantics, rich display fields, selection state, dependency requirements, create/detail affordances, or lookup filtering/sorting.

Pair with `praxis-fields-selection-lookup-controls` when the task also touches select, chips, tree,
list, inline selection overlays, option identity UI, or AI control-family guidance. Keep this skill
as the owner for backend option-source semantics, cascades, by-ids reload, and selected reload
policies.

Do not replace entity lookup with a plain async select unless the canonical metadata lacks entity semantics. If metadata lacks semantics but the domain requires them, fix the backend option-source contract instead of creating a local UI convention.

## Validation

Minimum focused checks:

- select base behavior: `simple-base-select.component.spec.ts` and `option-store.spec.ts`
- async select: `material-async-select.component.spec.ts`
- inline variants: affected `inline-*select.component.spec.ts`
- entity lookup: `inline-entity-lookup.component.spec.ts`
- display/hydration: `option-display-resolver.service` behavior or focused coverage where present
- editor/tooling discovery when metadata/editorial claims changed
- downstream materialization: dynamic-form, metadata-editor, table/filter, or CRUD smoke only when the option-source contract changed for that consumer

Always audit reopen/edit and presentation mode for selected values. A filter request that loads a page is not proof that a saved selected ID can be displayed later.
