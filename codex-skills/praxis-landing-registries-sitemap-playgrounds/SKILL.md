---
name: praxis-landing-registries-sitemap-playgrounds
description: Use when Codex must update or audit praxis-ui-landing-page registries, published guide frontmatter, sitemap, llms.txt/llms-full.txt/llm-index.json, dynamic examples, live playgrounds, decision playground, table manifests, vendor docs sync, generated docs, and local validation for public Praxis docs.
---

# Praxis Landing Registries Sitemap Playgrounds

Use this skill for the operational publication layer of `praxis-ui-landing-page`: registries, guides, routes, sitemap, LLM files, examples, playgrounds, generated docs, and validation tooling.

This skill handles how public docs are wired and validated. Use `praxis-landing-public-docs-contracts` for what the docs are allowed to claim.

## Source Audit

Inspect the landing publication surface before editing:

- `praxis-ui-landing-page/AGENTS.md`
- `praxis-ui-landing-page/package.json`
- `src/app/app.routes.ts`
- `src/app/data/site.data.ts`
- `src/app/data/guides/landing-docs.registry.ts`
- `src/app/data/guides/component-docs.registry.ts`
- `src/app/data/guides/**/*.md`
- `src/app/pages/*guide*`, `*examples*`, `*playground*`, and `*detail*`
- `src/app/playground/**`
- `public/examples/**`
- `public/sitemap.xml`
- `public/llms.txt`, `public/llms-full.txt`, and `public/llm-index.json`
- `tools/sync-sitemap.mjs`
- `tools/validate-published-guides.mjs`
- `tools/sync-dynamic-page-examples-catalog.mjs`
- `tools/sync-vendor-docs.mjs`
- `tools/validate-table-manifests.mjs`
- `tools/validate-quickstart-domain-catalog.mjs`
- `tools/docs/validate-docs.mjs`
- `tools/docs/report-component-docs-coverage.mjs`
- relevant E2E files under `e2e/**` when behavior or browser rendering changes

## Canonical Boundary

Registries, sitemap, LLM files, examples, and playground routes are derived publication artifacts. They should project:

- backend contracts from `praxis-metadata-starter`
- config and AI authoring contracts from `praxis-config-starter`
- runtime/component contracts from `praxis-ui-angular`
- reference proof from `praxis-api-quickstart`
- executable HTTP proof from `praxisui-http-examples`

Do not add landing-local catalog fields, fake capabilities, static HTTP facts, or prompt shortcuts when the canonical source already has or lacks the semantics. If an example needs data that does not exist, fix the owner or narrow the example.

## No Keyword Routing

Do not decide guide publication, sitemap inclusion, LLM exposure, playground scenario, or example category by title keywords, route slugs, regexes, aliases, or fuzzy text as the primary rule. Use route declarations, registry metadata, frontmatter, manifests, generated catalog scripts, canonical contracts, and validation output. Text search is only for locating candidate files after the owner and surface are known.

## Aderence Inventory

Before changing registries, routes, sitemap, LLM files, examples, playgrounds, or generated docs, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real gaps in the owning contract justify new canonical fields or route semantics. Most registry or sitemap changes are `ja-suportado-so-ux` or `ja-suportado-mal-nomeado-ou-mal-materializado`: the platform already knows the fact, but the public site is not publishing it well.

## Decision Rules

- Treat `package.json` scripts as the source of operational commands.
- Keep generated or synchronized artifacts generated. Do not hand-edit sitemap/vendor/generated docs when a sync script owns them.
- Preserve guide `slug`, `related_docs`, publication status, internal markdown links, and route validity.
- When adding a published guide, wire registry, route visibility, sitemap, related docs, LLM files, and validation together.
- When changing examples in `site.data.ts`, review table/list/crud/dynamic-page manifests and run the matching manifest gate.
- When changing playground behavior, validate the focused adapter/spec/E2E path and capture browser evidence if visual/product quality changed.
- When public docs mirror quickstart or HTTP examples, verify the referenced evidence still exists; do not cite stale smoke output.
- Exclude `dist/`, `artifacts/`, `output/`, `tmp/`, `.angular/`, and `node_modules/` from source audits unless debugging generated output.

## Validation Matrix

Choose the smallest sufficient gate:

- guide registry/frontmatter/route: `npm run validate:published-guides`
- sitemap: `npm run validate:sitemap`
- expected sitemap regeneration: `npm run sitemap:sync` then `npm run validate:sitemap`
- docs markdown/component docs: `npm run docs:validate`
- docs coverage report: `npm run docs:coverage`
- vendor docs projection: `npm run validate:vendor-docs`
- dynamic-page examples: `npm run validate:dynamic-page-examples`
- table manifests/examples: `npm run validate:table-manifests`
- quickstart domain catalog projection: `npm run validate:quickstart-domain-catalog`
- broad publication/integration change: `npm run check:integration`
- decision playground: `npm run e2e:decision-playground` or `npm run audit:decision-playground:visual` when behavior/visual proof changed
- live quickstart: `npm run e2e:live-quickstart` only when the public host integration itself is in scope

If the landing `node_modules` was installed in a platform-specific environment, run Node/Angular commands in the owner environment. Inspect package binaries before mixing WSL/Linux/Windows installs when applicable.

## Companion Skills

- Use `praxis-landing-public-docs-contracts` before changing platform-level claims.
- Use `praxis-angular-docs-playgrounds` for component docs manifests, Angular examples, AI recipes, and generated registry projections.
- Use `praxis-api-quickstart-cockpit-http-validation` when the page cites quickstart/cockpit evidence.
- Use `praxis-http-examples-llm-smoke` when `llms.txt`, `llms-full.txt`, `llm-index.json`, or safe-first HTTP lanes mirror executable examples.
- Use metadata/config skills when a registry or guide exposes backend contract semantics.

## Output Expectations

Report:

- publication surfaces touched
- canonical evidence checked
- generated artifacts synced or deliberately not changed
- validation commands run
- any route, sitemap, LLM, guide, or playground drift left open
