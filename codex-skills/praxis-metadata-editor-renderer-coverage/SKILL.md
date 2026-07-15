---
name: praxis-metadata-editor-renderer-coverage
description: Use when implementing, reviewing, or auditing `@praxisui/metadata-editor` renderer coverage: `FieldMetadataEditorComponent`, `DynamicEditorRendererComponent`, `EditorProperty[]` configs, inline editor coverage, dynamic-fields parity, form factory controls, visual coverage versus JSON-only fallback, hints, i18n labels, and public API for metadata editor components/services.
---

# Praxis Metadata Editor Renderer Coverage

Use this skill for visual metadata authoring coverage in `@praxisui/metadata-editor`. The editor owns the UI that edits canonical `FieldMetadata`; it does not render final form fields at runtime and it must not duplicate `@praxisui/dynamic-fields` component semantics.

When locating files, first resolve the Angular workspace root. Paths below are relative to
`praxis-ui-angular/projects/praxis-metadata-editor` unless another package is explicitly named.

## Canonical Boundary

`@praxisui/metadata-editor` owns:

- `FieldMetadataEditorComponent`
- `DynamicEditorRendererComponent`
- `ConfigRegistryService`
- `EditorComponentRegistryService`
- `EditorProperty[]` config catalogs under `src/lib/config/*.config.ts`
- `DynamicFormFactoryService`
- `SchemaNormalizerService`
- metadata-editor AI adapter, manifest, context pack, and capability catalog when visual coverage is AI-authorable
- visual coverage docs/checklists

`@praxisui/dynamic-fields` owns the actual field components, control type discovery, descriptors, and runtime interpretation. When a dynamic-field runtime property is missing from the editor, add visual coverage in metadata-editor; do not copy runtime component logic into the editor.

## Required Source Audit

Inspect before editing:

- `projects/praxis-metadata-editor/AGENTS.md`
- `README.md`
- `docs/metadata-editors-architecture.praxis.md`
- `docs/EDITOR-COVERAGE-CHECKLIST.md`
- `docs/HINTS-STYLE-GUIDE.md`
- `src/public-api.ts`
- `src/lib/components/field-metadata-editor/field-metadata-editor.component.ts`
- `src/lib/components/dynamic-editor-renderer/dynamic-editor-renderer.component.ts`
- `src/lib/config/*.config.ts` for the affected control type
- `src/lib/config/inline-filter-control-properties.map.ts` when inline filter coverage is involved
- `src/lib/config/inline-editor-coverage.spec.ts`
- `src/lib/services/schema-normalizer.service.ts`
- `src/lib/services/dynamic-form-factory.service.ts`
- `src/lib/registry/config-registry.service.ts`
- `src/lib/ai/praxis-metadata-editor-authoring-manifest.ts` and spec when the surface is AI-authorable
- `src/lib/ai/metadata-editor-ai.adapter.ts` and spec when AI patch application is involved
- `src/lib/ai/metadata-editor-context-pack.ts` and `metadata-editor-ai-capabilities.ts` when assistant grounding changes
- the owning dynamic-fields component/descriptor for the same control

## Coverage Rules

- Every critical runtime metadata property should have visual coverage or an explicitly documented advanced JSON fallback.
- JSON-only support is not acceptable for common authoring paths such as labels, placeholders, validators, icons, clear buttons, option sources, entity lookup, presentation, submit policy, and accessibility.
- `EditorProperty.name` dot paths must match canonical `FieldMetadata` paths or documented metadata-editor paths.
- Groups, hints, labels, placeholders, and options must use the metadata-editor i18n path when the lib has catalog coverage.
- Icon fields should use Material Symbols guidance such as `mi:...`; ordinary prefix/suffix text must not receive icon-only hints.
- `controlType` must be normalized through core helpers and must exist in both dynamic-fields discovery and metadata-editor config coverage.
- Metadata-editor may select and materialize a `controlType`, but it must not mint package-owned
  control identities. Unknown controls should fail through the dynamic-fields/core discovery path
  instead of creating a local editor-only type.
- Inline filter coverage must stay complete for `INLINE_FILTER_CONTROL_TYPE_VALUES`; aliases should
  resolve through `resolveInlineFilterEditorProperties(...)`, and unknown aliases should remain
  unsupported rather than receiving a guessed editor config.
- `ConfigRegistryService` and `EditorProperty[]` arrays are the visual coverage catalog for metadata
  editing. They should expose canonical paths with typed editor controls; advanced JSON textareas are
  acceptable only for genuinely structured/legacy escape hatches and should be documented as such.
- Renderer coverage proves that metadata can be authored and round-tripped visually; it does not prove
  that the owning dynamic-field, option-source provider, backend endpoint, entity lookup runtime,
  inline overlay, or AI authoring profile executes that behavior. When adding paths such as
  `optionSource.*`, `payloadMode`, selection policy, detail/create actions, or inline control
  properties, also point to the owning runtime/profile evidence before documenting the capability as
  active.
- For remote select/list/entity authoring, prefer governed fields such as `resourcePath` and
  `optionSource.*` over legacy `endpoint` properties. `configs-remote-source.spec.ts` is the boundary
  proof: common select-like configs should not reintroduce `endpoint`, while entity lookup visual
  coverage must expose `RESOURCE_ENTITY` metadata including key/type/entity/resource paths, identity,
  display, dependency, selection policy, capabilities, detail/create actions, dialog, and payload
  mode paths. Do not hide these common paths behind a JSON-only textarea or host-local editor patch.
- AI-assisted metadata editing must use declared manifest operations such as `controlType.set`,
  `renderer.configure`, and inline/presentation operations. The adapter must reject free-form
  `seed`/`controlType` patches and JSON-only coverage for required visual authoring.
- `renderer.configure` is a registry/editor-coverage operation, not a consumer seed patch. In the
  current adapter it requires a specialized runtime/editor handler and must not be compiled into a
  local `seed` or `FieldMetadata` patch. If a migration needs new visual coverage, update the owning
  `EditorProperty[]` catalog, renderer registry/factory evidence, specs, and AI manifest/context
  evidence instead of teaching the consumer or assistant to mutate one screen's metadata directly.

## Renderer And Form Factory

`DynamicEditorRendererComponent` renders `EditorProperty[]` into grouped form rows through `DynamicFieldLoaderDirective`. `DynamicFormFactoryService` creates controls by dot path and attaches contextual validators. Do not bypass that path with local component-specific forms unless the editor property type itself is missing and needs to be added to the registry.

When adding an editor property:

1. Confirm the runtime component actually consumes the metadata.
2. Add or update the correct `*.config.ts`.
3. Ensure `SchemaNormalizerService` hydrates seed defaults correctly for complex values.
4. Ensure `DynamicFormFactoryService` creates the control at the correct dot path.
5. Add/update focused coverage specs.
6. If the property claims runtime behavior beyond visual round-trip, verify the owning
   dynamic-fields/runtime/option-source skill evidence and keep unsupported paths marked as partial,
   declared-only, or JSON-only.
7. Update AI manifest/context-pack/capabilities if the visual coverage is AI-authorable.
8. Update docs/checklists if coverage status changed.

## Validation

Use focused gates:

- renderer layout or grouping: `components/dynamic-editor-renderer/dynamic-editor-renderer.component.spec.ts`
- field host/control-type resolution: `components/field-metadata-editor/field-metadata-editor.component.spec.ts`
- inline/dynamic-fields parity: `config/inline-editor-coverage.spec.ts`
- remote option/entity lookup visual coverage: `config/configs-remote-source.spec.ts` plus the owning
  dynamic-fields option-source/runtime evidence when behavior, not only editor materialization, changed
- form factory dot-path/control creation: `testing/dynamic-form-factory.service.spec.ts`
- schema normalization for defaults/complex values: `testing/schema-normalizer.service.spec.ts`
- i18n catalog behavior: `i18n/metadata-editor.i18n.spec.ts`
- AI manifest/adapter coverage: `ai/praxis-metadata-editor-authoring-manifest.spec.ts` and `ai/metadata-editor-ai.adapter.spec.ts`
- compile surface: `ng build praxis-metadata-editor`

Use `praxis-angular-public-api-governance` for root exports and `praxis-angular-validation-gates` to decide whether a consumer E2E is needed.
