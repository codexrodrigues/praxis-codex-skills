---
name: praxis-java-resource-authoring
description: Use when implementing, auditing, or migrating a complete Java/Spring Praxis resource in a host or praxis-api-quickstart: choose read-only versus mutable resource hierarchy, author resource identity and DTO contracts, controller/service/mapper integration, optional structural bulk CRUD update source, filters, lookups, actions, surfaces, capabilities, and focused HTTP or runtime proof.
---

# Praxis Java Resource Authoring

Build a resource as a governed semantic contract, not as a controller plus an
incidental CRUD screen. The canonical baseline is `resource + surfaces + actions + capabilities`; every projection must remain backed by an executable operation.

## Inspect Before Authoring

Read the host's `AGENTS.md`, the affected domain documentation, entity/query
source, existing resource keys and paths, controller/service/mapper, DTOs,
filters, tests, and direct consumers. In the starter, inspect the resource base,
schema resolution, and discovery contracts before adding a host convention.

Classify the work as `local-pequena`, `transversal`, `contrato-publico`, or
`arquitetural`. For a proposed field, endpoint, action, surface, capability,
lookup, stat, export, or metadata shape, classify adherence as
`ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`.

Only a real contract gap justifies a new platform contract. The quickstart is
operational proof, never the canonical owner of a starter or runtime semantic.

## Compose The Resource

1. Establish stable identity: `@ApiResource(resourceKey=...)`, the canonical
   path constant, `@ApiGroup`, resource intent, and a semantic name independent
   of a label or database table. Treat a path/key change as a public identity
   migration across schemas, links, option sources, actions, surfaces, tests,
   HTTP examples, and consumers.
2. Choose the smallest resource base that matches real operations (with exact generic parameter order):
   - read-only query/view:
     - `BaseCrudRepository<E, ID>`
     - `ResourceMapper<E, ResponseDTO, ?, ?, ID>`
     - `AbstractReadOnlyResourceService<E, ResponseDTO, ID, FilterDTO>` (`ID` is 3rd)
     - `AbstractReadOnlyResourceController<ResponseDTO, ID, FilterDTO>` (no `E`, `ID` is 2nd)
   - standard mutable resource:
     - `BaseCrudRepository<E, ID>`
     - `ResourceMapper<E, ResponseDTO, CreateDTO, UpdateDTO, ID>` (`E` is 1st, `ID` is 5th; `applyUpdate(E entity, UpdateDTO dto)` takes `entity` 1st)
     - `AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (`E` is 1st, `ID` is 3rd; call `super(repository, Entity.class)` and override `getResourceMapper()`, `getDatasetVersion()`, `getStatsFieldRegistry()`, and `StatsSupportMode.AUTO` methods)
     - `AbstractResourceController<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (no `E`, `ID` is 2nd; annotate with `@ApiResource(value=..., resourceKey=..., title=..., description=..., icon=..., identity=@ResourceIdentity(...), quickFilters={...})` and `@ApiGroup(...)`; override `getService()` and `getResponseId(dto)`)
   - create/update-only, unit-delete, or collection-command-only (`AbstractCollectionCommandResourceController`): use the canonical specialized base only when the resource genuinely lacks the omitted operation.
   - **Composite Primary Keys (`@EmbeddedId` / `CompositeResourceId`):** When a resource has an **immutable** composite business key (e.g., `VinculoId(Long numfunc, Integer numvinc)` or `DependenteId(Long numfunc, Integer numdep)`), model it as an `@Embeddable` record implementing `CompositeResourceId` and pass it directly as `ID` in `BaseCrudRepository<E, VinculoId>`, `ResourceMapper<..., VinculoId>`, `AbstractBaseResourceService<..., VinculoId, ...>`, and `AbstractResourceController<..., VinculoId, ...>`. The starter automatically serializes/deserializes `VinculoId` as a canonical wire string (`"1001:1"`) across path variables, query parameters (`ids`, `includeIds`), `OptionDTO<VinculoId>`, `RESOURCE_ENTITY` option sources (`valuePropertyPath = "id"`), `@Filterable(relation = "id.numfunc")` / `@Filterable(relation = "vinculo.id")`, composite `Sort` expansion (`sort=id,desc`), tabular exports, and `/schemas/filtered` (`type: "string"`, `format: "composite-id"`, `x-ui.compositeIdComponents`, `x-ui.compositeIdSeparator`). Ordinary `@Embeddable` classes used with `@Embedded` (value objects) do not implement `CompositeResourceId` and remain structured JSON objects while still navigating via `.get(part)` in JPA Criteria without erroneous joins. For optimal UX in `@praxisui/*` tables and forms: expose both `VinculoId id` and the individual business columns (`numfunc`, `numvinc`) in `ResponseDTO`; expose separate editable business fields in `CreateDTO` (`numfunc`, `numvinc`) and construct `new VinculoId(...)` in `ResourceMapper.newEntity`; and omit or mark PK fields `readOnly = true` in `UpdateDTO` (`applyUpdate` never mutates `entity.setId(...)`). Conversely, when a table's natural key includes **mutable** attributes that users edit in `PUT /{id}` (e.g., `FREQUENCIAS` where `dtini` and `codfreq` are editable), use an immutable surrogate PK (`Long id` / `pontlei`) + `UNIQUE` constraint on the natural columns because JPA forbids mutating `@EmbeddedId` components on a managed entity.
   Do not start new work on legacy CRUD/service hierarchies. For a complete copy-paste compiling slice, see `praxis-java-host-project/references/resource-baseline.md`.
3. Define operation-specific response, create, update, filter, and explicit
   command DTOs. `@Schema` describes verified business meaning; `@UISchema`
   describes presentation/control behavior; governance and AI-use metadata are
   deliberate. A filter models predicates, not a reduced create DTO.
   - **100% Entity Column Accounting & Anti-Minimalism Gate:** Never truncate a 20- to 55-column enterprise entity into an 8-field skeletal DTO or a 3-field `FilterDTO`. Every business column on the JPA entity must be accounted for in `ResponseDTO` (using `@UISchema(group = ...)` and `tableHidden = true` for secondary detail fields) and either editable in `CreateDTO`/`UpdateDTO` or governed by a dedicated `@ResourceIntent` (`PATCH` partial form with `@UiSurface(kind = SurfaceKind.PARTIAL_FORM)`) or `@WorkflowAction`. Deliver `@QuickFilter`s on `@ApiResource`, full lifecycle `@WorkflowAction`s, multiple `@ResourceFact`s, a comprehensive `FilterDTO` across all relevant `FilterOperation` families, and real domain business invariants in the `Service`.
4. Implement mapper, service, validation, transactions, and controller as one
   coherent slice. Preserve `RestApiResponse`, canonical `idField`, and `_links`;
   do not introduce host envelopes, endpoint aliases, string-built schema maps,
   or frontend-only id fixes.
   `ResourceMapper.applyUpdate` must preserve identity loaded from the route.
   MapStruct update methods over `@MappingTarget` must ignore `id` and every
   route-owned technical key, or use an equivalent deliberate mapper contract.
   A missing or divergent payload id never clears, replaces, or repairs the
   managed entity identity; do not reinsert it in Angular or after the mapper.
   Resource generators and scaffolds must emit this rule and keep a focused
   generated-source gate that rejects technical-identity assignment in update
   merges.
   Audit lifecycle fields in create, update, inherited DTOs, mappers and internal
   Java writers. A guarded workflow action is ineffective when a cadastral path
   can set the same status/reason. Keep business transitions in their action
   boundary; reject forbidden values explicitly instead of silently reporting a
   successful ignored write. Validate both HTTP binding and direct Java calls,
   protect merge targets, and prove legitimate cadastral edits still work.
   Initial state belongs to the domain: choose it from the existing lifecycle
   and prove the activation/signing journey; do not invent a permissive default.
   A lock query can return a previously managed stale instance: refresh under
   the same lock before deciding the transition. Bound lock acquisition and
   test the actual PostgreSQL behavior; mocks do not prove serialization.
   - Publishing an item ETag alone does not opt the inherited PUT into If-Match. Use `VersionedCreateUpdateResourceService` (`precondition.requireMatch` on the managed persisted version before applying the mapper, paired body/ETag via `ResourceRepresentationResult` / `getEntityResourceVersion(entity)`). For structural bulk CRUD update (`@BulkResourceOperations`, `@BulkEditable`, `BulkFieldChanges`, `bulk-update` / `bulk-update-items`), read [bulk-crud-update-and-versioned-put.md](references/bulk-crud-update-and-versioned-put.md).
5. Add relations only through governed option/lookup contracts. A resource entity
   lookup must prove its source key, `x-ui.optionSource`, filter endpoint,
   selected-value reload, dependencies, authorization, and human display value.
6. Model an explicit business transition as `@WorkflowAction`, with request and
   response schemas, state/authorization checks, negative paths, and capability
   discovery. Model a composed journey as `@UiSurface`. Do not hide either in a
   generic update, method name, or UI button; do not combine action and surface
   on one method without reviewing conflict validation.
7. Add capabilities, availability, stats, export, governance, or related
   resources only when the domain operation exists and the relevant canonical
   contract is fully backed. `/capabilities` aggregates availability; it is not
   an alternate schema or payload definition.
8. For tenant-specific JSONB extensibility (`custom_fields` + `custom_field_definitions`), map the entity column with `@JdbcTypeCode(SqlTypes.JSON)`, annotate `Map<String, Object> customFields` with `@CustomFields(resourceKey = ...)` on `ResponseDTO`, `CreateDTO`, `UpdateDTO`, and `FilterDTO`, and register a `CustomFieldDefinitionProvider` bean so `/schemas/filtered`, server-side validation, `/filter` JSONB predicates, `/export`, and `/schemas/domain` materialize tenant custom fields canonically. For derived business facts/indicators in `/schemas/domain`, annotate the resource with `@ResourceFact` or provide a `ResourceFactCatalogProvider` bean.

Read [resource-delivery-matrix.md](references/resource-delivery-matrix.md) when
planning a resource packet, selecting a proof, or deciding whether an optional
enterprise feature belongs in this delivery.

## Preserve Canonical Boundaries

- `praxis-metadata-starter` owns annotations, resource bases, `/schemas/filtered`,
  `x-ui`, surfaces, actions, capabilities, option-source contracts, and HATEOAS.
- `praxis-config-starter` owns governed decision authoring and config persistence.
  A host may consume an applied materialization but must not recreate its
  authoring, publication, or inference lifecycle.
- `praxis-ui-angular` is the runtime consumer. When a resource publishes a
  public metadata/discovery change, prove its materializability through the
  relevant schema, option, surface/action/capability, error, and stats/export
  consumer path rather than assuming a browser will infer it.

Do not choose semantic scope or execute primary intent through labels, aliases,
keyword lists, route fragments, regexes, or fuzzy matching. Use resource keys,
schemas, actions, surfaces, capabilities, governed catalogs, and declared tools;
text can only help rank already-scoped candidates.

## Produce Evidence, Not Just Files

Before editing a `transversal`, `contrato-publico`, or `arquitetural` resource,
record the canonical owner, affected consumers, public/derived artifacts, focused
tests, and beta migration/breaking risk. For a legacy-backed development
migration, mutations authorized by the process can be performed, but retain a
scoped probe, before/after evidence, and cleanup or rollback plan.

Prove the smallest complete path:

- resource base, CRUD, identity, and `_links`: focused starter or host resource
  tests, including update with absent and divergent payload ids followed by a
  read proving that the route identity stayed stable; for generated resources,
  inspect or assert the generated update implementation so it cannot assign a
  route-owned technical key;
- schema/`x-ui` contract: `/schemas/filtered` and operation resolution proof;
- lookup: filter and by-ids, including dependency and selected-value reload;
- action/surface/capability: positive and negative availability/discovery proof;
- public metadata change: quickstart HTTP proof and relevant Angular consumer
  tests or an explicit reason they are unaffected.

Review docs, OpenAPI/HTTP corpus, quickstart pilots, and Angular materialization
only when the published contract they mirror changes. State explicitly when no
derived artifact applies.

## Companion Skills

- `praxis-metadata-resource-baseline`: resource hierarchy, response envelope,
  HATEOAS, filters, stats, and export base behavior.
- `praxis-dto-annotations`: semantic, UI, governance, AI, filter, and lookup
  annotations on DTOs.
- `praxis-metadata-schema-contracts`: `/schemas/filtered`, schema references,
  OpenAPI, ETag, and `X-Schema-Hash`.
- `praxis-metadata-discovery-capabilities`: actions, surfaces, availability,
  capabilities, cockpit, stats, and export discovery.
- `praxis-metadata-domain-option-sources` and
  `praxis-resource-entity-lookup-backend`: domain governance and option-source
  implementation.
- `praxis-java-host-project`: host bootstrap, dependencies, and local project
  integration.

Close with the resource packet, resolved classifications, canonical owner,
operation matrix, tests run, consumer proof, and outstanding platform gap. A
resource is not complete because its controller compiles; it is complete when
its semantic contract is discoverable and its intended operation is proven.

For clean-context write guards, include create as well as update/actions. The base resource create path may query through its mapper and flush the entire persistence context; checking only beforeCreate can be too late. Reject caller-owned dirty or unbound contexts before the first mapper/repository/policy operation, including the NEVER_APPLIED policy branch. Prove that rejected creates do not flush unrelated managed lifecycle changes.
