---
name: praxis-api-quickstart-cockpit-http-validation
description: Use when Codex must implement, audit, or document Praxis API Quickstart HTTP evidence: the starter-bundled Praxis Cockpit, Cockpit reference inventory, verify-cockpit scripts, OpenAPI/schema/action/surface/relationship/stats/option-source contracts, build identity, domain-catalog context, domain authoring, governed domain-rule/knowledge/federation smokes, executable HTTP examples, or published-host diagnosis.
---

# Praxis API Quickstart Cockpit HTTP Validation

Use this skill to prove that Praxis contracts reach a real host over HTTP. The Cockpit, scripts, docs, and HTTP examples are executable evidence surfaces: they make published semantic behavior inspectable, but never become alternative owners of that behavior.

## Classify The Evidence Change

Classify before editing:

- `docs-apenas`: documentation or explanation that does not change a published contract or verifier assertion.
- `local-pequena`: one focused quickstart verifier/test with no public-contract change.
- `transversal`: a quickstart evidence change that also affects a starter, pilot domain, HTTP corpus, Angular/landing documentation, or published environment.
- `contrato-publico`: OpenAPI, `/schemas/**`, actions, surfaces, capabilities, option sources, HTTP headers, `ApiPaths`, public scripts, or published docs change.
- `arquitetural`: evidence reveals an ownership/lifecycle boundary between quickstart, metadata starter, config starter, or Angular runtime.

For `transversal`, `contrato-publico`, or `arquitetural`, map canonical owner, affected resource keys/paths, downstream docs/corpus, local proof, published proof, and breaking-change risk before a patch.

## Source Audit

Read the evidence producer and consumer, not only its prose:

- `praxis-api-quickstart/AGENTS.md`, `README.md`, and `pom.xml`
- `docs/COCKPIT-QUICKSTART-REFERENCE.md`
- `docs/AI-HOST-BUSINESS-GROUNDING-GUIDE.md` and `docs/LLM-DOMAIN-AUTHORING-GUIDE.md`
- `https/*.http`
- `scripts/verify-cockpit-*.sh`
- `scripts/ensure-domain-catalog-context.sh`, `scripts/verify-domain-catalog-context.sh`, and `scripts/verify-domain-catalog-authoring-runtime.sh`
- `scripts/verify-domain-rules-runtime.sh`, `scripts/verify-domain-knowledge-change-set-runtime.sh`, and `scripts/verify-domain-federation-runtime.sh`
- `PraxisCockpitStarterConsumptionIntegrationTest` and `ActuatorInfoBuildContractIntegrationTest`

Audit the affected pilot's `ApiPaths`, controller, DTO/filter, option-source registry, actions, surfaces, and focused integration test when an assertion refers to a resource contract.

## Canonical Boundary

The `praxis-metadata-starter` owns the Cockpit bundle and canonical backend discovery: `x-ui`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, capabilities, HATEOAS, OpenAPI/schema resolution, ETag, and `X-Schema-Hash`.

The `praxis-config-starter` owns domain catalog/federation, Domain Knowledge, domain rules, authoring context, lifecycle, diagnostics, publications, and materializations under `/api/praxis/config/**`.

The quickstart owns host composition, security/origin policy, concrete pilot data, the public deployment, and downstream HTTP proof. `PraxisCockpitStarterConsumptionIntegrationTest` proves that it serves Cockpit assets bundled by the starter; it must not copy or fork Cockpit HTML/assets into the host.

If evidence fails, identify the producer before changing an assertion:

| Failed evidence | Likely owner to inspect first |
| --- | --- |
| schema URL/shape, `x-ui`, headers, action/surface/capability discovery, Cockpit asset behavior | `praxis-metadata-starter` |
| persisted catalog/context, authoring, Domain Knowledge, rules, simulation, publication, materialization, timeline | `praxis-config-starter` |
| path/resource annotation, OpenAPI group, pilot data, CORS/origin/auth, deployment identity, docs/script drift | `praxis-api-quickstart` |
| rendering or consumption after the HTTP contract is correct | `praxis-ui-angular` |

Never make docs match a broken runtime, add host-local schema/action aliases, or weaken a verifier merely to get a green result.

## Evidence Lanes

Choose the narrowest lane that proves the question.

### 1. Static And Local Proof

Use shell syntax validation and focused Java integration tests while changing a verifier or host wiring. `ActuatorInfoBuildContractIntegrationTest` proves the public `/actuator/info` artifact/version contract; it is build identity evidence, not deployment success.

Use `PraxisCockpitStarterConsumptionIntegrationTest` to prove the host serves `/praxis/cockpit` from the metadata starter. It does not prove that a public Render deployment has updated.

### 2. Read-Only Cockpit Contract Proof

The `verify-cockpit-*` scripts are read-only and derive their resource inventory from each published `/v3/api-docs/{group}`. They then validate discovery and schema URLs rather than hard-coded UI assumptions:

- `verify-cockpit-inventory-doc.sh`: document counts versus OpenAPI resources and non-baseline surfaces/actions.
- `verify-cockpit-action-contracts.sh`: every discovered action has an OpenAPI method/path plus request and response filtered schemas.
- `verify-cockpit-surface-contracts.sh`: every semantic surface has complete metadata, an OpenAPI operation, and a materializable schema.
- `verify-cockpit-related-resource-contracts.sh`: `relatedResource` points at compatible parent/child resources, fields, selection keys, schemas, and child operations.
- `verify-cockpit-analytics-contracts.sh`: stats endpoints, request/response schemas, and chart surfaces agree.
- `verify-cockpit-option-source-contracts.sh`: `x-ui.optionSource` resolves to filter/by-ids endpoints and governed lookup behavior.
- `verify-cockpit-structural-ui-contracts.sh`: list, filter, create, update, and detail schemas provide a coherent structural UI contract.

Run only the verifier for the changed semantic surface during development. For a release/published cut, run relevant scripts serially against the intended host. They can make many requests; do not run the full suite concurrently or mistake `429`/transport throttling for a schema defect. Wait for recovery, rerun the affected script serially, and record the status before deciding whether there is a platform gap.

### 3. Read-Only Domain Grounding And Authoring Evidence

`verify-domain-catalog-context.sh` reads persisted releases and governed catalog items. `verify-domain-catalog-authoring-runtime.sh` reads resource-scoped context and authoring candidates, checks governed summaries and safe context hints, and only requires LLM diagnostics when its configured mode/key makes that contract applicable.

Use these before authoring a decision. They prove semantic scope, governed context, release identity, and safe projection; they do not execute business rules or grant permission to author arbitrary patches.

### 4. Mutating Governed Smokes

Treat these as controlled write workflows, not casual public-host probes:

- `ensure-domain-catalog-context.sh` may ingest `/schemas/domain` when persisted context is missing.
- `verify-domain-rules-runtime.sh` creates/transitions definitions and materializations and can publish/verify selection, validation, workflow, and approval-policy projections.
- `verify-domain-knowledge-change-set-runtime.sh` creates, validates, approves, applies, and optionally reverts governed evidence.
- `verify-domain-federation-runtime.sh` writes and activates a candidate federation release.

Before invoking a mutating script, explicitly set the documented `BACKEND_URL`, `TENANT_ID`, `ENVIRONMENT`, `ORIGIN`, and unique `SMOKE_RUN_ID` where available. Use an isolated tenant/environment; never reuse an ordinary production scope. Supply authentication only through the documented variables, and preserve script diagnostics/timeline evidence. Do not replace the lifecycle with direct database changes or write endpoints outside the governed flow.

## Build And Published Host Diagnosis

Use the canonical `/praxis/cockpit` URL. Query `/actuator/info` to identify the served artifact/version/build time, then run the focused verifier against that exact host. Cache-buster parameters such as `release`, `published`, and `qa` help request fresh browser content but are not deployment identity or proof on their own.

Diagnose in this order:

1. Confirm health and build identity through `/actuator/health` and `/actuator/info`.
2. Reproduce with one focused read-only verifier and capture its HTTP/status output.
3. Compare published OpenAPI, discovery response, filtered schema URL, headers, and resource key with the expected canonical contract.
4. Classify as host deployment/policy, docs drift, metadata starter, config starter, or consumer materialization.
5. Fix the owner, then retain or extend the quickstart verifier as downstream proof.

Respect the host's documented CORS, `Origin`, tenant/environment, authentication, CSRF, and ETag requirements. Do not invent an origin, port, bypass header, or public read/write policy for a smoke.

## HTTP Examples And Public Narrative

An HTTP example must exercise canonical paths and state its purpose, required headers/origin, tenant/environment scope, auth requirement, expected response/status, and relevant ETag or schema-hash behavior. It must not embed stale payload shapes or become a second source of truth for schemas.

When a verifier or HTTP contract changes, review the Cockpit reference, README, relevant domain/authoring guide, `praxisui-http-examples`, and landing/Angular docs that mirror the claim. Published documentation may summarize a contract, but its numbers and assertions must be derived from runtime evidence.

## No Keyword Routing

Do not choose a resource, catalog item, action, surface, option source, validation, or domain decision through labels, route fragments, aliases, regexes, or fuzzy matching as the primary decision. Use resource keys, OpenAPI operations, schema URLs, discovery contracts, capabilities, governed catalog context, decision diagnostics, and declared tools. Textual matching may only rank candidates after semantic scope is resolved.

## Adherence Inventory

Before changing docs, scripts, HTTP examples, cockpit counts, assertions, or published-host guidance, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new validation contract. State the missing behavior, canonical owner, consumers, derived artifacts, and minimum proof. A failed published probe is not automatically a contract gap: first exclude deployment lag, authentication/origin policy, environmental data, and rate limiting.

## Validation

Use the smallest reliable validation:

| Scope | Minimum proof |
| --- | --- |
| skill/script syntax | `bash -n scripts/verify-cockpit-*.sh scripts/ensure-domain-catalog-context.sh scripts/verify-domain-*.sh` |
| starter Cockpit hosting/build identity | `mvn "-Dtest=PraxisCockpitStarterConsumptionIntegrationTest,ActuatorInfoBuildContractIntegrationTest" test` |
| inventory or Cockpit docs | `scripts/verify-cockpit-inventory-doc.sh` |
| actions/surfaces/relationships/stats/options/structural UI | the corresponding single `scripts/verify-cockpit-*.sh` verifier |
| persisted domain context/authoring context | `scripts/verify-domain-catalog-context.sh` or `scripts/verify-domain-catalog-authoring-runtime.sh` against an approved scope |
| rules, knowledge, or federation lifecycle | the specific mutating script in an isolated scope; use the config-starter focused suite for canonical implementation changes |
| public release proof | focused serial verifier(s), `/actuator/info`, and the relevant published evidence only after local proof is green |

State what was not run, especially mutating or published-host checks. GitHub Actions is a release-phase gate, not the normal iteration loop.

## Companion Skills

- Use `praxis-api-quickstart-operational-proof` for host/starter ownership and dependency validation.
- Use `praxis-api-quickstart-domain-pilots` when evidence fails because pilot resource identity or behavior changed.
- Use `praxis-api-quickstart-security-config` for CORS, CSRF, Origin, read-open, rate limits, and config exposure.
- Use `praxis-metadata-schema-contracts`, `praxis-metadata-discovery-capabilities`, and `praxis-metadata-domain-option-sources` for structural/discovery/lookup contract ownership.
- Use `praxis-config-domain-decisions` for catalog, authoring, rules, knowledge, federation, publication, and materializations.
- Use `praxis-http-examples-corpus-manifest`, `praxis-http-examples-contract-surfaces`, and `praxis-http-examples-llm-smoke` for the external HTTP corpus and LLM-facing verification.
- Use `praxis-landing-public-docs-contracts`, `praxis-landing-registries-sitemap-playgrounds`, and `praxis-angular-docs-playgrounds` when public docs/playgrounds mirror quickstart evidence.
