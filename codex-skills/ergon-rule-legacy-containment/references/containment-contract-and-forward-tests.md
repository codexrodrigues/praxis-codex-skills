# Containment Contract and Forward Tests

Use the active repository's `phase-gates.md`, `artifact-contract.md`,
`customer-rule-customization-model.md`, `rule-execution-model.md` and Phase 16
decision as authority.

## Forward Tests

- A technically admitted target with no promotion decision cannot open Phase
  17 and produces no legacy change.
- A promoted atomic validation may keep a trigger as defense until duplicate
  execution and error precedence are proved safe.
- A trigger combining validation and mutation must be decomposed; never disable
  it as one opaque unit.
- Unknown customer EP/HADES behavior keeps the path retained or marks it not
  containable.
- A proposed bypass that weakens security, integrity, audit or legal behavior
  is rejected even when rollback exists.
- Containment passes only with target-environment evidence, no duplicate
  effects, verified rollback and an updated traceability matrix.
