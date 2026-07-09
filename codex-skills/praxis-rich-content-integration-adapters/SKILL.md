---
name: praxis-rich-content-integration-adapters
description: Use when Codex must integrate, audit, or document `RichContentDocument` across Praxis consumers, including Page Builder widgets, dynamic widget loaders, editorial forms, stepper `stepBlocksBeforeForm` or `stepBlocksAfterForm`, wizard adapters, dynamic-form/editorial inputs, metadata-driven previews, component registry metadata, docs, examples, or migration from legacy editorial blocks to canonical rich content.
---

# Praxis Rich Content Integration Adapters

Use this skill when rich content crosses package boundaries. The goal is to materialize one canonical `RichContentDocument`, not to create per-consumer editorial dialects.

## Source Audit

Inspect the owning consumer as well as rich-content:

- `projects/praxis-rich-content/**`
- `projects/praxis-core/src/lib/models/rich-content/**`
- `projects/praxis-page-builder/**` for widget metadata and dynamic page materialization
- `projects/praxis-editorial-forms/**` for editorial runtime/data collection adapters
- `projects/praxis-stepper/src/lib/praxis-stepper.ts`, config editor, wizard adapter, and rich-content specs
- `projects/praxis-dynamic-form/**` and `projects/praxis-dynamic-fields/**` when the task involves rich inputs or metadata-driven fields
- docs manifests, examples, AI recipes, and landing pages that publish rich-content examples

There is no local `projects/praxis-rich-content/AGENTS.md` in the audited checkout. Record that gap when changing this family.

## Integration Rules

- Use `RichContentDocument` as the interchange format between packages.
- Prefer `stepBlocksBeforeForm` and `stepBlocksAfterForm` in `@praxisui/stepper` instead of legacy wizard editorial blocks for new authoring.
- Use `PraxisRichContent` inside consumers rather than reimplementing node rendering.
- Register `providePraxisRichContentMetadata()` when dynamic widget catalogs need discovery.
- Preserve host-mediated action semantics. Consumers should dispatch actions through their own governed action/composition systems, not through rich-content local command strings.
- Keep migration adapters explicit when converting legacy editorial blocks to rich content. Do not silently duplicate both shapes in saved config.
- If a consumer needs a node type not currently supported, classify the gap before adding a contract. Prefer extending the core rich-content model and renderer over a consumer-local pseudo-node.

## Validation

Use focused consumer proof:

- rich-content runtime/editor/validator specs
- Page Builder widget and dynamic page materialization specs
- stepper rich-content specs and wizard adapter specs
- editorial-forms adapter/runtime specs
- dynamic-form or dynamic-fields specs when rich input metadata changes
- docs/examples/playground validation when published examples change

Report which consumer owns the integration and which rich-content derived artifacts were reviewed.

## Companion Skills

- Use `praxis-rich-content-runtime` for document and renderer semantics.
- Use `praxis-rich-content-authoring-settings` for editor and preset behavior.
- Use `praxis-page-builder-composition`, `praxis-editorial-forms-runtime`, `praxis-editorial-forms-adapters-ai`, `praxis-stepper-wizard-runtime`, `praxis-form-runtime-submit`, and `praxis-dynamic-fields-editorial` according to the consumer surface.
