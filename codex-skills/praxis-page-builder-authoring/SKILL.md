---
name: praxis-page-builder-authoring
description: Use when Codex must create, inspect, or fix @praxisui/page-builder authoring editors: PageConfigEditorComponent, DynamicPageConfigEditorComponent, WidgetShellEditorComponent, SettingsValueProvider, Settings Panel bridge, page settings, canvas/grouping/device/state/context editors, widget shell actions, ComponentDocMeta.configEditor hosting, visual/textual round-trip, save/apply/reset/reopen, i18n, page editor runtime parity, or authoring changes that may require Page Builder agentic validation gates.
---

# Praxis Page Builder Authoring

Use this skill for the visual/textual authoring editors that produce or update `WidgetPageDefinition`. The goal is not "any editor can mutate JSON"; the goal is a stable round-trip between canonical page semantics, visual editors, Settings Panel, persistence, and runtime rendering.

Pair it with:

- `praxis-settings-panel-shell` and `praxis-settings-roundtrip-authoring` for Settings Panel protocol, footer state, apply/save/reset/cancel, and bridge behavior.
- `praxis-authoring-editors` for cross-component editor ownership rules.
- `praxis-page-builder-composition` for `WidgetPageDefinition`, canvas, composition links, connection graph, and runtime materialization.
- `praxis-page-builder-ai-agentic` when authoring changes affect AI manifests, UI composition plans, or agentic preview/apply.

## Canonical Chain

Keep this chain coherent:

`WidgetPageDefinition -> Page/DynamicPage config editor state -> SettingsValueProvider output -> pageChange/apply/save -> ui_user_config identity/ETag when persisted -> reopen -> praxis-dynamic-page runtime`

For widget shell:

`widget.shell -> WidgetShellEditorComponent -> ShellEditorResult -> page.widgets[].shell / pagePreset -> runtime shell`

For child widget config:

`ComponentDocMeta.configEditor or child ComponentAuthoringManifest -> child-owned document/input patch -> page.widgets[].definition.inputs`

Page Builder hosts child editors; it does not redefine child component config documents.
When a child editor needs schemas, capabilities, resource catalogs, page targets, ports, or diagnostics only for authoring, provide them through `ComponentDocMeta.configEditor.contextResolver` as transient `context/contextDiagnostics`. Do not persist those values in `page.widgets[].definition.inputs`; only the editor's explicit settings result may update child inputs.
If the child editor is Visual Builder, Dynamic Form, Table, Chart, List, Rich Content, or another Praxis component, load that component's authoring skill and preserve its document/apply semantics inside `page.widgets[].definition.inputs`.
When a hosted child editor returns a `SettingsValueProvider` payload, Page Builder must apply the
child-owned canonical input patch/document projection as `definition.inputs`, not wrap it in a
Page-Builder-local envelope or merge back transient context. Missing blocks in a replace-all child
document must remain cleared unless the child owner declares merge semantics.

## Required Source Inventory

Before editing Page Builder authoring, inspect:

- `projects/praxis-page-builder/AGENTS.md`
- `projects/praxis-page-builder/src/lib/page-config-editor/page-config-editor.component.ts`
- `projects/praxis-page-builder/src/lib/page-config-editor/page-config-editor.component.spec.ts`
- `projects/praxis-page-builder/src/lib/dynamic-page-config-editor.component.ts`
- `projects/praxis-page-builder/src/lib/dynamic-page-config-editor.component.spec.ts`
- `projects/praxis-page-builder/src/lib/editor/widget-shell-editor.component.ts`
- `projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor.component.ts` when links or page state are editor-visible
- `projects/praxis-page-builder/src/lib/editor/component-palette-dialog.component.ts` when insertion presets or child editor launch points change
- `projects/praxis-page-builder/src/lib/i18n/page-builder.*.ts` when labels, helper text, errors, or empty states change
- `projects/praxis-page-builder/src/lib/ai/praxis-page-builder-authoring-manifest.ts` when authorable paths change

Also inspect `projects/praxis-core` composition and widget shell models when changing page or shell shape.

## Editor Rules

Page config editors may edit page layout/theme presets, canvas, grouping, device layouts, context, and state. They must preserve unknown canonical fields unless the change explicitly removes deprecated compatibility semantics.

Treat JSON text areas as advanced escape hatches that still produce validated canonical objects. Do not persist invalid JSON strings, legacy grid options, or page-builder-only shapes that `praxis-dynamic-page` cannot render.

Widget shell editor owns shell chrome only: title, subtitle, icon, preset, appearance, window actions, and shell actions. It must not mutate child component inputs. Available widget actions and commands should come from `ComponentMetadataRegistry` and `ComponentDocMeta`, not local command vocabularies.

When `applyToAll` or page preset behavior changes, confirm whether the canonical owner is page preset, shell preset, or widget shell. Do not silently copy shell style into every widget when a page-level preset can express the decision.

## Round-Trip Checklist

Before calling a Page Builder editor ready, verify:

- opening an existing page preserves `WidgetPageDefinition` without converting it to legacy `GridPageDefinition`.
- layout/theme/shell presets survive apply/save/reopen.
- canvas items reference existing widget keys.
- grouping and device layout JSON parse and preserve shape.
- page context/state remain structured objects.
- widget shell changes affect only `page.widgets[].shell`.
- child widget settings open through the child `ComponentDocMeta.configEditor` or manifest path.
- transient child editor context from `configEditor.contextResolver` is separated from persisted inputs and is not saved back to `page.widgets[].definition.inputs`.
- Page Builder does not persist `context`, `contextDiagnostics`, runtime drawer `surfaceRuntime`,
  `result$` envelopes, row-selection payloads, resolved catalogs, or diagnostics output as child
  widget inputs unless the child owner explicitly declares those paths as stable inputs.
- Visual Builder or rule editors hosted as child config preserve JSON Logic/graph round-trip and do not leak Page Builder-only rule state.
- reset returns to the initial page/shell and updates dirty/valid/busy state.
- runtime preview consumes the same document shape that persistence saves.
- i18n covers user-visible editor text.

## Validation

Run focused validation:

- page config editor: page config editor spec and dynamic page config editor spec.
- widget shell: widget shell editor coverage plus metadata/registry integration where action catalogs are involved.
- Settings bridge: Settings Panel focused specs or a real editor open/apply/save/reopen smoke.
- composition-visible authoring: connection editor specs and `praxis-page-builder-composition`.
- public behavior: `ng build praxis-page-builder`; browser validation when visible editor layout or page runtime changes.

Report skipped E2E explicitly. Build/spec validation is enough for non-agentic editor-only changes. Escalate to `praxis-page-builder-ai-agentic` and the full Playwright validation gate from `projects/praxis-page-builder/AGENTS.md` when the authoring change touches agentic authoring, SSE, manifests, backend tools, patch/apply, LLM integration, or Settings Panel bridge behavior used by agentic preview/apply.
