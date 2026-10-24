---
name: praxis-api-quickstart-operational-proof
description: "Use when Codex must implement, audit, or diagnose Praxis API Quickstart as the real Spring Boot reference host: Maven starter composition and versions, bootstrap/properties/datasources, security and browser policy, metadata/config/runtime HTTP integration, schemas and discovery, agentic authoring/SSE host proof, deployment identity, or ownership routing between quickstart, metadata starter, config starter, and Angular consumers."
---

# Praxis API Quickstart Operational Proof

Use this skill for the Quickstart's role as the operational reference host. It proves that canonical Praxis contracts survive Maven packaging, Spring Boot auto-configuration, security policy, real persistence, and HTTP consumption. It must be a thin, explicit integration point, never a parallel implementation of metadata, configuration, AI, or business-decision semantics.

## Governed cold-node recovery on Render

Inspect `LocalPublicationRecovery`, `LocalPublicationRecoveryClient`,
`GovernedOpenApiPublicationHealthIndicator` and the host's
`docs/engineering/render-startup-reconcile.md`. Metadata owns
`BulkOperationLifecycle.readPublishedReadyGeneration(identity)` and
`reconcilePublished`; the generation lookup is a fenced momentary hint, never
an authorization or promise that reconciliation will succeed.

Use only the fixed host operation/namespace and current durable generation.
Inspect its actual provider registration before adoption: the official administrative
endpoint is bound to the uniform operation. The current ASYNC profile requires all
six provisioned capacity coordinates. Missing registration or a previous SYNC
photograph stays closed; do not choose another READY provider as an alias for this
endpoint or copy test capacity into production. A producer/profile change needs
the existing explicit governed republication, outside the startup runner.
The startup runner may call the existing real HTTP reconcile once on its own
native Servlet listener (actual port/context path), using the already configured
publisher login. Never route through the Render load balancer, synthesize a
Servlet request/SecurityContext/JWT, assign an administrator alias, publish,
suspend, rebase or retry automatically. Native SSL listeners require their own
verified binding; never disable certificate verification.

The issued HttpOnly SESSION may use its officially supported Bearer SESSION
transport without changing Secure cookie attributes. Require the active stored
session and current RECONCILE grant at the controller, and actual CSRF cookie/header
when the effective host policy enables CSRF. Preserve logout204 plus GETsession401
with the same token as revocation proof. Uncertain issuance/cleanup keeps readiness
closed. Never log credentials, tokens, headers, response bodies or raw causes.

Readiness must include the live published photograph guard and existing dependency
health checks, veto startup PENDING and uncertain cleanup, and recheck durable
suspension after a successful recovery. Liveness stays separate. UNCOMPOSED remains
closed until explicit first publication; digest drift requires authorized
republication. Automated reconcile cannot approve changed producer bytes.

Prove the executable host JAR on assigned isolated Neon children with ordinary
runtime/control roles: first explicit publication, cold secure-cookie recovery
without manual reconcile, current grant revoked, fresh document drift and live
suspension. Attest exact source/JAR/dependency hashes, compare durable state and
domain inventory, and confirm temporary publisher sessions revoked. Local mocked
HTTP/runner tests do not certify IAM, Neon, public SDK adoption or Render. A private
candidate GAV/cache must be recorded separately and never overwrite public coordinates.
A new public SDK release remains a separate authorized official workflow gate.
Before creating a release tag, inspect Metadata `RELEASING.md` and run the official
`tools/release/neon_gate.py` inventory preflight for all three selections on the
clean reviewed source, with the full resolved base SHA and its current POM version.
A passing focal test does not update test-source hashes or broad impact/reuse
closures. Review affected dispositions against the actual production/dependency
diff before refreshing hashes; preserve original historical receipts and limits.
A tag-version-only commit is validated separately by the official assignment guard.
If a queued publication must be cancelled for stale custody, retain its immutable
tag and use the next free version after canonical repair; never silently retag,
substitute public bytes or count cancelled publication as release/adoption.

On the ASYNC host, retain six independent RR/READ ONLY snapshots of authority,
installed rights/slots, domain and empty proposal/execution/receipt/admission stores;
assert equality across publication/recovery/denial/drift/suspension. An owner
witness is not product-role evidence: provisioner/allocator/reader and runtime/control
must satisfy their actual canonical profiles. Invoke capacity provisioning only
as an external administrative preparation, never as startup automation.

For published-SDK cold proof, inspect the existing
`bulk-reference-consumer-proof.yml` cut `quickstart-startup-recovery-neon`, its
same-commit reusable `bulk-startup-recovery-proof.yml` and
`docs/engineering/cold-reconcile-public-sdk-proof.md`. Require the reviewed host
POM's public starter pins, a fresh Central-only cache, immutable release JAR/POM
hashes and matching nested/class-origin bytes; do not rebuild/install a replacement
SDK or override dependency versions. Package and attest before injecting the
dedicated child-assignment secret. Never overwrite the shared basic-proof secret
or reuse another worker's branch/lease. Execute only the five-boot method on the
assigned prepared fixture; retain sanitized source/package/branch receipts and
failed cuts separately. This proves public-artifact adoption only for that case,
not live Render cold recovery, HTTPS or Hero. Historical private-GAV receipts
remain bound to their original sources/bytes; an unpublished candidate needs its
own reviewed custody and cannot count as public adoption.

Inspect the existing governance reader pool before relaxing operational deadlines.
`DataSourceConfig.governanceReaderConfig` retains one validated ordinary idle
connection per replica. Hikari fail-fast closes its test connection when minimumIdle
is zero; a later cold remote TLS connection can exceed the <=1s acquisition budget.
Keep the same API endpoint/role, read-only reader, bounded maximum capacity and
acquisition/SQL budgets. Prove retained startup connectivity on Neon; mocked pool
configuration alone is not recovery proof. HTTP recovery diagnostics project only
closed phases/statuses and allowlisted existing API error codes, never raw responses.

A restored publication does not certify the Hero journey. If a fresh schema or
table read fails, inspect actual API/Config Hikari active/idle/waiting counters
and the exact pool configuration before attributing it to reconciliation. The
reference Render deployment exhausted an API pool of three connections with
four to eight waiters; keep that negative separate from the capture timeout.
Size finite pools through the existing host environment properties only after
checking actual Neon endpoint/role limits, other clients and rolling replicas.
Account for API, its detached governance reader and control plane together;
Config consumes its own endpoint budget. Keep acquisition <=1000ms and all SQL
budgets, roles, TLS and six provisioned ASYNC coordinates unchanged. A fixed pool
(minimumIdle=maximumPoolSize) is a best-effort maintained target, not proof of
prewarming or throughput. Require effective connections, new deployment/restart,
fresh schema/filter responses and rendered/paginated Hero rows before acceptance;
health UP or configured maximum alone is insufficient. Environment-variable
changes require the official Render deployment flow, not a presumed live update.

For a generation/runtime exception, reuse the existing bounded code-only
`BulkPublicationFailureDiagnostics.failureGraph` projection described below;
exclude messages/SQL/new diagnostic queries and preserve the original outcome
even if the diagnostic sink fails.

For failures in the authorized proposal/results readers, inspect Metadata's
`BulkReadFailureDiagnostics` and `docs/technical/BULK-COMPOSITION-GUIDE.md`, with
the current `praxis-java-command-concurrency-authoring` guidance. Its capture is
local to one invocation, bounded first/last and emitted after the owned decision;
it is distinct from publication diagnostics. Do not add queries or expose SQL,
messages or identities. A slow sink may delay delivery, and the release B/C/H/P4
gates do not observe these reader paths; retain that limit in consumer evidence.

## Pinning a pending Render candidate through its private IP

When the service hostname cannot identify the intended candidate, inspect the
host's `RenderNodeIdentityDiagnostics`, its focused test and
`docs/engineering/render-startup-reconcile.md`. Render documents
[direct private-IP access](https://render.com/docs/private-network#direct-ip-communication-advanced),
but that does not prove reachability of a pending instance. Treat this as an
existing route requiring identity evidence, not a new endpoint or an automatic
publication mode.

Bind the root Servlet startup log to the active Render deployment/instance and
reviewed source/build: allowlisted Render identity, actual JAR SHA256, build
version/time, private IPv4 interface candidates and actual listener port/context.
Inspect the exact `PRAXIS_RENDER_NODE_IDENTITY` JSON projection; do not infer an
unemitted address or source field. Keep
the diagnostic log-only, bounded and failure-isolated; never dump environment,
credentials, headers, responses or raw causes. A local address is a candidate,
not proof that it is reachable. Do not guess an IP or treat getLocalHost, wildcard
or loopback as the target identity.

If the old instance relays the request through its official SSH channel, attest
it separately: the relay SSH pin does not pin the remote HTTP candidate. Before
each command, recheck that the candidate is active in Render, compare the exact
source/build pins and `/actuator/info` with startup custody, and use only the
observed IP/port/context. Info alone does not attest JAR bytes or the IP. An IP
is a time-bound observation and can be reused; absent, divergent or ambiguous
identity stops the flow. Never use service DNS, a load balancer, proxy or redirect
as a substitute for that pin, or weaken health, TLS, ACL or CSRF to gain access.

When SSH is unavailable and WebShell reaches only the old live instance, inspect
the host's versioned `scripts/workspace/governed-publication-native/` package.
Its finite PropertiesLauncher client supports NATIVE and RELAY without starting
Spring; build against reviewed host dependencies and preserve the source/artifact
receipt, synthetic fixtures and explicit-main probes. Prove the actual candidate's
build, login, SESSION and logout204/session401 through the intended transport
before suspension. An open WebShell on the old node alone is insufficient.

RELAY fixes the startup-observed private IPv4 and pins the native relay per
request. Require the real Render CP snapshot within30s before login and the sole
POST, plus HTTP build checks before both; report that these are not candidate SSH
pins. The current-grant witness belongs to the relay. Require the coordinator's
preserved attestation of equal publisher/binding/datasource and an exact expected
target grant-context match; never label it an independent SQL observation of the
candidate. The target server still revalidates SESSION and current authority.
Keep credentials in the native environment/memory. Preserve CREATE_NEW/fsync
journals and independent post-command durable readbacks. Export sanitized HTTP
receipts/journals to custody outside an ephemeral relay before promotion destroys
it: fsync does not survive pod deletion. If a final HTTP receipt is lost, report
that limitation separately from durable publication/session readbacks; do not
repeat the command to recreate evidence. CP expiry after a long
POST must not suppress cleanup to the immutable target; unconfirmed cleanup or
response remains failed without retry. Suspend and publish each have their own
240s request limit and preparation/readback/cleanup, so qualify enough rollout
lifetime for both before opening the authorized global window. Do not extend
server budgets or weaken health to compensate for a short-lived candidate.

Before enabling the existing SPA CSRF policy in a deployed host, verify its
current effective flag and the browser SESSION header. Qualify cold recovery
with Secure=true on both SESSION and XSRF cookies: Java CookieManager does not
replay Secure cookies over native HTTP. The pinned loopback machine client must
explicitly echo the actually issued CSRF pair, preserve browser cookie attributes
and SESSION Bearer authentication, and still attest logout/session401. Never
solve that transport gap by disabling CSRF or downgrading Secure cookies.

Administrative CLI jobs need an observed launcher/argv receipt in the actual
Render image. Do not treat shell quoting validated locally as proof that Render
interprets startCommand identically. Qualify an inert probe, retain plan output
and JAR pins, then apply once with the reviewed fingerprint and unchanged inputs;
uncertain results require readback rather than automatic replay.

The optional ApplicationReady candidate capture is not a publish prerequisite:
Metadata178 prepares and validates the photograph inside the protected HTTP
publish request before its transactional CAS. Its Servlet-context requirement
makes an out-of-request diagnostic insufficient; do not fabricate a Servlet
principal/context or add an endpoint just to turn that diagnostic into acceptance.

Preserve the existing explicit global-window authorization, real login/SESSION,
current per-operation grants, effective CSRF, observed-generation CAS, both ledger
readbacks and logout204/session401. A timeout or503 can follow a committed phase;
inspect durable state without automatic retry, rebase or SQL repair. Never publish
from the diagnostic or startup recovery. Manual publication installs the photograph
in that JVM and can restore readiness when the live guard and dependency checks
pass; a previous UNAVAILABLE is not a veto, unlike PENDING or uncertain cleanup.
It does not retry or prove the one-shot runner. Keep cold reconciliation of the
identical photograph as a separate gate at the next required deployment; do not
require an immediate redeploy solely because the previous runner was unavailable.

Do not start a second full app in a job/ephemeral shell to bypass access: the
current startup may run the bulk worker and Config indexing recovery. Removing
capacity/lifecycle changes the producer photograph. Require a separately proved
administrative isolation before teaching such a process. Key acceptance followed
by channel closure does not establish a root-lock, image or health cause; do not
unlock root or change health based on that symptom. Keep this route pending until
an actual Render receipt binds source/JAR/instance/IP/listener, relay, commands,
cleanup and readbacks. Source integration, SDK publication/adoption and hosted
proof remain separate gates.

For an authorized isolated host proof, inventory startup event listeners (including
`ApplicationReadyEvent`) and synchronous callbacks as well as runners, scheduled
workers and `PostConstruct`. A Started log does not prove those callbacks finished.
Config162's API metadata indexing recovery is unconditional; registry-bootstrap=false,
Spring AI disabled or worker-count=0 do not disable it. Before booting an exclusively
assigned child for an unrelated journey, prove PENDING/PROCESSING=0 with a fresh
ordinary-runtime read and compare inherited rows after boot. This is observed
quiescence, not a recovery switch. Use the existing
`praxis.domain-catalog.rag-publication.enabled=false` when excluding domain-catalog
RAG recovery from that proof. If inherited work exists, stop and resolve isolation
canonically; never erase work, invent a flag or infer containment from missing logs.

## Isolated administrative one-off jobs

Prepare and prove the recovery transport **before suspending** a publication.
Inspect the host procedure, reviewed operator/dispatcher source, dependency/class
allowlist, artifact hashes and actual remote receipts. An open shell or a probe
from another process is not proof that the recovery client can operate. Without
a usable route, preserve the live service and report the blocker.

A one-off may run a finite HTTP administrative main; it must not boot the full
Spring app, its workers, Config indexing recovery or seeds. If it uses the host's
PropertiesLauncher and existing Jackson, prove that the explicit external main
alone executes: inspect for SpringApplication/context/SQL/bootstrap and run the
innocuous main probe plus focused local HTTP tests. A successful class load is
not that proof. Keep temporary operator artifacts tied to the reviewed operation;
do not present their paths as a shipped public host command.

Attest the relay job's actual service/commit/JAR separately from the candidate.
Do not infer its image from the pending rollout: job creation has no deploy/image
selector. Keep the destination immutable at the startup-observed private IP and
actual listener, confirm build over HTTP, and forbid service DNS, proxy, load
balancer, redirects and fallback. Inherit credentials only through the reviewed
environment boundary; never embed them in the start command, input projection,
logs or receipts.

Require real fresh Render CP and protected ledger readbacks before dispatch.
Queueing consumes validity: revalidate the reviewed evidence after job startup,
before login and before the sole POST. An embedded CP projection is a bounded
snapshot, not a live API check or guarantee during the request. Use the exact
reviewed client's fixed freshness budget; never refresh timestamps artificially
or turn a larger allowance for one measured queue into universal guidance.
Expiry before authentication is a protected negative, not publication success.

Before any create-job call, the prepared dispatcher durably records its attempt
with O_EXCL, private permissions and file/directory fsync. Never delete or replace
that sentinel after a failure, or silently choose another attempt name to repeat
an uncertain intent. Job creation accepted, execution started, request possibly
sent and response validated are different states. Inspect job outcome and both
ledgers after any uncertainty, without retry, rebase or SQL repair. A new attempt
requires the previous outcome resolved and explicitly reviewed fresh evidence.

Preserve global-window authorization, real SESSION/current grants, effective
CSRF, observed-generation CAS, one POST and finally cleanup on the same base.
Only logout204 plus session401 confirms revocation. Keep pre-auth expiry,
not-dispatched and uncertain-cleanup receipts distinct. The reviewed isolated
client's CP60s budget and 50 offline/local-HTTP cases belong to this cut, not a
platform-wide policy. Its later COMPLETED_HTTP_ONLY receipt confirmed the response
and session cleanup; separate readbacks confirmed READY15/PUBLISHED24 and Render
reported the deployment live. Do not derive durable state from the HTTP label
alone or erase the earlier pre-auth expiry. Source integration, public SDK
release/adoption, authenticated HTTPS, the next cold reconcile and Hero browser
proof must each have their own actual receipt and independent review. A subsequent
passing Hero pagination receipt is separate from publication acceptance and does
not replace authenticated HTTPS or cold-node proof.

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
- `run_local.sh`, datasource wiring, and the reviewed launch guard/offline negatives for the actual packaged-host proof, when present
- `SecurityConfig.java`, `ConfigOriginRestrictionFilter.java`, and related security filters
- `QuickstartMetadataMigrationIntegrationTest`, `EventosFolhaPilotIntegrationTest`, and `OpenApiGroupResolutionIsolatedIntegrationTest`
- `ResourceEntityLookupGovernanceIntegrationTest`, `ProcurementExternalOptionSourceProviderIntegrationTest`, and `VwStatsSmokeHttpTest` when option-source contracts are hosted
- `AiPatchSchemaResolutionIsolatedIntegrationTest` and `AgenticAuthoringStreamIsolatedIntegrationTest`
- the affected host authorization adapter and deterministic database fixture when a governed E2E lane exercises principal-specific capabilities
- `PraxisCockpitStarterConsumptionIntegrationTest` and `ActuatorInfoBuildContractIntegrationTest`
- `docs/COCKPIT-QUICKSTART-REFERENCE.md` and `docs/AI-HOST-BUSINESS-GROUNDING-GUIDE.md`

For a suspected starter defect, inspect the owner repository before proposing a host adaptation. The quickstart test is downstream evidence, not a replacement for the owner test.

## Remote Database Proof For Praxis

For every Praxis validation that depends on a database, run the focused test or
smoke against a remote Neon branch isolated and explicitly assigned to its worker
or run. Test code may run locally, and unit tests without a database may stay local;
an embedded/local PostgreSQL fixture is not a substitute for the remote proof.
If the branch, credentials or required role profile is unavailable, record the
pending gate without a silent local fallback.

Before connecting or mutating, verify Neon project/branch, endpoint, PostgreSQL
version, TLS and the concrete owner, runtime and control-plane identities and
grants when applicable. Exercise the same privileges required by the host; do not
infer SUPERUSER or treat a privileged setup identity as the product path. Mutate
and clean up only the assigned branch, never its parent or production database;
test authorization does not authorize deployment or release. Bind raw evidence to
source/dependency/binary hashes and branch identity. Prior local PostgreSQL results
remain historical local evidence, not a new remote Neon result.

This rule takes precedence over historical recipes below that start
`EmbeddedPostgres`, local fixtures or privileged setup roles. Adapt their causal
assertions to the assigned Neon branch and available permissions before counting
new database acceptance; if that is impossible, leave the specific gate pending.
Do not run an unchanged local recipe as replacement evidence or assume Neon exposes
SUPERUSER, host-based authentication files or cluster-internal catalogues.

### Integral Assigned-Neon Release Gate

Use the [integral gate procedure](references/integral-neon-gate.md) when accepting
the complete private and sanitized Quickstart trees. Inspect the current
`config/neon` test support, assignment materializer, isolation policy and both CI
workflows before running. Database allocation and ordinary runtime wiring are
test infrastructure; they do not replace SDK migrations or alter product ACLs.

For remote diagnosis of the declared Bulk cases, the same procedure documents
`validation_scope=bulk-focal`; its bounded source selection is not a release gate.
Keep focal results, helper validation, integral private/sanitized verification,
public snapshot publication and deployed HTTP acceptance separate. A declared
workflow or passing focal sample is not evidence that the integral gate ran.
Do not promote this procedure as accepted until its exact helper, source,
dependencies and two-tree remote results have passed independent review.

Before rerunning a database-backed HTTP fixture after a timeout, inspect its actual
runtime datasource and connection lifecycle. A simple datasource may establish a
fresh remote TLS session for every JDBC borrow; distinguish that harness cost from
an SDK transaction or HTTP failure. When the fixture uses a pool, require bounded
capacity/acquisition and explicit warm-up outside the measured operation, then a
read-only check of the same ordinary runtime identity, database and TLS path.
Keep owner/runtime credentials and privileges separate; do not replace identity
checks with role switching, weaken TLS, extend product deadlines or retry domain
commands. Close and attest the fixture-owned pool before assigned-database cleanup;
borrowed/unclosed connections and uncertain cleanup remain fail-closed evidence,
not permission to force-drop resources. Inspect the current `config/neon` support
and its offline lifecycle tests, then prove the unchanged HTTP/persistence oracles
and cleanup on the assigned Neon branch. Pool configuration or warm-up alone is
not acceptance, a throughput guarantee or a certified SLA.

## Integration Topology And Owners

### Durable OpenAPI Across Cold Nodes

Inspect the exact deployed Quickstart SHA and Metadata version before diagnosing
`GOVERNED_OPENAPI_PUBLICATION_UNAVAILABLE`. A READY operation and PUBLISHED ledger
with matching generation/digest attest durable compatibility, not installation in
the current JVM or equality of a newly captured document set. The ledger stores
the aggregate digest, not the original response bodies or producer source SHA;
retain deployment/JAR provenance and protected capture evidence outside it.

Metadata captures exact bytes of root, every group and `swagger-config` through
the official local Servlet transport. Springdoc can embed the physical listener
in generated `servers` and `oauth2RedirectUrl`. Ordering object keys does not
stabilize these values; fixing only `servers` leaves swagger-config unstable.
Use the host's standard Springdoc configuration and deployment-relative servers
to make the producer stable. An OAuth redirect must be an explicit absolute
deployment URL; Springdoc re-expands a relative redirect against the listener.
Inspect `OpenApiPublicationOriginConfig` when adopting the host correction, and
configure native `springdoc.swagger-ui.oauth2-redirect-url` before enabling its
governed-publication startup gate. Do not redirect the Metadata capture transport,
rewrite captured bytes, ignore server fields in hashing or fabricate producer leases.

Prove byte equality of root, group and swagger-config with different listener
addresses/ports, fresh Springdoc contexts and a non-root context. Include an
uncorrected control that reproduces the varying URLs. A test with no datasource
can prove producer stability; it cannot certify lifecycle installation. The
packaged lifecycle proof still needs assigned isolated Neon branches, real SESSION
and current grants. A cold restart on the same fixed listener does not cover pod
address changes. For a new producer digest, prepare explicit suspension/publication
with their global impact and observed CAS generations; reconcile cannot replace
the old digest and must not be retried after an uncertain response.

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

When fresh runtime roles are attested after V18/V19 storage was completed without
roles, provision the exact additional read boundary: SELECT on capacity marker,
installation, slot and occupation relations, plus EXECUTE on the canonical marker
and claim functions. Read the exact relation/function names from Metadata's existing
catalog and consumer fixture. Do not add DML, PUBLIC, grant options, bootstrap access
or owner membership, and never weaken COMPLETE validation to repair drift. Preserve
configured-role negatives and the bounded control/fence callbacks.

The independent fresh-JAR consumer must assert the packaged V18/V19 resources and
current migration count, preserve historical checksums and bind codeSource/private
classpath evidence to the committed candidate. Do not copy SDK helpers or classes
into the consumer, replace HTTP evidence with kernel assertions, or count the nested
consumer test twice in outer suite totals. Public adoption still requires Central
POM/JAR provenance and the host dependency without a local override. Non-superuser
OWNER PostgreSQL 14 evidence and superuser PostgreSQL 16 HTTP evidence certify
different profiles; neither closes the OWNER-16 membership compatibility risk.

Prove administrative image packaging separately from standalone consumer HTTP tests.
Use the official host Dockerfile and a manual, reviewed-SHA workflow with read-only
permissions, no persisted checkout credentials and public committed dependency pins.
Require public Central POM/JAR provenance and exact nested Metadata/Config JAR bytes,
image/base identities, wrapper bytes and mode0755. A network-none container with no
ports or mounts may run INSPECT against a proved-absent absolute configuration path:
assert exit64, empty stderr and the exact five-field INVALID_INPUT JSON without
startup output. This proves COPY, PropertiesLauncher and the SDK Main; it does not
prove PostgreSQL OWNER, FENCE, runtime serving, custody or continuity. Keep the
packaged-JAR PostgreSQL proof and host verify separate. Select
BulkCapacityLocalAdministrationPackagedJarPostgresProof explicitly after package;
default verify does not run the Proof suffix. Supply `praxis.bulk.admin.packagedJar`,
`praxis.bulk.admin.metadataCentralJar` and `praxis.bulk.proof.directory`: absolute
paths, with the evidence directory already existing and exclusive. compare the POM's public pin and all three SDK
byte origins. Byte equality alone does not establish Central provenance: retain
independent resolution evidence. Capture source drift, raw
output and cleanup of only owned image/container resources; upload evidence rather
than caches, JARs or credentials. Do not deploy or push an image for this gate. If
Docker is absent locally, the required official remote proof follows the existing
integration authorization after independent review; do not substitute B6 fixtures.
Private workflows and tests referencing them must remain excluded from the public
snapshot. Never describe unexecuted packaging code as an installed/proven container.

Do not infer base-image provenance from optional digest text in BuildKit progress
logs. Use the official Dockerfile unchanged with Buildx `--load --metadata-file --pull`
and `BUILDX_METADATA_PROVENANCE=max`, recording client/builder identities. Require
the two canonical Docker source steps to report registry `image.resolvemode=pull`
and the known platform; local resolver materials are not registry witnesses.
Require each source identifier to be the exact canonical name/tag plus `@sha256`
root verified from that base's registry graph; require its material digest to equal
that same root. Do not strip the pin or accept another valid manifest/config node. Verify
the typed output config digest against the actual loaded image ID. For each exact
Docker base material, check its canonical Docker Hub name, tag, platform and
digest against the pulled immutable reference and its verified OCI chain:
hash the registry response bytes for the index, selected platform manifest and
config, and link the config to the pulled image ID/OS/architecture. Index,
manifest and config digests are distinct identities; a digest-shaped string or
a hash found somewhere in a log is insufficient. Known canonical official-image
reference spellings may be normalized explicitly; never use fuzzy aliases.
Missing/duplicate/unknown metadata, wrong digest or platform must deny the gate,
without a text-log fallback. Keep offline negative cases for the verifier and
preserve the real graph/metadata plus source freeze and owned-resource cleanup.
Local-context `completeness.materials=false` does not certify hermetic builds,
complete SLSA provenance or reproducibility. A failed pre-launch provenance gate
does not certify wrapper execution; diagnose it before a single corrected retry,
and reuse unchanged Java/HTTP/JAR proofs rather than repeating their suites.
The reference procedure is in the host's
`scripts/workspace/bulk_capacity_image_provenance.py` and its offline tests.

## Keep Private Worker Proofs Separate From Host Adoption

When reviewing a Metadata worker candidate, freeze its source and private coordinate
before Maven, then require a different author's source review. Preserve each run's
actual exit, fresh XML, full source snapshot and owned-process cleanup. A predecessor
suite does not certify bytecode changed later; repeat only the cases affected by a
reviewed correction. Count one JUnit method with five scenarios as one test.

Use finite causal probes on the actual JDBC path when ordering cannot be established
from a snapshot. Delegate original SQL unchanged, retain its original exception,
and distinguish a marker after the handler decision from an early selection marker.
Verify physical domain/receipt commits independently. A fixture flag about built-in
barriers does not prove that custom instrumentation was absent.

SDK process/queue/lifecycle proofs do not certify host HTTP/JWT authorization,
background domain grants, public readiness or auto-configuration. Keep those
consumer gates pending until implemented and proven with the supported public
artifact. Namespace filtering in the same database is also distinct from tenant
or grant isolation. Do not expose a private internal worker as a public recipe.

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

When a domain unit already holds an API connection, audit every independent read
and synchronous durable evidence append, including item-command revalidation.
`REQUIRES_NEW` separates transactions, not physical pool capacity. A bounded timeout
does not prevent structural starvation when nested work needs another API slot.
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

For an existing independent JPA evidence append, inspect
`RuleExecutionObservationPublisher`, `RuleExecutionObservationOutbox`, its appender
and store configuration. Preserve synchronous commit before return and durability
for DENY and caller rollback; do not substitute REQUIRED, lossy asynchronous work,
larger domain pools or longer timeouts. A dedicated bounded physical writer pool must use
the same effective ordinary API runtime identity, destination and TLS settings.
Never delegate it back to the occupied API pool or borrow owner/Config credentials.
Keep its private PU/transaction manager restricted to the existing outbox entity
and table, without domain lookups, callbacks, duplicated SQL or schema creation;
retain the existing claim, acknowledgement and dispatch path. Verify mutable driver
and health-check Properties are detached: shallow Hikari copying plus merging
setters can still alias the source. Warm the pool with a read-only bootstrap probe,
close it through Spring before assigned-database cleanup, and include its capacity
in the per-instance connection budget. On assigned Neon, hold every API slot while
appending ALLOW/DENY evidence, require append completion before releasing callers,
then roll callers back and prove only the independent evidence remains committed.
Prove the writer's ordinary identity and single-entity mapping; retain the real
concurrent HTTP command's one-effect and 409/412 loser oracles. Source/unit proof
alone does not certify that saturation, rollback or HTTP interleaving on Neon.

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
Before Config or an independently acquired grant lookup, subtract the configured
maximum pool-acquisition time plus a small scheduling margin; validate that the effective pool setting
really enforces that cap. Recheck the unit deadline immediately after each
external/starter call and before any next read or mutation. If the reserve or
remainder is insufficient, fail closed without starting that work. Do not reuse a
stale `Duration` captured before a prior blocking call.

The SDK creates the durable five-second unit deadline before the host admission
callback; do not assume five seconds remain at callback entry. Inspect the actual
supplier passed through `MissionParticipantExecutionService` and the LOCK helpers.
For LOCK/read SQL/JPA on an already-bound operational connection, reading its
supplier must only sample the live remainder, without hidden SQL, `set_config` or
pool acquisition.
Bind each statement/query timeout from that fresh remainder and fail closed below
its usable granularity. Keep explicit timeout clamps at entry and immediately before
mutation/flush, whose ORM writes are not all individually wrapped; never widen a
stricter existing GUC or renew the deadline. A separate Config transaction or other
pool still requires its original acquisition reserve; an existing API connection
does not make that reserve redundant. Count actual SQL at getters and explicit
boundaries, then prove decreasing/subsecond remainder, lower GUC preservation and
expiry before mutation. Pair the finite tests with real Neon domain/receipt COMMIT
and rollback; fewer clamp roundtrips or local tests do not certify the complete HTTP
journey or Render deployment.

Distinguish a host capture phase-local view from the LOCK/execution pure
supplier: the capture SDK getter still performs SQL. Prove delayed-get accounting,
decreasing/expired local remainder, bounded fully materialized decoding without
per-row SQL, original-supplier rejection on normal exit, and preservation of a
primary exception or Error. Keep the capture transaction timeout derived/floored
from the existing eight-second remainder after pool reserve (about six seconds
in the current profile), the five-second unit and thirty-second execution budgets,
and immutable proposal expiry unchanged. `CAPTURE_FINISH` HTTP503 alone does not
establish a timeout or remote correction; retain the bounded private cause and
require assigned-Neon FULL3 preview/CONFIRM/executions/results/replay with complete
protected readback before claiming that gate.

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

## Repair Runtime Governance ACLs With Forward Migrations

Inspect actual table ACLs as well as the migration's GRANT statements. PostgreSQL
`GRANT SELECT` is additive: permissive owner default privileges can leave INSERT,
UPDATE and DELETE on newly created governance tables. A passing Flyway validation
or unchanged domain rows does not certify least privilege. For the host binding
and principal-grant tables, runtime access is read-only; administrator provisioning
and explicitly granted SECURITY DEFINER writers remain separate.

Use `V20261009_001__operational_governance_runtime_read_only.sql` and
`QuickstartPrincipalGrantRepositoryPostgresTest` as the forward correction/proof.
Revoke the configured runtime role's table privileges and restore SELECT only on
the affected objects. Do not rewrite an already applied migration/checksum, widen
runtime privileges to finish a probe, alter owner defaults globally, or replace
an auditable migration with an ad hoc production REVOKE. Ownership, superuser and
inherited administrative roles bypass a direct role revoke: keep runtime role
attestation and never certify those configurations from table ACL text alone.

Reproduce permissive default table DML before the original CREATE in a disposable
PostgreSQL fixture. Verify the gap before the forward repair, then execute actual
runtime INSERT/UPDATE/DELETE negatives on both tables with SQLSTATE42501. Preserve
SELECT, owner provisioning, and the explicitly authorized writer's version/audit
behavior. Review the new pending version/checksum and exact packaged SQL before
an owned hosted rehearsal; retain successful historical migration/data proofs,
but keep ACL acceptance and subsequent migrate-zero pending until the correction
has been applied and independently checked. This does not certify a public
starter pair, application deployment or an HTTP authorization surface.

## Govern Missing Operational Migration History

Inspect `docs/OPERATIONAL-DATASOURCE-MIGRATIONS.md`,
`db/operational-migrations/README.md`, the normal operational migrator and the
candidate `OperationalDatasourceHistoryRecovery*` source/tests before choosing a
recovery procedure. This is host-owned operational history, not Metadata or Config
history. Manual `JdbcSqlRunner` examples execute selected SQL without maintaining
Flyway history; an old file list is not a complete installation or recovery lane.
Do not reconstruct unavailable historical SQL or bypass strict validation with
`repair`, schema reset or missing-migration ignore patterns.

Treat the current recovery command as a candidate until its exact operational
gates are accepted. Build its proposal from a fresh complete history snapshot:
all ten columns, including installed_by and microsecond-precise installed_on,
and the canonical missing tuples. Bind approved bytes/digests to the actual
packaged host, loaded Flyway, JDK/truststore, endpoint, database, role and bounded
quiescence window. A manifest assertion alone does not establish exclusive access.

Rehearse first on an owned non-default copy-on-write child. Use official control
plane metadata to verify parent/child/endpoint identity, actual roles, limits and
cost; explicitly set and read back expiration before SQL because API creation
need not set it. Expiration cleanup is asynchronous and does not prove quiescence.
Capture receipts and before/after history, domain, grants and catalog snapshots
with explicit scope. Preserve the parent and third-party resources; obey the
selected deletion tool's approval rule rather than promising automatic cleanup.

Prove append-only markers preserve original history, atomic rollback, bounded
lock/window gates and uncertain-commit reconciliation without blind mutation
retry. Then use the normal strict migrator: check the exact actual pending tuples,
apply only approved migrations, validate and repeat with no work. Explicit
validate may report pending migrations as well as missing ones; do not confuse
that diagnostic with migrate's internal pending handling or weaken validation.

Keep focused JDBC tests, contention, packaged read-only inspection, real TLS/JDBC
rehearsal, public dependency adoption/verify and deployment as separate evidence.
Synthetic historical rows and column/sentinel snapshots do not certify a complete
hosted corporate database. Preserve failed runs, bind evidence to the tested tree,
require another reviewer, and leave unproved gates pending. A private JAR inspector
that never connects is not a database recovery, release or Angular-readiness proof.

## Compose Bulk Installation In The Existing Predeploy Command

Inspect `OperationalDatasourceMigrator`, `BulkOperationalMigrationConfiguration`,
the packaged `/app/bin/praxis-operational-migrate` wrapper and
`docs/OPERATIONAL-DATASOURCE-MIGRATIONS.md`. Verify that the tested checkout actually
contains this integration: an older command may migrate only the host schema.
Do not treat a source patch, an available overload in an old starter, or successful
compilation as evidence that the published Metadata contains later installation fixes.

The existing `praxis.bulk.lifecycle.enabled` adoption property selects bulk
installation. Resolve its namespace/deployment/role properties through the same
Spring environment naming and Boot conversion used by runtime, without starting
the application. The CLI reads its process environment, not application profiles
or ConfigData. Validate the whole enabled composition before the first host write.
Use `OPERATIONAL_MIGRATION_DATASOURCE_USERNAME/PASSWORD` only for host Flyway.
When bulk lifecycle is `true`, require explicit
`BULK_MIGRATION_DATASOURCE_USERNAME/PASSWORD` for the Metadata migrator, on the
same `OPERATIONAL_MIGRATION_DATASOURCE_URL` API database; there is no separate
bulk URL or fallback to operational, runtime or control-plane credentials. The
configured bulk expected owner must equal the explicit bulk username. The two
migration usernames may match when explicitly governed, but the operational
migration username must not be a bulk runtime or control-plane role. When bulk
lifecycle is absent or `false`, do not require bulk credentials. Preserve both
passwords literally and reject JDBC URL credential/identity overrides before
bootstrap. Do not use `SET ROLE`, transfer SESSION ownership, infer grants from
HTTP, copy Metadata SQL or perform deployment DDL at startup.

The host Flyway history and Metadata bulk history are separate and not globally
atomic. Configuration validation before DDL cannot prevent a live bulk failure
after operational Flyway has committed. The command must propagate failure after
either phase and must not claim rollout success after only the first one. The
declared BASIC confirmation identity starts deny-only/UNCOMPOSED; installation
does not publish readiness or business authorization. Preserve normal strict
retry behavior without repair/clean fallback.

Prove the packaged entrypoint on an assigned copy-on-write Neon child with the
exact host and Metadata artifacts, direct TLS connection, ordinary non-superuser
operational migration owner, and real ordinary runtime/control identities.
Preserve the SESSION predecessor, `current_user`/owner and mixed host history
under its strict forward; never use SQL repair, `ALTER OWNER` or an expected-owner
override to make it pass. Check both histories, Metadata's physical/catalog/CRC/
ACL validation, no-work repetition and resulting privileges. A Bulk owner with
the privileges admitted by the SDK's V20 gate does not itself prove the ordinary
operational or runtime/control paths. Binding/unit tests and packaged-JAR checks
are complementary; they do not replace invoking the packaged command. Until the
fresh entrypoint, read-only SDK validation and repeat-zero receipts pass on the
assigned child, keep Neon adoption pending. After each authorized Quickstart
main update, follow its automatic Render deploy to a terminal result and correlate
the source commit with the served build and health. An older healthy instance,
or an unchanged application version string alone, cannot certify the new deploy.

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

Keep API and Config datasource properties, Flyway policy, AI provider properties,
RAG/vector-store switches and test isolation explicit. Test profiles may disable
unrelated external services while preserving the host/starter wiring being
proved. Database-backed tests must use their assigned Neon destination; H2 or
embedded/local PostgreSQL is not an admitted fallback. A pure wiring test may
use an explicitly nonconnectable destination only when the whole test proves no
connection is made; it provides no database evidence.

### Pin local packaged-host launch inputs before Java

Inspect the actual launcher before every boot or retry. `run_local.sh` defaults
`ENV_FILE` to `.env.dev`, exports file values over inherited variables, lets Config
fall back to API credentials, and selects a JAR under `target/` when `APP_JAR` is
absent. An executable-permission failure followed by `bash run_local.sh` does not
preserve a selector omitted from that retry. Require an explicit absolute private
env-file path and absolute reviewed `APP_JAR` with its SHA-256 on every attempt;
never recover by loading the default file or relying on an earlier shell export.

Before the JVM starts, use a reviewed fail-closed preparation gate that validates
the env-file/launcher/JAR bytes and starts with a fresh allowlisted process
environment. Pin the intended JDK executable/version/hash and its `JAVA_HOME`/PATH
when selecting a non-system runtime; a clean datasource environment alone does
not prove which `java` executable runs. Reject inherited or file-based indirect
Spring configuration locations/JSON and JVM option overrides that could escape
the assignment. Enumerate every effective JDBC destination, including API,
Config, Flyway and any applicable reader/control pools and fallback relationships.
Match endpoints, database, TLS and distinct runtime/migration/control roles to the
explicitly assigned Neon children before launch; reject missing or unassigned
destinations and unexpected database-bearing variables instead of accepting a
PostgreSQL URL prefix or allowing parent/production fallback.

Exercise the gate offline with execution intercepted: missing/changed private
inputs, wrong endpoint/role, indirect overrides and a mismatched JDK must be
refused before Java. Record safe hashes and assertion outcomes, never env contents,
passwords or tokens. This proves launch preparation, not HTTP health, database
isolation after connection or absence of writes. A private task wrapper is not an
official product API or a correction to the production launcher; do not publish
its temporary paths as a reusable tool. Retain the actual owned process identity
for cleanup. After an unintended boot, stop that process and preserve the incident
receipt and uncertainty: Flyway validation with no new migration log does not
prove that seeds, listeners, recovery or other application paths made zero writes.

## Install the operational SESSION prerequisite

Before an authenticated host proof, inspect `EnterpriseSessionConfiguration`,
`EnterpriseSessionStore`, `EnterpriseSessionLifecycle`, the official
`OperationalDatasourceMigrator` and
`docs/ENTERPRISE-SESSION-OPERATIONAL-PREREQUISITE.md`. The reviewed forward
`V20261022_001__enterprise_session_operational_prerequisite.sql` installs the
existing Store contract on the API datasource, separately from Config Flyway.
Verify the exact source, packaged resource and deployment adoption before use;
local source or offline tests alone do not admit a hosted SESSION or G4 flow.

Run the forward through a distinct, non-superuser operational migration owner
with incompatible writers stopped. The owner needs schema CREATE/USAGE, database
TEMP and ownership of an existing predecessor; because the SQL issues `GRANT
USAGE ON SCHEMA public`, it also needs authority to grant that schema privilege
(schema ownership or the relevant grant option). The ordinary runtime must not
gain owner or schema/database CREATE authority. An existing table must pass the
locked strict catalog, dependency, ownership and effective-ACL checks without
row rewriting, ownership transfer or grant repair. A missing historical Flyway
resource still fails before this forward; do not clean/repair history or recreate
retired bytes from a fixture. `AssignedNeonStores.prepareApiSessions()` and
TESTONLY schema snapshots prepare isolated fixtures, not this installation.

Validate the packaged migration and repeat-zero on an exclusively assigned
Neon child through the required `AssignedNeonDatabase` path, with distinct real
owner and ordinary-runtime identities. Prove Store/lifecycle issue, subsequent
read, selection CAS and revoke through runtime, exact column-write denials,
compatible predecessor preservation and rollback of drift negatives. Record
source/resource hashes, TLS client evidence and raw result privately. A
same-resource adversarial rollback is not another full migrator run; an offline
pass or historical remote result is not fresh admission. If a committed forward
is followed by a failure, preserve that cut and reconcile rather than reset
history or silently retry. Authenticated HTTP, enterprise membership composition,
full gate and deploy remain separate proofs.

For assigned Neon contention proofs, prepare physical TLS connections and
observer statements in fixture setup before the bounded business window. Keep
the real ordinary-role observation, execution lifetime at most 30 seconds and
the revoker's 500 ms observation assertion unchanged; setup moving outside
those windows cannot weaken their measured work. Release gates and sessions,
cancel workers and confirm termination before closing writer-owned connections
or dropping the assigned database. On nontermination or cleanup failure, retain
the exact lease and journal for reconciliation, including after timeout or
interruption; do not turn cleanup into a passing business result.

The historical `scripts/workspace/Invoke-PayrollReactiveDeterminationHostedProof.sh`
is now a fail-closed entry point: it exits 2 before any provider call, even with
the former valid confirmation. Its retired Render PostgreSQL topology used the
owner as application runtime. The previous implementation remains in Git history
for diagnosis, not as a standard gate or main deployment path. Do not revive it
with an environment flag; requalification requires a separately governed,
assigned Neon proof with distinct migration-owner and ordinary-runtime identities.

## Qualify and provision the existing enterprise directory

Inspect `EnterpriseRuntimeProperties`, `JdbcEnterpriseMembershipSource`, the
operational migrator, `EnterpriseMembershipDirectory`,
`EnterpriseMembershipProvisioningCommand`, `scripts/workspace/Start-ApiRuntime.sh`
and `docs/ENTERPRISE-MEMBERSHIP-OPERATIONAL-ACTIVATION.md` together. Keep installing
storage, configuring public presentation and provisioning revocable membership
separate. Structural migrations must not seed subjects,
capabilities or validity. The existing-directory activation does not deliver a
fresh directory installer or authorize new DDL: preserve the admitted predecessor.
Presentation and `AUTH_*` technical accounts cannot substitute for persisted grants.

Before editing deployment settings, privately inventory their effective sources,
including `SPRING_APPLICATION_JSON`; preserve valid managed reference keys rather
than regenerating them because a catalog is empty. Compare the actual predecessor
catalog and effective ACLs with the candidate. Preserve directory FKs, constraints,
column types/defaults and the innocuous lock anchor even when there are no rows.
Reject an unsupported predecessor; do not convert it to a TESTONLY fixture schema,
drop dependencies or widen runtime UPDATE to make installation pass.

Qualify the exact image/JAR and deployment revision before an administrative job.
Use the existing operational migration lane with its segregated owner and strict
history. Resolve history by complete typed tuples, including legitimate `DELETE`
markers from the governed history-recovery path; a version alone does not identify
a pending/applied SQL migration. Do not delete markers, reconstruct retired SQL,
run `repair`/`clean`, or invoke demo fixtures to manufacture an acceptable history.

The packaged `/app/bin/praxis-enterprise-membership-admin preflight` is read-only:
use official Flyway validation/info to interpret history and report pending versions,
not to run migrations or manually reconstruct `DELETE` semantics. After the normal
deployment migration lane, `plan` and `apply` require no pending migrations. Review
the private plan, then use `apply --expected-plan-sha256 <approved-64-hex-digest>`
only with the same qualified artifact and stable inputs. The preflight fingerprint
is not an apply authorization. Consult the activation guide for exact environment
names; the command does not resolve Spring ConfigData/JSON login precedence, so
privately attest its subjects against the actual configured authentication source.

This command provisions only `lab-a/lab/org-1`: one tenant, one organization and
two memberships atomically, AUTHOR with `ui.authoring.configure` and PUBLISHER
with `ui.layout.publish`, empty groups and NULL sector/profile. The approved inputs
include a reference UUID, distinct membership UUIDs and an explicit UTC start;
validity is ninety days and application must occur while current and within the
first twenty-four hours. Preserve the absence precondition for the target directory
rows and either subject/UUID, history-before-directory lock order, and the reread
of the artifact/database/runtime/catalog/history-bound fingerprint before writes.
Expected-absence compare-and-set is not an upsert or a general grant replacement API.
Do not infer authorization to renew, expand or replace existing memberships from
permission to install storage; no restart seed or blind retry after lost output.
Keep approved input/receipt custody and reconcile an uncertain commit privately.

Keep owner datasource credentials available only to their administrative entry
points, outside the Java application process. `/app/bin/praxis-api-start` removes
`OPERATIONAL_MIGRATION_DATASOURCE_*` and `BULK_MIGRATION_DATASOURCE_*`; this does
not sanitize Config credentials, aliases, `JAVA_OPTS`, JVM flags, JSON or mounted
files, nor remove secrets from the deployment provider. Verify the runtime login
and remaining credential sources without printing values; claim only that boundary.

Reuse valid focused source/unit evidence and report its limits. A mocked plan/apply
test does not prove PostgreSQL locks, Flyway, grants or a live deployment. Do not
repeat Neon campaigns when the authorized cut explicitly excludes them; retain
that boundary and qualify the separate real operational action, readback and
SESSION/context/HTTP proof. Health UP, a successful predeploy or a saved environment
setting alone does not establish enterprise availability or the Hero journey.

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

### Prove A Minimal Corporate Page Publication

For the Config page contracts, inspect `QuickstartPageConfiguration`,
`QuickstartPageHost`, `QuickstartPageDocuments` and the current
`docs/CORPORATE-PAGES-PILOT.md`. Reuse Config creation/lifecycle/runtime owners;
explicitly import the pilot rather than creating parallel writers or activating
production memberships through component scan. Follow
`praxis-config-runtime-persistence` for canonical page/group integrity.

Pin the compatible public Config coordinate in the host POM without an override.
Verify Central JAR/POM checksums and byte equality with the packaged nested JAR;
private-GAV evidence remains private even when its sources match the release.
Reuse unchanged owner concurrency/rollback proofs with their exact source and
limits, then execute the focal host HTTP case on assigned isolated Neon.

`QuickstartPageCorporateHttpNeonTest#nativePageCreatePublishAndReadWithCurrentSessions`
proves the smaller native page path: two current SESSIONs with separate author
and publisher memberships, creation/draft, 404 before publication, revision,
assignment, freeze, submit, approve and head publication. Require the published
route/document/head, authorized 200/304, an independent ordinary-runtime read of
the committed head, logout and retained-SESSION rejection. Before accepting the
host providers, prove publisher-without-authoring creation denial, another tenant
receiving 404 despite a valid published ETag, and current membership revocation
receiving 403 rather than 304 with that ETag. Owner-only revocation belongs to the
assigned test fixture, never runtime grant repair. Keep the existing
budget, locks, CSRF and authority rechecks; six publication commands have separate
budgets, not one combined allowance. Preserve a failure before considering a new
attempt; cleanup does not establish rollback.

The seed has one empty Form and no navigation bindings; this case does not prove
business submission, menu/group publication, copy or browser rendering. A page
with no navigation bindings need not publish an unrelated group first. Those
later host surfaces require their own appropriate evidence before claiming them
operational; never fabricate a group head or reuse an old authorization result.

### Accept The Shared Page Deadline And Rollback

Before accepting the page pilot after Config #521, inspect the owner's
`P3C-VALIDATION-BUDGET-521.md`, the host guide and the exact current harness.
Keep forty seconds per initiating operation, including its reserved draft,
receipt, lineage and commit callbacks; six separate publication HTTP commands
still own six separate attempts. A blocked extension can return after the deadline,
but its result must be rejected without executing later callbacks or committing.
An expiry observed only after an actual database commit means uncertain delivery:
reconcile with the same creation key; never report that committed write as rollback.

After focused clock/authority tests, require assigned-Neon creation/publication/read
and a controlled failure after writes are staged but before commit. Observe actual
transaction rollback and absence of the affected catalog, draft, metadata, head and
creation-key records, as applicable, using an independent ordinary-runtime connection
before fixture cleanup. Logout and dropping test databases do not prove rollback.
Preserve failed receipts and record source, artifact hashes, roles, timings and
cleanup separately. Private-candidate success does not establish complete public
HTTP acceptance. Resolve and attest the officially published compatible artifact;
by default, run the appropriate consumer gate before claiming that acceptance.
Unit success alone does not close Neon, integration or release acceptance.

An explicit human decision may accept technical integration with a documented
availability limitation instead of repeating a campaign. First require independent
review of unchanged production-source equivalence, public artifact/nested-JAR custody,
focused consumer tests and the existing complete isolated-Neon functional proof.
Preserve every public negative and identify its exact failed phase; do not rename
private evidence as public success, infer rollback from cleanup, or attribute the
failure exclusively to topology without measurements. Record the decision, scope,
residual risk and unproved deployment/browser/performance claims in the host guide,
plan and tracking issue. This accepts a code increment, not production qualification.
Do not use this path to waive an unexplained integrity/security failure, weaken
current authority, alter the monotonic operation budget or bypass branch protection.
After an approved decision, do not repeat invariant suites or require a new executor
merely to advance unrelated functional adoption.

### Run The Fixed Page Focal Gate Without Publication

Inspect Quickstart `.github/workflows/publish-public-release.yml`, its same-source
`ci-java.yml`, `scripts/workspace/corporate_page_focal.py` and
`neon_gate_assignment.py`. The manual `page-focal` cut requires a branch dispatch,
`create_tag=false` and `release_gate=false`; it runs only
`QuickstartPageCorporateHttpNeonTest#nativePageCreatePublishAndReadWithCurrentSessions`.
Require the clean host checkout and assignment source SHA to equal the workflow's
exact SHA. This seam is implemented; complete public HTTP acceptance requires its
own passing reviewed receipt. Keep that result distinct from any explicitly approved
technical-integration decision described above.

With empty `page_config_ref`, consume the host POM's public Config pin without an
override or fallback, attest Central JAR/POM checksums and nested-JAR equality.
An optional candidate must be an exact full commit SHA in the fixed public Config
repository. Clone it privately, verify clean source, use a unique private GAV and
fresh isolated Maven repository, and attest that only project/version changed for
installation before restoring the canonical POM and clean source. Retain Config
commit, whole-tree and `src/main` tree identities plus canonical/private/installed
POM and JAR hashes. Matching production trees supports comparison with a later
release; it does not turn private bytes into public-artifact adoption.

Package and attest before injecting `CORPORATE_PAGE_NEON_ASSIGNMENT` through the
existing materialization gate. The coordinator exclusively assigns the isolated
Neon child, lease and resource root; never reuse or replace the basic-proof secret,
fall back to another assignment, or extend the lease silently. Keep the same forty
seconds, canonical checkpoints and two fresh authority observations per admission,
without authority caching. The Ubuntu remote runner is a topology, not evidence
of geographic proximity, browser behavior or a local latency/SLA guarantee.

Retain only the allowlisted custody, functional, assignment, test-results, cleanup
and resource-ledger JSON receipts. Require creation/publication/read, conditional
read, independent head, precommit failure, independent rollback observation,
same-key retry, other-tenant denial and current-revocation denial. Project only
closed phases/statuses/timings, fixed-route HTTP status/body hash, known error codes
and SPI aggregates; raw logs, reports, headers, environment and credentials stay
private. A hash or prior phase does not explain a later failure. Raw runner logs
are ephemeral; preserve failed sanitized receipts before diagnosing a new attempt.

The 25-minute job limit does not guarantee the harness cleanup completes after a
kill or runner loss. Verify cleanup separately; if incomplete, the coordinator
must reconcile the assigned resource root against the private journal and sanitized
resource ledger, removing only resources whose ownership is established. Never
clean a parent/shared branch or infer ownership from a broad prefix alone. Remove
the dedicated repository secret after the run; retain controlled private recovery
custody until reconciliation finishes. Cleanup is distinct from pre-cleanup rollback
proof. This gate neither publishes a release nor accepts menu/copy/browser paths.

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

| Changed surface | Minimum focused proof |
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

Use Cockpit, HTTP corpus, and published-host checks only after focused proof is green. They are release/downstream evidence, not the ordinary development loop. State exactly what did not run and why.

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

## Select an Isolated Authorized-reader Composition Cut

For the candidate `AUTHORIZED_READERS` harness cut, inspect
`scripts/render-composition-proof/{package,inputs,run,controls,boundary}.py`,
`RenderCompositionNeonFixture`, `RenderReaderCaptureOracle` and the selected
`RenderCompositionNeonSmoke` method. Metadata owns the two authorized proposal
facades; this test-only selector changes neither their contract nor their budgets.

Keep `FULL_COMPOSITION` available as its separately pinned full confirmation/replay
proof. Require the closed workflow selection to match the envelope and BUILD receipt
before connecting. BUILD uses accepted public artifacts without a dependency override,
credentials or SDK source build; collect the exact XML counts of the selected guards
and pin the launcher, classes, resources, nested dependencies and source manifest.
A pending public artifact or candidate compilation cannot authorize RUN.

For FULL's multiple explicit targets, distinguish the assignment's ordering from
the SDK's canonical intent ordering. Derive expected result/manifest/receipt
ordinals through the resolved public `BulkIntentSnapshot.uniform` and identity
codec, rather than assuming numeric ID order or copying a comparator into the
host. With integer IDs 41, 43 and 355, public171 canonizes 355, 41, 43. Preserve
exact identity, count, version and receipt-to-manifest checks; do not replace
ordered equality with set equality or use the observed result as its own oracle.
Reproduce an oracle mismatch against the pinned public JAR before changing the
test. Persisted executable previews without a new execution do not prove HTTP
preview, confirmation or replay; retain the failed run and its diagnostic limits.

Keep the secondary Python AFTER verifier separate from that Java ordered oracle.
Validate a bijection between assigned IDs and saved manifest ordinals, then bind
each receipt's ordinal to the exact manifest digest and opaque version bytes;
retain deadlines and exact ID-keyed physical domain changes. Do not convert an
opaque version into a numeric entity version or index numeric assignment order
by ordinal. Reject boolean IDs/ordinals and duplicate, missing or foreign IDs.
This relational check does not replace Java's canonical ordered proof or authorize
a coordinated manifest rewrite. A passing Java journey followed by FAILED_AFTER
remains a failed full run. Read back protected durable state before diagnosis;
controlFreshAfter=false may be an unassigned default after an earlier assertion,
not proof of expired control evidence. Preserve the failed receipt and review the
verifier correction before a new isolated official proof.

Select the codec's closed transport profile from the trusted workflow cut before
decoding, never from envelope contents. Encode and verify the exact-byte roundtrip
with that same profile; preserve existing default bounds and all rejection checks,
with no enlarged fallback. Measure the complete real envelope, including every
attachment, against the canonical codec limits before secret injection; synthetic
size tests are not that measurement.

When cloning an already provisioned child, retain original Main command/input/receipt
bytes, source and binary provenance. Require reviewed administrative source/resource
and public-JAR equivalence for the exact current artifact delta, plus current child identity and
resource receipts; do not label inherited commands as new executions. Read the current
`reader-artifact.json` and accepted equivalence receipt: the public171 comparison is
administrative only, with `wholeRuntimeEquivalent=false` and
`fullClassTransitiveClosureEqual=false`. Its runtime changes are not merely reader-only;
historical Main receipts remain unchanged and do not prove current HTTP composition.
Provision fresh
cursor material and its own finite ledger without resetting historical quota. Bind the
current complete domain rows, target/version and effective evaluation intent separately
from historical assignment; derive HTTP expectedVersion from the real strong GET ETag.
Counts, generations, roles, lease and snapshot values belong to that reviewed binding.

Observe the verified `ready.json` (source/JAR/PID, auto-started worker and physical
datasource profiles) and listener200/503 before issuing the explicit command. The
reader cut permits only RECONCILE; FULL uses its existing SUSPEND/PUBLISH CAS. Require
health200 after that command and before evaluation, within the same monotonic240s
startup deadline. Listener availability alone is not readiness, and publication does
not renew the deadline. Keep runtime readiness and worker budgets unchanged.

For host properties, use the existing helper that permits only the exact
`app.security.enterprise.presentation.contexts` key with an empty array alongside
scalar values. Reject other structured values and nonempty catalogs; never fabricate
memberships to obtain context.

Log in, reconcile the exact existing READY/publication pair, verify health200, evaluate one explicit
target, then call the real proposal and first results-page facades. Do not confirm,
replay, publish, suspend or send worker/Main commands in this cut. Independently compare
all named full BEFORE/AFTER sets, including after startup or reconcile failure. Before
evaluation require exact preservation; after attempted evaluation allow only the bounded
canonical six-store capture footprint and pending allocation, preserving all historical
rows and zero domain/execution/receipt/admission/slot/occupation effects. Validate the
proposal, fingerprint, manifest, preview and version relationships without inventing
a second cryptographic-digest implementation. Export only the closed bounded reader
failure projection; raw logs, sessions, HTTP and snapshots remain private.

Track every attempted login. Capture the issued SESSION token in memory immediately
after its response, then persist SESSION/CSRF in a private0600 file for secret scanning
before further body/status/session assertions. An IO failure must retain the in-memory
token for cleanup. In finally, attempt every owned session's logout204 with its own
SESSION cookie and CSRF, then GETsession401 using the same retained Bearer token with
no cookie jar; cookie removal is not proof.
Preserve the primary failure and record secondary cleanup failures. Uncertain issuance
or missing revocation evidence cannot produce CLOSED merely because the host stopped.
Keep bounded attempted/issued/revoked/tokenDenied/closed evidence private; zero sessions
before login may be clean but cannot establish a successful two-actor journey.

Offline guards and artifact checks prove preparation only. A passing same-object Neon
receipt certifies the selected two readers, not full confirmation/replay, scale, Render
or resolution of an earlier failure. Until that receipt is accepted, keep the reader
cut remotely pending; failed cleanup or malformed diagnostics cannot produce PASS.

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

For accepted units executing outside HTTP, use
[bulk-off-request-authority.md](references/bulk-off-request-authority.md).
Reuse the persisted kernel unit, current DB grants and one admission body; retain the
physical grant/domain transaction and receipt-first replay. Do not propagate JWT,
browser session or request context, expose an arbitrary subject factory, or infer
public ASYNC from a private worker. Verify artifact/baseline compatibility before
calling a candidate path adopted; focused proof on a compatible parent is qualified.

For bulk unit admission, inspect the Metadata-owned published-photograph path before adding a host workaround. The durable kernel owns the physical unit transaction and receipt; host admission callbacks run under that unit, and operational datasource reads/writes use its attested writable connection. Policy/grant authorities may use independent databases; their decisions must complete before the kernel rechecks control and invokes domain mutation. Published structural reads must retain the global SHARE on the same attested connection, with no cache lock or `REQUIRES_NEW` inside the unit. Readiness and capability/action response frames remain outside operational transactions. Receipt replay must precede new-mutation gates and must not invoke those callbacks again.

Prove uniform and per-item HTTP+PostgreSQL flows against the exact candidate artifact with the unchanged execution budget: positive domain/audit/receipt commit, stale-target denial without mutation, authorized delegated reads, unauthorized reads, and replay without another domain call. A getter that copies only its requested group does not prove the complete multi-group resolver fits the budget. Record source/artifact hashes and admission reasons; do not raise timeouts or claim adoption from compile-only/local-override evidence. Published dependency validation without an override remains a separate release/adoption gate.

For `MissionParticipantBulkCanonicalContract`, resolve the trusted registered MVC refs
and check declared IDs, methods, resource and group, capture one exact group snapshot,
then call `requireResourceOperations` for the complete batch BEFORE resolving the three
bodies with `requireResourceRequestBody(resourceKey, CanonicalOperationRef, TypeFactory)`.
That overload requires a snapshot-validated ref. Preserve full generic DTO resolution,
returned-ref equality, cross-group operation-ID collisions, fields/revision evidence and
the published scope's two durable guards. Reusing this immutable structural photograph
is not permission to cache grant/policy decisions or remove the independent pool reserve.
Prove order and fail-closed behavior with the real resolver and shared BASIC/ATOMIC paths;
reduced collision-domain scans or passing SQL fixtures do not certify the full five-second
host unit. Historically, the public Metadata `8.0.0-rc.162` SDK gate passed on isolated Neon,
including the deadline SQL oracles and commit/receipt/replay. That SDK evidence does not
itself accept host HTTP9 or deployed Render H5. Each adoption requires independent
consumer receipts bound to its exact source, public artifact bytes and deployment;
do not reuse an earlier consumer receipt as acceptance. Prove commit/read/replay
through both gates before claiming operational acceptance.

For ordered-batch adoption, reuse the Metadata `BulkOptionalPoliciesNeonTest` on its
assigned Neon branch and ordinary runtime/control identities. Use a finite test-only
latency profile on the same physical unit connection: record JDBC executes, real SQL
time, imposed delay and the original live remainder. Include the prepare marker UPDATE
whose `RETURNING` supplies deadline/clock; its pre-execute monotonic anchor consumes
transport, decode and close without a tail clock read or deadline renewal. Fixture
checkpoint counts are instrumentation of that exact test, not a public count contract
or SLA. A per-execute floor includes real
time already spent; do not add that delay blindly or instrument the product. Before
the unchanged independent Config policy pool reserve, require a remainder strictly
above 2.1 seconds, then continue through real commit and independent domain/receipt
readback plus replay without a second effect. Synthetic host cost and JDBC counts are
not wire RTT, a Render SLA or complete host evidence. Preserve five-second/one-second
bounds; do not accept a candidate from reaching admission or a passing mock alone.
The public Metadata `8.0.0-rc.164` SDK gate passed this physical Neon profile, including
the pre-policy reserve, commit/readback/replay and the four ordered-unit markers.
Require separate exact-artifact HTTP and deployed Render proof before claiming adoption.

## Bound BASIC Proposal Preparation and Capture Separately

For `MissionParticipantProposalService`, distinguish preliminary authenticated
admission/readiness, preparation, and the writable capture unit. Inspect the exact
host source before diagnosing an evaluation 503: a pool-reserve guard may reject
before opening SQL, after the same clock was consumed by readiness composition.
Correlate the request stage, monotonic remainder and final durable state. A local
instrumented reproduction does not establish the cause or timing of a prior CI run.

Keep preliminary authorization before expensive readiness composition, and readiness
before preparing the intent. Give preparation a finite deadline. Start the capture
unit's deadline once after preparation; share it through pool acquisition, writable
RR storage, retained current-grant authorization, projection and precommit checks.
Do not renew it inside callbacks. Preserve the prepared proposal's created/expiry
timestamps and the exact readiness expectation: locked checks must reject a changed
publication and require current authorization and sufficient target coverage. Do not reuse discovery response
frames as a capture authorization cache.

Use the host's `QuickstartUnitBudget.captureTransactionTimeoutSeconds` for the
BASIC capture transaction, not the five-second `queryTimeoutSeconds` cap intended
for individual protected reads. The capture calculation reserves 1.1 seconds for
pool acquisition/scheduling and floors the remaining aggregate allowance: a fresh
eight-second capture unit gives Spring six seconds. Preserve the monotonic
eight-second deadline, the fixed proposal validity and the final precommit check;
do not renew the allowance after blocking work. Host query caps stay at five
seconds. SDK statements inherit the remaining Spring transaction deadline and
retain any smaller SDK limit, so this correction does change their possible
transaction-derived allowance. Do not describe every SQL timeout as unchanged or
infer the cause of an earlier opaque storage failure from this correction.
Inspect `MissionParticipantProposalService`, `QuickstartUnitBudget` and their
focused tests. Prove Spring accepts work after five seconds within the six-second
transaction, rejects an expired six-second transaction even with aggregate time
left, and rolls back at the eight-second aggregate deadline. A mocked connection
with the real Spring timeout resource proves host arithmetic/wiring only; require
the exact corrected artifact's HTTP persistence/read/replay on isolated Neon and
keep the deployed Render HTTPS proof separate. This does not change the SDK
execution-unit or ATOMIC budgets.

Verify the implemented limits in source and size the HTTP observer for the complete
sequence, including the authorized read after commit. A sum of phase limits is not
an enforced global deadline. Distinguish this host preparation boundary from the
unchanged SDK mutation-unit budget; the BASIC change does not certify ATOMIC.
Prove phase isolation, one capture clock, expired capture denial and preservation of
expectation/validity with focused tests. Require an isolated Neon evaluation that
returns its persisted proposal through the authorized reader, with unchanged
domain/control state. Prefer a focused probe; an explicit stage of the existing
remote HTTP journey may provide this proof when a local probe stops upstream of
the changed path. Keep that local failure recorded as inconclusive for the patch,
not passing. Investigate any new failure before another run. Preserve any proposal
produced by an uncertain response; do not automatically retry or reset it.

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

For the candidate uniform ASYNC beta migration, follow
[the host adoption procedure](references/bulk-off-request-authority.md#candidate-uniform-async-host-adoption).
It preserves the operation identity, retires new uniform SYNC/QUERY admission and
retains authorized historical reads/replay. Earlier BASIC receipts remain historical;
the current Angular SYNC consumer, provisioning, HTTP and deployment have separate gates.

## Basic Bulk Publication Admission

Inspect the host's `MissionParticipantBulkPublicationController`, original-JSON
`MissionParticipantBulkPublicationShapeAdvice`, explicit SecurityConfig POST matchers
and `docs/operational-bulk-publication.md`. Metadata owns publish/reconcile/suspend
and durable CONTROL/global publication semantics; the host supplies one fixed basic
operation identity and the current server-configured binding. Do not create a second
registry, annotations or lifecycle implementation in the host.

Resolve each distinct current administrative permission, complete the separate grant
read before SDK control locks, and recheck the exact active SESSION. Never retain a
grant lock while calling lifecycle, infer authorization from JWT ADMIN, or use internal
delegation in this administrative entry. Publishing structure does not grant business
mutation or scoped target access. Suspension affects the global photograph of the logical deployment bound to the namespace.

Require exact integral `expectedGeneration`: publish/suspend permit 0 through MAX-1;
reconcile permits 1 through MAX. Reject duplicates/coercions/extras/trailing JSON. Do
not retry or rebase mutating commands on 503: it does not prove rollback or failed
durable publication. Reconcile only an already confirmed READY publication at its
exact generation. Identify an authorized protected evidence reader before administrative commands or basic operational
availability acceptance; fixture SQL and guessed zero are not an operational recovery procedure.

Prove the three HTTP commands with persisted SESSION/current grants/owned PostgreSQL,
stale CAS, revocation and delegation negatives, business-permission separation, and
served typed OpenAPI tied to the durable global generation/digest. Preserve distinct
MVC mocked-boundary, server CORS/CSRF, real HTTP/PG, final public JAR/loaded origins,
full bootstrap and deployed Neon/Render evidence. Combined accepted focal cases do
not erase a failed broader verify. Reuse unaffected valid cases; do not repeat them
merely to produce a new aggregate count.

For the packaged BASIC/READY host proof, inspect the
`quickstart-basic-ready-neon` cut in
`.github/workflows/bulk-reference-consumer-proof.yml` and its
`BulkBasicReadyPackagedNeonProof` test. Dispatch from the reviewed branch or tag
ref resolved to the full candidate SHA, and require `GITHUB_SHA`,
`GITHUB_WORKFLOW_SHA` and `CANDIDATE_SHA` to match that commit; the historical
Docker/local-Postgres lane is separate. Require the packaged public Metadata
`8.0.0-rc.164` and Config `0.1.0-rc.162` dependencies, unchanged source and JAR
bytes, and a current exclusive control-plane assignment for the API and Config
Neon child branches.
Keep their child-only credentials in the runner's private mode-0600 input, never
in the checkout or uploaded evidence.
Use one reviewed artifact expectation for both packaged-JAR and JVM class-origin
checks, and validate it against the host POM during dependency adoption. On host
shutdown, retain bounded log/classload hashes and termination evidence even when
origin validation fails; preserve the primary failure and release the owned process
reference without turning an origin mismatch into PASS. Test this failure path offline.
If the public scanner rejects evidence, keep its result failed. A separate closed
`REJECTED` scanner receipt may expose only fixed checkpoint/component names, bound
source/run identities and hashes, plus failed-proof context that already passed
schema and raw/decoded secret checks. It is diagnostic metadata, never accepted
HTTP or backend proof. Do not upload raw logs or rejected sidecars; if privacy inputs
or fallback validation are unavailable, emit no fallback artifact. Diagnose the
recorded rejection and correct its cause before rerunning the remote journey.

For lifecycle OpenAPI on Render, merge `springdoc.cache.disabled=true`
and an empty `app.openapi.internal-base-url` into the existing
`SPRING_APPLICATION_JSON` overlay, then check the served document after READY.
Inspect Metadata's `docs/spec/BULK-OPERATION-LIFECYCLE.md` and
`docs/technical/AUTO-CONFIGURACAO.md`, plus the host's
`src/main/resources/application-prod.properties` and README: its shared
`APP_OPENAPI_INTERNAL_BASE_URL` also feeds AI schema/capability URLs. Do not clear
that shared environment variable to fix the lifecycle lookup.

When diagnosing a publish 503, distinguish the control/runtime transaction deadline
from fresh OpenAPI capture. Inspect the exact released
`OpenApiInternalRestTemplate`, `CachedOpenApiDocumentService` and
`OpenApiDocsSupport` sources and the host's
`docs/operational-bulk-publication.md`. A response timeout while the root document
is still being generated is not evidence of a database privilege failure. The
host configures `praxis.openapi.http.read-timeout=60s`; this also affects ordinary
internal OpenAPI reads. Governed capture still uses the lesser of that response
budget and the remaining aggregate `praxis.openapi.bulk-composition-timeout`
(SDK default 60s). The Quickstart configures that existing composition property
at 180s for its complete root, groups and swagger-config capture. This property
also governs other composition scopes, including lock acquisition, descriptor
composition, installation and reads; it is not a single whole-publish deadline.
Do not renew the aggregate budget per document, weaken transaction deadlines, or
remove schemas/advice to make capture pass.
Render cold capture exhausted the previous 120s aggregate at group `operations`
after a 42.804s root and sequential groups. The host now budgets 180s for the
existing complete composition scope and observes startup reconcile for 240s,
retaining 60s per response and unchanged SQL/control deadlines. Keep the failed
120s cut separate; configured budgets alone do not certify cold recovery. Require
a successful complete capture and actual restart on the deployed source.
The startup observer remains single-shot: an uncertain timeout cannot trigger retry.
The administrative proof client allows
180s to observe the lifecycle's distinct stages, while the diagnostic validator
accepts a window up to 240s; neither changes SDK semantics or permits retrying an
uncertain publish. Confirm both settings in the exact deployed host artifact and
require full cold capture/READY/HTTP evidence before calling the sizing sufficient.

Cold reconciliation compares the exact producer response bytes with the durable
publication digest. The reference host enables the existing SpringDoc
`springdoc.writer-with-order-by-keys=true` so map/property insertion order does
not change that photograph across JVMs. Inspect SpringDoc's actual OpenAPI writer
and test typed OpenAPI/Schema documents with nested extension maps in opposite
orders; verify identical sorted bytes while preserving array order and values.
A generic map serializer alone does not prove the production writer. Do not
normalize only the digest, ignore differing fields, or replace a stored digest.
Changed producer bytes require a new authorized publication on the applicable
baseline. Require cold-node reconcile in the real HTTP journey; an offline
ordering test does not certify the whole READY flow.

For this journey, use the bounded code-only terminal event emitted by the host's
publication controller, not mass `JavaExceptionThrow` recording. Collect the five
fixed positive administrative stages: initial PUBLISH, warm RECONCILE, SUSPEND and
republish on host 1, then cold RECONCILE on host 2. Keep each stage in a separate
allowlisted sidecar, including successful commands, so a later failure does not
lose the preceding timings. Expected negative requests such as stale CAS remain
outside these windows. Bind every sidecar to its closed stage/command pair,
process, private log offsets, time window, reached prerequisite, source and host
JAR hashes. A sidecar cannot borrow another stage's or host's log or a phase that
was never reached. These windows do not cover other HTTP calls or assertions.
For failures outside those windows, retain at most eight ordered primary test
frames from the harness's exact allowlisted classes, bound to the source SHA.
BASIC permits `BulkBasicReadyPackagedNeonProof` and `BulkBasicReadyNeonFixture`.
FULL permits `BulkBasicReadyPackagedNeonProof`, `RenderCompositionNeonFixture`,
`RenderCompositionNeonSmoke` and `RenderCompositionMultiTargetOracle`.
Project these existing private frames
into the closed sanitized receipt before runner cleanup removes private inputs.
Export only class, bounded method identifier and line; never messages, file
paths or cause/suppressed graphs. Empty or absent frames do not prove a cause, and
a test call site identifies where the assertion failed, not the SDK failure cause.
The defensive projection must preserve the primary test outcome and pass the same
closed-shape and raw/decoded-secret checks as the receipt.
For BASIC evaluation, collect a separate bounded host scope for the same request,
process and exact source/artifact. Retain the first availability failure observed
at the host interception point before safe wrappers replace it, with monotonic
phase intervals and the existing reader outcome. Diagnostics must not add budget
getter calls, grant/policy reevaluation or storage probes. When a storage or reader
boundary hides the origin, retain `originLost` and `opaqueBoundary`; the boundary
and host call site do not recover an SDK exception or establish SDK causality.
`commitAcknowledged=false` means no acknowledgement was observed, not rollback;
confirm durable proposal/control/domain state with protected read-only readback.
This scope supplements the five administrative windows and preserves the primary
test-frame limits; it must not change the original HTTP outcome or work.
For BASIC confirmation ending in COMMON_GOVERNANCE_UNAVAILABLE, inspect the host
admission callback before its exception is discarded into the SDK reason. Retain
the first failure in memory during the callback; build the graph/JSON and emit
only after SDK advance returns or throws, outside its transaction. Collect one
code-only ADMIT_BASIC event without domain/request identities, with fixed flat
phases CONSTRAINT, CONTRACT_INPUT, CONTEXT, LOCK, AUTHORITY_POLICY and
RECHECK_PREPARED. Bind the initial positive confirmation to its separate
confirmation-diagnostics.json window on host 2 after cold RECONCILE, not to an
evaluation or publication window. An admission event may accompany HTTP200/202
or HTTP503 if the SDK fails afterward. Event outcome STOP is the callback
decision, not proof of durable STOP, commit or rollback; durable STOP and zero
receipts do not identify the discarded exception or its historical cause. Keep
first-failure provenance, nullable SQLSTATE and explicit originLost/opaqueBoundary
when wrappers hide the origin. Add no budget reads, SQL or repeated authorization
work; preserve deadlines, locks, SQL timeouts and returns. Graph/JSON/sink failure
must preserve the original advance result or Throwable; use protected readback
for durable execution, receipt and domain evidence.

For off-request ASYNC admission, inspect
`MissionParticipantExecutionService.createUnitCallbacks`,
`BulkAdmissionDiagnostics` and the released SDK's `BulkDurableWorker.executeOne`.
The callback factory runs inside the unit transaction, after receipt-first
preparation; its cleanup runs after `executeUnit` returns or throws. Allocate
only the bounded in-memory collector in the factory and emit the distinct
`ADMIT_ASYNC` projection from cleanup outside the transaction. The synchronous
collector does not propagate to a worker thread. Keep JSON initialization and
serialization inside the protected emission path, clear thread-local ownership
on construction failure and cleanup, and preserve the primary outcome when the
diagnostic sink fails. Do not add SQL, budget sampling or authorization work.
Prove these boundaries with focal tests, then exercise the actual worker on an
assigned isolated Neon branch; proposal-reader success alone does not cover it.

After confirmation202 followed by an execution-reader503, retain the exact
execution identity and inspect durable state before another command. The reader
failure and an admission STOP may have different causes. Internal
`UNIT_IN_FLIGHT` is projected as public `RUNNING` unless cancellation was
requested, when it becomes `CANCEL_REQUESTED`; do not broaden the HTTP oracle
from a storage row. A durable `STOPPED` execution cannot resume processing.
Preserve its receipts, allocations and history; a later identity replay cannot
turn a zero-effect failed intent into positive execution proof. Diagnose and
validate the correction before a separately identified new intent.

For execution-summary/results failures, first inspect the exact candidate's
`BulkAuthorizedExecutionReader`, `BulkAuthorizedExecutionResultsReader` and
`BulkReadFailureDiagnostics`. Proposal-reader diagnostics do not establish execution
coverage. Reuse the private bounded collector at the existing sanitization boundary;
record only references inside the owned snapshot and emit after its outcome is
selected and its transaction ends. Preserve protected denials, invalid cursors and
public states. A caller transaction may resume, and synchronous logging can still
add latency; do not claim globally transaction-free or latency-free emission.
The FULL harness must collect that closed projection in its failure cleanup, with
matching Java/Python enum validation and exact source/JAR binding. Empty diagnostics
are not success. A durable COMPLETED row and one effect after a polling503 establish
the committed outcome, but do not prove terminal HTTP, results or idempotent replay.
Keep those acceptance steps pending rather than retrying with a new identity.

When `SNAPSHOT_TRANSACTION` fails in the SDK's native RR/RO guard, a 503 or
`IllegalStateException` does not identify a timeout or the mismatched column.
Inspect the exact driver, JPA/JDBC transaction manager and pooler path; observe
the original guard's closed values without inserting a diagnostic SELECT before
it. A single successful read is inconclusive about an intermittent failure.
Keep diagnostic prewarming outside the measured transaction explicitly separate
from full-host evidence. A controlled initial READ COMMITTED state can prove an
owned-transaction setup correction, but is not a reproduction of the historical
failure. Require original deadlines, rollback/closure, ordinary runtime identity
and exact source/artifact binding. Adopt the correction through the canonical
Metadata artifact, then prove the full HTTP journey and persistence on Neon;
neither the diagnostic nor a structural fix alone accepts a new Render deploy.

Export only the closed diagnostic projection: class/method/line, nullable SQLSTATE
and bounded cause/suppressed references, never throwable messages, SQL or request
data. Each primary/cause/suppressed graph node must include `sqlState`: only a
SQLException's SQLSTATE matching five ASCII characters `[0-9A-Z]{5}`, otherwise
`null` for non-SQL exceptions, absent or invalid values. SQLSTATE categorizes an
observed failure; it does not prove the emitter, query or historical cause. Keep
existing graph limits and privacy checks; never inspect server-error fields or
traverse `nextException` chains. Distinguish one terminal event, absence, ambiguity and unavailable capture;
none of these states proves rollback. Numeric completed SpringDoc durations may
support diagnosis, but caught framework exceptions and static group counts alone
do not establish a performance bottleneck. Keep raw logs private and preserve the
original HTTP outcome when the diagnostic sink fails.

Accept only the selected test's zero-failure XML and a reviewed, sanitized v1
receipt bound to the candidate/workflow SHA, assignment and branch attestation
hashes, and host/nested JAR hashes. Require all nine named phases, including
SESSION/current-grant checks, publication CAS and cold-node reconcile, BASIC
HTTP commit/read/replay and revocation, plus two started and terminated host
processes with private class-load evidence. Diagnose a failed phase against its
private logs and exact source before any new dispatch; a protected SQL-readback
recipe failure before host startup, including a `psql` meta-command mismatch,
is not an HTTP result and must not be bypassed by retrying publish or confirm.
Preserve the failed receipt and use a new reviewed exact SHA for a corrected run.
The protected readback alone cannot certify HTTP, SESSION or READY behavior.

Before this packaged proof, provision fresh AES material for the isolated child
and its owner-managed cursor issuance budget through the existing
`BULK-CURSOR-ISSUANCE-OPERATIONS.md` procedure. Require zero initial reservations,
a finite quota, expiry covering the assignment lease and runtime EXECUTE on the
reservation function. The fixture preflight only inspects these prerequisites;
it must not create, reset, extend or repair a budget. A newly generated key does
not inherit a copied parent's budget: missing enrollment returns HTTP503 before
the results reader, even when publication and cold reconciliation passed.
Preserve that failed campaign; a new full proof needs a fresh UNCOMPOSED API child,
new cryptographic material and an independently reviewed source/assignment.

Even a passing isolated-child receipt does not certify Config policy outage or
mutation, cancellation before the first unit, browser navigation, ASYNC/ATOMIC,
or Render HTTPS deployment. Keep the deployed Render gate and its actual
credentials, session and publication evidence separate from the Neon fixture;
do not report BASIC/READY operational acceptance until the remote run and its
independent review have passed.

At the deployed BASIC boundary, retain the exact strong ETag served by the target
GET and reject a weak or absent token before evaluation; never normalize it to
force a positive run. If identity/gzip and Brotli produce different ETag strength,
inspect the canonical versioned response and proxy transformation policy. Preserve
`no-transform` and existing no-store/cache directives at the response owner, then
prove the public artifact on the transport actually negotiated by the client.
The directive alone is not a universal proxy guarantee. [Render Docker services](https://render.com/docs/docker)
include automatic Brotli/gzip compression; inspect the actual `Content-Encoding`
and ETag rather than assuming identity transport. Advertise only supported codings,
actually decode negotiated `br`/`gzip`, and bound encoded and decoded bodies before
parsing JSON; reject unexpected codings or incomplete/invalid streams. Preserve the
received strong token without stripping `W/` or synthesizing a replacement. If
identity/gzip paths still yield weak validators, record them as unproved for this
command case; a strong negotiated Brotli response does not certify those paths.
Header/encoding observations alone do not establish READY or deployed H5 acceptance.
An evaluation HTTP 200 is not permission to confirm: require the proposal to be
READY, with the intended executable count and no blocked items, before submitting
the idempotency key. Preserve blocked proposals as evidence; do not erase their
history to obtain a clean positive test. Record the bounded request, proposal and
idempotency key privately before each one-shot POST, excluding authentication
secrets, and retain bounded error responses before asserting HTTP status. On an
uncertain result, inspect the exact durable state before any explicit recovery.
A new evaluation requires a fresh domain baseline and its own attempt identity;
do not reuse or overwrite failed confirmation markers.

## Managed-owner bulk execution adoption

For bulk installation by a non-superuser CREATEROLE database owner, inspect the
Metadata-owned `BulkExecutionMigrator`, `BulkMigrationLineage`, migration-lineage
catalogue/archive and `BulkManagedOwnerPostgresTest` before adapting Quickstart.
Verify that the exact publicly resolved artifact contains the managed-owner fix;
rc.155 does not. Source proof and a local installed coordinate do not establish
public host adoption.

The corrected execution-storage path requires PostgreSQL 17 or later. This is an
optional bulk execution boundary requirement, not a universal Metadata REST,
Config or capacity-authority database baseline. Check the concrete host wiring;
do not impose an optional authority/jobs campaign on BASIC HTTP proof.

Resolve the complete successful Flyway history. Applied original resources keep
their exact bytes/checksums; only pending resources use corrected canonical SQL.
Unknown identities, failed rows, holes or noncanonical mixtures are denied. Never
repair/clean history or manually complete bootstrap markers. Original V1–V4 may
continue; original V5–V16 are explicitly unsupported automatic predecessors.
V17/V18/V19/V20 retain their existing strict predecessor/catalogue checks; do not
claim that the V1–V4 or original V5 cutoff tests certify every historical prefix.

Fresh base grants are permitted only for the canonical managed-V5 witness, all
five bootstrap phases PENDING, empty configured host ACLs and intact physical
preflights. Existing base/derived grants and latch completion share the existing
transaction and fence. PENDING alone is insufficient. Partial ACLs, completed
bootstrap with revoked permissions and newly added grantees are not healed.

Require focused remote Neon PostgreSQL proof using an actual non-superuser role creator:
fresh/strict/repeat-zero, original-prefix and managed-intermediate conservation,
DDL19 retry, unsafe memberships/CREATE/PUBLIC ACL rejection without cleanup, and
Error rollback after a real grant. Earlier SUPERUSER-prepared fixtures are local
historical evidence only. Any new adversarial or historical preparation on Neon
must use an explicitly authorized administrator actually available on the assigned
branch; a privileged setup identity must not execute the product path. If the
required privilege is unavailable, leave that focal gate pending.
Record source, dependencies, SQL catalogue and raw test evidence; independently
review the actual result. Reuse unchanged accepted cases rather than repeating
all suites. Follow the official release's required gates, then resolve Central
POM/JAR provenance and validate the host without a version override before
claiming public or hosted adoption.

## Cold Restart and Hero Acceptance

After an authorized official publication and Render restart, record the deployed
main SHA, exact publicly resolved SDK artifact, instance/recovery result and
protected publication compatibility. Health/readiness alone does not certify
schemas or the consumer. Use a fresh Hero load and inspect filtered schemas,
filters, resource pages, capabilities and actions through completion. For the
remote table, navigate to page two, wait for deferred Material callbacks and
late discovery responses, and confirm that the backend total and range remain
stable before navigating back. An intermediate correct range is not acceptance.

Keep negative receipts and separate source tests, public artifact adoption and
live proof. An intermittent schema 503 or a total reduced to the page size keeps
the live gate pending even if a later reload succeeds. Do not silently retry
publication, cache live ACL/role authority, reset user configuration or increase
pools/deadlines to turn that negative into a pass. Classify the real canonical
owner and coordinate a single official release for shared SDK changes.
