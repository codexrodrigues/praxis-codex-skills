# Read Parity Matrix Template

Use this artifact before handing a screen from discovery to read API implementation, and update it again after Java/API execution. Its purpose is to prevent a read endpoint from being treated as closed just because XML, Oracle, or Java code exists.

## Status

- Screen:
- Current read state: `Candidate` / `Implemented but needs parity` / `Parity closed` / `Blocked`
- Legacy runtime captured: yes/no/manual-only
- Java/API executed: yes/no
- Last updated:

## Endpoint Coverage

| Read case | Legacy evidence | Oracle source | Java/API evidence | Status | Required parity check | Gap / decision |
| --- | --- | --- | --- | --- | --- | --- |
| Main list default load | XML/runtime component, default selectors, page size, default sort | View/table/function | Controller/service/repository/HTTP endpoint | Candidate / Implemented / Executed / Blocked | Same user/company, first page, row count, visible columns, default sort |  |
| Main list search/filter | Runtime filter action and changed bind values | Predicate/bind behavior | FilterDTO/service query | Candidate / Implemented / Executed / Blocked | Empty/null/default, text search, exact filters, case/accent behavior if relevant |  |
| Pagination and ordering | UI footer/page controls, XML page size/order | SQL order by and count strategy | API pageable/sort behavior | Candidate / Implemented / Executed / Blocked | Page size, next/previous, deterministic tie-breaker, total count |  |
| Detail by public id | Row selection/detail panel, hidden fields | Key columns/view row | `GET /{id}` or equivalent | Candidate / Implemented / Executed / Blocked | Stable id, no public `ROWID`, not-found behavior |  |
| Options/lookup | Combo/select/search component | Lookup SQL/view | `/options/filter`, `/options/by-ids` | Candidate / Implemented / Executed / Blocked | Label, value, ordering, search, by-ids rehydration |  |
| Related tab/list | Tab/link runtime behavior | Related view/table | Related resource endpoint | Candidate / Implemented / Executed / Deferred | Parent binds, lazy load, empty state, row count |  |
| Authorization/scope | Visible user/company/profile and HADES access | Package/session/security function | Java identity/context handling | Candidate / Implemented / Executed / Blocked | Allowed, denied, company-scoped, special values |  |

## Runtime Bind Matrix

| Component | Bind token/order | Source evidence | Default/runtime value semantics | API exposure decision | Parity status |
| --- | --- | --- | --- | --- | --- |
|  |  | XML / browser / Oracle metadata / component reuse |  | public filter / server-side scope / constant bind / parent-row context / internal runtime |  |

When a Cronos bind is closed by XML plus Oracle metadata instead of browser
automation, record the evidence as `BIND_SEMANTICS_CLOSED_BY_XML_ORACLE` and
link the Oracle output. This is valid for bind semantics and scope classification,
not for visible workflow, restricted-user behavior, write payloads, or final
legacy/API parity.

## Field Mapping

| DTO field | Legacy visible label | Oracle column/expression | Type/nullability | UI visibility | Conversion/default | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Executed Parity Runs

| Run | Legacy input/context | Legacy result summary | API request | API result summary | Status | Evidence file |
| --- | --- | --- | --- | --- | --- | --- |
| Default list |  |  |  |  | Pending / Pass / Fail |  |
| Search/filter |  |  |  |  | Pending / Pass / Fail |  |
| Detail |  |  |  |  | Pending / Pass / Fail |  |
| Options |  |  |  |  | Pending / Pass / Fail |  |

## Closure Rules

- `Implemented but needs parity`: Java/API code exists, but HTTP/API output was not compared to legacy runtime/Oracle evidence.
- `Parity closed`: all required read endpoints for the current migration slice have executed parity evidence or an explicit, accepted deferral.
- Keep related tabs/popups as `Deferred` only when their parent screen can work without them and the deferral says which later skill/phase owns them.
- Do not mark read parity closed if public key strategy, scope/session context, filters, options, pagination, or related required reads remain unknown.
