---
name: praxis-http-examples-contract-surfaces
description: Use when Codex must work on praxisui-http-examples contract request surfaces: metadata examples for /schemas/filtered, /schemas/catalog, /schemas/surfaces, /schemas/actions, /capabilities, _links, ETag and schema headers; config examples for /api/praxis/config/**, ui config, AI context, AI registry, domain rules, domain knowledge, authoring/patch/SSE, Origin and tenant headers.
---

# Praxis HTTP Examples Contract Surfaces

Use this skill for HTTP examples that exercise Praxis metadata, config, and quickstart contracts. Examples must explain and execute canonical contracts; they must not redefine them.

## Source Audit

Inspect the owner before editing:

- `praxisui-http-examples/README.md`
- `http/metadata/**`
- `http/config/**`
- `http/resources/**`
- `http/views/**`
- `http/operations/**`
- `payloads/config/**`
- `payloads/resources/**`
- `payloads/views/**`
- `examples.manifest.json`
- `LLM_BOOTSTRAP.md`
- `LLM_SURFACE.md`
- `ENTITY_LOOKUP_PUBLICATION_RUNBOOK.md` when an example covers `RESOURCE_ENTITY`, provider-backed option sources, `dependencyFilterMap`, or governed option-source materialization

## Canonical Boundary

Metadata examples derive from `praxis-metadata-starter` and the quickstart published host: `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, item capabilities, `_links`, `ETag`, `If-None-Match`, `X-Schema-Hash`, option sources, stats, and resource endpoints.

Config examples derive from `praxis-config-starter` hosted by quickstart: `/api/praxis/config/ui`, `ai-context`, `ai-registry`, `domain-rules`, `domain-knowledge`, authoring/patch/SSE, tenant headers, and allowed `Origin`.

## Decision Rules

- Public metadata examples should stay header-light unless debugging requires tenant context.
- Auth-light examples may use `X-Tenant-ID`, `X-Env`, and `X-User-ID` for deterministic scoped behavior.
- Protected config examples must preserve allowed `Origin` and tenant/environment headers.
- Destructive/protected writes should not be promoted into default LLM operational examples.
- Do not infer persistence, AI, schema, option-source, or domain-rule contracts from illustrative-only/legacy examples.
- When a contract changes, update request file, payload, manifest, LLM surface, and source-of-truth links together.
- For option-source examples, separate LLM-safe operational evidence from canonical runtime proof. An HTTP example may demonstrate a published lookup route, mapped dependency payload, by-ids rehydration, or governed materialization readback, but it must point back to the canonical metadata/config owner and quickstart focused tests for descriptor semantics, selection policy, invalid-value handling, ordering guarantees, and provider SPI behavior.
- Do not promote an option-source example into `llmOperational` only because it succeeds once against the published backend. It must be read-only or auth-light, have stable headers, use a deterministic payload, avoid ordinary production scopes, and explain whether it is discovery/reachability, runtime lookup proof, or governed materialization evidence.
- For `dependencyFilterMap`, examples should show the backend filter payload accepted by the endpoint and link it to the schema-published mapping. Do not teach Angular, Ergon, or LLM consumers to invent local field translations when the backend descriptor is the source of truth.

## No Keyword Routing

Do not decide endpoint class, header requirements, source owner, or safety level by filename words, labels, aliases, regexes, or local fuzzy matching as the primary decision. Use manifest flags, HTTP method, route contract, source-of-truth links, protected/public classification, and canonical starter/quickstart evidence.

## Aderence Inventory

Before adding metadata/config examples, headers, payloads, response-shape hints, protected flags, or source links, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real example coverage gaps justify corpus additions. Backend contract gaps belong to the canonical owner.

## Validation

Use focused local gates:

- manifest and generated surface: `npm run verify:manifest`
- public metadata examples: `npm run smoke:public`
- protected/auth-light examples: `npm run smoke:auth` or the narrower relevant smoke
- LLM operational surface examples: `npm run smoke:llm-surface`
- generated LLM/bootstrap promises: `npm run smoke:corpus-promises` and `npm run smoke:bootstrap-minimums`
- domain-rule proof: `npm run smoke:domain-rules-publication`

State whether validation hit the published backend or only structural checks.

## Companion Skills

- Use `praxis-http-examples-corpus-manifest` for manifest flags and corpus integrity.
- Use `praxis-http-examples-llm-smoke` for LLM-safe lanes and smoke selection.
- Use `praxis-api-quickstart-security-config` for Origin/config exposure behavior.
- Use `praxis-metadata-*` and `praxis-config-*` skills for canonical contract changes.
