---
name: praxis-api-quickstart-security-config
description: Use when Codex must implement, audit, or prove praxis-api-quickstart host security and exposure policy: SecurityConfig, CORS contract headers, CSRF/cookie JWT, read-open/write-disabled, schemas/actuator/runtime/config endpoint policy, trusted proxy and origin governance, rate limiting, encoded-path firewall settings, or security-focused HTTP integration tests.
---

# Praxis API Quickstart Security Config

Use this skill for host security and exposure policy in `praxis-api-quickstart`. The quickstart hosts `praxis-metadata-starter` and `praxis-config-starter` in real HTTP; it owns how their public contracts are exposed, not the contracts' business, metadata, persistence, AI, or authorization semantics.

Security here is an executable policy matrix, not a collection of `permitAll` calls. Every public route, method, header, cookie, origin, rate-limit bucket, firewall exception, and filter exemption needs a named reason and a focused proof.

Pair it with:

- `praxis-api-quickstart-operational-proof` for host-versus-starter ownership and HTTP proof.
- `praxis-config-runtime-persistence` for `ui_user_config`, ETag, runtime context, and config header semantics.
- `praxis-config-agentic-authoring-streaming` for AI authoring/SSE security under `/api/praxis/config/**`.
- `praxis-metadata-schema-contracts` for `/schemas/**`, `ETag`, `X-Schema-Hash`, and structural metadata ownership.
- `praxis-api-quickstart-cockpit-http-validation` when security changes affect official cockpit HTTP examples or browser evidence.

## Canonical Boundary

- The quickstart owns Spring Security matcher order, CORS, CSRF, cookie/session bridge, trusted proxy treatment, rate limiting, HTTP firewall policy, local/prod properties, and downstream HTTP tests.
- `praxis-config-starter` owns config persistence, AI registry/context/authoring behavior, ETag semantics, tenant/user/environment headers, and endpoint contracts under `/api/praxis/config/**`.
- `praxis-metadata-starter` owns schemas, schema hashes, `x-ui`, actions, surfaces, capabilities, and structural discovery semantics.
- Angular and other browser clients consume the headers and exposure policy; they must not invent local storage, origins, cache validators, or authorization fallbacks to compensate for a host policy defect.

If a config or schema endpoint is `permitAll` but receives `403`, inspect host origin, CORS, CSRF, firewall, and rate-limit policy first. If the HTTP contract itself is wrong, fix the appropriate starter and keep quickstart as the operational proof.

## Required Source Inventory

Read `praxis-api-quickstart/AGENTS.md`, then inspect:

- `src/main/java/com/example/praxis/apiquickstart/config/SecurityConfig.java`
- `security/ConfigOriginRestrictionFilter.java`
- `security/PublicApiRateLimitFilter.java`
- `security/CookieJwtAuthenticationFilter.java`
- `security/SpaCsrfTokenRequestHandler.java` and `CsrfCookieFilter.java`
- session/JWT services and `/auth/**` controller behavior
- `src/main/resources/application.properties`, `application-dev.properties`, and `application-prod.properties`
- `docs/security-overview.md`, `docs/security-read-open.md`, README exposure notes, and official HTTP examples
- focused SecurityConfig, CORS, config-origin, rate-limit, CSRF, config AI, and schema integration tests

Treat effective properties and executable tests as source evidence. Documentation is a required derived surface, not proof that a default or route policy is actually configured.

## Exposure Matrix Before Editing

Inventory the route with all of these columns before adding a matcher or exception:

| Surface | Owner | Method | Browser credential/CSRF mode | Origin/CORS rule | Required response headers | Rate-limit class | Default policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| static docs/Swagger | host | GET/HEAD | none | public docs policy | only intended public headers | optional public-read | explicitly public |
| actuator health/info | host | GET | none | health-check policy | no sensitive values | health policy | public only when intended |
| actuator env/configprops | host | GET | authenticated | no public exposure | sanitized diagnostics only | protected | never read-open |
| `/schemas/**` | metadata starter | GET and filtered POST | contract-specific | schemas aggregator gate | `ETag`, `X-Schema-Hash` when published | public-query | host-gated public surface |
| `/api/praxis/config/**` | config starter | contract-specific | config CSRF/origin/auth policy | explicit allowed browser/proxy policy | `ETag` and config headers | config | host-governed, not automatically open |
| `/api/praxis/runtime/**` | config starter | contract-specific | principal/context policy | explicit CORS | safe projection headers only | runtime policy | never inferred from read-open labels |
| `/api/**` resources | quickstart/metadata | method-specific | session + CSRF unless explicit public query | explicit CORS | schema/config headers where contract says so | read/query/action class | authenticated by default |

Classify the proposed change before coding: `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only a real host exposure gap belongs in quickstart security; never create a local endpoint, header alias, schema, or config persistence rule to patch a starter gap.

## Matcher And Method Rules

Spring matcher order is policy. Review the complete ordered chain, not the one matcher being changed.

- Start from deny/authenticated-by-default; document every `permitAll`, method exception, and public POST.
- `read-open` is a demonstration policy, not generic authorization. Scope it by HTTP method and canonical endpoint class; public filter/options/locate/export/stats calls need explicit data-sensitivity and rate-limit evidence.
- `write-disabled` deny rules interact with earlier exceptions. Prove which public query/config/workflow calls intentionally win and which writes remain denied.
- `schemasAggregatorEnabled` may expose only the metadata routes required for the structural contract. It does not make all metadata or actuator routes public.
- Keep `/actuator/env` and sensitive actuator diagnostics authenticated and non-exposed even when `read-open` is enabled.
- `OPTIONS` is a CORS preflight concern, not authorization evidence. Test preflight separately from the actual credentialed request.
- Do not route policy by URL labels, aliases, keyword checks, or ad hoc regexes. Use explicit Spring path patterns, methods, canonical `ApiPaths`, and property-backed policy decisions.

## CORS And Contract Headers

CORS is part of the browser-visible Praxis contract.

- Use explicit official origins whenever cookies or credentials are enabled. A wildcard origin must disable credentials.
- Do not invent ports or origins. Use the documented official local origins and deployment origins from properties.
- Allowed methods and headers must match the public API surface, including preflight for `PUT`, `PATCH`, `DELETE`, config/AI calls, and schema reads only when actually supported.
- Expose non-simple canonical response headers that browser consumers must read. This includes `ETag` for config conditional persistence and `X-Schema-Hash` or other starter-published schema validators when applicable. `Access-Control-Expose-Headers` must come from the host CORS policy; clients cannot recover an unexposed header.
- Test allowed credentialed origins, blocked origins, wildcard-without-credentials behavior, allowed methods, and exposed headers with browser-equivalent requests.

## Config Origin, Proxy, And Rate-Limit Trust

`ConfigOriginRestrictionFilter` is operational host governance for `/api/praxis/config/**`; it complements but does not replace authentication, authorization, CSRF, tenant/user/environment resolution, ETag, or server-side AI principal policy.

- `permitAll` never means ungoverned config access. Preserve an explicit allowed-origin and method policy for browser traffic.
- Prefer canonical `Origin`; use `Referer` only as a parsed origin fallback. Missing/invalid browser provenance must fail closed unless an explicit, separately authenticated service-to-service policy applies.
- Do not treat caller-controlled `Host`, `X-Forwarded-Host`, `X-Forwarded-Proto`, `Forwarded`, or `X-Forwarded-For` headers as trusted facts on a directly reachable app.
- Honor forwarded headers only behind an explicitly configured trusted-proxy boundary. Origin reconstruction and rate-limit client identity must use the same trust policy.
- A proxy normalization policy belongs to the host/deployment boundary. Do not solve it with an Angular header, a config-starter bypass, or permissive origin fallback.
- Rate limiting is abuse protection, not authorization. Use distinct buckets for login, public read, public query, bulk action, config, and any high-cost AI/SSE surface; never let a forged forwarding header create arbitrary buckets.
- Include `Retry-After`, bounded/safe error bodies, and diagnostics that do not leak secrets, tokens, or private config values.

## CSRF, Session, And Filter Chain

Cookie JWT authentication, CSRF, origin governance, and rate limiting have separate responsibilities.

- Cookie authentication establishes the Spring principal; validate cookie attributes (`Secure`, `HttpOnly`, `SameSite`, lifetime, and configured name) by environment.
- When CSRF is enabled, a SPA cookie/header flow must accept the intended raw header and retain server-rendered XOR behavior. Prove both token issuance and a protected write with matching cookie/header.
- Any CSRF ignore matcher, especially `/api/praxis/config/**`, needs an equivalent stronger host policy and a documented reason. Do not disable CSRF globally to repair a local request.
- Assert filter order and behavior: origin/rate-limit gates must run before expensive public work, authentication must populate protected endpoints correctly, and CSRF cookie exposure must not become an authorization bypass.
- Local header identity for AI is an explicitly configured development exception. Corporate mode must resolve identity server-side; caller headers are not authorization proof.

## Path Normalization And HttpFirewall

Treat URL encoding as a public security contract, not a convenience setting.

- Inventory the exact canonical config identifier/path behavior that requires encoded input before enabling encoded slash, double slash, percent, or semicolon support.
- Allow the minimum set of encodings proven necessary. A global `StrictHttpFirewall` relaxation affects docs, schemas, runtime, and business routes too.
- Current quickstart policy allows `%2F` only under `/api/praxis/config/**`, because some `praxis-config-starter` routes still receive `componentId` as `@PathVariable` and canonical refs can contain `/`. Keep schemas, actuator, docs, runtime, and business routes on strict firewall behavior.
- Do not re-enable global encoded double slash, encoded percent, or semicolon support. `%2F%2F`, `%25`, path parameters, and `%2F` outside config must remain rejected unless a new source-audited canonical contract proves otherwise.
- Prefer the query-string variants of UI config endpoints (`componentType` + `componentId`) when a client can choose identifier transport; the host exception exists to preserve existing config path-variable compatibility, not to encourage new encoded-path designs.
- Reject malformed, ambiguous, double-slash, semicolon, and path-parameter variants unless an explicitly documented canonical route requires them.
- If the firewall cannot scope an exception safely, redesign identifier transport at the canonical config boundary rather than leaving a broad host bypass.
- Verify allowed canonical config identifiers and adversarial normalized paths in focused firewall/security tests.

## Documentation And Properties

Keep `application*.properties`, deployment variables, README, security docs, HTTP examples, and test profiles synchronized.

- Do not document a non-empty read-open whitelist as a default when the effective property default is empty.
- Distinguish base, dev, and prod defaults for CSRF, read-open, cookie security, CORS, config origin restriction, schemas aggregator, rate limits, and AI local identity.
- Mark demo-only exposure (`read-open`, `write-disabled`, bulk actions, local identities) as host demonstration policy, not a platform guarantee.
- Do not print secrets, JWTs, credentials, raw config payloads, or sensitive actuator values in startup logs, test fixtures, docs, or HTTP examples.

## Validation

Run the smallest security gate that proves the changed matrix.

```bash
mvn "-Dtest=SecurityConfigHttpFirewallTest,SecurityConfigActuatorPolicyTest,SecurityConfigAiPatchPolicyTest,SecurityConfigReadOpenStatsPolicyTest,SecurityConfigSpaCsrfPolicyTest,SecurityConfigCorsTest,ConfigOriginRestrictionFilterTest,PublicApiRateLimitFilterTest" test
```

For config/schema browser contract changes, add focused downstream proof:

```bash
mvn "-Dtest=AiPatchSchemaResolutionIsolatedIntegrationTest,AgenticAuthoringStreamIsolatedIntegrationTest" test
```

Add negative tests for blocked origin, forged forwarded host/proto/client IP, missing/invalid provenance, wildcard credentials, absent exposed `ETag`/`X-Schema-Hash`, protected actuator, CSRF mismatch, write-disabled precedence, excessive public/AI calls, and malformed encoded paths. Use real HTTP/browser evidence when the changed behavior is cross-origin; same-origin MockMvc alone cannot prove CORS header visibility.

Review public docs, properties, quickstart HTTP examples, config/metadata downstream consumers, and any related starter smoke after a public exposure change. State exactly which owner was changed and why the remaining derived artifacts were unaffected.
