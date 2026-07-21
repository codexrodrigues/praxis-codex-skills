---
name: ergon-rule-shadow-parity
description: Design and assess Ergon rule shadow contracts and parity evidence for Parte 2 Phases 13-14. Use when Codex must define an exact decision boundary, fixtures, baseline normalization, mismatch taxonomy, redacted observations, no-effect execution, fallback and phase evidence, or decide whether shadow is implemented, running, passed or inconclusive without changing user-visible results, skipping the approved baseline route or promoting authority.
---

# Ergon Rule Shadow Parity

Govern comparison, not authority. Use `$ergon-rule-migration-orchestration` for
phase admission and `$ergon-rule-target-planning` for the technical target.

## Step Zero: Readiness

Read `docs/migracao/rule-migration/factory-contracts/part2-foundation-readiness-v2.json`
before opening Phase 13 or 14. Require the active profile to
admit the exact shadow stage and action in the current environment. Development
shadow evidence never crosses automatically into homologation or production.

## Required Inputs

- exact screen, operation, decision and environment identity;
- approved Parte 1 baseline route and stable parity fixtures;
- admitted technical target plan with unresolved gaps visible;
- known decision order, HADES/client behavior and side effects;
- normalized input, output, error-envelope and observation contracts;
- fallback, disable control, cleanup and redaction policy.

Read `references/shadow-contract-and-forward-tests.md` before drafting or
reviewing shadow artifacts.

## Workflow

1. Define the atomic decision boundary and what remains DB-backed.
2. Separate `productDecision` from `legacyEffectiveDecision` when EP/HADES or
   composition can suppress, replace or reorder product behavior.
3. Define positive, negative, control and boundary fixtures with stable
   timestamps/timezones and explicit null semantics.
4. Normalize decision, code/message/fields, ordering, state, effects and
   baseline availability. HTTP status or no-mutation alone is insufficient.
5. Ensure shadow cannot decide, mutate, suppress errors, skip the baseline
   route or execute external effects.
6. Record redacted observations and classify every divergence or inconclusive
   comparison.
7. Update `shadow-contract.md`, `shadow-results.md`, the traceability matrix and
   the corresponding phase gate.

## Status Discipline

- `Shadow Implemented`: code is attached and focal tests pass; no live claim.
- `Shadow Running`: live evidence is being collected with baseline authority.
- `Shadow Passed`: declared coverage is sufficient for considering Phase 15.
- Missing control/ALLOW evidence, baseline unavailability, unknown order or
  lossy normalization is inconclusive, never passed.

Shadow success does not authorize preflight, promotion or containment.
