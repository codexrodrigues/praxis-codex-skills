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
local JDBC/JPA transaction manager and stable namespace. It is not registered automatically
and does not run DDL or workers. Do not infer its collaborators by Primary, bean name or URL.
JPA requires the same datasource exposed by EntityManagerFactoryInfo and its manager;
initialize both first. Opaque managers, routing and datasource wrappers are outside the
initial demonstrated subset. Do not add a fallback connection when composition fails.

Its withConnection callback requires a real existing writable transaction (MANDATORY),
with JdbcTemplate's connection bound to the configured datasource. It does not implement
registry/readiness, migrations or storage. A later runtime must compose and validate these
actual dependencies before advertising an executable operation; OpenApiDocumentWarmup is
optional/asynchronous and tolerates errors, so it is not an admission gate.

Validate BulkExecutionInfrastructureTest and the real-process
BulkExecutionInfrastructurePostgresTest before a host adoption. The latter proves JPA/JDBC
commit/rollback and lock contention on fixture tables, not production ledger migration.
No AutoConfiguration.imports change is needed merely to add this explicit value/participant.

## Adopt The Protected Proposal Migration Lane

`BulkExecutionMigrator.migrate(dataSource)` is explicit and separate from host Flyway
startup. Metadata supplies optional Flyway core/PostgreSQL dependencies (11.17.0 in the
reference candidate); consumers choosing this adapter must supply these dependencies.
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
`praxis_bulk_schema_history.success`; validate its owner and shape, not just its name. V1–V5
remain immutable; fresh migration applies six versions, V1 upgrade applies five, V2 upgrade
applies four, V3 upgrade applies three, V5 upgrade applies one, and repeat applies zero.
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
