---
name: praxis-api-quickstart-security-config
description: Use when Codex must work on praxis-api-quickstart security and exposure policy: SecurityConfig, ConfigOriginRestrictionFilter, CORS, CSRF, read-open, write-disabled, rate limits, /api/praxis/config/** permitAll plus origin governance, /schemas/** exposure, /api/praxis/runtime/**, Swagger/actuator policy, cookies, JWT filters, and security-focused integration tests.
---

# Praxis API Quickstart Security Config

Use this skill for host security/exposure policy in `praxis-api-quickstart`. Security is the quickstart's responsibility when it governs how starter endpoints are exposed by the host.

## Source Audit

Inspect the owner before editing:

- `praxis-api-quickstart/AGENTS.md`
- `src/main/java/com/example/praxis/apiquickstart/config/SecurityConfig.java`
- `src/main/java/com/example/praxis/apiquickstart/security/ConfigOriginRestrictionFilter.java`
- `src/main/java/com/example/praxis/apiquickstart/security/PublicApiRateLimitFilter.java`
- `src/main/java/com/example/praxis/apiquickstart/security/CookieJwtAuthenticationFilter.java`
- `src/main/java/com/example/praxis/apiquickstart/security/SpaCsrfTokenRequestHandler.java`
- `src/main/resources/application*.properties`
- `docs/security-overview.md`
- `docs/security-read-open.md`
- focused `SecurityConfig*`, CORS, actuator, AI patch policy, and config-origin tests.

## Canonical Boundary

`SecurityConfig` decides host exposure policy: public docs, schemas, cockpit, actuator health/info, read-open APIs, config endpoints, runtime endpoints, write-disabled behavior, and filter ordering.

`ConfigOriginRestrictionFilter` is host governance over `/api/praxis/config/**`. `permitAll` in Spring Security does not mean ungated operational use; the host may require allowed `Origin`/`Referer`/forwarded origin.

## Decision Rules

- If `/api/praxis/config/**` is permitted but returns 403, check origin restriction before blaming `praxis-config-starter`.
- Do not solve CORS/CSRF/origin problems by changing config-starter endpoint semantics.
- Do not expose `/actuator/env` publicly, even when read-open is enabled.
- Keep `/schemas/**` exposure aligned with metadata proof needs and `schemasAggregatorEnabled`.
- Preserve official local origins and documented host properties; do not invent ad hoc ports/origins.
- Treat `write-disabled` and read-open exceptions as public demo policy, not general platform contract.

## No Keyword Routing

Do not decide access, route class, origin allowance, write policy, or schema/config exposure by route labels, aliases, or regex fragments outside the declared security matchers and host properties. Use explicit path patterns, HTTP methods, headers, origin normalization, and policy tests.

## Aderence Inventory

Before adding matchers, filters, properties, origins, endpoint exceptions, or security docs, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only host exposure gaps justify quickstart security changes. Starter contract gaps belong to metadata/config starters.

## Validation

Use focused local gates:

- host policy: `mvn "-Dtest=SecurityConfigActuatorPolicyTest,SecurityConfigAiPatchPolicyTest,SecurityConfigReadOpenStatsPolicyTest,SecurityConfigSpaCsrfPolicyTest,SecurityConfigCorsTest" test`
- config exposure with schema/AI: `mvn "-Dtest=AiPatchSchemaResolutionIsolatedIntegrationTest,AgenticAuthoringStreamIsolatedIntegrationTest" test`

Review `docs/security-overview.md`, `docs/security-read-open.md`, README exposure notes, and quickstart HTTP examples when public security behavior changes.

## Companion Skills

- Use `praxis-api-quickstart-operational-proof` for dependency/version and starter ownership routing.
- Use `praxis-config-runtime-persistence` and `praxis-config-agentic-authoring-streaming` when endpoint behavior belongs to config-starter.
- Use `praxis-metadata-schema-contracts` when `/schemas/**` behavior belongs to metadata-starter.
