# Versioned PUT Preconditions And Structural Bulk CRUD Update

   Publishing an item ETag alone does not opt the inherited PUT into `If-Match`.
   Use the Metadata
   `VersionedCreateUpdateResourceService` contract consumed by
   `AbstractCreateUpdateResourceController`: its three-argument update must, in
   one transaction, call `precondition.requireMatch` on the managed persisted
   version before applying the mapper, then flush so `@Version` provides CAS.
   Inspect the concrete superclass as well as the versioned interface: Java
   selects a concrete inherited two-argument update over an interface default.
   The consumed starter must reject the precondition-less entry point before
   loading, hooks or mapping. Starter rc.169 and rc.170 require an explicit host override;
   the governance correction adds that guard in `AbstractBaseResourceService`
   itself, but source/candidate validation is not published adoption. Any custom
   override remains responsible for rejecting with `428`. Prove concrete/base/
   interface dispatch, and keep the mapper from accepting a payload version. Prove HTTP
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
