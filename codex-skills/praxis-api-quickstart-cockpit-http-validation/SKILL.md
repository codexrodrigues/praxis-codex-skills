---
name: praxis-api-quickstart-cockpit-http-validation
description: Use when Codex must validate or document praxis-api-quickstart real HTTP evidence: Praxis Cockpit, docs/COCKPIT-QUICKSTART-REFERENCE.md, verify-cockpit-* scripts, domain catalog ingest/verify scripts, HTTP examples, Render/public host proof, /actuator/info build evidence, schemas/actions/surfaces/related resources/stats/option-source verification, and quickstart validation routing.
---

# Praxis API Quickstart Cockpit HTTP Validation

Use this skill when the task is about proving quickstart behavior through real HTTP, cockpit inventory, verification scripts, public docs, or published host evidence.

## Source Audit

Inspect the owner before editing:

- `praxis-api-quickstart/AGENTS.md`
- `README.md`
- `docs/COCKPIT-QUICKSTART-REFERENCE.md`
- `docs/AI-HOST-BUSINESS-GROUNDING-GUIDE.md`
- `docs/LLM-DOMAIN-AUTHORING-GUIDE.md`
- `https/*.http`
- `scripts/verify-cockpit-*.sh`
- `scripts/ensure-domain-catalog-context.sh`
- `scripts/verify-domain-catalog-context.sh`
- `scripts/verify-domain-catalog-authoring-runtime.sh`
- `scripts/verify-domain-rules-*.sh`
- `scripts/verify-domain-knowledge-change-set-runtime.sh`
- `src/test/java/com/example/praxis/apiquickstart/config/PraxisCockpitStarterConsumptionIntegrationTest.java`
- `src/test/java/com/example/praxis/apiquickstart/config/ActuatorInfoBuildContractIntegrationTest.java`

## Canonical Boundary

The cockpit and scripts are evidence surfaces. They verify what the host publishes by HTTP: schemas, actions, surfaces, related resources, stats, option sources, structural UI contracts, domain catalog context, domain rules, domain knowledge, and build identity.

They do not redefine metadata/config contracts. When verification fails, determine whether the root cause is the quickstart host, metadata starter, config starter, docs drift, or a published environment mismatch.

## Decision Rules

- Prefer local focused scripts/tests before GitHub Actions or published-host checks.
- Use `/actuator/info` build time and requested release/cache-buster only as evidence of which build is being served.
- Keep cockpit numbers, docs, and verification scripts synchronized with runtime output.
- Do not update docs to match a broken runtime; fix the canonical owner or declare the divergence.
- HTTP examples should demonstrate canonical paths, headers, origins, ETag/schema hashes, and config/security requirements.
- Treat Render/public host smoke as published evidence, not exploratory development loop.

## No Keyword Routing

Do not decide validation target, resource, surface, action, option source, or domain decision by labels, aliases, regexes, or local fuzzy matching as the primary decision. Use published HTTP contracts, resource keys, schema URLs, cockpit inventory, verification script assertions, and starter-owned metadata/config evidence.

## Aderence Inventory

Before changing docs, scripts, HTTP examples, cockpit inventory, assertions, or public-host guidance, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real host-proof gaps justify new quickstart validation assets. If the starter contract is wrong, update the starter and keep the validation as proof.

## Validation

Use the narrowest proof:

- cockpit inventory/docs: `scripts/verify-cockpit-inventory-doc.sh`
- actions/surfaces/related resources/stats/options/structural UI: corresponding `scripts/verify-cockpit-*.sh`
- domain catalog/rules/knowledge: corresponding `scripts/verify-domain-*.sh`
- Java proof: `mvn "-Dtest=PraxisCockpitStarterConsumptionIntegrationTest,ActuatorInfoBuildContractIntegrationTest" test`

For changes requiring a running host, use official documented local scripts/origins. Do not invent alternate ports.

## Companion Skills

- Use `praxis-api-quickstart-operational-proof` to route root cause to quickstart, metadata starter, or config starter.
- Use `praxis-api-quickstart-domain-pilots` when evidence fails because a pilot resource path/domain changed.
- Use `praxis-http-examples-corpus-manifest`, `praxis-http-examples-contract-surfaces`, and `praxis-http-examples-llm-smoke` for the external HTTP corpus, manifest flags, LLM surface, and smoke validation.
- Use `praxis-landing-public-docs-contracts` when public landing/docs narrative cites quickstart evidence.
- Use `praxis-landing-registries-sitemap-playgrounds` when landing guide registries, sitemap, LLM files, examples, or playgrounds mirror quickstart evidence.
- Use `praxis-angular-docs-playgrounds` when Angular component docs/playgrounds mirror this evidence.
