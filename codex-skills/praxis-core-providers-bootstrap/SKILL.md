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
- `projects/praxis-core/src/lib/tokens/api-url.token.ts`
- `projects/praxis-core/src/lib/tokens/global-config.providers.ts`
- `projects/praxis-core/src/lib/tokens/global-config.token.ts`
- `projects/praxis-core/src/lib/tokens/enterprise-runtime-context.token.ts`
- `projects/praxis-core/src/lib/tokens/collection-export.token.ts`
- `projects/praxis-core/src/lib/tokens/field-selector-registry.token.ts`
- `projects/praxis-core/src/lib/tokens/loading-renderer.token.ts`
- `projects/praxis-core/src/lib/tokens/loading-context.token.ts`
- `projects/praxis-core/src/lib/services/global-config.service.ts`
- `projects/praxis-core/src/lib/services/config-storage.service.ts`
- `projects/praxis-core/src/lib/services/component-metadata-registry.service.ts`
- `projects/praxis-core/src/lib/services/field-selector-registry.service.ts`
- `projects/praxis-core/src/lib/services/loading-orchestrator.service.ts`
- `projects/praxis-core/src/lib/services/collection-export.service.ts`
- `projects/praxis-core/src/lib/services/enterprise-runtime-context.service.ts`
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
- Treat provider installation as the canonical proof that a host opted into a platform capability. Importing a component class, referencing a selector, or seeing a package in `package.json` does not prove that `ENVIRONMENT_INITIALIZER`, `APP_INITIALIZER`, registry providers, interceptors, i18n catalogs, or default tokens ran.
- Vertical metadata providers such as `providePraxis*Metadata()` install component registry facts; aggregate package providers such as `providePraxisDynamicFields()` may also install i18n, field selector registry defaults, logger bridges, styles, preloading, or HTTP defaults. Keep these capability bundles explicit and documented instead of recreating partial host-local provider arrays.
- If a capability is absent at runtime, fail closed to a missing-provider diagnostic and identify the canonical provider to install. Do not synthesize registry entries, local tokens, prompt-only catalogs, selector switches, or ad hoc fallback defaults to hide an uninstalled provider.
- Before adding a new token or provider, classify the gap as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`.
- For real public contract gaps, map direct consumers and derived docs before editing.

## Lazy host catalog and injector custody

Before moving providers to a lazy route, map each provider's owner, lifetime,
initializer, dictionaries and consumers. A metadata factory may import concrete
runtime components; a package aggregate can also install its engine, inline
renderers and i18n. A lazy editor loader alone does not guarantee a separate
physical chunk when root barrels or other eager consumers retain that graph.
Measure the normal production build; preserve budgets and intentional public
exports. Initial-chunk reduction does not prove lower total first-navigation cost.

Use one persistent route scope for a composition that needs the complete widget
catalog. Keep application-owned auth, HTTP, global config, registries, stateful
panel services and root-consumed authoring options in their original lifetime.
A child metadata initializer can register with the root registry, but dictionaries
installed only in the child are not automatically visible to a registry that
captured root i18n. Compare resolved descriptor text and locale before/after;
retain the canonical dictionary provider in root when required, rather than
copying private constants or creating another registry.

Use existing Settings Panel/Drawer bridges and their content-parent injector
contract. A bridge installed in the route may capture that injector while opening
through the same root panel service. Audit the actual injected interface before
patching an owner: a bridge call already carrying its injector needs no redundant
component change. Prove service identity, child engine/token visibility in a real
preview, editor Apply/Save/reopen/Cancel and overlay lifecycle. Never re-provide a
stateful root service merely to make child tokens visible to it.

## Validation

Use the smallest reliable proof:

- global config, config storage, and global config provider defaults:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/global-config.service.spec.ts --include=projects/praxis-core/src/lib/services/config-storage.service.spec.ts --include=projects/praxis-core/src/lib/tokens/global-config.providers.spec.ts
```

- loading providers/orchestrator/renderer and visual tokens:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/providers/loading.providers.spec.ts --include=projects/praxis-core/src/lib/services/default-loading-renderer.service.spec.ts --include=projects/praxis-core/src/lib/tokens/layer-scale.token.spec.ts --include=projects/praxis-core/src/lib/tokens/theme-surface.token.spec.ts
```

- icon providers, field selector registry, collection export, enterprise runtime context, and component metadata registry:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/providers/icon.providers.spec.ts --include=projects/praxis-core/src/lib/components/icon-picker/icon-picker.component.spec.ts --include=projects/praxis-core/src/lib/services/field-selector-registry.service.spec.ts --include=projects/praxis-core/src/lib/services/collection-export.service.spec.ts --include=projects/praxis-core/src/lib/services/http-collection-export.provider.spec.ts --include=projects/praxis-core/src/lib/models/collection-export.model.spec.ts --include=projects/praxis-core/src/lib/services/enterprise-runtime-context.service.spec.ts --include=projects/praxis-core/src/lib/services/component-metadata-registry.service.spec.ts
```

- `API_URL` or fetch/header contract changes require at least one direct consumer proof selected by actual imports, commonly:

```sh
npm run ng -- test praxis-charts --watch=false --progress=false --include=projects/praxis-charts/src/lib/services/chart-stats-api.service.spec.ts
npm run test:form -- --include=projects/praxis-dynamic-form/src/lib/praxis-dynamic-form.external-config-hydration.spec.ts
npm run ng -- test praxis-ai --watch=false --progress=false --include=projects/praxis-ai/src/lib/core/services/ai-backend-api.service.spec.ts
```

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
