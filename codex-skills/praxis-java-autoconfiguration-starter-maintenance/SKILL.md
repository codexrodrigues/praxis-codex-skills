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
credentials need schema USAGE and table SELECT/INSERT, not CREATE/UPDATE/DELETE. Migration
credentials are not inferred or manufactured by the starter. History checksum validation
alone is insufficient: validate physical constraints and the enabled immutability trigger.
No bean, readiness capability or executor is registered automatically by adding the SDK.

The three protected EXPLICIT/SYNC input modalities are the current store subset; QUERY,
ASYNC, evaluated readiness, quotas, ledger and workers remain separate gates. Test explicit
migration with a nonempty host public schema, repeat/concurrent invocation, unsupported
schema drift, restricted runtime credentials and real PostgreSQL persistence. See
Metadata docs/spec/BULK-PROPOSAL-STORAGE.md. Keep Boot's own Flyway lane configured by its
host; optional dependency changes must not silently enroll bulk DDL in it.

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
