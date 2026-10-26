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
Use the transversal Angular family when the work is not a single component behavior:
`praxis-angular-validation-gates` for local validation planning, `praxis-angular-public-api-governance`
for public exports and package boundaries, `praxis-angular-i18n-governance` for framework-owned text,
and `praxis-angular-docs-playgrounds` for public docs, examples, landing pages, playgrounds, and
derived artifacts.

## Skill Discovery Policy

Do not depend on migration docs, quickstarts, or one orchestration skill to enumerate every relevant `praxis-*` skill explicitly.

When the environment exposes skill inventory or search:

1. Classify the task by domain first: `core`, `table`, `form`, `list`, `crud`, `dialog`, `tabs`, `stepper`, `expansion`, `files-upload`, `rich-content`, `page-builder`, `visual-builder`, `metadata-editor`, `fields`, `charts`, `settings`, `ai`, `docs`, `i18n`, `public-api`, or `validation`.
2. Search the Praxis family for the matching domain skills.
3. Load the narrow functional owner first, then add transversal skills such as validation, public-api, i18n, docs, or visual-product QA only when the scope actually requires them.

When the environment does not expose skill discovery:

1. Start from this gateway skill for Angular-host work.
2. Use the family manifest plus the companion-skill list below as the canonical routing table.
3. Prefer routing by surface/runtime owner rather than by remembering a static list from migration documentation.

For Ergon/Archon migrations, the orchestration skill still owns phase gating, but once UI/platform work is in scope the agent should discover and load the relevant `praxis-*` specializations even if the migration roadmap did not cite them by name.

## Canonical Sources

- `praxis-ui-angular` owns the public Angular packages, runtime providers, tokens, services, component APIs, and public Angular contracts.
- `praxis-metadata-starter` owns backend metadata semantics: `x-ui`, `/schemas/filtered`, surfaces, actions, capabilities, schema/domain discovery, and metadata-driven resource contracts.
- `praxis-config-starter` owns `/api/praxis/config/**`, `ui_user_config`, AI registry/config, headers, ETag, and remote configuration persistence.
- `praxis-ui-quickstart` is the operational adoption reference for a first Angular host. Use it to copy proven host patterns, not to redefine contracts.
- `praxisui.dev` and `praxis-ui-landing-page` publish docs and examples; they do not override the canonical backend or runtime owners.

When these disagree, prefer the canonical owner. Do not create local frontend conventions that bypass a missing backend/runtime contract.

For backend metadata contract work, load the relevant `praxis-metadata-*` skill before adding host adapters, local schema aliases, fallback endpoint maps, or frontend-only semantic conventions. Angular hosts should prove and consume canonical metadata, not become a parallel metadata layer.

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

## Corporate SESSION Transport

For Quickstart-backed corporate hosts, inspect the backend AuthController/CSRF
contract and Hero's `corporate-session-*`, `corporate-context` and
`docs/engineering/corporate-session-journey.md` before adding another auth adapter.
Core already owns context/choices/CAS; cookie identity and transport belong to the
host. Keep demo personas and local page persistence separate from server grants.

Confirm login through GET `/auth/session`, consume its raw `X-XSRF-TOKEN` response
header and send it only on required mutations. Keep passwords/tokens out of storage,
logs and diagnostics. Serialize auth exchanges: discarding a stale callback cannot
undo a browser's late Set-Cookie. Fence context responses by session generation;
403/503 context failures do not mean logout. Preserve uncertain logout explicitly.

Scope credentials/CSRF to the exact configured origin and canonical route boundaries;
remove synthetic persona headers while preserving Core-confirmed context headers and
ETag/preconditions. Inspect the effective Angular HttpBackend: XHR may ignore a
redirect option. Reject credential redirects before another destination is contacted;
when needed, use a host-private FetchBackend only for corporate paths and preserve
legacy XHR/progress. Do not switch the whole application transport by convenience.

Proxy `/auth` without spoofing an allowed Origin, weakening TLS or rewriting cookie
security. The backend must allow the real origin. Test session restore, raw CSRF,
logout uncertainty, response races, exact-origin rejection and blocked redirects.
Browser responses controlled by tests prove consumer behavior, not real SESSION,
cross-site cookies, CORS or deployed-backend readiness. Record those limits and reuse
unchanged backend evidence instead of requiring another Neon campaign for UI work.

For page authoring hosts, put EnterpriseRuntimeContextService, UiLayoutLifecycleService
and the host page transport in one explicit corporate ancestor scope shared by entry,
editor and published reader. A component-scoped context paired with a root lifecycle
client creates different snapshots. Keep the demo's global headers out of this scope.
Invalidate that shared context on every SESSION generation change, not only logout;
fence reads and writes by both context revision and captured session generation.
After 401/new login, ready() must not reuse the previous actor's snapshot.

Use Config creationKey receipts and the by-creation-key reconciliation read for a
lost creation response; a 404 is not permission to recreate an in-flight command.
Keep revision, assignment, freeze, submit, approve and publish explicit, with the
server's current strong validators. Published/catalog HTTP ETags are weak read
receipts and must never be required or reused as strong draft/head write validators.
Do not report draft creation as successful SaveAs publication. Materialize only the
host-admitted document profile; a lifecycle state receipt is not an immutable review
preview or proof that a page renderer is wired. Keep those acceptance scopes separate.

For published-page copies, inspect Config's `PageRuntimeReadService` and the
host transport/editor together. Use the server-provided `copySource` from the
published read, correlated with that page and its authorized head. Send it to
creation with a new creationKey; let Config allocate the new page/draft/route
identity and rematerialize the source. Do not clone JSON or reuse source/menu
identities on the client. The copy is a draft with no inherited navigation
binding: explicitly select its destination group and publish through lifecycle.
On authorization denial, clear displayed protected content and fence further
writes. A reread may discard unsaved edits; this UI fence neither repairs stored
configuration nor grants access. Test copied content, distinct identity, empty
initial navigation and the denial path separately from real publication proof.

Treat navigation groups as a separate governed aggregate: publish the referenced
group before publishing a page binding to it. Consume the SDK's runtime navigation
in that same corporate provider scope; do not synthesize menus from the page
catalog. Inspect Config P3-A/P3-B and `QuickstartPageConfiguration`/`QuickstartPageDocuments`:
the native groups baseline is empty, not a clone of the published groups head.
A genuine head404 selects the existing first-publication precondition; an existing
head requires the complete admitted groups document and current strong CAS before
editing, or reuse of its groups without rewriting the aggregate. Never replace the
full groups document with a paginated/visibility-filtered navigation projection.
Prove persistent menu/route behavior separately from draft save and group creation.

## Governed Pages Host Adoption Protocol (`P4` / `P5-A` / `P5-B` / `P5-C` / `P5-D`)

When a host adopts governed dynamic pages (`praxis-dynamic-page`), follow this
10-step protocol without inventing parallel storage, routes, or menu registries:

1. **Separate operating modes**: use `PraxisPageSaveAsComponent` + `PraxisPageCopyActionComponent` (`@praxisui/page-builder`) with a Web Lock-protected local repository for browser-local laboratory flows (`P5-A`), and `GovernedPageWorkflowController` + `GovernedPageNavigationController` + `createCorporateGovernedPagePersistenceAdapter` + `/api/praxis/config/pages/**` + `/api/praxis/config/ui-layouts/**` for corporate governed flows (`P4` / `P5-B`).
2. **Enforce volatile child persistence**: render child `praxis-dynamic-form` and `praxis-table` widgets inside governed pages with `configPersistenceStrategy: 'volatile'` and configuration solely in `widget.definition.inputs.config`.
3. **Admit creation sources on the server**: create corporate pages via `POST /api/praxis/config/pages` using an admitted `registered-native` seed or a pinned `published-page` `copySource` (`pageId`, `releaseId`, `revisionId`) correlated with `GET /api/praxis/config/pages/{pageId}/published`.
4. **Reconcile timeouts by creation key**: on network timeout during `POST /api/praxis/config/pages`, query `GET /api/praxis/config/pages/by-creation-key?creationKey=...` with the same `creationKey` before retrying.
5. **Preserve childSources and fixed envelopes**: when saving a revision (`POST /drafts/{draftId}/revisions`), declare `childSources` only for newly added widget keys and keep fixed binding envelopes (`resourcePath`, `mode`, `readOnly`, `operation`) immutable per `widget.key`.
6. **Govern navigation groups and icons**: edit menu bindings (`navigationBindings[]`) in `praxis.dynamic-page.editor` and shared groups (`groups[]`) in `praxis.navigation-groups.editor` using only the host's admitted Material icon catalog (`GOVERNED_PAGE_DEFAULT_ALLOWED_ICONS` / `QuickstartPageConfiguration.ALLOWED_ICONS`).
7. **Complete the release lifecycle**: run `draft -> revision -> assignment -> freeze -> submit -> approve -> publish` (plus `rollback` and `withdraw`) with strong `If-Match` preconditions and distinct author/reviewer/publisher gates where required.
8. **Resolve from the single release head**: render the page catalog (`GET /api/praxis/config/pages`), stable route `/pages/:pageId` (`GET /api/praxis/config/pages/{pageId}/published`), and runtime menu (`GET /api/praxis/runtime/navigation`) from the same active head without falling back to `ui_user_config` or drafts.
9. **Fence session and context epochs**: require authenticated `SESSION`, raw `X-CSRF-TOKEN` on mutations, and confirmed `EnterpriseRuntimeContextService` (`X-Praxis-Context-Version`), invalidating in-flight requests and caches on logout or context switch (`A -> B -> A`).
10. **Migrate legacy pages explicitly**: import legacy `ui_user_config` pages (`LEGACY_PUBLISHED_PAGE_STORAGE_PREFIX`) through `inspectLegacyPublishedPagePayload` and `GovernedPageWorkflowController.importLegacyPublishedPage` (`P5-D`) rather than reading legacy snapshots at runtime.

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
   - Pin Angular framework packages, including compiler/compiler-cli, to one exact compatible patch within that cohort. Pin Material/CDK together and CLI/build together to their own exact compatible patches. Cross-cohort patch equality is not required: preserve the host's accepted release line and cohort checks, and validate the published package peer ranges and installed closure. Do not change another cohort solely to adopt a new Praxis UI train.
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
- `praxis-angular-validation-gates`: focused local validation, consumer builds, Playwright/screenshot QA, registry/docs gates, release preflight, and GitHub Actions boundaries.
- `praxis-angular-agents-governance`: `projects/*/AGENTS.md` inventory, missing local guidance, skill/platform drift, and follow-up routing for local governance gaps.
- `praxis-angular-public-api-governance`: `@praxisui/*` public exports, barrel ownership, cross-lib edges, direct-consumer validation, and derived public API artifacts.
- `praxis-angular-i18n-governance`: internal framework text, authoring chrome, locale catalogs, `PraxisI18nService`, hardcoded text audits, and PT-BR/en-US coverage.
- `praxis-angular-docs-playgrounds`: public docs, component docs manifests, examples, AI recipes, landing pages, playgrounds, sitemap, and docs validation.
- `praxis-landing-public-docs-contracts`: public landing/docs narrative that projects metadata, config, Angular runtime, quickstart, and HTTP evidence without redefining canonical contracts.
- `praxis-landing-registries-sitemap-playgrounds`: landing guide registries, sitemap, LLM files, dynamic examples, playgrounds, generated docs, and publication validation.
- `praxis-core-runtime-contracts`: core public API, tokens, providers, models, i18n, logging, and shared services.
- `praxis-core-resource-runtime`: core schema/resource discovery, actions, surfaces, capabilities, option sources, related resources, and analytics materialization.
- `praxis-metadata-schema-contracts`: backend `x-ui`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/domain`, schema refs, ETag, `X-Schema-Hash`, and operation-aware schema resolution.
- `praxis-metadata-resource-baseline`: resource-oriented controllers/services, `ResourceMapper`, filters, HATEOAS envelopes, export, stats, and canonical CRUD baseline.
- `praxis-metadata-discovery-capabilities`: backend surfaces, actions, capabilities, `_links`, availability, related-resource surfaces, export, stats, and cockpit discovery.
- `praxis-metadata-domain-option-sources`: domain governance, field access, option sources, `RESOURCE_ENTITY`, lookup/by-ids contracts, and semantic metadata review.
- `praxis-config-runtime-persistence`: `/api/praxis/config/ui`, `ui_user_config`, headers, ETag, tenant/user/environment scope, and `/api/praxis/runtime/**`.
- `praxis-config-ai-registry-manifests`: `ai_registry`, templates, component definitions, executable manifests, validators, compilers, and registry ingestion.
- `praxis-config-api-metadata-grounding`: `api_metadata`, AI context, RAG, Project Knowledge, API Catalog Q&A, and resource candidate grounding.
- `praxis-config-agentic-authoring-streaming`: backend semantic intent, declared tools, preview/apply, turn streams, quick replies, warnings, diagnostics, replay, and cancel.
- `praxis-config-domain-decisions`: domain rules, domain knowledge, simulations, publications, materializations, decision diagnostics, timelines, and derived projections.
- `praxis-api-quickstart-operational-proof`: reference host proof for metadata/config starter integration, Maven versions, and ownership routing.
- `praxis-api-quickstart-security-config`: quickstart CORS/CSRF/origin/read-open policy for `/schemas/**`, `/api/praxis/config/**`, and runtime endpoints.
- `praxis-api-quickstart-domain-pilots`: quickstart `ApiPaths`, pilot resources, DTOs, filters, option sources, stats, workflow actions, and example domains.
- `praxis-api-quickstart-cockpit-http-validation`: cockpit docs, verification scripts, HTTP examples, domain catalog/rule/knowledge smokes, and published-host evidence.
- `praxis-http-examples-corpus-manifest`: executable HTTP corpus manifest, flags, source-of-truth claims, payload references, and response-shape hints.
- `praxis-http-examples-contract-surfaces`: HTTP examples for metadata/config contracts, headers, Origin, ETag, schemas, capabilities, AI/context, and domain decisions.
- `praxis-http-examples-llm-smoke`: LLM-facing operational surface, safe-first lanes, bootstrap docs, and smoke validation.
- `praxis-core-composition-runtime`: dynamic widget pages, composition links, widget events, surface hosts, and runtime observations.
- `praxis-core-providers-bootstrap`: shared core providers, tokens, global config, API URL, loading, icons, field selectors, collection export, and registry bootstrap.
- `praxis-core-widget-observations`: dynamic widget contracts, widget pages, widget events, runtime observations, observation registry, diagnostics, and redaction proof.
- `praxis-core-logging-observability`: logging providers, logger sinks, telemetry payloads, error normalization, redaction, throttling, and observability alerts.
- `praxis-core-i18n-resource-copy`: shared `PraxisI18nService`, i18n providers, resource-discovery messages, value presentation, and PT-BR/en-US framework copy.
- `praxis-core-global-actions-metadata`: global actions, action catalogs/providers, payload validation, surface open presets, component metadata registry, and metadata services.
- `praxis-table-runtime-data`: table runtime umbrella for data modes, renderers, selection, export, analytics, and validation.
- `praxis-table-data-source-precedence`: local/remote source precedence, `resourcePath`, `queryContext`, local pipeline, persisted connections, and apply-plan diagnostics.
- `praxis-table-selection-export-runtime`: selected rows/ids, bulk state, export scopes, collection export, and selected-record context.
- `praxis-table-analytics-stats-runtime`: analytic-table projections, stats requests, fallback rows, and dashboard table views.
- `praxis-table-renderer-state-diagnostics`: renderers, formatting, empty/loading/error states, i18n, diagnostics, and runtime observations.
- `praxis-table-filter-actions`: table filters, dynamic filter payloads, toolbar/row/bulk actions, global actions, CRUD actions, and export grounding.
- `praxis-table-authoring-settings`: table Settings Panel, config editors, columns, rules, filters, actions, CRUD integration, and round-trip.
- `praxis-table-ai-validation`: table AI manifests, component edit plans, runtime operations, context packs, registry ingestion, and assistant E2E.
- `praxis-table-rule-effects-runtime`: `@praxisui/table-rule-builder` visual effects panel, `RuleEffectDefinition`, effect registry, presets, labels, and conversion utilities.
- `praxis-table-rule-animation-presets`: semantic table rule animations, preset aliases, fail-closed normalization, reduced-motion, and preview class policy.
- `praxis-table-rule-table-integration`: table-rule-builder effects embedded in `@praxisui/table`, renderer placement, `effects[]` normalization, and Settings Panel round-trip.
- `praxis-table-rule-ai-validation`: table-rule-builder AI manifest, effect operations, destructive confirmation, table delegation, and registry validation.
- `praxis-form-runtime-submit`: dynamic-form runtime modes, schema metadata, submit payload, local/transient fields, hooks, actions, and validation.
- `praxis-form-schema-runtime-modes`: dynamic-form `resourcePath`, `schemaUrl`, `readUrl`, `submitUrl`, `submitMethod`, create/edit/view, `initialValue`, metadata hot updates, and runtime reconciliation.
- `praxis-form-submit-payload-pipeline`: dynamic-form submit normalization, date arrays, local/transient fields, `submitPolicy`, entity lookup payloads, dirty filtering, and nested arrays.
- `praxis-form-actions-hooks-runtime`: dynamic-form actions, hooks, global action refs, surface open payloads, shortcuts, and action/hook editor round-trip.
- `praxis-form-editor-document-roundtrip`: `DynamicFormAuthoringDocument`, bindings, context snapshots, Settings Panel apply/save/reset, diagnostics, and editor reopen semantics.
- `praxis-form-layout-canvas`: dynamic-form layout policy, schema-driven layout, visual blocks, canvas, and layout validation.
- `praxis-form-authoring-settings`: dynamic-form config editors, Settings Panel, authoring document, apply/save/reset, and round-trip.
- `praxis-form-ai-rules-validation`: dynamic-form AI manifests, rules, diagnostics, context packs, registry ingestion, and assistant validation.
- `praxis-list-runtime-data`: list/card/tile runtime, local versus remote precedence, `resourcePath`, query context, selection, actions, templating, skin, and export.
- `praxis-list-authoring-settings`: list config editor, widget editor, JSON editor, Settings Panel round-trip, `ListAuthoringDocument`, and i18n chrome.
- `praxis-list-ai-validation`: list AI manifest, capabilities, context pack, adapter, component edit plans, registry ingestion, and declared-only warnings.
- `praxis-list-docs-evidence`: list README/json-api/docs manifest, living examples, executive evidence, landing/playground sync, and status table honesty.
- `praxis-metadata-editor-renderer-coverage`: `FieldMetadataEditorComponent`, `DynamicEditorRendererComponent`, `EditorProperty[]` configs, inline editor coverage, visual versus JSON-only gaps, and dynamic-fields parity.
- `praxis-metadata-editor-cascade-normalization`: cascade manager, `optionSource` dependency shapes, backend `x-ui` preservation, schema normalization, form factory, contextual validators, and remote-source editor coverage.
- `praxis-metadata-editor-consumer-bridges`: dynamic-form, table, manual-form, and Page Builder bridges that host `FieldMetadataEditorComponent`, `DynamicEditorRendererComponent`, or `CascadeManagerTabComponent`.
- `praxis-metadata-editor-ai-validation`: metadata-editor authoring manifest, capabilities, context packs, AI registry projection, and declared operation safety.
- `praxis-manual-form-runtime-bridge`: manual-form runtime umbrella for host `FormGroup` adoption, field autodetection, autosave, toolbar, persistence, and metadata-editor bridge.
- `praxis-manual-form-field-detection-instance`: projected `pdx-*` detection, `ManualFormInstance`, seed creation, metadata streams, bound components, `usePathNames`, and field key resolution.
- `praxis-manual-form-autosave-persistence`: `saveDraft`, `resetToSeed`, `ASYNC_CONFIG_STORAGE`, persistence options, storage keys, debounce, SSR-safe storage, and draft reload.
- `praxis-manual-form-toolbar-metadata-bridge`: `enableCustomization`, floating field toolbar, `pdxManualEdit`, Settings Panel, lazy metadata-editor bridge, and JSON Merge Patch diagnostics.
- `praxis-manual-form-ai-authoring`: manual-form authoring umbrella for config editor, Settings Panel, authoring manifest, AI capabilities, formRules, autosave/toolbar operations, and registry/docs validation.
- `praxis-manual-form-rules-agentic`: manual-form component edit plans, `formRules`, `formRulesState`, JSON Logic, agentic turn flow, context packs, governed rule handoff, and registry projection.
- `praxis-editorial-forms-runtime`: editorial-form runtime umbrella for journeys, snapshots, fallback, presentation, diagnostics, operational events, renderers, i18n, and labs.
- `praxis-editorial-forms-journey-snapshot-runtime`: `EditorialRuntimeInput`, solution/instance/context merge, journey and step resolution, presets, overrides, block provenance, runtime snapshots, and `snapshotChange`.
- `praxis-editorial-forms-presentation-diagnostics`: `solution.presentation`, fallback modes, diagnostics, operational events, theme CSS vars, stepper behavior, unsupported presentation keys, and runtime health.
- `praxis-editorial-forms-data-collection-adapters`: `dataCollection` blocks, adapter registry, optional dynamic-form adapter, config lookup, readiness diagnostics, adapter events, and `runtimeContext.formData`.
- `praxis-editorial-forms-adapters-ai`: editorial adapters/AI umbrella for data block adapters, optional dynamic-form adapter, AI manifest, field binding, and registry validation.
- `praxis-editorial-forms-agentic-authoring`: `PRAXIS_EDITORIAL_FORMS_AUTHORING_MANIFEST`, component edit plans, snapshot/fallback/presentation operations, adapter binding, data block add/remove, component metadata, docs, labs, and registry projection.
- `praxis-crud-runtime-openmodes`: CRUD runtime, `CrudLauncherService`, route/modal/drawer open modes, and table/form orchestration.
- `praxis-crud-drawer-adapter-contract`: lightweight drawer adapter entrypoint, host drawer parity, and drawer result propagation.
- `praxis-crud-dialog-form-host-lifecycle`: modal/drawer dynamic-form host lifecycle, save/delete/close results, and refresh-after-save/delete.
- `praxis-crud-ai-authoring`: CRUD authoring document, metadata editor, widget config editor, authoring manifest, capabilities, permissions, and child-operation delegation.
- `praxis-dialog-overlay-runtime`: Dialog service API, overlay lifecycle, tag mode, presets, focus, accessibility, sizing, positioning, and close policy.
- `praxis-dialog-global-actions-ai`: Dialog global actions, component/template registries, global presets from config, authoring manifest, and registry validation.
- `praxis-dialog-surface-global-actions`: dialog-backed surface materialization, `GLOBAL_SURFACE_SERVICE`, `SURFACE_DRAWER_BRIDGE`, and surface result forwarding.
- `praxis-tabs-runtime-authoring`: `@praxisui/tabs` group/nav runtime, `tabsId`, selected index, quick setup, Settings Panel authoring, `renderBody`, lazy loading, and widget events.
- `praxis-stepper-wizard-runtime`: `@praxisui/stepper` and `PraxisWizardFormComponent` runtime, `stepperId`, dynamic-form steps, canonical `resourcePath`, validation, wizard adapter, and widget events.
- `praxis-expansion-runtime-panels`: `@praxisui/expansion` metadata-first panels, defaults providers, `expansionId`, lazy content, panel events, registry metadata, and widget events.
- `praxis-navigation-containers-ai-validation`: AI authoring, manifests, context packs, registry projection, docs, and validation for tabs, stepper, wizard, and expansion containers.
- `praxis-navigation-container-composition-events`: nested widget event paths, dynamic page embedding, external tab bodies, lazy container materialization, and composition links across navigation containers.
- `praxis-stepper-wizard-orchestration`: dynamic-form steps, validation, server validation, wizard adapter, submit/completed/customAction outputs, preferences, and host workflow boundaries.
- `praxis-navigation-agentic-registry`: AI adapters, agentic turn flows, context packs, registry ingestion, generated docs, and cross-container authoring consistency.
- `praxis-files-upload-runtime`: `@praxisui/files-upload` direct/presign/auto runtime, `filesUploadId`, `baseUrl`, full/compact UX, validators, upload states, i18n, and events.
- `praxis-files-upload-backend-contract`: files API base URL, direct/bulk/presign endpoints, multipart fields, backend envelopes, quotas, rate limits, headers, and error codes.
- `praxis-files-upload-form-field`: `pdx-material-files-upload`, ControlValueAccessor behavior, `valueMode`, dynamic-form field integration, and submit payload shape.
- `praxis-files-upload-ai-validation`: files-upload authoring manifest, AI adapter, context pack, registry projection, endpoint/security operations, and assistant validation.
- `praxis-rich-content-runtime`: `@praxisui/rich-content` renderer, `RichContentDocument`, semantic nodes, context bindings, host-mediated actions, presets, and metadata provider.
- `praxis-rich-content-authoring-settings`: rich-content config editor, guided editing, preview, advanced JSON, presets, i18n, and Settings Panel round-trip.
- `praxis-rich-content-integration-adapters`: rich-content integration across Page Builder, stepper, editorial forms, dynamic forms, metadata previews, and migration from legacy editorial blocks.
- `praxis-rich-content-ai-security-validation`: rich-content AI manifest, validator, safe URL/style policy, JsonLogic fail-safe behavior, registry, docs, and assistant validation.
- `praxis-cron-builder-runtime`: `@praxisui/cron-builder` runtime, CRON editing, presets, CVA, validation, humanized descriptions, timezone/locale preview, and metadata provider.
- `praxis-cron-schedule-authoring`: canonical `ScheduleAuthoringConfig`, recurrence intent, CRON dialects, normalization, compile, diagnostics, and preview contracts.
- `praxis-cron-builder-form-field`: cron-builder integration with dynamic-form/dynamic-fields metadata, value shape, submit payload, and host form wiring.
- `praxis-cron-builder-ai-validation`: cron-builder AI authoring manifest, schedule operations, read-only validate/preview, diagnostics, context packs, and registry validation.
- `praxis-fields-runtime-loader`: dynamic-fields loader, component registry, selector mapping, hot metadata, and runtime coverage.
- `praxis-fields-option-sources`: optionSource, async/searchable selects, entity lookup, by-ids reload, and dependency filters.
- `praxis-fields-editorial-discovery`: dynamic-fields editorial descriptors, catalogs, i18n, and metadata-editor/tooling discovery.
- `praxis-fields-ai-canvas-validation`: dynamic-fields AI manifest, control profiles, catalog ingestion, recipes, and canvas validation.
- `praxis-fields-control-profile-ai`: dynamic-fields per-control AI profiles, capability catalogs, profile validators, and registry projection.
- `praxis-fields-inline-overlay-runtime`: inline filter controls, overlay apply/cancel/clear semantics, compact value shapes, surface tokens, and toolbar promotion boundaries.
- `praxis-fields-text-number-time-controls`: text, phone, regional document, numeric, currency, range, date, time, period, and temporal field semantics.
- `praxis-fields-selection-lookup-controls`: select, autocomplete, async select, entity lookup, chips, list, tree, option identity, and selection value semantics.
- `praxis-charts-runtime-data`: `@praxisui/charts` runtime, `x-ui.chart`, `chartDocument`, ECharts adapter boundary, analytics adapters, stats execution, `queryContext`, drilldown, and cross-filter.
- `praxis-charts-authoring-settings`: chart config editor, widget config editor, Settings Panel, apply/save/reset/reopen, governed resource/field/target catalogs, and chart editor round-trip.
- `praxis-charts-ai-validation`: chart AI manifest, editable targets, validators, handler contracts, registry ingestion, and component edit-plan validation.
- `praxis-charts-echarts-engine-boundary`: ECharts adapter lifecycle, option builder, engine provider, click event mapping, raw option safety, and micro-visualization boundary.
- `praxis-charts-analytics-interactions`: stats contracts, analytics projections, `queryContext`, drilldown, cross-filter, point selection, and dashboard chart interactions.
- `praxis-charts-authoring-catalogs`: chart config editor catalogs, `availableResources`, `availableFields`, `availableTargets`, preview mapper, and Settings Panel round-trip.
- `praxis-charts-ai-handler-contracts`: chart manifest operation schemas, validators, handler contracts, edit plans, and generated AI registry assets.
- `praxis-dashboard-analytics`: backend dashboard/analytics resources, `/stats/*`, `@UiAnalytics`, aggregate resources, custom dashboard catalog/summary endpoints, capabilities, and option sources.
- `praxis-page-builder-composition`: Page Builder runtime composition, component palette, `WidgetPageDefinition`, canvas, `page.composition.links`, connection graph, nested ports, and dynamic page materialization.
- `praxis-page-builder-authoring`: Page Builder page config editors, widget shell editor, Settings Panel bridge, child config editor hosting, apply/save/reset/reopen, and visual/textual round-trip.
- `praxis-page-builder-ai-agentic`: Page Builder agentic authoring, UI composition plans, capability catalogs, streaming turn flow, runtime observations, preview/apply, and AI registry gates.
- `praxis-visual-builder-rules`: Visual Builder umbrella skill for JSON Logic rules, graph validation, field schemas, context variables, property effects, templates, AI manifest, and round-trip.
- `praxis-visual-builder-graph-runtime`: `RuleBuilderState`, `RuleNode`, node IDs, root nodes, child edge IDs, registry integrity, selection, undo/redo, validation errors, orphan/cycle checks, and focused graph UI validation.
- `praxis-visual-builder-jsonlogic-roundtrip`: JSON Logic import/export, `currentJSON`, condition parsing, `FormLayoutRule` bridge, unsupported context/function operands, legacy expression safeguards, and semantic round-trip proof.
- `praxis-visual-builder-schemas-templates`: field schemas, target/property schemas, operator catalogs, context scopes/variables, collection validators, templates, and template-compatible rule nodes.
- `praxis-visual-builder-ai-validation`: visual-builder AI authoring manifest, adapter, capabilities, editable targets, operation validators, examples, registry ingestion, and `dsl.roundTrip.validate`.
- `praxis-settings-panel-shell`: Settings Panel shell, drawer protocol, bridge separation, footer actions, and sizing.
- `praxis-settings-roundtrip-authoring`: visual editor apply/save/reset/reopen, persistence, and runtime consume validation.
- `praxis-settings-global-config`: Global Config Editor, effective config, save/clear, and remote persistence.
- `praxis-settings-ai-i18n-validation`: Settings Panel AI manifest, adapter, context pack, diagnostics, and i18n coverage.
- `praxis-ai-assistant-runtime`: `@praxisui/ai` assistant shell/client/runtime state, quick replies, diagnostics, previews, and apply payloads.
- `praxis-ai-shell-session-context`: assistant shell, dock, session registry, session host, and safe context snapshots.
- `praxis-ai-composer-attachments-quick-replies`: composer actions, quick replies, clarifications, attachments, message replay, and voice input.
- `praxis-ai-turn-orchestration-transport`: assistant turn controllers, lifecycle phases, runtime observations, stream transport, and terminal results.
- `praxis-ai-backend-config-contracts`: AI endpoint resolution, backend config tokens, headers, provider endpoints, manifest endpoints, and Praxis Config boundary.
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


## Demonstrative host budgets and lazy routes

Inspect the host's actual bootstrap and dependency graph before changing build
configuration. Pages may already be lazy while eager metadata/provider imports
retain the entire catalog. Prefer the existing provider and injector contracts;
keep application singletons, root-consumed options and required dictionaries at
their correct lifetime. Use `praxis-core-providers-bootstrap` for the scope audit.
Do not raise budgets, remove deliberately published exports, or switch source
aliases to packaged libraries without measuring and preserving style coverage.
Report initial assets separately from the catalog fetched on first navigation.

When moving an existing route collection under a persistent lazy parent, preserve
URLs, precedence, redirects, feature gates and dynamic CRUD registration/removal.
Use public Router matching and the existing resource registry; never manipulate
private loaded-route caches. Exact URL segment matching is route admission, not
primary user-intent routing. Preserve multi-segment resource keys.

Shared action routes can reuse the same page instance across different resources.
A page that captures `ActivatedRoute.snapshot` once may retain the old resource,
id, formId or return target. Materialize current paramMap, queryParamMap and data
streams, including query removal. Prove navigation with the real host page and the
same instance; a probe with fresh snapshot getters can mask this defect. Validate
normal production budgets, direct navigation/refresh, editor round-trips and
panel context after the final productive change.
