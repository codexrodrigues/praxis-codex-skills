---
name: praxis-core-component-registry-contracts
description: Use when Codex must implement, audit, or consume @praxisui/core ComponentMetadataRegistry contracts: component docs metadata, editorial descriptors, component type aliases, input/output defaults, ports, insertion presets, i18n resolution, widget catalog discovery, Page Builder/Visual Builder registry projection, or AI component context grounding.
---

# Praxis Core Component Registry Contracts

Use this skill when work depends on `ComponentMetadataRegistry` or component metadata that builders, dynamic widgets, AI authoring, or surface hosts consume.

The registry is a shared Angular catalog for materialized components. It is not a local builder-only registry and should not duplicate semantic contracts owned by resource metadata, domain governance, or a vertical component package.

## Source Audit

Inspect before editing:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/docs/connection-editor.md`
- `projects/praxis-core/docs/rfc-dynamic-page-canvas-runtime.md`
- `projects/praxis-core/src/lib/services/component-metadata-registry.service.ts`
- `projects/praxis-core/src/lib/models/component-doc-metadata.interface.ts`
- `projects/praxis-core/src/lib/models/component-editorial-metadata.model.ts`
- `projects/praxis-core/src/lib/models/port-contract.model.ts`
- `projects/praxis-core/src/lib/ai/component-context.schema.ts`
- component metadata files in the owning vertical package.
- focused specs for registry, metadata model, AI context, and the direct builder/runtime consumer.

## Canonical Boundary

Core owns the registry mechanics and shared metadata contracts:

- component doc metadata lookup by normalized id and fixed compatibility aliases.
- editorial descriptor registration and resolution.
- normalized input/output defaults for common bindings.
- component type aliases only as compatibility lookup, not as intent routing.
- port contracts, insertion presets, and registry projections consumed by builders.
- i18n resolution for editorial descriptors; legacy doc metadata remains string-based.

Vertical packages own their component-specific metadata entries. Page Builder and Visual Builder author and display registry data but should not redefine the registry contract.

## Registration And Lookup Semantics

- Register vertical metadata through the owning package provider such as `providePraxisRichContentMetadata()`. Importing a component class does not populate `ComponentMetadataRegistry`; the host must install the provider so its `ENVIRONMENT_INITIALIZER` runs.
- Treat the registry as an in-memory, injector-scoped governed catalog. Duplicate normalized metadata ids, duplicate legacy `componentType` indexes for different metadata ids, duplicate editorial `componentMetaId`, and duplicate editorial `controlType` registrations fail closed instead of relying on provider order.
- `get(id)` resolves a normalized metadata id plus the fixed exact aliases `table`, `chart`, `form`, `crud`, `tabs`, `stepper`, `list`, and `expansion`. It does not perform arbitrary selector, component class, fuzzy, case-insensitive, or general `componentType` lookup.
- `resolveEditorial()` uses a different precedence: editorial descriptor by id/control type first, then raw legacy `ComponentDocMeta` by normalized id or legacy `componentType`. Do not assume its result is the same normalized object returned by `get()`.
- Use aliases only after the component scope is already known. The alias map is compatibility lookup, not extensible vocabulary or semantic intent routing.

`register()` clones ports and insertion-preset inputs at ingress, and registry reads (`get()`, `getAll()`, `getEditorial()` and `getAllEditorial()`) return defensive snapshots. Consumers must still treat results as read-only projections and clone preset/config payloads before materializing or editing them. Never mutate registry metadata to store builder state.

## Metadata And I18n Boundaries

Keep the two metadata paths distinct:

- `ComponentDocMeta` is the runtime/catalog contract for component refs, inputs, outputs, actions, commands, ports, config editor, authoring manifest ref, insertion presets, layout hints, tags, and owner lib. Its labels/descriptions are plain strings.
- `ComponentMetadataEditorialDescriptor` is the localized editorial projection. Its `PraxisTextValue` fields are resolved by `PraxisI18nService` through `resolveEditorial()`.
- Common input/output defaults injected by `normalizeMeta()` are resolved from the core `componentMetadataRegistry` i18n namespace, with built-in `pt-BR` and `en-US` catalog entries and clean textual fallback. Keep explicit component labels/descriptions authoritative over these defaults, and do not add component-specific business copy to the shared registry catalog.

When a localized builder/editor experience is required, register and resolve the editorial descriptor with its namespace. Do not copy localized labels into host palettes or reinterpret a raw `ComponentDocMeta` string as an i18n key.

## Projection Fidelity

Every consumer is a projection with its own fidelity; verify the target instead of assuming the whole registry travels intact:

- `DynamicWidgetLoaderDirective` looks up normalized metadata and validates only declared inputs/outputs. Missing metadata emits `metadata-missing`; strict mode throws for unknown bindings, while non-strict mode warns and drops them. Ports do not replace Angular input/output declarations at this boundary.
- `NestedPortCatalogService` consumes `ports` plus nested component metadata. A valid Angular output without a canonical port is not sufficient grounding for semantic composition.
- Page Builder palette reads runtime metadata to project entries, presets, and readiness badges, and clones preset inputs before insertion. Its palette entry is still a consumer projection, not a mutable registry record.
- `PageBuilderAiAdapter` currently projects only id, display copy, icon, tags, input/output names, and layout hints. It omits ports, insertion presets, actions, commands, config editor, and authoring manifest ref.
- `component-context.schema` defines component-specific options/actions/field resolvers and merge patches. It is not an automatic `ComponentDocMeta` registry projection, and a component context pack may maintain its own explicit option enum.
- Generated `tools/ai-registry/component-docs.json` preserves its own schema subset, including insertion presets, but does not prove runtime ports/actions/commands are grounded. Pair registry ingestion work with `praxis-ai-registry-ingestion` and inspect the generated schema/artifact.

Classify a missing fact in a projection as `suportado-parcialmente` until the canonical metadata exists and the target consumer demonstrably preserves it. Do not compensate with a second palette array, prompt-only component catalog, selector switch, or host metadata overlay.

## Registry Rules

- Register metadata with stable component ids, selectors, component refs, inputs, outputs, ports, insertion presets, owner package, and tags.
- Use `registerEditorial` for editorial descriptors with `componentMetaId`, `controlType`, localized text, family/track/tags, and binding descriptors.
- Keep aliases limited to resolving already-scoped component type compatibility. Do not route user intent by aliases or labels.
- Preserve port and insertion preset semantics when copying or projecting metadata; do not strip inputs, outputs, cardinality, semantic kinds, or diagnostics.
- Use the target consumer's explicit registry projection, component AI capabilities, and authoring manifest when an agent needs grounding; inspect their schemas instead of scraping rendered controls or assuming `component-context.schema` contains `ComponentDocMeta`.
- If metadata looks missing in a builder, first check whether the owning package registered it before adding fallback local registry data.
- Treat duplicate normalized ids, legacy component types or editorial control types as a governance error. Runtime registration now rejects these collisions, and generated catalog governance should continue rejecting duplicate component ids/selectors before runtime bootstrap.

## Aderence Inventory

Classify requests before adding registry contracts:

- `ja-suportado-so-ux`: registry entry exists but builder/editor/docs do not expose it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: local alias, selector switch, or hardcoded palette entry should normalize to registry metadata.
- `suportado-parcialmente`: metadata exists but inputs, outputs, ports, insertion presets, i18n, AI projection, or consumer proof is incomplete.
- `lacuna-real-de-contrato`: no registry field/model/AI context can carry the component fact.

Only real gaps justify changing core registry models or public API. Component-specific facts usually belong in the owning vertical package metadata.

## Validation

Use focused proof:

- `component-metadata-registry.service.spec.ts`
- component metadata model specs.
- component AI context/schema specs.
- Page Builder, Visual Builder, dynamic widget page, or surface host consumer spec when registry projection is user-visible.
- owning component package build/spec when metadata comes from that package.

For first-step issue resolution, audit a concrete registry entry: raw registration, normalized id, alias/controlType lookup, i18n text, inputs/outputs, ports, insertion presets, AI projection, and builder/runtime consumer visibility.

Prove three scenarios:

1. Happy path: an owning provider registers metadata; `get()` preserves normalized inputs/outputs, cloned ports and presets; palette/loader consume the intended subset.
2. Risk path: missing provider and unknown bindings emit their expected loader diagnostics; duplicate id/control type registrations fail closed; lossy AI projection is identified by source/catalog audit instead of being accepted as complete runtime behavior.
3. Adversarial path: reject keyword/label routing, selector switches, mutable host overlays, prompt-only catalogs, and assumptions that every projection contains ports/presets/actions.

Use focused gates from the `praxis-ui-angular` root:

```bash
npx ng test praxis-core --watch=false --progress=false \
  --include=projects/praxis-core/src/lib/services/component-metadata-registry.service.spec.ts \
  --include=projects/praxis-core/src/lib/widgets/dynamic-widget-loader.directive.spec.ts \
  --include=projects/praxis-core/src/lib/composition/nested-port-catalog.service.spec.ts
npx ng test praxis-page-builder --watch=false --progress=false \
  --include=projects/praxis-page-builder/src/lib/editor/component-palette-dialog.component.spec.ts \
  --include=projects/praxis-page-builder/src/lib/ai/page-builder-ai.adapter.spec.ts
npx ng test praxis-rich-content --watch=false --progress=false \
  --include=projects/praxis-rich-content/src/lib/praxis-rich-content.metadata.spec.ts
npx ng build praxis-core --configuration production
npx ng build praxis-page-builder --configuration production
```

These gates prove representative runtime, builder, and owner-package paths. Record registry ingestion generation, Visual Builder, a real host bootstrap, browser palette UX, and metadata from other vertical packages as unverified unless they were also exercised.

## Companion Skills

- Use `praxis-core-widget-observations` for dynamic widgets, runtime observations, and widget event evidence.
- Use `praxis-core-composition-runtime` for dynamic page, ports, links, and surface host execution.
- Use `praxis-page-builder-composition` or `praxis-page-builder-ai-agentic` when the registry is consumed by Page Builder.
- Use `praxis-core-domain-governance-runtime` when metadata is grounded in governed domain decisions.
- Use `praxis-angular-public-api-governance` for exported registry/model changes.
- Use `praxis-ai-registry-ingestion` when changing extraction, generated component docs, ingestion schemas, or backend registry artifacts.
