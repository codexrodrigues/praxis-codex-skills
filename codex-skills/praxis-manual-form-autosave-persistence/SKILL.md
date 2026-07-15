---
name: praxis-manual-form-autosave-persistence
description: Use when implementing or auditing `@praxisui/manual-form` autosave, draft persistence, `ManualFormInstance.saveDraft()`, `resetToSeed()`, storage key composition, `ManualFormPersistenceOptions`, `ASYNC_CONFIG_STORAGE`, SSR-safe storage, debounce, or persisted config/value reload.
---

# Praxis Manual Form Autosave Persistence

Use this skill when a manual form must persist user draft value and runtime config without host-owned storage duplication. Autosave is part of `ManualFormInstance`, not a host convenience layer.

## Source Audit

Inspect before editing:

- `projects/praxis-manual-form/AGENTS.md`
- `projects/praxis-manual-form/README.md`
- `projects/praxis-manual-form/src/lib/components/manual-form/manual-form.component.ts`
- `projects/praxis-manual-form/src/lib/stores/manual-form-instance.ts`
- `projects/praxis-manual-form/src/lib/models/manual-form.types.ts`
- `projects/praxis-manual-form/src/lib/seeds/manual-form.seed.ts`
- `projects/praxis-manual-form/src/lib/tokens/manual-form.tokens.ts` when storage tokens or providers are involved
- focused autosave, instance, and docs example specs

## Canonical Boundary

`ManualFormInstance.saveDraft()` owns draft payload persistence through the injected `ASYNC_CONFIG_STORAGE` contract from `@praxisui/core`.

Persist this shape through the instance:

- current `FormConfig`
- current or supplied raw form value
- saved metadata such as timestamp, profile, namespace
- seed version when available

Do not create a second host draft store for the same form. If a host needs remote persistence, provide an `AsyncConfigStorage` implementation or route through the platform config boundary; do not write local `localStorage` calls inside manual-form consumers.

## Storage Key Rules

- Prefer a stable `formId` for production flows.
- Use `ManualFormPersistenceOptions.storageKey` only for an intentional override.
- Otherwise compose keys from `manual-form`, `namespace`, `tenantId`, `profileId`, and `formId`.
- Treat `componentInstanceId` as a host/runtime identity input that may intentionally override the persistence key at the component boundary. It scopes equivalent repeated instances, but it is not a replacement for the canonical `formId` in the seed or runtime model.
- Keep storage browser/server safe. Do not assume `window`, `document`, or `localStorage` under SSR.
- Loading persisted config should call `replaceConfig()` and loading persisted value should patch the instance form with `emitEvent: false`. Do not replay saved values through normal value-change handlers, because reload must restore a snapshot without immediately triggering a new autosave cycle.

## Autosave Rules

- `enableAutoSave=true` should call `saveDraft()` after value changes using `autoSaveDebounceMs`.
- Manual save flows may call `saveDraft(value)` directly.
- Metadata bridge patches should save draft after successful patch application when storage exists.
- `resetToSeed()` restores the seed config; coordinate reset with the adopted host form when one exists.
- Missing storage is valid for local-only forms; it should be a no-op, not a runtime failure.
- Do not persist invalid arbitrary JSON patches. Persist the instance's current canonical config/value snapshot.
- Persist and reload only through `ManualFormInstanceFactory.create(...)`, `ManualFormInstance.saveDraft(...)`, `replaceConfig(...)`, and the injected `ASYNC_CONFIG_STORAGE`. Avoid host code that reads the same key and mutates `currentConfig`, `FormGroup`, or projected component metadata directly.

## Inventory Before New Contract

Classify requested changes:

- `ja-suportado-so-ux`: storage works but saved state, reset, or diagnostics are not visible enough.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a host calls drafts "config" or "autosave profile" while the instance already exposes `ManualFormPersistenceOptions`.
- `suportado-parcialmente`: debounce, reload, namespace/profile scoping, or SSR-safe provider guidance is incomplete.
- `lacuna-real-de-contrato`: no existing key, option, token, payload field, or config boundary can express the required persistence semantics.

Only a real contract gap should introduce public persistence fields or tokens.

## Validation

Use focused local proof:

- instance save/load/reset: focused `ManualFormInstance` specs or a narrow new spec
- component autosave debounce: `components/manual-form/manual-form.component.spec.ts`
- storage provider changes: `ng build praxis-manual-form` and a direct consumer build when public tokens change
- docs/example changes: manual-form doc example/showcase specs

Pair with `praxis-core-runtime-contracts` when `ASYNC_CONFIG_STORAGE` or shared config storage contracts change, and with `praxis-config-starter` guidance when persistence moves to `/api/praxis/config/**`.
