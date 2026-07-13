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

For business-rule, policy, eligibility, compliance, validation, or shared migration decisions, treat `/api/praxis/config/domain-rules/**` as the governed authoring/publication source and treat `form_config`, `option_source`, `backend_validation`, `workflow_action`, `approval_policy`, table effects, and other runtime targets as materializations. `formRules`, `formRulesState`, component edit plans, visual guidance, table config, and host callbacks may consume or preview a projection, but they must not become the primary owner of the decision.

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
5. Run the complete engine gate, including Javadocs, then consume only an officially published Maven coordinate in downstream repositories.

For snapshot work, prove the full ownership chain: the engine compiles the runtime-neutral candidate, Config Starter persists and advances the governed head transactionally, and a host compiles with its executable registry before an atomic last-known-good swap. A v1 → v2 → v1 rollback must preserve v1's content hash while issuing a new head ETag and activation revision.

Do not use `mvn install`, file repositories, or local version overrides as downstream release proof. While the public beta line is active, compatible additive work stays on the next beta unless release governance establishes a breaking change.

When migrating Ergon or another host, use the engine skill to remove cognitive load from migrators by routing questions to the canonical layer: missing facts or algorithms belong to the host/domain contract, shared decisions belong to `domain-rules`, deterministic expression semantics belong to the JSON Logic dialect/engine, and UI behavior belongs to materialized target adapters. Avoid screen-local rule transforms that make one migrated screen pass while leaving the platform unable to explain, simulate, publish, or replay the decision.

## Gates

Use Java 21 and Maven 3.9+:

```powershell
$env:JAVA_HOME='<JDK-21>'
$env:Path="$env:JAVA_HOME\bin;$env:Path"
mvn clean verify
```

When TypeScript semantics/models/RFC/corpus change, run focused service and conformance specs, `npm run build:praxis-core`, and a direct consumer build/test when an exported shape changes. Prove the packaged Java corpus is identical to the Angular corpus. Never treat a timeout as success.

Do not publish, tag or add CI until repository ownership and the official release channel are confirmed.
