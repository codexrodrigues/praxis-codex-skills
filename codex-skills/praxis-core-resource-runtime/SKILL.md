---
name: praxis-core-resource-runtime
description: Use when Codex must work with @praxisui/core resource runtime contracts: GenericCrudService, SchemaMetadataClient, ResourceDiscoveryService, /schemas/filtered consumption, actions, surfaces, capabilities, HATEOAS links, related-resource surfaces, option-source runtime, CRUD operation resolution, analytics schema contracts, stats request builders, or metadata-driven resource materialization.
---

# Praxis Core Resource Runtime

Use this skill for the `@praxisui/core` runtime path that turns canonical backend metadata into Angular resource behavior.

The backend remains the semantic owner. `@praxisui/core` should consume and materialize `praxis-metadata-starter` contracts such as `/schemas/filtered`, `/schemas/actions`, `/schemas/surfaces`, capabilities, HATEOAS links, `x-ui`, option sources, domain catalogs, and analytics projections. It must not invent local semantics to compensate for missing metadata.

## Source Audit

Inspect the affected source before changing guidance or code:

- `projects/praxis-core/src/lib/services/generic-crud.service.ts`
- `projects/praxis-core/src/lib/schema/schema-metadata-client.ts`
- `projects/praxis-core/src/lib/services/resource-discovery.service.ts`
- `projects/praxis-core/src/lib/services/resource-action-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.ts`
- `projects/praxis-core/src/lib/services/surface-open-materializer.service.ts`
- `projects/praxis-core/src/lib/services/related-resource-surface-resolver.service.ts`
- `projects/praxis-core/src/lib/services/crud-operation-resolution.service.ts`
- `projects/praxis-core/src/lib/services/analytics-schema-contract.service.ts`
- `projects/praxis-core/src/lib/services/analytics-stats-request-builder.service.ts`
- `projects/praxis-core/src/lib/models/resource-discovery.model.ts`
- `projects/praxis-core/src/lib/models/surface-action.model.ts`
- `projects/praxis-core/src/lib/models/record-related-surface.model.ts`
- `projects/praxis-core/src/lib/models/option-source.model.ts`
- `projects/praxis-core/src/lib/models/query-context.model.ts`

Also read nearby specs for the exact behavior being changed. They are often the clearest contract for edge cases such as related resources, denied actions, schema operation resolution, and selected-value reload.

## Runtime Boundary

Use canonical metadata as the source:

- `/schemas/filtered`: structural request/response schema, field metadata, `x-ui`, option-source metadata, operation-specific schema shape
- `/schemas/actions` and action metadata: action discovery and availability
- `/schemas/surfaces` and surface metadata: surface discovery and materialization
- capabilities and HATEOAS links: availability and executable operation proof
- option-source descriptors and `/by-ids`: remote select, entity lookup, dependency filters, and selected-value rehydration
- domain catalog/knowledge/rules: AI grounding and explanation, not local routing by labels
- analytics metadata: stats/projection materialization, not chart-local metric vocabulary

If these are missing or contradictory, classify the gap and return to the canonical backend/config owner. Do not patch with host-only aliases, label matching, local endpoint maps, or Angular-only action routers.

## Common Decisions

- `resourcePath` is a base resource path, not an operation URL.
- Do not add `/api`, `/filter`, `/{id}`, query strings, schema paths, or submit endpoints to `resourcePath` when `GenericCrudService` can resolve them.
- Use operation-specific `schemaUrl`, `submitUrl`, and `submitMethod` only when a real action/surface/command contract requires them.
- Treat capabilities and `_links` as availability gates for optional operations such as export, create, edit, delete, duplicate, workflow actions, and surface opens.
- For related resources, prefer `RelatedResourceSurfaceResolverService` and the `surface.relatedResource` contract over local parent-child filters.
- For selected rows or widget outputs, check `PraxisSurfaceHostComponent`, materializer output wiring, row events, and capabilities before declaring a platform gap.

## No Keyword Routing

Do not route user intent, action selection, surface opening, tab selection, lookup selection, or analytics metrics by labels, regex, XML names, aliases, or keyword lists as the primary decision. Textual matching may rank candidates only after canonical resource/operation/surface/field scope is resolved from metadata and governed tools.

## Validation Guidance

Use focused specs for the touched service or model:

- resource discovery: `resource-discovery.service.spec.ts`
- schema metadata: `schema-metadata-client.spec.ts` and schema normalizer specs
- actions/surfaces: action/surface adapter and materializer specs
- CRUD operation resolution: `crud-operation-resolution.service.spec.ts`
- related resources: resolver and outlet specs
- analytics: analytics schema/request builder specs
- option sources: option-source model and `GenericCrudService` option tests

For public or cross-lib changes, also validate a direct consumer such as table, CRUD, dynamic-form, list, or charts.

## Companion Skills

- Use `praxis-core-runtime-contracts` for public API, tokens, providers, shared models, logging, and i18n.
- Use `praxis-dto-annotations` and `praxis-resource-entity-lookup-backend` when the backend metadata contract is missing or wrong.
- Use `praxis-rich-crud-screen-authoring` for standard CRUD screen composition on top of resolved core contracts.
