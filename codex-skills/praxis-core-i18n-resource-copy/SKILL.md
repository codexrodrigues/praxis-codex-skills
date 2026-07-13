---
name: praxis-core-i18n-resource-copy
description: Use when Codex must implement, audit, document, or consume shared `@praxisui/core` i18n and resource-discovery copy, including `PraxisI18nService`, `providePraxisI18nConfig`, `providePraxisI18nTranslator`, i18n tokens/models/utils, namespace catalogs, resource availability messages, value presentation resolver, PT-BR/en-US coverage, public API, or cross-lib framework chrome translation.
---

# Praxis Core I18n Resource Copy

Use this skill for shared core i18n, translation providers, resource-discovery copy, and value presentation. Treat framework chrome as platform text and domain labels as host/backend metadata.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/src/public-api.ts`
- `projects/praxis-core/src/lib/i18n/i18n.models.ts`
- `projects/praxis-core/src/lib/i18n/i18n.tokens.ts`
- `projects/praxis-core/src/lib/i18n/i18n.providers.ts`
- `projects/praxis-core/src/lib/i18n/i18n.utils.ts`
- `projects/praxis-core/src/lib/i18n/i18n.service.ts`
- `projects/praxis-core/src/lib/i18n/component-metadata-registry.i18n.ts`
- `projects/praxis-core/src/lib/i18n/resource-discovery.i18n.ts`
- `projects/praxis-core/src/lib/i18n/value-presentation.models.ts`
- `projects/praxis-core/src/lib/i18n/value-presentation.resolver.ts`
- `projects/praxis-core/src/lib/actions/surface-open.i18n.ts`
- `projects/praxis-core/src/lib/surfaces/praxis-related-resource-outlet.i18n.ts`
- `projects/praxis-core/src/lib/widgets/dynamic-widget-page.i18n.ts`
- `projects/praxis-core/src/lib/widgets/widget-shell.i18n.ts`
- `projects/praxis-core/src/lib/services/component-metadata-registry.service.ts`
- `tools/i18n/i18n-conformance.manifest.json`
- `tools/i18n/validate-i18n-conformance.js`
- `tools/i18n/reports/catalog-coverage.md`
- `tools/i18n/reports/hardcoded-text-hotspots.md`
- focused i18n, resource discovery, and value presentation specs

## Canonical Boundary

`@praxisui/core` owns shared i18n models, translator token, config multi-provider, config merge semantics, `PraxisI18nService`, fallback behavior, component metadata registry defaults, resource discovery namespace, resource availability reason mapping, unavailable workflow copy, surface/related-resource chrome copy, widget shell copy, and value presentation helpers.

Vertical packages own package-specific namespaces and catalogs. Backend metadata/config owns domain labels, business names, option labels, resource names, and user-authored content.

## I18n Rules

- Use `providePraxisI18nConfig(...)` for namespace catalogs and keep it multi-provider.
- Use `providePraxisI18nTranslator(...)` only for a real external translator bridge.
- Keep at least `pt-BR` and `en-US` coverage for shared core framework text.
- Keep `componentMetadataRegistry`, `resourceDiscovery`, `surfaceOpen`, `relatedResourceOutlet`, `dynamicWidgetPage`, and `widgetShell` namespaces centralized in core when the text is framework chrome.
- Keep `resourceDiscovery` keys stable for workflow unavailable messages, row action menu copy, and availability reasons.
- Normalize resource availability reason codes before translating.
- Do not persist translated text as business data.
- Do not replace backend/domain labels with framework copy. Framework chrome goes through i18n; domain labels remain metadata/config.
- Prefer value presentation resolver paths for display formatting instead of per-component stringification.

## Inventory Before New Contract

Classify requests before adding i18n keys or providers:

- `ja-suportado-so-ux`: key/provider exists but a component does not render it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: hardcoded text or local copy should map to an existing namespace/key.
- `suportado-parcialmente`: core supports i18n but locale coverage, fallback, docs, or consumer adoption is incomplete.
- `lacuna-real-de-contrato`: no namespace, key, translator provider, value presentation contract, or metadata path can carry the text correctly.

For real gaps, update catalogs, specs, public API if needed, and affected consumers together.

## Validation

Use the smallest reliable proof:

- Core service/catalog/value presentation changes:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/i18n/i18n.service.spec.ts --include=projects/praxis-core/src/lib/i18n/resource-discovery.i18n.spec.ts --include=projects/praxis-core/src/lib/i18n/value-presentation.resolver.spec.ts`
- Component metadata registry defaults or fallback names:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/services/component-metadata-registry.service.spec.ts`
- Resource discovery, related-resource, or unavailable workflow copy:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts`
- Workspace-wide i18n conformance or hardcoded framework text cleanup:
  - `node tools/i18n/validate-i18n-conformance.js`
  - `node --test tools/i18n/validate-i18n-conformance.spec.js`
  - Review `tools/i18n/reports/catalog-coverage.md` and `tools/i18n/reports/hardcoded-text-hotspots.md` for the affected packages.
- Direct consumer specs when a package adopts shared copy, for example:
  - `npm run test:core -- --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts`
  - package-specific i18n specs such as `projects/praxis-manual-form/src/lib/i18n/manual-form.i18n.spec.ts`, `projects/praxis-metadata-editor/src/lib/i18n/metadata-editor.i18n.spec.ts`, `projects/praxis-page-builder/src/lib/i18n/page-builder-agentic-i18n.spec.ts`, or `projects/praxis-dynamic-fields/src/lib/editorial/metadata-i18n-contract.spec.ts` when those catalogs change.
- `npm run build:praxis-core` when exports, providers, tokens, or public value-presentation models change.

Report which text is framework chrome versus domain content and which locales were covered.

## Companion Skills

- Use `praxis-angular-i18n-governance` for workspace-wide i18n policy and hardcoded text audits.
- Use `praxis-core-resource-runtime` when resource discovery availability, actions, surfaces, or capabilities drive copy.
- Use `praxis-core-providers-bootstrap` when provider wiring changes.
- Use `praxis-angular-public-api-governance` and `praxis-angular-validation-gates` for exports and validation.
