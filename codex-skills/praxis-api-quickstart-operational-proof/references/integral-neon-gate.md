# Integral Quickstart Neon Gate

This is the acceptance procedure for the whole Quickstart source and sanitized
snapshot, not a claim that a particular campaign passed. Quickstart owns the
test infrastructure and release orchestration. Metadata and Config retain their
contracts, immutable migrations and privilege requirements.

## Inspect The Exact Candidate

Read root/local `AGENTS.md`, `RELEASING.md`, `ACTIONS-RELEASE-POLICY.md`,
`docs/NEON-RELEASE-GATE.md` and:

- `src/test/java/com/example/praxis/apiquickstart/config/neon/**`, its launcher
  SPI under `src/test/resources/META-INF/services/` and assignment example;
- `scripts/workspace/neon_gate_assignment.py` and its offline tests;
- `IntegrationTestIsolationPolicyTest`, selected fixtures and the current POM;
- `scripts/workspace/prepare-public-release.ps1`,
  `scripts/verify-packaged-runtime.sh`, `.github/workflows/ci-java.yml`,
  `.github/public-workflows/ci-java.yml` and the release workflow calling them.

Resolve public POM/JAR bytes and record their hashes and packaged dependencies.
An HTTP200 POM check alone does not prove JAR provenance. Keep candidate/local
SDK evidence separate from adoption of the committed public coordinates; do not
use version overrides or a local install to certify public adoption.

Freeze the source SHA/tree and relevant uncommitted bytes, dependency hashes,
fixture/helper and policy hashes. Generate the sanitized tree from that source,
record its own digest and inspect the sanitizer result. Later source or shared
fixture changes invalidate affected passes; do not relabel old evidence.

## Assignment And Actors Before Mutation

Use a trusted operator-issued child assignment with project, child, parent,
direct read-write endpoint, readiness/default/protection state, PostgreSQL
version, run/repository/source identity and a bounded lease. A self-asserted JSON
receipt alone is not a control-plane observation. Never copy a historical branch,
endpoint, role or private artifact path from an earlier campaign.

Inspect the materializer and helper for their exact required inputs. Current
materialization consumes the private `QUICKSTART_NEON_ASSIGNMENT` and binds
`PRAXIS_QUICKSTART_NEON_ASSIGNMENT_FILE`,
`PRAXIS_QUICKSTART_NEON_ASSIGNMENT_SHA256`, `PRAXIS_QUICKSTART_NEON_RUN_ID`,
`PRAXIS_NEON_EXPECTED_SOURCE_SHA` and `PRAXIS_NEON_EXPECTED_REPOSITORY`.
Keep secret-bearing files outside source/artifacts with private permissions;
never put DSNs/passwords in argv, Maven properties or public receipts. Release
authorization must bind the exact authorized tag/tree through the materializer;
do not rewrite a source identity to reuse an unrelated lease.

Verify client TLS `verify-full`, channel binding, actual peer, PostgreSQL major,
`session_user=current_user`, database and role privileges. The bulk managed-owner
fixture requires PostgreSQL17; this is not a universal Praxis database baseline.
The reviewed helper admits PG17 explicitly. Prove the available administrator
and migration-owner profiles rather than presuming SUPERUSER.

For a managed owner that must have zero inbound membership, follow the canonical
Metadata PG17 managed-owner tests and migration preflight. PostgreSQL17 can add
an ADMIN-only membership for a non-superuser role creator; attribute flags alone
do not satisfy the SDK's owner guard. The reviewed provisioning pattern uses a
unique `owner_ephemeralprovisioner` identity conceptually: an authorized admin
creates the disposable creator; that authenticated creator creates the campaign
migration owner; verify exact OIDs, attributes and membership options, then drop
only that creator after proving it has no unrelated dependencies. Reconnect as
the owner and prove no inbound/outbound memberships remain before migration.
Do not grant owner membership to the long-lived provision admin, mutate shared
owner defaults, relax the SDK guard or publish a copy of campaign-specific SQL.
Provisioning failure or an uncertain CREATE/DROP requires private-ledger
reconciliation before retry. This procedure is not a generic provisioning CLI.

The migration owner stays stable through the serialized SDK campaign. API and
Config databases and ordinary runtime/control/business-admin roles are unique
per concrete consuming fixture. The application gets ordinary credentials and
DDL disabled; only explicit setup/export/Flyway uses owner authority. Preserve
restrictive grants, negative ACL tests and migration placeholders. Functional
fixture DML grants cannot substitute for an authorization test.

## Lifecycle And Cleanup Are Part Of Acceptance

Use the reached `AssignedNeonStores`/`AssignedNeonDatabase` path admitted by the
isolation policy; a helper name in dead code is not isolation. Shared fixtures
receive the concrete consumer FQCN. Spring cleanup runs after context/pool
closure through `AssignedNeonSpringTest`; non-Spring fixtures close their owned
resources explicitly. Standalone packaged proofs also close the campaign.

Role membership is global to the branch. Admit SDK canonical roles only from
proved initial absence, retain exact recorded identities between sequential
fixtures and reset only at the explicit session boundary after zero leases and
owned database cleanup. Unexpected roles/memberships or changed OIDs block
cleanup; never adopt or remove them by prefix/name alone. Do not change immutable
SDK migration bytes to make successive fixtures fit.

Record intent before mutation and reconcile unknown transport outcomes by exact
identity. An unregistered allocation, unresolved intent, live connection or
cleanup exception cannot become a successful campaign-close receipt. Expiry
blocks new allocation without preventing cleanup of already owned resources.
Keep cancellation/runner-loss reconciliation explicit; a shutdown callback alone
is not cleanup evidence. Assignment, lock and journal custody must reject unsafe
file targets. Do not terminate unrelated sessions or run broad DROP OWNED/reset.

## Execute And Account For Both Trees

Use the official full command in the private checkout, then in the generated
sanitized checkout, with the same public coordinates and reviewed assignment
lifecycle; retain separately attributable reports from each tree:

```bash
./mvnw -B -fae -Dstyle.color=always verify
bash scripts/verify-packaged-runtime.sh
```

Do not add `-Dtest`, skip flags, exclusions or dependency overrides to call this
an integral gate. Invoke the reviewed assignment materializer and cleanup
attestation in their actual workflow order; do not invent credentials or a new
local bridge. Private and sanitized runs must not allocate concurrently against
one exclusive campaign. The public repository's later CI has its own secret and
does not replace pre-publication verification of the sanitized tree.

Inventory expected classes/cases and exact existing opt-in conditions before
execution. Compare fresh Surefire/Failsafe XML with that inventory: failures,
errors and missing required cases block acceptance. Require zero skips/aborts
for mandatory cases. Record every optional skip by class/method, condition and
reason, including lanes not discovered by default suffixes; an existing optional
lane is not newly proved by being absent from the run. No new skips or narrower
test selection may hide an unavailable assignment or migrated assertion.

Retain raw logs, XML and journals privately. Before any artifact export, review
redaction and allowlisted shape; XML can contain secrets in properties or error
text. Publish only sanitized assignment/cleanup receipts and reviewed reports,
bound to source/tree/dependencies, run/attempt and branch attestation. A lifecycle
receipt proves its attested cleanup, not every HTTP assertion; a green test count
without cleanup does not accept the campaign. Preserve failed attempts.

Close with separate states for offline helper/policy checks, focal Neon cases,
integral private verification, integral sanitized verification, source/public
publication and deployed HTTP proof. Require independent review of exact final
results before release adoption. Never infer deploy acceptance from this gate;
inspect authorized release triggers and actual runtime identity separately.
