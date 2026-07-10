---
name: praxis-metadata-resource-baseline
description: Use when Codex must implement, audit, or migrate praxis-metadata-starter resource-oriented backend patterns: AbstractResourceController, AbstractReadOnlyResourceController, AbstractResourceQueryController, AbstractBaseResourceService, AbstractReadOnlyResourceService, ResourceMapper, RestApiResponse, HATEOAS links, filters, stats, export, or canonical resource CRUD hierarchy.
---

# Praxis Metadata Resource Baseline

Use this skill for the canonical resource-oriented hierarchy in `praxis-metadata-starter`. The baseline is `resource + surfaces + actions + capabilities + HATEOAS`; do not reintroduce legacy controller/service hierarchies or host-specific CRUD shortcuts.

## Source Audit

Inspect the owner before editing:

- `praxis-metadata-starter/AGENTS.md`
- `src/main/java/org/praxisplatform/uischema/controller/base/**`
- `src/main/java/org/praxisplatform/uischema/service/base/**`
- `src/main/java/org/praxisplatform/uischema/mapper/base/ResourceMapper.java`
- `src/main/java/org/praxisplatform/uischema/rest/response/RestApiResponse.java`
- `src/main/java/org/praxisplatform/uischema/rest/response/RestApiLinks.java`
- `src/main/java/org/praxisplatform/uischema/filter/**`
- `src/main/java/org/praxisplatform/uischema/exporting/**`
- `src/main/java/org/praxisplatform/uischema/stats/**`
- related controller/base and service/base tests

## Canonical Boundary

Mutable resources should use `AbstractResourceController` plus `AbstractBaseResourceService` and `ResourceMapper`. Read-only resources should use `AbstractReadOnlyResourceController` plus `AbstractReadOnlyResourceService`.

`RestApiResponse` publishes HATEOAS under `_links`; do not regress to `links` or wrap resources in host-local envelopes. Query, command, export, stats, and filter behavior should remain resource-oriented unless a governed workflow action is explicitly modeled.

## Decision Rules

- Choose read-only, create/update/delete, unit-delete, or full mutable base intentionally.
- Do not hide business workflow commands as opportunistic PATCH/CRUD shortcuts. Use workflow action contracts when the domain operation is explicit.
- Do not add local DTO aliases or frontend-only id-field patches when the resource baseline can publish `idField`, `_links`, operation schemas, and capabilities.
- Keep controller/base, service/base, mapper, response envelope, and tests aligned in the same change.
- Treat legacy classes as migration surfaces unless the local AGENTS says otherwise.

## No Keyword Routing

Do not choose controllers, operations, filters, actions, or relationships through keyword lists, regexes, aliases, or label matching as the primary decision. Resolve the semantic resource scope from canonical annotations, OpenAPI operations, resource keys, capabilities, `_links`, and declared backend contracts; textual matching may only rank candidates after that scope is known.

## Aderence Inventory

Before adding a base class, controller method, endpoint convention, response field, mapper contract, or service hook, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real contract gaps justify new public hierarchy or response contracts. Most resource issues should be fixed by using the canonical base correctly.

## Validation

Use focused local gates:

- resource controllers and `_links`: `mvn "-Dtest=AbstractResourceControllerMappedCrudTest,AbstractResourceControllerJpaWriteIntegrationTest,AbstractReadOnlyResourceControllerLinksTest,AbstractResourceControllerLinksTest,AbstractResourceQueryControllerHateoasTest,AbstractResourceQueryControllerBasePathDetectionTest" test`
- export/stats/filter changes: focused tests for exporting, stats, filter normalizers, and affected base services
- downstream quickstart proof for public resource behavior: `QuickstartMetadataMigrationIntegrationTest` and the relevant pilot integration test

For public baseline changes, review README, guides, quickstart docs/examples, Angular `GenericCrudService`, and HTTP examples. State explicitly when no derived artifact is affected.

## Companion Skills

- Use `praxis-metadata-schema-contracts` for `/schemas/filtered`, schema refs, headers, and `x-ui` shape.
- Use `praxis-metadata-discovery-capabilities` when resource behavior changes surfaces, actions, capabilities, `_links`, export, stats, or availability.
- Use `praxis-api-quickstart` skills, when available, for downstream host proof instead of redefining starter contracts in the host.
