---
name: praxis-api-quickstart-operational-proof
description: "Use when Codex must implement, audit, or diagnose Praxis API Quickstart as the real Spring Boot reference host: Maven starter composition and versions, bootstrap/properties/datasources, security and browser policy, metadata/config/runtime HTTP integration, schemas and discovery, agentic authoring/SSE host proof, deployment identity, or ownership routing between quickstart, metadata starter, config starter, and Angular consumers."
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

## Prove A Packaged Administrative Entry

For capacity-local INSPECT/FENCE, reuse Metadata's public administrative Main and
`BULK-CAPACITY-LOCAL-ADMINISTRATION.md`; the host only selects that entry through
its existing PropertiesLauncher. Inspect the exact nested SDK artifact and class
origin. For unpublished code, use a distinct private GAV/cache and the actual host
property `praxis.core.version`; never install candidate bytes under a public
coordinate or call an override proof public adoption.

Run `BulkCapacityLocalAdministrationPackagedJarPostgresProof` explicitly AFTER
packaging with an absolute `praxis.bulk.admin.packagedJar`, a fresh absolute
`praxis.bulk.proof.directory` and fail-if-no-specified-tests. The Proof name keeps
it out of the default pre-package lane; missing inputs must fail, not skip or
substitute classes. Its disposable owner fixture must migrate owner-only, grant
exact host-owned runtime ACLs, then attest configured roles through the public
migrator. That fixture seed is not production enrollment or a restore recipe.

Preserve stdout as the closed SDK JSON, with no warning filtering. If spring-jcl
reports duplicate commons-logging in the packaged classpath, trace every actual
Maven edge (including omitted duplicate branches), exclude only the redundant
implementation on those consumer edges and retain spring-jcl/SLF4J, provider and
HTTP-client versions. Freeze the new POM/tree and repackage; verify the final
nested JAR inventory and exact SDK hash before repeating only affected proofs.
Check binary logging compatibility or an existing safe offline consumer proof;
mocked provider tests alone do not prove the actual bridge. Do not make network
AI calls or use credentials merely to test logging composition.

Require separate JVMs, unique SDK Main origin, safe current binding/role/ACL
negatives, confirmed FENCE/replay and artifact/PID/exit/cleanup evidence. Preserve
failed raw privately and always remove credential input; write success evidence
after owned PostgreSQL closes. Distinguish real JAR launcher proof from Docker
wrapper COPY/execution: no installed container command is certified by launcher
success. SDK SCRAM/D0-outage tests retain their own scope; a trusted local host
fixture does not inherit those guarantees. Keep independent review, canonical
guidance integration and selective local sync separate from publication/adoption.

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
A separate EXPLICIT preflight may read target facts in one consistent read-only
database snapshot; it does not replace the capture authorization. The protected
capture itself uses one writable repeatable-read transaction, acquiring durable
CONTROL/quota before current grant locks and target selection. A target that is
absent and one outside current scope must
produce the same redacted response, and neither may leave a proposal, evaluation,
manifest, preview or quota allocation. Do not rely on a later proposal/result reader to
make an already-persisted capture safe. A comparison-only revalidation of a creator-owned
proposal may return only whether evidence still matches and must not persist new evidence,
consume quota or authorize execution. If it refreshes/persists a proposal or allocates
quota, it is a new capture and must perform the same full-set authorization first;
execution still rechecks current governance under each unit's lock.

When a host first migrates protected storage without runtime roles and then
attests configured roles, a completed V16 atomic bootstrap will not grant
later runtime permissions automatically. Inspect Metadata
`BulkExecutionMigrator.ATOMIC_RUNTIME_TABLES`,
`provisionAtomicRuntimeGrants`, and `validateAtomicBootstrap`; provision
exact `SELECT, INSERT` on the four atomic evidence relations and `EXECUTE`
on `atomic_evidence_complete(uuid,integer)` for the runtime role before
the configured-role migration. The Quickstart
`ReferenceConsumerHttpFixture.initializeOperational` and
`ReferenceReadAuthorizationPostgresTest.provisionMetadataRoles` show this
host-owned fixture boundary. Do not loosen the migrator validator or add
`PUBLIC`, `UPDATE`, `DELETE`, or owner membership. Require separate
PostgreSQL 16 HTTP evidence for the B6 consumer; an ACL bootstrap repair
alone does not prove its bulk behavior.

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

To prove cancellation while an incomplete execution has a committed unit awaiting ACK, keep
the real transaction manager, datasource and existing listeners. Append only a test-scoped Spring
transaction listener: `beforeCommit` identifies the intended writable unit transaction on its
Spring-bound connection. In a fresh, bounded disposable PostgreSQL fixture, `xmin`/XID may bind
the observed attempt to that transaction; this is neither an SDK contract nor a production
identification technique. `afterCommit` with no commit error holds the return before ACK, without
changing the commit. Independently verify the first domain effect and receipt,
`UNIT_COMMITTED_PENDING_ACK`, cursor zero and pending suffix.

Call the real HTTP cancellation route while confirmation remains held: it records intent but
does not yet release the execution's quota allocation. After the stored unit deadline, release
the gate and require receipt-first ACK, `STOPPED`/`CANCELLED_BY_USER`, cursor one and the suffix
`NOT_PROCESSED` without another mutation. On the allocation bound to that execution,
terminalization changes only `state`, `released_at` and `release_reason` to `RELEASED`/a
timestamp/`TERMINAL_RECONCILED`, preserving its other binding fields and unrelated allocations;
replay leaves the full recorded durable state unchanged, including execution, domain, receipts
and allocation.
Keep the listener and gate test-only. This does not prove a two-JVM crash, uncertain JDBC commit,
`ATOMIC`, or B6/B7 completion.

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

Prove first confirmation of an unused retained proposal separately from terminal
receipt-first replay. In the concrete RuleLab capture, `expiresAt` is `evaluatedAt`
plus two minutes, not `createdAt` plus two minutes. Compare the public expiry, SQL
`praxis_bulk_proposal.expires_at`, and protected evaluation root `expiresAt` as
instants, including the exact interval from protected `evaluatedAt`. Keep operation
control, current grant and the governed ALLOW policy healthy. Capture complete bulk,
domain, facts, grant, protected proposal, Config, approval-audit and outbox baselines
before waiting. Require the initial PostgreSQL `clock_timestamp()` observation to
be strictly before expiry, then poll that clock read-only until it is at least
the expiry, with a bounded monotonic harness deadline and a total test timeout that
includes setup. Then make the first confirmation with the original creator and an
unused idempotency key; do not issue an expired proposal GET first. Require a JSON `failure` envelope with exactly one error
(`status=410`, `code=BULK_PROPOSAL_GONE`), absent/null `data`, `Cache-Control: no-store`
and no Location/ETag. Exclude UUIDs, proposal/execution/target identities, counts,
scope, fingerprints, schema, cursor and protected facts from that response. Require
no new execution reservation/allocation/admission/rejection/receipt/children or
approval effects, and unchanged baselines after both the wait and confirmation.
Preserve the legitimate pending-proposal allocation; zero execution allocation
does not mean the proposal-allocation table is empty.
Keep the cursor budget separate; this sequence does not issue results reads and must
not consume cursor reservations. Do not alter persisted expiry or protected digests,
substitute a fake Clock, shorten TTL or inflate execution deadlines for the proof.
Two minutes is RuleLab-specific: this case does not certify a generic profile TTL,
purge races, an already used proposal, an execution crossing TTL, or replay after
authorization changes. Record a served PostgreSQL focal before claiming this gate.

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

## Prove Real Config Outage Between Confirmed Units

For T06, use `ReferenceConsumerConfigOutageHttpPostgresTest` with the published
Metadata/Config artifacts and an isolated empty Maven cache. The existing
`config-outage` workflow selector executes only this HTTP focal and attests the
exact candidate, source, public JAR hashes and bounded sanitized evidence.

Publish a real ALLOW policy, then independently observe physical domain+receipt
commit of unit zero at the existing afterCommit barrier. It can still be
UNIT_COMMITTED_PENDING_ACK there: do not fabricate an ACK-certified prefix or
public admission before ACK. Stop ONLY Config; probe its ORIGINAL URL with correct
credentials for native SQLState class08 and independently prove operational DB
healthy. This focal composes connectTimeout/socketTimeout of1s on the Config
JDBC URL for both probe and runtime, without raising the native5s unit ceiling;
it does not certify default timeouts, pool behavior or general performance.
Release the barrier without cancel, runtime kill, transport fault or ACK
failure. The historical `releaseAfterCancel` name only opens the barrier; it does
not authorize calling cancel. Observe sufficient remaining execution deadline
before release, greater than the unchanged native unit ceiling; do not inflate
budgets or wait for expiry to make the scenario pass.

Require STOPPED/COMMON_GOVERNANCE_UNAVAILABLE, certified next ordinal1, unchanged
first physical receipt/domain and zero suffix receipt/admission/mutation. Authorized
reads and replay must leave protected state unchanged while Config stays offline.
Inspect source, XML, public bytes, manifest causal fields, images and owned cleanup
independently; the manifest is exported only after assertions and resource closure.
An abort, exception, pool saturation, policy denial or lost ACK is not a T06 PASS.
This focal does not certify uncertain commit, recovery, HA, worker, B6/B7 completion
or Angular readiness. Keep protected snapshots/settings/credentials private and
close only owned Spring, executor and containers before success export.

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

Pair the negative timeout proof with a positive read near the transaction's
one-second boundary on the resolved consumer runtime. Use a duration accepted by
the canonical read API whose effective transaction allowance is about one second;
hold contention from an independent PostgreSQL connection for less than the
remaining allowance and require the valid read to continue. Then hold contention
beyond the original deadline and require denial without domain, audit or receipt
effects. Record the absolute deadline, fresh remaining duration and actual wait;
recheck after the read and before mutation. A negative-only test can hide premature
expiration caused by framework rounding. Keep databases/connections isolated and
release waits on failure; preserve the existing budgets and fail-closed gates.

## Maven And Bootstrap Discipline

`pom.xml` intentionally pins `praxis.core.version` and `praxis.config.version`. A version change is an integration change, not a dependency-only edit:

1. Read the target starter release notes/contracts and identify the affected host surface.
2. Confirm Maven resolution without local dependency overrides or a host fork.
3. Run the focused downstream tests for that surface.
4. Run `mvn -B verify` when changing either Praxis starter version, dependency topology, bootstrap, or host packaging.
5. For an unpublished config-starter change, use the starter's documented local install/Quickstart packaging flow; do not edit the host POM into a permanent local workaround.

For starter adoption or transaction-budget failures, compare the BOM, Spring Boot,
Spring Framework and Hibernate versions effectively resolved by the canonical
owner's tests, downstream tests and packaged host. Inspect dependency trees and
the effective POM; declared starter pins alone do not show host dependency
mediation. Correlate an unavailable result with the actual remaining budget and
the resolved framework's timeout behavior before attributing it to exhaustion.
Prove any runtime difference with the positive/negative PostgreSQL pair above and
the affected HTTP flow. Correct compatibility in the owning baseline; do not add
a host Hibernate override, increase budgets or weaken denial for convenience.
Keep candidate proof separate from published-artifact adoption.

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

### Prove Bulk Restart Across OS Processes

For the case where the client received the response, pair the existing
`ReferenceConsumerHttpPostgresTest` with `ReferenceConsumerRestartHttpPostgresTest` when the latter
is available. Use the published Metadata `BulkOperationLifecycle.reconcilePublished` and durable
execution readers; a test-only helper route is not a production API. Prove distinct OS process IDs:
finish `COMPLETED` and receive the HTTP response, forcibly stop the first test process, verify it
is dead, then start the second. Keep the same two databases, namespace/deployment, identity,
proposal/idempotency key, cursor material and origin. Perform administrative migration, grants and
seed only once; the second process must not run DDL or reseed.

Require a cold denial before explicit reconciliation through the existing SDK, without a new
publish or CAS. Then continue the old cursor and replay the terminal request after its deadline;
assert unchanged execution, domain state, versions and receipts. Redact logs and clean up both
processes and databases. This proves response-observed terminal replay across processes.

For a terminal execution whose HTTP response was not observed, start a raw-socket observer before
the confirmation POST and require zero response bytes through EOF or reset observed after termination
is requested, with process death confirmed. Use a private test gate after response serialization
and before committing response bytes; correlate its body UUID marker
with the terminal execution and effects observed through private SQL. Kill the first OS process
while that gate remains closed and verify it is dead. Start the second process with the same origin
and durable identities, explicitly reconcile through the existing SDK, then replay after the
deadline; assert the execution, receipts and domain state are unchanged. Keep the gate and any
helper route test-only, redact logs and clean up sockets, processes and databases. This proves
HTTP response non-observation. Neither terminal-restart scenario proves TCP acknowledgement loss,
`PENDING_ACK`, uncertain database commit, incomplete execution or suffix recovery, cancellation
while running, or `ATOMIC`; keep those and B6/B7 completion as separate gates. A new reader or
Spring context in one JVM is not an OS restart.

Prove a crash at `UNIT_COMMITTED_PENDING_ACK` separately: hold JVM1 after the first unit's real
commit and receipt but before ACK, independently verify cursor zero and the untouched suffix,
then kill it and confirm process death. Start JVM2 on the same stores and published origin; require
cold denial before explicit `reconcilePublished`. Authenticate and scope any private test-only
recovery command to the trusted subject, namespace, operation, proposal and execution before an
SDK lookup. A current-grants reader is an additional guard, not recovery authority. The published
protected proposal store needs an operational writable transaction even for lookup: use the
existing bounded `REQUIRES_NEW`/repeatable-read boundary, not a read-only consistent reader.
Observe a real public control in JVM2 before calling the existing `JdbcBulkDurableExecution.recover`
with the proposal's exact `BulkFingerprintContext` and a JVM2-owned recovery identity; do not
pretend a JVM1 token survived. Require verified receipt prefix one, increased `owner_epoch`, old
control `FENCED`, `STOPPED`/`RECOVERY_STOPPED`, unchanged suffix and release of only the bound
allocation's `state`/`released_at`/`release_reason` to `RELEASED`/timestamp/
`TERMINAL_RECONCILED`. Waiting for the stored unit deadline may be a harness safety gate, not an
SDK recovery precondition. After the execution deadline, prove receipt-first SDK replay with zero
callbacks counted by the SDK harness, and HTTP terminal retry
with an unchanged full 24-table protected snapshot and inspected terminal branch; those harness
counters do not measure every HTTP callback. Do not present the private command as an endpoint.
This is not proof of uncertain JDBC commit, `ATOMIC`, or B6/B7 completion.

### Prove Outbox ACK Reconciliation Across Worker Processes

Use `ExtraordinaryBenefitStatementOutboxProcessRestartTest` and its test-only
`RuleLabOutboxWorkerProcess` for the host outbox protocol. Keep the two independent
EmbeddedPostgres fixtures alive while replacing clients; seed the outbox once. Run
the production dispatcher in worker JVM1 with the real repository, minimal EMF,
`JpaTransactionManager` and proxied `REQUIRES_NEW` lease service. The existing HTTPS
consumer commits its inbox before withholding the response past the complete-body
deadline. Require `RETRY_SCHEDULED`, attempt one, `HTTP_TIMEOUT`, persisted inbox one
and outbox `PENDING` without a lease or delivered timestamp. End worker JVM1 and the
consumer, confirm process exit, then replace both with distinct PIDs on the same
stores. This is graceful process replacement and ACK-response non-observation, not
a crash, uncertain JDBC commit or Metadata kernel `PENDING_ACK` recovery.

Run the reconciler first in worker JVM2: require the exact message UUID, immutable
envelope fingerprint and persisted acknowledgement timestamp, `RECONCILED`, then
dispatcher `EMPTY`, with attempt one and one inbox/outbox row. Execute deliberate
duplicate `200/DUPLICATE` and changed-envelope same-UUID `409` probes only after
reconciliation; both must preserve the inbox row. These probes are protocol checks,
not dispatcher redelivery. Domain/audit row-count equality is a limited oracle, not
a full content snapshot. Keep the child's role restricted to SELECT/UPDATE on the
private outbox fixture; no shared producer-grant change. Use loopback HTTPS with
temporary trust material and private environment secrets, without changing parent
JSSE defaults or setting the Neon ephemeral-branch flag for local PostgreSQL.

Apply the PID, redaction and cleanup discipline of the bulk process proof above.
Resolve Java/keytool and the Surefire classpath portably; bound readiness, result
files, logs and process waits. Run this focal test with
`-Dpraxis.outbox.restart.evidence-directory=<fresh-owned-directory>` to preserve
the safe JSON and checked child logs after successful temporary-directory cleanup.
Publish evidence only after workers, consumer, both stores and temporary TLS files
are closed/removed; bind it to source/artifact hashes and the selected XML report.
This does not prove host bootstrap/restart, PostgreSQL restart, Neon deployment,
provider/IAM governance, `approved.v1` business fulfillment, exactly-once business
effects, complete T15 or B7. Keep the controlled destination proof distinct from
choosing a real corporate adapter and its authorized effect.

### Prove A Controlled Approval Fact With The Existing Outbox

For F-OUTBOX, distinguish generic transport/inbox acceptance from an observable
projection of `human-resources.extraordinary-benefit.approved.v1`. Inspect the
existing workflow approval, `ResourceActionTransition`, typed approval payload,
writer and `ExtraordinaryBenefitBulkCommandOutboxPostgresTest` before changing
the destination. Reuse the real kernel, writer, audit and receipt helpers; do not
copy execution logic, fabricate an approval identity, or call the separate
simulated `apply` effect to make the test appear complete. Metadata retains
execution/receipt ownership. A controlled fact projection is not payroll/ERP.

Provision the destination's exact synthetic scope at startup and validate the
closed six-field payload with canonical UUIDs, bounded integral values and
operationId equal to transitionId before writing. Keep the source audit's global
transition identity as the fact's unique causal key, and bind one fact to one
inbox message. One destination JDBC transaction inserts the inbox and fact, then
commits before ACK. A different message for the same transition must conflict
without leaving an orphan inbox. A duplicate must verify the complete stored
fact and never repair missing evidence by inference.

Persist event type so GET/probe can determine which delivery requires a fact.
Reconstruct the approved payload and immutable envelope from persisted typed
fields, context and correlation, then compare their fingerprint and identity
bindings to the inbox. A missing/corrupt fact cannot produce positive ACK; GET
reports unavailability rather than 404 absence that could authorize redelivery.
Fail closed on incomplete startup scope or incompatible scaffold schema,
including wrong columns/constraint definitions; do not invent legacy backfill.

Inject failure at the final fact INSERT for the actual committed source approval
and independently read both stores: destination inbox/fact must roll back while
source domain, audit, receipt and immutable outbox evidence remain unchanged.
Confront all six payload fields, operation/event/context/correlation, receipt
effectRef and message identity. After ACK-response non-observation and client
process replacement, reconcile first and compare full causal source content and
destination projection; source replay must invoke no admission/mutation. Keep
mutable delivery state separate from immutable content comparisons. Exercise
input/scope/duplicate/corruption negatives and export the actual selected child
logs with the PID, redaction and cleanup discipline above. Sequential causal
conflict checks do not certify a concurrent two-connection race.

For a deterministic destination concurrency proof, use the existing HTTPS consumer
and two real JDBC transactions. A fixture owner may hold private exclusive advisory
gates: a BEFORE inbox INSERT acquires a shared start gate, and an AFTER fact INSERT
acquires a shared finish gate. Observe two distinct consumer backend PIDs blocked
at start before releasing it. Shared start locks must coexist; an exclusive gate
that serializes the requests would not prove the constraint race. Then observe the
winner blocked at finish and the loser blocked on the winner's transaction by the
inbox message key or fact transition key. Release finish only after recording that
chain with PostgreSQL activity/lock evidence. Futures or elapsed sleeps are not
proof of overlapping database transactions.

Keep the combined observation budget below the existing HTTP deadline rather than
raising it for the fixture. The same message/envelope yields PROCESSED plus DUPLICATE
with identical ACK identity, fingerprint and persisted time. Different message IDs
for the same transition yield PROCESSED plus conflict; independently assert one fact,
one inbox and no losing inbox. Compare complete source evidence and receipt-first
replay with zero new callbacks. Install fixture triggers after consumer startup and
remove triggers/functions, release gates and close/cancel requests, JDBC connections
and child processes in every failure path. Export safe backend PIDs and phases,
not raw queries or sensitive payloads. These interleavings prove destination unique
constraint contention, not uncertain source commit, database restart or corporate IAM.

Use the existing restart harness and consumer rather than another worker/SPI.
Revalidate its generic transport test and changed producer helpers as needed.
Bind selected reports to the accepted source/artifacts. The controlled fixture
fits B0's destination proof; choosing an authoritative corporate effect, adapter
and IAM is a separate extension. Neither a local projection nor this guidance
alone closes T15, B5/B6/B7, deployed governance, exactly-once or Angular readiness.

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

## Governed Bulk Published-Photograph Proof

For bulk unit admission, inspect the Metadata-owned published-photograph path before adding a host workaround. The durable kernel owns the physical unit transaction and receipt; host admission callbacks run under that unit, and operational datasource reads/writes use its attested writable connection. Policy/grant authorities may use independent databases; their decisions must complete before the kernel rechecks control and invokes domain mutation. Published structural reads must retain the global SHARE on the same attested connection, with no cache lock or `REQUIRES_NEW` inside the unit. Readiness and capability/action response frames remain outside operational transactions. Receipt replay must precede new-mutation gates and must not invoke those callbacks again.

Prove uniform and per-item HTTP+PostgreSQL flows against the exact candidate artifact with the unchanged execution budget: positive domain/audit/receipt commit, stale-target denial without mutation, authorized delegated reads, unauthorized reads, and replay without another domain call. A getter that copies only its requested group does not prove the complete multi-group resolver fits the budget. Record source/artifact hashes and admission reasons; do not raise timeouts or claim adoption from compile-only/local-override evidence. Published dependency validation without an override remains a separate release/adoption gate.

## Prove Candidate ATOMIC Bulk HTTP

For the Mission Participant pilot, inspect `MissaoParticipanteController`,
`MissionParticipantAtomicEvaluationProvider`, `MissionParticipantAtomicConsumer`,
`MissionParticipantBulkOperationsHandler`, and Metadata's
`BulkOperationalDescriptorComposer`/`BulkOperationLifecycle`. Bind the two ATOMIC
confirmation IDs (`operations.missao-participantes.bulk-update-atomic` and
`operations.missao-participantes.bulk-update-items-atomic`) and their evaluation refs
to the exact `(mode, atomicity)` descriptors, concrete provider and published
seven-reference photograph. Keep the two PER_ITEM identities distinct; never borrow
their proposal, reader binding or operation control as ATOMIC authority; revalidate
shared domain grants under the exact operation scope. Reuse the five shared
proposal, proposal-results, execution, execution-results and cancel HTTP paths, with
their existing cursor, one issuance reservation per results request and
`NOT_FOUND_OR_DENIED` fallback.

Prove native ATOMIC `EXPLICIT`/`SYNC` selection at 1 and 50 targets and rejection at
51, the canonical lexical wire-ID order against the protected stored selection,
one receipt with ordered children, untouched non-target rows and replay without new
writes. Suspend one control and verify the global photograph closes every variant;
republication of one control restores only that identity to `READY`. Prove cancellation
of a real reservation before its first unit separately from concurrent cancellation:
known and random IDs must have the same public error for a delegate or revoked creator,
without IDs or protected facts. Confirmation of a multi-target stale version or a
proposal from the older photograph must add no domain writes or receipts. Use
`MissionParticipantBulkOperationsHttpPostgresTest` and its official PostgreSQL fixture;
use `praxis-java-command-concurrency-authoring` for set transaction, deadline,
receipt-first replay and recovery. For an old proposal against a newly `READY`
control, trace Metadata's `BulkQuotaLedger.lockProposal` through
`JdbcBulkDurableExecution.reserve` to the host handler: `NOT_EXECUTABLE` maps to
safe `409`/`BULK_CONFLICT`; an unavailable current operation remains a separate
generic `503` path. A Git-addressed candidate dependency is local evidence only;
separately prove the published artifact and host adoption without an override. Do not
infer public host ATOMIC `READY`, T14/T15, B7 or
concurrent-cancel coverage from a focused HTTP test.

## Prove Overlapping ATOMIC Domain Sets

For the private Mission Participant kernel proof, inspect
`MissionParticipantAtomicConsumerPostgresTest`, `MissionParticipantBulkPreparation`
and `MissionTeamConcurrency` before inventing another lock protocol. Evaluate and
reserve two distinct proposals at the same versions with reversed target ordinals;
use independent consumers and the existing G→E→M→P locks. Hold the first actual
participant UPDATE at a disposable test trigger/advisory gate. Observe its exact
PostgreSQL PID and advisory key, then observe the competing PID blocked directly
on that writer's employee `FOR UPDATE` transactionid lock. Release the gate only
after this causal observation, within the native lock and aggregate unit budgets;
a sleep or two submitted futures alone is not concurrency evidence.

Require one complete domain commit and ordered receipt children bound to the
protected manifest, while the contender rechecks and leaves only its canonical
rejection, with no receipt, children or effects. Compare full selected rows with
the expected final state and unselected rows with their original state. Replay
both terminal controls and compare relevant execution/proposal evidence and both
proposal and execution allocations; `EXECUTION_ACTIVE` has a null proposal ID,
so a proposal-only snapshot misses its quota state. Keep protected snapshots in
memory and export only safe PID/status/count evidence. Close gates, triggers,
connections, futures and the fixture on failure as well as success. Run the new
method alone when previous helpers are unchanged, retaining source/XML/artifact
hashes. This proves the bounded private overlap case, not concurrent cancellation,
real uncertain COMMIT, HTTP readiness, global B4 completion or Angular readiness.

## Prove Cancellation During an ATOMIC Domain Transaction

For the private Mission Participant cancellation proof, hold the real first
participant UPDATE at the disposable domain gate. Observe the writer there, then
require the cancel PID waiting directly on that writer's execution row: an active
transaction, the execution `FOR UPDATE` query, a granted tuple AccessExclusiveLock
on the execution relation, and an ungranted transactionid ShareLock. The queued
tuple lock establishes cancel-before-ACK for this PostgreSQL test; a wait on an
earlier bucket/proposal is not the same proof. Release within the existing budgets.

Do not report this confirmed set as cancelled. Require the committed receipt and
all children, `RECONCILIATION_REQUIRED` with its cancel marker, and an active
execution allocation. Receipt-first recovery must certify the complete set, finish
`COMPLETED`, preserve the marker as history, advance the owner epoch, fence the old
control and release the allocation with `TERMINAL_RECONCILED`. A spy around the
real domain service may count calls but must not replace actual PostgreSQL writes.
Compare domain and protected evidence across recovery and replay, excluding only
expected lifecycle changes during recovery; the final replay must change nothing
and must invoke no admission or mutation callback. Preserve source/XML/artifact
hashes, export safe lock/status evidence and close all private gates/resources.
This covers cancel-before-ACK during a real collective mutation in one JVM/database;
ACK-first cancellation, HTTP/IAM, process loss and uncertain COMMIT remain separate.
