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
- `projects/praxis-core/docs/schema-flow.md`
- `projects/praxis-core/docs/rfc-surface-open.md`
- `projects/praxis-core/src/lib/models/resource-discovery.model.ts`
- `projects/praxis-core/src/lib/models/surface-action.model.ts`
- `projects/praxis-core/src/lib/services/resource-discovery.service.ts`
- `projects/praxis-core/src/lib/services/resource-action-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.ts`
- `projects/praxis-core/src/lib/services/related-resource-surface-resolver.service.ts`
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

## Aderence Inventory

Before adding a new adapter, field, input, or public type, classify the need:

- `ja-suportado-so-ux`: catalog/capability/link already exists; editor or host does not expose it.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: host manually builds URLs or strings that should use core adapters.
- `suportado-parcialmente`: core can express the surface, but materializer, binding, diagnostics, docs, or consumer proof is incomplete.
- `lacuna-real-de-contrato`: no backend catalog/capability/link or core payload field can express the operation.

Only `lacuna-real-de-contrato` justifies changing a canonical backend or public core contract.

## Validation

Use the smallest proof that exercises the changed flow:

- `resource-discovery.service.spec.ts`
- `resource-action-open-adapter.service.spec.ts`
- `resource-surface-open-adapter.service.spec.ts`
- `surface-open-materializer.service.spec.ts`
- `related-resource-surface-resolver.service.spec.ts`
- direct consumer spec/build for table, CRUD, dialog, dynamic-form, page-builder, or host app when the payload is materialized there.

For the first resolution step of an issue, also do a local audit: prove that generated payloads include the right `resourceKey`, `resourcePath`, `schemaUrl`, `readUrl`, `submitUrl`, `bindingOrder`, availability state, and user-visible failure behavior.

## Companion Skills

- Use `praxis-core-resource-runtime` for broader schema/resource runtime work.
- Use `praxis-core-global-action-payloads` when the surface is executed, edited, or validated as `GlobalActionRef`.
- Use `praxis-dialog-surface-global-actions` when the visual provider is dialog/drawer.
- Use `praxis-rich-crud-screen-authoring` when building a CRUD screen on top of resolved surfaces.
- Use `praxis-angular-public-api-governance` for exported contract changes.
