---
name: praxis-authoring-editors
description: Use when creating, expanding, or correcting visual authoring editors in `@praxisui/*`, especially `settings-panel`, config editors, builders, `metadata-editor`, apply/save/reset flows, persistence, reopening, or runtime/editor parity.
---

# Praxis Authoring Editors

Use this skill when a task creates, expands, or corrects any configuration that is editable through visual authoring in the Praxis Angular workspace.

This covers the normal authoring path used by libs such as `@praxisui/dynamic-form`, `@praxisui/table`, `@praxisui/list`, `@praxisui/charts`, `@praxisui/page-builder`, `@praxisui/manual-form`, `@praxisui/tabs`, `@praxisui/stepper`, `@praxisui/metadata-editor`, and any editor integrated with `@praxisui/settings-panel`.

For focused Settings Panel work, use the specialized family: `praxis-settings-panel-shell` for shell/protocol, `praxis-settings-roundtrip-authoring` for apply/save/reset/reopen across hosted editors, `praxis-settings-global-config` for the Global Config Editor, and `praxis-settings-ai-i18n-validation` for AI manifest and i18n coverage.
For AI-assisted authoring work, use `praxis-ai-assistant-runtime`, `praxis-ai-shell-session-context`, `praxis-ai-composer-attachments-quick-replies`, `praxis-ai-turn-orchestration-transport`, `praxis-ai-backend-config-contracts`, `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, and `praxis-ai-semantic-intent` according to whether the task touches assistant UX/context, composer controls, turn streams, backend contracts, executable manifests, generated registry/catalog artifacts, or semantic intent boundaries.
For shared core-backed editor concerns, use `praxis-core-global-actions-metadata` for structured global actions and metadata services, `praxis-core-widget-observations` for dynamic widget/editor observation contracts, `praxis-core-i18n-resource-copy` for shared i18n copy, and `praxis-core-providers-bootstrap` for provider or registry wiring.
For Page Builder work, use `praxis-page-builder-composition` for page/runtime composition, `praxis-page-builder-authoring` for page config, shell, Settings Panel and child editor hosting, and `praxis-page-builder-ai-agentic` for agentic page authoring. For Visual Builder rule authoring, use `praxis-visual-builder-rules` as the umbrella, then narrow to `praxis-visual-builder-graph-runtime`, `praxis-visual-builder-jsonlogic-roundtrip`, `praxis-visual-builder-schemas-templates`, or `praxis-visual-builder-ai-validation` according to the edited subdomain.
For `@praxisui/list`, use `praxis-list-authoring-settings` for list config editor, widget editor, JSON editor, `ListAuthoringDocument`, Settings Panel round-trip, and runtime/editor parity. Use `praxis-list-ai-validation` if the same path is authorable by assistant.
For `@praxisui/metadata-editor`, use `praxis-metadata-editor-renderer-coverage` for visual renderer/property coverage, `praxis-metadata-editor-cascade-normalization` for cascades, option-source dependencies, schema normalization, and form factory rules, `praxis-metadata-editor-consumer-bridges` for dynamic-form/table/manual-form/Page Builder hosts, and `praxis-metadata-editor-ai-validation` for manifest/capability/context-pack work.
For `@praxisui/manual-form`, use `praxis-manual-form-runtime-bridge` as the runtime umbrella and then narrow to `praxis-manual-form-field-detection-instance`, `praxis-manual-form-autosave-persistence`, or `praxis-manual-form-toolbar-metadata-bridge` for detection, draft storage, or metadata bridge work. Use `praxis-manual-form-ai-authoring` as the authoring umbrella and `praxis-manual-form-rules-agentic` for config editor, Settings Panel, manifest, capabilities, formRules, JSON Logic, agentic turn flow, and registry work. For `@praxisui/editorial-forms`, use `praxis-editorial-forms-runtime` as the runtime umbrella and then narrow to `praxis-editorial-forms-journey-snapshot-runtime`, `praxis-editorial-forms-presentation-diagnostics`, or `praxis-editorial-forms-data-collection-adapters` for journey/snapshot, fallback/presentation, or adapter work. Use `praxis-editorial-forms-adapters-ai` as the adapters/AI umbrella and `praxis-editorial-forms-agentic-authoring` for manifest operations, component metadata, registry ingestion, docs, and labs.
For `@praxisui/crud`, use `praxis-crud-runtime-openmodes` for runtime/open-mode/launcher/drawer behavior and `praxis-crud-ai-authoring` for CRUD authoring manifest, config editor, and child-operation delegation. For `@praxisui/dialog`, use `praxis-dialog-overlay-runtime` for overlay/focus/preset behavior and `praxis-dialog-global-actions-ai` for global actions, registries, and manifest work.
For `@praxisui/tabs`, use `praxis-tabs-runtime-authoring` for group/nav config, quick setup, `tabsId`, `renderBody`, selected index, widget events, and tabs editor capability. For `@praxisui/stepper`, use `praxis-stepper-wizard-runtime` for stepper config editor, dynamic-form steps, validation, wizard adapter, and `stepperId` persistence. For `@praxisui/expansion`, use `praxis-expansion-runtime-panels` for panel metadata, defaults providers, panel events, widget config editor, and `expansionId` persistence. Use `praxis-navigation-containers-ai-validation` when those editor changes are also AI-authorable or registry-projected.
For navigation container nested composition, use `praxis-navigation-container-composition-events`; for stepper/wizard workflow orchestration, use `praxis-stepper-wizard-orchestration`; for agentic registry/context-pack behavior, use `praxis-navigation-agentic-registry`.
For `@praxisui/table-rule-builder`, use `praxis-table-rule-effects-runtime` for the effects panel and registry, `praxis-table-rule-animation-presets` for semantic animations, `praxis-table-rule-table-integration` for table-owned placement and editor round-trip, and `praxis-table-rule-ai-validation` when the surface is AI-authorable or registry-projected.
For `@praxisui/files-upload`, use `praxis-files-upload-runtime` for runtime/config editor behavior, `praxis-files-upload-backend-contract` for endpoint/security/quota/rate-limit semantics, `praxis-files-upload-form-field` for form wrapper integration, and `praxis-files-upload-ai-validation` when the surface is AI-authorable or registry-projected.
For `@praxisui/rich-content`, use `praxis-rich-content-runtime` for `RichContentDocument` semantics, `praxis-rich-content-authoring-settings` for config editor and presets, `praxis-rich-content-integration-adapters` for cross-surface embedding, and `praxis-rich-content-ai-security-validation` for AI/sanitization/registry work.
For `@praxisui/cron-builder`, use `praxis-cron-builder-runtime` for component runtime and preview, `praxis-cron-schedule-authoring` for canonical schedule semantics and dialects, `praxis-cron-builder-form-field` for form/metadata integration, and `praxis-cron-builder-ai-validation` when the surface is AI-authorable or registry-projected.
For `@praxisui/charts`, use `praxis-charts-authoring-settings` for config editor and widget editor round-trip, `praxis-charts-authoring-catalogs` for resource/field/target catalogs and preview mapping, `praxis-charts-analytics-interactions` for `queryContext`, stats, drilldown, cross-filter, and selection behavior, `praxis-charts-echarts-engine-boundary` for preview/runtime ECharts adapter parity, and `praxis-charts-ai-handler-contracts` when the edited paths are AI-authorable.
For transversal Angular governance around an editor, use `praxis-angular-i18n-governance` for internal authoring text, `praxis-angular-public-api-governance` for public editor exports, `praxis-angular-docs-playgrounds` for examples/docs/playgrounds, `praxis-angular-validation-gates` to pick the local proof, and `praxis-angular-agents-governance` when local subarea AGENTS guidance is absent or suspected stale.

Do not use this skill as the primary workflow for `@praxisui/dynamic-fields` discovery/editorial changes. For that case, use `praxis-dynamic-fields-editorial`.
For dynamic-fields subdomains, route further to `praxis-fields-inline-overlay-runtime`,
`praxis-fields-text-number-time-controls`, `praxis-fields-selection-lookup-controls`, or
`praxis-fields-control-profile-ai` before changing metadata-editor coverage, Settings Panel
authoring, or generated docs for those controls.

This skill is not a generic frontend-design workflow. For Praxis, the canonical contract and the authoring round-trip matter more than local UI polish. The main question is not "can the user edit it?" but "does the editor express the canonical document correctly, persist it correctly, and survive reopen/reset without drift?"

Before changing this skill or implementing an authoring editor, inspect the current source for the
involved runtime and editor path instead of relying on memory. For widget input editors, this means
the component `ComponentDocMeta`, `configEditor`, `authoringManifestRef`, widget config editor,
editor-capability helpers, focused editor specs, AI manifest/context pack when present, i18n files,
and the host that opens the editor. The goal is to encode working Praxis platform knowledge into the
skill, not only document a UI convention.

## Primary Component Map

Use the real component family of the task, not a generic "editor changed" label.

- `@praxisui/settings-panel`: `SettingsPanelService`, `SettingsPanelRef`, `SettingsValueProvider`, `global-config-editor`, shell `Apply` / `Save` / `Reset` / `Cancel`
- `@praxisui/dynamic-form`: `config-editor`, `layout-editor`, `messages-editor`, `rules-editor`, `hooks-editor`, `actions-editor`, `json-config-editor`, canvas editors such as `section-editor`, `row-editor`, `column-editor`
- `@praxisui/table`: `praxis-table-config-editor`, `columns-config-editor`, `behavior-config-editor`, `toolbar-actions-editor`, `table-rules-editor`, `json-config-editor`, CRUD and filter authoring
- `@praxisui/list`: `list-config-editor`, `json-config-editor`
- `@praxisui/page-builder`: `page-config-editor`, `dynamic-page-config-editor`, `widget-shell-editor`, `connection-editor`
- `@praxisui/metadata-editor`: `field-metadata-editor`, `dynamic-editor-renderer`, cascade manager, coverage and normalization flows
- `@praxisui/manual-form`: `manual-form-config-editor`, field detection, `ManualFormInstance`, field toolbar, metadata bridge, autosave, formRules, and AI authoring flows
- `@praxisui/editorial-forms`: editorial runtime, journey snapshots, block provenance, dataCollection adapters, presentation/fallback diagnostics, component metadata, and manifest operations
- `@praxisui/crud`: CRUD metadata editor, widget config editor, launcher/open-mode authoring, and child delegation
- `@praxisui/dialog`: dialog shell, preset authoring, global actions, component/template registries, and child host authoring
- `@praxisui/charts`: `praxis-chart-config-editor`, `praxis-chart-widget-config-editor`, resource/field/target catalogs, preview mapper, `queryContext`, drilldown, cross-filter, runtime/editor parity, and AI authoring manifest
- `@praxisui/tabs`: tabs config editor, quick setup, editor capability, group/nav document, and AI authoring manifest
- `@praxisui/stepper`: stepper config editor, dynamic-form step config, wizard config adapter, and AI authoring manifest
- `@praxisui/expansion`: expansion widget config editor, provider metadata, panel document, and AI authoring manifest
- `@praxisui/table-rule-builder`: rule effects panel, presets, semantic animations, table rule integration, and AI authoring manifest
- `@praxisui/files-upload`: files upload config editor, widget config editor, field wrapper, backend upload policy, and AI authoring manifest
- `@praxisui/rich-content`: rich-content config editor, guided blocks, preview, JSON diagnostics, presets, validator, and AI authoring manifest
- `@praxisui/cron-builder`: CRON builder runtime metadata, schedule authoring config, preview/diagnostics, form field projection, and AI authoring manifest
- `@praxisui/visual-builder`: visual rule graph, JSON Logic round-trip, schemas/context/templates, property effects, collection validators, and AI authoring manifest

If the problem is structural and spans several editors, bias toward the canonical lib contract instead of patching a consumer editor locally.

## Canonical Goal

Every authoring change must keep this chain coherent:

`canonical config semantics -> editor UI/state -> apply/save payload -> persistence -> reopen/reload -> runtime interpretation`

If that chain is unclear, stop treating the task as a local editor tweak and identify the platform owner first.

For assistant-driven or agentic authoring, the same rule applies to progressive turns:

`backend/tool event stream -> assistant turn state -> editor UI feedback -> terminal preview/apply payload -> persistence -> reopen/reload`

Do not validate only the final response when the editor supports streaming, quick replies, clarifications, attachments, or diagnostics. A correct implementation must apply intermediate turn states to the visible assistant UI before the terminal preview/result, otherwise enterprise users see a stalled or generic assistant even though the backend is producing richer reasoning and context.

For component-scoped assistant authoring, preserve the canonical intent boundary:

- `consult/answer` is for factual questions about the active component context.
- `edit/componentEditPlan` is for governed edits that can become a reviewed patch.
- The frontend should expose safe `authoringContract` / `consultativeContext` facts and send them to the backend orchestrator; it must not classify prompts through local keywords.
- Specialized authoring flows should apply the shared scope policy helpers before backend turn resolution so greetings, loose prompts, or requests outside the active component scope return informational guidance instead of a fabricated patch.

For `@praxisui/dynamic-form` field metadata, local/transient submit semantics are part of that chain:

- `source: 'local'`, `transient: true`, and `submitPolicy` are canonical `FieldMetadata` properties owned by `@praxisui/core` and consumed by `@praxisui/dynamic-form`.
- Visual authoring must expose these properties through `@praxisui/metadata-editor` or the owning form editor when field metadata is editable.
- JSON-only support is incomplete for this contract because enterprise forms commonly need host-only helper fields that survive apply/save/reopen but stay out of backend payloads.
- Round-trip validation should prove both editor preservation and runtime submit behavior: local/transient fields remain in the UI value model while `formSubmit.formData`/HTTP payload omits them by default, with `rawFormData` retaining the full value bag.
- If a local field later collides with a backend schema field, the local submit semantics must not shadow the server-backed field.

## Canonical Boundaries

- `@praxisui/settings-panel` owns the canonical shell for runtime authoring UX.
- `SettingsPanelBridge`, `SettingsValueProvider`, and `Apply` / `Save` / `Reset` / `Cancel` are part of the contract.
- Consumer libs own the semantics of the config document they edit.
- Component input editors for dynamic widgets must be published by the owning lib through `ComponentDocMeta.configEditor`. Hosts such as `@praxisui/page-builder` should discover and open that editor via metadata instead of creating local editors for another lib's semantics.
- Widget config editors opened by a host should emit the owning component's canonical input patch or
  authoring document shape. When the component metadata exposes `inputPatch`, `configPatchChange`,
  `savedPatch`, or similar host-facing outputs, preserve that shape through
  `SettingsValueProvider.getSettingsValue()`/`onSave()` instead of inventing a host-local wrapper.
- If the component has `ComponentDocMeta.authoringManifestRef`, keep the visual editor, manifest
  operations, component capabilities, and config editor specs aligned. The visual editor is not a
  substitute for the manifest, and the manifest is not proof that the visual round-trip works.
- `@praxisui/metadata-editor` owns structural metadata authoring concerns such as dynamic renderer coverage, schema normalization, contextual hints, and cascade flows.
- For option-source cascades, treat `x-ui.optionSource.dependsOn` and `x-ui.optionSource.dependencyFilterMap` as the canonical backend/editor shape, and `dependencyFields`/`dependencyFilterMap` as runtime/manual metadata. Do not silently migrate persistence between those shapes unless the task explicitly includes an authoring migration; a form cascade editor may hydrate from the canonical shape while preserving its existing save contract.
- For global app actions in authored configs, the canonical persisted shape is `globalAction: { actionId, payload?, payloadExpr?, meta? }` and execution goes through `GlobalActionService.executeRef(...)`. Keep `action` for local component/host events only. Do not persist or reintroduce command strings such as `showAlert:...`, `openUrl:...`, `navigate:...`, `apiCall:...`, or `surface.open:{...}`.
- When visual authoring edits a `globalAction` payload, reuse the canonical `GlobalActionUiSchema`/`getGlobalActionUiSchema(...)` field model and shared global-action authoring helpers where available. Do not leave required payloads as JSON-only fields when the platform already exposes structured fields such as `dialog.alert.message`; the editor may keep an advanced JSON escape hatch, but the primary path must produce the canonical `GlobalActionRef` shape and validate required payloads before apply/save.
- Internal authoring chrome is platform text. Labels, placeholders, helper text, section titles, tab titles, empty states, and fallback messages must follow the lib i18n path instead of hardcoded literals.
- Domain Catalog, governance, and semantic context are grounding inputs for authoring decisions, not
  rules to copy into local `FormConfig`, table config, or CRUD metadata. Persist lightweight
  references/probes only when the owning contract declares that shape, such as
  `queryContext.meta.domainCatalog`; do not materialize shared governance rules into component JSON
  as a shortcut.
- Composed editors such as CRUD must delegate child semantics to their owners. Form layout,
  `FieldMetadata`, validation rules, and table columns belong to the dynamic-form, metadata-editor,
  or table contracts; the composed editor should bind/delegate rather than redefine those contracts.
- When a public authoring surface changes, also review the canonical lib artifacts that govern it: `README.md`, `src/public-api.ts`, and the subarea docs called out by the local `AGENTS.md`.
- Structural panel problems should be fixed in `@praxisui/settings-panel`, not reimplemented in each consumer editor.

## Trigger Conditions

Use this skill when the task changes any of:

- a new visual editor for an existing Praxis config document
- a new editable section/tab/panel for an existing editor
- config shape
- defaults
- normalization
- persistence
- restore or reopen behavior
- `apply/save/reset`
- embedded editor fields
- builder panels
- editor sections or tabs
- JSON editor contracts
- settings-panel inputs
- runtime/editor parity
- metadata editor coverage or renderer behavior
- authoring i18n or internal editor text
- editor-specific docs or public API that must stay aligned with the runtime path

## Required Preflight

Before editing, answer these explicitly:

1. What is the canonical owner of the semantics being edited?
2. Is the task creating a new editor surface or correcting an existing one?
3. What exact document shape or config path must the editor produce?
4. Where does the round-trip fail or need to be introduced:
   - open
   - edit
   - apply
   - save
   - reset
   - reopen
   - runtime consume
5. Which governed artifacts must stay in sync?

If the owner is unclear, load `references/scope-boundaries.md` and `references/owner-decision-matrix.md` before editing.

## Required Workflow

1. Identify the canonical owner of the config, metadata, or builder semantics.
2. Identify the concrete editor family and component that exposes it.
3. Map the chain:
   `runtime config -> editor state -> apply/save payload -> persistence -> reopen/reload`
4. Decide whether the fix belongs in:
   - `@praxisui/settings-panel`
   - `ComponentDocMeta.configEditor` in the lib that owns the widget input contract
   - the consumer lib editor
   - `@praxisui/metadata-editor`
   - `praxis-dynamic-fields-editorial` instead of this skill
5. For widget-hosted editors, verify the owning component metadata and host contract:
   - `ComponentDocMeta.configEditor`
   - `authoringManifestRef` when present
   - `SettingsValueProvider` output shape
   - host-facing `inputPatch`/saved patch outputs
   - focused editor-capability specs
6. Check whether the change affects:
   - field visibility
   - field editability
   - labels or internal authoring text
   - i18n coverage for internal authoring text
   - defaults
   - normalization
   - reset semantics
   - partial save behavior
   - schema normalization or metadata coverage
   - docs or `public-api` governed by the canonical lib
7. If the task creates or significantly expands an editor, load `references/new-editor-checklist.md`.
8. Run the smallest reliable round-trip validation for that component family.

## When Creating A New Editor

Creating a new editor is a contract task, not only a rendering task.

Start from the canonical config/runtime semantics, then make the editor faithfully expose them. Do not invent local aliases, editor-only semantics, or host-only wrappers just to make the UI easier to implement.

Minimum expectations for a new editor:

- the owning lib and owner boundary are explicit
- the edited document shape is known
- dynamic widget input editors are exposed via the owning component metadata (`ComponentDocMeta.configEditor`) when the editor is meant to be discovered by hosts
- the editor writes the canonical shape, not a temporary shape
- the editor participates correctly in `Apply` / `Save` / `Reset` / `Cancel` when hosted in `settings-panel`
- reopening the editor reloads the same value without silent normalization drift
- runtime consumes the saved document without adapter-only hacks
- i18n and governed docs/public API are reviewed when the surface is public
- widget-hosted editors preserve the canonical `inputPatch`/authoring document shape expected by
  page-builder or the host that opened the editor

If the runtime cannot already consume the intended semantics, fix the canonical runtime contract first instead of building a compensating editor.

## Required Checks

Before considering the task complete, verify:

- The changed config is still reachable in the canonical editor.
- The editor still emits the correct shape through `SettingsValueProvider`.
- Runtime still consumes the saved or applied document without hidden drift.
- Reopening the editor does not lose, rewrite, or silently normalize the value incorrectly.
- Reset semantics remain correct.
- New or changed internal authoring text still follows the workspace i18n rules instead of hardcoded literals.
- If the change touched a governed authoring surface, the canonical `README`, `public-api`, or subarea docs were reviewed for sync.
- If the task created a new editor surface, the editor owner and canonical document shape are now discoverable in the code and docs of the owning lib.
- For widget-hosted editors, the host receives the same canonical input patch or authoring document
  shape on apply/save that the owning component documents and tests.
- If the editor change crosses package, docs, i18n, or validation boundaries, the matching transversal Angular skill was applied or explicitly ruled out.

## Agentic Manifest Checks

When the authoring surface is an executable AI manifest, treat the manifest as a backend contract, not only as documentation.

- When changing a public `@praxisui/*` component, always check whether the change affects the component AI manifest. This applies even when the task starts as a runtime/editor fix rather than a manifest task.
- Review the manifest when the change touches public inputs, outputs, events, editable config paths, authoring operations, capabilities, actions, accepted schemas/paths, runtime/editor parity, persistence, `apply/save/reset/reopen`, `ComponentDocMeta`, `public-api`, public README, examples, recipes or playgrounds.
- For components with an existing manifest, verify `projects/<lib>/src/lib/ai/*authoring-manifest.ts`, focused manifest specs, AI registry projection when applicable, `docs/ai/agentic-authoring/component-authoring-contracts`, and derived recipes/examples when public behavior changed.
- If no manifest update is required after a functional component change, state why. Do not edit manifests mechanically when the public authoring surface did not change.
- If a public component still has no AI manifest, note whether the change raises manifest priority or should be recorded in the component-authoring-contract docs.
- When a component participates in agentic authoring, review whether its `authoringContext` still declares the correct response modes (`consult/answer`, `edit/componentEditPlan`), safe consultative facts, and scope policy application before assuming the manifest alone is sufficient.
- Do not count a parent `affectedPaths` entry as proof that every descendant capability is authorable. If a catalog publishes nested paths, focused specs must verify that each published path is covered by an operation whose input schema can actually express and validate that path.
- Keep operation schemas concrete for published enum and structured fields. Broad `type: object` payloads are acceptable only when paired with an explicit blocker or a downstream schema reference that backend tools can resolve deterministically.
- For operations that use `compile-domain-patch`, require a deterministic handler contract in the manifest. The contract should name read paths, write paths, stable identity keys, handler input schema when applicable, failure modes, and a concise operational description.
- Handler names alone are not enough for backend patch compilation. A focused spec should fail if any `compile-domain-patch` effect lacks the handler contract or uses array index as canonical identity.
- For family-level manifests, the registry must expose an aggregate entry addressable by the manifest `componentId`, not only copies attached to child components. Governance should fail if backend tools cannot resolve the family manifest by `COMPONENT_ID` or if the aggregate projection count drifts from the child component entries.
- When a runtime/config catalog marks fields as declared-only, the manifest may keep them authorable for config/editor round-trip, but docs and validators must not imply active runtime behavior.

## High-Risk Failure Modes

Treat these as canonical risks:

- editor created before clarifying canonical ownership
- editor writes a local convenience shape instead of the runtime contract
- config supported in JSON but hidden in the editor
- field visible but not persisted
- field persisted but ignored by runtime
- assistant stream treated as a terminal-only promise, causing progress, clarification, diagnostics, attachments, or quick replies to be hidden until the final response
- `Apply` works but `Save` does not
- `Save` works but reopen rewrites the value
- `Reset` clears too much or too little
- internal authoring text fixed functionally but left hardcoded outside the canonical i18n path
- editor renderer coverage diverges from what the metadata editor claims to support
- schema normalization or cascade flow mutates adjacent config silently
- public authoring docs describe a path or field that the editor no longer exposes
- component behavior changes while the AI manifest still advertises stale inputs, paths, operations or capability semantics
- manifest coverage tests accept broad parent paths while operation schemas cannot express the nested capability
- `compile-domain-patch` operations expose only handler names, leaving backend tools unable to compile or reject patches deterministically
- family-level manifests are projected only onto child components, leaving no aggregate registry entry addressable by the manifest `componentId`
- local workaround in a consumer instead of fixing the canonical panel/editor contract
- page-builder or another host creates a component-specific input editor instead of consuming `ComponentDocMeta.configEditor` from the owner lib
- host-specific glue becomes the de facto contract because the owning lib was not corrected
- global actions are serialized through `action` strings instead of persisted as structured `globalAction`

## Validation Guidance

Prefer the smallest relevant validation:

- `openConfigEditor` specs when opening or wiring changed
- `SettingsValueProvider` specs when payload or dirty/valid/busy contract changed
- focused integration specs when round-trip changed
- assistant/agentic specs that prove intermediate emitted turn states update the UI before the terminal preview when streaming is supported
- assistant scope-policy specs when the component declares consultative context or component edit plans, proving off-scope prompts stay informational and in-scope prompts still reach governed edit planning
- metadata-editor coverage or renderer specs when the task touches dynamic editor rendering, hints, flows, or schema normalization
- Playwright authoring flows when UI visibility, drag/drop, or multi-step authoring behavior is material and focused specs are not enough

For Playwright authoring flows, prefer stable component-owned `data-testid` or semantic test ids for opening editor chrome and critical apply/save/reset controls when the test purpose is functional round-trip behavior. Do not make these E2E flows depend on localized labels or visible copy if the component already exposes a stable selector. Keep accessible names, user-visible labels, and i18n coverage validated in focused component specs; stable selectors are not a substitute for accessibility or localization correctness.

When the authoring entrypoint is exposed through a host toolbar, validate the actual entrypoint in the smallest viewport that the workflow claims to support. If the global toolbar hides customization/edit mode in narrow/mobile, provide and validate an equivalent route-local or component-local authoring entrypoint rather than treating desktop access as sufficient.

For Settings Panel, metadata editor, drawer, side-sheet, and inspector flows, include a narrow viewport check with the editor open whenever visual layout changed or the edited field group uses multi-column, inline, or helper-text rows. A runtime screenshot after save is not enough to catch clipped labels, hidden help text, footer overlap, or unreachable apply/save controls inside the editor shell.

When a Playwright authoring flow validates `Save`/persistence followed by `reopen`, prefer reopening in a fresh page/context through the same canonical route and config endpoint instead of reusing the same browser page after a long authoring conversation. Reusing the same page can hide or create failures from residual runtime state, pending assistant UI state, stale selected widgets, or client-side caches. Use the existing project helper for clean reopen when one exists, and keep same-page reload assertions only when the behavior under test is explicitly in-place reload/state retention.

Bias the validation toward the owning lib:

- `dynamic-form`: config/layout/messages/rules/hooks/actions/json editor specs, then e2e only if authoring flow changed materially
- for deep `dynamic-form` work, use `praxis-form-authoring-settings`; add `praxis-form-layout-canvas` for layout/canvas/visual blocks and `praxis-form-ai-rules-validation` for AI/rules/diagnostics
- `table`: use `praxis-table-authoring-settings`; run focused editor specs first, then table authoring e2e when config visibility, Settings Panel round-trip, rules, filters, CRUD integration, or drag/drop behavior changed
- `list`: editor specs first, then doc-page or e2e only if canonical authoring behavior changed
- `page-builder`: focused builder or connection specs first; treat settings bridge changes as cross-lib impact
- `metadata-editor`: coverage, renderer, schema-normalizer, and cascade specs before broader validation
- `settings-panel`: panel/service/provider specs when shell semantics changed

Minimum acceptable flow for editable UI config:

`open editor -> change value -> apply/save -> runtime reflects -> reopen editor -> value still correct`

If no visual editor is affected, say that explicitly in the final response.

## References

Load these only as needed:

- `references/settings-panel-contract.md`
- `references/authoring-round-trip-checklist.md`
- `references/validation-matrix.md`
- `references/scope-boundaries.md`
- `references/owner-decision-matrix.md`
- `references/new-editor-checklist.md`
