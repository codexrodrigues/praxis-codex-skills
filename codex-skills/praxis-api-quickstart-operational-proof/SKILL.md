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

Until the production handlers and their complete lifecycle are proved against the published
starter artifacts, keep every host README, security/migration guide, and runtime smoke explicit
that the legacy bulk action is absent from discovery, capabilities, and OpenAPI. A Config
`approval_policy` materialization alone is not host enforcement. Smoke scripts may verify that
materialization and report host execution as pending, but must not call the retired action or
claim a runtime approval-policy gate passed. The default/automatic mode should warn honestly;
an explicitly required host-enforcement gate should fail with the S4c prerequisite. Include a
negative action-discovery assertion in the host proof.

The focused proof must exercise the real Config and API PostgreSQL stores,
including grants, a two-item committed prefix, proposal expiry after reservation,
policy/grant changes between items, a target race, isolated unit rollback,
commit-acknowledgement loss and receipt readback, Config timeout, replay under
current authorization, redacted responses, and recovery without mutation. A
candidate probe is not a production endpoint, published capability, or proof
that the public workflow is ready. Use
`praxis-java-command-concurrency-authoring` and the Metadata Starter bulk
execution contract when reviewing these guarantees.

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


## Prove The Authorized Bulk Read Consumer

Follow `praxis-java-command-concurrency-authoring` for the canonical G3a reader,
protected Target view, shared snapshot, budget, projection and deferred HTTP gates.
The operational proof must call `BulkAuthorizedProposalResultsReader` from the real
host package with `EventosFolhaBulkReadAuthorizationProvider`, not only call G2
inside a test-owned transaction or substitute a recording provider.

First verify whether the required Metadata artifact is published; rc.136 lacks this
API. While it remains unpublished, use a distinct candidate coordinate, an isolated
Maven cache and an explicit `praxis.core.version` override, recording exact artifact
and source evidence. Once it is published, pin the exact released
`praxis.core.version`, resolve it in an isolated cache and remove the candidate
override. Keep Config's separate version intact. Do not integrate a host change that
depends on overwritten release bytes or an unavailable artifact.

Exercise explicit host wiring and the real proposal writer's atomic allowlisted
preview. Keep provider/evaluator/projector revisions distinct. Prove delegated
access, denial caused by an off-page target, ambient transaction restoration and
old/new observations while both department assignment and grant change. Preserve
existing fixture identities: additional employees/departments belong to the test
that needs them. Reuse canonical PostgreSQL expiry/deadline proofs where still valid.
No HTTP result route, cursor or READY follows from this Java consumer alone.
