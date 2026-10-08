---
name: praxis-java-command-concurrency-authoring
description: "Use when implementing, auditing, or migrating a Praxis Java business command with state changes or its internal durable bulk-read foundation: @WorkflowAction, command request/response schemas, ResourceCommandExecutionRequest and Result, idempotency, item or collection scope, resource version ETag, If-Match preconditions, conflict/denial outcomes, bounded execution-result paging, action availability, REPEATABLE READ read-only MVCC snapshots, durable writable proposal capture under control/grant locks, and safe Angular/runtime handoff."
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

1. Model a business transition with `@WorkflowAction`, stable ID, collection/item scope,
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
URLs or namespace labels. Prepare or explicitly reconcile the complete photograph through attested exact-group producer captures outside JDBC transactions. Ordinary readiness must not regenerate SpringDoc or use a configurable remote source as current authority; cold/stale replicas fail closed until explicit reconciliation. Bound structural reads within a unit use the same attested operational connection and no cache lock or REQUIRES_NEW. When one execution unit rechecks multiple strict MVC request bodies and group identities, run the whole structural recheck inside one `OpenApiDocumentService.withPublishedBulkOpenApiPublication` scope on its already-bound writable transaction, preserving the durable guard before and after the callback, the operation fence, and the unit budget. Do not nest that scope or use the photograph as a grant or policy cache. A mocked scope proves callback placement, not the durable publication guard; verify the real path through PostgreSQL and HTTP, and measure cost without treating one timing sample as a guarantee. A `READY` descriptor does not prove production host handlers,
domain authorization, or atomic domain-plus-receipt behavior.

For the private candidate's `BulkExecutionUnit.certifiedPrefix`, first verify the
exact distinct candidate JAR/version; Metadata rc.154 does not publish this API.
The kernel builds a contiguous ordered prefix from earlier durable receipts and
admissions under the current unit's locks. Only `CONFIRMED` entries can justify
this execution's own prior effects; `UNCHANGED` and denied/invalid/conflict
admissions cannot. Frozen evidence is neither an after-image nor a grant, and
cannot replace current authority or external-dependency checks. `ATOMIC` callbacks
receive an empty prefix. The kernel's decoded-evaluation memo lasts for one
`advance` only. Under each fresh unit's control/execution locks, it re-reads all
eleven protected proposal/evaluation columns and checks the execution binding.
It reuses decoded data only when immutable headers and both payload byte arrays
match; changed payload bytes take the original decoder, while changed immutable
headers are `CORRUPT`. Standalone units, `ATOMIC`, recovery, readers and replay
keep their fresh decode and certification paths.

A host's advance-local schema memo is separate. For every unit, retain required
domain/grant locks and recheck the fresh published candidate/generation, exact
document, current MVC operation references, complete generic body types, current
policy, grants and domain/dependency state before mutation. Reuse only immutable
schemas after those checks, never the publication as authority. Do not infer
200-item completion, performance or host `READY` from focused SDK/host tests;
prove them by exact-artifact HTTP and PostgreSQL evidence before teaching adoption.

For the private B5b.1a candidate, inspect Metadata
`BulkCapacityAuthorityMigrator`, `BulkCapacityAuthorityInfrastructure`,
`BulkCapacityAuthorityCatalog`, `JdbcBulkCapacityIssuer`, its isolated V1
migration and focused PostgreSQL tests before changing capacity behavior.
Metadata rc.154 does not publish this issuer: only the explicit migrator is a
public Java type in the candidate; issuer, infrastructure and catalog remain
package-private. The issuer uses a separate PostgreSQL authority per logical
deployment with a fixed environment and an externally supplied authority
UUID/epoch. Binding enrollment is an immutable administrative declaration,
not proof of a physical operational database. Keep local `BulkQuotaLedger`
SYNC allocations and the same-database `BulkControlPlaneInfrastructure`
distinct from global rights. Pending requests are durable and idempotent;
each `allocateNext` emits at most one token and advances the persisted
per-class tenant cursor in the same transaction. Check 2 ACTIVE/20 QUEUE
rights per tenant and 8 ACTIVE/80 QUEUE per deployment across bindings,
including rights in transit. A token is not a job or local admission.
Prove limits, replay, rollback, two-client contention and cursor persistence
with `JdbcBulkCapacityIssuerPostgresTest` before teaching adoption. This
cut has no install, enqueue, retirement, worker, ASYNC, HTTP `202`, or
`READY`; neither issuer construction nor focused tests certify those paths.

For the B5b.1b.A internal installation candidate, inspect
`JdbcBulkCapacityInstallation`, `JdbcBulkCapacityIssuer.CapacityReader`, authority V2
and operational V18 with their PostgreSQL tests. Source compilation or the existence
of these types is not functional acceptance or publication in rc.154. Establish the
exact frozen implementation and focused evidence before teaching adoption. Installation
is trusted owner provisioning, not runtime authorization to invent a right: runtime
SQL receives only local SELECT, and the global reader receives only bounded read
functions, without allocator credentials. Never accept a caller's verified token DTO.

Pin deployment, tenant, environment, binding/generation, database and attestation UUIDs,
and authority UUID/epoch in the immutable local marker and installation FK. Read the
real issued token and complete the global transaction before opening the local owner
transaction. Reject ambient Spring transactions, including another manager. A
same-database owner/runtime advisory witness is the only deliberate overlap; it proves
that live association, not absence of a writable clone. Test alternate real authorities
with copied remaining fields so the constructor succeeds and the old marker itself
rejects reassociation, rather than proving only a configuration mismatch.

Keep PROVISIONED→ACTIVE/FENCED and ACTIVE→FENCED exact; FENCED never reopens, including
in a new process. ACTIVE requires authenticated matching attestation readback. Token UUID
remains the installation PK. Rights stay globally counted through failed installation;
there is no refund by timeout, deletion, occupancy placeholder or generation succession.
Use explicit remaining local time budgets, preserve smaller SQL timeouts and reject
expired work before the owner transaction callback returns. This is not a COMMIT
acknowledgment or instantaneous cancellation guarantee. Use known rollback and readback
after observed commit; do not repackage T08 as an uncertain-commit proxy experiment.

Require real PostgreSQL upgrade, privilege, rollback/replay, PID/XID transaction-order
and fence/install interleaving proofs. A four-process owner installation test must run
two JVMs per local database, observe four distinct PIDs and exit0, exactly one insertion
and one replay per database, and the authoritative full row. A new owner JVM must also
be denied after persistent FENCED. Threads or object reconstruction do not establish
process restart. This slice does not create QUEUED, accept jobs, occupy execution slots,
fence domain executors, enable HTTP202/ASYNC/READY or prove restore/cutover safety;
those remain B5b.1b.B/C and worker/consumer gates.

The V19 occupancy described below is an internal source candidate, unavailable in Metadata
`8.0.0-rc.154`. Confirm the exact SHA, diff/source freeze and matching proofs before use.
A host must not access or copy package-private `enqueue`/`claim` through reflection,
bridges or local SQL as a shortcut to public admission.

For the protected B5b.1b.B occupancy increment, inspect `JdbcBulkDurableExecution`,
`JdbcBulkCapacityOccupancy`, `BulkCapacityOccupancyCatalog`, operational V19 and
`BulkCapacityOccupancyPostgresTest` with its authenticated fixture. Reuse the existing
execution ledger, codecs, full control expectation and immutable expected binding.
Internal ASYNC construction is not public capture or a READY descriptor: the initial
subset is UNIFORM_UPDATE/EXPLICIT/PER_ITEM, at most 10,000 targets, absolute deadline
at most 30 minutes including queue time, and unit budget at most five seconds.
Public BulkStoredProposal constructors and capture/reservation remain SYNC-only until
their own gates close.

Enqueue must consume the pending proposal, create one QUEUED execution/allocation and
occupy one installed QUEUE slot in one local transaction. Replay preserves identity
and deadline; a second key must not duplicate the proposal's execution. Claim uses the
minimal NOLOGIN definer entrypoint, not a caller boolean, GUC or direct runtime UPDATE.
Preserve marker→control→quota/proposal→execution→slot lock order, full READY tuple and
owner epoch 1→2. Transfer the same EXECUTION_ASYNC allocation QUEUED→ACTIVE; release
QUEUE and occupy ACTIVE atomically. Slot sequence persists through release and reuse;
occupation history is append-only with controlled retention, not runtime DML.

Do not repair claim failures by granting unrelated ATOMIC helpers to the capacity owner.
A PER_ITEM trigger must branch before preparing ATOMIC expressions; preserve and test
ATOMIC commit/rollback gates. Terminal ASYNC release is certified after its materializer,
while SYNC keeps its existing local quota path. Reject nullable invalid slot transitions
in the trigger itself; distinguish this hardening from corruption already denied by CHECK.
Require domain/receipt transaction proof, replay before new-mutation gates, old-owner
fencing, confirmed-prefix recovery without callbacks, deadline/cancel/release, retention,
ACL drift and concurrent/process proofs before accepting the whole cut. Initial enqueue,
claim and cancellation tests alone do not prove that matrix, a worker, HTTP202, restore
safety or backend closure. Beta cutover is non-rolling: drain old executors and suspend
controls before migration; certify old-binary rejection using genuine ASYNC bytes before
consumer adoption. Never manufacture T08 or uncertain-commit proxy experiments.

For global occupancy conformance, distinguish issued/installed rights from occupied
execution slots. A local tenant's two ACTIVE/twenty QUEUE ceiling cannot prove the
global eight/eighty ceiling. Reuse one genuine authority with at least four distinct
trusted local bindings and databases; compare full issued identities through local
installation, current slot, execution, allocation and append-only history. Reuse
released QUEUE rights after claim, and consume each pending proposal before creating
the next so the pending quota is preserved. A later fifth binding must obtain no
new rights and must not install or enqueue another binding's genuine token.
`BulkCapacityGlobalOccupancyPostgresTest` demonstrates that internal candidate path.

Follow the canonical allocation shape: EXECUTION_ASYNC is owned by execution_id
(allocation_id equals execution_id, proposal_id is null). Link execution.proposal_id
to the unique consumed PROPOSAL_PENDING allocation and compare transferred scope
digests/versions; do not invent a second proposal link on the execution allocation.
Check the real stored proposal's context and fingerprint using the existing codec.
Serial quiescent reads across databases are not a distributed atomic snapshot or
four runtime OS processes. Keep the separate two-database/two-runtime-process gate;
OWNER provisioner JVMs, threads and reconstructed objects do not certify runtime
execution across processes. These internal proofs do not permit a host to copy
package-private APIs or enable public ASYNC/READY before its own composition gates.

For runtime-process conformance, use real runtime-only JVMs with genuine
enqueue/claim controls and authenticated bindings; keep OWNER provisioning in the
parent. Match every child event to its actual Process PID and verify class origin.
`BulkCapacityOccupancyProcessesPostgresTest` provides the finite candidate harness.
Prepare all children outside unit transactions, then exercise one database pair
at a time. Observe causal marker blockers with `pg_blocking_pids`; release the
observed callback before waiting for the other blocker, an ACK or child exit.
Do not increase unit or owner lock budgets to accommodate a test barrier.
Prove external absence before commit and matching callback XID/domain/receipt
`xmin` after commit. Test old-control fencing before marker fencing, then fresh
unit/claim/enqueue rejection and confirmed replay without callbacks. Compare full
binary rows by content, not Java array identity. Release barriers before cleanup
waits, join/kill owned children, remove private credentials and close the cluster.
Four passing runtime JVMs do not certify restart recovery, a product worker,
distributed atomic snapshots, global caps or public ASYNC/READY.

For clone/restore characterization, inspect `BulkCapacityCloneBaselinePostgresTest`
and the owning C plan before writing a new protocol. This internal test copies a
quiescent PostgreSQL database with the same ExpectedBinding, genuine tokens and
confirmed receipt. TEMPLATE does not copy database ACLs or settings: capture the
observed owner, grantor/grantee/options and role/database settings; transfer only
those values, fail unknown cases and compare the complete envelope before kernel
construction. Compare full binary rows, Flyway history, catalog/ACLs and roles by
content; do not migrate/heal the copy, generate new IDs or fabricate CONNECT grants.
Prove the original's fenced denial before callback separately from the copied
baseline's ability to commit domain and receipt in one physical transaction. Replay
confirmed receipts without mutation, keep the original authority unchanged and
restore connection policy/close only owned resources. No callback transaction spans
the copy. A passing C1a test characterizes a limitation; it does not prove anti-clone,
physical cluster restore, authority continuity, succession or public ASYNC/READY.
Keep frozen C1a evidence when C1b changes the expectation to rejection by a real
mechanism; never teach a host to call these internal APIs as a recovery workaround.

For controlled withdrawal of an accessible origin, inspect
`BulkCapacityControlledWithdrawalPostgresTest` before defining a new shutdown proof.
Certify the real callback/fence blocking edge with PostgreSQL PIDs and release the
callback immediately within its original budget. Prove domain and receipt share
the committed XID. Capacity fence stops new ASYNC units but does not stop SYNC:
retain a genuine SYNC positive and receipt replay without mutation.
Blocking new database connections does not remove an existing physical session.
Use a genuine UPDATE with rollback and an independent observer before terminating
only attested PID/database OID/role/backend_start tuples; verify exit, not just a
sent signal. Test original and restarted runtime JVMs with matching class hashes,
native SQLSTATE 55000, denied administrative reopening (42501) and zero callbacks.
Reconcile through a separately attested, preopened read-only lease, preserve the
confirmed prefix and authority, then close it to prove zero origin backends.
Owner/superuser remains trusted. The test certifies only its enumerated unpooled
runtime plus held session, not arbitrary pools, HA, PostgreSQL restart, clones,
lost authority or uncertain-commit recovery. Never infer absence of prior effects
from connection denial, promote a copy or reissue rights as a repair. Keep private
configuration out of argv/logs and release/abort held probes before cleanup waits.
This internal proof is not a public host administration API or deployment recipe.

For external connection quarantine, inspect the internal
`BulkCapacityExternalQuarantinePostgresTest` and its authenticated `SharedScope`
overload. Trusted administration does not mean a runtime client cannot select an
administrative username: use distinct SCRAM credentials for owner, each authority
role and runtime. Scope role/database/transport permissions explicitly. In this
harness, only the initial embedded healthcheck uses temporary owner-only loopback
trust; close it and attest real authentication before creating authority, migrations
or domain state. Keep the default fixture route unchanged and test its regression.

Authenticate the original positively; reject administrative/issuer impersonation
using the runtime password. Distinguish wrong-password 28P01 (and PGJDBC's exact
empty-password SCRAM 08004 branch) from native HBA quarantine 28000 with the CORRECT
runtime credential. A failed classpath, missing password or dead endpoint is not a
quarantine oracle. Seed all six role credentials before the baseline. Compare real
`pg_authid` verifiers and attributes only in private parent memory through a boolean
assertion; `pg_roles` masks passwords and cannot certify their preservation. Never
emit secrets, verifiers or full protected snapshots in assertion failures or logs.

Give child JVMs only the runtime credential in an owned private file, never owner
or issuer secrets in argv, environment, URLs or manifests. Read back the applied
external HBA path outside PGDATA, exact first-match rules and disabled/denied unused
transports. Preserve the genuine TEMPLATE copy's envelope, ACTIVE marker, rows,
receipts, controls and grants; separately compare shared cluster-wide credentials
unchanged (TEMPLATE does not copy roles). Certify child PID/class origin, original
receipt replay, native denial and zero callbacks before/after JVM restart. A held
session can still write after HBA reload: demonstrate UPDATE/rollback, then terminate
only its attested tuple and read back absence. Close children, private configurations
and the owned cluster. This proof covers an enumerated same-cluster copy and JVM
restart/HBA reload, not PostgreSQL restart, HA, physical cluster restore, monotonic
external continuity, C0/C1b/C2 completion or a public deployment recipe.

For `DOMAIN_COMMAND/ATOMIC` composition published in Metadata `8.0.0-rc.152`, start with the real
`@WorkflowAction`, typed command parameters and `BulkOperation` declaration.
Require matching action/bulk atomicity, the exact canonical action-registry
binding and provider, confirmation operation and all seven operation references
in one published photograph. Preserve the command action identity and its
parameters; do not turn it into CRUD field changes, an editable-fields capability
or a second command vocabulary. Check `EXPLICIT`/`SYNC`, at most 50 targets, an
aggregate unit deadline no greater than five seconds and the action's stricter `maxItems` limit.
The profile constructor itself rejects a deadline above five seconds, before
composition; test that boundary with a valid construction path, not an invalid
profile injected by spy or reflection. Mismatched bindings fail closed. The
protected ATOMIC kernel and published descriptor composition do not supply the
host's domain command provider, mutation/authorization proof, transactional
outbox or public `READY`; verify each against the exact artifact before adoption.

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

Preserve the real evaluation window: record proposal `createdAt` before policy and
factual observations, retain the owner's `policy.observedAt` unchanged, and close
`evaluatedAt` after all evidence and authorization reads. Keep one factual `asOf`
per capture. Standalone evaluation may derive proposal expiry from the completed
evaluation; durable locked capture fixes the proposal expiry before capture and must
not renew it while waiting or evaluating. The canonical
invariant is `createdAt <= policy.observedAt <= evaluatedAt < expiresAt`; creating
both proposal and evaluation timestamps after resolving policy rejects valid input.
Follow the host's `EventosFolhaApprovalEvaluationProvider` composition. Prove the
SDK constructor boundary separately from a real HTTP evaluation/confirmation/replay
regression; neither proof closes the accumulated SQL/lock/flush deadline budget.

For host factual capture, reuse `QuickstartUnitBudget.constrainedBudget` with the
already-bound operational datasource and one monotonic remaining-budget supplier.
Before each SQL, constrain LOCAL statement/lock timeouts to the smaller nonzero
current setting and live remaining time; verify physical RO/RW mode and check the
supplier again after work. Build the RR/read-only capture template per invocation
from the remaining budget after context/schema/policy work and pool reserve, never
mutate a shared template. The concrete JDBC factual-provider overload must join
that caller transaction without `REQUIRES_NEW`; keep the unary ITEM path intact.
Prove two successive queries consume one window with real PostgreSQL blockers,
read-your-own-uncommitted facts/dates in RW, and SQL capture failure publishes no
proposal or domain writes. Helper tests alone do not prove JPA locks or the
workflow/audit/final-flush/outbox path. To certify a prior LOCAL250ms JPA limit,
observe it inside the unit after SDK deadline setup: a role default can be
replaced by the SDK's LOCAL control timeout and is not that proof.

For a bulk domain approval, propagate one live unit supplier and the exact bound
operational datasource through consumer, workflow, audit and outbox. Use bulk-only
MANDATORY seams without changing the existing ITEM calls or constructors. Reject
missing budget arguments; tighten the PostgreSQL budget immediately before and
after find, request persistence, audit persistence, explicit flush and outbox work,
and check before returning the mutation. An assigned-ID audit `save` may defer SQL:
the bulk path uses `saveAndFlush` inside the budget, while ordinary ITEM persistence
retains its previous behavior. Preserve runtime/SQL failures for the kernel; never
clear an aborted transaction or restart a budget to reach a later write.

Prove the last outbox SQL uses the remainder, not merely the SDK's existing lock
limit. In the reference HTTP/PostgreSQL journey (`a4d827ff` source freeze), a
fixture-only first INSERT consumes part of its observed statement timeout; two
transaction advisory markers encode the initial and last LOCAL GUC on one backend.
The last INSERT's SQL wait exceeds the reduced limit and fails with 57014 after
both domain/audit writes and the first outbox have executed inside that transaction.
Verify whole request/fact snapshots, zero committed audit/outbox/admission/receipt
children/effect references, and one scoped atomic rejection `UNIT_ROLLED_BACK`.
That rejection is canonical rollback evidence, not a partial approval effect.
Require immediate `STOPPED/UNIT_ROLLED_BACK`, cleared attempt/deadline, released
allocation and same-key terminal replay with stable epoch. Do not force recovery
of an already stopped execution; no-header recovery has its separate proof.
Restore fixture objects in unconditional cleanup, preserve failed runs separately,
and distinguish this approval fixture from the local apply ledger it does not
contain. Validate unchanged ITEM lifecycle/apply and the old writer with their
existing canonical pilots. That last-outbox proof alone does not close JPA prior-250ms, public
receipt-present recovery, direct callbacks, old-control fencing or full IAM gates.

For the reference JPA prior-250ms proof, configure only the HTTP fixture's API
PostgreSQL with an activity-query text budget large enough for the actual Hibernate
SELECT (8 KiB); retain defaults for other fixtures and leave Config PostgreSQL
unchanged. Assert the effective setting on the API database. A truncated activity
query can hide the table and locking suffix; do not weaken the SQL oracle to make
that failure pass. Instrument only the success return of the existing F fixture
function to install LOCAL250 after SDK deadline setup. Preserve and restore its
exact definition, OID, owner and ACL in unconditional cleanup.

Observe the same unit PID's SELECT FOR UPDATE/NO KEY UPDATE, its ungranted
transactionid ShareLock and the direct publisher blocker. Measure statement start
through wait end using PostgreSQL query_start and a conservative server-clock end
bound; detecting wait entry or timing the HTTP response is insufficient. The
reference journey (`395be088` freeze) observed 261 ms, followed by public 202/RUNNING
and durable UNIT_IN_FLIGHT. These are different canonical status projections.
Require the live durable deadline, then recovery after its actual expiry to STOPPED,
RECOVERY_STOPPED, epoch+1/new owner, released allocation and stable replay with zero
approval effects. Preserve domain/fact and immutable evidence snapshots, restore
fixture catalog state and close workers/blockers. This is a bounded JPA row-wait
and no-receipt recovery proof, not total HTTP latency, uncertain COMMIT, public
receipt-present recovery, old-control fencing or complete IAM certification.

Distinguish a known committed receipt resuming its ACK from explicit kernel
recovery. In the public reference journey (`6719640d` freeze), a fixture-only
trigger blocks then fails only the separate PENDING_ACK-to-COMPLETED certification
UPDATE. An independent owner connection first observes the full committed header,
children/effect references and approved domain/audit/outbox while that ACK is
blocked. Never inject a COMMIT failure or fabricate receipt/control rows for this
proof. The valid SDK readback returns public 202/RUNNING and durable
UNIT_COMMITTED_PENDING_ACK. Revoke the grant through the official function, prove
retry/read denial without enumeration or changes to committed evidence, and restore
the grant with its monotonic version. After the original deadline elapses on the
database clock, remove the fixture fault and repeat the same proposal/key: expect
200/COMPLETED with the same execution, owner and epoch, cleared active attempt,
identical full receipt/children/effects and domain/audit/outbox snapshots at ACK
resumption. The terminal replay checks execution ID, domain versions/status and
outbox count; it does not repeat the full receipt/control snapshot oracle. Unlock the gate before bounded worker shutdown and unconditional
fixture cleanup. This proves receipt-first ACK resumption, not recoverAtomic,
epoch+1, direct callback counters, uncertain COMMIT or complete IAM. A readable
receipt normally takes this ACK path; do not force corrupt/unreadable evidence to
make the public handler enter a different recovery branch.

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

Do not accept row-lock plus COUNT as a sufficient quota proof under REPEATABLE READ:
an immutable bucket can serialize waiters while the losing transaction retains an
older allocation snapshot. Inspect the canonical V17 identity-preserving deployment
MVCC touch, its migration preflight and the capacity-edge PostgreSQL proofs. Apply the
touch only when `enforcePendingCapacity=true`; preserve SELECT FOR UPDATE for
reservation/replay. A serialization loser must not run or retry the callback internally.
The API returns sanitized UNAVAILABLE; CAPACITY requires a new transaction with a
fresh snapshot. Prove subject9/deployment99 with a prior losing RR snapshot, actual
transactionid wait and direct blocker, raw ledger SQLSTATE40001, zero loser callback,
all seven artifacts and bucket identities, and fresh CAPACITY without new rows.

V17 must reject prior V5 guard drift before CREATE OR REPLACE, preserving history and
the corrupted object rather than healing it. Inspect its transactional preflight for
schema ownership/function attributes/exact V5 body, owner-only ACL and exactly two
canonical active bucket triggers, including the global guard-binding count. Runtime
column UPDATE(deployment_id) already exists; do not add broad grants or a quota counter.
Prove cutover from the checksum-pinned public V16 SDK, unchanged historical checksums,
OID/ACL/bindings and runtime no-op identity preservation. Test prior body/ACL/disabled/
rebound/third-binding corruption with SQLSTATE55000, no history17 and no healing.
The old SDK expects the V5 guard and refuses V17: plan drain and coordinated cutover,
not concurrent-version compatibility. Keep API availability/publication and host HTTP
proofs as separate gates; a passing private core does not close the backend.

When authoritative capture must follow the control/quota locks, inspect the Metadata
candidate `captureAndInsertEvaluated(proposal, capture, project, callerRemaining)` and
the concrete MissionParticipant proposal service/provider. Verify the installed
artifact actually contains the API before adoption; a private candidate proves source
integration, not publication. Reuse the existing intent, evaluation, manifest and safe
preview; do not introduce a second population DTO or persist QUERY under an EXPLICIT
descriptor. Preserve `PER_ITEM_UPDATE`'s canonical `items` shape, which has no selection
object. QUERY requires a separate vertical contract/provider/kernel proof.

Create one monotonic deadline before pool/TX acquisition and immutable proposal before
capture. Join a writable physical RR transaction with MANDATORY; control/deployment/
subject quota locks precede the host's current grant G, then domain evidence. MissionParticipant
retains its 200-target/eight-second nominal limit; the store's nonrenewable 30-second
ceiling does not expand it. Pool/attestation/Java time is accounted and may cause late
refusal, not preemptive cancellation or a hard end-to-end guarantee. Tighten LOCAL
statement/lock timeouts without widening a lower caller limit, then restore when
possible. Require exact proposal/evaluation binding and safe preview before inserting
proposal/evaluation/manifest/preview/allocation together. Unexpected callback or
supplier exceptions become canonical UNAVAILABLE without protected text or cause;
even a caught outer exception must leave the participating transaction rollback-only.

For JdbcTemplate callbacks, unwrap the close-suppressing Connection proxy with
`DataSourceUtils.getTargetConnection` before `isConnectionTransactional`; compare that
physical target with the physical target of the Spring `ConnectionHolder`. Preserve
active writable RR, JDBC read-only/autocommit and datasource affinity checks. A raw
proxy can report nontransactional while its target is the bound connection; prove
raw/target observations and shared PID before changing a guard, then rerun the
affected capture paths. Do not remove the guard or expose protected exception causes.

Prove real PostgreSQL pre-TX elapsed budget, expiry by database clock, lower-GUC
preservation/restoration, control/quota before G, same callback PID/XID/role/RR across
JPA/JDBC and all seven physical tables, full readback and late-write rollback. Preview
state/item/integrity are separate physical dependents, not just one preview count.
Compare full existing rows on negative cases, not counts alone. A reduced scope during
capture conservatively fails as unavailable; the store must not interpret host HTTP
exceptions or unwrap protected causes. Distinguish host kernel proofs from real HTTP
403/503/cache/privacy proofs. Retained quota locks serialize related captures; do not
infer scale/fairness, QUERY/ASYNC, READY, release or backend closure from this prerequisite.

For governed QUERY adoption, inspect Metadata
`BulkOperationLifecycle.requireReady(identity, SYNC, QUERY)`, its opaque
`ReadyAdmission`, `JdbcBulkProposalStore.captureAndInsertEvaluated`, and
`JdbcBulkDurableExecution` together. A published, durably validated profile
must admit `UNIFORM_UPDATE`/`SYNC`/`PER_ITEM`/`QUERY`; neither the host nor a
test may forge the admission. Existing execution replay is resolved before a
fresh `READY` gate. An absent QUERY reservation probes existing state, obtains
admission outside the transaction, then rechecks publication and binding in its
fresh reservation transaction; EXPLICIT keeps its existing single-transaction
path. The old proposal APIs must still deny QUERY. Do not add readiness gates
to receipts, recovery or readback.

For an independent bulk update of ordinary resource fields, keep the source on
the resource with `@BulkResourceOperations` and `UPDATE_SOURCE`; do not invent
a `@WorkflowAction` or borrow a workflow approval policy. Inspect the
resource's versioned GET/PUT, editable fields, operation bindings, and
resource-validation policy before composing the bulk operation. The
`ReferenceCatalogItemController` and `ReferenceCatalogItemProvider` in the
Quickstart bulk reference consumer are a candidate for this route, not an
accepted HTTP or deployment proof.

The concrete host freezes its strict filter, exclusions, operation and
fingerprint before capture. In one writable physical RR transaction, acquire
CONTROL and quota before the current grant G, then resolve authorized SQL
population and evidence on the same JDBC/JPA connection. Apply functional
filter, current grant and exclusions before ordered `LIMIT 201`; retain numeric
ID order and store the selected IDs, expected ETags and ordinal manifest.
Confirmation reads that manifest without rerunning the filter, while current
grant, policy, references and version remain unit admission gates. If current
target coverage disappears while the global grant remains valid, the kernel can
durably stop with `AUTHORIZATION_REVOKED` and zero ordinal admissions; the HTTP
reader must still authorize the whole frozen manifest and answer with safe
`BULK_NOT_FOUND`/404, not disclose STOPPED. Global denial or global authorizer
unavailability retain their distinct pre-lookup outcomes; do not map every
authorization loss to 404.

Reproduce the boundary with Metadata `BulkUniformQueryContractTest` and
`JdbcBulkUniformQueryPostgresTest`, host
`MissionParticipantUniformQueryShapeTest`, and
`MissionParticipantUniformQueryHttpPostgresTest`. The private SDK candidate has
25 composed focal cases; the host has 49 composed focal cases and HTTP evidence for a
200-target capture plus a separate one-target confirmation/replay. These do
not prove a 200-target confirmation, 10,000-target or 30-second host budget,
complete IAM, ASYNC, Angular, or public QUERY availability. The current host
QUERY cap is 200 targets with its existing eight-second nominal budget; neither
the SDK's 10,000 exclusions nor 30-second store ceiling expands that cap.
Historical public rc153 remains EXPLICIT. QUERY is published in Metadata
`8.0.0-rc.154`, tag `7c974b5228d1f78fb82f3bc180c1940a886c6275`,
via official run `37236119846` (1,530 tests, zero failures/errors, three skips);
its POM/JAR are available on Maven Central. The earlier
`8.0.0-b5a-uniform-query-20261004-SNAPSHOT` remains private development evidence.
A host must independently pass adoption against the public rc154 POM without
version override or installation of the public SDK coordinate; publication alone
does not certify downstream adoption, deployment or backend closure.

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

For the protected V16 `ATOMIC` bulk kernel published in Metadata rc.150,
inspect the canonical
`praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/bulk/`
sources `JdbcBulkDurableExecution.java`, `BulkExecutionResultsReader.java`
and `BulkExecutionMigrator.java`, plus
`praxis-metadata-starter/src/main/resources/db/praxis-bulk-migrations/V16__bulk_atomic_set_execution.sql`
before asserting a contract. Verify whole-set
admission before mutation; one bounded transaction for domain writes, outbox,
one receipt header and ordered child evidence; and rollback of all of them
when the last target or evidence append fails. The published kernel bounds
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

Keep the host admission decision distinct from the durable protocol result.
A current grant check returning false is denial; dependency failure is not a
business denial. In the published ATOMIC kernel, unavailable budget detected
before SQL can produce `DEPENDENCY_UNAVAILABLE` / `UNIT_ROLLED_BACK` without
invoking mutation. A real PostgreSQL error such as permission denied (42501)
can instead abort the transaction: a wrapper returning `UNAVAILABLE` does not
restore it, and the kernel's following budget query can fail with 25P02 before
normal rejection is persisted. Preserve the canonical conservative
`RECONCILIATION_REQUIRED` result; do not change the kernel, clear the transaction,
or add a savepoint just to make the test expect a normal dependency rejection.

For this pre-mutation SQL failure, prove zero domain callbacks, domain changes,
audit, outbox, receipt headers, children, effect references and rejection rows.
Observe the retained `UNIT_IN_FLIGHT` state and active execution allocation;
verify a bounded independent lock attempt succeeds after rollback without
changing the grant. Await the real `active_unit_deadline_at` used by
`recoverAtomic`, with a bounded observer and the existing reservation lifetime
overload when a short-lived fixture is needed. Never edit persisted deadlines
or raise unit budgets to make recovery pass. With certified receipt absence,
in this case without a cancellation request, fenced recovery must give
`STOPPED` / `RECOVERY_STOPPED`, advance the owner epoch, release the allocation as `TERMINAL_RECONCILED`, fence the old owner and
allow terminal replay without readmission or mutation. A fresh grant read is a
separate authorization step and cannot revive the stopped unit. This local SQL
error before mutation is not evidence of a lost COMMIT response or public HTTP
behavior. Validate against the concrete host fence and PostgreSQL consumer
before publishing guidance or accepting its adoption.

For a public host confirm adapter using Metadata rc.152, receipt-first execution
is not automatic recovery of a no-header `UNIT_IN_FLIGHT` attempt. Compose the
existing `JdbcBulkDurableExecution.recover` only in POST confirmation after a direct
`RECONCILIATION_REQUIRED` failure: refresh and compare the full current trusted
lookup scope, require the existing authorized execution reader's `COMPLETE`
observation for the full manifest, then inspect the scoped durable state. Admit
only `UNIT_IN_FLIGHT`, `UNIT_COMMITTED_PENDING_ACK` or `RECONCILIATION_REQUIRED`;
never recover a clean `RUNNING` reservation or mutate from GET. Use a new opaque
server owner, let the SDK guard the real active deadline and receipts, and never
call the domain consumer again after recovery. Failures retain the existing safe
durable projection. Reader `COMPLETE` means authorized reading, not terminality;
normal domain state/version changes do not invalidate scope evidence, but target
absence/provenance drift may prevent public finalization without deleting a receipt.
Authorization is point-in-time, not atomic with recovery; reader/kernel have their
own budgets, so surrounding supplier checks do not prove a global HTTP latency cap.
Prove real F-lock failure, early retry retaining owner/epoch/deadline, post-deadline
`STOPPED/RECOVERY_STOPPED` with epoch advancement/allocation release and terminal
replay without effects. The initial no-header HTTP journey (source freeze `be65cd72`)
proved that lifecycle only. The subsequent journey (`f6339ddb`) also proves denial
for a revoked current grant, changed target provenance and another creator. The
denied HTTP calls add no execution/evidence/approval effects; the fixture changes
and restores provenance externally to those requests. Compare known and random references through
complete errors, absent/null data, UUID non-disclosure and sensitive headers; restore
grants through the canonical monotonic-version function, without resetting versions.
Two HTTP callers released through one barrier converge to the same stopped execution
with one epoch increment and allocation release. This proves concurrent dispatch and
observable convergence, not forced PostgreSQL lock interleaving. Neither journey
proves present-header pending-ACK recovery, direct callback counts, old-control fencing
through HTTP, JPA prior-250ms preservation, the remaining workflow/audit/final-flush/
outbox budget phase or the full corporate IAM matrix; retain those as separate gates with their own source evidence.

For a domain approval producer, keep the event contract owned by the domain
transition, not by the bulk kernel. In the RuleLab reference host, inspect
`ExtraordinaryBenefitApprovalOutboxPayload` and `ExtraordinaryBenefitApprovalOutboxWriter`:
the per-item `approved.v1` payload contains only executionId, attemptId, ordinal,
requestId, resultVersion and transitionId. Preserve the real resulting version;
do not assume every approval starts at version zero. The envelope operationId
is the persisted domain transitionId; the generated messageId is the item's
receipt effect reference. Neither UUID replaces the collective bulk execution
or the Metadata semantic operation identifier. Do not put justification,
request text or internal snapshots in the delivery payload.

The producer must join the same operational transaction with
`@Transactional(transactionManager="apiTransactionManager", propagation=MANDATORY)`.
Prove the managed bean rejects a valid call outside a transaction, and prove
inside the kernel that domain, audit, outbox and receipt share the physical
PostgreSQL PID/XID. When replacing a shared mutation helper, revalidate every
case that uses it, including the 50-target aggregate deadline, late append
rollback, denied whole-set admission, terminal replay and durable recovery.
A direct Java unit call or annotation inspection does not prove transactional
behavior. Compare `ExtraordinaryBenefitBulkCommandOutboxPostgresTest` and its
fixture in the reference host.

Preserve tenant/environment/correlation exactly after their governing owner
has resolved them. Validate nonblank values and storage bounds before writing. This reference
uses Java String.length (UTF-16), a conservative bound for supplementary
Unicode characters compared with PostgreSQL varchar; do not infer ASCII-only
identities or exact database character capacity. The outbox entity must not
trim identity values or silently merge different scopes.
Normalize only at the canonical context owner when its contract requires it.
An ACK from a custom probe must match the queried messageId before changing
local delivery state. A mismatched ACK schedules reconciliation without
confirming or resending that candidate. The scan returns PROBE_FAILED if no
subsequent candidate reconciles; a later valid ACK can yield RECONCILED instead.
Do not claim a per-candidate failure metric from this scan-level outcome. Inspect
`ExtraordinaryBenefitStatementOutboxReconcilerTest` for matching, absent,
mismatched and mixed-candidate scans.

For the host statement outbox `JsonNode` payload, prove the persistence boundary
before introducing content fingerprints: default Hibernate JSON mapping can lose
decimal precision during persistence, before a fresh read. Use a converter scoped
to that field, with exact decimal/integer parsing and a node-preserving mutable
snapshot (`JsonNode.deepCopy`), rather than changing the global mapper or marking
mutable JSON immutable. Converter round-trip snapshots can change IntNode/LongNode
types and trigger an unwanted UPDATE after INSERT; keep the producer role insert-only
to expose this regression. Reject write values that cannot pass the same bounded
reader, reject non-finite numeric type changes, and sanitize exception chains so they
do not retain payload fragments. In real PostgreSQL, check native `payload->>` numeric
values and `jsonb_typeof(payload)`, fresh JPA/wire values and a legitimate claim/flush
state update; revalidate affected rollback/replay proofs. Grant UPDATE only within
the isolated state-update characterization, never to hide a producer regression.
Preserving persisted numbers does not certify ACK fingerprint binding or delivery.

For the host statement envelope, inspect `ExtraordinaryBenefitStatementEnvelopeFingerprint`
and the independent literal-vector tests before changing the content identity. Its
versioned framing covers operationId, eventType, tenantId, environment, correlationId
and payload; messageId remains a separate binding and delivery attempt is mutable
retry state, whereas payload attemptId remains immutable content. Preserve JSON types,
exact decimal value, array order and opaque Unicode; schema canonicalizers that sort
`required` arrays are not appropriate for domain payloads. Check numeric coefficient
and scale budgets before rendering a large number and tree/member/string budgets before
copying or sorting. The delivery constructor validates the entire envelope before its
defensive copy and validates the stored snapshot again; payload-only validation cannot
account for envelope overhead. Exercise the independent bytes/SHA vector, boundary
counterexamples, no-copy rejection and mutable snapshot isolation. Compare fingerprint
values across the real JSONB/fresh JPA/wire round trip before attaching this evidence
to ACK/state transitions. A tested helper and immutable delivery record alone do not
prove fingerprint-bound ACKs, consumer business effects or process restart.

For the host ACK protocol, require the exact four wire fields messageId, status,
acknowledgedAtUtc and envelopeFingerprint, a non-null SPI result, canonical UUID,
lowercase SHA-256 and closed PROCESSED/DUPLICATE status. Reject duplicate, unknown,
missing, trailing or mistyped fields. A POST response must bind the delivered UUID
and immutable content; a foreign UUID from a GET/custom probe is a probe failure,
not proof that the queried row is corrupt. Preserve the identity guard above.
Compare same-UUID content evidence again under the existing row lock, with dispatcher
lease authority checked before any mutation. Recovery must never revoke a live lease.
Do not demote DELIVERED; validate evidence even when recording a positive audit for
an already-delivered row. Preserve the failure observed before external I/O.

Keep integrity quarantine distinct from temporal replay eligibility: reserved
OUTBOX_ENVELOPE_INVALID/MISMATCH dead letters cannot dispatch, reconcile or replay.
Use scalar bounded raw projections under the same API JPA transaction and row lock
before a legacy payload can fail entity conversion. Quarantine only the locked,
authorized row; preserve active leases and confirmed rows, and prove rollback and
progress of the next valid candidate. Do not catch all persistence failures as
integrity errors or commit uncertainty. A native JSONB text CASE bounds transfer
and Java parsing, not PostgreSQL's internal materialization work.

Certify PostgreSQL's expanded numeric representation before writing, not merely
compact exponent JSON: the scoped codec reader's 512-character token budget must
also constrain expanded numeric write text without rounding or allocating it.
Prove both exponent signs, the negative-sign boundary and rejection before INSERT.
The persistence codec is narrower than the transport helper: a compact exponent
such as 1E+4096 may fit the helper but exceed JSONB's expanded read representation.
The expanded-size calculation is conservative for zero with extreme scale; do not
claim PostgreSQL corruption or silently normalize values to broaden acceptance.
For fingerprinting,
bound raw numeric rendering before allocation, then apply precision256 to the
normalized coefficient so JSONB's equivalent trailing-zero representation retains
the same identity. Check actual ORM/raw claim and the independent vector.

The HTTP ACK budget must cover both bytes and elapsed time through complete EOF:
16 KiB with bounded subscription/backpressure and the configured total request
deadline, cancellation on timeout/interruption, and POST/GET stalled-body tests.
Request timeout plus BodyHandlers.ofInputStream alone is insufficient. Preserve
HTTP error status without trusting its body. X-Correlation-ID is an optional ASCII
observability projection; the opaque body value remains canonical, with no trim,
encoding alias or use of the header for fingerprint/authorization.

A committed outbox row certifies durable intent, not external delivery. The
approval event must not be presented as externally supported merely because
the existing statement transport accepts its JSON. Before certifying delivery,
require a consumer that handles the event and validates authenticated scope,
and ACK/probe evidence bound to the immutable envelope and payload. A UUID-only
ACK, a generic inbox, or a fresh adapter in the same JVM does not establish
that guarantee or a process-restart proof. Reuse the existing transport;
do not create a parallel dispatcher to hide an unfinished consumer contract.

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
storage and must not fabricate post-cutover `READY`. V16 storage and the
protected kernel are published in Metadata rc.150; publication alone does not
prove a working host consumer, composition/lifecycle/HTTP `ATOMIC`, B4 completion,
or exactly-once external effects. Host adoption and those separate gates require
their own evidence.

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
