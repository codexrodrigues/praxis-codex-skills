---
name: praxis-api-quickstart-operational-proof
description: Use when Codex must work on praxis-api-quickstart as the operational reference host proving Praxis contracts in real HTTP: starter dependency versions, pom.xml, Spring Boot bootstrap, /schemas/**, /api/praxis/config/**, /api/praxis/runtime/**, metadata/config integration, Maven resolution, quickstart smoke tests, and deciding whether a fix belongs to quickstart, praxis-metadata-starter, or praxis-config-starter.
---

# Praxis API Quickstart Operational Proof

Use this skill for the role of `praxis-api-quickstart` as the real HTTP proof host for Praxis. The quickstart hosts the starters and proves their integration; it must not redefine canonical metadata or config semantics.

## Source Audit

Inspect the owner before editing:

- `praxis-api-quickstart/AGENTS.md`
- `praxis-api-quickstart/README.md`
- `pom.xml`
- `src/main/java/com/example/praxis/apiquickstart/ApiQuickstartApplication.java`
- `src/main/java/com/example/praxis/apiquickstart/constants/ApiPaths.java`
- `src/main/resources/application*.properties`
- `src/test/java/com/example/praxis/apiquickstart/config/QuickstartMetadataMigrationIntegrationTest.java`
- `src/test/java/com/example/praxis/apiquickstart/config/OpenApiGroupResolutionIsolatedIntegrationTest.java`
- `src/test/java/com/example/praxis/apiquickstart/config/AiPatchSchemaResolutionIsolatedIntegrationTest.java`
- `src/test/java/com/example/praxis/apiquickstart/config/AgenticAuthoringStreamIsolatedIntegrationTest.java`
- `docs/COCKPIT-QUICKSTART-REFERENCE.md`
- `docs/AI-HOST-BUSINESS-GROUNDING-GUIDE.md`

## Canonical Boundary

The quickstart owns host composition: Spring Boot app, dependency versions, security wiring, paths for concrete example resources, pilot domains, and downstream validation.

It does not own canonical `x-ui`, `/schemas/filtered`, actions/surfaces/capabilities, AI registry, config persistence, manifests, validators, streaming, or domain decision semantics. Those belong to `praxis-metadata-starter` or `praxis-config-starter`.

## Decision Rules

- If the behavior is wrong in `/schemas/**`, `x-ui`, `_links`, schema hashes, surfaces, actions, capabilities, or operation/schema resolution, inspect `praxis-metadata-starter` first and use quickstart as downstream proof.
- If the behavior is wrong under `/api/praxis/config/**`, AI registry/context/patch/stream, headers, ETag, domain rules, or domain knowledge, inspect `praxis-config-starter` first and use quickstart as host proof.
- If the behavior is about host policy, dependency versions, app properties, CORS/CSRF/origin, concrete demo resources, `ApiPaths`, or demo data, it may belong to quickstart.
- Do not create local host adapters, endpoint aliases, DTO patches, or starter overrides to compensate for canonical starter gaps.
- Treat `praxis.core.version` and `praxis.config.version` changes as integration changes requiring Maven resolution and focused downstream proof.

## No Keyword Routing

Do not decide resource, workflow, domain, security, AI, or validation intent by labels, route text, aliases, regexes, or local fuzzy matching as the primary decision. Use canonical resource keys, paths, schemas, capabilities, config contracts, tests, and declared tools; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding endpoints, DTOs, dependency overrides, properties, tests, or examples, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only a real quickstart host gap justifies local changes. If the gap is canonical metadata/config, fix the starter and keep quickstart as proof.

## Validation

Use focused local gates:

- metadata downstream proof: `mvn "-Dtest=OpenApiGroupResolutionIsolatedIntegrationTest,QuickstartMetadataMigrationIntegrationTest,EventosFolhaPilotIntegrationTest" test`
- config downstream proof: `mvn "-Dtest=AiPatchSchemaResolutionIsolatedIntegrationTest,SecurityConfigAiPatchPolicyTest" test`
- dependency/version changes: confirm Maven resolution and run `mvn -B verify`
- broad host proof: `mvn test`

For config-starter authoring/SSE changes, prefer the quickstart HTTP/SSE smoke described in `praxis-config-starter/RELEASING.md`.

## Companion Skills

- Use `praxis-api-quickstart-security-config` for CORS, CSRF, origin, read-open, rate-limit, and config exposure policy.
- Use `praxis-api-quickstart-domain-pilots` for concrete domains, `ApiPaths`, controllers, DTOs, filters, mappers, services, and pilot resources.
- Use `praxis-api-quickstart-cockpit-http-validation` for cockpit docs, verification scripts, HTTP examples, and published host evidence.
- Use `praxis-http-examples-contract-surfaces` and `praxis-http-examples-llm-smoke` when the proof is maintained in the external executable HTTP corpus.
- Use `praxis-metadata-*` skills when the quickstart proves a metadata-starter issue.
- Use `praxis-config-*` skills when the quickstart proves a config-starter issue.
