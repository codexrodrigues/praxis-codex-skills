# Filters, Options, And Lookups

Use this reference when annotating FilterDTOs, option fields, entity lookups, and relationship IDs.

## Contents

- [FilterDTO Shape](#filterdto-shape)
- [Human-Facing Filter Metadata](#human-facing-filter-metadata)
- [Options And Direct Selects](#options-and-direct-selects)
- [Governed Entity Lookup](#governed-entity-lookup)
- [Validation](#validation)

## FilterDTO Shape

Filter DTOs should implement `GenericFilterDTO` and use one `@Filterable` per filterable field.
Prefer starter operations before writing custom query code.

Common operations include:

`EQUAL`, `NOT_EQUAL`, `LIKE`, `NOT_LIKE`, `STARTS_WITH`, `ENDS_WITH`,
`GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `NOT_IN`,
`BETWEEN`, `BETWEEN_EXCLUSIVE`, `NOT_BETWEEN`, `OUTSIDE_RANGE`, `ON_DATE`,
`IN_LAST_DAYS`, `IN_NEXT_DAYS`, `IS_NULL`, `IS_NOT_NULL`, `IS_TRUE`, `IS_FALSE`,
`SIZE_EQ`, `SIZE_GT`, and `SIZE_LT`.

Always set `relation` when the DTO field is an alias or targets a nested property:

```java
@Filterable(operation = Filterable.FilterOperation.IN, relation = "status")
private List<MissaoStatus> statusIn;

@Filterable(operation = Filterable.FilterOperation.BETWEEN, relation = "inicioPrev")
private List<OffsetDateTime> inicioPrevBetween;

@Filterable(operation = Filterable.FilterOperation.LIKE, relation = "departamento.nome")
private String departamentoNome;
```

Without `relation`, the builder may look for a persistent property named like the DTO alias
(`statusIn`, `inicioPrevBetween`, etc.).

## Human-Facing Filter Metadata

Filter labels and help text must describe the user decision, not the operator suffix.

For include/exclude pairs:

```java
@UISchema(label = "Mostrar status", controlType = FieldControlType.INLINE_MULTISELECT,
        helpText = "Mostra apenas missões nos status selecionados.", icon = "mi:toggle_on")
@Filterable(operation = Filterable.FilterOperation.IN, relation = "status")
@Schema(description = "Conjunto de fases que devem aparecer no resultado da busca.")
private List<MissaoStatus> statusIn;

@UISchema(label = "Ocultar status", controlType = FieldControlType.INLINE_MULTISELECT,
        helpText = "Remove do resultado as missões nos status selecionados.", icon = "mi:toggle_off")
@Filterable(operation = Filterable.FilterOperation.NOT_IN, relation = "status")
@Schema(description = "Conjunto de fases que devem ser removidas do resultado da busca.")
private List<MissaoStatus> statusNotIn;
```

For date ranges and relative dates:

- `BETWEEN` fields usually use `DATE_RANGE` or `DATE_TIME_RANGE`.
- `ON_DATE` fields usually use `DATE_PICKER`.
- `IN_LAST_DAYS`/`IN_NEXT_DAYS` fields usually use integer input with helper text.
- `INLINE_RELATIVE_PERIOD` fields must publish explicit allowed options when the UX uses presets.

## Options And Direct Selects

For ordinary remote options, use canonical resource paths centralized in `ApiPaths` or equivalent.
Do not scatter literal URLs in DTOs.

```java
@UISchema(
    label = "Cargo",
    controlType = FieldControlType.SELECT,
    endpoint = ApiPaths.HumanResources.CARGOS_JOB_ROLE_LOOKUP_OPTIONS,
    valueField = "id",
    displayField = "label",
    tableHidden = true,
    helpText = "Cargo ocupado atualmente.",
    icon = "mi:work"
)
private Integer cargoId;
```

The canonical options endpoints are:

- `POST /{resource}/options/filter`
- `GET /{resource}/options/by-ids?ids=1&ids=2`
- `POST /{resource}/option-sources/{sourceKey}/options/filter`
- `GET /{resource}/option-sources/{sourceKey}/options/by-ids?ids=1&ids=2`

## Governed Entity Lookup

This section guides DTO consumer annotation. When implementing or reviewing registry, descriptor,
executor, or policy behavior for option sources, also load `praxis-resource-entity-lookup-backend`.

Use `ENTITY_LOOKUP` or `INLINE_ENTITY_LOOKUP` only for real business entities selected by the user
or workflow. The resource service that owns the source should expose an `OptionSourceRegistry` with
a `RESOURCE_ENTITY` descriptor. Use an external `OptionSourceProvider` only for custom or
provider-required execution.

DTO consumers may point to the named option-source endpoint as a resolver/reference when the host
requires an `endpoint` attribute, but the canonical published contract is `x-ui.optionSource` in
`/schemas/filtered`, enriched from the registered descriptor:

```java
@UISchema(
    label = "Fornecedor",
    controlType = FieldControlType.ENTITY_LOOKUP,
    endpoint = ApiPaths.Procurement.SUPPLIERS_SUPPLIER_LOOKUP_OPTIONS,
    valueField = "id",
    displayField = "label",
    icon = "mi:business"
)
private Integer supplierId;
```

Do not publish DTO-level `optionSource` metadata through `extraProperties` just because
`@UISchema` has no `optionSource` attribute. `/schemas/filtered` should enrich `x-ui.optionSource`
from the registered descriptor. When `optionSource` exists, DTO-level `endpoint`, `valueField`, and
`displayField` do not redefine lookup semantics; they are compatibility/runtime hints at most.

Descriptor metadata should be deliberate:

- stable `sourceKey`;
- `resourcePath`;
- value and label property paths;
- `entityKey`;
- safe search fields;
- dependencies and `dependencyFilterMap`;
- selection policy and disabled reason;
- capabilities such as filter/byIds/detail/create;
- rich `display` fields when the lookup needs directory/reference/status presentation.

Sensitive fields must not be searchable or projected in public option metadata unless explicitly
governed.

## Validation

For changed filters/lookups, prefer focused proof:

- unit/integration test for `@Filterable` relation and generated filtering;
- `/schemas/filtered` contains the expected `x-ui.controlType`, label, visibility, options, or
  `x-ui.optionSource`;
- `POST /{resource}/option-sources/{sourceKey}/options/filter` returns expected options, where
  `{resource}` comes from the option source `resourcePath`;
- `GET /{resource}/option-sources/{sourceKey}/options/by-ids?ids=...` rehydrates selected values in
  the same semantic order expected by the UI and returns labels rich enough for display;
- blocked/inactive values are rehydratable but not selectable when policy says so, with a domain
  disabled reason when the lookup publishes one;
- direct `/{resource}/options/by-ids?ids=...` is proven for direct selects that do not use named
  option sources;
- include/exclude filters remain semantically and visually distinct in metadata.
