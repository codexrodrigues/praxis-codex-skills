# Provider Contract Matrix

## Execution Decision

| Situation | Execution mode and provider decision |
| --- | --- |
| Descriptor is fully JPA-executable | Keep JPA eligible; use the default provider. |
| External catalog, remote service, table function, or host query is mandatory | Use `PROVIDER_REQUIRED` and implement a host provider. |
| Host provider should override JPA for one source | Make support predicate precise and order host provider before JPA. |
| Two providers match at the same priority | Treat as configuration error; make ordering explicit. |

## Public Versus Private Data

| Public, descriptor-governed | Private, provider-only |
| --- | --- |
| source key/type, filter and by-ids endpoints, capabilities, display, dependencies, sort/filter policy, reload policy | datasource, credentials, tenant/session handle, internal query name, package, SQL, remote routing details |

## Required Proof

| Behavior | Minimum proof |
| --- | --- |
| Provider selection | `supports` receives descriptor/context/operation and intended provider wins by order |
| Public validation | Invalid request is rejected before provider counters advance |
| Filtering | Search, structured filter, dependency and sort reach typed provider execution |
| Reload | By-ids returns found values in requested order; contextual dependencies reach POST reload when needed |
| Runtime projection | `/schemas/filtered` exposes canonical endpoints, reload and invalid-sort policies |
| External version | Source-specific dataset version avoids resource-table access |
| Privacy | Context attributes and backend details do not appear in schema, response, examples, or client errors |

Do not mark a reusable source with `unsupported-with-waiver` merely to avoid
selected-value reload. A waiver requires an explicit limitation and platform
follow-up; it is not the normal migration route.
