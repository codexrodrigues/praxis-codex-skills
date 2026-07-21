# FND-12 Contract and Forward Tests

Load this reference before producing or reviewing a target plan.

## Canonical Artifacts

- `factory-contracts/part2-foundation-readiness-v2.json`;
- `factory-contracts/rule-target-binding-plan-v1.schema.json`;
- `factory-contracts/rule-target-binding-plan-check-result-v1.schema.json`;
- `factory-contracts/rule-target-binding-plan-admission-receipt-v1.schema.json`;
- `part2-foundation-fnd12-target-binding-plan-draft1.md`;
- `semantic-quality-gate.md` and `rule-migration-factory-rfc.md`;
- `tools/migration-factory/check-rule-target-binding-plan.ps1`;
- `tools/migration-factory/admit-rule-target-binding-plan.ps1`;
- `tools/migration-factory/test-rule-target-binding-plan.ps1`.

Repository-local contracts and commands are authoritative. Stop on drift.

## Forward Tests

### Admitted technical draft

Given `FACTORY_DEVELOPMENT`, complete lineage and an evidence-backed selection,
produce one unchecked plan, a separate verified result and, when requested, a
technical admission receipt. Emit zero executable payloads and Config writes.

### Unknown executor

Given a valid decision whose executor, order or reason-code consequence is not
proved, preserve explicit review envelopes and blockers. Do not copy engine
defaults or infer JSON Logic/Java from names.

### Corporate blockers

Given production `NOT_READY` but development draft admission, allow FND-12
technical work and keep homologation, publication and authority blocked.

### Adversarial plan

Reject path traversal, hash drift, unknown matrix row, secret/source/SQL
content, dirty producer, forged receipt, remote store and partial batch without
leaving a partial plan or head.
