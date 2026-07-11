# Conformance Evidence Matrix

## Required Levels

| Level | Evidence | Pass condition |
| --- | --- | --- |
| Static | Resource base, identity, DTO/mapper/service/controller and annotations | Published operations match executable implementation |
| Schema | OpenAPI and schema/discovery endpoints | Keys, paths, schema links, x-ui and discovery resolve canonically |
| HTTP | Real responses, errors, headers, links | Operation, structured failure, ETag/hash and HATEOAS behavior agree |
| Availability | Collection/item allowed and denied fixtures | Catalogs, capabilities and links agree without N+1 or fail-open |
| Persistence/parity | Scoped data read/write and cleanup when applicable | Legacy-backed behavior has reproducible evidence |
| Angular readiness | Direct official runtime consumer/spec | Contract materializes without a consumer-local rule |

## Operation-To-Proof Matrix

| Published operation | Minimum proof |
| --- | --- |
| Read/filter | Filter predicate, paging/sort, response `idField`, `_links`, filtered schema |
| Create/update/delete | Valid write, invalid field/state error, read-after-write, availability/HATEOAS |
| Option source | Filter plus by-ids reload, dependency and selected value behavior |
| Workflow action | Catalog/schema references, allowed execution, denied state/authority case |
| Surface | Catalog/schema references and supported operation/capability alignment |
| Capability | Collection/item snapshot compared with catalogs and `_links` |
| Stats/export | Registry/support mode, capability projection, request/result policy |

## Angular Consumer Map

| Published contract | Official consumer evidence |
| --- | --- |
| Filtered schema, `x-ui`, resource identity | `GenericCrudService`, `SchemaMetadataClient`, schema normalizer |
| ETag and schema hash | `fetch-with-etag` and schema metadata cache specs |
| `_links`, actions, surfaces, capabilities | `ResourceDiscoveryService` and action/surface adapters |
| Option source | Generic CRUD option filter/by-ids and field selection controls |
| Stats/export | Table/analytics/export consumer only when published |

Use `not-applicable` only when the resource does not publish that operation. Use
`blocked` only for an external unavailable prerequisite and record the exact
remaining probe. All evidence must be sanitized and reproducible.
