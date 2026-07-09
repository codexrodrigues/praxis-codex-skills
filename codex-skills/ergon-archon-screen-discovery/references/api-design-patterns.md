# API Design Patterns For Ergon/Archon Migration

Use this after browser/XML/Oracle discovery when the user asks for Java APIs or when `api-contract.md` is being prepared. In this migration workspace, also read `references/lib-ui-fieldspec-api.md` because API implementation should follow `lib-ui-fieldspec` unless the target module has a stronger local pattern.

## API Design Goal

The API contract must explain how each legacy screen behavior becomes a stable backend resource without leaking Archon implementation details such as `ROWID`, UI-only link fields, debug parameters, or unverified Oracle package state.

Design APIs from confirmed behavior, not from table names.

For Java implementation, prefer the `lib-ui-fieldspec` resource shape: `AbstractResourceController`, `BaseResourceService`, `GenericFilterDTO`, `@UISchema`, `OptionDTO`, `RestApiResponse`, `/filter`, `/options/*`, `/by-ids`, and `/schemas`.

When the work moves from contract to code, also use `java-api-implementation-playbook.md`. A materialized API includes application wiring, controller/resource, service/query behavior, DTO/FilterDTO metadata, options endpoints, mapper/conversion code, unsupported endpoint behavior, and tests.

## Endpoint Classification

Classify every candidate endpoint before implementation:

| Status | Meaning |
| --- | --- |
| `Required Now` | Needed for the current backend API slice and all gates are closed for that scope. |
| `Candidate` | Likely endpoint, but key, scope, source, authorization, runtime behavior, or parity is not closed. |
| `Blocked` | Needed eventually, but unsafe because a blocking dependency is known. |
| `Deferred` | Intentionally out of current phase; blocker and future evidence are documented. |
| `Not API` | UI-only behavior, static label, derived display field, or legacy helper that should not become a public endpoint. |

Never mark a write endpoint `Required Now` until `write-risk.md` is closed as `Write API ready`.

## Read API Slices

Most screen migrations should start with read slices:

1. Context/selectors: servidor, vinculo, empresa, perfil, transaction scope.
2. Main list/grid: filters, pagination, sorting, default bind values.
3. Detail/read panel: stable key, selected-row behavior, hidden fields needed by the API.
4. Lookups: combo/search fields and dependent lookup values.
5. Related tabs: only if visible and needed in the first migrated screen.
6. Related navigation: expose as links or separate endpoints only when the destination flow is in scope.

For read-first delivery, write actions may be returned as capability flags or omitted. Do not create fake write endpoints that only mirror button labels.

Read-first is a valid delivery state only when write is not an unknown. It must be explicitly `Blocked` or `Deferred` with evidence from `write-risk.md`.

## Write API Slices

Use [archon-write-patterns.md](archon-write-patterns.md) and `write-risk.md` before write API design.

For each write action, decide:

- `legacy-routine`: API calls the existing `db:*` routine after setting the same Oracle session context.
- `java-reimplementation`: Java reproduces the validations, side effects, triggers/package expectations, and pending behavior.
- `blocked`: write remains unavailable until legacy behavior is fully modeled.

Write contract must include:

- operation type and legacy operation parameter;
- payload fields and source XML components;
- stable key or row selection strategy;
- publication/legal-document fields;
- pending-record behavior and approval flow;
- validation errors and legacy messages;
- same-connection session context;
- transaction/rollback/autonomous transaction behavior;
- parity cases for insert, update, delete, duplicate, invalid input, no permission, pending on, and pending off.

## Resource Shape

Prefer resource names from business meaning and screen title, not physical table names alone.

Good candidates:

- resource base `/api/administracao-pessoal/frequencias` with `POST /filter` for the main grid;
- lookup resource `/api/administracao-pessoal/frequencia-tipos` with `POST /options/filter`;
- lookup resource `/api/administracao-pessoal/frequencia-codigos` with dependent `POST /options/filter` filters.

Avoid:

- exposing `ROWID` in public URLs;
- naming endpoints after views such as `/ergadm00189-frequencias`;
- one endpoint per XML component when components are only UI layout;
- generic `/query` endpoints unless the project already has that standard.
- custom `/search` endpoints when `POST /filter` from `lib-ui-fieldspec` is sufficient.

## Key Strategy

Choose the key before detail/update/delete endpoints:

| Priority | Key Type | Notes |
| --- | --- | --- |
| 1 | Stable domain/surrogate key such as `ID_REG` | Requires uniqueness evidence and authorization check. |
| 2 | Natural/composite key | Use separate path/query parameters when delimiter encoding would be brittle. |
| 3 | Legacy internal key | Allowed only for internal service-to-service APIs with documented risk. |
| 4 | `ROWID` | Reject by default for public APIs. Justify only if there is no stable alternative and the team accepts environment-specific behavior. |

Every chosen key needs:

- source column;
- uniqueness proof;
- URL encoding rule;
- not-found behavior;
- authorization check;
- parity case from legacy selected row to API detail.

## DTO Rules

Every DTO field needs source and confidence:

- source component and source column/expression;
- Oracle type and JSON type;
- nullability and default behavior;
- conversion such as `S/N` to boolean, formatted quantity/date to typed value, or code/description pair;
- whether the value is input, output, or read-only;
- whether it is UI-only, derived, stable, or internal.

Do not expose display-only fields as canonical write inputs without checking the underlying code/id field.

For `lib-ui-fieldspec`, DTO and FilterDTO design must also define `@UISchema` metadata for user-facing fields and select/options behavior. Important fields should state label, control type, data type, read-only/hidden/table-hidden/form-hidden status, validation hints, and option endpoint metadata.

## Scope And Session Context

Document scope as part of the contract, not as an implementation note:

- current user mapping to legacy `USUARIO`;
- company/servidor/vinculo/profile source;
- transaction code used for `FLAG_PACK`;
- special values such as `-1`, `-2`, null, blank, and default dates;
- same physical Oracle connection strategy for package state;
- cleanup/reset before returning pooled connections.

If the legacy SQL uses `FLAG_PACK`, `PACK_HADES`, `PACK_ERGON`, profile functions, or access-pattern flags, the API is not ready until this is either implemented or explicitly accepted as a prerequisite.

## Pagination, Sorting, And Filtering

For each list endpoint:

- preserve legacy default ordering unless the API contract explicitly changes it;
- add a deterministic tie-breaker when the legacy sort can produce unstable pages;
- document page base, default size, max size, and total-count strategy;
- map filter null/empty/default semantics from XML/runtime binds;
- keep lookup filters separate from main-list filters when they have different authorization or source objects.

## Error Semantics

Map legacy behavior to API errors deliberately:

| Legacy Case | API Decision |
| --- | --- |
| Empty grid | `200` with empty `items`. |
| Invalid filter format | `400` validation error. |
| No scope/user permission | `403` or project access error. |
| Selected row no longer exists | `404`. |
| Write button visible but write phase deferred | `405`, `501`, or omitted endpoint, following project convention. |
| PL/SQL validation error | Field/global validation error preserving useful legacy message. |
| Oracle/package failure | Project error envelope with correlation id; no SQL or credentials in response. |

## Parity Gates

An endpoint is API-ready only when it has executable parity cases:

- default list with same user/scope;
- each visible filter;
- special scope values;
- empty result;
- access denied;
- detail by chosen key;
- related tab/list if included;
- write success/failure cases when write is in scope.

Record both the legacy action/query and the API assertion. A parity case that cannot yet run should keep the endpoint `Candidate` or `Blocked`.

## ERGadm00189 Read-First Example

Likely first slice:

- `GET /servidores/{numfunc}/vinculos/{numvinc}/frequencias`
- `GET /servidores/{numfunc}/vinculos/{numvinc}/frequencias/{idReg}` only after `ID_REG` uniqueness is confirmed.
- `GET /frequencias/tipos`
- `GET /frequencias/tipos/{tipo}/codigos`
- Pending/publication/legal tabs as `Candidate` until scope is chosen.

Blocked/deferred write:

- create/update/delete/duplicate must remain blocked until `ERG_DML_FREQ_FORMATO`, `FREQUENCIAS` triggers, `PCK_FREQUENCIAS`, `PCK_FREQUENCIAS_PND`, publication, legal documents, and `FLAG_PACK` behavior are fully specified.

For a filled contract model, read `example-ergadm00189-api-contract.md`.
