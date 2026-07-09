# FieldSpec + Angular Contract Reference

Use this reference after the main skill loads, especially when deciding a control type or reviewing schema tests.

## Files To Inspect

Backend:

- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/extension/annotation/UISchema.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/FieldControlType.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/FieldDataType.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/filter/annotation/Filterable.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/extension/CustomOpenApiResolver.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/util/OpenApiUiUtils.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/controller/base/AbstractResourceController.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/controller/base/AbstractReadOnlyResourceController.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/controller/base/AbstractResourceQueryController.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/service/base/BaseResourceQueryService.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/util/DuplicateDraftUtils.java`

Angular:

- `praxis-ui-angular/projects/praxis-core/src/lib/models/field-metadata.model.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/schema-normalizer.service.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/generic-crud.service.ts`
- `praxis-ui-angular/projects/praxis-dynamic-fields/src/lib/services/component-registry/component-registry.service.ts`
- `praxis-ui-angular/projects/praxis-dynamic-fields/src/lib/components/material-async-select/material-async-select.component.ts`
- `praxis-ui-angular/projects/praxis-dynamic-fields/src/lib/components/material-searchable-select/material-searchable-select.component.ts`
- `praxis-ui-angular/projects/praxis-dynamic-fields/src/lib/components/material-autocomplete/material-autocomplete.component.ts`
- `praxis-ui-angular/projects/praxis-dynamic-fields/docs/generic-crud-service.md`

## Control Support Checklist

For each `controlType`, record:

| Layer | Required proof |
| --- | --- |
| Java enum | `FieldControlType` value exists and serializes to the intended string. |
| Java resolver | `CustomOpenApiResolver` or explicit `@UISchema` emits the intended `x-ui.controlType`. |
| Angular metadata | `FieldMetadata` accepts the string and required metadata keys. |
| Angular renderer | `ComponentRegistryService` registers a component for the string or a documented alias resolves to one. |
| Angular authoring | `field-configs.ts` and config file exist when field authoring/configuration is required. |
| Tests | OpenAPI/x-ui or component tests prove the schema/control shape. |

If any layer is missing, mark the control `blocked` or `needs-angular-work` and choose a safer supported pattern.

Important runtime rule: the effective renderability contract is the Angular registry, not the broad Java enum and not the broad TypeScript metadata union. Use `ComponentRegistryService.getRegisteredTypes()`, the selector registry/alias mapping from `@praxisui/core`, and direct inspection of `praxis-dynamic-fields` as the final renderability proof. Do not copy a stale hard-coded renderer list into migration docs; record the current evidence path and, when possible, the registry output observed in the target branch.

## Known Naming And Renderability Gaps

The Java enum and Angular metadata type can be broader than the dynamic field renderer. A control is not migration-ready until `ComponentRegistryService` can load it directly or through a documented canonical alias.

Observed important gaps:

- Naming gaps must be checked against the current alias mapping before handoff. Examples from older branches, such as `currency` versus `currencyTextBox` or `toggle` versus `switchButton`, are historical warnings, not current proof.
- Java/Angular metadata values such as `rangeSlider`, `autoComplete`, `multiColumnComboBox`, and `timePicker` are not proof of renderability unless they are registered in `ComponentRegistryService` or resolved by a documented selector alias.

For migration defaults, prefer controls proven in all layers on the current branch. If a screen needs a specialized control, prove backend `x-ui`, Angular metadata normalization, registry/alias resolution, and authoring/configurator support where applicable.

## Select And Options Contract

Remote selects depend on all of these pieces:

- DTO field annotated with `@UISchema(controlType = FieldControlType.SELECT, endpoint = "...")`.
- `displayField` pointing to a real business field when available.
- `filterField` for the search payload sent by Angular.
- `sortField` and `sortOrder` for stable options ordering.
- `optionsPageSize`, usually `50`.
- Resource implements `POST /options/filter` and `GET /options/by-ids`.
- Response item shape is `OptionDTO` with `valueField` and `displayField`.
- `POST /options/filter` returns the bare shape consumed by Angular: `Page<OptionDTO>`.
- `GET /options/by-ids` returns the bare shape consumed by Angular: `OptionDTO[]`.
- Option-source endpoints follow the same no-envelope convention: `POST /option-sources/{sourceKey}/options/filter` returns `Page<OptionDTO<Object>>`, and by-ids endpoints return `OptionDTO<Object>[]`. Use `praxis-resource-entity-lookup-backend` when the source is governed by `RESOURCE_ENTITY` or entity lookup metadata.

Schema test nuance:

- In `@UISchema`, `displayField` should name the business DTO field when available so the resolver can derive `filterField` and `sortField`.
- For select-like controls, the resolver normalizes the final `x-ui.valueField` and `x-ui.displayField` to the `OptionDTO` shape: `valueField` and `displayField`.
- Therefore, OpenAPI assertions for remote selects should verify `endpoint`, `filterField`, `sortField`, `sortOrder`, `optionsPageSize`, and the final `OptionDTO` mapping. Do not fail a schema test merely because final `x-ui.displayField` is `displayField` instead of the original business field.

Angular behavior observed:

- Current select/list components call `GenericCrudService` for remote options.
- They post to `/options/filter` or `/option-sources/{sourceKey}/options/filter`.
- When `filterField` is present, it sends `{ "<filterField>": query }`.
- It uses `/options/by-ids` to rehydrate selected values.
- Current selected-value reload in async/searchable/autocomplete components supports string or numeric IDs and calls `/options/by-ids` or option-source by-ids. Composite IDs and contextual option-source reload still need explicit evidence from the current component and backend contract.
- If `filterField` is missing, Angular may fallback to a real `displayField`, but it deliberately avoids generic `displayField`/`valueField` names as search payload keys. Remote selects should set `filterField` explicitly.

Static options warning:

- `SchemaNormalizerService.parseOptions` supports `valueField`/`displayField` and `key`/`value` object shapes.
- Backend enum helpers currently emit `value`/`label`; do not assume that shape renders correctly without a normalizer fix or explicit evidence.
- For migrated screens, prefer static options shaped as `[{ "valueField": "...", "displayField": "..." }]` or use a real options endpoint.

## Enum Array And Inline Filter Contract

Enum arrays and list-like filter fields are a cross-layer contract, not only an OpenAPI detail.

Backend requirements:

- The parent property must expose renderable `x-ui` metadata with `options` when the UI will render the field as `multiSelect`, `inlineMultiSelect`, chip input, or another select-like control.
- Options buried only in the array item schema are insufficient unless the current Angular normalizer explicitly reads that shape.
- Resolver code should not create empty `x-ui` blocks for plain arrays that have no enum or options source.
- Tests should include a positive enum array/list case and a negative plain array case.

Runtime validation:

- Execute `/schemas/filtered?path=...&operation=post&schemaType=request` for the exact filter endpoint.
- Confirm the field has the expected `controlType`, `options`, label, and help text.
- Exercise the running filter endpoint with at least one valid selected value.
- In browser, select one inline option and verify it appears once. Duplicate selected text or chips usually indicates a renderer/normalizer mismatch, even when the backend predicate is correct.

Corporate UX guidance:

- Use labels that describe the operator's intent, such as `Mostrar status` and `Ocultar status`.
- Use tooltips/help text for inclusion/exclusion pairs so operators understand whether selected values are kept or removed from the result.
- Avoid exposing DTO suffixes like `In`, `NotIn`, `Between`, `On`, or `LastDays` as public labels.

## Filterable Relation Contract

`@Filterable` operator aliases must be mapped deliberately.

JPA/specification-backed filters:

- If a FilterDTO property has the same name as the entity/view attribute, `relation` can be omitted.
- If the property is an alias created for an operator, such as `statusIn`, `statusNotIn`, `fimPrevBetween`, `criadoEmOn`, or `ultimosDias`, set `relation` to the real persistent attribute.
- `IN` and `NOT_IN` pairs should normally both point to the same persistent attribute.
- Add a reflective or schema contract test that fails when alias-like `IN`/`NOT_IN` filters omit `relation`.

Legacy SQL/PLSQL-backed filters:

- `@Filterable` helps schema generation, but it does not implement the predicate.
- The service must map each alias to the proven legacy SQL predicate, including null/default handling, authorization scope, date semantics, ordering, and pagination.

Validation examples:

- Use valid enum/option values in filter payloads when testing include/exclude behavior. A `400` for an invalid value proves validation is active; it does not prove the predicate is broken.
- Compare totals for include and exclude cases only when the seed data and expected distribution are known.
- For paired filters, verify that combining include and exclude is either supported with documented semantics or blocked deliberately.

## Schema Resolution Contract

Angular does not rely only on the resource-local `/schemas` redirect. `GenericCrudService` resolves metadata through the global filtered schema endpoint:

- list/detail response schema: `/schemas/filtered?path=/<resource>/all&operation=get&schemaType=response`;
- filter request schema: `/schemas/filtered?path=/<resource>/filter&operation=post&schemaType=request`;
- filter response schema when required: `/schemas/filtered?path=/<resource>/filter&operation=post&schemaType=response`;
- write request schemas when UI exposes commands: matching path, HTTP operation, and `schemaType=request`.

The UI contract is not closed until the exact filtered schema queries used by Angular resolve and carry the expected `x-ui` metadata.

## Flexible Field Schema Contract

Some Angular dynamic form components also request flexible-field metadata through:

- `/schemas/flex?entity=<entityName>`;
- resource-local redirects such as `/<resource>/schemas/flex` that lead to the global flexible schema endpoint.

This is a separate contract from `/schemas/filtered`. A screen can have all filtered schemas working and still emit a runtime error when the dynamic form asks for flexible fields.

Required decision:

- if the resource supports flexible fields, `/schemas/flex?entity=...` must return the expected metadata;
- if the resource does not support flexible fields, the endpoint should return a successful empty result or the migration artifact must record a formally accepted non-blocking residual;
- a `500` from `/schemas/flex?entity=...` is not acceptable as silent noise. Classify it as `blocking` when it prevents the form from rendering, or `residual-backend` when the form continues with the main schema.

## Date Range Contract

Use `dateRange` for period filters only when the value shape and backend semantics are explicit.

Expected shape:

- Angular emits an array `[inicio, termino]`.
- Dates are ISO `yyyy-MM-dd`.
- FilterDTO can use a list/array date field for schema purposes.
- JPA services may combine it with `@Filterable(BETWEEN)`.
- Legacy SQL services must translate the two dates to the actual legacy predicate, such as concomitance/overlap.

Do not implement interval filters as naive `dtini BETWEEN :inicio AND :termino` unless legacy evidence proves that is the real rule.

## Duplicate Contract

FieldSpec supports duplicate draft through:

- `POST /<resource>/{id}/duplicate-draft`;
- `DuplicateDraftResourceService`;
- `DuplicateDraftUtils`;
- `@UISchema(copyOnDuplicate = false)`;
- `@UISchema(unique = true)`.

Rules:

- IDs are not copied.
- Unique fields are not copied.
- Fields marked `copyOnDuplicate = false` are reset.
- Persisting the duplicate is a separate `POST`; the draft endpoint must not mutate.

## Legacy SQL Warning

`@Filterable` is not a substitute for legacy behavior when the service is custom SQL/PLSQL. It is useful for schema and for JPA Specification, but the service must still prove:

- null/default behavior;
- date and number formatting;
- authorization/company scope;
- package session context;
- dependency lookup filters;
- ordering and pagination;
- selected IDs/include IDs behavior.
