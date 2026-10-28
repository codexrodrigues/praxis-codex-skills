# Bulk Discovery Composition And Governed Photograph Boundaries

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

For `DOMAIN_COMMAND/ATOMIC` composition published in Metadata `8.0.0-rc.152`, inspect the real `@WorkflowAction`,
its action-registry binding, typed parameters, and `BulkOperation` declaration
before projecting discovery. Their atomicity must agree; the exact provider,
confirmation operation and seven canonical references must resolve in the same
published photograph. Preserve the action identity and request/response schemas;
do not manufacture a CRUD capability or editable fields for a command. The
operational profile remains `EXPLICIT`/`SYNC`, at most 50 targets, an aggregate
unit deadline no greater than five seconds and any stricter action `maxItems` limit. A mismatch
fails closed. The published composition does not establish a host command
provider, executable HTTP route, domain authorization, outbox, `READY`, or
public adoption; prove those separately against the exact published artifact.

`ActionCatalogService` must assemble each synchronous response inside the lifecycle's response scope while keeping contextual availability outside document-cache and preparation locks. Resource, group, item and collection entrypoints preserve the original action definitions, principal and availability contexts. Reuse only the structural descriptor captured for that response; `execution.bulk` is descriptive evidence and never a readiness or authorization token.

Scoped `requireReady` must recheck namespace/operation, current provider composition and the durable READY row against the captured generation, fingerprint and structural revision. It may reuse the structural snapshot, but must not memoize availability or share that scope across requests, threads or asynchronous continuations. Suspend/republish with identical content still changes the generation and must reject the old response.

After leaving fresh preparation, use the concrete ephemeral snapshot read fence to bound short read-lock acquisition by the original composition deadline and check cache epoch and transport revision before and after provider/durable reads. Capture from an actual prepared or installed published photograph while inside its structural read phase; dispose the fence and private response frame in `finally`. Never retain a public cache lock or a JDBC transaction around host rules or the response builder.

For non-bulk capability and related-resource discovery, inspect
`DefaultCapabilityService`, `SurfaceCatalogService` and the document-aware
five-argument auto-configuration wiring. With a local governed photograph,
resolve structural flags and operations from the same document in a short phase;
resolve each related resource once per `childResourcePath`, then detach private
projections. Check
the presence hint inside that phase, not only before lock acquisition. Run host
state/availability callbacks after document/preparation locks and JDBC scopes
have closed, and check existing parent/child read fences after the callbacks.
Preserve genuine legacy getters, constructors and caller transaction boundaries;
do not add a mode, TTL, READY cache or cached live role/ACL authority. A publication
failure must fail closed, not become a silently unsupported child. Guard counts
are scenario-specific; a selected no-database method in a mixed PostgreSQL test
class does not make the whole class eligible for the release no-db inventory.
`DiscoveryPublishedPhotographTest` and the selected compiler seam establish
structural/callback boundaries, not Neon IAM, throughput or hosted HTTP acceptance.

Preparation failure may invoke the builder once with an empty bulk projection and a denying scope. Once the builder starts, its exception or a failed final coherence check must propagate; do not repeat the builder or convert its failure into a second composition. Always run the final fence/provider/durable check after the builder returns, including when a host rule caught a readiness exception and returned denied.

Prove all four catalog entrypoints, exception cleanup, independent following requests, cache/transport changes (including transport replacement/restoration), deadlines, thread confinement, provider changes and durable generation changes. The concrete multigroup HTTP proof must preserve the authorized bulk body and references while demonstrating one fresh composition per catalog or collection-capabilities GET. A selective proof does not certify the complete backend, load performance or the full HTTP campaign.

