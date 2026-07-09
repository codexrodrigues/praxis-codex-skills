# Parte 1 Baseline Contract

Parte 2 only starts for a screen/operation after Parte 1 - Migracao Funcional has an approved baseline handoff. Treat Parte 1 artifacts as contractual baseline, not background reading.

The baseline is usually DB-backed. It may also be `WRITE_TABLE_DIRECT_SAFE` when Parte 1 explicitly proves that direct table/platform persistence preserves required rules, errors, side effects, context, cleanup, and parity for the exact operation. `WRITE_TABLE_DIRECT_CANDIDATE` is not a valid Parte 2 baseline.

## Required Inputs

For each target screen/operation, validate these files or equivalent sections:

| Artifact | Required use in Parte 2 |
| --- | --- |
| `operation-inventory.md` | Visible operations, implemented/deferred/blocked states, operation scope. |
| `write-route-decision.md` | Current route safety state (`WRITE_DB_BACKED_REQUIRED` or `WRITE_TABLE_DIRECT_SAFE`), chosen/rejected routes, transaction findings, fallback route. |
| `write-risk.md` | Write risk, missing evidence, side effects, mutation hazards. |
| `table-rule-audit-*.md` or `oracle-results/table-rule-audit/*.summary.md` | Product packages, triggers, EPs, HADES activation, side effects, dependency summary. |
| `write-contract.md` | Command DTO, payload semantics, route use, operation-specific constraints. |
| `plsql-error-map.md` | Known legacy errors, REST mapping, field hints, no-mutation evidence. |
| `write-parity-matrix.md` | Success, negative, permission, duplicate, dependency, cleanup, read-after-write cases. |
| `parity-results.md` | Baseline comparison outcome and residual risk. |
| `pilot-handoff.md` or final handoff | Approved delivery state, deferrals, reusable decisions. |
| `ui-execution-gate.md` or UI handoff, when the rule is exposed by UI | Confirms the UI consumes canonical capabilities/actions/surfaces/config state and does not expose blocked/deferred/preflight behavior locally. |

## Intake Decision

Classify the Parte 2 intake as:

- `Ready for Rule Inventory`: all required baseline evidence exists for at least one eligible operation.
- `Ready with adjustments`: baseline is enough for a narrow rule slice; residuals are non-blocking and carried forward.
- `Blocked - Missing Parte 1 Evidence`: missing or contradictory evidence blocks rule migration.
- `Deferred`: rule migration intentionally postponed with explicit owner/reason.

## Baseline Guardrails

- Do not infer parity from implementation alone.
- Do not migrate a rule whose operation is still blocked/deferred in Parte 1.
- Do not promote Java when the Parte 1 baseline route is not understood.
- Do not start Parte 2 from `WRITE_TABLE_DIRECT_CANDIDATE`; return to Parte 1 Phase 4/5 until it becomes `WRITE_TABLE_DIRECT_SAFE`, `WRITE_DB_BACKED_REQUIRED`, `WRITE_BLOCKED`, or `WRITE_DEFERRED`.
- Do not treat object existence as HADES activation.
- Do not treat a rule as product-only until EP/HADES/client behavior is classified.
- Reopen Parte 1 when Parte 2 discovers a missing rule, side effect, payload, error, or parity case.
- Do not start from table names, labels, XML names, or source snippets alone; the rule must be tied to a screen/operation, Parte 1 artifact, approved baseline route, and parity evidence.
- Do not create a new rule API, metadata field, UI capability, or config contract until `rule-canonical-decision-inventory.md` states whether the need is already supported, partially supported, badly materialized, or a real contract gap.
- If UI, dashboard, workflow, or external consumers expose the operation, their gate must agree with the Parte 1 baseline state before rule migration can promote or preflight behavior.
