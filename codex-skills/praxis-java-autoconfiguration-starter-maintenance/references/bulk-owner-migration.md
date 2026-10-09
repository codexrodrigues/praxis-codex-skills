# Opt-in bulk owner migration and recovery

## Inventory and authority

The canonical implementation is Metadata's `BulkExecutionMigrator`, not a host
recipe or raw Flyway call. Inspect its current source, SQL resources, initializer,
phase markers and focused migration tests before recommending a command. Migration
is explicit deployment work; context startup must not silently run owner DDL.
Keep owner, runtime and control roles distinct and declare the complete actual
runtime role set. Do not widen ACLs, invent grants or heal catalogs to make a test pass.

A changed SQL/resource sequence requires an impact map before editing: immutable
prior versions/checksums, pending and completed states, lock order, retained data,
consumer JAR provenance, and minimum tests. Historical labels in this reference
are evidence of a private candidate, not a promise that every published SDK includes it.
Check release/tag/JAR and host dependency separately.

## Staged migration boundary

The private V20 worker-queue candidate first attests and upgrades to V19 under the
existing owner coordinator lock, resumes canonical owner initialization, completes
capacity/occupancy phases, then reenters strict attestation before V20. Raw Flyway
history alone does not establish completed bootstrap or runtime authority.

Propagate the validated phase vector through nested owner validators; strict
serving/current validation and initializer validation after grants must remain
strict. Preserve the existing atomic grant-before-COMPLETE interval and phase CAS.
Do not reuse the permissive pending context after completion. A retained coordinator
loan must be released before initialization acquires its own resources.

Only a genuinely pending historical V19 installation with V8 manifest PENDING may
lack lifecycle derivations or the initial deny-only global identity. Existing
bindings, digests, authority rows, allocation tuples, catalog shape, ACLs and quota
projections still require exact validation. Derive absent data with the existing
initializer and explicit deployment map; never overwrite existing values or invent
published authority. COMPLETE V8 with other pending markers and current V20 must
reject missing global identity without repairing it. READY remains a separate gate.

## Publication identity at the V14 creation boundary

For the C17 candidate, inspect `PublicationCreationCallback` in
`BulkExecutionMigrator` before adopting a historical pre-V14 upgrade. This is
an instance-local Flyway callback on the canonical owner migration lane, not a
host repair command, SPI or a new SQL migration. Immutable SQL/checksums remain
unchanged. Check the actual released artifact before claiming this behavior is
publicly available.

BEFORE/AFTER events must identify the exact V14 script and checksum. Both run on
the same transactional PostgreSQL connection, backend and transaction, as the
configured authenticated owner (`session_user == current_user`), distinct from
the coordinator connection but in its database. BEFORE attests the protected
predecessor, locks namespace bindings in stable namespace order, validates the
explicit deployment map and requires their durable deployment buckets. AFTER
requires the same witness and unchanged bindings, then inserts one deny-only
`UNCOMPOSED / 0 / null` global identity per distinct bound deployment, in stable
deployment order. Empty bindings seed no synthetic deployment. Subsequent canonical
initialization remains responsible for configured fresh identities.

The identity inserts share the physical V14 DDL transaction. Flyway may use its
main connection for history: do not claim a single physical transaction for DDL,
seed and history. Prove rollback/retry for callback failure and deterministic
history INSERT failure separately; this does not establish uncertain-commit
reconciliation. Do not use `ON CONFLICT`, additional connections, manual commits, raw ledger repair,
publication or READY as a fallback. An already-applied V14 installation never
runs this creation callback: a missing ledger there is rejected, including when
another bootstrap latch is pending. Raw Flyway calls are not the canonical owner
entry point and do not acquire this creation authority.

Attest trigger semantics through PostgreSQL catalog fields, not the rendered
`pg_get_triggerdef` string: function qualification can depend on visibility and
search_path. Require the expected BEFORE/ROW/UPDATE/DELETE bits, normal enablement,
no arguments, column restriction, WHEN clause or constraint, and the exact function
identity/body/owner/schema/fixed search_path and remaining attributes. An enabled
`WHEN(false)` trigger is not an immutability guard. Do not alter the connection's
search_path or relax function/ACL attestation to accommodate rendering differences.

Focused proof includes `BulkPublicationCreationPostgresTest` (fresh/empty,
rollback and retry, deterministic history INSERT failure, wrong predecessor,
transaction/backend/owner witness and enabled conditional-trigger rejection),
authentic public pre-V14 producers in `BulkHistoricalPre14UpgradePostgresTest`
and `BulkHistoricalPre14ProvisionedUpgradePostgresTest`, and the pool4 proof.
Retain already-applied V14/V15 and current V19/V20 no-heal negatives when their
source/paths remain valid. A deterministic failure before history insertion
commits does not prove an uncertain commit, lost acknowledgement or reconciliation;
those remain separate proofs. A candidate source-classpath pass does not prove
packaged or published host adoption, HTTP readiness, or whole-backend closure.

## Concurrent owner initialization

In the private C1 correction, `initializeGovernedLifecycle` takes the existing
transaction advisory `(1347574124,5)`, then singleton row latches in order
V8→V9→V11→V12→V16→V18→V19 before READ_COMMITTED phase/ACL attestation.
Read and lock each whole marker table; validate exactly one row, its version and
PENDING/COMPLETE phase. A filtered query must not hide an extra marker row.
The separate capacity-read and occupancy bootstrap transactions hold only their
respective V18 and V19 latches. Never add the coordinator advisory to those
transactions: the coordinator may already hold it while waiting for a separate
bootstrap connection. Do not introduce V19→V18 lock acquisition.

A committed grant-before-COMPLETE transaction must be visible before initializer
attestation; a rollback must leave the coherent PENDING/zero-controlled-ACL state
for canonical retry. Keep serving/preflight REPEATABLE_READ validation unchanged,
without write locks or additional grantee privileges. Preserve native waits,
existing pool budgets, search_path/role restoration and transaction cleanup;
this ordering does not add a whole-migration or initializer deadline.

Inspect the causal PostgreSQL tests
`BulkDurableMigrationPostgresTest#initializerWaitsForOccupancyPhaseAndAclCommitBeforeAttestation`
and `#initializerWaitsForOccupancyRollbackThenCanonicalRetryCompletes`. A test-only
barrier holds the actual bootstrap row lock; an external observer identifies the
initializer's exact SQL, distinct PID and `pg_blocking_pids` edge before releasing
commit or rollback. Bound observation below the holder budget; an elapsed-time
assertion alone is insufficient. Keep revoked-COMPLETE ACL rejection, V18 rollback
and two-owner V18 convergence alongside the pool4/pool5 proofs. The focused C1
campaign passed ten cases on PG14.22/Java21; it does not replace the preserved RED
full verify, prove packaged adoption, repair historical ledger provenance, or
certify ASYNC, a fleet or backend READY. Check the exact tree and artifact first.

## Evidence and honest scope

Use real PostgreSQL and immutable source/ZIP hashes, fresh XML, actual Maven exit,
artifact/dependency identity and before/after cleanup census. Preserve RED runs,
diagnose the first failed gate, and repeat only affected tests after correction.

For disposable PostgreSQL clusters, process ancestry alone is insufficient:
`pg_ctl` may daemonize the server before a sampler observes it. Capture each
owned cluster's launcher/server PID, data directory, port and actual Unix socket
from the test's logs or process receipts; then verify process identity and absence,
data-directory removal, TCP refusal and socket absence. Preserve the identity of
protected third-party clusters. Never infer ownership from a matching executable,
port or generic process name, or signal an unattested process.

Keep the actual Maven/child exits separate from collector exits. If tests pass
but the collector misses a cluster, retain the original failed collector receipt.
A separately versioned, independently reviewed read-only supplement may establish
cleanup from existing exact receipts and current checks without rerunning valid
tests. Corrections must preserve earlier supplements and state which observation
was wrong; incomplete cleanup evidence is not a passing collector or backend gate.

Focused examples in the candidate are `BulkWorkerQueueIndexPostgresTest`, retained
row/binding/COMPLETE negatives in `BulkDurableMigrationPostgresTest`, and the retained
V7 upgrade in `BulkEvaluationStorePostgresTest`. Assert full retained content (including
byte arrays by content), prior history/checksums, no writes on rejection, canonical
retry and zero-work replay. Do not pregrant PENDING-controlled ACLs in fixtures.

A staged coordinator change also needs a real bounded-pool proof, such as
`BulkOwnerMigrationResourcesPostgresTest#freshPublicOwnerMigrationFitsFourPoolConnections`.
Observe acquisition/waiting/cleanup and strict final validation. A positive pool4
result proves that case, not a minimum pool size, zero waiting or fleet readiness.

For the V20 index, attest the exact partial index, ownership, key order, predicate,
access method and validity. Replays reject physical drift without repair. Measure
real runtime EXPLAIN plans with canonical seed, existing rights and timeouts; do not
force the planner. Parent buffer counts are inclusive; Index Only Scan can still
perform heap fetches. Finite cached PG14 measurements do not certify SLO, T13 or PG16.

## Causal historical backfill fixtures

A fixture proving a backfill must reach that gate with the protected predecessor
catalog, durable deployment binding, role ACLs and normal trigger enablement intact.
Assert the first rejection actually reached in the canonical migrator; a failure
in an earlier Flyway callback or catalog/role attestation does not prove data
backfill rejection. Preserve exception wrapping and the exact cause, history
prefix, pending markers, absent later migration and unchanged grants.

Inject corrupted legacy payloads only inside a test-owned disable/update/enable
window with re-enablement in finally, completed before invoking any migrator or
validation callback. Use the same bounded window to restore the valid payload.
Do not weaken production trigger/catalog guards or grant additional runtime
privileges to make the test reach a preferred error.

A rollback proof with a valid row followed by a corrupt row must fix their ordered
identities and assert their database order matches the canonical traversal. Random
UUIDs can make the corrupt row first and leave zero derived rows without exercising
rollback of preceding work. Require the error to identify the later corrupt row,
zero committed derived rows and the pending phase; then canonical retry and exact
zero-work replay must preserve the historical prefix and provision only intended
new privileges. Deterministic order and a focused pass do not alone establish
public artifact adoption, whole-backend readiness or uncertain-commit recovery.

## Historical producer and evidence reconciliation

Before transplanting a consumer fixture to a historical published SDK, inspect the
immutable published POM and corresponding tag, including the Spring Boot,
Springdoc and migration dependency baseline. A current consumer parent can be
incompatible with a historical SDK even when compilation succeeds. Keep the
historical producer dependency set coherent with that published baseline; do not
force execution by overriding the SDK dependencies or disabling converters.
Prove the actual JAR/POM/GAV, native SQL resource bytes and runtime CodeSource,
and exclude current candidate classes from the producer classpath. Create retained
state through the historical public APIs, not raw rows or fabricated phase markers.

For historical SDK fixtures required by the official `clean verify` gate, use
Metadata's pinned `download-maven-plugin` executions in `generate-test-resources`
and the test's canonical default under `target/historical-bulk-sdk`. The V19
fixture is `metadata-v19-rc155.jar`, verified against its fixed Central SHA-256
before loading the native SDK. An explicit fixture property may support a scoped
historical campaign but must not be required to make the release workflow work.
Missing or changed bytes remain a failing gate; never skip the historical test,
install a current public GAV as a replacement, or fall back to current classes.
Inspect `pom.xml`, `BulkWorkerQueueIndexPostgresTest` and the workflow's actual
`clean verify` command together before claiming release-test preparation complete.
This wiring proof does not replace the official complete release verify.

Compare artifact paths by physical identity as well as spelling. Resolve existing
paths and verify same-file identity, content hash and the actual CodeSource/classpath;
filesystem aliases such as `/tmp` and `/private/tmp` can refer to one file. Do not
invent an alias or accept a different artifact merely because its filename matches.
Qualify hashes collected after execution as after-run observations.

Record Maven's numeric process exit, the nested consumer exit and the collector's
exit separately. A collector path-comparison failure is not a Maven or runtime
failure. Preserve the original failed receipt and RED result; if independent
read-only reconciliation proves the physical artifact and all affected gates,
retain that supplemental review alongside the original evidence. Never rewrite
receipts, relabel the original collector as passing or repeat an already valid
runtime campaign solely to erase an evidence-collection defect. A characterization
of a blocked upgrade does not prove successful historical adoption or authorize
ACL/ledger repair; identify the first reached rejection and unreached gates.

## Packaged consumption and delivery

After source proof, build the private candidate into an isolated cache, verify
JAR/POM version and resource bytes against source, then use an independent consumer
whose runtime CodeSource is that JAR. Source-classpath tests do not prove packaged
resources or adoption. Assert V20 resource provenance and migration opt-in without
making the host or public Maven coordinate a local override target.

Record separate states: private tested, integrated, published, adopted and accepted.
A canonical skill change requires manifest hashes, structure/family audits,
independent review, branch/PR integration and selective installation sync. Do not
reopen unrelated worker guidance or overwrite existing destination drift. Public
recipes, release/deploy and Angular handoff require their own authorized gates.

## Maintenance cutover and scope of attestation

Live function catalog attestation may bound expensive identity decoding with the
already resolved canonical schema and function names before checking exact
signatures. Names are a query prefilter, never authority or a substitute for full
signature, expected-set equality, body, owner, attributes, fixed search_path and
ACL tuples. Preserve native live-attestation statement and reader deadlines;
do not cache authority or increase budgets to hide catalog cost. A healthy
EXPLAIN/rowset comparison is supplemental evidence: require the actual cursor
continuation and live corruption/membership/ACL/owner/search_path/missing-identity
negatives before accepting a query change. A finite isolated timing observation
is not a load/SLO, complete timeout cause or public artifact adoption proof.

The private candidate adds V20 while the public host still adopts rc.155/V19.
Stop admission and drain old executors before owner maintenance; perform the
canonical upgrade and strict V20 validation before admitting the candidate.
An old V19 reader can reject V20: no mixed-version rollout or online-upgrade SLA
is proven. Owner DDL/index creation can lock relations and consume I/O; the
coordinator SQL budget is not a bound on the pool, entire DDL, network or callbacks.

Inspect all seven latches: V8manifest, V9preview, V11preview-integrity,
V12preview-reader, V16atomic, V18capacity-read and V19occupancy. Validate coherent
prerequisite phases, zero controlled ACLs while PENDING and exact grants after
COMPLETE. Another PENDING latch never licenses repairing a COMPLETE one.

Index attestation is performed by owner migrate/validate/readiness. The live
job role keeps its existing ACLs; this does not claim online index-drift detection.
Inspect `BulkExecutionMigrator` and V20 SQL, `BulkWorkerQueueIndexPostgresTest`,
retained/COMPLETE negatives in `BulkDurableMigrationPostgresTest`, and
`BulkOwnerMigrationResourcesPostgresTest` in the same candidate source.
