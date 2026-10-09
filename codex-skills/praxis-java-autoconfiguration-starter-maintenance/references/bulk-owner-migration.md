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
