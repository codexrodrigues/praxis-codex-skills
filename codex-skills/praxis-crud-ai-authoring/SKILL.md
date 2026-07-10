---
name: praxis-crud-ai-authoring
description: Use when changing or validating `@praxisui/crud` authoring and AI surfaces, including `CrudAuthoringDocument`, `CrudMetadataEditorComponent`, `PraxisCrudWidgetConfigEditor`, `openCrudMetadataEditor`, `PRAXIS_CRUD_AUTHORING_MANIFEST`, `CRUD_AI_CAPABILITIES`, CRUD context packs, resource/list/create/edit/view/delete operations, permissions, dialog defaults, child-operation delegation, registry ingestion, and authoring round-trip.
---

# Praxis CRUD AI Authoring

Use this skill for governed CRUD authoring. CRUD AI edits must compile to manifest-backed operations over `CrudMetadata`; they must not emit free JSON patches or redefine table, form, dialog, or settings-panel child contracts.

Pair with `praxis-crud-drawer-adapter-contract` for drawer adapter/public entrypoint work and with `praxis-crud-dialog-form-host-lifecycle` for modal/drawer form-host lifecycle, semantic result propagation, and refresh behavior.

## Required Source Audit

Inspect:

- `projects/praxis-crud/AGENTS.md`
- `src/lib/ai/praxis-crud-authoring-manifest.ts`
- `src/lib/ai/crud-ai-capabilities.ts`
- `src/lib/ai/crud-ai.adapter.ts`
- `src/lib/ai/crud-context-pack.ts`
- `src/lib/crud-authoring-document.model.ts`
- `src/lib/crud-editor-capability.ts`
- `src/lib/crud-metadata-editor.component.ts`
- `src/lib/praxis-crud-widget-config-editor.ts`
- `src/lib/open-crud-metadata-editor.ts`
- README, docs manifest, public API, and focused specs

## Authoring Boundary

CRUD authoring owns:

- resource binding
- list surface orchestration
- create/edit/view/delete action binding
- open mode defaults and dialog host defaults
- permissions/capability policy references
- child-operation delegation
- CRUD authoring document persistence events

Delegate child details to their owners:

- table operations to table skills/manifests
- form config, field metadata, submit, and rules to dynamic-form/metadata-editor skills
- dialog shell details to dialog skills
- Settings Panel protocol to settings-panel skills

## Manifest Rules

Use `PRAXIS_CRUD_AUTHORING_MANIFEST` as executable source.

- `resource.bind` must validate canonical resource path/key, id field, schema path, api metadata, and capabilities.
- `list.surface.configure` may patch CRUD list orchestration but must delegate table semantics.
- `surface.create|edit|view.configure` must produce complete route/modal/drawer bindings.
- Drawer bindings configure CRUD orchestration only; host drawer shell overrides remain adapter contracts and must not be authored as freeform component patches.
- `delete.enabled.set` requires explicit confirmation/capability policy when destructive.
- `dialog.size.set` or dialog defaults must remain shell-level and delegate dialog details.
- `form.childOperation.delegate` is required when the user asks to change form fields, rules, layout, or submit behavior.

Do not materialize Domain Catalog governance rules into `CrudMetadata` as a shortcut. Store only declared lightweight references/probes when the contract supports them.

## Validation

Minimum gates:

- manifest: `src/lib/ai/praxis-crud-authoring-manifest.spec.ts`
- adapter/context: `src/lib/ai/crud-ai.adapter.spec.ts`
- editor capability: `src/lib/crud-editor-capability.spec.ts`
- metadata editor/widget editor: focused editor specs
- authoring entrypoint: `src/lib/praxis-crud.authoring-entrypoint.spec.ts`
- compile: `npm run build:praxis-crud`
- registry/docs: `npm run generate:registry:ingestion` when component docs or AI assets change

Pair with `praxis-crud-runtime-openmodes` for runtime launcher behavior and `praxis-angular-validation-gates` for validation scope.
