---
name: ergon-fieldspec-ui-contract
description: Validate and design Praxis metadata DTO, FilterDTO, option, OpenAPI x-ui, and Angular dynamic-field control contracts for Ergon/Archon migrations. Use when mapping @UISchema, @Filterable, schemas, filters, selects/options, date ranges, duplicate drafts, command DTOs, or when checking whether @praxisui Angular can render fields generated from Java annotations.
---

# Ergon FieldSpec UI Contract

Use this skill to close the contract between migrated Java APIs and the Angular dynamic UI. It is a gate skill: it verifies that DTO/FilterDTO annotations, OpenAPI `x-ui`, resource endpoints, and Angular controls match before frontend work starts.

This skill is versioned from `codex-skills/ergon-fieldspec-ui-contract`. If the installed copy under `$CODEX_HOME/skills` diverges, update this canonical source first and then sync it to the local installation.

## Core Rule

Do not assume a control is supported because it exists in one layer. A field contract is valid only when the backend emits the intended `x-ui` and the Angular library can normalize and render it.

Do not close this gate using only static code inspection. When endpoints already exist, execute the schema/options endpoints the frontend will call and record the actual metadata and response wrappers. Static OpenAPI assertions are useful, but they are not proof that Angular can consume the running backend.

For published examples, demos, and corporate-facing surfaces, validate both contract and presentation. A filter is not ready if it works technically but exposes implementation suffixes, ambiguous labels, missing tooltips, duplicate selected values, or labels that hide the business effect of the predicate.

## When To Run

Run this skill:

- during Phase 2 when designing `filter`, detail, `by-ids`, and options contracts;
- during Phase 3 when adding OpenAPI/schema/x-ui tests;
- during Phase 5 when creating command DTOs for create, update, delete, duplicate, legal documents, publications, or pending flows;
- during Phase 6 when implementation may change DTOs or inherited FieldSpec endpoints;
- during Phase 6.5 when Angular wiring consumes schemas, HATEOAS/actions, options, selected reload, filters, forms, or write metadata;
- before frontend handoff.

## Required Inputs

- Screen operation inventory and API contract candidates.
- DTO, FilterDTO, command DTO, option DTO, controller, service, and OpenAPI paths.
- Legacy field evidence: label, component type, bind, null/default behavior, validation message, and business semantics.
- For Ergon domain documentation, `D:\Developer\Techne\ErgonX\migracao\docs-legado` is the primary source of truth when available. Use it before writing or approving `@Schema.description`, `@UISchema.helpText`, filter semantics, option labels, command DTO text, governance notes, or AI-facing metadata.
- Target local code for `praxis-metadata-starter`, `praxis-ui-angular`, and the application module.

## Workflow

1. Classify each field role: grid, detail, filter, form, options source, hidden/internal, action state, or related resource.
2. Choose DTO and FilterDTO shape from behavior, not only database type.
3. Add or review `@Schema`, `@UISchema`, validation annotations, and `@Filterable` where applicable. Treat this as public product documentation, not only UI metadata: descriptions must explain the business role of each field, filter, option, command, and relationship using legacy evidence and docs-legado where available.
4. Validate the backend contract:
   - `FieldControlType` contains the serialized value;
   - `CustomOpenApiResolver` / `OpenApiUiUtils` preserves it in `x-ui`;
   - resource endpoints expose `filter`, detail, `by-ids`, `options/filter`, `options/by-ids`, and schemas when needed;
   - `/schemas/filtered` can resolve response and request schemas for the exact resource path, operation, and schema type that Angular will request;
   - enum arrays and collection fields expose options on the parent field `x-ui` shape consumed by Angular, not only on an item schema that the normalizer cannot see;
   - plain non-enum arrays do not receive empty or misleading `x-ui` select metadata merely because they are arrays;
   - `/schemas/flex?entity=...` returns a non-error response when Angular dynamic forms or flexible-field metadata request it, or the absence of flexible fields is explicitly documented as a non-blocking residual, classified as accepted-gap with owner and next action;
   - resource `filter` endpoints follow their resource response contract, while generic options endpoints follow the current Praxis options contract consumed by `GenericCrudService`: bare `Page<OptionDTO>` for `POST /options/filter` and bare `List<OptionDTO>` for `GET /options/by-ids`;
   - option-source endpoints follow the same no-envelope options convention: bare `Page<OptionDTO<Object>>` for `POST /option-sources/{sourceKey}/options/filter` and bare `List<OptionDTO<Object>>` for `GET /option-sources/{sourceKey}/options/by-ids` or its contextual POST variant;
   - dependent option sources prove selected-value reload separately from filtering: `GET .../by-ids` is enough only when the public ID is self-contained, otherwise `POST .../by-ids` must carry the required public filter/dependency context through the current backend and Angular path;
   - command DTOs hide derived/internal fields and use `copyOnDuplicate` deliberately.
   - when the API is implemented, execute the running endpoints that provide this contract and record payload/response evidence, not only generated OpenAPI.
5. Validate the Angular contract:
   - `FieldMetadata` accepts the metadata;
   - `schema-normalizer.service.ts` propagates the `x-ui` keys;
   - `praxis-dynamic-fields` has a renderable component for the control; treat `ComponentRegistryService.getRegisteredTypes()` and direct inspection of the current component registry as the renderability source of truth, not the Java enum or TypeScript union;
   - naming mismatches and aliases are resolved deliberately through the current Praxis selector/control-type mapping, not by inventing host-local aliases;
   - field configurator support exists when authoring is required;
   - list/select components can call the expected endpoints;
   - selected-value reload uses an ID shape that the current Angular code will actually pass to `/options/by-ids`, including explicit evidence for composite IDs or option-source contextual reload; if Angular cannot send required context yet, downgrade the handoff to a platform follow-up instead of declaring the source reusable.
   - HATEOAS/action metadata or equivalent action state exposes only operations implemented with parity evidence; blocked/deferred operations must be omitted, hidden, disabled, or blocked deliberately.
6. Verify service semantics:
   - JPA filters may use `@Filterable`;
   - JPA FilterDTO aliases such as `statusIn`, `statusNotIn`, `periodoBetween`, `criadoEmOn`, `inicioPrevLastDays`, and other operator-specific fields must declare `relation` when the DTO property name is not the entity/view attribute name;
   - every `IN` and `NOT_IN` filter with an alias-like property must be checked against the actual entity/view field, because otherwise the specification builder can target the DTO field name instead of the persistent attribute;
   - legacy SQL/PLSQL services must translate each FilterDTO field manually to the proven legacy predicate;
   - options endpoints must support filtering, paging, sorting, selected-value reload, and dependency filters.
7. Add or update tests and artifacts:
   - OpenAPI/schema assertions for `x-ui`;
   - controller/service tests for options and filter payloads;
   - parity cases for each visible filter/control;
   - reflective or schema contract tests that fail when `IN`/`NOT_IN` filter aliases omit `relation`;
   - `ui-contract-checklist.md` or equivalent section in the screen docs. In this workspace, use `docs/migracao/ui-contract-checklist-template.md` when available.

## Semantic Documentation And Future Consumers

For Ergon migrations, rich DTO/OpenAPI annotations are part of the platform contract. They feed not only Angular runtime rendering, but also OpenAPI, `/schemas/filtered`, `/schemas/domain`, catalogs, AI/RAG flows, authoring tools, and future `praxis-config-starter` consumers such as governed metadata, templates, registry/config surfaces, and AI-assisted configuration.

Apply these rules before closing the FieldSpec gate:

- Consult `D:\Developer\Techne\ErgonX\migracao\docs-legado` and the local screen evidence before describing business fields, filters, commands, states, relationships, or option semantics.
- Write `@Schema.description` property by property with the field's business meaning, operational impact, source of truth, relationships, constraints, and misuse risk when relevant. Do not derive descriptions from camelCase, database names, enum constants, or `@UISchema.label`.
- Use `@UISchema.label` for short UI copy and `helpText` for operator-facing interpretation; do not let UI labels substitute for domain documentation.
- Record the legacy source used when the annotation changes sensitive business meaning, such as HR/employment data, payroll/financial behavior, legal documents, authorization, HADES/session scope, write side effects, or AI-visible metadata.
- If docs-legado is missing or inconclusive, say so in the migration artifact and limit the annotation to behavior proven by XML, runtime evidence, Oracle probes, services, and tests.
- Pair this skill with `praxis-dto-annotations` whenever the work creates or changes DTO descriptions, governance, AI policy, `@Operation`, `@ResourceIntent`, `@UiSurface`, `@WorkflowAction`, or other metadata that will be consumed beyond Angular rendering.

## Angular Host Handoff

Before handing a FieldSpec contract to Angular implementation, classify host/runtime fit with the same vocabulary used by `praxis-angular-host-project`: `already-supported`, `supported-partially`, `platform-gap`, or `migration-skill-gap`.

Apply native Praxis first for frontend consumption. Confirm the intended table, form, CRUD, surface, option, action, and capability behavior can be consumed through official Praxis components, services, outputs, adapters, tokens, and metadata-driven paths before accepting host-owned launchers, local schema projection, CSS selectors, manual related-resource tables, or local event bridges.

If the backend emits a technically valid schema but Angular needs local `FormConfig`, local labels, DOM selectors, or manual actions to achieve the target UX, do not silently approve the handoff as canonical. Either return to DTO/schema/platform contract hardening or record a traceable Praxis platform follow-up with the smallest temporary host bridge and its removal trigger.

For Angular host implementation details, use `praxis-angular-host-project`; keep this skill focused on proving that DTO, OpenAPI, options, schemas, and action metadata are renderable without frontend semantic compensation.

## Standard Mapping

| Legacy need | New contract |
| --- | --- |
| Consultar/listar | `POST /<resource>/filter`, FilterDTO, `filterable=true`, OpenAPI request/response schemas. |
| Ler detalhe | `GET /<resource>/{id}`, stable public ID, hidden technical keys. |
| Schemas | Global `/schemas/filtered?path=...&operation=...&schemaType=...` metadata resolution for list/detail/filter/options/write schemas consumed by Angular. |
| Options/lookups | `POST /<resource>/options/filter`, `GET /<resource>/options/by-ids`, bare `Page<OptionDTO>`/`List<OptionDTO>` responses, `OptionDTO(valueField, displayField)`, select `@UISchema(endpoint, displayField, filterField, sortField, sortOrder, optionsPageSize)`. |
| Periodo | Date array/list field, `controlType = DATE_RANGE`, ISO dates, service predicate matching legacy interval semantics. |
| Incluir/excluir valores | Alias FilterDTO with `IN`/`NOT_IN`, `relation` pointing to the persistent field, business label such as "Mostrar status" or "Ocultar status", and tooltip explaining inclusion/exclusion. |
| Novo/Editar | Command DTO or write DTO when read DTO has derived/internal fields; validation and schema request tests. |
| Apagar | Delete endpoint only after write audit; no accidental inherited delete if operation is blocked. |
| Duplicar | `duplicate-draft`, `DuplicateDraftResourceService`, `DuplicateDraftUtils`, deliberate `copyOnDuplicate` and `unique` annotations. |
| Cancelar | Frontend no-op/reset; no backend mutation endpoint. |
| Documentos legais/Publicacoes/Pendencias | Related resource contract unless evidence proves they belong to the same resource. |

## Filter DTO Review

For `FilterDTO` classes, review both machine semantics and human-facing metadata.

- Treat operator suffixes (`In`, `NotIn`, `Between`, `On`, `Before`, `After`, `LastDays`, `Ids`) as implementation details, not publication labels.
- Prefer labels that describe the user decision: `Mostrar status`, `Ocultar status`, `Periodo previsto`, `Criadas em`, `Ultimos dias`, `Responsaveis`, or the domain equivalent backed by evidence.
- Use `helpText` or tooltip metadata to explain the effect, especially for exclusion filters. Example: "Remove do resultado as missoes nos status selecionados."
- Avoid raw technical names such as `Ameacas ID`, `Fim Prev Between`, `Fim previsto na data (Excluir)`, or labels that mix operation and field mechanically.
- For `IN` and `NOT_IN`, prove the selected values map to valid enum/option values and that invalid values fail as validation, not as a broken business predicate.
- For enum/list inline filters, execute the running schema endpoint and one browser interaction: open the dropdown, select one option, verify the selected chip/text appears once, and verify the paired include/exclude filters remain visually distinct.
- For corporate scenarios, validate labels and tooltips with the same standard as product documentation. They should tell a developer what the platform can express and tell an operator what the filter will do.

## Hard Gates

- No DTO, FilterDTO, command DTO, option DTO, action, or surface handoff with empty, generic, label-derived, camelCase-derived, or purely technical `@Schema.description` when the contract is public.
- No Ergon business annotation handoff without consulting `docs-legado` where relevant and recording a source/evidence note for sensitive or domain-critical semantics.
- No select-like field without either small static `options` or a real `endpoint` with `/options/filter` and `/options/by-ids`.
- No remote select without `filterField`, `sortField`, `sortOrder`, and a deliberate `optionsPageSize`.
- No static `options` handoff unless the option shape is compatible with the current Angular normalizer. Prefer `[{ "valueField": "...", "displayField": "..." }]` or `[{ "key": "...", "value": "..." }]`; do not assume backend enum output shaped as `{ "value": "...", "label": "..." }` renders correctly without evidence.
- No enum array or list handoff when options exist only on the item schema and the parent property lacks the `x-ui.options` shape Angular will render.
- No plain array field should be promoted to select-like `x-ui` metadata without enum/options evidence.
- No schema assertion for remote selects that expects the final `x-ui.displayField` to remain the business DTO field. The resolver normalizes select-like controls to `OptionDTO` (`valueField`/`displayField`); assert the business search/sort fields through `filterField` and `sortField`.
- No selected-value reload handoff for composite IDs unless the current Angular component has evidence that it calls `/options/by-ids` or the contextual option-source by-ids endpoint for that ID shape. Do not use old `BaseDynamicListComponent` behavior as current evidence; inspect the active `praxis-dynamic-fields` component and `GenericCrudService`. A passing `POST /option-sources/{sourceKey}/options/filter` smoke does not prove reopen/edit hydration.
- No `/schemas` handoff without proving the exact `/schemas/filtered` query Angular uses, including `path`, `operation`, and `schemaType`.
- No dynamic-form handoff when Angular requests `/schemas/flex?entity=...` and that endpoint returns `500`. Absence of flexible fields should return an empty successful result or be formally accepted as a non-blocking residual with owner and next action.
- No `rangeSlider` or specialized control unless it is emitted in `x-ui`, accepted by `FieldMetadata`, and registered in the current `ComponentRegistryService`.
- No use of Java enum values or TypeScript `FieldMetadata` union values as proof of renderability. Controls such as `rangeSlider`, `currency`, `toggle`, `phone`, `arrayInput`, `autoComplete`, `multiColumnComboBox`, and `timePicker` require explicit current Angular registry evidence, documented alias support, or a safer mapped control.
- No alias mismatch handoff without an approved platform mapping. Prefer correcting the canonical Praxis metadata/runtime contract over creating host-local control aliases.
- No `@Filterable(IN)` or `@Filterable(NOT_IN)` alias without `relation` when the property name is not the real entity/view attribute. This includes paired fields such as `statusIn` and `statusNotIn`.
- No `@Filterable(BETWEEN)` as proof of legacy SQL semantics; services must implement the actual predicate.
- No public demo or landing-page example should expose raw FilterDTO/operator labels when deliberate business labels and tooltips can be provided.
- No public `ROWID` or routine flag in UI DTOs unless explicitly accepted and documented.
- No frontend handoff while OpenAPI/x-ui assertions are missing for controls that drive filters or forms.
- No frontend handoff while the running `/schemas/filtered`, options, selected reload, or HATEOAS/action metadata was not executed and compared with the Angular consumption path.

## References

For detailed local evidence and examples, read [fieldspec-angular-contract.md](references/fieldspec-angular-contract.md).
