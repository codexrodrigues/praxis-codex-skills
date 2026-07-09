# Read Parity Matrix Template

## Status

- Screen:
- Resource:
- Read state: `Candidate` / `Required Now` / `Ready for implementation` / `Implemented` / `Implemented with automated backend tests` / `Schema/static contract passed` / `Executed endpoint smoke` / `Legacy parity pending` / `Smoke-tested against Oracle fixture` / `Verified` / `Blocked` / `Deferred` / `Not API`
- Discovery handoff state: `Ready for read API` / `Read handoff ready; write deferred` / other:
- Evidence sources:
  - `browser-runtime.md`:
  - `component-lineage-matrix.md`:
  - `investigation.md`:
  - `api-contract.md`:
  - Oracle output:

## Endpoint Matrix

| Endpoint | Legacy Component | Source SQL/Object | Public Key | Internal Legacy Key | Scope/Session | Unsupported write behavior | Status |
|---|---|---|---|---|---|---|---|
| `POST /filter` |  |  |  | n/a |  | n/a |  |
| `GET /{id}` |  |  |  |  |  | n/a |  |
| `GET /by-ids` |  |  |  | n/a |  | n/a |  |
| `POST /options/filter` |  |  |  | n/a |  | n/a |  |
| `GET /options/by-ids` |  |  |  | n/a |  | n/a |  |
| `/schemas` |  |  |  | n/a |  | n/a |  |
| `POST create` |  |  |  |  |  | omitted / 405 / 501 / override |  |
| `PUT update` |  |  |  |  |  | omitted / 405 / 501 / override |  |
| `DELETE` |  |  |  |  |  | omitted / 405 / 501 / override |  |
| `DELETE batch` |  |  |  |  |  | omitted / 405 / 501 / override |  |

## Session Context

| Requirement | Value / Decision | Evidence | API Implementation Note |
|---|---|---|---|
| Legacy user value |  |  |  |
| Transaction value |  |  |  |
| Company/profile value |  |  |  |
| User mapper | default / custom / n/a |  | Must map production principal to legacy user value when they differ |
| Company resolver | default / custom / n/a |  | Must map requested/session/token/header company to legacy company value |
| Required setters, such as `HADES.FLAG_PACK` |  |  | Must run on the same physical connection used by the query |
| Cleanup/reset policy |  |  | Required before returning pooled connections |
| Persistence convention | Spring Data/JPA / starter service / EntityManager / shared executor / other |  | Do not assume `JdbcTemplate`; inspect module convention first |

## Parity Cases

| Case | Fixture/User/Scope | Legacy Action | API Request | Legacy Expected | API Expected | Fields Compared | Automation Status | Status |
|---|---|---|---|---|---|---|---|---|
| Default load |  | Open screen | `POST /filter` with default filters | same rows/order/page semantics |  | ids, labels, sort fields | manual / automated |  |
| Filter by text/code |  | Fill search field | `POST /filter` with field value | same predicate behavior |  | filtered ids/count | manual / automated |  |
| Date interval |  | Use date filters | `POST /filter` with date range | same overlap/null behavior |  | interval rows | manual / automated |  |
| Company/scope | company/user, including `-1`/`-2` if present | Change company/scope | request with same scope context | same visible rows |  | ids/count | manual / automated |  |
| Detail by key |  | Select row | `GET /{id}` | same selected record |  | public fields | manual / automated |  |
| Batch by ids |  | Multi-select/reopen | `GET /by-ids` | same records, stable ordering |  | ids/order | manual / automated |  |
| Options |  | Open combo/search | options endpoint | same option set and labels |  | value/label/order | manual / automated |  |
| Related tab/deferred flow |  | Open related area | endpoint or deferred decision | same/deferred behavior |  | ids/count | manual / automated |  |
| Empty result |  | Filter no rows | endpoint returns empty page/list | no false error |  | count=0 | manual / automated |  |
| Unauthorized/scope limited | restricted user/scope | Restricted user/scope | endpoint request | same denial or hidden rows |  | status/count | manual / automated |  |
| Authorization helper predicate | allowed and denied users when helper exists | Screen applies helper such as `MOSTRA_FREQ` | endpoint request under both users | allowed row visible; denied row hidden/forbidden | same; do not return denied rows only flagged as denied | ids/count/status | manual / automated |  |
| Write remains blocked |  | Try create/update/delete if exposed by resource | write request | legacy write is outside read API scope | blocked/omitted as designed | HTTP status/body | automated |  |

## Backend Test Coverage

| Test Target | Required Assertions | Status |
|---|---|---|
| Service/query boundary | route (`READ_ONLY` when applicable), screen transaction, target object, user/company/session context, filters, paging/sort, returned rows | planned / passed / deferred |
| Context provider | user mapper, company resolver, default fallbacks, and custom production hooks | planned / passed / deferred |
| Authorization predicate | legacy visibility helper predicates such as `MOSTRA_FREQ` are present or equivalently implemented; denied rows are filtered, not only marked by permission metadata | planned / passed / deferred |
| Key lookup | `GET /{id}` backing path and `GET /by-ids` order preservation | planned / passed / deferred |
| Include ids | first-page includeIds prioritization when resource supports it | planned / passed / deferred |
| Read-only write block | create/update/delete/batch delete return chosen blocked behavior, usually 405 | planned / passed / deferred |
| OpenAPI/x-ui | group exists, schema paths resolve, labels/control metadata present | planned / passed / deferred |

## Read Parity Results

Create or update `read-parity-results.md` after implementation begins.

Minimum sections:

- backend automated test command, working directory, JDK/toolchain if relevant, and result;
- cases covered by service/controller/OpenAPI tests;
- live Oracle/browser smoke fixture, request, context user/company/transaction, and key returned fields;
- identity and company mapping evidence, including production hook status and fallback behavior;
- link to `production-context-integration.md` when the real authentication principal or selected-company source is not closed;
- allowed/denied authorization fixture evidence when user/profile scope is involved;
- remaining gaps such as filter-change parity, company isolation, restricted users, and production identity mapping.

## Residual Risks

- 
