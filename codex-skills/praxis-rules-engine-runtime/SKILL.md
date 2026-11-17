---
name: praxis-rules-engine-runtime
description: Implement, review, debug, or extend the deterministic Praxis rules engine, including JSON Logic parity, RuleSet contracts, composition slots, planner DAGs, versioned Java executors, five-state decisions, limits, packaging, and neutral host consumption.
---

# Praxis Rules Engine Runtime

## Owners and boundaries

Treat `@praxisui/core` RFC, models, descriptors and shared corpus as the current normative dialect owner. Treat `praxis-rules-engine` as the owner of the pure Java runtime. Change RFC, TypeScript, Java and corpus in the same cycle when semantics change.

Keep the engine stateless, thread-safe, embeddable and free of Spring, I/O, persistence, endpoints, tenant stores, mutable snapshot heads, workflow, effects, database access and domain-specific rules. The engine owns the immutable runtime-neutral snapshot contract and compiler; `praxis-config-starter` owns authoring, publication, append-only snapshot persistence, active heads and rollback; domain hosts own facts, executable Java registries, security, transactions, algorithms and effects; `praxis-metadata-starter` owns metadata projection.

Treat RuleSet identity, slots, bindings, closed aggregation policies, deterministic plans, compatibility coordinates, results, and executor registry contracts as owned by `praxis-rules-engine`. A host may adapt these contracts but must not redefine their semantics.

In the platform monorepo, the accepted Angular evidence currently points to the Java runtime as the external `praxis-rules-engine` repository. If that repository is not present locally, do not infer Java behavior from Angular code or create a host-local backend evaluator. Record the missing repository as a validation blocker for Java parity and keep Angular/core, corpus, and domain-rule materialization changes honest about their actual proof boundary.

For business-rule, eligibility, compliance, validation, or shared migration decisions (`decisionKind = BUSINESS`), treat `/api/praxis/config/domain-rules/**` as the governed authoring/publication source and treat `form_config`, `option_source`, `backend_validation`, `workflow_action`, `approval_policy`, table effects, and other runtime targets as materializations. `formRules`, `formRulesState`, component edit plans, visual guidance, table config, and host callbacks may consume or preview a projection, but they must not become the primary owner of the decision. Keep `praxis-rules-engine` strictly scoped to `decisionKind = BUSINESS` (deterministic JSON Logic / Java domain executors); security, RBAC/ABAC/ReBAC, field masking, and LGPD access enforcement belong to `decisionKind = AUTHORIZATION` (`ruleType = "authorization_policy"`, `targetLayer = "policy_engine"`, `targetArtifactType = "opa-policy"`, executed by `praxis-authz-starter` / `praxis-authz-enforcement-core` / `praxis-authz-opa`).

## Required source audit

Read applicable `AGENTS.md`, then inspect:

- `praxis-ui-angular/projects/praxis-core/docs/rfc-json-logic-semantics.md`
- TypeScript models, token, service and focused specs under `projects/praxis-core/src/lib`
- `praxis-ui-angular/docs/json-logic-conformance/conformance-fixtures.json`
- all Java production/tests and engine documentation
- `docs/operator-conformance-matrix.md` and `docs/architecture.md`
- if the task touches governed decisions or runtime materialization, inspect `DomainRuleService`, `DomainRuleMaterialization`, `DomainRuleFormRulesService`, and the relevant quickstart smoke before changing a runtime target

Classify semantic changes as `arquitetural`, `contrato-publico` and `transversal`; map direct consumers and derived artifacts before editing.

## Invariants

- Distinguish missing from `null` internally; never leak the sentinel publicly.
- Freeze `nowUtc` and require explicit `userTimeZone` for contextual operators.
- Normalize JSON numbers by value, independent of Jackson concrete classes.
- Preserve documented short-circuit and evaluate selected arguments once.
- Parse only `a.b`, `a.b[0]`, `a["key"]` and `$.a.b`.
- Use the common safe regex subset and deterministic structural/operation limits.
- Treat `operatorCatalog` in the shared corpus as normative for operator name, source and arity; both runtimes must compare every published descriptor against it.
- Apply byte, node, depth, array and string limits to expressions and public results. Test expansion where individually valid inputs combine into an oversized result.
- The common bounded regex subset permits literals, escapes, character classes, anchors, `?` and `{n}`/`{n,m}` with maximum 256. Reject groups, alternation, backreferences, `*` and `+` before compiling.
- Make registry descriptors introspectable; native names are reserved and host operators require namespaces.
- Share descriptor, arity and semantic definitions between validation and evaluation.
- Return stable code, path and operator diagnostics.
- Pin every RuleSet to the exact engine contract, JSON Logic dialect, and normative corpus SHA-256 accepted by the runtime.
- Require exact namespaced key and version for Java executors; reject missing or incompatible implementations during planning.
- Keep Java executor discovery split by boundary: publication uses a planning-only coordinate registry that proves an exact key/version is allowed without instantiating host code; the consuming host supplies the executable registry and must compile the complete candidate before activation. Never put host executors in Config Starter.
- Distinguish immutable snapshot content identity from mutable activation identity. `snapshotContentHash` is stable for canonical content; an opaque strong head ETag and monotonic activation revision must change on every activation, including rollback to previously active content, to prevent ABA.
- Represent slot cardinality and aggregation explicitly. Customer composition must respect product-owned override policy; protected guards cannot be customized.
- Compile dependencies as a bounded DAG with deterministic stage/order/key tie-breaking. Reject cycles, later-stage references, excessive edges, and excessive fan-out.
- Preserve `ALLOW`, `DENY`, `NOT_APPLICABLE`, `INCONCLUSIVE`, and `TECHNICAL_ERROR`; never convert technical failure into business denial.
- Treat target-adapter diagnostics such as invalid form conditions, unsupported properties, missing targets, iteration limits, failed materialization-to-rule conversion, unavailable materialization stores, or host executor absence as technical/projection evidence. They may suppress that projection, expose diagnostics, keep last-known-good, or require review, but they must not be reinterpreted as `DENY`, copied into `propertiesWhenFalse`, or used to invent a fallback RuleSet. A business denial must come from an evaluated governed decision with the required facts and compatible runtime coordinates.
- Continue independent branches after `INCONCLUSIVE` so a real `DENY` is not hidden, while preventing dependent execution and effect planning.
- Consolidate the final allow/not-applicable outcome from terminal DAG bindings. An intermediate guard or prerequisite `ALLOW` must never lift a terminal `NOT_APPLICABLE` branch.
- Require every effect-intent binding to declare an explicit decision dependency, and never execute it while any prior branch is inconclusive.
- Apply deterministic structural limits to host-resolved facts and Java executor outputs, not only to JSON Logic expressions.
- Include stable plan/facts digests and exact runtime/implementation coordinates in evaluation results. Keep wall-clock duration and observation infrastructure outside the deterministic core.
- Dynamic-form, table, page-builder, rich-content, and workflow targets may translate a governed decision into visible or executable effects, but this translation is a projection. Do not repair a missing governed decision by adding local `formRules`, `formRulesState`, JSON snippets, component-edit-plan operations, table-only predicates, or host callbacks.

## Changing semantics or operators

1. Inventory RFC, TypeScript registry/runtime, Java registry/runtime and corpus.
2. Record the convergence decision before implementation; do not copy a runtime bug merely for parity.
3. Update the normative RFC and operator matrix.
4. Update both runtimes and their validators from the same decision.
5. Extend the shared corpus with typed values, truthiness, structured errors and any operator catalog change.
6. Add focused tests for missing/null, invalid type, arity, path, limits and determinism.
7. For a host operator, require namespace and prove presence in every runtime that may evaluate persisted rules.

Do not create textual DSL fallbacks, parallel V1/V2 contracts, permissive JSONPath, unrestricted regex, implicit process time, or runtime database access.

Do not accept "works in the Angular preview" as proof of rule-platform parity. Preview/runtime projection proves only that a target consumed a materialization. Parity requires the normative RFC, TypeScript runtime, shared corpus, Java runtime, descriptors, and host operator availability to agree.

## Changing RuleSet contracts or planning

1. Read the accepted Rule Platform ADRs and classify the change as public-contract and architectural.
2. Map the engine, Config Starter, Quickstart, public documentation, goldens, and Maven coordinate impact before editing.
3. Keep public records immutable and defensively copy mutable JSON values.
4. Add positive and negative tests for identity, compatibility, composition, DAG ordering, missing/null, decision precedence, effect gating, limits, and thread safety.
5. During implementation, run the affected contract/planner/snapshot tests and direct-consumer checks first. Run the complete engine gate, including Javadocs, on the consolidated candidate before accepting a RuleSet contract/planning change. Downstream release proof must then consume an officially published Maven coordinate; source-candidate integration remains a separate development proof.

For snapshot work, prove the full ownership chain: the engine compiles the runtime-neutral candidate, Config Starter persists and advances the governed head transactionally, and a host compiles with its executable registry before an atomic last-known-good swap. A v1 → v2 → v1 rollback must preserve v1's content hash while issuing a new head ETag and activation revision.

Do not use `mvn install`, file repositories, or local version overrides as downstream release proof. While the public beta line is active, compatible additive work stays on the next beta unless release governance establishes a breaking change.

When migrating a legacy enterprise system or building another domain host, use the engine skill to remove cognitive load by routing questions to the canonical layer: missing facts or algorithms belong to the host/domain contract, shared decisions belong to `domain-rules`, deterministic expression semantics belong to the JSON Logic dialect/engine, and UI behavior belongs to materialized target adapters. Avoid screen-local rule transforms that make one migrated screen pass while leaving the platform unable to explain, simulate, publish, or replay the decision.

When a host projects a RuleSet as Reactive Determinations, keep the engine
runtime-neutral. Form modes, triggers, field bindings, metadata projection, and
Angular cancellation/application belong to the determination handoff described
by `praxis-reactive-determinations`; do not add form-specific execution to the
engine.

## Ontological Fact Graph (5 Canonical Roots), Wave 1 Fluent Builders (`0.1.0-beta.20`), Parametric Calculators & 1:1 Rule Lineage

When a host uses `praxis-rules-engine` (current Wave 1 baseline: `0.1.0-beta.20`) for domain or migrated business rules (`decisionKind = BUSINESS`), enforce the **SAP BDC Ontology & SHACL-Style JSON Logic** architecture:

1. **Five Canonical Ontological Fact Roots (`PraxisFactTreeBuilder` & `OntologicalFactTreeMapper`):**
   - Never pack multi-entity variables into a flat scalar bag (`facts.*`). Every fact provider (`*Facts.java`) must build its tree using `PraxisFactTreeBuilder` or the stateless, thread-safe **`OntologicalFactTreeMapper`** (`org.praxisplatform.rules.facts.OntologicalFactTreeMapper`: `iso8601()`, `epochDay()`, `isoAndEpochDay()`, `mapFiveRoots(...)`, `ConceptBinding.of(...)` / `ConceptBinding.absent(...)`, loading declarative JSON/YAML fact definitions via `RuleFactCatalogLoader` enriched by `DtoMetadataFactCatalogEnricher`):
     - `draft` (`PraxisFactTreeBuilder.ROOT_DRAFT` / `putDraft`): candidate mutation state (`NEW` in database triggers/packages), captured **after** server-side hydration (`hydrate*`);
     - `current` (`PraxisFactTreeBuilder.ROOT_CURRENT` / `putCurrent`): persisted prior state on `UPDATE`/`DELETE` (`OLD` in prior state, or `null` on `CREATE`) so immutability (`draft.field == current.field`) and state transitions are evaluated inside JSON Logic;
     - `<concept>` (`putConcept("vacancy", ...)` / `putConceptEntity("vacancy", entity, idPresentInDraft, nullDefaults)`): 1-hop related domain entity nodes resolved via foreign keys. `putConceptEntity` (and `OntologicalFactTreeMapper` via `PraxisFactTreeBuilder.toScalarObjectNode(Object, DateSerializationMode)`) projects only scalar/flat properties so JPA persistence associations are never lazy-loaded or traversed accidentally, emitting `"present": false` with `nullDefaults` when absent. **Never pass stubbed `false`/`null` values** for 1-hop concept attributes that a `DecisionBinding` guards — always load the real related entity;
     - `neighborhood` (`PraxisFactTreeBuilder.ROOT_NEIGHBORHOOD` / `putNeighborhood`): N-hop aggregate facts or sibling collections within the same scope/tenant (e.g., `hasDateRangeOverlap` count, active holder count, occupied slots);
     - `context` (`PraxisFactTreeBuilder.ROOT_CONTEXT` / `putContext`): execution metadata, tenant (`tenantId`), operation, and frozen clock.
   - **Explicit `DateSerializationMode` (`ISO_8601`, `EPOCH_DAY`, `ISO_AND_EPOCH_DAY`):** Both `PraxisFactTreeBuilder` and `OntologicalFactTreeMapper` honor `PraxisFactTreeBuilder.DateSerializationMode`, allowing civil `LocalDate` fields to publish ISO-8601 strings, epoch-day integers, or dual (`<prop>` + `<prop>EpochDay`) without ad hoc date conversion helpers. Both validate built fact trees against `JsonLogicLimits`.
2. **Injection-Safe JSON Logic DSL (`PraxisJsonLogic`) & `OntologyRuleSetBuilder` (`0.1.0-beta.20`):**
   - Author ontological expressions using **`org.praxisplatform.rules.ontology.PraxisJsonLogic`** instead of manual JSON strings: it builds defensive Jackson `ObjectNode`/`ArrayNode` ASTs (`PraxisJsonLogic.Expr` with fluent `.and(...)`, `.or(...)`, `.not()`, `.when(...)`, `.nonDelete()`, `.whenOperation(...)`, ontological references `draft`, `current`, `concept`, `neighborhood`, `context`, `localVar`, and `PraxisPath` validation).
   - Compose complete `RuleSetDefinition`s (and multi-customer catalogs via `withCustomerErrorDescriptors(...)` / `withProductAndCustomerErrorDescriptors(...)` -> `RuleSetCatalogBundle`) through **`org.praxisplatform.rules.ontology.OntologyRuleSetBuilder`**, accepting `PraxisJsonLogic.Expr` natively in `Rule`, `binding(...)`, `Rule.replaceable(...)`, `.withStage(...)`, typed `RuleParameterTemplate` helpers (`integerTemplate`, `decimalTemplate`, `stringTemplate`, `booleanTemplate`), and `requireReferencedFactPaths(...)` alongside automatic AST introspection.
3. **Strict Boundary Between 1-Hop Edge Traversal (`*FactSource`) and Business Constraints (`*RuleSet`):**
   - **No business predicates in 1-hop SQL `WHERE` clauses:** 1-hop `<concept>` queries in `*FactSource` must filter **only by edge/identity keys** (`tenant_id`, `id`, composite business keys). Never filter status, effective-date coverage (`start_date <= :start AND end_date >= :end`), or business flags inside SQL to return a pre-baked `COUNT(*)` or boolean flag to the engine;
   - **Primitive Projection + JSON Logic Evaluation:** project the raw attributes of the related node (`concept.type`, `concept.status`, `concept.startDate`, `concept.endDate`) and express the full constraint in the JSON Logic AST of `*RuleSet.java` so the rule remains 100% transparent in `/api/praxis/config/domain-rules/**` and `Rules Studio`;
   - **N-Hop `neighborhood` Queries:** SQL aggregations (`COUNT`) are valid **exclusively** under `neighborhood.*` to quantify sibling collisions in a collection (e.g., `neighborhood.overlappingAssignments`, `neighborhood.activeHoldersInVacancy`).
4. **Automatic AST Introspection (`extractReferencedRoots` / `extractReferencedFactPaths`):**
   - Never hardcode `List.of("facts")` in `RuleSetDefinition.availableRoots` or `DecisionBinding.requiredFactPaths`. Use `PraxisFactTreeBuilder.extractReferencedRoots(expression)` and `PraxisFactTreeBuilder.extractReferencedFactPaths(expression)` (including inside `RuleParameterTemplate` builders), which inspect the JSON Logic AST while respecting iterator-local variable scopes (`map`, `filter`, `all`, `some`, `none`, `reduce`).
5. **Canonical Pure-Java Parametric Calculators & Multi-Epoch Selectors (`PLAT-EVO-08`, `PLAT-EVO-12`, `PLAT-EVO-18`):**
   - **Temporal Interstice, Suspension & Reset Math (`org.praxisplatform.rules.parametric.EffectiveDatedIntervalCalculator`, `PLAT-EVO-08`):** Do not hand-code date loops in services or previews for progression interstices, probation, or seniority counting. Delegate to `EffectiveDatedIntervalCalculator` (`InterruptionEffect.SUSPEND` with union-of-overlapping intervals so concurrent leaves never double-penalize, `InterruptionEffect.INTERRUPT_AND_RESTART` resetting on `interruptionEnd + 1` while ignoring leaves starting after `cutoffDate`, `InterruptionEffect.IGNORE`, capped `BonusAddition`, `O(K)` causal projection across active open-ended leaves, and structured `TrailStep` explainability).
   - **Progressive Tax/Contribution Brackets, Cap Abatement & Pro-Rata Math (`org.praxisplatform.rules.parametric.ProgressiveBracketAndCapCalculator`, `PLAT-EVO-12`):** Do not hand-code progressive tax loops, constitutional cap abatement, consignable margin, or pro-rata formulas in host services. Delegate to `ProgressiveBracketAndCapCalculator` (`BracketMode.MARGINAL_SLICES` with optional `ceilingBaseCap`, `BracketMode.TABLE_RATE_MINUS_DEDUCTION`, `calculateCapAbatement` preserving exempt indemnizatory parcels, `reconcileNetAndMargin`, `calculateProRata`, `HALF_UP` rounding, and structured `FinancialTrailStep` audit trails).
   - **Multi-Epoch Temporal Parametric Tables & Matrix/Tri-State Selectors (`org.praxisplatform.rules.parametric.EffectiveDatedBracketTable`, `EffectiveDatedMatrixMatcher<T>`, `TriStateOverrideResolver`, `PLAT-EVO-18`):** Never hardcode single-year tax/contribution brackets or ceiling constants in rule executors or services when retroactive/historical calculation is possible. Register multi-epoch schedules via `EffectiveDatedBracketTable.of(tableKey, description, epochs)` over chronological `BracketScheduleEpoch` windows (`epochId`, `validFrom`, `validTo`, `BracketMode mode`, `ceilingAmount`, `perDependentDeduction`, `brackets`, `ruleCode`, `legalBasis`, `publicationRef` — rejecting overlapping epochs fail-closed at registration) and evaluate via `findEpochAsOf(asOfDate)`, `requireEpochAsOf(asOfDate)`, `resolveCeilingAsOf(asOfDate)`, `calculateProgressiveAsOf(...)` (`TemporalProgressiveResult`), and `calculateCapAbatementAsOf(...)` (`TemporalCapAbatementResult`). On retroactive or multi-period settlements where an item's accrual/reference date differs from the current batch/payment run date, always resolve `EffectiveDatedBracketTable` by the **accrual/reference date of the legal fact** before falling back to the processing run date, and keep addition versus deduction inputs sign-explicit in `ProgressiveBracketAndCapCalculator`. For multi-dimensional parametric rule matching and hierarchical overrides, use `EffectiveDatedMatrixMatcher<T>` (`Criterion<T>`, rejecting ambiguous specificity ties fail-closed) and `TriStateOverrideResolver` (`TriState.PERMITIR | VEDAR | HERDAR`, `parse`, `resolve`, `resolveNumber` preserving explicit `0`/`false`).
6. **1:1 KEEP_SEPARATE Error Lineage & Zero Split-Brain:**
   - Every distinct domain error code must map `1:1` to an individual entry in `*RuleErrorCatalog.java` -> an atomic `DecisionBinding` in `*RuleSet.java` -> an individual `@Test` in `*Test.java`. Never merge multiple error codes into one catalog entry or binding;
   - When an entity or operation is governed by a `*RuleSet`, `PraxisRulesEngine` is the **sole authority** for business rules (`422`). Host `*Invariants` classes must contain **only** structural HTTP guards (`403` tenant isolation, `404` FK existence, `409` `If-Match`/concurrency, and transactional locks) and must never duplicate or short-circuit `RuleSet` rules;
   - Server-side hydration (`hydrate*`) and structural `404`/`403` tenant FK guards must run **before** `RuleEngine` evaluation, and fields hydrated by the server must not carry blocking `@NotNull`/`@NotBlank` bean-validation annotations on `CreateDTO`/`UpdateDTO`.

## Mandatory product controls (source engine contract 1.7)

`DecisionSlot.requiredControlDependencies` is an immutable product declaration of
guard binding keys. Every enabled binding in that slot must include these keys in
`dependsOn`, including REPLACE_EXACT and PARAMETERIZE. The compiler rejects missing,
disabled, non-PRODUCT or non-PROTECTED_GUARD/FORBIDDEN controls and applies the normal
DAG bounds and cycle checks. Host admission must compare product slots and protected
bindings exactly; the neutral compiler cannot authenticate product authorship.

Require exactly one enabled binding in every SINGLE slot, including slots absent
from the enabled-binding index. Removing or disabling the only business decision
must fail cardinality validation even when its protected controls remain intact.
Empty optional extension points must declare their appropriate MULTIPLE contract.
Host previews must reject a missing selected decision as a technical plan failure;
returning without evaluation is not evidence that the decision is inapplicable.

Keep applicability outside a replaceable business predicate. An inapplicable guard
returns NOT_APPLICABLE; unavailable evidence remains inconclusive. Customer-extension/business error
messages remain independent decisions and must still deny when product execution is
dispensed. Technical guards have their own identities, never invented legacy errors.

Use `PraxisRulePlanCompiler.compilePreview` to validate the complete source and
compile the selected transitive dependency closure. Never strip dependsOn in a host
preview. Preserve source parameterization, control declarations, error descriptors,
digests and compatibility through Config manifests and snapshots. Historical content
stays immutable; new execution requires current-contract compilation and admission.
This source guidance does not claim a published coordinate or integrated acceptance.

## Governed scalar parameterization (introduced in engine contract 1.6)

Inspect `RuleParameterTemplate`, `RuleParameterDefinition`, `RuleParameterization`,
`RuleParameterResolver`, planner and snapshot compiler together. A PARAMETERIZABLE
slot must publish a product template; it is not permission for arbitrary JSON Logic.
Use the actual contracts: `OverridePolicy.PARAMETERIZABLE` admits
`CompositionPolicy.PARAMETERIZE` with `RuleParameterTemplate`;
`OverridePolicy.REPLACEABLE` admits `CompositionPolicy.REPLACE_EXACT`, subject to
all remaining planner/admission checks. `PARAMETRIC_TEMPLATE` is not an enum value
or a replacement composition policy.
A CUSTOMER/PARAMETERIZE source binding carries only exact template identity and
values, with executor/negative outcome/required facts absent. The compiled plan
materializes these from the template; serialized snapshots retain source bindings
so recompilation repeats admission, rather than trusting a derived executor.

- Declare STRING/NUMBER/INTEGER/BOOLEAN restrictions, required/nullable/readOnly,
  unit, inclusive bounds, enum, explicit default and exact literal JSON Pointers.
  Java null means no default; native JSON null is explicit. Preserve absent,
  null, false and zero. Defaults must equal original template literals.
- Every parameter binds existing scalar operands; reject var/missing addressing,
  overlapping/duplicate sites, unknown keys, structural edits and readonly changes.
  Optional/readOnly entries need an explicit default. Java parameterization and
  host-extension operators are unsupported; built-in dialect validation fails closed.
- Reuse the public pure resolver for Config admission; never invent a host evaluator,
  facts namespace overlay, JSON patch language or second parameter schema.
- Bound template, declared/effective values and expression expansion. Include schema,
  defaults, unit, declared values and compiled expression in canonical identity.
  Compare canonical numeric JSON, not Java record/BigDecimal scale equality.
- Update direct constructor consumers in the same beta cut; no compatibility overload
  that permits old PARAMETERIZE expressions. Prove equal-facts A/B results, invalid
  types/limits/defaults/null/readonly, source-snapshot roundtrip and digest changes.

This contract guidance does not assert release availability. For source development,
an isolated Maven repository may consume the exact candidate JAR with recorded SHA;
keep that proof distinct from the published-coordinate release gate above.

## Direct dependency outputs (engine contract 1.5)

This guidance accompanies the G1 implementation of contract 1.5. It is not
proof of a published Maven release or downstream adoption. Verify the actual
engine coordinate and contract before using it; beta.15/contract 1.4 only gates
and orders dependencies and does not supply this data channel.

- Capture native finite JSON facts once for every binding and the facts digest.
  Reject POJO/binary/missing/non-finite facts as FACTS_INVALID; bound canonical
  UTF-8 size before hashing so compact decimal exponents cannot cause unbounded
  expansion. FACTS_LIMIT_EXCEEDED is technical, and its budget is independent
  from output transport. The host keeps the input stable during initial capture.
- Recheck exact engine/dialect/corpus coordinates in evaluation before invoking
  executors, including restored plans. PLAN_COMPATIBILITY_INVALID returns the
  current runtime baseline without execution or factsDigest; it does not rewrite
  the original definition or authenticate a manually constructed plan. Compile
  candidates through the governed host flow; never relabel stale cached plans.
- Keep one evaluation of the governed DAG. `RuleExecutorContext.directDependencyOutputs`
  derives only from direct `dependsOn` results in the current evaluation; never
  enrich facts between passes, create a host-local graph, or use a submitted
  derived value as authority.
- Both producer and consumer must be PRODUCT Java bindings in DOMAIN_DECISION
  or POST_DECISION. Other edges remain control-only, including attested CUSTOMER,
  SECURITY, protected guards, generated infrastructure, and intent stages.
  ALLOW supplies output; preserve all five decision states and existing gates.
- Missing Java output omits the key; explicit JSON null preserves it. Consumers
  decode and validate domain output using their exact implementation/host
  contracts. Missing or malformed required output is technical failure, never
  zero, business denial, or fallback to facts. JSON Logic still sees original
  facts only; this channel does not change the dialect or shared corpus.
- Transport native JSON trees with finite numbers only. POJO, binary, missing
  sentinel and non-finite nodes in eligible output fail with
  DEPENDENCY_OUTPUT_INVALID, without consumer execution or partial binding
  results; do not coerce them or change control-only edges.
- Keep map order deterministic and copy mutable JSON defensively. Prove isolation
  across accesses, bindings, retained results and concurrent evaluations.
- Bound canonical UTF-8 bytes (including keys) before transport copies, both per
  context and cumulatively per evaluation against MAX_PUBLIC_RESULT_BYTES.
  Validate the entire map shape first: INVALID has fixed precedence over size,
  independent of field insertion order. Empty maps cost zero; fan-out charges
  every delivered context again. Overflow
  produces DEPENDENCY_OUTPUT_LIMIT_EXCEEDED/TECHNICAL_ERROR with no partial binding
  results. Preserve existing structural and public result limits too.
- Prove positive chaining without prefilled derived facts, direct-only access,
  excluded trust/stage pairs, missing/null, five-state gates, exact/over-budget
  boundaries, cumulative fan-out, deterministic digests and thread safety.
- Contract 1.5 is an exact compatibility boundary. Recompile and reapprove new
  compositions; do not relabel old snapshots or hashes. Config historical
  verification, executable admission and coordinated migration are separate
  downstream gates. Engine tests do not prove host rollout, UI or database paths.

## Gates

Define completion criteria and select tests from the changed semantic contract,
including negative, determinism and compatibility cases and direct consumers.
Use incremental focused runs while editing. After a failure, diagnose and rerun
the affected cases/dependents before broadening. A test/fixture change can have
shared impact; inspect it rather than assuming all test-only edits are isolated.

The complete engine gate remains mandatory for contract/planning changes and
where required by release governance. Run it on the consolidated candidate and
repeat only after relevant evidence invalidation, a demonstrated coverage gap or
an explicit gate requirement. Do not repeat Config/host-wide suites merely because
the engine's gate ran. Keep cross-runtime corpus and consumer gates below when
their contracts change. Source/dependency identity must remain valid; no concurrent
builds in one target or replacement of artifacts while a consumer uses them.

For the complete gate, use Java 21 and Maven 3.9+:

```powershell
$env:JAVA_HOME='<JDK-21>'
$env:Path="$env:JAVA_HOME\bin;$env:Path"
mvn clean verify
```

When TypeScript semantics/models/RFC/corpus change, run focused service and conformance specs, `npm run build:praxis-core`, and a direct consumer build/test when an exported shape changes. Prove the packaged Java corpus is identical to the Angular corpus. Never treat a timeout as success.

Report command, reason for scope, duration, result and candidate identity. Stop
when the scoped change and all required gates/derived artifacts are complete;
a time limit with proof outstanding is a partial checkpoint, not acceptance.

Do not publish, tag or add CI until repository ownership and the official release channel are confirmed.
