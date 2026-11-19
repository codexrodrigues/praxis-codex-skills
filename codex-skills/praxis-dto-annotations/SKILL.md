---
name: praxis-dto-annotations
description: "Annotate or review Java DTOs, FilterDTOs, command DTOs, and OpenAPI metadata for hosts that use praxis-metadata-starter. Use when Codex must fill or correct @Schema, @UISchema, @Filterable, @DomainGovernance, AiUsagePolicy, FieldControlType, x-ui labels/help text/icons/groups/order/visibility/valuePresentation/numericFormat/mask, table display formatting, option endpoints, optionSource/entityLookup metadata, or PT-BR domain documentation in Praxis backend projects."
---

# Praxis DTO Annotations

Use this skill to make DTO metadata self-describing for Praxis. Treat DTO annotations as public
contract because they feed OpenAPI, `/schemas/filtered`, `x-ui`, `/schemas/domain`, catalogs, RAG,
AI authoring, and the official Angular runtime.

This skill is versioned from `codex-skills/praxis-dto-annotations`. If the installed copy under
`$CODEX_HOME/skills` diverges, update this canonical source first and then sync it locally.

Before changing this skill or annotating DTOs, inspect the resolved starter/source for the emitted
contract: `@UISchema`, `FieldControlType`, `FieldDataType`, `NumericFormat`, `@Filterable`,
`UISchemaPreset`, `@DomainGovernance`, `AiUsagePolicy`, option-source descriptors, `CustomOpenApiResolver`,
`/schemas/filtered`, `/schemas/domain`, and representative host DTOs/tests when available. The
goal is to codify what the platform already publishes before adding annotation fields, local
`extraProperties`, host renderers, or AI-facing prose.

## Reusable API paths in annotations

Before wiring remote options, create or extend the host-owned `final ApiPaths`
(private constructor, `public static final String` compile-time constants).
Compose resource bases, stable source keys and named filter endpoint constants
once. Reuse them in controllers, `OptionSourceDescriptor`, DTOs, FilterDTOs,
command DTOs, surfaces and links. Do not concatenate option-source paths in each
DTO, put deployment origins in annotations, use a constants interface, call
methods to initialize annotation values, or introduce a DTO `optionSource` field.
Static/enum options need no remote endpoint. Keep governed lookup semantics in
`OptionSourceRegistry` and consume the published runtime endpoints in Angular.
Validate annotation endpoints against descriptor runtime endpoints and controller
mappings; keep independent literal contract fixtures to catch accidental route
changes. Recompile consumers when constants change. For the complete decision,
see `praxis-metadata-starter/docs/guides/API-PATHS-E-OPTION-SOURCES.md` when available;
the rules above also apply outside the monorepo.

Keep constant-holder classes independent of inheritance. DTO inheritance itself
is not a reason to waive or fail endpoint proof: pass the exact declaring type
and the selected dependency sources (directory or sources.jar) to the auditor.
It traverses known superclasses/interfaces and proves imported references when
no inherited member can shadow them; annotation/method uses are not declarations.
Do not whitelist marker interfaces or host names. Missing/ambiguous/cyclic source
graphs, possible inherited-member collisions and unsupported syntax stay unproved;
never fall through to imports or outer scopes on a failed binding. A file-only
caller cannot infer the owner of an annotation in a multi-type source file.
Record the source-universe fingerprint and retain compiler regressions for both
valid inheritance and shadowing. Static proof does not replace the host Java gate.
When changing lookup examples, compile the exact documentation snippets against
the selected starter artifact and verify descriptor semantics, not only skill
syntax or manifest hashes. In the canonical skills repository, run
`python scripts/check-java-lookup-example.py --java-home <JDK> --classpath <starter.jar>`
for the host baseline; record the artifact version/hash and the integration limits.


## Required Pairing

*(In external Antigravity workspaces, full companion skills are available under `~/.gemini/praxis-skills/<skill-name>/SKILL.md` or `$CODEX_HOME/skills/<skill-name>/SKILL.md`.)*

Use `praxis-java-host-project` with this skill when creating or changing a Java host resource.
Use `praxis-resource-entity-lookup-backend` as well when a field uses `ENTITY_LOOKUP`,
`INLINE_ENTITY_LOOKUP`, `RESOURCE_ENTITY`, `OptionSourceRegistry`, or
`/{resource}/option-sources/*`.
Use `praxis-dynamic-fields-editorial` when changing control vocabulary or Angular renderability,
because Java enum presence is not enough proof that the official UI can render a control.
Use `praxis-ui-product-design` when `@UISchema` work materially affects visual UX, hierarchy,
iconography, grouping/layout, responsive behavior, official examples, or reusable UI patterns.

Do not use consumer-specific fieldspec guidance for ordinary Praxis resources. The canonical owner is `praxis-metadata-starter`.

## Classification

Classify DTO annotation changes before editing:

- `contrato-publico`: any change to DTO fields, `@Schema`, `@UISchema`, `@Filterable`,
  `@DomainGovernance`, option metadata, OpenAPI examples, `x-ui`, or `/schemas/filtered`.
- `transversal`: host plus docs/examples/http corpus/skills/Angular examples.
- `local-pequena`: private implementation detail with no schema or public annotation impact.
- `docs-apenas`: prose-only documentation outside emitted contract.

For `contrato-publico` or `transversal`, map impact first: canonical owner, affected consumers,
public docs, examples/playgrounds/http corpus, minimum validation, and breaking-change risk.

## Canonical Sources

Prefer these local sources when available:

- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/extension/annotation/UISchema.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/extension/annotation/UISchemaPreset.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/NumericFormat.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/UiOption.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/option/PraxisUiOptionEnum.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/TableView.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/UiFormLayout.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/UiSection.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/LayoutMode.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/CalculationMemory.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/CalculationTrail.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/CalculationStep.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/StepKind.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/exporting/CollectionExportFieldPresentation.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/QuickFilter.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/FilterCriterion.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/QuickFilterTone.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/schema/QuickFilterDescriptor.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/ResourceIdentity.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/ResourceReference.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/ReactiveDetermination.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/DeterminationOutput.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/BulkEditable.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/bulk/BulkResourceOperations.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/fact/ResourceFact.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/FieldControlType.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/filter/annotation/Filterable.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/annotation/DomainGovernance.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/options/OptionSourceDescriptor.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/options/OptionSourceRegistry.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/options/EntityLookupDescriptor.java`
- `praxis-metadata-starter/src/main/java/org/praxisplatform/uischema/options/OptionSourcePolicy.java`
- `praxis-metadata-starter/docs/guides/GUIA-06-REDACAO-SEMANTICA-DE-ANNOTATIONS-PARA-IA.md`
- `praxis-metadata-starter/docs/spec/README.md`
- `praxis-metadata-starter/docs/spec/x-ui-field.schema.json`
- `praxis-metadata-starter/docs/spec/x-ui-option-source-rfc.md`
- `praxis-metadata-starter/docs/spec/CONFORMANCE.md`
- `praxis-metadata-starter/docs/guides/OPTIONS-ENDPOINT.md`
- `praxis-metadata-starter/docs/guides/SEMANTIC-METADATA-AUTHORING.md`
- `praxis-ui-angular/ICON-PREFIXES.md` and the target Angular host's icon/runtime
  configuration when the task affects iconography or UX.
- The target host's own controllers, DTOs, entities, services, validation tests, and Angular host
  conventions when they are available in the current workspace.

Do not require any reference host checkout. The skill must work in consumer environments where only
the target host and starter dependency/documentation are present.
When starter source is unavailable, use resolved dependency docs, source jars/Javadocs, Maven
metadata, `javap` against resolved jars if necessary, generated OpenAPI, `/schemas/filtered`, and
focused host HTTP/schema smokes. Do not require local monorepo source to annotate a consumer host.

## Workflow

1. Read local `AGENTS.md` files and classify the change.
2. Identify the resource boundary: controller, `@ApiResource(resourceKey=...)`, DTOs, FilterDTO,
   create/update/action DTOs, entity/view, mapper, service, relationships, option sources,
   stats/analytics registries, and tests.
3. Read the real domain sources before writing text: system documentation, functional
   specifications, legacy manuals, business glossaries, screen/help text, rules, services, and tests
   when they are available. Do not infer business meaning only from property names or UI labels.
   For legacy migration work, treat the consumer workspace's approved legacy documentation as the
   primary source when available, and cite or record the consulted artifact in the host or migration
   package when the annotation changes sensitive business semantics.
4. Decide field role before choosing formatting. Do not rely only on Java/OpenAPI type. Classify the
   information as identifier, editable domain field, resolved display field, hidden technical field,
   filter-only field, relationship ID, option/lookup, command input, result output, monetary amount,
   quantity, percentage/rate, score, date/time, document, contact value, status, metric, dimension,
   sensitive data, or action state.
5. For each public field, decide the four contracts together: domain meaning (`@Schema`), storage or
   transport representation (Java/OpenAPI type), UI control/presentation (`@UISchema`/`x-ui`), and
   executable validation (Bean Validation/service rule). Formatting is correct only when all four
   contracts agree.
   `@UISchema(preset = ...)` may reduce repetitive presentation metadata, but it never writes the
   domain description. A preset without verified `@Schema.description` is incomplete metadata.
   Also check derived eligibility surfaces such as filters, options, stats, analytics, export, and
   AI catalogs so identifiers and documents are not reintroduced as mathematical measures outside
   the DTO annotations.
6. Inventory existing platform support before inventing metadata. Classify each needed improvement:
   already supported but missing in UX, supported but poorly named/materialized, partially supported,
   or a real contract gap. Only a real contract gap justifies changing `praxis-metadata-starter`,
   `@UISchema`, `x-ui`, `@Filterable`, governance annotations, option-source descriptors, or public
   examples. Do not create a second DTO-local concept when the fact already exists in OpenAPI,
   `x-ui`, option sources, surfaces/actions, capabilities, domain catalog, stats/export metadata, or
   config/AI materializations.
7. Fill annotations deliberately:
   - `@ApiResource`/`resourceKey`: stable resource identity, not a local label or URL nickname.
   - `@Operation`: business summary/description for public operations when the host declares them.
   - `@Schema`: domain contract and product documentation.
   - `@UISchema`: presentation, control, layout, helper text, visibility, validation hints,
     value formatting, masks, and table display semantics.
   - `@Filterable`: backend predicate and relation to the real persistent field.
   - `@DomainGovernance`/`AiUsagePolicy`: privacy, compliance, AI visibility/training/reasoning.
   - `@ResourceIntent`, `@UiSurface`, and `@WorkflowAction`: semantic discovery for real HTTP
     operations only, without redefining payloads outside `/schemas/filtered`.
   - Bean Validation: executable validation aligned with schema and UI metadata.
8. Validate the emitted contract with the smallest reliable command. Prefer focused tests,
   `/schemas/filtered`, OpenAPI, and host HTTP/schema smokes over broad suites unless the blast
   radius requires more.
9. Check derived artifacts when public metadata changed: public docs, host examples,
   `praxisui-http-examples`, `docs/ai/*`, recipes, or Angular host examples when present.

### Proactive Domain Expansion For New Resources (First-Shot Excellence)

When a developer or architect asks for a new resource from a brief domain prompt (without manually listing every annotation), do **not** generate bare-bones `@UISchema(label = "Nome")` skeletons. Deliver the complete Praxis semantic contract on the first shot:

1. **Class-Level Identity, Declarative Layout/Table Projection & 100% Domain Column Accounting:** Annotate `ResponseDTO` with `@Schema(name = ..., description = ...)` and full `@ResourceIdentity(keyField = "id", titleField = ..., subtitleField = ..., metadataFields = {...}, displayLabelField = ...)`. (`ResponseDTO` is the mandatory single source of truth; omitting `identity` on `@ApiResource` avoids duplication, though if declared on both Controller and `ResponseDTO` they must remain semantically identical.) Use `@TableView(columns = {...}, pinnedStart = {...}, pinnedEnd = {...})` on `ResponseDTO` (`@Target(TYPE)`) instead of repeating manual `order`/`tableHidden = true` across dozens of fields: `TableView` publishes `x-ui.tableOrder`, `x-ui.pinned` (`"start"`/`"end"`), and automatically sets `x-ui.tableHidden = true` on unlisted fields (reviewed by `SemanticMetadataReviewer` for `tableview-column-unknown` / `tableview-pinned-conflict`). For multi-section forms/details (`FLAT`, `TABS`, `ACCORDION`, `STEPPER`), declare `@UiFormLayout(mode = LayoutMode.*, sections = {@UiSection(id = ..., title = ..., subtitle = ..., icon = ..., order = ..., groups = {...})})` on the DTO (`x-ui.formLayout`, checked for `form-layout-section-duplicate-id` / `form-layout-section-icon-invalid`). Annotate `CreateDTO` and `UpdateDTO` with `@JsonIgnoreProperties({"id"})` and `@Schema(...)`. **Never mutilate or truncate an enterprise entity** by exposing only 8–10 of its 30–55 business columns: expose all business columns in `ResponseDTO`, organizing secondary/detail attributes into semantic `@UISchema(group = ...)` sections with `tableHidden = true` (or `@TableView`) so the main table remains scannable while forms and detail views are 100% complete. Columns mutated exclusively by business commands (`@WorkflowAction`) or partial forms (`@ResourceIntent`) remain `readOnly = true` in `ResponseDTO` and are excluded from generic `UpdateDTO`.
2. **Semantic Grouping, Adjacent Column Alignment & Valid `snake_case` Material Icons:** Organize properties into 3–5 business groups (`group = "Identificação"`, `"Vínculo e Lotação"`, `"Remuneração e Finanças"`, `"Situação Operacional"`), deterministic `order` (`10, 20, 30...`), 12-column grid widths (`colSpan = 1..12`, `0` automatic, emitted as `x-ui.colSpan`), valid lowercase `snake_case` Material icon ligatures (`icon = "badge"`, `"payments"`, `"event_available"`, `"assured_workload"` — never PascalCase `"Assured_Workload"` or invented icon tokens that render raw text in `<mat-icon>`), and `quickViewVisible = true` / `quickViewOrder` on the primary summary fields. When authoring shared `*Dados` superclasses or DTOs with multiple adjacent boolean/incidence/status flags, verify 1:1 column-to-property order against the `@Entity` / DDL so `@Schema` and `@UISchema` descriptions are never swapped between neighboring fields.
3. **Complete Field Triad:** Every property must carry:
   - `@Schema(description = "...", example = "...")` with real PT-BR business role, lifecycle impact, and boundaries;
   - `@UISchema(...)` with `preset` (canonical presets include `ENTERPRISE_ID`, `ENTERPRISE_CODE`, `ENTERPRISE_NAME`, `ENTERPRISE_STATUS`, `DATE_RANGE`, `MONETARY_AMOUNT`, `BOOLEAN_FLAG`, `LEGAL_DOCUMENT_REFERENCE`, `TENANT_LABEL`, `AUDIT_TIMESTAMP`, plus `LOCAL_DATE`, `LOCAL_DATE_TIME`, `INTEGER_COUNTER`, and `ENTITY_LOOKUP`), `type`, `controlType`, `numericFormat` (defaults to `NumericFormat.AUTO`, which omits `x-ui.numericFormat` unless explicitly set or supplied by a preset such as `INTEGER_COUNTER` -> `NumericFormat.INTEGER`), `mask`, `helpText`, `conditionalReadOnly` (JSON Logic expression emitted as `x-ui.conditionalReadOnly`, checked via `uischema-conditional-readonly-invalid`), `colSpan` (`x-ui.colSpan`, `0..12`, checked via `uischema-colspan-invalid`), and visibility (`readOnly`, `formHidden`, `tableHidden`);
   - `@DomainGovernance(..., aiUsage = @AiUsagePolicy(...))` on personal (`PERSONAL`), financial (`FINANCIAL`), sensitive (`SENSITIVE`), or security-scoped fields.
4. **Relationship Pairing, `PraxisUiOptionEnum` & Rich `EntityLookupDescriptor`:** Pair foreign-key fields (`positionId`, `departmentId`) using `ENTITY_LOOKUP` (`UISchemaPreset.ENTITY_LOOKUP` + `tableHidden = true`, pointing to `/option-sources/<sourceKey>/options/filter`) with read-only resolved display fields (`positionName`, `departmentName`, `readOnly = true, formHidden = true`) annotated with `@ResourceReference(resourceKey = "...", valueField = "...Id", surfaceId = "detail", previewSurfaceId = "...", detailPresentation = "drawer")` on `ResponseDTO`. For typed status/domain enums, implement `PraxisUiOptionEnum` (`value()`, `label()`, `icon()`, `tone()`, `selectableInLookup()`, `workflowInitial()`): `OpenApiUiUtils` emits `{value, label, icon, tone}` automatically for `@UISchema(optionEnum = MyEnum.class)`, and `EntityLookupDescriptor.directoryBuilderFromDto(...)` auto-detects `PraxisUiOptionEnum` properties (or `@ResourceState` fields) to populate `statusPropertyPath`, `statusLabelMap`, and `LookupSelectionPolicy` (`allowedStatuses`/`blockedStatuses` from `selectableInLookup()`). In `OptionSourceRegistry`, always populate the complete `EntityLookupDescriptor` (`codePropertyPath`, `descriptionPropertyPaths`, `statusPropertyPath`, `LookupSelectionPolicy` with `allowRetainInvalidExistingValue = true`, `LookupDetailDescriptor` wired to the 360° surface, `LookupDisplayDescriptor`, `LookupFilteringDescriptor`, and cross-field `dependsOn`/`dependencyFilterMap` — never leaving them `null`).
5. **In-Cell `@MicroVisualization`, Backend `@CalculationMemory` + `@CalculationStep`, Governed Export Presentation, `@BulkEditable` & Read-Only Table Scannability:** Annotate occupancy, progress, quota, delta, and distribution fields on `ResponseDTO` with `@MicroVisualization(kind = ..., thresholds = {@Threshold(...)}, valueExpr = ..., targetExpr = ..., totalExpr = ...)` validated by `PraxisExpressionStaticValidator`. When a `ResponseDTO` exposes explainable financial, tax/social-security, constitutional-cap, SLA, or interstice calculations (`Base -> + Additions -> - Deductions -> × Factor/Rate -> ≤ Cap -> = Result`), annotate the DTO class (or inherited `*Dados` superclass) with `@CalculationMemory(title = ..., subtitleExpr = ..., icon = ..., legalBasis = ..., trails = {@CalculationTrail(id = ..., title = ..., ruleCode = ..., formula = ..., visibleWhen = ..., steps = {@CalculationStep(label = ..., expr = ..., format = ..., kind = StepKind.BASE | ADDITION | DEDUCTION | FACTOR | CAP | SUBTOTAL, hintExpr = ..., legalBasis = ...)}, base* = ..., addition* = ..., deduction* = ..., factor* = ..., cap* = ..., result* = ..., legalBasis = ..., legalPurpose = ...)})` (`org.praxisplatform.uischema.annotation.CalculationMemory` / `CalculationTrail` / `CalculationStep` / `StepKind`, `PLAT-EVO-20`): use `steps` for extensible N-step waterfalls or distinct fixed stage fields (never repeating the same field/expression in both `baseExpr` and `additionExpr`), note that `CalculationMemoryMetadataResolver` projects root `x-ui.calculationMemory` on `/schemas/filtered` (`schemaType=response`), run `PraxisExpressionStaticValidator.validateDtoClasses(dtoClasses, true)` in JUnit to statically validate every `row.*` expression (including `@CalculationStep.expr`/`hintExpr`), and let `@praxisui/table`'s `PraxisAnalyticalDrawerComponent` materialize the calculation memory automatically. For tabular exports, `ResourceExportSupport` auto-derives `CollectionExportFieldPresentation` (including `valueLabels` from `@UiOption` / `PraxisUiOptionEnum`) so `AbstractTabularCollectionExportEngine` formats cells consistently when `CollectionExportRequest.applyFormatting() == Boolean.TRUE`. On `UpdateDTO`, annotate fields/methods/record components eligible for batch maintenance with `@BulkEditable(modes = {BulkMode.UNIFORM_UPDATE, BulkMode.PER_ITEM_UPDATE}, allowClear = ...)` (adding `@Schema(nullable = true)` whenever `allowClear = true`). On read-only projection DTOs (`READ_PROJECTION` / `VIEW`), keep 5 to 10 executive columns with `tableHidden = false` and set `tableHidden = true` on secondary detail fields so tables and drawers stay scannable.
6. **High-Power `FilterDTO` Matrix & Inline Promotion (`@Filterable(inline = true)`):** Design `FilterDTO implements GenericFilterDTO` with a rich combination of `@Filterable` predicates (`LIKE` for text, `EQUAL` for status/booleans, `IN` for multi-select relations/enums, `BETWEEN` with `DATE_RANGE` / `PRICE_RANGE` for ranges, and `IN_LAST_DAYS` for relative windows), always setting `relation = "<entityPath>"` whenever the filter property is an alias (`hireDateRange`, `salaryBetween`, `departmentIdsIn`), and annotating `@Filterable(inline = true)` (`praxis-metadata-starter:8.0.0-rc.197+`, emitting `x-ui.inlineFilter = true`) on primary filter criteria that should appear inline in the toolbar/scope bar without duplicating `inlineFilterFields` lists in Angular. See `praxis-java-host-project/references/resource-baseline.md` and `META-INF/praxis/AI-RESOURCE-BLUEPRINT.md` for a full compiling exemplar.

## Contract Boundaries

- `/schemas/filtered` is the structural source for DTO fields, `x-ui`, option metadata, governance
  extensions, request/response schemas, and runtime UI materialization. `/schemas/catalog` documents
  and helps discovery; `/schemas/domain` republishes semantic/domain vocabulary for AI; capabilities
  advertise availability. Do not treat catalog/domain/capability snapshots as replacement structural
  schemas.
- `@Schema.description` and `@UISchema.label/helpText` do not decide user intent. They provide
  evidence for semantic resolution, RAG, catalog discovery, and UI explanation after the platform has
  grounded the target resource/operation/field through canonical contracts.
- Do not add keyword-rich labels, aliases, hidden command strings, regex-oriented field names, or
  generic examples so assistants can route intent. If AI cannot resolve a field, improve canonical
  descriptions, resource identity, operation/surface/action metadata, domain catalog, or declared
  tools instead of adding DTO text-routing workarounds.
- `@UISchema.extraProperties` is only for public `x-ui` keys that already exist in the resolved
  schema/runtime or for an explicit platform contract change. Do not use it to smuggle host-private
  renderers, table-only shortcuts, option-source descriptors, governance facts, or AI instructions.

## Documentation Areas

Every DTO property must be documented across all applicable Praxis areas. Do not stop at Java type
or UI control selection; the metadata must explain business meaning, presentation, governance, AI
use, filtering, analytics, and operational constraints when they apply.

### Domain and Product Semantics

- `@Schema.description` must explain what the field represents in the business process, who uses it,
  what real-world object/event/value it identifies or measures, and what can go wrong if it is wrong.
- Document the field's role in that resource, not the dictionary meaning of the word. For example,
  an `email` field can be a contact channel, a login key, a notification routing address, an
  external identity, an ownership proof, or a unique registry key; the correct description depends
  on the business process and source documentation.
- Include verified product constraints when present: lifecycle state, organizational scope, temporal
  validity, uniqueness, source of truth, relationship to parent/child resources, and whether the
  value is derived or user-entered.
- Do not use descriptions that merely repeat `@UISchema.label`, Java type, property name, database
  column name, or enum constant name.
- When the agent has access to product/system documentation, it must consult it to learn the field's
  business meaning before documenting the DTO. If documentation is missing or inconclusive, say so
  in the implementation notes and write only claims supported by code behavior.
- For legacy-backed domain DTOs, prefer approved legacy documentation plus runtime/database
  evidence over labels, XML/property names, table names, or inferred camelCase meaning. The result
  should be useful for future Praxis metadata/config consumers, including `praxis-config-starter`
  registries, templates, catalogs, and AI-assisted configuration surfaces.
- Prefer precise PT-BR product language. Avoid vague text such as "código do registro", "data do
  cadastro", or "informação do usuário" unless domain analysis proves that is the full semantics.

### UI, Table, and Presentation Metadata

- `@UISchema.label` is short PT-BR UI copy (1 to 4 words, max ~35 characters, never ending with a period `.`, and **never** a copy of `@Schema.description`); `helpText` explains how to fill or interpret the value; `placeholder` is only an input example and must not replace domain documentation.
- Every `LocalDate` / `LocalDateTime`, `BigDecimal`, or foreign-key (`*Id`) property must explicitly declare `type` (`FieldDataType`), `controlType` (`DATE_PICKER`, `DATE_TIME_PICKER`, `CURRENCY_INPUT`, `ENTITY_LOOKUP`, `SELECT`, etc.), and `icon` in `@UISchema(...)`. Declaring `UISchemaPreset` complements presentation formatting, but **does not replace** explicit `type`, `controlType`, and `icon` (checked by `audit-java-resource-completeness.py`).
- Choose `FieldControlType`, mask, `valuePresentation`, `numericFormat`, date/time format, alignment, grouping, visibility, read-only/hidden state, and icon from the information role, not only from the Java type.
- Table/list metadata must be complete enough that Angular hosts do not need custom presentation code for common values: CPF, CNPJ, CEP, telefone, e-mail, moeda, percentual/taxa, quantidade, data, data e hora, status, booleano, codigo/identificador, documento, protocolo, and resolved lookup display values.
- Numeric-looking identifiers, document numbers, phone numbers, fiscal keys, and protocol numbers must be treated as text/display values with masks when needed. They are not decimal numbers and must not receive locale numeric formatting such as `7,00`.
- Use host/project icon conventions. For Angular hosts this normally means Material icon names, not arbitrary icon sets invented in DTO metadata.
- **Mandatory Quick View / 360° Contract on Every Resource:**
  1. Declare `@ResourceIdentity(keyField = ..., titleField = ..., subtitleField = ..., avatarField = ..., metadataFields = {...}, displayLabelField = ...)` on `ResponseDTO` (mandatory single source of truth; omitting `identity` on `@ApiResource` is preferred, and if declared on both Controller and `ResponseDTO` they must remain identical — both `subtitleField` **AND** `metadataFields = {...}` are **mandatory**, never leaving `@ResourceIdentity` with only `keyField` and `titleField`).
  2. Curate **4 to 8 high-signal executive summary fields** on every `ResponseDTO` with `@UISchema(quickViewVisible = true, quickViewOrder = ...)` so the Quick View card body is populated. Remember that `ResourceQuickViewService.buildSummaryItems` promotes `metadataFields` to the **first rows** of the Quick View card body before `quickViewVisible` fields: never repeat `keyField` (e.g. `"id"`), `titleField`, `subtitleField`, or `avatarField` inside `metadataFields` or `quickViewVisible`, never overlap `metadataFields` with `quickViewVisible`, and never put low-signal/raw-code fields (`tratamento`, nullable `observacao`, raw numeric FK IDs, or untranslated catalog codes without `FieldControlType.SELECT` + `@UiOption` / `optionEnum`) in `metadataFields` or `quickViewVisible`. Declare closed static options with `@UISchema(controlType = FieldControlType.SELECT, optionItems = {@UiOption(value = "...", label = "...", icon = "...", tone = QuickFilterTone.*)})` (`org.praxisplatform.uischema.annotation.UiOption`, where `QuickFilterTone` exposes the unified 10-token semantic scale: `NEUTRAL`, `PRIMARY`, `SECONDARY`, `INFO`, `SUCCESS`, `WARNING`, `DANGER`, `CRITICAL`, `POSITIVE`, `NEGATIVE`) or `optionEnum = MeuEnum.class` — respecting mutual exclusivity (`uischema-options-source-conflict`), non-empty `enum` (`uischema-option-enum-invalid`), unique non-blank `value`, concise `label <= 36` chars without a trailing period, lowercase `snake_case` Material Icons `icon` without `"mi:"`, and avoiding `@Deprecated(since = "2.1.0")` stringified `options = "..."`. Order `quickViewOrder = 1..N` by executive priority: (1) status/badge (`situacao`, `ativa` with lowercase `snake_case` `icon`), (2) human-readable role/allocation (`cargoNome`, `setorNome`, `estcivil`, `escolaridade`), (3) key dates/contact channels (`dtexerc`, `dtnasc`, `eMail`, `numtelCelular`), and (4) integer counters/indicators (`NumericFormat.INTEGER` so integers never render with `,00`). See `praxis-metadata-starter/docs/guides/QUICK-VIEW-360-E-CURADORIA-EXECUTIVA.md`.
  3. Annotate the resource's own primary title field AND every foreign-key display projection (`departmentName`, `managerName`, `positionName`, `costCenterName`, `customerName`, `supplierName`, etc.) with `@ResourceReference(resourceKey = "...", valueField = "...", surfaceId = "detail", previewSurfaceId = "...", detailPresentation = "drawer")` (`detailPresentation` supports `"drawer"` or `"modal"`, checked by `SemanticMetadataReviewer`) so `/schemas/filtered` publishes `x-ui.resourceReference` and Angular surfaces (`@praxisui/table`, `@praxisui/list`, `@praxisui/rich-content`) synthesize governed Quick View 360° overlays automatically.
- Before closing any DTO authoring task, run `python scripts/workspace/audit-java-resource-completeness.py <path-to-host> --strict` and verify `QuickViewCols >= 4`, `RichIdentity = YES`, and `EditorialIssues = 0`. Preserve the full output/exit code. For a declared phase/increment, apply `praxis-java-contract-conformance` acceptance classification: DTO/current-phase failures, regressions and required controls block closure; future-only obligations remain pending. The auditor has no phase selector; final resource acceptance still requires its full pass and all other mandatory gates.

### Governance, LGPD, and Compliance (Declarative Metadata Only)

- **Exact Canonical Attributes of `@DomainGovernance` and `@DomainLineage`:** Use only the 9 real attributes of `@DomainGovernance` (`org.praxisplatform.uischema.annotation.DomainGovernance`): `preset` (`DomainGovernancePreset.NONE | LGPD_PERSONAL_ID | LGPD_PERSONAL_CONTACT | LGPD_SENSITIVE_DATA | CONFIDENTIAL_FINANCIAL | PUBLIC_TRANSPARENCY_REMUNERATION | SECURITY_CREDENTIAL | INTERNAL_OPERATIONAL | LEGAL_COMPLIANCE`), `kind` (`DomainGovernanceKind.PRIVACY | SECURITY | COMPLIANCE`), `classification` (`DomainClassification.PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED`), `dataCategory` (`DomainDataCategory.CREDENTIAL | SENSITIVE_PERSONAL | PERSONAL | FINANCIAL | OPERATIONAL | LEGAL`), `complianceTags` (`{"LGPD", "PII"}`, `{"LAI", "LGPD_ART_23", "PUBLIC_TRANSPARENCY_REMUNERATION"}`), `exportable` (`boolean`, default `true`), `aiUsage = @AiUsagePolicy(visibility = AiVisibilityMode.ALLOW | MASK | SUMMARIZE_ONLY | DENY, trainingUse = AiTrainingUseMode.ALLOW | DENY, ruleAuthoring = AiControlledUseMode.ALLOW | REVIEW_REQUIRED | DENY, reasoningUse = AiControlledUseMode.ALLOW | REVIEW_REQUIRED | DENY)`, `reason`, and `confidence` (default `1.0d`). `@DomainGovernance` also supports `@Target(ElementType.TYPE)` for class/interface-level baseline inheritance with restrictive monotonic merging. Prefer `preset = DomainGovernancePreset.*` with `reason = "..."` to keep DTOs concise when the standard profile applies: in public-sector compensation/payroll DTOs (`PLAT-EVO-13`), apply `PUBLIC_TRANSPARENCY_REMUNERATION` (`PUBLIC` + `FINANCIAL` + `exportable = true` + `aiVisibility = ALLOW`) to gross statutory remuneration, career tables, and constitutional cap fields subject to active transparency (LAI), while keeping `CONFIDENTIAL_FINANCIAL` (`CONFIDENTIAL` + `exportable = false` + `MASK`) on private deductions (alimony, payroll loans, union dues, private health plans, bank accounts) in the very same DTO. Pair projected DTO properties with `@DomainLineage(attributeId = "...", sourceClass = ..., sourcePaths = {...}, transformation = ...)` (keeping `@DomainGovernance` on the DTO property so DTO contracts stay self-contained and pass `lineage-governance-weakened`). **Never invent non-existent attributes or enums** on `@DomainGovernance` such as `owner`, `steward`, `retentionPolicy` (which belong to `GovernanceSummary` in `/schemas/domain` and `DomainRuleDefinition` in `praxis-config-starter`, not `@DomainGovernance`), `sensitive`, `lgpdPurpose`, `maskingPattern`, `DomainFieldKind`, or `DomainDataClassification`.
- **Automatic Lookup & Policy-Studio Fact Introspection from DTO Annotations (`PLAT-EVO-06`, `PLAT-EVO-09`):** Marking visible natural/business codes on `ResponseDTO` with `preset = UISchemaPreset.ENTERPRISE_CODE` lets `EntityLookupDescriptor.directoryBuilderFromDto(...)` automatically prioritize that business code over surrogate `id` in `codePropertyPath` and `searchPropertyPaths`. Similarly, `DtoMetadataFactCatalogEnricher` introspects `@Schema` and `@UISchema` across standard DTO classes, inherited `*Dados` superclasses, Java `record`s, and write DTOs (`inspectWriteDto`) to enrich `praxis-policy-studio` fact catalogs with human PT-BR labels, descriptions, types, and closed options without manual duplication.
- **Praxis Decision Platform (`praxis-authz-*` vs. `praxis-rules-engine`) Architectural Boundary:** `@DomainGovernance`, `@DomainLineage`, and `@UISchema(visibleForAuthorities = {...}, editableForAuthorities = {...}, fieldAccessReason = "...")` are **strictly declarative semantic metadata** published in `/schemas/filtered` (`x-domain-governance`, `x-domain-governance.lineage`, `x-ui.fieldAccess`) and `/schemas/domain` (`?strict=true`) for AI assistants, export allowlists, and `praxis-authz-starter` / `praxis-authz-enforcement-core` / `praxis-authz-opa` (`decisionKind = AUTHORIZATION`, `ruleType = "authorization_policy"`). Do not introduce ad-hoc runtime security enforcement or field masking inside DTO getters, mappers, or controllers.

- Use `@DomainGovernance` when the field contains or controls personal data, sensitive personal data,
  employment/HR data, payroll or financial data, health/benefit data, access/security data,
  audit/provenance data, contractual data, or any restricted-purpose value.
- Document the verified product purpose, intended visibility, masking/redaction expectations, export
  eligibility, logging/audit implications, retention relevance, and whether the value may appear in
  lists, filters, analytics, RAG, assistant context, or generated documents.
- If legal basis, retention rule, or consent model is not explicit in code or source documentation,
  do not invent it. Record only the verifiable purpose and leave the governance gap visible for
  domain review.
- Default to least exposure for sensitive fields: hidden, read-only, masked, export-restricted,
  analytics-excluded, and AI-excluded unless a governed use case proves otherwise.

### AI, RAG, and Agent Behavior

- Set `AiUsagePolicy` and related AI metadata deliberately. Decide whether the field may be used for
  display, retrieval, reasoning, summarization, explanation, recommendation, automated action,
  training, or must be excluded.
- Fields containing secrets, credentials, tokens, raw documents, private notes, disciplinary data,
  medical/benefit information, payroll details, security context, or high-risk personal data must be
  excluded or masked for AI unless an explicit governed use case exists.
- AI-facing descriptions must explain business semantics, valid interpretation, misuse risk, and
  relationships to other fields. Avoid ambiguous words like "data", "info", "codigo", or "valor"
  without the domain qualifier.
- For command/action DTOs, document side effects, confirmation needs, reversibility, idempotency
  expectations, authorization relevance, and validation boundaries so agents do not treat a business
  action as a harmless edit.

### Filters, Options, and Lookups

- For FilterDTOs, document predicate semantics: exact match, contains, enum set, date range, relative
  period, relationship filter, tenant/organization scope, active/inactive handling, and
  deleted/archived inclusion when relevant.
- Use `@Filterable` only when the backend implements the predicate. Labels must describe the business
  filter and must not expose implementation/operator suffixes.
- Select and lookup fields require static typed choices (`@UISchema(optionItems = {@UiOption(...)})` from `org.praxisplatform.uischema.annotation.UiOption` or `optionEnum = MyEnum.class`, mutually exclusive and without deprecated stringified `options`), an options endpoint, `optionSource`, or `entityLookup` metadata with value field, display field, dependency policy, and inactive/missing-value behavior when applicable. For controller quick filters, `@QuickFilter` criteria (`@FilterCriterion(field, values/bool/number/decimal)`) or `AbstractResourceQueryController#defineQuickFilters()` must reference existing `@Filterable` fields on the bound `FilterDTO`.
- Relationship IDs should normally have a resolved display field or lookup metadata. Do not leave
  users or agents with only opaque foreign keys when the UI needs a human-readable value.

### Analytics, Stats, and Export

- Decide whether each field is exportable, groupable, a chart dimension, a metric/measure, a bucket,
  or excluded from analytics.
- Money, quantities, percentages, rates, durations, and scores may be measures only when the domain
  meaning supports aggregation.
- Identifiers, document numbers, phone numbers, protocol numbers, fiscal keys, external references,
  and sequence codes are not numeric measures by default, even when their Java type is numeric.
- Sensitive fields require explicit governance before becoming exportable, filterable, groupable, or
  available to AI-assisted analytics.

### Audit, Technical, and Legacy Fields

- Audit/provenance fields such as `createdAt`, `updatedAt`, `createdBy`, `updatedBy`, source system,
  version, ETag, import batch, and legacy status are usually read-only and grouped separately.
- Legacy `ROWID`, SQL identifiers, package names, bridge/session internals, provider-specific keys,
  and infrastructure fields must not become public UI fields unless explicitly part of the public
  contract.
- When technical fields are intentionally exposed, document why they are visible, who uses them, and
  whether they should be hidden from forms, exports, filters, analytics, and AI contexts.

### Tenant Custom Fields (`@CustomFields`) and Domain Facts (`@ResourceFact`)

- When a resource persists tenant-defined attributes in a JSONB `custom_fields` column governed by a metadata table (`custom_field_definitions`), declare `private Map<String, Object> customFields = new LinkedHashMap<>();` annotated with `@CustomFields(resourceKey = "<canonical.resource-key>")` and `@Schema(description = "...")` on `ResponseDTO`, `CreateDTO`, `UpdateDTO`, and `FilterDTO`.
- Keep `customFields` as an explicit nested map on the wire (`{"name": "Ana", "customFields": {"numero_calcado": 42}}`); never flatten dynamic tenant fields onto the root DTO with `@JsonAnyGetter` or `@JsonAnySetter`.
- Register a `CustomFieldDefinitionProvider` bean in the host so `/schemas/filtered` and `/schemas/domain` project each active `CustomFieldDescriptor` with full PT-BR `label`, `description`, `controlType`, validation constraints, `filterOperation`, and `x-ui.customField = true` / `x-ui.customFieldKey = "<key>"` / `x-ui.customFieldScope = "tenant"` under `properties.customFields` (`x-ui.customFieldsContainer = true`).
- When a resource exposes calculated domain indicators or business facts for AI/RAG and rule authoring, annotate the controller or `<R>` `ResponseDTO` (or method) with `@ResourceFact` (or `@ResourceFacts`) or register a `ResourceFactCatalogProvider` bean. Omit `resourceKey` when declared under an enclosing `@ApiResource` so it inherits automatically without risking `resource-fact-resource-key-mismatch`, keep `label <= 36` chars without a trailing period, declare lowercase `snake_case` `icon`, valid semantic `tone`, and canonical string wire values validated against `ResourceFactDataType`, `ResourceFactSourceKind`, `ResourceFactAuthority`, `ResourceFactEvaluationPhase`, `ResourceFactMissingValuePolicy`, and `ResourceFactScope` (matching an existing DTO property when `sourceKind` is `"dto_field"` or `"entity_field"`).

## DTO Kind Rules

- Response DTOs must describe the stable read model, display fields, relationships, derived values,
  audit fields, visibility, and table/list presentation.
- Create/update DTOs must describe user intent, validation rules, defaults, required/nullability
  behavior, side effects, editable fields, and governance of submitted values.
- FilterDTOs must document predicate semantics and supported operators. Do not document filters as if
  they were stored entity fields.
- Command/action DTOs must document business action semantics, side effects, authorization relevance,
  confirmation needs, reversibility, idempotency, and AI/agent restrictions.
- Option/lookup DTOs must document identity, display value, disabled/inactive state, ordering,
  grouping, and whether the option set is tenant-, date-, or context-dependent.
- Analytics DTOs must document dimensions, measures, aggregation semantics, grain, time bucket,
  currency/unit, privacy restrictions, and whether values are exact, rounded, masked, or sampled.

### Separating Lifecycle From Ordinary Updates

Audit inherited Bean Validation constraints before removing lifecycle fields from
an update contract. A getter override with `@Null` does not cancel an inherited
field's `@NotNull`; that combination can reject every request. Separate the
existing operation DTO when its write contract differs, preserving the annotations
and governance of legitimate editable fields. Do not change the create operation's
initial-state policy merely to simplify update validation.

Hidden schema metadata is not rejection. If a forbidden input must fail, retain
explicit validation/binding rejection instead of silently discarding it with a
read-only or ignored Jackson property. Define omission versus explicit null:
`@Null` alone accepts null. When the contract forbids the key itself, verify the
host's Jackson null/coercion behavior and use the existing payload-error boundary;
do not change global ObjectMapper policy for one field.

Keep the Java service guard before private reads/mapping and prevent lifecycle
mutation in both update projection and merge mappers. Preserve the legitimate
workflow action's precondition, reason and audit path. Prove omission, same and
opposite state values, explicit null, coercible and incompatible JSON values,
generated mapper behavior, and unchanged create/read contracts. Use the configured
host mapper, validator and canonical advice; a DTO test is not authenticated HTTP
or transactional proof. Update the HTTP corpus and validate that form consumers
submit the operation schema rather than copying the whole read representation.

## Per-Property Completion Checklist

Before considering a DTO property complete, verify:

- Business meaning is documented in `@Schema.description` with product semantics, not UI label
  paraphrase.
- The description explains the field's business role in this resource, not only the generic meaning
  suggested by the property name.
- Java/OpenAPI type, format, nullability, requiredness, default, validation, and examples match
  runtime behavior.
- `@UISchema` label, help text, control, icon, order, group, visibility, editability, alignment,
  mask, value presentation, and table/list formatting match the information role.
- Filter metadata exists only when the backend predicate exists and the label/help text describes the
  business filter.
- Option, enum, or lookup metadata is complete when the field needs controlled values or resolved
  display.
- Governance/LGPD metadata is present for personal, sensitive, financial, employment, security,
  audit, or restricted-purpose data.
- AI policy is explicit for fields that may affect retrieval, reasoning, summarization,
  recommendations, automated actions, or exposure to assistant context.
- Export, analytics, stats, and chart eligibility are deliberate and do not treat identifiers or
  documents as numeric measures.
- Audit, technical, or legacy fields are hidden/read-only/grouped/protected as appropriate.
- Emitted OpenAPI and `x-ui` metadata are validated through the smallest reliable check for the
  changed scope.

## Hard Rules

- Do not create scripts that fill `@Schema` descriptions in bulk from `@UISchema.label`,
  camelCase, endpoint names, or generic heuristics.
- Do not let `@UISchema` substitute for `@Schema`. Label is UI; description is domain meaning.
- Do not publish a select-like field without either static enum/options evidence or a real options
  endpoint/option-source contract.
- Do not use `ENTITY_LOOKUP` against generic `/{resource}/options/filter` when governed entity
  metadata is required; use a named `/{resource}/option-sources/{sourceKey}/options/filter`
  backed by `OptionSourceRegistry`.
- Do not use `@UISchema(preset = ...)` as semantic authorship. Presets only materialize
  presentation/value handling such as enterprise code, monetary amount, legal document, tenant
  label, boolean flag, or audit timestamp. They do not replace `@Schema.description`,
  `@DomainGovernance`, validation, option source, or AI policy.
- Do not expose technical IDs, `ROWID`, provider internals, SQL, package names, or private context in
  `@UISchema.extraProperties`, `x-ui.optionSource`, `OptionDTO.extra`, or public descriptions.
- Do not add labels that expose operator suffixes such as `statusIn`, `statusNotIn`,
  `inicioPrevBetween`, `createdAtOn`, or `lastDays`.
- Do not model identifiers, codes, document numbers, phone numbers, postal codes, or fiscal IDs as
  mathematical numbers just because the legacy database stores them in a numeric column. Preserve
  display semantics with `String`, `FieldDataType.TEXT`, masks, or explicit presentation metadata so
  tables do not render values as locale decimals.
- Do not choose formatting from type alone. A `Long` can be a mathematical quantity or a nonnumeric
  identifier; a `String` can be free text, status code, fiscal document, masked contact value,
  external reference, enum-like code, or resolved display value. Investigate the information role
  and expected corporate display before annotating.
- Do not publish large legacy identifiers, document numbers, fiscal access keys, barcodes, or other
  non-arithmetic numeric-looking values as JSON numbers when browser precision, leading zeroes, or
  locale formatting can change their meaning. Use textual public representation and explicit
  normalization/validation instead.
- Do not register identifiers, operational codes, document numbers, phone numbers, postal codes,
  fiscal IDs, or protocol values as numeric stats measures, histograms, `SUM`, `AVG`, `MIN`, or
  `MAX` just because the Java or database type is numeric. Use categorical buckets only when
  grouping by that value is a real operator task; otherwise omit the field from stats/analytics
  eligibility.
- When changing a public DTO field from legacy numeric storage to textual transport, update the
  host boundary deliberately: mapper or adapter conversion in both directions, normalization policy,
  Bean Validation, error behavior for invalid input, and focused tests. Validate OpenAPI or
  `/schemas/filtered` to prove the field now publishes `string` metadata.
- Do not invent domain effects, permissions, workflows, integrations, or compliance claims that the
  controller/service/validation does not implement.
- Do not let `@Operation`, `@ResourceIntent`, `@UiSurface`, or `@WorkflowAction` fall back to
  generic catalog text when the operation is part of a public/corporate reference surface.

## Declare Bulk-Editable Update Fields

When the resolved Metadata version provides `@BulkEditable`, read its
`docs/spec/BULK-EDITABLE-FIELDS.md` and `BulkEditableFields` implementation first.
Annotate only update DTO fields/accessors/record components (`FIELD`, `METHOD`, `RECORD_COMPONENT`) with verified business eligibility;
commands use typed parameters. Defaults allow both update families and forbid CLEAR.
Do not infer editable fields or identity/version/workflow protection from names.

Compile with the host's configured ObjectMapper, concrete JavaType, resolved canonical
update schema, the actual OpenAPI `SpecVersion`, and trusted protected **wire** names.
The immutable result feeds `BulkFieldChanges`; it does not add x-ui or enable a runtime.
Do not build a permissive parallel schema or remove composition constraints to make
compilation pass. Missing properties, hidden/read-only/protected fields, ambiguous
Jackson bindings and unresolved schema composition must fail explicitly.

CLEAR requires explicit nullability in the declared dialect; `nullable:true` applies
to V30, while V31 requires a null type/union. Absence of required is not nullability.
Cross-check DTO constraints on accessors/constructor members and Jackson null handling;
a setter that skips/converts null is not a valid CLEAR transport. Final candidate and
domain validation/authorization remain mandatory. Run `BulkEditableFieldsTest` plus
`BulkFieldChangeValidationTest` and prove the exact candidate JAR in the consumer.
The annotation SDK alone does not certify registry bootstrap, real evaluation schemas,
providers, workflows, persistence or Angular readiness.

## References

- Read `references/semantic-writing.md` when writing `@Schema`, `@Operation`, DTO descriptions,
  governance text, or AI-facing documentation.
- Read `references/ui-field-contract.md` when choosing controls, labels, groups, icons, helper text,
  visibility, table/read-only formatting, masks, value presentation, validation metadata, and PT-BR
  UX copy.
- Read `references/filters-options-lookups.md` when editing FilterDTOs, options, option sources,
  entity lookups, include/exclude filters, date ranges, and relative periods.
