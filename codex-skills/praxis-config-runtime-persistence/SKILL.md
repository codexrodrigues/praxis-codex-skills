---
name: praxis-config-runtime-persistence
description: Use when Codex must work on praxis-config-starter runtime configuration persistence: /api/praxis/config/ui, ui_user_config, tenant/user/environment headers, ETag, If-Match, If-None-Match, config payload sanitization, global config storage, /api/praxis/runtime/** enterprise context, tenants, navigation, and security-event projections.
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
- `src/main/java/org/praxisplatform/config/controller/EnterpriseRuntimeContextController.java`
- `src/main/java/org/praxisplatform/config/service/AiPrincipalContextResolver.java`
- `src/main/java/org/praxisplatform/config/service/DefaultEnterpriseRuntimeContextProvider.java`
- `src/main/resources/db/migration/V5__create_ui_user_config.sql`
- focused `UserConfigControllerTest`, `UserConfigServiceTest`, `EnterpriseRuntimeContextControllerTest`, and enterprise runtime auto-configuration tests.

## Canonical Boundary

`/api/praxis/config/ui` governs `ui_user_config`, including tenant, user, environment, scope, version, ETag, tags, payload, and secret sanitization. `X-Tenant-ID`, `X-User-ID`, `X-Env`, `X-Updated-By`, `If-Match`, and `If-None-Match` are part of the contract, not host-local conventions.

`/api/praxis/runtime/**` exposes safe enterprise runtime projections for context, tenant choices, navigation, context switches, and security/runtime events. It must not leak private entitlement internals, raw roles, policies, tokens, prompts, SQL, or private audit data.

## Decision Rules

- Do not store shared Praxis config in browser local storage or host-local singleton services when `/api/praxis/config/ui` is available.
- Preserve scope semantics: user config can override tenant config; tenant config must not require `X-User-ID`.
- Preserve ETag and conditional write/read semantics. A save that ignores `If-Match` can overwrite governed state.
- Do not put page identity, ETag policy, tenant, user, or environment inside component documents when they belong to the config boundary.
- Keep secret/API-key sanitization in `UserConfigService` and `AiApiKeyProtectionService`; do not duplicate redaction only in UI.
- Treat runtime context as a safe projection. Host authorization remains host-owned.

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
- runtime context: `mvn "-Dtest=EnterpriseRuntimeContextControllerTest,EnterpriseRuntimeAutoConfigurationTest,DefaultEnterpriseRuntimeContextProviderTest" test`
- broad starter smoke for shared contract changes: `mvn -B -P ci-smoke-unit -T 1C clean verify`

For public persistence changes, review `README.md`, `docs/ai/**` when AI config is affected, Angular storage clients, Settings Panel global config, quickstart smokes, and HTTP examples. State explicitly when no derived artifact is affected.

## Companion Skills

- Use `praxis-config-ai-registry-manifests` when persisted config interacts with AI registry templates or executable manifests.
- Use `praxis-config-agentic-authoring-streaming` when config persistence is applied from agentic preview/apply or streamed turns.
- Use `praxis-api-quickstart-security-config` and `praxis-api-quickstart-operational-proof` for downstream host proof of config endpoint exposure, headers, origin policy, and Maven version resolution.
- Use `praxis-ai-backend-config-contracts` for Angular AI backend client endpoint/header behavior.
- Use `praxis-settings-global-config` for Settings Panel global config UX over this backend.
