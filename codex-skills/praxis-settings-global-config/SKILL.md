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
- `praxis-config-starter` owns `/api/praxis/config/ui` persistence in `ui_user_config`, including tenant/user/environment scope, ETag preconditions, payload limits, write authorization, and secret sanitization.

Use `praxis-config-runtime-persistence` when save, clear, reload, tenant/user/environment scope, ETag, or remote config storage semantics depend on `praxis-config-starter`. Use `praxis-config-ai-registry-manifests` or `praxis-config-agentic-authoring-streaming` when global settings affect AI provider/model, registry, or authoring backend contracts.

## Required Inventory

Inspect:

- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/global-config-editor/global-config-editor.component.ts`
- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/global-config-editor/global-config-admin.service.ts`
- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/global-config-editor/global-config-editor.schema.ts`
- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/global-config-editor/global-config-editor.models.ts`
- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/global-config-editor/global-config-editor.tokens.ts`
- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/global-config-editor/open-global-config-editor.ts`
- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/global-config-editor/*.spec.ts`
- `praxis-ui-angular/projects/praxis-settings-panel/src/lib/i18n/global-config-editor.i18n.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/global-config.service.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/config-storage.service.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/tokens/global-config.providers.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/tokens/global-config.token.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/models/global-config.model.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/global-config.service.spec.ts`
- `praxis-ui-angular/docs/global-config.md`

When remote persistence is touched, also inspect:

- `praxis-config-starter/src/main/java/org/praxisplatform/config/controller/UserConfigController.java`
- `praxis-config-starter/src/main/java/org/praxisplatform/config/service/UserConfigService.java`
- `praxis-config-starter/src/main/java/org/praxisplatform/config/service/UiConfigWriteAuthorizer.java`
- `praxis-config-starter/src/main/java/org/praxisplatform/config/domain/UiUserConfig.java`

## Current Contract

- `GlobalConfigService.ready()` loads the active storage key before consumers rely on effective config.
- The storage key is `praxis:global-config` or `praxis:global-config:{tenant}` when a tenant is set or resolved.
- `setTenant()` changes the active key and invalidates the loaded config/cache state.
- Effective config is built from configured provider values plus the stored config overlay. Runtime getters such as `getCrud()`, `getDynamicFields()`, `getTable()`, `getDialog()`, and `get(path)` read that merged effective snapshot.
- `saveGlobalConfig(partial)` deep-merges the partial over the current effective config, persists the merged config through `ASYNC_CONFIG_STORAGE`, updates the in-memory snapshot, and emits config changes.
- `clearGlobalConfig()` clears the active storage key, reloads effective config from provider/server defaults, resets the stored snapshot, and emits config changes.
- `hasStoredConfig()` is meaningful only after the service is ready because it reflects the loaded storage snapshot.
- `GlobalConfigAdminService` must use public `GlobalConfigService` getters and save/clear APIs; do not reach into cache internals or duplicate merge logic.
- `GlobalConfigEditorComponent.getSettingsValue()` returns only changed fields by comparing `currentValues` with `initialValues`.
- Changed form fields are nested by `dataAttributes.globalPath`; generated safe names are an implementation detail and must not become persisted contract.
- `onSave()` validates compact table appearance values before save, toggles busy state, delegates to `GlobalConfigAdminService.save(partial)`, updates the baseline after success, and returns `undefined` on blocked/failed saves.
- `clearStoredConfig()` delegates to `GlobalConfigAdminService.clearStoredConfig()`, reloads effective config, resets forms from the fresh snapshot, and refreshes the stored/source indicator.

## Rules

- Preserve tenant/global storage semantics; do not store global config in a host-local singleton when the configured storage contract exists.
- Save partial config intentionally. Do not overwrite unrelated global config branches when editing CRUD, dynamic-fields, table, cache, dialog, or AI settings.
- `clearStoredConfig()` must return to server/provider defaults and refresh effective config.
- Every editable dynamic form field must declare `dataAttributes.globalPath`. Add a new editable path only when a runtime consumer reads that path from `GlobalConfigService` or the same change adds that canonical runtime consumption.
- Keep `buildGlobalConfigFormConfig` field names as safe names derived from global paths; do not persist or document safe names as public config paths.
- Compact table appearance fields must normalize whitespace and reject invalid CSS length values before persistence.
- AI provider/model settings must use the AI provider catalog and backend test/model APIs where available; do not persist only opaque display strings.
- AI model requests should include `apiKey` only when the user typed a new key. Stored keys are server-side state and must not be exposed back into the editor as raw values.
- Preserve `apiKeyLast4`, `hasStoredApiKey`, and safe status labels as UI state only. They are not the persisted secret.
- Backend error details for AI keys, model fetching, and save failures must not leak raw upstream or encryption messages into visible editor copy.
- Keep dynamic form fields and validation aligned with runtime config consumers.
- Put authoring chrome text in Settings Panel i18n catalogs; avoid hardcoded visible strings.
- Open the editor through `openGlobalConfigEditor(settingsPanelService, options)` / `SettingsPanelService.open`; do not create a separate drawer or dialog host for global config.
- `GLOBAL_CONFIG_DYNAMIC_FORM_COMPONENT` intentionally keeps `settings-panel` from depending directly on `dynamic-form`. Preserve this injection-token bridge when evolving form rendering.

## Remote Persistence Rules

- `ApiConfigStorage` maps `praxis:global-config*` keys to component type `praxis-global-config-editor` and component id equal to the storage key.
- `/api/praxis/config/ui` requires `X-Tenant-ID`. `X-User-ID`, `X-Env`, `X-Updated-By`, and `scope=user|tenant` govern the resolved record.
- Reads use `If-None-Match` and may return `304 Not Modified`; `ApiConfigStorage` must reuse the cached payload in that case.
- Saves and clears use cached `ETag` as `If-Match` when available. A `412 Precondition Failed` is a real concurrency signal; do not mask it as a successful save.
- `UserConfigService` owns user-vs-tenant resolution, payload size limits, ETag generation, precondition checks, and AI key sanitization before writing `ui_user_config`.
- `UserConfigController` sanitizes secret fields again for response. UI code must treat returned key material as status metadata, not as the raw credential.
- If bootstrap uses `providePraxisGlobalConfigBootstrap`, preserve the auth gate, tenant resolver, headers factory, `errorPolicy`, and blocking mode semantics.

## Validation

Prefer focused checks:

- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/global-config-editor/global-config-editor.component.spec.ts`
- `npx ng test praxis-settings-panel --watch=false --progress=false --include=projects/praxis-settings-panel/src/lib/global-config-editor/global-config-admin.dialog.spec.ts`
- `npx ng test praxis-core --watch=false --progress=false --include=projects/praxis-core/src/lib/services/global-config.service.spec.ts`

For persistence changes, validate save, clear, reload/reopen, and runtime consumption. A successful form submit is not enough if the next open reads a different effective value.

For `/api/praxis/config/ui` changes, add a focused `praxis-config-starter` validation that proves tenant/user scope, ETag/If-Match, delete, and sanitized AI key response behavior. Use `praxis-config-runtime-persistence` for the backend-specific test selection.
