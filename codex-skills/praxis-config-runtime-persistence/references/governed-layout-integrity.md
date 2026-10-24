# Governed Layout Integrity

## Source And Scope

Owner: `praxis-config-starter`, not the Metadata starter or the Angular host.
Audit these existing surfaces in the exact checkout being adopted:

- `UiLayoutLifecycleCommandService`, `UiLayoutLifecycleReadService`,
  `UiLayoutLifecycleService`, `UiLayoutFrozenWorkspaceResolver` and
  `UiLayoutWorkspaceSelectionVerifier` in `service/`;
- `UiLayoutLifecycleInvocation`, `UiLayoutCompositionRegistration`,
  `UiLayoutValidationAttempt` and the host's invocation/admission/budget providers;
- `CanonicalJsonHashService`, `UiLayoutRevisionJsonInput`,
  `UiLayoutDraftWorkspaceCodec`, `UiLayoutMetadataCaptureCodec` and
  `JpaUiLayoutCompositionReleaseReader`;
- `docs/ai/contracts/ui-layout-canonical-exact-hash.md`,
  `ui-layout-validation-attempt.md`, `ui-layout-create-key-lookup.md`,
  `ui-layout-metadata-postgres-gate.md`, current lifecycle/read contracts and
  migrations V64–V68.

Layout drafts, immutable revisions, review, publication heads and historical
reads have their own governed lifecycle. Reuse the returned refs and validators,
pinned composition, metadata capture and server-owned admission. Do not invent
another registry, DTO, workflow or source of layout business rules in the host.

## Authority And Identity Checks

1. Resolve actor, tenant, environment, current context and registered composition
   on the server. JSON/header claims are not authority. Recheck current authority
   and invocation after the last extension and at the effective write commit
   gates. `validation.require` checks budget/snapshot; it is not a new grant read.
2. Keep one monotonic, nonrenewable validation attempt. A cooperative deadline
   prevents late acceptance where checked; it does not interrupt a blocked SPI,
   JDBC transaction or worker, and does not prove distributed revocation ordering.
3. Follow every persisted patch reader, including the historical selection
   verifier used during publication. A host mapper configured to omit null must
   not turn a removal patch into an omission. Use the existing closed boundaries;
   never fix this by mutating the application's global mapper.
4. Audit precision before materialization loses it. Exact identity must refuse
   arbitrary-precision input whose value changes under the existing canonical
   number token. Preserve raw decimals on parsing; do not round both sides and
   call the match exact. Finite materialized Float/Double semantics and raw
   precise-input semantics differ. Read the owner's contract before changing
   numeric formatting or the legacy `sha256` path.
5. Distinguish a bounded revision/target document from the aggregate workspace
   envelope. Preserve per-document byte/depth controls and the codec's existing
   envelope controls. Do not apply the revision's 256 KiB limit to a multi-target
   envelope, raise that limit globally, or invent an aggregate quota in a parser
   fix. Preserve strict JSON, duplicate/trailing checks and sanitized failures.
6. Persisted malformed evidence must fail as historical integrity, not as a new
   malformed request. Preserve the owner's diagnostic mapping; never rehash,
   drop explicit nulls or repair history merely to make publication pass.
7. Audience selectors have optional fields with canonical meanings. Audit the
   selector DTO, persistence and conversion together before changing null versus
   omission comparison. Do not derive selector authority from labels or make a
   host serializer the source of business semantics.

A candidate correction remains a candidate until independently reviewed and
integrated. This procedure is an audit requirement, not a claim that every
published version has all of these protections.

## One Owner For Nested Validation

For Config #521 adoption, inspect `UiLayoutValidationAttempt`,
`UiLayoutValidationContext`, `UiLayoutValidationScope` and
`docs/ai/contracts/page-publication-p0/P3C-VALIDATION-BUDGET-521.md` in the exact
candidate. These correlation/scope seams are internal, not public host APIs or DTOs.
Keep one owner budget across reserved draft creation, receipt reads, source lineage
and commit checks. Correlated views retain its operation, correlation ID, original
ticker, deadline and monotonic balance; never rebuild `now + remaining` or obtain
a fresh child allowance. Changing a root does not permit changing actor, tenant,
unit, environment or context version. Close the owner to invalidate every view;
closing a view must not close its owner or siblings.

Pass validation explicitly where the internal reserved-command/read signatures
support it. Only SPIs without that parameter use the lexical scope frame carrying
the attempt. It must contain no principal, membership, grants or cached admission.
Restore the previous frame with resource cleanup, prohibit unrelated nested budgets
and worker inheritance, and fail closed on absent/expired scope or changed authority
correlation. Commit callbacks reinstall their captured attempt for their execution;
do not retain ThreadLocal state until transaction completion or mint another budget.

Bound each external callback before and after execution, including metadata and
child admission. Expiry in root metadata must stop before calling child producers;
denial only after traversing more callbacks is insufficient. Prove this with a
deterministic clock, plus correlated closure, reentrancy, exception cleanup and
cross-thread tests. These guards preserve every current-authority checkpoint and
prevent late acceptance; they do not cancel blocked JDBC/SPI work or establish
that a public artifact already contains the correction.

## V68 Metadata And PostgreSQL Proof

All new database-dependent validation uses a remote Neon branch exclusively
assigned to the worker/run. Confirm project, branch, endpoint, PostgreSQL version,
TLS and actual owner/runtime/control-plane privileges before mutation. Existing
local PostgreSQL workflow evidence is historical and does not satisfy this gate.
Do not substitute embedded/local PostgreSQL or a privileged owner fixture for the
runtime path. A proxy's `pg_stat_ssl` value alone may not establish client TLS;
verify the actual JDBC client's TLS connection and hostname validation without
logging credentials.

Read the current opt-in test/runbook before reserving a database. The metadata
capture gate requires an existing exclusive `b1a_it_*` schema migrated through
V68, and the documented `PRAXIS_UI_LAYOUT_PG_*` inputs. Never print credentials.
The reader gate itself does not authorize creating a remote schema,
EmbeddedPostgres or Docker as a substitute for its admitted window. The
lifecycle gate has different migration effects; do not combine them by reflex.

For an authorized native PostgreSQL preparation, inspect the actual
`.github/workflows/domain-catalog-postgres-migration.yml` and both
`ui-layout-metadata-postgres-gate.md` and
`ui-layout-create-key-lookup-postgres-gate.md` in the exact Config candidate.
Confirm that the workflow contains separate lifecycle preparation, admission
and existing-schema reader phases before relying on it. An older workflow
running only catalog/template tests does not prove UI-layout persistence.

- Reserve an isolated Neon branch and the documented exclusive schema/database
  for the validation. Preserve its parent branch and all unrelated data. Record
  UTF8, owner, runtime privileges and the migration starting state before lifecycle.
- Use the exclusive documented `b1a_it_*` schema in JDBC `currentSchema` without
  `public` fallback. Let canonical lifecycle/Flyway install extensions naturally;
  verify actual vector/pgcrypto namespaces, required types/opclasses, owner,
  encoding, V65/V68 history and creation-key index before readers. Do not move an
  extension, manually bootstrap vector, repair or clean to make admission pass.
- The two existing-schema readers may run together after lifecycle completes;
  neither may migrate or mutate schema/history. Preserve per-phase actual Maven
  and tee exits, fresh exact XML suites and skip reasons, source/workflow hashes
  and PostgreSQL logs. Require executed tests and zero failures/errors/skips.
- Capture the registered catalog fields and history/checksums before and after
  readers. Once admitted readers start, capture the latter even if tests fail;
  keep capture, comparison and XML-validation exits distinct and record not-run
  separately. A matching snapshot proves its recorded fields, not all database
  data or every catalog property. A privileged disposable owner is not a proof
  of least-privilege Neon roles, producer admission or live host HTTP.
- Before dispatch, verify the real triggers and immutable source/workflow/run
  SHAs; a checkout override must not execute an older workflow unnoticed. Use
  the reviewed official resource window and evidence gate, not a tag as a CI
  probe. Static workflow review is not PostgreSQL execution or release approval.

V68's NOT VALID constraint protects new inserts without certifying incomplete
historical rows. Do not backfill or VALIDATE CONSTRAINT to manufacture missing
provenance. SQL hashes do not prove Java codec admission, current authority,
normalization, producer reproduction or a browser journey.

## Page And Internal Child Admission

Inspect `UiLayoutPageRevisionReproduction`, `UiLayoutPageChildCaptures`, the
workspace source/codec, command service and `docs/ai/contracts/page-publication-p0/`.
The root target is `praxis-dynamic-page` with its opaque page UUID; children do
not become additional external lifecycle targets. Reuse native Form/Table
projection and reproduction checks even when page widgets are an atomic array.

- Reconstruct native child documents from `definition.inputs.config` plus the
  admitted binding/context inputs without defaults. Bindings and native envelope
  stay fixed for each widget key. New binding/resource/mode needs a new key.
- Require `childSources` to name exactly the previously unknown keys. Resolve
  each registered source/revision server-side and capture its genuine native seed
  and metadata. The source request, a hash supplied by a client, or an intact
  historical `captureText` is not current authority. The source/admission SPI must
  bind the requested immutable source to the captured evidence and current scope.
- Preserve evidence for removed keys; restoration uses the historical seed and
  must pass current admission. Reject replacement declarations for known keys,
  missing/extra/duplicate requests, scope substitution and changed fixed envelopes.
- Keep exact capture identity through workspace serialization and database JSONB.
  Revalidate native reproduction, source admission and transaction gates at the
  relevant mutation/execution paths. Historical authorized inspection proves
  integrity and scope, not fresh admission to mutate or execute the page.
- Compare schema/resource copies and Java/TypeScript corpus vectors. Preserve
  Unicode codepoint limits, absolute regex endings, absence/null semantics and
  exact-number guards; do not tighten one engine incidentally or normalize both
  sides before comparing. Align revision reason with the existing lifecycle
  storage limit, rejecting excess before SQL rather than widening storage to
  accommodate an accidental contract divergence.

Use focal codec/capture/lifecycle tests plus the owner's opt-in Neon page lifecycle
gate when changes touch durable writes. Prove create/edit/add/remove/restore,
freeze/publication/read and denied-source rollback on a fresh connection. A
mocked repository cannot prove JPA new-entity/version behavior or JDBC/JPA sharing
one Config transaction. Record the actual migration slice, runtime identity,
source/dependency hashes and limits; a partial DDL fixture is not full Flyway or
live host HTTP proof. Those child-admission tests do not by themselves prove
catalog, routes, menus, cross-head transactions or host adoption. Use the dedicated
creation/group sections below and [published-page-runtime.md](published-page-runtime.md)
for their separate implementation and evidence gates.

## Page Creation And Copy Admission

Before adopting creation/copy, inspect the owner's P0 and P2 design, the actual
`PageCreationService`, host attestation, catalog/lifecycle bridge, codec and
migration. A planned endpoint is not an available host feature. Keep the
catalog's durable identity and immutable creation evidence separate from mutable
drafts, publication heads, titles and authored documents.

- Resolve application and route namespace through independent server-owned host
  attestation. Neither a module hint, an invocation supplied by a caller, nor a
  catalog record grants application access. Metadata/lifecycle callbacks without
  a Principal still need independently validated current host context before
  application-scoped lookup or rebasing; do not infer authority from the ledger
  or introduce a ThreadLocal to conceal a missing contract.
  Include route namespace in page lookup predicates and immutable-read keys;
  prove isolation within one transaction and uniform known/unknown rejection.
  Preserve the separately defined creation-key idempotency scope.
- Copy only an exact registered native source/revision or the selected published
  page/release/revision. A historical publication need not be the current head,
  but a frozen release that was never published is not a published source.
  Never substitute latest, effective configuration, a draft or the current DOM.
- Reproduce the typed widget/link identity map and preserve ordinary literals.
  Config-produced native output must be correlated with the complete immutable
  original source, captures, map, transformation and hashes. NativeIdentity must
  genuinely reproduce that output. A producer prefix, stored row or matching hash
  alone cannot admit it. New draft observations reflect the current actor and
  context; original observations remain historical evidence, not grants.
- Require CREATE at the destination and READ_SOURCE/COPY_SOURCE for the directly
  selected source at creation/replay and commit. Do not invent perpetual COPY
  permission or ancestral page ACL requirements for an independent copy.
  Integrity/reproduction and current producer, domain and derived-use admission
  still apply throughout its provenance chain. Do not expose ancestral private
  evidence through a receipt or association lookup.
- Scope the creation key to actor/application/tenant/environment. Equal replay
  returns the same page and current draft validator without recapture; a different
  command conflicts. Context version must be current but is not a new key scope.
  Reconciliation needs current association and draft visibility, without requiring
  permission to the old selected source. Verify no-store, the quoted current
  draft ETag, absence of 304 and a Location that can actually read that draft.
- Preserve one atomic Config transaction for catalog, ledger, draft and metadata.
  Reuse the shared actual JDBC/JPA connection invariant and reject rollback-only
  results. Recheck context and current grants after the final extension in each
  commit callback; checking a budget/snapshot after a revoking SPI is insufficient.
  Nested provenance traversal must consume the remaining outer deadline, with
  explicit cycle/depth/aggregate limits and denial rather than truncation.

Keep a participating REQUIRED operation's validation attempt alive until the
outer Config transaction completes. Its returned receipt is provisional until
that owner commits; do not force a separate transaction to obtain an early
acknowledgement. Check the same deadline before and after the actual commit and
before returning an owned transaction's result. A failure after JDBC COMMIT is
uncertain delivery, not rollback evidence: preserve the creation key, reconcile
the original identity and never recapture or silently generate another key.
Prove both owned and participating transactions, including delayed responses
after a successful real commit and inspection through a fresh connection.

Measure repeated historical reads before increasing a validation budget. If
reuse is necessary, restrict it to positively resolved immutable evidence inside
the actual Config transaction, bound to its owner and JDBC connection. Never
reuse an authority decision, current context, head, negative lookup or mutable
review state. A data hit must still run current source/domain/structure admission,
reproduction and final grant checks. Bound retained bytes/entries, preserve
defensive copies and clear on completion; eviction reloads data rather than
truncating provenance. Prove separation across owners/connections, suspended and
new transactions, rollback/completion and scope keys, including actor when a
creation-key association is reused. Compare SQL count and elapsed time before
and after; a fixture measurement is not a production SLA.

Rollback to a savepoint keeps the outer synchronization list alive, so completion
cleanup alone cannot prevent reuse of rows that were rolled back. Clear retained
positive bytes on savepoint rollback and disable both immutable-read retention
and isolation-proof reuse for the rest of that transaction. Subsequent guarded
accesses require a fresh pinning SELECT and load immutable records without
retaining them. Prefetch still enforces bounds and accounts for consumed rows.
Spring invokes `savepointRollback` before the physical rollback; another
synchronization can reenter a ledger and obtain proof that the subsequent rollback
undoes, or repopulate bytes that it later removes. Merely clearing a flag or the
retained rows and allowing reuse again is unsafe. Prove that reentry followed by
physical rollback cannot preserve proof or bytes, and that a later read reloads
discarded records. These invariants do not establish support
for nested JPA lifecycle operations or their business callbacks.

Include driver metadata calls in that measurement: PgJDBC isolation getters can
issue server SQL outside a prepared-statement counter. A SHOW alone does not
establish PostgreSQL's first-query isolation boundary. Audit the owner's explicit
read-transaction admission and prove isolation cannot change after its SELECT;
retain the regular mutation guards and recheck connection/rollback state on reuse.
Inspect `ConfigJdbcTransactionGuard` together with `ConfigTransactionReadSet`:
their shared proof concerns transaction isolation only, never principal, grants,
source admission or provenance. Bind it to the exact datasource, connection
holder, JDBC connection and active synchronization lifetime. Reuse across guard
instances in that same transaction must not repeat the isolation getter; a new
or resumed transaction must use its own synchronization/proof. Without active
synchronization, retain the full guard validation rather than retaining proof.
Prove savepoint rollback invalidation independently of positive-cache eviction,
and prove denial if isolation changed before the replacement pinning SELECT.
Use focused no-database JDBC instrumentation to count getter/server statements
and adversarial identity/rollback cases. Report that result as a measured local
cost reduction, not a fresh Neon rollback proof or a guaranteed 40-second journey.

A `RELEASED` label alone does not make a draft row immutable. For a frozen copy,
prove that its candidate reproduces the captured B0 plus the selected immutable
revision patch, and audit protection of the whole workspace, including embedded
child captures. If the lifecycle already makes freeze terminal, enforce that
invariant in the database rather than maintaining a parallel fingerprint path.
Prove that DRAFT edits and the transition to RELEASED still work with real JPA
flushes, while later body/ETag/state changes cannot succeed. Distinguish a denial
by SQL privileges from execution of an immutability trigger; neither authorizes
rewriting old evidence. Previous DDL evidence does not certify a newly added seal.

Use the owner's opt-in isolated Neon gate with its actual migration slice and
restricted runtime. Prove equal and divergent concurrent commands, lost-response
reconciliation, source isolation, current authority, and failures after actual
SQL writes as well as at commit. Verify absence of partial catalog, ledger,
draft and metadata rows from a fresh connection. Fault injection belongs in the
test JDBC fixture, not a production bypass. Bind raw logs/XML and fixture,
source and dependency hashes to the reviewed tree. Report skipped/full migration,
live HTTP, host and browser gates separately; a passing SQL fixture does not
prove those downstream journeys.

## Navigation Groups Admission

For native navigation groups, reuse the P0 `groupsDocument` schema and the
Config reproduction owner rather than adding a second schema or publication
machine. The document contains a flat complete groups array; omission removes
an entry and an empty array removes all. Page bindings remain authored by each
page, never duplicated into the groups document. Preserve array order, stable
UUID identities and order ties without coercing or normalizing authored values.

A codec that validates UUID shape, icon syntax, bounds and exact patch
reproduction does not register the root or admit its source and icon catalog.
Require current host-owned source and structure policies; an unavailable catalog
must fail closed. Register one stable app-shell root per authenticated navigation
scope, without deriving UUIDs from arbitrary strings or trusting client scope.
Exercise the operational host resolver: identical authenticated scope reuses the
same root and an alternative requested UUID is denied. A UUID constructor or
Javadoc alone does not prove that registration invariant.

Review dispatcher, revision and frozen-release integration separately from an
isolated codec. Validate native group metadata before any draft write
and re-admit persisted root evidence on revision, freeze and commit; history
inspection does not grant current mutation rights. Until cross-head integrity is
implemented and proved, block group publish, rollback and withdrawal in the
lifecycle owner itself, including direct callers with permissive policy and no
page-creation host. A codec or permissive fixture does not prove those guarantees.
Keep the issue open while required integration, documentation or skills remain
pending.

For page/group head transitions, inspect the owner's P3-A design, core
`moveHead`/`withdraw`, command factory, `PageCreationHost`, Config transaction
guard and immutable workspace resolver. Require an internal integrity owner in
the effective core path; an admission callback alone or a caller-supplied
"validated" flag cannot replace it. Missing dependencies must deny page/group
head changes rather than silently enabling the earlier path.

Resolve the navigation root through the host's explicit registered mapping, then
independently attest the inverse root-bound context. One stable root per scope
must also mean one application/namespace per physical tenant/environment/root;
two scopes aliasing that head break application-partitioned checks. Mapping is
not a grant. Recheck it with current context/authority after locks and at commit;
do not infer application from actor, administrative unit, module or an anchor.
Admit the active groups dependency through its current READ_HEAD policy as well
as source/metadata/structure checks. Recheck admission after those extensions;
an active group or a valid UUID alone does not authorize a page to use it.

Plan affected group IDs from both the prior and candidate release, including
omission and withdrawal. Lock the shared navigation identities deterministically
before the physical root/head, including first publication. Administrative units
sharing a navigation scope must share its exclusion. Ordering each call alone
does not prevent inversions across several REQUIRED calls: inspect the owner's
try-lock/conflict protocol and require rollback of the entire Config transaction
on contention. Catching the exception or rolling back to a savepoint must not
restore commit eligibility. Retry means a new transaction and explicit fresh
preconditions, never REQUIRES_NEW or acquiring an expanded set out of order.

Flush own JPA writes before authoritative JDBC reads and refresh the managed
head under the lock before changing it. A second `findForUpdate` may return a
stale first-level entity; refresh must not discard a previous valid write in the
same transaction. Re-read the base used to choose locks and reject a changed
base without renewing If-Match. Before commit, check the final heads under the
retained locks, allowing valid repeated transitions of one root while retaining
current context/grant checks for each command. Validate the final page's current
root metadata, children and complete structure as well as its groups dependency;
checking only its reproduced group IDs is insufficient. Evaluate head
preconditions against the authoritative refreshed state, so a stale managed
entity cannot reject an otherwise current ETag before reaching that check.
Bind each governed root to its expected native authoring kind before applying
revision reproduction. A kind-dispatch helper may skip unrelated descriptors;
that skip cannot admit malformed historical groups under permissive host SPIs.
Never memoize heads as immutable evidence. Require actual JDBC/JPA connection
identity for reads, locks, flush and mutation even when the JDBC holder reports
itself synchronized; synchronization alone does not prove a shared connection.

Count all active page references in the attested scope, including private pages
and other administrative units. Scan with an immutable keyset and bounded
batches, not OFFSET under READ COMMITTED: unrelated insertions/removals can shift
offsets past a stable reference. Exceeding the deadline denies the operation;
a partial scan is not absence. Do not reuse copy-chain quotas as a page-count
limit. Bound ORM first-level retention too: batching SQL does not bound memory
if every frozen workspace stays managed. After flushing own writes, release
sealed read entities and other read records loaded exclusively by the scan;
preserve pre-existing managed definitions, which do not have an immutable seal.
Never clear the whole persistence context or discard mutable heads/drafts.
When increasing batch count to reduce remote round trips, also bound the
serialized workspace text selected in each batch. Select an ordered keyset
prefix, retain missing release/draft rows for the canonical verifier, and always
include the first row so an oversized or malformed record cannot be skipped or
stall progress. Advance from the last row actually returned. This is a batching
resource budget, not a page admission quota or a partial-scan shortcut. Workspace
text bytes do not bound heap, patches or all associated records; record those
costs separately and prove complete identities across passes after tuning.
An active page head whose catalog ownership cannot be
proved must fail closed; document the explicit adoption/migration prerequisite
rather than inferring its application or treating it as unreferenced. A derived index, if
introduced, needs atomic maintenance and historical completeness proof.

Prove races in both orders against group omission, rollback and withdrawal;
check the invariant from a new connection. With multiple try-locks both
contenders may legitimately abort; do not require an artificial winner. Include
external REQUIRED inversions, swallowed conflicts/savepoints, initial heads,
preloaded JPA heads, own writes and repeated transitions, cross-unit private
references, and rollback of A without changing B or groups. Distinguish failure
after actual SQL, a beforeCommit exception, and a server rejection of COMMIT;
each claim needs its own evidence. Measure a dense scan without asserting an
unmeasured production SLA or claiming the later host/HTTP/navigation gates.

## Focused Validation And Evidence

Choose selectors from the changed entrypoints, not a frozen suite count:

- hash/raw identity: `CanonicalJsonHashServiceTest`,
  `UiLayoutMetadataCaptureCodecTest`, `UiLayoutDraftWorkspaceCodecTest`;
- revision and historical publication: `UiLayoutLifecycleHttpRoundTripTest`,
  `UiLayoutLifecycleServiceTest`, `JpaUiLayoutCompositionReleaseReaderTest`,
  plus existing direct tests for any changed reader;
- authorized real PostgreSQL: the documented opt-in lifecycle/capture tests
  with an allocated schema and explicit migration/resource authority.

Test null removal versus omission on the SAME patch, and loss rejection before
immutable writes. Exercise malformed persisted patches through publication:
no head write, sanitized historical error, no-store. Keep valid near-limit
baseline creation and rejection of an oversized derived patch separate.

Record the tree, Java, dependency/classpath origin, actual Maven exit, fresh
selected XML identities and all failure/skip reasons. Archive original reports
before an incremental run. Do not count unselected stale XMLs as fresh tests.
Surefire schemas may omit a native XML timestamp: report that limitation and
verify freshness through explicit pre-run removal, empty output, fresh mtimes,
run log and exact suite/file identities; do not invent a date or rerun solely
for a collector assumption. Keep wrapper exit distinct from Maven exit.

A passing subset does not make an earlier failed broad suite green. MockMvc
with simulated repositories is not real PostgreSQL, a live HTTP host or browser
E2E. A local private JAR is not public adoption: prove official publication,
Central POM/JAR hashes and the host dependency/package without local overrides.
Review public docs/corpus and adjacent skills when the taught route changes;
state every remaining release, persistence, host and frontend gate explicitly.
