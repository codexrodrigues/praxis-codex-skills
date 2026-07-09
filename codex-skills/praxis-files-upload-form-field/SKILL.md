---
name: praxis-files-upload-form-field
description: Use when Codex must wire, audit, document, or author `pdx-material-files-upload` and dynamic-form file upload integration, including ControlValueAccessor behavior, `valueMode` shapes, `metadata` versus `id` form values, compact upload shell UX, hidden `praxis-files-upload` runtime delegation, validation errors, pending file state, upload side effects, accessibility, dynamic-fields metadata, CRUD/form consumers, docs, examples, or host form integration.
---

# Praxis Files Upload Form Field

Use this skill for the form-field wrapper around the upload runtime. Treat `pdx-material-files-upload` as the canonical Dynamic Fields upload bridge when forms need operational uploads, not as a generic file picker.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-files-upload/AGENTS.md`
- `projects/praxis-files-upload/README.md`
- `projects/praxis-files-upload/docs/host-files-upload-integration.md`
- `projects/praxis-files-upload/src/lib/components/files-upload-field/pdx-files-upload-field.component.ts`
- `projects/praxis-files-upload/src/lib/components/files-upload-field/pdx-files-upload-field.component.spec.ts`
- `projects/praxis-files-upload/src/lib/components/files-upload/praxis-files-upload.component.ts`
- `projects/praxis-dynamic-fields/**` when metadata discovery or field catalog behavior changes
- dynamic-form, CRUD, docs, examples, or playground consumers that embed the upload field

## Canonical Boundary

`pdx-material-files-upload` owns:

- `ControlValueAccessor` integration for upload fields
- `valueMode` output shapes: `metadata`, `id`, `metadata[]`, and `id[]`
- compact shell UX for pending files, upload/cancel actions, more actions, hints, and errors
- delegation to hidden `praxis-files-upload` for real upload execution
- `uploadSuccess`, `bulkComplete`, and `error` outputs for host side effects
- accessibility for grouped field shell, pending file overlay, error live region, and disabled state

The runtime component still owns upload execution, presign/direct/bulk behavior, progress, rate-limit feedback, config persistence, and backend contract mapping.

## Form Rules

- Pick `valueMode` from the backend form contract. Do not switch from metadata to id values only to simplify host code.
- Use array modes when the form contract expects a stable array shape even for one file.
- Preserve uploaded metadata fields required by downstream forms, CRUD, audit, or document workflows.
- Keep client validation errors visible in the field shell while final file validation remains backend-owned.
- Avoid using the dynamic-fields lightweight `upload` control when the workflow needs operational upload, presign, quotas, rate-limit feedback, or persisted upload config.
- Do not duplicate upload execution in form hosts. Let the wrapper delegate to `praxis-files-upload`.

## Integration Rules

- Pass `baseUrl` and `config` through the wrapper into the runtime component.
- Keep disabled state aligned with the Angular form control, upload in-flight state, and missing `baseUrl`.
- Preserve `pendingStateChange` and proximity behavior through the wrapper when UI state matters.
- In CRUD or dynamic-form screens, keep upload field semantics in field metadata or canonical config, not in per-screen event hacks.
- Use `praxis-form-runtime-submit` when upload field values affect dynamic-form submit payloads or local/transient field rules.

## Validation

Use the smallest reliable proof:

- `pdx-files-upload-field.component.spec.ts`
- runtime component specs for delegated upload behavior
- dynamic-fields metadata discovery/catalog specs when the wrapper registration changes
- dynamic-form or CRUD focused validation when submit payload shape changes
- files-upload E2Es for manual selection, UI events, and backend contract when wrapper behavior reaches real upload

Report exact `valueMode` assumptions and all skipped gates.

## Companion Skills

- Use `praxis-files-upload-runtime` for the underlying runtime behavior.
- Use `praxis-files-upload-backend-contract` for HTTP/presign/quota/rate-limit contracts.
- Use `praxis-form-runtime-submit`, `praxis-dynamic-fields-editorial`, and `praxis-crud-runtime-openmodes` when form metadata, dynamic field catalog, submit payload, or CRUD flows are affected.
