---
name: praxis-java-resource-authoring
description: "Use when implementing, auditing, or migrating a complete Java/Spring Praxis resource in a host or praxis-api-quickstart: choose read-only versus mutable resource hierarchy, author resource identity and DTO contracts, controller/service/mapper integration, optional structural bulk CRUD update source, filters, lookups, actions, surfaces, capabilities, and focused HTTP or runtime proof."
---

# Praxis Java Resource Authoring

Build a resource as a governed semantic contract, not as a controller plus an
incidental CRUD screen. The canonical baseline is `resource + surfaces + actions + capabilities`; every projection must remain backed by an executable operation.

## Reusable API paths in annotations

Before wiring remote options, create or extend the host-owned `final ApiPaths`
(private constructor, `public static final String` compile-time constants).
Compose resource bases, stable source keys and named filter endpoint constants
once. Reuse them in controllers, `OptionSourceDescriptor`, DTOs, FilterDTOs,
command DTOs, surfaces and links. Do not concatenate option-source paths in each
DTO, put deployment origins in annotations, use a constants interface, call
methods to initialize annotation values, or introduce a DTO `optionSource` field.
Static/enum options need no remote endpoint. Keep governed lookup semantics in
`OptionSourceRegistry` and consume the published runtime endpoints in Angular.
Validate annotation endpoints against descriptor runtime endpoints and controller
mappings; keep independent literal contract fixtures to catch accidental route
changes. Recompile consumers when constants change. For the complete decision,
see `praxis-metadata-starter/docs/guides/API-PATHS-E-OPTION-SOURCES.md` when available;
the rules above also apply outside the monorepo.

Keep constant-holder classes independent of inheritance. DTO inheritance itself
is not a reason to waive or fail endpoint proof: pass the exact declaring type
and the selected dependency sources (directory or sources.jar) to the auditor.
It traverses known superclasses/interfaces and proves imported references when
no inherited member can shadow them; annotation/method uses are not declarations.
Do not whitelist marker interfaces or host names. Missing/ambiguous/cyclic source
graphs, possible inherited-member collisions and unsupported syntax stay unproved;
never fall through to imports or outer scopes on a failed binding. A file-only
caller cannot infer the owner of an annotation in a multi-type source file.
Record the source-universe fingerprint and retain compiler regressions for both
valid inheritance and shadowing. Static proof does not replace the host Java gate.
When changing lookup examples, compile the exact documentation snippets against
the selected starter artifact and verify descriptor semantics, not only skill
syntax or manifest hashes. In the canonical skills repository, run
`python scripts/check-java-lookup-example.py --java-home <JDK> --classpath <starter.jar>`
for the host baseline; record the artifact version/hash and the integration limits.


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
     - `BaseResourceRepository<E, ID>` (compatibility supertype: `BaseCrudRepository<E, ID>`)
     - `ResourceMapper<E, ResponseDTO, ?, ?, ID>`
     - `AbstractReadOnlyResourceService<E, ResponseDTO, ID, FilterDTO>` (`ID` is 3rd)
     - `AbstractReadOnlyResourceController<ResponseDTO, ID, FilterDTO>` (no `E`, `ID` is 2nd)
   - standard mutable resource:
     - `BaseResourceRepository<E, ID>` (compatibility supertype: `BaseCrudRepository<E, ID>`)
     - `ResourceMapper<E, ResponseDTO, CreateDTO, UpdateDTO, ID>` (`E` is 1st, `ID` is 5th; `applyUpdate(E entity, UpdateDTO dto)` takes `entity` 1st)
     - `AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (`E` is 1st, `ID` is 3rd; call `super(repository, Entity.class)` and override `getResourceMapper()`, `getDatasetVersion()`, `getStatsFieldRegistry()`, and `StatsSupportMode.AUTO` methods)
     - `AbstractResourceController<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (no `E`, `ID` is 2nd; annotate with `@ApiResource(value=..., resourceKey=..., title=..., description=..., icon=..., identity=@ResourceIdentity(...), quickFilters={...})` and `@ApiGroup(...)`; override `getService()` and `getResponseId(dto)`)
   - create/update-only, unit-delete, or collection-command-only (`AbstractCollectionCommandResourceController`): use the canonical specialized base only when the resource genuinely lacks the omitted operation.
   - **Composite Primary Keys (`@EmbeddedId` / `CompositeResourceId`):** When a resource has an **immutable** composite business key (e.g., `EmployeeAssignmentId(Long employeeId, Integer assignmentNumber)` or `OrderItemId(Long orderId, Integer lineNumber)`), model it as an `@Embeddable` record implementing `CompositeResourceId` and pass it directly as `ID` in `BaseResourceRepository<E, EmployeeAssignmentId>`, `ResourceMapper<..., EmployeeAssignmentId>`, `AbstractBaseResourceService<..., EmployeeAssignmentId, ...>`, and `AbstractResourceController<..., EmployeeAssignmentId, ...>`. The starter automatically serializes/deserializes `EmployeeAssignmentId` as a canonical wire string (`"1001:1"`) across path variables, query parameters (`ids`, `includeIds`), `OptionDTO<EmployeeAssignmentId>`, `RESOURCE_ENTITY` option sources (`valuePropertyPath = "id"`), `@Filterable(relation = "id.employeeId")` / `@Filterable(relation = "assignment.id")`, composite `Sort` expansion (`sort=id,desc`), tabular exports, and `/schemas/filtered` (`type: "string"`, `format: "composite-id"`, `x-ui.compositeIdComponents`, `x-ui.compositeIdSeparator`). Ordinary `@Embeddable` classes used with `@Embedded` (value objects) do not implement `CompositeResourceId` and remain structured JSON objects while still navigating via `.get(part)` in JPA Criteria without erroneous joins. For optimal UX in `@praxisui/*` tables and forms: expose both `EmployeeAssignmentId id` and the individual business columns (`employeeId`, `assignmentNumber`) in `ResponseDTO`; expose separate editable business fields in `CreateDTO` (`employeeId`, `assignmentNumber`) and construct `new EmployeeAssignmentId(...)` in `ResourceMapper.newEntity`; and omit or mark PK fields `readOnly = true` in `UpdateDTO` (`applyUpdate` never mutates `entity.setId(...)`). Conversely, when a table's natural key includes **mutable** attributes that users edit in `PUT /{id}` (e.g., `TimesheetEntry` where `entryDate` and `activityCode` are editable), use an immutable surrogate PK (`Long id`) + `UNIQUE` constraint on the natural columns because JPA forbids mutating `@EmbeddedId` components on a managed entity.
   Do not start new work on legacy CRUD/service hierarchies. For a complete copy-paste compiling slice, see `praxis-java-host-project/references/resource-baseline.md`.
3. Define operation-specific response, create, update, filter, and explicit
   command DTOs. `@Schema` describes verified business meaning; `@UISchema`
   describes presentation/control behavior; governance and AI-use metadata are
   deliberate. A filter models predicates, not a reduced create DTO.
   - **100% Entity Column Accounting, 20-Pillar Completeness & 3-Phase Execution Gate:** Consult `META-INF/praxis/AI-RESOURCE-BLUEPRINT.md` (or `praxis-metadata-starter/docs/guides/GUIA-00-BLUEPRINT-COMPLETO-RECURSO-PRAXIS.md`). Never truncate a 20- to 55-column enterprise entity into an 8-field skeletal DTO or a 3-field `FilterDTO`, and never attempt all layers of a multi-resource module in a single shallow pass. Execute in **3 vertical phases with 100% depth**:
     - **Phase 1 (Data, DTOs, `@UISchema`, `@FormLayout`, `@MicroVisualization`, Quick View 360°, Rich Lookups & `FilterDTO`):** 100% entity business columns in `ResponseDTO` (with 5–10 visible columns in the main table and secondary fields under `@UISchema(group = ..., tableHidden = true)`), short `@UISchema.label` (<= 36 chars, no trailing period), optional `@FormLayout` on multi-group `CreateDTO`/`UpdateDTO`/`ResponseDTO` (`FormLayoutMode.STEPPER`, `TABS`, `ACCORDION`, `FLAT`, or `AUTO` heuristics with `@FormLayoutSection`, `@FormLayoutStep`, `stepperReviewStep`, `draftPersistence`, and `stepperInReadMode`), typed closed options via `@UISchema(optionItems = {@UiOption(...)})` (`org.praxisplatform.uischema.annotation.UiOption`) or `optionEnum = ...` (never deprecated stringified `options`), `@MicroVisualization` + `@Threshold`, `@DomainGovernance` (`preset = DomainGovernancePreset.*`, `exportable`, `reason`, `@AiUsagePolicy`) + `@DomainLineage` (on projected attributes, keeping `@DomainGovernance` on the DTO) + `fieldAccess`, rich `@ResourceIdentity` (`subtitleField`, `metadataFields`), 4–8 `quickViewVisible` fields, `@ResourceReference` with `previewSurfaceId` on the resource title and all FK display fields, rich `EntityLookupDescriptor` (`LookupSelectionPolicy`, `LookupDetailDescriptor`, `LookupDisplayDescriptor`, `LookupFilteringDescriptor`, `dependsOn`/`dependencyFilterMap`), and an exhaustive `FilterDTO` + typed `@QuickFilter`s (`criteria = {@FilterCriterion(...)}` or `AbstractResourceQueryController#defineQuickFilters()` via `QuickFilterDescriptor`, minimum 2 per `@ApiResource`, never deprecated raw `filter = "..."`) + `ResourceFilterAccessScope` (including at least one **broad/omnibox search field** with `@Filterable(operation = FilterOperation.LIKE, relations = {"fullName", "socialName", "motherName", "dependents.fullName", "taxId"})`, multi-operator combinations on the same attribute such as `LIKE`+`STARTS_WITH`+`EQUAL`+`IN` and `BETWEEN`+`IN_LAST_DAYS`+`IN_NEXT_DAYS`, completeness filters `IS_NULL`/`IS_NOT_NULL`, collection cardinality `SIZE_GT`/`SIZE_EQ`, and multi-level cross-entity paths `relation = "a.b.c"`).
     - **Phase 2 (Surfaces, New Cross-Entity Endpoints, Intents, Workflow Actions, Governed Bulking Beyond the Obvious, Facts, Analytics & Export):** `@UiSurface` (`READ_PROJECTION` for Quick View 360° and child collections `relatedChildResourceKey`, `PARTIAL_FORM` paired with `@ResourceIntent`, and `VIEW`, declaring `legalPurpose = LegalTreatmentPurpose.*` + `legalBasisRef` when applicable), new dedicated read-only projection endpoints (`AbstractReadOnlyResourceController`) when entity relationships reveal non-obvious analytical/operational views (e.g., vacancy/occupancy matrices, expiring-items radar, compliance audits), full lifecycle `@WorkflowAction`s with `If-Match`/`Idempotency-Key` and `legalPurpose`/`legalBasisRef`, **Governed Bulking across all 3 modes beyond obvious columns** (audit 100% of mutable fields: enable `BulkMode.UNIFORM_UPDATE` on all collective standardization fields such as unit, cost center, shift, regime/plan, payment/bank, manager, and flags; enable `BulkMode.PER_ITEM_UPDATE` broadly on inline batch-grid revision fields such as phones, emails, addresses, bank accounts, individual amounts/limits, external codes, and per-item dates; keep `@BulkResourceOperations(protectedUpdateFields = ...)` strictly disjoint from `@BulkEditable` fields; and discover collective `BulkMode.DOMAIN_COMMAND` `@WorkflowAction(scope = ActionScope.COLLECTION)` transitions from the entity lifecycle and relationships such as batch relocation, batch approval/homologation, batch suspension/reactivation, or parametric revision), `@ResourceFact`s (inheriting `resourceKey` from `@ApiResource` when omitted on the controller or `<R>` `ResponseDTO`, short `label` <= 36 chars without trailing period, lowercase `snake_case` `icon`, valid `tone`, and canonical wire strings validated against `ResourceFactDataType` / `SourceKind` / `Authority` / `EvaluationPhase` / `MissingValuePolicy` / `Scope`), `StatsFieldRegistry` + `@UiAnalytics`/`@AnalyticsProjection`, and `CollectionExport` (`CSV`, `JSON`, `EXCEL` with `CollectionExportFieldPresentation`).
     - **Phase 3 (Transactional Invariants, Reactive Determinations, Rules Engine & Automated Gates):** transactional domain invariants (`409`/`422` with `fieldErrors`), `ReactiveDeterminationDefinitionProvider` / `@ReactiveDetermination` (`POST /{resource}/reactive-determinations/evaluate`, using `@DeterminationOutput("fieldName")` shorthand whenever response key equals target form field), deterministic `praxis-rules-engine` `RuleSet`s (`decisionKind = BUSINESS`, keeping authorization/data-scope/masking policies in `decisionKind = AUTHORIZATION` via `praxis-authz-*` / `OPA`), N+1 cold query-count assertions, native JUnit completeness gate (`SemanticMetadataReviewer` + `PraxisExpressionStaticValidator` + `OptionSourcePublicationInventory`), and `python scripts/workspace/audit-java-resource-completeness.py <host> --strict`.
   - **Phase acceptance:** define the phase/resources before execution and run the applicable completeness auditor with its full output and exit code retained (there is no phase selector). Follow `praxis-java-contract-conformance`: current-phase failures, regressions and required dependencies/security controls block the phase. Record future-only obligations with their responsible phase and next step; do not expand the task automatically or call an overall `FAIL` a `PASS`. Final resource/host acceptance still requires the full scorecard, native gates and required runtime/consumer proofs.
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
   - For effective-dated resources (`dtini`/`dtfim` or `startDate`/`endDate`), use **`org.praxisplatform.uischema.service.base.EffectiveDatedResourceSupport`** (`EffectiveDatedInterval`, `MutableEffectiveDatedInterval`, `ValidityInterval`, `prepareAndValidateInsert`, `closePreviousOpenValidity`, `validateNoOverlap`, `validateRange`, `isEffectiveOn`, `vigenteEm`, `asOfDate`, `resolveTemporalState`, `isContiguous`, `findGaps` — never reference the non-existent `org.praxisplatform.uischema.temporal` package) rather than duplicating interval-overlap or auto-closing helpers across services or rule executors.
   - For contextual action/surface/operation availability on item endpoints (`PLAT-EVO-01`), override `toResourceStateSnapshot(E entity)` in the service and populate declarative keys in `ResourceStateSnapshot.metadata()` (`action.<id>.allowed`, `action.<id>.reason`, `action.<id>.legalBasis`, `action.<id>.legalPurpose`, `action.<id>.customTitle`, `action.<id>.blockedByRule`, `surface.<id>.*`, `operation.<id>.*`, `resource.legalBasis`, `resource.legalPurpose`). `DefaultResourceAvailabilityService` evaluates these keys automatically with deterministic legal-metadata precedence (`action.<id>.legalBasis` -> `@WorkflowAction.legalBasisRef` -> `resource.legalBasis`) and fails closed (`SNAPSHOT_UNAVAILABLE`) when `allowedStates` is declared without a resolved state. Do **not** create per-resource `*ContextualAvailabilityConfig` boilerplate classes unless external cross-service evaluation truly requires `ContextualResourceActionService`.
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
8. For tenant-specific JSONB extensibility (`custom_fields` + `custom_field_definitions`), map the entity column with `@JdbcTypeCode(SqlTypes.JSON)`, annotate `Map<String, Object> customFields` with `@CustomFields(resourceKey = "<canonical.resource-key>")` on `ResponseDTO`, `CreateDTO`, `UpdateDTO`, and `FilterDTO`, and register a `CustomFieldDefinitionProvider` bean so `/schemas/filtered`, server-side validation, `/filter` JSONB predicates, `/export`, and `/schemas/domain` materialize tenant custom fields canonically. For derived business facts/indicators in `/schemas/domain`, annotate the resource with `@ResourceFact` (omitting `resourceKey` when declared on `@ApiResource` controller or its `<R>` `ResponseDTO` so it inherits automatically, keeping `label <= 36` chars without trailing period, lowercase `snake_case` `icon`, valid semantic `tone`, and canonical string wire values validated against `ResourceFactDataType`, `ResourceFactSourceKind`, `ResourceFactAuthority`, `ResourceFactEvaluationPhase`, `ResourceFactMissingValuePolicy`, and `ResourceFactScope`) or provide a `ResourceFactCatalogProvider` bean.
9. Audit `CreateDTO`, `UpdateDTO`, and entity relationships for **Reactive Determinations (`@ReactiveDetermination` / `ReactiveDeterminationDefinitionProvider` — Beyond the Obvious)** across four families: (a) cross-entity lookup/directory projections (`"/postalCode"` -> address fields, `"/positionId"` -> salary floor/schedule/vacancies); (b) multi-field deterministic formulas (`"/grossSalary"` + `"/baseDeductions"` -> `"/netSalary"`, `"/startDate"` + `"/probationDays"` -> `"/expectedEndDate"`); (c) chained determinations (`A -> B -> C` where an output of Determination 1 triggers Determination 2); and (d) draft policy/eligibility/capacity previews. Declare all output fields on `CreateDTO`/`UpdateDTO`, annotate `create`/`update` and the non-persisting `POST` determination endpoint with explicit `@Operation(operationId = ...)`, prefer `@ReactiveDetermination` + `@DeterminationInput` + `@DeterminationOutput` directly on the controller `POST` method (`PLAT-EVO-16`, auto-discovered by `AnnotationDrivenReactiveDeterminationDefinitionProvider`, using shorthand `@DeterminationOutput("fieldName")` whenever response key and target form field share the same name and reserving `response`/`field` for distinct names), preserve **1:1 sign and domain-meaning fidelity** in `@DeterminationInput` (never binding a deduction/discount form field onto an addition/credit request property) plus explicit accrual-date versus processing-date inputs when consulting `EffectiveDatedBracketTable` (`PLAT-EVO-18`), and follow `praxis-reactive-determinations`. When `ResponseDTO` exposes explainable calculations, annotate it with `@CalculationMemory` + `@CalculationTrail` (`PLAT-EVO-20`, keeping every stage expression semantically non-redundant and validated by `PraxisExpressionStaticValidator.validateDtoClasses(dtoClasses, true)`).

Read [resource-delivery-matrix.md](references/resource-delivery-matrix.md) when
planning a resource packet, selecting a proof, or deciding whether an optional
enterprise feature belongs in this delivery.

## Assisted Copy Versus Transactional Clone

Inspect the selected starter's neutral
`AbstractDuplicateDraftResourceController<R, ID, F, C, U, D>`,
`DuplicateDraftResourceService<R, ID, F, C, U, D>` and
`DuplicateDraftResourceCommandService<ID, D>`. Use these for optional item
`POST /{resource}/{id}/duplicate-draft`: backend allowlist/clearing policy,
explicit create-compatible partial DTO, no persistence/source mutation/reservation.
Do not inherit removed public `LegacyBacked*` bases or invent `DuplicateDraftUtils`,
`DeepCloneUtils`/`copyOnDuplicate` semantics. A legitimate private adapter is allowed.
Final CREATE uses its request schema, mandatory validation and separate POST after
confirmation; do not weaken required booleans to accommodate unanswered draft null.

Require opt-in plus real POST mapping and fail-closed affirmative availability
for create COLLECTION, view ITEM and duplicate-draft ITEM. Preserve the base's
annotation for action discovery; immediate transactional `1:N` cloning is another
business `@WorkflowAction`. Follow the starter adoption/availability guides and
the conformance skill's duplicate-draft evidence reference. Report local tests,
real persistence/HTTP, Angular/browser and public dependency adoption separately.

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

## Automated Static Auditor Gates (16 Checks) and Batch Hydration Rules

Before closing any Java resource or slice, run `python scripts/workspace/audit-java-resource-completeness.py <host-root> --strict` (when present in the monorepo) and verify all **16 static checks** pass with `0 FAIL`:

1. **Check 1–3 (`Entity-to-DTO Coverage`, `Table Columns`, `@UISchema` Editorial Quality & Expression Validation):** 100% of business columns in `@Entity` accounted for in `ResponseDTO` (verifying 1:1 adjacent boolean/flag column alignment on shared `*Dados`/DTO classes so neighboring `@Schema`/`@UISchema` descriptions are never swapped); **5 to 10 visible columns** (`tableHidden = false`) in main tables (including read-only `Radar*` views); short `@UISchema.label` and `@UiOption.label` (<= 36 chars, no trailing period, distinct from `@Schema.description`); closed choices declared with `optionItems = {@UiOption(...)}` (`org.praxisplatform.uischema.annotation.UiOption`) or `optionEnum = ...` (`uischema-options-source-conflict` / `uischema-option-enum-invalid`, never deprecated `options = "..."`); explicit `controlType`, lowercase `snake_case` Material `icon` ligature (`"assured_workload"`, never PascalCase `"Assured_Workload"`), and `@MicroVisualization` + `@Threshold` / `@CalculationMemory` + `@CalculationTrail` validated with `PraxisExpressionStaticValidator.validateDtoClasses(dtoClasses, true)`.
2. **Check 4–7 (`Quick View 360°`, `@ResourceReference`, Rich `EntityLookupDescriptor`, `@Filterable` Matrix & Typed Quick Filters):** Full `@ResourceIdentity` (`keyField`, `titleField`, `subtitleField`, and 2–3 `metadataFields` disjoint from header identity fields) declared on `ResponseDTO` (optional on Controller; identical if present on both); **4 to 8** `quickViewVisible = true` fields; `@ResourceReference(previewSurfaceId = ..., detailPresentation = "drawer" | "modal")` on the resource title and all FK display fields; full `EntityLookupDescriptor` sub-contracts on every `RESOURCE_ENTITY` option source; exhaustive `FilterDTO` (`Omnibox` multi-relation `LIKE`, `@Filterable(inline = true)` on primary toolbar/scope filters, multi-operator combinations, `IS_NULL`/`IS_NOT_NULL`, `IN_LAST_DAYS`/`IN_NEXT_DAYS`, human-vocabulary `relation = "a.b"`); and at least 2 typed quick filters (`@QuickFilter(..., criteria = {@FilterCriterion(...)})` or `AbstractResourceQueryController#defineQuickFilters()` returning `List<QuickFilterDescriptor<FD>>`, never deprecated raw `filter = "..."`) aligned with `@Filterable` properties on `FilterDTO`.
3. **Check 8–12 (`@UiSurface`, `@WorkflowAction`, Governed Bulking, `@ResourceFact`, `@DeterminationOutput` & `CollectionExport`):** `@UiSurface` for 360° projections and `1:N` child collections (`relatedChildResourceKey`); full lifecycle `@WorkflowAction`s with `If-Match` + `Idempotency-Key`; `@BulkEditable` across `UNIFORM_UPDATE` and `PER_ITEM_UPDATE` + `DOMAIN_COMMAND` collection actions with `@BulkResourceOperations(protectedUpdateFields = ...)` strictly disjoint from `@BulkEditable` (`bulk-protected-field-conflicts-with-bulk-editable`); `@ResourceFact`s (inheriting `resourceKey` from `@ApiResource` when omitted on controller or `<R>` `ResponseDTO`, `label <= 36` chars without period, lowercase `snake_case` `icon`, valid semantic `tone`, and canonical wire values matching `ResourceFact*` enums); shorthand `@DeterminationOutput("fieldName")` whenever response key matches form field (`reactive-determination-output-redundant-explicit-pair` otherwise); and `CollectionExport` (`CSV`/`JSON`/`EXCEL`).
4. **Check 13 (`StatsFieldRegistry` PropertyPath & Key Integrity):** Every `propertyPath` registered in `StatsFieldRegistry` (`stringGroupField`, `dateField`, `numericField`) must resolve to a real field on the `@Entity` (never a transient `ResponseDTO`-only getter), and bucket/metric keys must never be duplicated in the same registry.
5. **Check 14 (Hydration Before Validation — No Blocking `@NotNull` on Hydrated Fields):** Every attribute populated by server-side hydration (`hydrate*` in the Service before `RuleEngine`) must **not** carry `@NotNull` or `@NotBlank` on `CreateDTO`/`UpdateDTO`, preventing Bean Validation (`400`) from pre-empting server hydration and governed domain rules (`422`).
6. **Check 15 (`1:1 KEEP_SEPARATE` Rule Lineage, Ontological Roots & Zero Split-Brain):** 1:1 parity across `*RuleErrorCatalog.java` <-> `DecisionBinding` in `*RuleSet.java` <-> `@Test` in `*Test.java`; zero hardcoded `List.of("facts")` (always use `PraxisFactTreeBuilder.extractReferencedRoots` / `extractReferencedFactPaths` over the 5 canonical roots `draft`, `current`, `<concept>`, `neighborhood`, `context`); and zero business rule codes or `422` validations inside `*Invariants.java`.
7. **Check 16 (Lifecycle Delete Guard, Tenant FK Guards & Batch Read Hydration without Loop N+1):** Every mutable service with domain rules must implement `beforeDelete` or `deleteById` with tenant scope check (`checkOrg`) and dependency/state guards. Every foreign key on `create`, `update`, `@WorkflowAction`, and non-persisting `ReactiveDetermination` preview endpoints must verify both existence (`404 NOT_FOUND`) and tenant/shared-catalog membership (`403 FORBIDDEN`) **before** `RuleEngine` evaluation or preview projection (preventing cross-tenant oracle leaks and false `200`/`422` outcomes). Any Hibernate `@Formula` subquery on an `@Entity` must correlate the tenant column so read projections never leak cross-tenant rows. In `enrichResponses(List<R>)` / `*ReadFacts`, if a host base service overrides `enrichResponses` without calling `super.enrichResponses(responses)`, explicitly invoke `hydrateScopedResourceReferences(responses)` so standard `@ResourceReference` display fields hydrate automatically, and batch-load any composite/non-standard displays using `WHERE id IN :ids` + tenant filter (1 query per target entity; **never** call `em.find(...)` or repository lookups inside a `for (R row : responses)` loop).

### Native Platform Anti-Boilerplate Primitives (`PLAT-EVO-01..20`)

Never re-implement generic infrastructure in the host when the platform provides canonical primitives:

1. **`DefaultResourceAvailabilityService` Declarative Snapshot Keys, `EffectiveDatedResourceSupport`, `@ReactiveDetermination` & `@CalculationMemory` (`praxis-metadata-starter`, `PLAT-EVO-01..02`, `16`, `20`):** Populate `action.<id>.*`, `surface.<id>.*`, `operation.<id>.*`, `resource.legalBasis`, and `resource.legalPurpose` in `toResourceStateSnapshot(E entity)` instead of creating `*ContextualAvailabilityConfig` classes; delegate temporal validity validation/auto-closing to `org.praxisplatform.uischema.service.base.EffectiveDatedResourceSupport`; annotate controller `POST` preview handlers directly with `@ReactiveDetermination` (`@DeterminationInput`, `@DeterminationOutput`, `@DeterminationScope` -> `AnnotationDrivenReactiveDeterminationDefinitionProvider`) instead of writing `*DeterminationConfig` classes; and annotate explainable `ResponseDTO`s with `@CalculationMemory` + `@CalculationTrail` (`CalculationMemoryMetadataResolver` -> `x-ui.calculationMemory`, statically checked by `PraxisExpressionStaticValidator`).
2. **`OntologyRuleSetBuilder`, `RuleErrorCatalog.merge`, `RuleFactCatalogLoader`, `EffectiveDatedIntervalCalculator`, `ProgressiveBracketAndCapCalculator` & `EffectiveDatedBracketTable` (`praxis-rules-engine`, `PLAT-EVO-04`, `06`, `08`, `12`, `18`):** Build ontological `RuleSetDefinition`s via `org.praxisplatform.rules.ontology.OntologyRuleSetBuilder`, load fact catalogs from `RuleFactCatalogLoader` + `DtoMetadataFactCatalogEnricher` (supporting POJOs, `*Dados` superclasses, Java `record`s, and `inspectWriteDto`), and delegate parametric interstice/suspension/reset math (`EffectiveDatedIntervalCalculator`), progressive tax/contribution/constitutional-cap abatement math (`ProgressiveBracketAndCapCalculator`), and multi-epoch effective-dated schedules/matrices (`EffectiveDatedBracketTable`, `EffectiveDatedMatrixMatcher`, `TriStateOverrideResolver`) to `praxis-rules-engine` instead of hand-coding loops in services or previews.
3. **`GovernedHostRuleBundleRuntime<O>` & `GovernedRuleFamilyDescriptor` (`praxis-config-starter`, `PLAT-EVO-04..05`):** Do not write bespoke `<Resource>Runtime` + `<Resource>Runtimes` classes or hardcoded family switches per resource. Use `org.praxisplatform.config.runtime.GovernedHostRuleBundleRuntime<O>` and `GovernedRuleFamilyDescriptor` (`ofSingleRuleSet(...)` or multi-operation descriptors) / `GovernedRuleFamilyRegistry` for snapshot caching, product-baseline admission, `CommitFence` (`beforeCommit`), and dynamic `ruleType` / `ReactiveDeterminationProvenance` resolution.
4. **Zero-Boilerplate Directory Lookups, PAP Catalogs, Authz Introspection & Selective Financial Governance (`praxis-metadata-starter` + `praxis-authz-starter`, `PLAT-EVO-07`, `09`, `10`, `13`):** Register slice-scoped `@Component` beans implementing `DomainRuleSetDescriptorContributor`, `RuleErrorCatalog`, and `OptionSourceRegistryContributor`; build rich lookups via `EntityLookupDescriptor.directoryBuilderFromDto(entityKey, ResponseDTO.class)` (2 arguments, auto-prioritizing visible `UISchemaPreset.ENTERPRISE_CODE` over surrogate `id`); expose PAP decision points via `ResourceDecisionPointCatalogService` (`deriveForController` / `deriveForResource`) and runtime authorization specs via `AuthzResourceGovernanceSpec.fromAnnotatedResource(serviceKey, tenantFieldName, entityClass, responseDtoClass, filterDtoClass, controllerClass)`; and apply `DomainGovernancePreset.PUBLIC_TRANSPARENCY_REMUNERATION` alongside `CONFIDENTIAL_FINANCIAL` for selective LAI vs. LGPD column governance.
5. **Tenant-Safe Batch Hydration, Governance SPIs, Export, Multitenancy & Service Helpers (`praxis-metadata-starter:8.0.0-rc.197`):**
   - **DTO & Controller Annotations:** Use `@TableView` and `@UiFormLayout`/`@UiSection`/`@LayoutMode` on DTOs; single-source `@ResourceIdentity` on `ResponseDTO`; `@UISchema(conditionalReadOnly, colSpan)` with `NumericFormat.AUTO` default, 10-token `QuickFilterTone`, and `PraxisUiOptionEnum`; `@ContextScopeBinding` (`ScopeDimension`: `ORGANIZATION`, `COMPANY_GROUP`, `UNIT`, `PERSON`, `BOND`, `CONTRACT`); `@DraftCleared` (auto-clearing non-primitive fields to `null` during `duplicate-draft`); `@ResourceState(initialStates, putMutableStates)` (server-enforced `409 CONFLICT` on invalid create or full `PUT` transitions while allowing `PATCH`/`@WorkflowAction`); `@ResourceProgression`, `@ResourceTimeline`, and `@ResourceSchedule` on response/controller types; `@WorkflowAction(icon, tone, modifiedFields, disallowedStateReason)`; `@Filterable(primarySearch = true, inline = true)` with `FilterFieldMetadataInheritanceSupport` (auto-inheriting `icon`, `endpoint`, `valueField`, `displayField`, `options` from `ResponseDTO`) and `praxis.filter.time-zone` (`ZoneId` on `RelativePeriodPayloadNormalizer` and `GenericSpecificationsBuilder`); class-or-method `@UiAnalytics` (`TYPE`+`METHOD`); `@BulkEditable`/`@DefaultSortColumn` (`FIELD`+`METHOD`+`RECORD_COMPONENT`) discovered automatically via `AnnotationDrivenBulkDescriptorDiscovery`; and `PraxisMetadataRequestMatchers.readOnlyPostPatterns(...)` for CSRF/security exemptions on read-only POST routes.
   - **Composable Governance & Availability SPIs:** Implement ordered `ResourceGovernanceInterceptor` beans (`customizeFilterAccessScope`, `verifyEntityAccess`/`verifyEntitiesAccess(AccessMode)`, `decorateResponse`/`decorateResponses`, `filterExportFields`, `authorizeExport`, `filterStatsRegistry`, `beforeMutation(MutationContext, candidate, previous)`, `afterMutationBeforeCommit(MutationContext, persistedEntity)` using `AccessMode`, `MutationContext`, and `MutationKind`) and `ResourceOperationAvailabilityRule` beans (aggregated fail-closed by `CompositeResourceOperationAvailabilityEvaluator`) instead of reimplementing service hooks.
   - **Export, Bulk Startup & Composite Codecs:** Use `CollectionExportFieldPresentation` (including `valueLabels` auto-derived from `@UiOption`/`PraxisUiOptionEnum` and `CollectionExportRequest.applyFormatting()`) and `praxis.export.include-table-hidden-by-default`; use `BulkOperationLifecycle.ensureReadyOnStartup(...)` for startup convergence; and serialize composite snapshots with `composite:<SimpleOrClassName>` via `BulkSnapshotStorageCodec` / `BulkIdentityCodecs.composite(...)` (`CompositeIdSupport.findRegisteredCompositeIdType(...)`).
   - **Opt-In Multitenancy Primitives (`org.praxisplatform.uischema.multitenancy`):** `TenantRealmContext` (`ThreadLocal` scope), `TenantRealmRoutingDataSource` (`AbstractRoutingDataSource`), `TenantRequestValidationInterceptor` (`X-Tenant-Realm` + `ResourceTenantContextResolver`), `MultiOrganizationAccessScopeResolver` (`scalarField`, `nullableOrIn`, `elementCollection`, `parentSubquery`), `RealmScopedCsrfTokenRepository`, and `RealmScopedSecurityContextRepository`.
   - **Service Helpers:** Use `ScopedBatchReferenceHydrator` (`resolveScopedTitlesByIds` / `hydrateScopedResourceReferences`), `allExportableFields()`, `applyVersionedPatch(id, patch, precondition)`, `snapshotBeforeMutation(entity)`, `toBulkUpdate(...)`, and `resolveBulkIdentityCodec()` from `AbstractBaseResourceService`.

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
- `praxis-reactive-determinations`: step-by-step `ReactiveDeterminationDefinitionProvider`
  authoring, compiler invariants, and chained form determinations.
- `praxis-java-host-project`: host bootstrap, dependencies, and local project
  integration.

Close with the resource packet, resolved classifications, canonical owner,
operation matrix, tests run, consumer proof, and outstanding platform gap. A
resource is not complete because its controller compiles; it is complete when
its semantic contract is discoverable and its intended operation is proven.

For clean-context write guards, include create as well as update/actions. The base resource create path may query through its mapper and flush the entire persistence context; checking only beforeCreate can be too late. Reject caller-owned dirty or unbound contexts before the first mapper/repository/policy operation, including the NEVER_APPLIED policy branch. Prove that rejected creates do not flush unrelated managed lifecycle changes.
