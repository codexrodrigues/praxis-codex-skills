# UI Field Contract

Use this reference when choosing `@UISchema` metadata for DTO fields that publish `x-ui`.

## Contents

- [Separation Of Concerns](#separation-of-concerns)
- [Labels](#labels)
- [Groups And Order](#groups-and-order)
- [Control Selection](#control-selection)
- [Presentation Presets](#presentation-presets)
- [Layout And Value Presentation](#layout-and-value-presentation)
- [Semantic Formatting Decision](#semantic-formatting-decision)
- [Table Display Formatting](#table-display-formatting)
- [Icons](#icons)
- [Validation And Formatting](#validation-and-formatting)

## Separation Of Concerns

- `@Schema.description`: domain meaning.
- `@UISchema.label`: short visible label.
- `@UISchema.helpText`: short user guidance or effect of a filter/control.
- `@UISchema.description`: visual/presentation explanation when needed.
- Bean Validation: executable constraints.
- `@UISchema` validation fields: UI hints aligned with Bean Validation.

Do not duplicate long domain paragraphs in `helpText`. Keep helper text actionable and short.

## Labels

Use PT-BR labels that an operator understands. Avoid technical suffixes and raw field names.
Keep labels short and consistent across form, table, detail, and filter surfaces:

- include units or fiscal meaning when ambiguity matters, such as `Valor mensal`, `Saldo atual`,
  or `Data de competência`;
- use relationship labels deliberately: `Cargo` for the resolved name shown to the user,
  `Código do cargo` only when the numeric identifier is operationally meaningful;
- use table/detail labels that may be shorter but keep the same product vocabulary as forms;
- avoid internal acronyms unless they are the official business term visible to operators;
- choose singular/plural by surface: a filter that accepts many values can say `Status`, while an
  include/exclude pair should say `Mostrar status` and `Ocultar status`.

Good filter labels:

- `Mostrar status`
- `Ocultar status`
- `Período previsto de início`
- `Início previsto em`
- `Início previsto rápido`
- `Admissões recentes`
- `Faixa salarial`

Bad labels:

- `statusIn`
- `statusNotIn`
- `Inicio Prev Between`
- `Fim previsto na data (Excluir)`
- `Cargo Ids`

## Groups And Order

Use `group` for business sections, not database tables. Common examples:

- `Identificação`
- `Contato`
- `Profissional`
- `Governança`
- `Planejamento`
- `Execução`
- `Compras`, `Suprimentos`, or another host-approved PT-BR business term. Keep an English group
  only when it is the official product/domain name exposed to users.

Use stable order values with gaps, commonly increments of `10`. Keep resolved display fields next
to their ID field when both are exposed; for example `cargoId` order `40`, `cargoNome` order `41`.

For read-only resolved fields:

```java
@UISchema(label = "Cargo", readOnly = true, formHidden = true, group = "Profissional", order = 41, icon = "mi:work")
private String cargoNome;
```

For hidden technical fields, prefer `hidden = true` only when the field must not appear anywhere.
Use `tableHidden` or `formHidden` when the field belongs to one surface but not the other.

## Control Selection

Prefer explicit `controlType` when UX matters. Leave `AUTO` only when the starter heuristic is
enough and the exact control is not part of the public contract.

Common mappings:

| Field need | Suggested control |
| --- | --- |
| short text/name/code | `INPUT` |
| long narrative | `TEXTAREA` |
| email | `EMAIL_INPUT` or `type = FieldDataType.EMAIL` with validated runtime support |
| URL | `URL_INPUT` or `type = FieldDataType.URL` |
| phone | `PHONE` |
| CPF/CNPJ | `CPF_CNPJ_INPUT` plus mask |
| boolean | `CHECKBOX` or deliberate `TOGGLE` |
| enum small | `RADIO` or `SELECT` |
| enum/common select | `SELECT` |
| list of enum values | `MULTI_SELECT` or `INLINE_MULTISELECT` in dense filters |
| date | `DATE_PICKER` |
| date-time | `DATE_TIME_PICKER` |
| date/date-time range filter | `DATE_RANGE` or `DATE_TIME_RANGE` |
| money | `CURRENCY_INPUT` plus `numericFormat = NumericFormat.CURRENCY` |
| numeric range money filter | `PRICE_RANGE` |
| avatar/display image | `AVATAR` |
| governed business entity | `ENTITY_LOOKUP` or `INLINE_ENTITY_LOOKUP` plus option source |
| compact embedded filter/edit | explicit `INLINE_*` variant |
| relative date shortcut | `INLINE_RELATIVE_PERIOD` plus allowed options |

Check `FieldControlType.java` and `x-ui-field.schema.json` before using a less common control. If
renderability is uncertain, also use `praxis-dynamic-fields-editorial`.

## Presentation Presets

Use `@UISchema(preset = UISchemaPreset.*)` only for repetitive presentation/value-handling choices
that the platform already publishes in `x-ui.presentationPreset` and `x-ui.presentation`.

Canonical presets currently include:

- `ENTERPRISE_ID`
- `ENTERPRISE_CODE`
- `ENTERPRISE_NAME`
- `ENTERPRISE_STATUS`
- `DATE_RANGE`
- `MONETARY_AMOUNT`
- `BOOLEAN_FLAG`
- `LEGAL_DOCUMENT_REFERENCE`
- `TENANT_LABEL`
- `AUDIT_TIMESTAMP`

Presets reduce visual boilerplate; they do not author domain meaning. A field with a preset still
needs an explicit `@Schema.description` that explains the business role, and may still need
`@DomainGovernance`, Bean Validation, option-source metadata, or AI policy.

Good:

```java
@Schema(description = "Codigo operacional reconhecido pelo backend legado de folha para classificar eventos e rubricas.")
@UISchema(label = "Codigo", preset = UISchemaPreset.ENTERPRISE_CODE)
private String code;
```

Incomplete:

```java
@UISchema(label = "Codigo", preset = UISchemaPreset.ENTERPRISE_CODE)
private String code;
```

## Layout And Value Presentation

Use layout metadata only when it expresses a reusable platform UX decision:

- `width`: reserve for predictable form/grid proportions; avoid one-off pixel tuning.
- `displayOrientation`: use for compact filter groups, radio/toggle rows, and related controls when
  the runtime supports the value.
- `valuePresentation`: prefer for read-only scalar values where display semantics matter, such as
  currency, percentage, date, datetime, time, or compact numbers.
- `numericFormat`, `numericStep`, `numericMin`, and `numericMax`: align numeric input and display
  with Bean Validation and domain constraints.

Corporate defaults:

- numeric and currency fields should be visually comparable in tables and summaries;
- dates and datetimes should use a consistent locale/timezone policy;
- long free text should not dominate dense operational forms;
- IDs should normally be hidden or secondary unless the user uses them operationally;
- resolved display fields should be read-only and adjacent to the relationship they explain.

Do not invent alignment keys that are absent from the `x-ui` schema. If alignment or table display
requires a new public contract, treat that as a platform contract change, not a local DTO tweak.

## Semantic Formatting Decision

Choose formatting from the information role, not from Java type alone. For each field, inspect the
DTO, entity/view, mapper, service, filter behavior, validation, examples, and corporate UI context,
then decide these contracts together:

- Domain meaning: what the value represents and how operators use it.
- Transport representation: the Java/OpenAPI type that should be published to consumers.
- UI control and display: `@UISchema.type`, `controlType`, mask, `numericFormat`, and
  `valuePresentation` where supported.
- Executable validation: Bean Validation, service normalization, or lookup policy that enforces the
  same semantics.
- Derived eligibility: filters, stats, analytics, export, and AI catalogs that might reuse the
  field outside the table/form surface.

Common semantic roles:

| Information role | Public representation | Typical UI metadata | Notes |
| --- | --- | --- | --- |
| Internal ID hidden from operators | Numeric or string as implemented | `hidden = true` or surface-specific hiding | Expose only when operationally useful. |
| Operational code, sequence, protocol, enrollment, item code | Usually `String` | `type = FieldDataType.TEXT`, `INPUT`, optional mask/pattern | No decimal/currency formatting or numeric stats measures even when stored as number. |
| CPF, CNPJ/CGC, CEP, phone, email, URL | `String` | Specific control plus mask/pattern where supported | Preserve leading zeroes and punctuation policy. |
| Person, organization, place, role, cost center lookup | ID plus resolved display field or entity lookup | `SELECT`, `ENTITY_LOOKUP`, option source metadata | Validate rehydration and labels, not only the ID field. |
| Status, category, phase, type | Enum/string with controlled values | `SELECT`, `RADIO`, chip/badge only when supported | Do not present raw technical codes unless they are user vocabulary. |
| Quantity, count, age, workload, score | Numeric | `FieldDataType.NUMBER`, integer/decimal constraints | Choose integer/decimal from business rule, not database column. |
| Money, balance, salary, price, tax amount | Numeric decimal | `CURRENCY_INPUT`, `NumericFormat.CURRENCY`, min/scale | Document currency and rounding/scale when relevant. |
| Percentage, rate, index, factor | Numeric decimal | `NumericFormat.PERCENT` or number plus clear help text | State whether `0.15` or `15` means 15%. |
| Large legacy numeric identifier | Usually `String` | `FieldDataType.TEXT`, hidden or secondary display | Avoid JavaScript precision loss and locale decimal formatting. |
| High-precision decimal, ratio, calculated financial basis | `BigDecimal`/decimal contract | Numeric format plus explicit scale, min/max, and help text | Do not reduce to floating-point semantics in UI or examples. |
| Date, time, datetime, period | Java temporal type or ISO string by contract | Date/time control, PT-BR display format where supported | Timezone and competence/reference date must be explicit. |
| Boolean flag | Boolean | `CHECKBOX`, `TOGGLE`, or read-only boolean presentation | Label the business state, not only `Ativo?`. |
| Free text, notes, justification | `String` | `TEXTAREA`, max length, helper text | Avoid making long text a prominent table column by default. |
| Sensitive personal/financial/legal data | Contract type based on role | Control plus governance and masking policy | Add `@DomainGovernance` and AI policy when applicable. |

When the same storage type can represent multiple roles, the role wins. For example, `BigDecimal`
can be money, percentage, quantity, score, or identifier imported from a legacy numeric column; each
requires different formatting and validation.

For corporate systems, also check browser-safe precision. Values such as long legacy identifiers,
document numbers, protocol numbers, barcodes, bank agreement numbers, or fiscal access keys should
usually be published as text even when the database type is numeric. Numeric publication is
appropriate only when arithmetic, ordering, aggregation, or numeric range filtering is a real user
operation and precision/scale are explicitly controlled.

## Table Display Formatting

Treat table cells as a first-class consumer of DTO metadata. If a value looks wrong in a generated
table, prefer fixing the DTO/schema semantics over adding a custom table renderer, host-side pipe,
or one-off column config.

For rich table cells, distinguish two levels of readiness:

- Semantic readiness: the DTO publishes the correct public type, label, icon, help text, mask,
  governance, and domain description. This is necessary but not enough for chips, badges, prefixes,
  composed cells, or status pills.
- Renderability readiness: the running `/schemas/filtered` metadata contains a public `x-ui`
  contract that the target `@praxisui/table` version actually maps to a generated column renderer.
  Prove this with source/tests or a browser check before calling the field "richly formatted".

Do not claim that a field will render as a chip, badge, prefixed code, or composed cell only because
it has `icon`, `helpText`, `FieldDataType.TEXT`, `controlType = INPUT`, or a domain description.
Those keys improve schema and detail/form presentation, but they do not by themselves configure a
table renderer.

Use canonical `x-ui.presentation` for read-only/list rich cells. The supported semantic presenters
include `chip`, `badge`, `status`, and `iconValue`; `iconValue` may define `prefix`/`suffix` so
codes can render as `#099` while preserving the raw value for sorting, filtering, export, and
persistence. `valuePresentation` remains reserved for scalar value formatting, not for visual
wrappers such as chips or badges. If the target starter/runtime version does not yet publish or
consume `x-ui.presentation`, record a Praxis table/schema presentation gap instead of adding
host-only column renderers as the migration pattern.

Classify the information before choosing Java type and `@UISchema` formatting:

- Identifier/code: use `String` in the public DTO when the value is not used for arithmetic, even
  when the legacy column is numeric. Examples: empresa code shown as `7`, matrícula, protocolo,
  item code, document number, postal code, phone number, fiscal ID.
- Mathematical number: use numeric Java type plus `FieldDataType.NUMBER`, scale, min/max, and
  `valuePresentation` when the user compares or calculates the value.
- Currency/amount: use numeric Java type plus `controlType = CURRENCY_INPUT`,
  `numericFormat = NumericFormat.CURRENCY`, and explicit currency/decimal metadata when the host
  supports it.
- Percentage/rate: use numeric Java type plus `numericFormat = NumericFormat.PERCENT` and document
  whether the stored value is `0.15` or `15`.
- Date/time: use Java temporal types plus date/time control and display format appropriate to PT-BR
  when the runtime supports it. Do not use date/time `numericFormat` as a table fix unless the
  target starter/runtime proves that path.
- Document/contact fields: use textual DTO type, a specific control such as `CPF_CNPJ_INPUT`,
  `PHONE`, or `EMAIL_INPUT`, and a mask/display hint when needed.

For table scanning, verify the visual result expected by the semantic role: text, codes, names,
documents, and contacts should behave as textual columns; numbers, money, percentages, counts, and
rates should be visually comparable; dates and datetimes should be readable without custom host
pipes. Do not invent DTO keys for alignment. If the generated table cannot align or present a
well-modeled semantic type, record a canonical table/runtime gap instead of creating a local
presentation workaround.

Avoid the common failure where an identifier or fiscal document is published as `number` and the
table formats it as a decimal locale value. A screen showing `Código = 7,00` or
`CGC = 89.522.437.000.107,00` is a contract defect, not a table styling problem. The backend DTO
should publish the field as text or with an explicit supported presentation so `@praxisui/table`,
`@praxisui/dynamic-fields`, and AI authoring receive the same semantics.

Use direct `@UISchema` attributes first:

- `type = FieldDataType.TEXT` for codes and identifiers that must not receive numeric formatting.
- `controlType = FieldControlType.CPF_CNPJ_INPUT`, `PHONE`, `EMAIL_INPUT`, `DATE_PICKER`,
  `DATE_TIME_PICKER`, `CURRENCY_INPUT`, or another semantic control when the role is known.
- `mask` for display/input masks such as `00.000.000/0000-00`, `000.000.000-00`,
  `(00) 00000-0000`, or `00000-000` when supported by the target runtime.
- `numericFormat` for real numeric values: integer, decimal, number, fraction, scientific,
  currency, or percent according to the resolved starter enum. Temporal enum values in the schema
  are not proof that `numericFormat` is the correct table-display path for dates or times.

When the desired scalar display is supported by `x-ui.valuePresentation` but not by a direct
`@UISchema` attribute, use `extraProperties` only for public schema keys that exist in
`x-ui-field.schema.json`, normally `valuePresentation.type`, `valuePresentation.style`, and
`valuePresentation.format`. Nested `valuePresentation.currency` or `valuePresentation.number`
objects are open schema objects; use nested keys only when the target runtime/docs prove the exact
contract or after a platform contract change. Never hide table-only formatting in private
`custom.*` keys when the problem is a domain presentation semantics issue.

In the canonical Angular runtime, textual `x-ui.mask` values using `0`, `#`, `9`, `X`, or `x`
tokens are mapped to table column `format` and rendered as textual formatting by `@praxisui/table`.
This is intended for documents, contact values, postal codes, operational identifiers, and legacy
numeric-looking identifiers. Date/time, boolean, currency, and percentage semantics still take
precedence over text masks; do not use an input mask as a table date format. Use a date/time control
and supported display/value-presentation metadata for temporal values. When the target host may be
using an older runtime package, validate the emitted `/schemas/filtered` metadata and the generated
table column before assuming the mask is active.

Treat `mask` as a display/input-format contract, not as the complete validation rule. In the
Angular runtime, masks composed only of `0`, `#`, or `9` consume digits; masks containing `X` or `x`
consume alphanumeric characters for protocol-like values. The mask renderer does not replace Bean
Validation, service normalization, option-source policy, or document checksum rules. If a field has
mixed numeric and alphanumeric positions, add explicit backend validation or normalization that
matches the public DTO contract.

For legacy numeric storage with textual semantics, map explicitly at the host boundary:

```java
@UISchema(
    label = "CNPJ/CGC",
    type = FieldDataType.TEXT,
    controlType = FieldControlType.CPF_CNPJ_INPUT,
    mask = "00.000.000/0000-00",
    tableHidden = false
)
@Schema(description = "Identificador fiscal da empresa, publicado sem semântica matemática.")
@Pattern(regexp = "\\d{14}", message = "Informe 14 dígitos para CNPJ/CGC.")
private String cgc;
```

Use the `@Pattern` above only when the API contract receives normalized digits, for example because
the control or mapper submits an unmasked value. If the public DTO accepts a formatted value, align
Bean Validation with that contract, for example `\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}`, or
normalize the value before validation in the host boundary. Do not rely on the visible mask alone to
define what the backend accepts.

If the entity column remains numeric, convert it in the mapper/adapter and filter by normalized
digits in the service. Do not force the UI table to undo numeric formatting after the schema was
published incorrectly.

When a public DTO field changes from a legacy numeric entity column to textual transport, verify
the complete boundary instead of changing only annotations:

- mapper/entity adapter converts entity numeric value to the public text shape, preserving required
  width such as 11 or 14 digits when the business document requires it;
- mapper/entity adapter accepts the documented input shape, normally normalized digits and/or the
  visible masked form, and rejects incomplete values before persistence;
- Bean Validation matches the public transport contract, not only the visual mask;
- FilterDTOs either keep the field absent or implement explicit normalization before touching the
  numeric legacy column;
- OpenAPI or `/schemas/filtered` proves the public field type is `string` and `x-ui` carries the
  intended `type`, `controlType`, and `mask`;
- mapper tests and one focused schema smoke cover the conversion so future DTO enrichments do not
  regress the contract back to JSON number.

Also review stats and analytics registries for the same field. Identifiers, operational codes,
documents, protocols, phone numbers, postal codes, and fiscal IDs must not be registered as
`numericMeasureField`, `numericHistogramMeasureField`, `SUM`, `AVG`, `MIN`, or `MAX`. Keeping them
out of analytics is better than publishing mathematically meaningless corporate metrics. Use a
categorical bucket only when grouping by that identifier is a real operator workflow.

Minimum proof for table-related DTO changes:

- `/schemas/filtered` publishes the expected OpenAPI type; identifiers/documents should not arrive
  as JSON `number` unless they are mathematically numeric.
- `schema.properties.<field>.x-ui.type`, `controlType`, `mask`, `numericFormat`, and
  `valuePresentation` match the semantic role.
- For rich cells such as chips, badges, prefixed identifiers, or composed labels, the emitted
  metadata is known to be consumed by the current table runtime, not merely present in OpenAPI.
- The Angular-derived table column is `string`/textual for codes and documents, not a numeric column
  inferred from stale metadata.
- No `numericFormat` is attached to textual identifiers, documents, phones, postal codes, or
  external references.
- Stats/analytics registries do not expose textual identifiers or documents as numeric measures,
  histograms, sums, averages, minima, or maxima.
- A browser/screenshot check is run when visual table formatting is the user-visible issue; if it is
  not run, state why.

## Icons

Use the icon vocabulary adopted by the target Angular host. In the official Praxis Angular runtime,
`PraxisIconDirective` and `ICON-PREFIXES.md` define prefixed Material icon values:

- `mi:` Material Icons baseline/fill, such as `mi:work`, `mi:badge`, `mi:event`;
- `mso:` Material Symbols Outlined, such as `mso:home`;
- `msr:` Material Symbols Rounded, such as `msr:check`;
- `mss:` Material Symbols Sharp, such as `mss:warning`.

For new persisted metadata, prefer prefixed values when the target host follows this Praxis pattern.
Unprefixed values are legacy/compatibility input and should not be introduced in new corporate DTO
metadata unless the target host explicitly uses an older convention.

When the target Angular host is available, inspect its `mat-icon`, icon font, `praxisIcon`,
`PraxisIconDirective`, `MatIconRegistry`, or style configuration before adding new icon names. Reuse
names already used by that host when they fit the domain. When no Angular host is present, use the
starter contract plus official Praxis Angular documentation/source if available; otherwise document
the assumption and avoid host-specific icon styling keys.

Common prefixed examples: `mi:badge`, `mi:fingerprint`, `mi:event`, `mi:work`, `mi:apartment`,
`mi:email`, `mi:phone`, `mi:payments`, `mi:toggle_on`, `mi:toggle_off`, `mi:warning`,
`mi:location_on`, `mi:priority_high`, `mi:business`, `mi:tag`, `mi:notes`, `mi:link`, and
`mi:account_circle`.

Choose icons by domain meaning. Do not use emojis, decorative icons, or CSS class names as a
substitute for the canonical `icon` value. Use `iconPosition`, `iconSize`, `iconColor`,
`iconClass`, `iconStyle`, or `iconFontSize` only when the target runtime/design system has evidence
for them. Do not invent `iconColor`/`iconClass` conventions to compensate for a missing icon.

For public examples and corporate-facing surfaces, validate icons against the Angular host's
existing runtime usage or icon registry. If visual correctness is in scope, run a narrow
browser/screenshot check; an unknown icon name should be treated as a UX defect, not as harmless
decoration.

When visual correctness is in scope, screenshots should also cover label length, group ordering,
helper text density, hidden/read-only fields, filter grouping, value presentation, and narrow
viewport wrapping. If screenshot validation is not run, state the reason explicitly.

## Validation And Formatting

Keep UI hints aligned with Bean Validation:

- `@NotBlank`/`@NotNull` -> `required = true` when the UI should enforce it.
- `@Size(max = n)` -> `maxLength = n`.
- `@Pattern` -> compatible `mask` or `patternMessage` when the UI can help.
- dates in PT-BR forms may use `mask = "dd/MM/yyyy"` and explicit locale/display format through
  `extraProperties` when the runtime supports those keys.
- currency fields should define numeric format and min/scale when the domain requires it.

Use `extraProperties` sparingly for public `custom.*` or runtime-supported keys. Never put private
provider, SQL, adapter, endpoint secret, package name, or cache details there.
