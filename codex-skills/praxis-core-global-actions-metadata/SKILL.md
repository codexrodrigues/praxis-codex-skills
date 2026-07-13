---
name: praxis-core-global-actions-metadata
description: Use when Codex must implement, audit, document, or consume shared `@praxisui/core` global actions and metadata services, including `GlobalActionRef`, global action tokens/providers/catalogs, `GlobalActionService`, global action UI schemas, payload validation, surface open presets/editors, component metadata registry, resource discovery service, domain catalog/knowledge/rule services, schema metadata services, public API, or cross-lib action/metadata integration.
---

# Praxis Core Global Actions Metadata

Use this skill for shared global action and metadata service contracts in `@praxisui/core`. Treat actions and metadata as governed semantic contracts, not local command strings or per-component aliases.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/docs/schema-flow.md`
- `projects/praxis-core/docs/connection-editor.md`
- `projects/praxis-core/src/public-api.ts`
- `projects/praxis-core/src/lib/models/global-action.model.ts`
- `projects/praxis-core/src/lib/tokens/global-action.*`
- `projects/praxis-core/src/lib/services/global-action.service.ts`
- `projects/praxis-core/src/lib/actions/global-action-ref.utils.ts`
- `projects/praxis-core/src/lib/actions/global-action-ui.ts`
- `projects/praxis-core/src/lib/actions/surface-open-presets.ts`
- `projects/praxis-core/src/lib/services/component-metadata-registry.service.ts`
- `projects/praxis-core/src/lib/services/resource-discovery.service.ts`
- `projects/praxis-core/src/lib/schema/schema-metadata-client.ts`
- `projects/praxis-core/src/lib/services/schema-normalizer.service.ts`
- `projects/praxis-core/src/lib/services/domain-catalog.service.ts`
- `projects/praxis-core/src/lib/services/domain-knowledge.service.ts`
- `projects/praxis-core/src/lib/services/domain-rule.service.ts`
- `projects/praxis-core/src/lib/ai/domain-catalog-context-pack.ts`
- focused global action, surface open, metadata registry, schema/resource, and consumer specs

## Canonical Boundary

`@praxisui/core` owns `GlobalActionRef`, global action catalog tokens/providers, `GlobalActionService`, payload validation, UI schema helpers, surface open presets, component metadata registry, resource discovery service, domain catalog/knowledge/rule services, schema normalization, and shared metadata service contracts.

Consumers may declare package-specific actions and metadata entries, but should not persist command strings, invent local global-action payload shapes, or duplicate schema/resource discovery logic.

## Action And Metadata Rules

- Persist global actions as `globalAction: { actionId, payload?, payloadExpr?, meta? }`.
- Keep local component `action` fields for local component/host events only.
- Do not reintroduce command strings such as `showAlert:...`, `openUrl:...`, `navigate:...`, `apiCall:...`, or `surface.open:{...}`.
- Validate required payload keys and payload type with `validateGlobalActionRef(s)`.
- Use `getGlobalActionUiSchema(...)` when authoring structured payload fields.
- Use surface open presets and editors for canonical surface open actions.
- Use component metadata registry for component docs/discovery; do not create package-local registries for shared metadata semantics.
- Use resource/domain services for resource discovery, domain catalog, knowledge, and rules. Do not copy metadata service logic into table/form/list/page-builder consumers.

## Inventory Before New Contract

Classify requests before adding action or metadata contracts:

- `ja-suportado-so-ux`: action/catalog/schema metadata exists but the editor or runtime does not expose it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: command strings, local action wrappers, or aliases should normalize to `GlobalActionRef` or core metadata services.
- `suportado-parcialmente`: core can represent the action/metadata but payload UI, validation, docs, consumer bridge, or AI registry projection is incomplete.
- `lacuna-real-de-contrato`: no global action, UI schema, payload validator, resource/domain service, metadata registry, or schema flow can carry the semantic decision.

For real gaps, update core contract, public API, specs, docs, and at least one direct consumer proof.

## Validation

Use the smallest reliable proof:

- global action refs, execution, UI schema, and `surface.open` editor/presets:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/actions/global-action-ref.utils.spec.ts --include=projects/praxis-core/src/lib/services/global-action.service.spec.ts --include=projects/praxis-core/src/lib/actions/editors/surface-open-action-editor.component.spec.ts --include=projects/praxis-core/src/lib/actions/surface-open-presets.spec.ts
```

- component metadata registry and dynamic widget consumption:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/component-metadata-registry.service.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-runtime-observation.spec.ts
```

- resource discovery, schema metadata, and schema normalization:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/resource-discovery.service.spec.ts --include=projects/praxis-core/src/lib/schema/schema-metadata-client.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer.service.spec.ts --include=projects/praxis-core/src/lib/services/schema-normalizer-array.service.spec.ts
```

- domain catalog, knowledge, rules, and safe timeline projections:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/domain-catalog.service.spec.ts --include=projects/praxis-core/src/lib/services/domain-knowledge.service.spec.ts --include=projects/praxis-core/src/lib/services/domain-rule.service.spec.ts --include=projects/praxis-core/src/lib/models/domain-knowledge-timeline.rich-content.spec.ts --include=projects/praxis-core/src/lib/models/domain-rule-timeline.rich-content.spec.ts
```

- direct consumer specs where actions or metadata are materialized:

```sh
npm run test:form -- --include=projects/praxis-dynamic-form/src/lib/action-authoring/global-action-authoring.util.spec.ts --include=projects/praxis-dynamic-form/src/lib/services/domain-rule-form-rules.service.spec.ts
npm run test:table -- --include=projects/praxis-table/src/lib/table-global-action-adapter.spec.ts --include=projects/praxis-table/src/lib/praxis-table-config-editor.global-actions.spec.ts
npm run ng -- test praxis-page-builder --watch=false --progress=false --include=projects/praxis-page-builder/src/lib/editor/component-palette-dialog.component.spec.ts --include=projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor.component.spec.ts --include=projects/praxis-page-builder/src/lib/ai/page-builder-ai.adapter.spec.ts
```

- package authoring manifests only when metadata/action catalog changes must be projected to AI authoring:

```sh
npm run test:table -- --include=projects/praxis-table/src/lib/ai/praxis-table-authoring-manifest.spec.ts
npm run test:form -- --include=projects/praxis-dynamic-form/src/lib/ai/praxis-dynamic-form-authoring-manifest.spec.ts
npm run ng -- test praxis-page-builder --watch=false --progress=false --include=projects/praxis-page-builder/src/lib/ai/praxis-page-builder-authoring-manifest.spec.ts
```

For public export changes, run `npm run build:praxis-core` plus a direct consumer build selected by actual imports. Report which consumers were checked and whether command-string migration, alias cleanup, metadata registry projection, or AI manifest projection remains.

## Companion Skills

- Use `praxis-core-global-action-payloads` for focused `GlobalActionRef`, payload schema/UI schema, payloadExpr, validation, onResult, and command-string migration work.
- Use `praxis-core-surface-materialization` for resource-derived `surface.open` payloads, action/surface adapters, related resources, and materializer behavior.
- Use `praxis-core-component-registry-contracts` for `ComponentMetadataRegistry`, component docs metadata, editorial descriptors, ports, insertion presets, and builder/AI registry projection.
- Use `praxis-core-domain-governance-runtime` for domain catalog, domain knowledge, domain rules, governed decisions, simulations, publications, and materializations.
- Use `praxis-core-resource-runtime` for broader schema/resource discovery, actions, surfaces, capabilities, option sources, related resources, and analytics materialization.
- Use `praxis-dialog-global-actions-ai` when dialog global actions or presets are the vertical surface.
- Use `praxis-dialog-surface-global-actions` when surface open payloads are materialized through dialog/drawer providers.
- Use `praxis-authoring-editors` when global actions are edited through Settings Panel/config editors.
- Use `praxis-angular-public-api-governance` and `praxis-angular-validation-gates` for exports and validation.
