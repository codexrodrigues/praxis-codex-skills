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
- `projects/praxis-core/src/lib/i18n/i18n.service.ts`
- `projects/praxis-core/src/lib/i18n/resource-discovery.i18n.ts`
- `projects/praxis-core/src/lib/i18n/value-presentation.resolver.ts`
- focused i18n, resource discovery, and value presentation specs

## Canonical Boundary

`@praxisui/core` owns shared i18n models, translator token, config multi-provider, `PraxisI18nService`, fallback behavior, resource discovery namespace, resource availability reason mapping, unavailable workflow copy, and value presentation helpers.

Vertical packages own package-specific namespaces and catalogs. Backend metadata/config owns domain labels, business names, option labels, resource names, and user-authored content.

## I18n Rules

- Use `providePraxisI18nConfig(...)` for namespace catalogs and keep it multi-provider.
- Use `providePraxisI18nTranslator(...)` only for a real external translator bridge.
- Keep at least `pt-BR` and `en-US` coverage for shared core framework text.
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

- `i18n.service.spec.ts`
- `resource-discovery.i18n.spec.ts`
- `value-presentation.resolver.spec.ts`
- direct consumer specs when a package adopts shared copy
- hardcoded-text audit or report review for broad cleanup
- `npm run build:praxis-core` when exports/providers change

Report which text is framework chrome versus domain content and which locales were covered.

## Companion Skills

- Use `praxis-angular-i18n-governance` for workspace-wide i18n policy and hardcoded text audits.
- Use `praxis-core-resource-runtime` when resource discovery availability, actions, surfaces, or capabilities drive copy.
- Use `praxis-core-providers-bootstrap` when provider wiring changes.
- Use `praxis-angular-public-api-governance` and `praxis-angular-validation-gates` for exports and validation.
