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

## Rebase the adapter onto the current host

Inspect the current resolver and execution service before reusing a historical
off-request patch. Preserve connection-acquisition reserves, the current-grant
query deadline, diagnostic reasons, HTTP header checks and Config attribute
hygiene. Share the admission body instead of replacing the current classes with
an older candidate.

A callback factory must perform no I/O and allocate independent prepared state
for each pair. Admission resolves the persisted kernel subject with the complete
server-bound operation and namespace; an unrelated SecurityContext must have no
effect. Mutation consumes prepared state once, and cleanup only clears that
state. Test two interleaved pairs, failed admission and cleanup, plus the existing
HTTP path. Unit doubles establish adapter behavior, not a physical grant lock or
domain/receipt atomicity; those require the scoped Neon consumer proof.

An adapter can be prepared while the host still accepts only SYNC. Do not silently
open ASYNC in unit-input validation or wire an automatic worker as part of the
extraction. Public SDK admission, authenticated capacity provisioning, the host
HTTP contract and exact-artifact deployment each retain their own acceptance.

## Candidate Uniform ASYNC Host Adoption

When adopting the uniform mission-participant operation as ASYNC, inspect the exact host source and candidate/released Metadata APIs first. Retain `operations.missao-participantes.bulk-update-evaluate`, `operations.missao-participantes.bulk-update`, `/bulk/update/evaluation`, `/bulk/update` and the canonical `bulk-update` capability. Do not declare a second UNIFORM_UPDATE/PER_ITEM operation on the same resource or invent an execution-mode suffix: the canonical CRUD capability identity does not distinguish SYNC from ASYNC. This beta migration retires fresh uniform SYNC/QUERY ingress on this host; it does not remove SDK SYNC/QUERY or change the host's other operations.

Require ASYNC/EXPLICIT/PER_ITEM for new uniform work. Keep the host's explicit 200-target bound, five-second unit deadline and original pool/lock reserves; the SDK's 10,000-target ceiling is not a host or scale acceptance. Missing all six provisioned capacity coordinates leaves the uniform descriptor/lane unavailable and other families intact; partial or invalid coordinates fail startup. Reuse deployment, tenant and environment from the existing server binding. Validate scalar configuration without MVC/DB work, then resolve lane/worker dependencies only for a complete binding. Configuration is neither installation, current capacity, grants nor READY.

Provision capacity outside the application with the canonical administrative entry point. `BulkCapacityProvisioningMain` is a separate candidate JVM for existing bootstrap/enroll/attestation/activation/issue/install steps; inspect the exact published JAR and its independent provisioning proof before adopting it. Never copy package-private installation SQL, reflect into the kernel, pass owner credentials to the HTTP host, or declare the candidate command public merely because its source exists. Preserve private inputs/receipts, ordinary runtime/control identities, exact nine-coordinate binding and child-only Neon assignment.

Capture through lifecycle-minted ASYNC ReadyAdmission before preparation, with fixed proposal timestamps/expiry and the original bounded writable transaction. Confirm using public enqueue; do not advance a unit in HTTP. Bind the canonical worker to the same operational datasource/transaction manager and exact operation reference; allocate fresh callback pairs per unit, resolve current database grants from the persisted kernel unit without request/JWT/SecurityContext, and keep kernel-owned transaction/fences/receipt distinct from the host callbacks that retain domain/grant locks, validate rules and perform the domain mutation within that same transaction. HTTP202/Location represents a durable nonterminal execution; a concurrent completed result may be HTTP200. Neither status proves every target succeeded.

Keep authorized historical proposal/execution/result reads using their persisted mode and exact evaluator revision, independently of the current ASYNC profile. For a retired SYNC confirmation, use the canonical proposal/key/revision finder only to observe an existing reservation; never call reserve/advance, fabricate an expired deadline, renew validity or insert when it is absent. Current HTTP authorization and full-target reader grants still apply. A lookup may acquire transaction locks; do not label it PostgreSQL READ ONLY. Preserve all historical rows and replay the original key, without granting an unconfirmed historical proposal new admission.

The current Angular BASIC client supports SYNC/EXPLICIT/PER_ITEM and must omit the uniform ASYNC-only capability rather than force SYNC. Its accepted unit/mock receipts and the historical BASIC nine-phase proof do not certify ASYNC UI or the new host adoption. Require independent exact-artifact Neon HTTP receipts for authenticated evaluation with zero effects, durable enqueue/Location, worker commit/read/results/replay, one effect/receipt and the specified negative boundaries. Capacity provisioning, scale8/80 and deployed Render acceptance remain separate. Update consumer docs/corpus only where the actual published reference is affected; keep historical receipts qualified.

## Separate historical SYNC proof from current-candidate continuation

When historical setup runs in CI before a current-candidate host consumes it, use
separate reviewed product and test-only checkouts. Package only the exact legacy
product commit/tree with its public dependency versions and checksums; prove that
additional proof code leaves legacy production, POM and storage resources unchanged.
Capture tracked checkout bytes before and after packaging alongside HEAD/tree and
clean status. Respect the checkout's Git filters and line endings: a working-file
hash need not equal the committed blob hash. Do not overwrite files from Git blobs,
normalize bytes or exempt changed source to force custody equality.

Build before injecting private inputs, with a public-only mirror and isolated cache.
Prepare the test provider/executor dependencies without DB work before the remote
offline invocation. Disable Python bytecode in frozen checkouts with
`PYTHONDONTWRITEBYTECODE=1` or use an external cache; never ignore newly untracked
cache files to force clean status. Capture bounded preparation/startup diagnostics
before cleanup and distinguish dependency/provider failure from HTTP/domain oracles.
Bind the actual command, governed environment, host/nested JAR hashes, loaded
CodeSource/classes and test classpath; neither candidate classes nor cached private
coordinates may substitute for the legacy product. Freeze the proof source too.
Run only the assigned history cut on isolated Neon with fresh controls and real
identities/TLS. Compare complete before/after RR/RO snapshots of domain, authority,
catalogues, grants and historical rows, preserving row strings, duplicates, types
and UTC transport. Consecutive database snapshots are not a distributed transaction.

Hand off a validated closed receipt plus private IDs/original key and raw custody
hashes. Stop owned processes and verify cleanup; preserve the primary failure if
readback or evidence writing also fails. Export only the allowlisted receipt and
code-only diagnostics; secrets, session/CSRF, HTTP bodies and raw rows remain private.
Public hashes bind private custody; they do not claim raw export or autonomous offline
access. Before continuing, freshly match the full snapshots and handoff to the receipt.
Do not rerun Main, the legacy JVM or completed setup, fabricate history with owner
DML, restart the whole BASIC proof, renew proposal/execution TTL or use local DB.

For the authorized historical creator after actual proposal expiry, require proposal
GET410/BULK_GONE while retained proposal-results, execution/results and original-key
replay remain200 when current full-target authorization permits them. The fresh
reader/cursor budget does not renew admission validity. Preserve stored mode, exact
execution identity, domain and receipt; reject new confirmation of the retired
unconfirmed SYNC proposal. This cut proves historical behavior only: current ASYNC
HTTP/worker, scale and deployment still need their own exact-artifact receipts.
Inspect `scripts/sync-history-proof/{package.py,run.py,README.md}` and the host's
`BulkAsyncUniformPackagedNeonProof` receipt/continuation checks before adapting it.
