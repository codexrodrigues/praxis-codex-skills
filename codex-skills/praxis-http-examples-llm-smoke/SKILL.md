---
name: praxis-http-examples-llm-smoke
description: Use when Codex must work on praxisui-http-examples LLM-facing operational surface and smokes: LLM_SURFACE.md, LLM_BOOTSTRAP.md, llm_bootstrap.json, LLM_COMMON_QUESTIONS.md, smoke:llm-surface, smoke:public, smoke:auth, smoke:corpus-promises, smoke:bootstrap-minimums, smoke:domain-rules-publication, safe-first lanes, protected contracts, published backend proof, and CI baseline.
---

# Praxis HTTP Examples LLM Smoke

Use this skill for the LLM-facing operational surface and smoke validation in `praxisui-http-examples`. The LLM surface is a safe-first curated runtime lane, not the whole platform contract.

## Source Audit

Inspect the owner before editing:

- `LLM_BOOTSTRAP.md`
- `llm_bootstrap.json`
- `LLM_COMMON_QUESTIONS.md`
- `LLM_SURFACE.md`
- `OPENAPI_COVERAGE.md`
- `smoke/generate-llm-surface.mjs`
- `smoke/smoke-llm-surface.mjs`
- `smoke/smoke-public-examples.mjs`
- `smoke/smoke-auth-examples.mjs`
- `smoke/smoke-corpus-promises.mjs`
- `smoke/smoke-bootstrap-minimums.mjs`
- `smoke/smoke-domain-rules-publication.mjs`
- `.github/workflows/http-examples-ci.yml`
- `examples.manifest.json`
- `ENTITY_LOOKUP_PUBLICATION_RUNBOOK.md` when promoting entity lookup, provider-backed option-source, `dependencyFilterMap`, or governed materialization examples into the LLM surface

## Canonical Boundary

`LLM_SURFACE.md` is generated from `examples.manifest.json`. It should contain only examples useful for LLM-driven discovery and currently operational against the published backend.

Safe-first order is: health/OpenAPI/catalog/filtered schemas, then auth-light options/views/filters/stats, then read-only governed decision proof, then protected contract reading when explicitly needed.

`smoke:llm-surface` executes every `llmOperational` example against the published backend. Passing it proves the selected HTTP examples are reachable with their documented headers and payloads; it does not prove every canonical runtime semantic behind the endpoint. For option sources, use the LLM smoke as operational evidence only after the canonical descriptor, dependency mapping, by-ids ordering, selected reload, invalid-selection policy, provider SPI, or governed materialization semantics have been proven by quickstart/starter tests or runbooks.

## Decision Rules

- Do not put protected writes, destructive examples, unstable examples, or reference-only examples into the default LLM lane.
- Keep `LLM_SURFACE.md` generated, not hand-edited.
- Keep `llm_bootstrap.json` and `LLM_BOOTSTRAP.md` aligned with accepted-now and recommended-stable header lanes.
- When smoke fails, classify whether runtime, corpus claim, published backend, or canonical contract is wrong before editing examples.
- CI baseline currently emphasizes `verify:manifest`, `smoke:llm-surface`, `smoke:corpus-promises`, and `smoke:bootstrap-minimums`.
- Promote option-source examples to `llmOperational` only when they are read-only or auth-light, deterministic, safe for repeated execution, and explicitly classified as discovery/reachability, runtime lookup evidence, or governed materialization readback. Do not let one successful published request imply that LLM consumers may invent local `dependencyFilterMap`, rehydration, invalid-selection, or materialization behavior.
- If an example demonstrates `dependencyFilterMap`, the LLM-facing docs should show the backend payload accepted by the endpoint and point to the filtered schema/manifest/runbook evidence. The smoke should confirm the request is usable; the schema/starter/quickstart evidence remains the authority for the mapping.

## No Keyword Routing

Do not decide LLM-operational status, safe lane, header minimums, or smoke inclusion by filename labels, route words, aliases, regexes, or fuzzy matching as the primary decision. Use manifest flags, smoke outcomes, endpoint class, protected/public status, destructive status, and published-backend evidence.

## Aderence Inventory

Before changing LLM docs, bootstrap JSON, smoke whitelist, CI commands, or operational flags, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real LLM surface gaps justify changes. Contract/runtime gaps belong to quickstart or the starters.

## Validation

Use focused local gates:

- generated docs and manifest: `npm run verify:manifest`
- LLM runtime lane: `npm run smoke:llm-surface`
- bootstrap minimums: `npm run smoke:bootstrap-minimums`
- promise consistency: `npm run smoke:corpus-promises`
- option-source LLM promotion: `npm run smoke:llm-surface`, `npm run smoke:corpus-promises`, `npm run smoke:bootstrap-minimums`, plus the focused quickstart/starter proof named by the relevant option-source skill
- domain-rule published proof: `npm run smoke:domain-rules-publication`

If network or published backend access is not used, state that only structural generation/manifest checks were run.

## Companion Skills

- Use `praxis-http-examples-corpus-manifest` for manifest layer/flag changes.
- Use `praxis-http-examples-contract-surfaces` for request/payload/header semantics.
- Use `praxis-api-quickstart-cockpit-http-validation` for reference-host evidence and cockpit docs.
- Use `praxis-landing-public-docs-contracts` when public docs claim platform meaning from the LLM surface.
- Use `praxis-landing-registries-sitemap-playgrounds` when landing `llms.txt`, `llms-full.txt`, `llm-index.json`, sitemap, examples, or playgrounds mirror the LLM surface.
- Use `praxis-angular-docs-playgrounds` when Angular component docs/playgrounds mirror the LLM surface.
