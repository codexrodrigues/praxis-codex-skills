---
name: praxis-java-autoconfiguration-starter-maintenance
description: Use when implementing, auditing, or evolving praxis-metadata-starter Spring Boot auto-configuration: @AutoConfiguration, @ConditionalOnMissingBean, configuration properties, SPI extension points, bean ordering, OptionSourceProvider/registry/executor wiring, AutoConfiguration.imports, starter bootstrap tests, host compatibility, and public contract impact.
---

# Praxis Java Auto Configuration Starter Maintenance

Treat auto-configuration as a public integration contract. It must give a host
one predictable canonical implementation, leave documented extension points, and
fail clearly when a required capability cannot be composed.

## Inventory Before Adding A Bean

Inspect the affected auto-configuration class, `AutoConfiguration.imports`,
configuration properties, existing conditional beans, SPI interfaces, consumers,
starter bootstrap tests, and a real host. Classify the need as supported,
poorly materialized, partial, or a real contract gap before adding a property,
bean, provider, executor, or configuration class.

Map owner, direct consumers, public metadata/HTTP impact, properties/defaults,
override behavior, ordering, validation, and breaking risk. A host-local bean
override is not a replacement for an ambiguous starter contract.

## Evolve The Starter Safely

1. Put canonical wiring in the responsible auto-configuration class and register
   it in `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`.
2. Use conditional registration only for intentional extension points. Name the
   default, the override contract, required collaborator, ordering rule, and
   failure behavior. Do not create two beans for the same public facade.
3. Keep a single `OptionSourceQueryExecutor` facade backed by the composite
   executor and provider registry. Register JPA as provider fallback; host-specific
   providers extend the SPI and order explicitly instead of adding executor beans.
4. Bind public configuration through typed properties with safe defaults and
   validation. Do not use undocumented environment reads or host-specific magic
   flags to alter public resource semantics.
5. Preserve canonical owner boundaries. Metadata starter owns metadata/discovery
   composition; config starter owns config persistence/authoring; host owns domain
   beans and private integration adapters. Do not move semantic decisions into
   auto-configuration merely to make a sample start.
6. When wiring affects `x-ui`, schemas, option sources, surfaces, actions,
   capabilities, headers, or runtime behavior, treat it as public contract work:
   map consumers and update focused proof rather than relying on context startup.

Read [bootstrap-contract-matrix.md](references/bootstrap-contract-matrix.md)
when selecting a condition, property, SPI, ordering rule, or validation gate.

## Preserve Explicit Bulk Infrastructure Adoption

`BulkExecutionInfrastructure` is a host-constructed binding of the operational datasource,
local JDBC/JPA transaction manager, stable namespace/deployment, and an explicit
`BulkExecutionRoleConfiguration`. The four-argument constructor has been removed; runtime
configuration must include the provisioned schema owner and at least one runtime grantee role.
The role record also carries separate retention membership and control-plane grantee allowlists;
keep those roles disjoint and sourced from actual provisioning. The binding is not registered
automatically and does not run DDL or workers. Do not infer its collaborators by Primary, bean
name or URL. JPA requires the same datasource exposed by EntityManagerFactoryInfo and its manager;
initialize both first. Opaque managers, routing and datasource wrappers are outside the
demonstrated subset. Do not add a fallback connection when composition fails.

Every operational `withConnection` call re-attests `session_user == current_user` against the
runtime allowlist and checks live protected schema/table/function ACLs, ownership, and V7
descriptor-fence function/trigger definitions on the exact connection that will perform the
work. The attestation runs before namespace access and before the caller callback; a role or
catalog drift denies the operation without running it. `withLifecycleRead` performs the same
runtime attestation on its short independent lifecycle connection. This is a live drift check,
not the privileged provisioning/migration lane: it does not run Flyway or DDL, and successful
attestation alone does not compose a descriptor or prove an operation READY. Each attestation SQL
uses at most 250 ms while preserving and restoring a stricter prior statement timeout; 250 ms is
per statement, not a total budget for all checks. Runtime lifecycle reads cap lock and statement
timeouts at one and two seconds. The control plane separately requires its expected role in the
configured control-plane allowlist, rechecks its live identity/ACL/owner/V7 fence before CAS work,
and verifies the runtime connection sees its temporary advisory lock in the same physical
PostgreSQL database. Runtime and control-plane lifecycle checks preserve stricter configured
timeouts rather than broadening them.

Its withConnection callback requires a real existing writable transaction (MANDATORY),
with JdbcTemplate's connection bound to the configured datasource. It does not implement
registry/readiness, migrations or storage. A later runtime must compose and validate these
actual dependencies before advertising an executable operation; OpenApiDocumentWarmup is
optional/asynchronous and tolerates errors, so it is not an admission gate.

Validate BulkExecutionInfrastructureTest and the real-process
BulkExecutionInfrastructurePostgresTest before a host adoption. The latter proves JPA/JDBC
commit/rollback and lock contention on fixture tables with a restricted PostgreSQL login; the
control-plane PostgreSQL test proves live identity, ACL/owner/fence drift rejection and timeout
preservation for restricted runtime/control credentials. These tests do not prove a host's
production ledger migration or establish backend/API READY. No AutoConfiguration.imports change
is needed merely to add this explicit value/participant.

## Adopt The Protected Proposal Migration Lane

Run the explicit bulk migration outside Spring transactions. For a fresh schema,
migrate without configured runtime roles, provision the exact PostgreSQL roles/grants,
then call `BulkExecutionMigrator.validate(dataSource, roleConfiguration)` before runtime.
For an upgrade from V7 with existing exact evaluation grants, drain old writers and use
`BulkExecutionMigrator.migrate(dataSource, namespaceToDeploymentId, roleConfiguration,
operationIdentities)`. Supply the complete namespace-to-deployment map and declared
`BulkOperationControlIdentity` values. This lane is separate from host Flyway startup.
Metadata supplies optional Flyway core/PostgreSQL
dependencies (11.17.0 in the reference candidate); consumers choosing this adapter must
supply these dependencies.
Use `classpath:db/praxis-bulk-migrations`, schema `praxis_bulk`, and history
`praxis_bulk_schema_history`; do not put the SQL in the default db/migration lane or
baseline an unknown nonempty bulk schema. Existing tables in public remain independent.

Run privileged migration/validation outside domain transactions, then construct
JdbcBulkProposalStore using the operational datasource and transaction binding. Runtime
credentials need schema USAGE and only the exact table/column/function grants in the
`BulkExecutionMigrator` allowlist for the selected store path. The proposal/admission path
includes narrowly scoped UPDATE grants needed for PostgreSQL row locks and lifecycle
columns; never generalize those to unrestricted table UPDATE. Migration
credentials are not inferred or manufactured by the starter. History checksum validation
alone is insufficient: validate physical constraints and the enabled immutability trigger.
No bean, readiness capability or executor is registered automatically by adding the SDK.

V8 adds a private immutable ordinal manifest linked to the exact evaluation, not a
public results reader. `insertEvaluated` must persist evaluation, manifest and quota
allocation in one host transaction. The manifest keeps canonical wire identity and
expected version as lossless bytes; SQL must not cast protected JSON to `jsonb` or
place a potentially long identity directly in a unique btree index. A deferred
evaluation guard rejects old writers at commit. V8 Flyway DDL leaves a private
`PENDING` marker; a retryable Java bootstrap validates/backfills existing evidence,
grants only the new manifest to explicitly configured runtime roles already holding
exact evaluation rights, and marks `COMPLETE` in that same transaction. Failed
bootstrap retries while `PENDING`, even with zero new Flyway migrations. In
`COMPLETE`, validate all manifest rows against protected evidence without inserting
missing rows or restoring revoked ACLs, including during later migrations. Drain old writers before
V8 and reopen admission only after strict validation; the commit guard is a final
fence, not a rolling-upgrade plan. Keep schema, owner, ACL, retention/quota deletion
order and marker phase in the migrator's physical validator. The bootstrap marker
must have no non-owner ACL at all, including retention owner/executor and PUBLIC;
prove that an accidental UPDATE grant is rejected before it could reset COMPLETE.

The V9 preview migration is integrated in Metadata source, but host availability
still depends on the exact published starter revision; verify it before treating
this storage as an available contract. It keeps a separately persisted,
provider-approved public preview by
V8 manifest ordinal. The migration/bootstrap must create a preview state for
every evaluation: `COMPLETE` only for a typed evaluation with an explicitly
allowlisted projection, `UNAVAILABLE` when the provider deliberately declines a
safe projector, and `UNAVAILABLE_LEGACY` for historical non-typed evidence. Do
not backfill public rows from protected payloads. For `COMPLETE`, validate the
exact evaluation fingerprint, ordinal count/coverage, provider revision,
canonical allowlist and projection digest; only decision plus allowlisted
diagnostic category/code/message can enter the public rows. Targets, facts,
plans, protected text and metadata must remain absent.

Keep the state fence in the physical schema: a target-preview INSERT must verify
first that its parent preview state is `COMPLETE`, rejecting a later insert into
`UNAVAILABLE` or `UNAVAILABLE_LEGACY`. Do not add an explicit `FOR KEY SHARE`
runtime lock as a shortcut; it requires PostgreSQL `UPDATE` privilege and would
break the restricted runtime ACL. The composite foreign-key binding must instead
protect concurrent parent deletion, so migration proof includes a later
transactional insert rejection and an insert-versus-retention/delete race.

Run V8→V9 through the existing explicit privileged migration lane, with old
writers drained and the exact configured runtime roles verified before admission
reopens. The durable bootstrap phase may retry only while pending. Once complete,
missing preview state for any evaluation, missing target rows for `COMPLETE`,
altered digest, or revoked ACL is physical drift and must fail closed;
`UNAVAILABLE` and `UNAVAILABLE_LEGACY` instead require zero target-preview rows,
and any such row is corruption. Later migration invocations must validate rather
than recreate rows or privileges. Extend the
physical validator and retention/purge path in
the same cut, preserving foreign-key and quota deletion order and owner-only
bootstrap control. Prove V8→V9 upgrade/retry/no-heal, state coverage, allowlist
and ordinal/digest corruption, late target-preview rejection, concurrent
insert-versus-retention/delete, transaction rollback, restricted PostgreSQL
runtime/retention roles, expiry and purge. This migration alone adds no bean,
reader, HTTP endpoint, action/capability or READY; host adoption and public
authorization remain separate gates.

For the V11 item-integrity migration, verify the exact Metadata source revision
before adoption. Drain V9 writers and retention executors, await their in-flight
transactions, and keep both drained until `COMPLETE` plus validation; this is
not a zero-downtime cutover. Use the explicit privileged migration lane,
outside domain transactions and Boot's default Flyway path. The PostgreSQL DDL
must atomically install an owner-only `PENDING` marker, a physical guard blocking
every new preview parent while pending, and `integrity_version=11` with no
surviving default; after `COMPLETE`, a V9 writer that omits the version must
still fail. Bootstrap validates V8 manifest and the complete V9 projection and
allowlist against protected evidence before deriving per-item checksums from
persisted bytes. In one transaction it verifies leaves, schema/owner, trigger
bindings and ACL, then marks `COMPLETE` last. A failed or wrong-role bootstrap
leaves `PENDING` for retry; after completion, validation must reject drift and
never regenerate leaves or grants. Runtime roles receive only `SELECT,INSERT`
on the leaf table; privileged retention removes leaves before preview rows in
the governed expiry/purge functions, with the FK restricting orphan creation.
Prove fresh and V10→V11 migration, pending and DDL-wait fences, wrong-role retry,
no-heal, tampering, restricted grants, 10,000 items and expiry/purge in PostgreSQL.
Keep an explicit time/memory budget for the full V9/V11 privileged
`migrate`/`validate` scan; bounded pages do not make that scan cheap. V11
storage alone grants no reader,
cursor, HTTP route, authorization, capability or `READY`.

The RS2 reader's separate V12 bootstrap gate is integrated in Metadata source
at merge `17d102ec69c5e00c4b75101ad8c6f0f9652bb228`, but is not published.
Inspect the exact published Metadata revision before host adoption.
Keep the V11 marker owner-only; do not grant runtime
roles `SELECT` on either bootstrap marker. Flyway V12 installs a restricted
`SECURITY DEFINER` boolean function and owner-only `PENDING` marker. In the
explicit privileged lane, grant `EXECUTE` only to configured runtime roles
while V12 is pending; validate function signature/body/owner/search path,
`STABLE` volatility, effective ACL and role memberships, then mark `COMPLETE`
in the same transaction. Retry a failed pending bootstrap, but after completion
reject missing/revoked grants or catalog drift without healing. Live runtime
attestation must repeat the function/ACL checks, and the reader must call the
gate in its own read-only snapshot before any proposal rows. Drain older hosts
and retention workers through DDL, bootstrap and validation; the older binary
is not a rolling-upgrade participant. Prove fresh and V11→V12 migrations,
wrong-role rollback/retry, marker denial, drift/no-heal and old-binary catalog
rejection in PostgreSQL. V12 is an internal read gate, not HTTP/READY.

The V10 cancellation design is a candidate until its Metadata PR is integrated and published;
verify the exact source revision before adoption. It adds durable cancellation to the
protected execution ledger; it does not add a
bean, endpoint, reader, capability, worker or `READY` signal. Treat
`cancel_requested_at` as a database-clock marker written once, with no historical
backfill/reclassification. The protected `requestCancel(scope, executionId)` command
is idempotent: an out-of-scope reference does not enumerate, a terminal execution
returns its terminal snapshot without writing, and a repeat preserves the timestamp.
Only a post-commit response admits the marker; timeout or lost acknowledgement requires
scoped readback/reconciliation, never a false accepted cancellation.

Migrate through the same explicit privileged lane and extend `BulkExecutionMigrator`
validation for V10's column, CHECKs/transition triggers, `CANCELLED_BY_USER` reason,
purge mapping, function ownership/search paths and exact ACLs. Preserve V1–V9 checksums.
Runtime access remains only the table/column operations necessary for the protected
command; do not grant broad DML. The migration/bootstrap never heals drift, never runs
DDL from a starter bean, and keeps V5's one-time terminal allocation release and
retention deletion order intact. A user-cancelled `STOPPED` writes a `CANCELLED`
tombstone status on purge; historical `STOPPED` stays `STOPPED`.

The cancel/recovery lifecycle lock order is namespace binding `FOR SHARE`, operation
control `FOR SHARE`, deployment bucket `FOR UPDATE`, subject bucket `FOR UPDATE`,
proposal `FOR UPDATE`, execution `FOR UPDATE`, then receipt/admission. Recheck scope,
binding and epoch under those locks. The helper must permit `SUSPENDED` control so
cancel/recovery can complete; do not reuse a quota helper that requires `READY`, or
add governance locks after locking execution. Java and physical V10 fences both matter:
the marker closes new attempt/admission/callback work, yet a receipt-first ACK already
committed before the marker may advance only that prefix. If it reaches the final ordinal,
normal completion wins; uncertain evidence remains reconciliation-required.

Prove fresh V10 and V9→V10 upgrade/retry/no-heal with real PostgreSQL, including two
connections for cancel before prepare, cancel between prepare/apply, callback commit and
rollback, committed receipt pending ACK (including final ordinal), duplicate/terminal/
cross-scope request, recovery/epoch and `SUSPENDED` races, timeout without false admission,
and a V9 writer against V10. Verify domain effect and no extra callback, not just returned
state. Also prove allocation release once with rollback, retention/purge tombstone mapping,
and migrator rejection of CHECK/trigger/ACL/owner drift. This is Metadata kernel evidence;
HTTP, host adoption and public authorization remain separate gates.

The three protected EXPLICIT/SYNC input modalities are the current store subset; QUERY,
ASYNC, evaluated readiness, quotas, ledger and workers remain separate gates. Test explicit
migration with a nonempty host public schema, repeat/concurrent invocation, unsupported
schema drift, restricted runtime credentials and real PostgreSQL persistence. See
Metadata docs/spec/BULK-PROPOSAL-STORAGE.md. Keep Boot's own Flyway lane configured by its
host; optional dependency changes must not silently enroll bulk DDL in it.

The evaluation-evidence adapter adds V2 without rewriting V1. Verify fresh migration=2,
V1 upgrade=1 and repeat=0; old inputs remain readable without invented evidence.
`insertEvaluated` and `findEvaluation` require SELECT/INSERT on both proposal and evaluation
tables. Physical validation must cover the immediate composite FK, parent unique key and
both immutable triggers. Migrate before enabling the new SDK consumer; adding this evidence
still registers no READY/public capability. Prove BulkEvaluationStorePostgresTest and see
Metadata docs/spec/BULK-EVALUATION-EVIDENCE.md.

## Adopt Durable Bulk Execution Explicitly

The V3 migrator adds reservation, mutable execution control and append-only per-item
receipts; V5 adds quota allocations and retention, and V6 splits operation-control
locking from its governed transition. These migrations register no bean, registry,
capability, readiness signal, endpoint, queue or worker. Construction of
`JdbcBulkDurableExecution` is explicit and uses
the operational datasource/manager already validated by
`BulkExecutionInfrastructure`. Host domain writes and receipt must share that physical
transaction. Adoption is not complete until the host has tested its concrete callback
with an independent PostgreSQL observer and proves that transaction propagation, grants,
recovery and current domain authorization match the promised workflow. Metadata cannot
introspect and forbid arbitrary host code from opening a second transaction or datasource.

Runtime table/function grants depend on the adopted store path and are checked by
`BulkExecutionMigrator` against explicitly supplied role names. In V6, runtime calls
`lock_operation_control` but has no direct SELECT or UPDATE on the operation-control
table; its shared lock remains held until the operational transaction ends. The separately
configured `controlPlaneGranteeRoles` receive EXECUTE on the CAS transition only, not
table DML or membership in `praxis_bulk_control_owner`. The dedicated owner is NOLOGIN,
NOINHERIT, has no members, and has only the columns needed by the lock/CAS and admission
triggers. Never reuse migration, runtime, retention-executor, and control-plane identities
implicitly. The migration validates the physical schema, immediate validated constraints,
immutability guards, function bodies/owners/search_paths and exact ACLs, not only Flyway
checksums. V5 is already part of the migration line: keep its checksum immutable; V6 is
the additive privilege correction and proves a V5→V6 upgrade preserves that checksum.
Reject configured roles that inherit undeclared PostgreSQL roles, including predefined
privileged roles such as `pg_write_all_data`; permit only the explicitly configured
retention membership closure.
Catalog validation must be stable when the
operational datasource sets `currentSchema=praxis_bulk` and must restore that same connection's
search path. Reject unowned types, overloads, aggregates, expression/standalone indexes, rules
and policies. The sole unowned index exception is Flyway's nonunique one-column btree on
`praxis_bulk_schema_history.success`; validate its owner and shape, not just its name. V1–V6
remain immutable; V7 adds the proposal/execution descriptor fence. Verify migration counts:
fresh install=7, V1 upgrade=6, V2 upgrade=5, V3 upgrade=4, V5 upgrade=2, V6 upgrade=1,
and repeat=0 for the V7 baseline. With V8, fresh install=8, V1 upgrade=7,
V2 upgrade=6, V3 upgrade=5, V5 upgrade=3, V6 upgrade=2, V7 upgrade=1,
and repeat=0. Prove V7 backfill, lossless NUL/long identities and versions,
10,000-target boundary, old-writer rollback including allocation/quota,
restricted owner upgrade, failed-bootstrap retry, no ACL healing after COMPLETE,
and purge/expiry under restricted roles in PostgreSQL.
Upgrades never synthesize execution/receipt rows. CAS setting READY is not a composition
proof; the descriptor, provider set and local/durable generation+fingerprint checks must
be complete before the host publishes readiness or advertises any action. See Metadata
`docs/spec/BULK-DURABLE-EXECUTION.md` and prove `BulkDurableMigrationPostgresTest` plus
the upgraded `BulkEvaluationStorePostgresTest` and `JdbcBulkProposalStorePostgresTest`.

A replay reads and validates its receipt before gates that only govern a new mutation.
Recovery is explicit and never invokes domain callbacks; it fences old owner/epoch controls
through durable row locking. Commit-uncertain work blocks subsequent units until readback
or recovery. Do not configure readiness or advertise runtime behavior from starter
construction or migration success.

## Prove Bootstrap And Consumers

Prove default context startup, intended host override, absent-required capability,
and duplicate/ambiguous provider behavior. Assert bean identity/ordering rather
than only context success. For public effects, add focused schema/HTTP proof plus
quickstart and Angular consumer checks where relevant. Do not add aliases or
fallback beans merely to conceal a failed contract.

Use auto-configuration and bootstrap tests first; run focused resource/schema/
option/discovery tests for affected behavior. State when no public artifact changes.

## Companion Skills

- `praxis-java-host-project`: host dependency, scan, and composition proof.
- `praxis-java-option-source-provider-authoring`: provider SPI and execution rules.
- `praxis-metadata-schema-contracts`: public metadata/schema impact.
- `praxis-java-contract-conformance`: downstream evidence pack.

Close with bean graph, property/override contract, ordering proof, host bootstrap
evidence, consumer impact, and remaining gap. A starter is ready when a host can
adopt it without guessing which bean or property owns the behavior.
