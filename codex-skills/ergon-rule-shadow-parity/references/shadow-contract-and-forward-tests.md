# Shadow Contract and Forward Tests

Use canonical `artifact-contract.md`, `phase-gates.md`, `templates.md`,
`rule-execution-model.md` and `rule-runtime-adr.md` from the active migration
repository.

## Required Proof

- baseline route remains the only authority;
- shadow output and observations are deterministic and redacted;
- zero Java effects and no baseline suppression;
- DENY, ALLOW/control, null and boundary fixtures;
- normalized error marker/code/message/fields and side-effect comparison;
- explicit fallback, disable control and cleanup;
- all divergences classified, including `BASELINE_UNAVAILABLE`.

## Forward Tests

- Unit-only evidence may reach `Shadow Implemented`, never `Shadow Passed`.
- A matching HTTP status with different code/fields is a mismatch or
  inconclusive result, not parity.
- A Java DENY that prevents the baseline call violates shadow mode.
- HADES absent in development does not prove parity for another environment.
- A baseline timeout is recorded separately and never converted to Java ALLOW.
