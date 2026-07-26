# Catalog and Phase Forward Tests

Use these cases when changing the catalog assembler, checker, phase projection,
alias resolution or cockpit next-action logic in the migration repository.

## Documentary Rule and Atomic Decision

Given one documentary rule with multiple atomic proposals, report the two
populations separately. A phase or semantic change for one atomic decision must
not change the documentary parent or a sibling proposal unless a governed
source explicitly changes each artifact.

## Alias Resolution

Resolve a working alias only through both `canonicalRuleId` and `decisionKey`.
Reject missing, ambiguous, orphan or conflicting mappings. An alias is a
navigation aid, not a new rule identity or authority source.

## Phase Round Trip

Start from a checker-green catalog, select one atomic decision and route phase
work through `$ergon-rule-migration-orchestration`. After the focal phase gate
changes governed evidence or state, rebuild and recheck the portfolio, Domain
Catalog projection and cockpit together. The updated atomic state and next
action must appear without changing unrelated entries.

## Fail-closed State Preservation

Fixtures containing `UNKNOWN`, `REVIEW_REQUIRED`, `KEEP_DB_BACKED`, a blocked
phase, or unresolved ownership must preserve those states after regeneration.
They must not produce semantic confirmation, shadow/preflight admission,
target authority, publication, activation or legacy disablement.

## Determinism and Sanitization

Two builds from identical canonical inputs must be byte-identical. Reject stale
source references, duplicate identities, unexpected fields, absolute local
paths, credentials, raw client data, SQL session context and HADES internals in
the sanitized Domain Catalog or cockpit.
