---
name: praxis-metadata-discovery-capabilities
description: "Use when Codex must work on praxis-metadata-starter semantic discovery: /schemas/surfaces, /schemas/actions, resource/item capabilities, @UiSurface, @WorkflowAction, availability contexts, ResourceStateSnapshot, relatedResource surfaces, collection export, stats capabilities, HATEOAS operation availability, or cockpit discovery."
---

# Praxis Metadata Discovery Capabilities

Use this skill for semantic discovery and availability in `praxis-metadata-starter`. Surfaces, actions, and capabilities are discovery and availability contracts over real resource operations; they must not become alternate schemas or local UI command vocabularies.

## Source Audit

Inspect the owner before editing:

- `praxis-metadata-starter/AGENTS.md`
- `src/main/java/org/praxisplatform/uischema/surface/**`
- `src/main/java/org/praxisplatform/uischema/action/**`
- `src/main/java/org/praxisplatform/uischema/capability/**`
- `src/main/java/org/praxisplatform/uischema/controller/docs/SurfaceCatalogController.java`
- `src/main/java/org/praxisplatform/uischema/controller/docs/ActionCatalogController.java`
- `src/main/java/org/praxisplatform/uischema/controller/base/AbstractResourceQueryController.java`
- `src/main/java/org/praxisplatform/uischema/rest/response/RestApiResponse.java`
- `src/main/java/org/praxisplatform/uischema/controller/cockpit/PraxisCockpitController.java`
- focused surface/action/capability/cockpit tests

## Canonical Boundary

`@UiSurface` describes semantic UI surfaces over real operations. `@WorkflowAction` describes explicit business commands. Do not combine them on the same method without reviewing validation mode and conflict semantics.

`GET /{resource}/capabilities` and `GET /{resource}/{id}/capabilities` aggregate canonical operations, surfaces, actions, export, stats, and availability; they are snapshots, not a second source of schema truth.

Availability should use contextual resolvers and shared `ResourceStateSnapshot` rather than repeated N+1 resource loads.

`resourceKey` is the stable semantic resource identity for discovery aggregation; `resourcePath`, action/surface `path`, HTTP method, schema URLs, and `_links` are operational execution evidence. Do not make URL shape the semantic identity, and do not hide a missing `resourceKey` with host-local aliases.

`capabilities.operations` governs whether an operation exists and is currently available; `_links` expose the executable hypermedia target. They must remain coherent. If a capability is denied, stale, missing, or contradicted by `_links`, treat it as a contract defect to fix in metadata/capability/HATEOAS generation, not as permission for Angular or agents to infer availability from labels, buttons, or route patterns.

## Decision Rules

- Surfaces/actions reference real operations and canonical schemas; they do not define inline payloads.
- Use `AbstractCollectionCommandResourceController` for an `@ApiResource` whose only real operations are collection-level `@WorkflowAction` commands. It owns canonical `/actions`, `/capabilities`, governed execution, and schema links without advertising query or CRUD operations.
- Do not add a fake `BaseResourceQueryService`, in-memory collection, CRUD controller, or `@UiSurface` merely to make a command-only resource discoverable. Such a resource remains outside the surface registry, so a resource-filtered `/schemas/surfaces` lookup may return `404`, until it exposes a real semantic surface.
- Absence in `actions` and absence in `capabilities` do not mean the same thing. Preserve the distinction.
- Related-resource surfaces must publish child binding and supported child operations only when backed by canonical child capabilities.
- Collection export is a collection operation with scope, selection, filters, sort, fields, limits, and capability proof.
- Stats discovery should come from `StatsFieldRegistry` and `StatsSupportMode`, not from trial-and-error chart fields.
- If a runtime needs a button, drawer, tab, related list, or workflow affordance, first check surfaces/actions/capabilities before inventing host UI metadata.

## No Keyword Routing

Do not route action, surface, cockpit, related-resource, export, or stats intent through labels, command words, regexes, aliases, or local fuzzy matching as the primary decision. Use `@UiSurface`, `@WorkflowAction`, canonical operations, capabilities, `_links`, availability contexts, and declared tools for grounding; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding a discovery field, action, surface, availability rule, capability operation, or cockpit projection, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new discovery contract. Otherwise complete the existing surface/action/capability materialization.

## Validation

Use focused local gates:

- surfaces: `mvn "-Dtest=AnnotationDrivenSurfaceDefinitionRegistryTest,DefaultSurfaceAvailabilityContextResolverTest,DefaultSurfaceAvailabilityEvaluatorTest,SurfaceCatalogServiceTest,SurfaceCatalogE2ETest,ResourceQuerySurfaceE2ETest" test`
- actions: `mvn "-Dtest=AnnotationDrivenActionDefinitionRegistryTest,DefaultActionAvailabilityContextResolverTest,DefaultActionAvailabilityEvaluatorTest,ActionCatalogServiceTest,ActionCatalogE2ETest,WorkflowNegativePathsE2ETest" test`
- capabilities/hypermedia: `mvn "-Dtest=OpenApiCanonicalCapabilityResolverTest,CapabilityServiceTest,CapabilityE2ETest,CapabilityConsistencyE2ETest,HypermediaDiscoveryE2ETest,HateoasAndPayloadSizeE2ETest" test`
- quickstart downstream proof: `QuickstartMetadataMigrationIntegrationTest` and `EventosFolhaPilotIntegrationTest`

Review Angular core action/surface/materializer tests and public docs/examples when discovery behavior changes.

## Companion Skills

- Use `praxis-metadata-schema-contracts` for schema URLs, request/response shape, ETag, and `X-Schema-Hash`.
- Use `praxis-metadata-resource-baseline` when discovery depends on resource base controller/service behavior.
- Use `praxis-api-quickstart-cockpit-http-validation` for downstream proof of surfaces, actions, related resources, stats, option sources, cockpit inventory, and HTTP scripts.
- Use `praxis-core-surface-materialization`, `praxis-core-global-action-payloads`, and `praxis-core-resource-runtime` for Angular runtime consumption.
