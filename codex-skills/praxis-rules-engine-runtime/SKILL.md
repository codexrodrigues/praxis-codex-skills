---
name: praxis-rules-engine-runtime
description: Implement, review, debug, or extend the deterministic Praxis rules engine, including JSON Logic parity, RuleSet contracts, composition slots, planner DAGs, versioned Java executors, five-state decisions, limits, packaging, and neutral host consumption.
---

# Praxis Rules Engine Runtime

## Owners and boundaries

Treat `@praxisui/core` RFC, models, descriptors and shared corpus as the current normative dialect owner. Treat `praxis-rules-engine` as the owner of the pure Java runtime. Change RFC, TypeScript, Java and corpus in the same cycle when semantics change.

Keep the engine stateless, thread-safe, embeddable and free of Spring, I/O, persistence, endpoints, tenant stores, snapshots, workflow, effects, database access and domain-specific rules. Keep authoring/publication/snapshots in `praxis-config-starter`; keep facts, security, transactions, algorithms and effects in domain hosts; keep metadata projection in `praxis-metadata-starter`.

Treat RuleSet identity, slots, bindings, closed aggregation policies, deterministic plans, compatibility coordinates, results, and executor registry contracts as owned by `praxis-rules-engine`. A host may adapt these contracts but must not redefine their semantics.

## Required source audit

Read applicable `AGENTS.md`, then inspect:

- `praxis-ui-angular/projects/praxis-core/docs/rfc-json-logic-semantics.md`
- TypeScript models, token, service and focused specs under `projects/praxis-core/src/lib`
- `praxis-ui-angular/docs/json-logic-conformance/conformance-fixtures.json`
- all Java production/tests and engine documentation
- `docs/operator-conformance-matrix.md` and `docs/architecture.md`

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
- Represent slot cardinality and aggregation explicitly. Customer composition must respect product-owned override policy; protected guards cannot be customized.
- Compile dependencies as a bounded DAG with deterministic stage/order/key tie-breaking. Reject cycles, later-stage references, excessive edges, and excessive fan-out.
- Preserve `ALLOW`, `DENY`, `NOT_APPLICABLE`, `INCONCLUSIVE`, and `TECHNICAL_ERROR`; never convert technical failure into business denial.
- Continue independent branches after `INCONCLUSIVE` so a real `DENY` is not hidden, while preventing dependent execution and effect planning.
- Consolidate the final allow/not-applicable outcome from terminal DAG bindings. An intermediate guard or prerequisite `ALLOW` must never lift a terminal `NOT_APPLICABLE` branch.
- Require every effect-intent binding to declare an explicit decision dependency, and never execute it while any prior branch is inconclusive.
- Apply deterministic structural limits to host-resolved facts and Java executor outputs, not only to JSON Logic expressions.
- Include stable plan/facts digests and exact runtime/implementation coordinates in evaluation results. Keep wall-clock duration and observation infrastructure outside the deterministic core.

## Changing semantics or operators

1. Inventory RFC, TypeScript registry/runtime, Java registry/runtime and corpus.
2. Record the convergence decision before implementation; do not copy a runtime bug merely for parity.
3. Update the normative RFC and operator matrix.
4. Update both runtimes and their validators from the same decision.
5. Extend the shared corpus with typed values, truthiness, structured errors and any operator catalog change.
6. Add focused tests for missing/null, invalid type, arity, path, limits and determinism.
7. For a host operator, require namespace and prove presence in every runtime that may evaluate persisted rules.

Do not create textual DSL fallbacks, parallel V1/V2 contracts, permissive JSONPath, unrestricted regex, implicit process time, or runtime database access.

## Changing RuleSet contracts or planning

1. Read the accepted Rule Platform ADRs and classify the change as public-contract and architectural.
2. Map the engine, Config Starter, Quickstart, public documentation, goldens, and Maven coordinate impact before editing.
3. Keep public records immutable and defensively copy mutable JSON values.
4. Add positive and negative tests for identity, compatibility, composition, DAG ordering, missing/null, decision precedence, effect gating, limits, and thread safety.
5. Run the complete engine gate, including Javadocs, then consume only an officially published Maven coordinate in downstream repositories.

Do not use `mvn install`, file repositories, or local version overrides as downstream release proof. While the public beta line is active, compatible additive work stays on the next beta unless release governance establishes a breaking change.

## Gates

Use Java 21 and Maven 3.9+:

```powershell
$env:JAVA_HOME='<JDK-21>'
$env:Path="$env:JAVA_HOME\bin;$env:Path"
mvn clean verify
```

When TypeScript semantics/models/RFC/corpus change, run focused service and conformance specs, `npm run build:praxis-core`, and a direct consumer build/test when an exported shape changes. Prove the packaged Java corpus is identical to the Angular corpus. Never treat a timeout as success.

Do not publish, tag or add CI until repository ownership and the official release channel are confirmed.
