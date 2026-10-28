---
name: praxis-metadata-resource-baseline
description: Use when working on praxis-metadata-starter resource-oriented backend patterns (either inside the starter or in a consuming Java host): AbstractResourceController, AbstractReadOnlyResourceController, AbstractCollectionCommandResourceController, AbstractResourceQueryController, AbstractBaseResourceService, AbstractReadOnlyResourceService, ResourceMapper, RestApiResponse, HATEOAS links, filters, stats, export, or canonical resource CRUD hierarchy.
---

# Praxis Metadata Resource Baseline

Use this skill for the resource-oriented backend hierarchy owned by `praxis-metadata-starter`.

## Operating Mode & Source Audit

Determine whether you are operating in **Platform Source Mode** or **Consumer Host Mode**:

- **Platform Source Mode (`praxis-metadata-starter` checkout present in the workspace):**
  Inspect the starter before editing:
  - `praxis-metadata-starter/AGENTS.md`
  - `praxis-metadata-starter/README.md`
  - `src/main/java/org/praxisplatform/uischema/annotation/ApiResource.java`
  - `src/main/java/org/praxisplatform/uischema/annotation/ApiGroup.java`
  - `src/main/java/org/praxisplatform/uischema/controller/base/AbstractResourceQueryController.java`
  - `src/main/java/org/praxisplatform/uischema/controller/base/AbstractReadOnlyResourceController.java`
  - `src/main/java/org/praxisplatform/uischema/controller/base/AbstractCreateUpdateResourceController.java`
  - `src/main/java/org/praxisplatform/uischema/controller/base/AbstractCollectionCommandResourceController.java`
  - `src/main/java/org/praxisplatform/uischema/controller/base/AbstractResourceController.java`
  - `src/main/java/org/praxisplatform/uischema/service/base/AbstractBaseQueryResourceService.java`
  - `src/main/java/org/praxisplatform/uischema/service/base/AbstractReadOnlyResourceService.java`
  - `src/main/java/org/praxisplatform/uischema/service/base/AbstractBaseResourceService.java`
  - `src/main/java/org/praxisplatform/uischema/mapper/base/ResourceMapper.java`
  - `src/main/java/org/praxisplatform/uischema/rest/response/RestApiResponse.java`
- **Consumer Host / Published Dependency Mode (`io.github.codexrodrigues:praxis-metadata-starter` consumed via Maven):**
  Do not search for `src/main/java/org/praxisplatform/uischema/**` on disk. Pair with `praxis-java-resource-authoring` and `praxis-java-host-project`, inspect the host's `pom.xml`, controllers, services, mappers, DTOs, and resolved starter classes on the classpath (or via `javap` when needed), and validate through the host's focused tests and HTTP endpoints.

## Canonical Boundary

`praxis-metadata-starter` owns the canonical resource baseline:

```text
@ApiResource(value = "...", resourceKey = "...", title = "...", description = "...", icon = "...", identity = @ResourceIdentity(...), quickFilters = {...})
BaseCrudRepository<E, ID>
ResourceMapper<E, ResponseDTO, CreateDTO, UpdateDTO, ID>  (applyUpdate(E entity, UpdateDTO dto))
AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>
AbstractReadOnlyResourceService<E, ResponseDTO, ID, FilterDTO>
AbstractResourceController<ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>
AbstractReadOnlyResourceController<ResponseDTO, ID, FilterDTO>
AbstractCollectionCommandResourceController
RestApiResponse<T> with HATEOAS _links and metadata headers
```

`AbstractCrudController`, `AbstractReadOnlyController`, `BaseCrudService`, `AbstractBaseCrudService`, and legacy mapper patterns are migration surfaces only. Do not start new resources on legacy hierarchies unless the task is explicitly maintaining a legacy test or compatibility boundary.

## Decision Rules

- Choose `AbstractReadOnlyResourceController` and `AbstractReadOnlyResourceService` for query/read-only resources, projections, views, and analytical datasets.
- Choose `AbstractResourceController` and `AbstractBaseResourceService` for mutable resources with separate `ResponseDTO`, `CreateDTO`, `UpdateDTO`, and `FilterDTO`.
- Choose `AbstractCreateUpdateResourceController` or `AbstractUnitDeleteResourceController` only when the resource intentionally omits full delete or batch delete semantics.
- Choose `AbstractCollectionCommandResourceController` when an `@ApiResource` exposes only collection-level `@WorkflowAction` commands and has no query, read-by-id, options, stats, export, or CRUD service. Do not invent an in-memory query service or placeholder CRUD endpoints just to register `/actions` and `/capabilities`.
- Keep `resourceKey` stable, semantic, and aligned with controller path, surfaces, actions, capabilities, and domain catalog entries.
- Preserve `RestApiResponse`, `_links`, `X-Data-Version`, ETag, and schema link generation from the base controllers. Do not wrap responses in a host-local envelope.
- Preserve `ResourceMapper` as the entity/DTO boundary. Do not leak JPA entities into public responses or OpenAPI schemas.
- `ResourceMapper.applyUpdate` must update the managed entity loaded by the route without overwriting its route-owned technical identity from a missing or divergent payload id. Do not compensate for mapper identity bugs in the controller or in Angular.
- **Native Composite Primary Keys (`@EmbeddedId` / `CompositeResourceId`) and `@Embedded` value objects:** `praxis-metadata-starter` supports `@EmbeddedId` composite keys (e.g., `@Embeddable public record VinculoId(Long numfunc, Integer numvinc) implements CompositeResourceId {}`) as the `ID` type parameter of `BaseCrudRepository<E, ID>`, `ResourceMapper<..., ID>`, `AbstractBaseResourceService<..., ID, ...>`, and `AbstractResourceController<..., ID, ...>`. On the HTTP/JSON/OpenAPI wire, composite IDs are serialized and deserialized as canonical colon-delimited strings (`"1001:1"`, with `%3A`/`%25` escaping for colons/percents) across `@PathVariable`, `@RequestParam` (`ids`, `includeIds`), `OptionDTO<ID>`, `RESOURCE_ENTITY` option sources, `@Filterable(relation = "id.numfunc")` / `@Filterable(relation = "vinculo.id")`, stats (`JpaStatsQueryExecutor`), HATEOAS `_links`, ETag, and `BulkIdentityCodecs.composite(VinculoId.class)`. Use `@EmbeddedId` for **immutable** natural/composite domain keys (such as `VINCULOS (numfunc, numvinc)` or `DEPENDENTES (numfunc, numdep)`), and use a surrogate `id BIGINT` + `UNIQUE` business constraint for **mutable** event tables where the user can edit the date or event code in `PUT /{id}` (since JPA forbids mutating `@EmbeddedId` fields on a managed instance).
- Keep ordinary CRUD in the resource baseline; model non-CRUD business transitions with `@WorkflowAction` and composed UI journeys with `@UiSurface`.
- Before persisting a resource write, verify that the persistence context is clean and bound so a mapper lookup or repository query cannot autoflush caller-owned entity mutations ahead of governance or validation.
- Keep controller/base, service/base, mapper, response envelope, and tests aligned in the same change.
- All resource stats endpoints (`groupByStats`, `timeSeriesStats`, `distributionStats`, `comparisonStats`) in `AbstractBaseQueryResourceService` must resolve their base specification via `resolveResourceFilterQuery(request.filter(), Pageable.unpaged()).effectiveSpecification()` so row-level access scope (`resolveResourceFilterAccessScope()`) is enforced identically to `filter()`.
- Multidimensional `group-by` (`dimensions[]` with `StatsDimensionExtraction`, finite-domain `fillGaps`, and `AVG_PER_CYCLE_OCCURRENCE`) belongs to the canonical `POST /{resource}/stats/group-by` contract (`GroupByStatsRequest` / `GroupByStatsResponse`); do not create bespoke heatmap or cross-tab endpoints per resource.
- Treat legacy classes as migration surfaces unless the local AGENTS says otherwise.

## No Keyword Routing

Do not infer resource operations, CRUD mode, capabilities, or workflow intent from controller names, method words, labels, or route regexes. Resolve behavior from `@ApiResource`, controller hierarchy, OpenAPI operations, `@UiSurface`, `@WorkflowAction`, and capability snapshots.

## Adherence Inventory

Before adding a new base controller method, response field, filter endpoint, export mode, or stats hook, classify the need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public baseline contract.

## Validation

- **In Platform Source Mode (`praxis-metadata-starter`):**
  - resource CRUD/query/hypermedia: `mvn "-Dtest=AbstractResourceControllerMappedCrudTest,ResourceControllerStatsAndLocateTest,HypermediaDiscoveryE2ETest,HateoasAndPayloadSizeE2ETest" test`
  - filters/pagination: `mvn "-Dtest=GenericSpecificationsBuilderTest,FilterRequestBodyAdviceTest,PageableBuilderTest" test`
  - export: `mvn "-Dtest=CollectionExportControllerTest,AbstractBaseQueryResourceServiceCollectionExportTest,CollectionExportExecutorTest" test`
  - downstream proof when public contracts change: `QuickstartMetadataMigrationIntegrationTest` or `EventosFolhaPilotIntegrationTest` in `praxis-api-quickstart`.
- **In Consumer Host Mode:**
  - run the host's focused resource controller/service/MockMvc tests verifying `/filter`, CRUD/actions, `RestApiResponse._links`, `/schemas/filtered`, and `/capabilities`.

For public baseline changes, review README, guides, quickstart docs/examples, Angular `GenericCrudService`, and HTTP examples. Keep the opening and quickstart sections of `README.md` focused on onboarding and canonical architecture; record incremental RC/candidate checkpoints in `docs/technical/BULK-AND-RELEASE-CANDIDATES-STATUS.md` or dedicated technical docs. State explicitly when no derived artifact is affected.

## Companion Skills

*(In external Antigravity workspaces, full companion skills are available under `~/.gemini/praxis-skills/<skill-name>/SKILL.md` or `$CODEX_HOME/skills/<skill-name>/SKILL.md`.)*

- Use `praxis-java-resource-authoring` and `praxis-java-host-project` when implementing or scaffolding resources in a Java host.
- Use `praxis-metadata-schema-contracts` for `/schemas/filtered`, `x-ui`, ETag, and `X-Schema-Hash`.
- Use `praxis-metadata-discovery-capabilities` for `@UiSurface`, `@WorkflowAction`, `/schemas/surfaces`, `/schemas/actions`, and `/capabilities`.
- Use `praxis-metadata-domain-option-sources` and `praxis-dto-annotations` for DTO, filter, governance, and option-source contracts.
- Use `praxis-core-resource-runtime` when verifying Angular `GenericCrudService` consumption.
