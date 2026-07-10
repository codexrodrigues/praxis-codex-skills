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

- component doc metadata lookup by id/component type.
- editorial descriptor registration and resolution.
- normalized input/output defaults for common bindings.
- component type aliases only as compatibility lookup, not as intent routing.
- port contracts, insertion presets, and registry projections consumed by builders.
- i18n resolution for registry labels and descriptions.

Vertical packages own their component-specific metadata entries. Page Builder and Visual Builder author and display registry data but should not redefine the registry contract.

## Registry Rules

- Register metadata with stable component ids, selectors, component refs, inputs, outputs, ports, insertion presets, owner package, and tags.
- Use `registerEditorial` for editorial descriptors with `componentMetaId`, `controlType`, localized text, family/track/tags, and binding descriptors.
- Keep aliases limited to resolving already-scoped component type compatibility. Do not route user intent by aliases or labels.
- Preserve port and insertion preset semantics when copying or projecting metadata; do not strip inputs, outputs, cardinality, semantic kinds, or diagnostics.
- Use `component-context.schema` or component AI capabilities when an agent needs registry grounding, instead of scraping rendered controls.
- If metadata looks missing in a builder, first check whether the owning package registered it before adding fallback local registry data.

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

## Companion Skills

- Use `praxis-core-widget-observations` for dynamic widgets, runtime observations, and widget event evidence.
- Use `praxis-core-composition-runtime` for dynamic page, ports, links, and surface host execution.
- Use `praxis-page-builder-composition` or `praxis-page-builder-ai-agentic` when the registry is consumed by Page Builder.
- Use `praxis-core-domain-governance-runtime` when metadata is grounded in governed domain decisions.
- Use `praxis-angular-public-api-governance` for exported registry/model changes.
