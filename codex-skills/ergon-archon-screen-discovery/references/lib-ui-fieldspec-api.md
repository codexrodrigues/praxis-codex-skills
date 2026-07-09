# lib-ui-fieldspec API Guidance

Use this reference whenever an Ergon/Archon screen investigation moves into Java API design or implementation in this migration workspace.

Local library documentation lives under:

```text
D:/Developer/Techne/ErgonX/migracao/lib-ui-fieldspec
```

Read the current local docs before implementing because the library may evolve:

- `README-RESOURCE-MIGRATION.md`
- `docs/guides/resource-endpoints.md`
- `docs/reference/lib-reference.md`
- `docs/templates/ia-crud-template.md`

Also inspect the target application before designing or editing APIs. In `ms-administracao-pessoal`, the current integration points include:

- `api/src/main/java/br/com/ergon/administracao/pessoal/api/ApiEndpoints.java`
- `api/src/main/java/br/com/ergon/administracao/pessoal/configuration/SwaggerConfig.java`
- `api/src/main/java/br/com/ergon/administracao/pessoal/configuration/SwaggerValidationConfig.java`
- `api/src/main/resources/application.yaml`
- existing controllers, DTOs, FilterDTOs, services, option resources, and HTTP/test scripts under `ms-administracao-pessoal`

## Default API Architecture

Migrated Java APIs should follow `lib-ui-fieldspec` resource-centric conventions unless the target module already has a stronger local pattern.

Default classes:

- Controller: `com.uifieldspec.controller.resource.AbstractResourceController<E, D, ID, FD extends GenericFilterDTO>`
- Service: `com.uifieldspec.service.resource.BaseResourceService<E, D, ID, FD>`
- Filter DTO: `FD extends com.uifieldspec.filter.dto.GenericFilterDTO`
- Option DTO: `com.uifieldspec.dto.OptionDTO<ID>`
- Response envelope: `com.uifieldspec.rest.response.RestApiResponse`
- UI metadata: `com.uifieldspec.extension.annotation.UISchema`
- Optional resource annotations: `@ApiResource`, `@ApiGroup`

Avoid starting new migrated APIs from deprecated `AbstractCrudController` unless the existing target module explicitly requires that migration step.

## Target Application Integration

Before proposing implementation, verify how the target module wires resources.

For `ms-administracao-pessoal`, adding a resource normally requires:

1. Add three constants to `ApiEndpoints.java`:
   - `<RECURSO>_PATH`, for example `"/frequencias"`;
   - `<RECURSO>_GROUP`, for example `"frequencias"`;
   - `<RECURSO>_TAG`, for example `"Frequências"`.
2. Use the path constant in the controller: `@RequestMapping(ApiEndpoints.<RECURSO>_PATH)`.
3. Use the tag constant in `@Tag(name = ApiEndpoints.<RECURSO>_TAG, ...)`.
4. Add a `GroupedOpenApi` bean in `SwaggerConfig`:
   - `.group(ApiEndpoints.<RECURSO>_GROUP)`;
   - `.pathsToMatch(ApiEndpoints.<RECURSO>_PATH + "/**")`.
5. Confirm `OpenApiGroupResolver` remains registered so `/schemas/filtered` can resolve groups.
6. Check `application.yaml` for `server.servlet.contextPath`, `springdoc.api-docs.path`, datasource/profile behavior, and `uifieldspec` settings.
7. Check existing test scripts and docs, such as `scripts/run-consulta-100-test.ps1`, before adding or changing schema/x-ui assertions.

Do not edit framework constants such as `lib-ui-fieldspec/src/main/java/constants/ApiPaths.java` for application resources. Use the application-level `ApiEndpoints.java`.

If the target module already has resource-specific services, DTO conventions, package layout, tests, or OpenAPI grouping, follow those local patterns before using generic examples from the lib docs.

## Standard Resource Endpoints

Design contracts around the library's resource endpoints:

| Endpoint | Use |
| --- | --- |
| `POST /filter` | Main list/grid with filters, paging, sort, and `includeIds`. |
| `POST /filter/cursor` | Cursor/keyset pagination when implemented; otherwise returns `501`. |
| `POST /locate` | Find absolute position/page for a selected id when implemented; otherwise `501`. |
| `GET /all` | Full list, mainly for schema discovery or small datasets. Be careful with large legacy tables. |
| `GET /{id}` | Detail by stable public id. |
| `GET /by-ids` | Load selected records preserving requested order. |
| `POST /options/filter` | Select/lookup options with paging and filtering. |
| `GET /options/by-ids` | Rehydrate selected option values. |
| `POST /`, `PUT /{id}`, `DELETE /{id}`, `DELETE /batch` | Only when write is proven API-ready. |
| `GET /schemas` | Redirects to the filtered schema URL for the resource. |
| `POST /stats/*` | Optional resource statistics when the service supports it. |

For read-first Ergon migration, `POST /filter`, `GET /{id}`, `/options/*`, and schema endpoints are usually more important than raw CRUD.

## OpenAPI And x-ui Contract

API clients should be able to discover field metadata from OpenAPI filtered schemas enriched with `x-ui`.

Use PT-BR labels and descriptions in DTO annotations because they feed the UI directly. Preserve accents and business terminology from the legacy screen, such as `Frequência`, `Código`, `Mnemônico`, `Ônus`, `Início`, `Término`, `Observação`, and `Documentos legais`. Do not normalize user-facing labels to ASCII. If terminal output displays mojibake, verify the file itself is UTF-8 before changing text.

Contract requirements:

- DTO fields that appear in forms, grids, filters, or options should have `@UISchema` when inference is insufficient.
- Use `@UISchema(label=...)` for user-facing field names from the legacy screen.
- Use `@Schema(name=..., description=...)` in PT-BR for DTOs/FilterDTOs when the module uses OpenAPI documentation as part of UI/schema discovery.
- Use `@UISchema(controlType=...)` and `type=...` for dates, numeric fields, booleans, selects, text areas, read-only fields, hidden/internal fields, and formatted quantities.
- Mark ids/internal fields with `readOnly`, `tableHidden`, `formHidden`, or `hidden` as appropriate.
- For select-like fields, define `endpoint`, `displayField`, and usually `filterField`, `sortField`, `sortOrder`, and `optionsPageSize`.
- `OptionDTO` uses `valueField` and `displayField`; do not invent `id/label` or `value/display` response shapes for options.
- `GET /schemas/filtered?path=/api/{resource}/filter&operation=post&schemaType=request` should expose filter schema.
- For list item response schema, prefer the `GET /all` response schema when `POST /filter` wraps the DTO too deeply.

## DTO And UI Control Design

Design DTO annotations from the intended UI behavior, not only from Java/Oracle types.

Before choosing a `controlType`, verify the FieldSpec/API layers.

| Layer | What To Check | Typical Files |
| --- | --- | --- |
| FieldSpec backend enum | Java annotation value exists and serializes to expected `x-ui.controlType` | `lib-ui-fieldspec/src/main/java/com/uifieldspec/FieldControlType.java` |
| FieldSpec resolver | OpenAPI/x-ui inference or annotation processing preserves the control | `lib-ui-fieldspec/src/main/java/com/uifieldspec/extension/CustomOpenApiResolver.java`, `OpenApiUiUtils.java` |

Do not assume a control is API-valid just because it exists in one layer. A valid Java enum without resolver/schema support blocks backend handoff.

| Legacy Field / Need | DTO / FilterDTO Shape | Recommended FieldSpec Metadata | Notes |
| --- | --- | --- | --- |
| Date field displayed in grid/detail | `LocalDate` or `Instant` field on response DTO | `type = FieldDataType.DATE`, `controlType = DATE_PICKER` or `DATE_TIME_PICKER`, `readOnly` when derived | Match Oracle date/time precision and legacy formatting. |
| Date interval filter, such as início/término | `List<LocalDate>` or equivalent range field in FilterDTO | `@Filterable(operation = BETWEEN)`, `type = DATE`, `controlType = DATE_RANGE`, `filterable = true` | A pair of separate legacy fields should usually become one date-range filter for the UI when semantics are interval/concomitance. |
| Numeric range filter | `List<Integer>`, `List<Long>`, or `List<BigDecimal>` in FilterDTO | Prefer paired numeric fields unless FieldSpec resolver/schema support for a range control is proven | FieldSpec has `RANGE_SLIDER`, but the executor must verify backend schema support before using it. |
| Single code lookup | id/code field plus optional description field | `controlType = SELECT`, `endpoint`, `displayField`, `filterField`, `sortField`, `optionsPageSize` | Use `/options/filter`; do not hardcode full option lists unless static and small. |
| Dependent lookup, such as código filtered by tipo | child field with dependency metadata | `dependentField`, `dependencyFields`, `dependencyFilterMap`, `resetOnDependentChange = true` when needed | Confirm payload expected by the UI before implementation; document the mapping in `api-contract.md`. |
| Boolean legacy flag `S/N` | Boolean field in DTO when business meaning is boolean | `type = BOOLEAN`, `controlType = CHECKBOX` or `TOGGLE` | Keep original code only if the API must expose exact legacy value. |
| Numeric amount/quantity | `BigDecimal`, `Integer`, or formatted read-only string plus raw value | `type = NUMBER`, `controlType = NUMERIC_TEXT_BOX`, numeric format/min/max/step when known | For legacy formatted quantities, prefer raw typed value plus formatted display field if both are needed. |
| Long observations/text | `String` | `controlType = TEXTAREA`, max length when known | Match legacy field size. |
| Internal key | ID field | `readOnly = true`, `tableHidden = true`, `formHidden = true` or `hidden = true` | `ROWID` should stay internal unless explicitly accepted. |
| Display-only derived text/link | read-only DTO field or omitted | `readOnly = true`, `formHidden = true` when not editable | Do not make display links canonical API fields. |
| Capability/action state | explicit capability DTO fields or policy outside DTO | Boolean fields with clear names if exposed | Only expose capabilities if the backend API deliberately includes action state. |

Do not rely only on type inference for fields that drive UX. Important fields need explicit `@UISchema` so the UI renders the correct control.

### PT-BR Annotation Rules

For `@UISchema` and `@Schema`:

- labels should be user-facing PT-BR with accents;
- descriptions should explain business meaning, not database implementation;
- placeholders should use PT-BR and match the field's expected search behavior;
- technical names such as `tipoFreq` may stay in Java fields, but labels should be `Tipo de frequência`;
- prefer business terms from the legacy screen unless they are misleading in the new UI;
- keep hidden/internal fields labeled clearly when they appear in schemas, for example `ROWID legado`;
- do not expose raw Archon tokens, XML ids, or procedure names in labels.

Review existing DTOs in the target app for terminology consistency before inventing labels. For frequency resources, compare with `TipoFrequenciaDto`, `CodigoFrequenciaDto`, `DocumentoLegalDto`, and their FilterDTOs.

## Filter Implementation Rules

`lib-ui-fieldspec` can generate filter schemas dynamically, but the backend still needs a real implementation that preserves legacy semantics.

For every FilterDTO field, document and implement:

- source XML/runtime field and bind token;
- Java field name and type;
- UI control type;
- null/blank/default behavior;
- Oracle predicate or legacy function equivalence;
- whether the filter is direct SQL/JPA, dependent lookup, computed, or custom business logic;
- expected test/parity case.

### Date Range Filters

Use a date range when the legacy UI has start/end fields or the SQL checks interval overlap/concomitance.

Before using `FieldControlType.DATE_RANGE`, verify the current control support:

- FieldSpec enum: `FieldControlType.DATE_RANGE("dateRange")`.
- FieldSpec resolver: `CustomOpenApiResolver` / `OpenApiUiUtils` may infer `dateRange` for `BETWEEN` date array filters.

Recommended contract:

```java
@UISchema(
    label = "Período",
    type = FieldDataType.DATE,
    controlType = FieldControlType.DATE_RANGE,
    filterable = true
)
@Filterable(operation = Filterable.FilterOperation.BETWEEN, relation = "dtini")
private List<LocalDate> periodo;
```

Use `@Filterable(BETWEEN)` only when the service is really using JPA Specifications and the relation maps to the correct entity path. For legacy Oracle SQL/JDBC, the DTO can still use `DATE_RANGE` as API metadata, but the service must manually translate `periodo[0]` and `periodo[1]` to the legacy predicate, such as `pack_hades.eh_concomitante(...)`.

For ERGadm00189, the visible `Início`/`Término` filter should be modeled as a range filter for the UI, while the service must preserve the legacy overlap logic from the screen SQL instead of a naive `dtini between :start and :end`.

### Other Range Controls

When the screen needs a range that is not a date interval, do not reuse `DATE_RANGE`.

Check available controls first:

- FieldSpec backend currently includes `RANGE_SLIDER("rangeSlider")` and `DATE_RANGE("dateRange")`.
- Existing app tests may already assert range metadata, for example numeric range filters using `x-ui.controlType=rangeSlider`.

If backend metadata is uncertain, choose a safer supported API pattern and document the gap. Examples:

- two numeric inputs for min/max;
- array input with `filter=BETWEEN` only if the API contract documents it clearly;
- existing `rangeSlider` only when FieldSpec schema tests confirm the emitted metadata.

Every range field must state:

- range value shape sent by UI;
- Java DTO type;
- OpenAPI array/item type;
- `x-ui.controlType`;
- `x-ui.filter` and `x-ui.filterControlType`;
- backend predicate;
- parity case.

### Dynamic Lookups And Options

For select-like filters:

- create a resource endpoint that supports `POST /options/filter`;
- return `OptionDTO<ID>` with `valueField` and `displayField`;
- support `GET /options/by-ids` to rehydrate selected values;
- set `endpoint`, `displayField`, `filterField`, `sortField`, `sortOrder`, and `optionsPageSize` in `@UISchema`;
- implement parent/dependent filters in the child lookup service, not only in annotation metadata.

For dependent lookups, the annotation is only metadata. The backend must enforce the parent filter even if a client sends malformed or missing dependency values.

When the target app already has lookup resources, reuse them instead of creating duplicate lookup APIs. For example, a frequency screen should check existing `tipos-frequencia`, `codigos-frequencia`, `empresas`, and `documentos-legais` resources and update them only if the new screen requires fields, filters, option labels, or dependency behavior they do not already provide.

## Filter DTO Design

Map legacy XML/runtime filters into a `FilterDTO`.

For each filter:

- preserve null/blank/default behavior from Archon binds;
- choose the `@Filterable` operation only when using JPA Specifications;
- for custom Oracle SQL/JDBC queries, still document equivalent filter semantics in the DTO and service;
- represent date intervals, code lookups, special values, and dependent selectors explicitly;
- avoid leaking raw Archon token names such as `#srcTipoFreq#` into Java API field names.

When a migrated endpoint uses custom SQL against legacy Oracle views, the service may not use JPA `Specification`, but the public filter DTO should still follow `lib-ui-fieldspec` conventions so the UI can consume schemas consistently.

## Service Rules For Legacy Oracle

Use `BaseResourceService` as the API boundary even when persistence is custom JDBC instead of a normal JPA repository.

Implementation must decide:

- how `filterWithIncludeIds` maps filters to legacy SQL;
- how `getDefaultSort()` reproduces legacy ordering plus a deterministic tie-breaker;
- how each FilterDTO field is translated to SQL, package call, view predicate, or business rule;
- which filters are deliberately not supported and how validation reports that;
- whether `filterByCursor` and `locate` are implemented or intentionally left as `501`;
- how `findAllById`, `filterOptions`, and `byIdsOptions` work for stable ids;
- whether `getDatasetVersion()` can return a useful value for `X-Data-Version`;
- how same-connection Oracle package context is initialized before query execution.

Do not use `GET /all` for large legacy tables as the primary grid endpoint.

If the endpoint reads legacy Oracle views with package-state functions, prefer a custom repository/query object behind `BaseResourceService` over forcing JPA Specifications that cannot express the legacy predicate correctly.

## Business Logic Placement

Do not put legacy business rules only in DTO annotations.

Use this split:

| Concern | Preferred Place |
| --- | --- |
| Field labels, controls, option endpoints | DTO/FilterDTO `@UISchema` |
| Filter operations for simple JPA-backed resources | `@Filterable` + service/repository |
| Legacy SQL predicates, package calls, concomitance, permission functions | Repository/query object or service method |
| Authorization and Oracle session package setup | Service boundary, same connection as query |
| Validation that protects business invariants | Service/domain validation, not just UI annotation |
| Legacy PL/SQL validation and generated DML behavior | Legacy routine call or documented Java reimplementation |
| Mapping Oracle rows to API response | Mapper |

For migration APIs, `@UISchema` helps the UI render correctly; it does not replace backend validation, authorization, or SQL behavior.

## Existing Resource Update Checklist

When a screen needs APIs, first decide whether to create a new resource or update existing ones.

Investigate:

- `ApiEndpoints.java`: missing path/group/tag constants;
- `SwaggerConfig.java`: missing `GroupedOpenApi`;
- controller package: existing `AbstractResourceController` for the same business resource;
- DTO package: labels, types, visibility flags, `@Schema`, and `@UISchema`;
- FilterDTO package: dynamic filter fields, `filter`, `filterControlType`, `@Filterable`, dependency metadata, and required scope fields;
- service package: `filterWithIncludeIds`, `filterOptions`, `byIdsOptions`, default sort, includeIds behavior, and custom legacy SQL/JDBC;
- configuration: context path, `springdoc.api-docs.path`, `OpenApiGroupResolver`, CORS, datasource/profile, and `uifieldspec` settings;
- tests/scripts: OpenAPI schema assertions, x-ui assertions, HTTP examples, and endpoint smoke tests.

If the resource exists, prefer extending it in a compatible way over creating a second resource with overlapping meaning. Update tests when x-ui metadata changes.

## Implementation Playbook Reference

When moving from contract to code, read `java-api-implementation-playbook.md` and follow it as the execution checklist. In particular, do not stop at DTO annotations:

- wire app-level endpoint constants and OpenAPI group;
- implement controller/resource and service behavior;
- implement custom SQL/JDBC or repository predicates for legacy filters;
- implement option endpoints and selected-value rehydration;
- map Oracle rows to DTOs;
- define unsupported endpoint behavior;
- update OpenAPI/x-ui/parity tests.

For ERGadm00189 or similar frequency screens, compare the planned contract with `example-ergadm00189-api-contract.md`.

## Validation And Smoke Tests

After implementation or contract generation, define checks for:

- `/v3/api-docs/{group}` exists for the new resource group;
- `/schemas/filtered` resolves request and response schemas;
- `POST /filter` returns `RestApiResponse<Page<EntityModel<DTO>>>`;
- `POST /options/filter` returns `OptionDTO` values with `valueField` and `displayField`;
- x-ui fields include expected `controlType`, `filter`, `filterControlType`, `multiple`, dependency metadata, and PT-BR labels;
- hidden/internal fields do not appear in table/form when they should not;
- date ranges are emitted as `dateRange` metadata;
- numeric or other range controls have resolver/schema evidence, not only a FieldSpec enum;
- unsupported cursor/locate/stats/write endpoints return the intended `501`, blocked, or disabled behavior.

For `ms-administracao-pessoal`, inspect and update `scripts/run-consulta-100-test.ps1` or add equivalent tests when adding fields/endpoints that affect OpenAPI/x-ui.

## Write Endpoint Rule

Do not expose `POST`, `PUT`, `DELETE`, or `DELETE /batch` merely because `AbstractResourceController` provides them.

For read-first migration:

- either override/disable write behavior according to the target module convention;
- or keep write endpoints out of the current implementation plan;
- document the blocked/deferred state in `api-contract.md` and `write-risk.md`.

Only implement writes when `write-risk.md` is closed as `Write API ready` and the service can preserve generated DML, triggers, audit, pending records, publication/legal documents, and session context.

## API Contract Additions

Every `api-contract.md` must state:

- whether the endpoint follows `AbstractResourceController` or is custom;
- DTO class, FilterDTO class, ID type, and resource path;
- which standard endpoints are enabled, intentionally `501`, disabled, or out of scope;
- `@UISchema` requirements for important fields;
- `OptionDTO` endpoints for lookups/selects;
- schema URLs exposed by the API;
- response envelope behavior and whether unwrap compatibility is allowed;
- `X-Data-Version` decision;
- HTTP test file or examples covering `/filter`, `/options/filter`, `/by-ids`, `/schemas`, and any enabled write.

## ERGadm00189 Guidance

For a read-first frequency API:

- model the main grid as a resource list with `POST /filter`, not as a custom `/search` unless the target module requires it;
- use `ID_REG` as candidate id only after uniqueness is proven;
- keep `ROWID_REG` internal/hidden if it must be used to call legacy routines later;
- map `Início`/`Término` as a `DATE_RANGE` FilterDTO field and implement the legacy `pack_hades.eh_concomitante` behavior in the service/query;
- map type and code as select/dependent-select filters with `/options/filter` implementations;
- expose frequency type/code lookups through `/options/filter` endpoints;
- annotate formatted quantity/code fields with `@UISchema` rather than relying on raw strings;
- keep create/update/delete/duplicate blocked until the generated DML write stack is closed.
