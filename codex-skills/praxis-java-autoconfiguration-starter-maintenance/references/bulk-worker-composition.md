# Explicit Durable Worker Composition

Canonical owner: Metadata. Inspect `BulkDurableWorkerComposition`, `BulkCapacityBinding`,
`BulkDurableWorker`, `JdbcBulkDurableExecution`, `BulkExecutionInfrastructure`, and
`docs/technical/BULK-WORKER-EXPLICIT-COMPOSITION.md` in the exact SDK candidate consumed.
The B5b.3 seam was proved against private version
`8.0.0-b5b3-worker-composition-20261008-SNAPSHOT`; this is not a published dependency
or proof of current host adoption. Public rc.155 does not contain this candidate API.
Do not teach protected internals as public APIs in older artifacts.

## Compose From Public Inputs

1. Bind the stable operational datasource and local transaction manager used by domain
   mutation through existing `BulkExecutionInfrastructure`. JPA additionally requires
   the same exposed datasource in manager and EMF; a JDBC consumer proof does not prove JPA.
2. Supply canonical `BulkCapacityBinding` from trusted provisioning, outside request
   headers and restored copies. Preserve all nine fields: deployment, tenant, environment,
   binding, generation, database UUID, attestation UUID, authority UUID and authority epoch.
   Nonblank canonical texts, nonnull UUIDs and positive generation/epoch only validate
   configuration. They do not attest authority. Never invent UUIDs, infer identity from
   JDBC URLs or equate binding generation, authority epoch and execution owner epoch.
3. Declare each resource plus complete canonical operation (group/id/path/method), with
   a fresh per-unit factory of admission/mutation/cleanup callbacks. Lists are copied;
   duplicate operations/bindings and more than eight bindings are rejected. Construction
   does not connect to DB, migrate, install grants or start work.
4. Call `compose` and explicitly register the returned `SmartLifecycle` in the host.
   A nonempty registered lifecycle auto-starts at Spring refresh; empty does not.
   This explicit registration is not starter discovery or automatic worker activation.
   Do not publish an extra kernel constructor, registry, annotation or host claim loop.

The owner separately provisions/migrates/installs rights. The runtime receives no owner
credentials. Expected binding is checked against existing durable marker, attestation,
ledger and fences. The worker's owned-unit kernel is not a QUERY admission bypass;
new proposal admission/lifecycle remains in its existing owner. Public DTO/HTTP ingress,
ASYNC202, availability/READY and B7 are separate gates.

## Per-Unit Authority and Preparation

Factory is lazy inside real kernel admission, after receipt/admission replay lookup.
It allocates local state only: no Config/grants/policy/domain access before receiving
an immutable actual unit. Admission resolves current grants from persisted subject/
context and trusted server operation, using remaining budget. Never propagate JWT,
request, SecurityContext or a mutable singleton preparation to the worker.

Admission and mutation share that invocation's pair. Mutation participates in the
existing kernel transaction; domain and receipt commit or roll back together. Cleanup
runs once per allocated pair after execution returns/throws, including denials/failures;
it only discards local state and must not open transactions, read policy or mutate domain.
Cleanup failure is sanitized and cannot mask original durable outcome or retry mutation.
Confirmed replay allocates no pair and calls no exclusive new-mutation gate.

No hard deadline exists for arbitrary callback/cleanup or pool acquisition. Stop requested
is distinct from thread terminated: stop callback confirms actual termination; bounded
synchronous wait may remain pending. Do not close runtime pools before real termination
or treat timeout as shutdown acknowledgement. Recovery does not execute new mutations.

## Prove the Artifact, Not Only Source Compilation

Use a new private GAV/cache/target, never install modified code under a public coordinate.
Compile an external-package consumer against the actual private JAR and dependencies
with NO SDK target/classes or target/test-classes. It constructs infrastructure and the
canonical expected binding itself; do not hand it a magical internal kernel. Keep owner
setup/protected job seed in a separate canonical test harness, not in a public enqueue API.

Run with JAR first and independently compiled consumer before test harness classes;
exclude SDK target/classes. Compare exact CodeSource real paths, actual JAR classes/
resources/migrations sets and bytes with frozen output, JAR/private POM identity and
hashes, dependency classpath, source before/after, commands/exits/logs/timestamps and
owned-resource cleanup. A wrapper that catches errors and exits zero is not a passing
proof; inspect each real stage and assertion result. Do not fix class counts by assumption.

Test fresh pair identity under concurrent workers sharing an Operation, cleanup on
success/denial/failure, throwing cleanup after commit, replay factory zero, real domain+
receipt rollback, physical observer PID/XID, full identity and truthful stop. A standalone
artifact harness is not JUnit; package with skipped tests is not verify. Preserve RED
campaigns and reuse only unchanged qualified evidence. Do not rerun valid PG suites
merely for documentation or guidance changes.

The recorded private proof used Java21.0.10/PostgreSQL14.22, 18 PG JUnit from V2 plus
three structural JUnit from a V3 test-only fix, and an independently compiled JAR consumer
with two domain/receipt units. Those are separate qualified proofs, not a new full verify,
public HTTP deployment, generic host grants implementation or backend completion.
