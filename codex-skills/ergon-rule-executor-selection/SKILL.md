---
name: ergon-rule-executor-selection
description: Classify an Ergon rule decision conservatively as JSON Logic, typed Java, fact-provider plus decision, host orchestration/effect, or KEEP_DB_BACKED for governed target planning. Use when Codex must choose the appropriate execution surface from evidence about purity, facts, queries, algorithms, side effects, security, customization and supported operators without inferring semantics or generating Java, expressions, runtime definitions or authority.
---

# Ergon Rule Executor Selection

Classify the execution responsibility; do not implement it. Feed the result to
`$ergon-rule-target-planning` and leave phase advancement to
`$ergon-rule-migration-orchestration`.

## Step Zero: Readiness

Read `docs/migracao/rule-migration/factory-contracts/part2-foundation-readiness-v2.json`
and resolve profile, environment, authority and allowed action before selecting a target. Selection may proceed as technical
draft only when admitted. A selection never authorizes executable draft,
shadow, publication or activation.

## Evidence Required

- canonical decision identity and reviewed source lineage;
- known input/output semantics, null behavior and deterministic order;
- facts and providers, queries, algorithms, mutations and effects;
- security/protection and customer-extension policy;
- JSON Logic operator/subset coverage and Java runtime contract evidence;
- explicit gaps from the semantic gate and Parte 1 reconciliation.

Read `references/selection-matrix-and-forward-tests.md` before classifying.

## Selection Rules

- Choose `JSON_LOGIC` (`decisionKind = BUSINESS`, `praxis-rules-engine`, `DecisionBinding`) only for a pure, deterministic business rule expression whose facts,
  null semantics, operators, limits and outcomes are fully representable in
  the published common subset.
- Choose `JAVA_TYPED` (`decisionKind = BUSINESS`) for protected guards, typed algorithms, complex
  calculations or product-owned implementations that remain deterministic and
  effect-free at the decision boundary.
- Choose `FACT_PROVIDER_PLUS_DECISION` when Java must obtain or normalize typed
  facts but the resulting decision remains pure and separately representable.
- Distinguish **`decisionKind = AUTHORIZATION`** (`praxis-authz-*` / `OPA`, `RuntimeEnforcementBinding`) whenever the legacy PL/SQL or HADES logic governs actor/principal permission, organizational/sectoral row scope (`empCodigo`, `FLAG_ACESSO`, Cedente vs. Cessionário, `SIS_DEPTO` -> `DataScopePlan`), field-level read/write authority, or LGPD post-read masking (`FieldMaskingPlan`); never encode security/ABAC/data-scope rules as `JSON_LOGIC` business `RuleSet`s.
- Choose host orchestration/effect ownership for queries, persistence,
  integration, audit or other effects. Never hide them inside a free rule.
- Choose `KEEP_DB_BACKED` when semantics, precedence, dependencies, effects,
  provider ownership or representability remain unsafe or unknown.

Record evidence for every selected axis. If evidence conflicts, preserve the
conflict and select no executable target. Labels, PL/SQL shape, error-code type,
candidateTarget, camelCase and implementation convenience are not evidence.

## Output Boundary

Produce a reviewable selection record or populate only the governed selection
input expected by FND-12. Do not emit an expression, Java skeleton, Config
payload, snapshot, executor registry entry or approval. Do not turn
`KEEP_DB_BACKED` into a runtime binding.
