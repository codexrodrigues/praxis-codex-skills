---
name: praxis-config-domain-decisions
description: Use when Codex must work on praxis-config-starter governed semantic decisions: /api/praxis/config/domain-rules/**, /api/praxis/config/domain-knowledge/**, domain catalog/federation, DomainRuleService, DomainKnowledgeChangeSetService, intake, simulation, publication, materialization, decisionDiagnostics, explainability, approval policy, timelines, evidence lifecycle, Project Knowledge derived indexes, and runtime surfaces as derived projections.
---

# Praxis Config Domain Decisions

Use this skill for governed domain decisions in `praxis-config-starter`. Domain rules, domain knowledge, publications, and materializations are canonical semantic decisions; forms, tables, option sources, actions, UI rules, and runtime artifacts are derived projections.

## Source Audit

Inspect the owner before editing:

- `praxis-config-starter/AGENTS.md`
- `docs/2026-04-federated-domain-catalog-rfc.md`
- `docs/domain-catalog/**`
- `docs/ai/categorical-field-semantics-v1.md`
- `docs/ai/domain-rule-timeline-v*.md`
- `src/main/java/org/praxisplatform/config/controller/DomainRuleController.java`
- `src/main/java/org/praxisplatform/config/controller/DomainKnowledgeChangeSetController.java`
- `src/main/java/org/praxisplatform/config/controller/DomainCatalogController.java`
- `src/main/java/org/praxisplatform/config/controller/DomainFederationController.java`
- `src/main/java/org/praxisplatform/config/service/DomainRuleService.java`
- `src/main/java/org/praxisplatform/config/service/DomainKnowledgeChangeSetService.java`
- `src/main/java/org/praxisplatform/config/service/DomainKnowledgeChangeSetValidator.java`
- `src/main/java/org/praxisplatform/config/domain/DomainRuleDefinition.java`
- `src/main/java/org/praxisplatform/config/domain/DomainRuleMaterialization.java`
- `src/main/java/org/praxisplatform/config/domain/DomainKnowledgeChangeSet.java`
- focused domain rule, domain knowledge, catalog, federation, timeline, and migration tests.

## Canonical Boundary

`/api/praxis/config/domain-rules/**` owns intake, definitions, status transitions, simulations, publications, materializations, timelines, explainability, and `decisionDiagnostics`.

`/api/praxis/config/domain-knowledge/change-sets/**` owns governed knowledge patch creation, validation, review, apply, timeline, evidence lifecycle, and derived Project Knowledge indexing.

Domain catalog/federation publishes semantic graph context and relationships for AI grounding. It must not be reduced to labels.

## Decision Rules

- If a request is about a shared business rule, validation, eligibility, compliance, approval, or policy over a resolved resource, route to domain decisions before component preview/apply.
- UI, option sources, backend validation, workflow actions, and approval policies should be materializations of the governed decision when possible.
- Preserve `decisionDiagnostics`, `explainability`, publication diagnostics, materialization outcomes, timeline events, statuses, source hashes, and canonical owner fields.
- Status transitions are directional; do not reactivate rejected/retired decisions or failed/superseded/reverted materializations without the canonical transition path.
- Domain Knowledge apply is separate from approval and must validate scope, validation result, lifecycle, and evidence state.
- Project Knowledge used in authoring is derived from governed active evidence, not raw prompts or stale chat history.

## No Keyword Routing

Do not decide domain rule, knowledge, approval, materialization, catalog relationship, or resource policy intent by labels, aliases, regexes, command words, or local fuzzy matching as the primary decision. Use governed LLM/tool resolution, Domain Catalog/Knowledge, semantic decisions, rule definitions, active evidence, declared tools, and canonical context; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding domain-rule fields, knowledge patch operations, materialization kinds, statuses, diagnostics, timelines, quick replies, catalog edges, or publication behavior, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real gaps justify new decision contracts. Identify which UX/behavior cannot be implemented, canonical source, impacted consumers, derived artifacts, and minimum proof.

## Validation

Use focused local gates:

- domain rules: `mvn "-Dtest=DomainRuleControllerTest,DomainRuleServiceTest,DomainRuleMigrationConstraintTest" test`
- domain knowledge: `mvn "-Dtest=DomainKnowledgeChangeSetControllerTest,DomainKnowledgeChangeSetServiceTest,DomainKnowledgeChangeSetValidatorTest,DomainKnowledgeEntityLifecycleTest,DomainKnowledgeProjectionServiceTest" test`
- catalog/federation: `mvn "-Dtest=Domain360CatalogControllerTest,Domain360CatalogServiceTest,DomainCatalogIngestionServiceTest,DomainCatalogPromptContextServiceTest,DomainFederation*Test" test`

For public decision/materialization changes, review `docs/ai/**`, `docs/domain-catalog/**`, quickstart smokes, Angular core domain services, Page Builder handoff, and public docs/examples.

## Companion Skills

- Use `praxis-core-domain-governance-runtime` for Angular clients and cockpit projection of these decisions.
- Use `praxis-config-agentic-authoring-streaming` when turn streams route into shared rule/domain knowledge authoring.
- Use `praxis-config-api-metadata-grounding` when decisions depend on API metadata, Domain Catalog, Project Knowledge, or resource candidates.
- Use `praxis-metadata-discovery-capabilities` when materializations project to backend resource actions, surfaces, capabilities, or option sources.
