---
name: praxis-core-domain-governance-runtime
description: Use when Codex must implement, audit, or consume @praxisui/core domain governance runtime services: DomainCatalogService, DomainKnowledgeService, DomainRuleService, domain catalog context packs, domain 360 discovery, governed rule intake/simulation/publication/materialization, config-starter headers, or Angular projections of AI-authored semantic decisions.
---

# Praxis Core Domain Governance Runtime

Use this skill when Angular needs to consume governed domain catalog, knowledge, or rule APIs from Praxis.

Praxis is a platform of AI-authored semantic decisions. In this boundary, `praxis-config-starter` is the canonical owner for domain catalog, domain knowledge, domain rules, simulations, publications, and materializations under `/api/praxis/config/**`. `@praxisui/core` provides the Angular runtime clients and context projections.

## Source Audit

Inspect before editing:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/src/lib/services/domain-catalog.service.ts`
- `projects/praxis-core/src/lib/services/domain-knowledge.service.ts`
- `projects/praxis-core/src/lib/services/domain-rule.service.ts`
- `projects/praxis-core/src/lib/models/domain-catalog.model.ts`
- `projects/praxis-core/src/lib/models/domain-knowledge.model.ts`
- `projects/praxis-core/src/lib/models/domain-rule.model.ts`
- `projects/praxis-core/src/lib/models/domain-knowledge-timeline.rich-content.ts`
- `projects/praxis-core/src/lib/models/domain-rule-timeline.rich-content.ts`
- `projects/praxis-core/src/lib/ai/domain-catalog-context-pack.ts`
- `projects/praxis-core/src/public-api.ts` when services, models, timelines, or context packs are exported or public consumption changes.
- focused specs for the touched service/model/context pack.

When behavior depends on backend semantics, also inspect the corresponding `praxis-config-starter` endpoint/contract instead of inferring it from the Angular caller.

Use `praxis-config-domain-decisions` for the backend owner of domain rules, domain knowledge, simulations, publications, materializations, explainability, timelines, and evidence lifecycle. Use `praxis-config-api-metadata-grounding` when Domain Catalog or Project Knowledge grounding affects authoring context.

## Canonical Boundary

- `DomainCatalogService` reads releases, items, governance context, and Domain 360 catalog projections.
- `DomainKnowledgeService` creates, validates, transitions, applies, and reads timelines for change sets.
- `DomainRuleService` handles intake, definitions, simulation, publication, materialization, and status transitions.
- These services resolve URLs and headers through `ResourceDiscoveryService` and `API_URL`; they should not hardcode host-specific origins or bypass official config headers.
- Angular may present, simulate, and materialize governed decisions; it must not become the primary source of business rules.

## Decision Rules

- Prefer authored domain decisions, rules, simulations, and materializations over frontend form rules or ad hoc config patches.
- Do not route domain intent by keyword, alias, regex, or local fuzzy matching. Resolve semantic scope through governed context, domain catalog entries, declared tools, and AI-authored contracts.
- If a needed domain tool is missing, model or create the canonical tool/contract. Do not replace the missing tool with label matching.
- Treat local textual search as candidate ranking after the resource/context/release scope is already semantic.
- Keep headers, ETag/origin behavior, service key, release key, resource key, context key, and query parameters aligned with config-starter contracts.
- Timeline rich-content helpers are visual projections over backend-provided safe events. Filter to `visibility=safe`, preserve safe summaries/metadata, and do not synthesize missing domain-rule or domain-knowledge events from prompts, DTO timestamps, frontend handoff state, smoke output, raw evidence, patch payloads, or local history. An empty timeline means no safe persisted events were published for that projection.

## Aderence Inventory

Classify every requested addition:

- `ja-suportado-so-ux`: config-starter or core client already returns the evidence, but the UI does not expose it.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: a local rule/config concept should map to domain knowledge/rule/catalog.
- `suportado-parcialmente`: API and client exist, but context packs, diagnostics, timeline, validation, or consumer proof is incomplete.
- `lacuna-real-de-contrato`: no config-starter contract, core model, or governed materialization can express the semantic decision.

Only real gaps justify new contracts. For them, identify source owner, affected consumers, derived artifacts, docs, and a minimal HTTP/client validation.

## Validation

Use focused proof:

- domain service specs for URL, headers, params, response mapping, status transitions, semantic filters, simulation, publication, materialization, timeline reads, and service/resource/release/context propagation:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/services/domain-catalog.service.spec.ts --include=projects/praxis-core/src/lib/services/domain-knowledge.service.spec.ts --include=projects/praxis-core/src/lib/services/domain-rule.service.spec.ts
```

- rich-content timeline specs when timeline evidence, safe visibility, or prompt/payload redaction changes:

```sh
npm run test:core -- --include=projects/praxis-core/src/lib/models/domain-knowledge-timeline.rich-content.spec.ts --include=projects/praxis-core/src/lib/models/domain-rule-timeline.rich-content.spec.ts
```

- context-pack/model specs when AI grounding, registry projections, catalog schema, or public model shapes change.
- `npm run build:praxis-core` when exports, public models, services, or context packs change; add a direct consumer smoke when UX, authoring, or runtime materialization changes.
- Angular HTTP mocks prove client URL/header/body mapping only. When endpoint semantics, status lifecycle, publication/materialization behavior, evidence lifecycle, diagnostics, catalog retrieval policy, or backend grounding changes, also run the focused backend gates from `praxis-config-domain-decisions` or `praxis-config-api-metadata-grounding`.

For first-step issue resolution, audit that the flow preserves service key, resource key, release key/context key, headers, semantic decision id, status/timeline evidence, and failure diagnostics.

## Companion Skills

- Use `praxis-core-runtime-contracts` for shared models, API_URL, public API, and provider boundaries.
- Use `praxis-ai-backend-config-contracts` when backend config AI contracts are being changed.
- Use `praxis-config-domain-decisions` when backend domain decision semantics, diagnostics, publication, or materialization contracts are being changed.
- Use `praxis-config-agentic-authoring-streaming` when turn streams route into shared-rule or domain-knowledge authoring.
- Use `praxis-core-component-registry-contracts` when domain decisions are projected into component catalogs or authoring registries.
- Use `praxis-angular-validation-gates` for focused validation selection.
