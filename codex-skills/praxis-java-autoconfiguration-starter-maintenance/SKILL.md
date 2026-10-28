---
name: praxis-java-autoconfiguration-starter-maintenance
description: Use when implementing, auditing, or evolving praxis-metadata-starter Spring Boot auto-configuration: @AutoConfiguration, @ConditionalOnMissingBean, configuration properties, SPI extension points, bean ordering, OptionSourceProvider/registry/executor wiring, AutoConfiguration.imports, starter bootstrap tests, opt-in bulk owner migrations, interrupted bootstrap recovery, packaged migration resources, host compatibility, and public contract impact.
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
Before changing Springdoc wiring, confirm the resolved Boot/Springdoc versions in
both the starter and its consumer, then inspect the builder's public constructor
and context initialization for each generation using that matrix.

## Explicit Bulk Infrastructure, Migrations, And Worker Composition

`BulkExecutionInfrastructure`, `BulkExecutionMigrator`, `JdbcBulkProposalStore`,
`JdbcBulkDurableExecution`, and `BulkDurableWorker` are explicit, opt-in host
integrations; they are never auto-started or auto-migrated by adding the starter JAR:

- Read [bulk-infrastructure-and-migrations.md](references/bulk-infrastructure-and-migrations.md)
  for `BulkExecutionInfrastructure` role/connection attestation, the protected proposal
  and durable execution migration lanes (`classpath:db/praxis-bulk-migrations`, `V1`–`V19`),
  and capacity authority boundaries.
- Read [bulk-owner-migration.md](references/bulk-owner-migration.md) for staged schema
  upgrades, phase-aware attestation, reject-only completed installations, pool/resource
  proof, and packaged-consumer evidence.
- Read [bulk-worker-composition.md](references/bulk-worker-composition.md) when composing
  the durable worker in an external host.

## Prove Bootstrap And Consumers

Before accepting a manually composed host facade, inspect the complete
`@ConditionalOnBean` prerequisites of its canonical auto-configuration. A collaborator
constructed only as a local variable inside another `@Bean` factory is not itself a
Spring bean and does not satisfy that condition. Register required infrastructure as
real beans with the actual datasource, transaction manager and role bindings; retain
the canonical auto-configuration rather than treating manual facade construction as
proof that it ran.

Assert the conditioned bean's presence and identity, then verify initialization
and ordering of any registered filter or serving guard. When HTTP behavior is
claimed, prove the actual Servlet registration and cold denial followed by
publication/restoration through the real HTTP path and canonical security/filter chain.

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
