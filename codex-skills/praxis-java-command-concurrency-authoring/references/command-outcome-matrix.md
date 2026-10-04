# Command Outcome Matrix

## Transition Packet

| Decision | Evidence |
| --- | --- |
| Command identity | Action ID, resource key, item/collection scope, target selection |
| Business transition | Allowed source state, target state, side effect, reversibility |
| Authorization | Backend policy and denied result |
| Idempotency | Key/fingerprint scope, replay behavior, retention, conflict behavior |
| Concurrency | Persisted version, ETag emission, If-Match requirement, stale result |
| Outcome | Accepted/success, denied, validation, conflict, sanitized error |
| Consumer | Action schema, capabilities/links, result and conflict materialization |

## Minimum Stress Proof

| Scenario | Expected proof |
| --- | --- |
| Valid command | One transition, correct outcome and resulting state |
| Same retry | No repeated effect and documented replay result |
| Different command with same identity | Explicit conflict or rejection, never accidental replay |
| Stale If-Match | Canonical precondition/conflict response; no overwrite |
| Missing required If-Match | Canonical refusal; no execution |
| Denied state/authority | Action unavailable and endpoint rejects consistently |
| Collection command | Per-target result and partial/atomic behavior match publication |
| Private atomic set admission | Last-target denial runs no mutation; dirty admission is rolled back before one fenced rejection |
| Private atomic set failure | Last-target or evidence-append failure leaves no domain, outbox, header or child commit; no partial read window |
| Private atomic set uncertainty | Lost ACK reads the receipt first; absent receipt before the unit deadline stays unresolved, and post-deadline recovery never repeats mutation |
| Current grant denial | False current-authority check maps to authorization rejection, with no mutation; dependency failure is never relabeled as denial |
| Private atomic pre-SQL unavailability | Budget refusal before SQL preserves typed DEPENDENCY_UNAVAILABLE / UNIT_ROLLED_BACK and no effects |
| Private atomic SQL-aborted admission | Real 42501 can abort the transaction and lead to RECONCILIATION_REQUIRED before normal rejection; prove zero callbacks/effects/receipt/rejection, not a fabricated successful refusal |
| Private atomic SQL-failure recovery | Observe the active unit deadline and allocation, await real active_unit_deadline_at expiry; bounded independent lock read after rollback; for this case without a cancellation request, fenced recovery STOPPED / RECOVERY_STOPPED, epoch+1, RELEASED / TERMINAL_RECONCILED, old owner FENCED, terminal replay without mutation |
| Private atomic set visibility | Watermark remains zero before certification and advances to the entire ordered set only after ACK or fenced recovery |

Schema ETags cache metadata. Resource-version ETags protect item mutation. Do
not conflate them or use one as a substitute for the other.

Host admission decisions and the durable kernel result are separate oracles.
An UNAVAILABLE wrapper return does not clear an aborted PostgreSQL transaction.
A pre-mutation permission error is not a lost-COMMIT proof; public HTTP mapping
requires its own concrete consumer evidence. Never rewrite deadlines, increase
budgets or introduce savepoints solely to satisfy a test expectation.
