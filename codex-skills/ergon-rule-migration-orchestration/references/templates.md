# Parte 2 Templates

Copy these templates into `docs/migracao/<SCREEN>/rule-migration/` and fill them for the current screen/operation.

## `rule-migration-intake.md`

```markdown
# <SCREEN> Rule Migration Intake

## Scope

| Item | Value |
| --- | --- |
| Screen |  |
| Operations in scope |  |
| Operations excluded |  |
| Parte 1 handoff package |  |
| Intake decision | Open |

## Parte 1 Baseline Checklist

| Artifact | Status | Link | Notes |
| --- | --- | --- | --- |
| operation-inventory.md |  |  |  |
| write-route-decision.md |  |  |  |
| write-risk.md |  |  |  |
| table-rule-audit-*.md |  |  |  |
| write-contract.md |  |  |  |
| plsql-error-map.md |  |  |  |
| write-parity-matrix.md |  |  |  |
| parity-results.md |  |  |  |
| pilot-handoff.md |  |  |  |

## Eligible Operations

| Operation | Parte 1 state | Baseline | Decision |
| --- | --- | --- | --- |

## Blocking Gaps

| Gap | Impact | Return to Parte 1 | Owner/Next action |
| --- | --- | --- | --- |

## Decision

State one of: `Ready for Rule Inventory`, `Ready with adjustments`, `Blocked - Missing Parte 1 Evidence`, `Deferred`.
```

## `preflight-runtime-evidence-plan.md`

```markdown
# <SCREEN> Preflight Runtime Evidence Plan

## Status

State one of: `Open`, `Reviewed - planning accepted`, `Blocked`, or `Deferred`.

This artifact is a plan. It does not approve implementation and is not runtime evidence.

## Exact Boundary

| Item | Value |
| --- | --- |
| Rule |  |
| Operation/API path |  |
| DENY fixture |  |
| ALLOW/control fixture |  |
| Environment |  |
| Target company/tenant |  |

## Gates

| Gate | Default | Required proof |
| --- | --- | --- |
| Feature flag | false in local/CI/homolog/prod unless explicitly overridden | Flag off uses the approved Parte 1 baseline route. |
| Operational approval | false independently from feature flag | Feature flag alone cannot block before the approved baseline route. |
| Target environment allowlist/gate id, if used | closed | Target environment is explicit and auditable. |

## Runtime Proofs Required

| Proof | Required evidence |
| --- | --- |
| DENY blocked before baseline route | Direct proof the approved baseline executor/route was not called; row counts alone are insufficient. |
| ALLOW still baseline route | Executor/route called, API succeeds, readback/cleanup proves persistence path. |
| Error envelope parity | Preflight error uses accepted status, code, legacyCode/message marker, fields, ruleId, category, and correlation/request id behavior. |
| Observability | `ergon_rule_preflight` event with ruleId, screen, operation, user/company/tenant, target environment, request/correlation id, HTTP status, service status, decision, featureFlagState, operationalApprovalState, flagVersion, comparison. |
| Rollback | Controlled smoke rollback procedure; if restart/redeploy is required, state that corporate rollout remains blocked without separate operational acceptance. |

## Expected `preflight-results.md`

List files, logs, API captures, SQL/counts, tests, and cleanup outputs expected from the runtime run.

## Decision

State whether this plan is ready for implementation-readiness review.
```

## `preflight-implementation-readiness.md`

```markdown
# <SCREEN> Preflight Implementation Readiness

## Decision

State one of:

- `Reviewed - planning gate accepted; implementation still requires explicit approval`
- `Implementation approved for controlled smoke`
- `Blocked`
- `Deferred`

## Scope Reviewed

| Item | Value |
| --- | --- |
| Rule |  |
| Boundary |  |
| Evidence plan | `preflight-runtime-evidence-plan.md` |

## Readiness Checks

| Check | Result | Notes |
| --- | --- | --- |
| Boundary exact and fixture-scoped |  |  |
| Feature flag and operational approval independent/default-off |  |  |
| DENY no-DB proof defined beyond row counts |  |  |
| ALLOW baseline route proof defined |  |  |
| Envelope parity defined |  |  |
| Observability event contract defined |  |  |
| Rollback accepted for controlled smoke |  |  |
| Corporate rollout explicitly blocked |  |  |

## Decision

State whether code implementation may start. If implementation is not explicitly approved here, do not write preflight code.
```

## `rule-traceability-matrix.md`

```markdown
# <SCREEN> Rule Traceability Matrix

| Rule | Legacy origin | Operation | Parte 1 artifact | Dependencies | HADES/EP/client | Side effects | Mode | Promotion boundary | Still DB-backed | Double-execution risk | Observability | Fallback | Return to Parte 1 | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

## `phase-<PHASE-ID>-execution-gate.md`

```markdown
# <SCREEN> Parte 2 Phase <PHASE-ID> Execution Gate

## Decision

State one of: `Open`, `Blocked`, `Ready for next phase`, `Ready for next phase with adjustments`, `Deferred`.

## Scope

| Item | Value |
| --- | --- |
| Screen |  |
| Operation(s) |  |
| Rule(s) |  |

## Evidence Executed

| Evidence | Result | Link |
| --- | --- | --- |

## Artifacts Updated

| Artifact | Status | Link |
| --- | --- | --- |

## Rule Status Changes

| Rule | Previous | Current | Reason |
| --- | --- | --- | --- |

## Residual Issues

| Issue | Blocks? | Owner | Next action |
| --- | --- | --- | --- |

## Return To Parte 1

| Trigger | Parte 1 phase | Action |
| --- | --- | --- |

## Next Recommended Step

Name the next phase and skill.
```

## `hades-rule-chain.md`

```markdown
# <SCREEN> HADES Read-Only Rule Chain

## Status

This artifact is read-only evidence. It does not execute Java, does not call HADES from Java to decide, and does not authorize shadow by itself.

## Execution Evidence

| Item | Value |
| --- | --- |
| SQL | `hades-rule-chain.sql` |
| Output | `hades-rule-chain.out.txt` |
| Execution path | SQLcl, or JDBC fallback if SQLcl fails with Windows console error |
| Scope |  |
| Decision |  |

## HADES Parent Rows

| Routine | `HAD_CAD_SPROC` row | `EXEC` | `EXEC_MULT_EPS` | `SINTAXE` | Classification |
| --- | --- | --- | --- | --- | --- |

## HADES Multiple-EP Children

| Routine | Child rows | Active children | Order evidence | Classification |
| --- | ---: | ---: | --- | --- |

## C_ERGON / ERGON Objects

Record whether matching routines exist in `C_ERGON` or `ERGON`. Object existence is secondary evidence and never proves activation by itself.

## Effective Classification

Use these labels consistently: `NO_PARENT_ROW`, `NOT_CONFIGURED`, `NO_CHAIN`, `ACTIVE_SINGLE`, `EXECUTES_SINGLE`, `MULTI_EP_PARENT`, `EXECUTES_MULTIPLE`, `MULTI_EP_WITHOUT_ACTIVE_CHILD`, `DOES_NOT_EXECUTE`, `BLOCKED_ACTIVE_WITHOUT_SYNTAX`.

| Routine | Parent class | Child rows | Active children | Effective class |
| --- | --- | ---: | ---: | --- |

## Rule Impact

| Rule | HADES impact | Phase decision |
| --- | --- | --- |

## Notes

- Do not treat object existence as activation.
- Do not execute Java from DB in this phase.
- Separate package EPs from trigger EPs.
- Absence of HADES configuration is environment-specific. Revalidate target-environment HADES before corporate rollout or promotion.
```

## `shadow-contract.md`

```markdown
# <SCREEN> Shadow Contract

## Status

| Item | Value |
| --- | --- |
| Phase | `13 - Shadow Contract` |
| Rule |  |
| Operation |  |
| Contract status | Open |
| Runtime authority | Approved Parte 1 baseline route |
| Java implementation allowed by this artifact | Only shadow calculation in Phase 14; no decision authority |

## Rule Boundary

| Item | Boundary |
| --- | --- |
| Java rule id |  |
| Business question |  |
| Allowed operation |  |
| Allowed decision shape | `ALLOW`, `DENY`, or `INCONCLUSIVE` for shadow comparison only |
| Approved DENY fixture |  |
| Out of scope |  |

## Legacy Origin

| Origin | Evidence |
| --- | --- |

## Inputs

| Input | Source | Required for shadow | Notes |
| --- | --- | --- | --- |

## Fixtures

| Fixture | Payload / context | Expected legacy result | State proof | Evidence |
| --- | --- | --- | --- | --- |

## Expected Java Shadow Output

| Case | Java shadow decision | Required fields |
| --- | --- | --- |

## Comparison Contract

| Aspect | Required comparison |
| --- | --- |
| Decision | Compare Java `ALLOW`/`DENY`/`INCONCLUSIVE` with approved Parte 1 baseline result. |
| Message/code | Compare stable legacy marker, API status, structured code when available, and accepted deviations. |
| Fields | Compare field hints or explicitly record operation-level error. |
| State | Compare mutation/no-mutation and readback evidence. |
| Side effects | Compare audit/pending/publication/other side effects or mark out of scope. |
| Cleanup | Define cleanup and final count proof. |

## Observability

| Event | Required fields |
| --- | --- |
| `rule-shadow-evaluation` | `mode`, `ruleId`, screen, operation, decision, reasonCode, relevant inputs, request/correlation id, comparisonStatus |

## Fallback

| Condition | Fallback |
| --- | --- |
| Shadow disabled | Approved Parte 1 baseline route only. |
| Missing context | Shadow returns `INCONCLUSIVE`; approved Parte 1 baseline route decides. |
| Divergence | Mark `Shadow Failed`; keep approved baseline route; do not proceed to preflight. |
| Missing observability/correlation | Mark `Shadow Inconclusive`. |

## Still Baseline Route

List the behavior that remains owned by the legacy route.

## Promotion Boundary

State `None` unless a later Phase 16 explicitly approves authority.

## Double-Execution Risk

| Risk | Classification | Notes |
| --- | --- | --- |

## Phase 14 Entry Criteria

- where the shadow evaluator will run;
- proof it cannot block, mutate, or skip the approved Parte 1 baseline route;
- feature/config guard if needed;
- event/log fields;
- selected DENY and ALLOW/control fixtures;
- return-to-Parte-1 triggers for missing evidence.
```

## `shadow-results.md`

```markdown
# <SCREEN> Shadow Results

## Status

State one of: `Shadow Implemented`, `Shadow Running`, `Shadow Passed`, `Shadow Failed`, or `Shadow Inconclusive`.

Use `Shadow Implemented` when Java code is attached and unit-tested but no live Oracle-backed comparison has been captured. Do not use it to open Phase 15.

## Implementation Evidence

| Item | Evidence |
| --- | --- |
| Java evaluator |  |
| Integration point |  |
| Proof it cannot decide/mutate/skip baseline route |  |
| Focused tests |  |

## Runtime Evidence

| Case | Java decision | Baseline result | Response comparison | State/side effects | Cleanup | Status |
| --- | --- | --- | --- | --- | --- | --- |
| DENY fixture |  |  |  |  |  |  |
| ALLOW/control fixture |  |  |  |  |  |  |

## Observability

| Event/log | Required fields | Evidence |
| --- | --- | --- |
| shadow evaluation | mode, rule id, screen, operation, decision, reason, relevant inputs, legacy status/code/message marker, comparison, request/correlation id when available |  |

## Limits And Divergences

| Limit or divergence | Impact | Required next action |
| --- | --- | --- |

## Decision

State whether the rule remains `Shadow Implemented`, moves to `Shadow Running`, reaches `Shadow Passed`, becomes `Shadow Failed`, or is `Shadow Inconclusive`. Phase 15 can only be considered after live evidence is sufficient for the declared boundary.
```

## `preflight-decision.md`

```markdown
# <SCREEN> Preflight Decision

## Status

State one of: `Preflight Candidate`, `Preflight Approved`, `Preflight Deferred - runtime blocked`, `Preflight Failed`, or `Preflight Inconclusive`.

This artifact is a decision/gate artifact. It is not runtime evidence and does not authorize promotion or legacy containment.

## Identity Check

| Item | Value | Evidence |
| --- | --- | --- |
| Screen/transaction |  |  |
| Resource/API path |  |  |
| Rule id |  |  |
| Operation |  |  |
| Environment |  |  |
| User/company fixtures |  |  |

If any identity differs between code, logs, matrix, and artifact path, stop and fix the artifact location or matrix before deciding preflight.

## Conceptual Boundary

| Item | Value |
| --- | --- |
| DENY condition Java might block |  |
| ALLOW behavior | Must remain on the approved Parte 1 baseline route unless Phase 16 later promotes authority |
| Still baseline route |  |
| Out of scope |  |

## Runtime Blockers

| Blocker | Status | Evidence | Decision |
| --- | --- | --- | --- |
| Create/update/delete error precedence |  | `create-preflight-precedence-plan.md` or equivalent |  |
| Structured error envelope |  | `structured-error-envelope-decision.md` or Parte 1 contract |  |
| Feature flag default off |  |  |  |
| Operational approval gate |  |  |  |
| Rollback model |  |  |  |
| Observability/event contract |  |  |  |
| Target-environment HADES |  |  |  |
| Non-smoke evidence for rollout |  |  |  |

## Decision

Choose one:

- `Preflight Candidate`: boundary can be analyzed, but not yet approved.
- `Preflight Approved`: guarded runtime can be implemented for the exact boundary.
- `Preflight Deferred - runtime blocked`: conceptual boundary may be valid, but runtime execution is blocked by listed evidence gaps.

## Next Step

State whether to return to Parte 1 Phase 4/5/7/8, collect runtime evidence, or keep the approved baseline route.
```

## `create-preflight-precedence-plan.md`

```markdown
# <SCREEN> Create Preflight Precedence Plan

## Purpose

Prove whether Java may block before the approved Parte 1 baseline route without changing which baseline error wins.

## Scope

| Item | Value |
| --- | --- |
| Rule |  |
| Operation | create |
| Candidate DENY |  |
| User/company/transaction fixture |  |
| Payload boundary |  |

## Precedence Cases

| Conflict case | Fixture | Expected baseline winner | API/Oracle evidence | Java preflight decision | Safe to block before baseline route? |
| --- | --- | --- | --- | --- | --- |
| permission/security + duplicate |  |  |  |  |  |
| permission/security + required field missing |  |  |  |  |  |
| permission/security + type/code missing |  |  |  |  |  |
| permission/security + invalid quantity/format |  |  |  |  |  |
| permission/security + invalid period/vinculo |  |  |  |  |  |
| permission/security + scoped validation error |  |  |  |  |  |

## Decision

State one of:

- `Precedence proves preflight safe for exact boundary`.
- `Precedence blocks runtime preflight`.
- `Inconclusive - return to Parte 1 Phase 7`.
```

## `structured-error-envelope-decision.md`

```markdown
# <SCREEN> Structured Error Envelope Decision

## Scope

| Item | Value |
| --- | --- |
| Rule |  |
| Operation |  |
| Legacy marker |  |
| API status |  |

## Envelope Fields

| Field | Expected | Actual | Decision |
| --- | --- | --- | --- |
| `status` |  |  |  |
| `code` |  |  |  |
| `legacyCode` |  |  |  |
| `fields` |  |  |  |
| `ruleId` |  |  |  |
| `message` | Preserve legacy, normalize, or accepted deviation |  |  |
| `correlationId/requestId` |  |  |  |

## Decision

State one of:

- `Envelope accepted as-is`.
- `Envelope accepted with formal deviation`.
- `Return to Parte 1 Phase 5 to change write/error contract`.
- `Blocked - envelope unknown`.
```

## `preflight-results.md`

```markdown
# <SCREEN> Preflight Results

## Status

State whether this is `Preflight Running`, `Preflight Failed`, or `Preflight Inconclusive`.

This artifact is runtime evidence. It is not a promotion decision and does not authorize legacy containment.

## Scope

| Item | Value |
| --- | --- |
| Rule |  |
| Java rule id |  |
| Approved boundary |  |
| Operations |  |
| Feature flag |  |
| Operational approval gate |  |
| Runtime authority for ALLOW | Approved Parte 1 baseline route |

## Flag And Rollback

| Check | Expected | Result | Evidence |
| --- | --- | --- | --- |
| Flag off | All cases call the approved Parte 1 baseline route |  |  |
| Operational approval off | Feature flag alone does not block before the approved baseline route |  |  |
| Flag on | Approved DENY blocks before the approved baseline route |  |  |
| Rollback | Disabling flag restores the approved Parte 1 baseline route |  |  |

## Runtime Cases

| Case | Flag | Payload condition | Java decision | Baseline route called? | API status/code | State proof | Comparison |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DENY preflight | on |  | block before baseline route | no |  | no mutation |  |
| ALLOW still baseline route | on |  | allow | yes |  | read-after-write/cleanup |  |
| Flag-off baseline | off | same DENY payload | baseline route decides | yes |  | no mutation |  |
| Update precedence, if update preflight is proposed | on | missing row, permission/security denial, dependency conflict, scoped validation | preserve legacy precedence | case-specific |  | no unexpected mutation |  |

## Observability

| Event | Required fields | Evidence |
| --- | --- | --- |
| preflight block | mode, rule id, operation, decision, code, fields, target environment, user/company or tenant when available, request/correlation id when available, featureFlagState, operationalApprovalState, flagVersion |  |
| allowed baseline route | mode/flag evidence or request trace |  |
| rollback | flag state and baseline-route evidence |  |

## Corporate Rollout Blockers

Controlled smoke is not corporate rollout. Close or explicitly defer each blocker before rollout or promotion.

| Blocker | Current state | Required before rollout |
| --- | --- | --- |
| Target-environment HADES |  | Re-run Phase 12 against the target environment and prove active client/product EP behavior does not change the approved boundary. |
| Rollback model |  | Dynamic/auditable flag is preferred; if rollback requires restart/redeploy, record formal acceptance and operating procedure. |
| Structured error envelope |  | Prove status, code/message marker, fields, ruleId/correlation behavior, and accepted deviations. |
| Observability |  | Prove event contract, status interpretation, request/correlation id, user/company or tenant when available, and flag/approval states. |
| Non-smoke evidence |  | Record monitored runtime evidence beyond disposable smoke fixtures, or keep corporate rollout blocked. |

## Cleanup

Link final-count SQL/output or equivalent proof.

## Decision

State whether the rule moves to `Preflight Running`, remains `Preflight Approved`, becomes `Preflight Deferred - runtime blocked`, becomes `Preflight Failed`, or is `Deferred`.
```
