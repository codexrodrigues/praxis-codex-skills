# Bulk unit authority outside HTTP

Use this procedure when auditing or extending a host callback that executes an already
accepted durable bulk unit after its originating HTTP request has ended. This is not
permission to publish ASYNC, create a subject endpoint, or bypass public profiles.

## Inspect before extending

Inspect Metadata BulkExecutionUnit, BulkFingerprintContext, existing admission/mutation
callbacks and JdbcBulkDurableExecution; then host QuickstartOperationalContextResolver,
QuickstartPrincipalGrantRepository, MissionParticipantScopeAuthorizer,
MissionParticipantEvaluationProvider and MissionParticipantExecutionService. Verify the
actual pinned artifact exposes the intended entry point. Internal/package-private pilot
methods and protected worker internals are not public extension APIs. The B5b.3
private candidate adds explicit public composition; inspect its exact artifact and read
`praxis-java-autoconfiguration-starter-maintenance/references/bulk-worker-composition.md`
for binding provenance, fresh callback pairs and independent JAR consumer proof. This
seam does not itself make ASYNC ingress or current host adoption operational. If an external
host cannot compose the worker, record the real Metadata contract gap; do not use
reflection, direct kernel SQL, a fake request, a host bridge or a duplicate registry.

Separate owners: Metadata controls durable units/receipts/fences; Config owns governed
policy; the host owns immutable tenant/environment binding, current grants and domain
rules. The accepted subject comes only from the kernel-materialized persisted proposal,
never a request parameter, copied JWT, cached grant, inherited SecurityContext or browser
session. A background unit is not a newly authenticated HTTP session.

## Resolve and retain authority

1. Before a grant query, compare the complete expected CanonicalOperationRef (group,
   operation ID, path, method), resource key and server-configured namespace with the
   accepted unit. Validate the accepted subject; reject anonymous/guest identities.
   Required authority is fixed by server operation composition.
2. Reuse the existing Context and independently budgeted READ_COMMITTED current-grant
   query. Tenant/environment come from the server binding and exact grant, not intent.
   Preserve HTTP header checking and Config attribute hygiene on the HTTP entry path.
3. The current grant read is a candidate photograph, not mutation authority. Retain the
   exact physical grant G in the kernel's writable domain transaction before E→M→P
   locks. Verify captured and current fields/references, grant fingerprint, policy,
   schema revision, target versions/dependencies and final candidate. Do not suspend
   the unit or open another domain transaction to obtain a convenient context.
4. The off-request and HTTP paths share one admission body and the existing mutation
   callback. Scope prepared
   values to one invocation/unit and clear them before admission, on consumption and
   on every failed/finished invocation; no singleton holder or ThreadLocal cache.
5. Use the same absolute remaining budget; account for independent connection acquisition
   and do not renew deadlines or increase timeout to make a test pass.
6. Let Metadata check receipt before new-mutation gates. Confirmed replay must not consult
   fresh grant/Config or call domain callbacks, including after revocation/expiration.
   Domain and receipt commit or roll back on the same physical unit transaction.

## Prove the concrete consumer

Use real PostgreSQL and a real grant resolver, not a fixture that always returns a
fixed context. Run on a distinct thread with SecurityContext and RequestContextHolder
empty. Prove positive domain/receipt commit; causal grant revocation after the first
commit but before the next unit; failure after real flush with domain/receipt rollback
observed by a second connection; interleaved invocations with distinct prepared values;
wrong complete operation/resource/namespace/subject rejected before grant/private
projection; and replay through the new service path after revocation, expired deadline
and simulated policy outage with zero authorization/policy/domain callbacks. Existing
pending-ACK recovery evidence stays qualified; a terminal replay is not a new recovery
proof. Preserve focused HTTP auth/header/attribute regressions where resolution is shared.

Concrete candidate source/tests: quickstart docs/BULK-OFF-REQUEST-AUTHORIZATION-B5B3.md,
MissionParticipantExecutionServicePostgresTest, MissionParticipantExecutionServiceTest,
QuickstartOperationalUnitContextTest and QuickstartOperationalContextHttpTest. These
sources may belong to an unintegrated candidate: inspect the execution record and actual
checkout before using them as released behavior. Public SYNC proof does not demonstrate
ASYNC admission, worker composition, HTTP202 or backend completion.

## Evidence and baseline incompatibility

Capture HEAD, diff/full relevant source freeze before/after, resolved public artifact
origin/checksum and actual test classpath, Java/PostgreSQL versions, raw command exit,
fresh XML with negatives/assertions and cleanup. A build failure before test execution
is not a failing domain test. If unrelated main sources require symbols absent in the
public pinned dependency, identify their unchanged blobs and missing JAR classes,
preserve the RED and coordinate the owning source/public-adoption correction. Do not
exclude those sources, install a candidate under the public GAV or claim an override is
public adoption. A separately approved proof on the last compatible baseline can advance
independent work, but does not certify current main or permit its merge/deploy.

Review pilot docs for authority ownership, datasource/physical-grant distinctions,
operator diagnosis, supported limits and reproducible scoped tests. Update this existing
skill when the procedure changes; do not create a skill for each phase. Final acceptance
requires independent source/evidence review and any public integration/adoption gate
that remains open; hashes alone do not certify the business guarantee.

## Candidate Worker Consumption Is a Separate Proof

For the B5b.3 private seam, construct infrastructure and all nine provisioned binding
coordinates using public APIs; keep protected owner/job seeding in the canonical test
harness. Never import a package-private kernel factory into a host or expose enqueue
just to run the consumer. A source-package helper alone is insufficient: compile the
consumer against the private JAR without SDK class/test output, check exact CodeSource
and byte provenance, then run real domain/receipt units and terminate exclusive resources.

Keep callback preparation fresh per unit across concurrent worker invocations. Factory
only allocates local state after receipt-first lookup; admission receives the real unit
and resolves current database grants. Cleanup only discards local state, never performs
policy/domain/TX work, and cannot mask confirmed effects. Stop callback acknowledges
actual termination, not a timed-out join. Runtime JDBC evidence does not imply JPA or HTTP.

Reuse the host's qualified off-request grants evidence only when its source/dependencies
remain unchanged. SDK worker composition and its private packaged-consumer proof do not
resolve a current-main host dependency incompatibility, publish a release, enable ASYNC202
or close B7. Separate original RED fixture campaigns, targeted repairs and reused PG
proofs; do not announce a fresh green full verify from their combined test counts.
