---
name: praxis-java-quickstart-proof
description: Use when creating, extending, or auditing a Praxis API Quickstart operational proof for a Java resource: real HTTP schemas, OpenAPI, filters, option sources, actions, surfaces, capabilities, errors, stats/export, test data, write readback/cleanup, Cockpit verification, and downstream starter/runtime evidence.
---

# Praxis Java Quickstart Proof

Treat Quickstart as an operational proof host, never the owner of starter semantics.
Choose one representative resource and prove a canonical path by HTTP with fixtures
that demonstrate both success and an important negative condition.

## Build The Proof Slice

Inspect `ApiPaths`, controller, service, DTO/filter/action, mapper, option source,
test fixtures, security/origin setup, and existing pilot integration tests. Reuse
an existing pilot when it proves the same capability; do not copy a domain only
to make a new example. Fix a starter gap in the starter, then add the smallest
downstream proof here.

## Required Evidence

1. Prove resource identity in OpenAPI and `/schemas/filtered`, including stable
   path/resource key, request/response operation schemas, `x-ui`, ETag and hash.
2. Exercise each published operation in scope: filter/read, lookup reload,
   action/surface/capabilities, stats/export, or write. Verify `_links` and
   collection/item discovery agree.
3. Include a negative case: invalid payload, missing resource, denied state,
   invalid filter/option request, conflict, or policy limit. Prove no mutation
   follows a rejected write.
4. For database-backed proof, use explicitly assigned isolated Neon branches;
   unit tests without a database may run locally. For writes, retain controlled
   fixtures, read-after-write, side-effect evidence and cleanup. Do not substitute
   H2, embedded/local PostgreSQL or an unassigned parent/production branch.
5. Run the relevant `QuickstartMetadataMigrationIntegrationTest`,
   `EventosFolhaPilotIntegrationTest`, focused pilot test, or Cockpit verifier.
   Review direct Angular runtime proof when the published contract changes.

Read [proof-slice-matrix.md](references/proof-slice-matrix.md) when selecting
the smallest representative resource and required evidence.

## Focal Proof And The Integral Neon Gate

A focused pilot proves its selected behavior. It does not accept the host's
integral release gate, even when its Maven goal is `verify`. For starter adoption,
bootstrap or packaging changes that require the wider gate, follow the existing
[`praxis-api-quickstart-operational-proof` procedure](../praxis-api-quickstart-operational-proof/references/integral-neon-gate.md).
Verify the final private source and generated sanitized tree in sequence against
the same public coordinates, with separately attributable reports and cleanup.

Retain every required test and its assertions. Inventory optional cases by exact
class/method, existing opt-in condition and reason; report skipped/aborted cases
by name rather than accepting a total alone. Optional lanes outside the selected
gate remain explicitly unproved. Missing assignment, new exclusions, disabled
tests or an empty selection cannot produce a passing database proof. Keep raw
logs, credentials and failure reports private until their export is reviewed;
publish only the closed, sanitized evidence projection.

## Published SDK Adoption On Neon

Inspect the Quickstart POM, `src/test/java/com/example/praxis/apiquickstart/config/MetadataAdoptionNeonFixture.java`,
its unit tests, `src/test/resources/metadata-adoption/neon-fixture.sql`, and the three
Metadata downstream pilots before selecting this gate. This route proves host
consumption of published SDKs; it does not publish an SDK or release the host.

1. Verify the public POM/JAR bytes first, then adopt the published coordinates in
   the host POM. Resolve through `.mvn/ql07-central-only-settings.xml` and a fresh
   isolated Maven repository. Do not use a local SDK install, candidate GAV or
   `praxis.core.version`/`praxis.config.version` override as public-adoption proof.
2. Inspect the current `MetadataAdoptionNeonFixture` and
   `config/neon/AssignedNeonStores`: the reviewed PR #482 fixture uses the shared
   Quickstart assignment, not the historical three-file adoption lease. Follow
   [the integral gate's assignment procedure](../praxis-api-quickstart-operational-proof/references/integral-neon-gate.md)
   to bind `PRAXIS_QUICKSTART_NEON_ASSIGNMENT_FILE`, its SHA-256, run ID,
   expected repository and source SHA. Confirm the target checkout contains this
   fixture before executing; do not apply candidate guidance to an older release.
   Keep credential files private and outside source/artifacts. Never copy
   passwords/DSNs into guidance, manifests, reports or command arguments, or reuse
   historical endpoint/expiry values. Serialize classes sharing the SDK roles.
3. Confirm endpoint/TLS/PostgreSQL identity and actual role privileges before
   mutation. Owner may prepare and remove only assigned fixture databases/roles. The application
   uses ordinary API and Config runtimes: neither may be superuser, bypass RLS,
   create roles/databases, or be a member of `neondb_owner`/`neon_superuser` and
   assume those roles. Direct privilege flags alone do not prove this separation.
4. Enable the official external-test opt-in, retain all selected cases and use
   the host's published POM without overrides. From the Quickstart checkout, with
   the assignment inputs exported and an absolute fresh repository path in
   `PRAXIS_ADOPTION_MAVEN_REPO`:

```bash
: "${PRAXIS_ADOPTION_MAVEN_REPO:?Set an absolute fresh isolated Maven repository}"
PRAXIS_EXTERNAL_SMOKE_TESTS=true mvn -B -ntp \
  -s .mvn/ql07-central-only-settings.xml \
  "-Dmaven.repo.local=$PRAXIS_ADOPTION_MAVEN_REPO" \
  -Dtest=OpenApiGroupResolutionIsolatedIntegrationTest,QuickstartMetadataMigrationIntegrationTest,EventosFolhaPilotIntegrationTest \
  -Dsurefire.failIfNoSpecifiedTests=true verify
```

Require the reviewed selection's full case count and zero failures, errors and
skips (currently 43 cases across these three classes). Missing inputs must fail
closed; an opt-in-disabled/skipped run is not a proof. Bind raw reports, source
and SQL hashes, resolved public dependency bytes and packaged dependencies to
this exact run and child assignment.

If a failed assertion is corrected without changing production source, dependencies,
shared fixtures or the passing classes, rerun the affected class with separate
reports after verified cleanup. Reuse the cache only when its exclusively public
origin remains proven. Preserve the negative run and compare source/dependency
hashes before retaining earlier passes. Require the complete case matrix to pass;
label combined evidence explicitly rather than claiming a single green 43-case
run. Changes to shared fixtures or runtime behavior invalidate the affected prior
passes and require those cases to run again.

Use the official bootstrap and migrations on the assigned databases. The
financial fixture must activate approved governance through the real Config
publication path and write payroll/events through admitted HTTP actions; SQL
inserts into those governed aggregates cannot replace that authority. Scope
nonfinancial seed and assertions to unique case IDs, including unique text keys.
Preserve inherited-row snapshots during the run, revoke issued sessions and close
Spring before deleting the owned databases/roles by their recorded OIDs. Do not
claim row restoration when the actual cleanup removes the whole disposable store.

A selected `verify` proves this focal slice plus packaging, not unrestricted
`mvn verify`, the broad host release gate, or a published/deployed release. The
financial authority logs its governance actors in through `/auth/login`. Case
principals receive persistent sessions through `EnterpriseSessionLifecycle.issue`;
the pilots verify HTTP SESSION admission/revocation, not password/identity-provider
login for those case principals. Config governance uses a fixed host tenant and
ordinary API/Config runtimes.
That is not multitenant Config rollout, browser login, CSRF or general departmental
authorization proof. Preserve the explicit policy/mock boundaries in the current
fixture and record skipped/aborted cases separately. Prior private-candidate
passes remain tied to their source and dependency hashes; an integrated PR or
unchanged GAV does not turn them into public-artifact evidence.

## Boundaries

- Quickstart owns host wiring, data, security, paths, and operational evidence.
- Metadata starter owns schemas, discovery, capabilities, option contracts, and
  resource semantics. Angular owns runtime materialization.
- Do not add aliases, schema patches, duplicate Cockpit assets, or host-local
  decision logic to make a smoke pass.

Close with resource key, operations proved, fixtures, commands, sanitized HTTP
outcomes, cleanup state, and unresolved owner follow-up. A pilot is useful only
when another host can reproduce the platform behavior from its evidence.
