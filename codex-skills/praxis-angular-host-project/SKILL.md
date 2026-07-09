---
name: praxis-angular-host-project
description: Create or evolve Angular host applications that consume Praxis UI packages. Use when Codex must scaffold a new Angular project using published @praxisui/* packages, adapt a host from praxis-ui-quickstart, wire API_URL/PAX_FETCH_HEADERS/GenericCrudService/providers, create resource-oriented table/form/crud/list routes, configure local or remote Praxis UI runtime config, validate resourcePath/schema-driven integration, or decide which Praxis UI companion skills apply for authoring, dynamic-fields, config storage, or visual QA.
---

# Praxis Angular Host Project

Use this skill to build Angular hosts for the Praxis UI runtime. Default to public npm packages and treat `praxis-ui-quickstart` as a reference host, not as the source of platform semantics or a required local dependency.

Before changing this skill or implementing a host, audit the current runtime contract that will be consumed: `@praxisui/core` public API, `API_URL`, `PAX_FETCH_HEADERS`, `GenericCrudService`, `SchemaMetadataClient`, global config bootstrap/storage, resource discovery, surface and related-resource materializers, `@praxisui/crud` launcher/open-mode APIs, component registry assets, and the reference quickstart package/bootstrap graph. Codify what Praxis already knows and materializes before adding host adapters, local schemas, local aliases, or new contracts.

Use `praxis-core-runtime-contracts` whenever the task touches `@praxisui/core` public API, tokens,
providers, shared services, i18n, logging, or cross-lib contracts. Use
`praxis-core-resource-runtime` for `GenericCrudService`, schema metadata, resource discovery,
actions, surfaces, capabilities, option sources, related resources, and analytics runtime. Use
`praxis-core-composition-runtime` for dynamic widget pages, composition links, surface hosts, and
runtime observations.

## Canonical Sources

- `praxis-ui-angular` owns the public Angular packages, runtime providers, tokens, services, component APIs, and public Angular contracts.
- `praxis-metadata-starter` owns backend metadata semantics: `x-ui`, `/schemas/filtered`, surfaces, actions, capabilities, schema/domain discovery, and metadata-driven resource contracts.
- `praxis-config-starter` owns `/api/praxis/config/**`, `ui_user_config`, AI registry/config, headers, ETag, and remote configuration persistence.
- `praxis-ui-quickstart` is the operational adoption reference for a first Angular host. Use it to copy proven host patterns, not to redefine contracts.
- `praxisui.dev` and `praxis-ui-landing-page` publish docs and examples; they do not override the canonical backend or runtime owners.

When these disagree, prefer the canonical owner. Do not create local frontend conventions that bypass a missing backend/runtime contract.

## Semantic Runtime Boundary

Treat an Angular host as the cockpit and runtime for governed Praxis materializations, not as the primary source of business rules or semantic decisions. The host owns shell, routes, auth, tenant/locale/user headers, deployment, theme, and product layout decisions. It consumes canonical decisions and projections from `praxis-metadata-starter`, `praxis-config-starter`, and the published `@praxisui/*` runtime.

Use `/schemas/filtered` as the structural schema source. Use `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain`, capabilities, HATEOAS links, option sources, and `/api/praxis/config/**` as discovery, availability, grounding, persistence, or materialization surfaces according to their canonical owner. Do not make a host component, route, page-builder screen, or assistant flow redefine those contracts.

Do not route user intent in the Angular host by keywords, regexes, command words, field aliases, or local fuzzy matching as the primary decision mechanism. If an assistant or authoring UI needs to decide intent, use governed AI/LLM authoring contracts, component registries, semantic catalogs, capabilities, actions, surfaces, and declared tools as grounding. Text matching may rank candidates only after the semantic scope is resolved.

Before creating a new Angular-only input, DTO, adapter, service, manifest field, config shape, or fetcher, inventory platform support and classify the gap as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only `lacuna-real-de-contrato` justifies a new public contract, and the owner should normally be `praxis-ui-angular`, `praxis-metadata-starter`, or `praxis-config-starter`, not an app-local route.

## Platform And Skill Feedback Loop

When a host implementation exposes repeated boilerplate, a missing public input/output, a weak runtime materialization, or a visual/UX pattern that would be copied by other hosts, do not finish by patching only the host.

Classify the finding before coding:

- `already-supported`: use the native Praxis component/service path and remove host duplication.
- `supported-partially`: use the native Praxis path for the supported part, keep only the smallest temporary host bridge for the missing part, and record the removal trigger.
- `platform-gap`: open or register a traceable Praxis platform follow-up with owner, expected behavior, observed evidence, impact, temporary workaround, and a prompt for the platform specialist.
- `consumer-guidance-gap`: update or request an update to the consumer-specific skill, example, recipe, or roadmap that caused agents to choose the wrong component, local adapter, CSS workaround, or boilerplate.

For Angular migration hosts, apply native Praxis first: check the official component, service, output, adapter, token, and metadata-driven path before writing host-owned CRUD, table, surface, form, or styling code.

For migration or consumer hosts, keep the host thin. If the desired screen pattern requires custom launchers for actions/surfaces/capabilities, local schema projection, CSS selectors against internal Praxis classes, per-screen layout metadata that should come from `x-ui`, or manual event bridges for materialized widgets, treat that as platform or consumer-guidance debt first. A temporary host workaround must name the removal trigger and must not be promoted as the reference pattern.

When replacing host-authored presentation with generated Praxis layout, such as `layoutPolicy` or generated form presets, validate the actual browser result before removing the curated host layout. If the generated layout builds but adds irrelevant fields, creates low-value groups, breaks first-viewport master-detail fit, or otherwise lowers UX quality, classify it as `platform-gap` or `supported-partially`, keep only the smallest temporary visual workaround, and register the runtime improvement instead of forcing the generated output as the migration reference.

For CRUD create/edit/view launchers, check `PraxisCrudComponent` and `CrudLauncherService` before building host-owned drawers or dialogs. With `@praxisui/* >= 9.0.0-beta.33`, schema-backed drawer flows should use `CrudLauncherService` with `openMode='drawer'` and the platform drawer runtime; do not build per-screen backdrop, sizing, focus, expand/collapse, submit-result, or refresh shells in the host. If a required drawer behavior is still missing from the platform runtime, classify only that behavior as a `platform-gap` and keep the host workaround explicitly temporary.

For migration hosts consuming `@praxisui/* >= 9.0.0-beta.31`, use schema-driven form layout as the default reference pattern. Detail/read-only master-detail forms should use `PraxisDynamicForm` with a response schema and `layoutPolicy.source='schema'`, `intent='detail'`, `preset='compactPresentation'`. Create/edit command forms should use request schemas and `layoutPolicy.source='schema'`, `intent='command'`, `preset='groupedCommand'`. Do not add `FormConfig.sections` or placeholder `sections: []` just to make a schema-driven form work; if the generated layout is wrong, classify the gap and fix the canonical runtime or metadata contract.

Before promoting a consumer screen as a reusable Praxis example, run the host's official static checker when present. A valid checker should reject local form section stubs, table responsive overrides, deep CSS selectors, host-owned CRUD shells, and temporary adapters that duplicate platform runtime behavior.

Use temporary-checker bypasses only for in-progress screens with an explicitly documented removal trigger. A final canonical reference must pass strict mode and must not contain local `FormConfig.sections`, `sections: []`, table responsive overrides, `::ng-deep`, or a host-owned CRUD drawer shell.

For materialized related surfaces, separate row-selection transport from action authorization. Before opening a platform issue, check whether the consumed `@praxisui/core` exposes `PraxisSurfaceHostComponent` outputs such as `rowClick`, `selectionChange`, and `widgetEvent`, and whether `SurfaceOpenMaterializerService` wires those outputs for `praxis-table`. If those outputs exist and the host already listens to them, treat disabled edit/delete buttons as a `_links`/capabilities/fixture validation problem, not as a missing surface selection contract.

For metadata-driven related resources, prefer the platform `surface.relatedResource` contract before writing host-local filters, relationship adapters, or resource-page wrappers. When a catalog surface publishes `relatedResource`, use `PraxisRelatedResourceOutletComponent` or `RelatedResourceSurfaceResolverService` so the parent-child filter comes from `childParentField` and the selected parent id comes from `parentIdPathVariable` or explicit `parentResourceId`. Do not duplicate the same parent filter in page `composition.links` unless the page is intentionally overriding the canonical query context. For examples and AI recipes, anchor the fixture in the real quickstart contract `operations.missoes` surface `team` -> `operations.missao-participantes` with `childParentField=missaoId`, instead of synthetic surface names such as `participants`.

For table chrome, use the public `TableConfig` contract before styling internals. If a migration screen must hide the assistant affordance, set `ai.assistant.enabled=false` instead of targeting table DOM or CSS selectors.

When updating skills, change the versioned source under `codex-skills/` when it exists, then run `scripts/sync-praxis-skills.ps1` for the smallest necessary sync. If the relevant migration skill is installed locally but has no versioned source in this repo, record that ownership gap instead of silently editing only the installed copy.

## Required Workflow

1. Classify the host mode:
   - New public-npm host.
   - Existing Angular host being upgraded to Praxis UI.
   - Platform validation host using local `praxis-ui-angular/dist`.
   - Authoring/customization host with remote config persistence.
2. Identify the backend:
   - Published quickstart API: `https://praxis-api-quickstart.onrender.com/api`.
   - Host-specific Praxis API.
   - Local reference API such as `praxis-api-quickstart-public`.
3. Resolve dependency train before editing:
   - Use the existing host lockfile/package train when present.
   - Otherwise inspect npm metadata, peer dependencies, and the published quickstart package graph.
   - Treat conflicting docs/package manifests as drift until verified against npm/package metadata.
   - Prefer a fixed version or lockfile for reproducible starters. Use `latest` only after verifying it is the intended active release train for the Angular major and that the full peer closure resolves.
   - Pin Angular packages to one exact patch across framework, Material/CDK, CLI/build, and compiler packages; do not mix a newer core patch with an older Material/CDK patch.
4. Scaffold or adapt the host with canonical bootstrap:
   - `API_URL.default.baseUrl` is the single API base.
   - `resourcePath` values are relative when the API base already includes `/api`.
   - Register `PAX_FETCH_HEADERS` with tenant, locale, auth, and user/env headers when available.
   - Register Praxis runtime providers and the pipes required by table/form runtime.
5. Add the smallest useful route set:
   - First adoption path: table, dynamic form, CRUD, and list against the same resource.
   - Expansion path only after the core path works: manual form, tabs, stepper, expansion, charts, editorial forms, page builder, AI shell.
6. Validate with the narrowest useful gates:
   - Build and smoke/unit tests for the host.
   - Network or browser validation for remote schema/data flows when feasible.
   - Screenshot QA when the request includes visual/product quality.

## Source-Free Package Discovery

When working from published `@praxisui/*` packages without local `praxis-ui-angular` source, first inspect the package's AI registry asset when present:

- `@praxisui/<package>/ai/component-registry.json`

This asset is package-scoped and is generated from the canonical ingestion registry. Use it to understand selectors, component metadata, inputs, outputs, authoring chunks, capabilities, icons, tags, and package-owned component guidance before inventing local host conventions. For aggregate or cross-package release analysis inside the monorepo, use `dist/praxis-component-registry-ingestion.json` from `praxis-ui-angular`; do not require host projects to have that source artifact.

## Scaffold Procedure

For a new host, prefer this order:

1. Create a modern Angular standalone app with routing and SCSS, using the Angular version compatible with the chosen Praxis UI train.
2. Install Angular Material/CDK and the required `@praxisui/*` packages from npm. Install only the expansion packages that the first route set actually uses.
3. Resolve and install the complete peer graph for the chosen Praxis UI train; the current public graph may require packages such as settings-panel, metadata-editor, dialog, rich-content, visual-builder, table-rule-builder, and ai even when the first route set is narrow.
4. Add an Angular Material theme stylesheet, Material icons/symbols, CDK overlay styles, and `@praxisui/core/theme-bridge.css` or a proven equivalent host bridge before validating Material/Praxis components. `theme-bridge.css` complements the Material theme; it is not a replacement for the base Material component CSS. If a CSS file is not exported as a package subpath in the published train, add it through `angular.json` using the `node_modules/...` file path.
5. Create a central platform config file for API origin/base URL, resource paths, tenant/locale defaults, and `GlobalConfig` defaults.
6. Wire `app.config.ts` with `API_URL`, headers, providers, pipes, logging when appropriate, and route providers.
7. Add the core route set: table, form, CRUD, and list against the same resource.
8. Run build/smoke validation before adding advanced authoring or visual polish.

If the host already exists, preserve its routing, auth, design system, build tool, and deployment conventions unless they conflict with the canonical Praxis integration contract.

## Host Decisions

Use these defaults unless the host already has stronger local governance:

- Angular: standalone components and route-level lazy loading.
- Runtime model: when using `provideZoneChangeDetection`, install `zone.js` and include it in the app build polyfills.
- URL policy: `API_URL.default.baseUrl = '<origin>/api'` or `'/api'` behind a dev proxy; component `resourcePath = 'domain/resource'`.
- Resource path policy: pass the base resource only, such as `human-resources/funcionarios`; do not pass `/api`, `/filter`, `/all`, `/{id}`, query strings, schema endpoints, or operation URLs as `resourcePath`.
- First resource: reuse `human-resources/funcionarios` when validating against the public quickstart API.
- Core route intent: table, dynamic-form, CRUD, and list. Package install must still include the complete peer closure for the chosen train, not only the packages imported in templates.
- Host owns shell, auth, routing, theme, design tokens, tenant/locale/auth headers, and deployment.
- Praxis UI owns metadata interpretation, runtime materialization, reconcilers, storage contracts, component behavior, and governed authoring adapters.

Do not prefix resource paths with `/api` when `API_URL` already points at `/api`. Avoid `resourcePath="/api/..."`, `resourcePath=".../filter"`, and duplicated `/api/api/...` paths. CRUD, schema, filter, option, item-id, submit, and capability endpoints are resolved by Praxis runtime services from the base resource and metadata.

## Route Parity Diagnostics

When table works but form, CRUD, or list fail for the same resource, check whether the table is relying on a local `TableConfig.meta.idField` while the other surfaces consume `/schemas/filtered` through `GenericCrudService` without an explicit `idField` query parameter. Query `/schemas/filtered?path=<base-resource>/filter&operation=post&schemaType=response` and `schemaType=request` exactly as the runtime does. If `x-ui.resource.idField` diverges from the resource DTO key, fix the canonical backend metadata owner, usually `praxis-metadata-starter`, or the host's published OpenAPI/schema metadata. Do not compensate by threading ad hoc `idField` params through Angular runtime calls or by adding frontend aliases.

## Minimum Runtime Modes

Always separate the target component mode:

- Local-only runtime: local config/data; no backend schema discovery required.
- Backend metadata-driven runtime: `resourcePath` or operation-specific schema/submit endpoints resolve schemas/data from the backend.
- Authored/customizable runtime: host enables config persistence and authoring/editor flows; this may require `praxis-config-starter`.

For minimum component details, load `references/runtime-components.md` and, when needed, use `praxis-component-minimums`.

## Config Storage Decision

Use local/static config for a first host unless the user asks for persisted customization, shared settings, AI provider config, or `/api/praxis/config/**`.

When remote config is required:

- Backend must have `praxis-config-starter` and `/api/praxis/config/ui`.
- Prefer `providePraxisGlobalConfigBootstrap(...)` as the remote storage entry point.
- Keep `provideGlobalConfig(...)` for product defaults.
- Avoid `provideGlobalConfigSeed(...)` during remote migration unless the current host explicitly uses the quickstart-style local seed.
- Decide whether saves are user-scoped or tenant-scoped before implementation.
- Keep headers symmetric between interceptors and `PAX_FETCH_HEADERS`.

Load `references/host-bootstrap.md` for bootstrap and remote config guidance.

## Query And Persistence Policy

For table, list, CRUD, charts, and composed surfaces, prefer `queryContext` for filters, pagination, sort, joins, contextual fan-out, and host-provided criteria. Treat older `filterCriteria` style inputs as legacy bridges unless the existing host already uses them.

For configurable surfaces:

- Keep `enableCustomization` off for immutable demo surfaces, transient previews, or surfaces that should not write preferences.
- Choose the component's documented config persistence strategy deliberately, such as volatile/input-first/local-first/remote-backed behavior when available.
- Do not enable remote persistence just because a component supports customization; persistence is a host/product decision.

## Companion Skills

Use these alongside this skill when the task scope requires them:

- `praxis-component-minimums`: minimum setup for table/form/list/CRUD, local vs remote metadata-driven modes, and `resourcePath` boundaries.
- `praxis-core-runtime-contracts`: core public API, tokens, providers, models, i18n, logging, and shared services.
- `praxis-core-resource-runtime`: core schema/resource discovery, actions, surfaces, capabilities, option sources, related resources, and analytics materialization.
- `praxis-core-composition-runtime`: dynamic widget pages, composition links, widget events, surface hosts, and runtime observations.
- `praxis-table-runtime-data`: table runtime data modes, `resourcePath`, renderers, selection, export, analytics, and validation.
- `praxis-table-filter-actions`: table filters, dynamic filter payloads, toolbar/row/bulk actions, global actions, CRUD actions, and export grounding.
- `praxis-table-authoring-settings`: table Settings Panel, config editors, columns, rules, filters, actions, CRUD integration, and round-trip.
- `praxis-table-ai-validation`: table AI manifests, component edit plans, runtime operations, context packs, registry ingestion, and assistant E2E.
- `praxis-form-runtime-submit`: dynamic-form runtime modes, schema metadata, submit payload, local/transient fields, hooks, actions, and validation.
- `praxis-form-layout-canvas`: dynamic-form layout policy, schema-driven layout, visual blocks, canvas, and layout validation.
- `praxis-form-authoring-settings`: dynamic-form config editors, Settings Panel, authoring document, apply/save/reset, and round-trip.
- `praxis-form-ai-rules-validation`: dynamic-form AI manifests, rules, diagnostics, context packs, registry ingestion, and assistant validation.
- `praxis-fields-runtime-loader`: dynamic-fields loader, component registry, selector mapping, hot metadata, and runtime coverage.
- `praxis-fields-option-sources`: optionSource, async/searchable selects, entity lookup, by-ids reload, and dependency filters.
- `praxis-fields-editorial-discovery`: dynamic-fields editorial descriptors, catalogs, i18n, and metadata-editor/tooling discovery.
- `praxis-fields-ai-canvas-validation`: dynamic-fields AI manifest, control profiles, catalog ingestion, recipes, and canvas validation.
- `praxis-charts-runtime-data`: `@praxisui/charts` runtime, `x-ui.chart`, `chartDocument`, ECharts adapter boundary, analytics adapters, stats execution, `queryContext`, drilldown, and cross-filter.
- `praxis-charts-authoring-settings`: chart config editor, widget config editor, Settings Panel, apply/save/reset/reopen, governed resource/field/target catalogs, and chart editor round-trip.
- `praxis-charts-ai-validation`: chart AI manifest, editable targets, validators, handler contracts, registry ingestion, and component edit-plan validation.
- `praxis-dashboard-analytics`: backend dashboard/analytics resources, `/stats/*`, `@UiAnalytics`, aggregate resources, custom dashboard catalog/summary endpoints, capabilities, and option sources.
- `praxis-settings-panel-shell`: Settings Panel shell, drawer protocol, bridge separation, footer actions, and sizing.
- `praxis-settings-roundtrip-authoring`: visual editor apply/save/reset/reopen, persistence, and runtime consume validation.
- `praxis-settings-global-config`: Global Config Editor, effective config, save/clear, and remote persistence.
- `praxis-settings-ai-i18n-validation`: Settings Panel AI manifest, adapter, context pack, diagnostics, and i18n coverage.
- `praxis-ai-assistant-runtime`: `@praxisui/ai` assistant shell/client/runtime state, quick replies, diagnostics, previews, and apply payloads.
- `praxis-ai-authoring-manifests`: component authoring manifests, operations, validators, handler contracts, and edit plans.
- `praxis-ai-registry-ingestion`: AI registry ingestion, catalog governance, generated component docs, packaged AI assets, and backend sync.
- `praxis-ai-semantic-intent`: semantic intent routing, consult/edit boundaries, scope policy, and no keyword-based assistant routing.
- `praxis-ui-product-design`: visual quality, responsive layout, screenshot QA, product polish, theme/accessibility.
- `praxis-authoring-editors`: Settings Panel, config editors, apply/save/reset, editor/runtime round-trip.
- `praxis-dynamic-fields-editorial`: control types, aliases, field discovery, `optionSource`, async select, metadata editor coverage.
- `praxis-resource-entity-lookup-backend`: backend `RESOURCE_ENTITY` option-source contracts consumed by Angular controls.
- `praxis-java-host-project`: create or fix the backend host that publishes the metadata/config surfaces consumed by this Angular host.

## What To Avoid

- Do not assume access to local `praxis-ui-angular` source or `dist`.
- Do not use `npm link` as the default local-library strategy.
- Do not scaffold local schema fetchers that bypass `GenericCrudService`, `SchemaMetadataClient`, or Praxis runtime services for critical schema flows.
- Do not create frontend-only aliases for missing backend semantics, fields, filters, surfaces, actions, or capabilities.
- Do not author frontend-only semantic decisions, AI patch formats, field aliases, command vocabularies, or keyword routers to compensate for missing platform tools or canonical metadata.
- Do not enable remote config persistence when the backend contract and headers are not ready.
- Do not treat `praxis-ui-quickstart` as complete component catalog coverage.

## References

Load only what is needed:

- `references/host-bootstrap.md`: app bootstrap, providers, headers, API base, proxy/SSR notes, remote config persistence.
- `references/runtime-components.md`: table/form/CRUD/list first path, expansion runtimes, resourcePath/schema behavior.
- `references/validation-checklist.md`: build, smoke, browser, network, and integration gates for new hosts.
