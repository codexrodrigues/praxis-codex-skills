---
name: praxis-config-domain-decisions
description: Use when Codex must implement, audit, or consume praxis-config-starter governed semantic decisions: domain-rule intake, structural simulation, publication and materialization; Domain Knowledge change sets and evidence lifecycle; Domain Catalog or Federation grounding; decision diagnostics, approvals, timelines, and Angular runtime projections.
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
- `src/main/resources/db/migration/V18__create_domain_knowledge_layer.sql` through `V26__add_domain_knowledge_evidence_lifecycle.sql`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/domain-rule.service.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/domain-knowledge.service.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/services/domain-catalog.service.ts`
- `praxis-ui-angular/projects/praxis-core/src/lib/ai/domain-catalog-context-pack.ts`
- focused domain rule, domain knowledge, catalog, federation, timeline, and migration tests.

## Canonical Boundary

`/api/praxis/config/domain-rules/**` owns intake, definitions, status transitions, simulations, publications, materializations, timelines, explainability, and `decisionDiagnostics`.

`/api/praxis/config/domain-knowledge/change-sets/**` owns governed knowledge patch creation, validation, review, apply, timeline, evidence lifecycle, and derived Project Knowledge indexing.

Domain catalog/federation publishes semantic graph context and relationships for AI grounding. It must not be reduced to labels.

## Layer Model

Keep these owners and lifecycles distinct:

- Domain Catalog releases are immutable producer snapshots. Their RAG documents are derived indexes, not the transactional source of truth.
- Domain Federation is a validated, LLM-safe read model over accepted releases. Ingestion creates a `candidate`; explicit activation makes it authoritative and supersedes the prior active release.
- Domain Knowledge is a governed, change-set-versioned semantic graph of concepts, aliases, bindings, relationships, and evidence. It does not execute business rules.
- Domain Rule definitions hold reusable decision intent, condition, parameters, evidence refs, owner, steward, and governance independently from any component.
- Materializations project an approved/published definition into target artifacts. Angular, Java validation, option sources, workflow actions, and approval policies consume those projections; they do not become the rule owner.

## Domain Rule Workflow

1. Resolve tenant, environment, `resourceKey`, `ruleType`, context, evidence, and semantic owner through governed metadata/catalog/tooling before intake.
2. `POST /domain-rules/intake` persists a `draft` definition and returns grounding plus `decisionDiagnostics`. Do not treat the prompt or assistant text copied into the definition as durable Domain Knowledge evidence.
3. `POST /domain-rules/simulations` may use a persisted definition or an ad hoc request. The current simulation detects approved/active overlapping coverage, predicts target materializations, derives required approvals and publication readiness; it does **not** execute the rule condition against business records or prove business outcomes.
4. Review `existingCoverage`, `predictedMaterializations`, `requiredApprovals`, warnings, explainability, and timeline evidence before publication. Existing approved/active coverage and declared approvals block publication.
5. `POST /domain-rules/publications` requires a persisted definition. In the current contract, `draft`, `proposed`, `approved`, and `active` are publishable when readiness is otherwise clear, and publication promotes the definition to `active`. Therefore, encode required human review in governance and enforce caller authorization at the host; do not assume status alone guarantees prior approval.
6. Publish or create target materializations and preserve stable key, target identity, `sourceHash`, validation result, status, and materialization outcome diagnostics. A stable-key collision with another definition or changed derived source hash must fail instead of silently overwriting a projection.

The current auto-derived publication targets are:

- `selection_eligibility` -> `option_source/resource-option-source`
- validation-family rules -> `backend_validation/resource-validation`
- `workflow_action_policy` -> `workflow_action/resource-workflow-action`
- `approval_policy` -> `approval_policy/resource-action-approval`

Other predicted targets, including form guidance, may require an explicit materialization. Never infer that a predicted target was persisted; inspect `materializations` and `publicationDiagnostics.materializationOutcomes`.

Use only canonical status endpoints. Definition transitions allow review paths including `deprecated -> active`, but `rejected` and `retired` are terminal. Materializations may recover from `failed`, `superseded`, or `reverted` only through `draft` or `pending_review`; they cannot jump directly back to `applied`.

## Domain Knowledge Workflow

- LLM-authored change sets must begin as `proposed`, include stable operation ids, reasons, evidence refs, confidence in `[0,1]`, and a target within the request tenant/environment. Raw prompts, transcripts, or chat memory are not canonical evidence.
- Creation is idempotent only when the same change-set key has the same patch hash and author identity. Reusing a key with different semantics must fail.
- Validation, review, and apply are separate operations. Approval requires a valid stored validation result and reviewer; apply requires `approved`, rechecks validity, and is idempotent after `applied`.
- The validator recognizes concept, alias, binding, relationship, visibility, summary, add-evidence, and revert-evidence operation types, but the current apply service executes only `add_evidence` and `revert_evidence`. Treat all other operations as `suportado-parcialmente`; do not advertise them as operational until an applier and focused proof exist.
- Applying evidence updates the Project Knowledge derived index. Revert deactivates the evidence; an active replacement marks the previous evidence `superseded`, otherwise it becomes `reverted`.
- Timelines and responses expose safe summaries. Do not rehydrate raw patch payloads, prompts, private evidence, or chat transcripts into UI lifecycle events.

## Grounding Safety

- Domain Catalog v0.2 and Federation provide semantic context, ownership, vocabulary, evidence, relationships, visibility, and retrieval policy. They do not define or execute final business rules.
- Apply `aiUsage.visibility`, contract visibility, confidence, tenant/environment scope, release identity, and retrieval policy before returning LLM context. Never bypass `deny` or `deny_for_llm` for ordinary authoring.
- Prefer an active persisted federation release; use catalog projection fallback only as declared by the query response. Preserve `sourceMode`, release keys, policy report, evidence refs, and redaction decisions.
- The existing `policy_reference` option-source prediction contains residual text matching after semantic scope resolution. Do not extend it or use it as primary intent routing; require an explicit canonical `ruleType`/target contract for new behavior.

## Decision Rules

- If a request is about a shared business rule, validation, eligibility, compliance, approval, or policy over a resolved resource, route to domain decisions before component preview/apply.
- UI, option sources, backend validation, workflow actions, and approval policies should be materializations of the governed decision when possible.
- Preserve `decisionDiagnostics`, `explainability`, publication diagnostics, materialization outcomes, timeline events, statuses, source hashes, and canonical owner fields.
- Do not report `simulation.result=pass` as a successful evaluation of business data; it currently describes authoring/coverage diagnostics.
- Status transitions are directional; use the canonical transition endpoints and never mutate status fields or projection records directly.
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
- Angular consumers: `npm run test:core -- --include=projects/praxis-core/src/lib/services/domain-rule.service.spec.ts --include=projects/praxis-core/src/lib/services/domain-knowledge.service.spec.ts --include=projects/praxis-core/src/lib/services/domain-catalog.service.spec.ts`

For public decision/materialization changes, review `docs/ai/**`, `docs/domain-catalog/**`, quickstart smokes, Angular core domain services, Page Builder handoff, and public docs/examples.

## Companion Skills

- Use `praxis-core-domain-governance-runtime` for Angular clients and cockpit projection of these decisions.
- Use `praxis-config-agentic-authoring-streaming` when turn streams route into shared rule/domain knowledge authoring.
- Use `praxis-config-api-metadata-grounding` when decisions depend on API metadata, Domain Catalog, Project Knowledge, or resource candidates.
- Use `praxis-api-quickstart-cockpit-http-validation` and `praxis-api-quickstart-domain-pilots` for downstream proof of domain-rule/domain-knowledge materializations in the reference host.
- Use `praxis-http-examples-contract-surfaces` and `praxis-http-examples-llm-smoke` when governed decision examples or read-only LLM lanes are affected.
- Use `praxis-metadata-discovery-capabilities` when materializations project to backend resource actions, surfaces, capabilities, or option sources.
