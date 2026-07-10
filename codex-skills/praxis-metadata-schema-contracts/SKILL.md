---
name: praxis-metadata-schema-contracts
description: Use when Codex must work on praxis-metadata-starter structural schema contracts: x-ui, /schemas/filtered, /schemas/catalog, /schemas/domain, OpenAPI operation resolution, schema references, ETag, X-Schema-Hash, schemaId/schemaUrl, docs/spec schemas, or Angular schema consumption.
---

# Praxis Metadata Schema Contracts

Use this skill for the canonical structural schema surface of `praxis-metadata-starter`. This starter publishes backend semantic grounding for Praxis runtimes and AI authoring; it is not merely a JSON-schema generator for Angular components.

## Source Audit

Inspect the owner before editing:

- `praxis-metadata-starter/AGENTS.md`
- `praxis-metadata-starter/README.md`
- `src/main/java/org/praxisplatform/uischema/controller/docs/ApiDocsController.java`
- `src/main/java/org/praxisplatform/uischema/controller/docs/DomainCatalogController.java`
- `src/main/java/org/praxisplatform/uischema/controller/docs/SemanticDomainCatalogController.java`
- `src/main/java/org/praxisplatform/uischema/openapi/OpenApiDocumentService.java`
- `src/main/java/org/praxisplatform/uischema/openapi/CanonicalOperationResolver.java`
- `src/main/java/org/praxisplatform/uischema/schema/SchemaReferenceResolver.java`
- `src/main/java/org/praxisplatform/uischema/schema/FilteredSchemaReferenceResolver.java`
- `src/main/java/org/praxisplatform/uischema/hash/**`
- `src/main/java/org/praxisplatform/uischema/http/IfNoneMatchUtils.java`
- `docs/spec/**` and `docs/guides/**` when public contract or narrative changes

## Canonical Boundary

`/schemas/filtered` is the structural source of truth. It owns operation-specific schema shape, `properties.*.x-ui`, `x-ui.resource.idField`, `x-ui.resource.capabilities`, `schemaId`, `schemaUrl`, `ETag`, and `X-Schema-Hash`.

`/schemas/catalog` is documentary/discovery material. `/schemas/domain`, `/schemas/surfaces`, `/schemas/actions`, and capabilities may reference schemas, but they must not redefine the filtered schema payload inline.

Use canonical operation resolution from OpenAPI before inventing endpoint maps. `path + operation + schemaType` should resolve through `CanonicalOperationResolver`, `OpenApiDocumentService`, and `SchemaReferenceResolver`.

## Decision Rules

- Do not fix missing schema semantics in Angular, quickstart, HTTP examples, or docs when the canonical source is the starter.
- Do not add parallel endpoints for request/response schema variants when `/schemas/filtered` plus canonical operation resolution can express them.
- Keep `schemaId` and `schemaUrl` aligned when adding structural dimensions such as `includeInternalSchemas`, `idField`, or `readOnly`.
- If `ApiDocsController` changes, review cache headers, `ETag`, `X-Schema-Hash`, `If-None-Match`, and exposed headers in the same pass.
- If `x-ui` shape changes, review `docs/spec/*.schema.json`, examples, conformance docs, Angular consumers, and quickstart downstream tests.

## No Keyword Routing

Do not resolve resource, operation, schema, or field intent through keywords, regexes, aliases, or local fuzzy matching as the primary decision. Use canonical OpenAPI operations, resource keys, schema references, governed semantic catalogs, and declared tools for grounding; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding schema fields, headers, query params, endpoint variants, or resolver branches, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public schema contract. In that case name the missing data, canonical owner, consumers, derived docs/examples, and minimum validation.

## Validation

Use focused local gates:

- docs/schema refs/hash: `mvn "-Dtest=ApiDocsControllerTest,ApiDocsControllerPathResolutionTest,ApiDocsControllerSchemaHashTest,DomainCatalogControllerTest,FilteredSchemaReferenceResolverTest,OpenApiCanonicalOperationResolverTest" test`
- quickstart downstream proof for public schema changes: `QuickstartMetadataMigrationIntegrationTest`, `EventosFolhaPilotIntegrationTest`, and `OpenApiGroupResolutionIsolatedIntegrationTest`
- Angular consumer proof when schema runtime changes: `schema-metadata-client.spec.ts`, `fetch-with-etag.util.spec.ts`, and `generic-crud.service.spec.ts`

Review `README.md`, `CHANGELOG.md`, `docs/index.md`, `docs/guides/**`, `docs/spec/CONFORMANCE.md`, `docs/spec/*.schema.json`, and `docs/spec/examples/**` when public schema semantics change. State why if no derived artifact is updated.

## Companion Skills

- Use `praxis-metadata-resource-baseline` for resource-oriented controller/service hierarchy.
- Use `praxis-metadata-discovery-capabilities` for surfaces, actions, capabilities, `_links`, availability, stats, and export discovery.
- Use `praxis-metadata-domain-option-sources` for `@DomainGovernance`, semantic domain catalog, option sources, field access, and entity lookup contracts.
- Use `praxis-api-quickstart-operational-proof` and `praxis-api-quickstart-cockpit-http-validation` for downstream HTTP proof of schema contracts in the reference host.
- Use `praxis-http-examples-contract-surfaces` when the public executable HTTP corpus for `/schemas/**`, headers, or schema examples is affected.
- Use `praxis-core-resource-runtime` for Angular consumption of these contracts.
