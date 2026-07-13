---
name: praxis-http-examples-corpus-manifest
description: Use when Codex must work on praxisui-http-examples corpus governance: examples.manifest.json, EXAMPLE_STATUS.md, http/**, payloads/**, responseShapeHint, llmOperational, protectedContract, referenceOnly, runtimeRecordConfirmed, selectorConfirmed, publishedBackendConfirmed, knownPublishedFailure, sourceOfTruth, manifest validation, and derived example classification.
---

# Praxis HTTP Examples Corpus Manifest

Use this skill for the executable HTTP examples corpus. `praxisui-http-examples` is a derived operational surface, not a canonical contract source.

## Source Audit

Inspect the owner before editing:

- `praxisui-http-examples/README.md`
- `examples.manifest.json`
- `EXAMPLE_STATUS.md`
- `http/**`
- `payloads/**`
- `smoke/verify-manifest.mjs`
- `smoke/shared-http-example-parser.mjs`
- `package.json`
- `.github/workflows/http-examples-ci.yml`
- `ENTITY_LOOKUP_PUBLICATION_RUNBOOK.md` when changing lookup, provider-backed option-source, `dependencyFilterMap`, or governed materialization flags

## Canonical Boundary

The manifest indexes examples and their runtime claims. `llmOperational`, `protectedContract`, and `referenceOnly` are mutually exclusive surface layers. Flags such as `runtimeRecordConfirmed`, `selectorConfirmed`, `publishedBackendConfirmed`, and `knownPublishedFailure` are evidence claims, not backend truth.

When an example diverges from the backend or starter contract, the canonical owner wins: `praxis-metadata-starter`, `praxis-config-starter`, or `praxis-api-quickstart`.

For option-source examples, the manifest describes the corpus lane, not the full semantic contract. `publishedBackendConfirmed=true` means the committed HTTP example currently works on the published quickstart; it does not prove descriptor ownership, dependency mapping authority, by-ids ordering, selected reload, invalid-selection policy, provider SPI behavior, or governed materialization semantics. Those must be referenced through `sourceOfTruth`, runbooks, and focused quickstart/starter evidence.

## Decision Rules

- Do not update examples to institutionalize a backend/starter bug.
- Every `http/**` and `payloads/**` file should be referenced by `examples.manifest.json`.
- Keep `authRequired` aligned with `sessionAuthRequired || tenantScopedHeadersRequired`.
- Treat `protectedContract` as contract-reading, not default operational LLM surface.
- Treat `referenceOnly` as caveat/troubleshooting/legacy/illustrative, not recommended default.
- When changing an example, update manifest flags, `sourceOfTruth`, payload references, and generated LLM surface if relevant.
- Promote a lookup or option-source example to `llmOperational` only when it is read-only/auth-light, deterministic, safe for repeated execution, published-backend confirmed, and backed by canonical `sourceOfTruth` entries for the descriptor/provider/pilot behavior it claims.
- Keep provider-backed examples `referenceOnly` or `protectedContract` until the published backend confirms the exact committed request and the example does not teach consumers to infer `RESOURCE_ENTITY` semantics from lightweight `OptionDTO{id,label}` behavior.
- For `dependencyFilterMap`, require the committed payload to show the backend filter fields accepted by the endpoint and require `sourceOfTruth` to include the schema/DTO/service/descriptor evidence that owns the mapping. Do not encode local consumer translations as manifest truth.

## No Keyword Routing

Do not classify examples by filename words, route labels, aliases, regexes, or local fuzzy matching as the primary decision. Use manifest fields, source-of-truth links, endpoint class, HTTP method, required headers, runtime confirmation flags, and canonical owner evidence.

## Aderence Inventory

Before adding examples, payloads, flags, status labels, or manifest fields, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real corpus gaps justify new examples/manifest claims. Contract gaps belong to the canonical starter or quickstart.

## Validation

Use focused local gates:

- manifest/corpus: `npm run verify:manifest`
- LLM surface affected: `npm run generate:llm-surface` then `npm run verify:manifest`
- OpenAPI coverage affected: `npm run generate:openapi-coverage`
- LLM or lookup flag promotion: `npm run verify:manifest`, `npm run smoke:llm-surface`, `npm run smoke:corpus-promises`, and `npm run smoke:bootstrap-minimums`, plus focused quickstart/starter proof when the claim includes option-source semantics

When network/published backend behavior matters, run the narrow smoke for the changed surface and state if it was skipped.

## Companion Skills

- Use `praxis-http-examples-contract-surfaces` for metadata/config HTTP request semantics.
- Use `praxis-http-examples-llm-smoke` for LLM surface and smoke commands.
- Use `praxis-api-quickstart-operational-proof` when a runtime example fails against the reference host.
- Use `praxis-metadata-*` and `praxis-config-*` skills when source-of-truth changes belong to starters.
