---
name: praxis-java-contract-conformance
description: Use when auditing a Praxis Java resource or host before migration/API handoff: verify OpenAPI, filtered/catalog/domain schemas, x-ui, ETag and X-Schema-Hash, RestApiResponse _links, structured errors, filters, option sources, actions, surfaces, collection/item capabilities, stats/export, sanitized evidence, and Angular runtime readiness through GenericCrudService, SchemaMetadataClient, ResourceDiscoveryService, forms, tables, or analytics consumers.
---

# Praxis Java Contract Conformance

Use this as the final proof gate for an implemented resource. It does not replace
the focused implementation skills; it assembles their evidence and reveals which
contract edge still prevents a migration-ready API.

## Build A Resource Evidence Pack

Start with one resource key and canonical path. Inspect its controller, service,
mapper, DTOs, filters, actions, surfaces, option descriptors, errors, tests,
HTTP examples, direct Angular consumers, and any legacy parity artifact. Record
the operation matrix before running tests.

For every failure, classify it as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. A conformance failure is
not permission to add a frontend alias, duplicate endpoint, second schema, or
host-local metadata map. Locate and fix the canonical owner.

Read [conformance-evidence-matrix.md](references/conformance-evidence-matrix.md)
to select only the evidence required by the resource's actual operations.

## Audit In Levels

0. **Domain Completeness & Anti-Truncation Scorecard (Mandatory First Gate):**
   Never approve a resource merely because `mvn test` or a minimal smoke test passes. Before inspecting schema or HTTP details, compute and report the **Domain Completeness Scorecard** (and run `python scripts/workspace/audit-java-resource-completeness.py <host-path>` when auditing a workspace host):
   - **Entity-to-DTO Column Accounting (`100%` business column accountability):** Compare every column of the JPA Entity against `ResponseDTO`, `CreateDTO`, `UpdateDTO`, `@ResourceIntent` DTOs, and `@WorkflowAction` request DTOs. Every business column must either be:
     1. Exposed in `ResponseDTO` + `CreateDTO`/`UpdateDTO` (grouped via `@UISchema(group = ...)`, using `tableHidden = true` for secondary detail fields so tables remain concise while forms/detail views are complete);
     2. Exposed as `readOnly = true` in `ResponseDTO` and mutated by a dedicated `@WorkflowAction` or `@ResourceIntent` (`PATCH`); or
     3. Explicitly justified as internal/technical (`@Version`).
     If a resource silently drops domain columns (e.g., exposing 9 of 55 entity columns or 15 of 51 columns), mark `static` as **`fail`** immediately (`lacuna-de-completude-de-dominio`).
   - **`FilterDTO` Predicate Density & Variety:** Verify that `FilterDTO` covers all operational search dimensions of the entity across multiple `FilterOperation` families (`LIKE`/`STARTS_WITH`, `EQUAL`, `IN`/`NOT_IN`, `BETWEEN`/`GREATER_OR_EQUAL`/`LESS_OR_EQUAL`, `IN_LAST_DAYS`/`IN_NEXT_DAYS`/`ON_DATE`, `IS_NULL`/`IS_NOT_NULL`, `IS_TRUE`, cross-entity `relation = "parent.field"`, and `@CustomFields` when JSONB is present). A 2- to 4-field `FilterDTO` on a rich domain entity is an automatic **`fail`**.
   - **Praxis Capability Density (`@QuickFilter`, `@ResourceIntent`, `@WorkflowAction`, `@ResourceFact`, Business Invariants):**
     - Verify `@QuickFilter`s on `@ApiResource` for operational cohorts;
     - Verify `@ResourceIntent` (`PATCH`) + `@UiSurface(kind = SurfaceKind.PARTIAL_FORM)` on wide entities (20+ columns or multiple functional sub-blocks);
     - Verify that every lifecycle state transition in the entity (`situacao`, `dtExtincao`, `dtHomologEstagio`, etc.) has a corresponding `@WorkflowAction` backed by `ResourceStateSnapshotProvider`;
     - Verify `@ResourceFact` annotations for derived domain indicators;
     - Verify that real domain invariants (chronological date order, vacancy balance, extinct record guards, constitutional accumulation, cross-tenant FK consistency, uniqueness, conditional requiredness) are enforced in the `Service` and covered by negative tests (`409`/`422`).
1. **Static:** resource identity, canonical path, selected resource base,
   operation-specific DTOs, mapper/service wiring, annotations, governance, and
   explicit commands are coherent. A read-only resource must not claim writes;
   a mutable resource must not hide workflows in generic updates. For shared bulk
   lifecycle handlers, inspect `@BulkResourceOperations` and each handler's
   `@BulkResourceOperation` role. The five declared IDs must bind to one real MVC
   handler each; do not infer them from Java names, labels, or paths. For a bulk
   domain command, also inspect the real `@WorkflowAction` confirmation handler's
   `@BulkOperation` binding and verify that its distinct evaluation operation is
   a body-bearing POST handler in the same resource controller.
2. **Schema:** `/v3/api-docs`, `/schemas/filtered`, `/schemas/catalog`,
   `/schemas/domain`, `/schemas/surfaces`, and `/schemas/actions` agree on
   resource key/path/group, operations, schema references, `x-ui`, option
   sources, field access, and discovery. Catalogs and capabilities are never
   accepted as alternate structural schemas. For shared bulk lifecycle handlers,
   confirm `requireResourceOperation(resourceKey, operationId, method)` returns
   the expected `CanonicalOperationRef`, the exact named group document preserves
   that identity, and every currently published group is inspected for rewrites
   or collisions in paths, callbacks, and webhooks.
3. **HTTP:** exercise filter/get/write/action/export/stats operations that exist;
   verify `RestApiResponse._links`, structured error shape, validation errors,
   status semantics, ETag, `If-None-Match`, and `X-Schema-Hash`. Capture only
   sanitized evidence; never publish database, package, token, session, SQL, or
   provider-context details.
4. **Availability:** compare collection and item `/capabilities`, action and
   surface catalogs, and `_links` in both allowed and denied states. Verify that
   item decisions use the shared resource state snapshot and remain fail-closed
   where protected.
5. **Runtime readiness:** trace each published contract to its real Angular
   consumer. `GenericCrudService` consumes resource/schema/filter/option paths;
   `SchemaMetadataClient` and `fetch-with-etag` consume ETag/hash semantics;
   `ResourceDiscoveryService` follows `_links` for surfaces/actions/capabilities;
   forms, tables, and analytics consume the matching normalized metadata. Do not
   require building a new screen, but do require that an existing official runtime
   path can materialize the contract without custom consumer rules.
6. **Persistence/parity:** when the resource is legacy-backed, prove a scoped
   development mutation or read path as appropriate, preserve before/after
   evidence, cleanup/rollback plan, and parity result. Do not claim parity merely
   from a matching DTO name or one happy-path row.

## Scope Evidence To Existing Operations

Only audit option-source filter/by-ids, actions, surfaces, stats, export, field
access, related resources, or config materializations when the resource publishes
them. Conversely, every published feature needs its matching proof. Do not mark
a resource conformant because unrelated broad tests are green.

Public contract changes require focused starter tests, quickstart HTTP proof when
available, and affected Angular specs. Use source-local `AGENTS.md` commands;
prefer focused tests over broad suites. Review docs, corpus, examples, and
playgrounds only when they publish the changed contract.

## Bulk Protocol, Artifact Provenance, Strict OpenAPI, And Cold-Start Gates

When auditing `org.praxisplatform.uischema.bulk` protocol input/results,
`BulkConsumerArtifactIntegrationTest` git provenance, `@BulkEditable` compilation,
strict canonical OpenAPI group snapshots (`getDocumentForGroupStrict`), or
`EmbeddedPostgresColdStartTest`, read
[bulk-and-openapi-conformance-gates.md](references/bulk-and-openapi-conformance-gates.md).

## Report Without Ambiguity

Return an evidence pack containing:

- identity and operation matrix;
- status for `static`, `schema`, `http`, `availability`, `persistence/parity`,
  and `angular-readiness`: `pass`, `not-applicable`, `blocked`, or `fail`;
- source files, endpoints, fixtures, commands, and sanitized outcomes;
- canonical owner and classification for every non-pass result;
- derived-artifact decision, remaining risk, and exact next action.

`blocked` is only valid when an external prerequisite is unavailable and the
remaining local checks were exhausted. `not-applicable` must name the absent
published operation. Never use either label to hide an untested public claim.

## Preserve Canonical Ownership

- `praxis-metadata-starter` owns resource metadata, schemas, discovery,
  capabilities, `_links`, HTTP metadata headers, and their conformance rules.
- `praxis-config-starter` owns governed config/authoring contracts; a resource
  audit may verify materialization but must not redefine config semantics.
- `praxis-ui-angular` owns runtime materialization; conformance checks consumers
  rather than creating a competing UI contract.
- Quickstart and HTTP corpus provide operational proof and do not become owners.

Do not decide resource scope, operation, action, surface, or consumer path with
keyword routing, regexes, label matching, or route-string guesses. Ground it in
resource keys, canonical schemas, links, action/surface IDs, capabilities, and
declared runtime contracts.

## Companion Skills

- `praxis-java-resource-authoring`: implementation and resource operation matrix.
- `praxis-java-filter-query-authoring`: filter/query proof.
- `praxis-java-option-source-provider-authoring`: external option source proof.
- `praxis-java-availability-discovery-authoring`: action/surface/capability proof.
- `praxis-metadata-schema-contracts`: schema, OpenAPI, ETag, and hash semantics.
- `praxis-api-quickstart-cockpit-http-validation`: HTTP/cockpit evidence.
- `praxis-core-resource-runtime`: Angular runtime materialization.

Close only when the evidence pack shows a resource can be consumed canonically by
the intended runtime, or when every remaining gap has a named owner and an
explicit follow-up. Compilation alone is not conformance.
