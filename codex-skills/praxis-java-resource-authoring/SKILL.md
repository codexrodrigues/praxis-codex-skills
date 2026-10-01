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
2. Choose the smallest resource base that matches real operations:
   - read-only query/view: `AbstractReadOnlyResourceController` plus
     `AbstractReadOnlyResourceService`;
   - standard mutable resource: `AbstractResourceController` plus
     `AbstractBaseResourceService` and `ResourceMapper`;
   - create/update-only or unit-delete: use the canonical specialized base only
     when the resource genuinely lacks the omitted operation.
   Do not start new work on legacy CRUD/service hierarchies.
3. Define operation-specific response, create, update, filter, and explicit
   command DTOs. `@Schema` describes verified business meaning; `@UISchema`
   describes presentation/control behavior; governance and AI-use metadata are
   deliberate. A filter models predicates, not a reduced create DTO.
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
   Publishing an item ETag alone does not opt the inherited PUT into `If-Match`.
   Use the Metadata
   `VersionedCreateUpdateResourceService` contract consumed by
   `AbstractCreateUpdateResourceController`: its three-argument update must, in
   one transaction, call `precondition.requireMatch` on the managed persisted
   version before applying the mapper, then flush so `@Version` provides CAS.
   Override any inherited two-argument Java update entry point to reject with
   `428`, and keep the mapper from accepting a payload version. Prove HTTP
   missing `If-Match` (`428`), malformed (`400`), stale and wrong binding or
   resource ID (`412`), and a fresh successful token; also prove the direct
   Java entry point cannot bypass the precondition and two PostgreSQL writers
   cannot commit updates from the same version.
   For the B4-R1 candidate Java migration, inspect Metadata
   `ResourceRepresentationResult`, `AbstractBaseQueryResourceService.findById`,
   and the versioned three-argument update before changing a host override.
   Remove old `getResourceVersion(id)` overrides in favor of
   `getEntityResourceVersion(entity)`; migrate Java callers of `findById` to
   unwrap `.body()` and versioned three-argument PUT implementations to return
   the body/revision pair. Do not retain an alias or second version-query API.
   Capture response DTO and persisted revision from the same managed entity in
   the read transaction or, for PUT, after the last modifying hook and flush.
   Require the captured revision **inside the write transaction** before return:
   `toResourceRepresentation` guards services implementing the versioned
   interface, while a custom implementation must call `requirePersistedVersion`
   itself. The controller's later guard cannot roll back a committed write.
   Do not reread the current version for the header, infer it from client
   `If-Match`, or add a wire field. Inventory security and scope overrides, map
   all Java consumers, and migrate the beta API cleanly. Prove paired body/ETag
   with two PostgreSQL connections and barriers around GET projection and PUT
   response assembly, plus rollback when a versioned service captures no
   revision; this does not certify related graphs or links.
   If the same resource opts into structural bulk CRUD update, inventory its
   real PUT and concrete update DTO first. On `@BulkResourceOperations`, declare
   the PUT's canonical `updateSourceOperationId` and all identity, version, and
   workflow-state wire names accepted by that update DTO/schema in
   `protectedUpdateFields`; omitted semantic roles
   cannot be inferred from naming. The canonical base PUT already carries
   `@BulkResourceOperation(UPDATE_SOURCE)`; preserve its merged annotation on a
   real override and do not create an override only to repeat metadata. Verify
   unique exact operation ID, resource key, OpenAPI group, request `JavaType`,
   and resolved update schema. Compile `@BulkEditable` on that same DTO using
   the configured `ObjectMapper`, not a separate bulk DTO or an isolated
   `TypeFactory`. Migrate constructor consumers to the `ObjectMapper` signature
   and prove they compile. A workflow command is not a generic update source;
   keep its action contract separate. Inspect Metadata
   `BulkResourceOperationBindings`, `BulkOperationStructuralCompiler`, and
   `docs/spec/BULK-CRUD-STRUCTURE.md` before applying the opt-in.
   For a bulk update candidate, reconstruct the complete prior update state
   from the protected domain snapshot before applying only the declared field
   changes. Do not bind a changes fragment to a DTO whose defaults could turn
   omission into a write. Prefer a dedicated full update DTO over inheritance
   from the read/create model; preserve the existing lookup/control metadata.
   Use the compiled per-mode writable/clearable sets with `BulkFieldChanges`,
   then validate exact wire value types before Jackson binding and validate
   both the prior aggregate and the candidate. Neither that SDK nor DTO
   annotations authorize fields, validate candidate values, or make permissive
   Jackson coercion safe. A nullable enum must admit JSON null in its structural
   enumeration before CLEAR is eligible; null is not a domain option to add
   to `x-ui.options`. Prove the generated schema rather than repairing only
   a test fixture. Keep identities and the prior state from one protected
   source; reject a corrupt aggregate rather than repairing it implicitly.
   Distinguish explicit SET/CLEAR intent from a full-state ordinary PUT: when
   the domain restricts editing a field by lifecycle state, an explicit bulk
   field operation must pass that boundary even if its value is unchanged.
   Preserve omitted values, `false`, zero and allowed null distinctly. Prove
   the canonical schema and configured mapper, both modes, invalid types and
   operators, aggregate invariants and ordinary writer/version behavior.
   Structural compilation alone does not publish bulk CRUD capabilities, operational
   readiness, or an executor; require those separate contracts and proofs
   before advertising availability. The lifecycle compiles all declarations
   before filtering operational modes: a valid structural UPDATE without a
   provider need not degrade a coexisting READY command, while an invalid
   source, schema, or UPDATE binding fails the composition closed. Do not
   promise per-operation error isolation for a malformed declaration.
   For candidate operational UPDATE composition, require a singleton profile
   with `SYNC` execution, `EXPLICIT` selection, and `PER_ITEM` outcomes.
   Keep `parametersPointer` on domain commands only; UPDATE supplies none.
   The provider still supplies `identitySchemaPointer` for the appropriate
   explicit target or per-item ID path. Check `capabilities.operations` for `bulk-update` or
   `bulk-update-items` only after provider and durable readiness agree with
   the structural source, schema, and field policy. The capability is a
   `COLLECTION` `POST` with seven lifecycle references and sorted editable
   fields, not proof that the host grants or domain mutation exist. Removing a
   provider makes `requireReady` deny but does not automatically suspend its
   durable READY row; never execute from a stale
   capability snapshot. Follow Metadata `docs/spec/BULK-CRUD-OPERATIONS.md`
   and prove source/consumer discovery plus denial paths before adoption.
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
