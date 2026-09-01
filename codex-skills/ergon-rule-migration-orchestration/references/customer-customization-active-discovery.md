# Active customer-customization discovery

Use this contract when a short Parte 2 prompt asks whether a customer
customization is active for a screen/write operation.

## Resolve the request without expanding the prompt

Derive the exact CREATE/UPDATE/DELETE scope and DB-backed route from the Parte 1
handoff. Keep client-side UI rules in the inventory, but select a customer
customization only from evidence tying the write route to HADES/EP or another
customer-owned server-side object. Required links are:

1. screen and write operation to the approved legacy route;
2. current HADES registration/activation for the relevant hook;
3. customer-owned Oracle object identity and validity;
4. structural source block for the candidate decision.

If a link is absent, report that link as missing. Do not silently replace the
candidate with an XML/form rule, and do not implement a decision during this
discovery step.

## Freshness rule for “active”

Activation is environment-bound and drift-prone. A historical HADES output is
provenance, not confirmation of current activation. When the declared
development connection is available and read-only queries are admitted, query
the current HADES registration and Oracle object state. Record environment
class and observation timestamp without publishing company, user, credentials
or connection details.

If current access is technically unavailable, label the conclusion historical
or stale and state the exact refresh needed. Never say “não existe ativa” as a
current fact solely from an older snapshot. When current and historical
evidence disagree, current environment evidence controls the current-state
claim; preserve the drift as evidence.

## HADES parent and child semantics

Evaluate the configured mode without conflating direct execution and multiple
EP execution:

When the captured fields match this model, run
`scripts/classify_hades_activation.py` to materialize the classification. The
helper classifies only supplied, already-sanitized facts; it does not query the
database or discover objects.

- parent `EXEC=S`: the parent is directly active when its executable syntax or
  route is present; `EXEC_MULT_EPS=N` does not deactivate that direct parent;
- parent `EXEC=N`, `EXEC_MULT_EPS=S`: evaluate the ordered child registrations
  and each child's `EXEC` state;
- parent `EXEC=N`, `EXEC_MULT_EPS=N`: a child row with `EXEC=S` alone is not a
  reachable chain through that parent;
- missing syntax/object or unresolved route remains explicit even when a flag
  is enabled.

Do not infer current state from a similarly named historical hook. Match the
exact operation, registered parent/child identity and effective route.

## Adversarial acceptance scenarios

### UI rule plus active direct customer parent

Given an XML `onChanged` date comparison and a current HADES parent with
`EXEC=S`, `EXEC_MULT_EPS=N`, executable syntax and a valid customer Oracle
object, investigate the server-side object as the requested customer
customization. Keep the XML rule as a separate UI finding.

### Old inactive snapshot plus current active registration

Given a historical `EXEC=N/EXEC_MULT_EPS=N` snapshot and a current read-only
observation of the exact parent as `EXEC=S/EXEC_MULT_EPS=N`, the current claim
is active direct execution and the historical-to-current drift is reported.

### Unreachable child

Given parent `EXEC=N/EXEC_MULT_EPS=N` and only a child row with `EXEC=S`, report
`NO_CHAIN` for that parent path. Do not generalize this result to another
current parent or environment.

## Output boundary

For discovery-only prompts, stop after the structural inventory, activation
chain and exact decision source/range. Return the three audience artifacts and
the freshness/authority statement. Do not choose an executor, implement Java,
run shadow, publish Config or change authority.
