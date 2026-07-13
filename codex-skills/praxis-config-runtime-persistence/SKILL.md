---
name: praxis-config-runtime-persistence
description: Use when Codex must implement, audit, or consume praxis-config-starter runtime configuration persistence: /api/praxis/config/ui, ui_user_config scope and environment resolution, ETag conditional requests, payload secret protection, Angular ApiConfigStorage, or /api/praxis/runtime/** enterprise context projections.
---

# Praxis Config Runtime Persistence

Use this skill for the canonical persistence/runtime-context boundary of `praxis-config-starter`. This starter owns persisted runtime configuration and safe enterprise context projection; Angular hosts consume it and must not create parallel storage or context semantics.

## Source Audit

Inspect the owner before editing:

- `praxis-config-starter/AGENTS.md`
- `praxis-config-starter/README.md`
- `src/main/java/org/praxisplatform/config/controller/UserConfigController.java`
- `src/main/java/org/praxisplatform/config/service/UserConfigService.java`
- `src/main/java/org/praxisplatform/config/domain/UiUserConfig.java`
- `src/main/java/org/praxisplatform/config/dto/UserConfigResponse.java`
- `src/main/java/org/praxisplatform/config/dto/UpsertUserConfigRequest.java`
- `src/main/java/org/praxisplatform/config/http/HttpEntityTagCondition.java`
- `src/main/java/org/praxisplatform/config/service/UiConfigWriteAuthorizer.java`
- `src/main/java/org/praxisplatform/config/autoconfig/UiConfigWriteAuthorizationAutoConfiguration.java`
- `src/main/java/org/praxisplatform/config/controller/EnterpriseRuntimeContextController.java`
- `src/main/java/org/praxisplatform/config/service/AiPrincipalContextResolver.java`
- `src/main/java/org/praxisplatform/config/service/DefaultEnterpriseRuntimeContextProvider.java`
- `src/main/resources/db/migration/V5__create_ui_user_config.sql`
- `src/main/resources/db/migration/V7__migrate_ui_user_config_component_type_selectors.sql`
- `src/main/resources/db/migration/V9__dedupe_ui_user_config_null_scope_uniques.sql`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/config-storage.service.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/enterprise-runtime-context.service.ts`
- focused `UserConfigControllerTest`, `UserConfigServiceTest`, `AiPrincipalContextResolverTest`, `EnterpriseRuntimeContextControllerTest`, `DefaultEnterpriseRuntimeContextProviderTest`, enterprise runtime auto-configuration tests, and Angular service specs.

## Canonical Boundary

`/api/praxis/config/ui` governs `ui_user_config`, including tenant, user, environment, scope, version, ETag, tags, payload, and secret sanitization. `X-Tenant-ID`, `X-User-ID`, `X-Env`, `X-Updated-By`, `If-Match`, and `If-None-Match` are part of the contract, not host-local conventions.

`/api/praxis/runtime/**` exposes safe enterprise runtime projections for context, tenant choices, navigation, context switches, and security/runtime events. It must not leak private entitlement internals, raw roles, policies, tokens, prompts, SQL, or private audit data.

Keep these boundaries separate: `ui_user_config` persists component runtime state; enterprise runtime endpoints project effective host context. Runtime context is not another config store, and config headers are not proof of authorization.

## Scope And Resolution

- `X-Tenant-ID` is required for config requests. `X-User-ID`, `X-Env`, and `X-Updated-By` are optional according to the operation.
- With no `scope` query parameter, a read resolves the exact user record first when `X-User-ID` is present, then the exact tenant record. The same requested environment is used for both lookups; there is no environment-to-global fallback.
- `scope=user` performs only the exact user lookup and requires `X-User-ID`. `scope=tenant` performs only the exact tenant lookup and ignores user identity for persistence. Explicit scope disables user-to-tenant fallback.
- Writes and deletes target one exact scope. Presence of `X-User-ID` selects user scope only when `scope` is omitted; do not rely on incidental headers when ownership must be explicit.
- Use canonical selector-based `componentType` values such as `praxis-table`, `praxis-dynamic-form`, and `praxis-tabs`. Do not reintroduce V7 legacy aliases or invent host-local aliases.
- Treat `(tenant, user-or-null, componentType, componentId, environment-or-null)` as the logical identity. PostgreSQL partial unique indexes from V9 and the service conflict targets enforce the four null/non-null user/environment combinations.

## Conditional Persistence

- Successful GET and PUT responses expose a quoted HTTP `ETag`; the JSON response carries the raw UUID value. Cache the response header and quote it when sending `If-Match` or `If-None-Match`.
- `If-None-Match` enables `304 Not Modified` reuse after a cached read. The canonical parser supports `*`, quoted validators, and comma-separated validators; weak validators may match reads because GET uses weak comparison.
- `If-Match` is optional. With a cached ETag, send it to prevent overwriting a newer exact-scope record. A stale or missing target returns `412 Precondition Failed`.
- `If-Match` uses strong comparison. Weak validators such as `W/"etag"` and malformed unquoted values are rejected before persistence.
- `If-Match: *` means that the exact target must already exist; it is not create-only behavior. With no `If-Match`, PUT uses the PostgreSQL atomic upsert path and is last-write-wins.
- PUT returns `200 OK` with the persisted payload and new ETag. DELETE returns `204 No Content`; it may also be conditional with the cached ETag.
- The backend increments `version` and rotates the UUID ETag on each write. Do not synthesize either value in a client.
- `UiConfigWriteAuthorizer` is the host-owned write policy hook. The starter ships a permissive compatibility default, but corporate hosts should replace it with server-principal based authorization before governed config writes are accepted.

## Payload And Client Rules

- `AiApiKeyProtectionService.sanitizeForStorage(payload, existingPayload)` protects and merges supported secrets before persistence; `sanitizeForResponse` redacts the returned payload. Preserve both stages instead of adding UI-only redaction.
- The 256 KiB limit applies to the sanitized payload. `tags` are separate metadata and are not secret-sanitized; never place credentials or private payload fragments in tags.
- For governed shared or cross-device state, configure Angular `ApiConfigStorage` through `ASYNC_CONFIG_STORAGE` and provide host-derived headers. Its ETag cache drives conditional reads, saves, and clears.
- `LocalStorageConfigService` and the default local adapter are valid only for explicit local/offline or development state. `RemoteConfigStorage` is a synchronous compatibility bridge that returns local cache immediately and refreshes remotely; do not mistake that first local value for authoritative persisted state.
- Respect the `AsyncConfigStorage` acknowledgement contract: success emits at least one value before completion; soft failure may complete without emission; hard failure errors. Do not report a soft completion as a confirmed save.
- `ApiConfigStorage` can soft-fail noncritical keys under the default error policy. Use `errorPolicy: 'fail'` where the workflow requires a hard persistence guarantee and handle `412` as a conflict requiring reload/reconciliation, not blind retry.

## Decision Rules

- Do not promote browser local storage or host-local singleton state to the canonical source for shared Praxis config.
- Preserve exact scope and environment semantics; do not invent environment fallback or merge user and tenant documents client-side.
- Preserve ETag and conditional read/write semantics. A first save can legitimately have no validator, but an edit based on a cached version should use `If-Match`.
- Preserve the host write-authorization hook. Do not treat caller-supplied capabilities, component payload flags, or frontend state as authority to mutate governed config.
- Do not put page identity, ETag policy, tenant, user, or environment inside component documents when they belong to the config boundary.
- Keep secret/API-key sanitization in `UserConfigService` and `AiApiKeyProtectionService`; do not duplicate redaction only in UI.
- In corporate mode, resolve tenant and user from the authenticated server principal. Caller headers are hints only in explicitly configured local mode; host authorization and context-switch validation remain host-owned.
- Treat default runtime providers as safe baselines: the default context provider exposes minimal context, the default tenant provider only the active tenant, and default navigation/security-event providers empty projections. Rich corporate data requires host-owned providers, not fabricated client data.

## No Keyword Routing

Do not infer tenant, user, environment, profile, module, navigation target, or security state from labels, route text, regexes, aliases, or local fuzzy matching as the primary decision. Use headers, host providers, safe runtime projections, declared canonical refs, and governed contracts for grounding; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding headers, config fields, storage tokens, endpoint variants, context fields, or DTOs, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new public persistence/runtime contract. Name the missing data, canonical owner, consumers, docs/examples, generated artifacts, and minimum validation.

## Validation

Use focused local gates:

- config persistence: `mvn "-Dtest=UserConfigControllerTest,UserConfigServiceTest" test`
- runtime context: `mvn "-Dtest=AiPrincipalContextResolverTest,EnterpriseRuntimeContextControllerTest,EnterpriseRuntimeAutoConfigurationTest,DefaultEnterpriseRuntimeContextProviderTest" test`
- Angular consumers: `npm run test:core -- --include=projects/praxis-core/src/lib/services/config-storage.service.spec.ts --include=projects/praxis-core/src/lib/services/enterprise-runtime-context.service.spec.ts`
- broad starter smoke for shared contract changes: `mvn -B -P ci-smoke-unit -T 1C clean verify`

For public persistence changes, review `README.md`, `docs/ai/**` when AI config is affected, Angular storage clients, Settings Panel global config, quickstart smokes, and HTTP examples. State explicitly when no derived artifact is affected.

## Companion Skills

- Use `praxis-config-ai-registry-manifests` when persisted config interacts with AI registry templates or executable manifests.
- Use `praxis-config-agentic-authoring-streaming` when config persistence is applied from agentic preview/apply or streamed turns.
- Use `praxis-api-quickstart-security-config` and `praxis-api-quickstart-operational-proof` for downstream host proof of config endpoint exposure, headers, origin policy, and Maven version resolution.
- Use `praxis-http-examples-contract-surfaces` when `/api/praxis/config/ui` examples, allowed Origin, tenant headers, or protected config corpus claims are affected.
- Use `praxis-ai-backend-config-contracts` for Angular AI backend client endpoint/header behavior.
- Use `praxis-settings-global-config` for Settings Panel global config UX over this backend.
