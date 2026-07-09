---
name: praxis-resource-entity-lookup-backend
description: Use when implementing or reviewing governed Praxis backend RESOURCE_ENTITY option sources, x-ui.optionSource contracts, OptionSourceRegistry/OptionSourceDescriptor wiring, entityLookup DTO endpoints, filter/by-ids lookup APIs, selection policies, dependencies, display metadata, or schema validation in praxis-metadata-starter or praxis-api-quickstart.
---

# Praxis RESOURCE_ENTITY Backend

Use this skill for backend/starter work that publishes a business entity as a governed
`RESOURCE_ENTITY` option source for Praxis metadata-driven UI.

This skill is not a general Angular Entity Lookup guide. If the task touches runtime/editorial
discovery in `@praxisui/dynamic-fields`, also use `praxis-dynamic-fields-editorial`.
If the task asks for the minimum setup to render a component, use `praxis-component-minimums`.

## Canonical Boundary

Treat `praxis-metadata-starter` as the canonical owner of `x-ui.optionSource`,
`/schemas/filtered`, query/options/option-sources semantics, and schema conformance.

Treat `praxis-api-quickstart` as a reference host that proves the starter contract through real
controllers, services, DTOs, filters, OpenAPI, security, and HTTP examples.

Do not redefine `RESOURCE_ENTITY` semantics in Angular, app consumers, local aliases, or ad hoc
DTO conventions.

## Provider SPI Boundary

`OptionSourceQueryExecutor` is the compatibility facade consumed by existing resource controllers.
The canonical default bean must be the composite executor, which delegates execution to
`OptionSourceProvider` implementations through `OptionSourceProviderRegistry`.

Keep the default JPA implementation behind `JpaOptionSourceProvider`. Do not register
`JpaOptionSourceQueryExecutor` itself as a Spring bean, because that creates a second
`OptionSourceQueryExecutor` and makes controller injection ambiguous.

Custom execution backends should implement `OptionSourceProvider`, declare support by descriptor,
context, and operation, and let the registry resolve the provider. The default JPA provider remains
the fallback for JPA-executable descriptor types so unsupported-type errors keep the public 501
behavior from the executor instead of becoming a provider-resolution failure. Host-specific or
external catalogs that require a custom provider must opt out of JPA fallback with
`OptionSourceExecutionMode.PROVIDER_REQUIRED`; do not rely on `id`/`label` aliases or path
resolution failures to reveal a missing provider.

When multiple providers support the same descriptor and operation, order them explicitly with
`Ordered` or `@Order`. A host-specific provider should precede the JPA fallback, while two
providers at the same order for the same source/operation are a configuration error.

Validate public request semantics before resolving or invoking a provider. Invalid structured
filters, unsupported sort keys, disallowed `includeIds`, disabled search, search terms shorter
than `policy.minSearchChars`, page sizes above `policy.maxPageSize`, or missing operation
capabilities should fail as `422` or `501` at the Praxis orchestration layer, with tests proving
the provider was not called.

Treat `Pageable.sort` as public request semantics too. Query-string `?sort=...` for
`/option-sources/{sourceKey}/options/filter` must be normalized to the effective option-source
sort key or rejected before provider resolution; never let a custom provider receive unvalidated
`pageable.getSort()` values that could be interpolated into SQL or Oracle `ORDER BY` clauses.
For simple option sources without structured `filtering.sortOptions`, only the legacy `id` and
`label` aliases are implicitly allowed.

Validate dependency metadata before provider dispatch: every `dependencyFilterMap` key must be
declared in `dependsOn`. Do not require dependency values to be present in every request unless a
future explicit policy says the dependency is mandatory.

When a descriptor publishes `dependsOn` or `dependencyFilterMap`, the executing provider must
receive and apply the effective filter payload for those dependencies, or the descriptor must stop
publishing them. Add tests proving dependent values change the returned option set; otherwise the
contract looks enterprise-ready while the runtime ignores a business constraint.

Treat selected-value reload as a separate contract from filtering. `GET
/option-sources/{sourceKey}/options/by-ids` is sufficient only when the public ID is
self-contained for the provider. If reload needs the same public dependencies used by filtering,
the backend must prove the contextual `POST /option-sources/{sourceKey}/options/by-ids` path sends
the effective filter/dependency payload to the provider and still preserves requested ID order.
Do not claim a dependent source is reusable or Angular-ready from a passing filter smoke alone.

Use `OptionSourceContextResolver` as the internal extension point for host execution context.
Provider context attributes can carry tenant, datasource, user, or other private host state, but
those attributes must never be published through `x-ui.optionSource`, OpenAPI, docs examples, or
error messages.

For host-specific or external providers, do not let option-source endpoints inherit resource-level
versioning that queries the base JPA repository. If the host resource computes `getDatasetVersion()`
from `repository.count()`, `max(updatedAt)`, or another table-backed query, override
`getOptionSourceDatasetVersion(sourceKey)` for non-JPA sources with a source-specific version or
`Optional.empty()`. The canonical endpoint may still emit the version header, but external option
sources must not depend on the resource table existing or being queryable.

For lightweight external catalogs, prefer `allowIncludeIds=false` on the filter policy and expose
rehydration through the canonical `/option-sources/{sourceKey}/options/by-ids` endpoint. Do not
mark `x-ui.optionSource.includeIds=true` unless the filter provider deliberately supports merging
selected IDs into the first page. Keep Angular aligned so option-source filters send `includeIds`
only when the published metadata explicitly allows it.

## Classification

Classify changes involving `RESOURCE_ENTITY` as `contrato-publico` when they alter any of:

- `OptionSourceDescriptor`
- `OptionSourceRegistry`
- `@UISchema(controlType = FieldControlType.ENTITY_LOOKUP)`
- `/option-sources/{sourceKey}/options/filter`
- `/option-sources/{sourceKey}/options/by-ids`
- `x-ui.optionSource`
- `/schemas/filtered`
- OpenAPI paths or published DTO schemas

If multiple resources, DTO operations, Angular examples, docs, recipes, or skills change, also
classify as `transversal`.

## RESOURCE_ENTITY Decision

Use `RESOURCE_ENTITY` only when the value is a real domain entity selected by a user or another
runtime workflow.

Prefer other option-source types when appropriate:

- `LIGHT_LOOKUP`: small catalog or lightweight reference without rich entity semantics.
- `DISTINCT_DIMENSION`: analytic dimension derived from a view or aggregation.
- `CATEGORICAL_BUCKET`: numeric/date/status buckets or ranges.
- Static enum/select: closed in-code value set.

For `LIGHT_LOOKUP`, verify that the target starter/host version includes the shared JPA executor
coverage and that the descriptor declares executable paths: use `propertyPath` when value and label
are the same field, or `valuePropertyPath` plus `labelPropertyPath` when they differ. Use
`LIGHT_LOOKUP` only for lightweight `OptionDTO{id,label}` sources; if the source needs status,
selection policy, detail navigation, rich display, or corporate structured filters, model it as a
rich `RESOURCE_ENTITY` instead.

Do not promote a resource to `RESOURCE_ENTITY` only because it has `/{resource}/options/filter`.
Generic options endpoints remain useful, but governed entity lookup requires a named
`/option-sources/{sourceKey}` contract.

## Backend Workflow

1. Identify the resource owner and source service.
2. Define a stable `sourceKey`, such as `employee`, `mission`, `threat`, `base`, `team`,
   `vehicle`, or `equipment`.
3. Add or extend the resource service with `OptionSourceRegistry` and `OptionSourceDescriptor`.
4. Register the descriptor in the host-level registry, such as quickstart `OptionSourceConfig`.
5. Prove the named endpoints before changing consumers:
   - `POST /{resource}/option-sources/{sourceKey}/options/filter?page=0&size=25`
   - `GET /{resource}/option-sources/{sourceKey}/options/by-ids?ids=1&ids=2`
6. Update DTO consumers only after the endpoint and schema contract are real.
7. Validate `/schemas/filtered` for every affected operation/schema type.
8. Update docs, HTTP examples, recipes, and Angular examples only when they mirror the published
   public contract or become official examples.

## Descriptor Checklist

Define each field deliberately. Do not copy another resource's descriptor mechanically.

Required or expected:

- `key`: stable source key.
- `type`: `OptionSourceType.RESOURCE_ENTITY`.
- `resourcePath`: canonical API resource path.
- `filterField`: field name used by DTOs when binding this lookup. Omit it when a single
  `RESOURCE_ENTITY` source is deliberately reused by multiple consumer field names; in that case
  the DTO field remains the consumer-side binding and the source describes only the entity provider.
- `valuePropertyPath`: stable identity value.
- `labelPropertyPath`: human-readable label.
- `entityKey`: semantic entity identity used by runtime and AI surfaces.

Governed metadata:

- `codePropertyPath`: short business code when available.
- `descriptionPropertyPaths`: secondary fields that disambiguate similar entities. Do not repeat
  `codePropertyPath` here; the JPA executor projects code and description fields separately and
  duplicated paths can create duplicate select aliases. Also avoid repeating `statusPropertyPath`
  when status is already projected for badges and selection policy.
- `statusPropertyPath`: domain status used for badges and selection policy.
- `disabledPropertyPath` and `disabledReasonPropertyPath`: explicit disabled state and reason.
- `searchPropertyPaths`: safe fields allowed in text search. Exclude sensitive fields.
- `dependsOn`: canonical UI dependency fields.
- `dependencyFilterMap`: map UI field names to backend filter fields when they differ.
- `selectionPolicy`: allowed/blocked statuses or selectable flag.
- `capabilities`: at least filter and by-ids support; detail/create/edit only when true.
- `detail`: route, href, or surface metadata when detail navigation is supported.
- `display`: preset, usage, density, selected layout, result layout, rich fields and badges.
- `filtering`: advanced filters/sort options when the backend owns operators and serialization.

## DTO Consumer Rules

Update every public DTO surface that publishes the relationship:

- response DTO
- create DTO
- update/patch DTO
- action request DTO
- filter DTO

Prefer:

```java
@UISchema(
    label = "...",
    controlType = FieldControlType.ENTITY_LOOKUP,
    endpoint = ApiPaths.Domain.RESOURCE + "/option-sources/<sourceKey>/options/filter",
    valueField = "id",
    displayField = "label"
)
```

When `ApiPaths` already centralizes path constants, add named constants for option-source endpoints
instead of spreading literals across DTOs.

Do not add a DTO-level `optionSource` attribute only because it is absent from the annotation.
The canonical `/schemas/filtered` enrichment resolves `x-ui.optionSource` from a named
`/option-sources/{sourceKey}/options/filter` endpoint plus the registered `OptionSourceDescriptor`.
Treat missing schema metadata as a registry/endpoint resolution issue before duplicating the key in
every DTO annotation.

Do not use `@UISchema.extraProperties` to publish private `optionSource` execution details such as
SQL, provider config, package/function names, external endpoints, context keys, bind parameters, or
cache internals. `/schemas/filtered` must sanitize `x-ui.optionSource` against the closed public
schema allowlist, including nested maps and arrays such as `display.fields`,
`display.actions`, `filtering.availableFilters`, and `filtering.sortOptions`. Registered
`OptionSourceDescriptor` metadata should win over annotation metadata when both publish the same
public key. Add negative tests for private-key leakage whenever changing option-source enrichment.

Do not publish provider identity in `OptionDTO.extra`. Values such as `provider`,
`providerName`, adapter names, package names, SQL identifiers, or external system internals are
execution details, not public option metadata. Keep `extra` limited to domain-facing selection and
display data such as `code`, `status`, `selectable`, `disabledReason`, or catalog attributes that
the user interface may legitimately show.

Do not leave a relationship as `ENTITY_LOOKUP` pointing to `/{resource}/options/filter`; that loses
the governed `RESOURCE_ENTITY` metadata and often breaks rich display, by-ids rehydration, or
selection policy.

## Selection Policy

Model selection policy by domain.

Common pattern:

- Active/selectable records can be selected for new values.
- Inactive, completed, blocked, unavailable, or maintenance records can be returned by `by-ids`
  for existing data, but are disabled for new selection.
- The disabled reason should explain the domain rule, not a technical failure.

Examples:

- completed mission: rehydratable, not selectable for a new incident.
- unavailable vehicle: rehydratable, not selectable for a new sortie.
- equipment in maintenance: rehydratable, not selectable for a new allocation.
- inactive team or base: rehydratable, not selectable for new assignments.
- neutralized threat: domain decision required; do not assume selectable.

## Dependency Order

Implement providers before consumers. In the quickstart pilot, prefer this order:

1. `risk-intelligence.ameacas` before `operations.missoes`.
2. `operations.bases` before `operations.equipes`.
3. `operations.equipes` before workflows that select teams.
4. `operations.missoes` before incident, mission participant, event, summary, and vehicle usage
   consumers.
5. `assets.veiculos` before `veiculo-missao-usos`.
6. `assets.equipamentos` before `equipamento-alocacoes`.

## Backend Validation

Add or update a focal integration test similar to an existing entity lookup pilot.

Cover:

- `/schemas/filtered` publishes `controlType=entityLookup`.
- `/schemas/filtered` includes `x-ui.optionSource.type=RESOURCE_ENTITY`.
- `resourcePath`, `entityKey`, `valuePropertyPath`, `labelPropertyPath`, dependencies and
  capabilities are present.
- `POST /option-sources/{sourceKey}/options/filter` returns expected options.
- `GET /option-sources/{sourceKey}/options/by-ids` rehydrates selected IDs in order.
- For dependent or context-sensitive sources, `POST /option-sources/{sourceKey}/options/by-ids`
  rehydrates selected IDs with the declared dependency/filter payload and preserves the requested
  order.
- Blocked/inactive records are rehydratable but not selectable when the policy says so.
- Search excludes sensitive fields.

Quickstart focal suite candidates:

```powershell
mvn "-Dtest=OpenApiGroupResolutionIsolatedIntegrationTest,QuickstartMetadataMigrationIntegrationTest,ProcurementEntityLookupPilotIntegrationTest" test
```

Add resource-specific pilot tests when promoting new domains.

## HTTP Corpus Publication

When adding Praxis HTTP examples for `RESOURCE_ENTITY` or `LIGHT_LOOKUP`, keep the corpus honest
about where the endpoint is proven:

- If the endpoint is proven only by the local branch or quickstart tests, mark the example as
  `referenceOnly: true`, `publishedBackendConfirmed: false`, and `status: ["illustrative-only"]`.
- Keep the first `### status:` line in the `.http` file aligned with the manifest status.
- Promote to `runtime-confirmed`, `recommended`, or `llmOperational` only after the committed
  request succeeds against the published backend and the manifest sets `publishedBackendConfirmed:
  true`.
- Run `npm run verify:manifest`; it enforces these governed lookup corpus rules.

## Angular And Editorial Handoff

Do not change Angular to compensate for an incomplete backend contract.

Angular expects:

- `optionSource.key`
- `resourcePath`
- `valuePropertyPath`
- `labelPropertyPath`
- `searchPropertyPaths`
- `dependsOn`
- `dependencyFilterMap`
- `selectionPolicy`
- `capabilities.byIds`
- `display`
- `detail` or `create` only when supported

If the task updates official Angular examples, recipes, registry, or editor discoverability, use
`praxis-dynamic-fields-editorial` and validate runtime/editorial coverage separately.

## High-Risk Failure Modes

- Changing only `controlType` without registering an option source.
- Publishing `ENTITY_LOOKUP` against generic `/options/filter`.
- Forgetting `/option-sources/{sourceKey}/options/by-ids`.
- Copying procurement status policy into an unrelated domain.
- Exposing sensitive fields in `searchPropertyPaths` or descriptions.
- Publishing `dependsOn`/`dependencyFilterMap` without passing and enforcing the effective filter
  payload in host-specific or external providers.
- Marking a dependent option source as reusable after only `filter` passes, without proving
  selected-value reload through either self-contained IDs or contextual `POST .../by-ids`.
- Letting `@UISchema.extraProperties` leak private `optionSource.sql`, `providerConfig`, package
  names, raw endpoints, context fields, bind parameters, or cache internals through `/schemas/filtered`,
  including inside nested public containers.
- Publishing host provider identity through `OptionDTO.extra.provider` or equivalent public payload
  fields.
- Publishing a consumer-specific `filterField` from a shared entity provider used by different
  DTO field names.
- Updating response DTOs but not create/update/action/filter DTOs.
- Treating quickstart as the canonical source of `x-ui.optionSource` semantics.
- Adding Angular aliases or adapters instead of fixing the backend contract.
- Updating recipes/docs before the backend schema and HTTP endpoints are proven.
