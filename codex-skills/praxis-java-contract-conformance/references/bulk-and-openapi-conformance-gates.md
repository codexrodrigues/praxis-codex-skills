# Bulk Protocol, Artifact Provenance, Strict OpenAPI, And Cold-Start Conformance Gates

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

## Independent Artifact Proof Provenance

Before accepting `BulkConsumerArtifactIntegrationTest`, inspect its archive source:
`archiveCommittedCandidate` builds production from Git `HEAD`, not dirty `src/main`
or the caller's compiled classes. Commit the intended production/POM before this
proof, or use a clean checkout of that exact commit; preserve unrelated local drift.
Verify `candidate.gitRevision`, `candidate.gitSrcMainTree`, `candidate.gitPomBlob`,
JAR/POM hashes and the copied consumer fixture hash in
`target/b1f-consumer-artifact-evidence.properties` against the intended tree. A green
suite or matching working-tree hashes cannot substitute for these identities.
The provenance guard must reject changed tracked production/POM and non-ignored
untracked production before archiving;
checkout line endings alone may be ignored. Prove that rejection with a real temporary
Git repository, without changing global Git configuration or weakening the artifact gate.

When lifecycle DDL changes, migrate the independent fixture too: narrow grants to
the current function signatures and runtime/control-plane roles, retain cold reads
as unavailable, and publish through the real HTTP/nonce path before structural reads.
Do not seed a fictional READY photograph, bypass the failing consumer test, rerun an
unchanged failed tag or move a release tag. If release validation fails before upload,
record the failed run and actual registry availability separately, correct and review
the fixture, then obtain any required authorization for the next immutable version.

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

Use `CanonicalOperationResolver.requireResourceOperations(resourceKey, operations,
snapshot)` to bind the whole set to strict MVC mappings and globally published
OpenAPI identities without fetching the captured group again. The five lifecycle
roles are bodyless at both layers: after binding, call
`snapshot.requireNoRequestBody(operation)` for each lifecycle operation. An MVC
handler with no `@RequestBody` is insufficient because an OpenAPI customizer can
add one. The resolver normalizes only the same structural route when groups rename
template variables; a changed ID on that target route or a duplicate elsewhere
still fails closed. Evaluation and confirmation retain their DTO and schema checks
against the same snapshot.

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

For the private bulk-candidate batch/index path, first prove the exact candidate
JAR/version with a distinct coordinate; Metadata rc.154 does not publish this path.
Where that candidate supplies `requireResourceRequestBodies`, pass the ordered
operation references, one exact-group snapshot and the configured `TypeFactory`.
Require an immutable result with exactly one binding per requested operation in
the same order, and recheck each current MVC handler and full generic body type;
the batch is no authority or body-type cache. Its publication-local document index
must cover every published group, including paths, callbacks and webhooks, and
reject global operation-ID ambiguity or a changed identity at an aliased route.
If the resolver does not implement the strict batch, fail closed; repeated singular
or permissive lookups are not an equivalent substitute.
The selected snapshot must retain its document-service source and equal the full
published group document under the candidate/generation guard; digest or group
name alone is insufficient. An alias callback receives a defensive paths copy
and cannot mutate the index. Prove these boundaries with the exact candidate's
focused tests and host binding, without treating passing SDK tests as HTTP 200,
durable `READY`, authorization, or throughput evidence.

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

