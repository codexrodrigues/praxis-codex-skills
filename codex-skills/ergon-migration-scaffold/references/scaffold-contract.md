# Scaffold Contract

The scaffold requires both a semantic `resourceKey` and the real host
`basePath`. It is an implementation packet, not a generated Java source tree and
not a phase gate. It creates these files:

| File | Purpose |
| --- | --- |
| `README.md` | Immutable command inputs and source-evidence reminder |
| `operation-inventory.md` | Standard screen operations with state and route evidence |
| `praxis-contract-outline.md` | Resource endpoint and metadata outline to verify in the target module |
| `implementation-slice.md` | Ordered, smallest-first implementation tasks and proof obligations |
| `scaffold-manifest.json` | Machine-readable identity, operations, and generated version |
| `factory-timing.json` | Prospective elapsed-time ledger from scaffold creation |

Operation defaults are deliberately conservative:

| Operation | Praxis shape | Default state |
| --- | --- | --- |
| `list` | `POST /{resource}/filter` | `READ_EVIDENCE_REQUIRED` |
| `detail` | `GET /{resource}/{id}` | `READ_EVIDENCE_REQUIRED` |
| `options` | `POST /{resource}/options/filter` | `READ_EVIDENCE_REQUIRED` |
| `create` | `POST /{resource}` | `WRITE_ROUTE_REQUIRED` |
| `update` | `PUT /{resource}/{id}` | `WRITE_ROUTE_REQUIRED` |
| `delete` | `DELETE /{resource}/{id}` | `WRITE_ROUTE_REQUIRED` |
| `duplicate` | `POST /{resource}/{id}/duplicate-draft`, then `POST` | `WRITE_ROUTE_REQUIRED` |
| `cancel` | no mutation | `NO_MUTATION_PROOF_REQUIRED` |

Unknown operations must be added only from screen evidence. A write state becomes
`WRITE_TABLE_DIRECT_SAFE` only after its table-rule audit and parity proof; a
scaffold may never grant that state.

Timing events retain ISO-8601 UTC time, elapsed minutes, outcome, and an
evidence path. Supported milestones are `implementation-started`,
`first-endpoint-executed`, `schema-validated`, `focused-tests-passed`, and
`legacy-parity-assessed`. Repeating an identical event is idempotent; changing
the evidence, outcome, or time for an existing milestone requires a new named
investigation artifact instead of rewriting history.
