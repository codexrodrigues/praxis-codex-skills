---
name: praxis-core-providers-bootstrap
description: Use when Codex must implement, audit, document, or consume shared `@praxisui/core` providers, tokens, bootstrap utilities, global config, API URL, fetch headers, loading providers, icon providers, field selector registry providers, collection export providers, enterprise runtime context, public API exports, or cross-lib provider wiring for Praxis Angular packages and hosts.
---

# Praxis Core Providers Bootstrap

Use this skill for shared `@praxisui/core` provider and token wiring. Treat core providers as platform infrastructure, not as convenience snippets to duplicate inside vertical libraries or host apps.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/README.md`
- `projects/praxis-core/src/public-api.ts`
- `projects/praxis-core/src/lib/tokens/**`
- `projects/praxis-core/src/lib/providers/**`
- `projects/praxis-core/src/lib/services/global-config.service.ts`
- `projects/praxis-core/src/lib/services/component-metadata-registry.service.ts`
- `projects/praxis-core/src/lib/services/field-selector-registry.service.ts`
- `projects/praxis-core/src/lib/services/loading-orchestrator.service.ts`
- focused provider/token/service specs and direct consumer imports

## Canonical Boundary

`@praxisui/core` owns shared Angular tokens, provider factories, registries, bootstrap services, global config, API URL contracts, loading renderer/orchestrator contracts, collection export providers, icon providers, field selector registry defaults, component metadata registry, and enterprise runtime context.

Vertical packages may register their package metadata or package defaults through core providers, but they should not redefine core token shapes or expose transitively owned core contracts as local public APIs.

## Provider Rules

- Use exported core provider factories and tokens instead of host-local injection tokens.
- Keep provider defaults centralized in core when multiple `@praxisui/*` packages consume the behavior.
- Avoid root `public-api` reexports from a vertical lib when the contract owner is core; import from `@praxisui/core` directly unless an intentional stable facade is reviewed.
- Keep multi providers multi when the token is additive, such as i18n config, action catalogs, or registry entries.
- Preserve bootstrap order when global config, API URL, headers, loading, logging, i18n, and metadata registry providers interact.
- Before adding a new token or provider, classify the gap as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`.
- For real public contract gaps, map direct consumers and derived docs before editing.

## Validation

Use the smallest reliable proof:

- focused provider/token specs such as icon, loading, collection export, global config, or registry specs
- `npm run build:praxis-core` when exports or provider contracts change
- direct consumer build for at least one package that imports the provider/token
- `praxis-angular-public-api-governance` checks when `src/public-api.ts` changes
- `praxis-angular-validation-gates` for scoped command selection

Report direct consumers, skipped consumers, and whether public API artifacts/docs were reviewed.

## Companion Skills

- Use `praxis-core-runtime-contracts` for shared core models, public exports, i18n, logging, and services.
- Use `praxis-core-resource-runtime` for `GenericCrudService`, resource discovery, schema metadata, actions, surfaces, and capabilities.
- Use `praxis-core-widget-observations` for dynamic widget providers and runtime observation registry.
- Use `praxis-angular-public-api-governance` and `praxis-angular-validation-gates` whenever provider changes affect public API or cross-lib validation.
