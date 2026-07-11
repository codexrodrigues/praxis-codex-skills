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

Schema ETags cache metadata. Resource-version ETags protect item mutation. Do
not conflate them or use one as a substitute for the other.
