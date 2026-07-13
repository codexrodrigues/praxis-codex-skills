---
name: praxis-fields-option-sources
description: Use when implementing or reviewing @praxisui/dynamic-fields or praxis-dynamic-fields package option-source controls, async selects, searchable selects, entity lookup, `RESOURCE_ENTITY` lookup projections, selected-value reload by IDs, dependency filters, option display resolution, `GenericCrudService` option APIs, or backend `x-ui.optionSource` materialization in Angular fields.
---

# Praxis Fields Option Sources

This `praxis-fields-*` plus `praxis-dynamic-fields-editorial` skill family is the canonical Codex skill surface for `@praxisui/dynamic-fields` and `projects/praxis-dynamic-fields`; do not create parallel dynamic-fields guidance unless this family cannot express a proven contract gap.

Use this skill for select-like fields backed by canonical Praxis option sources. The goal is to prevent local autocomplete/select implementations when `x-ui.optionSource`, `RESOURCE_ENTITY`, `async-select`, `searchable-select`, or `entityLookup` already cover the workflow.

## Canonical Boundary

- Backend metadata publishes `x-ui.optionSource`.
- `@praxisui/core` owns `OptionSourceMetadata`, `GenericCrudService.filterOptionSourceOptions`, `GenericCrudService.getOptionSourceOptionsByIds`, lookup DTOs, and resource discovery contracts.
- `@praxisui/dynamic-fields` materializes option loading in `SimpleBaseSelectComponent`, `MaterialAsyncSelectComponent`, inline select variants, `InlineEntityLookupComponent`, `OptionStore`, and `OptionDisplayResolverService`.
- Backend `RESOURCE_ENTITY` semantics belong with `praxis-resource-entity-lookup-backend`; this skill owns the Angular runtime/editorial consumption.

When backend metadata is wrong or incomplete, use `praxis-metadata-domain-option-sources` to audit `@DomainGovernance`, field access, `x-ui.optionSource`, entity lookup publication, selected reload policy, invalid sort policy, and filter/by-ids endpoints before adding Angular workarounds.

Do not route field intent through keywords such as "customer" or "status". Use the semantic `optionSource` contract, declared resource, and resolved `controlType`.

## Required Inventory

First resolve the Angular workspace root. In the platform monorepo the files may live under
`praxis-ui-angular/projects/...`; in a standalone Angular checkout they may live directly under
`projects/...`. Audit the active `praxis-ui-angular` workspace, not stale issue worktrees such as
`praxis-ui-angular-issue*`, unless the user explicitly targets one of those worktrees.

Before editing, inspect:

- `src/lib/base/simple-base-select.component.ts`
- `src/lib/base/option-store.ts`
- `src/lib/services/option-display-resolver.service.ts`
- `src/lib/components/inline-async-select/**`
- `src/lib/components/inline-entity-lookup/**`
- `src/lib/components/material-async-select/**`
- `src/lib/components/material-searchable-select/**`
- `src/lib/components/material-autocomplete/**`
- `src/lib/components/material-select/**`
- `src/lib/directives/dynamic-field-loader.presentation-mode.spec.ts`
- `src/lib/directives/dynamic-field-loader.select-rebind.spec.ts`
- `src/lib/base/pdx-base-select-runtime-contract.json-api.md`
- `src/lib/ai/praxis-dynamic-fields-authoring-profiles.ts`
- `src/lib/ai/praxis-dynamic-fields-authoring-manifest.ts` and spec
- `src/lib/ai/inline-filter-recipes.spec.ts`
- `src/lib/catalog/dynamic-fields-playground.catalog.ts` and catalog specs
- `src/lib/editorial/wave1/entity-lookup.editorial.ts`
- `src/lib/editorial/wave1/material-select.editorial.ts`
- `src/lib/editorial/metadata-contract.spec.ts`
- `src/lib/editorial/metadata-i18n-contract.spec.ts`
- affected `material-select`, `material-searchable-select`, `material-async-select`, `inline-*select`, or `inline-entity-lookup` component and spec
- `src/lib/components/**/pdx-*.json-api.md` for public runtime claims
- `src/lib/editorial/**` when the option-source field must be discoverable
- `projects/praxis-core/src/lib/models/option-source.model.ts` and spec
- `projects/praxis-core/src/lib/services/types/options.ts`
- `projects/praxis-core/src/lib/services/generic-crud.service.ts` and spec
- `projects/praxis-core/src/lib/helpers/field-definition-mapper.ts` and spec
- `projects/praxis-core/src/lib/helpers/metadata-normalizer.ts` and spec
- `projects/praxis-core/src/lib/services/schema-normalizer.service.ts` and spec
- `projects/praxis-core/src/lib/services/schema-normalizer-array.service.spec.ts`
- `@praxisui/dynamic-form` submit/runtime skills when selected value shape enters form payloads
- `@praxisui/metadata-editor` cascade normalization skills when the editor authoring surface changes dependencies
- backend `x-ui.optionSource` producer when the Angular runtime lacks required data

When the platform monorepo is available, inspect the backend option-source contract docs before
adding Angular fallbacks:

- `praxis-metadata-starter/README.md`, especially the `/option-sources/{sourceKey}/options/filter`
  and `/options/by-ids` checklist
- `praxis-metadata-starter/docs/guides/OPTION-SOURCE-PROVIDER-SPI.md`
- `praxis-metadata-starter/docs/concepts/ui-schema.md` when `dependsOn`,
  `dependencyFilterMap`, or `x-ui.optionSource` publication changes

## Option Source Rules

- Prefer `optionSource.key` plus `filterOptionSourceOptions(...)` over ad hoc endpoints when the backend publishes an option source.
- Treat `optionSource.filterEndpoint` and `optionSource.byIdsEndpoint`, when present in backend metadata, as execution evidence for the published contract. Angular code may route through `GenericCrudService`, but it must preserve the same source key, resource path, endpoint intent, and request envelope instead of synthesizing a different lookup route.
- Use `optionSource.resourcePath` or the canonical resource path to configure the CRUD service; do not invent local routes or derive a path from label/value names.
- If Angular can only execute a deterministic legacy route because old metadata lacks endpoint publication, mark the path as compatibility and keep a diagnostic or test proving that backend publication is the desired fix. Do not normalize missing endpoints into a new local convention.
- Honor `optionSource.dependsOn` and `optionSource.dependencyFilterMap`. Legacy `dependencyFields` and `dependencyFilterMap` may be runtime/manual metadata, but canonical backend-driven flows should come from `optionSource`.
- Convert dependency criteria to lookup filters through the existing option-source filter pipeline; do not encode dependency routing with local text matching.
- Honor `optionSource.includeIds`. Send `includeIds` in filter requests only when the contract allows it.
- For selected-value hydration, prefer `getOptionSourceOptionsByIds(optionSource.key, ids, options)` for option sources and `getOptionsByIds(ids)` only for generic resource options.
- For contextual selected-value reload, use the option-source by-ids endpoint with the same
  structural filter context published by the backend. Do not rehydrate dependent selected IDs with
  a generic unfiltered resource lookup when `selectedReloadPolicy` says context matters.
- When `selectedReloadPolicy` is `required` or `supported`, by-ids is part of the canonical proof for reopen/edit/presentation mode. A failure in by-ids should surface as an option-source contract or execution diagnostic, not silently degrade to a broad `filter` request that can display stale or unauthorized labels.
- When `selectedReloadPolicy` is `unsupported-with-waiver` or the source lacks `capabilities.byIds`, the UI may preserve already available object labels/local options, but must label the scenario partial and avoid claiming full edit/reopen support.
- When the host `FilterDTO` has fields named `search`, `sort`, `filters`, or `includeIds`, use the
  explicit option-source request envelope (`filter`, `filters`, `search`, `sort`, `includeIds`) so
  structural resource filters do not collide with option-source execution metadata.
- `byIds` responses should contain concrete options only; missing IDs are omitted, and runtime/UI
  code must not manufacture `null` options as if the backend selected value still existed.
- Preserve the requested ID order when displaying by-ids results. Backend and executor should already
  normalize this, but Angular code should not reshuffle selected-value reloads by page/search order.
- Preserve `entityKey`, `selectionPolicy`, `capabilities`, display property paths, status/disabled fields, and rich display fields when mapping backend lookup results to select/display DTOs. Those fields are governance evidence, not optional decoration for entity lookup.
- Presentation/read-only mode still needs selected display proof. Use by-ids/display resolver coverage; a working open panel does not prove saved values render after reopen.
- Preserve `selectedReloadPolicy`, `invalidSortPolicy`, and backend waivers in UX/tooling claims. If by-ids reload is not supported, mark the scenario partial instead of pretending edit/reopen is fully supported.
- Respect `invalidSortPolicy`: with `reject`, do not send arbitrary UI sort keys or fallback to client-side resorting as if the backend had accepted the request; with `ignore` or `unsupported`, explain the degraded sort behavior in diagnostics/tooling.
- Keep categorical buckets distinct: when the source is `CATEGORICAL_BUCKET`, default loading/search behavior may intentionally differ from free-text remote search.
- Keep legacy top-level `valueField`, `displayField`, `dependencyFields`, and `dependencyFilterMap` as compatibility inputs only. Canonical backend-driven flows should normalize through `OptionSourceMetadata`, mapper/normalizer specs, and runtime option-source filters.
- Do not infer `dependencyLoadOnChange`, reset policy, or reload policy from `dependsOn` unless the canonical contract declares it.
- Keep dynamic-form and table/filter consumers aligned: the same `optionSource` decision should drive form controls, inline filters, metadata-editor authoring, and CRUD/table lookup displays without host-local duplication.
- Treat Cockpit verifiers, HTTP examples, and LLM smokes as external evidence that a backend contract is reachable, not as permission to duplicate lookup semantics in Angular. If a published example demonstrates `dependencyFilterMap`, by-ids order, invalid-value display, provider-backed lookup, or governed materialization, the Angular runtime still must consume the canonical `OptionSourceMetadata`/`GenericCrudService` pipeline rather than copying the example payload or translating fields locally per screen.
- When debugging an Ergon migration or another consumer, first prove whether Angular received `optionSource.dependsOn`, `dependencyFilterMap`, `filterEndpoint`, `byIdsEndpoint`, `selectedReloadPolicy`, and `invalidSortPolicy` from `/schemas/filtered`. If the metadata is present but the UI does not materialize it, fix the Angular mapper/runtime. If it is absent, route to metadata/config ownership; do not add a screen-specific workaround.
- For dependent selected-value hydration, preserve the same mapped dependency context used by the filter request when calling `getOptionSourceOptionsByIds`. A working `smoke:llm-surface` example or Cockpit reachability check does not prove edit/reopen correctness unless the Angular by-ids path also receives the contextual filter.

## Entity Lookup

Use `entityLookup` / `inlineEntityLookup` for corporate entity selection when the backend publishes `RESOURCE_ENTITY` semantics, rich display fields, selection state, dependency requirements, create/detail affordances, or lookup filtering/sorting.

Pair with `praxis-fields-selection-lookup-controls` when the task also touches select, chips, tree,
list, inline selection overlays, option identity UI, or AI control-family guidance. Keep this skill
as the owner for backend option-source semantics, cascades, by-ids reload, and selected reload
policies.

Do not replace entity lookup with a plain async select unless the canonical metadata lacks entity semantics. If metadata lacks semantics but the domain requires them, fix the backend option-source contract instead of creating a local UI convention.

## Validation

Minimum focused checks:

- Core option-source contracts and metadata normalization:
  - `npx ng test praxis-core --watch=false --progress=false --include=projects/praxis-core/src/lib/models/option-source.model.spec.ts --include=projects/praxis-core/src/lib/services/generic-crud.service.spec.ts --include=projects/praxis-core/src/lib/helpers/field-definition-mapper.spec.ts --include=projects/praxis-core/src/lib/helpers/metadata-normalizer.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer-array.service.spec.ts`
- Base option-source behavior, dependency filters, `includeIds`, and selected reload:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/base/simple-base-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/base/option-store.spec.ts`
- Display/hydration and presentation mode:
  - Add or run focused `OptionDisplayResolverService` coverage for by-ids/display path behavior.
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.presentation-mode.spec.ts --include=projects/praxis-dynamic-fields/src/lib/directives/dynamic-field-loader.select-rebind.spec.ts`
- Async/searchable/autocomplete controls:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/material-async-select/material-async-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-async-select/inline-async-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-searchable-select/material-searchable-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-searchable-select/inline-searchable-select.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/material-autocomplete/material-autocomplete.component.spec.ts --include=projects/praxis-dynamic-fields/src/lib/components/inline-autocomplete/inline-autocomplete.component.spec.ts`
- Entity lookup and `RESOURCE_ENTITY` semantics:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/components/inline-entity-lookup/inline-entity-lookup.component.spec.ts`
- Editor/tooling/catalog/AI discovery when metadata/editorial claims change:
  - `npx ng test praxis-dynamic-fields --watch=false --progress=false --include=projects/praxis-dynamic-fields/src/lib/catalog/catalog-derivation.spec.ts --include=projects/praxis-dynamic-fields/src/lib/catalog/dynamic-fields-playground.catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-contract.spec.ts --include=projects/praxis-dynamic-fields/src/lib/editorial/metadata-i18n-contract.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/control-type-ai-catalog.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/praxis-dynamic-fields-authoring-manifest.spec.ts --include=projects/praxis-dynamic-fields/src/lib/ai/inline-filter-recipes.spec.ts`
- Downstream materialization: dynamic-form, metadata-editor, table/filter, or CRUD smoke only when the option-source contract changed for that consumer. Useful focused examples include:
  - `projects/praxis-dynamic-form/test-dev/e2e/funcionarios-form-demo-select-interaction.playwright.spec.ts`
  - `projects/praxis-dynamic-form/test-dev/e2e/form-config-editor-cascades.playwright.spec.ts`
  - `projects/praxis-crud/test-dev/e2e/funcionarios-edit-hydration-gap.playwright.spec.ts`
  - `projects/praxis-crud/test-dev/e2e/funcionarios-modal-select-overlay.playwright.spec.ts`
  - `projects/praxis-table/test-dev/e2e/filter-inline-metadata-editor.playwright.spec.ts`
- `npm run build:praxis-dynamic-fields` when public dynamic-fields contracts or metadata claims change.
- Build/test the direct consumer when option-source normalization changes a public core contract.

Always audit reopen/edit and presentation mode for selected values. A filter request that loads a page is not proof that a saved selected ID can be displayed later.

For backend-aligned option-source work, include a negative check for fields named `search`, `sort`,
`filters`, or `includeIds` and a by-ids check that verifies missing IDs are omitted and returned
options preserve requested order.
