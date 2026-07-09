---
name: praxis-settings-ai-i18n-validation
description: Use when auditing or changing Praxis Settings Panel AI authoring manifest, settings-panel AI adapter/capabilities/context pack, AI-assisted settings edits, authoring scope, internal i18n catalogs, diagnostics text, button/status labels, or validation that Settings Panel behavior is available to AI-assisted authoring without local keyword routing.
---

# Praxis Settings AI I18n Validation

Use this skill when Settings Panel behavior is exposed to AI authoring or internal authoring chrome changes. AI should reason over the canonical panel protocol and hosted editor contracts, not over local command strings or keyword routes.

## Canonical Sources

Inspect:

- `src/lib/ai/praxis-settings-panel-authoring-manifest.ts`
- `src/lib/ai/settings-panel-ai.adapter.ts`
- `src/lib/ai/settings-panel-ai-capabilities.ts`
- `src/lib/ai/settings-panel-context-pack.ts`
- `src/lib/ai/*.spec.ts`
- `src/lib/i18n/settings-panel.i18n.ts`
- `src/lib/i18n/settings-panel.en.ts`
- `src/lib/i18n/settings-panel.pt-BR.ts`
- `src/lib/i18n/global-config-editor.i18n.ts`
- `src/lib/i18n/text-normalize.ts`

## AI Rules

- Treat the Settings Panel manifest as the shell protocol: open, attach editor, apply, save, reset, cancel, resize, diagnostics. Hosted editor fields belong to the owning component manifest.
- Do not route authoring intent with keywords, regex command parsing, or localized labels. Ground AI decisions in manifests, component metadata, settings value providers, config editor contracts, and declared tools.
- Keep `consult/answer` separate from governed edit plans when the adapter supports both.
- If a hosted editor owns a manifest, verify the Settings Panel context pack does not duplicate or contradict that component's authoring contract.
- Validate intermediate assistant states when streaming/diagnostics are part of the UX, not only terminal saved output.

## I18n Rules

- Internal authoring chrome is platform text: Apply, Save, Reset, Cancel, status, disabled reason, diagnostics, global config sections, snackbars, and confirmation dialogs must use the Settings Panel i18n path.
- Keep `en` and `pt-BR` aligned when adding visible strings.
- Use text normalization helpers only for display hygiene, not as semantic routing.

## Validation

Prefer focused checks:

- `praxis-settings-panel-authoring-manifest.spec.ts`
- `settings-panel-ai.adapter.spec.ts`
- i18n-focused specs when catalogs or normalization change
- shell specs when AI operations affect apply/save/reset/close behavior

For public behavior changes, review `src/public-api.ts`, README, and host integration docs. If no AI manifest update is required, state why.
