---
name: ergon-rule-target-planning
description: Build, check and technically admit non-executable FND-12 TargetBindingPlan drafts for Ergon rule migration. Use after evidence-bound decomposition and semantic-gap reporting when Codex must project a selected decision into governed JSON Logic, Java, host or DB-backed target surfaces, preserve unknowns and blockers, run the canonical checker/admission chain, or prepare target-planning evidence without generating code, Config records, runtime definitions, business approval or authority.
---

# Ergon Rule Target Planning

Materialize only the internal FND-12 technical plan. Let
`$ergon-rule-migration-orchestration` decide phase admission and use
`$ergon-rule-executor-selection` for the executor classification.

## Step Zero: Readiness

Read `docs/migracao/rule-migration/factory-contracts/part2-foundation-readiness-v2.json`
before opening inputs. Resolve the active profile, environment, authority,
allowed stages/actions and blocking gaps. Continue only when the requested work
is admitted as `MATERIALIZE_TECHNICAL_DRAFT`; never translate corporate
`NOT_READY` into a global development block or reuse development admission in
another environment.

## Required Inputs

- exact screen, operation, canonical decision identity and environment;
- RF-01 source manifest, RF-03 decision proposal, RF-04 materialized profile
  and RF-05 semantic-gap report with verified lineage;
- reconciled Parte 1 evidence and explicit unresolved conflicts;
- an evidence-backed executor selection or explicit `UNKNOWN`/review question;
- canonical FND-12 schemas, matrix, checker, materializer and toolchain from the
  active migration repository.

Read `references/contract-and-forward-tests.md` before creating or reviewing a
plan.

## Workflow

1. Freeze evidence revisions, hashes and canonical decision identity.
2. Confirm every requested target surface is admitted by the total surface
   matrix; reject any unlisted combination.
3. Copy only governed facts. Preserve order, dependencies, reason-code
   semantics, cardinality, aggregation and executor details as explicit
   unknown envelopes when evidence is insufficient.
4. Produce exactly one `RULE_TARGET_BINDING_PLAN` with
   `MATERIALIZED_UNCHECKED`. Do not embed checker or admission results.
5. Run the independent checker. Accept only a separate
   `TECHNICAL_PLAN_VERIFIED` result bound to the exact plan digest.
6. When local admission is requested, use the official admission command from
   a clean revision and the fixed-local-disk store capability. Accept only a
   separate `TECHNICAL_PLAN_ADMITTED` receipt.
7. Update traceability and stage blockers. Do not close a migration phase from
   FND-12 status alone.

## Hard Boundary

Never create JSON Logic expressions, Java classes, `RuleSetDefinition`, Config
materialization, executable snapshots, runtime bindings, publication,
activation, shadow authorization or legacy containment. `KEEP_DB_BACKED` is an
authority hold, not an engine executor. Technical admission is not business
homologation.

Fail closed on evidence drift, unknown target surface, ungoverned default,
secret/source/SQL leakage, dirty producer revision, checker mismatch, remote
store, forged capability or partial batch.
