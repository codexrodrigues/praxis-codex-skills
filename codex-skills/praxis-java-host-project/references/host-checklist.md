# Host Checklist

Use this reference before finalizing a new Praxis Java host scaffold.

## Bootstrap

- Java version matches the reference host release train.
- Maven resolves Praxis starters from the configured artifact repository. Do not require the starter source repository to exist in the same workspace.
- For external/consumer hosts, starter versions are proven against the configured artifact repository or Maven Central; do not assume a local quickstart version is published.
- Maven properties pin explicit released versions, such as `praxis.core.version`; include `praxis.config.version` only when the host intentionally uses `praxis-config-starter`.
- When a local `praxis-api-quickstart` checkout is unavailable, use `https://github.com/codexrodrigues/praxis-api-quickstart-public` as the preferred public reference if needed, plus the user request, existing host dependency management, Maven metadata, release notes, or organization standards. Do not block scaffolding merely because the private/local reference host is absent.
- When using the public quickstart as reference in docs, prompts, or repeatable validation, prefer a tag or pinned commit over a floating `main` branch.
- `@SpringBootApplication(scanBasePackages=...)` includes the host package and `org.praxisplatform.uischema`. Include `org.praxisplatform.config` only for hosts that intentionally expose config/AI surfaces and have the required config-store wiring.
- Hosts using `praxis-config-starter` have explicit config-store JPA/entity/repository wiring, datasource properties, migrations/tables, and baseline policy. Do not reuse a legacy application datasource as the config store without an explicit architecture decision.
- Datasource properties are environment-driven for real deployments.
- Test profile or test annotations use H2 or another isolated local datasource.
- Hosts that read an existing legacy database they do not migrate should set an explicit Flyway policy. For Oracle 11.2 or other unsupported legacy engines, disable Flyway in that host (`spring.flyway.enabled=false`) instead of letting auto-configuration fail or attempt ownership of the schema.
- For Oracle 11.2, add `org.hibernate.orm:hibernate-community-dialects` and set `spring.jpa.database-platform=org.hibernate.community.dialect.Oracle10gDialect`. Hibernate's standard `OracleDialect` can generate `offset ... fetch first`, which Oracle 11.2 rejects.

## Source Availability

- Published dependency mode is the default for consumer hosts. Use public API types, dependency metadata, compiled jars, and runtime behavior.
- Local source mode is only for platform development, suspected starter defects, or explicit requests to change the starter.
- If source is absent and an API detail is unclear, inspect the resolved jar (`jar tf`, `javap`) or write a small compile probe instead of assuming monorepo paths.
- Do not tell the user to clone the platform repo just to create a normal host.
- Do not require cloning the public quickstart to create a normal host; use it as a reference. Consumer hosts should still resolve `praxis-metadata-starter` and optional `praxis-config-starter` as Maven artifacts.
- Validation for external hosts should succeed without `../praxis-*` paths, local starter source, or quickstart-local properties.

## Canonical Surfaces

- Metadata contracts come from `praxis-metadata-starter`.
- Config/AI contracts come from `praxis-config-starter` when that starter is in scope.
- The host does not redefine `x-ui`, schema endpoints, capabilities, config headers, or ETag semantics.
- `/schemas/domain` is treated as the derived AI-operable domain catalog owned by the metadata starter, not as a structural schema source.
- Public resource paths are centralized.
- Public `resourceKey` values are stable and domain meaningful.
- Public DTO id fields are explicit. If the identifier property is not `id`, the service overrides `getIdFieldName()` and the controller `getResponseId(...)` returns the same field.
- Resources use the current resource-oriented base contracts: mutable resources with CRUD base controller/service, read-only views/projections with read-only base controller/service.
- DTOs are distinct by operation: response, create, update, and filter for mutable resources; response and filter for read-only resources.
- Filter behavior uses `GenericFilterDTO` and `@Filterable` before any custom service/repository predicate logic.
- Host-local base abstractions, when used, remain thin wrappers over Praxis base contracts and do not redefine resource, filter, schema, option, surface, action, export, or capability semantics.
- Controllers follow the resolved starter or target host annotation pattern. Do not add Spring stereotypes such as `@RestController` by reflex when `@ApiResource` already supplies the required semantics for the target version.
- The host has a documented decision for each optional metadata feature it exposes: cursor, locate, stats, option sources, surfaces, actions, export, and config.
- `@ResourceIntent`, `@UiSurface`, and `@WorkflowAction` are used only on real HTTP operations and never as schema or payload sources parallel to `/schemas/filtered`.
- Surfaces that declare item-level projections validate `responseCardinality` against the actual response shape.
- Contextual availability based on real item state has a `ResourceStateSnapshotProvider`, `ActionAvailabilityRule`, or `SurfaceAvailabilityRule`; static availability is documented as static.
- Capabilities are not accepted on trust; every capability needed by the consumer is verified by an HTTP call.

## Optional Runtime Features

- Stats are exposed only when the service declares support modes and a valid `StatsFieldRegistry`.
- Collection export is exposed only when the service declares support, capability metadata, field allowlist, server-side row limits, and a real export executor.
- Governed `RESOURCE_ENTITY`, `LIGHT_LOOKUP`, and other option-source work follows `praxis-resource-entity-lookup-backend` when it goes beyond simple id/label options.

## Security And Origins

- Real hosts define a deliberate security policy instead of relying accidentally on Spring defaults.
- Hosts expected to run behind a dev/prod reverse proxy set a deliberate forwarded-header policy, such as `server.forward-headers-strategy=framework`, so HATEOAS links do not leak internal backend origins to browser clients.
- Config endpoints under `/api/praxis/config/**` respect the required headers and origin policy.
- Local/demo exposure is documented as local/demo exposure, not production policy.
- Do not copy quickstart `permitAll` policies as production defaults. For config/AI surfaces, document CORS, CSRF, authentication, `Origin`/`Referer`, stream signed-token behavior, and required tenant/user/environment headers.

## Derived Artifacts

Review whether changes require updates to:

- public platform docs;
- quickstart or landing-page examples;
- HTTP corpus and manifests;
- `docs/ai/*`;
- generated API docs or schema snapshots.

If none are required, say so explicitly.

## Minimum Done Criteria

- Skill or scaffold files validate structurally.
- The new host compiles with `mvn -B test` or an equivalent focal command.
- Maven dependency resolution proves the selected Praxis starter artifacts are available.
- The implemented resource has a smoke result for `/filter` and the relevant metadata endpoints.
- For resources whose id field is not `id`, `/schemas/filtered` is checked for the intended `x-ui.resource.idField` or the unresolved starter/runtime gap is explicitly reported.
- Semantic metadata in `@Operation`, `@Schema`, `@ResourceIntent`, `@UiSurface`, and `@WorkflowAction` is deliberate, domain-specific, and aligned with the real DTO/service behavior when those annotations are present.
- Runtime smoke covers `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, `/schemas/domain`, collection and item capabilities, collection and item actions, item surfaces, stats, export, and option-sources when those features are in scope.
- Governance-sensitive fields validate `x-domain-governance` in `/schemas/filtered` and their representation in `/schemas/domain` when domain catalog is exposed.
- External-host proof uses published artifacts, for example with `mvn dependency:get` or a temporary `-Dmaven.repo.local`, when independence from the monorepo is part of the task.
- Any skipped runtime validation is explicitly reported.
- Interactive shells or servers started for validation are stopped before handoff.
