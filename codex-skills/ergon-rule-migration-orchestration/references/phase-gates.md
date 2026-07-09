# Parte 2 Phase Gates

Use these gates to decide whether a phase can advance. A plan is not closeout evidence.

## Cross-Artifact Identity Gate

Every phase must validate that the same identity appears in code, artifacts, evidence, and matrix:

- screen/transaction;
- resource/API path;
- rule id;
- operation;
- environment and tenant/company/user fixture when relevant.

If Java code reports `screen=ERGadm00189`, do not evaluate or close that rule from `docs/migracao/ERGadm00033/`. A screen/resource/rule mismatch blocks phase closeout until the artifact location or matrix row is corrected.

## Phase 9 - Rule Migration Intake

Required outputs:

- `rule-migration-intake.md`
- initial `rule-traceability-matrix.md`
- `phase-9-execution-gate.md`

Close only when:

- Parte 1 baseline artifacts are present or missing gaps are explicitly mapped to Parte 1;
- eligible and excluded operations are listed;
- approved baseline route (`WRITE_DB_BACKED_REQUIRED` or `WRITE_TABLE_DIRECT_SAFE`) and parity baseline are linked;
- intake decision is recorded.

## Phase 10 - Rule Inventory

Required outputs:

- `rule-inventory.md`
- updated `rule-traceability-matrix.md`
- `phase-10-execution-gate.md`

Close only when:

- rules are extracted from Parte 1 audits/source;
- each rule has legacy origin and operation;
- product/client/security/side-effect classification is recorded;
- initial keep/candidate/defer/reject decision exists.

## Phase 11 - Rule Dependency Graph

Required outputs:

- `rule-dependency-graph.md`
- updated `rule-traceability-matrix.md`
- `phase-11-execution-gate.md`

Close only when:

- nested package/function/table/HADES/side-effect dependencies are mapped;
- unknown dependencies are blocking or deferred explicitly;
- high-risk rules are marked `Keep DB-backed`, `Deferred`, or `Blocked - Dependency Unknown`.

## Phase 12 - HADES Read-Only Chain

Required outputs:

- `hades-rule-chain.sql`
- `hades-rule-chain.out.txt`
- `hades-rule-chain.md`
- updated `rule-traceability-matrix.md`
- `phase-12-execution-gate.md`

Close only when:

- `HAD_CAD_SPROC` and `HAD_CAD_MULT_EPS` activation/order are classified for relevant routines;
- EP package and trigger semantics are separated;
- Java does not execute HADES from DB in this phase;
- object existence is not treated as activation.

Execution notes:

- Use the Parte 1 Oracle access contract. Prefer SQLcl when it works; if SQLcl fails with the known Windows console error, rerun the same read-only SQL through the JDBC fallback and record the execution path.
- Keep the SQL and output with the screen package. The `.md` summary must link to both.
- Use these HADES classifications consistently: `NO_PARENT_ROW`, `NOT_CONFIGURED`, `NO_CHAIN`, `ACTIVE_SINGLE`, `EXECUTES_SINGLE`, `MULTI_EP_PARENT`, `EXECUTES_MULTIPLE`, `MULTI_EP_WITHOUT_ACTIVE_CHILD`, `DOES_NOT_EXECUTE`, `BLOCKED_ACTIVE_WITHOUT_SYNTAX`.
- Absence of HADES configuration is environment-specific evidence. It can unblock controlled smoke in that environment, but target-environment HADES must be revalidated before corporate rollout or promotion.

## Phase 13 - Shadow Contract

Required outputs:

- `shadow-contract.md`
- updated `rule-traceability-matrix.md`
- `phase-13-execution-gate.md`

Close only when:

- Java rule boundary is exact;
- fixtures and comparison cases are defined;
- observability and fallback are defined;
- promotion boundary, still-DB-backed behavior, and double-execution risk are recorded.

## Phase 14 - Shadow Execution

Phase 14 has layered rule statuses:

- `Shadow Implemented`: Java shadow code is attached, cannot decide, cannot mutate, cannot skip the approved Parte 1 baseline route, and focused tests pass.
- `Shadow Running`: live runtime is emitting shadow evidence while the approved Parte 1 baseline route remains authority.
- `Shadow Passed`: live evidence covers the declared boundary and is sufficient to consider Phase 15.

Required outputs:

- `shadow-results.md`
- updated `rule-traceability-matrix.md`
- `phase-14-execution-gate.md`

Close only when:

- Java ran in live runtime without deciding;
- approved Parte 1 baseline route still decided;
- results compare Java decision, legacy result, normalized marker/code/message/fields, state, side effects, and cleanup;
- DENY and ALLOW/control fixtures are covered;
- divergences are classified as pass/fail/inconclusive.

Unit tests or compile-only evidence may update a rule to `Shadow Implemented`, but must not close Phase 14 or open Phase 15. Missing ALLOW/control evidence must close as `Shadow Inconclusive` or keep the phase blocked, never as `Shadow Passed`.

## Phase 15 - Preflight Decision + Runtime Evidence

Required outputs:

- `preflight-decision.md`
- `create-preflight-precedence-plan.md` for any create preflight that would block before the approved Parte 1 baseline route and could mask legacy errors
- `structured-error-envelope-decision.md` when the API error envelope is not already fully proven by Parte 1
- `preflight-runtime-evidence-plan.md` when runtime preflight is being planned but not yet implemented
- `preflight-implementation-readiness.md` before any preflight implementation work begins
- `preflight-results.md` when runtime preflight is executed or required before Phase 16
- updated `rule-traceability-matrix.md`
- `phase-15-execution-gate.md`

Close only when:

- only proven cases may be blocked by Java;
- allowed cases still call the approved Parte 1 baseline route unless promotion is separately approved;
- decision is classified as `Preflight Candidate`, `Preflight Approved`, `Preflight Approved Candidate - planning only`, `Preflight Deferred - runtime blocked`, `Preflight Running`, `Preflight Failed`, or `Preflight Inconclusive`;
- runtime blockers are separated from conceptual approval;
- create/update/delete precedence risks are explicitly covered before any Java block-before-DB behavior;
- structured error envelope decision is linked or explicitly returned to Parte 1 Phase 5;
- fallback/feature flag/rollback path is clear;
- residual DB-backed coverage is explicit.

Important:

- `Preflight Approved` is not `Preflight Running`.
- `Preflight Approved Candidate - planning only` is not implementation approval and is not runtime evidence.
- `Preflight Deferred - runtime blocked` is the expected status when Phase 15 can reason about a boundary but cannot safely execute runtime preflight yet.
- Do not implement runtime preflight until `preflight-implementation-readiness.md` explicitly says implementation is approved.
- Do not treat Phase 15 decision closeout as runtime evidence. It only approves or defers the precise DENY boundary that may be implemented later under guardrails.
- Before Phase 16, create `preflight-results.md` from a controlled run, or keep promotion blocked/deferred.
- Corporate rollout is still blocked until target-environment HADES is revalidated, rollback is operationally acceptable, structured API error behavior is closed, observability status interpretation is closed, and non-smoke observation evidence exists.
- No preflight rule may block before the approved Parte 1 baseline route if it can mask a higher-priority legacy error. For create, cover at minimum permission/security plus duplicate, missing required fields, missing type/code, invalid quantity/format, invalid period/vinculo, and the scoped validation error. If precedence is not proven, keep runtime preflight blocked.

## Preflight Runtime Evidence - Preflight Running

Output:

- `preflight-results.md`
- updated `rule-traceability-matrix.md`

Close only when:

- feature flag off proves all cases still use the approved Parte 1 baseline route;
- runtime preflight requires both the feature flag and an explicit operational approval gate, or an equivalent dynamic/auditable provider that fails closed;
- feature flag on plus approved DENY proves Java blocks before the legacy route, including direct proof that `ErgonLegacyExecutor` or the scoped legacy routine was not called;
- feature flag on plus ALLOW proves the request still calls the approved Parte 1 baseline route;
- preflight error response matches the legacy/API contract, including status, code/message marker, fields, and structured envelope when the API exposes one;
- log/event records mode `preflight`, rule id, operation, decision, code, fields, target environment, user/company or tenant when available, request/correlation id when available, featureFlagState, operationalApprovalState, flagVersion, and comparison status;
- DENY path has no-mutation evidence;
- DENY no-mutation evidence must be paired with executor/route non-call evidence; row counts alone are not sufficient;
- cleanup final count is recorded;
- rollback is proven by disabling the flag.

For update preflight, prove baseline error precedence before blocking before the approved baseline route. At minimum cover missing row, permission/security denial, dependency conflict, and the scoped validation error. If precedence is not proven, keep update on the approved baseline route/shadow even if create preflight is allowed.

This evidence can be recorded as a continuation of Phase 15 before any Phase 16 promotion decision. Do not create a new canonical phase number for it unless the package later splits preflight implementation into its own skill/phase.

## Phase 16 - Promotion Decision

Required outputs:

- `promotion-decision.md`
- updated `rule-traceability-matrix.md`
- `phase-16-execution-gate.md`

Close only when:

- Java authority is limited to an exact promotion boundary;
- controlled preflight runtime evidence exists in `preflight-results.md`, or promotion is explicitly blocked/deferred;
- shadow/preflight comparisons do not treat status alone as equivalence; when code/message/fields cannot be extracted, classify as `Inconclusive`;
- double-execution risk is absent, accepted with proof, or blocking;
- side effects and client/HADES behavior are covered, retained, or formally out of scope;
- rollback and observability are ready.

## Phase 17 - Legacy Rule Containment

Required outputs:

- `legacy-containment.md`
- updated `rule-traceability-matrix.md`
- `phase-17-execution-gate.md`

Close only when:

- each promoted rule has a legacy treatment: retained defense, bypassed, deactivated, fallback-only, duplicated intentionally, or not containable;
- any DB change has owner/approval/evidence;
- no unproven duplicate side effects remain.

## Phase 18 - Final Rule Handoff

Required outputs:

- `final-rule-handoff.md`
- final `rule-traceability-matrix.md`
- `phase-18-execution-gate.md`

Close only when:

- every rule in scope has final status;
- authoritative/preflight/shadow/DB-backed/rejected/deferred rules are summarized;
- residual risks and reentry triggers are explicit;
- downstream teams know what Java decides and what the legacy route still owns.
