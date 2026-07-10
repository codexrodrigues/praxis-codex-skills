---
name: praxis-landing-public-docs-contracts
description: Use when Codex must update or audit praxis-ui-landing-page public docs as the official projection of Praxis canonical contracts: platform narrative, landing pages, published guides, metadata starter, config starter, Angular runtime, quickstart evidence, HTTP examples, LLM docs, generated docs, and derived artifact decisions.
---

# Praxis Landing Public Docs Contracts

Use this skill when public Praxis documentation or landing copy must explain the platform contract across backend metadata, governed config/AI authoring, Angular runtime, quickstart proof, and HTTP examples.

The landing is a publication layer. It explains, routes, and proves canonical contracts; it does not redefine them.

## Source Audit

Inspect the landing/public docs owner before editing:

- `praxis-ui-landing-page/AGENTS.md`
- `praxis-ui-landing-page/package.json`
- `praxis-ui-landing-page/docs/landing-editorial-axis.md`
- `praxis-ui-landing-page/docs/enterprise-positioning-plan-2026-04.md`
- `praxis-ui-landing-page/docs/landing-editorial-rollout-plan-2026-05.md`
- `praxis-ui-landing-page/src/app/app.routes.ts`
- `praxis-ui-landing-page/src/app/data/site.data.ts`
- `praxis-ui-landing-page/src/app/data/guides/landing-docs.registry.ts`
- `praxis-ui-landing-page/src/app/data/guides/component-docs.registry.ts`
- published guide markdown under `praxis-ui-landing-page/src/app/data/guides/**`
- `praxis-ui-landing-page/public/llms.txt`, `llms-full.txt`, `llm-index.json`, and `sitemap.xml` when LLM/search/public routing changes

Then inspect the canonical owner for every claim:

- `praxis-metadata-starter` for `resource + surfaces + actions + capabilities`, `/schemas/filtered`, `x-ui`, HATEOAS, option sources, schema hashes, and semantic grounding.
- `praxis-config-starter` for `/api/praxis/config/**`, `ui_user_config`, AI registry/config, agentic authoring, domain decisions, headers, and ETag.
- `praxis-ui-angular` for `@praxisui/*` runtime contracts, component docs, manifests, AI registry projections, examples, recipes, playground behavior, and public API.
- `praxis-api-quickstart` for reference-host proof by real HTTP.
- `praxisui-http-examples` for executable examples, corpus manifests, safe-first LLM surfaces, and smoke evidence.

## Canonical Boundary

Public docs should describe Praxis as a platform of AI-authored semantic decisions:

`backend metadata grounding -> governed config/AI authoring -> Angular materialization -> quickstart/HTTP proof -> public docs projection`

Do not turn landing copy, guide frontmatter, route registries, LLM text files, screenshots, playground labels, or examples into primary business semantics. If a public page needs a fact that the canonical owner cannot prove, classify it as a gap in the owner, not as copy freedom.

## No Keyword Routing

Do not decide which platform pillar, resource, guide, route, capability, or AI flow a page describes by keywords, slugs, regexes, aliases, or fuzzy title matching as the primary mechanism. Use canonical owner, registry metadata, route declarations, manifests, published guide frontmatter, executable examples, HTTP proof, and semantic contracts. Text matching may only find candidate files after the canonical scope is known.

## Aderence Inventory

Before adding or changing a public narrative, guide, route, registry entry, LLM page, example, or diagram, classify the need:

- `ja-suportado-so-ux`: the canonical owner already exposes the meaning and only the page presentation must improve.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the owner has the semantics but the public docs or runtime materialization misnames, hides, or weakly frames it.
- `suportado-parcialmente`: some evidence exists, but claims must be narrowed or split between confirmed capability and roadmap.
- `lacuna-real-de-contrato`: the public behavior cannot be stated truthfully because the canonical owner lacks data, contract, endpoint, manifest, tool, event, or proof.

Only `lacuna-real-de-contrato` justifies a new canonical contract. In that case name the missing UX/behavior, canonical owner, affected consumers, derived artifacts, and minimum validation before changing public docs.

## Decision Rules

- Start from `praxis-ui-landing-page/AGENTS.md` and the relevant canonical owner; never start by inventing landing-local semantics.
- Publish `praxis-metadata-starter` as semantic grounding and structural schema source, not as a JSON generator.
- Publish `praxis-config-starter` as governed authoring, simulation, approval, publication, persistence, and materialization boundary, not just preference storage.
- Publish `praxis-ui-angular` as cockpit/runtime for materialized decisions, not as primary business-rule source.
- Use `praxis-api-quickstart` and `praxisui-http-examples` as operational proof surfaces, not contract owners.
- Distinguish shipped, proven, public, beta, and roadmap claims. Do not upgrade aspirational direction into current capability.
- When public docs disagree with code, backend contracts, or HTTP proof, fix the canonical owner or document drift; do not normalize the landing as truth.
- If a new public route or guide is created, update registries, sitemap, LLM surfaces, related docs, and validation scope together.
- If no derived artifact changes, record the negative evidence: no route, guide, sitemap, LLM surface, registry, example, playground, public API, or canonical contract claim changed.

## Impact Map

For non-trivial landing/docs changes, map before editing:

- canonical subproject affected
- impacted consumers such as Angular docs, quickstart docs, HTTP corpus, LLM surfaces, examples, playgrounds, or public site visitors
- public docs and generated docs potentially affected
- examples, playgrounds, recipes, or screenshots potentially affected
- minimum validation
- breaking-change or public-claim risk

## Validation

Use the narrowest landing gate that matches the changed surface:

- published guide or route: `npm run validate:published-guides` and `npm run validate:sitemap`
- sitemap drift: `npm run sitemap:sync`, then `npm run validate:sitemap`
- component docs publication: `npm run docs:validate` and, when needed, `npm run docs:coverage`
- vendor/generated docs: `npm run validate:vendor-docs`
- dynamic page examples: `npm run validate:dynamic-page-examples`
- table manifests/examples in `site.data.ts`: `npm run validate:table-manifests`
- quickstart domain catalog projection: `npm run validate:quickstart-domain-catalog`
- broad publication surface: `npm run check:integration`

For browser proof against the public quickstart, use the official landing origins from `AGENTS.md`, especially `127.0.0.1:4301`/`localhost:4301`. Do not invent ports.

## Companion Skills

- Use `praxis-landing-registries-sitemap-playgrounds` for guide registries, sitemap, LLM files, playgrounds, examples, and validation tooling.
- Use `praxis-angular-docs-playgrounds` for Angular component docs, manifests, examples, AI recipes, and playground behavior.
- Use `praxis-metadata-schema-contracts`, `praxis-metadata-discovery-capabilities`, and `praxis-metadata-domain-option-sources` for metadata claims.
- Use `praxis-config-runtime-persistence`, `praxis-config-ai-registry-manifests`, `praxis-config-agentic-authoring-streaming`, and `praxis-config-domain-decisions` for config/AI/governance claims.
- Use `praxis-api-quickstart-cockpit-http-validation` for reference-host proof.
- Use `praxis-http-examples-corpus-manifest`, `praxis-http-examples-contract-surfaces`, and `praxis-http-examples-llm-smoke` for executable HTTP examples and LLM surfaces.

## Output Expectations

Report:

- canonical owner consulted
- adherence classification
- public docs/routes/registries/LLM surfaces changed or reviewed
- validation commands run
- derived artifacts updated or intentionally left unchanged, with reason
- unresolved drift between public docs and canonical owner
