---
name: praxis-dto-annotations
description: Annotate or review Java DTOs, FilterDTOs, command DTOs, and OpenAPI metadata for hosts that use praxis-metadata-starter. Use when Codex must fill or correct @Schema, @UISchema, @Filterable, @DomainGovernance, AiUsagePolicy, FieldControlType, x-ui labels/help text/icons/groups/order/visibility/valuePresentation/numericFormat/mask, table display formatting, option endpoints, optionSource/entityLookup metadata, or PT-BR domain documentation in Praxis backend projects.
---

# Praxis DTO Annotations

Use this skill to make DTO metadata self-describing for Praxis. Treat DTO annotations as public
contract because they feed OpenAPI, `/schemas/filtered`, `x-ui`, `/schemas/domain`, catalogs, RAG,
AI authoring, and the official Angular runtime.

This skill is versioned from `codex-skills/praxis-dto-annotations`. If the installed copy under
`$CODEX_HOME/skills` diverges, update this canonical source first and then sync it locally.

Before changing this skill or annotating DTOs, inspect the resolved starter/source for the emitted
contract: `@UISchema`, `FieldControlType`, `FieldDataType`, `NumericFormat`, `@Filterable`,
`@DomainGovernance`, `AiUsagePolicy`, option-source descriptors, `CustomOpenApiResolver`,
`/schemas/filtered`, `/schemas/domain`, and representative host DTOs/tests when available. The
goal is to codify what the platform already publishes before adding annotation fields, local
`extraProperties`, host renderers, or AI-facing prose.

## Required Pairing

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

- `@UISchema.label` is short PT-BR UI copy; `helpText` explains how to fill or interpret the value;
  `placeholder` is only an input example and must not replace domain documentation.
- Choose `FieldControlType`, mask, `valuePresentation`, `numericFormat`, date/time format,
  alignment, grouping, visibility, read-only/hidden state, and icon from the information role, not
  only from the Java type.
- Table/list metadata must be complete enough that Angular hosts do not need custom presentation code
  for common values: CPF, CNPJ, CEP, telefone, e-mail, moeda, percentual/taxa, quantidade, data,
  data e hora, status, booleano, codigo/identificador, documento, protocolo, and resolved lookup
  display values.
- Numeric-looking identifiers, document numbers, phone numbers, fiscal keys, and protocol numbers
  must be treated as text/display values with masks when needed. They are not decimal numbers and
  must not receive locale numeric formatting such as `7,00`.
- Use host/project icon conventions. For Angular hosts this normally means Material icon names, not
  arbitrary icon sets invented in DTO metadata.

### Governance, LGPD, and Compliance

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
- Select and lookup fields require enum/static options, options endpoint, `optionSource`, or
  `entityLookup` metadata with value field, display field, dependency policy, and
  inactive/missing-value behavior when applicable.
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

## References

- Read `references/semantic-writing.md` when writing `@Schema`, `@Operation`, DTO descriptions,
  governance text, or AI-facing documentation.
- Read `references/ui-field-contract.md` when choosing controls, labels, groups, icons, helper text,
  visibility, table/read-only formatting, masks, value presentation, validation metadata, and PT-BR
  UX copy.
- Read `references/filters-options-lookups.md` when editing FilterDTOs, options, option sources,
  entity lookups, include/exclude filters, date ranges, and relative periods.
