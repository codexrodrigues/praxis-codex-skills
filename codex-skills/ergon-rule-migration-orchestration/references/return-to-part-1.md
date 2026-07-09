# Return To Parte 1 Policy

Parte 2 never fixes a Parte 1 gap silently. If the baseline is incomplete or contradicted, stop Parte 2 advancement and return to the correct Parte 1 phase.

## Return Map

| Finding in Parte 2 | Return target |
| --- | --- |
| Rule, trigger, product package block, client EP, HADES branch, side effect, audit, pending, publication, legal-document, workflow, or nested dependency was not audited | Parte 1 Phase 4 |
| Payload, operation discriminator, command DTO, hidden key, `P_OPER`, `P_ROWID_REG`, `PB_*`, `PP_*`, `P_MENS`, public key strategy, or route decision is incomplete | Parte 1 Phase 5 |
| Legacy error, `P_MENS`, ORA mapping, validation message, permission failure, dependency failure, duplicate/collision, or no-mutation behavior is unmapped | Parte 1 Phase 5 and/or Phase 7 |
| Required parity case is absent or fixture coverage cannot prove baseline behavior | Parte 1 Phase 7 |
| Handoff says a behavior is closed but evidence contradicts it | Parte 1 Phase 8 |
| A consumer or external flow exposes an operation whose backend/rule state is not closed | Parte 1 Phase 6 or Phase 8, depending on source of contradiction |
| UI exposes preflight/promoted/blocked/deferred behavior through local capability, action, surface, drawer, or workflow semantics | UI track via `ergon-angular-ui-screen-wiring`, and Parte 1 Phase 8 if backend handoff is inconsistent |
| New rule contract, metadata, config, feature flag, or error envelope is needed but canonical owner/support classification is missing | Parte 2 Canonical Decision Gate before implementation; if backend contract changes, Parte 1 Phase 5/6/8 as applicable |

## Return Artifact

When returning, record in the Parte 2 gate:

- finding;
- affected rule and operation;
- missing or contradictory Parte 1 artifact;
- exact Parte 1 phase to reopen;
- evidence that triggered the return;
- rule status after return, usually `Blocked - Missing Parte 1 Evidence` or `Blocked - Dependency Unknown`.

## Hard Blocks

Block Parte 2 if any of these are true:

- the operation is not approved in Parte 1;
- no approved Parte 1 baseline route exists (`WRITE_DB_BACKED_REQUIRED` or `WRITE_TABLE_DIRECT_SAFE`);
- HADES/EP/client behavior is unknown and could affect the rule;
- side effects are unclassified;
- no fallback is defined;
- promotion would cause unproven double execution.
- a host/UI/dashboard adapter is being used as the primary rule source instead of canonical Praxis metadata/config/API decision state.
