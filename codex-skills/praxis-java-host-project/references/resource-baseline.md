# Resource Baseline

Use this reference when implementing concrete resources in a new Praxis Java host.

## Required Shape

- Import contracts from the resolved starter dependency. Do not assume source files are present next to the host.
- Define public paths in an `ApiPaths` class. Do not scatter path literals.
- Annotate controllers with `@ApiResource(value = ApiPaths..., resourceKey = "...")`.
- Use stable `resourceKey` values such as `administracao-pessoal.colaboradores`; they are public identity, not local labels.
- Use `@ApiGroup` when the group becomes part of public OpenAPI discovery.
- Use `BaseCrudRepository<E, ID>` for CRUD resources.
- Use `AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` or a thin host-local subclass.
- Use `AbstractReadOnlyResourceService<E, ResponseDTO, ID, FilterDTO>` and `AbstractReadOnlyResourceController<ResponseDTO, ID, FilterDTO>` for database views, analytics projections, read models, and resources that must not publish create/update/delete.
- Use `ResourceMapper<E, ResponseDTO, CreateDTO, UpdateDTO, ID>` as the service boundary. A concrete mapper may implement the interface directly, or a thin host-local base service may adapt MapStruct methods/functions to a `ResourceMapper`.
- Prefer MapStruct for DTO/entity conversion when the host has multiple resources.
- Host-local base classes are allowed when they stay thin and pedagogical, as in the quickstart pattern: they may centralize repeated mapper wiring, stats OpenAPI examples, dataset-version defaults, or HATEOAS helpers, but they must still extend/delegate to the Praxis base controller/service and must not redefine resource semantics.
- Do not add `@RestController` by reflex. Inspect the resolved starter and the target host's existing controller pattern. Some reference hosts may carry `@RestController` for historical or local reasons; a new host should follow the current starter/reference guidance for its version and avoid duplicate stereotype annotations when `@ApiResource` already supplies the required controller semantics.

## Generation Inputs And Order

Before generating code, obtain or infer:

- base package and module package;
- entity or projection name, ID type, mutability/read-only mode, and table/view source;
- `resourcePath`, stable `resourceKey`, and `@ApiGroup`;
- DTO fields, validation constraints, relationships, option labels, sensitive fields, and domain descriptions;
- filter fields and `Filterable.FilterOperation` choices;
- whether options, option-sources, stats, export, surfaces, resource intents, or workflow actions are actually required.

Safe generation order for a new application is `ApiPaths`, entity/projection, repository, DTOs, mapper, service, controller. Safe order for adding a resource to an existing host is DTOs, repository, mapper, service, controller, then optional surfaces/intents/actions/stats/export.

## Praxis Metadata Feature Coverage

For each resource, decide explicitly which Praxis metadata features are in scope:

| Feature | Host responsibility |
| --- | --- |
| OpenAPI and `x-ui` | Add deliberate `@Schema`, `@UISchema`, `@Filterable`, `@ApiResource`, and `@ApiGroup`. |
| `/schemas/filtered` | Ensure request/response DTOs are discoverable from the generated OpenAPI operation. |
| `/filter` | Implement a `GenericFilterDTO` with valid `@Filterable` operations and verify pageable SQL against the target database. |
| `/options/filter` and `/options/by-ids` | Ensure the entity has a stable id and option label, commonly with `@OptionLabel`; use `praxis-resource-entity-lookup-backend` for governed cross-resource lookups. |
| `/filter/cursor` | The starter provides baseline cursor behavior; validate sort stability and generated SQL. Override only for keyset, dialect, performance, or domain-specific behavior. |
| `/locate` | Override `locate` in the service when the UI needs position restoration. |
| `/stats/*` | Override stats support modes and publish `StatsFieldRegistry`; validate payload shape and SQL. |
| `/export` | Publish only when the service implements collection export support, capability, executor, field allowlist, limits, and truncation/audit metadata. |
| `/capabilities` | Treat as advertised capability snapshot; still execute the endpoint it advertises. |
| `/surfaces` and `/actions` | Use starter defaults only when they match the real UX contract; otherwise register/implement the required domain semantics deliberately. |
| `/schemas/domain` | Derived semantic/domain vocabulary and AI-operable catalog. Improve real DTO, operation, surface, action, and governance annotations; do not treat it as a structural schema source. |
| `/api/praxis/config/**` | Out of scope unless `praxis-config-starter` is intentionally included and wired. |

## DTO Rules

- Response DTOs describe the public resource state.
- Create DTOs should exclude server-owned identifiers, commonly with `@JsonIgnoreProperties({"id"})`.
- Update DTOs should express editable fields for an existing resource.
- Read-only resources should not generate create/update DTOs unless there is a real write operation elsewhere; do not expose mutable endpoints for views/projections just to satisfy a generic CRUD template.
- Filter DTOs implement `GenericFilterDTO` and use `@Filterable` on filterable fields.
- `@Schema(description=...)` must be written manually with domain semantics.
- `@UISchema` can carry labels, control hints, grouping, ordering, max length, and help text, but it is not a substitute for domain documentation.
- When using `FieldControlType` or `Filterable.FilterOperation`, verify enum values against the resolved starter jar or official docs for the target version. Common valid names include `DATE_PICKER` and `EQUAL`; do not guess aliases such as `DATEPICKER` or `EQUALS`.
- For control types expected to render in the official Angular runtime, verify runtime support with the appropriate Praxis UI/dynamic-fields guidance when there is any doubt. Java enum presence alone is not proof of frontend renderability.

## Filter Rules

- Model filters through the canonical Praxis mechanism first: `FilterDTO implements GenericFilterDTO` plus one `@Filterable(operation = Filterable.FilterOperation.<OP>)` per filterable field.
- Do not create host-local filter DSLs, ad hoc query parameters, custom request payload shapes, manual JPA `Specification` builders, or controller-specific predicate logic when the requirement fits a built-in `FilterOperation`.
- Treat `Filterable.FilterOperation` as the operation vocabulary. The metadata starter currently provides 26 built-in operations: `EQUAL`, `NOT_EQUAL`, `LIKE`, `NOT_LIKE`, `STARTS_WITH`, `ENDS_WITH`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL`, `IN`, `NOT_IN`, `BETWEEN`, `IS_NULL`, `IS_NOT_NULL`, `BETWEEN_EXCLUSIVE`, `NOT_BETWEEN`, `OUTSIDE_RANGE`, `ON_DATE`, `IN_LAST_DAYS`, `IN_NEXT_DAYS`, `SIZE_EQ`, `SIZE_GT`, `SIZE_LT`, `IS_TRUE`, and `IS_FALSE`.
- Use `relation = "entity.path"` when the DTO field is an operational alias or targets a nested entity property, for example `statusIn` with `IN` and `relation = "status"`, or `departamentoNome` with `LIKE` and `relation = "departamento.nome"`.
- Use the canonical payload shapes expected by the starter: lists for `IN`/`NOT_IN`, range lists or supported range objects for `BETWEEN`-family operations, `Boolean.TRUE` activation for null checks, and `Integer` day counts for relative date operations.
- Add custom filtering only after proving the needed predicate cannot be expressed with the starter operation vocabulary. Keep such exceptions inside the service/repository boundary, document the reason, and avoid changing the public `/filter` contract shape unless the starter contract itself is being evolved.

## Controller Rules

Expose the inherited endpoints deliberately. For a minimal scaffold, a controller can inherit most behavior from `AbstractResourceController` and override only:

- `getService()`
- `getResponseId(ResponseDTO dto)`

Add explicit endpoint methods only when the host needs richer public OpenAPI documentation or domain-specific behavior over inherited routes. When adding them, write deliberate `@Operation` summaries/descriptions and keep paths aligned with starter conventions such as `/filter`, `/filter/cursor`, `/locate`, `/options/filter`, `/options/by-ids`, item detail, collection capabilities, and item capabilities.

For read-only resources, use the read-only controller baseline and do not publish write endpoints. The expected public surface should still include structural discovery, filter, options when supported, baseline cursor when validated, locate when implemented, stats when registered, and capabilities.

`@ResourceIntent`, `@UiSurface`, and `@WorkflowAction` must annotate real HTTP operations:

- Use `@ResourceIntent` for partial maintenance that remains inside the resource contract, such as `PATCH /{id}/profile`.
- Use `@UiSurface` for semantic discovery of an experience over a real operation; it does not define a separate payload or schema.
- Use `@WorkflowAction` only for explicit business commands, not for ordinary CRUD or partial resource maintenance.
- For item-level read/projection surfaces, set and validate `responseCardinality` against the real response shape, especially when an item endpoint returns a related collection.
- If `allowedStates`, `requiredAuthorities`, or contextual availability depend on real item state, provide a `ResourceStateSnapshotProvider`, `ActionAvailabilityRule`, or `SurfaceAvailabilityRule`; otherwise state that availability is static and validate the resulting `availability` decision in item surfaces/actions/capabilities.
- Keep `/schemas/filtered` as the structural source for request/response schemas. `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain`, and capabilities are discovery or aggregate surfaces.

## Service Rules

- Implement resource services as Praxis services first, not as generic Spring services. The normal shape is a concrete class extending `AbstractBaseResourceService<E, ResponseDTO, ID, FilterDTO, CreateDTO, UpdateDTO>` or a thin host-local abstraction that still delegates to the Praxis base service.
- Keep the controller thin and let the base service handle standard list/detail/create/update/delete/filter/options behavior through `BaseCrudRepository`, `ResourceMapper`, and the typed DTO set.
- Do not reimplement ordinary CRUD, pageable filter, options id/label, schema metadata, or capability behavior in the service when the base resource service already provides it.
- Keep domain update semantics explicit in `applyUpdate`; do not blindly replace persistent entities.
- Keep mapper semantics at the `ResourceMapper` boundary. Avoid hand-mapping DTOs throughout service methods except for small, explicit domain exceptions.
- Override `getIdFieldName()` when the public DTO identifier is not named `id`, for example a legacy business key such as `companyCode`. Also keep `getResponseId(...)` aligned in the controller. Otherwise `/schemas/filtered` and Praxis UI may report or consume a divergent `x-ui.resource.idField`.
- Implement `getDatasetVersion()` when the host can provide a cheap stable version such as `EntityName:count` or a real update marker.
- Register option sources only when fields actually need governed entity lookup. Do not publish provider internals in public payloads.
- Treat cursor pagination, locate, and stats according to their actual support model. Cursor pagination has a baseline implementation but still needs runtime proof for sort stability, SQL, and page continuity; override it only for keyset/dialect/performance/domain behavior. `locate` is opt-in and must be implemented when the UI needs jump-to-row or position restoration. Stats require support modes plus `getStatsFieldRegistry()` before claiming `/stats/*` works.
- Add host-specific service methods only for real domain commands or integration behavior that is not covered by the resource baseline. Do not add `buscarPorNome`, `filtrar`, `listarPorStatus`, or similar methods when the same behavior belongs in the `FilterDTO` with `@Filterable`.
- For collection export, do not rely on frontend-provided fields or `maxRows` as authority. The service must declare `supportsCollectionExport()`, return `getCollectionExportCapability()`, enforce server-side field allowlists and row limits, apply the resource filter/security rules, and use the canonical export executor or an equivalent governed engine.
- Validate advertised capabilities against HTTP. Do not rely only on OpenAPI or `/capabilities`; execute `/filter`, `/filter/cursor`, `/locate`, `/stats/*`, `/options/*`, `/export` when supported, `/schemas/filtered`, `/schemas/domain` when available, item/collection capabilities, item surfaces, and item actions for the resource under test.
- For legacy Oracle or other constrained databases, validate generated SQL for pageable filters and stats early. Dialect mismatch is a host integration issue until proven to be a starter defect.

## Semantic Text Rules

- Write `@Operation(summary=..., description=...)` for public resource endpoints when they are explicitly declared in the host. Omission is acceptable for inherited endpoints or not-yet-curated scaffolds only, and should be treated as a documentation gap before the resource becomes a public reference.
- Make summaries and descriptions describe the business operation, real fields/dimensions, constraints, effects, and relationships. Do not describe only the HTTP verb, pagination, or endpoint path.
- `@Schema.description` is domain documentation for each DTO/property. `@UISchema.label` is UI text and must not be used as a source for generated `@Schema` descriptions.
- For `@ResourceIntent`, `@UiSurface`, and `@WorkflowAction`, keep `id`, `title`, `intent`, `tags`, `scope`, and descriptions stable and aligned with the real method, DTO, service behavior, allowed states, and authorities.
- Preserve stable `operationId` when exposed, use OpenAPI tags as real domain grouping, and keep `@ExampleObject` or examples aligned with validation and actual use cases. These values are indexed by catalog/RAG surfaces and should not be filler.
- For fields with privacy, compliance, AI usage, security, finance, identity, or policy relevance, add deliberate `@DomainGovernance`, `AiUsagePolicy`, or `AiUsageMode` metadata and verify it in `x-domain-governance` and `/schemas/domain`.
- Avoid negative descriptions that introduce unrelated domain terms and pollute semantic search. Do not promise fields, workflow effects, permissions, or integrations not implemented by the endpoint.

## Tests

For a new resource, prefer at least:

- compile/test phase for mapper and generics correctness;
- Maven dependency resolution against the artifact repository used by the host;
- a schema smoke for the create or filter DTO when runtime proof is in scope;
- a resource filter or options smoke when the UI/runtime will consume it immediately.
