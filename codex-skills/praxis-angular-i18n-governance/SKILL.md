---
name: praxis-angular-i18n-governance
description: Use when implementing, auditing, or migrating Praxis Angular framework-owned text: PraxisI18nService/config/providers, namespace catalogs and locales, authoring chrome, hardcoded labels/tooltips/placeholders/aria/errors/empty states, LOCALE_ID formatting, translation fallbacks/overrides, legacy text tokens, catalog conformance, or i18n-derived docs and visual QA.
---

# Praxis Angular i18n Governance

Use this skill for framework-owned text in `@praxisui/*`. Praxis i18n translates internal runtime and authoring chrome while preserving host-owned business language from metadata, schemas, config, actions, capabilities, and domain decisions. It must never turn the library catalog into a second source of truth for domain semantics.

## Classify The Text Before Editing

Classify every visible string, including a generated default, before choosing a catalog key:

| Text kind | Owner and treatment |
| --- | --- |
| library chrome: buttons, tabs, menus, tooltips, aria labels, placeholders, empty states, generic validation, loading, confirmations | owning `@praxisui/*` namespace/catalog |
| shared framework/resource-discovery/value-presentation text | `@praxisui/core` i18n runtime or shared surface catalog |
| host business label, field/help text, resource/action/surface name, domain status, governance description | preserve metadata/schema/config/backend value; do not copy into a lib catalog |
| consumer override of library chrome | structured `PraxisTextValue`/documented override above the library catalog; do not persist it into a domain rule/effect |
| technical error, exception, provider message, trace, raw server response | diagnostics/logging; normalize into a safe i18n key before user presentation |

If the requirement is already a metadata/config/domain string that Angular is failing to materialize, classify it as `ja-suportado-so-ux` or `ja-suportado-mal-nomeado-ou-mal-materializado`. Do not create a library translation key for it. Only a real missing framework-text contract is `lacuna-real-de-contrato`.

## Required Inventory

Read `praxis-ui-angular/AGENTS.md`, `codex-rules.md`, and applicable local `AGENTS.md`. For Angular implementation work, follow the workspace Angular MCP requirements.

Inspect:

- the owning library's existing `src/lib/i18n/**`, providers, public API, focused specs, and local conventions;
- `@praxisui/core` `PraxisI18nService`, models, tokens, providers, utilities, global config, and formatting behavior;
- authoring/editor config, descriptors, action specs, defaults, metadata, and Settings Panel bridge when text is visible during editing;
- `tools/i18n/reports/catalog-inventory.md`, `catalog-coverage.md`, `hardcoded-text-hotspots.md`, and `locale-formatting-map.md` for audit context, treating reports as baseline evidence rather than a source of truth;
- README/docs/examples/playgrounds/screenshots that quote the framework text.

Search templates, TypeScript defaults, dialogs, UX services, descriptors, schemas, and aria attributes. Do not use a raw string search result as proof that a string is framework chrome: classify its runtime source and ownership first.

## Canonical Runtime And Precedence

`PraxisI18nService` is the shared runtime. Use `providePraxisI18nConfig`/`providePraxisI18n` with multi-provider configuration and a stable namespace; do not create a parallel translator service for one component.

The current resolution order for `t`/`tForLocale` is:

1. configured host/external translator;
2. namespace dictionary for the requested/current locale;
3. global dictionary for that locale;
4. namespace/global fallback locale;
5. controlled fallback text; then the key.

`resolve(PraxisTextValue)` intentionally preserves a plain string as a supplied value and resolves a descriptor through the same namespace-aware path. Use descriptors for framework-owned configurable defaults; leave host-domain strings intact. Do not parse display text back into keys, intent, actions, fields, or permissions.

Locale selection is config locale, then authenticated/bootstrap locale, then `pt-BR`; fallback locale is configured fallback then `pt-BR`. Formatting through `formatDate`, `formatNumber`, and `formatCurrency` follows this runtime locale with `Intl`. When a component also uses Angular `LOCALE_ID` or pipes, preserve the documented precedence and test the selected locale; do not introduce an unrelated locale source.

## Catalog Design And Migration

For new framework text:

1. Reuse the owning namespace and naming convention; create a new namespace only for a cohesive surface.
2. Add semantically stable keys, not English sentences as keys and not labels that encode domain data.
3. Add `pt-BR` and `en-US` coverage together. New Brazilian Portuguese files use `.pt-BR.ts`, preserve UTF-8, accents, and normative grammar.
4. Register through the owning provider/config, then test locale, fallback locale, interpolation, and consumer override behavior.
5. Update the visible editor/runtime behavior and any declared default descriptors in the same change.

Do not scatter microcatalogs among templates/components when the library has a shared catalog. Do not use a default parameter, an `err.message`, a translated-looking string constant, or a `labels` object as a hidden second catalog.

Existing legacy tokens or compatibility bridges may remain only with a documented owner and removal plan. Do not extend them for new work. Migrate to the canonical namespace/provider incrementally and keep compatibility at the boundary, rather than duplicating all catalog logic in components.

## Editors And Special Surfaces

Authoring chrome includes form defaults, action specs, editor descriptors, JSON-editor hints, section/tab names, buttons, validation, empty states, confirmation copy, accessibility labels, and Settings Panel lifecycle messages. A runtime-only catalog update is incomplete if the canonical editor still exposes hardcoded or stale text.

- Dynamic Fields: also inspect registry metadata, editorial descriptors, field catalogs, loader failures, inline filters, Metadata Editor, and Dynamic Form consumers.
- Table: keep table runtime/editor chrome in their namespaces while preserving host `config.localization` and metadata text as host overrides, not library defaults.
- Settings Panel/Page Builder/Form/Charts/Visual Builder: update the shared library catalog and prove the `Apply`/`Save`/`Reset`/reopen path when text appears in authoring.
- Cron Builder and Table Rule Builder: keep internal presets, panel/preview/validation/aria text in their owning namespace; host schedule/rule names and governance descriptions stay external.
- Dialog, Files Upload, and generic error services: do not expose raw or default technical text. Treat legacy defaults/tokens as migration surfaces and use safe normalized keys for new behavior.

## Accessibility And Visual Evidence

Translate all framework-owned visible and assistive copy consistently: text content, `aria-label`, `aria-describedby`, `title`, placeholders, hints, loading state, keyboard-help, and error/empty-state announcements. Preserve accessible names and do not reduce meaning to fit a translation.

For a visible or authoring change, inspect browser output in desktop and narrow viewports when feasible. Validate at least both configured locales for the affected surface, including text fit, focus/aria behavior, fallback behavior, and a no-result/error state when relevant.

## Validation Matrix

| Scope | Minimum evidence |
| --- | --- |
| one catalog key/component | focused component/catalog spec proving current locale, fallback locale, interpolation, and override/fallback path |
| shared i18n runtime/provider/formatting | core i18n specs, `npm run build:praxis-core`, and a direct consumer test |
| library catalog/provider export | owning lib focused spec plus build; use its full test script when behavior is transverse |
| authoring chrome/default descriptors | focused runtime/editor round-trip spec plus browser evidence when visible/stateful |
| broad cleanup or catalog migration | conformance/report tooling plus representative provider-backed and legacy surfaces; do not claim exhaustive coverage from `rg` alone |
| docs/examples/playgrounds | `praxis-angular-docs-playgrounds` and affected docs validation |
| AI manifest/component docs affected by copy/config semantics | `praxis-ai-authoring-manifests`/registry ingestion and the owning runtime/editor proof |

Use `praxis-angular-validation-gates` for exact commands and environment ownership. For skills-only changes, validate skills/manifest/sync only; Angular builds are required when Angular source, generated assets, or runtime contracts change.

## Derived Artifacts And Follow-ups

Review catalogs, providers, public API, docs, examples, screenshots, playgrounds, manifests/registry, locale-formatting documentation, and hardcoded-text/conformance reports as applicable. State why each is unaffected when skipped.

If audit reports identify a current framework-text hotspot without an executable conformance/migration path, register a platform issue instead of allowing a local exception silently. The current program-level follow-up is `praxis-ui-angular#164` for executable catalog parity and framework-chrome conformance; keep it distinct from resource-specific migrations such as Component Metadata defaults.

## No Keyword Routing

Do not use translated labels, aliases, phrases, regexes, or fuzzy matching to choose a resource, field, action, capability, authoring operation, or domain decision. Translation is presentation. Resolve semantic scope through canonical identifiers, metadata, schemas, capabilities, governed catalogs, and backend-issued decisions; text matching may only rank already-scoped candidates.

## Reporting

Report text classification, namespace/provider, locale coverage, compatibility/legacy decision, editor/runtime parity, exact validation, derived artifacts, and remaining hotspots. Clearly distinguish unrun browser, docs, registry, or broader conformance evidence.

## Companion Skills

- Use `praxis-core-i18n-resource-copy` for shared core runtime, resource-discovery, formatting, and cross-lib framework copy.
- Use `praxis-angular-validation-gates` and `praxis-angular-agents-governance` for scope, commands, and local rules.
- Use `praxis-authoring-editors`, `praxis-angular-docs-playgrounds`, and `praxis-ui-product-design` for editor, public, and visual proof.
- Use functional field/form/table/chart/settings/builder skills and `praxis-ai-authoring-manifests` when i18n changes affect their canonical contracts.
