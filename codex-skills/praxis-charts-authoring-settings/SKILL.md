---
name: praxis-charts-authoring-settings
description: Use when Codex must implement or audit @praxisui/charts visual authoring and Settings Panel round-trip: PraxisChartConfigEditor, PraxisChartWidgetConfigEditor, SettingsValueProvider, direct chart versus widget input envelopes, apply/save/reset/reopen, canonical x-ui.chart version and defaults, queryContext editing, config editor metadata, preview parity, governed catalogs, i18n, or AI manifest alignment.
---

# Praxis Charts Authoring Settings

Use this skill for chart config editors and their Settings Panel hosts. The editor materializes canonical `x-ui.chart` decisions; it does not own business rules, analytics capabilities, persistence infrastructure, or an ECharts-shaped configuration language.

Pair it with:

- `praxis-settings-panel-shell` for shell, footer, close, drawer, and `SettingsValueProvider` protocol defects.
- `praxis-settings-roundtrip-authoring` for shared apply/save/reset/reopen invariants.
- `praxis-authoring-editors` and `praxis-ui-product-design` for transversal editor governance and visual UX changes.
- `praxis-charts-authoring-catalogs` for resource, field, target, capability, and preview catalog grounding.
- `praxis-charts-runtime-data` and `praxis-charts-analytics-interactions` for mapper, stats, `queryContext`, and runtime consumption.
- `praxis-charts-ai-validation` and `praxis-charts-ai-handler-contracts` when visual paths, component metadata, or executable manifest operations change.
- `praxis-charts-echarts-engine-boundary` only for preview/runtime engine materialization.

## Canonical Owners

- `praxis-metadata-starter/docs/spec/x-ui-chart.schema.json` owns the published structural `x-ui.chart` vocabulary and version. Do not advance an Angular editor default independently from that schema.
- `@praxisui/charts` owns `PraxisXUiChartContract`, normalization, validation, editor semantics, runtime mapping, preview, component metadata, and chart authoring manifest alignment.
- `@praxisui/settings-panel` owns Apply/Save/Reset/Cancel gating and obtains values from `SettingsValueProvider`.
- The dynamic Page Builder/core widget host owns opening `ComponentDocMeta.configEditor`, replacing widget inputs from the returned envelope, and persisting the page definition.
- `praxis-config-starter` or the declared host storage owns governed persistence, ETag, approval, and publication. A chart editor does not write storage directly.
- Backend metadata, schemas, analytics projections, option sources, and capabilities own which resources, fields, operations, metrics, and targets are authorable.

## Two Authoring Envelopes

Do not conflate the direct chart editor with the widget editor.

### Direct runtime chart

`PraxisChartComponent.openConfigEditor()` hosts `PraxisChartConfigEditor` and expects the panel value to be a `PraxisXUiChartContract`:

`chartDocument -> editor state -> getSettingsValue/onSave -> applied$/saved$ -> runtimeChartDocument -> chartDocumentApplied/chartDocumentSaved`

Apply updates the component preview/runtime without closing. Save emits the same document shape; the external host decides whether and where to persist it.

### Dynamic widget/Page Builder

`ComponentDocMeta.configEditor` points to `PraxisChartWidgetConfigEditor`. The widget host passes one `inputs` object and accepts either an `{ inputs }` envelope or a legacy bare object, then replaces the widget's complete input object:

`widget.definition.inputs -> PraxisChartWidgetConfigEditor -> { inputs } -> apply/save -> complete widget input replacement -> page persistence -> reopen`

Therefore the widget editor must preserve every unrelated input deliberately, update `inputs.chartDocument` and `inputs.queryContext`, and remove only inputs whose precedence would be wrong. For `source.kind = "praxis.stats"`, remove stale local `inputs.data`; do not silently delete shell or host inputs.

## Initialization And Baselines

- `PraxisChartConfigEditor` may initialize from its documented component input or `SETTINGS_PANEL_DATA` compatibility shape. Keep one canonical input name and do not rely on passing duplicate aliases that the Settings Panel filters out.
- Normalize a cloned external document into both current state and the reset baseline. Controlled normalization drift must be tested and documented; unknown canonical fields must not disappear accidentally.
- New documents must use the version published by the metadata schema and accepted by the manifest/validator. As of the current draft this is `0.1.0`; a local `1.0.0` default is not a version migration.
- A widget with only runtime `config`/`data` has no canonical authoring document. Do not fabricate a generic chart document on save and let it take precedence over the existing chart. Prefer canonical `chartDocument` insertion defaults; otherwise require an explicit, tested `PraxisChartConfig -> PraxisXUiChartContract` migration or block authoring with a diagnostic.
- Preserve a separate baseline for `queryContext` and every widget-owned editable input. Reset must restore the entire editor scope, not only the nested chart document.
- When external inputs change while clean, rebase all baselines. Do not overwrite dirty local work silently.

## SettingsValueProvider Semantics

- `isDirty$`, `isValid$`, and `isBusy$` are authoritative shell signals. Compose child editor and widget-level state without losing either source.
- `getSettingsValue()` powers Apply and must be side-effect free: it returns the current canonical value but does not mark it saved or replace the reset baseline.
- `onSave()` may finalize the same value, then establish the saved baseline. It must not return a different envelope from Apply.
- `reset()` restores the opening/saved baseline for chart document, `queryContext`, errors, dirty, valid, and busy state. It must be idempotent.
- Invalid state should prevent shell actions, but value methods should still fail predictably rather than leaking an unhandled `JSON.parse` exception if invoked programmatically.
- Do not add local Apply/Save gating or persistence calls to compensate for Settings Panel behavior.

## Canonical Document Editing

Use `ChartContractNormalizerService` and `ChartContractValidationService`, then prove every visually editable path survives round-trip. Review at least:

- version, kind, preset, id, title/subtitle, source, dimensions, metrics, aggregations, group/sort/filter/limit;
- operation-specific stats options and refresh semantics supported by the runtime;
- legend, labels, tooltip, theme, surface, sizing, states, and motion;
- point click, selection, drilldown, cross-filter, governed targets, and mappings.

Changing kind, source, operation, or resource may invalidate dependent state. Preserve compatible values; surface validation for incompatible values; remove data only through explicit normalizer rules. Do not silently keep stale metric/axis/source options merely because the form control is hidden.

The preview must consume the normalized document through the same canonical mapper and `PraxisChartComponent`. Synthetic rows are acceptable for an explicitly local authoring preview, but the UI must not imply that a remote stats request or backend capability was proved.

## Query Context

- Keep `queryContext` as a structured widget runtime input, separate from `chartDocument.source` and static document filters.
- A JSON textarea is an advanced fallback, not proof of rich authoring. Accept only a serializable non-array object and preserve filters, sort, limit, page, and meta that the runtime contract supports.
- Do not display raw parser exception messages. Use chart i18n keys for label, help, invalid JSON, and non-object errors.
- Empty text removes `inputs.queryContext`; reset restores the original value and dirty/valid state; apply/save/reopen preserve semantic equality.
- Do not promise that every `queryContext` property changes the default stats POST. Use `praxis-charts-runtime-data` for the exact execution boundary.

## Governed Catalogs

- `availableResources`, `availableFields`, and `availableTargets` are authoring context from governed metadata/catalog owners, not values the editor invents.
- Remote resource, field, metric, operation, and event-target choices must fail closed when required catalogs/capabilities are unavailable. A free-form resource URL or target input is not a safe fallback for governed authoring.
- Selecting a resource must resolve or refresh its compatible field, metric, operation, and capability catalog before dependent selections are accepted.
- Preserve stable identities: resource canonical key/path, `metrics[].field`, dimension field, and target id. Labels are presentation only.
- Determine whether catalogs are transient editor context or intentionally persisted runtime inputs. Do not freeze stale API metadata into page config by accidental object spreading.
- Reuse canonical option-source/search controls where appropriate; do not create a chart-local lookup service when shared metadata or `@praxisui/dynamic-fields` already owns discovery.

## Metadata, AI, And Derived Artifacts

When an editable path or input envelope changes, inspect together:

- `praxis-chart.metadata.ts`: runtime inputs, outputs, `configEditor`, insertion defaults/presets, ports, and `authoringManifestRef`;
- `praxis-charts-authoring-manifest.ts`: schema version, runtime inputs, editable targets, operations, validators, affected paths, and round-trip requirements;
- AI registry ingestion/generated assets when metadata or manifest projection changes;
- README, public docs, recipes, playgrounds, and the Settings Panel smoke when public authoring behavior changes.

The visual editor and AI manifest must author the same canonical paths. Metadata must not expose a config editor whose default widget inputs cannot be reopened safely.

## Inventory Before New Contract

- `ja-suportado-so-ux`: canonical path exists; editor layout, i18n, diagnostics, or preview presentation is incomplete.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: local default version, raw URL/target fallback, stale catalog copy, or widget envelope obscures an existing canonical contract.
- `suportado-parcialmente`: document/input/protocol exists but baseline, reset, catalog cascade, manifest metadata, persistence host, or runtime parity is incomplete.
- `lacuna-real-de-contrato`: no canonical schema field, renderer-neutral runtime input, Settings Panel operation, catalog capability, or widget host envelope can express the behavior.

Only a real gap justifies a new public input, model, operation, or persistence contract. During beta, correct the canonical source and migrate monorepo consumers in one cycle instead of adding parallel aliases.

## Validation Matrix

Require focused assertions for the changed rows:

- document editor: input/DI initialization, current versus baseline, dirty/valid/busy, controlled normalization, Apply, Save, Reset, readonly, external rebase, and every affected canonical path;
- widget editor: full `{ inputs }` preservation, chart document precedence, missing-document behavior, query context valid/invalid/non-object/empty, remote-data pruning, reset, reopen, and multiple save cycles;
- catalogs: governed selection, missing-catalog fail-closed behavior, resource-to-field cascade, stale selection diagnostics, and stable identities;
- metadata/defaults: canonical `0.1.0` insertion document, `configEditor`, ports, runtime inputs, and manifest reference;
- AI: manifest version/schema/editable paths and registry projection;
- runtime parity: normalizer, validator, canonical mapper, component precedence, and local preview boundary;
- host proof: open -> edit -> Apply -> runtime reflects -> Save -> persisted widget inputs -> reopen -> Reset, at desktop and narrow widths when UI changed.

Typical focused gates from the Angular workspace root are:

```bash
npx ng test praxis-charts --watch=false --progress=false --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-config-editor.spec.ts' --include='projects/praxis-charts/src/lib/config-editor/praxis-chart-widget-config-editor.spec.ts' --include='projects/praxis-charts/src/lib/praxis-chart.metadata.spec.ts' --include='projects/praxis-charts/src/lib/ai/praxis-charts-authoring-manifest.spec.ts'
npx ng test praxis-charts --watch=false --progress=false --include='projects/praxis-charts/src/lib/services/chart-contract-normalizer.service.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-contract-validation.service.spec.ts' --include='projects/praxis-charts/src/lib/services/chart-canonical-contract-mapper.service.spec.ts' --include='projects/praxis-charts/src/lib/components/praxis-chart/praxis-chart.component.spec.ts'
npm run build:praxis-charts
npx playwright test --config tools/e2e/playwright/praxis-charts-settings-panel.playwright.config.ts
```

Do not claim round-trip from helper tests alone. Report the exact Settings Panel/host flow proved, backend/catalog capabilities not exercised, skipped screenshot/browser checks, and whether docs, metadata, manifest, registry, and direct consumers required updates.
