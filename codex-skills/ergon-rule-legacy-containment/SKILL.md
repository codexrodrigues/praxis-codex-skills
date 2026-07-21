---
name: ergon-rule-legacy-containment
description: Govern Ergon legacy-rule containment for Parte 2 Phase 17 after an explicit Phase 16 authority decision. Use when Codex must decide and evidence whether each legacy package, trigger, constraint, HADES/EP path or side effect is retained as defense, bypassed, deactivated, fallback-only, deliberately duplicated or not containable, with rollback and double-execution controls, without disabling legacy behavior from a draft, shadow or preflight state.
---

# Ergon Rule Legacy Containment

Contain only an explicitly promoted boundary. Planning may identify risks
earlier, but it must remain a draft and cannot open Phase 17.

## Step Zero: Readiness and Promotion

Read `docs/migracao/rule-migration/factory-contracts/part2-foundation-readiness-v2.json`
first. Require the active target-environment profile to admit
`PHASE_17_LEGACY_CONTAINMENT` and the necessary action. Then verify an explicit
Phase 16 promotion decision for the exact decision, operation, environment and
evidence revision. Without both, stop before any database/configuration change.

## Required Inputs

- promotion boundary and authority revision;
- complete trigger/package/HADES/EP/client execution path;
- side effects, persistence and double-execution analysis;
- current fallback, rollback, observability and incident procedures;
- owner and executable evidence for every proposed legacy change;
- target-environment revalidation and sanitized before-state evidence.

Read `references/containment-contract-and-forward-tests.md` before drafting or
executing containment.

## Workflow

1. Enumerate every legacy origin that can still affect the promoted boundary.
2. Assign an evidence-backed treatment: retained defense, bypassed,
   deactivated, fallback-only, deliberately duplicated or not containable.
3. Prove that protected security, authorization, integrity, audit and legal
   controls are not weakened. Customer restrictions may become stricter, never
   silently broader.
4. Prove no duplicate mutation/effect and document residual DB-backed behavior.
5. Define atomic cutover, rollback trigger, restoration procedure,
   observability and post-change verification.
6. Execute only through the approved owner/route and record sanitized before,
   action, after and rollback evidence.
7. Update `legacy-containment.md`, the traceability matrix and
   `phase-17-execution-gate.md`.

## Hard Stops

Shadow, preflight, target admission, business intent or code completion never
authorizes containment. Do not use `BYPASS_ALL`, do not disable a whole product
composition to customize one atomic decision, and do not remove a legacy
fallback before rollback is operable. Unknown client/HADES behavior or side
effects keeps the affected origin retained or not containable.
