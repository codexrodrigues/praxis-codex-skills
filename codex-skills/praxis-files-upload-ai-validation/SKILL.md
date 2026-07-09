---
name: praxis-files-upload-ai-validation
description: Use when Codex must change, audit, or validate AI-assisted authoring for `@praxisui/files-upload`, including `PRAXIS_FILES_UPLOAD_AUTHORING_MANIFEST`, files-upload AI adapter, capabilities, context packs, endpoint and strategy operations, accepted types, limits, security policy, quota and rate-limit authoring, error-message operations, Settings Panel round-trip, component registry ingestion, docs, examples, or assistant validation for Praxis upload surfaces.
---

# Praxis Files Upload AI Validation

Use this skill for AI authoring and registry validation of `@praxisui/files-upload`. Pair it with the runtime, backend, or form-field skill for the concrete surface being changed.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-files-upload/AGENTS.md`
- `projects/praxis-files-upload/README.md`
- `projects/praxis-files-upload/src/lib/ai/praxis-files-upload-authoring-manifest.ts`
- `projects/praxis-files-upload/src/lib/ai/files-upload-ai.adapter.ts`
- `projects/praxis-files-upload/src/lib/ai/files-upload-ai-capabilities.ts`
- `projects/praxis-files-upload/src/lib/ai/files-upload-context-pack.ts`
- AI manifest and adapter specs
- config editor, widget editor, runtime component, and docs that expose the same operations
- `tools/ai-registry/**` when component docs, capabilities, context packs, or package AI assets change

## Canonical Decision Boundary

AI must operate through governed manifest operations and semantic context. It must not decide upload intent through keywords, regexes, filename text, local command strings, or arbitrary JSON patches.

Text matching may rank error codes, config paths, or target fields only after the component scope and semantic operation are resolved by the manifest, context pack, or declared tool contract.

## Manifest Rules

`PRAXIS_FILES_UPLOAD_AUTHORING_MANIFEST` governs:

- accepted types through `ui.accept`, `options.allowedExtensions`, and `options.acceptMimeTypes`
- size limits through `limits.maxFileSizeBytes` and `options.maxUploadSizeMb`
- file count and bulk size limits
- endpoint strategy through `baseUrl` and `strategy`
- security policy through strict validation, virus scanning, conflict policy, target directory, quotas, rate-limit feedback, and headers
- error message overrides under `messages.errors`
- display mode and visual UI flags

Endpoint operations are security-sensitive and require confirmation. They should preserve canonical `baseUrl`-derived paths and reject per-operation URL overrides unless the platform contract changes.

## AI Authoring Checks

Before considering the AI path complete, verify:

- The requested edit maps to an operation, target, validator, affected path, and submission impact in the manifest.
- Security-sensitive edits require confirmation and preserve the backend contract.
- Client-side and backend-facing settings stay consistent, especially accept lists and file size limits.
- Settings Panel apply/save/reset/reopen consumes the same config document that the manifest patches.
- Context packs expose safe component facts, not local prompt classifiers.
- Registry projection and docs are updated or explicitly ruled out.
- Public API exports remain owned by `@praxisui/files-upload`.

## Validation

Use the smallest reliable proof:

- `praxis-files-upload-authoring-manifest.spec.ts`
- `files-upload-ai.adapter.spec.ts`
- config editor and widget editor specs when authoring round-trip changes
- `npm run validate:authoring-contracts` when the repo-level authoring contract gate is in scope
- `npm run generate:registry:ingestion` or narrower AI registry validation when registry projection changes
- docs/playground validation when public examples or docs change

Report exactly what was validated and what remained unvalidated.

## Companion Skills

- Use `praxis-files-upload-runtime` for runtime config, states, i18n, Settings Panel, and events.
- Use `praxis-files-upload-backend-contract` for endpoint, presign, quota, rate-limit, headers, and error-code semantics.
- Use `praxis-files-upload-form-field` when AI-authored config affects form values or `valueMode`.
- Use `praxis-ai-authoring-manifests`, `praxis-ai-registry-ingestion`, `praxis-authoring-editors`, and `praxis-angular-docs-playgrounds` for their governed surfaces.
