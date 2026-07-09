---
name: praxis-java-host-project
description: Create or evolve Java/Spring Boot backend host projects for the Praxis platform using published Maven starter dependencies by default. Use when Codex must scaffold a new Praxis Java microservice, choose Praxis starter versions, wire praxis-metadata-starter or praxis-config-starter, create resource-oriented controllers/services/DTOs, adapt reference host patterns when available, or validate a host publishes canonical Praxis metadata surfaces such as /schemas/filtered, /schemas/domain, ApiResource, x-ui, actions, capabilities, export, and /api/praxis/config/**.
---

# Praxis Java Host Project

## Overview

Use this skill to create a new Java host that composes the Praxis platform correctly instead of inventing local contracts. Treat published Praxis starters as external Maven dependencies by default; use local starter source only when it is actually present and the task is platform-development work.

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
6. Generate resource files in dependency order. For a new application prefer `ApiPaths`, entity/projection, repository, DTOs, mapper, service, controller. For an existing application adding a resource, prefer DTOs, repository, mapper, service, controller, and only then surfaces, intents, actions, export, or analytics.
7. Use the canonical resource-oriented baseline for new resources:
   - `@ApiResource(value=..., resourceKey=...)`;
   - `@ApiGroup(...)` when grouping is meaningful;
   - `AbstractResourceController` or a project-local thin subclass around it;
   - `AbstractBaseResourceService` or a project-local thin subclass around it;
   - `AbstractReadOnlyResourceController` and `AbstractReadOnlyResourceService` for read-only views/projections;
   - `BaseCrudRepository`;
   - `ResourceMapper` as the service boundary, implemented directly or adapted through a thin host-local wrapper;
   - mutable resources: response DTO, create DTO, update DTO, and filter DTO with deliberate `@Schema` and `@UISchema`;
   - read-only resources: response DTO and filter DTO only.
8. Include `praxis-config-starter` only when the host must expose `/api/praxis/config/**` or AI authoring/config-store surfaces and can provide the required config-store datasource, migrations/tables, and host adapters. Do not include it for a metadata/filter-only service. Before adding it, confirm the target host meets the starter's release prerequisites such as compatible Spring Boot baseline, supported config database/store, Flyway/baseline strategy, AI/RAG secrets when enabled, stream/auth policy, and required host adapters.
9. Keep starter semantics in the starters. Do not patch a new host to redefine `x-ui`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/domain`, actions, capabilities, export, config headers, ETag, or AI contracts.
10. Create only the host-owned code needed for the domain: application bootstrap, dependency composition, security/origin policy, datasource properties, resources, tests, and documentation.
11. Validate with the smallest reliable command. For a new host, start with `mvn -B test`; add HTTP/schema smoke tests when the task claims the runtime metadata endpoints work.

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

Use companion Praxis skills when the API needs a specialized platform surface:

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
- `praxis-config-starter` owns `/api/praxis/config/**`, persisted UI config, AI registry, templates, config headers, config ETag, and authoring/context contracts.
- The new host owns Spring Boot composition, dependency versions, datasource wiring, security policy, concrete domain resources, domain persistence, and downstream proof that selected starters work in a real service.
- `praxis-api-quickstart-public` is the preferred public reference host for external users and LLMs. `praxis-api-quickstart` local/private source is useful when available for platform development and comparison. Neither is a required checkout or the canonical owner of starter semantics.

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
- `spring-boot-starter-test` and H2 for isolated tests

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

For sensitive fields or fields that should guide AI/RAG behavior, use `@DomainGovernance`, `AiUsagePolicy`, and `AiUsageMode` deliberately. Validate that governance appears in `x-domain-governance` on `/schemas/filtered` and is reflected in `/schemas/domain` when the host publishes the domain catalog.

## Validation

Prefer focused validation:

- New host scaffold or resource compile proof: `mvn -B test`.
- Published dependency proof for external hosts: resolve starter artifacts with Maven metadata or `mvn dependency:get`, preferably using a temporary local Maven repository when the task must prove no monorepo dependency.
- Metadata/public contract proof: add or run a focused `@SpringBootTest`/MockMvc or TestRestTemplate test for `/v3/api-docs`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain` when available, resource filter, options, actions, and capabilities.
- Config starter proof: include H2 datasources for both app and config datasource, disable Flyway when appropriate, and test `/api/praxis/config/**` with the host's required headers/origin.
- Dependency/version change: confirm Maven resolution and run at least the host's test phase.
- For a full resource proof, execute the endpoints the UI/runtime will rely on: `/filter`, `/filter/cursor`, `/locate`, `/options/filter`, `/options/by-ids`, option-source endpoints when registered, `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces?resource=...`, `/schemas/actions?resource=...`, `/schemas/domain` when available, collection and item `/capabilities`, collection and item `/actions`, item `/surfaces`, configured `/stats/*`, and `/export` when collection export is supported.

When validation is partial, state exactly what ran and what remains unvalidated.

## References

- Read `references/resource-baseline.md` before implementing concrete resources.
- Read `references/host-checklist.md` before finalizing a scaffold or reporting completion.
- When local platform docs are available, use `praxis-metadata-starter/docs/guides/GUIA-01-AI-BACKEND-APLICACAO-NOVA.md`, `GUIA-02-AI-BACKEND-CRUD-METADATA.md`, `GUIA-04-QUANDO-USAR-RESOURCE-SURFACE-ACTION-CAPABILITY.md`, `GUIA-05-DO-CRUD-AO-CONTRATO-SEMANTICO.md`, `GUIA-06-REDACAO-SEMANTICA-DE-ANNOTATIONS-PARA-IA.md`, `FILTROS-E-PAGINACAO.md`, `OPTIONS-ENDPOINT.md`, and `COLLECTION-EXPORT.md` as supporting references for gaps not covered here.
