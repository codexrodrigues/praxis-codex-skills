# Status Taxonomy

Use separate statuses for rules and phases.

## Rule-Level Status

| Status | Meaning |
| --- | --- |
| `Discovered` | Rule or possible rule found but not classified. |
| `Classified` | Origin, type, dependencies, HADES/client, side effects, and fallback are initially classified. |
| `Blocked - Missing Parte 1 Evidence` | Parte 1 baseline lacks required evidence. Return to Parte 1. |
| `Blocked - Dependency Unknown` | Nested calls, tables, functions, HADES, client hook, or side effects are not understood. |
| `Keep DB-backed` | Rule should remain executed by the legacy route for now. |
| `Candidate` | Rule is suitable for a migration experiment. |
| `Shadow Contract Ready` | Inputs, outputs, fixtures, comparison, observability, and fallback are defined. |
| `Shadow Implemented` | Java shadow code is attached and unit-tested, but no live Oracle-backed comparison has been captured after the change. |
| `Shadow Running` | Java is executing in live runtime in parallel without deciding, while the approved Parte 1 baseline route remains authority. |
| `Shadow Passed` | Live shadow evidence is sufficient for the declared promotion boundary or preflight candidate, including DENY and ALLOW/control coverage, response comparison, state/side-effect comparison, and cleanup. |
| `Shadow Failed` | Java diverged from baseline in a blocking way. |
| `Shadow Inconclusive` | No blocking divergence, but sample/fixture coverage is insufficient. |
| `Preflight Candidate` | Phase 15 may analyze a DENY boundary, but runtime preflight is not approved yet. |
| `Preflight Approved` | Governance decision: Java may block selected proven cases before the legacy route in a future guarded run. No runtime preflight evidence yet. |
| `Preflight Approved Candidate - planning only` | Runtime evidence plan and implementation-readiness review are accepted, but no preflight code or runtime execution is approved yet. |
| `Preflight Deferred - runtime blocked` | Phase 15 was analyzed, but runtime preflight is explicitly blocked by missing precedence, structured error, rollback, observability, HADES, or other guardrail evidence. |
| `Preflight Running` | Runtime evidence: Java blocks approved cases under a feature flag; allowed cases still pass through the approved Parte 1 baseline route; rollback is proven. |
| `Authoritative Approved` | Java becomes decision authority for the exact promotion boundary. |
| `Contained Legacy` | Legacy rule is deactivated, bypassed, fallback-only, retained as defense, or deliberately duplicated with proof. |
| `Rejected` | Rule should not be migrated under the current strategy. |
| `Deferred` | Rule migration postponed with explicit reason and reentry condition. |

## Phase-Level Status

Use the same mental model as Parte 1 phase gates:

- `Open`: still being investigated.
- `Blocked`: missing evidence or contradiction prevents safe advancement.
- `Ready for next phase`: required artifacts and evidence are present.
- `Ready for next phase with adjustments`: required scope works, non-blocking residuals are named and carried forward.
- `Deferred`: intentionally postponed with explicit risk and owner.

Do not use rule-level statuses as phase closeout. Every phase needs its own gate file.
