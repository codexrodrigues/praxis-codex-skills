---
name: praxis-java-host-project
description: Create or evolve Java/Spring Boot backend host projects for the Praxis platform using published Maven starter dependencies by default. Use when Codex must scaffold a new Praxis Java microservice, choose Praxis starter versions, wire praxis-metadata-starter or praxis-config-starter, create resource-oriented controllers/services/DTOs, adapt reference host patterns when available, or validate a host publishes canonical Praxis metadata surfaces such as /schemas/filtered, /schemas/domain, ApiResource, x-ui, actions, capabilities, export, and /api/praxis/config/**.
---

# Praxis Java Host Project

## Overview

Use this skill to create a new Java host that composes the Praxis platform correctly instead of inventing local contracts. Treat published Praxis starters as external Maven dependencies by default; use local starter source only when it is actually present and the task is platform-development work.

Before changing this skill or implementing a Java host, audit the resolved starter or local platform source for the contract being used: `@ApiResource`, `AbstractResourceController`, `AbstractReadOnlyResourceController`, `AbstractBaseResourceService`, `AbstractReadOnlyResourceService`, `ResourceMapper`, schema/catalog controllers, capabilities, actions, surfaces, export, option sources, config headers/ETag, and a representative quickstart resource when available. The goal is to codify what Praxis already knows canonically before adding host-local endpoints, DTO fields, registries, or AI/config abstractions.

When local source is available, start with `praxis-metadata-starter/AGENTS.md`, `praxis-config-starter/AGENTS.md`, and `praxis-api-quickstart/AGENTS.md` to confirm the current starter and reference-host boundaries. When source is absent, use released dependency metadata, generated docs, Maven artifacts, and HTTP behavior instead of requiring the monorepo.

When preparing a starter publication required for public host adoption, read
[starter-publication-and-adoption.md](references/starter-publication-and-adoption.md).
Keep signed source, validated bundle, Central deployment, artifact availability
and consumer adoption as separate evidence gates. Follow the owning repository's
actual release workflow; this skill does not authorize a release.

## Required Classification

Classify the request before editing:

- `arquitetural` when creating a new host, choosing starter boundaries, or changing bootstrap structure.
- `contrato-publico` when changing resource paths, `@ApiResource`, DTO schema, `x-ui`, `/schemas/**`, capabilities, actions, headers, or `/api/praxis/config/**`.
- `transversal` when updating the host plus docs/examples/http corpus or shared starters.
- `local-pequena` only for a contained host implementation detail with no public contract impact.
- `docs-apenas` for editorial guidance only.

For `arquitetural`, `contrato-publico`, or `transversal`, map impact before patches: canonical owner, affected consumers, public docs, examples/playgrounds/HTTP corpus, minimum validation, and breaking-change risk.

## Workflow

1. Read the host repository's `AGENTS.md` files when present.
2. Determine dependency mode:
   - **Published dependency mode, default**: the host consumes `io.github.codexrodrigues:praxis-metadata-starter` and, when needed, `io.github.codexrodrigues:praxis-config-starter` from Maven Central or the configured artifact repository.
   - **Local Maven mode**: the host consumes a starter version already installed in `~/.m2`; do not assume source code is available.
   - **Platform source mode**: starter source is present in the same workspace; inspect it only when debugging starter behavior or changing platform contracts.
3. Resolve versions from the user's requested release, the host's existing `pom.xml`, Maven Central metadata, or the reference host documentation. Prefer the public reference host `https://github.com/codexrodrigues/praxis-api-quickstart-public` when a local quickstart checkout is unavailable, but treat it as an example/reference, not a file dependency. Use local `praxis-api-quickstart` source only if it is available locally and the task benefits from comparing against the private/reference host. For consumer hosts, do not assume any quickstart `pom.xml` version has been published; prove artifact availability with Maven metadata or `mvn dependency:get`, preferably with a temporary `-Dmaven.repo.local` when the task is about an external scaffold.
4. Decide whether the new project is:
   - a minimal host proving platform bootstrap;
   - a domain host with real resources;
   - a reference/demo host that must mirror quickstart breadth.
5. Collect or infer the minimum resource contract before generating files: base package, module, entity/projection name, ID type, `resourcePath`, stable `resourceKey`, OpenAPI group, mutability/read-only mode, real fields, relationships, filter needs, option/lookup needs, and whether surfaces/actions/export/stats are in scope.
6. Generate resource files in dependency order using the exact generic signatures and templates in [resource-baseline.md](references/resource-baseline.md) (including Section 0 for complete `pom.xml`/`application.yml` bootstrap with `-parameters`, MapStruct/Lombok annotation processors, `springdoc.writer-with-order-by-keys: true`, and `praxis.resource-version.etag.secret`). For a new application prefer `ApiPaths`, entity/projection, repository, DTOs, mapper, service, controller. For an existing application adding a resource, prefer DTOs, repository, mapper, service, controller, and only then surfaces, intents, actions, export, or analytics.
7. Use the canonical resource-oriented baseline and deliver the **Full-Power Praxis Value Pack** on the first shot so the resource compiles immediately and showcases the platform without back-and-forth:
   - `@ApiResource(value=..., resourceKey=..., title=..., description=..., icon=..., visualTone=..., identity=@ResourceIdentity(...), quickFilters={@QuickFilter(...)})` (note: `@ApiResource` is already meta-annotated with `@RestController` and `@RequestMapping`);
   - `@ApiGroup(...)` with semantic/visual metadata when grouping is meaningful;
   - Entity with `@OptionLabel` on the canonical human label getter/field (enabling `/options/filter` and `/options/by-ids` automatically) and `@DefaultSortColumn`;
   - `BaseCrudRepository<E, ID>`;
   - `ResourceMapper<E, ResponseDTO, CreateDTO, UpdateDTO, ID>` (note: `ID` is 5th; `applyUpdate(E entity, UpdateDTO dto)` takes `entity` first and must never overwrite route-owned `id`);
   - `AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (note: `ID` is 3rd) overriding `getResourceMapper()`, `getDatasetVersion()`, `getStatsFieldRegistry()`, and `StatsSupportMode.AUTO` (`getGroupByStatsSupportMode()`, `getTimeSeriesStatsSupportMode()`, `getDistributionStatsSupportMode()`, `getComparisonStatsSupportMode()`) so `/stats/*` works out of the box;
   - `AbstractResourceController<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` (note: 5 type params, no `E`, `ID` is 2nd) overriding `getService()` and `getResponseId(ResponseDTO dto)`;
   - `AbstractReadOnlyResourceController<ResponseDTO, ID, FilterDTO>` and `AbstractReadOnlyResourceService<E, ResponseDTO, ID, FilterDTO>` for read-only views/projections;
   - mutable resources: separate `ResponseDTO`, `CreateDTO` (`@JsonIgnoreProperties({"id"})`), `UpdateDTO` (`@JsonIgnoreProperties({"id"})`), and `FilterDTO implements GenericFilterDTO` with rich domain `@Schema(description=...)`, `@UISchema` (`preset`, `controlType`, `numericFormat`, `group`, `order`, `icon`, `quickViewVisible`, `helpText`), `@DomainGovernance`/`@AiUsagePolicy`, and a multi-operator `@Filterable` matrix (`LIKE`, `EQUAL`, `IN`, `BETWEEN`, `IN_LAST_DAYS`);
   - read-only resources: `ResponseDTO` and `FilterDTO` only;
   - **Composite PKs (`@EmbeddedId`), Optimistic Concurrency (`@Version`), Governed Relationships (`@ResourceReference` / `OptionSourceRegistry` + Rich `EntityLookupDescriptor`), `@Embedded` Value Objects, JSONB `@CustomFields`, `@ResourceFact`, `@MicroVisualization`, `@UiAnalytics`, Governed Bulking (`@BulkEditable` / `@BulkResourceOperations` / `@BulkOperation`), Rich `CollectionExport` (`CSV`/`JSON`/`EXCEL` + `CollectionExportFieldPresentation`), `ReactiveDeterminationDefinitionProvider`, and Native JUnit Completeness Gate (`SemanticMetadataReviewer` + `PraxisExpressionStaticValidator` + `OptionSourcePublicationInventory`):** follow Sections 9, 10, 11, 12, and 13 of [resource-baseline.md](references/resource-baseline.md) and the 20-Pillar / 3-Phase Blueprint (`META-INF/praxis/AI-RESOURCE-BLUEPRINT.md` bundled in `praxis-metadata-starter` or `GUIA-00-BLUEPRINT-COMPLETO-RECURSO-PRAXIS.md`). Never attempt a multi-resource showcase in a single shallow pass; execute in 3 deep vertical phases (Phase 1: Data/DTOs/`@UISchema`/`@MicroVisualization`/Quick View 360°/Rich Lookups/`FilterDTO`; Phase 2: `@UiSurface`/`@ResourceIntent`/`@WorkflowAction`/Bulking/`@ResourceFact`/`@UiAnalytics`/`CollectionExport`; Phase 3: Domain Invariants/`ReactiveDetermination`/`praxis-rules-engine`/`/praxis/cockpit`/N+1 & Completeness Gates).
8. Treat `AbstractCrudController`, `AbstractReadOnlyController`, `BaseCrudService`, and similar pre-resource-oriented classes as migration surfaces only. Do not use them as the default for new resources when the resolved starter exposes the resource-oriented baseline.
9. Include `praxis-config-starter` only when the host must expose `/api/praxis/config/**` or AI authoring/config-store surfaces and can provide the required config-store datasource, migrations/tables, and host adapters. Do not include it for a metadata/filter-only service. Before adding it, confirm the target host meets the starter's release prerequisites such as compatible Spring Boot baseline, supported config database/store, Flyway/baseline strategy, AI/RAG secrets when enabled, stream/auth policy, and required host adapters.
10. Keep starter semantics in the starters. Do not patch a new host to redefine `x-ui`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/domain`, actions, capabilities, export, config headers, ETag, or AI contracts.
11. Create only the host-owned code needed for the domain: application bootstrap, dependency composition, security/origin policy, datasource properties, resources, tests, and documentation.
12. Validate with the smallest reliable command after inspecting which tests connect to a database. Local execution is limited to unit tests without a database. Use an explicitly assigned isolated remote Neon branch for database-backed tests; add real HTTP/schema proof when the task claims the runtime metadata endpoints work.

## Diagnose Missing UI Metadata After Dependency Changes

When `@UISchema` is present on DTOs but generated `x-ui` is absent or incomplete after a Spring Boot, Springdoc, Swagger Jakarta, or starter version change, read [openapi-metadata-troubleshooting.md](references/openapi-metadata-troubleshooting.md) to audit `CustomOpenApiResolver` ABI, OpenAPI 3.0 vs. 3.1 dialect wiring, and `ModelConverters` pipeline proofs before changing DTO annotations.

## Reference Resource Audit

When the user asks to make an existing backend resource an exemplar for future
hosts or migrations, do not stop at "it compiles" or "the endpoint exists".
Audit the complete Praxis contract and classify reusable findings before
changing code:

- For migration or reference-host work, use the consumer workspace's approved
  playbooks, phase gates, semantic-contract checkers, and reference-audit
  templates when they exist. Do not copy the newest pilot blindly. Classify the
  reusable backend shape first: read-only, partial mutable resource, full CRUD,
  workflow action, related surface, master-detail resource, shared related
  write, or blocked/deferred flow. A package marked not-reference-ready or
  control-only must not become a platform reference until the consumer gate is
  repaired and explicitly promotes it.
- Confirm the resource uses the narrowest canonical baseline that matches the
  real operation state: read-only, read + create/update, full CRUD,
  duplicate-draft, workflow action, related surface, or blocked/deferred.
- Verify response DTO, FilterDTO, command DTOs, option DTOs and lookup
  descriptors publish deliberate `@Schema`, `@UISchema`, validation,
  governance and options metadata. Public text must be semantic product
  documentation, not labels copied into descriptions.
- Execute or inspect focused runtime evidence for `/filter`, detail/by-ids,
  `/options/filter`, `/options/by-ids`, `/schemas/filtered`,
  `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain` when available,
  item/collection capabilities and HATEOAS links/actions.
- For each write-like operation, record whether it is implemented, blocked,
  deferred, not API, direct-table safe, or legacy/DB-backed required. Do not
  infer delete, duplicate, or workflow actions from a legacy button label.
- Check that private context and locators such as tenant/company, user,
  profile, session, SQL names, ROWID, package flags, and bridge internals stay
  server-side and do not appear in DTOs, schemas, option payloads or x-ui.
- For related tabs or child resources, prefer `@UiSurface` plus real
  resource/operation/schema paths. Host-specific links may be assembled locally
  when they are domain composition, but availability and schema semantics must
  still come from canonical Praxis/host services.
- Separate platform gaps from host gaps. If a recurring need belongs in
  `praxis-metadata-starter`, `praxis-config-starter`, shared starters, public
  docs, examples, or this skill, record/update the canonical owner instead of
  hiding the problem in the consumer host.
- Update handoff/parity artifacts after late-scope implementation. A resource
  is not a good reference if final docs contradict implemented endpoints or
  validated operation states.

## Skill Coverage

This skill is sufficient for ordinary Java host API work with `praxis-metadata-starter`: project bootstrap, Maven dependency wiring, resource-oriented CRUD/read APIs, DTOs, filters, schemas, OpenAPI discovery, capabilities, surfaces, options, cursor/locate, stats, and collection export.

*(In external Antigravity workspaces, full companion skills are available under `~/.gemini/praxis-skills/<skill-name>/SKILL.md` or `$CODEX_HOME/skills/<skill-name>/SKILL.md`.)*

Use companion Praxis skills when the API needs a specialized platform surface:

- Use `praxis-metadata-resource-baseline` when choosing resource-oriented controllers/services, `ResourceMapper`, filters, HATEOAS envelopes, export, stats, and canonical CRUD/read-only baselines.
- Use `praxis-metadata-schema-contracts` for `x-ui`, `/schemas/filtered`, schema hashes, OpenAPI operation resolution, ETag, and Angular schema consumption.
- Use `praxis-metadata-discovery-capabilities` for surfaces, actions, capabilities, `_links`, availability, related resources, stats, and export discovery.
- Use `praxis-metadata-domain-option-sources` for domain governance, field access, option sources, entity lookup, lookup/by-ids contracts, and semantic metadata review.
- Use `praxis-config-runtime-persistence`, `praxis-config-ai-registry-manifests`, `praxis-config-api-metadata-grounding`, `praxis-config-agentic-authoring-streaming`, or `praxis-config-domain-decisions` before adding `/api/praxis/config/**`, AI registry, RAG/API metadata, authoring, SSE, or governed decision surfaces.
- Use `praxis-api-quickstart-operational-proof`, `praxis-api-quickstart-security-config`, `praxis-api-quickstart-domain-pilots`, and `praxis-api-quickstart-cockpit-http-validation` when a host should mirror or validate against the reference operational proof.
- Use `praxis-http-examples-corpus-manifest`, `praxis-http-examples-contract-surfaces`, and `praxis-http-examples-llm-smoke` when a Java-host change must update executable HTTP examples, public corpus promises, or LLM-facing lanes.
- Use `praxis-landing-public-docs-contracts` and `praxis-landing-registries-sitemap-playgrounds` when the host change affects public docs, guides, examples, sitemap, LLM files, or landing projections.
- Use `praxis-dto-annotations` when filling or reviewing `@Schema`, `@UISchema`,
  `@Filterable`, `@DomainGovernance`, FieldControlType, PT-BR labels/help text, groups, icons,
  options, and DTO/OpenAPI documentation for hosts that consume `praxis-metadata-starter`.
- Use `praxis-resource-entity-lookup-backend` for governed `RESOURCE_ENTITY` lookup, `OptionSourceRegistry`, `LIGHT_LOOKUP`, `x-ui.optionSource`, provider policies, and option-source endpoints.
- Use `praxis-component-minimums` when the question is about the minimum frontend/host runtime wiring needed for Angular components to consume this backend.
- Use `praxis-dynamic-fields-editorial` when changing or validating control types, dynamic-field aliases, or Angular renderability beyond the Java/OpenAPI contract.
- Use `praxis-authoring-editors` only for authored UI/editor/config persistence workflows, not for ordinary backend resources.

Do not use consumer-specific fieldspec guidance for Praxis resources unless the task explicitly targets that legacy fieldspec stack. For Praxis APIs, `praxis-metadata-starter` annotations and contracts are the source of truth.

## Canonical Boundaries

- `praxis-metadata-starter` owns `x-ui`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain`, capabilities, OpenAPI enrichment, HATEOAS schema links, export contracts, governance metadata, and resource-oriented base contracts.
- `praxis-config-starter` owns `/api/praxis/config/**`, persisted UI config, AI registry, templates, config headers, config ETag, authoring/context contracts, and the governed boundary for semantic-decision authoring, simulation, approval, publication, and materialization when that feature set is in scope.
- The new host owns Spring Boot composition, dependency versions, datasource wiring, security policy, concrete domain resources, domain persistence, and downstream proof that selected starters work in a real service.
- `praxis-api-quickstart-public` is the preferred public reference host for external users and LLMs. `praxis-api-quickstart` local/private source is useful when available for platform development and comparison. Neither is a required checkout or the canonical owner of starter semantics.

## Schema And Decision Boundaries

- Treat `/schemas/filtered` as the structural schema source for UI/runtime consumption. Treat `/schemas/catalog` as documentation/discovery, `/schemas/surfaces` and `/schemas/actions` as semantic discovery, `/schemas/domain` as AI-operable domain vocabulary, and resource capabilities as aggregate availability snapshots. Do not use catalogs or capabilities as a second structural schema source.
- For AI or assistant features in a Java host, do not route primary user intent with keyword lists, regex command matching, or controller-local text heuristics. Expose canonical resources, tools, operation schemas, catalogs, surfaces, actions, capabilities, governed context, and config-starter contracts so semantic resolution can be LLM/governance-led and then grounded against those canonical candidates.
- If a required AI/config tool or contract is missing, model the tool or contract in the canonical owner, usually `praxis-config-starter` for authoring/config decisions or `praxis-metadata-starter` for metadata discovery. Do not compensate by adding host-local AI registries, patch formats, magic request fields, or string-routing shortcuts.
- Before adding a new host contract, inventory whether the platform already publishes the needed fact through DTO annotations, OpenAPI enrichment, `x-ui`, option sources, surfaces, actions, capabilities, domain catalog, config headers/ETag, quick replies, previews, diagnostics, or materializations. Classify the finding as already supported, poorly materialized, partial, or a real contract gap.

## Project Baseline

Use Java 21 unless the selected starter release documents a different baseline. Prefer Maven unless the target host already standardizes on Gradle.

When no local platform repo is present, do not inspect `praxis-metadata-starter` or `praxis-config-starter` source. Use the dependency's public package names, generated API docs, Maven dependency metadata, `javap` against resolved jars when necessary, and runtime HTTP validation.

Minimum dependencies for a CRUD host usually include:

- `spring-boot-starter-web`
- `spring-boot-starter-data-jpa`
- `spring-boot-starter-validation`
- `spring-boot-starter-actuator`
- `spring-boot-starter-security` when the host exposes real HTTP endpoints
- `praxis-metadata-starter`
- `praxis-config-starter` only when the host must provide `/api/praxis/config/**` and its required config-store/RAG/domain adapters
- database driver
- MapStruct and Lombok if following quickstart mapper/entity conventions
- `spring-boot-starter-test` for tests; use the selected PostgreSQL driver for assigned remote Neon database proof, not H2 or embedded/local database substitutes

In Maven, declare explicit starter versions unless the host imports a managed Praxis BOM or parent:

```xml
<properties>
    <praxis.core.version><!-- selected released version --></praxis.core.version>
</properties>

<dependency>
    <groupId>io.github.codexrodrigues</groupId>
    <artifactId>praxis-metadata-starter</artifactId>
    <version>${praxis.core.version}</version>
</dependency>
```

Application bootstrap must scan the host package and the metadata starter package:

```java
@SpringBootApplication(scanBasePackages = {
        "com.example.praxis.<host>",
        "org.praxisplatform.uischema"
})
```

Do not copy historical quickstart controllers literally. In the current starter, `@ApiResource` is the resource declaration and already supplies the necessary controller/request-mapping semantics; only add extra Spring stereotypes when the resolved starter version or target host pattern explicitly requires them.

If `praxis-config-starter` is in scope, treat it as a separate config-store boundary. Include `org.praxisplatform.config` scanning, config starter JPA repository/entity wiring, migrations/tables, and datasource configuration only when the host actually exposes `/api/praxis/config/**`. Do not point a legacy Oracle application datasource at the config store by accident; config/AI persistence normally needs its own supported store and baseline.

## Domain Documentation Rule

Do not generate `@Schema(description=...)` in bulk from labels, property names, or camelCase. Investigate each field and write domain descriptions deliberately: what the field represents, constraints, relationships, and business impact. Keep `@UISchema` for UI behavior and labels; keep `@Schema` as product/domain documentation.

Also write `@Operation`, `@ResourceIntent`, `@UiSurface`, and `@WorkflowAction` text as semantic product contract. These strings feed `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain`, capabilities snapshots, RAG, and LLM consumers. Do not rely on generic Springdoc fallback summaries for public resource operations.

## Deep Domain & Relational Synthesis Rule ("Além do Óbvio")

Do not act as a mechanical `1 table = 1 obvious CRUD` generator. Analyze the business domain and the relationship graph between entities (`@ManyToOne`, `@OneToMany`, `@Embedded`) to uncover non-obvious enterprise capabilities across 3 dimensions:
1. **Deep Filtering & Unified Broad Search (`@Filterable(relations = {...})`):** Every operational `FilterDTO` must include at least one broad/omnibox search field (`searchTerm` / `buscaAmpla` / `identificacaoOuFamiliar`) using `@Filterable(operation = FilterOperation.LIKE, relations = {"fullName", "socialName", "motherName", "fatherName", "dependents.fullName", "taxId"})` so users can search across name, surname, parent/dependent name, or ID in one input (`OR`), plus multi-operator coverage on the same attribute (`LIKE`+`STARTS_WITH`+`EQUAL`+`IN`, `BETWEEN`+`IN_LAST_DAYS`+`IN_NEXT_DAYS`, completeness `IS_NULL`/`IS_NOT_NULL`, collection cardinality `SIZE_GT`/`SIZE_EQ`) and multi-level cross-entity paths (`relation = "department.costCenter.region"`).
2. **Exhaustive Bulking Discovery Across All 3 Modes:** Audit 100% of mutable attributes instead of picking 2–3 obvious fields: enable `BulkMode.UNIFORM_UPDATE` on all collective standardization fields (unit, cost center, shift, regime/plan, payment/bank, manager, flags); enable `BulkMode.PER_ITEM_UPDATE` broadly on inline batch-grid revision fields (phones, emails, addresses, bank accounts, individual amounts/limits, external codes, per-item dates); and analyze entity relationships and lifecycle to create collective `BulkMode.DOMAIN_COMMAND` `@WorkflowAction(scope = ActionScope.COLLECTION)` operations (batch relocation across units, batch approval/homologation, batch suspension/reactivation, parametric revision).
3. **New Cross-Entity Endpoints & Subdomain Intents:** Create dedicated read-only analytical/consolidated endpoints (`AbstractReadOnlyResourceController`) when entity relationships answer cross-table operational questions (vacancy/occupancy matrices, expiring-items radar, compliance audits), expose all `1:N` child collections as 360° surfaces (`@UiSurface` + `relatedChildResourceKey`), and decompose broad entities into persona-oriented `@ResourceIntent` (`PATCH` + `SurfaceKind.PARTIAL_FORM`) endpoints.

For sensitive fields or fields that should guide AI/RAG behavior, use `@DomainGovernance`, `AiUsagePolicy`, and `AiUsageMode` deliberately. Validate that governance appears in `x-domain-governance` on `/schemas/filtered` and is reflected in `/schemas/domain` when the host publishes the domain catalog.

## Validation

Prefer focused validation:

- New host scaffold or resource compile proof: select the host's unit tests that do not open database connections; use `mvn -B test` only after confirming its complete selection is database-free or all database cases use the reviewed Neon assignment.
- Published dependency proof for external hosts: resolve starter artifacts with Maven metadata or `mvn dependency:get`, preferably using a temporary local Maven repository when the task must prove no monorepo dependency.
- Metadata/public contract proof: add or run a focused `@SpringBootTest`/MockMvc or TestRestTemplate test for `/v3/api-docs`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain` when available, resource filter, options, actions, and capabilities.
- Config starter proof: assign isolated remote Neon API/Config resources explicitly, verify project/child/endpoint/PostgreSQL identity and client TLS before connecting, and prove the real owner/runtime/control-plane privileges and memberships required by the flow. Keep credentials private, bound fixture writes and cleanup to the assignment, preserve inherited data, and test `/api/praxis/config/**` with the host's required headers/origin. A privileged fixture is not proof of the ordinary runtime path; do not disable migrations merely to imitate an old local fixture.
- Dependency/version change: confirm Maven resolution and run at least the host's test phase.
- For a full resource proof, execute the endpoints the UI/runtime will rely on: `/filter`, `/filter/cursor`, `/locate`, `/options/filter`, `/options/by-ids`, option-source endpoints when registered, `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces?resource=...`, `/schemas/actions?resource=...`, `/schemas/domain` when available, collection and item `/capabilities`, collection and item `/actions`, item `/surfaces`, configured `/stats/*`, and `/export` when collection export is supported.

Do not copy historical H2, embedded PostgreSQL or Testcontainers fixtures from
reference hosts or checklists into a new database proof. A reference host may
still contain unmigrated local database tests in its broad Maven/release gate;
record that gap and migrate or compose the complete required case matrix on
assigned Neon resources before release. Removing those tests, accepting skips,
or replacing them with a focal SDK-adoption or cold-start proof does not close
the broad release gate. Unit and focal passes remain evidence only for their
stated scope. Follow the owning repository's actual private and sanitized-public
release gates, retaining source/dependency identity, raw reports and cleanup.

When validation is partial, state exactly what ran and what remains unvalidated.

## References

- Read `references/resource-baseline.md` before implementing concrete resources (contains the exact generic signatures, starter imports, and the complete 1-Shot Golden Path code template).
- Read `references/host-checklist.md` before finalizing a scaffold or reporting completion.
- Read `references/openapi-metadata-troubleshooting.md` when diagnosing missing `x-ui` metadata after Spring Boot, Springdoc, or starter version changes.
- When local platform docs are available, use `praxis-metadata-starter/docs/guides/GUIA-01-AI-BACKEND-APLICACAO-NOVA.md`, `GUIA-02-AI-BACKEND-CRUD-METADATA.md`, `GUIA-04-QUANDO-USAR-RESOURCE-SURFACE-ACTION-CAPABILITY.md`, `GUIA-05-DO-CRUD-AO-CONTRATO-SEMANTICO.md`, `GUIA-06-REDACAO-SEMANTICA-DE-ANNOTATIONS-PARA-IA.md`, `FILTROS-E-PAGINACAO.md`, `OPTIONS-ENDPOINT.md`, and `COLLECTION-EXPORT.md` as supporting references for gaps not covered here.
