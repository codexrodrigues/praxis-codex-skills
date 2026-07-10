---
name: praxis-rich-content-runtime
description: Use when Codex must implement, audit, document, or consume `@praxisui/rich-content` runtime surfaces, including `RichContentDocument`, semantic nodes, block or inline layout, context bindings, JsonLogic visibility/loading/disabled/style rules, host-mediated actions, presets, `PraxisRichContent`, component metadata, public API, docs, examples, or dynamic page materialization for Praxis rich content.
---

# Praxis Rich Content Runtime

Use this skill for the canonical rich content renderer. Treat rich content as structured Praxis document semantics, not as arbitrary HTML, markdown, or a generic visual widget.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-rich-content/README.md`
- `projects/praxis-rich-content/src/public-api.ts`
- `projects/praxis-rich-content/src/lib/praxis-rich-content.ts`
- `projects/praxis-rich-content/src/lib/praxis-rich-content.metadata.ts`
- `projects/praxis-rich-content/src/lib/rich-content-document-validator.ts`
- `projects/praxis-rich-content/src/lib/rich-content-preset-registry.service.ts`
- `projects/praxis-rich-content/docs/praxis-docs.manifest.json`
- `projects/praxis-core/src/lib/models/rich-content/**`
- focused runtime, metadata, validator, and preset specs

There is no local `projects/praxis-rich-content/AGENTS.md` in the audited checkout. Record that governance gap when working in the subarea until a local AGENTS file exists.
Use `praxis-angular-agents-governance` to re-audit the gap and decide whether the correction belongs in `praxis-ui-angular` local guidance or only in skill routing.

## Canonical Boundary

`@praxisui/core` owns the shared `RichContentDocument` and node model. `@praxisui/rich-content` owns rendering, validation helpers, metadata provider, editor, presets, i18n, and AI authoring surfaces.

Do not introduce local rich-content dialects in consumers. New semantic content should use:

```ts
{
  kind: 'praxis.rich-content',
  version: '1.0.0',
  nodes: []
}
```

## Runtime Rules

- Use `PraxisRichContent` for rendering documents and nodes.
- Use `layout='inline'` only for compact compositions; keep document-style content in block layout.
- Prefer semantic nodes such as text, badge, icon, card, callout, key/value list, stats, timeline, media block, record summary, lookup surfaces, action card, decision package, disclosure, accordion, form launcher, and preset references.
- Use `context` and expression fields for materialized values. Do not pre-render HTML strings when the document can bind to governed context.
- Host-mediated actions must stay actions. The renderer does not execute business behavior by itself.
- Register `providePraxisRichContentMetadata()` when dynamic widget loaders or Page Builder need to discover the component.
- Use `RichContentPresetRegistryService`, `PRAXIS_RICH_BLOCK_PRESETS`, and `providePraxisDefaultRichBlockPresets()` for governed presets.

## Validation

Use the smallest reliable proof:

- `praxis-rich-content.spec.ts`
- `praxis-rich-content.metadata.spec.ts`
- `rich-content-document-validator.spec.ts`
- preset registry specs when preset behavior changes
- docs/playground validation when public rich-content examples change
- focal consumer validation when stepper, page-builder, editorial-forms, or dynamic pages materialize the document

Report exactly what was validated and what remained unvalidated.

## Companion Skills

- Use `praxis-rich-content-authoring-settings` for the config editor, guided editing, preview, JSON tab, and presets.
- Use `praxis-rich-content-integration-adapters` when rich content is embedded in stepper, Page Builder, editorial forms, dynamic forms, or composed widgets.
- Use `praxis-rich-content-ai-security-validation` for validator, sanitization, safe URLs/styles, JsonLogic fail-safe behavior, AI manifest, and registry validation.
- Use `praxis-core-runtime-contracts` when the shared core rich-content model or public exports change.
