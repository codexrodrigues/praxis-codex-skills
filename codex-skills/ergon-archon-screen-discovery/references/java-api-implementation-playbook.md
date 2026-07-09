# Java API Implementation Playbook

Use this after `api-contract.md` is drafted and the current slice is classified as `read-first` or `read-write`.

This playbook is implementation-oriented. It tells the executor where to edit, what to verify, and when to block instead of coding.

## 1. Confirm Implementation Scope

Before editing Java code, confirm:

- `closure-checklist.md` state is `Ready for read API` or `Ready for write API` for the intended slice.
- `api-contract.md` marks each endpoint as `Required Now`, `Candidate`, `Blocked`, `Deferred`, or `Not API`.
- `write-risk.md` exists when the legacy screen has create/edit/delete/duplicate/pending/publication/legal behavior.
- Write endpoints are disabled, omitted, or intentionally `501` unless `write-risk.md` is `Write API ready`.

Do not implement endpoints marked `Candidate`, `Blocked`, or `Deferred` except for explicit unsupported responses required by project convention.

## 2. Inspect Target Application Wiring

For `ms-administracao-pessoal`, inspect before adding files:

- `api/src/main/java/br/com/ergon/administracao/pessoal/api/ApiEndpoints.java`
- `api/src/main/java/br/com/ergon/administracao/pessoal/configuration/SwaggerConfig.java`
- `api/src/main/java/br/com/ergon/administracao/pessoal/configuration/SwaggerValidationConfig.java`
- `api/src/main/resources/application.yaml`
- existing controller/resource packages
- existing DTO, FilterDTO, service, mapper, option endpoint, and test/script patterns

Prefer extending an existing business resource when it already represents the same concept. Create a new resource only when the current resource boundary would become ambiguous.

## 3. Add Or Reuse Endpoint Constants

Application resources should use application constants, not framework constants.

For a new resource, add:

```java
public static final String FREQUENCIAS_PATH = "/frequencias";
public static final String FREQUENCIAS_GROUP = "frequencias";
public static final String FREQUENCIAS_TAG = "Frequências";
```

Use the path constant in `@RequestMapping` and the tag constant in `@Tag`.

Add or reuse a `GroupedOpenApi` bean:

```java
@Bean
GroupedOpenApi frequenciasApi() {
    return GroupedOpenApi.builder()
        .group(ApiEndpoints.FREQUENCIAS_GROUP)
        .pathsToMatch(ApiEndpoints.FREQUENCIAS_PATH + "/**")
        .build();
}
```

If the module uses a context path, document the final public path in `api-contract.md`.

## 4. Build DTOs For UI And API Behavior

Create DTOs from the API contract, not directly from table columns.

Every user-facing field should specify:

- Java field name;
- JSON name if different;
- source column/expression and confidence;
- `@Schema` label/description in PT-BR when the project uses OpenAPI docs;
- `@UISchema` label/control/type/visibility/options metadata when inference is insufficient;
- read-only/hidden/table-hidden/form-hidden status;
- conversion rule, for example `S/N` to boolean or formatted quantity plus raw value.

Do not expose Archon ids, XML component ids, procedure names, or `ROWID` as user-facing labels.

## 5. Build FilterDTOs As UI Contract And Service Input

`GenericFilterDTO` and dynamic schema generation do not implement business behavior by themselves.

For each filter field, implement or document:

- legacy UI field(s);
- bind token or SQL predicate;
- Java type and payload shape;
- `@UISchema` control metadata;
- `@Filterable` only when the service really uses JPA specifications for that relation;
- manual service/query mapping when using legacy SQL/JDBC;
- null, blank, and default behavior;
- parity case.

Date interval fields should normally use a single `dateRange` control for the UI, but the service must preserve the exact legacy predicate. For ERGadm00189, this means translating the period into the legacy concomitance/overlap logic, not a naive `BETWEEN`.

For select and dependent select filters, also implement:

- `/options/filter`;
- `/options/by-ids`;
- parent filter enforcement in the service;
- `OptionDTO` with `valueField` and `displayField`;
- rehydration of selected values.

## 6. Implement Service Boundary

Prefer the `lib-ui-fieldspec` boundary:

- controller extends `AbstractResourceController<E, D, ID, FD>`;
- service extends or conforms to `BaseResourceService<E, D, ID, FD>`;
- responses use `RestApiResponse`;
- list uses `POST /filter`;
- options use `/options/filter` and `/options/by-ids`;
- schema uses `/schemas` and `/schemas/filtered`.

Custom JDBC or Oracle-specific query objects can live behind this boundary when JPA specifications cannot express the legacy SQL.

The service must define:

- `filterWithIncludeIds` behavior;
- default sort and deterministic tie-breaker;
- page size and max size;
- `findById` and `findAllById` only after stable public key decision;
- `filterOptions` and `byIdsOptions` for option resources;
- unsupported cursor/locate/stats/write behavior;
- same-connection Oracle package context setup and cleanup when needed.

For legacy-backed operations that require `FLAG_PACK` or equivalent package state, keep context resolution centralized. In `ms-administracao-pessoal`, use or create an `ErgonLegacyContextProvider` and replaceable hooks such as `ErgonLegacyUserMapper` and `ErgonLegacyCompanyResolver`. Resource services should pass only the screen transaction and requested/selected company; they should not each inject fallback user/company properties or parse production authentication/session details directly.

## 7. Place Business Logic Deliberately

Use this split:

| Concern | Place |
| --- | --- |
| UI labels, controls, visibility, option endpoint metadata | DTO/FilterDTO annotations |
| Simple JPA filter predicates | `@Filterable` plus repository/specification |
| Legacy SQL predicates, package calls, concomitance, permission functions | service/query object |
| Authorization and scope | service boundary plus Oracle context when needed |
| Business validation | service/domain validation |
| Legacy generated DML behavior | legacy routine call or documented Java reimplementation after write closure |
| Oracle row to API response conversion | mapper |

Do not hide authorization, validation, or SQL semantics in annotations only.

For legacy authorization helpers, distinguish visibility filtering from display metadata. If the screen SQL or generated view uses helpers such as `MOSTRA_FREQ(flag_pack.get_usuario, tipofreq, codfreq)`, `PACK_HADES.PADRAO_ACESSO_TRANS`, profile package functions, or company/user scope helpers, the migrated endpoint must apply the same predicate or a proven equivalent. Do not rely only on columns like `PERMISSAO_USU`, `PERF_ALT`, or `PERF_REM`; those can be returned as row metadata while the legacy screen still filters denied rows.

## 8. Verify Controls Against FieldSpec

Before using specialized controls, check the FieldSpec/backend libraries.

- `lib-ui-fieldspec/src/main/java/com/uifieldspec/FieldControlType.java`
- `lib-ui-fieldspec/src/main/java/com/uifieldspec/extension/CustomOpenApiResolver.java`
- `lib-ui-fieldspec/src/main/java/com/uifieldspec/util/OpenApiUiUtils.java`
- specific `<control>.config.ts`
- existing mocks/tests and target app schema assertions

`dateRange` is the expected date interval control when registry and config are present. Numeric or non-date ranges must be checked separately; do not assume `rangeSlider` works from the backend enum alone.

## 9. Add Tests And Smoke Checks

At minimum, define or update backend checks:

- service/query test using a fake legacy executor/connection when SQL depends on Oracle package state;
- `READ_ONLY` or equivalent route, screen transaction, target object, user/company context, and cleanup-facing executor usage;
- context provider/user mapper/company resolver tests covering default and custom production mapping;
- filter parameter mapping, null/default handling, pagination, and deterministic sort;
- legacy authorization predicate presence when the screen depends on functions such as `MOSTRA_FREQ`; include allowed and denied fixtures in live/API parity when possible;
- `findById`, `/by-ids`, and `includeIds` behavior when exposed;
- unsupported create/update/delete/batch delete behavior, usually controller-level `405` overrides for inherited generic routes.

Then define or update OpenAPI/x-ui checks for:

- `/v3/api-docs/{group}` exists;
- `/schemas/filtered` resolves request schema for `POST /filter`;
- response schema resolves for list item DTO;
- `POST /filter` returns the expected envelope, paging, sort, and filters;
- `/options/filter` returns `OptionDTO` shape;
- `/options/by-ids` rehydrates selected values;
- `x-ui.controlType`, labels, visibility, filters, dependencies, and PT-BR text are correct;
- unauthorized/no-scope behavior follows project convention;
- unsupported endpoints return the intended disabled/501/405 behavior;
- parity cases match legacy SQL/runtime behavior.

For `ms-administracao-pessoal`, inspect existing scripts before creating new ones. Update OpenAPI/x-ui assertions whenever metadata changes.

Record the backend test command/result and first live smoke fixture in `read-parity-results.md`. If a live Oracle/browser fixture is unavailable, mark the endpoint `Implemented with automated backend tests` and list the fixture blocker instead of claiming `Verified`.

## 10. Read-First Versus Write-Ready Decision

Read-first API can proceed when read gates are closed and write behavior is explicitly `Deferred` or `Blocked` with evidence.

Write-ready API requires:

- write routine and payload mapped;
- generated DML and triggers inspected;
- audit, pending, publication, legal document, and session-context side effects known;
- permissions and button-state rules mapped;
- validation and legacy error behavior mapped;
- parity tests for success, invalid input, no permission, pending on/off, and rollback behavior.

When these are missing, implement read endpoints only and document write as blocked/deferred.
