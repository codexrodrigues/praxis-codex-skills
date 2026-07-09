---
name: praxis-rich-content-ai-security-validation
description: Use when Codex must change, audit, or validate AI-assisted authoring or safety rules for `@praxisui/rich-content`, including `PRAXIS_RICH_CONTENT_AUTHORING_MANIFEST`, AI capabilities, recipes, context packs, `validateRichContentDocument`, safe URL and style policy, JsonLogic visibility/loading/disabled/style behavior, action safety, registry ingestion, docs, examples, or assistant validation for structured `RichContentDocument` authoring.
---

# Praxis Rich Content AI Security Validation

Use this skill for rich-content AI authoring, sanitization, and registry validation. Pair it with runtime, authoring, or integration skills for the concrete surface.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-rich-content/src/lib/ai/praxis-rich-content-authoring-manifest.ts`
- `projects/praxis-rich-content/src/lib/ai/rich-content-ai-capabilities.ts`
- `projects/praxis-rich-content/src/lib/ai/*.spec.ts`
- `projects/praxis-rich-content/src/lib/rich-content-document-validator.ts`
- `projects/praxis-rich-content/src/lib/praxis-rich-content.ts`
- `projects/praxis-rich-content/src/lib/praxis-rich-content-config-editor.ts`
- `tools/ai-registry/**` when registry projection changes

There is no local `projects/praxis-rich-content/AGENTS.md` in the audited checkout. Record that governance gap until the subarea has local instructions.

## Safety Rules

- AI authoring must produce structured `RichContentDocument` JSON, not HTML, markdown patches, or free-form DOM.
- Validate documents before persistence with `validateRichContentDocument`.
- Keep `kind='praxis.rich-content'` and `version='1.0.0'`.
- Respect validator limits such as supported node types, maximum nesting depth, and maximum node count.
- Preserve safe URL and style policies. Unsafe `javascript:`, `vbscript:`, dangerous `data:`, CSS expression/import/binding patterns, malformed style names, and unsafe class names must not be persisted.
- JsonLogic conditions fail safe: invalid visibility/loading/style rules fail closed, and invalid disabled rules disable interactive surfaces.
- Rich content actions are host-mediated. Do not invent local command strings or let AI bypass the host action/composition contract.

## Manifest Rules

`PRAXIS_RICH_CONTENT_AUTHORING_MANIFEST` governs document replacement, block add/remove/reorder, text updates, link nodes, media blocks, timeline nodes/items, presets, metadata, and sanitization policy.

Before considering an AI change complete, verify:

- the operation has a declared target, validator, affected path, and submission impact
- destructive or broad document replacement is confirmed where required
- node ids remain stable enough for follow-up edits
- editor preview, advanced JSON, validation badges, and runtime rendering agree
- registry/docs/examples are updated or explicitly ruled out

## Validation

Use the smallest reliable proof:

- `praxis-rich-content-authoring-manifest.spec.ts`
- `rich-content-ai-capabilities.spec.ts`
- `rich-content-ai-recipes.spec.ts`
- `rich-content-document-validator.spec.ts`
- config editor specs when AI apply affects authoring round-trip
- `npm run validate:authoring-contracts` or registry ingestion validation when in scope
- docs/playground validation when public examples or recipes change

Report exact validation and skipped gates.

## Companion Skills

- Use `praxis-rich-content-runtime` for renderer and document semantics.
- Use `praxis-rich-content-authoring-settings` for editor round-trip and presets.
- Use `praxis-rich-content-integration-adapters` when AI-generated rich content is embedded in Page Builder, stepper, editorial forms, or dynamic forms.
- Use `praxis-ai-authoring-manifests` and `praxis-ai-registry-ingestion` for shared manifest and registry governance.
