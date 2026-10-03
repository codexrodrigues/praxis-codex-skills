---
name: praxis-java-command-concurrency-authoring
description: Use when implementing, auditing, or migrating a Praxis Java business command with state changes or its internal durable bulk-read foundation: @WorkflowAction, command request/response schemas, ResourceCommandExecutionRequest and Result, idempotency, item or collection scope, resource version ETag, If-Match preconditions, conflict/denial outcomes, bounded execution-result paging, action availability, REPEATABLE READ read-only MVCC snapshots, and safe Angular/runtime handoff.
---

# Praxis Java Command Concurrency Authoring

Treat a business command as an explicit governed transition, not a convenient PATCH.
It must state what changes, which state and authority permit it, retry behavior,
expected version, and a result that callers can safely materialize.

## Establish The Transition

Inspect resource, state model, CRUD path, action catalog, availability, command service,
persistence version, errors, direct consumer, and focused tests. Decide whether it is an
ordinary edit, item command, collection command, or accepted asynchronous operation.

Classify each command endpoint, request field, outcome, idempotency key, precondition,
ETag behavior, or action metadata as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or
`lacuna-real-de-contrato`. New command semantics belong in canonical resource/action
contracts, never in a host controller convention.

## Author The Command Contract

1. Model the transition with `@WorkflowAction`, stable ID, collection/item scope,
   schemas, side effect, authorization/state boundary, HTTP outcome, and negative path.
   Keep ordinary CRUD on the resource base.
2. Use dedicated request/response DTOs. Document intent, targets, validation,
   reversibility, confirmation, external effects, audit, and governance. Never reuse
   a create DTO or untyped map.
3. Use `ResourceCommandExecutionRequest`, `ResourceCommandExecutionProvider`, and
   `ResourceCommandExecutionResult` when the starter command infrastructure applies.
   Return accepted, denied, expected failure, or sanitized unexpected outcome deliberately.
4. Define idempotency by domain: scope, key, fingerprint, retention, replay result, and
   conflict behavior. Replay is valid only for the same caller-authorized command.
5. For mutable item commands, use resource-version ETag and `If-Match` when persisted
   version support exists. Reject stale or required-missing conditions canonically;
   never compare versions only in Angular or silently overwrite. Schema and resource
   version ETags solve different problems.
   For B4-R1 candidate resource responses, pair the DTO with the persisted
   revision captured from that same entity, then emit the ETag from the pair;
   a second lookup after projection or commit can sign a newer version onto an
   older body. A versioned PUT must validate the input precondition and require
   a nonempty captured result inside its write transaction after the last
   hook/flush; the controller's post-commit guard does not roll back arbitrary
   custom services. Historical action replay uses its captured revision or
   omits ETag, never the current row's revision. Prove GET/PUT interleavings
   with two PostgreSQL connections, DTO token/header agreement when a DTO
   token exists, stale token `412`, empty-revision rollback, and replay without
   token renewal. Do not infer a snapshot of links or related entities.
6. Align action catalog, capabilities, `ResourceStateSnapshot`, endpoint enforcement,
   and `_links`. Availability is not security; execution enforces the same decision.
7. For collection commands, define per-item outcome, atomicity, partial failure, retry,
   and ordering. Never report complete success when targets were denied or conflicted.

For a metadata-driven bulk command, keep composition readiness separate from command
authorization and execution. The Metadata lifecycle may return a durable expectation
only after the descriptor is recomposed from the installed, durably validated published photograph; the proposal writer must still revalidate
that exact namespace/operation generation, fingerprint, and structural revision under
the V7 transaction/lock before reserving or mutating. Publish and suspend use the
separate PostgreSQL control-plane credential, while proposal/execution use the runtime
credential; prove both bindings reach the same database, not merely matching JDBC
URLs or namespace labels. Prepare or explicitly reconcile the complete photograph through attested exact-group producer captures outside JDBC transactions. Ordinary readiness must not regenerate SpringDoc or use a configurable remote source as current authority; cold/stale replicas fail closed until explicit reconciliation. Bound structural reads within a unit use the same attested operational connection and no cache lock or REQUIRES_NEW. A `READY` descriptor does not prove production host handlers,
domain authorization, or atomic domain-plus-receipt behavior.

Read [command-outcome-matrix.md](references/command-outcome-matrix.md) when selecting
scope, preconditions, idempotency, result status, or focused proof.

## Bind Resource-Version ETags To The Operational Scope

When a host must separate resource-version ETags across operational bindings, inspect
the published `ResourceVersionScopeProvider` and use one server-owned, immutable
binding scope for item GET/body ETags, action responses, and `If-Match` evaluation.
Changing only an action's precondition leaves GET and command tokens inconsistent;
a global provider also affects other versioned resources, so inventory their GET,
update, action, anonymous-read, and direct-consumer paths before enabling it. Do not
derive the ETag scope from request headers, a mutable principal/grant, or an authority
hint. A GET with a configured scope proves token composition, not database identity
or authorization; verify the actual binding separately.

After a composed host adopts binding scope, reject old `GLOBAL` tokens rather than
accepting both scopes or silently retrying them. `GLOBAL` may remain legitimate in an
uncomposed, non-operational host; do not invent a binding there. Prove GET/action
agreement and rejection of the old token, then compare two real bindings/databases
with the same signing secret, resource key, ID, and version: a token from one must not
satisfy the other's precondition. Keep GET token generation bounded; avoid a new
database query per resource read merely to compute the scope. These checks do not
replace current grant or target authorization, receipt/replay, or deployment proof.

## Fence Cross-Resource Authority And Writers

When a command's decision depends on a current grant and mutable related rows,
inventory every writer of that predicate before choosing locks: item and batch CRUD,
the command itself, parent state and scope changes, and privileged direct SQL. Action
availability is a UI hint, not authorization; a JWT authority alone cannot prove the
current persisted grant or scope. Resolve the authenticated operational context and
recheck the current grant and target scope at execution, without leaking the existence
of out-of-scope rows.

Keep the authorization fence and domain mutation in one writable transaction on the
same physical database connection. Establish a shared lock order across participating
writers: a governed command locks its current grant first, then distinct parent IDs
in sorted order, then distinct child IDs in sorted order. Ordinary CRUD and batch
writers enter at their first shared resource lock (parent, then child); they do not
acquire the grant after locking a parent. Discover parent IDs with scalar reads that
do not auto-flush; acquire the locks before staging changes. Apply the shared resource
order to create, update, delete, batch delete, and parent lifecycle writers. Inspect
whether the base
batch path bypasses per-item hooks; a correct single-item hook does not cover it.

For a multi-parent aggregate such as a mission team, discover the complete union of
current and proposed references before the first shared lock, then lock distinct
employees, missions, and participants in that order, sorting IDs within each set.
Use scalar reads with `FlushModeType.COMMIT`, reject an already-dirty persistence
context, and recheck the discovered memberships and statuses after locking. A newly
discovered dependency is a conflict, not permission to acquire a late parent lock.
Apply the same fence to item/batch CRUD, team planning, mission status/deletion,
and employee deletion; do not let ordinary CRUD bypass a workflow transition.

When retained participants exchange references, a PostgreSQL uniqueness constraint
may need `DEFERRABLE INITIALLY IMMEDIATE` while ordinary writers keep immediate
enforcement. Defer that named constraint only in the protected planning transaction
that actually changes retained references; validate the entire proposed team first,
flush the final state, and set the constraint back to `IMMEDIATE` before returning
from the transaction. Do not add an engine-specific fallback that silently weakens
the invariant. Inspect `db/operational-migrations/V20261001_004__mission_team_reference_uniqueness.sql`
and `operations/service/MissaoService#planTeam` in the quickstart before reusing this
pattern elsewhere.

Before locking or refreshing managed entities, reject a dirty persistence context so
pending caller changes cannot be flushed prematurely or erased. Under the row locks,
compare the database parent and version with any already-managed entity. Reject a
stale or missing row, including any missing batch member, instead of refreshing it
into an apparently current command; refresh only clean, matching entities. Stage the
mutation after these checks and preserve the transaction's rollback on denial or
conflict. Keep denial, conflict, and unexpected infrastructure outcomes sanitized;
verify their actual HTTP mapping in the host and canonical command executor.

Prove the protocol with real PostgreSQL and two independent connections: revoke or
change the grant while a command waits, interleave parent and child writers in both
directions, exercise batch deletion and missing IDs, and assert rollback leaves no
partial domain change. Include stale and dirty managed-entity cases; exercise
representative opposing interleavings and report any observed deadlocks. Verify the
actual JDBC identity and database
role (`session_user` and `current_user`) of each test connection, along with the
runtime role's function permissions; matching JDBC URLs do not prove the binding.
A test of the command alone cannot establish
that all writers participate. Direct SQL and imports remain outside an application
lock protocol unless they explicitly follow it or a database-enforced boundary covers
them; record that limit rather than claiming global serialization.

## Refactor Command Parameters Without Invalidating Existing Work

Before separating selection/version transport from shared business parameters,
inspect the current handler DTO, Bean Validation, emitted request schema, action
links and durable command fingerprint implementation. Reuse a typed parameter model
only when it preserves the active endpoint contract; inheritance is an option, not
a requirement. Prove inherited constraints and field metadata in real HTTP schemas,
not only a local ModelConverters result. Keep the complete request schema distinct
from a parameter-only model; extracting a class does not publish a bulk evaluator.

For strict bulk binding, require an explicit globally unique operation ID on the
real resource handler and verify discovery links resolve that operation. Changing
an automatically generated ID requires consumer rediscovery; do not add aliases by
reflex or silently redirect saved operation references.

DTO refactoring can change Jackson property order even when the JSON object has
the same logical fields. If the current ledger hashes serialized POJO bytes, map-key
sorting alone does not make bean property order stable. Capture pre-change bytes or
a fingerprint with the host's mapper and prove replay of a previously completed
record against the new code. Preserve the existing wire order when that is the
scoped compatible correction; do not rewrite hashes or globally normalize the ledger
without a separate migration design. Same-version retry tests alone miss this risk.

## Preserve Boundaries

- `praxis-metadata-starter` owns command execution types, resource version
  preconditions, action discovery, schemas, capability projection, and the shared
  governed-bulk persistence kernel: protected proposals/evaluations, execution
  controls, item receipts, fencing, quota allocations, and retention primitives.
- The host owns the domain transition and current authorization/policy decision.
  In the durable bulk path the Metadata kernel owns the physical operational unit
  transaction and atomic receipt; host admission runs under that unit. Operational
  datasource reads/writes and published structural reads use its attested writable
  connection. Policy/grant authorities may use independent databases and must
  complete before control recheck and domain mutation. Keep remote effects behind an outbox or another independently
  idempotent boundary; a PostgreSQL receipt cannot make a remote side effect atomic.
  Do not leak database version, package, queue, token, or internal exception details.
- `praxis-ui-angular` consumes action schemas, links, capabilities and safe conflicts.
  It does not infer idempotency or manufacture `If-Match` locally.

Do not resolve command intent from labels, route fragments, keywords, regexes, or aliases.
Use resource/action IDs, schemas, availability, capabilities, and governed context;
text can only rank already-scoped candidates.

## Bind Bulk JDBC Work To The Operational Transaction

`BulkExecutionInfrastructure(dataSource, transactionManager, namespace, deploymentId,
roleConfiguration)` is the Metadata-owned explicit integration boundary. The former four-argument
constructor is removed: provide a `BulkExecutionRoleConfiguration` with an expected schema owner
and at least one explicit runtime grantee role, populated from real database provisioning. Keep
runtime, control-plane and retention identities disjoint. It provides transaction participation;
storage is composed explicitly through `JdbcBulkProposalStore`. Neither class is an executor,
worker or runtime capability. Construction performs no database access or DDL. The namespace is
explicit and stable; it is not authentication or authorization and must not be inferred from
untrusted headers.

Use the actual shared datasource instance with a local JDBC manager or a JPA manager
whose EntityManagerFactory exposes the same datasource through EntityManagerFactoryInfo.
Initialize the beans first. The initial subset rejects opaque/mismatched managers,
routing and datasource wrappers; do not compare URLs or choose a Primary bean.

`withConnection(ConnectionCallback)` joins MANDATORY, writable, existing physical
transactions through JdbcTemplate. Before the namespace read and callback, it attests the
authenticated/effective identity (`session_user == current_user`) against the configured runtime
roles and rechecks live protected-table/function ACLs, schema/table/function ownership and V7
descriptor-fence definitions on that same transaction connection. Drift or an unconfigured role
fails closed before the caller's callback. `withLifecycleRead` repeats the runtime attestation
inside its separate short transaction. These live checks do not run Flyway or DDL and do not
replace the explicit privileged migration/physical-validation step. Each attestation SQL is
bounded to 250 ms, preserving any stricter existing statement timeout and restoring the previous
setting; this bounds each SQL separately, not the total sequence. Lifecycle reads also cap lock
and statement timeouts at one and two seconds without increasing stricter configured values.

No independent transaction is started by `withConnection`. The callback must not commit/rollback,
change auto-commit or retain the connection. Its return is provisional until the outer owner
commits; domain authorization, deadlines and receipt semantics remain separate. Manager-visible
rollback-only is rejected; a local outer status mark may not yet be visible to a participant. Stop
mutations when the owner decides rollback. The binding rejects
`globalRollbackOnParticipationFailure=false` at construction and before work, preserving the
required rollback-only behavior when a callback fails.

Prove the adopted pair with real PostgreSQL/JPA: same backend PID for JPA/JDBC, independent
observer before/after commit, both writes rolled back, deferred constraint failing at
COMMIT after callback completion, manager mismatch, and two-connection lock contention.
Use BulkExecutionInfrastructureTest, BulkExecutionInfrastructurePostgresTest, and
BulkControlPlaneInfrastructurePostgresTest as required real-PostgreSQL gates. The control-plane
proof must cover live runtime/control-plane identity and ACL/owner/fence drift rejection, the
runtime/control-plane advisory-lock witness on the same physical database, and preservation of
stricter statement/lock timeouts. Fixture tables are not the production ledger DDL; these gates
do not certify the host's production migration or bulk execution. Consult Metadata
docs/spec/BULK-EXECUTION-INFRASTRUCTURE.md.

## Build An Internal Durable Bulk Read Before A Public Reader

Treat a durable execution read as an internal consistency boundary, not as a shortcut to an
HTTP resource. Inspect the live `JdbcBulkDurableExecution`, `BulkExecutionInfrastructure`,
protected evaluation/manifest codecs, receipt/admission ledger, allocation lifecycle, retention
and tombstone paths, PostgreSQL tests, and the current `docs/spec/BULK-H1B-READ-MODEL.md` before
changing a reader or its projection. The Metadata starter owns this read kernel; a host performs
current authorization before using any future public projection.

1. Open one independent, short transaction before the first data query. It must be physically
   `REPEATABLE READ` and `READ ONLY` on the runtime PostgreSQL connection, with bounded local
   lock/statement timeouts, namespace/role attestation, and a closed transaction. Do not reuse an
   ambient writer transaction or rely only on Spring/JPA flags: prove
   `transaction_isolation=repeatable read` and `transaction_read_only=on`, including with a
   `JpaTransactionManager`.
2. Read execution, proposal/evaluation, ordinal manifest, receipts/admissions, both allocation
   records, and tombstone in that one MVCC snapshot. Revalidate scope, fingerprints, digests,
   structural versions, cardinality, uniqueness, manifest binding, ledger form, and legal
   status/allocation combinations. Missing, duplicate, cross-scope, drifted, or impossible state
   is `CORRUPT`/unavailable and fails closed; never fabricate a partial aggregate.
3. In `RECONCILIATION_REQUIRED`, count only the certified contiguous prefix below `nextOrdinal`.
   A physically present receipt or admission at or after that ordinal remains `UNKNOWN`: validate
   it for corruption, but never turn it into `CONFIRMED`, another completed outcome, or public
   `NOT_PROCESSED`. Keep the conservative suffix as
   `unknown = targetCount - nextOrdinal` even when the physical ledger contains more rows.
4. Keep the result package-private and protected. An internal `ABSENT`, `LIVE`, or `TOMBSTONE`
   observation does not decide 404/410, does not expose protected blobs/facts/plans/diagnostics,
   does not acquire write locks, call domain code, mutate quota or epochs, or serialize a response.
   Do not add HTTP, cursor, public reader, `READY`, Angular, corpus, or playground work until the
   separate authorized reader contract, redaction, authorization, pagination, and cost proof exist.
5. Prove on real PostgreSQL, not a mock or only context startup: physical write rejection
   (`SQLSTATE 25006`), JPA-manager isolation, cross-scope invisibility, receipt commit racing the
   snapshot, purge racing a tombstone, manifest/receipt/allocation corruption, and the 10,000-target
   boundary. A paused reader after its first snapshot-fixing SELECT must never return a mixture of
   epochs; a new read may observe the later commit or tombstone.

The RS3 internal foundation is integrated in Metadata source, but source integration
does not prove a published starter or a public capability. Compare the current
Metadata main and adopted revision before relying on it.

### Derive An Internal Summary From The Certified RS3 Snapshot

Metadata merge `766bd6b586331949d1fcf3d405be3bd3e5a59b4c` adds the
package-private `BulkExecutionSummary` and
`JdbcBulkDurableExecution.summarizeConsistent`. Inspect those sources and the
RS3 section of `docs/spec/BULK-H1B-READ-MODEL.md` before changing a status or
total. Derive the summary only from `inspectConsistent` in its physical
snapshot; do not re-read mutable control or infer an outcome from raw ledger
row counts. Preserve `ABSENT`, `LIVE` and `TOMBSTONE` as internal observations,
without choosing 404/410 before the host's current, whole-set authorization.

- Count `CONFIRMED`, `UNCHANGED` and governed admissions only in the certified
  prefix below `nextOrdinal`. For `RUNNING`, `UNIT_IN_FLIGHT` and
  `UNIT_COMMITTED_PENDING_ACK`, keep the remainder `pending`; an unacknowledged
  receipt does not become a certified success. Project `CANCEL_REQUESTED` only
  when persisted `cancelRequestedAt` exists. A request for cancellation alone
  does not prove a terminal `CANCELLED` state.
- In `RECONCILIATION_REQUIRED`, count the whole suffix as `UNKNOWN`, even if a
  physical receipt is present. For terminal `STOPPED`, count the suffix as
  `NOT_PROCESSED` only after RS3 proves physical absence of receipts and
  admissions there. Map `CANCELLED_BY_USER` to `CANCELLED` only after that
  terminal proof. Completed states require an integral certified prefix and
  compatible outcomes.
- Require the outcome totals to sum to `targetCount` and reject inconsistent
  status, counts or timestamps as `CORRUPT` without protected causes. Preserve
  persisted instants in the internal summary. Metadata V13, merged at
  `46c130494d74188e863c3c0c8bd8e20acffbcb65`, now enforces chronology in
  `V13__bulk_execution_time_order.sql`; do not normalize timestamps in the
  reader or edit applied V5/V10 migrations. Before changing this path, inspect
  V13, `BulkExecutionMigrator`, terminal writers and their PostgreSQL tests.
  V13 preflights the exact V5 terminal guard and V10 cancellation guard bodies,
  owner/ACL boundaries and all six execution UPDATE trigger bindings. Its
  versioned replacement of `guard_terminal_execution()` restores the governed
  owner and privileges; the migrator attests the V13 body, trigger catalog and
  chronology constraint, and must reject later drift rather than heal it.
  Under the migration's transaction and table lock, historical
  `terminal_at > updated_at` rows receive `updated_at=terminal_at` while the
  certified triggers are temporarily disabled and then restored. Other
  violations of the V13 chronology CHECK abort the migration. The CHECK
  enforces created, updated, terminal and cancellation order for old and new rows.
  Terminal writers use one SQL statement clock per UPDATE; the database guard
  remains authoritative for retention:
  `new.terminal_at := greatest(clock_timestamp(), old.updated_at, old.cancel_requested_at)`
  and `new.updated_at := greatest(new.updated_at, new.terminal_at)`. This may
  preserve a later old timestamp rather than the current database instant.
  V10's cancellation guard participates in the same UPDATE without a separate
  assumed rewrite.

Prove this projection with focused PostgreSQL tests for initial and partial
states, receipts/admissions, pending ACK, cancellation before and after
reconciliation, `STOPPED` suffix absence, completed outcomes, cross-scope
absence, tombstone and corruption. Reuse the RS3 snapshot, concurrent
receipt/purge and 10,000-target evidence when that reader is unchanged. Keep
the summary opaque to Jackson and logs; it introduces no public endpoint,
cursor, capability, `READY` or host authorization shortcut.
Before Flyway V13, drain V12 writers and retention; restart and reopen traffic
only on V13 binaries because V12 attestation rejects the changed V5 body.
PostgreSQL 14.22 proof for PR #193 covered terminal transitions and V10/V13
same-UPDATE ordering, historical repair/refusal, V5 checksum stability, and
trigger/owner/ACL restoration and drift rejection: 69/69 execution tests,
22/22 migration tests, 90 affected reader/store passes and 2/2 corrected
fixture reruns. Repeat the focused affected proofs when this boundary changes.
The `BulkExecution` public DTO, HTTP handler, release and host
authorization/redaction remain separate gates.

### Compose an Authorized Execution Summary (G3c-a)

The public SDK `BulkAuthorizedExecutionReader` is a server-side composition, not an
HTTP surface. It composes a trusted resource key, confirmation operation and
authorization provider; its protected lookup helpers remain package-private. Callers
supply only the authenticated subject and execution UUID. Use its single Metadata-owned `REPEATABLE READ READ ONLY`
snapshot for global authorization, retained-execution lookup, protected proposal and
full current authorization of every historical target, then RS3 `summarizeConsistent`
and projection. These observations must share the same physical connection and snapshot;
do not add a second reader transaction, reconstruct proposal metadata or execution
results from current descriptors/domain rows, or authorize only the displayed summary.
The host authorization provider must consult its current authoritative grant/coverage
source within the same snapshot. Derive status/totals/timestamps only from the
certified RS3 summary and durable validated intent. Preserve the certified prefix; do
not count pending ACK receipts as confirmed, and map `STOPPED`'s internal reason to its
fixed sanitized diagnostic rather than returning a stored cause.

For an absent live execution, use the scoped historical tombstone digest. Only its
matching creator with current global grant can observe `GONE`; delegated requesters,
other scope and unknown IDs share `NOT_FOUND_OR_DENIED`. Before full set authorization,
lookup/decode/correlation and proposal-specific storage failures remain non-enumerating
`NOT_FOUND_OR_DENIED`; after successful authorization, summary corruption or deadline
expiry is `UNAVAILABLE`. Global denial/unavailability precede protected lookup. Validate
namespace, resource, operation and authenticated subject as nonblank strict UTF-8 scope
text with no NUL before SQL; reject malformed surrogate input, never let replacement
encoding alias a different identity. After decoding the protected proposal, compare
the execution locator's input and evaluation fingerprints with the decoded proposal's
snapshot and evaluation fingerprints before building targets or calling `authorize`;
mismatch remains `NOT_FOUND_OR_DENIED`. Preserve execution-retention
reads past execution expiry only while authorization and retained evidence still permit
them.

This composition creates no route, result-item endpoint/cursor, RS4 behavior, worker,
capability or `READY`; do not treat internal `GONE` as a public HTTP status before a
separate host contract and redaction decision. Require PostgreSQL proof and independent
review for this composition; integration, publication and adoption remain separate
gates.

### Compose Authorized Execution Result Pages (G3c-b)

Reuse G3c-a protected execution/proposal correlation helpers and the internal RS4 page reader; do not
duplicate the keyset, fixed-watermark or byte-budget rules in the RS4 section below.
The public Java facade accepts only authenticated subject, execution UUID, size (1–200) and optional
continuation, with trusted server bindings for infrastructure, resource, provider and
cursor configuration. Decode with purpose `EXECUTION_RESULTS` before protected lookup;
on every live page perform global authorization, correlate the execution's input and
evaluation fingerprints to the decoded historical proposal, then authorize every
historical target from the host's current authoritative grant/coverage source. Full-set
authorization and RS4 certification must share one physical `REPEATABLE READ READ ONLY`
connection/snapshot; use the connection-taking RS4 seam, never nest its transaction or
run RS3's full scan to serve a page.

Bind proposal/execution, creator scope, current requester/provider fingerprint,
position, size, fixed `watermarkExclusive`, `execution-results-v1` projection revision,
and original issue/expiry times in the authenticated cursor. Keep the watermark, size
and expiry fixed across continuation; initial watermark zero returns an empty page with
no cursor. A new read may observe a later STOPPED suffix, but an open window never widens
across ACK, cancellation, or reconciliation. Project only certified wire identity and
status. CONFIRMED/UNCHANGED have no diagnostics; DENIED/INVALID/CONFLICT/NOT_PROCESSED
use closed generic diagnostics by status, without raw reason, cause, version, facts,
parameters, target pointers or extra identifiers. This is execution evidence, not an
evaluation preview: do not require a V9 preview association.

For live executions, mismatched requester/scope/fingerprint remains
`NOT_FOUND_OR_DENIED`; after full authorization, expiry/size/projector mismatch is
`PRECONDITION_FAILED`, impossible claims normalize to a negative result, an old
watermark beyond the current certified prefix is `UNAVAILABLE`, and post-auth RS4 item
corruption is `UNAVAILABLE`. A purged tombstone is a separate minimal authorization:
the historical creator plus current global grant may receive payload-free `GONE` after
the scoped digest check. With a cursor, bind purpose, execution, namespace/resource/
operation and requester equal to its creator; purged data cannot revalidate proposal ID
or target authorization fingerprint. A delegated cursor copied to the creator may
therefore yield the same empty `GONE` the creator can obtain without it. Claim full
anti-copy protection only for live pages, not this post-purge exception. Enforce the
three-second monotonic publication deadline after transaction completion. Before
publishing, verify the continuation token is still sendable: an initially issued `next`
token already expired at completion is `UNAVAILABLE`; an expired continuation is
`PRECONDITION_FAILED`. Preserve the original expiry and never renew TTL.

If Quickstart hosts issuance, reuse its G3b-O durable budget and the same immutable
`BulkReadCursorProperties.Provisioned` key-material snapshot and ledger. Count possible
cursor issuance against the shared material quota regardless of AEAD purpose; do not
create an `EXECUTION_RESULTS`-specific quota. This Java facade adds no HTTP route,
`READY`, capability, or public host adoption. Require PostgreSQL proof and independent
review; publication, adoption and future HTTP mapping remain separate gates.

### Expose Authorized Execution Reads Over Host HTTP (G3c-HTTP)

Compose the host's two bodyless GETs from the authorized Metadata readers; do not add
host-owned result DTOs, a parallel registry, capability, cancel route, or claim the
remaining lifecycle bindings are complete. The planned resource is the existing
`human-resources.eventos-folha`: `GET R/bulk/executions/{executionId}` with operationId
`human-resources.eventos-folha.bulk-execution-read`, and `GET
R/bulk/executions/{executionId}/results` with operationId
`human-resources.eventos-folha.bulk-execution-results`. Keep `ApiPaths`, the real
controller mapping, `CanonicalOperationResolver`, and the named OpenAPI document in
agreement. Both requests are bodyless; only results accepts `size` (1–200) and an
optional opaque `after` continuation.

Map only the approved host states: 200 for an authorized live summary or results page;
400 for malformed cursor/page size; 403 for global authorization denial; indistinguishable
404 for absence, denial or a specific failure before full authorization; payload-free
410 for an authorized creator tombstone; 412 only for a live, fully authorized resource
with a stale continuation; and generic 503 for global unavailability or protected-read
failure after full authorization. Do not reuse proposal preview's 409. Apply
`Cache-Control: no-store` to success and errors. Use `RestApiResponse` and
`CustomProblemDetail`; publish result identity as strict `Integer`/OpenAPI `int32`,
rejecting type drift instead of coercing. The summary reader emits no cursor and
consumes no issuance budget. Results reserve the shared G3b-O ledger before entering
the core reader, never refund the reservation, and create no purpose-specific quota.
After that outer reservation, decode `EXECUTION_RESULTS` inside the core before any
protected SQL or authorization; perform global authorization before protected lookup.

Both GET and HEAD matchers must require authentication before any broad `readOpen`
rule. Prove anonymous denial under `readOpen`, full-set reauthorization for live
results, uniform absence/cross-scope/delegation negatives, and that a retained
tombstone yields only the documented creator-only 410. After purge there are no
targets to reauthorize: do not claim live-page anti-copy guarantees for tombstones.
Keep path/query parse failures non-enumerating as well. Verify bodyless operations,
exact operation IDs, resolved response schemas, `int32` identity, and the canonical
resource/method binding in OpenAPI tests. Do not mark HTTP acceptance, publication,
adoption, any lifecycle `READY`, or Angular readiness from this implementation plan;
those remain separate evidence gates.

## Page Internal Durable Execution Results Without Widening The Window

The RS4 `BulkExecutionResultsReader` is integrated in Metadata source at merge
`ff0d6b074c0d7922cc887340b01edec81285417e`, but is package-private and not
a published host reader. Inspect it with `docs/spec/BULK-H1B-READ-MODEL.md`, the
V8 target manifest, V3 receipts, V4 admissions, scoped tombstone, and RS3
`inspectConsistent`. RS3 audits the whole execution, counts and allocations;
RS4 proves only the returned items and minimum terminal state in a bounded
page. Do not use RS3's 10,000-target scan to serve a small page or claim that
an RS4 page proves the whole ledger.

1. Use the existing `withConsistentRead` physical `REPEATABLE READ READ ONLY`
   transaction. Read header, scoped tombstone and ordinal keyset with the
   manifest and receipt/admission joins in one snapshot; order by ordinal and
   select at most `size+1` rows. Bind namespace, subject, resource, operation,
   execution and proposal scope, then verify evaluation fingerprint, target
   count, wire identity, version and digests for each selected row.
2. The first page returns `watermarkExclusive`. Require the caller to carry
   that fixed value on every continuation; reject continuation without it and
   never widen the old window after ACK or `STOPPED`. A new read may observe a
   later status or tombstone. Status and totals can advance independently of an
   older page.
3. Below `nextOrdinal`, require exactly one coherent receipt or governed
   admission per item. An uncertain suffix during `RECONCILIATION_REQUIRED`
   stays outside the window: never materialize `UNKNOWN`. In terminal
   `STOPPED`, return `NOT_PROCESSED` only for an ordinal from `nextOrdinal`
   onward with physical absence of both receipt and admission on that row.
   Nonterminal states do not invent future results.
4. Require `COMPLETED` and `COMPLETED_WITH_ERRORS` to have
   `nextOrdinal=targetCount`; the former has no admission and the latter has at
   least one. Reject contradictory terminal state, gaps, duplicate evidence or
   binding drift as `CORRUPT`; SQL, ACL and timeout failures are `UNAVAILABLE`
   without protected payload or private reason in the exception.
5. Count selected header and row bytes against 20 MiB per call, including the
   `size+1` lookahead row. Accept exact equality; reject the first excess byte
   without returning a partial page. Set `fetchSize(1)` before query execution
   as a conservative fetch strategy, not proof of a heap bound or production
   latency. Benchmark representative data before public exposure.

Prove RS4 with focused real-PostgreSQL tests for fixed-watermark continuation
across ACK and `STOPPED`, no `UNKNOWN` in reconciliation, terminal admission
consistency, cross-scope absence, drift, concurrent ACK and purge across
connections, 10,000-target keysets and lookahead byte overflow. Reuse RS3's
physical JDBC/JPA snapshot proof when that infrastructure is unchanged, while
retaining RS3 for full audits. Keep the value opaque to Jackson and logs.
Current granular authorization, identity/reason redaction, protected cursor,
HTTP, capability and `READY` need separate reviewed gates; this internal
reader supplies none of them.

## Persist Protected Bulk Inputs Explicitly

Compose `JdbcBulkProposalStore` with the same BulkExecutionInfrastructure. Persist a
`BulkStoredProposal` containing the UUID, microsecond timestamps and immutable
`BulkIntentSnapshot` (trusted context, built-in identity codec, modality and intent).
The adapter accepts EXPLICIT/SYNC inputs in all three modalities. A new proposal
and its `PROPOSAL_PENDING` quota allocation are inserted in one transaction under
durable deployment/subject bucket locks. It is still not a READY evaluation or a
captured QUERY manifest, and storage does not authorize execution. Do not persist
the redacted public BulkProposal as execution input.

Insert/find join the existing writable transaction. Insert is provisional until commit;
UUID conflicts never overwrite. Find requires trusted namespace, subject, resource and
operation ID; original operation coordinates/schema revision are returned for subsequent
revalidation. Reading an expired snapshot does not authorize execution. Never expose this
object through HTTP, logs or UI; store failures omit protected driver/parser causes.
Fingerprint checking detects inconsistent content, not malicious database administrators.

Before persisting, require canonical wire validation of every target, not only a recognized
codecId: a custom codec must not claim integer/UUID while storing incompatible JSON tokens.
Use BulkStoredProposalContractTest for this boundary and preserve compatible custom encoders.

Read HTTP decimal tokens directly as BigDecimal as well as in protected storage; Jackson's
tree reader can probe a valid large exponent as double/Infinity despite exact-decimal settings.
Prove normalization is closed under repeated validation and storage decoding: trailing zeros
at scale -256 must not produce an invalid scale after normalization. Preserve the existing
fingerprint framing, distinguish integer from decimal, and prove commit/readback of input,
facts and plan in BulkEvaluationStorePostgresTest. Do not relax transport numeric limits.

Use the internal storage codec, not the host ObjectMapper: canonical decimal 1.0 must
remain DecimalNode and differ from integer 1. Preserve exact large integers, decimal
precision/scale limits and defensive copies. Protocol node validation is reused internally;
the public raw-byte reader keeps its original lexical limits.

Migrate explicitly with BulkExecutionMigrator on the operational PostgreSQL datasource,
outside domain transactions. Follow Metadata docs/spec/BULK-PROPOSAL-STORAGE.md for the
isolated migration lane, privileged migration identity, runtime grants, physical schema
validation and unsupported features. Prove JdbcBulkProposalStorePostgresTest and
BulkSnapshotStorageCodecTest, including concurrent migration/insertion, rollback,
scoped lookup, immutable rows and corrupted content. Update this guidance as evaluated
facts, target manifests and execution state are actually implemented.

## Compose A Durable Per-Item Execution In Metadata

`JdbcBulkDurableExecution` is a protected Metadata kernel composed explicitly with the
same operational `BulkExecutionInfrastructure`; it does not register an operation,
authorize the actor, establish eligibility, publish HTTP, or start workers. This cut
only supports stored-evidence `EXPLICIT`/`SYNC`/`PER_ITEM` proposals. Verify the exact
contracts in Metadata `docs/spec/BULK-DURABLE-EXECUTION.md` and
`docs/spec/BULK-GOVERNED-UNIT-ADMISSION.md`; validate the V3→V4 admission migration
(`V4__bulk_governed_admission.sql`) with `BulkExecutionMigrator.validate(DataSource)`
and `BulkDurableMigrationPostgresTest`. V3 alone is the prior receipt-only state and
does not establish S4b readiness; do not infer readiness from this class existing.

Reserve with a stable server-authorized scope, proposal ID, caller's idempotency key,
owner ID, structural revision, and execution deadline. Only the key digest is persisted.
The unique database constraints bind one execution to a proposal and one scoped key to
one binding. Resolve a replay and compare the proposal/evidence fingerprints before
applying the proposal's initial expiry gate. Same key with changed binding conflicts;
a second key for a consumed proposal returns its existing execution. A timeout or
ambiguous reservation commit requires scoped readback and must never mint a replacement
key or execution.

For the B3 candidate synchronous composition, `JdbcBulkDurableExecution.advance(
reservation, admission, mutation)` takes only the protected reservation returned by
`reserve(scope, ...)` in the same host call; it is not a wire credential or an extra
subject-authorization gate. Before even a terminal no-op, reject an ambient Spring
transaction. Under a bounded operational transaction and the existing control lock,
verify namespace, owner/epoch, immutable proposal/target-count binding, and the
reservation ordinal against durable `nextOrdinal`. The kernel may call `executeUnit`
to recognize an existing receipt or admission, but any replay ends that invocation;
a retry of A must never dispatch B. Only a non-replay result in `RUNNING` permits the
next ordinal. A fresh unit may invoke admission; only `admit()` permits mutation.
Receipt/admission replay invokes neither callback. Keep each
unit's own transaction and remaining budget, stopping on terminal, cancel, stop,
uncertainty or replay, including lost ACK on the second of three units. Do not add
automatic retry/recovery or a transaction around the whole sequence. The host
retains the execution UUID and projects results through the authorized durable
reader, not a synthetic suffix. Verify the Metadata PostgreSQL advance cases and
both host HTTP consumers against the exact candidate or released artifact; a
passing kernel candidate alone does not establish published adoption or HTTP readiness.

Call `executeUnit(control, expectedOrdinal, admission, mutation)` for one explicitly
identified unit. Do not implement a host-local `executeNext` loop that dispatches B
from a retry of A. The kernel commits a durable attempt barrier before running the typed
`BulkUnitAdmissionCallback`, then runs the domain `BulkUnitMutationCallback` only for
`BulkUnitAdmission.admit()`. Denied/invalid/conflict outcomes are persisted per ordinal;
`stop(reason)` closes the execution and prevents the suffix. The mutation callback's
return is limited to `BulkUnitMutationResult.confirmed()` or `unchanged()`; it is
provisional until the append-only receipt and domain mutation commit together. Admission
and mutation callbacks run within the unit transaction after the durable barrier and
control/receipt checks. Keep domain repository work on the bound manager/datasource and
verify this with an independent PostgreSQL observer. Never use `REQUIRES_NEW`, another
datasource, manual commit/rollback, or an external irreversible call inside either
callback.

The kernel persists one absolute deadline per attempt before admission, bounded by both
the execution deadline and the configured unit budget. Pass the callback a monotonic
remaining budget derived from the database deadline; do not restart a fresh timeout for
Config policy, grant, pool acquisition, target locking, mutation, or receipt work. Every
external read must consume only the remainder and fail closed when less than its minimum
usable interval remains. Bound idle transactions as well as statements so waiting in a
separate Config/grant pool cannot leave the API transaction open for unbounded time.
Before invoking a domain mutation, re-check the durable unit deadline. A confirmed receipt
replay is different: read the receipt before rejecting on expiry, because an already
committed effect remains confirmed after its deadline.

When proving a received remaining budget under lock contention, keep the real blocker
held until the waiter finishes and correlate PostgreSQL waiter/blocker PIDs and the
intended lock phase. Cancellation alone, or merely observing calls to the budget
supplier, does not prove the received budget was applied: an ordinary longer timeout
can produce the same cancellation. Use an oracle that distinguishes the smaller
received remainder from a restarted timeout, such as a calibrated monotonic upper
bound with explicit scheduling tolerance or observed JDBC timeout configuration.
Verify rollback and unchanged domain state; do not advertise a local timing oracle
as a precise deadline or HTTP SLA. A controlled test-only counterexample using the
ordinary timeout can validate that oracle; restore the accepted source exactly and
rerun the positive focal before accepting evidence or packaging classes.

The separate ACK/readback/recovery transaction must have its own short statement and row
lock limits (at most one second in the current contract). If it cannot acquire the control
row, preserve the receipt and return a reconcilable/unknown outcome; never call the domain
callback again or dispatch a suffix. Retrying that ordinal after the lock clears must read
the receipt and acknowledge it once. These database limits bound lock/statement waits, not
network failure or physical COMMIT acknowledgement time; ambiguous commit still requires
receipt reconciliation rather than an assumption of rollback.

The admission callback is the host's per-item gate: re-evaluate the currently authenticated
binding/grant and governed policy, then lock/read the domain target and compare its state
and expected version before allowing mutation. A receipt or durable item decision is
resolved before gates that apply only to a new mutation; confirmed effects remain
readable after proposal expiry. Config and the operational database do not share a
distributed transaction: Config is a bounded admission read, while the operational
database atomically commits domain state, transition audit and Metadata receipt.

For a host that shares one concrete domain decision between an item command and a
bulk unit, keep its inputs as immutable copies of authorized facts and parameters.
Capture the server-selected `evidenceDate` once in the protected evaluation plan;
confirmation reads that date from the persisted plan, not the wall clock or client
payload. Preparing that plan must not mutate domain rows. At admission, recheck the
current grant and recompute the decision from freshly protected facts. For a
current-department scope such as absence coverage, recheck each referenced parent's
current department and lock the grant before sorted parent IDs and then child IDs.
Bound JPA/JDBC waits and independent policy/grant reads by the callback's
remaining budget, including a usable floor before starting another read. Apply the
domain append and Metadata receipt on the same physical transaction; consult an
existing receipt before gates for a new mutation. This composition uses the published
kernel and policy contracts, not a host-local receipt or Config schema.
For the Quickstart example, inspect `praxis-api-quickstart/src/main/java/com/example/praxis/apiquickstart/hr/service/AbsenceCoverageDecision.java`
and `FeriasAfastamentoService.prepareCoverage`/`applyCoverage`; use
`praxis-api-quickstart/src/test/java/com/example/praxis/apiquickstart/config/BulkAbsenceCoverageHttpTest.java`
as the focused HTTP proof of the composed path.

For protected result reads, authorize the complete retained target set in the same
read-only snapshot as the result page. In a current-department scope, bind the current
grant and coverage to both the captured parent and any changed current parent, plus
each referenced parent; missing rows or reduced coverage deny the whole set without
partial output. This does not replace a domain's historical-assignment policy, such
as payroll's competence-based scope. Keep private notes out of authorization
fingerprints and public diagnostics.

A lost COMMIT acknowledgement is not a domain failure. Stop later ordinals and reconcile
through the durable receipt/control under lock. A valid earlier receipt remains readable
after deadline and even when later execution state requires reconciliation. Replaying an
ordinal already inside the acknowledged prefix, or replaying under
`RECONCILIATION_REQUIRED`, is read-only: it neither calls the callback nor advances progress.
A receipt for exactly `nextOrdinal` in `UNIT_COMMITTED_PENDING_ACK` may acknowledge that
already committed unit and advance progress once, but it never calls the callback again.
Recovery obtains the same row lock, fences
old owner/epoch controls, validates receipt/attempt/ordinal/target/version correspondence,
and performs no domain mutation. Contradictory evidence remains blocked for operator
reconciliation; absence alone is not proof of failure unless receipt atomicity and fencing
exclude every earlier writer. When recovery finds an invalid receipt, retain the contiguous
verified receipt prefix as the safe replay boundary: an intact receipt before that boundary
may be read, while the inconsistent receipt and every later ordinal stay blocked. Prove both
replay of an earlier valid receipt and rejection of the corrupted pending receipt without a
callback. Preserve terminal timestamps on repeated recovery.

## Cancel A Durable Bulk Execution Without Reopening Mutation

The V10 cancellation design is a candidate until its Metadata PR is integrated and published;
verify the exact source revision before using this guidance for adoption. It makes cancellation
a Metadata-owned durable command, not a host-local interruption or an HTTP promise. Inspect
`JdbcBulkDurableExecution.requestCancel`, the execution snapshot,
V10 migration, `BulkExecutionMigrator`, `prepare`, `applyAndReceipt`, ACK and `recover`
together. The host supplies a current trusted scope before calling the protected kernel;
the cut creates no endpoint, reader, action/capability, worker, `READY` signal, or host
authorization substitute. Cross-scope lookup must fail without enumerating an execution.

Persist `cancel_requested_at` once from the database clock. Terminal executions return their
current terminal snapshot without a write and a repeated request returns the existing marker.
Only a response after commit is an admitted request; lock timeout or an ambiguous commit is
`RECONCILIATION_REQUIRED` until scoped readback, never a successful cancellation claim. A
`RUNNING` execution with no active attempt may terminalize in that same transaction only
when the verified prefix and the absence of suffix effects are proved. Otherwise retain the
marker and project `CANCEL_REQUESTED`. `RECONCILIATION_REQUIRED` has public precedence over
the marker; proven terminal evidence has precedence over `CANCEL_REQUESTED`.

Use one lifecycle lock helper in this exact order whenever cancel or recovery may
terminalize: namespace binding `FOR SHARE`, operation control `FOR SHARE`, deployment bucket
`FOR UPDATE`, subject bucket `FOR UPDATE`, proposal `FOR UPDATE`, execution `FOR UPDATE`,
then receipt/admission. Recheck scope, binding and epoch after the locks. This helper must
not require operation control `READY`: cancellation and reconciliation remain available while
`SUSPENDED`. Do not reuse `BulkQuotaLedger.lockProposal()` if it enforces readiness, do not
add bucket locks after an execution lock in `recover`, and never lock a domain target merely
to admit cancellation.

Read receipt/admission before any new-mutation gate. `prepare` tests the marker only before a
new attempt, and `applyAndReceipt` rechecks it under the execution lock before admission or
the domain callback. If cancellation wins in that gap, no callback runs. If the domain
transaction already holds the row, cancellation waits, then observes its committed receipt or
rollback; it never compensates a confirmed effect. A committed receipt with pending ACK may
advance its already-confirmed prefix, including a V9 ACK, but it must not admit the next unit.
If that ACK completes `targetCount`, normal `COMPLETED`/`COMPLETED_WITH_ERRORS` wins; with a
proved excluded suffix, V10 may close `STOPPED` with `CANCELLED_BY_USER`. Unknown or
contradictory evidence remains `RECONCILIATION_REQUIRED`, with no callback retry and no
`CANCELLED` assertion.

The V10 physical fence complements Java checks for mixed versions: forbid a new
`RUNNING`→`UNIT_IN_FLIGHT` transition after the marker, prevent later receipt/admission that
would defeat a marker, preserve ACK of evidence already committed, and reject an old writer
that changes a marked execution to `STOPPED` for another reason. Do not treat triggers as a
replacement for lock/recheck logic. Add `CANCELLED_BY_USER` to persisted reason checks and
guards; it requires `STOPPED`, a proven incomplete prefix, no active attempt and complete
terminal evidence. V5's terminal trigger releases active allocation exactly once in the same
commit. Rollback retains both allocation and prior marker state.

Prove same-key/same-binding and conflicting races with two kernel instances and
independent database connections; two keys for one proposal; JDBC and JPA commit/rollback;
replay before new-mutation gates; lost COMMIT acknowledgement and confirmed rollback;
retry A after B and after deadline; recovery racing an open unit; old epoch rejection;
corrupt receipt handling; migration upgrade and restricted grants. An authorized replay
whose retained tombstone proves that detailed terminal evidence was purged is a distinct
`RESULT_PURGED`/410 condition, not the ordinary key/proposal `CONFLICT`/409; keep the
lookup bound to the same current namespace, subject, resource and operation scope. Use
the shared versioned idempotency digest helper so migration fixtures and runtime cannot
silently drift in framing. Use
`BulkDurableExecutionPostgresTest`, `BulkDurableMigrationPostgresTest`,
`BulkEvaluationStorePostgresTest`, and `JdbcBulkProposalStorePostgresTest`. These prove
the Metadata kernel only: a real host callback still must demonstrate domain invariants,
current policy/admission for each unit, external effects, and the host's actual transaction
composition before a business workflow is exposed. Do not treat a returned status as
proof that the caller was authorized.

## Enforce Durable Bulk Capacity And Retention

Quota is a transactionally maintained lifecycle ledger, not a preflight count or
an in-memory throttle. The current bounded profile allows at most 100 pending
proposals per deployment, 10 pending proposals per authenticated subject within
that deployment, and 80 active executions per deployment. Proposal insertion
locks namespace binding, operation control, deployment bucket, and subject bucket
before checking limits and inserting both proposal and pending allocation.
Reservation resolves a matching durable execution before new-work capacity gates,
then locks those governance/bucket rows and the proposal before converting pending
capacity to active capacity. A second idempotency key cannot consume one proposal
twice.

Terminal acknowledgement releases the active allocation in the same transaction
as terminal status/evidence. Unknown commit, an active owner, or incomplete evidence
retains capacity. A restricted `praxis_bulk_retention_executor` may invoke one-item
`expire_unconsumed_proposal` and `purge_terminal_execution` operations; it receives
no direct table mutation grants. Expiry removes only an unconsumed expired proposal
and its pending allocation. Purge accepts complete terminal evidence older than the
fixed retention interval, writes a minimal idempotency tombstone first, then removes
detailed proposal/execution/evidence and allocations atomically. Tombstone replay
returns the distinct `RESULT_PURGED` outcome after payload deletion. The database controls the immutable
terminal timestamp; never accept a caller-provided retention clock.

For a V10 user-cancelled `STOPPED`, purge writes `terminal_status='CANCELLED'` in the
minimal tombstone; historical non-user `STOPPED` rows remain `STOPPED`. Keep payload, target
and free-form reason out of the tombstone and preserve replay denial. The V10 migration and
`BulkExecutionMigrator` must validate the new column, immutable/check/transition guards,
purge mapping, function bodies/owners and exact runtime/retention/control ACLs. Run the
privileged migration and validator explicitly; do not add automatic DDL or broad runtime DML.

Migrate with explicit namespace-to-deployment bindings and exact configured runtime,
retention, and control-plane roles. V5 is already an applied migration: never edit its
SQL/checksum to change privileges. V6 adds the operation-control privilege boundary and V7
adds the descriptor fence, so verify a V5→V6 upgrade keeps the stored V5 checksum and exercises
the same ACLs as a fresh V1→V7 install. Validate physical catalog ownership, memberships, narrow
table/column/function grants, mutation-protection triggers, and fixed definer
search_paths; reject inherited PostgreSQL roles outside the declared retention
membership closure (including predefined roles such as `pg_write_all_data`); a valid Flyway checksum alone is insufficient. Prove the retention
functions under the effective restricted executor and control functions under
separate runtime/control-plane logins in PostgreSQL, not only by catalog inspection.

V6 runtime roles call lock_operation_control through EXECUTE and receive no direct
SELECT or UPDATE on praxis_bulk_operation_control. The SECURITY DEFINER lock holds a shared row
lock to transaction end; a governed transition waits for earlier admitted transactions
before suspending the operation. Separately configured controlPlaneGranteeRoles receive
EXECUTE on the generation-CAS transition only, never table DML or membership in
praxis_bulk_control_owner. That owner is NOLOGIN/NOINHERIT with no members and minimal
column grants. V6 keeps its trigger guards inside the same narrow owner boundary.
Treat this as the durable fence substrate only: CAS accepting READY does not prove the
descriptor was composed, its providers/schemas are valid, or its fingerprint matches
the local snapshot. Publish READY or advertise an action only after the full S4c
composition and runtime comparisons are implemented and tested.

V7 binds each proposal and execution to the exact descriptor generation, fingerprint,
and structural revision that authorized it. Insert guards reject old writers that omit
the current tuple; historical rows remain unbound and never receive mutation authority
through backfill. For a unit, resolve an existing receipt/admission replay first, then
lock operation control before the execution row and require the persisted tuple to
match the live V6 control row, protected proposal tuple, and execution tuple at
preparation and again before the domain callback. Keep that shared lock
through callback and receipt commit: suspension that wins between preparation and
apply prevents callbacks, while a unit already inside the transaction completes
atomically before CAS can suspend. Replaying confirmed evidence and recovery stay
available under suspension; recovery never invokes domain callbacks. Prove this fence
with PostgreSQL two-connection tests for both CAS interleavings, stale generation after
READY is republished with the same fingerprint/revision, receipt replay while suspended,
legacy null tuples, and least-privilege trigger-owner column grants.

V8's private ordinal manifest is an index over protected evaluation evidence, not
an execution result or permission grant. Before readers use it, prove every ordinal,
wire identity, expected version and digest matches the immutable evaluation. Use
lossless bytes for wire identity/version and a compact framed identity digest; do
not parse protected JSON through PostgreSQL `jsonb` or index a long wire ID
directly. `insertEvaluated` writes proposal, evaluation, manifest and pending
allocation in one transaction. A deferred guard rejects older writers that omit
the manifest; drain those writers for the cutover and prove full rollback on a
mixed-version attempt. Upgrade V7→V8 with exact existing runtime roles/grants;
fresh installation provisions roles after migration and validates before use.
The V8 bootstrap marker permits backfill and focal manifest grants only while
`PENDING`, with the configured runtime grantees matching actual evaluation
grantees before `COMPLETE`. After `COMPLETE`, missing rows or revoked grants are
drift to reject, never material to regenerate. The marker is private to its
schema owner; even retention owner/executor must have no direct grant on it.
Preserve quota release and
retention deletion order. Prove NUL/long wire values, 10,000-target boundary,
retry after failed bootstrap, no healing, restricted PostgreSQL owner/roles,
expiry and purge. This storage cut alone publishes no reader, endpoint or READY.

## Prepare A Safe Evaluation Preview Candidate

The V9 preview storage is integrated in Metadata source, but availability in a
host still depends on the exact published starter revision. Verify that revision
before relying on these types or tables. V9 adds a provider-approved public
projection by **ordinal**, alongside
the protected evaluation and V8 manifest. It is neither an execution outcome,
an authorization decision, nor permission to expose a reader. The protected
evaluation remains the replay authority.

For a typed evaluation, the provider must choose one of two deliberate paths in
the same transaction that inserts proposal, evaluation, manifest, allocation and
quota: persist a `COMPLETE` projection, or persist `UNAVAILABLE` with no public
row. A complete projection preserves only the protected eligibility decision and
the order/count of diagnostic categories and codes. It replaces diagnostic text
only through a versioned provider allowlist; it never copies target identity,
facts, plan, protected text, target pointer, metadata, or an unlisted diagnostic.
Bind the stored rows to the exact evaluation fingerprint and manifest ordinal,
and validate a canonical digest over the revision, allowlist, decisions and
per-ordinal public payload. Do not derive a “safe” result by serializing the
protected blob or by redacting it after the fact.

Enforce the item-state fence in PostgreSQL before every target-preview INSERT:
the parent preview state must already be `COMPLETE`. Later SQL must therefore
fail closed when it tries to add an item under `UNAVAILABLE` or
`UNAVAILABLE_LEGACY`. Do not teach an explicit `FOR KEY SHARE` lock for this
runtime path: the least-privilege runtime role does not receive the `UPDATE`
privilege that PostgreSQL requires for that lock. Use the composite referential
binding to the parent state so a concurrent retention/purge delete cannot leave
an orphan item; prove both a later transaction and an insert-versus-delete race
in PostgreSQL.

Legacy evaluations lacking typed eligibility are `UNAVAILABLE_LEGACY`, never
silently backfilled into public items. A legacy or otherwise unavailable preview
is an explicit storage state with no per-target rows; it is not `READY`,
`BLOCKED`, a page with guessed emptiness, or a reason to weaken current
authorization. Preserve the states exactly: `COMPLETE`, `UNAVAILABLE`, and
`UNAVAILABLE_LEGACY`.

Treat V8→V9 like the V8 cutover: drain writers that cannot create preview state,
migrate/backfill only the safe state permitted by immutable evidence, validate
the exact role/grant closure and physical rows, then reopen admission. A failed
bootstrap may retry only before its durable completion marker; after `COMPLETE`,
missing preview state for any evaluation, missing target rows for a `COMPLETE`
projection, digest drift or revoked grants are faults to reject rather than data
or ACLs to heal. For `UNAVAILABLE` and `UNAVAILABLE_LEGACY`, zero items is the
invariant; an item is corruption, not a missing-row repair request. Retention
and purge must delete preview rows in the same
referential/quota-safe order as their proposal; the restricted retention executor
receives no new direct preview mutation privilege. Prove all of this in PostgreSQL: complete
allowlisted projection, unlisted/private-diagnostic rejection, ordinal/digest
tampering, late target-preview rejection, insert-versus-retention/delete race,
full transaction rollback, V8→V9 legacy state, retry/no-heal, least-privilege
ACL drift, expiry and purge.

This candidate deliberately ships no proposal-results reader, secure cursor,
HTTP route, action/capability, execution reader, or READY claim. A host still
needs a real current-grant/domain authorizer before it can expose any result, and
the later reader must perform its own scoped authorization and cursor proof.

For V11 preview integrity, verify the exact Metadata source revision before
relying on the storage. Keep the V9 global projection digest as the full audit
in the migrator's privileged bootstrap and `migrate`/`validate` scan. In the
evaluation transaction, derive each versioned
item checksum from the exact persisted V8 manifest identity/version/digest,
V9 parent context, ordinal, decision and allowlisted diagnostic bytes. Freeze
the binary framing with an independent golden vector; writer and validator
using the same helper alone cannot reveal symmetric format drift. A future
RS2 reader may verify only its bounded `size+1` items inside the same scoped
`REPEATABLE READ READ ONLY` snapshot; it must not rehash the whole proposal or
decode protected evaluation for each page. Bound aggregate page bytes as well
as row count. The checksum relies on ACL and immutability, not on secrecy of
SHA-256; the schema owner is outside this runtime threat model. V11 does not
provide that reader, a cursor, HTTP authorization or `READY`.

The internal RS2 page reader below is integrated in Metadata source at merge
`17d102ec69c5e00c4b75101ad8c6f0f9652bb228`, but is not published. Do not
present it as available in the host before adopting a published revision. Inspect Metadata's
`BulkPreviewPageReader`, `BulkPreviewItemIntegrity`, `BulkExecutionInfrastructure`
and `docs/spec/BULK-H1B-READ-MODEL.md` at the exact source revision before
using the path. Keep the reader package-private and its result out of JSON/HTTP.
Use the existing scoped `withConsistentRead` transaction, physically
`REPEATABLE READ READ ONLY`, for parent/evaluation state, V8 manifest, V9
preview and V11 leaves in one snapshot. Before reading the header, call the
V12 governed `SECURITY DEFINER` gate on that connection and require exactly
one `true` result: V11/V12 bootstrap must both be `COMPLETE`. Runtime must
not get marker-table `SELECT`; missing function/grant, altered owner/body/ACL,
`PENDING`, false/null/duplicate result or SQL failure closes the read. Include
the V12 function in live role/ACL/body attestation, not only startup validation.
The V12 grant-once bootstrap is privileged and must never repair drift after
`COMPLETE`. Page by manifest ordinal with an
exclusive lower bound, immutable `targetCount` watermark, size 1–200 and
`LIMIT size+1`; missing preview/leaf, duplicate or noncontiguous ordinal,
binding mismatch and checksum drift are corruption. Verify diagnostics against
the versioned public allowlist. Never return wire identity, expected version,
target digest, protected evaluation, facts or plan. Distinguish absent,
not-evaluated, `UNAVAILABLE` and `UNAVAILABLE_LEGACY` internally, and reject
ghost rows; none of these states chooses a public HTTP status before the
host's current authorization.

Budget every selected header and row column in bytes, including manifest
fields, digests/fingerprints, fixed-size fields and the extra lookahead row, as
well as row count. V8 permits large wire/version values: configure JDBC fetch
size before query execution as a bounded-fetch strategy; prove PostgreSQL heap
behavior separately because fetch size and a payload counter are not a heap
guarantee.
The conservative fetch size may cost one round trip per row; benchmark page
latency and the full privileged startup scan on representative data before
release or public API. A budget refusal is fail-closed, not a truncated page.
Prove PostgreSQL 10,000-target keysets, exact byte-budget boundary and
lookahead overflow, V11/V12 `PENDING` denial, tampered diagnostics/leaf/manifest,
legacy/unavailable ghost rows, cross-scope invisibility and purge concurrency;
reuse RS3's JPA/read-only infrastructure proof if that plumbing is unchanged.
This internal reader does not supply an authenticated cursor, granular host
authorization, endpoint, capability or `READY`.

## Compose A Protected Capture In The Host

For a host entry point whose result must mean the protected capture committed, inspect
`EventosFolhaApprovalProposalService` and its focused unit/PostgreSQL HTTP proofs in
Quickstart. The store only participates in an existing transaction. Make ownership
explicit: reject an ambient transaction/synchronization, capture fresh authorized
input outside the write transaction, then insert input and evidence together in a
local transaction using the exact operational datasource/manager. Do not silently
suspend the caller's domain transaction or return a participant result as committed.
A deliberately participating internal API must instead document its provisional result.

Use the evaluator's clock and check validity before and after insertion. Translate
storage and commit failures without protected causes; a failed or ambiguous commit
must not be reported as success. This capture has no idempotent receipt: a caller
must not assume a retry is deduplicated. Elapsed validity after commit does not undo
storage and never grants permission to execute.

`TransactionTemplate.setTimeout` alone does not apply query timeouts to the store's
manually prepared JDBC statements. In this PostgreSQL adapter, the host can apply a
server-owned `SET LOCAL statement_timeout` through `BulkExecutionInfrastructure`
on the same transaction connection before storage calls. Keep the limit local to the
transaction, not the pool/global configuration. It bounds each SQL statement; do not
advertise it as a total request deadline or a guaranteed COMMIT timeout. Prove a
concurrent lock times out safely and rolls back both rows using real PostgreSQL.

Recover a stored evaluation only through fresh trusted scope and current grants.
When comparing a separately captured request, require equal input fingerprints first,
then compare current context, TTL, facts/plans and governance. Equivalent evidence may
still describe blocked targets: true is not eligibility, READY, admission or execution.
Prove changed parameters, revocation, other subjects, expiry, policy/fact drift,
companion failure, deferred COMMIT failure and absence of domain writes. Migrate and
validate the canonical schema with a separate privileged identity; runtime gets only
the documented bulk SELECT/INSERT grants and necessary domain reads.

## Bind Domain Evaluation Evidence Before Readiness

Use `BulkTargetEvidence` with the existing canonical wire BulkTarget/expectedVersion,
observedVersion, minimal exact-number facts and the evaluated candidate plan.
`BulkEvaluationSnapshot(proposal, evaluatedAt, targets, governance)` requires exact original target
coverage and versions, normalizes evidence order to the input (including per-item order),
and binds UUID/input fingerprint/validity/instant/facts/plan/governance with the distinct
`praxis.bulk.evaluation/1` frame. It does not produce eligibility, public totals or READY.
A different observed version is a recorded conflict fact, not permission to proceed.

The host/provider supplies authoritative, minimal domain evidence and dependency
revalidation/locking semantics. Do not store full domain state by default, fabricate
facts for inaccessible targets, or encode policy absence as an allow boolean. Config
remains the owner of operational policy resolution; readiness awaits governed provider
composition, real current grants and current-context revalidation.

Capture mandatory `BulkEvaluationGovernance` from the trusted evaluator revision,
current authorization fingerprint and nonempty `BulkPolicyObservation` list. Observations
retain tenant/environment, canonical Config layer/type/key, opaque resolution state,
resolution fingerprint and observedAt. Metadata rejects duplicate coordinates and binds
this evidence; it does not interpret Config states, duplicate policy payload/head identity,
or check provider target completeness. The host must validate the full Config resolution
and all required targets, including an explicit lookup for NEVER_APPLIED. Do not fabricate
revocable grants from a JWT or static authority catalog. A test fingerprint is not a
production authorization provider. Multiple observations require consistency proof from
their owner, not an assumption of atomic multi-target Config reads.

`matchesCurrentEvidence` compares the full trusted current context, validity window,
target evidence and governance using `praxis.bulk.revalidation/1`; only observation and
evaluation timestamps are excluded. A loaded integer and the same fresh integer must
compare equal even if Jackson uses different integer node classes; integer and decimal
remain distinct. Use canonical typed digests, never JsonNode.equals for this comparison.
It performs no reads and cannot detect reused stale observations. Call only after fresh
policy/grant/domain reads and checks; true is not permission/READY. Invalid current shape
throws validation errors which the orchestrator must treat as an impediment; context/TTL
mismatch returns false. Re-evaluate under a new UUID when evidence changes.

For a host's per-unit admission, compare a closed, typed set of protected facts and
plan fields, including field presence and exact integral values. The published codec
may load an integer as `BigInteger` while the fresh value is `Integer` or `Long`; prove
the comparison across that round trip without equating integers to decimals. Do not
recapture other targets inside one unit merely to call full-snapshot
`matchesCurrentEvidence`, or add a general JSON-semantic equality rule.

When evidence comes from a separately recaptured snapshot, first require its protected
`BulkIntentSnapshot.fingerprint()` to equal the stored proposal's intent fingerprint,
or reconstruct the capture exclusively from the stored proposal input. The comparison
method reuses the original intent and cannot detect changed parameters from current
targets/governance alone. Prove equal-input fresh evidence compares equal, changed
grants/facts invalidate it, and a parameter-only change fails the input guard. A new
snapshot's overall fingerprint differs because UUID/timestamps differ; that inequality
alone is not proof of changed authorization or domain evidence.

The SDK beta constructor has no compatibility path without governance. Old evaluation
payloads without it are CORRUPT even with an otherwise valid old hash; recover input only
to obtain a new governed evaluation. Do not rewrite immutable evidence or invent history.
V1/V2 SQL checksums remain unchanged. Prove BulkGovernanceEvidenceTest and the PostgreSQL
legacy/readback cases in addition to the existing suite.

`JdbcBulkProposalStore.insertEvaluated` inserts input plus evidence atomically in the
existing physical transaction; no attach/update/upsert. Re-evaluation needs a new UUID.
`findEvaluation` scope-checks the input and verifies the protected companion binding;
missing evidence is not reconstructed, corrupt linkage is not a fallback to input.
Those public store calls use separate observations and do not establish an atomic
proposal/evaluation read. The internal RS1 `BulkProtectedProposalReader` is integrated
in Metadata source at merge `712eb13f1bad382b8cb6f4a57ae619d24e8e7c1b`,
but is not published; verify the published revision before host adoption. It
shares the existing protected decoders inside one physical
`REPEATABLE READ READ ONLY` snapshot, scopes by namespace, historical subject,
resource and operation, and distinguishes internal absent, not-evaluated and
evaluated observations. A proposal without evaluation must not have manifest,
preview or integrity dependents; corruption fails closed without protected
payload in diagnostics, and SQL/ACL/timeout failures are unavailable. The
package-private observation is not a response DTO and must stay opaque to
Jackson, logs and `toString`. Do not infer creator-versus-delegate permission,
current target/field/reference grants, retention HTTP status, or `redactedIntent`
from the snapshot. The provider must project domain-safe intent/evidence, and
the host must authorize the entire historical set before a public RS1 route.
Prove the same-snapshot unconsumed-proposal expiry race, cross-scope absence, blob corruption,
revoked read grant and serialization boundary against real PostgreSQL. No
HTTP/cursor/capability or `READY` follows from this reader alone.

The EventosFolha approval projector owns only the domain intent projection;
the canonical RS1 facade composes authorization and the proposal DTO. Its
`redactedIntent` is deliberately
only `{selection:{mode:"EXPLICIT",targetCount:<certified full historical count>}}`.
The count must match the complete immutable certified target set; never compute
it from an authorized subset. The projector accepts only its exact historical
producer tuple: `DOMAIN_COMMAND`, integer identity codec, the fixed resource and
operation group/id/path/POST binding, `PER_ITEM`, a syntactically valid
lowercase 64-hex historical schema digest, evaluator revision
`eventos-folha.approval-evaluation/2`, synchronous explicit selection, and the
exact supported input/selection/target shapes with typed eligibility on every
target. Compare against this semantic producer tuple, not today’s descriptor or
schema hash; valid old schema digests remain projectable. Incompatible shapes,
legacy evaluations without typed eligibility, or uncertified counts fail
closed—do not substitute `{}` or a reconstructed preview. No permission to
reveal parameters, IDs/versions, facts, plans, business values or policy
references follows from `PAYROLL_APPROVE` or from hiding a field in this
projection. The projector emits only `redactedIntent`; it does not compose
evidence or diagnostics. The RS1 facade uses empty evidence under the current non-disclosure policy
and derives diagnostics only from the
persisted allowlisted preview projection, never protected message, target or
metadata values. These rules belong to the facade, not the intent projector. A retained
expired proposal maps to 410 only after current full-set authorization; removed
proposals remain 404. The projector itself makes neither decision. Authorized
facade adoption and HTTP remain separate gates; the facade must retain its
PostgreSQL expiry/auth proof. This work does not expose an endpoint, certify `READY`, or
complete the P1 protocol.

For the canonical authorized RS1 composition, inspect
`BulkAuthorizedProposalReader`, `BulkProposalProjectionProvider` and the
concrete host projection provider together. Bind the pure projection provider
by exact resource/confirmation-operation and revision; it supplies only
redacted intent and does not authorize or query current domain/Config state.
Do not compose through `find` plus a separate `findEvaluation` transaction.
Global grant, protected lookup, full historical target authorization and public
projection must share the Metadata-owned REPEATABLE READ read-only snapshot.
Expired retained proposals are GONE only after full authorization; a missing
or removed proposal has no reconstructed execution tombstone.

Validate the complete persisted V11 preview with bounded internal pages,
matching each ordinal, wire identity, decision and diagnostic category/code
sequence to typed historical eligibility. Public text comes from the persisted
allowlist. Aggregate at most64 distinct category/code/text triples without
truncation; target and metadata stay empty, and evidence remains empty under
this cut's explicit non-disclosure policy. Legacy or unavailable/incompatible
projection after full authorization is UNAVAILABLE, not an invented BLOCKED
proposal or the RS2 preview409. Pre-authorization corruption stays the same
non-enumerating absence as missing/denied.

Preserve both the monotonic3s publication budget and conservative20MiB total
preview selected-byte limit, including repeated page headers/lookahead. The
protected lookup retains its own codec/storage byte bounds and is not included
in this preview budget. Constrain SQL
by remaining time before every page and recheck after transaction completion.
Discard COMPLETE if proposal validity expires before publication; do not turn
403/404 into GONE. These limits can deny availability and are not a corporate
SLA, total process-memory limit or promise of absolute query cancellation.
Prove paginated aggregation, semantic corruption, decoded legacy, full-set
revocation/retention in one snapshot, expiry and late completion with real
PostgreSQL before accepting the facade. Validate the concrete host against the
exact controlled candidate artifact, then publish/adopt only at the authorized
release milestone. A Java reader and bean wiring do not expose an HTTP route,
capability or READY, and do not close the backend gate for Angular.

Migration V2 preserves V1, adds the immediate composite FK and immutable companion table;
runtime needs SELECT/INSERT on both. One bounded payload (8 MiB) is not proof of efficient
paged/per-item execution. Review access/indexing with those future consumers.

Prove BulkEvaluationSnapshotTest and BulkEvaluationStorePostgresTest, including V1→V2,
exact typed coverage, numeric limits, corruption, concurrent conflicting evidence,
observer-before-commit and caught companion failure rolling back both rows. See Metadata
docs/spec/BULK-EVALUATION-EVIDENCE.md; do not expose these protected values as public results.

## Prove The Command Under Stress

Prove permitted execution; denied state/authority; validation failure; same retry;
different conflicting command; stale/missing `If-Match`; result/status schema;
action/capability/`_links` alignment; and no repeated external side effect. For collection
commands, prove mixed outcome and atomicity/ordering rules.

For the private V16 `ATOMIC` bulk candidate, inspect the canonical
`praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/bulk/`
sources `JdbcBulkDurableExecution.java`, `BulkExecutionResultsReader.java`
and `BulkExecutionMigrator.java`, plus
`praxis-metadata-starter/src/main/resources/db/praxis-bulk-migrations/V16__bulk_atomic_set_execution.sql`
before asserting a contract. Verify whole-set
admission before mutation; one bounded transaction for domain writes, outbox,
one receipt header and ordered child evidence; and rollback of all of them
when the last target or evidence append fails. The current candidate bounds
the entire set to 50 targets and one aggregate five-second unit deadline,
including evidence append. A commit with lost acknowledgement requires
receipt-first recovery without invoking the mutation again. Absence of a
receipt after an uncertain commit, while the active deadline is still open,
remains `RECONCILIATION_REQUIRED`; only a fenced post-deadline recovery may
certify that absence. The reader must publish zero children until the whole set is
certified, then the complete ordered set, never a partial prefix. Compare
these guarantees with `praxis-metadata-starter/src/test/java/org/praxisplatform/uischema/bulk/`
`BulkAtomicExecutionPostgresTest.java` and `BulkDurableMigrationPostgresTest.java`;
a callback return or a green happy path alone does not prove them.

For V16 protected proposal metadata, preserve the opaque payload and fingerprint
byte for byte. PostgreSQL `json` operators can de-escape unrelated strings too;
changing `jsonb` to `json` alone does not preserve canonical escaped NUL input.
Inspect the migration's lexical-copy projection: replace escaped NUL with U+FFFD
only in the derived copy used to extract `atomicity`, then parse with `json`.
Never rewrite the stored payload, use a regex JSON parser, or convert the whole
opaque snapshot to `jsonb`, whose numeric/Unicode domain is narrower. Keep the
column non-null and use `IS NOT DISTINCT FROM` in the metadata CHECK so missing
or null metadata cannot pass through SQL UNKNOWN. Attest the exact catalog
expression. Prove real PostgreSQL upgrade/backfill and protocol-two inserts with
NUL in unrelated keys/values, literal backslash sequences, unchanged raw bytes,
invalid/missing/null/type-mismatched atomicity and invalid JSON/UTF-8. Use the
existing READY/publication tuple for insert fixtures, and a separate empty
database for catalog-drift tests; do not disable admission/delete guards to make
a synthetic snapshot pass full storage validation. Compare
`BulkAtomicProposalJsonConstraintPostgresTest` and `BulkEvaluationStorePostgresTest`.
This projection preserves the canonical codec language, not arbitrary JSON.

For V16 storage review, verify that the cutover suspends existing publication
and operation controls, new runtime grants on atomic evidence are limited to
the four evidence tables and required evidence function, and both `migrate` and
`validate` reject ACL drift after bootstrap `COMPLETE` without silently
repairing it. Historical protocol-one fixtures must use genuine historical
storage and must not fabricate post-cutover `READY`. This is candidate
guidance, not an assertion of public `READY`, a working host consumer, B4
completion, or exactly-once external effects. Those require their own
authorized release and consumer evidence.

For paged result/read APIs attached to a durable collection command, keep result
navigation separate from access control:

- Preserve the creator as historical owner where the command contract uses that
  identity, but authorize every read using the currently authenticated requester.
  Creation or confirmation authority does not grant permanent result-read access.
- A cursor proves only continuation position and the fixed result window. It must
  not authorize access; bind it to the stable requester and effective scope, then
  re-evaluate current operation and target/field/reference grants on every page.
- If the requester lacks access to any member of the immutable target set or any
  field/reference required by the response, deny the whole page. Do not filter,
  renumber, return partial totals, or reveal inaccessible identities.
- Compose authorization evidence and the result page from one coherent database
  snapshot, a server-owned verifiable attestation, or a change-detection scheme
  that fails closed. Separate `REPEATABLE_READ` transactions do not by themselves
  prove a shared snapshot.
- Prove delegated access only when the canonical contract explicitly permits it;
  otherwise prove that a delegate is rejected. In either case, test a cursor copied
  between requesters with equivalent grants, grants reduced/revoked between pages,
  authority-source failure, and concurrent permission/domain-scope changes. Compare
  status, body, headers, IDs,
  totals and links for absent, cross-scope and insufficient-coverage cases to
  prevent an existence oracle.

Use focused command execution, version-precondition, action catalog, capability, and
negative-path tests. Add quickstart HTTP proof for public commands and Angular action
runtime tests when metadata or precondition behavior changes.

## Companion Skills

- `praxis-java-availability-discovery-authoring`: action, availability, capability,
  and HATEOAS alignment.
- `praxis-java-resource-authoring`: operation and DTO/service boundary.
- `praxis-metadata-discovery-capabilities`: canonical action/capability discovery.
- `praxis-metadata-schema-contracts`: action schemas, ETag, and public headers.
- `praxis-java-contract-conformance`: evidence pack and Angular readiness.

Close with transition matrix, idempotency/precondition policy, outcome contract, stress
evidence, and platform gaps. A command is ready when retry, stale, and denied callers
all receive deliberate safe behavior.


## Compose Authorized Bulk Result Reads

For G3b proposal-results, use the Metadata-owned `BulkAuthorizedProposalResultsReader`,
`BulkReadCursorConfiguration` and `BulkProposalItemResult<WI>` with the host's concrete
`BulkReadAuthorizationProvider`. Verify the exact dependency first. A candidate
`SNAPSHOT` is not a published artifact: prove it with its distinct candidate coordinate,
an isolated Maven repository and an explicit host version override. Never replace bytes
under a published coordinate. For later adoption, wait until the required release resolves
from its intended repository, pin that exact `praxis.core.version`, use an isolated cache,
and remove the candidate override. Source integration and candidate tests do not prove
published adoption.

Fix the resource and operation through trusted host wiring. The `@ApiResource` resource
key and `CanonicalOperationResolver.requireResourceOperation` must identify the exact
GET mapping and its OpenAPI operation; continuation is bodyless. Do not add placeholder
handlers, infer operation identity from route text, or declare `READY` to exercise this
read path. The proposal-results handler does not create execution, cancel execution,
read tombstones, or make the bulk lifecycle ready.

The requester is the authenticated server principal. Preserve the proposal creator as
historical owner, but bind the cursor's effective authorization fingerprint to the
current requester as well as the host's full-set authorization result. Every page
reauthorizes every historical target, including off-page targets, in the same
Metadata-owned `REPEATABLE READ READ ONLY` snapshot as the protected evaluation and
bounded page projection. Missing evaluation, incomplete historical facts, reduced or
failed coverage, and copied requester/scope tokens must not fall back to creator
ownership, current domain state, or operation-wide permission. A small page never
reduces the set that must be authorized.

The host adapter must verify the bound `ConnectionHolder` before obtaining its
connection, join the exact operational infrastructure and physical connection, and
preserve the owner's transaction. Matching JDBC URLs or independent RR/RO transactions
do not establish one snapshot. Reuse the existing JDBC proxy's transaction timeout,
retain smaller SQL timeouts, and pass only the remaining monotonic budget to host work.
Include acquisition/setup, CPU and final publication in the budget; discard output if
the deadline elapsed after completion. This is a publication deadline, not an
instantaneous wall-clock cancellation promise.

Persist the explicit allowlisted preview atomically with evaluation through the
canonical store. Keep provider, evaluator and projector revisions distinct, changing
only the revision whose behavior changed. Execution expiry alone must not hide retained
results that remain authorized for reading.

The cursor is AEAD-protected, purpose-bound, requester-bound and fixed-window. Keep
claims internal. Require the same page size (1–200) on every continuation; do not
renew `issuedAt` or `expiresAt` when issuing the next token. Recheck token expiry after
the read transaction completes, before publishing the page. Configure an explicit
active key ID, AES-256 key set and positive TTL no greater than 15 minutes; provide no
default or ephemeral key and never expose or log key material or tokens. Provision the
new key on every replica before switching the active key ID, and retain old keys until
the maximum lifetime of their issued tokens has elapsed. Tests that construct a new
reader with the rotated key set prove reader reconstruction in one process, not an
operating-system process restart. Because the Metadata codec is stateless, the host
must protect issuance. The Quickstart host implementation reserves each possible
issuance against one durable ledger shared by exactly that database authority and
fleet; this is host operational policy, not a universal Metadata consumer contract.
Do not share that key material or ledger with another service, environment, or
independent database authority. Commit the reservation in its own `REQUIRES_NEW`
transaction before the reader's single RR/RO snapshot; authorization, protected
evaluation and page projection must share that immutable reader snapshot. Bind its
lifetime quota to SHA-256 of the
decoded 32-byte key material (not `kid`); cap it at 2^31 reservations per key material.
Build reader configuration and budget digest from the same immutable
`BulkReadCursorProperties.Provisioned` key-material snapshot; do not derive them
independently from mutable properties.
The reservation precedes cursor decoding and core protected SQL, and is never refunded, including
outer rollback, uncertain commit, invalid/denied reads, or final pages. An absent,
exhausted, expired or unavailable budget returns generic 503 before the reader. The
absolute reservation deadline limits admission, not subsequent encryption; the core
read deadline starts later, so account separately for host pool acquisition and
reservation commit. The host's candidate runbook uses a protected shared operational
database ledger and a bounded `outcome` metric (`reserved`, `denied`, `unavailable`)
without key, digest, user, proposal or token tags. Database restore/clone or lost/uncertain
ledger commits require fresh cryptographic key material before issuance resumes. These
controls are implemented in the candidate, but do not prove fleet provisioning,
monitoring/alerts or an operational exercise; record those and released-artifact
adoption separately.

Keep the public item contract exact: `BulkProposalItemResult` supports only String or
Integer wire identities; the concrete host API must prove its actual Integer identity
through OpenAPI. Each item contains only `id`, `decision` (`EXECUTABLE` or `BLOCKED`)
and safe diagnostics. `BLOCKED` requires diagnostics, `EXECUTABLE` has none, and public
diagnostics have null `target`, empty `metadata`, nonblank code/message and at most 16
entries. Do not emit ordinal, facts, plan, versions, digests, authorization fingerprints,
parameters, or generic before/after values. RS1 `BulkProposal.redactedIntent` is a
separate unresolved projection; do not imply this RS2 route exposes it.

Use the public status matrix deliberately: malformed/authentication-invalid cursors are
400 before protected SQL in the core when issuance reservation succeeds; if the host budget is unavailable,
exhausted or expired, its 503 gate precedes cursor decoding and the reader. Global
denial is 403 and global-authorizer unavailability is 503 before proposal lookup.
Proposal-specific storage failure before full authorization, absence,
incomplete set, other requester/scope/proposal or changed effective fingerprint all
produce indistinguishable 404 responses without page data. Only after the proposal is
live and the complete set is authorized may expiry or incompatible cursor shape/size
produce 412. An unavailable legacy preview on the first page is 409. Corruption after
authorization and operational/deadline failures are 503. Keep `Cache-Control: no-store`
and compare the negative response body and sensitive headers so the route is not an
existence oracle.

For the host proof, exercise the real HTTP/OpenAPI mapping and PostgreSQL-backed
authorization provider, not only an authorizer unit test or recording provider. Cover
delegated requester access, requester-copied cursor, grant reduction/revocation,
off-page denial, first/next page, changed size, cursor tampering/expiry, key rotation,
full-set privacy, status/body/header equivalence for negative cases, and the exact
Integer/bodyless OpenAPI operation. Metadata's continuation PostgreSQL tests prove
bounded same-snapshot paging and cursor reconstruction/rotation; do not describe them
as a process-restart proof. Distinguish candidate-SNAPSHOT host proof from tests against
the released artifact. A passing G3b result read does not prove execution, tombstones,
`READY`, Angular materialization, or RS1 redaction.
