---
name: ergon-rule-migration-orchestration
description: Orchestrate Parte 2 - Migracao Progressiva de Regras for Ergon/Archon through progressive gates for development discovery, homologation and production authority. Use when Codex must validate Parte 1 evidence, plan or gate phases 9-18, decide which profile/actions are admitted, coordinate rule inventory, dependency graph, HADES read-only chain, shadow mode, preflight/promotion, legacy containment, final rule handoff, or return work to Parte 1 phases 4/5/7/8.
---

# Ergon Rule Migration Orchestration

Use this skill as the top-level conductor for Parte 2 - Migracao Progressiva de Regras. Development intake may start with sufficient screen/operation/source identity and explicit Parte 1 gaps; missing baseline evidence blocks phase closeout or the first transition that depends on it, not creation of the intake package. Shadow comparison, preflight and authority still require the approved Parte 1 baseline appropriate to their boundary. The baseline is usually DB-backed, but may be `WRITE_TABLE_DIRECT_SAFE` when Parte 1 explicitly proved direct table/platform persistence is safe for that exact operation.

## Core Rule

Treat rule migration as governed decision migration, not as a mechanical PL/SQL-to-Java rewrite. The legacy route is the approved parity authority and evidence source; the target platform shape should be a canonical, observable, reversible decision boundary that can later be materialized through Praxis metadata, config/authoring, runtime services, UI capabilities, and API responses.

Apply progressive governance on two axes: pipeline stage and execution
profile/environment. `FACTORY_DEVELOPMENT` is the normal low-bureaucracy path
for intake, inventory, dependency discovery, HADES read-only, technical drafts,
offline simulation and controlled development experiments. It may coexist with
corporate production readiness `NOT_READY`. `HOMOLOGATION_CANDIDATE` and
`PRODUCTION_AUTHORITY` require fresh admissions bound to their target
environment; development evidence or permission never crosses that boundary
automatically.

Fail closed at the first action capable of producing the corresponding risk,
not at earlier evidence-gathering stages. Preserve early controls for secrets,
data minimization/redaction, provenance, toolchain integrity, bounded queries
and technically enforced read-only access. Do not require production SIEM, SLO,
HA/DR, final retention policy, business owner confirmation or per-run human
approval merely to open development intake or inventory.

## Mandatory Readiness First

Before reading phase-local status, creating an artifact or routing to another
Parte 2 skill, read
`docs/migracao/rule-migration/factory-contracts/part2-foundation-readiness-v2.json`
from the active migration repository. Resolve and record:

- `corporateReadinessStatus` as production context, never as an automatic
  development veto;
- active profile, environment class and authority level;
- the exact requested stage and action;
- profile-specific blockers and constraints;
- whether cross-environment admission reuse is forbidden.

If readiness is missing, invalid or does not admit the requested stage/action,
do not advance that transition. Read-only diagnosis may identify the precise
repair, but must not manufacture a profile, waiver or implicit admission.

Apply the root migration `AGENTS.md` when Parte 2 introduces or changes public
runtime contracts, rule APIs, error envelopes, feature flags, or migration
documents. Do not expose HADES, SQL, `ROWID`, empresa, usuario, perfil,
package names, or session context as public API metadata while moving rules
toward Java.

Before creating a new rule contract, rule API, feature flag, error envelope,
metadata field, action, surface, or UI affordance, inventory what Praxis already
knows but has not materialized correctly. Classify each need as
`ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. Only
`lacuna-real-de-contrato` justifies a new platform contract; otherwise fix the
canonical owner or materialization.

Use the canonical owner map when a rule becomes platform behavior:
`praxis-config-starter` is the natural boundary for governed semantic decision
authoring, simulation, approval, publication, templates, registry state, ETag,
and materialization contracts; `praxis-metadata-starter` owns resource
metadata, schemas, capabilities, HATEOAS links, actions, surfaces, and
operation/schema resolution; `praxis-ui-angular` consumes materialized
decisions and must not become the primary rule source.

Do not route rule intent, UI actions, rule selection, or promotion boundaries by
keywords, labels, regexes, aliases, XML names, or table-name heuristics. Textual
matching may rank candidates only after the target screen, operation, rule, and
canonical artifact scope have been resolved from governed evidence.

Never let Parte 2 correct, complete, or contradict Parte 1 silently. If rule migration discovers missing baseline evidence, record the gap in intake/matrix and return the affected closeout or downstream transition to the correct Parte 1 phase. Unrelated read-only discovery may continue when the active profile admits it.

No rule can close shadow comparison, preflight evidence, homologation or promotion without:

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

If a UI, dashboard, workflow, or external consumer can expose the operation
whose rule is migrating, validate the latest UI/dashboard/handoff gate before
advancing. A UI must not expose a preflight, promoted, blocked, or deferred rule
as a local capability; it must consume the canonical API/metadata/config state
or return to Parte 1/UI wiring for repair.

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
- `rule-canonical-decision-inventory.md`
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

Starting a discovery phase and closing it are different decisions. In
`FACTORY_DEVELOPMENT`, unknowns are expected inputs to Phases 9-12. They block
only the closeout or downstream action whose evidence they invalidate; they do
not require a waiver to create intake, inventory or a dependency graph draft.

## Workflow

This skill is the conductor for Parte 2 phases 9-18. It owns orchestration, gates, and cross-artifact consistency; specialized skills own bounded phase work. Use `$ergon-rule-source-extraction` for Phase 10 structural source inventory and preserve its blockers without promoting them to semantic conclusions. Use `$ergon-rule-decision-decomposition` for the evidence-bound RF-03 decision pack; keep technical proposals separate from later business homologation. Use `$ergon-rule-executor-selection` and `$ergon-rule-target-planning` for conservative executor classification and non-executable FND-12 planning. Use `$ergon-rule-shadow-parity` for Phases 13-14 and `$ergon-rule-legacy-containment` only for an admitted Phase 17 after explicit promotion.

For corporate use, ensure this local skill is distributed/versioned as part of the migration kit. If the skill is not installed in the developer workstation, execute the same flow manually from the portable repo artifacts under `docs/migracao/rule-migration/`.

Before closing any phase, validate cross-artifact identity: screen/transaction, resource/API path, rule id, operation, environment, and relevant user/company fixtures must match across code, evidence, matrix, and artifact location. If code or logs say `screen=ERGadm00189`, do not close that rule under `docs/migracao/ERGadm00033/`; fix the artifact location or matrix first.

1. Read readiness V2 and prove that the active profile admits the exact requested stage/action in the current environment.
2. Identify the target screen, operation, and current Parte 2 phase.
3. Read `references/part-1-baseline-contract.md` and validate required Parte 1 inputs.
4. Create or update `rule-migration-intake.md`, `rule-canonical-decision-inventory.md`, and `rule-traceability-matrix.md`.
5. If baseline evidence is missing, use `references/return-to-part-1.md` and stop only the closeout/downstream transition that depends on it.
6. Route admitted work to the bounded skill:
   - Phase 10 structural source inventory and evidence-backed classification through `$ergon-rule-source-extraction`;
   - RF-03 decision proposals, total occurrence coverage and governed review queue through `$ergon-rule-decision-decomposition`;
   - executor responsibility through `$ergon-rule-executor-selection`;
   - FND-12 technical target planning/check/admission through `$ergon-rule-target-planning`;
   - dependency graph;
   - HADES read-only chain;
   - Phase 13-14 shadow contract/execution through `$ergon-rule-shadow-parity`;
   - preflight/promotion;
   - admitted Phase 17 containment through `$ergon-rule-legacy-containment`;
   - final handoff.
7. Close each phase with `phase-<PHASE-ID>-execution-gate.md`.

Phase 15 has planning/decision outcomes before runtime: `Preflight Candidate`, `Preflight Approved`, `Preflight Approved Candidate - planning only`, and `Preflight Deferred - runtime blocked`. `Preflight Approved` records the governance decision in `preflight-decision.md`; `Preflight Approved Candidate - planning only` means a runtime evidence plan and readiness review exist, but implementation still requires explicit approval; `Preflight Deferred - runtime blocked` is required when the boundary is understood but precedence, structured error, rollback, observability, HADES, or rollout evidence is missing. `Preflight Running` requires `preflight-results.md` evidence showing feature flag plus operational approval gate, rollback, DENY blocked before the baseline route, ALLOW still uses the approved baseline route, compatible structured error response, no-mutation, cleanup, and observability. Do not treat HTTP status alone as shadow/preflight equivalence; if code/message/fields cannot be extracted, classify the comparison as inconclusive.

Before implementing preflight runtime, create `preflight-runtime-evidence-plan.md` and `preflight-implementation-readiness.md`. The readiness gate must explicitly approve the technical implementation boundary; planning approval alone is not permission to write code. In `FACTORY_DEVELOPMENT`, this is an automated/focal technical gate and does not require human approval per run. Homologation or production preflight requires the additional admission of that profile. The runtime plan must require independent default-off technical controls, proof that DENY did not call the approved baseline executor/route, proof that ALLOW still uses the approved Parte 1 baseline route, v2/error-envelope parity, rollback, and observability. Oracle row counts alone are not sufficient proof that the approved baseline route was not called.

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
