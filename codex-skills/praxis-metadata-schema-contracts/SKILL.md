---
name: praxis-metadata-schema-contracts
description: Use when Codex must work on praxis-metadata-starter structural schema contracts: x-ui, /schemas/filtered, /schemas/catalog, /schemas/domain, OpenAPI operation resolution, schema references, ETag, X-Schema-Hash, schemaId/schemaUrl, docs/spec schemas, or Angular schema consumption.
---

# Praxis Metadata Schema Contracts

Use this skill for the canonical structural schema surface of `praxis-metadata-starter`. This starter publishes backend semantic grounding for Praxis runtimes and AI authoring; it is not merely a JSON-schema generator for Angular components.

## Source Audit

Inspect the owner before editing:

- `praxis-metadata-starter/AGENTS.md`
- `praxis-metadata-starter/README.md`
- `src/main/java/org/praxisplatform/uischema/controller/docs/ApiDocsController.java`
- `src/main/java/org/praxisplatform/uischema/controller/docs/DomainCatalogController.java`
- `src/main/java/org/praxisplatform/uischema/controller/docs/SemanticDomainCatalogController.java`
- `src/main/java/org/praxisplatform/uischema/openapi/OpenApiDocumentService.java`
- `src/main/java/org/praxisplatform/uischema/openapi/CanonicalOperationResolver.java`
- `src/main/java/org/praxisplatform/uischema/schema/SchemaReferenceResolver.java`
- `src/main/java/org/praxisplatform/uischema/schema/FilteredSchemaReferenceResolver.java`
- `src/main/java/org/praxisplatform/uischema/hash/**`
- `src/main/java/org/praxisplatform/uischema/http/IfNoneMatchUtils.java`
- `docs/spec/**` and `docs/guides/**` when public contract or narrative changes

## Canonical Boundary

`/schemas/filtered` is the structural source of truth. It owns operation-specific schema shape, `properties.*.x-ui`, `x-ui.resource.idField`, `x-ui.resource.capabilities`, `schemaId`, `schemaUrl`, `ETag`, and `X-Schema-Hash`.

`/schemas/catalog` is a derived documentary/discovery projection over OpenAPI. It enumerates candidate endpoints and publishes group/resource presentation, operation summaries/examples, and request/response schema links. Its `resourceKey`, `path`, and `method` can scope subsequent discovery, but catalog presence is not structural schema truth, authorization, or current capability proof.

Capabilities are a contextual availability snapshot. They aggregate canonical operation flags, stats field eligibility/metrics, actions, surfaces, and stable `resourceKey` plus operational `resourcePath`; they do not redefine property structure. `/schemas/domain`, `/schemas/surfaces`, `/schemas/actions`, and capabilities may reference schemas, but none may replace or inline a second version of the filtered schema payload.

Use canonical operation resolution from OpenAPI before inventing endpoint maps. `path + operation + schemaType` should resolve through `CanonicalOperationResolver`, `OpenApiDocumentService`, and `SchemaReferenceResolver`.

For `/schemas/filtered`, `schemaId`, `schemaUrl`, `ETag`, and `X-Schema-Hash` are one structural evidence chain. Any new structural dimension such as `includeInternalSchemas`, `idField`, `readOnly`, `operation`, or `schemaType` must be reflected consistently in `FilteredSchemaReferenceResolver`, `ApiDocsController`, schema hash calculation, conditional request handling, docs/spec examples, and Angular cache consumption.

Do not transfer that conditional-cache contract to `/schemas/catalog`, capabilities, surfaces, actions, or domain catalogs by association. A consumer must use `If-None-Match`, 304 handling, or a schema hash only when the exact endpoint independently publishes those headers and semantics. Where an endpoint does not, a bounded consumer TTL is an operational policy, not inherited structural evidence and not a substitute for capability refresh.

Surfaces/actions/capabilities should reference canonical `schemaUrl`/`requestSchemaUrl`/`responseSchemaUrl` values produced by the resolver. They must not reconstruct schema URLs by concatenating paths, copy inline schema fragments, or treat a `schemaId` from another structural variant as equivalent.

The convenience `SchemaReferenceResolver.resolve(CanonicalOperationRef, schemaType)`
does not itself infer the `idField` or `readOnly` values that `/schemas/filtered`
derives from the selected UI schema and operation. For a published descriptor that
embeds a `CanonicalSchemaRef`, do not assume this syntactic default resolves to the
same identity variant the endpoint serves. Derive the selected component, `idField`,
and `readOnly` from the same immutable OpenAPI snapshot used to compose the descriptor,
share that projection rule with `/schemas/filtered`, and call the resolver with those
explicit dimensions. Validate the complete `schemaId`/type/URL tuple by fetching the
published URL and comparing it with the returned UI variant; include ETag/hash checks
when the endpoint publishes them. Derive these values per operation role: a workflow
confirmation schema does not supply the identity defaults for its evaluation, proposal,
execution, or result DTOs. Keep the raw HTTP response schema as a separate transport
contract and fingerprint input. If the same selector/default derivation cannot be
shared faithfully, do not publish the embedded reference until the contract is redesigned.

When a consumer receives `schemaUrl`, `requestSchemaUrl`, or `responseSchemaUrl`
from surfaces/actions/capabilities, treat that URL as the canonical structural
reference for the already-resolved operation variant. Consumers may resolve the
href against their configured API origin, but must not rebuild the query string,
swap `schemaType`, reuse a response `schemaId` as a request schema, or infer a
different operation from `resourcePath`. If the published URL is missing or
wrong, repair `SchemaReferenceResolver`/`FilteredSchemaReferenceResolver` or the
metadata publication that produced it.

For durable bulk-operation composition, the action registry's references are
canonical projections of its `CanonicalOperationRef`: they include the resource
`idField` and `readOnly=false`, so they are intentionally not byte-equal to the
generic OpenAPI operation references. Validate the action references by resolving
the full schemaId/type/URL tuple through the same `SchemaReferenceResolver` for
that exact action operation and variant. Do not loosen operation, resource,
workflow, group-snapshot, or seven-binding identity checks to accommodate the
projection.

The canonical OpenAPI response reader may preserve a bounded, non-empty `oneOf`
only on response schemas when a real wire response has object-or-array shape
(such as repeated HATEOAS links). Resolve each variant recursively from the same
strict group snapshot and preserve the `oneOf` operator in structural evidence.
Request schemas remain composition-free; empty/malformed variants, cycles,
external references, and exceeded depth/node/byte budgets fail closed. When an
action schema reference or response schema enters a durable structural
descriptor, include it in the versioned digest. Changing digest inputs requires
a new framing version and focused sensitivity tests; the durable lifecycle must
suspend/recompose and pass its current CAS fence before readiness can be
republished.

## Strict Canonical OpenAPI Reading

Read Metadata `docs/spec/CANONICAL-REQUEST-SCHEMA.md` before composing a
resource operation. For the S4c composition path, obtain the named group only
through `OpenApiDocumentService.getDocumentForGroupStrict(group)`. Never call
`getDocumentForGroup` here: its ungrouped fallback cannot prove that the named
group exists. Resolve each declared operation explicitly by resource, operation
ID and method against that exact document.

Capture one immutable exact-group document snapshot for a descriptor and pass it
to every request and response reader used for its operations. Do not refetch the
seven operations independently, and do not treat a cache entry or a later cache
lookup as that snapshot. Cache invalidation, group replacement, or publication
failure requires rejecting or suspending composition until one complete snapshot
can be captured again. `/schemas/filtered` remains the UI projection and
`SchemaReferenceResolver` remains its identity/URL owner; neither replaces this
backend compilation snapshot.

For governed bulk descriptor publication and readiness, compose from an isolated fresh snapshot of the complete published OpenAPI group collision domain; refreshing only the target group leaves duplicate operation IDs in cached non-target groups undetected. Do not replace shared cached group documents while one operation remains READY. When
the bulk lifecycle is active, `OpenApiDocumentService` must install and enforce its
durable invalidation guard for both public cache-clear and strict-refresh calls.
Implementations that cannot enforce the guard fail closed. Lifecycle publication and readiness must read a fresh isolated all-groups snapshot without replacing shared OpenAPI caches; serialize this composition against local invalidation. Return defensive copies of cached JSON trees so callers cannot mutate a shared document behind the fence. The canonical Springdoc
source caches its generated description by default; hosts that activate governed
bulk lifecycle must set `springdoc.cache.disabled=true` and retain strict exact-group
fetching with no fallback. HTTP `Cache-Control` revalidation alone does not bypass
Springdoc's calculated-description cache. Never let a host call a lower-level cache
API to skip the durable suspension signal.

For the official multigroup composition, keep HTTP preparation outside the public
cache write lock. Serialize preparations separately, capture local invalidation epoch
and public entries under short read locking, then recheck epoch and public/fresh parity
under the write lock before installing complete cold entries and invoking the callback.
A clear/refresh attempt advances the epoch even if its durable guard fails. Do not
confuse that local epoch with upstream authority or use it to cache the source forever.
Cold preparation must independently fetch ordinary public and fresh documents; never
install fresh merely to compare it to itself. Keep the complete published collision domain.

Inspect `OpenApiInternalRestTemplate` and the official client bean. Defaults are
`praxis.openapi.http.connect-timeout=1s`, `praxis.openapi.http.read-timeout=10s`
(complete HTTP response, headers and body), and
`praxis.openapi.bulk-composition-timeout=60s` (aggregate preparation/admission).
Use positive Duration values in the supported millisecond range. The shared JDK client
waits for the complete response with the smaller request/remaining budget, requests
best-effort cancellation, and must not follow redirects. An opaque host RestTemplate
or replaced factory cannot silently prove bounded fresh composition. Prove factory
swap/restore rejection and preserve legitimate interceptors/error handlers; those
custom hooks are not covered by a forced cancellation guarantee.

Recheck admission after obtaining the control-plane connection and before the actual
READY transition. Distinguish failure before attempting CAS from uncertain confirmation
after the attempt: a pre-CAS timeout must not reconcile another publisher's READY as its
own success. Do not check expiration after a confirmed READY and convert its effect to
failure. If drift is already known under the write lock, perform the durable guard before
cache eviction even after new-admission budget expiry; guard/pool/transaction/reconciliation
have their own bounds. Explicit strict refresh retains its historical exclusive section;
this change does not prove every cache fill or business operation has a hard wall-clock
bound or that server-side work stops when the client cancels.

Prove off-lock readers, epoch clear/refresh races, cold parity, failed guard, timed
preparation/write-lock waits, slow headers/body, factory replacement and pre-CAS failure
with focused composition/transport/lifecycle tests. Then run the identified candidate JAR
against the real host 53-group diagnostic before the workflow HTTP suite. A diagnostic
with a local observer does not prove PostgreSQL suspension, execution, readiness or
release adoption; record candidate, integrated, published and adopted states separately.

Every shared OpenAPI-document and schema-hash cache fill must participate in the
same read-lock/epoch protocol as invalidation. A fill that began before a clear
must not repopulate a stale document or hash after the clear completes. The
standard Springdoc freshness capability rejects any configured external
`app.openapi.internal-base-url`; custom `OpenApiDocumentService` implementations
may opt in only with independent freshness proof, rather than relying on
`Cache-Control` headers.

Governed bulk lifecycle requires two distinct proofs from an
`OpenApiDocumentService`: `supportsFreshBulkLifecycleComposition()` and
`supportsFreshBulkLifecyclePublicCacheCoherence()`. The latter must compare the
fresh exact-group snapshot with the documents the public `/schemas/filtered`
endpoint actually serves before invoking readiness, publication, or action
projection callbacks. If any public cached document differs, call the durable
invalidation guard first, clear document and schema-hash caches only after the
suspension commits, then fail closed. Do not return `READY`, invoke the callback,
retry publication, or synthesize a new generation automatically; an operator or
governed host flow must explicitly recompose and publish against the new CAS
generation. A custom implementation's default `false` capability is not proof.

Treat `getDocumentForGroupStrict` as a read, not an implicit refresh. A cold
strict load is supported; promotion of a public non-strict entry must preserve
the identical document. Reject a different exact document before changing
public JSON or cached hashes. Use the existing guarded explicit refresh or
invalidation path for replacement, followed by lifecycle republication where
required. Never upgrade a read lock while an HTTP schema materialization holds
its enclosing read lock. Prove changed-source rejection, identical promotion,
cold strict loading, and the existing guard/hash refresh behavior with
`CachedOpenApiDocumentServiceStrictPromotionTest` and
`CachedOpenApiDocumentServiceRefreshTest`.

The standard `/schemas/filtered` path must hold the shared cache read lock from
operation/schema selection through document materialization and hash/ETag/304
response creation. Strict document replacement and hash invalidation use the
exclusive side of that same lock, so an in-flight old request cannot repopulate
a stale hash after suspension. Verify this property at the actual controller
callsite, not only in a cache unit test. When query selectors such as `idField`
contain a literal plus, encode it as `%2B` (and spaces as `%20`) so servlet query
decoding preserves the same selector and `schemaId`; prove URL, response body,
schema hash, ETag, and conditional 304 agree.

For each request, require the declared 3.0/3.1 dialect, exactly one JSON
representation of `application/json` or `application/<subtype-token>+json`, where
the subtype token uses valid ASCII `tchar` characters. Reject wildcard media
types, parameters, whitespace, invalid Unicode, unsupported composition, cycles,
reference siblings, external references, custom dialects, and ambiguous content.
Defaults, examples, descriptions, and `x-ui` remain literal schema data; do not
flatten `allOf` by dropping constraints.

For each successful response, inspect every explicit final status in `200` through
`299`. `default`, `2XX`, and other status ranges do not establish success, and a
non-2xx response never proves it. Every accepted 2xx response needs exactly one
media type from that same JSON allowlist and one resolvable schema. Limit
resolution to the same local component references and bounds as request reading;
reject missing, external, cyclic, sibling, or ambiguous references and content.
Request schemas remain composition-free. Response schemas may preserve only a
non-empty `oneOf` list whose every variant resolves recursively against the same
snapshot; keep the operator and variant order in the canonical schema, and reject
non-array or empty `oneOf` lists, invalid variants, composition operators other
than `oneOf`, cyclic or external refs,
and depth/node budget violations. This supports canonical response shapes such as
`RestApiLinks`, where one relation serializes as one link object or a list when
multiple links share that relation. Never flatten or remove this `oneOf` in a host.
Compare the resolved schemas with `SchemaCanonicalizer`. It intentionally preserves metadata
such as descriptions, examples, and `x-ui`, so equality is conservative and
metadata drift blocks reuse. The structural fingerprint must directly include
the ordered `(status, media type)` variants and the complete shared canonical
schema. A schema-hash cache is an optimization only and is never fingerprint
authority.

The self-HTTP source must run after the server/document is available. This
structural binding does not prove startup readiness, provider availability,
authorization, capability/action projection, or an executable bulk registry. Use
`CanonicalOperationResolver.requireResourceRequestBody` with the configured
`mapper.getTypeFactory()` to obtain the operation and actual MVC body type,
including controller/interface generics. The binding does not certify custom
converters or arbitrary SpringDoc overrides. Keep the required concrete DTO
subset and fail on raw, wildcard, or optional bodies instead of guessing a class.
A bulk evaluation wrapper is not the unit update DTO; never infer the latter from
method names or the first PUT/PATCH operation.

Prove strict no-fallback group loading, one shared immutable snapshot, request
schema reading, and every explicit 2xx response tuple in focused reader and HTTP
fixtures. Include rejected `default`/`2XX`, non-2xx-only, missing or ambiguous
content, unsupported refs, and metadata-only schema differences. Then regress
`OpenApiDocsSupport`/`ApiDocsController` and the exact candidate JAR in
Quickstart. The HTTP fixture proves schema compilation, not persistence,
authorization, or bulk execution.

## Decision Rules

- Do not fix missing schema semantics in Angular, quickstart, HTTP examples, or docs when the canonical source is the starter.
- Do not add parallel endpoints for request/response schema variants when `/schemas/filtered` plus canonical operation resolution can express them.
- Keep `schemaId` and `schemaUrl` aligned when adding structural dimensions such as `includeInternalSchemas`, `idField`, or `readOnly`.
- Preserve the request/response boundary. Workflow actions and writable
  surfaces must use `requestSchemaUrl` or request `schemaUrl` for form inputs
  and may carry `responseSchemaUrl` only as response evidence. Read projections
  and view surfaces use response schemas. Do not let an Angular adapter or host
  choose the variant by inspecting method names, labels, widget mode, or local
  URL conventions.
- If `ApiDocsController` changes, review cache headers, `ETag`, `X-Schema-Hash`, `If-None-Match`, and exposed headers in the same pass.
- If `/schemas/catalog` or capabilities are consumed for authoring, keep their roles separate: catalog enumerates candidates, an exact published capabilities href proves current operation/field eligibility, and `/schemas/filtered` supplies structural property metadata. Do not infer one surface's freshness or authority from another's headers.
- If `x-ui` shape changes, review `docs/spec/*.schema.json`, examples, conformance docs, Angular consumers, and quickstart downstream tests.

Reactive Determinations are operation-specific `x-ui` operation metadata,
compiled from the canonical definition registry. Preserve stable identity,
form/trigger modes, typed input/output bindings, and provenance. Do not
republish removed Form Effect annotations or a second form-owned schema.

## No Keyword Routing

Do not resolve resource, operation, schema, or field intent through keywords, regexes, aliases, or local fuzzy matching as the primary decision. Use canonical OpenAPI operations, resource keys, schema references, governed semantic catalogs, and declared tools for grounding; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding schema fields, headers, query params, endpoint variants, or resolver branches, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public schema contract. In that case name the missing data, canonical owner, consumers, derived docs/examples, and minimum validation.

## Validation

Use focused local gates:

- bulk structural composition and schema variants: `mvn "-Dtest=BulkOperationStructuralCompilerTest,CanonicalRequestSchemaTest,CanonicalResponseSchemaTest" test`
- docs/schema refs/hash: `mvn "-Dtest=ApiDocsControllerTest,ApiDocsControllerPathResolutionTest,ApiDocsControllerSchemaHashTest,DomainCatalogControllerTest,FilteredSchemaReferenceResolverTest,OpenApiCanonicalOperationResolverTest" test`
- quickstart downstream proof for public schema changes: `QuickstartMetadataMigrationIntegrationTest`, `EventosFolhaPilotIntegrationTest`, and `OpenApiGroupResolutionIsolatedIntegrationTest`
- Angular consumer proof when schema runtime changes: `schema-metadata-client.spec.ts`, `fetch-with-etag.util.spec.ts`, and `generic-crud.service.spec.ts`

Review `README.md`, `CHANGELOG.md`, `docs/index.md`, `docs/guides/**`, `docs/spec/CONFORMANCE.md`, `docs/spec/*.schema.json`, and `docs/spec/examples/**` when public schema semantics change. State why if no derived artifact is updated.

## Companion Skills

- Use `praxis-reactive-determinations` when schema metadata drives governed reactive form execution.

- Use `praxis-metadata-resource-baseline` for resource-oriented controller/service hierarchy.
- Use `praxis-metadata-discovery-capabilities` for surfaces, actions, capabilities, `_links`, availability, stats, and export discovery.
- Use `praxis-metadata-domain-option-sources` for `@DomainGovernance`, semantic domain catalog, option sources, field access, and entity lookup contracts.
- Use `praxis-api-quickstart-operational-proof` and `praxis-api-quickstart-cockpit-http-validation` for downstream HTTP proof of schema contracts in the reference host.
- Use `praxis-http-examples-contract-surfaces` when the public executable HTTP corpus for `/schemas/**`, headers, or schema examples is affected.
- Use `praxis-core-resource-runtime` for Angular consumption of these contracts.
- Use `praxis-landing-public-docs-contracts` and `praxis-landing-registries-sitemap-playgrounds` when public landing/docs, guides, sitemap, LLM files, examples, or playgrounds publish `/schemas/filtered`, `x-ui`, schema hash, or metadata grounding claims.
