---
name: praxis-visual-builder-schemas-templates
description: Use when Codex must implement, audit, or consume @praxisui/visual-builder field schemas, target schemas, property schemas, FieldSchemaService, FIELD_TYPE_OPERATORS, operator labels, FieldSchemaContext, ContextManagementService, context scopes, variables, custom functions, collection validators, RuleTemplateService, template gallery/editor/preview, template import/export, or template-compatible rule nodes.
---

# Praxis Visual Builder Schemas Templates

Use this skill for governed authoring inputs around the visual builder: fields, operators, targets, context variables, property schemas, collection validators, and reusable templates. These are grounding surfaces for rule authoring, not a place to route primary user intent by keywords.

Pair it with:

- `praxis-visual-builder-graph-runtime` when schemas or templates create or mutate nodes.
- `praxis-visual-builder-jsonlogic-roundtrip` when a schema/operator/template must serialize as supported JSON Logic.
- `praxis-visual-builder-ai-validation` when AI operations add variables, set effects, or validate target/schema constraints.
- `praxis-fields-option-sources`, `praxis-fields-runtime-loader`, or `praxis-dynamic-fields-editorial` when field metadata originates in dynamic field surfaces.
- `praxis-form-ai-rules-validation` when schemas and rules materialize into dynamic-form behavior.
- `praxis-page-builder-composition` when schemas, targets, or templates are used to connect widgets through composition links or page state.

## Source Audit

Before editing schema/template behavior, inspect:

- `projects/praxis-visual-builder/AGENTS.md`
- `projects/praxis-visual-builder/README.md`
- `projects/praxis-visual-builder/src/lib/models/field-schema.model.ts`
- `projects/praxis-visual-builder/src/lib/models/array-field-schema.model.ts`
- `projects/praxis-visual-builder/src/lib/models/rule-builder.model.ts`
- `projects/praxis-visual-builder/src/lib/services/field-schema.service.ts`
- `projects/praxis-visual-builder/src/lib/services/context/context-management.service.ts`
- `projects/praxis-visual-builder/src/lib/services/rule-template.service.ts`
- `projects/praxis-visual-builder/src/lib/docs/collection-validators.md`
- `projects/praxis-visual-builder/src/lib/docs/TEMPLATE-SYSTEM-GUIDE.md`
- component specs for field condition, property effect, collection validator, template gallery, template editor, and template preview

## Canonical Boundary

`@praxisui/visual-builder` owns:

- `FieldSchema`, `FieldType`, `FIELD_TYPE_OPERATORS`, `OPERATOR_LABELS`, `FieldSchemaContext`, `ContextVariable`, and `CustomFunction`;
- `FieldSchemaService` schema storage, operator lookup, schema grouping, JSON Schema conversion, and form metadata conversion;
- `RuleBuilderConfig.fieldSchemas`, `targetSchemas`, `targetPropertySchemas`, `contextVariables`, `customFunctions`, and `templates`;
- `ContextManagementService` scopes, scoped variables, providers, provider merging, path validation, and strict context checks;
- `RuleTemplate`, `RuleTemplateService`, template categories, search, import/export, validation, application, metadata, and statistics;
- collection validator configs and docs for array/collection-oriented validation.

When a host supplies schemas from widgets, form fields, table columns, or page state, preserve the origin and canonical id. Labels can help users choose targets, but the persisted rule must use schema identities that the host can resolve after reopen.

Consumers should not create local operator catalogs, field search rules, target-property allowlists, or template persistence formats when these surfaces already exist.

## Inventory Before New Contract

Classify every requested schema/template change:

- `ja-suportado-so-ux`: a schema, operator, context variable, template category, or validation result exists but needs clearer editor presentation.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host uses local field aliases, CSS selectors, or string labels where `FieldSchema.name`, target IDs, context scope/name, or template IDs already provide identity.
- `suportado-parcialmente`: the schema exists, but JSON Logic round-trip, property-effect validation, template application, or docs are incomplete.
- `lacuna-real-de-contrato`: no field schema, operator mapping, target property schema, context scope, template metadata, or collection validator can represent the authoring decision.

Only real gaps justify new exported types or config fields. Prefer improving the canonical schema service, context service, docs, and tests before adding host-local conventions.

## Semantic Authoring Rules

- Use `FieldSchema.name` as field identity; labels and search text are ranking/display aids after semantic scope is known.
- Use `FieldSchema.origin` to distinguish form fields, sections, actions, rows, columns, visual blocks, table fields, and table columns when context-sensitive filtering matters.
- Use `FIELD_TYPE_OPERATORS` and `OPERATOR_LABELS` as UI support, but confirm that selected operators also round-trip through `RuleBuilderService`.
- Treat context variables as governed scope/name entries. Do not smuggle them through string interpolation into persisted conditions unless the JSON Logic shape is canonical and tested.
- Use `targetPropertySchemas` and `RULE_PROPERTY_SCHEMA` for property effects. Do not infer allowed effects from editor labels or CSS classes.
- Keep templates as reusable `RuleNode[]` plus `rootNodes` with required fields and metadata; template application must validate missing fields and incompatible features.
- Page/widget templates may reference page state or component ports only when those references are represented as governed field/context/target schemas.
- Template search may use text matching only after the user’s semantic scope is known. It must not decide primary intent.

## Validation

Use focused local gates:

- `field-schema.service` specs for field conversion, operator lookup, suggestions, and grouping;
- context management specs for scope inheritance, path validation, providers, and strict validation;
- collection validator component/docs specs when array validation changes;
- template service and template component specs for CRUD, import/export, validation, and application;
- JSON Logic round-trip validation when an operator, context, function, or template produces rule conditions;
- `npm run build:praxis-visual-builder` when exported schema/template contracts change.

State exactly which schema, context, template, collection, round-trip, and build checks were run.
