---
name: praxis-api-quickstart-domain-pilots
description: Use when Codex must work on praxis-api-quickstart concrete pilot domains: ApiPaths, @ApiResource controllers, DTOs, filters, @Schema business descriptions, @UISchema endpoints, @DomainGovernance, option sources, entity lookup pilots, stats, export, actions, services, mappers, operational migrations, hero-demo domains, HR, operations, assets, procurement, risk intelligence, and pilot integration tests.
---

# Praxis API Quickstart Domain Pilots

Use this skill for concrete quickstart resources and pilot domains. These domains are didactic operational proof of Praxis patterns, not sources of canonical starter semantics.

## Source Audit

Inspect the owner before editing:

- `praxis-api-quickstart/AGENTS.md`
- `src/main/java/com/example/praxis/apiquickstart/constants/ApiPaths.java`
- `src/main/java/com/example/praxis/apiquickstart/hr/**`
- `src/main/java/com/example/praxis/apiquickstart/operations/**`
- `src/main/java/com/example/praxis/apiquickstart/operationalassets/**`
- `src/main/java/com/example/praxis/apiquickstart/procurement/**`
- `src/main/java/com/example/praxis/apiquickstart/riskintelligence/**`
- `db/operational-migrations/**`
- `docs/DEMO-DATABASE.md`
- `docs/SEMANTIC-DOMAIN-CATALOG-CONTRACT.md`
- focused pilot integration tests for the affected domain.

## Canonical Boundary

`ApiPaths` is a contract synchronization point. It feeds real resource URLs, `@ApiResource`, OpenAPI, `/schemas/filtered`, `x-ui.endpoint`, lookup endpoints, cockpit docs, and Angular runtime discovery.

Pilot domains should demonstrate resource-oriented controllers/services, DTO business descriptions, filters, options, entity lookup, stats, export, workflow actions, surfaces, domain governance, and domain-rule materializations.

## Decision Rules

- Do not spread path literals when an `ApiPaths` constant exists.
- Do not change `ApiPaths` without reviewing controllers, DTOs, filters, option-source endpoints, OpenAPI groups, tests, docs, and cockpit verification scripts.
- Treat `@Schema(description=...)` as business meaning, not UI labels or technical field restatements.
- Use `@UISchema` for UI behavior and `@DomainGovernance`/domain catalog for governance meaning.
- Model business workflows as actions/workflows, not opportunistic CRUD/PATCH shortcuts.
- If a pilot exposes a starter bug, fix the starter and keep the pilot as proof.

## No Keyword Routing

Do not infer resources, fields, filters, option sources, actions, or workflow intent from labels, aliases, regexes, or local fuzzy matching as the primary decision. Use `ApiPaths`, `@ApiResource(resourceKey=...)`, DTO/schema metadata, option-source keys, actions, capabilities, and domain catalog grounding; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding or changing paths, resources, DTO fields, filters, option sources, stats, actions, migrations, or examples, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only local host/domain gaps justify quickstart pilot changes. Canonical metadata/config gaps belong to the starters.

## Validation

Use focused local gates:

- metadata pilot proof: `mvn "-Dtest=QuickstartMetadataMigrationIntegrationTest,EventosFolhaPilotIntegrationTest,OpenApiGroupResolutionIsolatedIntegrationTest" test`
- domain-specific pilots: run the affected `*PilotIntegrationTest`, entity lookup test, stats smoke, or export smoke.
- `ApiPaths` or broad resource identity changes: add cockpit verification scripts and `mvn test` when focal proof is insufficient.

Review README, `docs/DEMO-DATABASE.md`, `docs/COCKPIT-QUICKSTART-REFERENCE.md`, HTTP examples, and public docs when a pilot changes public behavior.

## Companion Skills

- Use `praxis-api-quickstart-operational-proof` for host/starter ownership and dependency validation.
- Use `praxis-api-quickstart-cockpit-http-validation` for cockpit and script proof.
- Use `praxis-metadata-resource-baseline`, `praxis-metadata-schema-contracts`, `praxis-metadata-discovery-capabilities`, and `praxis-metadata-domain-option-sources` when the pilot exercises metadata starter contracts.
- Use `praxis-config-domain-decisions` when pilots consume governed domain-rule/domain-knowledge materializations.
