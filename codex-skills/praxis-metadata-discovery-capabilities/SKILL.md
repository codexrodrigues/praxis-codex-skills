---
name: praxis-metadata-discovery-capabilities
description: "Use when working on praxis-metadata-starter semantic discovery (inside the starter or in a consuming Java host): /schemas/surfaces, /schemas/actions, resource/item capabilities, bulk CRUD update discovery, @UiSurface, @WorkflowAction, availability contexts, ResourceStateSnapshot, relatedResource surfaces, collection export, stats capabilities, HATEOAS operation availability, or cockpit discovery."
---

# Praxis Metadata Discovery Capabilities

Use this skill for semantic discovery and availability in `praxis-metadata-starter`. Surfaces, actions, and capabilities are discovery and availability contracts over real resource operations; they must not become alternate schemas or local UI command vocabularies.

## Operating Mode & Source Audit

Determine whether you are operating in **Platform Source Mode** or **Consumer Host Mode**:

- **Platform Source Mode (`praxis-metadata-starter` checkout present in the workspace):**
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
- **Consumer Host / Published Dependency Mode (`io.github.codexrodrigues:praxis-metadata-starter` consumed via Maven):**
  Do not search for `src/main/java/org/praxisplatform/uischema/**` on disk. Pair with `praxis-java-availability-discovery-authoring` and `praxis-java-resource-authoring`, inspect the host's `@ApiResource`, `@UiSurface`, `@WorkflowAction`, `ResourceStateSnapshotProvider`, `ResourceOperationAvailabilityProvider`, and `StatsFieldRegistry`, and validate through the host's `/schemas/surfaces`, `/schemas/actions`, and `/capabilities` HTTP endpoints.

## Canonical Boundary

`@UiSurface` describes semantic UI surfaces over real operations. `@WorkflowAction` describes explicit business commands. Do not combine them on the same method without reviewing validation mode and conflict semantics.

`GET /{resource}/capabilities` and `GET /{resource}/{id}/capabilities` aggregate canonical operations, surfaces, actions, export, stats, and availability; they are snapshots, not a second source of schema truth.

Keep `canonicalOperations` structural: it says which capabilities the OpenAPI and resource service support, never whether the current principal may execute them. Use `operations.{operationId}.availability` for current executable discovery. The maps are related but not identical: the structural projection can publish capability IDs such as `filterExpression`, while the executable projection can carry CRUD aliases such as `view` and `edit`. Treat the current CRUD, query, options, stats, comparison, and export IDs as an evolving catalog; consumers must preserve unknown future IDs instead of validating against a closed key set or zipping both maps by position or presumed membership.

Apply `ResourceOperationAvailabilityProvider` with the published stable ID and the operation's own scope. Collection operations remain `COLLECTION`, including inside an item capability snapshot; do not leak item state or `resourceId` into their policy context. The provider governs discovery and HATEOAS. The host's `SecurityFilterChain` remains the executable authorization boundary.

Availability should use contextual resolvers and shared `ResourceStateSnapshot` (`ResourceStateSnapshotScope` per item capability projection in `DefaultCapabilityService`) rather than repeated N+1 resource loads.

For an item surface without `resourceId`, evaluate principal-independent item context only after restrictions that can already decide eligibility. In the default rule chain, required authorities precede contextual and allowed-state rules: an ineligible principal receives `missing-authority`; an eligible one may then receive `resource-context-required`. Never expose the principal, token, security expression, or protected resource state in availability metadata.

`resourceKey` is the stable semantic resource identity for discovery aggregation; `resourcePath`, action/surface `path`, HTTP method, schema URLs, and `_links` are operational execution evidence. Do not make URL shape the semantic identity, and do not hide a missing `resourceKey` with host-local aliases.

`capabilities.operations` governs whether an operation exists and is currently available; `_links` expose the executable hypermedia target. They must remain coherent. If a capability is denied, stale, missing, or contradicted by `_links`, treat it as a contract defect to fix in metadata/capability/HATEOAS generation, not as permission for Angular or agents to infer availability from labels, buttons, or route patterns.

`/schemas/surfaces` and `/schemas/actions` must be queried with exactly one scope: `resource=<resourceKey>` for resource semantic discovery or `group=<apiGroup>` for group discovery. Do not pass `resourcePath`, URLs, labels, operation names, or inferred cockpit keys as the `resource` parameter. If a consumer only has a path-derived fallback, surface that as inferred evidence and repair the `@ApiResource(resourceKey=...)`, action/surface publication, or cockpit resource catalog instead of treating the inferred key as canonical.

## Decision Rules

- Surfaces/actions reference real operations and canonical schemas; they do not define inline payloads.
- Use `AbstractCollectionCommandResourceController` for an `@ApiResource` whose only real operations are collection-level `@WorkflowAction` commands. It owns canonical `/actions`, `/capabilities`, governed execution, and schema links without advertising query or CRUD operations.
- Do not add a fake `BaseResourceQueryService`, in-memory collection, CRUD controller, or `@UiSurface` merely to make a command-only resource discoverable. Such a resource remains outside the surface registry, so a resource-filtered `/schemas/surfaces` lookup may return `404`, until it exposes a real semantic surface.
- Absence in `actions` and absence in `capabilities` do not mean the same thing. Preserve the distinction.
- Absence from `/schemas/actions` or `/schemas/surfaces` for a `resourceKey` means that the corresponding semantic catalog entry was not published for that resource. It does not mean Angular should downgrade to label matching, generic CRUD conventions, or host-authored command strings; either complete the metadata publication or keep the consumer in a diagnosed compatibility mode.
- Related-resource surfaces must publish child binding and supported child operations only when backed by canonical child capabilities (`SurfaceCatalogService` memoizes child capability lookups per normalized `childResourcePath` within each catalog pass).
- Collection export is a collection operation with scope, selection, filters, sort, fields, limits, and capability proof.
- Stats discovery should come from `StatsFieldRegistry` and `StatsSupportMode`, not from trial-and-error chart fields. `StatsCapability` publishes multidimensional governance (`maxDimensions`, `maxCells`, `supportedMetrics` including `AVG_PER_CYCLE_OCCURRENCE`) and `StatsFieldCapability.supportedExtractions` (`StatsDimensionExtraction`: `NONE`, cyclic `HOUR_OF_DAY`, `DAY_OF_WEEK`, `DAY_OF_MONTH`, `MONTH_OF_YEAR`, `QUARTER_OF_YEAR`, and linear `HOUR`, `DAY`, `WEEK`, `MONTH`, `QUARTER`, `YEAR`).
- Do not make one authority imply another by name, prefix, role hierarchy guess, or textual matching. Let the host provider evaluate each operation and surface explicitly.
- Keep HATEOAS alternatives coherent with availability: a denied `filter`, `cursor`, `all`, stats, or export operation must not be advertised as an executable link for that principal.
- If a runtime needs a button, drawer, tab, related list, or workflow affordance, first check surfaces/actions/capabilities before inventing host UI metadata.

## Bulk Discovery Composition & Governed Photographs

When working on bulk CRUD UPDATE discovery (`bulk-update`, `bulk-update-items`, `bulk-update-atomic`, `bulk-update-items-atomic`), `DOMAIN_COMMAND/ATOMIC` discovery, `ActionCatalogService` response scopes, or `DefaultCapabilityService` / `SurfaceCatalogService` governed OpenAPI photographs, read [bulk-discovery-composition.md](references/bulk-discovery-composition.md).

## No Keyword Routing

Do not route action, surface, cockpit, related-resource, export, or stats intent through labels, command words, regexes, aliases, or local fuzzy matching as the primary decision. Use `@UiSurface`, `@WorkflowAction`, canonical operations, capabilities, `_links`, availability contexts, and declared tools for grounding; textual matching may only rank already-scoped candidates.

## Adherence Inventory

Before adding a discovery field, action, surface, availability rule, capability operation, or cockpit projection, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new discovery contract. Otherwise complete the existing surface/action/capability materialization.

## Validation

- **In Platform Source Mode (`praxis-metadata-starter`):**
  - surfaces: `mvn "-Dtest=AnnotationDrivenSurfaceDefinitionRegistryTest,DefaultSurfaceAvailabilityContextResolverTest,DefaultSurfaceAvailabilityEvaluatorTest,SurfaceCatalogServiceTest,SurfaceCatalogE2ETest,ResourceQuerySurfaceE2ETest" test`
  - actions: `mvn "-Dtest=AnnotationDrivenActionDefinitionRegistryTest,DefaultActionAvailabilityContextResolverTest,DefaultActionAvailabilityEvaluatorTest,ActionCatalogServiceTest,ActionCatalogE2ETest,WorkflowNegativePathsE2ETest" test`
  - capabilities/hypermedia: `mvn "-Dtest=OpenApiCanonicalCapabilityResolverTest,CapabilityServiceTest,CapabilityE2ETest,CapabilityConsistencyE2ETest,HypermediaDiscoveryE2ETest,HateoasAndPayloadSizeE2ETest" test`
  - quickstart downstream proof: `QuickstartMetadataMigrationIntegrationTest` and `EventosFolhaPilotIntegrationTest`
- **In Consumer Host Mode:**
  - run focused host HTTP/MockMvc tests for `/schemas/surfaces?resource=...`, `/schemas/actions?resource=...`, `GET /{resource}/capabilities`, `GET /{resource}/{id}/capabilities`, and `RestApiResponse._links`.

When operation IDs or availability shape changes, also run the focused Angular `ResourceDiscoveryService` test and build `praxis-core` and direct public consumers.

## Companion Skills

*(In external Antigravity workspaces, full companion skills are available under `~/.gemini/praxis-skills/<skill-name>/SKILL.md` or `$CODEX_HOME/skills/<skill-name>/SKILL.md`.)*

- Use `praxis-java-availability-discovery-authoring` when authoring `@UiSurface`, `@WorkflowAction`, `ResourceStateSnapshotProvider`, and capabilities in a Java host.
- Use `praxis-metadata-schema-contracts` for schema URLs, request/response shape, ETag, and `X-Schema-Hash`.
- Use `praxis-metadata-resource-baseline` when discovery depends on resource base controller/service behavior.
- Use `praxis-api-quickstart-cockpit-http-validation` for downstream proof of surfaces, actions, related resources, stats, option sources, cockpit inventory, and HTTP scripts.
- Use `praxis-core-surface-materialization`, `praxis-core-global-action-payloads`, and `praxis-core-resource-runtime` for Angular runtime consumption.
