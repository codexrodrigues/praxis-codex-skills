# Executor Selection Matrix and Forward Tests

## Matrix

| Evidence shape | Classification |
| --- | --- |
| Pure supported expression, known facts/nulls/limits | `JSON_LOGIC` candidate |
| Deterministic protected guard or typed algorithm | `JAVA_TYPED` candidate |
| External typed fact acquisition plus pure predicate | `FACT_PROVIDER_PLUS_DECISION` candidate |
| Query, mutation, integration, audit or workflow | host/orchestration/effect owner |
| Any material unknown or conflict | `KEEP_DB_BACKED` / review required |

Use the active repository's surface matrix and schemas for exact enum values.
This table describes responsibility and must not invent a schema value.

## Forward Tests

- A date comparison with known nullable facts and supported operators may be a
  JSON Logic candidate; a missing null contract keeps it under review.
- A payroll algorithm with loops and typed domain calculations selects Java,
  not a large opaque JSON expression.
- A database cardinality query stays in a provider/repository; only its typed
  result may feed a pure decision.
- A trigger that mutates and raises an error must be decomposed; never classify
  the whole trigger as one Java or JSON Logic rule.
- A suggestive name and repeated error code with incomplete lineage yields
  `KEEP_DB_BACKED`, not an inferred executor.
