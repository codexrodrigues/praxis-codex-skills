---
name: praxis-core-resource-runtime
description: Use when Codex must work with @praxisui/core resource runtime contracts: GenericCrudService, SchemaMetadataClient, ResourceDiscoveryService, /schemas/filtered consumption, actions, surfaces, capabilities, HATEOAS links, related-resource surfaces, option-source runtime, CRUD operation resolution, analytics schema contracts, stats request builders, or metadata-driven resource materialization.
---

# Praxis Core Resource Runtime

Use this skill for the `@praxisui/core` runtime path that turns canonical backend metadata into Angular resource behavior.

The backend remains the semantic owner. `@praxisui/core` should consume and materialize `praxis-metadata-starter` contracts such as `/schemas/filtered`, `/schemas/actions`, `/schemas/surfaces`, capabilities, HATEOAS links, `x-ui`, option sources, domain catalogs, and analytics projections. It must not invent local semantics to compensate for missing metadata.

When a backend contract is missing, contradictory, or weakly materialized, load the relevant `praxis-metadata-*` skill before patching Angular. Treat the Angular runtime as the consumer/projection layer, not as the place to invent backend metadata semantics.

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
- Treat `x-ui.resource.identity` as the canonical structured identity of a record. `keyField`, `titleField`, ordered `metadataFields`, and `displayLabelField` come from `@ApiResource(identity = @ResourceIdentity(...))`; Angular must not infer these roles from property names or split a concatenated `displayLabel`.
- For list/detail continuity, prefer the `resourceIdentity` already materialized on Praxis Table row/selection events and render it with `PraxisResourceIdentityComponent`. Re-fetching schema in the host, duplicating field-role config in CRUD metadata, or composing a screen-specific identifier header is a platform bypass.
- Preserve field-level `x-ui.presentation` when materializing identity parts. A visual key may inherit prefix/appearance from its field while title and metadata remain structurally governed by `x-ui.resource.identity`.

## No Keyword Routing

Do not route user intent, action selection, surface opening, tab selection, lookup selection, or analytics metrics by labels, regex, XML names, aliases, or keyword lists as the primary decision. Textual matching may rank candidates only after canonical resource/operation/surface/field scope is resolved from metadata and governed tools.

## Validation Guidance

Use focused specs for the touched service or model:

- resource discovery: `resource-discovery.service.spec.ts`
- schema metadata: `schema-metadata-client.spec.ts` and schema normalizer specs
- record identity: `resource-identity.model.spec.ts`, `resource-identity.component.spec.ts`, `generic-crud.service.spec.ts`, and the Table event spec that proves `resourceIdentity` propagation
- actions/surfaces: action/surface adapter and materializer specs
- CRUD operation resolution: `crud-operation-resolution.service.spec.ts`
- related resources: resolver and outlet specs
- analytics: analytics schema/request builder specs
- option sources: option-source model and `GenericCrudService` option tests

For public or cross-lib changes, also validate a direct consumer such as table, CRUD, dynamic-form, list, or charts.

## Companion Skills

- Use `praxis-metadata-schema-contracts` for backend `x-ui`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/domain`, schema refs, ETag, `X-Schema-Hash`, and OpenAPI operation resolution.
- Use `praxis-metadata-discovery-capabilities` for backend `/schemas/surfaces`, `/schemas/actions`, capabilities, `_links`, availability, related resources, export, stats, and cockpit discovery.
- Use `praxis-metadata-domain-option-sources` for `/schemas/domain`, `@DomainGovernance`, field access, `x-ui.optionSource`, entity lookup publication, and by-ids reload policy.
- Use `praxis-metadata-resource-baseline` for resource controllers/services, `ResourceMapper`, filters, HATEOAS envelopes, export, and stats.
- Use `praxis-core-runtime-contracts` for public API, tokens, providers, shared models, logging, and i18n.
- Use `praxis-core-surface-materialization` for action/surface adapter payloads, `surface.open` materialization, readUrl/submitUrl wiring, related-resource surfaces, and first-step payload audits.
- Use `praxis-core-global-action-payloads` for structured `GlobalActionRef`, payload validation, payloadExpr, UI schema, onResult, and command-string cleanup.
- Use `praxis-core-domain-governance-runtime` for domain catalog, domain knowledge, domain rules, governed simulations/publications/materializations, and config-starter semantic decision clients.
- Use `praxis-core-global-actions-metadata` for the broader global action and metadata-service umbrella.
- Use `praxis-core-i18n-resource-copy` when resource discovery availability, row action menu copy, or value presentation text changes.
- Use `praxis-core-providers-bootstrap` when resource runtime requires shared provider/token wiring.
- Use `praxis-dto-annotations` and `praxis-resource-entity-lookup-backend` when the backend metadata contract is missing or wrong.
- Use `praxis-rich-crud-screen-authoring` for standard CRUD screen composition on top of resolved core contracts.
