---
name: praxis-settings-global-config
description: Use when changing or reviewing @praxisui/settings-panel or praxis-settings-panel package Global Config Editor, GlobalConfigAdminService, openGlobalConfigEditor, global config schema, AI provider/model settings, cache/persistence settings, dynamic-fields/table/CRUD global policies, stored config clear/save behavior, or `/api/praxis/config/**`-backed global config persistence.
---

# Praxis Settings Global Config

The `praxis-settings-*` skill family is the canonical Codex skill surface for `@praxisui/settings-panel` and `projects/praxis-settings-panel`; do not create parallel `praxis-settings-panel-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the global configuration editor inside `@praxisui/settings-panel`. Global config is a governed platform configuration surface, not a screen-local settings form.

## Canonical Boundary

- `GlobalConfigService` in `@praxisui/core` owns effective runtime config, storage readiness, and save/clear APIs.
- `GlobalConfigAdminService` reads effective config and persists partial updates.
- `GlobalConfigEditorComponent` owns the visual editor, dynamic form sections, AI provider/model controls, validation, dirty/busy state, and save/clear UX.
- `buildGlobalConfigFormConfig` owns the dynamic form schema for editable global config fields.
- Remote persistence belongs to the configured global config storage, commonly `/api/praxis/config/**` from `praxis-config-starter`.

Use `praxis-config-runtime-persistence` when save, clear, reload, tenant/user/environment scope, ETag, or remote config storage semantics depend on `praxis-config-starter`. Use `praxis-config-ai-registry-manifests` or `praxis-config-agentic-authoring-streaming` when global settings affect AI provider/model, registry, or authoring backend contracts.

## Required Inventory

Inspect:

- `src/lib/global-config-editor/global-config-editor.component.ts`
- `src/lib/global-config-editor/global-config-admin.service.ts`
- `src/lib/global-config-editor/global-config-editor.schema.ts`
- `src/lib/global-config-editor/global-config-editor.models.ts`
- `src/lib/global-config-editor/global-config-editor.tokens.ts`
- `src/lib/global-config-editor/open-global-config-editor.ts`
- `src/lib/global-config-editor/*.spec.ts`
- `@praxisui/core` `GlobalConfigService` and config storage contracts when persistence behavior changes

## Rules

- Preserve tenant/global storage semantics; do not store global config in a host-local singleton when the configured storage contract exists.
- Save partial config intentionally. Do not overwrite unrelated global config branches when editing CRUD, dynamic-fields, table, cache, dialog, or AI settings.
- `clearStoredConfig()` must return to server/provider defaults and refresh effective config.
- AI provider/model settings must use the AI provider catalog and backend test/model APIs where available; do not persist only opaque display strings.
- Keep dynamic form fields and validation aligned with runtime config consumers.
- Put authoring chrome text in Settings Panel i18n catalogs; avoid hardcoded visible strings.

## Validation

Prefer focused checks:

- `global-config-editor.component.spec.ts`
- `global-config-admin.dialog.spec.ts`
- schema tests or focused dynamic form validation where present
- GlobalConfigService/storage tests when save/clear/effective config semantics change

For persistence changes, validate save, clear, reload/reopen, and runtime consumption. A successful form submit is not enough if the next open reads a different effective value.
