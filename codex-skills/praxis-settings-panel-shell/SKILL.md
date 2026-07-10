---
name: praxis-settings-panel-shell
description: Use when changing or reviewing `@praxisui/settings-panel` or the praxis-settings-panel package shell behavior, SettingsPanelService, SettingsPanelRef, SettingsValueProvider, BaseSidePanelService, drawer sizing, close/backdrop/Escape mediation, Apply/Save/Reset/Cancel enablement, diagnostics, tokens, or host bridge integration.
---

# Praxis Settings Panel Shell

The `praxis-settings-*` skill family is the canonical Codex skill surface for `@praxisui/settings-panel` and `projects/praxis-settings-panel`; do not create parallel `praxis-settings-panel-*` guidance unless this family cannot express a proven contract gap.

Use this skill for the canonical authoring drawer shell. Do not duplicate drawer chrome, footer protocol, dirty/valid/busy rules, resize, shortcuts, or close mediation in consumer editors when the issue belongs to `@praxisui/settings-panel`.

## Canonical Boundary

- `SettingsPanelService` opens authoring drawers.
- `SettingsPanelRef` emits `applied$`, `saved$`, `reset$`, `closed$`, and `sizeChanged$`.
- `SettingsValueProvider` is the editor contract: `getSettingsValue`, optional `onSave`, optional `reset`, and required `isDirty$`, `isValid$`, `isBusy$`.
- `BaseSidePanelService` owns shared overlay, scope replacement, backdrop, Escape, width presets, resize, and persisted width.
- `providePraxisSettingsPanelBridge()` is authoring; `providePraxisSurfaceDrawerBridge()` is runtime `surface.open`. Do not mix these semantics.

## Required Inventory

Inspect:

- `projects/praxis-settings-panel/AGENTS.md`
- `src/public-api.ts`
- `src/lib/settings-panel.service.ts`
- `src/lib/settings-panel.component.ts`
- `src/lib/settings-panel.ref.ts`
- `src/lib/settings-panel.types.ts`
- `src/lib/base-side-panel.service.ts`
- `src/lib/base-side-panel.types.ts`
- `src/lib/settings-panel-bridge.provider.ts`
- `src/lib/surface-drawer-bridge.provider.ts`
- `docs/host-settings-panel-integration.md`

## Shell Rules

- Keep Apply and Save enabled only when dirty, valid, and not busy.
- `Apply` previews without closing through `applied$`; `Save` emits through `saved$` and closes.
- `Reset` delegates to the hosted editor and emits `reset$`; it must not clear unrelated host state.
- `Cancel`, backdrop, Escape, and replacement of an open panel must pass through the canonical close mediation, including `onBeforeClose` and dirty discard confirmation where applicable.
- Persist width through `persistSizeKey`; expanded/collapsed state must not accidentally overwrite persisted manual width.
- Use `SettingsPanelConfig.diagnostics` only to show/hide status, disabled reason, busy state, or validation state. It must not change the gating rules.
- Use canonical tokens/classes for visual changes: `--pfx-settings-panel-*`, `.praxis-settings-panel-backdrop`, and `.praxis-settings-panel-pane`.

## Validation

Prefer focused checks:

- `settings-panel.service.spec.ts`
- `settings-panel.component.spec.ts`
- `base-side-panel.service.spec.ts`
- bridge specs when host/runtime drawer wiring changes
- screenshot or Playwright evidence when visual drawer behavior is material

Review README, public API, and host integration docs when shell behavior, public tokens, or bridge semantics change.
