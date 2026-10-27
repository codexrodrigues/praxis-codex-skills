---
name: praxis-core-resource-runtime
description: Use when Codex must work with @praxisui/core resource runtime contracts: GenericCrudService, SchemaMetadataClient, ResourceDiscoveryService, /schemas/filtered consumption, actions, surfaces, capabilities, HATEOAS links, related-resource surfaces, option-source runtime, CRUD operation resolution, bulk execution polling and observation deadlines, analytics schema contracts, stats request builders, custom-field schema expansion, or metadata-driven resource materialization.
---

# Praxis Core Resource Runtime

Use this skill for the `@praxisui/core` runtime path that turns canonical backend metadata into Angular resource behavior.

The backend remains the semantic owner. `@praxisui/core` should consume and materialize `praxis-metadata-starter` contracts such as `/schemas/filtered`, `/schemas/actions`, `/schemas/surfaces`, capabilities, HATEOAS links, `x-ui`, option sources, domain catalogs, and analytics projections. It must not invent local semantics to compensate for missing metadata.

When a backend contract is missing, contradictory, or weakly materialized, load the relevant `praxis-metadata-*` skill before patching Angular. Treat the Angular runtime as the consumer/projection layer, not as the place to invent backend metadata semantics.

## Source Audit

Inspect the affected source before changing guidance or code:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/src/public-api.ts` when resource runtime models, services, components, tokens, or helpers are exported or public consumption changes
- `projects/praxis-core/src/lib/services/generic-crud.service.ts`
- `projects/praxis-core/src/lib/schema/schema-metadata-client.ts` and its specs
- `projects/praxis-core/src/lib/schema/schema-request-key.ts` (internal representation key)
- `projects/praxis-core/src/lib/services/schema-normalization-kernel.ts`
- `projects/praxis-core/src/lib/helpers/field-definition-mapper.ts` and its spec
- `projects/praxis-core/src/lib/services/dynamic-form.service.ts` and its spec
- `projects/praxis-core/src/lib/models/field-definition.model.ts`
- `projects/praxis-core/src/lib/models/component-metadata.interface.ts`
- `projects/praxis-core/src/lib/models/form/server-owned-field-semantics.ts`
- `projects/praxis-core/src/lib/models/form/materialize-custom-fields-layout.ts`
- `projects/praxis-core/src/lib/models/form/custom-fields-reconciliation.spec.ts`
- `projects/praxis-core/src/lib/models/form/form-config.model.ts` (`syncWithServerMetadata`)
- `projects/praxis-core/src/lib/reconcilers/form-config-reconciler.ts` and `filter-config-reconciler.ts`
- `projects/praxis-core/src/lib/services/resource-discovery.service.ts`
- `projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts`
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
- `projects/praxis-core/src/lib/models/bulk-operation.model.ts`
- `projects/praxis-core/src/lib/services/bulk-operation-client.service.ts` and its spec
- `projects/praxis-core/src/lib/services/bulk-sync-state.service.ts` and its spec
- `projects/praxis-core/src/lib/models/enterprise-runtime-context.model.ts` for complete scope identity

Also read nearby specs for the exact behavior being changed. They are often the clearest contract for edge cases such as related resources, denied actions, schema operation resolution, and selected-value reload.

## Runtime Boundary

Use canonical metadata as the source:

- `/schemas/filtered`: structural request/response schema, field metadata, `x-ui`, option-source metadata, operation-specific schema shape
- `/schemas/catalog`: documentary/discovery enumeration of OpenAPI endpoints, resource/group visuals, operation examples, and canonical request/response schema links; it scopes candidates but does not replace filtered structural schema
- `/schemas/actions` and action metadata: action discovery and availability
- `/schemas/surfaces` and surface metadata: surface discovery and materialization
- capabilities and HATEOAS links: availability and executable operation proof
- option-source descriptors and `/by-ids`: remote select, entity lookup, dependency filters, and selected-value rehydration
- domain catalog/knowledge/rules: AI grounding and explanation, not local routing by labels
- analytics metadata: stats/projection materialization, not chart-local metric vocabulary
- Preserve the distinction between semantic identity and operational address. `resourceKey` is the stable backend semantic identity for surfaces/actions/capabilities; `resourcePath`, `path`, `method`, `schemaUrl`, `_links`, and resolved hrefs are operational evidence. Do not collapse them into a single route string or local endpoint map.
- Treat operation resolution source as evidence quality. `explicit`, `capability`, `surface`, and `link` resolutions carry declared contracts; `convention` is a compatibility fallback that must emit/keep diagnostics and should trigger a backend metadata audit before agents treat the operation as canonical.
- Treat `/schemas/filtered` availability as an origin-level capability only when
  the endpoint itself is unavailable. A structured 404/business miss for a
  specific path or operation means the metadata endpoint is alive and the
  requested catalog entry is missing; do not cache the whole origin as
  unavailable, and do not replace the missing catalog entry with a local
  endpoint convention without recording diagnostics and auditing metadata.

If these are missing or contradictory, classify the gap and return to the canonical backend/config owner. Do not patch with host-only aliases, label matching, local endpoint maps, or Angular-only action routers.

`ResourceDiscoveryService` exposes the shared read path for these projections:

- `getSchemaCatalog(query, options)` requests `/schemas/catalog` through the configured API origin and forwards only canonical `group`, `path`, and `operation` filters;
- `getCapabilitiesByUrl(href, options)` follows the exact capabilities href already published by discovery metadata, preserving the normal trusted-origin/proxy resolution rules instead of rebuilding a convention from `resourceKey`;
- `getCapabilities(source, options)` remains the HATEOAS-rel path when a resource envelope already owns the `capabilities` link.

Keep the Angular models aligned with the real backend payloads. `ResourceSchemaCatalogResponse` owns `group`, `groupVisual`, and endpoint entries; each endpoint carries canonical path/method/resource identity, visuals, request/response schema summaries, parameters, examples, and schema links. `ResourceCapabilitySnapshot.stats.fields[]` carries public field identity, metrics, modes, and each eligibility boolean. Do not shrink these payloads into chart-specific aliases or use `Record<string, unknown>` where the starter already publishes a stable shape.

## Common Decisions

- `resourcePath` is a base resource path, not an operation URL.
- Do not add `/api`, `/filter`, `/{id}`, query strings, schema paths, or submit endpoints to `resourcePath` when `GenericCrudService` can resolve them.
- Use operation-specific `schemaUrl`, `submitUrl`, and `submitMethod` only when a real action/surface/command contract requires them.
- Treat capabilities and `_links` as availability gates for optional operations such as export, create, edit, delete, duplicate, workflow actions, and surface opens.
- When `CrudOperationResolutionService` returns `source: "convention"`, keep
  that source and diagnostics visible to the caller. Convention resolution may
  build canonical `/schemas/filtered` and submit URLs for compatibility, but it
  is not proof that `/schemas/actions`, `/schemas/surfaces`, capabilities, or
  HATEOAS links published the operation.
- `availability.allowed=false`, missing rels, missing schema URLs, stale capability snapshots, or denied actions must fail closed to disabled UI, clarification, or diagnostics. Do not infer permission from button visibility, route patterns, component presence, or matching action labels.
- For related resources, prefer `RelatedResourceSurfaceResolverService` and the `surface.relatedResource` contract over local parent-child filters.
- For selected rows or widget outputs, check `PraxisSurfaceHostComponent`, materializer output wiring, row events, and capabilities before declaring a platform gap.
- Treat `x-ui.resource.identity` as the canonical structured identity of a record. `keyField`, `titleField`, ordered `metadataFields`, and `displayLabelField` come from `@ApiResource(identity = @ResourceIdentity(...))`; Angular must not infer these roles from property names or split a concatenated `displayLabel`.
- For list/detail continuity, prefer the `resourceIdentity` already materialized on Praxis Table row/selection events and render it with `PraxisResourceIdentityComponent`. Re-fetching schema in the host, duplicating field-role config in CRUD metadata, or composing a screen-specific identifier header is a platform bypass.
- Preserve field-level `x-ui.presentation` when materializing identity parts. A visual key may inherit prefix/appearance from its field while title and metadata remain structurally governed by `x-ui.resource.identity`.

## Item Representation And Revision Custody

Use `getByIdHttpResponse` when a consumer must retain the ETag with the exact body that hydrated its edit state; `getByIdResponse` remains the body wrapper API. Use `updateHttpResponse` to consume the mutation representation and headers together. `CrudOperationOptions.resourceVersion` distinguishes undefined (existing cache/body fallback behavior), a strong snapshot token (explicit precondition) and null (omit If-Match, including an inherited configured header). Another consumer advancing the shared cache must not authorize an older edit payload. The generic undefined path retains cache, DTO token and configured-header precedence; an absent response ETag may preserve that DTO fallback, while an explicit invalid ETag clears cache. The automatic form always supplies its own original-GET strong token or explicit null, so none of those generic fallbacks can authorize its edit.

`readStrongResourceEtag` validates the item validator; do not substitute schema/cache validators or weak tags. The consumer owns snapshot identity, destination, actor/tenant scope and request epoch. Reconfigure its transport when context changes, including removal of named/custom endpoints, and invalidate pending reads/writes across reset, reload and A→B→A context changes. Compare the operation epoch as well as identity before accepting late responses. A successful same-resource save may replace the body and ETag together; an explicit or cross-resource command precondition does not authorize hydrating the origin form from the command response. Missing/partial mutation representations require explicit reconciliation, not attaching a new token to an old body.

Prove these rules in the Core client and direct Form consumer, with focused builds and real authenticated HTTP/browser evidence. Candidate source APIs are not evidence of published-package adoption; retain that distinction in release and consumer guidance.

## Bulk Execution Observation

Inspect `services/praxis-bulk-client.service.ts`, its focused spec and the CRUD
bulk dialogs before changing `PraxisBulkClientService.waitForExecution`. This
client and the BASIC `BulkOperationClientService` are distinct paths; a polling
fix does not certify BASIC read deadlines or enable ASYNC in BASIC.

Preserve the terminal-only observable contract. Allow at most one execution GET
in flight; a polling tick must not abort a useful slow response. Start the
observation deadline on subscription and enforce it independently of response
emissions. Pending responses do not renew the deadline. Timeout, error,
unsubscribe and destruction must tear down the timer and active HTTP request;
a late response cannot revive an expired observation.

Use the canonical terminal classification. `CANCEL_REQUESTED` remains pending;
terminal does not mean successful. An observation timeout says nothing about
rollback or whether the backend has committed. Resuming observation reads the
same execution with a fresh consultation deadline; it must not evaluate a new
proposal or repeat confirmation automatically.

Prove this with the real service and controlled HTTP: responses slower than the
poll interval, a request that never responds, repeated pending responses, delayed
and repeated subscriptions, transport failure, unsubscribe and the deadline
boundary. A spy returning a terminal value from `waitForExecution` does not test
polling. Also validate both direct CRUD consumers and keep mock evidence distinct
from real protected HTTP and backend effect/replay receipts.

## BASIC Bulk Intent and Authorized Projection

For BASIC, consume the published `SYNC / EXPLICIT / PER_ITEM` descriptor through
`BulkOperationClientService` and `BulkSyncStateService`; do not infer support for
QUERY, ASYNC or ATOMIC from enum members. Retain exact operation/group/method/path,
resource, configured origin and wire IDs. Read each selected resource's original
strong ETag from its canonical self GET with the published identity accessor;
reject weak, missing or cross-identity tokens, and never substitute a schema ETag.
Evaluate an immutable selection/intent without domain effects, then read the
protected preview and require a separate explicit confirmation of its proposal.
Keep one original Idempotency-Key for confirmation uncertainty and replay of that
same intent; changed intent needs a separately initiated evaluation, never an
automatic replacement proposal or a retry that resubmits successful targets.

Separate proposal/execution/key custody from permission to display retained data.
On protected 401/403/404/410 or scope loss, the consuming workflow invalidates its projection;
retained state is not current authorization or proof that no effect committed.
The consuming workflow uses an authorization epoch so late successes cannot restore data after denial or
context change. Before redisplay, require complete fresh authorized reads for the
same resource/operation, actor, tenant, environment and organization scope, including
`effectiveContext.activeOrganizationId`. Do not replace the original proposal/key,
change actor to regain permission, or use local persistence as authority.

Keep BASIC read lifetime separate from mutation custody. `BulkSyncSession.refreshExecution(signal?)`
and `readResults(size, after, signal?)` retain their Promise contract and accept an
optional standard `AbortSignal`. Cancellation must unsubscribe the underlying GET,
reject pre-aborted calls before dispatch, remove listeners and release in-flight
state without letting an older completion clear a newer read. A timeout around
`from(Promise)` or `Promise.race` alone does not cancel that transport. The Core
session does not impose a universal deadline on callers that omit the signal.

The owning Table workflow supplies its existing `LoadingConfig.requestTimeoutMs`
consultation policy (default 30000; zero disables it under a separate governed
policy). Do not substitute the backend unit deadline or the ASYNC polling deadline.
Timeout/destruction stops observation, never proves a terminal execution or rollback.
Keep evaluate/confirm POST custody and the original key independent of these GETs;
an aborted GET must not remain as pending session work that blocks remount.

Prove protocol/ETag/key/identity in the client/state specs and denial-versus-late-200
interleavings in the owning Table consumer. Mocks prove controlled transport
and UI behavior; require distinct real protected HTTP/backend commit/read/replay
receipts before claiming operational effects or deployed acceptance. Review the
exact runtime source and its focused evidence before adopting this workflow.

## Custom-Field Materialization

Audit the backend schema before changing expansion. `SchemaNormalizerService`
expands a property marked with boolean `x-ui.customFieldsContainer: true`, or an
object named `customFields` with inline `properties`, through the normal child
field path. The container is wire structure and never an independent control.
Children still need ordinary `x-ui` field metadata; expansion does not invent
controls for undocumented children.

Preserve child labels, controls, options, option sources, validators, groups and
order, including the container schema's `required` list. Retain the original root
schema when resolving child collection references and keep global field ordering.
Each expanded child uses the full value path, such as `customFields.numero_calcado`,
and `customField: true`; retain the published `customFieldKey` and
`customFieldScope`, defaulting only absent values to the original child name and
`tenant`. `mapFieldDefinitionToMetadata` must carry that identity into
`FieldMetadata`. Identity does not grant permission or replace backend validation.

Keep parent restrictions monotonic when expanding: `disabled: true`, `readOnly: true` and `formHidden: true` remain restrictive on children. Do not distribute
scalar parent defaults/validators to leaves. Keep `formHidden` server-owned during
sync. Inherit absent child `fieldAccess`; accept equivalent authority sets, but
reject different parent/child policies and require the backend's effective leaf
policy rather than approximating AND with an OR-list. A normalizer error alone
does not prove end-to-end fail-closed behavior: saved-config catches/fallbacks can
retain earlier metadata, so inspect those consumers before claiming authorization.

Do not certify every backend-valid custom key as an Angular control. Own-key
payload helpers do not resolve FormGroup limitations with `constructor`,
`toString` or `hasOwnProperty`; align the canonical backend key policy and
consumers rather than adding screen aliases or private Angular API workarounds.
Field read-only is also not submit omission: the custom-field backend rejects
read-only property presence while request publication can still expose it.
`x-ui.submitPolicy` is not materialized by the current FieldDefinition/normalizer
contract. Record that backend/runtime adoption blocker; do not claim adding a
local policy or omitting every hidden field resolves it canonically.

Keep `customField`, `customFieldKey` and `customFieldScope` server-owned through
form/filter reconciliation and `syncWithServerMetadata`, using the existing
`applyServerOwnedFieldSemantics` path. Refresh current identities and clear stale
local identities when the server no longer publishes them; saved UI customizations
must not override schema identity. Include changes/removals of all three identity
keys in `syncResult.modifiedFields` and `hasChanges`, even when no visual metadata
changed, so callers can persist the corrected configuration.

When a saved raw container is absent from the current schema but
that schema publishes its direct children with `customField: true`, materialize its
metadata and layout references as those current children before reconciliation.
Use the internal `materializeCustomFieldsLayout` path across all three entrypoints.
A colliding saved container, even `source: "local"`, yields to the current server
shape; do not carry its omit policy into the children. Preserve noncolliding local
fields, ancestors still declared by the current schema, more distant ancestors,
and ordinary dotted fields without custom-field identity. Migrate both legacy `fields` and mixed `items` layouts, retain rich content and already placed
children, avoid duplicate references/item IDs, tolerate missing rows/columns and
leave the input unchanged. Synchronization diagnostics must report container
removal even when all children were already saved; repeating the migrated config
must report no further removal. Do not infer trusted children from saved configuration or introduce a host migration adapter.

Do not flatten wire values into literal dotted JSON keys or add host transforms.
Use `praxis-form-submit-payload-pipeline` for nested submit paths, date hydration
and filter value restoration; the JSON remains
`{ "customFields": { "numero_calcado": 40 } }`.

## No Keyword Routing

Do not route user intent, action selection, surface opening, tab selection, lookup selection, or analytics metrics by labels, regex, XML names, aliases, or keyword lists as the primary decision. Textual matching may rank candidates only after canonical resource/operation/surface/field scope is resolved from metadata and governed tools.

## Schema transport resilience

Keep public structural identity separate from representation custody.
`buildSchemaId`, metadata `schemaId` and `getLastSchemaInfo()` retain their semantic
identity; equal IDs do not prove equal tenant-specific schema bodies or hashes.
The shared internal `buildSchemaRequestKey` binds schema cache entries and
`SchemaMetadataClient` in-flight ownership to
`[schemaId, resolved request URL, declared tenant ?? null, declared locale ?? null]`.
Use it for `GenericCrudService.getSchema`, `getFilteredSchema` and direct-schema
fallbacks, including ETag/304 revalidation and status-0 cache recovery. Never fall
back to an old neutral-ID cache entry. `getFilterSchema` observable replay must
also include the endpoint key and full representation tuple; capture the context
when creating the observable, before delayed subscription or a context switch.

The compiled `DynamicFormService` L1 key uses the shared structured tuple too;
do not reintroduce tenant/locale delimiter concatenation. GenericCrud detects
API/configured-endpoint/declared-tenant/locale changes, invalidates derived
identity/capability metadata, hints and filter replay, and checks an internal
epoch before late schema callbacks update current state. Getters also validate
the declared context; returning to an earlier context needs a read/revalidation,
not replay of its former observable. The isolated representation cache may remain
for its own ETag revalidation. Remove derived resource fields absent from the new
schema instead of retaining the previous context's values.

This epoch covers configured scope only. Per-call `endpointKey`/`parentPath`
overrides can run under the same epoch and compete for singleton derived metadata
or hints even with separate representation cache keys. The getters do not accept
per-call context. Record shared concurrent multi-endpoint/multi-parent adoption
as an unresolved Core contract blocker; do not infer its safety from cache tests.

Hosts must declare representation context: `GetSchemaParams.tenant`/`locale` for
`SchemaMetadataClient`, and the configured tenant plus browser locale for
`GenericCrudService`. Preserve that captured context through asynchronous cache
reads and retries. Implicit global header hooks, interceptors, cookies or principal
changes do not add a cache dimension; this tuple does not certify their isolation.
Extra global headers must not override explicitly declared headers through
case differences. That precedence does not partition an implicit authentication
principal. Do not change public `buildSchemaId` or export the internal key to hide
that limit. Status-0 cache recovery and saved-config reconciliation warnings also
do not prove schema freshness; the existing ready/error surface does not expose
all degraded states. Keep that UX limitation explicit, without inventing a local
freshness or authorization signal.

- `SchemaMetadataClient` owns the schema-read deadline. Angular consumers inject `SCHEMA_METADATA_CLIENT_OPTIONS`; direct clients pass constructor options. `requestTimeoutMs` defaults to 30000; finite nonnegative values are required and 0 explicitly disables the deadline. Do not invent per-widget timeout settings for this policy.
- Propagate `GetSchemaParams.signal` and preserve shared-request isolation: cancelling one subscriber must not cancel others; cancelling the final subscriber aborts the transport. Timeout must release in-flight state even if transport ignores abort, and late responses must not start cache writes.
- The deadline covers cache reads, fetch/body consumption and a 304 refetch. It does not bound all component initialization, hooks or independent preference persistence. A cache write already started is not rolled back by abort.
- Keep tenant, locale, credentials and host headers on a 304 refetch. Prove timeout, retry, cancellation, shared subscribers and response-body stalls with focused tests.
- Diagnose a pending browser request separately from backend latency. Compare the exact observed URL and capture response/failure evidence. A client-block error is not proof of a backend defect; a timeout improves recovery but does not prove that the block was fixed.
- Consumers must not silently substitute a different schema operation after timeout or cancellation. Form retries must invalidate old initialization attempts before they can mutate the current configuration.

## Validation Guidance

Use focused specs for the touched service or model:

- resource discovery, schema metadata, and schema normalization:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts --include=projects/praxis-core/src/lib/schema/schema-metadata-client.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer-array.service.spec.ts
```

- custom-field schema expansion and metadata mapping:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts --include=projects/praxis-core/src/lib/helpers/field-definition-mapper.spec.ts --include=projects/praxis-core/src/lib/services/dynamic-form.service.spec.ts
```

Prove explicit and implicit containers, absent identity defaults, child required
fields, global ordering, original-root collection refs, malformed containers and
schema immutability. Prove normalization-to-`DynamicFormService` integration creates
nested controls, retains validators, and round-trips structured values. Also prove
the direct form consumer's nested value path.

For saved configurations, run the focused integration across form reconciliation,
filter reconciliation and metadata synchronization:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/models/form/custom-fields-reconciliation.spec.ts
```

Prove schema identity refresh/removal, raw-container metadata/layout migration,
direct-child-only replacement including a colliding local parent, noncolliding
local/current/distant ancestor preservation, parent restriction/fieldAccess cases, mixed
content, unique item IDs, incomplete layouts, child placement without duplication,
identity-only change/removal diagnostics, sync container-removal diagnostics,
idempotence and source immutability.

- schema representation isolation across both real consumers:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/schema/schema-metadata-client.spec.ts --include=projects/praxis-core/src/lib/schema/schema-metadata-client.transport.spec.ts --include=projects/praxis-core/src/lib/services/generic-crud.service.spec.ts
```

Prove separate tenant/locale/resolved-URL entries, same-tuple client deduplication,
independent cancellation, per-context ETags/304s, ignored neutral legacy entries
and captured context across pending reads. Cover all three GenericCrud schema
lanes, status-0 recovery without cross-tenant reuse, pending 304 races, filter
replay isolation, delayed subscription, delimiter-safe L1 keys and stale derived
state fencing/removal across context changes. Include `dynamic-form.service.spec.ts`
for L1 and `fetch-with-etag.util.spec.ts` for case-insensitive declared headers.
Keep these controlled transport proofs
separate from real authenticated host adoption and implicit credential isolation.

- CRUD runtime, option sources, and selected-value rehydration:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/generic-crud.service.spec.ts --include=projects/praxis-core/src/lib/models/option-source.model.spec.ts
```

- record identity and list/detail continuity:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/models/resource-identity.model.spec.ts --include=projects/praxis-core/src/lib/components/resource-identity/resource-identity.component.spec.ts --include=projects/praxis-core/src/lib/services/generic-crud.service.spec.ts
```

```sh
npm run test:table -- --include=projects/praxis-table/src/lib/praxis-table.events.spec.ts
```

- action/surface opening, related resources, and outlet registration:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/resource-action-open-adapter.service.spec.ts --include=projects/praxis-core/src/lib/services/resource-surface-open-adapter.service.spec.ts --include=projects/praxis-core/src/lib/services/surface-open-materializer.service.spec.ts --include=projects/praxis-core/src/lib/services/related-resource-surface-resolver.service.spec.ts --include=projects/praxis-core/src/lib/services/surface-outlet-registry.service.spec.ts
```

- CRUD operation resolution:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/crud-operation-resolution.service.spec.ts
```

- analytics schema and stats request materialization:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/analytics-schema-contract.service.spec.ts --include=projects/praxis-core/src/lib/services/analytics-stats-request-builder.service.spec.ts
```

- schema catalog and exact-href capability discovery:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts
```

Prove catalog query serialization, configured-origin resolution, exact capability-href following, and the full typed stats/catalog payload projection. Do not claim `/schemas/filtered` ETag behavior for catalog or capability calls unless those endpoints independently publish that contract.

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
