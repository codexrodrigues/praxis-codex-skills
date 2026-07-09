---
name: praxis-files-upload-backend-contract
description: Use when Codex must audit, implement, document, or validate Praxis file upload backend integration for `@praxisui/files-upload`, including `praxis-file-management`, direct upload, bulk upload, presign contracts, `baseUrl` path derivation, multipart fields, backend envelopes, quotas, rate limits, tenant or user headers, conflict policy, strict validation, virus scanning, error codes, ETag-backed effective config, or host/backend contract tests.
---

# Praxis Files Upload Backend Contract

Use this skill for the boundary between `@praxisui/files-upload` and the backend files API. Treat backend upload behavior as a platform contract, not as a visual adaptation inside a host screen.

## Source Audit

Audit local Angular contract evidence first:

- `projects/praxis-files-upload/AGENTS.md`
- `projects/praxis-files-upload/README.md`
- `projects/praxis-files-upload/docs/host-files-upload-integration.md`
- `projects/praxis-files-upload/src/lib/services/files-api-client.service.ts`
- `projects/praxis-files-upload/src/lib/services/presigned-uploader.service.ts`
- `projects/praxis-files-upload/src/lib/services/error-mapper.service.ts`
- `projects/praxis-files-upload/src/lib/config/config.service.ts`
- `projects/praxis-files-upload/src/lib/types/Api.ts`
- `projects/praxis-files-upload/src/lib/types/Upload.ts`
- `projects/praxis-files-upload/src/lib/types/Errors.ts`
- matching service specs and backend-contract Playwright specs

When the backend repository is available, audit `praxis-file-management/AGENTS.md`, API controllers, DTOs, security filters, quota/rate-limit logic, presign implementation, and tests. If that repo is absent, explicitly state that the backend source was not locally available.

## Canonical Backend Shape

The files API base is `baseUrl`. The runtime derives paths:

- `POST {baseUrl}/upload` for direct single upload
- `POST {baseUrl}/bulk` for bulk upload
- `POST {baseUrl}/upload/presign?filename=...` for presign discovery

Do not add arbitrary per-operation URL fields unless the owning contract intentionally changes. Endpoint authoring should change `baseUrl` and `strategy`, not create local URL aliases.

## Request Rules

- Direct upload sends multipart `file` plus optional `options`, `metadata`, and `conflictPolicy`.
- Bulk upload sends repeated multipart `files`, optional `options`, optional `failFastMode`, and JSON arrays for `metadata` and `conflictPolicy` when present.
- Presign discovery returns `uploadUrl`, optional `headers`, and optional `fields`.
- `PresignedUploaderService` posts to the presigned target with `withCredentials=false`.
- Praxis-specific fields are appended to the presigned target only for same-origin or relative upload URLs. Do not leak Praxis metadata fields to arbitrary cross-origin storage targets.

## Response And Error Rules

- Successful single upload maps backend `UploadResponseData` into `FileMetadata`.
- Bulk upload returns `BulkUploadResponseData` with per-file result status, file metadata, and item errors.
- Error handling should use canonical error envelopes and `ApiErrorItem` through `ErrorMapperService`.
- Rate-limit detection uses backend error codes such as `LIMITE_TAXA_EXCEDIDO`, `RATE_LIMIT_EXCEEDED`, or `SYS_RATE_LIMIT`, plus headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset`.
- Quota, security, virus scanning, conflict policy, and storage failures must remain backend decisions surfaced through structured errors, not hidden by host-local success assumptions.

## Effective Config Rules

- Backend effective config may publish `options`, `bulk`, `rateLimit`, `quotas`, `messages`, and `metadata`.
- `ConfigService` and `useEffectiveUploadConfig` are the Angular entry points for effective config loading and ETag-aware caching.
- Host headers such as tenant/user should be symmetric with the backend policy. Do not invent local header names when the config or host platform already declares them.

## Validation

Use the narrowest proof for the contract touched:

- `files-api-client.service.spec.ts`
- `presigned-uploader.service.spec.ts`
- `error-mapper.service.spec.ts`
- `config.service.spec.ts`
- `files-upload-backend-contract.playwright.spec.ts`
- rate-limit, conflict, too-large, fail-fast, and single-error E2Es when behavior crosses HTTP/runtime boundaries
- backend tests in `praxis-file-management` when that repo is available

Report backend source availability and all skipped gates.
