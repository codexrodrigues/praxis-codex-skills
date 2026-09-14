---
name: praxis-java-command-concurrency-authoring
description: Use when implementing, auditing, or migrating a Praxis Java business command with state changes: @WorkflowAction, command request/response schemas, ResourceCommandExecutionRequest and Result, idempotency, item or collection scope, resource version ETag, If-Match preconditions, conflict/denial outcomes, action availability, and safe Angular/runtime handoff.
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
6. Align action catalog, capabilities, `ResourceStateSnapshot`, endpoint enforcement,
   and `_links`. Availability is not security; execution enforces the same decision.
7. For collection commands, define per-item outcome, atomicity, partial failure, retry,
   and ordering. Never report complete success when targets were denied or conflicted.

Read [command-outcome-matrix.md](references/command-outcome-matrix.md) when selecting
scope, preconditions, idempotency, result status, or focused proof.

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
  preconditions, action discovery, schemas, and capability projection.
- The host owns domain transition, transaction boundary, operational datasource and
  adoption of idempotency storage, external-effect coordination, and authorization.
  Metadata owns the shared bulk infrastructure described below. Do not leak database version,
  package, queue, token, or internal exception details.
- `praxis-ui-angular` consumes action schemas, links, capabilities and safe conflicts.
  It does not infer idempotency or manufacture `If-Match` locally.

Do not resolve command intent from labels, route fragments, keywords, regexes, or aliases.
Use resource/action IDs, schemas, availability, capabilities, and governed context;
text can only rank already-scoped candidates.

## Bind Bulk JDBC Work To The Operational Transaction

`BulkExecutionInfrastructure(dataSource, transactionManager, namespace)` is the
Metadata-owned explicit integration boundary. It provides transaction participation. Storage is composed explicitly through
JdbcBulkProposalStore; neither class is an executor, worker or runtime capability. Construction
performs no database access or DDL. The namespace is explicit and stable; it is not
authentication or authorization and must not be inferred from untrusted headers.

Use the actual shared datasource instance with a local JDBC manager or a JPA manager
whose EntityManagerFactory exposes the same datasource through EntityManagerFactoryInfo.
Initialize the beans first. The initial subset rejects opaque/mismatched managers,
routing and datasource wrappers; do not compare URLs or choose a Primary bean.

`withConnection(ConnectionCallback)` joins MANDATORY, writable, existing physical
transactions through JdbcTemplate. No independent transaction is started. The callback
must not commit/rollback, change auto-commit or retain the connection. Its return is
provisional until the outer owner commits; authorization, deadlines and receipt semantics
remain separate. Manager-visible rollback-only is rejected; a local outer status mark
may not yet be visible to a participant. Stop mutations when the owner decides rollback.
The binding rejects globalRollbackOnParticipationFailure=false at construction and before
work, preserving the required rollback-only behavior when a callback fails.

Prove the adopted pair with real PostgreSQL/JPA: same backend PID for JPA/JDBC, independent
observer before/after commit, both writes rolled back, deferred constraint failing at
COMMIT after callback completion, manager mismatch, and two-connection lock contention.
Use BulkExecutionInfrastructureTest and BulkExecutionInfrastructurePostgresTest. Fixture
tables are not the production ledger DDL; this gate does not certify fencing/replay or
bulk execution. Consult Metadata docs/spec/BULK-EXECUTION-INFRASTRUCTURE.md.

## Persist Protected Bulk Inputs Explicitly

Compose `JdbcBulkProposalStore` with the same BulkExecutionInfrastructure. Persist a
`BulkStoredProposal` containing the UUID, microsecond timestamps and immutable
`BulkIntentSnapshot` (trusted context, built-in identity codec, modality and intent).
This initial adapter accepts EXPLICIT/SYNC inputs in all three modalities. It is not
a READY evaluation, a captured QUERY manifest, admission/quota control or a receipt.
Do not persist the redacted public BulkProposal as execution input.

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

The SDK beta constructor has no compatibility path without governance. Old evaluation
payloads without it are CORRUPT even with an otherwise valid old hash; recover input only
to obtain a new governed evaluation. Do not rewrite immutable evidence or invent history.
V1/V2 SQL checksums remain unchanged. Prove BulkGovernanceEvidenceTest and the PostgreSQL
legacy/readback cases in addition to the existing suite.

`JdbcBulkProposalStore.insertEvaluated` inserts input plus evidence atomically in the
existing physical transaction; no attach/update/upsert. Re-evaluation needs a new UUID.
`findEvaluation` scope-checks the input and verifies the protected companion binding;
missing evidence is not reconstructed, corrupt linkage is not a fallback to input.
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
