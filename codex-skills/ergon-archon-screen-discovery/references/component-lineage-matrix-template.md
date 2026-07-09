# Component To API Inventory Template

Use this matrix to classify each relevant legacy Cronos/Archon component by API impact. The goal is not to recreate HTML. The goal is to decide whether a component becomes an endpoint, DTO field, FilterDTO field, option resource, write operation, related resource, authorization/capability rule, or `Not API`.

This is the fastest handoff artifact for API planning. Keep it small, evidence-backed, and decision-oriented.

## Matrix

| Component XML | Functional Role | Evidence | SQL / Action / Link | Binds / Params / Hidden Keys | API Translation | Resource / Endpoint | DTO / FilterDTO / Option Impact | Status | Blocking Checks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<grid>` | `main-list` | `CONFIRMED_XML` / runtime ref | `sqlSelect ...` | `:pEmpresa`, `#filtro#` | `list-endpoint` | `POST /<resource>/filter` | response DTO + FilterDTO | `Candidate` | key, scope, parity |
| `<combo>` | `lookup` |  | source SQL/view | parent bind | `option-resource` | `POST /<lookup>/options/filter` | OptionDTO + dependent filter | `Candidate` | parent semantics |
| `<recordPanel>` | `detail` |  | selected-row source | id/row locator | `detail-endpoint` / `dto-only` | `GET /<resource>/{id}` | detail DTO | `Candidate` | public key |
| `<recordPanelEdit>` | `write-action` |  | `db:<routine>` | `ROWID`, operation fields | `write-risk` | blocked until write gate | CommandDTO candidate | `Blocked` | routine, triggers, parity |
| `<label/layout>` | `layout-only` |  | none | none | `not-api` | none | none | `Not API` | none |

## How To Fill

- `Component XML`: exact component id or block name from XML/debug.
- `Functional Role`: choose one of `main-list`, `filter`, `lookup`, `detail`, `field`, `related-resource`, `navigation`, `write-action`, `authorization/capability`, `context`, `layout-only`, or `unknown`.
- `Evidence`: runtime/XML/Oracle/local-source confidence and artifact reference.
- `SQL / Action / Link`: `sqlSelect`, option SQL, linked transaction, package/procedure call, or action.
- `Binds / Params / Hidden Keys`: Archon tokens, URL params, hidden fields, selected-row params, defaults, `ROWID`, `ID_REG`, operation flags.
- `API Translation`: choose one of `list-endpoint`, `detail-endpoint`, `filter-field`, `dto-field`, `option-resource`, `related-resource`, `write-risk`, `capability`, `context`, `not-api`, or `defer`.
- `Resource / Endpoint`: endpoint candidate or `none`; prefer business resources over XML/view names.
- `DTO / FilterDTO / Option Impact`: exact DTO field, FilterDTO field, OptionDTO/resource, CommandDTO candidate, or `none`.
- `Status`: `Required Now`, `Candidate`, `Blocked`, `Deferred`, or `Not API`.
- `Blocking Checks`: exact next check needed before implementation.

## Rules

- Do not create one API per visual component. Multiple components can feed one resource.
- Do not list broad dependencies here; keep this matrix at screen-component granularity and decision-oriented.
- If a component introduces a related screen, include the related screen and parameters, not the entire related contract.
- Keep `ROWID` and hidden fields visible in the matrix, but mark them internal unless explicitly approved.
- Mark pure layout, grouping, labels, separators, static text, and visual containers as `Not API` unless they carry data, action, authorization, or source semantics.
- Mark writes as `Blocked` until write-risk closes. Do not infer CRUD from a visible save button.
- Promote an API candidate to `Required Now` only when XML/runtime behavior, Oracle metadata, key strategy, authorization, session context, and parity cases are resolved for the intended scope.
