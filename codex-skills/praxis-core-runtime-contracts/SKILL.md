---
name: praxis-core-runtime-contracts
description: Use when Codex must inspect, change, or rely on @praxisui/core shared runtime contracts: public-api exports, tokens, providers, i18n, logging, common services, registries, shared models, presentation microvisualizations, schema infrastructure, global actions, config storage, CRUD/discovery services, or cross-lib contracts consumed by other @praxisui/* packages.
---

# Praxis Core Runtime Contracts

Use this skill for `@praxisui/core`, the canonical Angular owner of shared contracts, tokens, services, registries, models, providers, logging, i18n, schema infrastructure, global actions, and runtime utilities used by the other `@praxisui/*` libraries.

This skill is about the Angular runtime contract. It does not make Angular the source of backend business semantics. `praxis-metadata-starter` owns `x-ui`, schemas, actions, surfaces, capabilities, option-source semantics, and metadata emission. `praxis-config-starter` owns governed config/registry/template persistence. `@praxisui/core` consumes, normalizes, materializes, and exposes stable Angular contracts for those projections.

## Source Audit

Before changing a core-facing skill or implementation, inspect the real source for the affected area:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/README.md` when package usage, setup, public contracts, or consumer guidance changes
- `projects/praxis-core/src/public-api.ts`
- `projects/praxis-core/docs/schema-flow.md` when schema or metadata flow changes
- `projects/praxis-core/docs/connection-editor.md` when connection, widget wiring, or actions change
- `projects/praxis-core/docs/rfc-dynamic-page-canvas-runtime.md` when dynamic page runtime, `WidgetDefinition`, dynamic widget loading, or page composition contracts change
- `projects/praxis-core/src/lib/models/**`
- `projects/praxis-core/src/lib/services/**`
- `projects/praxis-core/src/lib/tokens/**`
- `projects/praxis-core/src/lib/providers/**`
- `projects/praxis-core/src/lib/i18n/**`
- `projects/praxis-core/src/lib/logging/**`
- `projects/praxis-core/src/lib/reconcilers/**`

Do not rely on memory of the package. The core public API changes often and is the upstream owner for many runtime behaviors that vertical libs consume.

## Canonical Owner Decision

Put the fix in `@praxisui/core` when the concern is shared across libraries or affects one of these contracts:

- `GenericCrudService`, schema metadata clients, resource discovery, config storage, global config, and common CRUD/data access helpers
- global actions, global surfaces, action refs, action UI schema, action catalogs, and shared action providers
- tokens such as `API_URL`, `PAX_FETCH_HEADERS`, global config, loading, overlay decisions, export, external editors, field selectors, or surface/drawer bridges
- common models: table config, field metadata, option sources, resource discovery, domain catalog, domain knowledge/rules, query context, analytics presentation, loading state, collection export, surface actions, runtime observations
- shared rich-content models such as `RichContentDocument`, rich nodes, action refs, presenter nodes, and JsonLogic-backed rich-content conditions
- logging, observability, error normalization, telemetry sinks, and global error handling
- i18n service, providers, resource-discovery copy, value presentation, and shared internal framework text
- reconcilers and config normalization shared by multiple libs

Do not move shared semantics into `praxis-table`, `praxis-dynamic-form`, `praxis-list`, host apps, examples, or migration code when the contract belongs in core.
Core runtime contracts should stabilize Angular materialization boundaries, not promote consumer convenience into semantic authority. If a vertical package, host, recipe, or migration needs a shared model only because it is compensating for missing backend metadata, config-starter state, AI manifest data, action/surface discovery, capability discovery, or provider bootstrap, fix the canonical source or projection first.
When a core contract represents a projection of backend/config/AI evidence, preserve source refs, operation ids, resource/action/surface ids, diagnostics, freshness, and ownership. Do not collapse that evidence into display labels, enum aliases, command strings, or local booleans that later agents could mistake for primary authorization.

## Public API Guardrails

Any change to `src/public-api.ts`, exported models, exported services, exported tokens, root providers, or shared AI contracts is at least `contrato-publico`.

Before editing:

1. Identify the canonical owner of the contract.
2. Search for direct consumers in `projects/*`, examples, docs, and recipes.
3. Check whether another public lib is using the core root barrel as a transitively convenient facade.
4. Prefer a minimal stable export from the true owner over reexporting another lib's root API.
5. Plan at least a focal build/test for `praxis-core` and one direct consumer when the export is used outside core.

Do not add a root export merely to make a local import easier. `public-api.ts` must remain an intentional, packageable contract.
Do not use `@praxisui/core` as a transitively convenient facade for contracts owned by another public package. If another lib owns the runtime behavior, either import from that owner, move the shared contract into core with an explicit consumer map, or define a narrow structural adapter at the consumer boundary.

## Platform Aderence Inventory

Before creating a new model, token, provider, service, config field, event, adapter, or export, answer:

`What does Praxis already know, but the Angular runtime or consumer is not materializing well?`

Classify each need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public core contract. If the data already exists in backend metadata, config starter state, action/surface/capability discovery, AI manifests, config storage, diagnostics, or runtime registries, fix the owner or materialization instead of adding a parallel Angular concept.

## Enterprise Navigation And Context Generation

Before changing `EnterpriseRuntimeContextService.navigation`, inspect its model,
service/spec and Config's current `P3B-DESIGN.md`, provider and DTOs. Config owns
publication/visibility; Core consumes that projection, not a second menu registry.
Reuse Core's existing `UiLayoutReleaseHeadReceipt` by owner-local type import.
Preserve the admitted icon token, lazy `children: null`, required receipt/context
fields and nullable continuation; do not infer private child counts or grants.

Capture the existing `contextRevision` before awaiting `ready()`. Require a ready,
nonblank server context version; recheck generation/current version after the
wait, after host header preparation, and after HTTP success or failure. A→B→A
must reject the first A's callback even if business identifiers repeat. Reuse
`EnterpriseRuntimeContextObsoleteError`; preserve current-generation HTTP errors.
Copy validated pagination options before the wait and use the confirmed snapshot
headers while preserving authentication and endpoint overrides. Never dispatch
navigation using bootstrap context claims or an unconfirmed version.

The minimal navigation client does not cache bodies or send If-None-Match. Any
later cache adoption needs explicit 304/body and revocation handling; a stored
menu is not authority to open its route. Prove the public HTTP service with the
focused `enterprise-runtime-context.service.spec.ts`, including obsolete success,
error, pending-ready and header callbacks. Build Core and a real direct consumer.
A Dynamic Form build proves package integration, not menu navigation. Locate an
actual visual consumer before selecting browser E2E; report renderer/route wiring
and live host HTTP separately when those downstream gates remain unimplemented.

## Presentation Distribution Contract

For `PraxisPresentationVisualizationConfig`, inspect
`projects/praxis-core/src/lib/models/presentation-visualization.model.ts` and its
spec before editing a consumer. Core owns normalization, denominator resolution,
and HTML materialization; Charts owns the Angular microvisualization renderer,
which must consume this policy instead of defining a second validation policy.

- For `stackedBar`, preserve the supplied distribution. Reject missing/invalid
  segments (including sparse arrays), negative or non-finite values, a non-finite
  sum, and an invalid, negative, or materially smaller explicit `total` by removing
  all segments and rendering `fallbackText`. Never drop only the bad category, clamp its data,
  renormalize to fit, or invent a remainder category.
- An absent `total` uses the finite segment sum; explicit zero is valid only
  when the sum is zero. Compare floating-point sums with relative tolerance from
  the canonical normalizer, not an absolute epsilon that admits tiny bad totals.
- Outside `table-cell`, `legend: true` requires every segment label; missing
  labels cause the same complete fallback. For `table-cell`, normalize legend to
  false and remove the presentation title without mutating the input. The HTML
  path must also omit compact metadata, keeping cells free of category text.
- Accept materialized category colors only through the existing hex-color
  normalization. Keep bar/swatch colors, zero-width segments, denominator-based
  percentages, fallback accessibility, and application locale aligned across
  Charts and HTML consumers.

Use Core's `getPraxisStackedBarPaintStyle` for segment/swatch paint. It sets
`--prx-micro-category-color` and `color` on each category span from validated hex
or tone. Trusted host CSS may set `--prx-micro-segment-background`,
`--prx-micro-segment-shadow`, `--prx-micro-swatch-shadow`,
`--prx-micro-track-shadow`, `--prx-micro-track-height`, and the existing
`--prx-micro-track-radius`/`--prx-micro-track-color`. For category-dependent host
gradients or shadows, use `currentColor`: an ancestor token referencing
`var(--prx-micro-category-color)` resolves on that ancestor before the local
category context exists. Metadata still supplies only validated hex/tone;
do not add raw CSS in JSON, new DTO fields, or feature flags for host styling.

Shadows default to `none`; a zero-value segment always has `box-shadow:none`
even when a host shadow is set, while its legend swatch retains its styling.
Entry motion uses track opacity `0` to `1` once, with
`--prx-micro-motion-duration` (`0ms`), `--prx-micro-motion-delay` (`0ms`), and
`--prx-micro-motion-easing` (`ease-out`). Preserve the no-motion default and
disable animation/transition under `prefers-reduced-motion: reduce` regardless
of host tokens. Do not animate width, scale, or clip paths: proportions must stay
truthful and the reveal must not clip shadows.

Proof requires the model spec and real consumer DOM specs:
`projects/praxis-table/src/lib/praxis-table.micro-visualization-renderer.spec.ts`
and `projects/praxis-dynamic-fields/src/lib/components/field-shell/field-shell.micro-visualization.spec.ts`.
Cover over-total/negative/non-finite evidence, zero totals, missing legend labels,
localized percentages, matching colors, and table-cell suppression. Helper-only
assertions do not prove consumer sanitization, layout, styles, or locale wiring.
Keep geometry at calculation precision; `toFixed` belongs only to display labels,
not segment widths. Compare HTML and Charts with 201 equal categories: cumulative
width must not overflow and hide the last category. Include a small positive
allocation that two-decimal width rounding would erase. Exercise hundreds of
decimal fractions against an exact declared total (300 values of `0.1`, total `30`)
to catch summation error causing a false fallback. Retain rejection of genuinely
incoherent tiny totals, such as total `Number.MIN_VALUE` with value `1`; do not
widen an absolute epsilon to make the decimal case pass.
Through the real Table renderer, omit `surface` and also supply a conflicting
`surface: 'card-summary'` with title/legend requested. The owning cell must still
materialize `table-cell` semantics. Core config normalization alone cannot prove
that the consumer supplies its actual surface context.
For host effects, prove computed category paint/shadows, zero-segment geometry
and shadow suppression, track tokens, and motion in Charts, Table, and FieldShell.
Exercise browser reduced-motion emulation separately; checking the current media
query branch alone does not prove the override. Record unexecuted gates explicitly.
Prove unchanged rerenders do not restart entry animations, while row/locale
updates remain fresh; inspect Table's `getMicroVisualizationHtml` materialization.
For FieldShell lifecycle tests, spy on `getPresentationHtml` and assert it was
called during the unchanged check before comparing DOM identity. Drive the
OnPush component view through its own `ChangeDetectorRef`; a host-fixture check
alone can skip that view and pass without exercising materialization. Then change
data/locale and assert fresh output. A failing gate remains an open runtime defect;
adding guidance does not establish that the implementation is corrected.
Review Core/Charts docs, examples and public landing projections for drift.

## Validation Guidance

Prefer the smallest reliable validation:

- localized shared service/model/reconciler change: focused `.spec.ts` for the area
- exported contract or public API change: `npm run build:praxis-core` plus at least one consumer build/test
- schema flow, `GenericCrudService`, resource discovery, global actions, i18n, logging, or widgets: treat as transversal and include focused consumer specs
- AI contract/manifest change: validate the relevant manifest spec and registry ingestion when applicable

Use concrete focused gates from `praxis-ui-angular` before broadening:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/generic-crud.service.spec.ts --include=projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts
```

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/config-storage.service.spec.ts --include=projects/praxis-core/src/lib/services/global-action.service.spec.ts --include=projects/praxis-core/src/lib/actions/global-action-ref.utils.spec.ts
```

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/i18n/i18n.service.spec.ts --include=projects/praxis-core/src/lib/i18n/resource-discovery.i18n.spec.ts --include=projects/praxis-core/src/lib/i18n/value-presentation.resolver.spec.ts
```

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/logging/logger.service.spec.ts --include=projects/praxis-core/src/lib/logging/provide-praxis-logging.spec.ts --include=projects/praxis-core/src/lib/logging/praxis-global-error-handler.spec.ts
```

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/reconcilers/filter-config-reconciler.spec.ts --include=projects/praxis-core/src/lib/reconcilers/form-config-reconciler.spec.ts --include=projects/praxis-core/src/lib/services/table-config-reconciler.spec.ts
```

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/component-metadata-registry.service.spec.ts --include=projects/praxis-core/src/lib/services/runtime-component-observation-registry.service.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-record-surface-open.spec.ts
```

For root barrel, exported model, token, provider, or shared service changes, run:

```sh
npm run build:praxis-core
```

Then validate at least one direct consumer that imports the changed contract, commonly:

```sh
npm run build:praxis-dynamic-form
npm run build:praxis-table
npm run build:praxis-dynamic-fields
```

Pick the consumer by actual imports rather than running all builds reflexively. If the change touches table-facing contracts, `npm run test:table` is the usual first consumer test gate.

If PowerShell audit scripts are unavailable, use the repository Python fallbacks:
`python3 scripts/audit-praxis-skills.py --family praxis` for manifest/hash drift,
`python3 scripts/validate-praxis-skills.py --family praxis` for structure/frontmatter,
and `python3 scripts/sync-praxis-skills.py --family praxis` when local skill installation must be refreshed.

Use `praxis-angular-validation-gates` for command selection and `praxis-angular-public-api-governance`
before changing root exports or cross-lib public contracts. Use `praxis-angular-i18n-governance` when
core text, logging UX, resource-discovery copy, or shared localization changes. Use
`praxis-angular-docs-playgrounds` when public docs, examples, or package docs reflect the contract.

## Companion Skills

- Use `praxis-core-resource-runtime` for resource discovery, schema, capabilities, HATEOAS, option sources, CRUD operation resolution, and analytics request contracts.
- Use `praxis-core-surface-materialization` for focused resource action/surface adapter payloads, `surface.open` materialization, related-resource surfaces, and first-step local audits.
- Use `praxis-core-global-action-payloads` for `GlobalActionRef`, payload schema/UI schema, validation, payloadExpr, onResult, and command-string cleanup.
- Use `praxis-core-domain-governance-runtime` for domain catalog, knowledge, rules, simulations, publications, materializations, and config-starter semantic decision clients.
- Use `praxis-core-component-registry-contracts` for `ComponentMetadataRegistry`, component docs/editorial metadata, ports, insertion presets, and builder/AI registry projection.
- Use `praxis-core-composition-runtime` for composition runtime, widgets, dynamic widget pages, nested ports, connection/link execution, and surface hosts.
- Use `praxis-core-providers-bootstrap` for shared providers, tokens, bootstrap, global config, loading, icon, field selector, collection export, and registry wiring.
- Use `praxis-core-widget-observations` for dynamic widgets, widget pages, widget events, composition observations, runtime observation envelopes, and observation registry.
- Use `praxis-core-logging-observability` for logging, telemetry sinks, error normalization, PII redaction, throttling, global error handling, and observability alerts.
- Use `praxis-core-i18n-resource-copy` for `PraxisI18nService`, i18n providers, resource-discovery copy, value presentation, and shared framework text.
- Use `praxis-core-global-actions-metadata` for the broader global action and metadata-services umbrella.
- Use `praxis-rich-content-runtime` and `praxis-rich-content-ai-security-validation` when shared rich-content models, validator assumptions, host-mediated actions, or public rich-content exports are involved.
- Use `praxis-angular-host-project` when applying core contracts in a consuming host.
- Use `praxis-component-minimums` when the question is the smallest runtime setup for a component.
- Use `praxis-ui-product-design` for visual/product UX and screenshot validation.
- Use `praxis-angular-public-api-governance` for public API boundaries and cross-lib export decisions.
- Use `praxis-angular-validation-gates` for focused local validation and release/preflight boundaries.
