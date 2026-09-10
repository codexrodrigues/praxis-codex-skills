---
name: praxis-rich-content-authoring-settings
description: Use when Codex must implement, audit, document, or author `@praxisui/rich-content` visual authoring, including `PraxisRichContentConfigEditor`, Settings Panel round-trip, guided block editing, preview, advanced JSON, preset insertion, rich content i18n, validation badges, widget config editor metadata, apply/save/reset/reopen behavior, docs, examples, or public authoring API for `RichContentDocument`.
---

# Praxis Rich Content Authoring Settings

Use this skill for the canonical rich-content editor and Settings Panel surface. The editor must preserve the same document envelope consumed by the renderer.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-rich-content/README.md`
- `projects/praxis-rich-content/src/lib/praxis-rich-content-config-editor.ts`
- `projects/praxis-rich-content/src/lib/praxis-rich-content-config-editor.spec.ts`
- `projects/praxis-rich-content/src/lib/rich-content-authoring.ts`
- `projects/praxis-rich-content/src/lib/rich-content-authoring.spec.ts`
- `projects/praxis-rich-content/src/lib/rich-content-document-validator.ts`
- `projects/praxis-rich-content/src/lib/i18n/**`
- `projects/praxis-rich-content/src/lib/praxis-rich-content.metadata.ts`

Read `projects/praxis-rich-content/AGENTS.md` before editing rich-content authoring. Use `praxis-angular-agents-governance` if the local AGENTS file is missing, stale, or contradicts this skill.

## Canonical Editor Contract

The editor opens and saves the widget input envelope:

```ts
{
  inputs: {
    document: { kind: 'praxis.rich-content', version: '1.0.0', nodes: [] },
    layout: 'block',
    rootClassName: 'employee-summary'
  }
}
```

Do not create editor-only document shapes or host wrappers that the renderer cannot consume.

## Authoring Rules

- Preserve guided editing, preview, and advanced JSON as synchronized views of one canonical document.
- Use `EDITABLE_TOP_LEVEL_NODE_TYPES`, presenter node types, and default node factories from `rich-content-authoring.ts`.
- Validate before apply/save with `validateRichContentDocument`.
- Keep document-level context, aliases, bindings, `visibleWhen`, `disabledWhen`, `loadWhen`, `classWhen`, and `styleWhen` available through structured controls or focused JSON.
- Keep labels and validation messages in `providePraxisRichContentI18n()` catalogs.
- Use presets for repeatable structures instead of copying bulky local JSON into consumers.
- Keep Settings Panel apply/save/reset/reopen behavior aligned with runtime rendering.
- When another editor embeds Rich Content, delegate through the canonical document/input contract and keep guided editing, preview, advanced JSON, validation, and unapplied-draft state connected to the host apply/save lifecycle. Do not fork a reduced host-local card or callout editor.
- Preserve semantic callout/card tone, icon, title, message, context-path bindings, action references, and safe advanced properties. Validate `rootClassName` and the full document even when content enters through advanced JSON.
- Treat action nodes as references only. The owning host must resolve them against its governed action catalog and enforce capability, record authorization, confirmation, and dispatch; a rendered button never grants authority.
- Prefer semantic tones and platform tokens. Arbitrary styles or gradients remain advanced input and require the canonical safety validator plus rendered contrast evidence across supported themes.

## Validation

Use the smallest reliable proof:

- `praxis-rich-content-config-editor.spec.ts`
- `rich-content-authoring.spec.ts`
- `rich-content-document-validator.spec.ts`
- Settings Panel round-trip validation when hosted editor behavior changes
- i18n audit when authoring text changes
- docs/playground validation when public authoring examples change

## Companion Skills

- Use `praxis-rich-content-runtime` for renderer and document semantics.
- Use `praxis-rich-content-ai-security-validation` when authoring touches manifest operations, sanitization, safe URLs/styles, or AI-generated documents.
- Use `praxis-authoring-editors` and `praxis-settings-roundtrip-authoring` for shared Settings Panel protocol and round-trip behavior.
