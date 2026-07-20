---
name: ergon-archon-read-api-migration
description: Design and implement read/query APIs for Ergon/Archon screens after screen discovery is closed. Use when Codex must turn investigation.md, component-lineage-matrix.md, browser-runtime.md, and candidate api-contract.md into Java/Spring read-only endpoints, DTOs, filters, options, schema metadata, OpenAPI/x-ui tests, and read parity checks.
---

# Ergon Archon Read API Migration

Use this skill after `ergon-archon-screen-discovery` closes the screen discovery gate. This skill owns read/query API design and implementation. It does not own write API design.

In a multi-phase migration, use `ergon-migration-orchestration` first to confirm the Phase 3 read/options implementation gate for the intended slice.

When this skill designs or changes DTOs, FilterDTOs, OptionDTOs, `@Schema`, `@UISchema`, `@Filterable`, `x-ui`, OpenAPI schemas, or `/schemas/filtered`, also use `praxis-dto-annotations` and `ergon-fieldspec-ui-contract`. Use `praxis-java-host-project` when creating or changing a Java/Spring resource. Use `praxis-resource-entity-lookup-backend` when the contract includes `RESOURCE_ENTITY`, `OptionSourceRegistry`, `OptionSourceDescriptor`, or `/option-sources/{sourceKey}`.

## Platform Governance

Before designing or implementing read/options contracts, apply the root
migration `AGENTS.md`. Classify the change as `docs-apenas`, `local-pequena`,
`transversal`, `contrato-publico`, or `arquitetural`, and record the canonical
owner in the phase plan/gate.

Before editing Java, docs, tests, DTOs, resources, or build files, run the
duplicate-module-root guard from `ergon-migration-orchestration` for the target
module/artifactId. If it reports a competing `migracao-package` or another
duplicate root, switch to the canonical root from `AGENTS.md` or require an
explicit human choice before implementation evidence is accepted.

Do not create Ergon-local substitutes for Praxis contracts. Before adding an
endpoint shape, schema metadata, option source, capability, surface, action, or
Angular-facing workaround, inventory the native Praxis support and classify the
need as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. Only
`lacuna-real-de-contrato` should become a Praxis platform follow-up.

If a defect belongs to `praxis-metadata-starter`, `praxis-config-starter`, or
`praxis-ui-angular`, record `Praxis Platform Follow-up` evidence instead of
fixing it inside the Ergon host. Temporary workarounds must have an owner,
removal trigger, canonical replacement, and must not be promoted as scalable
examples.

## Phase Boundary

This is the read API phase.

1. `ergon-archon-screen-discovery` discovers the legacy screen: browser behavior, XML/runtime SQL, binds, keys, components, authorization, session context, write surface, and candidate endpoints.
2. `ergon-archon-read-api-migration` converts closed read candidates into Java/Spring read-only APIs.
3. Write actions remain blocked/deferred unless a later phase explicitly handles them with `ergon-archon-write-api-migration`.
4. Do not run `ergon-table-rule-audit` for read-only implementation unless read SQL depends on write-side package behavior or the same artifact is needed for the future write phase.

If discovery artifacts are missing, `closure-checklist.md` is not closed as `Ready for read API`, `Read handoff ready; write deferred`, or an equivalent read-ready state for the intended slice, or the read gate is open, return to `ergon-archon-screen-discovery`.

## Phase Entry Gate

Before editing Java, prove the handoff is not still discovery or contract design:

- Phase 1 has `phase-1-execution-gate.md`, `closure-checklist.md`, `operation-inventory.md`, `component-lineage-matrix.md`, `read-parity-matrix.md`, and `platform-reuse-inventory.md` or equivalent reuse decisions.
- The target endpoint is marked `Required Now` or `Ready for implementation`, not merely `Candidate`.
- `api-contract.md` records the `praxis-dto-annotations`, `ergon-fieldspec-ui-contract`, `praxis-java-host-project`, and, when applicable, `praxis-resource-entity-lookup-backend` reviews.
- Read-only scope is explicit for visible write operations: create, edit, delete, duplicate, legal documents, publications, pending flows, and cancel/reset are omitted, blocked, 405/501, or deferred with owner and follow-up.
- Same-connection context, server-side authorization/scope, stable public key, filter predicates, options, schemas, and parity cases are closed or explicitly blocked/deferred.

If any item is missing, do not implement a local Java endpoint as a shortcut. Return to the owning phase or mark the read endpoint `Blocked`.

Use the term `same-connection context` in the gate artifact when Oracle package/session state must be set and cleaned on the same physical connection that executes the read query.

## Required Inputs

Before using this skill, verify the screen package has:

- `browser-runtime.md`;
- `component-lineage-matrix.md`;
- `operation-inventory.md` or an equivalent operation-status section in `closure-checklist.md`;
- `investigation.md`;
- `closure-checklist.md`;
- finalized `api-contract.md` for Phase 3 implementation; if only a candidate contract exists, return to Phase 2 before editing Java;
- `platform-reuse-inventory.md` or an equivalent explicit decision for each read/options candidate: `reuse`, `extend`, `create`, `block`, `defer`, or `not-api`;
- `java-session-context.md`, `java-oracle-session-context.md`, or an equivalent section in `api-contract.md` when Oracle SQL depends on package/session state;
- `authorization-scope.md` or an equivalent authorization section in `investigation.md`/`api-contract.md` when scope is user/company/profile dependent;
- `write-risk.md` and `write-api-handoff.md` when the legacy screen has write actions, even though this skill will keep writes blocked.

For Phase 2 contract work, `api-contract.md` must record the `praxis-dto-annotations` and `ergon-fieldspec-ui-contract` review. For Phase 3 implementation work, `read-parity-results.md` must record the same reviews plus `praxis-java-host-project` when Java resources changed and `praxis-resource-entity-lookup-backend` when governed option sources were used.

## Core Strategy

Prefer Praxis metadata/API read resources when the repository supports them:

- controller/resource declared with `@ApiResource(value = ..., resourceKey = ...)`;
- read-only controller/service built on `AbstractReadOnlyResourceController` and `AbstractReadOnlyResourceService`, or an equivalent host-local thin subclass, for read-only views/projections;
- service/query class for legacy SQL, behind the host's resource service boundary;
- DTO and FilterDTO;
- `@UISchema`, `@Filterable`, DTO, FilterDTO, ID type, mapper/conversion, and response envelope consistent with the local project;
- `OptionDTO(id, label, extra)` and option endpoints for combos/lookups;
- `/all`, `/filter`, `/filter/cursor`, `/locate`, `/by-ids`, `/options/filter`, `/options/by-ids`, `/{resource}/option-sources/{sourceKey}/options/filter`, `/{resource}/option-sources/{sourceKey}/options/by-ids`, collection/item `/capabilities`, `/schemas`, and `/schemas/filtered` where appropriate;
- explicit unsupported write behavior for create/update/delete/batch delete until write gates close.

Do not add `@RestController` alongside `@ApiResource` when the resolved `praxis-metadata-starter` version already meta-annotates `@ApiResource` as the REST controller declaration. Allow an exception only when the resolved starter version proves `@ApiResource` is not meta-annotated and the host pattern explicitly requires the Spring stereotype.

Map read-facing legacy operations to Praxis metadata/API methods explicitly:

- `Consultar/listar` becomes `POST /<resource>/filter` and `BaseResourceQueryService.filter(filter, pageable, includeIds)` or the target host's equivalent current starter service method.
- `Ler detalhe` becomes `GET /<resource>/{id}` and `BaseResourceService.findById`; use `GET /by-ids` / `findAllById` for selected-value reloads.
- Combo/list-of-values behavior becomes either:
  - generic options: `POST /<resource>/options/filter`, `GET /<resource>/options/by-ids`, and `OptionDTO(id, label, extra)`;
  - governed Praxis option sources: `POST /<resource>/option-sources/{sourceKey}/options/filter`, `GET /<resource>/option-sources/{sourceKey}/options/by-ids`, `OptionSourceRegistry`, `OptionSourceDescriptor`, and `x-ui.optionSource`.
- For DTO fields using remote options, declare `@UISchema(endpoint = ..., valueField = "id", displayField = "label", filterField = ..., sortField = ..., optionsPageSize = ...)` unless `x-ui.optionSource` fully governs the source; in that case do not duplicate private option-source execution details in annotation metadata.
- Schema metadata becomes `/schemas`, `/schemas/filtered`, DTO/FilterDTO annotations, `x-ui`, OpenAPI assertions, and optionally `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, or `/schemas/domain` only when those surfaces are part of the scoped contract. These discovery surfaces do not replace `/schemas/filtered`.
- Visible write operations inherited by generic resources must be deliberately blocked, omitted, or documented as Phase 3. A read-first API is incomplete if `Novo`, `Editar`, `Apagar`, `Duplicar`, `Cancelar`, legal documents, publications, or pending flows are not represented in the operation inventory.

Use canonical Praxis schema paths in contracts and tests:

- filter request: `/schemas/filtered?path=/<resource>/filter&operation=post&schemaType=request`;
- filter/list response when the starter publishes an `all` response schema: `/schemas/filtered?path=/<resource>/all&operation=get&schemaType=response`;
- read-only view response: `/schemas/filtered?path=/<resource>/all&operation=get&schemaType=response`;
- detail response when published by the host/starter: `/schemas/filtered?path=/<resource>/{id}&operation=get&schemaType=response`;
- option-source request/response schemas when applicable, using the exact `path`, `operation`, and `schemaType` consumed by the UI/runtime.

The `resourceKey` is semantic identity, not a cosmetic copy of the URL. Preserve a stable, domain-meaningful `resourceKey` even if the operational path changes.

## Praxis Options And Option Sources

Choose the option surface deliberately:

| Need | Preferred Praxis surface |
| --- | --- |
| Stable catalog/resource with its own API | `POST /<resource>/options/filter` and `GET /<resource>/options/by-ids` |
| Named or derived dimension without a standalone CRUD resource | `/{resource}/option-sources/{sourceKey}/options/*` |
| Rich selectable business entity with policy, dependencies, detail, or display metadata | `RESOURCE_ENTITY` option source |
| Lightweight id/label lookup | `LIGHT_LOOKUP` option source |

Do not promote a lookup to `RESOURCE_ENTITY` only because `/options/filter` exists. Use `RESOURCE_ENTITY` only when the selected value is a real domain entity and the backend can publish governed metadata.

For `POST /{resource}/option-sources/{sourceKey}/options/filter`, use the canonical request envelope: `filter`, `filters`, `search`, `sort`, and `includeIds`. Validate public request semantics before provider execution:

- invalid structured filters, unsupported sort, or malformed request: `422`;
- unsupported operation/capability, such as disabled filter or by-ids: `501`;
- unknown `sourceKey`: `404`;
- `includeIds` is allowed only when the descriptor explicitly supports it. Otherwise use `/{resource}/option-sources/{sourceKey}/options/by-ids` for selected-value rehydration.

For `RESOURCE_ENTITY`, the minimum `OptionSourceDescriptor` evidence is: `key`, `type=RESOURCE_ENTITY`, `resourcePath`, `entityKey`, `valuePropertyPath`, `labelPropertyPath`, `searchPropertyPaths`, `capabilities.byIds`, and, when applicable, `dependsOn`, `dependencyFilterMap`, `selectionPolicy`, `display`, and `filtering`. Tests must prove `/schemas/filtered` publishes `controlType=entityLookup`, `x-ui.optionSource.type=RESOURCE_ENTITY`, dependencies/capabilities, and no private execution keys. Public `x-ui.optionSource` keys may include governed metadata such as `dependsOn`, `dependencyFilterMap`, `excludeSelfField`, `searchMode`, `pageSize`, `includeIds`, and `cachePolicy` when the descriptor supports them.

Keep `OptionDTO.extra` limited to domain-facing display/selection metadata, such as `code`, `description`, `status`, `selectable`, `disabledReason`, `detailHref`, `detailRoute`, `resourcePath`, `entityKey`, `badges`, or `richFields`. Do not publish provider identity, SQL/package names, context keys, bind values, cache internals, user/company/session data, or host adapter details.

For Ergon framework screens, treat `Consultar/listar` and `Ler detalhe` as the minimum read surface. Also identify read-only supporting resources needed by the screen, such as options/lookups and `Documentos legais` tabs. A read-first slice may defer writes, but it must still state the backend behavior for inherited or visible write operations: `Novo/Salvar`, `Editar/Salvar`, `Apagar`, `Duplicar`, `Cancelar`, legal-document writes, publications, and pending flows should be `405`, omitted, `Blocked`, or explicitly implemented by a later write phase.

Before drafting final contracts or editing Java, load the existing discovery references from `ergon-archon-screen-discovery` when present: `api-design-patterns.md`, Praxis metadata/API reference notes, and `java-api-implementation-playbook.md`. These remain the detailed API/Praxis playbooks; this skill owns when to apply them.

Do not expose Archon internals as public API by default. `ROWID`, XML ids, debug parameter names, and PL/SQL routine names are implementation evidence, not API contract.

For screens that prove both a stable public key and a legacy internal row locator, prefer this split:

- expose the stable key such as `ID_REG` in read/list/detail APIs;
- keep `ROWID`, `ROWID_REG`, XML hidden ids, and component-specific row fields internal;
- resolve internal row locators server-side only when a later legacy-backed flow explicitly requires them.

Before accepting the discovery key strategy, verify that uniqueness was tested
against the effective legacy query with server-side scope/session predicates,
not against the raw view alone. Duplicate keys in an unscoped view can be
technical fan-out for company/query modes and do not by themselves require a
composite or opaque id. When the base domain key is unique in the effective
resource slice, use it for list/detail/by-ids and keep scope internal. If the
effective slice still duplicates the key, return to discovery to classify
same-entity projection versus genuinely distinct resources before designing
normalization, a composite key, or an opaque representation.

When read SQL or screen views depend on `HADES.FLAG_PACK` or similar package state, the API design must require setup and cleanup on the same physical Oracle connection used by the query. Do not treat context set in SQLcl, a separate JDBC connection, or a different transaction as API parity evidence.

For read-only legacy queries that require package/session context, prefer a shared same-connection executor. In the Praxis host/backend module, use or add an explicit read route such as `ErgonLegacyRoute.READ_ONLY` instead of misusing write routes. The resource service may contain legacy SQL mapping, but context setup/cleanup and Oracle exception/session handling must stay behind the shared bridge.

Resolve legacy context through a single application hook before calling the shared executor. In `ms-administracao-pessoal`, prefer `ErgonLegacyContextProvider` plus replaceable `ErgonLegacyUserMapper` and `ErgonLegacyCompanyResolver` instead of injecting `usuario-padrao`, `empresa-padrao`, `sistema-padrao`, or role in every resource service. The default user mapper may use `Authentication.getName()` with a configured fallback, and the default company resolver may use the requested company with a configured fallback; production IdP/company-session differences must be isolated behind the mappers/resolvers.

When production identity or selected-company sources are not yet known, create a small `production-context-integration.md` handoff artifact. It must state the current default/fallback behavior, the production decisions still needed, the expected custom `ErgonLegacyUserMapper`/`ErgonLegacyCompanyResolver` beans, and acceptance tests proving user/company context before write migration.

When the legacy screen uses authorization helpers such as `MOSTRA_FREQ(flag_pack.get_usuario, tipofreq, codfreq)`, preserve the helper predicate in the endpoint SQL or prove an exact Java-equivalent rule. Do not treat a permission/display column returned by a view, such as `PERMISSAO_USU`, as sufficient filtering evidence by itself; a view can expose denied rows with a permission flag. Add an allowed and denied user fixture whenever the read surface is user/profile scoped.

## Workflow

1. Read discovery artifacts and `platform-reuse-inventory.md`; classify read candidates as `Required Now`, `Candidate`, `Blocked`, `Deferred`, or `Not API`, and decide whether each one reuses, extends, or creates a Java/OMS resource.
2. Verify every `Required Now` endpoint has source SQL, bind behavior, filters, key strategy, scope/session context, authorization, DTO fields, sort/pagination, and parity cases. Ensure `Consultar/listar` and `Ler detalhe` are either implemented or explicitly `Not API` with evidence.
   - For visible legacy fields in the scoped list/detail/tabs, decide and record one of: included in response/detail DTO, deliberately omitted from the new slice with justification, moved to a child/shared resource, or deferred. Do not leave visible same-resource detail fields for the Angular phase to discover.
   - For every legacy LOV/select/dropdown in a required filter or form, choose the Praxis control and option contract now. If a source exists, do not publish it as free text metadata.
   - For every visible grid, filter, detail, or read-only form field, choose a representative Praxis/Material icon in `@UISchema(icon = "mi:...")`, or explicitly document why the field should not publish an icon. Treat icons as DTO contract metadata, not as an Angular cleanup task.
3. Produce or update `api-contract.md` as the read contract. If the existing contract was created during discovery, treat it as a draft. Record the applied `praxis-dto-annotations` and `ergon-fieldspec-ui-contract` review in the contract before marking Phase 2 ready.
4. Produce `read-parity-matrix.md` from [read-parity-template.md](references/read-parity-template.md).
5. Do not edit Java or mark an endpoint `Ready for implementation` until `api-contract.md` and `read-parity-matrix.md` exist for the scoped read/options endpoints.
6. Inspect target Java modules and existing resource patterns before editing code. For `ms-administracao-pessoal`, verify endpoint constants, `@ApiResource(value = ..., resourceKey = ...)`, Swagger/OpenAPI grouping, validation config, `application.yaml`, existing controllers/services/DTOs/FilterDTOs, mappers/query classes, option-source registries, and OpenAPI/x-ui test scripts. If an existing resource was found in Phase 1.5, extend or reuse it unless the semantic gap is documented in `platform-reuse-inventory.md`. Before changing DTOs or annotations, apply `praxis-dto-annotations`; before changing Java resource structure, apply `praxis-java-host-project`.
7. Inspect the module/starter persistence convention before choosing implementation mechanics. Prefer existing Spring Data/JPA, starter service, repository, `EntityManager`, resource service, or legacy executor patterns. Do not assume `JdbcTemplate` is the project standard merely because Oracle package state or PL/SQL calls are involved; use lower-level JDBC only as an implementation detail of a shared same-connection executor when the local project pattern supports or requires it.
8. Implement only closed read endpoints. Keep write operations blocked with deliberate HTTP behavior.
9. Add automated backend tests before moving to the next backend phase:
   - service test with fake legacy executor verifying `READ_ONLY`, screen transaction, target object, user/company context, filter params, sort/paging, and cleanup-facing bridge usage;
   - context-provider tests for user and company mapping: authenticated principal, fallback user, requested company, fallback company, and custom production mapper/resolver;
   - authorization predicate test when the legacy query uses helpers such as `MOSTRA_FREQ`, `PADRAO_ACESSO`, profile/package functions, or user/company scope helpers;
   - `findById`/`findAllById`/`includeIds` behavior;
   - `@ApiResource`/`resourceKey` and read-only controller/service behavior;
   - `/schemas/filtered` request/response schemas for the exact paths and operations consumed by the UI/runtime;
   - baseline read endpoints and capabilities when published by the starter/scope: `/all`, `/filter/cursor`, `/locate`, collection `/capabilities`, and item `/capabilities`;
   - `OptionDTO(id, label, extra)`, `/options/by-ids`, and governed `option-sources` when applicable;
   - explicit `405` or chosen blocked behavior for create/update/delete/batch delete.
10. Add or update OpenAPI/schema/x-ui tests when the test context can load them reliably. If not yet stable, mark them planned in `read-parity-results.md` instead of calling the endpoint verified.
11. Execute the implemented endpoints with recorded payloads/responses before calling them smoke-tested or verified: `GET /all`, `POST /filter`, `POST /filter/cursor`, `GET /locate`, `GET /{id}`, `/by-ids`, `/options/filter`, `/options/by-ids`, `/{resource}/option-sources/{sourceKey}/options/filter`, `/{resource}/option-sources/{sourceKey}/options/by-ids`, collection/item `/capabilities`, `/schemas/filtered`, and optional `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, or `/schemas/domain` when the scoped delivery requires them. Record status, row counts, ids/keys, labels, option wrappers, HATEOAS/actions, `x-ui.resource`, `ETag`/`X-Schema-Hash`, and relevant metadata. If the baseline starter does not emit `x-ui.resource`, `ETag`, or `X-Schema-Hash`, record a version/conformance gap instead of silently treating it as not applicable.
12. Compare the executed endpoint output against the legacy screen using the same user/company/context and filters when fixtures/access are available. If this comparison cannot run, record the fixture/access blocker and keep the endpoint below `Verified`.
13. Run verification and update `read-parity-results.md` with executed HTTP evidence, legacy comparison status, blockers, and final read state.

Do not treat a new read endpoint as closed until backend read contracts, minimal automated backend tests, executed endpoint smoke/parity evidence, and explicit write blocking are recorded.

After read/options implementation, expect executed endpoint evidence and Phase 7 Quality Round 2 before final backend/pilot handoff. The agent should operate the authenticated legacy screen, execute representative filters, detail selection, selected-value reload, and option searches, then compare them with `POST /filter`, `GET /{id}`, `/by-ids`, and `/options/*`. Record the comparison in `quality-round-2.md`; API tests alone are not a substitute for this browser-vs-endpoint pass.

At minimum, the executed evidence must include the exact HTTP method/path, request payload, response status, response wrapper shape, representative id/key fields, row/option counts, option labels, `/schemas/filtered` `x-ui` metadata, capabilities/actions when scoped, and the user/company/session context used by the shared legacy bridge. A schema/static test without running HTTP is `Schema/static contract passed`, not `Verified`.

## Read Gates

An endpoint can move to implementation only when:

- the component or workflow requiring it is identified;
- source SQL/view/package and bind values are confirmed;
- public key strategy is stable, was proven in the effective legacy query scope
  (not inferred from an unscoped view count), and does not expose internal
  `ROWID` unless explicitly accepted;
- filter semantics match legacy behavior, including date overlap and null/default handling;
- authorization and company/user scope are known;
- user/company mapping has a central provider or documented project equivalent, with production-specific mapping isolated behind replaceable hooks;
- legacy authorization helpers are preserved as filtering predicates, not only returned as display/permission columns;
- same-connection Oracle session context setup and cleanup are defined if required;
- DTO fields are mapped to legacy fields and UI meaning;
- visible DTO and FilterDTO fields have deliberate `@UISchema` labels, order, groups, controls, and representative prefixed icons such as `mi:tag`, `mi:badge`, `mi:event`, or an explicit no-icon decision;
- visible same-resource grid/detail fields for the target slice are either represented in response/detail DTOs or explicitly omitted/deferred with evidence and owner;
- options/lookups are identified when the UI needs them;
- legacy select/LOV/dropdown fields do not degrade to plain `SEARCH_INPUT`/free text when an approved option endpoint/source is available;
- `OptionDTO` shape is `id`, `label`, `extra`, and selected-value rehydration uses `/options/by-ids` or `/option-sources/{sourceKey}/options/by-ids`;
- governed lookups use `OptionSourceRegistry`/`OptionSourceDescriptor` and expose public `x-ui.optionSource` only through `/schemas/filtered`;
- private option-source details such as SQL, provider names, package names, external endpoints, bind/context fields, `FLAG_PACK`, user, company, or cache internals are not published through `x-ui`, `extraProperties`, OpenAPI examples, or `OptionDTO.extra`;
- Phase 1.5 reuse discovery proves whether the endpoint/lookup already exists in the new platform and whether it will be reused, extended, or newly created;
- pagination and ordering are defined;
- unsupported write endpoint behavior is explicit and testable, such as omitted, `405`, `501`, or controller override;
- operation inventory states what will happen to `Novo/Salvar`, `Editar/Salvar`, `Apagar`, `Duplicar`, `Cancelar`, `Documentos legais`, publication, and pending flows in the read-first slice;
- parity cases cover default load, filtered load, empty result, unauthorized/scope-limited user, key lookup, options, and special scope values such as `-1`/`-2` when present.

For read-first screens with deferred writes, the read endpoint can still be `Ready for implementation` when write risk is explicitly documented as blocked/deferred and the read surface has closed runtime, key, scope, and session-context evidence.

If any gate is open, keep the endpoint `Candidate` or `Blocked`.

## Read States

Use these states consistently:

- `Candidate`: plausible endpoint, not closed.
- `Required Now`: endpoint belongs to the current migration slice and must be closed.
- `Ready for implementation`: contract and gates are closed, but code has not been changed.
- `Implemented`: code exists and compile passes, but tests/evidence may still be incomplete.
- `Implemented with automated backend tests`: resource/service/controller tests cover the backend contract, context bridge, key lookup, and blocked writes.
- `Schema/static contract passed`: OpenAPI/schema/x-ui assertions passed, but the running endpoint was not executed.
- `Executed endpoint smoke`: running endpoint was executed with payload/response evidence, but legacy comparison or scoped API metadata is incomplete.
- `Legacy parity pending`: endpoint execution exists, but legacy browser comparison is blocked by fixture/access/context.
- `Smoke-tested against Oracle fixture`: at least one configured live/Oracle fixture was exercised and recorded.
- `Verified`: implemented endpoint has automated tests plus executed parity evidence in `read-parity-results.md`; unexecuted cases are explicitly deferred with risk.
- `Blocked`: evidence or access is missing.
- `Deferred`: intentionally postponed with risk accepted.
- `Not API`: explicitly outside the API surface.

Do not call an endpoint `Verified` without executed evidence and legacy/contract comparison. If code exists but tests are not present, call it `Implemented` and list the missing tests. If backend tests exist but the endpoint was not executed, call it `Implemented with automated backend tests`. If OpenAPI/schema assertions passed but no endpoint smoke ran, call it `Schema/static contract passed`. If the endpoint was executed but legacy comparison is incomplete, call it `Executed endpoint smoke` or `Legacy parity pending`, not fully verified.

## Praxis Metadata Starter Conformance Checklist

Before closing implementation or declaring the API compatible with `praxis-metadata-starter`, verify:

- dependency mode is known: published starter dependency, local Maven artifact, or local platform source;
- the controller/resource uses `@ApiResource(value = ..., resourceKey = ...)`;
- read-only resources use `AbstractReadOnlyResourceController` and `AbstractReadOnlyResourceService`, or a proven host-local equivalent;
- `@RestController` is not added alongside `@ApiResource` unless the resolved starter version proves `@ApiResource` is not meta-annotated as the REST controller declaration;
- response DTO and FilterDTO expose deliberate `@Schema`, `@UISchema`, and `@Filterable` metadata;
- `resourceKey` is stable semantic identity, not just a copy of the URL;
- `/schemas/filtered` resolves the exact request/response schemas that the UI/runtime uses, including `path`, `operation`, and `schemaType`;
- `/schemas/filtered` publishes `x-ui.resource` with `idField`, `idFieldValid`, `readOnly`, and capabilities in the current baseline; if absent, record a version/conformance gap;
- `ETag` and `X-Schema-Hash` are captured in the current baseline; if absent, record a version/conformance gap;
- baseline read capabilities are validated when in scope: `all`, `filter`, `cursor`, `byId`, `options`, and item/collection capabilities;
- `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, and `/schemas/domain` are validated only when scoped, and never replace `/schemas/filtered`;
- generic options use `OptionDTO(id, label, extra)`, `POST /<resource>/options/filter`, and `GET /<resource>/options/by-ids`;
- governed lookups use `OptionSourceRegistry`, `OptionSourceDescriptor`, `/{resource}/option-sources/{sourceKey}/options/filter`, and `/{resource}/option-sources/{sourceKey}/options/by-ids`;
- option-source filter requests use the public envelope `filter`, `filters`, `search`, `sort`, and `includeIds`, and invalid public semantics fail before provider execution;
- `@UISchema` uses `valueField = "id"` and `displayField = "label"` for `OptionDTO` sources;
- `x-ui.optionSource` is resolved from the registered descriptor and endpoint, not copied as private ad hoc metadata;
- private execution details never leak through `x-ui.optionSource`, `extraProperties`, docs examples, error payloads, or `OptionDTO.extra`.

## Required Output

For each read API migration attempt, produce or update:

- `api-contract.md`;
- `read-parity-matrix.md`;
- updated `operation-inventory.md` or closure checklist operation table;
- Java implementation plan or code changes;
- OpenAPI/schema/x-ui tests;
- API tests;
- `read-parity-results.md`;
- Praxis metadata/API evidence for `@ApiResource`, `resourceKey`, `/schemas/filtered`, `x-ui.resource`, options/option-sources, and read-only resource behavior;
- `production-context-integration.md` when user/company mapping is still a production handoff item;
- final read state: `Ready for implementation`, `Implemented`, `Implemented with automated backend tests`, `Schema/static contract passed`, `Executed endpoint smoke`, `Legacy parity pending`, `Smoke-tested against Oracle fixture`, `Verified`, `Blocked`, `Deferred`, or `Not API`.

## Pilot Pattern For Repeatable Screens

After the first read endpoint compiles, follow this hardening sequence before starting another operation:

1. Add a backend service test with a fake legacy executor/connection. Assert operation route, screen, target object, `FLAG_PACK` context values, query params, paging/sort, and returned DTO/service behavior.
2. Centralize legacy context resolution. Resource services should ask a provider for `ErgonLegacyContext`; production user/company mapping should live behind replaceable hooks, not inside each service.
3. Add controller or boundary tests for deliberate read-only behavior, especially write endpoints inherited from generic resource controllers.
4. Run module tests with the required JDK/toolchain and record the command in `read-parity-results.md`.
5. Run one live smoke test with a legacy/browser-confirmed fixture and record request, response key fields, user, transaction, and company.
6. If the screen is user/profile scoped, run at least one allowed and one denied user fixture. A denied fixture must prove the row is omitted or forbidden, not merely returned with a denied permission flag.
7. Update `api-contract.md`, `read-parity-matrix.md`, and `read-parity-results.md` with exact states and remaining gaps.
8. Keep remaining filters, company isolation, and restricted-user parity as explicit backend follow-ups until fixtures are available.

## Case and Prompt Guidance

Use [read-operation-prompt-examples.md](references/read-operation-prompt-examples.md) when the user wants PT-BR prompts for list, detail, options, related tabs, and read-only hardening.

## Do Not

- Do not implement writes in this skill.
- Do not mark a read endpoint ready if write is unknown and the screen contains visible write actions; write can be blocked/deferred, but not ignored.
- Do not use generated CRUD write behavior from read resources.
- Do not trust a view name as the full data lineage; use the discovery artifacts and Oracle expansion.
- Do not simplify legacy filters unless parity explicitly accepts the change.
