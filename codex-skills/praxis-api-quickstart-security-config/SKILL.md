---
name: praxis-api-quickstart-security-config
description: Use when Codex must implement, audit, or prove praxis-api-quickstart host security and exposure policy: SecurityConfig, CORS contract headers, CSRF/cookie JWT, read-open/write-disabled, schemas/actuator/runtime/config endpoint policy, trusted proxy and origin governance, rate limiting, encoded-path firewall settings, current operational grants and trusted context, or security-focused HTTP integration tests.
---

# Praxis API Quickstart Security Config

Use this skill for host security and exposure policy in `praxis-api-quickstart`. The quickstart hosts `praxis-metadata-starter` and `praxis-config-starter` in real HTTP; it owns how their public contracts are exposed, not the contracts' business, metadata, persistence, AI, or authorization semantics.

Security here is an executable policy matrix, not a collection of `permitAll` calls. Every public route, method, header, cookie, origin, rate-limit bucket, firewall exception, and filter exemption needs a named reason and a focused proof.

Pair it with:

- `praxis-api-quickstart-operational-proof` for host-versus-starter ownership and HTTP proof.
- `praxis-config-runtime-persistence` for `ui_user_config`, ETag, runtime context, and config header semantics.
- `praxis-config-agentic-authoring-streaming` for AI authoring/SSE security under `/api/praxis/config/**`.
- `praxis-metadata-schema-contracts` for `/schemas/**`, `ETag`, `X-Schema-Hash`, and structural metadata ownership.
- `praxis-api-quickstart-cockpit-http-validation` when security changes affect official cockpit HTTP examples or browser evidence.

## Canonical Boundary

- The quickstart owns Spring Security matcher order, CORS, CSRF, cookie/session bridge, trusted proxy treatment, rate limiting, HTTP firewall policy, local/prod properties, and downstream HTTP tests.
- `praxis-config-starter` owns config persistence, AI registry/context/authoring behavior, ETag semantics, tenant/user/environment headers, and endpoint contracts under `/api/praxis/config/**`.
- `praxis-metadata-starter` owns schemas, schema hashes, `x-ui`, actions, surfaces, capabilities, and structural discovery semantics.
- Angular and other browser clients consume the headers and exposure policy; they must not invent local storage, origins, cache validators, or authorization fallbacks to compensate for a host policy defect.

If a config or schema endpoint is `permitAll` but receives `403`, inspect host origin, CORS, CSRF, firewall, and rate-limit policy first. If the HTTP contract itself is wrong, fix the appropriate starter and keep quickstart as the operational proof.

## Required Source Inventory

Read `praxis-api-quickstart/AGENTS.md`, then inspect:

- `src/main/java/com/example/praxis/apiquickstart/config/SecurityConfig.java`
- `security/ConfigOriginRestrictionFilter.java`
- `security/PublicApiRateLimitFilter.java`
- `security/CookieJwtAuthenticationFilter.java`
- `security/SpaCsrfTokenLifecycle.java`, `SpaCsrfTokenRequestHandler.java`, and `CsrfCookieFilter.java`
- `security/EnterpriseSessionLifecycle.java`, `EnterpriseSessionStore.java`, `VerifiedJwtCredential.java`, and `JwtTokenService.java`
- `/auth/**` controller issuance, revocation and identity-switch behavior
- `src/main/resources/application.properties`, `application-dev.properties`, and `application-prod.properties`
- `docs/security-overview.md`, `docs/security-read-open.md`, README exposure notes, and official HTTP examples
- focused SecurityConfig, CORS, config-origin, rate-limit, CSRF, config AI, and schema integration tests

Treat effective properties and executable tests as source evidence. Documentation is a required derived surface, not proof that a default or route policy is actually configured.

## Enterprise context and Config write admission

Inspect `EnterpriseRuntimeConfiguration`, `EnterpriseRuntimeProperties`,
`QuickstartEnterprisePresentationSource`, `QuickstartUiConfigAdmission`, its MVC
interceptor and `QuickstartUiConfigAdmissionConfiguration` together. Config owns
runtime/context DTOs and the `UiConfigWriteAuthorizer` SPI; the host composes its
actual SESSION, membership, presentation and admission sources.

Require two distinct managed 32-byte reference keys and an explicitly configured
presentation catalog. A missing catalog is incomplete composition; an explicitly
empty catalog is valid and grants nothing. With an empty authoritative directory,
authenticated context returns selection-required with no effective context and
no choices. Never seed production tenants, organizations or memberships to make
the endpoint ready. Presentation labels and JWT roles do not authorize access.

Before generating or rotating reference keys, inventory the effective deployment
configuration privately, including `SPRING_APPLICATION_JSON`, environment aliases
and property precedence. Missing individual environment variables do not prove
missing keys. Record only presence, validity and source, never values or a full
environment/JSON dump. Preserve valid managed keys; rotation is a separate explicit
operation affecting issued references, not a remedy for an empty catalog.
An explicitly empty `app.security.enterprise.presentation.contexts` is different
from missing configuration, missing membership storage and an empty authoritative
membership directory. Diagnose each independently.

Inspect `JdbcEnterpriseMembershipSource`, `EnterpriseRuntimeProperties` and
`QuickstartEnterprisePresentationSource` together. Persistent membership supplies
the exact subject/tenant/environment/optional-selector tuple, revision, validity,
revocation and capabilities; presentation supplies only reviewed public labels.
`AUTH_*` lab identities establish authentication, not enterprise grants. Neither
an ADMIN role, a presentation entry nor successful login can replace membership.
Provision access through a separately authorized administrative operation with a
reviewable plan, explicit compare-and-set precondition and bounded validity;
startup, migrations and demo authentication must not insert or renew grants.

Inventory the actual membership catalog before installation: column types,
nullability/defaults, constraints, foreign keys, ownership and effective ACLs.
An empty table is not permission to replace its schema or drop directory FKs.
For PostgreSQL `SELECT ... FOR UPDATE`, UPDATE on an innocuous column may provide
the lock privilege even when table-level UPDATE is false. Preserve the admitted
lock anchor and check its effective column grant; do not alter its type or grant
UPDATE on capability, selector or revision columns to satisfy a fixture shape.

For every canonical UserConfigController handler, including both identifier
transports and conditional reads, revalidate the active SESSION, current selected
membership, contextVersion and exact tenant/environment/user headers before the
controller. Non-read methods additionally require the current membership's
`ui.authoring.configure`; USER scope is not a personal-preference exemption.
Install the existing write-authorizer SPI too, rechecking admission immediately
before persistence. USER targets the authenticated subject; TENANT targets the
selected tenant; an optional updated-by value must match the subject. Distinguish
unauthenticated, forbidden, stale-context and unavailable-source results. The
separate API and Config transactions do not provide an XA revocation fence.

Validate through real HTTP on an exclusively assigned Neon child using ordinary
runtime identities, TLS and actual column privileges. Membership FOR UPDATE may rely on the innocuous lock-anchor column UPDATE
privilege; verify SESSION issuance, selection and revocation column grants
separately. Do not widen grants because table-level UPDATE is false. Prove empty directory, session-bound choices,
concurrent selection CAS, Config ETag and fallback, denied capability/forged
identity, revoked membership, stale context, scoped cleanup and logout204 plus
old-SESSION401. Preserve failed receipts and resolve uncertain issuance before
retrying. Readiness warming is not proof of first-request behavior after an idle
pool; record that boundary explicitly. For error responses such as Config's
textual412, capture status and body hash before attempting JSON decoding.

## Cost of enterprise authority admissions

For repeated enterprise/page admissions, inspect `EnterpriseContextSessionService`,
`JdbcEnterpriseContextSnapshotReader`, `EnterpriseSessionStore` and
`JdbcEnterpriseMembershipSource` before changing budgets or transaction managers.
The host reader composes the existing SESSION and membership snapshot; Config still
owns lifecycle checkpoints and persistence. Keep two fresh observations around each
admission unit and compare the session revision and complete membership. Do not cache grants,
remove checkpoints, raise the page validation budget or widen runtime privileges.

Audit `QuickstartPageHost.require` before multiplying operational reads inside one
callback: app/namespace shape and complete invocation/capability/source policy can
share one `requireCurrent` admission with both observations still around the policy.
Do not reuse that result in the next callback or globally weaken `requireContext`.
For the canonical
`PageCreationHost.requireCreation(principal, contextVersion, expected, source)`
contract, evaluate the FULL resolve policy plus CREATE_PAGE, READ_SOURCE and
COPY_SOURCE in one admission using the supplied Principal. Do not substitute
thread identity or the expected actor. Preserve
`QuickstartUiLayoutContextAuthorization.authorize`'s existing identity check:
the supplied Authentication must be the ambient SecurityContext Authentication;
do not accept a detached credential or replace the supplied identity to pass it.
Return the freshly observed context only
after both observations succeed; Config requires exact equality with expected
and rejects null. Expected grants no authority and must not silently rebase scope.
This is an explicit joint decision
window, with the same operational locks and fresh before/after observations around
all three pure policies; it changes their former separate linearization points.
No Config work, source I/O or arbitrary extension belongs between these policies.
Config still invokes the unit at each creation/replay/commit checkpoint, and
revocation between units must deny the later call. Test policy completeness,
stale scope and expiry, retaining independent admissions for other callbacks.
Do not generalize this grouping to unrelated policies or claim the unchanged
40-second operational budget is met from an observation-count reduction alone.
The separate canonical `requireNativeProvenance` unit is restricted to captures
classified by Config as Native with wholly non-generated root/child metadata.
In the closed Quickstart producer, `documents.requirePage` checks the exact
historical producer, root metadata and every child's source/metadata inside one
`requireCurrent` policy, without arbitrary extensions or Config I/O. Config calls
that unit before and after structural extensions; both calls retain their own
fresh before/after SESSION/membership observations. Prove the second call rejects
revocation or expiry during those extensions and that no child policy is omitted.
It also includes the FULL resolveLifecycle policy, including custom registration
restrictions, and returns a fresh context for Config's exact-equality check.
Ledger-derived comparison values never authorize the call. Preserve pre-catalog
admission and the post-extension call; post-I/O authority is resolved inside the
joint unit, not reused from the earlier context. Test a stricter custom resolver,
null or divergent returned context, and the supplied Principal boundary.
Mixed captures still use `requireNative` with independent metadata/child checks
and Config provenance correlation; published traversal is unchanged. Do not let
the host select this route from labels or generated-marker guesses.
For child evidence, implement `requirePageChildEvidence` as one current admission
covering source, document, reproduction and full metadata; the default denies.
Do not delegate to an old callback or omit restored/frozen children. Config owns
generated-child correlation and its provenance traversal, not a host grant cache.
The configured lifecycle admission bean itself must implement
`PageLifecycleAdmission`. Its `requirePage` preserves all operation/domain
policies of `require` while attesting current context in the same authority
window. A separate provider or ignored delegate would bypass custom restrictions.
Retain fresh before/after observations, post-catalog context checks and renewed
admission after provenance/at commit. Unknown page UUIDs need admission before
lookup; non-page invocations still use `require`. Test plain-bean rejection and
restrictive custom policies as well as stale context and revocation.
For the closed pilot, structure validation may be pure: retain `validation.require`,
registered tenant/environment/unit, exact root/sole composition/target, canonical
schema/reproduction, icons, Form restrictions and selectors. Inspect
`QuickstartPageFormContentPolicy` before evolving content: the native B0 stays
empty, while revisions/copied baselines may contain the admitted SDK local fields
(`controlType`, `source: local`, `transient: true`, `submitPolicy: omit`) and
field-only sections/rows/columns. Text controls use `input`, not `text`. Keep
field references/order consistent with metadata and reject unknown properties;
do not silently strip editor output. No resource/API bindings, actions, hooks,
rules, option sources, default values or entered preview data are admitted by
this presentation-only cut. Validate real public-editor projection fixtures and
negative widening cases with `QuickstartPageFormContentPolicyTest`; an accepted
structure is not a business-data submission or HTTP publication proof.
Structural acceptance grants no operation or source access. Outside these explicit joint units,
preserve independent current admissions for invocation, lifecycle, mapping,
native source, metadata and children; historical
captures are never grants. Use `QuickstartPageHostTest` and
`QuickstartPageStructureTest` for forged/stale scope, revocation between callbacks
and absence of structural authority I/O. Confirm the Config owner budget propagation
separately; reducing host calls does not repair nested deadline renewal or prove
that the real Neon operation fits forty seconds.

Use the same physical writable operational transaction and datasource for both
stores. The composed query locks materialized SESSION before the exact membership
lookup (NULL selectors are significant), reuses verified identity and the original
parsers/clocks, and evaluates validity after lock waits. Invalid SESSION must be
rejected before interpreting grant JSON; technical membership failures must not
become successful absence or authentication failures.

At READ COMMITTED, a membership inserted while the statement waits on SESSION may
be conservatively absent even when the changed SESSION is visible. Preserve denial;
never recover an old grant or silently retry using an alternate read. A subsequent
fresh request can observe the new membership. Document this availability boundary.

Use `JdbcEnterpriseContextSnapshotReaderTest` for physical guards/choreography and
the assigned-Neon `JdbcEnterpriseContextSnapshotReaderNeonTest` for actual two-query
admissions, SESSION-before-membership locks, revocation, expiry after waits and
coherence rollback. For group-draft HTTP acceptance, use
`QuickstartPageCorporateHttpNeonTest#groupsDraftCreateReadAndCommitRollback` only
with the explicitly resolved compatible Config artifact. Require create/read below
the unchanged budget; force failure after draft and metadata are staged, observe
transaction rollback, and independently read their absence through another ordinary
runtime connection before retrying the same creation key. Fixture cleanup is not
rollback proof. Bind receipts to source, dependencies, branch, privileges and timings;
these focal gates do not certify publication, navigation, browser or deployment.

## Current Operational Grants And Context

For bulk-provider composition, inspect `security/QuickstartOperationalContextResolver.java`,
`QuickstartPrincipalGrantRepository.java`, `docs/OPERATIONAL-GRANTS-CONTEXT.md` and the
canonical `db/operational-migrations/V20260914_001__operational_binding_and_principal_grants.sql`.
Do not use token authorities or the demo catalog as a revocable authorization source.

- The host reference profile binds one dedicated operational database to an immutable
  namespace/tenant/environment. Configure all three `app.security.operational-binding.*`
  properties explicitly; absence blocks resolution, partial values fail bean creation.
  Future registry readiness must verify persisted binding before advertising availability.
- Provision binding/grants administratively after the official migration. Runtime needs
  schema USAGE and only SELECT on the authorization tables, with no owner/admin role
  membership. Reads reject effective table/column write privileges; this is not a universal
  proof against role escalation or an administrator disabling triggers.
- Revoke by deactivation, preserving UUID/subject/namespace and monotonic row version.
  Administrative UPDATE must condition on the expected version and verify one returned row;
  the trigger increments versions but cannot enforce an administrator's WHERE predicate.
- Resolve the authenticated subject, reject divergent/repeated identity headers, and load
  the current grant on a separate READ COMMITTED `governanceReaderDataSource` connection.
  Never reuse an ambient transaction or the Config datasource for admission; account for
  an extra pool connection. Authorized result readers use `readCurrentInSnapshot` on their
  caller-owned physical read-only REPEATABLE READ connection, preserving one coherent snapshot.
  Publish Config server attributes only after authorization and clear previous bridge values
  on every attempt. Missing grants deny; infrastructure/binding failures stay unavailable.
- Validate well-formed Unicode scalar values before JDBC and identity hashing. Isolated
  UTF-16 surrogates can survive a signed JWT and be silently replaced by `?` by JDBC or
  a permissive UTF-8 encoder, borrowing another subject's grant and colliding fingerprints.
  Reject malformed input rather than normalizing/replacing it, use strict digest encoding,
  and compare the stored subject exactly with the authenticated subject. Keep valid
  supplementary characters distinct; Java limits remain UTF-16 code-unit limits. Prove
  both malformed high/low surrogates via real JWT/HTTP/PG and positive valid Unicode.
- The context's grant fingerprint does not authorize fields/targets/references, and its
  ResourceVersionScope is not installed globally. No new bulk route, job authorization or
  READY is implied. Review session versus legacy internal-delegation token admission when
  composing the actual provider/executor. Revocation applies to the next fresh lookup,
  not retroactively to an admitted transaction.

Run `QuickstartOperationalIdentityTest`, `QuickstartPrincipalGrantRepositoryPostgresTest`, `QuickstartOperationalContextHttpTest`
and the operational migrator tests; verify actual PostgreSQL versions in logs. On macOS ARM,
`embedded.postgres.binary.version` selects the test binary (default 17.11.0, 16.14.0 override).
Do not label other platforms as PG16/17 without runtime evidence. EmbeddedPostgres's
`getJdbcUrl(user, database)` embeds the user in the URL: assert `current_user` to avoid testing
with owner credentials accidentally. The HTTP fixture proves context resolution only;
write admission/CSRF, domain effects, replay/status/cancel and worker delegation need their
own integration gates. Existing route policies and demo grounding are not replaced by this source.

## Mission Participant Grants

When extending mission-participant update authorization, inspect the host's
`QuickstartPrincipalGrantRepository`, `V20261002_001__mission_participant_grants.sql`,
mission grant PostgreSQL proofs and `OPERATIONAL-GRANTS-CONTEXT.md`. These are host-owned
operational entitlements; Metadata owns the bulk protocol and Config the governed policy.

- Reuse the revocable parent grant and its revision. `MISSION_PARTICIPANT_UPDATE` requires
  explicit mission coverage, wire fields (`funcionarioId`, `papel`, `ordem`, `principal`,
  `resultado`) and employee-reference coverage. Department coverage or JWT authorities
  cannot grant this access. Empty references deny access to references; they never mean all.
- Persist employee references as relational rows with individual FK `RESTRICT`, not only
  arrays. Require administrative revocation before mission/employee deletion. Audit keeps
  historical identifiers without domain FKs so deletion cannot erase evidence. Keep the
  grant identity and append-only audit protected; do not provision grants through demo seeds.
- Administrative replacement requires expected revision and evidence, locks grant before
  the sorted union of old/new employees and mission, increments the parent once and records
  before/after scope atomically. Canonical no-op changes neither revision nor audit. Grant
  deactivation/authority removal clears mission scope before changing the parent and keeps
  departmental authorization/audit behavior intact. Mixed revocation uses grant → employees
  → missions → departments. Do not silently replace existing applied migrations.
- Keep runtime SELECT-only for coverage and without admin function, audit or sequence access.
  Harden new-object default/PUBLIC ACLs and provision administrator EXECUTE explicitly for
  the new P3 replacement function. Preserve intentional P1/P2 administrator grants.
  The reader must check unsafe effective privileges, use one SQL instruction for all scope
  in both RC admission and RR result reads, and avoid Cartesian products that duplicate rows.
  Validate exact typed rows/collections and fail closed on inconsistent or orphan scope.
- Prove real PostgreSQL FK denial followed by governed revocation/deletion with retained
  audit, stale revision/no-op, rollback, runtime privilege denial and coherent immutable
  scope reads. Update every constructor and fixture that consumes the extended grant.
  Schema-only fixtures still need domain key tables and the real migration; do not mask a
  missing migration by fabricating an empty mission scope in the reader. Run the official
  migrator PostgreSQL proof with separate migration/runtime identities; a Docker skip is
  not this proof. The host uses EmbeddedPostgres for this gate, including concurrent
  hosted bootstrap and migration history. Check actual baseline/version ordering before
  changing expected counts; do not weaken assertions to hide a missing or duplicate migration.

For the mission-participant mutation fence, inspect the additive
`V20261002_002__mission_participant_authorization_fence.sql`,
`MissionParticipantScopeAuthorizer` and the concrete bulk preparation before wiring adapters.
Retain the exact authenticated grant revision with a boolean-only SECURITY DEFINER function
on the same writable physical transaction. Check the real runtime login, binding, subject,
UUID, active authority and revision; runtime EXECUTE is restricted and defaults/PUBLIC are
revoked. Administrative G1 writers must acquire this parent grant before changing scope.

Require coverage of every target mission, explicit field (including SET to the same value)
and both current/proposed employee references. Bulk omission preserves intent; ordinary PUT
has separate effective-change semantics and must not be inferred from a mapper. Initial
missing and out-of-scope targets share one sanitized 404. Drift after authorized coordinate
discovery conflicts without acquiring a late employee or mission lock. Discover only scalar
target/population coordinates before E; fix the authorized missions, acquire sorted E→M,
recheck targets, then read/lock P and private team facts. Do not reread full target facts and
compare only afterwards: that leaves a reparenting window. Peers needed for aggregate checks
are not automatically editable. Prove the concrete preparation, grant fence and domain
mutation together on PostgreSQL with two connections; separate mock/lock tests alone do not
prove the complete chain. Keep the caller's live deadline throughout.
A scope-race oracle must distinguish forbidden private reads from rejection after such a
read: an HTTP conflict and absence of new locks alone are insufficient. Inspect prepared SQL
on the caller's session and require no private projection before denial. Verify the oracle
with a temporary test-only negative control that attempts the forbidden projection, fails
that specific assertion, and is restored byte for byte; never add a production bypass.

For the concrete mission protected-read provider, inspect
`MissionParticipantBulkReadAuthorizationProvider` and its unit/PostgreSQL proofs.
Capture and readback must reuse the caller-owned physical read-only REPEATABLE READ
connection. Reload the grant in that snapshot and use its actual revision and complete
scope evidence in the authorization fingerprint; an earlier READ COMMITTED admission
fingerprint cannot certify captured facts. Authorize the complete target set, explicit
fields and captured/current/proposed employee references using scalar coordinates before
any private team projection. A different reader may access results only with full current
coverage; creator identity alone neither grants access nor forbids an authorized delegate.
Keep namespace, operation and subject bound to trusted composition, reject unsupported
connections, and consume the caller's live deadline without renewing it. A tested provider
without concrete wiring does not expose an endpoint or certify READY. Distinguish these
public-release proofs from a later evaluator that requires an explicitly named candidate
Metadata coordinate; never install candidate code under the public version number.

For mission bulk mutation, distinguish that complete read-scope fingerprint from
`BulkEvaluationGovernance.authorizationFingerprint`. The latter must identify the grant
revision observed by the evaluator's RR capture through the existing
`Grant.fingerprint(MISSION_PARTICIPANT_UPDATE)`, never the earlier admission RC grant.
It is not field/reference coverage. All governed coverage/authority writers must bump that
revision by CAS; retain the exact revision by G in the operational transaction and check
captured/current/proposed coverage before private facts. A fingerprint incorporating every
target's mutable version cannot serve as per-unit grant evidence: a confirmed earlier item
would invalidate unrelated later items. Keep the read provider's complete fingerprint intact.

Revalidate a unit from its immutable intent through the Metadata protocol reader/codec;
compare structural binding, typed policy state/fingerprint and complete protected domain
facts. Acquire G→E→M→P once, reuse the protected graph for candidate validation and JPA
flush, and keep the SDK receipt on that same physical transaction. Do not recapture domain
in REQUIRES_NEW to pretend the mutation is fenced. Compare integral values by their exact
validated domain types across storage round trips, without JsonNode implementation equality
or a host canonical-JSON protocol. Preserve cohort versions: an earlier confirmed write in
the same mission may conflict with the next unit; never absorb that drift to allow a joint
leader swap. Unrelated missions must remain independently executable.

Use the SDK's protected reservation and advance flow. Receipt/admission replay precedes
gates exclusive to new effects; recovery reconciles evidence without dispatching fresh
mutations. Prove real domain+receipt commit/rollback, no repeated callback on replay,
revocation waiting for retained G, stale facts/policy rejection and the unchanged live unit
budget with PostgreSQL/JPA. Internal adapters and test-only composition do not prove HTTP,
production READY, public dependency adoption or cross-database atomicity with Config.

The SQL timeout bounds the instruction, not the number of authorization rows or Java
materialization time. IAM coverage is not the bulk target limit. Before P3 execution/READY
or B7 closure, prove expected scope volume, pool pressure and memory limits; do not claim
an end-to-end SLA from setQueryTimeout alone.

This persistence/read foundation does not expose READY, execute a bulk mutation, authorize
peer editing, or prove an HTTP adapter. Evaluation and execution must still authorize all
current/proposed references, share grant fencing and protect domain+receipt in one physical
transaction. Do not infer deployment/public adoption from local candidate proofs.

## Exposure Matrix Before Editing

Inventory the route with all of these columns before adding a matcher or exception:

| Surface | Owner | Method | Browser credential/CSRF mode | Origin/CORS rule | Required response headers | Rate-limit class | Default policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| static docs/Swagger | host | GET/HEAD | none | public docs policy | only intended public headers | optional public-read | explicitly public |
| actuator health/info | host | GET | none | health-check policy | no sensitive values | health policy | public only when intended |
| actuator env/configprops | host | GET | authenticated | no public exposure | sanitized diagnostics only | protected | never read-open |
| `/schemas/**` | metadata starter | GET and filtered POST | contract-specific | schemas aggregator gate | `ETag`, `X-Schema-Hash` when published | public-query | host-gated public surface |
| `/api/praxis/config/**` | config starter | contract-specific | config CSRF/origin/auth policy | explicit allowed browser/proxy policy | `ETag` and config headers | config | host-governed, not automatically open |
| `/api/praxis/runtime/**` | config starter | contract-specific | principal/context policy | explicit CORS | safe projection headers only | runtime policy | never inferred from read-open labels |
| `/api/**` resources | quickstart/metadata | method-specific | session + CSRF unless explicit public query | explicit CORS | schema/config headers where contract says so | read/query/action class | authenticated by default |

Classify the proposed change before coding: `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only a real host exposure gap belongs in quickstart security; never create a local endpoint, header alias, schema, or config persistence rule to patch a starter gap.

## Matcher And Method Rules

Spring matcher order is policy. Review the complete ordered chain, not the one matcher being changed.

- Start from deny/authenticated-by-default; document every `permitAll`, method exception, and public POST.
- `read-open` is a demonstration policy, not generic authorization. Scope it by HTTP method and canonical endpoint class; public filter/options/locate/export/stats calls need explicit data-sensitivity and rate-limit evidence.
- When a governed mutation shares a path pattern with a broad demo exception (for example, a POST action wildcard), place the explicit mutation matcher first. Require a non-anonymous authenticated principal and apply the global write kill switch before the application performs current-grant and resource-scope authorization; do not let the demo exception bypass either gate. Prove anonymous requests receive the canonical 401 and authenticated requests under the write-disabled policy receive 403 on every governed mutation route.
- `write-disabled` deny rules interact with earlier exceptions. Prove which public query/config/workflow calls intentionally win and which writes remain denied.
- `schemasAggregatorEnabled` may expose only the metadata routes required for the structural contract. It does not make all metadata or actuator routes public.
- Keep `/actuator/env` and sensitive actuator diagnostics authenticated and non-exposed even when `read-open` is enabled.
- `OPTIONS` is a CORS preflight concern, not authorization evidence. Test preflight separately from the actual credentialed request.
- Do not route policy by URL labels, aliases, keyword checks, or ad hoc regexes. Use explicit Spring path patterns, methods, canonical `ApiPaths`, and property-backed policy decisions.
- Scope authentication entry points with the same care as authorization matchers. In Spring Security, a lone `defaultAuthenticationEntryPointFor(entryPoint, matcher)` mapping can be promoted to the default entry point for the whole filter chain; do not assume its matcher will constrain it. When an entry point is meant for one surface, configure an explicit fallback that preserves the legacy response elsewhere and test both an in-scope anonymous request and an out-of-scope protected route/method.

## CORS And Contract Headers

CORS is part of the browser-visible Praxis contract.

- Use explicit official origins whenever cookies or credentials are enabled. A wildcard origin must disable credentials.
- Do not invent ports or origins. Use the documented official local origins and deployment origins from properties.
- Allowed methods and headers must match the public API surface, including preflight for `PUT`, `PATCH`, `DELETE`, config/AI calls, and schema reads only when actually supported.
- Expose non-simple canonical response headers that browser consumers must read. This includes `ETag` for config conditional persistence and `X-Schema-Hash` or other starter-published schema validators when applicable. `Access-Control-Expose-Headers` must come from the host CORS policy; clients cannot recover an unexposed header.
- Test allowed credentialed origins, blocked origins, wildcard-without-credentials behavior, allowed methods, and exposed headers with browser-equivalent requests.

## Config Origin, Proxy, And Rate-Limit Trust

`ConfigOriginRestrictionFilter` is operational host governance for `/api/praxis/config/**`; it complements but does not replace authentication, authorization, CSRF, tenant/user/environment resolution, ETag, or server-side AI principal policy.

- `permitAll` never means ungoverned config access. Preserve an explicit allowed-origin and method policy for browser traffic.
- Prefer canonical `Origin`; use `Referer` only as a parsed origin fallback. Missing/invalid browser provenance must fail closed unless an explicit, separately authenticated service-to-service policy applies.
- Do not treat caller-controlled `Host`, `X-Forwarded-Host`, `X-Forwarded-Proto`, `Forwarded`, or `X-Forwarded-For` headers as trusted facts on a directly reachable app.
- Honor forwarded headers only behind an explicitly configured trusted-proxy boundary. Origin reconstruction and rate-limit client identity must use the same trust policy.
- A proxy normalization policy belongs to the host/deployment boundary. Do not solve it with an Angular header, a config-starter bypass, or permissive origin fallback.
- Rate limiting is abuse protection, not authorization. Use distinct buckets for login, public read, public query, bulk action, config, and any high-cost AI/SSE surface; never let a forged forwarding header create arbitrary buckets.
- Include `Retry-After`, bounded/safe error bodies, and diagnostics that do not leak secrets, tokens, or private config values.

Apply the dedicated AI per-client rate limit before the broader config limit for
`/api/praxis/config/ai/**`. Keep its limit/window externally configurable and
prove denial without triggering a provider call. The reference in-memory
limiter is host baseline only; production gateway/WAF and provider project
budgets remain separate controls. Pair provider-cost or probe work with
`praxis-config-ai-provider-operations`.

## CSRF, Session, And Filter Chain

Cookie JWT authentication, CSRF, origin governance, and rate limiting have separate responsibilities.

- Inspect `EnterpriseSessionStore`, `EnterpriseSessionLifecycle`, and `CookieJwtAuthenticationFilter` together. A signed JWT of kind `SESSION` is accepted only with an active persisted issuance. In JDBC/real HTTP fixtures, issue it through `EnterpriseSessionLifecycle.issue` after server-side authentication/grant preparation and verify the persisted credential/subject before the first request. Direct `JwtTokenService.generate` does not establish that session; never replace SESSION with INTERNAL_DELEGATION or mock active-session checks to claim this proof.
- Prepare session storage on the operational datasource before issuance, with only the fixture runtime privileges actually required. A disposable test schema may use an explicitly sourced current schema snapshot, but must be labeled TESTONLY. It does not recover original migration bytes/checksums or prove Flyway, deployment, membership selection, or production grants. Preserve the original failed run and repeat only the affected focal after diagnosis/review.
- Distinguish direct ACL entries from effective privileges and from the role actually configured in the running host. Check relevant SELECT/INSERT/UPDATE privileges without copying user/session data; do not silently repair hosted grants during a fixture test.
- Both cookie and bearer credentials of kind SESSION need the same active issuance bound to UUID, subject and exact expiry. Changing the transport to bearer does not remove SESSION admission. INTERNAL_DELEGATION is an explicit internal bearer kind, not a substitute for browser-session/context/grant fixtures.
- In real HTTP fixtures, issue once per intended session and reuse the credential through its journey. Cleanup must address only that fixture's issuance UUID and subject, preserving unrelated credentials. Reissuing on every request can mask revocation negatives.
- In WebMvc policy slices that exclude persistence, retain real JWT validation, the JWT filter, controller and SecurityConfig. A narrow stateful lifecycle double may simulate issuance/revocation only when it binds UUID, subject and exact expiry and rejects unissued, revoked or expired credentials. Clear only its own state between scenarios. Never return isActive=true unconditionally or inject a principal to bypass the JWT filter. This boundary proves slice policy, not PostgreSQL, transaction participation, tenant/context or grants; a CSRF-disabled role slice is not CSRF evidence.
- Keep reachable positives and existing role/grant negatives. For SPA policy, prove signed-but-unissued token rejection, old-cookie denial after identity switch, and active-session writes rejecting absent or mismatched XSRF while matching tokens reach the intended action. Do not weaken statuses, filters, permission policy or CSRF exceptions to repair fixture prerequisites. Reuse valid evidence from unaffected classes and preserve the failed campaign; repeat only corrected paths unless a separate adoption gate requires broader verification.
- Cookie authentication establishes the Spring principal; validate cookie attributes (`Secure`, `HttpOnly`, `SameSite`, lifetime, and configured name) by environment.
- When CSRF is enabled, a SPA cookie/header flow must accept the intended raw header and retain server-rendered XOR behavior. Prove both token issuance and a protected write with matching cookie/header.
- Audit CSRF authentication lifecycle, not just `SessionCreationPolicy.STATELESS`.
  In Security6.5.11 an implicitly installed `SessionManagementFilter` can call
  `CsrfAuthenticationStrategy` whenever the cookie-JWT filter reconstructs an
  Authentication. Rotating XSRF on each ordinary authenticated request is a host
  bug: an unchanged SESSION with concurrent context GETs must keep its existing
  cookie/header pair stable. Inspect the actual strategies/filter chain and fix
  the host owner; do not hide it with frontend retries or an old-pair Node CAS replay.
- Rotate/clear CSRF explicitly at actual successful login, successful identity
  switch and logout boundaries. Keep token issuance when absent, the SPA raw
  header/XOR contract, origin controls and missing/mismatch rejection. Do not
  disable CSRF or widen ignore matchers to fix lifecycle rotation. Failed login
  must not rotate an established pair. Reuse an existing registered repository;
  removing automatic per-request rotation is not removal of CSRF validation.
- Prove sequential and concurrent authenticated GET/protected-write pair stability,
  rotation at real auth boundaries, unchanged SESSION during a context-only switch,
  and natural browser continuation of stale selection CAS reaching context409.
  A generic403 caused by CSRF is not context-conflict evidence. Record only safe
  booleans/hashes, never cookie/header/password values; preserve failed campaigns
  and require current real SESSION/Neon proof before calling the fix accepted.
  Holding/forwarding a real Config ACK after commit is a separate transport proof,
  not authorization to bypass CSRF on context commands.
- Any CSRF ignore matcher, especially `/api/praxis/config/**`, needs an equivalent stronger host policy and a documented reason. Do not disable CSRF globally to repair a local request.
- Assert filter order and behavior: origin/rate-limit gates must run before expensive public work, authentication must populate protected endpoints correctly, and CSRF cookie exposure must not become an authorization bypass.
- Local header identity for AI is an explicitly configured development exception. Corporate mode must resolve identity server-side; caller headers are not authorization proof.

## Corporate page CSRF and cross-origin bootstrap

When adopting the page host, inspect `SpaCsrfTokenLifecycle`, `SecurityConfig`,
`SpaCsrfTokenRequestHandler`, `AuthController`, `SecurityConfigSpaCsrfPolicyTest`
and `SecurityConfigCorsTest` together. The lifecycle bean owns the one cookie
repository shared by the filter chain and actual auth-boundary rotation. Keep
ordinary cookie-JWT reconstruction from invoking automatic login rotation;
retain raw request-header validation and XOR request attributes/parameters.

For an explicitly allowed credentialed origin, bootstrap through
`GET /auth/session` with browser credentials included and read the exposed raw
`X-XSRF-TOKEN` response header. A SPA on another host cannot read the API's
host-only cookie through `document.cookie`. The browser retains SESSION and
XSRF cookies; send the returned raw value in `X-XSRF-TOKEN` on protected writes.
Consume the fresh header after successful login or identity switch and clear it
on logout. Auth responses are `no-store`; the bootstrap can return401 with a
CSRF token, which grants no SESSION or operation authority. Do not expect every
Config/runtime response to republish the header. CORS must expose
`X-XSRF-TOKEN` and lifecycle `Location` as well as existing validators.

Cross-site production cookies require HTTPS, `Secure` and `SameSite=None` for
both SESSION and XSRF, with SESSION still HttpOnly. Same-origin/local Lax tests
and a manual HTTP cookie jar do not prove browser cookie delivery, cross-site
policy, CORS enforcement or third-party-cookie availability. Use the official
origin catalog and environment properties; test the deployed browser path
separately. Never export raw cookie/header pairs in assertions, traces or logs.

The existing Config CSRF exclusion must subtract both `/api/praxis/config/pages`
and `/api/praxis/config/pages/**`, and both `/api/praxis/config/ui-layouts` and
`/api/praxis/config/ui-layouts/**`. Use the same Spring MVC-aware path semantics
as controller dispatch, not raw request-URI prefix checks. Preserve unrelated
Config exclusions deliberately; origin admission alone does not exempt these
page/lifecycle writes from CSRF. For every canonical and encoded equivalent
(for example `%70ages` and `ui%2Dlayouts`), prove a matching pair reaches the
intended controller and missing/mismatched pairs receive403. A firewall404 or
an unreachable positive does not prove the matcher. Keep broader firewall
encoding restrictions unchanged.

Run the focused SPA/CORS/firewall and auth-lifecycle tests with the host's
published dependency coordinates. Protecting page/lifecycle paths does not
install their providers or prove their journey. When reviewing a separately
composed page host, pair with `praxis-java-config-boundary-integration` and its
actual HTTP gate: require login, current SESSION, opaque choices/CAS and the
promised operations on the assigned remote Neon branch with ordinary runtime
roles. Compare status before JSON and retain only safe hashes; prove logout and
retained-SESSION401 even after a failed scenario. Reuse component evidence only
when source identity, dependencies and limits are explicit. A policy slice or
SESSION/CSRF pass does not certify publication, navigation, copy, browser cookie
behavior or a new full HTTP campaign. Keep private-candidate/public-adoption
and integration gates separate.

## Operational SESSION storage installation

Inspect `EnterpriseSessionStore`, the operational migrator, and
`docs/ENTERPRISE-SESSION-OPERATIONAL-PREREQUISITE.md` before admitting a hosted
SESSION flow. The reviewed forward
`V20261022_001__enterprise_session_operational_prerequisite.sql` belongs to the
segregated API migration owner, never the application login or Config datasource.
The owner must be able to issue its `GRANT USAGE ON SCHEMA public` (schema
ownership or a grant option for USAGE), in addition to its CREATE/USAGE, TEMP and
predecessor-table ownership requirements. Health UP and a signed SESSION JWT do
not replace a persisted issuance. The forward does not install enterprise
membership, payroll grants or G4 composition.

The intended ordinary-runtime profile is schema USAGE and table SELECT, INSERT
only on `credential_id`, `subject_id`, `expires_at`, and UPDATE only on
`revoked_at`, `revision`, `tenant_id`, `environment`, `organization_id`,
`sector_id`, `profile_id`. Preserve compatible non-grantable canonical column
SELECT grants; do not widen INSERT/UPDATE to the table. Deny UPDATE of issuance
identity/subject/expiry and INSERT of revision/selection fields. Inspect
effective privileges, including PUBLIC, grant options, role membership and
SET ROLE through NOINHERIT, plus owner/server-role and schema/database CREATE
reachability. Do not assume Neon SUPERUSER or repair global grants/default
privileges to make a predecessor pass.

Existing storage is admitted only after a strict parsed-catalog comparison
under the owner lock, preserving rows while rejecting unexpected structure,
dependencies, ownership or ACLs. A TESTONLY fixture cannot reconstruct retired
Flyway resources; missing history must fail before the forward without
clean/repair/bypass. Pair with `praxis-api-quickstart-operational-proof` for the
required `AssignedNeonDatabase` proof of the packaged migration, repeat-zero,
real ordinary-runtime lifecycle and forbidden writes. Historical remote results,
offline source checks and same-resource rollback negatives are distinct from
fresh installation and authenticated HTTP adoption; report each boundary
separately.

## Path Normalization And HttpFirewall

Treat URL encoding as a public security contract, not a convenience setting.

- Inventory the exact canonical config identifier/path behavior that requires encoded input before enabling encoded slash, double slash, percent, or semicolon support.
- Allow the minimum set of encodings proven necessary. A global `StrictHttpFirewall` relaxation affects docs, schemas, runtime, and business routes too.
- Current quickstart policy allows `%2F` only under `/api/praxis/config/**`, because some `praxis-config-starter` routes still receive `componentId` as `@PathVariable` and canonical refs can contain `/`. Keep schemas, actuator, docs, runtime, and business routes on strict firewall behavior.
- Do not re-enable global encoded double slash, encoded percent, or semicolon support. `%2F%2F`, `%25`, path parameters, and `%2F` outside config must remain rejected unless a new source-audited canonical contract proves otherwise.
- Prefer the query-string variants of UI config endpoints (`componentType` + `componentId`) when a client can choose identifier transport; the host exception exists to preserve existing config path-variable compatibility, not to encourage new encoded-path designs.
- Reject malformed, ambiguous, double-slash, semicolon, and path-parameter variants unless an explicitly documented canonical route requires them.
- If the firewall cannot scope an exception safely, redesign identifier transport at the canonical config boundary rather than leaving a broad host bypass.
- Verify allowed canonical config identifiers and adversarial normalized paths in focused firewall/security tests.

## Documentation And Properties

Keep `application*.properties`, deployment variables, README, security docs, HTTP examples, and test profiles synchronized.

- Do not document a non-empty read-open whitelist as a default when the effective property default is empty.
- Distinguish base, dev, and prod defaults for CSRF, read-open, cookie security, CORS, config origin restriction, schemas aggregator, rate limits, and AI local identity.
- Mark demo-only exposure (`read-open`, `write-disabled`, bulk actions, local identities) as host demonstration policy, not a platform guarantee.
- Do not print secrets, JWTs, credentials, raw config payloads, or sensitive actuator values in startup logs, test fixtures, docs, or HTTP examples.

## Validation

Run the smallest security gate that proves the changed matrix.

```bash
mvn "-Dtest=SecurityConfigHttpFirewallTest,SecurityConfigActuatorPolicyTest,SecurityConfigAiPatchPolicyTest,SecurityConfigReadOpenStatsPolicyTest,SecurityConfigSpaCsrfPolicyTest,SecurityConfigCorsTest,ConfigOriginRestrictionFilterTest,PublicApiRateLimitFilterTest" test
```

For config/schema browser contract changes, add focused downstream proof:

```bash
mvn "-Dtest=AiPatchSchemaResolutionIsolatedIntegrationTest,AgenticAuthoringStreamIsolatedIntegrationTest" test
```

Add negative tests for blocked origin, forged forwarded host/proto/client IP, missing/invalid provenance, wildcard credentials, absent exposed `ETag`/`X-Schema-Hash`, protected actuator, CSRF mismatch, write-disabled precedence, excessive public/AI calls, and malformed encoded paths. Use real HTTP/browser evidence when the changed behavior is cross-origin; same-origin MockMvc alone cannot prove CORS header visibility.

Review public docs, properties, quickstart HTTP examples, config/metadata downstream consumers, and any related starter smoke after a public exposure change. State exactly which owner was changed and why the remaining derived artifacts were unaffected.

## Administrative Bulk Publication Exposure

For the three basic bulk publication POSTs, inspect the controller and exact host
`ApiPaths.Operations` matchers before changing security exposure. Each command needs
its own current grant permission (`BULK_PUBLICATION_PUBLISH`, `_RECONCILE`, `_SUSPEND`),
active SESSION admission and configured binding; ADMIN/JWT authorities and demo
read-open/bulk settings cannot substitute authorization. Preserve the write-disabled
matcher for all three paths and keep current grant reads outside SDK control locks.

`ConfigOriginRestrictionFilter` governs Config paths, not these operations paths.
Use the existing CORS and CSRF chain: credentialed official Origin, actual cookie
repository emission via authenticated `/auth/session`, and raw `X-XSRF-TOKEN` equal
to the `XSRF-TOKEN` cookie. Bearer SESSION has no automatic CSRF exemption. Test
missing/mismatched XSRF on all commands, successful cookie/header pairs, allowed
preflight and actual credentialed request, foreign preflight/POST rejection, and
write-disabled rejection with valid XSRF. Do not use a CSRF postprocessor to claim
real repository issuance. MVC policy with simulated SESSION and mocked SDK/grant
is server-filter proof, not browser execution, persistence or deployed availability.

Keep the minimal no-store response and generic 503. Do not leak fingerprints, current
grants or installation errors, infer rollback, or retry publication automatically.
Document the logical-deployment-wide suspension effect and a protected generation/evidence
procedure before administrative commands or basic operational availability acceptance. Strict original JSON and generation bounds
belong to admission; existing SDK publication semantics remain canonical.

## Managed bulk roles and effective SESSION privileges

Inspect the Metadata-owned managed migration and role preflights before changing
host IAM. PostgreSQL 17 automatic ADMIN-only membership is role administration,
not inherited data access or SET authority. Only the exact canonical administrative edge with the schema owner as MEMBER
is admitted: trusted bootstrap-superuser GRANTOR, ADMIN true, INHERIT false, SET
false and canonical multiplicity. The target ROLE must belong to the applicable
canonical check; this includes runtime/control roles created by that owner and
internal owner roles where the actual predicate admits them. This never allows
a runtime/control MEMBER to reach an internal owner.
Check the exact artifact before relying on it; rc.155 lacks this correction.

Temporary function-owner SET authority and schema CREATE must be scoped to the
actual owning role and restored transactionally. Explicit grantor provenance
matters: revoke only the temporary self-issued edge, preserving the trusted
administrative edge. Reject unsafe pre-state before entering scopes; do not
silently remove unexpected grants, memberships or role attributes. Runtime and
control identities must remain separated from internal owner reachability.
Never substitute a host superuser, arbitrary SET ROLE or broad grant recipe for
a canonical starter correction. Capacity authority has a separate catalogue and
must not be certified from execution-storage proof.

For SESSION failures, derive the required columns from actual store SQL and
inspect effective table **or column** privileges, role closure, schema USAGE and
grant options. Column-scoped INSERT/UPDATE can satisfy the canonical store even
when table-level checks are false. Do not infer missing access from table ACLs
alone or promote least-privilege column grants to table-wide writes. Bind the
catalogue observation to the exact database/role and follow with real SESSION/HTTP
proof; SQL permission evidence alone does not certify authentication or browser
policy. Keep credentials and private connection settings out of logs/reports.
