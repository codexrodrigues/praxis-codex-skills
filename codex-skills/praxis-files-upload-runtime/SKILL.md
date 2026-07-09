---
name: praxis-files-upload-runtime
description: Use when Codex must implement, audit, document, or author `@praxisui/files-upload` runtime surfaces, including direct, presigned, or auto uploads, `filesUploadId` persistence, `baseUrl`, full or compact display modes, upload states, pending files, progress, drag proximity, client validators, quota and rate-limit feedback, i18n, Settings Panel config, docs, examples, or host integration for Praxis file upload UI.
---

# Praxis Files Upload Runtime

Use this skill for the canonical Angular upload component in `@praxisui/files-upload`. Treat it as the governed Praxis upload runtime, not as a local file input wrapper.

## Source Audit

Before editing code or guidance, inspect:

- `projects/praxis-files-upload/AGENTS.md`
- `projects/praxis-files-upload/README.md`
- `projects/praxis-files-upload/docs/host-files-upload-integration.md`
- `projects/praxis-files-upload/src/public-api.ts`
- `projects/praxis-files-upload/src/lib/components/files-upload/praxis-files-upload.component.ts`
- `projects/praxis-files-upload/src/lib/types/**`
- `projects/praxis-files-upload/src/lib/models/index.ts`
- `projects/praxis-files-upload/src/lib/validators/file-upload.validators.ts`
- `projects/praxis-files-upload/src/lib/config/**`
- focused unit specs and `test-dev/e2e/*.playwright.spec.ts` when backend, rate-limit, conflict, drag proximity, or UI events change

If `praxis-file-management` source is available, audit its AGENTS and backend upload contract too. If it is not checked out locally, state that and rely on the files-upload docs/services/specs as the local contract evidence.

## Canonical Boundary

`@praxisui/files-upload` owns:

- runtime upload strategies `direct`, `presign`, and `auto`
- `filesUploadId`, `componentInstanceId`, and `ASYNC_CONFIG_STORAGE` persistence
- `baseUrl` consumption for canonical files API paths
- UI state for selected/pending files, progress, errors, readiness, drag proximity, full/compact modes, and result actions
- client validators for accepted types, max file size, max files per bulk, and max bulk size
- config separation into `ui`, `limits`, `options`, `bulk`, `quotas`, `rateLimit`, `headers`, and `messages`
- i18n through `providePraxisFilesUploadI18n`
- Settings Panel config editor and widget config editor

The host owns API origin, auth, tenant/user headers, storage policy, authorization, final file lifecycle, and product decisions about whether runtime customization is allowed.

## Runtime Rules

- Require `baseUrl` for real uploads. Do not hide a missing base URL with a no-op upload path.
- Use stable `filesUploadId` for persisted or customizable surfaces. Add `componentInstanceId` when the same upload appears multiple times on a route.
- Use `strategy='auto'` only when trying presign first and falling back to direct is an intentional product behavior.
- Preserve canonical endpoints through the client: direct uses `baseUrl/upload`, bulk uses `baseUrl/bulk`, and presign discovery uses `baseUrl/upload/presign?filename=...`.
- Keep visual choices in `config.ui`; keep client guards in `config.limits`; keep backend-facing upload options in `config.options`; keep execution policy in `config.bulk`.
- Keep quota and rate-limit fields as user feedback policy. Backend quota/rate enforcement remains a backend contract.
- Emit lifecycle events instead of adding host-local polling: `uploadStart`, `uploadProgress`, `uploadSuccess`, `bulkComplete`, `error`, `rateLimited`, `readinessChange`, `pendingStateChange`, and `proximityChange`.
- Preserve accessibility state such as `aria-busy`, error live regions, progress labels, and focusable pending-file controls.

## Authoring Rules

- Use `PraxisFilesUploadConfigEditor`, `PraxisFilesUploadWidgetConfigEditor`, `ConfigService`, and `useEffectiveUploadConfig` where applicable.
- Keep Settings Panel apply/save/reset/reopen aligned with runtime config consumption.
- Keep authoring text and user-facing messages on the i18n path or explicit host-provided `messages.errors` overrides.
- Do not create host-local config aliases for strategy, limits, headers, quota, or rate-limit behavior when `FilesUploadConfig` already has the canonical path.
- Before introducing a new field, classify the gap as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`.

## Validation

Use the smallest reliable proof:

- `npm run build:praxis-files-upload`
- focused specs for component runtime, validators, config service, config editor, widget editor, error mapper, API client, and presigned uploader
- `test-dev/e2e/*.playwright.spec.ts` for backend contract, rate limit, conflict, fail-fast, manual selection, drag proximity, and UI event behavior
- docs/playground validation when public docs or examples change
- AI registry validation when manifests, capabilities, or component docs change

Report exactly what was validated and what remained unvalidated.

## Companion Skills

- Use `praxis-files-upload-backend-contract` for presign, direct/bulk endpoints, backend envelopes, quotas, rate limits, headers, and error codes.
- Use `praxis-files-upload-form-field` for `pdx-material-files-upload`, dynamic-form integration, `valueMode`, and ControlValueAccessor behavior.
- Use `praxis-files-upload-ai-validation` for authoring manifests, AI adapters, registry projection, and assistant validation.
- Use `praxis-authoring-editors`, `praxis-angular-i18n-governance`, `praxis-angular-docs-playgrounds`, `praxis-angular-public-api-governance`, and `praxis-angular-validation-gates` when the change touches those governed surfaces.
