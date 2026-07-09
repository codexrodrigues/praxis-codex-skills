# Validation Matrix

## Opening/Wiring Changed

Prefer:
- `openConfigEditor` specs
- bridge/panel wiring specs
- focused component specs for the owning config editor or builder

## Payload Contract Changed

Prefer:
- `SettingsValueProvider` specs
- apply/save payload specs
- consumer editor specs that prove `getSettingsValue()` matches the runtime contract

## Round-Trip Changed

Prefer:
- focused editor integration specs
- runtime + editor same-flow specs
- metadata renderer / schema normalization specs when metadata authoring is involved

## UI Visibility/Behavior Changed

Prefer:
- focused editor specs
- Playwright authoring flows only when visual behavior is material

Typical owner mapping:

- `dynamic-form`: config/layout/messages/rules/hooks/actions/json editor specs, then e2e
- `table`: columns/behavior/toolbar/rules/json editor specs, then e2e
- `list`: list-config/json specs, then e2e or doc-page evidence
- `page-builder`: page-config/dynamic-page/widget-shell/connection specs
- `metadata-editor`: renderer, coverage, cascade, schema normalization specs
- `settings-panel`: component/service/provider specs
- `charts`, `manual-form`, `tabs`, `stepper`: the lib's config editor or quick-setup specs

## Reset/Persistence Changed

Prefer:
- focused reset/save/reopen specs
- storage/config-remote integration only when relevant

## Rules

- Do not rely on build-only validation for authoring changes.
- Do not use Playwright by reflex when focused specs prove the contract.
- If validation is partial, say exactly what was and was not validated.
- If runtime and editor are correct but governed docs or `public-api` are stale, record that as sync debt and fix it in the owning lib instead of masking it as a validation pass.
