---
name: ergon-rule-migration-orchestration
description: Orchestrate Parte 2 - Migracao Progressiva de Regras for Ergon/Archon migrations after an approved Parte 1 functional baseline handoff. Use when Codex must validate a Parte 1 baseline, plan or gate phases 9-18, decide whether rule migration may start, coordinate rule inventory, dependency graph, HADES read-only chain, shadow mode, preflight/promotion, legacy containment, final rule handoff, or return work to Parte 1 phases 4/5/7/8.
---

# Ergon Rule Migration Orchestration

Use this skill as the top-level conductor for Parte 2 - Migracao Progressiva de Regras. It starts only after Parte 1 - Migracao Funcional has a closed, approved baseline handoff for the target screen/operation. The baseline is usually DB-backed, but may be `WRITE_TABLE_DIRECT_SAFE` when Parte 1 explicitly proved direct table/platform persistence is safe for that exact operation.

## Core Rule

Apply the root migration `AGENTS.md` when Parte 2 introduces or changes public
runtime contracts, rule APIs, error envelopes, feature flags, or migration
documents. Do not expose HADES, SQL, `ROWID`, empresa, usuario, perfil,
package names, or session context as public API metadata while moving rules
toward Java.

Never let Parte 2 correct, complete, or contradict Parte 1 silently. If rule migration discovers missing baseline evidence, return to the correct Parte 1 phase before proceeding.

No rule can advance to shadow, preflight, or promotion without:

- identified legacy origin;
- referenced Parte 1 artifact;
- known parity baseline;
- classified dependencies;
- classified HADES/EP/client behavior;
- classified side effects;
- explicit fallback;
- explicit return-to-Parte-1 rule.

For every operation under Parte 2, the orchestrator must be able to answer or explicitly block on this canonical question: which legacy rules exist for this operation, where each rule comes from, in what known order they execute, whether each one is product/client/security/side-effect/unknown, and what HADES activates, bypasses, orders, or leaves unknown. If any part is unknown, do not infer it; route to Phase 10/11/12, `ergon-table-rule-audit`, or the appropriate Parte 1 return.

If Parte 1 uses `WRITE_TABLE_DIRECT_SAFE` instead of DB-backed for an operation, validate that `write-route-decision.md`, `write-contract.md`, `write-parity-matrix.md`, `parity-results.md`, and the handoff all carry that state explicitly. If the operation is only `WRITE_TABLE_DIRECT_CANDIDATE`, Parte 2 must not start for rule migration on that operation.

Do not make legacy fallback the permanent conceptual model for new rule runtime code. Treat DB-backed behavior as a current baseline/authority and historical parity source. For reusable abstractions, prefer neutral names such as `RuleExecutionMode`, `RuleExecutionTarget`, `RuleAuthority`, `RuleDecisionPlan`, `RuleEvaluationResult`, and `RuleObservation`. Avoid new long-lived names such as `LegacyFallback`, `LegacyRuleEngine`, `OracleRuleRuntime`, or `HadesRuleEngine`. Parte 2 must not be blocked by TemporalIO, DSL, or workflow orchestration, but new contracts should be DSL-ready and TemporalIO-ready for later phases.

## Canonical Phases

| Phase | Name | Purpose |
| --- | --- | --- |
| 9 | Rule Migration Intake | Validate that Parte 1 handoff is complete enough to start rule migration. |
| 10 | Rule Inventory | Extract candidate product/client/security/side-effect rules from Parte 1 evidence. |
| 11 | Rule Dependency Graph | Map nested calls, packages, functions, tables, HADES, and side effects. |
| 12 | HADES Read-Only Chain | Build activation/order chains from `HAD_CAD_SPROC` and `HAD_CAD_MULT_EPS` without executing Java decisions from DB. |
| 13 | Shadow Contract | Define Java rule scope, fixtures, inputs, outputs, comparison, observability, and fallback. |
| 14 | Shadow Execution | Run Java in parallel without deciding; compare against the approved Parte 1 baseline route. |
| 15 | Preflight Decision + Runtime Evidence | Decide whether Java may block proven cases before the legacy route, then prove guarded runtime execution in `preflight-results.md`; DB still confirms allowed cases unless promotion is separately approved. |
| 16 | Promotion Decision | Decide whether Java becomes authoritative for a precise promotion boundary. |
| 17 | Legacy Rule Containment | Decide whether the legacy rule remains, is bypassed, deactivated, fallback-only, or deliberately duplicated. |
| 18 | Final Rule Handoff | Consolidate authoritative, preflight, shadow, DB-backed, rejected, and deferred rules. |

## Required Artifacts

Use `docs/migracao/<SCREEN>/rule-migration/` for Parte 2 artifacts.

Always maintain:

- `rule-migration-intake.md`
- `rule-traceability-matrix.md`
- `phase-<PHASE-ID>-execution-gate.md`

Create phase-specific artifacts when the phase runs:

- `rule-inventory.md`
- `rule-dependency-graph.md`
- `hades-rule-chain.md`
- `shadow-contract.md`
- `shadow-results.md`
- `preflight-decision.md`
- `create-preflight-precedence-plan.md`
- `structured-error-envelope-decision.md`
- `preflight-runtime-evidence-plan.md`
- `preflight-implementation-readiness.md`
- `preflight-results.md`
- `promotion-decision.md`
- `legacy-containment.md`
- `final-rule-handoff.md`
- global `rule-execution-model.md` in the portable process package when runtime code or reusable abstractions are introduced

Phase IDs continue from Parte 1: `phase-9-execution-gate.md` through `phase-18-execution-gate.md`.

## Operation Rule Discovery Question

During diagnosis and especially Phases 10-12, answer this for the exact screen/operation:

1. Which legacy rules exist or are suspected for this operation?
2. Where does each rule originate: trigger, package, procedure, constraint, HADES, EP, `C_ERGON`, view, permission/security, or side effect?
3. Is each rule product, client, security, side effect, dependency blocker, edge validation, or unknown?
4. What known execution order exists across trigger/package/HADES/EP/client behavior?
5. What does HADES activate, bypass, order, or leave unknown in the current environment?
6. Which rules remain DB-backed, which can become candidate/shadow/preflight, and which are blocked/deferred?

If the answer is incomplete, keep the phase blocked/deferred and record the missing evidence in the matrix and execution gate.

## Workflow

This v1 skill is the single conductor for Parte 2 phases 9-18. Specialized Parte 2 skills may be extracted later, but this skill owns orchestration, gates, and artifact consistency for now.

For corporate use, ensure this local skill is distributed/versioned as part of the migration kit. If the skill is not installed in the developer workstation, execute the same flow manually from the portable repo artifacts under `docs/migracao/rule-migration/`.

Before closing any phase, validate cross-artifact identity: screen/transaction, resource/API path, rule id, operation, environment, and relevant user/company fixtures must match across code, evidence, matrix, and artifact location. If code or logs say `screen=ERGadm00189`, do not close that rule under `docs/migracao/ERGadm00033/`; fix the artifact location or matrix first.

1. Identify the target screen, operation, and current Parte 2 phase.
2. Read `references/part-1-baseline-contract.md` and validate required Parte 1 inputs.
3. Create or update `rule-migration-intake.md` and `rule-traceability-matrix.md`.
4. If baseline evidence is missing, use `references/return-to-part-1.md` and stop Parte 2 advancement.
5. If the baseline is sufficient, route the work to the appropriate Parte 2 skill or phase:
   - inventory and classification;
   - dependency graph;
   - HADES read-only chain;
   - shadow contract/execution;
   - preflight/promotion;
   - legacy containment;
   - final handoff.
6. Close each phase with `phase-<PHASE-ID>-execution-gate.md`.

Phase 15 has planning/decision outcomes before runtime: `Preflight Candidate`, `Preflight Approved`, `Preflight Approved Candidate - planning only`, and `Preflight Deferred - runtime blocked`. `Preflight Approved` records the governance decision in `preflight-decision.md`; `Preflight Approved Candidate - planning only` means a runtime evidence plan and readiness review exist, but implementation still requires explicit approval; `Preflight Deferred - runtime blocked` is required when the boundary is understood but precedence, structured error, rollback, observability, HADES, or rollout evidence is missing. `Preflight Running` requires `preflight-results.md` evidence showing feature flag plus operational approval gate, rollback, DENY blocked before the baseline route, ALLOW still uses the approved baseline route, compatible structured error response, no-mutation, cleanup, and observability. Do not treat HTTP status alone as shadow/preflight equivalence; if code/message/fields cannot be extracted, classify the comparison as inconclusive.

Before implementing preflight runtime, create `preflight-runtime-evidence-plan.md` and `preflight-implementation-readiness.md`. The readiness gate must explicitly approve implementation; planning approval alone is not permission to write code. The runtime plan must require two independent default-off gates, proof that DENY did not call the approved baseline executor/route, proof that ALLOW still uses the approved Parte 1 baseline route, v2/error-envelope parity, rollback, and observability. Oracle row counts alone are not sufficient proof that the approved baseline route was not called.

Before implementing any reusable rule runtime classes, check the portable `rule-execution-model.md` if present. Implementation readiness should record that the slice uses neutral execution-mode, authority, decision, and observation names and does not introduce TemporalIO as a Parte 2 dependency.

No preflight may block before the approved Parte 1 baseline route when it can mask a higher-priority baseline error. For create preflight, require `create-preflight-precedence-plan.md` and evidence covering at least permission/security plus duplicate, missing required fields, missing type/code, invalid quantity/format, invalid period/vinculo, and the scoped validation error. If precedence is not proven, keep runtime preflight blocked. For update preflight, prove missing row, permission/security denial, dependency conflict, and the scoped validation error before blocking before the baseline route.

Before corporate rollout or promotion, revalidate target-environment HADES. Current-environment HADES absence can unblock controlled smoke in that environment, but it never authorizes corporate rollout or promotion by itself. Corporate rollout also requires an acceptable rollback model, structured API error behavior, observability status interpretation, and non-smoke observation evidence.

## Reference Files

- `references/part-1-baseline-contract.md`: required Parte 1 handoff inputs.
- `references/artifact-contract.md`: Parte 2 artifact definitions and matrix fields.
- `references/phase-gates.md`: phase gates and closeout rules.
- `references/return-to-part-1.md`: hard return rules to Parte 1 phases 4/5/7/8.
- `references/status-taxonomy.md`: rule-level statuses and phase-level statuses.
- `references/templates.md`: copyable Markdown templates.

Read only the references needed for the current phase.
