# Java API Migration Template

Use this after screen discovery when the user wants backend APIs. Read `references/api-design-patterns.md` and `references/lib-ui-fieldspec-api.md` before filling this file.

## Migration Scope

- Screen:
- API phase: `read-first` / `read-write` / `discovery-only`
- Included flows:
- Deferred flows:
- Explicitly out-of-scope legacy actions:
- Blocking decisions:
- Source artifacts: `component-lineage-matrix.md`, `closure-checklist.md`, `write-risk.md`, Oracle output:
- FieldSpec docs checked: yes/no, paths:

## Blocking Decisions Must Be Resolved Before Implementation

Do not mark an endpoint as `Required Now` while any blocking decision remains about:

- Stable keys or replacement for `ROWID`.
- Scope values and whether special values are public API.
- Authorization source: Java, Oracle session, package/function, or both.
- Oracle package state such as `FLAG_PACK`, including same-connection setup and cleanup with pooled connections.
- Data source confidence below `CONFIRMED_XML`, `CONFIRMED_RUNTIME`, or `CONFIRMED_ORACLE_METADATA`.
- Browser/runtime behavior missing for user-triggered flows that affect binds, filters, tabs, or navigation.
- Write behavior, triggers, packages, generated columns, or side effects.
- Explicit write deferral boundary when the first API phase is read-only.
- `lib-ui-fieldspec` resource contract: controller/service base, DTO, FilterDTO, ID type, `@UISchema`, options endpoints, schema URLs, response envelope, and disabled/501 endpoints.

If any item remains unresolved, mark the endpoint `Candidate` or `Blocked`; do not mark it `Required Now`.

## Endpoint Status Rules

| Status | Use When |
| --- | --- |
| `Required Now` | Needed for the current backend API slice and all gates are closed for this endpoint. |
| `Candidate` | Likely needed, but key/scope/source/runtime/parity is not closed. |
| `Blocked` | Needed eventually, but a known blocker prevents implementation. |
| `Deferred` | Intentionally outside current phase with evidence-backed future checks. |
| `Not API` | UI-only, display-only, debug-only, or internal legacy behavior. |

Do not use table/view names as endpoint names unless they match the business resource. Do not expose `ROWID` publicly unless explicitly justified and accepted.

## Component To API Decision Summary

Summarize the decisions from `component-lineage-matrix.md`. Do not create one endpoint per component; group components by business resource and API responsibility.

| Legacy Component(s) | Functional Role | API Translation | Resource / Endpoint | DTO / FilterDTO / Option Impact | Status | Reason / Evidence |
| --- | --- | --- | --- | --- | --- | --- |
|  | `context` | scope/context parameter |  | FilterDTO/context provider | Candidate |  |
|  | `main-list` | list endpoint | `POST /<resource>/filter` | response DTO + FilterDTO | Candidate |  |
|  | `detail` | detail endpoint / dto-only | `GET /<resource>/{id}` | detail DTO | Candidate |  |
|  | `lookup` | option resource | `POST /<lookup>/options/filter` | OptionDTO + selected reload | Candidate |  |
|  | `related-resource` | related endpoint |  | related DTO | Deferred |  |
|  | `write-action` | write-risk | blocked | CommandDTO candidate | Blocked | see `write-risk.md` |
|  | `layout-only` | not-api | none | none | Not API | visual structure only |

Use `Candidate`, `Blocked`, or `Deferred` for endpoints whose keys, scope, authorization, source object, runtime binds, parity cases, or write behavior are still unresolved.

## Current Slice Recommendation

State the smallest useful API slice for the migrated screen:

- Required read endpoints:
- Required lookup/context endpoints:
- Candidate related-flow endpoints:
- Deferred write endpoints:
- Explicit non-API UI behaviors:

State whether this is `read-first` or `write-ready`. For `read-first`, write actions must be explicitly blocked/deferred with `write-risk.md` evidence. For `write-ready`, list the closed write routine, trigger, audit, pending, publication/legal-document, permission, validation, and parity evidence.

## lib-ui-fieldspec Resource Contract

| Item | Decision | Notes |
| --- | --- | --- |
| Resource path |  | Prefer application constants or `@ApiResource`; do not edit framework `constants.ApiPaths`. |
| Controller base | `AbstractResourceController<E,D,ID,FD>` | Or explain custom/deviation. |
| Service base | `BaseResourceService<E,D,ID,FD>` | Custom JDBC is allowed behind this boundary. |
| Entity/read model |  | JPA entity, projection, view model, or custom row model. |
| DTO |  | Include `@UISchema` requirements. |
| FilterDTO |  | Extends `GenericFilterDTO`; map legacy filters. |
| ID type |  | Must be stable public id; avoid `ROWID`. |
| Response envelope | `RestApiResponse` | Note unwrap compatibility only if supported/allowed. |
| Default sort |  | Preserve legacy order plus deterministic tie-breaker. |
| Dataset version |  | `X-Data-Version` yes/no/source. |
| Schema URLs |  | `/schemas/filtered` request/response paths. |

## Target App Integration Checklist

| File / Area | Required Check | Decision / Change |
| --- | --- | --- |
| `ApiEndpoints.java` | Add or reuse `<RECURSO>_PATH`, `<RECURSO>_GROUP`, `<RECURSO>_TAG` |  |
| `SwaggerConfig.java` | Add or reuse `GroupedOpenApi` for the resource |  |
| `SwaggerValidationConfig.java` | Confirm group logging/validation still works |  |
| `application.yaml` | Confirm context path, springdoc path, datasource/profile, and uifieldspec settings |  |
| Existing controllers | Reuse/extend existing resource or create new one |  |
| Existing DTOs/FilterDTOs | Reuse/update PT-BR labels, x-ui controls, filters, dependencies |  |
| Existing services | Reuse/update option endpoints, filters, includeIds, default sort, custom SQL |  |
| Tests/scripts | Update OpenAPI/x-ui/HTTP assertions |  |

## Java Implementation Checklist

Use this only for endpoints marked `Required Now`.

| Layer / File | Required Implementation | Status |
| --- | --- | --- |
| Endpoint constants | Path/group/tag added or reused in app-level constants |  |
| Swagger/OpenAPI group | `GroupedOpenApi` added or reused; schema resolver still works |  |
| Controller/resource | Uses `AbstractResourceController` or documents custom deviation |  |
| Service | Implements `filterWithIncludeIds`, id lookup, options, unsupported endpoints, scope and authorization |  |
| Query/repository | Preserves legacy SQL predicates, binds, ordering, pagination, and Oracle package context |  |
| DTO | PT-BR `@Schema`/`@UISchema`, visibility, conversion, hidden/internal fields |  |
| FilterDTO | Dynamic filters, control metadata, payload shape, null/default behavior |  |
| Options | `/options/filter` and `/options/by-ids` return `OptionDTO` shape |  |
| Mapper | Oracle/projection rows convert to API DTOs consistently |  |
| Tests/scripts | OpenAPI/x-ui, filter, options, unsupported writes, and parity checks |  |

## Standard Endpoint Enablement

| Standard Endpoint | Status | Reason / Implementation |
| --- | --- | --- |
| `POST /filter` | Required Now / Candidate / Blocked | Main grid/list. |
| `GET /{id}` | Candidate / Blocked | Requires stable key. |
| `GET /by-ids` | Candidate / Blocked | Needed for selected records. |
| `POST /options/filter` | Candidate / Required Now | Select/lookup options. |
| `GET /options/by-ids` | Candidate / Required Now | Rehydrate selected options. |
| `POST /filter/cursor` | 501 / Candidate / Required Now | Cursor pagination if implemented. |
| `POST /locate` | 501 / Candidate / Required Now | Locate selected row if implemented. |
| `GET /all` | Schema/small datasets only | Avoid for large legacy tables. |
| `GET /schemas` | Required Now | UI schema discovery. |
| `POST/PUT/DELETE/DELETE batch` | Blocked / Deferred / Required Now | Only when write-risk is closed. |
| `POST /stats/*` | 501 / Candidate / Required Now | Only when useful and supported. |

## Scope Semantics

Document special values and current-session dependencies. Example:

| Value | Meaning | Source | API Representation | Confidence |
| --- | --- | --- | --- | --- |
| `-2` | no company association | view SQL | enum/value object |  |
| `-1` | all/global | view SQL | enum/value object |  |
| `N` | company id | view SQL | numeric company id |  |

## Authorization Policy

State whether each rule remains in Oracle or moves to Java:

| Rule | Legacy Source | Java Strategy | Risk |
| --- | --- | --- | --- |
| Current user |  |  |  |
| Current company |  |  |  |
| Current transaction |  |  |  |
| Oracle package context |  |  |  |
| Company access |  |  |  |

## REST Contract

For each endpoint:

```text
METHOD /path
Purpose:
Legacy source:
Status: Required Now | Candidate | Blocked | Deferred | Not API
Blocking decisions:
Path variables: name, type, required, validation
Query params:
Pagination: default page/size, max size, response envelope fields
Sorting: default, allowed fields, deterministic tie-breaker
Filters: name, type, matching rules, legacy function equivalence
Authorization/scope: caller, company/user source, accepted special values, Oracle package context setup if applicable
Response DTO:
Capability flags:
FieldSpec/x-ui notes:
Example request:
Example response JSON:
Errors: HTTP status, project error shape, functional code, field errors
Oracle failures/timeouts:
Parity cases: executable legacy query/action and API assertion
```

## List Endpoint Details

| Endpoint | Legacy Grid/SQL | Default Binds | Default Sort | Page Size | Max Size | Total Count Strategy | Required Tie-Breaker |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Lookup Endpoint Details

| Endpoint | Legacy Component | Source SQL/Object | Parent Filter | Returned Fields | Authorization/Scope | Cacheable |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Key Design

For every detail, update, delete, related-list, or navigation endpoint, document key strategy before choosing a path:

| Endpoint | Candidate Key | Source | URL Safe | Stable Across Environments | Pros | Risks | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | natural key |  |  |  |  |  |  |
|  | composite key |  |  |  |  |  |  |
|  | surrogate/id column |  |  |  |  |  |  |
|  | `ROWID` |  |  |  |  |  | rejected unless explicitly justified |

If using a composite path id, specify delimiter, percent-encoding behavior, and parsing errors. Prefer separate path/query fields when the composite form is brittle.

## DTO Field Map

| DTO | Kind | Field | JSON Type | Source Column | Source Type | Nullable | Validation | Conversion | Stable Key | Read Only | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | list/detail/lookup/write |  |  |  |  |  |  |  |  |  |  |

## FieldSpec x-ui Map

| DTO / FilterDTO | Field | Legacy Label | FieldSpec Type | Control Type | UI Flags | Options Endpoint | Filter/Sort Field | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | readOnly/hidden/tableHidden/formHidden/filterable |  |  |  |

## Control Availability Check

Before choosing specialized controls such as `DATE_RANGE` or `RANGE_SLIDER`, verify FieldSpec/backend support.

| Control Need | Candidate `controlType` | FieldSpec Enum | FieldSpec Resolver | Example/Test | Decision |
| --- | --- | --- | --- | --- | --- |
| Date interval | `dateRange` | `FieldControlType.DATE_RANGE` |  |  |  |
| Numeric range | `rangeSlider` or alternative | `FieldControlType.RANGE_SLIDER` |  |  |  |

PT-BR review:

- Labels and descriptions preserve accents and legacy business terms:
- No raw XML ids, Archon tokens, procedure names, or column-only labels leak into UI:
- Hidden/internal fields are clearly marked:
- Existing module terminology was checked against similar DTOs:

## Filter Implementation Map

Dynamic filter schemas do not implement business behavior by themselves. Map every filter to backend logic.

| FilterDTO Field | Legacy UI Field(s) | UI Control | UI Payload Shape | Java Type | Legacy Bind / SQL Semantics | Backend Implementation | Null/Default Behavior | Parity Case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| periodo | Início + Término | `dateRange` | confirm `start/end` vs array | `List<LocalDate>` or equivalent | interval overlap / concomitance | custom SQL/JDBC or `@Filterable(BETWEEN)` only if equivalent |  |  |
|  |  |  |  |  |  |  |  |

For each filter, also state whether it updates an existing FilterDTO or requires a new one.

## Business Implementation Map

| Behavior | Legacy Evidence | Java Layer | Implementation Decision | Tests / Parity |
| --- | --- | --- | --- | --- |
| list query | XML/runtime SQL | repository/query object |  |  |
| authorization/scope | function/package/access flags | service + query context |  |  |
| dynamic lookup | combo/search SQL | lookup resource service |  |  |
| dependent lookup | parent/child XML bind | lookup service + `@UISchema` dependency metadata |  |  |
| validation | XML/PLSQL/browser error | service/domain or legacy routine |  |  |
| write routine | `write-risk.md` | blocked / legacy routine / Java reimplementation |  |  |

Required decisions for custom filters:

- whether the annotation is only UI metadata or also drives a JPA predicate;
- exact service/query method that translates the filter;
- validation for malformed dependency or range payload;
- behavior when the filter is null, blank, partially filled, or outside allowed scope;
- parity case comparing legacy screen/runtime behavior to API result.

Conversions to document explicitly:

- `S/N` to boolean.
- `CHAR(1)` flags to enum/boolean.
- `ROWID` exposure or replacement by stable natural key.
- Derived link fields such as `Consultar/Editar`.
- Lookup descriptions versus ids.
- Java validation annotations or equivalent rules, such as required fields, max length, numeric precision, enums, and date/number formats.
- Response versioning or compatibility notes when the API contract may evolve.
- Date interval filters should use a UI range control when the screen has start/end semantics. For legacy Oracle SQL, document the exact manual predicate instead of assuming JPA `BETWEEN` is equivalent.

## Capability And Button State Map

Use this only when the backend API deliberately exposes action availability.

| Capability | Legacy Evidence | API Field Or Policy | Scope/User Dependency | Status |
| --- | --- | --- | --- | --- |
| canCreate |  |  |  | Candidate |
| canEdit |  |  |  | Candidate |
| canDelete |  |  |  | Candidate |
| canDuplicate |  |  |  | Candidate |
| canViewPending |  |  |  | Candidate |
| canViewPublication |  |  |  | Candidate |

## Error Semantics

Recommended defaults unless the local project has a stronger convention:

| Case | HTTP | Body/Behavior |
| --- | --- | --- |
| Empty list | `200` | empty `items` |
| Invalid filter/scope value | `400` | validation error |
| No access to company/scope | `403` | access error |
| Detail not found | `404` | not found |
| Write in read-only migration phase | `405` or not implemented | explicit unsupported operation |
| Oracle timeout/failure | project convention | include correlation/log id without leaking SQL data |

## Parity Matrix

| Case | User/Company Fixture | Legacy Action Or Query | Legacy Expected | API Request | API Expected | Comparison Fields | Automation Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| default list |  |  | count, order, key fields |  |  |  |  |
| company scope |  |  |  |  |  |  |  |
| special value `-1` |  |  |  |  |  |  |  |
| special value `-2` |  |  |  |  |  |  |  |
| filter by code |  |  |  |  |  |  |  |
| filter by name |  |  |  |  |  |  |  |
| related codes |  |  |  |  |  |  |  |
| empty result |  |  |  |  |  |  |  |
| no access |  |  |  |  |  |  |  |
| selected detail |  |  |  |  |  |  |  |
| deferred write action |  | visible button / write-risk | blocked/deferred |  | blocked/deferred error or no endpoint |  |  |

## Implementation Skeleton

Record the intended Java structure without forcing package names:

| Layer | Class/Responsibility | Notes |
| --- | --- | --- |
| Controller/Resource |  | paths, validation, response envelope |
| Service |  | `BaseResourceService`, authorization, scope semantics, orchestration |
| Repository/Query object |  | SQL, binds, pagination, same-connection Oracle context if needed |
| Mapper |  | Oracle row to DTO conversions |
| Tests |  | integration and parity coverage |
| HTTP examples |  | `/filter`, `/options/filter`, `/by-ids`, `/schemas`, enabled writes |

## Required Verification

| Check | Command / Evidence | Status |
| --- | --- | --- |
| Maven/test target compiles |  |  |
| OpenAPI group exists | `/v3/api-docs/{group}` |  |
| Filter request schema resolves | `/schemas/filtered?...schemaType=request` |  |
| Response item schema resolves | `/schemas/filtered?...schemaType=response` or `GET /all` schema |  |
| x-ui labels and controls are correct | OpenAPI schema or script assertion |  |
| Options endpoint returns `valueField`/`displayField` | `/options/filter` and `/options/by-ids` |  |
| Unsupported endpoints behave intentionally | cursor/locate/stats/write |  |
| Legacy parity cases pass or are explicitly blocked | default list, every visible filter, options, empty result, no access, selected detail |  |

## Implementation Notes

Inspect the target module and starter convention before choosing persistence mechanics. Prefer the existing Spring Data/JPA, service/repository, `EntityManager`, starter helper, or shared legacy executor pattern already used by the module. Do not make `NamedParameterJdbcTemplate` the default standard just because the source is a legacy Oracle view. Use lower-level JDBC only behind a shared same-connection executor when package state, callable PL/SQL, or Oracle session context requires it. If SQL depends on `FLAG_PACK` or similar package state, initialize and clean it up on the same physical connection/transaction as the query before connection reuse.

When write behavior is deferred, state that explicitly in the contract and link `write-risk.md`. Do not leave write as a vague future task; record whether it is `Blocked for write API`, `Deferred`, or `Out of scope`, and list the exact legacy routines/triggers/packages that force that decision.
