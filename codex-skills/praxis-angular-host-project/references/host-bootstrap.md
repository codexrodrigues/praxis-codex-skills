# Host Bootstrap Reference

Use this file when creating or reviewing Angular host bootstrap for Praxis UI.

## Dependency Train

- Prefer the host's existing lockfile and Angular major.
- For a new host, resolve the current public npm train and Angular peer range before installing.
- Prefer fixed versions in starters and lockfiles. `latest` can be the active public beta train, but use it only after validating Angular peer range and full peer closure.
- External adopters consume published `@praxisui/*` packages. Local source checkout is optional.
- If docs, quickstart, and source package manifests disagree, treat that as drift. Prefer npm metadata and the published quickstart graph for external adoption.
- Pin every Angular package in the app to one exact patch after checking Material/CDK availability. Do not let `@angular/core`, `@angular/common`, `@angular/compiler-cli`, `@angular/build`, `@angular/cli`, `@angular/material`, or `@angular/cdk` float to different patches.
- Include peer-required Angular packages even when the app does not import them directly. Published Praxis UI trains may pull packages such as `@angular/platform-browser-dynamic` through secondary peer closure.
- If the host uses `provideZoneChangeDetection`, install `zone.js` and add it to build polyfills. New Angular CLI scaffolds may not include `zone.js` automatically.

The quickstart reference observed in the platform uses Angular 21 and `@praxisui/*` `9.0.0-beta.0`. Re-check current packages when building a real host because the package train is temporally unstable.

## New Host Commands

Use commands like these after resolving the version train:

```bash
npx @angular/cli@<angular-major-compatible> new <app-name> --routing --style=scss
cd <app-name>
npm install @angular/material @angular/cdk
npm install zone.js @praxisui/core@<train> @praxisui/dynamic-fields@<train> @praxisui/dynamic-form@<train> @praxisui/table@<train> @praxisui/crud@<train> @praxisui/list@<train>
```

Then resolve peer dependencies for the selected train and pin the complete closure. The current graph can require packages that are not visible in the first route templates, such as:

```bash
npm install @praxisui/ai@<train> @praxisui/dialog@<train> @praxisui/metadata-editor@<train> @praxisui/rich-content@<train> @praxisui/settings-panel@<train> @praxisui/table-rule-builder@<train> @praxisui/visual-builder@<train>
```

Add expansion route packages such as `tabs`, `stepper`, `expansion`, `charts`, `editorial-forms`, `manual-form`, or `page-builder` when those routes are used or required by peers.

Do not scaffold with local tarballs, local `dist`, or `npm link` unless the task is explicitly platform validation.

After install, run `npm ls @praxisui/core @praxisui/table @praxisui/dynamic-form @praxisui/crud @praxisui/list` and inspect unresolved peers before coding around failures.

For hosts that consume a broad Praxis UI graph, align initial bundle budgets with the reference quickstart or an explicit product budget. Angular's default production budget can fail before it reveals a real integration problem.

## Required Providers

Baseline providers for a browser-only host:

```ts
import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideEnvironmentInitializer,
  provideZoneChangeDetection,
} from '@angular/core';
import { provideHttpClient, withFetch } from '@angular/common/http';
import {
  CurrencyPipe,
  DatePipe,
  DecimalPipe,
  LowerCasePipe,
  PercentPipe,
  TitleCasePipe,
  UpperCasePipe,
} from '@angular/common';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideRouter } from '@angular/router';
import {
  API_URL,
  type ApiUrlConfig,
  GenericCrudService,
  provideGlobalConfig,
  provideGlobalConfigReady,
  provideGlobalConfigSeed,
  providePraxisLoadingDefaults,
  withPraxisHttpLoading,
} from '@praxisui/core';
import { providePraxisDynamicFieldsCore } from '@praxisui/dynamic-fields';
```

Register for remote runtime:

- `provideHttpClient(withFetch(), withPraxisHttpLoading())` or the host's canonical interceptor chain. Standalone browser hosts should prefer `withFetch()` so lazy Praxis surfaces do not depend on an `XhrFactory` provider from legacy module bootstrap.
- `...providePraxisDynamicFieldsCore()`.
- `...providePraxisLoadingDefaults()`.
- `{ provide: API_URL, useValue: { default: { baseUrl } } satisfies ApiUrlConfig }`.
- `GenericCrudService`.
- Seven common pipes: `DatePipe`, `DecimalPipe`, `CurrencyPipe`, `PercentPipe`, `UpperCasePipe`, `LowerCasePipe`, `TitleCasePipe`.
- `provideGlobalConfig(...)` for product defaults.
- `provideGlobalConfigSeed(...)` and `provideGlobalConfigReady()` only for local/static quickstart-style config, not for remote config bootstrap.
- `providePraxisLogging(...)` for enterprise/production hosts when the app needs platform diagnostics.

Metadata registry providers are a separate concern from basic data runtime and can add significant bundle weight. Register them at route or feature scope when the host uses authoring, page builder, AI registry/catalog, widget discovery, or component catalogs:

- `providePraxisDynamicFormMetadata()`
- `providePraxisTableMetadata()`
- `providePraxisCrudMetadata()`
- `providePraxisListMetadata()`
- corresponding providers for charts, editorial forms, files upload, dialog, page builder, and other routed runtimes when used

Styles for Material/Praxis components should include the base Angular Material theme before the CDK overlay CSS and Praxis theme bridge. `@praxisui/core/theme-bridge.css` maps Praxis/Material tokens for host theming, but it does not replace Angular Material's component CSS. Missing the Material theme can make `mat-form-field` inputs render with native-looking geometry, cramped values, or broken overlay/panel spacing.

Configure these styles through the Angular builder when package subpath exports block Sass imports:

```json
"styles": [
  "node_modules/@angular/material/prebuilt-themes/azure-blue.css",
  "node_modules/@angular/cdk/overlay-prebuilt.css",
  "node_modules/@praxisui/core/theme-bridge.css",
  "src/styles.scss"
]
```

Load both Material Icons and Material Symbols in `src/index.html` when the host uses `mat-icon` or Praxis `praxisIcon`; current Praxis components can render ligatures with the `material-symbols-outlined` class:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
```

## API URL And Resource Paths

Choose one source of truth:

- Browser/dev proxy: `API_URL.default.baseUrl = '/api'`.
- Published API: `API_URL.default.baseUrl = 'https://praxis-api-quickstart.onrender.com/api'`.
- Host API: `API_URL.default.baseUrl = 'https://host.example.com/api'`.

Then use relative resource paths:

```ts
const resourcePath = 'human-resources/funcionarios';
```

Do not use `/api/human-resources/funcionarios` when `API_URL` already includes `/api`.

`API_URL` and `resourcePath` are transport/runtime wiring, not semantic modeling surfaces. The host must not encode operation semantics by changing resource paths to `/filter`, `/options`, `/schemas/filtered`, item-id URLs, action URLs, or query strings. Praxis runtime services derive those operations from the base resource plus canonical metadata.

For SSR, use an absolute `API_URL.default.baseUrl`. Relative bases can produce invalid URL errors during server rendering.

For local proxy mode, proxy `/api`, `/schemas`, and `/v3/api-docs` to the backend. Data may work while schema discovery fails if `/schemas` is omitted. When forwarded headers are enabled, backend schema code may resolve OpenAPI discovery through the frontend origin; omitting `/v3/api-docs` can make `/schemas/filtered` fail even though direct backend calls work. If the backend emits absolute HATEOAS links, send forwarded headers from the dev proxy and make sure the backend honors them, otherwise browser clients can follow `http://backend-port/...` links and hit CORS even though ordinary data requests use `/api`.

Example dev proxy headers:

```json
{
  "/api": {
    "target": "http://127.0.0.1:8091",
    "changeOrigin": true,
    "headers": {
      "Authorization": "Basic <local-dev-token>",
      "X-Tenant-ID": "demo",
      "X-Tenant": "demo",
      "X-Forwarded-Proto": "http",
      "X-Forwarded-Host": "127.0.0.1:4301"
    }
  },
  "/schemas": {
    "target": "http://127.0.0.1:8091",
    "changeOrigin": true,
    "headers": {
      "Authorization": "Basic <local-dev-token>",
      "X-Tenant-ID": "demo",
      "X-Tenant": "demo",
      "X-Forwarded-Proto": "http",
      "X-Forwarded-Host": "127.0.0.1:4301"
    }
  },
  "/v3/api-docs": {
    "target": "http://127.0.0.1:8091",
    "changeOrigin": true,
    "headers": {
      "Authorization": "Basic <local-dev-token>",
      "X-Tenant-ID": "demo",
      "X-Tenant": "demo",
      "X-Forwarded-Proto": "http",
      "X-Forwarded-Host": "127.0.0.1:4301"
    }
  }
}
```

## Headers

Set `PAX_FETCH_HEADERS` for Praxis runtime fetches. Keep it server-safe if SSR is used and keep it consistent with the host interceptor.

Recommended browser shape:

```ts
provideEnvironmentInitializer(() => {
  (globalThis as any).PAX_FETCH_HEADERS = () => {
    if (typeof window === 'undefined') return {};

    const tenant = localStorage.getItem('pax.api.tenant') || 'demo';
    const token = localStorage.getItem('pax.api.token') || '';
    const headers: Record<string, string> = {
      'X-Tenant-ID': tenant,
      'X-Tenant': tenant,
      'Accept-Language': navigator.language || 'pt-BR',
    };

    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  };
});
```

Add `X-User-ID`, `X-Env`, and `X-Updated-By` when adopting remote config or audited enterprise flows.

## Route-Level Providers

Keep app-level providers minimal and add feature-specific metadata/i18n providers on routes when the runtime needs them. If a lazy Praxis route declares its own HTTP runtime providers, keep the chain aligned with bootstrap, for example `provideHttpClient(withFetch(), withPraxisHttpLoading())`.

Examples:

- Table route: `GenericCrudService`; add `providePraxisDynamicFormMetadata()` and `providePraxisTableMetadata()` when authoring, widget metadata, related forms, or catalog discovery are used.
- Form route: `GenericCrudService`; add `providePraxisDynamicFormMetadata()` for metadata registry/authoring/catalog discovery.
- CRUD route: `GenericCrudService`; add `providePraxisDynamicFormMetadata()` and `providePraxisCrudMetadata()` when authoring/catalog discovery are used.
- List route: add `providePraxisListMetadata()` when authoring/catalog discovery are used.
- Tabs/expansion routes: charts/editorial providers only when embedding those runtimes.

## Remote Config

Use remote config only when persisted customization, shared Global Config, AI provider config, or `/api/praxis/config/**` is part of the task.

Recommended stance:

- `provideGlobalConfig(...)` holds static product defaults.
- `...providePraxisGlobalConfigBootstrap(...)` activates remote storage.
- Remove quickstart-style `provideGlobalConfigSeed(...)` during remote migration.
- Decide `USER` versus `TENANT` scope explicitly.
- Backend must expose `/api/praxis/config/ui`, require `X-Tenant-ID`, support ETag/If-Match, and have the config migrations applied.
- Remote config may persist governed materializations and user/product configuration, but it does not make the Angular host the canonical author of backend metadata, AI contracts, option sources, or business rules.

Important behavior:

- If `X-User-ID` is sent and no explicit scope is supported by the current flow, writes tend to be user-scoped.
- `CONFIG_STORAGE` remote can be optimistic and may not prove persistence strongly.
- For critical authoring persistence, validate the actual network calls and reload behavior.

## Local Praxis Libs

Use local libs only for platform development. Prefer the official quickstart local-praxis flow that copies packages from `../praxis-ui-angular/dist` into `.local-praxis`, not `npm link` package-by-package.

Typical quickstart commands:

```bash
npm run build:local-praxis
npm run start:local-praxis -- --host 127.0.0.1 --port 4301
```

For normal app scaffolding, install published `@praxisui/*` packages from npm.
