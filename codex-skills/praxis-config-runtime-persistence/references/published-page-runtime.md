# Published Page Runtime

## Inspect The Owner And Adoption State

Config owns catalog identity, publication heads and operational resolution.
Inspect the exact candidate's `docs/ai/contracts/page-publication-p0/P3B-DESIGN.md`,
implementation report and evidence, `PageRuntimeReadService`, `PageRuntimeStore`,
`PageRuntimeCursor`, `UiLayoutNativeSnapshotReader`, `PageCreationHost`, runtime
navigation provider/controller, error handlers and auto-configuration. Check the
P0 native document and page/group lifecycle invariants before changing them.

The existing lifecycle/frozen evidence and context contracts are reusable;
generic effective composition also permits baseline/overlay behavior and is not
the published-page resolver. Do not repair an operational read by falling back to
a draft, baseline, personal configuration or another release. Inspect the actual
published artifact and host wiring separately before claiming an endpoint is
available in a consumer; source integration does not publish a package.

## Resolve One Authorized Publication

- Resolve authenticated actor/application/namespace/tenant/environment and the
  expected context version through existing host contracts. Caller hints, a
  cursor, an old menu or a catalog identity do not grant access. Correlate current
  audience and invocation without equating administrative unit and organization.
- Resolve catalog → current head → pinned frozen release. Reproduce the native
  KIND, captured B0 and exact patch; admit current producer, metadata, children
  and complete structure. READ_HEAD by itself does not run every creation bridge
  check. Historical capture identity is not current source/domain authority.
- URL requires the page's own READ_HEAD and matching assignment selector.
  Navigation additionally requires its registered groups root's visibility.
  Denying groups may hide the menu while an independently authorized URL remains
  valid; permitting groups never exposes a denied page. Preserve the existing
  root-level policy instead of inventing per-group ACLs or perpetual ancestral
  COPY_SOURCE grants.
- Repeat current context/audience, relevant grants and root mapping after the
  last extension, before body or 304 acceptance. A validation budget check alone
  is not a fresh grant read. Denied items may be excluded before public projection;
  corruption, unavailable source or deadline exhaustion must not become an empty
  list or a partial successful scan. External authority rechecks are not a
  distributed atomic revocation fence.

## Coherence, Paging And Conditional Reads

Use the actual Config transaction/JDBC/JPA connection and REQUIRED lifetime.
Flush the caller's legitimate JPA writes before both fresh JDBC head collections;
do not clear the EntityManager or refresh away pending state. Compare full scope
catalog/head vectors, including absent/withdrawn heads, insertions and head
ETag/version changes. Materialize the releases pinned by the first vector and
reject a changed second vector without an internal retry or renewed deadline.
Retain no mutable head, grant, context or negative lookup in an immutable cache.
The two collections establish the operation's read point. A later legitimate
write in an outer REQUIRED transaction must not invalidate that earlier read or
prevent read → write → read. Keep current authority/context/deadline checks until
completion, without pinning the earlier vector again at outer commit. A returned
participant receipt is provisional and describes its read point, not subsequent
writes or the transaction's final publication. Prove this ordering and external
rollback explicitly; do not introduce a registry of latest responses.

Keep the complete vector private. Public receipts and continuation digests derive
only from the authorized projection and its heads, not hidden IDs, counts or a
hash of the private vector. Preserve global group/binding order and cross-page
identity ties; an entry identity must include page and binding identity.
Lazy `children: null` does not assert whether private children exist.

Audit cursor format/length/closed fields before queries. The cursor is an untrusted
position, not a signed grant: recompute current visibility, bind scope/actor/
context/query/parent/page size, compare the authorized view and confirm the last
position is authorized. Stale continuation conflicts; never silently restart or
combine snapshots. Tampering may select another authorized position but cannot
admit a private item. Do not add a secret, cursor registry or second navigation
endpoint merely to authenticate a position.

Scan completeness precedes paging. Bound body batches and retained payloads;
do not sort only the first UUID batch, use OFFSET under READ COMMITTED or infer
the end from private items. Vector metadata and the scan can remain O(N).
Serialized workspace batching does not bound heap, patches or all ORM state.
Measure the actual fixture's SQL, elapsed time, bytes and managed retention;
reject deadline exhaustion rather than truncate or claim an unmeasured SLA.

## Prefetch Immutable Bytes Without Moving Admission

Inspect `ConfigTransactionReadSet`, `PageCatalogStore` and
`JdbcUiLayoutMetadataCaptureStore` before optimizing repeated evidence reads.
Feed the same store instance used by the creation/lifecycle adapters; a second
store owner will not warm their readset. Run the SQL loader inside the existing
transaction admission, with the same owner/holder/JPA-JDBC connection checked
before and after loading. Preserve mutation guards, suspension, completion and
savepoint rollback cleanup; a hit never renews the validation deadline.

Prefetch complete immutable raw rows, including every SQL column needed by the
original correlation, without parsing private documents or running semantic
codecs early. Preserve the existing order: mapping, delegate READ_HEAD, ledger
consumption, frozen document/selector, then matching metadata/source/structure
admission. READ_HEAD denial must prevent ledger and capture validation; selector
mismatch prevents capture admission but does not undo the earlier ledger check.
A physical metadata row key identifies stored bytes; it does not attest the full
source/descriptor/baseline binding. Recheck that binding and scope on every
admitted read, and create fresh mutable objects from retained strings. SQL or
connection failure remains a failure, never a cached miss.

Keep raw page-row and published-source snapshot key types distinct within the
shared catalog owner. Preserve application/tenant/environment/namespace/page
identity, with release/revision identity for a published snapshot; do not replace
these keys with ambiguous aliases.

Consume each selected prefix before prefetching the next. Bound both candidate
count and bytes before loading, and check actual UTF-8 envelope bytes before
retaining them; replacement must subtract the previous value. A missing or
oversized item must still advance through the existing individual loader when
its admission gates allow consumption, without being hidden, truncated or
retained as a negative result. Limits belong to each owner: ancestry may reach
additional stores, and neither their sum nor SQL text sizes establish a global
heap bound. Final authority checks may prefetch raw rows in windows only after
all mapping callbacks, preserving the final grant fence and fresh head vector.

Prove that corrupt private ledger/capture bytes leave the public projection and
receipt unchanged when their current gates deny consumption; admitting that
same source must still fail closed. Also prove a mismatching expected binding
on a raw-row hit, mutation isolation, eviction/reload, savepoint rollback and
current revocation after a hit. Compare measured SQL/getter costs and complete
admission before claiming capacity. A diagnostic test that accepts an unavailable
response after its budget is not a successful capacity gate.

Exercise real P2 creation from a PUBLISHED source as well as a native seed.
After publishing the destination, withdraw the source head and deny ancestral
READ_HEAD/READ_SOURCE/COPY_SOURCE. The independently admitted destination must
still resolve its own head in catalog, URL and menu; revoking its current
producer/domain admission must still deny it. This exercises the shared raw-row
and published-snapshot cache plus the extra metadata owner. A thousand native
pages do not prove capacity for a thousand ancestry chains.

## Conditional Validators

The semantic receipt excludes the changing `resolvedAt`, so these GETs require
weak HTTP ETag `W/"<receiptEtag>"` and weak If-None-Match comparison after current
authorization. Keep the stored head ETag strong for lifecycle If-Match/412.
Success is private/no-cache; errors are sanitized/no-store. Audit runtime's own
handler as well as Config advice: an advice scoped to layout controllers may not
cover runtime navigation or parameter conversion errors.

## Host And Recovery Boundaries

Keep `/api/praxis/runtime/navigation` as the sole navigation surface. A host
explicitly delegates its existing provider to Config; installing a page host
must not append menus or replace a custom provider. Missing providers fail
closed. A host that changes/composes the projection owns the receipt, ordering,
cursor and final authority checks of that final result; it cannot alter nodes
while retaining a fragment's receipt or continuation.
Validate the provider boundary too: require a nonblank node ID, preserve nullable
lazy children and reject null members in a present children list. Malformed
provider DTOs/receipts and invalid server-owned root identities are unavailable
sources (503), not caller cursor errors (400). Keep malformed client parameters
and conditional headers distinct and sanitized; prove both with If-None-Match
present so invalid output cannot escape as 304.

Recovery is pull revalidation of durable heads. Prove a lost commit response and
a fresh reader reconstruct the current publication; event UUID/time is not a
commit-ordered checkpoint. Do not claim outbox, push invalidation or a cache of
authority. A stale menu click must resolve the published URL again.

Core reuses context generation to reject obsolete navigation callbacks, including
A→B→A. Its minimal transport has no body cache/If-None-Match. A later client cache
needs explicit 304/body/revocation behavior. Renderer and routes are distinct
consumer integration gates, not consequences of a wire model or build.

## Minimum Evidence

Require independent source review plus focal controller/service tests: ownwrites
and external rollback, pinned releases and changed vectors/ABA, scopes and
selectors, both page/group visibility directions, revocation in the last SPI,
authority before 304, clock changes with weak validators, cursor isolation and
global ordering, default/partial/custom host wiring, and pull recovery.

Database-dependent proof uses an exclusively assigned remote Neon branch with
actual TLS/PG/owner/runtime/control-plane preflight. Preserve raw failures and
fresh logs/XML, source/tree/dependency/artifact linkage, migration slice and role
privileges. A restricted-runtime fixture is not the live host's SESSION proof;
MockMvc is not real host HTTP. Separate library Neon, Quickstart HTTP, Core public
HTTP specs/builds and actual visual E2E in the report, without summing overlapping
runs or presenting later unexecuted gates as complete. Review official docs,
consumer contracts and these skills before integration/adoption.
