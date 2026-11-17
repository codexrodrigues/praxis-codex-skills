---
name: praxis-authz-decision-platform
description: Use when implementing, auditing, or consuming the Praxis Authorization Decision Platform (praxis-authz-contracts, praxis-authz-enforcement-core, praxis-authz-opa, praxis-authz-starter): DecisionPointDescriptor, FactContract, QueryableResourceProjection, DataScopePlan (praxis.data-scope/v1), RuntimeEnforcementBinding, AuthorizationPolicyDefinition (praxis.authorization-policy/v1), Rego v1 compilation, 8 acyclic digest domains, 3-step SEARCH same-instance revision guard, 15-step enforcement pipeline, detached DTO masking, obligation barriers, or startup compatibility handshakes.
---

# Praxis Authorization Decision Platform

Use this skill whenever work touches **`decisionKind = AUTHORIZATION`** across `praxis-authz-contracts`, `praxis-authz-enforcement-core`, `praxis-authz-opa`, `praxis-authz-starter`, or host integrations consuming governed authorization, row-level `DataScopePlan`, attribute-level `FIELD_USE`/`FIELD_WRITE`, server-side `MASK`, and `OBLIGATION` barriers.

## 1. Canonical Architectural Boundary (`decisionKind = BUSINESS` vs `decisionKind = AUTHORIZATION`)

Never conflate deterministic business rules with authorization/data-protection policies:

- **`decisionKind = BUSINESS` (`praxis-rules-engine`):** Owns domain invariants, eligibility, calculations, and 5-state business outcomes (`RULE_TRUE`, `RULE_FALSE`, `NOT_APPLICABLE`, `INDETERMINATE`, `ERROR`) in JSON Logic (`RuleSet`). Governed in `praxis-rules-studio` under the **Business Rules Lens**.
- **`decisionKind = AUTHORIZATION` (`praxis-authz-*` + OPA/Rego v1):** Owns access control (`ACCESS`), row-level query scoping (`DATA_SCOPE`), field read/inference restrictions (`FIELD_USE` across `VALUE | FILTER | SORT | GROUP | AGGREGATE | JOIN`), field mutation authorization (`FIELD_WRITE` over `WriteIntent`), detached DTO masking (`MASK`), and conditional obligations (`OBLIGATION` across `BEFORE_EXECUTION | BEFORE_COMMIT_OUTBOX | BEFORE_DISCLOSURE`). Governed in `praxis-rules-studio` under the **Access & Data Protection Lens** using `DomainRuleDefinition` (`ruleType = "authorization_policy"`, schema `praxis.authorization-policy/v1`).

## 2. Source Audit Before Editing

Inspect the canonical owners and contracts before changing code or authoring policies:

- Published Maven Central coordinates (`0.1.0-beta.*` line, currently `0.1.0-beta.2` under `io.github.codexrodrigues`):
  - `io.github.codexrodrigues:praxis-authz-contracts:0.1.0-beta.2`
  - `io.github.codexrodrigues:praxis-authz-enforcement-core:0.1.0-beta.2`
  - `io.github.codexrodrigues:praxis-authz-opa:0.1.0-beta.2`
  - `io.github.codexrodrigues:praxis-authz-starter:0.1.0-beta.2`
- Architecture & Contract Closure Pack (`CC01–CC12`):
  - `docs/architecture/praxis-policy-starter/README.md`
  - `docs/architecture/praxis-policy-starter/decision-platform-contract-closure-pack.md`
  - `docs/architecture/praxis-policy-starter/MATRIZ-INTEGRACAO-E-GATES.md`
- Pure contracts (`praxis-authz-contracts` — no Spring, no Hibernate/JPA, no HTTP SDKs):
  - `org.praxisplatform.authz.contracts.annotation.*` (`@AuthzTenantScope`, `@AuthzScopeAnchor`, `@AuthzCustodyPartition`, `@AuthzMask`, `@AuthzMasks`, `@AuthzActionRule`, `AuthzTenantScopeMode`, `AuthzDelegationSplitMode`, `AuthzCustodyRole`, `AuthzMaskStrategy`, `EvaluationMode`)
  - `org.praxisplatform.authz.contracts.decisionpoint.*` (`DecisionPointIdentity`, `DecisionPointDescriptor`, `EnforcementCapability`, `FieldUseCategory`, `PointAuthorityMode`)
  - `org.praxisplatform.authz.contracts.context.*` (`FactDescriptor`, `FactContract`, `ContextCompositionProfile`, `ResolvedFactValue`, `FactResolutionStatus`, `ProviderInputProjection`)
  - `org.praxisplatform.authz.contracts.datascope.*` (`QueryableResourceProjection`, `SearchPredicateIr`, `DataScopePlan`, `KleeneSearchPredicateEvaluator`)
  - `org.praxisplatform.authz.contracts.binding.*` (`RuntimeEnforcementBinding`, `WriteIntent`, `ReadinessStage`)
  - `org.praxisplatform.authz.contracts.policy.*` (`AuthorizationPolicyDefinition`, `AuthorizationPolicyCandidateValidator`, `DefaultAuthorizationPolicyCandidateValidator`, `DualScopeDelegationSpec`)
  - `org.praxisplatform.authz.contracts.masking.*` (`MaskStrategyRegistry`, `DefaultMaskStrategyRegistry`)
  - `org.praxisplatform.authz.contracts.obligation.*` (`ObligationHandlerRegistry`, `DefaultObligationHandlerRegistry`)
  - `org.praxisplatform.authz.contracts.digest.*` (`DigestDomainKind`, `CanonicalDigestCalculator`, `PolicyDigestChain`, `OpaRuntimeRelease`, `OpaRuntimeHead`)
  - `org.praxisplatform.authz.contracts.compatibility.*` (`HostPolicyCompatibilityManifest`, `ImpactGraphBaseline`, `DefaultHostPolicyCompatibilityVerifier`)
- Runtime enforcement core (`praxis-authz-enforcement-core` — no Spring Boot, no Hibernate ORM):
  - `org.praxisplatform.authz.enforcement.context.*` (`UntrustedRequestHeaderGuard`, `ContextCompositionCoordinator`, `TrustedFactSource`)
  - `org.praxisplatform.authz.enforcement.writeintent.*` (`DtoWriteIntentExtractor`, `FieldWriteAuthorizer`)
  - `org.praxisplatform.authz.enforcement.fielduse.FieldUseQueryGuard`
  - `org.praxisplatform.authz.enforcement.jpa.*` (`JpaDataScopeAdapter`, `QueryAdapterFieldBinding`, `CompiledDataScopeCriterion`, `RelationTraversalStrategy`)
  - `org.praxisplatform.authz.enforcement.masking.DetachedDtoMaskingProcessor`
  - `org.praxisplatform.authz.enforcement.obligation.ObligationBarrierCoordinator`
  - `org.praxisplatform.authz.enforcement.pipeline.*` (`EnforcementPipelineExecutor`, `HostDecisionNormalizationEngine`, `AuthorizationProviderPort`)
- OPA compiler, bundle assembler, and client (`praxis-authz-opa` — no Spring, no JPA):
  - `org.praxisplatform.authz.opa.compiler.RegoV1PolicyCompiler`
  - `org.praxisplatform.authz.opa.bundle.OpaBundleAssembler`
  - `org.praxisplatform.authz.opa.revision.SameInstanceSearchRevisionGuard`
  - `org.praxisplatform.authz.opa.client.*` (`OpaAuthorizationProviderAdapter`, `HttpClientOpaTransport`, `DeterministicLocalOpaTransport`)
  - `org.praxisplatform.authz.opa.governance.GovernedOpaReleaseCoordinator`
- Spring Boot starter & end-to-end pilot (`praxis-authz-starter`):
  - `org.praxisplatform.authz.autoconfigure.*` (`PraxisAuthzAutoConfiguration`, `PraxisAuthzProperties`, `PraxisAuthzHostBridgeAutoConfiguration`, `PraxisAuthzAgentBridgeAutoConfiguration`)
  - `org.praxisplatform.authz.agent.*` (`AuthzAgentAuthorizationBridge`, `AuthzAgentThreadContextPropagator`)
  - `org.praxisplatform.authz.compatibility.*` (`HostPolicyCompatibilityStartupVerifier`, `HostRuntimePolicyCoordinates`, `PraxisAuthzReadinessHealthIndicator`)
  - `org.praxisplatform.authz.catalog.*` (`SemanticDecisionPointCatalogService`, `FieldLineageCatalogEntry`, `MethodBindingAdmissionRecord`)
  - `org.praxisplatform.authz.channel.GovernedChannelInvocationExecutor`
  - `org.praxisplatform.authz.export.GovernedCollectionExportGuard`
  - `org.praxisplatform.authz.pilot.*` (`WorkforceLeaveAuthzPilotBlueprint`, `WorkforceLeavePilotRuntimeHost`, `JdbcSessionContextIsolationGuard`, `GovernedPolicyAuthoringGateway`)
  - `org.praxisplatform.authz.host.metadata.*` (`AbstractAuthzGovernedResourceService`, `AbstractAuthzGovernedReadOnlyResourceService`, `AuthzResourceGovernanceSpec`, `AuthzResourceGovernanceInterceptor`, `AuthzResourceOperationAvailabilityRule`, `MultiOrganizationHardScopeResolver`, `MetadataDtoGovernanceIntrospector`, `AuthzHostPolicyBootstrapBuilder`, `AuthzHostReadinessReviewer` [`AUTHZ-HOST-001..014`], `PraxisAuthzExceptionHandler` using `"fieldUseCategory"` in `CustomProblemDetail` instead of the reserved `"category"` extension key)

Read [contracts-and-gates-matrix.md](references/contracts-and-gates-matrix.md) for the `CC01–CC12` contract summary, the 15-step enforcement pipeline order, and the 8 acyclic digest domains.

## 3. Non-Negotiable Platform Invariants

1. **Zero Trust on Request Headers (`P01`, `P42`, `P61`):**
   - `UntrustedRequestHeaderGuard` blocks all `x-authz-*`, `x-praxis-authz-*`, `x-bypass-*`, and `x-workflow-*` headers unconditionally, and forbids authority spoofing across `x-tenant-id`, `x-org-id`, `x-organization-unit-ids`, `x-delegated-destination-org-ids`, roles, and principal headers.
   - Any other request header (`X-Org-Id`, `X-Tenant-Id`, `x-delegated-destination-org-ids`) may only narrow a `subject.*` fact that is already `FactResolutionStatus.PRESENT` in the authenticated principal's server-side envelope; it can never assert `resource.*`, `transition.*`, or `context.*` facts or expand scope.
2. **6-State Fact Resolution & Fail-Closed Missing Facts (`P04`, `P30`):**
   - Facts resolve to `PRESENT`, `NULL`, `ABSENT`, `STALE`, `UNAVAILABLE`, or `ERROR` across `EXTRACT -> ENRICH -> DERIVE`.
   - `DERIVE` sources short-circuit to `UNAVAILABLE` if any upstream dependency is not `PRESENT`/`NULL`.
   - In both Rego v1 (`input.facts["..."].status == "PRESENT"`) and `DeterministicLocalOpaTransport`, `UNAVAILABLE`/`ABSENT`/`ERROR` facts never satisfy equality or membership predicates.
3. **Persistence-Neutral `DataScopePlan` & Kleene 3VL SQL Pushdown (`CC03`, `P06`, `P24`):**
   - `DataScopePlan` (`format = "praxis.data-scope/v1"`) and `SearchPredicateIr` reference only canonical `fieldPath` and `attributeId` from `QueryableResourceProjection`. JPA/SQL paths (`nativeJpaPath`, `RelationTraversalStrategy`) live exclusively inside `QueryAdapterFieldBinding` in `JpaDataScopeAdapter`.
   - `IS_NULL(MISSING) = UNKNOWN` and `IS_NOT_NULL(MISSING) = UNKNOWN` in `KleeneSearchPredicateEvaluator`.
   - `JpaDataScopeAdapter` pushes negation into Negation Normal Form via De Morgan's laws, uses correlated `EXISTS` / `NOT EXISTS` subqueries for collection/optional paths, escapes `LIKE ... ESCAPE '\'` wildcards, applies `LOWER(col)` when `caseInsensitive == true`, and always composes dynamic scope with the host's mandatory `hardScope` via `AND`.
4. **Algebraic Combining Without Numeric Priority (`CC12`, `PCB-ORDER-001`):**
   - Numeric rule priority is banned.
   - `ACCESS` combines as `DENY > ALLOW > NOT_APPLICABLE` (any `RESTRICT` veto dominates any `GRANT`).
   - `DATA_SCOPE` combines `GRANT` predicates by **union (`OR`)** and `RESTRICT` predicates by **intersection (`AND`)**, intersected with the host `hardScope`.
5. **Complete `WriteIntent` Extraction & Dual-Scope Custody (`CC06`, `P13`, `P14`, `P45`):**
   - `DtoWriteIntentExtractor` classifies mutations into `SET`, `CLEAR_EXPLICIT_NULL`, and `REMOVE` (for omitted mapped fields when `partialPatch == false` on full-replacement `PUT`). Any business JSON wire path not mapped in `attributeIdByWirePath` (and not explicitly listed in `ignoredTechnicalWirePaths`) fails closed with `AUTHZ_UNMAPPED_WRITE_WIRE_PATH`.
   - `FieldWriteAuthorizer` enforces neutral `DualScopeDelegationSpec` modes (`ORIGIN_DESTINATION_SPLIT`, `ORIGIN_ONLY_WRITE`, `READ_ONLY_DESTINATION`, constructed via `DualScopeDelegationSpec.ofOriginAndDestination(...)`) and rejects callers matching neither custody scope. Organizational scope transfers (`OLD` -> `NEW`) require custody over both `OLD` and `NEW` scopes (`P14`).
6. **Detached DTO Masking & Commutative Lattice (`CC09`, `P12`, `P25`, `P36`):**
   - Never mutate managed JPA entities for masking. `DetachedDtoMaskingProcessor` operates exclusively on detached DTO maps/projections (including nested paths and collections) using `MaskStrategyRegistry` (`OMIT > NULLIFY > REDACT_CONSTANT > HASH_TOKEN_KEYED > SUMMARY_ONLY > CPF_CNPJ_PARTIAL / PARTIAL_MASK`). `FIELD_USE(VALUE) = DENY` dominates any mask.
7. **3-Step `SEARCH` Same-Instance Revision Guard (`CC11`, `P17`, `P18`):**
   - `OpaAuthorizationProviderAdapter.evaluateSearch` executes `search_preflight -> compile_data_scope -> runtime_head` pinned to the same OPA `instanceId` via `SameInstanceSearchRevisionGuard`. Instance hops fail closed immediately; same-instance bundle rotations allow at most the configured bounded retry (default `1`).
8. **Governed Release Coordinator & Anti-`denyAll` Corpus Gate (`P28`, `P32`, `P53`, `P55`, `P63`):**
   - `GovernedOpaReleaseCoordinator` requires `POLICY_ADMIN_PUBLISH`, verifies pinned `definitionFingerprint` (`Stage 1` of the 8-domain digest chain covering the full semantic policy AST), rejects competing `policyUnitKey`/`policyId` (`P38`), and executes mandatory positive (`ALLOW`/`FILTER`) and negative (`DENY`/`NOT_APPLICABLE`/`NONE`) corpus cases before emitting a `PolicyCandidateActivationReceipt`.
9. **Channel Admission, Cache-Hit Re-Authorization & Governed Collection Export (`P11`, `P12`, `P18`, `P21`, `P25`, `P26`, `P29`, `P34`, `P41`, `P42`, `P56`, `P60`):**
   - `GovernedChannelInvocationExecutor` blocks unproxied self-invocation (`P41`), verifies admitted invocation channels (`P34`), restores outer `EvaluationContextSnapshot`s after nested calls (`P29`), never skips inner decision point evaluation (`P42`), frames scoped cache/ETag keys with length prefixes (`P21`), and re-executes authorization + detached masking on every cache hit (`P26`).
   - `GovernedCollectionExportGuard` verifies live `OpaRuntimeHead` freshness before and after row processing (`P18`), enforces static and inherited `exportable = false` lineage across all representations (`P56`, `P60`), applies per-row detached masking (`P12`, `P25`), and neutralizes CSV/TSV delimiter/formula injection.
10. **JDBC Session Context Isolation & Governed Policy Authoring Gateway (`P27`, `P33`, `P51..P55`, `P61`, `P63`):**
   - `JdbcSessionContextIsolationGuard` binds transaction-scoped RLS variables (`app.current_tenant_id`, `app.current_principal_id`, `app.current_org_id`) before the first SQL statement, scrubs pooled connections in `finally`, and rejects `BYPASSRLS`/superuser database roles fail-closed.
   - `GovernedPolicyAuthoringGateway` isolates untrusted prompt/document text from execution (`P54`), validates target decision points against the caller's delegated `serviceKey` hard scope, verifies `FactContract` membership, provider fact support, and `ADMISSION`/`TARGET` phase compatibility (`P52`, `P61`), and delegates release activation to `GovernedOpaReleaseCoordinator`.
11. **Zero-Blueprint Resource Introspection (`PLAT-EVO-10`), Pure `@Authz*` Annotations (`0.1.0-beta.2` / Wave 1.4B) & Metadata PAP Discovery (`PLAT-EVO-07`):**
   - Instead of writing ~350-line manual `*AuthzBlueprint` classes per resource, decorate entities/DTOs/controllers with pure annotations from `org.praxisplatform.authz.contracts.annotation.*` (`@AuthzTenantScope` with `AuthzTenantScopeMode.TENANT_ONLY | ORGANIZATIONAL_UNIT | AUTHENTICATED_SHARED`, `@AuthzScopeAnchor`, `@AuthzCustodyPartition`, `@AuthzMask`, `@AuthzActionRule`) and build `AuthzResourceGovernanceSpec` via **`AuthzResourceGovernanceSpec.fromAnnotatedResource(...)`** (6-arg, 7-arg, or `createDtoClass`/`updateDtoClass`/`serviceClass` overloads) or **`AuthzResourceGovernanceSpec.<E>builder(resourceKey)...introspectFromResource(...)`**.
   - **Auto-Synthesized Policy Bootstrap (`AuthzHostPolicyBootstrapBuilder`):** Call `addAnnotatedResource(spec[, responseDtoClass, createDtoClass, updateDtoClass])` or `addAnnotatedResources(specs)` to automatically synthesize primary tenant/organization scope rules, `@AuthzActionRule` gates, and `@AuthzMask` + `@DomainGovernance`-derived redactions (`MetadataDtoGovernanceIntrospector` automatically derives `REDACT_CONSTANT("***")` for `String`, `NULLIFY` for nullable non-`String`, and `VALUE+DENY` for non-nullable/primitive non-`String` and `SECRET`/`CREDENTIAL` fields).
   - **Zero-Inheritance Enforcement & Operational Agent Bridge:** Register `AuthzResourceGovernanceInterceptor` (`ResourceGovernanceInterceptor`, `DEFAULT_ORDER = HIGHEST_PRECEDENCE + 200`), `AuthzResourceOperationAvailabilityRule` (`ResourceOperationAvailabilityRule`, `DEFAULT_ORDER = HIGHEST_PRECEDENCE + 300`, composing cleanly inside `CompositeResourceOperationAvailabilityEvaluator`), `MultiOrganizationHardScopeResolver` (`HARD_TENANT_IDS_PARAM`), and `PraxisAuthzAgentBridgeAutoConfiguration` (`AuthzAgentAuthorizationBridge` + `AuthzAgentThreadContextPropagator` wiring `praxis-config-starter`'s `OperationalAgentAutoConfiguration` fail-closed through OPA/caller context).
   - `fromAnnotatedResource` / `introspectFromResource` automatically introspects `@ApiResource` + MVC mappings (including root `@GetMapping` empty-subpath list endpoints alongside `/{id}`, `/filter`, `@WorkflowAction`, `@UiSurface`, and `/export`), maps `@DomainGovernance`/`@DomainLineage` and `@Authz*` annotations, treats `@ManyToOne(optional = false)`, `@OneToOne(optional = false)`, and `@JoinColumn(nullable = false)` as `FactPresenceModel.ALWAYS_PRESENT`, coerces tenant `hardScope` values to the JPA attribute type (`String`, `Integer`, `Long`, `Short`, `UUID`), and enforces readiness checks `AUTHZ-HOST-001..014` in `AuthzHostReadinessReviewer` (including **`AUTHZ-HOST-010`**: verifying `HostRuntimePolicyCoordinates` binding coverage across CRUD/action/surface methods, `QueryableProjectionRef` on bulk `SEARCH` actions, and `operationModifiedAttributes` on custom `FIELD_WRITE` actions).
   - Pair runtime enforcement in `praxis-authz-starter` with `ResourceDecisionPointCatalogService` (`deriveForController` / `deriveForResource` in `praxis-metadata-starter`, `PLAT-EVO-07`) when publishing PAP catalog inventories to `praxis-rules-studio`.

## 4. Validation & Release Order

Run focused Maven gates with JDK 21 on the affected modules:

- Contracts (`P1`): `mvn -f praxis-authz-contracts/pom.xml test`
- Enforcement Core (`P2`): `mvn -f praxis-authz-enforcement-core/pom.xml test`
- OPA Compiler, Bundle & Client (`P3`): `mvn -f praxis-authz-opa/pom.xml test`
- Spring Boot Starter, `P01..P64` Conformance Matrix & HTTP/Reentrant Suites (`P4` + `P5`): `mvn -f praxis-authz-starter/pom.xml test` (`P01ToP64CompleteConformanceMatrixTest`, `P11HttpAndReentrantServiceIntegrationTest`)

When publishing a coordinated Maven Central release across the four repositories (see each repository's `RELEASING.md`), always release in strict dependency order and wait for Maven Central `HTTP 200` on each stage before tagging the next:
`praxis-authz-contracts` -> `praxis-authz-enforcement-core` -> `praxis-authz-opa` -> `praxis-authz-starter`.

## 5. Companion Skills

- `praxis-java-domain-governance-field-access` for `@DomainGovernance`, `@DomainLineage`, `@AiUsagePolicy`, `LegalTreatmentPurpose`, and `/schemas/domain`.
- `praxis-config-domain-decisions` for `/api/praxis/config/domain-rules/**` lifecycle, maker-checker approvals, and snapshot control plane.
- `praxis-rules-engine-runtime` when working on `decisionKind = BUSINESS` JSON Logic `RuleSet`s rather than authorization policies.
