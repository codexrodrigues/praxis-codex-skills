---
name: praxis-metadata-discovery-capabilities
description: "Use when Codex must work on praxis-metadata-starter semantic discovery: /schemas/surfaces, /schemas/actions, resource/item capabilities, bulk CRUD update discovery, @UiSurface, @WorkflowAction, availability contexts, ResourceStateSnapshot, relatedResource surfaces, collection export, stats capabilities, HATEOAS operation availability, or cockpit discovery."
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

Keep `canonicalOperations` structural: it says which capabilities the OpenAPI
and resource service support, never whether the current principal may execute
them. Use `operations.{operationId}.availability` for current executable
discovery. The maps are related but not identical: the structural projection can
publish capability IDs such as `filterExpression`, while the executable
projection can carry CRUD aliases such as `view` and `edit`. Treat the current
CRUD, query, options, stats, comparison, and export IDs as an evolving catalog;
consumers must preserve unknown future IDs instead of validating against a
closed key set or zipping both maps by position or presumed membership.

Apply `ResourceOperationAvailabilityProvider` with the published stable ID and
the operation's own scope. Collection operations remain `COLLECTION`, including
inside an item capability snapshot; do not leak item state or `resourceId` into
their policy context. The provider governs discovery and HATEOAS. The host's
`SecurityFilterChain` remains the executable authorization boundary.

Availability should use contextual resolvers and shared `ResourceStateSnapshot` rather than repeated N+1 resource loads.

For an item surface without `resourceId`, evaluate principal-independent item
context only after restrictions that can already decide eligibility. In the
default rule chain, required authorities precede contextual and allowed-state
rules: an ineligible principal receives `missing-authority`; an eligible one may
then receive `resource-context-required`. Never expose the principal, token,
security expression, or protected resource state in availability metadata.

`resourceKey` is the stable semantic resource identity for discovery aggregation; `resourcePath`, action/surface `path`, HTTP method, schema URLs, and `_links` are operational execution evidence. Do not make URL shape the semantic identity, and do not hide a missing `resourceKey` with host-local aliases.

`capabilities.operations` governs whether an operation exists and is currently available; `_links` expose the executable hypermedia target. They must remain coherent. If a capability is denied, stale, missing, or contradicted by `_links`, treat it as a contract defect to fix in metadata/capability/HATEOAS generation, not as permission for Angular or agents to infer availability from labels, buttons, or route patterns.

`/schemas/surfaces` and `/schemas/actions` must be queried with exactly one
scope: `resource=<resourceKey>` for resource semantic discovery or `group=<apiGroup>`
for group discovery. Do not pass `resourcePath`, URLs, labels, operation names,
or inferred cockpit keys as the `resource` parameter. If a consumer only has a
path-derived fallback, surface that as inferred evidence and repair the
`@ApiResource(resourceKey=...)`, action/surface publication, or cockpit resource
catalog instead of treating the inferred key as canonical.

## Decision Rules

- Surfaces/actions reference real operations and canonical schemas; they do not define inline payloads.
- Use `AbstractCollectionCommandResourceController` for an `@ApiResource` whose only real operations are collection-level `@WorkflowAction` commands. It owns canonical `/actions`, `/capabilities`, governed execution, and schema links without advertising query or CRUD operations.
- Do not add a fake `BaseResourceQueryService`, in-memory collection, CRUD controller, or `@UiSurface` merely to make a command-only resource discoverable. Such a resource remains outside the surface registry, so a resource-filtered `/schemas/surfaces` lookup may return `404`, until it exposes a real semantic surface.
- Absence in `actions` and absence in `capabilities` do not mean the same thing. Preserve the distinction.
- Absence from `/schemas/actions` or `/schemas/surfaces` for a resourceKey means
  that the corresponding semantic catalog entry was not published for that
  resource. It does not mean Angular should downgrade to label matching,
  generic CRUD conventions, or host-authored command strings; either complete
  the metadata publication or keep the consumer in a diagnosed compatibility
  mode.
- Related-resource surfaces must publish child binding and supported child operations only when backed by canonical child capabilities.
- Collection export is a collection operation with scope, selection, filters, sort, fields, limits, and capability proof.
- Stats discovery should come from `StatsFieldRegistry` and `StatsSupportMode`, not from trial-and-error chart fields.
- Do not make one authority imply another by name, prefix, role hierarchy guess, or textual matching. Let the host provider evaluate each operation and surface explicitly.
- Keep HATEOAS alternatives coherent with availability: a denied `filter`, `cursor`, `all`, stats, or export operation must not be advertised as an executable link for that principal.
- If a runtime needs a button, drawer, tab, related list, or workflow affordance, first check surfaces/actions/capabilities before inventing host UI metadata.

## Bulk discovery composition

For bulk CRUD UPDATE discovery, inspect Metadata
`docs/spec/BULK-CRUD-STRUCTURE.md` and `BULK-CRUD-OPERATIONS.md` before
projecting a capability. Metadata rc.150 publishes the protected V16 `ATOMIC`
kernel, while its existing discovery projects a complete operational UPDATE as `bulk-update` or `bulk-update-items`
(`UNIFORM_UPDATE` or `PER_ITEM_UPDATE`) as a `COLLECTION` `POST` at `.bulk`,
with seven canonical
cycle references and ordered `editableFields` (`sourceOperation` as a
`CanonicalOperationRef`, `requestSchema`, `writableFields`, `clearableFields`). Reuse the same response frame and
readiness fence as the action; neither a real PUT source nor a structural
allowlist alone makes UPDATE READY. A valid UPDATE without a provider must not
degrade an independent command READY, but malformed declarations fail the
whole composition. `publish` and `requireReady` reject orphaned identities
before durable I/O; response preparation may read durable evidence before
compilation. Removing a provider makes `requireReady` deny but does not
automatically change the durable READY row; `suspend` or invalidation follows
its own close protocol. Keep availability outside preparation/cache locks and preserve the
final poison check and cleanup on all exits. The published rc.150 UPDATE
composition is `SYNC`/`EXPLICIT`/`PER_ITEM`; do not infer selection queries,
async or atomic batch behavior, host grants, or domain mutation from it. Verify source,
schema, frame coherence, provider removal, orphan denial, and a following clean
request before teaching consumers to display the capability.
`collectionOperationAvailability` is a contextual provider decision, even for
unknown operation IDs; it does not prove structural support or READY. In this
cut, the capability snapshot under that frame is the only READY projection for
the `.bulk` operation and its seven canonical references. Resource bases do
not add bulk `_links` automatically. If a later cut adds them, derive them from
the operation in the same snapshot/fence, without a separate lookup or a URL
convention.

Metadata rc.151 publishes `ATOMIC` CRUD composition. Derive one capability identity from
the pair `(mode, atomicity)`: `UNIFORM_UPDATE/PER_ITEM` → `bulk-update`,
`PER_ITEM_UPDATE/PER_ITEM` → `bulk-update-items`, `UNIFORM_UPDATE/ATOMIC` →
`bulk-update-atomic`, and `PER_ITEM_UPDATE/ATOMIC` → `bulk-update-items-atomic`.
Reject duplicate `(resourceKey, mode, atomicity)` declarations, missing or
ambiguous exact confirmation providers, and a mismatch of operation, schema,
or provider against the one published OpenAPI photograph. CRUD UPDATE composes
`ATOMIC` with `EXPLICIT`/`SYNC`, 1–50 targets and an aggregate unit deadline no
greater than five seconds.
Each variant has its own confirmation operation/control identity and seven
canonical references; the five bodyless proposal, proposal-results, execution,
execution-results and cancel handlers are shared. The publication fence is
global: suspending one variant invalidates the photograph and readiness of all
variants. Republishing one variant recaptures and validates the global
photograph but returns only that variant to `READY` and capabilities; the
others remain absent until their own publication. Contextual
availability is neither execution authorization nor a proof of host `READY`.
Consult `praxis-java-command-concurrency-authoring` for whole-set admission,
transactional mutation, receipt and recovery proof. Do not teach consumers
these IDs as host-adopted capabilities until the exact artifact is consumed and
downstream readiness is separately proved.

For a candidate `DOMAIN_COMMAND/ATOMIC`, inspect the real `@WorkflowAction`,
its action-registry binding, typed parameters, and `BulkOperation` declaration
before projecting discovery. Their atomicity must agree; the exact provider,
confirmation operation and seven canonical references must resolve in the same
published photograph. Preserve the action identity and request/response schemas;
do not manufacture a CRUD capability or editable fields for a command. The
operational profile remains `EXPLICIT`/`SYNC`, at most 50 targets, an aggregate
unit deadline no greater than five seconds and any stricter action `maxItems` limit. A mismatch
fails closed. This composition candidate does not establish a host command
provider, executable HTTP route, domain authorization, outbox, `READY`, or
public adoption; prove those separately against the exact published artifact.

`ActionCatalogService` must assemble each synchronous response inside the lifecycle's response scope while keeping contextual availability outside document-cache and preparation locks. Resource, group, item and collection entrypoints preserve the original action definitions, principal and availability contexts. Reuse only the structural descriptor captured for that response; `execution.bulk` is descriptive evidence and never a readiness or authorization token.

Scoped `requireReady` must recheck namespace/operation, current provider composition and the durable READY row against the captured generation, fingerprint and structural revision. It may reuse the structural snapshot, but must not memoize availability or share that scope across requests, threads or asynchronous continuations. Suspend/republish with identical content still changes the generation and must reject the old response.

After leaving fresh preparation, use the concrete ephemeral snapshot read fence to bound short read-lock acquisition by the original composition deadline and check cache epoch and transport revision before and after provider/durable reads. Capture only from the actual fresh callback; dispose the fence and private response frame in `finally`. Never retain a public cache lock or a JDBC transaction around host rules or the response builder.

Preparation failure may invoke the builder once with an empty bulk projection and a denying scope. Once the builder starts, its exception or a failed final coherence check must propagate; do not repeat the builder or convert its failure into a second composition. Always run the final fence/provider/durable check after the builder returns, including when a host rule caught a readiness exception and returned denied.

Prove all four catalog entrypoints, exception cleanup, independent following requests, cache/transport changes (including transport replacement/restoration), deadlines, thread confinement, provider changes and durable generation changes. The concrete multigroup HTTP proof must preserve the authorized bulk body and references while demonstrating one fresh composition per catalog or collection-capabilities GET. A selective proof does not certify the complete backend, load performance or the full HTTP campaign.

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
- Angular contract proof: run the focused `ResourceDiscoveryService` test, then build `praxis-core` and direct public consumers when operation IDs or availability shape changes.

Review Angular core action/surface/materializer tests and public docs/examples when discovery behavior changes.

## Companion Skills

- Use `praxis-metadata-schema-contracts` for schema URLs, request/response shape, ETag, and `X-Schema-Hash`.
- Use `praxis-metadata-resource-baseline` when discovery depends on resource base controller/service behavior.
- Use `praxis-api-quickstart-cockpit-http-validation` for downstream proof of surfaces, actions, related resources, stats, option sources, cockpit inventory, and HTTP scripts.
- Use `praxis-core-surface-materialization`, `praxis-core-global-action-payloads`, and `praxis-core-resource-runtime` for Angular runtime consumption.
