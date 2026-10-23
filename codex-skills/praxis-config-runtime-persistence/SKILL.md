---
name: praxis-config-runtime-persistence
description: Use when Codex must implement, audit, or consume praxis-config-starter runtime configuration persistence: /api/praxis/config/ui, ui_user_config scope and environment resolution, ETag conditional requests, payload secret protection, Angular ApiConfigStorage, governed UI-layout lifecycle, exact revision identity, immutable metadata evidence, or /api/praxis/runtime/** enterprise context projections.
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
- `praxis-ui-angular/projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.ts`, its persistence spec/i18n and `docs/dynamic-page-serialized-persistence.md`
- `praxis-ui-angular/src/app/features/remote-config-storage-persistence-lab/session-tabs-consumer.component.ts` and its focused spec; inspect the current SESSION browser regression and its source-bound evidence before asserting same-SESSION switching
- focused `UserConfigControllerTest`, `UserConfigServiceTest`, `AiPrincipalContextResolverTest`, `EnterpriseRuntimeContextControllerTest`, `DefaultEnterpriseRuntimeContextProviderTest`, enterprise runtime auto-configuration tests, and Angular service specs.

## Canonical Boundary

`/api/praxis/config/ui` governs `ui_user_config`, including tenant, user, environment, scope, version, ETag, tags, payload, and secret sanitization. `X-Tenant-ID`, `X-User-ID`, `X-Env`, `X-Updated-By`, `If-Match`, and `If-None-Match` are part of the contract, not host-local conventions.

`/api/praxis/runtime/**` exposes safe enterprise runtime projections for context, tenant choices, navigation, context switches, and security/runtime events. It must not leak private entitlement internals, raw roles, policies, tokens, prompts, SQL, or private audit data.

Keep these boundaries separate: `ui_user_config` persists component runtime state; enterprise runtime endpoints project effective host context. Runtime context is not another config store, and config headers are not proof of authorization.

## Governed Layout Lifecycle

For `/api/praxis/config/ui-layouts/**`, use the existing Config lifecycle rather
than treating a draft, release or published head as ordinary `ui_user_config`.
Inspect the command/read services, frozen workspace resolver, selection verifier,
private codecs and current migration/contracts before changing the host adapter.
Follow [governed-layout-integrity.md](references/governed-layout-integrity.md)
for invocation/authority, null and numeric identity, historical reads, V68
metadata evidence, quotas and evidence-qualified validation.

For `praxis.dynamic-page.editor` and internal Form/Table children, follow the
page-specific admission procedure in that reference and the owner's P0 corpus.
Child source requests select versioned registered sources; they never attest
their own provenance. Keep the page as the sole external lifecycle target.

A source merge or a passing MockMvc fixture does not prove a published Maven
artifact, PostgreSQL persistence, a live host or browser rendering. Pin and
verify public artifacts separately; do not install a candidate under a public
coordinate to manufacture adoption.

## Scope And Resolution

- `X-Tenant-ID` is required for config requests. `X-User-ID`, `X-Env`, and `X-Updated-By` are optional according to the operation.
- `tenantId`, `componentType`, and `componentId` are trimmed and required. `X-User-ID`, `X-Env`, and `X-Updated-By` are trimmed and blank values are treated as absent.
- A blank environment targets the global environment scope (`environment IS NULL`); it must not create a separate empty-string environment.
- Identity lengths are enforced before repository or atomic-upsert paths: tenant, user, updater, and component id are limited to 255 characters; component type and environment are limited to 64 characters. Preserve deterministic `400 Bad Request` behavior for invalid identity input.
- With no `scope` query parameter, a read resolves the exact user record first when `X-User-ID` is present, then the exact tenant record. The same requested environment is used for both lookups; there is no environment-to-global fallback.
- `scope=user` performs only the exact user lookup and requires `X-User-ID`. `scope=tenant` performs only the exact tenant lookup and ignores user identity for persistence. Explicit scope disables user-to-tenant fallback.
- Writes and deletes target one exact scope. Presence of `X-User-ID` selects user scope only when `scope` is omitted; do not rely on incidental headers when ownership must be explicit.
- Use canonical selector-based `componentType` values such as `praxis-table`, `praxis-dynamic-form`, and `praxis-tabs`. Do not reintroduce V7 legacy aliases or invent host-local aliases.
- Treat `(tenant, user-or-null, componentType, componentId, environment-or-null)` as the logical identity. PostgreSQL partial unique indexes from V9 and the service conflict targets enforce the four null/non-null user/environment combinations:
  - tenant + component type + component id, when both user and environment are absent;
  - tenant + component type + component id + user, when user is present and environment is absent;
  - tenant + component type + component id + environment, when environment is present and user is absent;
  - tenant + user + component type + component id + environment, when both user and environment are present.
- `V7__migrate_ui_user_config_component_type_selectors.sql` maps legacy `table`, `form`, `tabs`, and `page` values to selector-based component types only when that does not collide with an existing selector-based row. New code must not revive the legacy values.

## Conditional Persistence

- Successful GET and PUT responses expose a quoted HTTP `ETag`; the JSON response carries the raw UUID value. Cache the response header and quote it when sending `If-Match` or `If-None-Match`.
- `If-None-Match` enables `304 Not Modified` reuse after a cached read. The canonical parser supports `*`, quoted validators, and comma-separated validators; weak validators may match reads because GET uses weak comparison.
- `If-Match` is optional. With a cached ETag, send it to prevent overwriting a newer exact-scope record. A stale or missing target returns `412 Precondition Failed`.
- `If-Match` uses strong comparison. Weak validators such as `W/"etag"` and malformed unquoted values are rejected before persistence.
- `If-Match: *` means that the exact target must already exist; it is not create-only behavior. With no `If-Match`, PUT uses the PostgreSQL atomic upsert path and is last-write-wins.
- PUT returns `200 OK` with the persisted payload and new ETag. DELETE returns `204 No Content`; it may also be conditional with the cached ETag.
- The backend increments `version` and rotates the UUID ETag on each write. Do not synthesize either value in a client.
- `UiConfigWriteAuthorizer` is the host-owned write policy hook. The starter ships a permissive compatibility default, but corporate hosts should replace it with server-principal based authorization before governed config writes are accepted.
- `UserConfigController` calls `UiConfigWriteAuthorizer` before `UserConfigService.upsert` or `delete`. A denied write must not reach persistence or secret sanitization side effects.

## Payload And Client Rules

- `AiApiKeyProtectionService.sanitizeForStorage(payload, existingPayload)` protects and merges supported secrets before persistence; `sanitizeForResponse` redacts the returned payload. Preserve both stages instead of adding UI-only redaction.
- The 256 KiB limit applies to the sanitized payload. `tags` are separate metadata, are passed to the write authorizer, and are persisted separately, but they are not secret-sanitized; never place credentials or private payload fragments in tags.
- For governed shared or cross-device state, configure Angular `ApiConfigStorage` through `ASYNC_CONFIG_STORAGE` and provide host-derived headers. Its ETag cache drives conditional reads, saves, and clears.
- `ApiConfigStorage` maps storage keys to canonical component types. In particular, `praxis:global-config*` maps to `praxis-global-config-editor`, `table-config:*` maps to `praxis-table`, and dynamic form/page prefixes map to their corresponding Praxis selectors. Prefer `componentTypeResolver` only for explicit host-owned custom keys.
- `ApiConfigStorage` sends `componentType` and `componentId` as query parameters; `componentId` remains the full storage key.
- `ApiConfigStorage` default headers are demo/local defaults (`X-Tenant-ID=demo`, stable demo `X-User-ID`, `X-Env=local`). Corporate hosts must provide real headers through the headers factory or enterprise runtime context projection.
- `LocalStorageConfigService` and the default local adapter are valid only for explicit local/offline or development state. `RemoteConfigStorage` is a synchronous compatibility bridge that returns local cache immediately and refreshes remotely; do not mistake that first local value for authoritative persisted state.
- Respect the `AsyncConfigStorage` acknowledgement contract: success emits at least one value before completion; soft failure may complete without emission; hard failure errors. Do not report a soft completion as a confirmed save.
- `ApiConfigStorage` can soft-fail noncritical keys under the default error policy. Critical keys such as `praxis:global-config*` and `table-config:*` should propagate save/clear failures. Use `errorPolicy: 'fail'` where the workflow requires a hard persistence guarantee and handle `412` as a conflict requiring reload/reconciliation, not blind retry.
- `ApiConfigStorage` treats `404` loads as missing config and must release its availability probe so later keys still load. A missing global config key must not block subsequent table or page config reads.
- Treat a scope returned by an unscoped read as cache provenance only. A user-to-tenant fallback must not add `scope=tenant` to later unscoped reads, writes, or deletes. Write ownership comes from the explicit `scope` option or the current request headers; response scope does not transition ownership.
- Reuse a cached write ETag only when its recorded scope matches the scope targeted by the current save/delete request. A tenant fallback validator must never become `If-Match` for a user override, and clearing that user override must reveal rather than delete the tenant document.
- A successful PUT and rotated ETag prove storage acknowledgement, not runtime round-trip. Reload the real consumer and verify that the acknowledged remote document wins according to its declared precedence; a host-authored input can otherwise mask a correctly persisted preference.

## Decision Rules

- Do not promote browser local storage or host-local singleton state to the canonical source for shared Praxis config.
- Preserve exact scope and environment semantics; do not invent environment fallback or merge user and tenant documents client-side.
- Preserve ETag and conditional read/write semantics. A first save can legitimately have no validator, but an edit based on a cached version should use `If-Match`.
- Preserve the host write-authorization hook. Do not treat caller-supplied capabilities, component payload flags, or frontend state as authority to mutate governed config.
- Do not put page identity, ETag policy, tenant, user, or environment inside component documents when they belong to the config boundary.
- Keep secret/API-key sanitization in `UserConfigService` and `AiApiKeyProtectionService`; do not duplicate redaction only in UI.
- In corporate mode, resolve tenant and user from the authenticated server principal. Caller headers are hints only in explicitly configured local mode; host authorization and context-switch validation remain host-owned.
- Default enterprise runtime providers fail closed with `503 RUNTIME_PROVIDER_UNAVAILABLE`; absence is not an empty or minimal ready context. Inspect each installed host provider before claiming that context, choices, tenants, navigation or security events are available.

## Enterprise Runtime Context Rules

- `EnterpriseRuntimeContextService.ready()` loads `/api/praxis/runtime/context` and stores the safe snapshot used to derive propagation headers.
- Runtime context endpoints are configurable per surface, but the default root is `/api/praxis/runtime` under the configured Praxis API root.
- `EnterpriseRuntimeContextService.headers(fallback)` removes unconfirmed contextual headers and derives them from the confirmed snapshot. Nullable or absent selection fields must not retain tenant/user/profile claims from bootstrap fallbacks.
- Context and opaque `choices()` must work before first selection using the authenticated SESSION. Tenant discovery is a separate surface; it does not select context or replace complete choices. Do not require a preselected tenant to discover authorized choices.
- `switchContext()` sends only `choiceRef` and `expectedSelectionVersion`; the host revalidates SESSION and the current exact membership tuple, performs selection CAS and returns state after commit. The consumer invalidates its prior snapshot and accepts only the current server response; stale asynchronous responses cannot reinstate a previous context.
- `EnterpriseRuntimeContextController` passes the servlet principal and normalized language/timezone/module hints to the host provider. Tenant/user/profile headers do not establish identity or selection; this transport does not resolve the selection through `AiPrincipalContextResolver`.
- Only `ready` includes effective context and `contextVersion`. A valid SESSION with no selected membership returns `selection-required`; a stored invalid selection returns `selection-invalid`. An authoritative empty directory can return an empty choices page. Source unavailability must remain an error, not an empty directory or synthetic tenant.
- A ready context does not authorize Config or business writes. Compose fresh host admission for Config scope and the existing `UiConfigWriteAuthorizer` SPI. Require the actual current membership capability for governed writes; `scope=user`, ADMIN/BASIC claims, payload flags and tags are not exemptions. Validate tenant/environment, user ownership and optional updater against the authenticated principal. Preserve ETag semantics and safe denial responses.
- Managed reference keys and public presentation are separate from grants. Do not seed production memberships merely to make context ready. Verify effective column privileges with the actual runtime role: table-level ACL summaries can miss a restricted lock column or SESSION column grants. Do not grant broad membership UPDATE or run as owner to make `FOR UPDATE` pass.
- Record the authorization boundary honestly: a committed operational admission before a separate Config transaction is not an inter-database atomic fence. Test revocation, stale context, concurrent selection CAS, publication identity and persistence in the assigned Neon branch; mocked SESSION or historical H2 evidence is not that proof.

## Captured Storage Scope And SPA Epochs

- Audit `ApiConfigStorage.captureRequest`, compatible write-validator selection,
  cache/probe identity and context-obsolescence guards before touching a host.
  Capture headers/identity at method invocation, not subscription or callback.
  Partition payload, ETag and availability probes by endpoint/type/key, explicit
  scope, effective identity headers and the canonical enterprise fingerprint/epoch.
  A key-only cache or base-URL-only probe crosses owners. Unconfigured local hosts
  retain header capture/partitioning without acquiring corporate SESSION authority.
- Explicit enterprise invalidation/tuple changes advance an epoch, clear obsolete
  cache and release owned probes. Recheck provenance at deferred subscription and
  every callback. An obsolete operation must fail without delivering a payload,
  ACK or a synthetic404/null result; A1→B→A2 must not reuse A1's response/validator.
  Finalize probes on completion/error/unsubscribe; release idempotently and remove
  only the promise still owned by that operation, never a later owner's probe.
  Adapter-injector destruction stops its context observation, rejects operations
  and releases probes. DWP drain after view destruction requires this adapter
  provider to remain alive in the parent; it is not a provider-destruction promise.
- Preserve response-scope provenance. An unscoped user read may fall back to a
  tenant document; that response must not silently promote future requests to
  `scope=tenant` or supply its ETag to a user-owned write. Explicit tenant scope
  remains explicit. Prove user-save/user-clear/tenant-fallback with each scope's
  actual validators instead of interpreting one unscoped GET as ownership proof.
- The host uses opaque choices/CAS and a fresh render owner/epoch in the same
  SESSION, with fresh canonical defaults, after confirmation. It clears the former
  state on invalidation and rejects stale callbacks. This does not change the
  component storage key/type per tenant, invent new contracts, require browser
  reload, or preserve the old document as the new tenant's defaults.
- Only emitted load results confirm readiness. Genuine404 may return absence.
  Set `API_CONFIG_STORAGE_OPTIONS.errorPolicy: 'fail'` for non404 responses such
  as503 to remain errors, as the lab does. Existing `ignore` compatibility may
  soft-fallback to `of(null)` and does not provide this503 fail-closed guarantee.
  Emitted hard errors/throw or EMPTY leave persistence disabled with the existing
  localized DWP load-failure alert. Do not turn unavailable Config into "missing"
  or let a failed read authorize a default save. Choices discovery failure is
  separate: it does not itself revoke an otherwise confirmed context.
- Keep jobs/headers scoped to their owner. Pending obsolete jobs are not retargeted;
  already-sent requests are not rolled back by destroying or switching views. A
  real commit remains a commit even if its ACK is withheld or ignored. Backend
  membership/admission and ETag remain authoritative; no cross-database fence,
  multi-tab coordination or authorization freeze is implied.

## Confidential Real-Transport SESSION Proof

Require current source/build/served-host provenance and an assigned isolated Neon
branch before claiming this behavior. Treat these as acceptance criteria, not as
passing results merely because code, documentation or a fixture exists:

1. Login through the real host, retain the browser-issued HttpOnly SESSION and
   actual CSRF flow, discover opaque choices and select through current CAS. Use
   the same SESSION/SPA for tenant changes, edit real controls and preserve the
   component key/type. No JWT/cookie seeding, fake grants or Config response mocks.
   Do not bootstrap fixed-header demo consumers beside that principal: the
   existing `user.resolvedFromServerPrincipal === true` DTO fact selects the lab's
   SESSION-only presentation, latched through null so auto-fit/color/demo-tabs
   cannot restart during selection. This is no grant, cookie/role heuristic or
   new contract/route/flag. Require the parent mount-count spec and browser
   `corporateLab` absence assertions; pending/failed E2E runs stay unapproved.
   Reuse the successful selection PUT's confirmed snapshot for transition/header
   assertions instead of issuing a redundant concurrent context GET during
   bootstrap. Keep deliberate remote Config GET/hydration proof distinct; reusing
   confirmation does not replace that persistence evidence.
2. Gate an A write before it reaches the backend, confirm B and release the exact
   real request: require host scope403. Bound every raw delay/hold handshake
   (for example `Promise.race` with a 30s deadline), clear its timer and release
   held transport in `finally` even if navigation/assertions fail. Cover A→B→A
   with the obsolete version and require context409. Inspect canonical error codes, all writes and final records;
   do not synthesize the denial or infer it from UI state.
3. Separately allow A to commit, withhold its real ACK, select B and then release
   it. Prove the recorded commit remains in A without updating B or the new A
   epoch's cache/validator/view. Hold a real GET response too and reject its late
   hydration. Distinguish before-admission denial from after-commit stale delivery.
4. Prove current loads503/EMPTY block saving with an accessible localized alert,
   whereas404 permits fresh defaults; check exact GET/PUT validators, scope
   ownership and ETag chains including legitimate hydration echoes. Require zero
   exact-key pending requests and record every request failure before teardown.
5. For confidential browser HTTP, use same-origin browser-native fetch with native
   cookies and catch transport errors inside the evaluated function, returning
   only a static failure marker. Use a real non-HTML static auxiliary resource
   to avoid bootstrapping another Angular app. Navigate with `waitUntil: 'commit'`
   and an explicit bounded timeout (for example 15s), then assert the expected
   same origin; image documents need not emit DOMContentLoaded. Do not wait for
   that event or leave auxiliary navigation unbounded. Do not use `route.fetch` or authenticated
   APIRequestContext: their reporter step can record Cookie/XSRF before an outer
   catch, even with traces off. Transport delays must forward the real request and
   release the real response, never fabricate Config/SESSION payloads or ACKs.
6. Disable credential-bearing traces/video. Export no passwords, Cookie/XSRF or
   raw opaque context versions; compare/export presence or hashes, including
   assertion failures. Prove logout of every issued SESSION and revoked-cookie401
   via an in-memory real probe with static errors and no credential logs. Preserve
   a sanitized lifecycle/result record. Historical reload evidence is not proof
   of same-SESSION switching, load/SLA, corporate SSO or every application.
7. Before a rerun after unexpected503/timeout, inspect host/transport logs and
   record canonical defaults, effective pool/minimum-idle values, warmup state,
   acquisition deadlines and the observed connection/concurrency budget for each
   datasource. Neither an undersized override nor the canonical default proves
   capacity adequate for real bootstrap/admission work: transaction locks and
   remote RTT can exhaust it. Diagnose that bottleneck first. If demand exceeds
   the default, a justified bounded capacity adjustment through existing official
   knobs, with explicit warmup and a database-wide connection budget, is allowed;
   record its values/rationale in the receipt. Do not reflexively inflate pools,
   blindly rerun, mask503, weaken authorization or extend acquisition/authentication/
   session deadlines to force a pass. Preserve those deadlines and distinguish
   capacity evidence from security correctness, load/SLA certification and bounded
   transport cleanup.

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
- For fallback ownership changes, prove tenant seed -> unscoped fallback -> user save -> conditional user read -> user clear -> tenant fallback -> explicit tenant clear. Compare the two scope-specific documents and ETags directly; a single unscoped GET cannot prove ownership isolation.
- For component preference precedence, establish the owning consumer's Apply/Save semantics first.
  Prove that preview-only Apply stays unpersisted where that is the declared contract. If accepted
  Apply persists, as in PraxisFilter field metadata editing, await its storage acknowledgement
  before the next write or reload. Settings Panel `saved$`/closure alone does not await an
  asynchronous storage subscriber. Prove Save acknowledgement, browser reload, reopen,
  stale-ETag conflict without blind retry, and preservation of unmanaged sibling fields in the
  complete document. For HTTP proof, require the real successful PUT and returned quoted ETag
  before reload, then a successful remote GET and the consumer's restored authored value.

For public persistence changes, review `README.md`, `docs/ai/**` when AI config is affected, Angular storage clients, Settings Panel global config, quickstart smokes, and HTTP examples. State explicitly when no derived artifact is affected.

## Companion Skills

- Use `praxis-config-ai-registry-manifests` when persisted config interacts with AI registry templates or executable manifests.
- Use `praxis-config-agentic-authoring-streaming` when config persistence is applied from agentic preview/apply or streamed turns.
- Use `praxis-api-quickstart-security-config` and `praxis-api-quickstart-operational-proof` for downstream host proof of config endpoint exposure, headers, origin policy, and Maven version resolution.
- Use `praxis-http-examples-contract-surfaces` when `/api/praxis/config/ui` examples, allowed Origin, tenant headers, or protected config corpus claims are affected.
- Use `praxis-ai-backend-config-contracts` for Angular AI backend client endpoint/header behavior.
- Use `praxis-settings-global-config` for Settings Panel global config UX over this backend.
