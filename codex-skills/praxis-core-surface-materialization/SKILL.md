---
name: praxis-core-surface-materialization
description: Use when Codex must implement, audit, or consume @praxisui/core resource action/surface materialization: ResourceDiscoveryService, capabilities, HATEOAS links, ResourceActionOpenAdapterService, ResourceSurfaceOpenAdapterService, SurfaceOpenMaterializerService, related-resource surfaces, schemaUrl/readUrl/submitUrl wiring, or table/form surface.open payloads.
---

# Praxis Core Surface Materialization

Use this skill for the first implementation step that turns canonical backend resource metadata into `surface.open` payloads and renderable Angular widgets.

This is a materialization skill, not a backend contract skill. `praxis-metadata-starter` owns resources, `/schemas/filtered`, `/schemas/actions`, `/schemas/surfaces`, capabilities, HATEOAS links, `x-ui`, and operation semantics. `@praxisui/core` consumes those contracts and projects them into stable Angular runtime payloads.

## Source Audit

Inspect the affected source before changing code or guidance:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/src/public-api.ts` when surface payload models, adapters, materializers, related-resource outlets, action editors, presets, or providers are exported or public consumption changes
- `projects/praxis-core/docs/schema-flow.md`
- `projects/praxis-core/docs/rfc-surface-open.md`
- `projects/praxis-core/src/lib/models/resource-discovery.model.ts`
- `projects/praxis-core/src/lib/models/surface-action.model.ts`
- `projects/praxis-core/src/lib/services/resource-discovery.service.ts`
- `projects/praxis-core/src/lib/services/resource-action-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.ts`
- `projects/praxis-core/src/lib/services/related-resource-surface-resolver.service.ts`
- `projects/praxis-core/src/lib/surfaces/praxis-related-resource-outlet.component.ts`
- `projects/praxis-core/src/lib/actions/editors/surface-open-action-editor.component.ts`
- `projects/praxis-core/src/lib/actions/surface-open-presets.ts`
- focused specs for the touched adapter/materializer/resolver and the direct consumer.

## Canonical Flow

Use the hypermedia-first path:

1. Start from a `RestApiResponse<T>` or explicit resource discovery context.
2. Resolve `_links.surfaces`, `_links.actions`, or `_links.capabilities` with `ResourceDiscoveryService`.
3. Preserve `resourceKey` as semantic identity and `resourcePath` as operational address.
4. Convert catalog items with the core adapter:
   - `ResourceSurfaceOpenAdapterService` for surfaces.
   - `ResourceActionOpenAdapterService` for typed workflow actions.
   - `RelatedResourceSurfaceResolverService` for child resource tables.
5. Execute through `GlobalActionRef { actionId: 'surface.open', payload }`.
6. Let `SurfaceOpenMaterializerService` hydrate item read projections when the surface response must become a renderable widget.

Do not reconstruct resource keys, schema URLs, submit URLs, read URLs, or action ids from labels, DOM text, route fragments, endpoint naming conventions, or command strings.

## Materialization Rules

- `resourceKey` identifies the resource semantically in action/surface/capability catalogs.
- `resourcePath` remains the base operational resource path. Do not append `/api`, `/filter`, `/{id}`, schema paths, action paths, or query strings to it.
- `SurfaceCatalogItem.path` plus `method` becomes `submitUrl`/`submitMethod` only for writable form surfaces.
- `ActionCatalogItem.requestSchemaUrl` becomes dynamic-form `schemaUrl`; `ActionCatalogItem.path`/`method` becomes submit target.
- Item-scoped actions and surfaces require either an explicit `resourceId` or a binding such as `payload.row.id`.
- Collection `VIEW` and `READ_PROJECTION` surfaces materialize to `praxis-table`; item `FORM`, `PARTIAL_FORM`, `VIEW`, and `READ_PROJECTION` surfaces materialize to `praxis-dynamic-form`.
- Related resources should use `surface.relatedResource` and resolver output rather than host-local parent/child filter conventions.
- Availability, denied operations, and permission-limited states must come from capabilities, catalog availability, or HATEOAS links, not frontend guesses.
- Preserve the materialization provenance carried in `payload.context.resource`, `payload.context.surface`, and `payload.context.action`. Consumers may display titles, subtitles, icons, shell state, and hydrated widget inputs, but must not replace the context with labels, generated ids, component names, selected row text, or host-local route state.
- `SurfaceOpenPayload.onResult` and `surface.result` are declarative continuation hooks for a governed result. They do not make the surface the primary owner of business state, resource identity, permission, or semantic decision. Route returned results through `GlobalActionRef`, composition links, or backend-confirmed actions; do not mutate host state from a surface result by local command parsing.
- `SurfaceOpenMaterializerService` may hydrate read projections and add materialization diagnostics such as `readUrl`, `dataShape`, `recordCount`, and presentation mode. Treat those as derived runtime evidence. Do not use a successful hydration, fallback form projection, or unavailable data diagnostic as proof that the backend authorized an edit, action, or alternate resource target.
- Treat materialized `widget.inputs`, `bindingOrder`, hydrated rows, fallback projections, and
  diagnostics as derived runtime payload for the opened surface. They are not a Page Builder
  `definition.inputs` authoring source, not a child component config editor result, and not a
  replacement for metadata/HATEOAS/capability catalogs. If a consumer wants to persist a reusable page
  or widget configuration, persist only the owning component's canonical config or the authored
  `GlobalActionRef`/composition link that can rematerialize the surface from canonical metadata.

## Aderence Inventory

Before adding a new adapter, field, input, or public type, classify the need:

- `ja-suportado-so-ux`: catalog/capability/link already exists; editor or host does not expose it.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: host manually builds URLs or strings that should use core adapters.
- `suportado-parcialmente`: core can express the surface, but materializer, binding, diagnostics, docs, or consumer proof is incomplete.
- `lacuna-real-de-contrato`: no backend catalog/capability/link or core payload field can express the operation.

Only `lacuna-real-de-contrato` justifies changing a canonical backend or public core contract.

## Validation

Use the smallest proof that exercises the changed flow:

- discovery plus adapter/materializer flow:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts --include=projects/praxis-core/src/lib/services/resource-action-open-adapter.service.spec.ts --include=projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.spec.ts --include=projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts
```

- related-resource surfaces and outlet registration:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/related-resource-surface-resolver.service.spec.ts --include=projects/praxis-core/src/lib/surfaces/praxis-related-resource-outlet.component.spec.ts --include=projects/praxis-core/src/lib/services/surface-outlet-registry.service.spec.ts
```

- `surface.open` authoring/editor presets:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/actions/editors/surface-open-action-editor.component.spec.ts --include=projects/praxis-core/src/lib/actions/surface-open-presets.spec.ts
```

- dynamic widget page surface materialization:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-record-surface-open.spec.ts
```

- CRUD consumer materialization when `schemaUrl`, `readUrl`, `submitUrl`, `submitMethod`, availability, or adapter payload handoff changes:

```sh
npm run ng -- test praxis-crud --watch=false --progress=false --include=projects/praxis-crud/src/lib/praxis-crud.component.spec.ts --include=projects/praxis-crud/src/lib/crud-launcher.service.spec.ts --include=projects/praxis-crud/src/lib/dynamic-form-dialog-host.component.spec.ts
```

- direct visual/runtime E2E proof only when rendered table/form/list behavior changes:

```sh
npx playwright test projects/praxis-table/test-dev/e2e/surface-open-funcionarios-demo.playwright.spec.ts
npx playwright test projects/praxis-dynamic-form/test-dev/e2e/surface-open-form-demo.playwright.spec.ts
npx playwright test projects/praxis-list/test-dev/e2e/surface-open-list-demo.playwright.spec.ts
```

For public or cross-lib changes, also run `npm run build:praxis-core` and a direct consumer build selected by actual imports (`praxis-table`, `praxis-crud`, `praxis-dynamic-form`, `praxis-list`, `praxis-dialog`, or `praxis-page-builder`).

For the first resolution step of an issue, also do a local audit: prove that generated payloads include the right `resourceKey`, `resourcePath`, `schemaUrl`, `readUrl`, `submitUrl`, `bindingOrder`, availability state, and user-visible failure behavior.

## Companion Skills

- Use `praxis-core-resource-runtime` for broader schema/resource runtime work.
- Use `praxis-core-global-action-payloads` when the surface is executed, edited, or validated as `GlobalActionRef`.
- Use `praxis-dialog-surface-global-actions` when the visual provider is dialog/drawer.
- Use `praxis-rich-crud-screen-authoring` when building a CRUD screen on top of resolved surfaces.
- Use `praxis-angular-public-api-governance` for exported contract changes.
