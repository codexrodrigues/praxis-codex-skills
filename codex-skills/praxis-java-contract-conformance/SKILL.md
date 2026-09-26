---
name: praxis-java-contract-conformance
description: Use when auditing a Praxis Java resource or host before migration/API handoff: verify OpenAPI, filtered/catalog/domain schemas, x-ui, ETag and X-Schema-Hash, RestApiResponse _links, structured errors, filters, option sources, actions, surfaces, collection/item capabilities, stats/export, sanitized evidence, and Angular runtime readiness through GenericCrudService, SchemaMetadataClient, ResourceDiscoveryService, forms, tables, or analytics consumers.
---

# Praxis Java Contract Conformance

Use this as the final proof gate for an implemented resource. It does not replace
the focused implementation skills; it assembles their evidence and reveals which
contract edge still prevents a migration-ready API.

## Build A Resource Evidence Pack

Start with one resource key and canonical path. Inspect its controller, service,
mapper, DTOs, filters, actions, surfaces, option descriptors, errors, tests,
HTTP examples, direct Angular consumers, and any legacy parity artifact. Record
the operation matrix before running tests.

For every failure, classify it as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. A conformance failure is
not permission to add a frontend alias, duplicate endpoint, second schema, or
host-local metadata map. Locate and fix the canonical owner.

Read [conformance-evidence-matrix.md](references/conformance-evidence-matrix.md)
to select only the evidence required by the resource's actual operations.

## Audit In Levels

1. **Static:** resource identity, canonical path, selected resource base,
   operation-specific DTOs, mapper/service wiring, annotations, governance, and
   explicit commands are coherent. A read-only resource must not claim writes;
   a mutable resource must not hide workflows in generic updates. For shared bulk
   lifecycle handlers, inspect `@BulkResourceOperations` and each handler's
   `@BulkResourceOperation` role. The five declared IDs must bind to one real MVC
   handler each; do not infer them from Java names, labels, or paths. For a bulk
   domain command, also inspect the real `@WorkflowAction` confirmation handler's
   `@BulkOperation` binding and verify that its distinct evaluation operation is
   a body-bearing POST handler in the same resource controller. Confirm atomicity
   matches the workflow declaration; an orphan or invalid binding must fail closed.
2. **Schema:** `/v3/api-docs`, `/schemas/filtered`, `/schemas/catalog`,
   `/schemas/domain`, `/schemas/surfaces`, and `/schemas/actions` agree on
   resource key/path/group, operations, schema references, `x-ui`, option
   sources, field access, and discovery. Catalogs and capabilities are never
   accepted as alternate structural schemas. For shared bulk lifecycle handlers,
   confirm `requireResourceOperation(resourceKey, operationId, method)` returns
   the expected `CanonicalOperationRef`, the exact named group document preserves
   that identity, and every currently published group is inspected for rewrites
   or collisions in paths, callbacks, and webhooks. A group fetch that falls back
   to the ungrouped document is not proof that the named group exists; unavailable
   or uninspectable groups must fail closed. Read the group set at validation time
   when groups can be registered dynamically. Ensure later schema readers consume
   the same exact-group snapshot validated by the resolver, never a stale cached
   base-document fallback. This binds operation identity only;
   it does not prove a provider, action/capability projection, or executable
   readiness. For bulk confirmation/evaluation, validate both request and response
   schemas from that same snapshot. The operation binding alone does not prove
   schema validity, provider/infrastructure wiring, a durable descriptor, or `READY`.
3. **HTTP:** exercise filter/get/write/action/export/stats operations that exist;
   verify `RestApiResponse._links`, structured error shape, validation errors,
   status semantics, ETag, `If-None-Match`, and `X-Schema-Hash`. Capture only
   sanitized evidence; never publish database, package, token, session, SQL, or
   provider-context details.
4. **Availability:** compare collection and item `/capabilities`, action and
   surface catalogs, and `_links` in both allowed and denied states. Verify that
   item decisions use the shared resource state snapshot and remain fail-closed
   where protected.
5. **Runtime readiness:** trace each published contract to its real Angular
   consumer. `GenericCrudService` consumes resource/schema/filter/option paths;
   `SchemaMetadataClient` and `fetch-with-etag` consume ETag/hash semantics;
   `ResourceDiscoveryService` follows `_links` for surfaces/actions/capabilities;
   forms, tables, and analytics consume the matching normalized metadata. Do not
   require building a new screen, but do require that an existing official runtime
   path can materialize the contract without custom consumer rules.
6. **Persistence/parity:** when the resource is legacy-backed, prove a scoped
   development mutation or read path as appropriate, preserve before/after
   evidence, cleanup/rollback plan, and parity result. Do not claim parity merely
   from a matching DTO name or one happy-path row.

## Scope Evidence To Existing Operations

Only audit option-source filter/by-ids, actions, surfaces, stats, export, field
access, related resources, or config materializations when the resource publishes
them. Conversely, every published feature needs its matching proof. Do not mark
a resource conformant because unrelated broad tests are green.

Public contract changes require focused starter tests, quickstart HTTP proof when
available, and affected Angular specs. Use source-local `AGENTS.md` commands;
prefer focused tests over broad suites. Review docs, corpus, examples, and
playgrounds only when they publish the changed contract.

## Bulk Protocol Input Proof

When reviewing the Metadata `org.praxisplatform.uischema.bulk` package, first read
`docs/spec/BULK-PROTOCOL-INPUT.md` in the exact starter revision being tested.
Distinguish an available Java input SDK from advertised HTTP/discovery and from
an executable, durable operation. Parser tests alone do not certify proposals,
fingerprints, idempotency, authorization, atomicity, recovery, or Angular readiness.

Prove `BulkProtocolReader` against original JSON bytes before any DTO/Map coercion:
Long IDs use canonical decimal strings, Integer IDs use int32 tokens, and SET,
CLEAR, omission, duplicates, unknown transport fields and limits stay distinct.
`BulkIdentityCodec.wireSchema()` is a fragment; only a real operation binding can
prove its projection into OpenAPI and `/schemas/filtered`. Require typed and
validated domain parameter/filter readers; structural allowlists do not authorize
an actor or validate aggregate rules. The HTTP adapter must also bound stream
reading before allocating the body.

Run `BulkProtocolContractTest`, `BulkIdentityCodecTest` and
`BulkFieldChangeValidationTest` when these files exist in the candidate; inspect
reports rather than treating a selector as proof. Validate the exact candidate
JAR in the direct consumer using an isolated Maven repository and explicit
candidate version. Existing host HTTP tests prove regression, not new bulk HTTP
behavior. Do not mark later lifecycle phases complete because this input gate
passes, or publish corpus calls to endpoints absent from the candidate. A focused
consumer regression gate does not replace the later independent consumer fixture
that proves the complete executable protocol. Programmatic decimal changes must
use exact decimal nodes; reject binary Float/Double values that may already have
lost precision.

## Bulk Snapshots And Result Schemas

For `BulkIntentSnapshot`, `BulkProposal`, `BulkExecution` or `BulkItemResult`,
read Metadata `docs/spec/BULK-PROTOCOL-RESULTS.md` and the exact revision of
`docs/spec/bulk-protocol.schema.json`. Extend the input gate with
`BulkIntentFingerprintTest`, `BulkResponseContractTest` and `BulkProtocolSchemaTest`.
Inspect fixed reference vectors for the versioned framing, context/operation/codec
binding, set normalization, ordered items/business arrays, exact decimals, deep
copies and bounds before defensive allocation. Preserve the published hash
algorithm: changing canonicalization without a migration invalidates persisted
fingerprints even if equality-only tests remain green.

A digest of evaluation intent does not bind a future frozen QUERY manifest,
proposal identity or durable receipt by itself. Require those additional bindings
in storage/execution proof; do not claim idempotency from SDK tests. Keep protected
intent separate from an explicitly redacted public preview. Constructors validate
shape/invariants, not authorization or redaction. Diagnostics use the canonical
message type with empty metadata; evidence references expose only authorized data.

Compare Java-valid outputs with each concrete identity schema, including optional
operation groups, string IDs containing spaces, all three request modalities,
reserved parameter names, status/count constraints and decimal round-trips. Use
an isolated mapper with JavaTimeModule, ISO dates, USE_BIG_DECIMAL_FOR_FLOATS and
STRIP_TRAILING_BIGDECIMAL_ZEROES disabled for response JSON; do not alter global
Jackson. Pending differs from NOT_PROCESSED; terminal executions cannot retain
pending/unknown, and RECONCILIATION_REQUIRED is not terminal. Public output types
are not proof of persisted proposals, schema discovery or executable endpoints.

## Bulk Editable Field Compilation

For `@BulkEditable`/`BulkEditableFields`, read Metadata
`docs/spec/BULK-EDITABLE-FIELDS.md` in the exact candidate. Require the update DTO and
resolved schema of the real operation, configured Jackson naming, actual OpenAPI
SpecVersion and trusted wire names for identity/version/workflow protections. Never
supply a client-controlled allowlist or infer protection from a conventional field name.

Prove `BulkEditableFieldsTest` with isolated ModelConverters/CustomOpenApiResolver,
renaming, naming strategy, inheritance/records, hidden/read-only fields, both update
modes, immutable sets, and application through `BulkFieldChanges`. Explicitly test
CLEAR under V30/V31, Bean Validation on accessors, Jackson null policies and rejected
unresolved schema composition. A model-conversion test is not an HTTP evaluation
schema or bootstrap proof. Keep those registry/provider gates open, and run the
existing consumer HTTP regression with the exact isolated candidate artifact.

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
Compare the resolved schemas with `SchemaCanonicalizer`. It intentionally preserves metadata
such as descriptions, examples, and `x-ui`, so equality is conservative and
metadata drift blocks reuse. A future structural fingerprint must directly include
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

## Prove PostgreSQL Bootstrap With An Empty Binary Cache

For PostgreSQL integration or starter release evidence, an isolated Maven repository
does not imply an empty extracted-binary cache. Preserve `EmbeddedPostgresColdStartTest`
in Metadata: use a new working directory and a distinct binary resolver instance so
Zonky's process-wide resolver cache cannot bypass extraction; start the real database,
query it, and close it before temporary-directory cleanup. Do not clear shared caches
or disable PostgreSQL tests to hide bootstrap failures.

When bootstrap fails with a missing method, inspect the resolved dependency tree and
upstream POM requirements before blaming the OS. Align existing Commons Lang/Compress
dependencies in their canonical Maven owner, including compile/runtime where applicable;
a test-only override can leave consumers broken. Reproduce the failing cold path,
then run the relevant release gate. During host adoption, inspect its actual resolved
versions: a direct dependency or BOM can override the starter's published choices.
Record cold-path proof separately from cached database tests and artifact availability.

## Report Without Ambiguity

Return an evidence pack containing:

- identity and operation matrix;
- status for `static`, `schema`, `http`, `availability`, `persistence/parity`,
  and `angular-readiness`: `pass`, `not-applicable`, `blocked`, or `fail`;
- source files, endpoints, fixtures, commands, and sanitized outcomes;
- canonical owner and classification for every non-pass result;
- derived-artifact decision, remaining risk, and exact next action.

`blocked` is only valid when an external prerequisite is unavailable and the
remaining local checks were exhausted. `not-applicable` must name the absent
published operation. Never use either label to hide an untested public claim.

## Preserve Canonical Ownership

- `praxis-metadata-starter` owns resource metadata, schemas, discovery,
  capabilities, `_links`, HTTP metadata headers, and their conformance rules.
- `praxis-config-starter` owns governed config/authoring contracts; a resource
  audit may verify materialization but must not redefine config semantics.
- `praxis-ui-angular` owns runtime materialization; conformance checks consumers
  rather than creating a competing UI contract.
- Quickstart and HTTP corpus provide operational proof and do not become owners.

Do not decide resource scope, operation, action, surface, or consumer path with
keyword routing, regexes, label matching, or route-string guesses. Ground it in
resource keys, canonical schemas, links, action/surface IDs, capabilities, and
declared runtime contracts.

## Companion Skills

- `praxis-java-resource-authoring`: implementation and resource operation matrix.
- `praxis-java-filter-query-authoring`: filter/query proof.
- `praxis-java-option-source-provider-authoring`: external option source proof.
- `praxis-java-availability-discovery-authoring`: action/surface/capability proof.
- `praxis-metadata-schema-contracts`: schema, OpenAPI, ETag, and hash semantics.
- `praxis-api-quickstart-cockpit-http-validation`: HTTP/cockpit evidence.
- `praxis-core-resource-runtime`: Angular runtime materialization.

Close only when the evidence pack shows a resource can be consumed canonically by
the intended runtime, or when every remaining gap has a named owner and an
explicit follow-up. Compilation alone is not conformance.
