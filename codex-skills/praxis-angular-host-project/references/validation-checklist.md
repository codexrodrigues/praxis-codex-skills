# Validation Checklist

Use this file before finishing a Praxis Angular host scaffold or integration change.

## Static Checks

- `package.json` uses a consistent Angular/Praxis UI package train, with Angular framework, Material/CDK, CLI/build, and compiler packages pinned to one exact compatible patch.
- `zone.js` is installed and listed in build polyfills when the host uses `provideZoneChangeDetection`.
- `npm ls` shows the selected `@praxisui/*` peer closure is resolved; unresolved peers are fixed by package train alignment, not by local aliases.
- `API_URL.default.baseUrl` is the single API base.
- `resourcePath` values are relative when the base URL includes `/api`.
- `resourcePath` values are base resources only; no `/filter`, `/options`, `/schemas`, item ids, or query strings.
- `PAX_FETCH_HEADERS` exists and returns tenant and locale; auth/user/env headers are included when the host requires them.
- Seven common pipes are registered for standalone host runtime usage.
- `GenericCrudService` and runtime metadata providers exist at app or route scope where remote table/form/CRUD flows need them.
- Metadata registry providers are registered only when needed for authoring/catalog/widget discovery; do not confuse them with basic data runtime requirements.
- An Angular Material theme stylesheet is loaded before validating Material/Praxis controls. `@praxisui/core/theme-bridge.css` is required for the Praxis token bridge, but it does not replace the base Material component theme CSS.
- `overlay-prebuilt.css`, Material icons/symbols, and `@praxisui/core/theme-bridge.css` or a proven equivalent theme bridge are present when overlays or Material-based controls are used. If the package does not export the CSS subpath, the style is referenced through `angular.json` with the `node_modules/...` file path.
- App-level metadata registry providers are avoided unless authoring/catalog/widget discovery is actually in scope; basic table/form/CRUD/list runtime does not require global component-catalog registration.
- Table, CRUD, and list configs are checked against published TypeScript types; avoid guessed config flags, CRUD action operation names, or list-only `queryContext` nesting that the current train does not expose.
- Dev proxy maps `/api`, `/schemas`, and `/v3/api-docs` when using relative local backend paths with Praxis metadata/OpenAPI discovery.
- Dev proxy forwards auth, tenant, and `X-Forwarded-Proto`/`X-Forwarded-Host` when the backend emits HATEOAS links that browser components may follow.
- New filter/pagination/sort/contextual constraints use `queryContext` unless the existing host is intentionally on a legacy bridge.
- No local schema/data fetcher bypasses Praxis runtime services for critical schema-driven flows.

## Build And Test Gates

For a new standalone host:

```bash
npm install
npm ls @praxisui/core @praxisui/table @praxisui/dynamic-form @praxisui/crud @praxisui/list
npm run build
npm run test:smoke
```

If no smoke script exists, run the narrowest available unit/test target and add a small smoke test when the host is intended as a reusable starter.

For Angular 21 `@angular/build:unit-test`, do not add unsupported test-target `polyfills` options. Prefer a minimal smoke test that compiles the app shell and calls `fixture.detectChanges()` before DOM assertions.

For platform validation of unpublished local Praxis UI libraries only:

```bash
npm run build:local-praxis
npm run start:local-praxis -- --host 127.0.0.1 --port 4301
```

Do not use the local-praxis flow as a consumer-external gate. For external adoption, validate from npm registry packages in a clean project or with the host's normal lockfile. Use the official documented port/origin of the host. Do not invent a new origin if the repo already defines one.

When validating package publication or a public starter inside the platform workspace, prefer existing package gates such as public install, peer validation, registry validation, or tarball validation when available.

## Network Validation

When validating against a live backend, verify at least:

- `GET /schemas/filtered` or equivalent schema requests through the runtime.
- Resource filter/data request, usually `POST <resourcePath>/filter`.
- Form load for an existing id.
- Create/edit submit path only when writes are in scope.
- Option-source or `/options/filter` requests when selects/autocomplete fields are present.
- Capabilities/actions/surfaces requests when UI exposes optional operations or row actions.

Watch for:

- duplicated `/api/api`.
- missing `/schemas` or `/v3/api-docs` proxy in local dev.
- missing `X-Tenant-ID`.
- CORS failures from non-official origins.
- CORS failures from absolute HATEOAS links pointing at the backend port instead of the frontend proxy origin.
- 400 from calling `GET /filter` when the backend expects `POST /filter`.
- schema 304 without prior cache in the current session.

## Remote Config Validation

When `providePraxisGlobalConfigBootstrap(...)` is enabled, verify:

- requests to `/api/praxis/config/ui` exist.
- `X-Tenant-ID` is sent.
- expected `X-User-ID`/`X-Env`/`X-Updated-By` policy is sent or deliberately omitted.
- first read returns expected `200/404` and later reads can use `ETag`/`304`.
- save/reload restores table/filter/form/global config as expected.
- user-scoped versus tenant-scoped behavior is documented and tested.

## Browser And Visual QA

Use browser validation when:

- the host is newly scaffolded and should be runnable.
- remote schema/data integration must be proven.
- the request includes visual/product quality, theme, responsive behavior, overlays, settings panels, or authoring UI.

Check at least:

- desktop route renders table/form/CRUD/list without blank states caused by bootstrap errors.
- narrow viewport does not clip runtime controls or overlay entrypoints.
- theme switch or host tokens do not break overlays.
- settings/editor drawers, menus, autocomplete, dialogs, and filters are not clipped when in scope.

If browser validation is skipped, state exactly what was validated instead and why.
