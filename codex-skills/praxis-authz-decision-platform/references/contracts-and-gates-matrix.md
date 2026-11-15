# Praxis Authorization Decision Platform — Contracts, Pipeline, and Digest Matrix

## 1. Contract Closure Pack (`CC01–CC12`)

| ID | Contract / Schema | Canonical Owner | Key Classes |
| :-: | :--- | :--- | :--- |
| **`CC01`** | `praxis.authorization-policy/v1` (`ruleType = "authorization_policy"`) | `praxis-authz-contracts` | `AuthorizationPolicyDefinition`, `AuthorizationPolicyRule`, `AuthorizationRuleContributions`, `TargetResolutionManifest`, `FieldResolutionManifest` |
| **`CC02`** | `praxis.authorization-condition/v1` (`authorization-target/v1` & `authorization-search-source/v1`) | `praxis-authz-contracts` | `AuthorizationSourceCondition`, `ConditionProfileKind`, `DefaultAuthorizationPolicyCandidateValidator` (`MAX_AST_DEPTH=12`, `MAX_AST_NODES=128`, `MAX_IN_LITERALS=64`, `MAX_REFERENCED_FACTS=32`) |
| **`CC03`** | `praxis.data-scope/v1` & Kleene 3VL Truth Table | `praxis-authz-contracts` + `praxis-authz-enforcement-core` | `QueryableResourceProjection`, `DataScopePlan`, `SearchPredicateIr`, `KleeneSearchPredicateEvaluator`, `JpaDataScopeAdapter`, `QueryAdapterFieldBinding` |
| **`CC04`** | 5-Artifact Context Architecture & 6-State Fact Resolution | `praxis-authz-contracts` + `praxis-authz-enforcement-core` | `FactDescriptor`, `FactContract`, `ContextCompositionProfile`, `ContextEnvelope`, `ProviderInputProjection`, `ContextCompositionCoordinator`, `UntrustedRequestHeaderGuard` |
| **`CC05`** | Canonical `DecisionPointIdentity` Grammar & `DecisionPointDescriptor` | `praxis-authz-contracts` | `DecisionPointIdentity`, `DecisionPointDescriptor`, `DecisionPointRef` |
| **`CC06`** | `RuntimeEnforcementBinding`, `FieldUseCategory` & `WriteIntent` | `praxis-authz-contracts` + `praxis-authz-enforcement-core` | `RuntimeEnforcementBinding`, `FieldUseCategory`, `WriteIntent`, `DtoWriteIntentExtractor`, `FieldWriteAuthorizer`, `FieldUseQueryGuard` |
| **`CC07`** | 15-Step Enforcement Pipeline, `ProviderEvaluationEnvelope` & `DecisionEvidence` | `praxis-authz-contracts` + `praxis-authz-enforcement-core` | `ProviderEvaluationEnvelope`, `DecisionEvidence`, `HostDecisionNormalizationEngine`, `EnforcementPipelineExecutor` |
| **`CC08`** | `HostPolicyCompatibilityManifest` & `ImpactGraphBaseline` | `praxis-authz-contracts` + `praxis-authz-starter` | `HostPolicyCompatibilityManifest`, `ImpactGraphBaseline`, `DefaultHostPolicyCompatibilityVerifier`, `HostPolicyCompatibilityStartupVerifier` |
| **`CC09`** | `MaskStrategyRegistry` & Commutative Merge Lattice | `praxis-authz-contracts` + `praxis-authz-enforcement-core` | `MaskStrategyRegistry`, `DefaultMaskStrategyRegistry`, `DetachedDtoMaskingProcessor` |
| **`CC10`** | `Obligation` Types, Handlers & Fulfillment Barriers | `praxis-authz-contracts` + `praxis-authz-enforcement-core` | `ObligationHandlerRegistry`, `DefaultObligationHandlerRegistry`, `ObligationBarrierCoordinator` |
| **`CC11`** | OPA Provider I/O Schemas, 8 Acyclic Digest Domains & 3-Step `SEARCH` Guard | `praxis-authz-contracts` + `praxis-authz-opa` | `DigestDomainKind`, `CanonicalDigestCalculator`, `RegoV1PolicyCompiler`, `OpaBundleAssembler`, `SameInstanceSearchRevisionGuard`, `OpaAuthorizationProviderAdapter` |
| **`CC12`** | Authority Convergence (`RuleAuthority` -> `ExecutionDispositionMode` × `PointAuthorityMode`) | `praxis-authz-contracts` + `praxis-authz-enforcement-core` | `EffectiveAuthorityBinding`, `ExecutionDispositionMode`, `PointAuthorityMode` |

---

## 2. The 15-Step Enforcement Pipeline (`EnforcementPipelineExecutor`)

1. **`STEP_01_RESOLVE_BINDING_AND_READINESS`:** Verify `RuntimeEnforcementBinding.isFailClosedReady()`, alignment with `EffectiveAuthorityBinding` and `ContextCompositionProfile`, and `HardGuard` admission.
2. **`STEP_02_GUARD_UNTRUSTED_HEADERS`:** Run `UntrustedRequestHeaderGuard.validateHeaders(...)`.
3. **`STEP_03_COMPOSE_CONTEXT_ENVELOPE`:** Run `ContextCompositionCoordinator` (`EXTRACT -> ENRICH -> DERIVE`).
4. **`STEP_04_PROJECT_MINIMIZED_PROVIDER_INPUT`:** Build minimized `ProviderInputProjection` (excluding undeclared and sensitive unreferenced facts).
5. **`STEP_05_EVALUATE_STRUCTURAL_HARD_GUARDS`:** Enforce host tenant/scope structural invariants (`HardGuard`).
6. **`STEP_06_EXTRACT_WRITE_INTENT`:** Extract `WriteIntent` (`SET`, `CLEAR_EXPLICIT_NULL`, `REMOVE`) for mutations.
7. **`STEP_07_INVOKE_AUTHORIZATION_PROVIDER`:** Invoke `AuthorizationProviderPort.evaluateTarget(...)` or 3-step guarded `evaluateSearch(...)`.
8. **`STEP_08_NORMALIZE_DECISION_ENVELOPE`:** Combine outcomes via `HostDecisionNormalizationEngine` (`RESTRICT_BASELINE` vs `AUTHORITATIVE`, conflict detection).
9. **`STEP_09_FULFILL_BEFORE_EXECUTION_OBLIGATIONS`:** Execute `BEFORE_EXECUTION` obligations (`REQUIRE_MFA`, `REQUIRE_JUSTIFICATION`).
10. **`STEP_10_ENFORCE_FIELD_USE_OR_DATA_SCOPE_PUSHDOWN`:** Validate query fields via `FieldUseQueryGuard` and compile `DataScopePlan` via `JpaDataScopeAdapter`.
11. **`STEP_11_ENFORCE_FIELD_WRITE_AUTHORIZATION`:** Validate `WriteIntent` against `FIELD_WRITE` directives and `DualScopeDelegationSpec` via `FieldWriteAuthorizer`.
12. **`STEP_12_EXECUTE_PROTECTED_HOST_OPERATION`:** Execute the host repository/service operation within the authorized scope.
13. **`STEP_13_FULFILL_BEFORE_COMMIT_OUTBOX_OBLIGATIONS`:** Record transactional audit evidence (`DURABLE_AUDIT_EVIDENCE`) in `TransactionalAuditOutboxPort`.
14. **`STEP_14_APPLY_DETACHED_DTO_MASKING_AND_FIELD_PROJECTION`:** Suppress `FIELD_USE(VALUE)=DENY` fields and apply `MaskStrategyRegistry` transformations on detached DTO projections via `DetachedDtoMaskingProcessor`.
15. **`STEP_15_FULFILL_BEFORE_DISCLOSURE_AND_EMIT_EVIDENCE`:** Execute `BEFORE_DISCLOSURE` obligations (`WATERMARK`) and emit sanitized `DecisionEvidence` using the deterministic `temporalContext.instant()`.

---

## 3. The 8 Acyclic Digest Domains (`DigestDomainKind`)

1. **`DEFINITION_FINGERPRINT` (`Stage 1`):** Canonical SHA-256 of the complete semantic `AuthorizationPolicyDefinition` AST.
2. **`DEPENDENCY_MANIFEST_DIGEST` (`Stage 2`):** Canonical SHA-256 of sorted `TargetResolutionManifest`s and `FieldResolutionManifest`s.
3. **`COMPILE_INPUT_DIGEST` (`Stage 3`):** Hash of `(DEFINITION_FINGERPRINT, DEPENDENCY_MANIFEST_DIGEST, compilerProfileVersion)`.
4. **`GENERATED_ARTIFACT_DIGEST` (`Stage 4`):** Hash of `(COMPILE_INPUT_DIGEST, regoSource)`.
5. **`MATERIALIZATION_FINGERPRINT` (`Stage 5`):** Hash of `(policyUnitKey, DEFINITION_FINGERPRINT, GENERATED_ARTIFACT_DIGEST)`.
6. **`COMPOSITION_DIGEST` (`Stage 6`):** Hash of `(systemCombiningDigest, ordered policyUnitKeys + materializationFingerprints)`.
7. **`POLICY_SET_DIGEST` (`Stage 7`):** Hash of `(environmentKey, COMPOSITION_DIGEST)`.
8. **`BUNDLE_ARTIFACT_DIGEST` (`Stage 8`):** Hash of `(POLICY_SET_DIGEST, runtimeRevision, headEtag, activationRevision, opaCapabilitiesDigest, unitKeysByDecisionPointKey, sortedBundleFiles)`.
