---
name: praxis-api-quickstart-operational-proof
description: Use when Codex must implement, audit, or diagnose Praxis API Quickstart as the real Spring Boot reference host: Maven starter composition and versions, bootstrap/properties/datasources, security and browser policy, metadata/config/runtime HTTP integration, schemas and discovery, agentic authoring/SSE host proof, deployment identity, or ownership routing between quickstart, metadata starter, config starter, and Angular consumers.
---

# Praxis API Quickstart Operational Proof

Use this skill for the Quickstart's role as the operational reference host. It proves that canonical Praxis contracts survive Maven packaging, Spring Boot auto-configuration, security policy, real persistence, and HTTP consumption. It must be a thin, explicit integration point, never a parallel implementation of metadata, configuration, AI, or business-decision semantics.

## Classify And Map Impact

Classify before editing:

- `local-pequena`: host-only implementation or property change with no public contract change.
- `transversal`: quickstart plus a starter, pilot, HTTP corpus, Angular consumer, or public docs.
- `contrato-publico`: `ApiPaths`, OpenAPI groups, `/schemas/**`, headers/ETag, capabilities, `/api/praxis/config/**`, security exposure, HTTP/SSE route, or published dependency behavior.
- `arquitetural`: a change to host/starter ownership, resource/config boundary, security trust boundary, persistence topology, or the operational-reference role.

For `transversal`, `contrato-publico`, or `arquitetural`, identify the canonical owner, affected resource/config scope, direct consumers, docs/examples/corpus, focused local proof, deployment proof, and breaking-change risk before patching.

## Source Audit

Read the host composition and the exact downstream proof before deciding where the fix belongs:

- `praxis-api-quickstart/AGENTS.md`, `README.md`, and `pom.xml`
- `ApiQuickstartApplication.java`, `ApiPaths.java`, and `application*.properties`
- `SecurityConfig.java`, `ConfigOriginRestrictionFilter.java`, and related security filters
- `QuickstartMetadataMigrationIntegrationTest`, `EventosFolhaPilotIntegrationTest`, and `OpenApiGroupResolutionIsolatedIntegrationTest`
- `ResourceEntityLookupGovernanceIntegrationTest`, `ProcurementExternalOptionSourceProviderIntegrationTest`, and `VwStatsSmokeHttpTest` when option-source contracts are hosted
- `AiPatchSchemaResolutionIsolatedIntegrationTest` and `AgenticAuthoringStreamIsolatedIntegrationTest`
- the affected host authorization adapter and deterministic database fixture when a governed E2E lane exercises principal-specific capabilities
- `PraxisCockpitStarterConsumptionIntegrationTest` and `ActuatorInfoBuildContractIntegrationTest`
- `docs/COCKPIT-QUICKSTART-REFERENCE.md` and `docs/AI-HOST-BUSINESS-GROUNDING-GUIDE.md`

For a suspected starter defect, inspect the owner repository before proposing a host adaptation. The quickstart test is downstream evidence, not a replacement for the owner test.

## Integration Topology And Owners

The quickstart owns Spring Boot composition, pinned Maven versions, host properties, concrete pilot domains, operational datasource/migrations, host security, and integration tests.

| Concern | Canonical owner | Quickstart responsibility |
| --- | --- | --- |
| `x-ui`, filtered schemas, OpenAPI resolution, schema headers, actions/surfaces/capabilities, HATEOAS, Cockpit bundle | `praxis-metadata-starter` | declare real resources and prove the published contract through HTTP |
| config persistence, AI registry/context/patch/stream, domain catalog/knowledge/rules, ETag lifecycle, materializations | `praxis-config-starter` | host the version, provide policy/persistence/config, and prove use in HTTP |
| paths, controller annotations, DTOs, demo data, operational migrations | quickstart | model concrete reference domains using canonical starter contracts |
| UI materialization after contract publication | `praxis-ui-angular` | provide stable HTTP evidence; do not reimplement client semantics in Java |

The metadata and config starters are parallel canonical boundaries. Never move a metadata behavior into config or a config decision into schema/UI configuration merely because the host can see both.

## Ownership Routing

Route by evidence, not by the route name alone:

- `/schemas/**`, `x-ui`, schema hashes/ETag, `_links`, operation resolution, action/surface/capability catalog, and Cockpit assets: inspect metadata starter first.
- `/api/praxis/config/**`, config scope/headers/ETag, registry/context/authoring/patch/stream, Domain Catalog/Knowledge/Rule/Federation: inspect config starter first.
- CORS/CSRF/origin, cookies, rate limits, trusted proxy policy, allowed public reads, datasource wiring, app properties, Maven versions, pilot data, deployment identity: quickstart owns the host integration.
- A correct HTTP contract rendered or consumed incorrectly: route to Angular only after proving the backend contract.

Do not add endpoint aliases, DTO copies, Spring overrides, local manifest validators, local AI orchestration, browser bypasses, or schema patches to cover a starter gap. Correct the owner and keep only the smallest quickstart proof.

## Protected Bulk Capture Adoption

For protected proposal capture and recapture in the host, use
`praxis-java-command-concurrency-authoring` and inspect
`EventosFolhaApprovalProposalService`, its unit tests and
`EventosFolhaApprovalEvaluationHttpTest`. Prove commit/rollback, current scoped grants,
restricted runtime credentials and safe SQL lock failure on real PostgreSQL. A
persisted snapshot or equivalent recapture is not READY or execution; keep migration
identity separate and leave uncomposed public capabilities unavailable.

When a SQL timeout proof also performs readiness/discovery, follow
[the bulk SQL phase proof](references/bulk-sql-phase-proof.md) to observe the actual
blocked statement, separate HTTP preparation from storage timing, and preserve
evidence before cleaning stale compiled diagnostics.

Before inserting a proposal or consuming any proposal/quota allocation, authorize the
entire explicit target set against the current scoped grant and temporal assignments.
Read the target facts and make that complete authorization decision in one consistent
read-only database snapshot. A target that is absent and one outside current scope must
produce the same redacted response, and neither may leave a proposal, evaluation,
manifest, preview or quota allocation. Do not rely on a later proposal/result reader to
make an already-persisted capture safe. A comparison-only revalidation of a creator-owned
proposal may return only whether evidence still matches and must not persist new evidence,
consume quota or authorize execution. If it refreshes/persists a proposal or allocates
quota, it is a new capture and must perform the same full-set authorization first;
execution still rechecks current governance under each unit's lock.

## Preserve Historical Authorization Dependencies

Before composing historical bulk readers, trace target identity through mutable
parents to the facts needed for authorization. A target ETag does not attest an
unversioned parent. For payroll, the event links to a payroll sheet whose employee
and year/month determine the employee and first day of the competence month.
Capture those minimal dependencies in protected, provider-versioned evidence from
one consistent query, reusing Metadata evidence codecs and digests. Reject missing
relationships, invalid identities and invalid calendar values; never repair them
from today's entity or a demonstration department scope.

Do not copy whole domain entities or salaries into evidence for convenience, and
do not serialize protected facts into results, diagnostics or logs. Historical
employee/competence links are not historical permissions: current grants and the
authoritative temporal assignment still require the read composition's coherent
snapshot. Old evidence without required dependencies cannot silently acquire them
from current rows; preserve confirmed receipt replay independently of new-mutation
gates and leave unsupported public projections closed.

Prove persistence and reload after changing the parent without changing the target
version, strict invalid-input failure, and existing execution/replay regressions.
Capturing evidence alone does not stabilize the parent until commit. Before using
these dependencies to authorize mutations, separately define the lock order,
revalidation and concurrency proof across the target and its mutable parents.
Keep that gate explicit; this capture increment does not certify granular access,
public readback, or READY.

## Stabilize Mutable Parent Dependencies During Admission

For a new payroll mutation, compare the protected attribution tuple from the
proposal with fresh evidence and scalar rows read under transaction-bound locks.
Use the Metadata unit's operational connection: durable control/execution locks,
then the historical payroll parent `FOR SHARE`, then the event `FOR UPDATE`.
Keep both domain locks until domain, transition audit and receipt commit together.
A parent `FOR KEY SHARE` does not protect non-key attribution fields; a parent
`FOR UPDATE` unnecessarily conflicts with the FK `KEY SHARE` used by reparenting.
Do not substitute a cached JPA parent for the locked scalar observation.

Inventory every parent/child writer first, including generated mappers and delete
paths. An update DTO that omits children must not clear an owning child collection
through a generated merge mapper. Prove the real JPA path and preserve children
explicitly where they are outside that update contract. Test with the production
FK/NOT NULL behavior, not only unconstrained fixture tables. Provision the minimum
row-lock privilege explicitly; PostgreSQL requires UPDATE privilege on at least
one parent column in addition to the applicable SELECT privileges.

Missing or malformed protected dependency facts fail closed. A changed tuple uses
the existing `TARGET_DEPENDENCY_CHANGED` result, without a domain effect; distinguish
its durable admission/decision record from a confirmed mutation receipt. Preserve deadline limits,
rollback and receipt-first replay. Reapply the remaining unit budget on the bound
connection immediately before each parent/child lock and refresh, preserving stricter
database limits: governance reads may already have consumed most of the initial budget.
Prove both concurrent writer orders, parent-lock
timeout, FK reparent compatibility, stale JPA context and replay after parent change.
This lock proof does not grant departments/fields/references or complete the public
reader's authorization snapshot.

## Protected Bulk Execution Adoption

For an internal host pilot that executes a captured proposal, use the Metadata
Starter durable-execution contract and the focused host HTTP/PostgreSQL proof. Do
not recreate reservation, idempotency, per-ordinal admission, receipts, recovery,
or fencing in Quickstart. Metadata owns those semantics; Config remains the
separate source of current policy, and the host owns the concrete domain mutation.

For every ordinal, the host must re-read the current Config policy and scoped
grant, then lock the target row and compare its permitted state and expected
version under that lock. Only after admission should the callback mutate the
domain entity and write its transition audit; Metadata persists the receipt in
the same operational transaction. Do not use `REQUIRES_NEW`, manually commit or
roll back, or use transition replay as execution authority. Config and API use
separate databases, so the proof is point-in-time admission, not distributed
atomicity.

Propagate the kernel's remaining monotonic unit budget into every Config policy read
and scoped-grant JDBC read. These are sequential parts of one five-second unit budget,
not independent five-second allowances; round query timeouts down and fail closed when
the remainder is too small. Bound API and Config connection-pool acquisition separately
so a saturated pool cannot spend the entire unit budget waiting for a connection. Recheck
the remaining budget after each external read and immediately before target mutation.
A timeout or expired budget must leave the domain row, transition audit, and receipt
unchanged for that ordinal and stop the suffix. PostgreSQL tests must exhaust the budget
through an independently acquired Config/grant connection, not by sleeping on the API
transaction itself.

Read an existing receipt before deadline or fresh-governance gates. If commit
acknowledgement is uncertain, return the confirmed prefix, `UNKNOWN` for the
current ordinal, and preserve the unresolved execution state. Do not label the
suffix `NOT_PROCESSED` merely because this request stopped dispatching units:
that result requires a durable, reconciled terminal boundary proving that those
targets will not be executed by this execution. While it remains active or needs
reconciliation, use only the unresolved/pending representation supported by the
canonical contract; never fabricate certainty or a new item status. A partial
commit must remain discoverable through its execution identity and confirmed
results, not disappear behind a generic error. Retry must read the receipt
without rerunning domain or audit callbacks. Recovery fences the previous owner
and reconstructs recorded outcomes only; it never invokes a mutation callback.
Common grant/policy loss, timeout, or unavailable governance must stop the
unstarted suffix. A target-specific state/version conflict remains a durable
per-item result. Keep reservation/recovery probes test-only until the canonical
public confirmation protocol and consumer contract are released together.

Until the durable proposal protocol and its complete lifecycle are proved against the published
starter artifacts, distinguish it from any legacy direct bulk action that exists in the base
host. Inspect the current controller, action annotations, discovery and OpenAPI before making
availability claims: do not document a legacy route as absent when the integrated host still
exposes it. State explicitly that a direct legacy command is not the persisted proposal/receipt
protocol, and that a candidate replacement is not integrated or deployed. A Config
`approval_policy` materialization alone does not prove that the new durable protocol is live.
Smoke scripts may verify that materialization and report the new protocol as pending, but must
not claim its host gate passed. When a change actually removes or disables the legacy action,
prove that removal in its own discovery/capability/OpenAPI contract test; until then, test and
document the behavior that the current source really provides.

The focused proof must exercise the real Config and API PostgreSQL stores,
including grants, a two-item committed prefix, proposal expiry after reservation,
policy/grant changes between items, a target race, isolated unit rollback,
commit-acknowledgement loss and receipt readback, Config timeout, replay under
current authorization, redacted responses, and recovery without mutation. A
candidate probe is not a production endpoint, published capability, or proof
that the public workflow is ready. Use
`praxis-java-command-concurrency-authoring` and the Metadata Starter bulk
execution contract when reviewing these guarantees.

## Preserve Confirmation Outcomes After Proposal Purge

When a confirmation retry arrives after retention removed its proposal/evaluation,
do not add a host-side tombstone query or restore a proposal from execution storage.
Let the host confirmation service reject the absent proposal, then resolve only
that absence through the existing `BulkAuthorizedProposalReader`. Distinguish its
`TOMBSTONED` state (purged proposal plus retained tombstone, after current global
operation grant and historical creator-scope digest match) from `GONE` (a live
proposal whose TTL elapsed after full-set authorization). Within this absence
fallback, only `TOMBSTONED` maps to payload-free `410`; `GONE`, `COMPLETE`, unknown
IDs, and cross-scope requests keep the same redacted `404`. The normal creator-scoped
confirmation path still returns its existing `410` for a retained expired proposal
that it can find; a delegated confirmation remains `404`. The proposal-read route may
map both `GONE` and `TOMBSTONED` to `410`. An unavailable reader fails closed. Prove the actual
purge procedure and retry through the production HTTP mapping, and prove that a
delegated reader of both live and expired proposals cannot confirm another creator's
proposal. Include unchanged receipts, audit and domain state. Keep the cancellation
route's OpenAPI response set aligned with its actual `410` mapping.

Validate client-supplied `X-Correlation-ID` and `X-Request-ID` before proposal
reservation or any durable admission. Enforce the persisted storage limit (255 Unicode
code points here), reject control characters and noncanonical surrounding whitespace,
and keep absent or blank values on the server-generated/absent fallback path. Do not
invent a UUID-only format when the trace contract does not require one. Prove that
255-character values persist, 256-character or control-bearing values return a
sanitized `400`, and rejected requests create no execution, receipt, transition audit,
or domain mutation. This prevents an invalid trace header from consuming an
idempotency reservation and failing later during audit persistence.

## Avoid Nested Acquisition From The Domain Pool

When a bulk unit already holds an API connection, audit every independent read in
its admission callback. A bounded connection timeout does not prevent structural
starvation if grants or facts need a second connection from that same pool.
Do not fix this solely by increasing the pool or limiting bulk threads while
unrelated API traffic can still occupy the required connections.

Keep proposal capture/storage anchored to the operational API datasource and keep
domain mutation, transition audit and receipt in the Metadata transaction. Use a
separate bounded governance reader pool for current grants and the facts read by
`evaluateUnit`; do not borrow Config/control-plane connections or reuse an ambient
transaction to simulate a fresh authorization read. Preserve autocommit,
READ_COMMITTED, exact namespace/tenant/environment checks and runtime-role checks.

Derive the reader from the effective authoritative API connection configuration,
including SSL, JDBC/driver properties, schema/catalog and initialization settings.
Copying only URL/user/password is insufficient. Do not expose a separate reader
origin or silently route to a replica. Audit datasource wrappers, shared backing
pools and overrides; distinct bean names alone do not prove physical separation.
Complete pool initialization during bootstrap, outside request deadlines; lazy Hikari
initialization can run checkFailFast before the acquisition timeout starts. Reject
pool suspension where it would bypass bounded acquisition. Keep acquisition bounded
by the aggregate deadline. Document total configured
connections per instance (API + governance + Config + control plane) multiplied by
the maximum replicas; separation removes the dependency cycle, not all overload.

On real PostgreSQL, retain API connections while a unit holds the last slot and
prove admission can still read grants/facts and make progress. Separately exhaust
the reader and prove bounded fail-closed behavior without a new domain effect,
audit or receipt. Preserve capture/storage identity, externally committed grant
revocation, replay and transactional rollback proofs. Distinguish controlled pool
occupancy from multiple complete concurrent HTTP executions and from a production
capacity certification. Release retained connections and await pending requests
before clearing shared test hooks.

## Compose Shared Deadlines Across The Host And Config

The Config Starter owns operational-policy semantics and its read-transaction
timeout; the Quickstart owns the aggregate unit deadline and its datasource pool
configuration. For a bounded Config read, treat
`OperationalPolicyService.resolveOperationalPolicy(..., Duration)` as a
transaction-query budget, not an end-to-end deadline. Its timeout is floored to
whole seconds, capped at five seconds, and fails closed below one second; pool
acquisition and work around that transaction may fall outside the timeout.

Pass a fresh remainder from the monotonic unit deadline at each blocking read.
Before Config or grant lookup, subtract the configured maximum pool-acquisition
time plus a small scheduling margin; validate that the effective pool setting
really enforces that cap. Recheck the unit deadline immediately after each
external/starter call and before any next read or mutation. If the reserve or
remainder is insufficient, fail closed without starting that work. Do not reuse a
stale `Duration` captured before a prior blocking call.

Database timeouts establish bounded local waiting, not the outcome of an
uncertain commit. After a write or lost acknowledgement, consult the canonical
receipt/readback path before retrying; never infer rollback or rerun a domain
callback from timeout alone. Prove budget exhaustion, reserved pool acquisition,
post-call revalidation, and fail-closed behavior with the host's real Config/API
PostgreSQL tests.

## Maven And Bootstrap Discipline

`pom.xml` intentionally pins `praxis.core.version` and `praxis.config.version`. A version change is an integration change, not a dependency-only edit:

1. Read the target starter release notes/contracts and identify the affected host surface.
2. Confirm Maven resolution without local dependency overrides or a host fork.
3. Run the focused downstream tests for that surface.
4. Run `mvn -B verify` when changing either Praxis starter version, dependency topology, bootstrap, or host packaging.
5. For an unpublished config-starter change, use the starter's documented local install/Quickstart packaging flow; do not edit the host POM into a permanent local workaround.

Keep API and config datasource properties, Flyway policy, AI provider properties, RAG/vector-store switches, and test isolation explicit. Test profiles may disable external services or use H2, but must preserve the host/starter wiring being proven. Never use an in-memory shortcut as proof that deployed config persistence, origin policy, or streaming works.

## Host Security Is Integration, Not A Starter Override

The quickstart owns CORS, CSRF, cookies, origin restriction, firewall policy, rate limiting, and public/read/write exposure. These policies constrain hosted starter endpoints without redefining their semantics.

- A `permitAll` config route still needs the host's Origin, method, CSRF, tenant/user/environment, and authorization policy where applicable.
- Diagnose a config call failure in this order: canonical route and starter contract, host Origin/CORS policy, cookie/CSRF/authentication, tenant/environment headers, then service behavior.
- Preserve exposed response headers required by browser consumers, including `ETag` and `X-Schema-Hash` when the contract publishes them.
- Treat forwarded headers, URL encoding, public reads, local AI identity, and rate-limit buckets as explicit host trust decisions. Do not broaden them to make a smoke pass.
- Security policy changes require negative-path proof as well as the expected allowed request.

Use `praxis-api-quickstart-security-config` for detailed security changes; this skill routes the issue and requires downstream integration proof.

## Prove The Complete Contract

Use real resource keys, OpenAPI operations, filtered schema URLs, headers, capabilities, actions, surfaces, and option-source contracts. A successful controller response alone is insufficient when a consumer depends on discovery.

For metadata integration, prove the chain:

`@ApiResource`/path -> OpenAPI group -> `/schemas/catalog` -> `/schemas/filtered` -> `x-ui`/schema headers -> actions/surfaces/capabilities/links -> downstream consumer evidence.

When a resource controller delegates route behavior to an application handler, keep Spring MVC
mapping and OpenAPI parameter annotations on the actual mapped controller method. An annotation on
the delegated handler does not describe the HTTP route to Springdoc. Verify the rendered OpenAPI
group for path parameter names, requiredness and formats (including UUIDs), and for each mapped
error response; do not weaken the HTTP/OpenAPI assertion to accommodate missing metadata. When a
confirmation can return `202 Accepted`, document its `Location` response header as the tracking URI
and test the actual header/body pair against the production mapping; describe the execution status
as observed rather than assuming that a lost acknowledgement already changed durable status to a
reconciliation-required state.

For a bulk-operation readiness/composition proof, use the production `ActionDefinitionRegistry`
discovered from the real `@WorkflowAction` controller. A hand-built or mocked action catalog can
prove a small isolated rule, but cannot prove the host's canonical composition. Assert that the
action points to the exact confirmation `CanonicalOperationRef` and that its schema links equal the
resolver's action projection, including resource `idField` and `readOnly=false`; these are not the
generic schema references for the operation. Keep `ActionDefinition.group` (the `@ApiGroup`
catalog/business category) distinct from `CanonicalOperationRef.group` (the exact OpenAPI document
group). The action operation identity must still match exactly, and the seven bulk operation
references must still resolve from one strict group snapshot.

Do not flatten, strip, or replace an unsupported schema composition such as `oneOf` in the host to
make readiness pass. Keep the compiler fail-closed, identify the affected role and operation ID,
then inspect the canonical OpenAPI fragment and its DTO/annotations at the owning source. The
descriptor fingerprint must include the action schema projections and catalog group so changes to
either invalidate a prior structural revision.

When adapting a canonical bulk request into a host/provider DTO, preserve nullable optional members
exactly as the public contract defines them. In particular, do not collapse omitted `excludedIds`
into an empty list unless the contract specifies that equivalence; handle `null` before iterating.
Prove the real HTTP request with optional members omitted as well as explicitly present when both
forms are supported.

When a real `@WorkflowAction` must remain registered for structural composition but is
operationally unavailable until a durable bulk lifecycle is ready, project that state through
the existing `ActionAvailabilityRule` path. Scope the rule to the exact resource key and
operation identity; use the server-owned namespace and current `BulkOperationLifecycle` readiness
check. Fail closed when the opt-in lifecycle/binding is absent or readiness is uncomposed,
suspended, stale, or otherwise unavailable. Keep the action registered, apply the same existing
availability projection to `/schemas/actions` and resource capabilities, and recheck readiness before
admitting a new proposal or a fresh domain mutation. Discovery availability is a hint, never
authorization or a reservation; do not cache it or create a parallel capability/flag. Preserve
receipt-before-gate replay of already-confirmed effects and cooperative cancellation of an existing
execution during suspension. Prove the real discovery and capability responses before/after publish,
suspend and external cache refresh, plus the opt-in-off case.

For hosted option-source integration, prove the chain:

`canonical descriptor/provider -> OpenAPI generic route -> /schemas/filtered for option-source endpoints -> x-ui.optionSource metadata -> authenticated filter/by-ids HTTP execution -> stable OptionDTO/entity metadata -> no provider class or execution context leaked in public docs`.

The host may own a provider implementation or pilot data, but it must not translate dependencies, reload policy, invalid-selection policy, or entity lookup semantics locally for consumers. Those must come from metadata-starter descriptors and be proven through HTTP. If the backend publishes `dependencyFilterMap`, the quickstart proof must send the mapped filter payload accepted by the endpoint; Angular or Ergon-facing consumers should not hand-code that translation per screen.

For config/AI integration, prove the chain:

`host policy + scope headers + starter persistence -> canonical config/authoring endpoint -> ETag or stream semantics -> safe response/diagnostics -> actual consumer or focused host smoke`.

For agentic authoring/SSE, the quickstart proves HTTP reachability, identity/origin/security, persistence, event transport, cancellation, and cleanup. It does not create a second intent router, prompt parser, tool registry, compiler, or patch validator. Primary intent remains semantic and LLM/tool-grounded; keyword or route-text inference may not become a host fallback.

For a cross-platform authoring gate, require stronger operational evidence than a successful browser assertion:

- provision a deterministic PostgreSQL database owned by the lane, validate its semantic golden fixture, and drop it even on failure;
- adapt the authenticated host principal and authorities into the starter-owned authorization SPI; keep domain policy out of the starter and test both the normal principal and a reduced-capability principal;
- wait until the governed Domain Catalog RAG status is reconciled with a non-zero expected/published count before the first turn, then prove in a redacted provider transcript that every pre-intent call received that context;
- correlate browser traffic with the expected principal and capability surface. A reduced aggregate-only principal must not cause individual/table reads or materialize table-derived detail/KPIs;
- retain visual, responsive, accessibility, network, persistence/reload, and redaction evidence, and clean up owned processes, temporary databases, and temporary local artifacts without touching user runtimes.

For provider operations, distinguish a deterministic local gate, a no-inference
connection/model probe, and a paid external-provider journey. Preserve bounded
call count, usage origin, sanitized provider metadata, cancellation/fallback,
and dedicated AI rate-limit evidence; do not treat a successful LLM response as
the only connectivity or security proof.

## Prove Persisted Department Coverage Before Public Readers

For the host-owned operational grant, reuse its immutable identity and revision.
Do not turn a global authority, demo scope, empty coverage or a JWT role into
implicit department access. Inspect the operational migrations, grant repository,
focused PostgreSQL proof and `docs/OPERATIONAL-GRANTS-CONTEXT.md` together.

Before implementing an administrative writer, record the lock order, CAS revision,
revocation behavior and effective privileges. Lock the grant before child DML;
lock referenced departments in stable order before replacing coverage. A child
trigger that updates the parent may invert the intended order. Read revision and
coverage in one SQL statement or verified snapshot, not two READ COMMITTED reads.

Prove no default grants, constrained references, stale-writer rejection, atomic
revision/coverage/audit rollback and revocation without silent restoration. Runtime
must not write authorization state or execute administrative functions; table
privilege checks alone do not cover SECURITY DEFINER. Verify fixed search_path,
qualified objects and effective EXECUTE privileges, including inherited grants.
Record the authenticated database actor; in SECURITY DEFINER, current_user is the
function owner, while session_user identifies the session login. An external
approval reference records provenance, not enforcement of human approval.

PostgreSQL fixtures must seed or change coverage through the migration-owned writer
function rather than direct child-table DML. Follow its compare-and-swap `row_version`
through every change: a changed replacement advances the expected version for the next
fixture mutation, while an identical replacement is an idempotent no-op. Otherwise a stale
fixture can fail before the test reaches the intended revocation or reduction assertion.

Keep these guarantees separate: persisted coverage; temporal department resolution
for the historical employee/competence; and authorization of the complete result
set in the Metadata reader snapshot. Grant revision does not version assignments.
Do not claim granular enforcement, safe public pages or READY from persistence
alone. Update fixtures through the official migration lane and preserve the
independent current-grant connection used by mutation admission.

## Prove Temporal Read Authorization On One Snapshot

For payroll result access, resolve department assignment from protected historical
employee/competence dependencies, not the current event or employee department.
Require exactly one assignment in the half-open interval at competence day one and
explicit current coverage for every target. Missing, overlapping or partial coverage
must not authorize a filtered subset. Keep unavailable distinct internally from deny.

Use the same physically attested REPEATABLE READ READ ONLY connection for grant,
coverage and scalar assignments. JDBC flags alone are not proof of server settings.
Do not acquire an independent grant connection, change isolation, or commit/rollback/
close the caller's transaction. Attestation and queries share one monotonic budget;
preserve smaller server limits and do not reserve pool acquisition time again.

Bind the read fingerprint to the authenticated requester, binding, current grant and
coverage, ordered complete dependencies and assignment identity/department/interval.
Grant revision does not version assignment changes. Do not replace evaluation's
global authorization fingerprint with this whole-set digest: unit execution recaptures
one target and would no longer compare with the original multi-target evaluation.

Prove the profile's full target limit, missing/multiple/partial assignments, two
requesters, reduction/revocation, concurrent grant and assignment changes, bad physical
transaction settings, bounded failure and sanitized outputs on PostgreSQL. A coherent
host snapshot is not yet proof of sharing the Metadata reader snapshot or wiring a
public API; keep that integration and mutation admission as explicit later gates.

## Adherence Inventory

Before adding a property, endpoint, DTO, dependency override, test fixture, controller adapter, security exception, or example, ask what the platform already publishes and classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` permits a new public contract. Name missing behavior, canonical owner, affected consumers, derived artifacts, operational/security impact, and minimum proof. A test failure caused by fixture/bootstrap drift is not evidence that a new starter API is needed.

## Focused Validation Matrix

Run the narrowest reliable gate first:

| Changed surface | Minimum local proof |
| --- | --- |
| metadata/schema/discovery downstream contract | `mvn "-Dtest=OpenApiGroupResolutionIsolatedIntegrationTest,QuickstartMetadataMigrationIntegrationTest,EventosFolhaPilotIntegrationTest" test` |
| hosted option-source endpoint contract | `mvn "-Dtest=ResourceEntityLookupGovernanceIntegrationTest,ProcurementExternalOptionSourceProviderIntegrationTest,VwStatsSmokeHttpTest" test` plus the affected pilot test |
| config patch/schema or host config security | `mvn "-Dtest=AiPatchSchemaResolutionIsolatedIntegrationTest,SecurityConfigAiPatchPolicyTest" test` |
| CORS/CSRF/read-open/origin/rate-limit | `mvn "-Dtest=SecurityConfigActuatorPolicyTest,SecurityConfigAiPatchPolicyTest,SecurityConfigReadOpenStatsPolicyTest,SecurityConfigSpaCsrfPolicyTest,SecurityConfigCorsTest,ConfigOriginRestrictionFilterTest,PublicApiRateLimitFilterTest" test` |
| starter Cockpit hosting/build identity | `mvn "-Dtest=PraxisCockpitStarterConsumptionIntegrationTest,ActuatorInfoBuildContractIntegrationTest" test` |
| agentic authoring/stream host integration | `mvn "-Dtest=AgenticAuthoringStreamIsolatedIntegrationTest,AiPatchSchemaResolutionIsolatedIntegrationTest" test`; use config-starter's official Quickstart HTTP/SSE smoke for release proof |
| principal-aware governed authoring adapter | focused adapter/security/golden-fixture tests plus the disposable PostgreSQL browser gate for normal and reduced-capability principals |
| targeted pilot resource | its focused pilot/lookup/stats/export test with `praxis-api-quickstart-domain-pilots` |
| starter version, Maven/bootstrap, broad cross-cutting host change | Maven resolution plus `mvn -B verify` |

Use Cockpit, HTTP corpus, and published-host checks only after local proof is green. They are release/downstream evidence, not the ordinary development loop. State exactly what did not run and why.

## Derived Evidence

When public behavior changes, review `README.md`, properties/deployment guidance, Cockpit docs/scripts, quickstart HTTP examples, `praxisui-http-examples`, starter docs/specs, and Angular/landing documentation that mirrors the contract. A host-only internal change may require none; state that conclusion explicitly.

## No Keyword Routing

Do not choose resource, schema, action, capability, security policy, domain decision, AI route, or validation path using labels, route fragments, aliases, regexes, or fuzzy matching as the primary decision. Use canonical resource keys, OpenAPI/schema references, starter contracts, governed catalog/context, capabilities, diagnostics, and declared tools. Textual matching may only rank already-scoped candidates.

## Companion Skills

- `praxis-config-ai-provider-operations`: provider status, routing, telemetry, pricing, paid gates, and cost controls.

- Use `praxis-api-quickstart-security-config` for host exposure, CORS/CSRF/origin/firewall/rate-limit policy.
- Use `praxis-api-quickstart-domain-pilots` for concrete resource paths, domains, DTOs, lookups, actions, and migration proof.
- Use `praxis-api-quickstart-cockpit-http-validation` for Cockpit scripts, HTTP examples, published evidence, and build diagnosis.
- Use `praxis-metadata-resource-baseline`, `praxis-metadata-schema-contracts`, `praxis-metadata-discovery-capabilities`, and `praxis-metadata-domain-option-sources` when the root cause is metadata-owned.
- Use `praxis-config-agentic-authoring-streaming`, `praxis-config-domain-decisions`, `praxis-config-runtime-persistence`, and `praxis-config-api-metadata-grounding` when the root cause is config-owned.
- Use `praxis-http-examples-contract-surfaces` and `praxis-http-examples-llm-smoke` for the external executable corpus.


## Compose An Authorized Bulk Execution Summary (G3c-a)

Before adding any host surface, inspect Metadata's `BulkAuthorizedExecutionReader`,
`BulkExecutionSummary`, and G3c-a in `docs/spec/BULK-H1B-READ-MODEL.md`. The public SDK
reader is a server-side composition, not an HTTP endpoint; its protected lookup helpers
remain package-private. Bind a trusted resource key, confirmation operation and host
authorization provider; accept only the authenticated subject and execution UUID from
the request. Use one Metadata-owned `REPEATABLE READ READ ONLY`
physical snapshot for global authorization, execution/proposal lookup, full current
authorization of every historical target, the certified RS3 summary and projection.
Do not add another reader transaction, reconstruct proposal metadata or execution
results from current descriptors/domain rows, or reduce authorization to the summary
fields. The host authorization provider must consult its current authoritative
grant/coverage source within that same snapshot.

For a retained execution, project metadata operation/mode/atomicity only from the
durable validated intent; project status, totals and persisted timestamps only from
the certified RS3 summary. Preserve the confirmed prefix and pending-ACK boundary.
Use the fixed sanitized STOPPED diagnostic; never expose its internal reason, protected
facts, target identities, arbitrary metadata or stored causes. Retention after execution
expiry permits reads only while current authorization and retained evidence still allow
them.

If there is no live execution, the reader uses the scoped historical tombstone digest:
only the matching historical creator after the current global grant may observe its
internal `GONE`; delegate, other scope and unknown ID must remain indistinguishable
`NOT_FOUND_OR_DENIED`. Keep global denial/unavailability before protected lookup;
keep proposal/lookup/decode/correlation failure before full target authorization
non-enumerating; map summary corruption after authorization and expired read budget to
unavailable. Scope identities must be strict nonblank UTF-8 with NUL and
malformed-surrogate input rejected before SQL. After decoding the protected proposal,
compare the locator's input and evaluation fingerprints with the decoded proposal's
snapshot and evaluation fingerprints before constructing the target list or invoking
authorization; mismatch stays non-enumerating.

Require PostgreSQL proof and independent review for the composition, including
same-snapshot authorization and summary,
creator-versus-delegate tombstone behavior, unknown/cross-scope non-enumeration,
pre-authorization storage failure, post-authorization summary corruption, strict UTF-8,
sanitized STOPPED projection and deadline enforcement after transaction completion.
Integration, publication and adoption remain separate gates. The DTO/route/security/OpenAPI
contract and redaction review are also separate host gates. This
cut adds no HTTP route, RS4 item results/cursor, worker, capability or `READY`; leave
those decisions closed until separately specified and proved.

## Adopt Authorized Execution Result Pages (G3c-b)

For a future Quickstart consumer, follow the G3c-b section in
`praxis-java-command-concurrency-authoring` and inspect the Metadata facade, G3c-a
protected execution/proposal correlation helpers, and connection-taking RS4 seam. Do
not call the G3c-a summary reader as a helper that opens a separate transaction. The
facade accepts authenticated subject, execution UUID, size and opaque continuation only.
The outer Quickstart G3b-O issuance reservation happens first. Inside the core reader,
decode the `EXECUTION_RESULTS` purpose before protected SQL or authorization; global
authorization precedes protected lookup. On live pages,
correlate execution/proposal fingerprints and reauthorize the full historical target
set from the current authoritative source in the same physical RR/RO connection that
certifies the RS4 page. Do not nest a second reader transaction or perform RS3's full
scan for a page.

Preserve the cursor's execution/scope/requester fingerprint, fixed watermark, size,
projector revision and original expiry; initial watermark zero has no next cursor.
Project only certified wire identity and status with fixed generic diagnostics by
status, never raw reason or protected details. Reuse G3b-O's shared durable issuance
budget and the same `BulkReadCursorProperties.Provisioned` key-material snapshot;
AEAD purpose does not create a new quota. Apply the G3c-b tombstone exception exactly:
creator plus current global grant may get payload-free GONE, and a delegated token copied
to the creator may produce that same minimal result. Do not claim live-page anti-copy
guarantees for purged executions; no target fingerprint remains to validate.

After transaction completion, verify the continuation is still sendable: if the initial
page's newly issued token expired before publication, return `UNAVAILABLE`; an expired
continuation returns `PRECONDITION_FAILED`. Preserve original expiry and never renew TTL.

Require PostgreSQL proof and independent review before adoption. This facade adds no
HTTP route or `READY`; publication, host adoption and any future HTTP status mapping
remain separate gates.

## Prove The Authorized Bulk Read Consumer

Follow `praxis-java-command-concurrency-authoring` for the G3b proposal-results
reader, cursor, item projection and status matrix. The concrete route is
`GET /api/human-resources/eventos-folha/bulk/proposals/{proposalId}/results` with
`size` and optional `after`; its resource key and exact GET operation must agree
between the `@ApiResource` controller, `CanonicalOperationResolver` and the named
OpenAPI document. Prove bodyless continuation and the concrete Integer/int32 item
identity in OpenAPI. The host endpoint is a read path: it does not declare `READY`,
execute, cancel, or expose tombstones.

Treat a Metadata candidate `SNAPSHOT` as candidate-only. Use its distinct coordinate,
an isolated Maven repository and explicit `praxis.core.version` override for local
consumer proof; record the exact source and resolved JAR. Do not overwrite a published
coordinate. For later adoption, require the released artifact to resolve from the
intended repository, pin that exact version, use an isolated cache and remove the
candidate override. Candidate source/tests and an HTTP proof against a candidate do
not establish published adoption. Keep Config's pin independent.

Use the real controller, authenticated non-anonymous principal, configured cursor
keys and PostgreSQL-backed authorizer. Each first or continuation page must reauthorize
the whole immutable target set in the same snapshot as projection. Preserve the
historical creator while binding continuation to the current requester and effective
authorization fingerprint. The cursor is AEAD-protected; require the same size on every
page, retain the original issue/expiry instants without TTL renewal, and recheck expiry
after transaction completion before returning the page. Configure positive TTL up to
15 minutes, no default/ephemeral key, and no token/key logging. For rotation, provision
the new key across every replica before changing the active key and retain old keys
through the maximum issued-token lifetime. A test constructing a new reader with a
rotated key set proves reader reconstruction in the same process; do not claim that an
OS process restart was tested. The Quickstart host implementation protects issuance
around the stateless codec: reserve a
durable attempt in one ledger shared by that database authority and fleet before every
reader call. This is host operational policy, not a universal Metadata consumer
contract. Commit in its own `REQUIRES_NEW` transaction before the reader's single RR/RO
authorization/projection snapshot. Key the lifetime quota by SHA-256 of the decoded
32-byte AES material, not `kid`, and cap it at 2^31 reservations per material. Keep
reader configuration and budget digest derived from the same immutable
`BulkReadCursorProperties.Provisioned` key-material snapshot; never derive them
independently from mutable properties.
the material and ledger exclusive to this host database authority and fleet; do not
reuse them across services, environments, or independent databases. Authorization,
protected evaluation and page projection still share one immutable reader snapshot. The
reservation precedes cursor decoding/core protected SQL and is never refunded, including
outer rollback, uncertain commit, invalid or denied reads, and final pages. Missing,
exhausted, expired, or unavailable budget returns generic 503
before the reader. The absolute `issuance_not_after` gates reservation time, not later
encryption; the core read deadline begins inside the reader, so include host pool
acquisition and reservation commit separately in end-to-end timing. On database restore,
clone, or known/uncertain loss of committed ledger state, provision fresh key material
before reopening issuance; never reset/reuse the old material's quota. Emit only a
bounded metric outcome (`reserved`, `denied`, `unavailable`) with no key, digest, user,
proposal, token, claim, nonce or fingerprint tags. These controls exist in the candidate
implementation, but candidate tests do not prove real-fleet provisioning, monitoring,
alerts or runbook exercise; neither publication nor adoption is implied.

The host adapter must verify the bound `ConnectionHolder` before obtaining its
connection and join the exact physical connection used by the operational transaction;
matching JDBC URLs or independent RR/RO transactions do not prove one snapshot. Preserve
the owner's transaction, reuse its timeout, retain smaller SQL timeouts and pass only
the remaining monotonic budget to host work. Include acquisition/setup, CPU and final
publication in the budget and discard output after the deadline; this is a publication
deadline, not instantaneous cancellation. Persist the allowlisted preview atomically
with evaluation, keep provider/evaluator/projector revisions separate, and let execution
expiry leave otherwise-authorized retained results readable.

Verify the response contains only Integer `id`, `EXECUTABLE`/`BLOCKED` decision and
public diagnostics. Do not expose ordinals, totals, identities beyond the authorized
page, facts, plan, versions, fingerprints, or protected authorization context. The
proposal's `redactedIntent` remains a distinct RS1 concern. Require `Cache-Control:
no-store` and no domain mutation.

Prove the deliberate public matrix and compare negative responses for non-enumeration:
after a successful issuance reservation, an invalid cursor is 400 before protected
SQL; an unavailable/exhausted/expired budget returns 503 before cursor decoding or
reader entry. Then prove global denial 403; global-authorizer failure 503 before
lookup; pre-full-authorization proposal-specific storage failure, absence, incomplete
coverage, copied requester/scope/proposal and changed fingerprint as indistinguishable
404; authorized live proposal with expired or incompatible cursor as 412; unavailable
legacy preview on the first page as 409; and corruption after authorization or bounded
operational/deadline failure as 503. No negative response may contain page data, totals,
cursor, or sensitive identifying headers.

Use the real PostgreSQL/HTTP fixture in `EventosFolhaApprovalEvaluationHttpTest` for
delegated access, paging, requester-copied cursor, revoked/reduced grants, privacy and
OpenAPI. Keep `SecurityConfigBulkProposalResultsPolicyTest` and
`BulkReadCursorPropertiesTest` focused on matcher and key/TTL configuration behavior;
they do not replace the end-to-end proof. The host's
`durableCursorReservationIsCommittedBeforeReadAndNeverRefunded` covers route ordering,
including terminal-page consumption and fail-closed behavior when reservation authority
is unavailable; `BulkCursorIssuanceBudgetPostgresTest` covers cross-instance durable
quota, rollback/uncertain commit, expiry, bounded telemetry and runtime privileges.
Neither test proves provisioning, alerts or recovery procedures in a deployed fleet.
Metadata's
`BulkAuthorizedProposalResultsContinuationPostgresTest` proves same-snapshot bounded
continuation, scope reauthorization, expiry and same-process reader reconstruction.
Re-run the exact host tests against the chosen candidate or released artifact and
record which it was. Keep evidence in the execution record: distinguish Metadata core
proof from host HTTP, controller/security/OpenAPI proof, identify the exact candidate or
released artifact, and do not claim statuses or scenarios unless that layer's test
demonstrates them. A candidate can pass technical review without being published or
adopted. Do not infer execution, tombstone, `READY`, Angular, or RS1 coverage from these
read tests.

## Prove Host Execution Summary and Result HTTP Reads (G3c-HTTP)

Use the adopted Metadata G3c-a/b readers behind the existing resource's two planned
bodyless GETs: `/api/human-resources/eventos-folha/bulk/executions/{executionId}`
(`human-resources.eventos-folha.bulk-execution-read`) and its `/results` child
(`human-resources.eventos-folha.bulk-execution-results`). Before treating these as
adopted behavior, inspect the actual pinned artifact, host controller, `ApiPaths`,
security matchers and named OpenAPI document; a candidate controller or guidance
does not establish host HTTP acceptance or publication.

Prove the closed status contract: 200 live summary/results; 400 invalid cursor/size; 403 global
denial; 404 indistinguishable absence, cross-scope or post-lookup denial; 410 only for
the historical creator with a current global grant and no execution/item payload;
412 stale continuation after full authorization; 503 generic unavailability. There
is no preview 409. Both endpoints return `Cache-Control: no-store` and canonical
`RestApiResponse` envelopes. The summary has no cursor and reserves no budget. Results
reserve once in the shared G3b-O key-material ledger before core access, even when the
page has no continuation; never refund, renew the cursor TTL, or create a separate
AEAD-purpose quota. After the outer reservation, the core decodes the
`EXECUTION_RESULTS` purpose before protected SQL or authorization, and checks global
authorization before protected lookup. Check Integer wire identity as `int32`, bodyless query parameters,
the exact operation IDs and `CanonicalOperationResolver` resource/method binding.

Exercise the routes with a real authenticated principal and PostgreSQL-backed reader.
Explicit GET/HEAD authorization must beat `readOpen`; anonymous requests must remain
denied. Prove live full-set reauthorization and requester-bound continuation, invalid
token behavior, expiry/size preconditions, current revocation, protected negatives,
reservation committed before the reader and tombstone purge/copy boundaries. A tombstone
returns only creator-authorized payload-free 410; delegates and unknown/cross-scope IDs
receive the same 404. Since purge removes target evidence, do not promise full cursor
anti-copy protection in that tombstone exception. Keep malformed path/query handling
non-enumerating and assert no cacheable response or protected diagnostics.

Only after the host HTTP/OpenAPI/PostgreSQL proof is accepted, document the routes in
Quickstart's README and add manual reference-only corpus requests with the verified
controller as source. Mark each manifest entry `referenceOnly: true`, `public: false`,
`authRequired: true`, and `llmOperational: false`; do not add credentials, real
execution IDs, fabricated response payloads, or expose these examples in
`LLM_SURFACE.md`. Run the corpus's official manifest validator after edits; it checks
file references and generated LLM surface parity. Do not claim `READY`,
published host adoption, or Angular readiness from route-level success; the remaining
bulk lifecycle and later gates are separate.
