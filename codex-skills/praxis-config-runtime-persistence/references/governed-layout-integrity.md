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
live host HTTP proof. Catalog, routes, menus, cross-head transactions and host
adoption remain their separately scoped downstream work.

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

Review dispatcher, revision and frozen-release integration separately from an
isolated codec. Until the inter-aggregate head guards are implemented and proved,
do not enable publish, rollback or withdrawal of groups. The later gate must
serialize page/group transitions, re-read authoritative heads and reject removal
of groups with active references. Unit codec tests or a permissive host fixture
do not prove those guarantees. Keep the issue open while required lifecycle
integration seams, root registration, documentation or skills remain pending.

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
