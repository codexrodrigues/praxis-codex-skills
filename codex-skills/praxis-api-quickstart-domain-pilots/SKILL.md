---
name: praxis-api-quickstart-domain-pilots
description: "Use when Codex must implement, audit, or extend Praxis API Quickstart pilot domains: ApiPaths, resource-oriented controllers and services, DTO/filter meaning, @UISchema, @DomainGovernance, option sources and entity lookup, stats/export, surfaces/actions, demo data, operational migrations, cockpit evidence, or governed domain-decision materializations across HR, operations, assets, procurement, and risk intelligence."
---

# Praxis API Quickstart Domain Pilots

Use this skill when a concrete quickstart domain must prove a Praxis capability in a real Spring Boot host. A pilot is not a disposable CRUD example: it is executable, didactic evidence that semantic grounding, metadata, discovery, governed decisions, and runtime behavior agree end to end.

## Classify And Map Impact

Classify a change before editing:

- `local-pequena`: one host resource, with no public contract change.
- `transversal`: a pilot plus another quickstart domain, docs, HTTP evidence, or a runtime consumer.
- `contrato-publico`: `ApiPaths`, `@ApiResource`, OpenAPI groups, schemas, option-source endpoints, `_links`, actions, surfaces, capabilities, stats, or export behavior changes.
- `arquitetural`: ownership or lifecycle crosses the quickstart, metadata starter, config starter, or Angular runtime.

For `transversal`, `contrato-publico`, or `arquitetural`, map the canonical owner, affected resource keys and paths, consumers, cockpit/docs/HTTP evidence, focused tests, and breaking-change risk before patching.

## Source Audit

Read the host and the exact pilot before deciding that it needs a new contract:

- `praxis-api-quickstart/AGENTS.md`
- `src/main/java/com/example/praxis/apiquickstart/constants/ApiPaths.java`
- `src/main/java/com/example/praxis/apiquickstart/config/OptionSourceConfig.java`
- the affected `controller`, `service`, `dto`, `dto/filter`, `dto/actions`, `mapper`, `entity`, and repository
- `db/operational-migrations/**` and `docs/DEMO-DATABASE.md` when persistence or seed data changes
- `docs/SEMANTIC-DOMAIN-CATALOG-CONTRACT.md`
- `docs/COCKPIT-QUICKSTART-REFERENCE.md` and its verification scripts when a published pilot contract changes
- focused integration tests in `src/test/java/com/example/praxis/apiquickstart/**`

The current reference families are intentionally complementary:

| Pilot family | Primary proof |
| --- | --- |
| Human resources | resource CRUD, payroll workflow, privacy/governance, export, and people lookup |
| Operations | explicit lifecycle actions, cross-domain relationships, mission and incident workflows |
| Assets | custody, readiness, allocation, fleet/missions, and analytics |
| Procurement | governed entity lookup, supplier eligibility, contract/product/order lifecycle, and config decision materialization |
| Risk intelligence | threat lookup, triage actions, derived incident analytics, and chart-ready stats |

Do not copy one pilot mechanically into another. Start with the business question, existing resource keys, published schemas, capability/action catalogs, and decision evidence.

## Canonical Ownership

The quickstart owns concrete example resources, host composition, paths, demo persistence, security exposure, and downstream proof. It is not the source of canonical platform semantics.

- `praxis-metadata-starter` owns `x-ui`, `/schemas/filtered`, schema resolution and headers, surfaces, actions, capabilities, HATEOAS, resource bases, option-source runtime contracts, and metadata discovery.
- `praxis-config-starter` owns governed Domain Catalog/Federation/Knowledge, domain-rule intake, simulation, approval, publication, diagnostics, and materialization lifecycle.
- `praxis-rules-engine` owns runtime-neutral RuleSet/snapshot contracts, deterministic planning and evaluation; Config Starter owns their governed snapshot store/head, while the quickstart owns only the executable host registry and activation adapter.
- `praxis-ui-angular` consumes materialized contracts and decisions; it must not become an alternative owner of backend semantics.
- The quickstart proves all of the above with real resources, HTTP contracts, and focused tests.

If a metadata or config behavior is missing, reproduce it with the pilot, fix it in the responsible starter, and keep the quickstart change as a minimal downstream proof. Do not add host-local endpoint aliases, schema patches, decision engines, or UI conventions to hide a platform gap.

## ApiPaths Is An Identity Ledger

`ApiPaths` is a public synchronization point, not a string helper. A path or lookup-source change must be audited as one identity change across:

1. `@ApiResource(value, resourceKey)` and OpenAPI group resolution.
2. Controller mappings, resource base behavior, `_links`, and schema operation URLs.
3. `@UISchema(endpoint=...)`, filter DTOs, option-source descriptors, filter/by-ids endpoints, and dependency maps.
4. Related-resource/surface/action references, stats/export endpoints, test fixtures, HTTP scripts, and cockpit documentation.
5. Existing external consumers and the breaking-change plan.

Prefer the existing `ApiPaths` constant everywhere. Do not construct an equivalent URL in a DTO, service, test, documentation script, or frontend consumer. A resource key is the stable semantic identity; a label or path fragment is not a substitute for it.

## Build A Resource As A Complete Contract

For a mutable pilot, use the resource-oriented baseline: `AbstractResourceController`, `AbstractBaseResourceService`, `ResourceMapper`, and `RestApiResponse`. For read-only analytics/views, use the read-only counterpart. Keep the controller, service, mapper, response ID, filter, and test evidence aligned.

For each resource, verify:

- a stable `@ApiResource(resourceKey=...)`, canonical `ApiPaths` path, and correct `@ApiGroup`;
- operation-specific create, update, response, filter, action, and stats schemas resolve through `/schemas/filtered` rather than a host map;
- DTO `@Schema(description=...)` explains business meaning, boundary, relationship, or lifecycle in the context of that operation;
- `@UISchema` publishes presentation/control behavior only; it does not redefine business or governance meaning;
- filters express query semantics and option-source dependencies, rather than being create DTOs with a few fields removed;
- resource identity, `_links`, capabilities, export, and stats remain inherited from the canonical resource base where applicable.

Never use a generic PATCH or ordinary CRUD update to conceal an explicit business transition. A command such as approval, triage, activation, custody resolution, cancellation, or payment must be a documented workflow action with its own request/response schema, state checks, outcome, and discovery metadata.

For a real collection-level command that has no queryable or persisted collection, extend the metadata starter's `AbstractCollectionCommandResourceController`. Publish the action, capabilities, schemas, and governed command response without fabricating a repository, query service, CRUD endpoints, or decorative surface. Move that pilot to the resource-oriented persistent baseline only when the domain gains real item identity, persistence, and read operations; update host proof, discovery evidence, and consumers in the same change.

When that persistent resource has a mutable lifecycle but ordinary CRUD would bypass its business states, use the read-only resource baseline for query/filter/stats and publish every mutation as an explicit workflow action. Expose `getResourceVersion` so item GET and action responses emit the canonical ETag. Require `If-Match` on item commands, but check for a completed idempotent replay before rejecting a now-stale ETag: a retry of an already committed command must return the original result without repeating the transition.

Scope an idempotency key by resource key, collection/item target, action and authenticated actor, and fingerprint the complete command. Persist the domain mutation, append-only transition/effect ledger and completed idempotent response in one operational transaction; a committed mutation without a replayable result is not an acceptable corporate proof. A batch that promises partial success must declare itself non-atomic, preserve input order and run each item in its own transaction. If an effect leaves the operational database, replace direct remote execution with a transactional outbox and an idempotent consumer; same-database ledgers prove local atomicity only.

## Metadata, Governance, And Lookup

Use the published contract rather than local UI knowledge:

- `@Schema` states business semantics; it is not a duplicate of a screen label or Java type.
- `@UISchema` declares UI behavior such as control type, endpoint, read-only, formatting, or field mechanics.
- `@DomainGovernance` and the semantic domain catalog express privacy, compliance, AI-use, visibility, and governance context. UI hints do not enforce security or replace this meaning.
- Register option sources in `OptionSourceConfig` and publish a descriptor for every declared source.
- Use `RESOURCE_ENTITY` with canonical source key, resource path, value/display fields, dependencies, filter endpoint, by-ids reload behavior, selection policy, and entity-lookup capability metadata when a relation points at a Praxis resource.
- Use a provider-backed option source only when the source truly is not a resource entity; do not build a separate autocomplete endpoint.

When a lookup crosses domains, prove the chain from the consuming field's `x-ui.optionSource` through its source key, source resource, filter/by-ids endpoints, dependency filters, selected-value reload, and authorization behavior. The `ResourceEntityLookupGovernanceIntegrationTest` pattern is the reference inventory, not an optional UI enhancement.

For a dependent `RESOURCE_ENTITY` or governed option-source pilot, schema presence is not enough. Prove the runtime contract that removes cognitive load from consumers:

- `/schemas/filtered` must publish `type`, `key`, `entityKey`, `resourcePath`, `filterEndpoint`, `byIdsEndpoint`, `dependsOn`, `dependencyFilterMap`, `selectedReloadPolicy`, `invalidSortPolicy`, capability flags, and selection policy from the canonical descriptor.
- `dependencyFilterMap` is backend `x-ui.optionSource` grounding: it maps observed schema fields to backend filter payload names. Do not replace it with Angular metadata-editor cascade patches or local field-name translations in the consumer.
- The filter endpoint must accept the mapped dependency payload and return selectable/disabled metadata, including code/status/description/disabled reason when the descriptor declares those semantics.
- The by-ids endpoint must rehydrate existing values, preserve requested order, and return invalid/non-selectable rows with enough metadata for the runtime to retain or reject according to policy.
- If a pilot uses provider-backed options instead of `RESOURCE_ENTITY`, still prove `filterEndpoint`, `byIdsEndpoint`, selected reload, invalid sort, dependencies, and lightweight `OptionDTO{id,label}` behavior, while making clear that it does not publish rich entity lookup metadata.

Use `ProcurementEntityLookupPilotIntegrationTest` for dependent supplier/contract/product lookup proof, `VwStatsSmokeHttpTest` and `VwAnalyticsFolhaPagamentoServiceStatsTest` for `dependencyFilterMap` on analytical option sources, and `ProcurementExternalOptionSourceProviderIntegrationTest` for provider-backed dependency and reload policies. This distinction is especially important in migrations such as Ergon: Praxis should publish the canonical lookup and reload contract so migrators do not hand-code cascade, rehydration, or invalid-selection decisions per screen.

Do not decide a resource, field, lookup, action, relation, or domain intent from labels, aliases, regexes, routes, or fuzzy matching as the primary mechanism. Resolve semantic scope through resource keys, schemas, governed catalogs, actions, capabilities, and declared tools. Textual matching can only rank candidates after that scope is known.

## Actions, Surfaces, And Decision Materializations

`@WorkflowAction` publishes a business command; `@UiSurface` publishes a composed business experience. Both must say what decision or journey is supported, which resource/action contract it uses, and how a runtime can discover it. Do not create decorative surfaces or labels that have no executable contract.

For a workflow action, check action id, scope, allowed states, request/response schema, HTTP status semantics, success/failure result, HATEOAS schema links when the controller exposes them, action catalog, capabilities, and negative-path test. Collection actions such as payroll bulk approval must preserve per-item outcomes instead of pretending that every transition is atomic.

When a pilot consumes a shared domain decision:

1. Resolve the domain and target through metadata/catalog grounding before authoring a rule.
2. Treat Domain Rule/Domain Knowledge definitions, evidence, simulation, approval, publication, diagnostics, statuses, source hashes, and materialization outcomes as config-starter contracts.
3. Consume only an applied materialization in the host, such as procurement supplier selection eligibility, backend validation, or workflow-action policy.
4. Keep the host enforcement narrow and deterministic; it must not recreate authoring, publication, status transitions, or policy inference locally.
5. Prove a published materialization changes runtime behavior, including the relevant rejected state, without presenting simulation as business-data execution.

If `DomainRuleService` is unavailable, the materialization store is missing, or no valid `applied` materialization exists for the target layer/artifact, treat that as missing operational proof for this host execution. The quickstart may return no optional policy or mark the proof unavailable according to the existing resolver contract, but it must not synthesize a fallback business rule from DTO labels, prompt text, demo data, Java defaults, or migration-specific assumptions. `DomainRuleOptionSourcePolicyResolver`, `DomainRuleBackendValidationPolicyResolver`, and `DomainRuleWorkflowActionPolicyResolver` are the reference boundary: they select the latest valid applied materialization from Config Starter and otherwise return empty. Empty means "no governed materialization available to this host now", not "the semantic rule is absent", not "the consumer can decide locally", and not "the pilot owns the policy".

The quickstart may demonstrate a materialization, but no pilot may route rules through command words, local keyword rules, or copied assistant text. Governed semantic resolution remains the primary path.

## Governed Snapshot Consumption

When a pilot consumes an active runtime snapshot, keep it as a downstream data-plane proof:

1. Load only the configured tenant, environment, owner, RuleSet and host-contract identity from the Config Starter head/read boundary.
2. Revalidate immutable content hash, validity interval and strictly monotonic activation revision. Cache hits may use the same head ETag; stale or reordered activations must be rejected.
3. Compile the complete candidate with the host's executable Java registry before exposing it. The authoring/config boundary uses only planning coordinates and must never receive host executor instances.
4. Swap the compiled plan atomically. Network failure, invalid content, incompatibility or missing executor preserves the last-known-good; do not rebuild a bootstrap-local fallback as a parallel authority.
5. Prove rollback v1 → v2 → v1: v1's content hash repeats, but the opaque head ETag and activation revision must advance so ABA is rejected.
6. Make polling/startup loading operationally opt-in where the host profile does not provide the snapshot tables. Publish health as unavailable/out-of-service until an effective plan exists, without leaking snapshot payloads, facts or approval evidence.

The loader changes which governed plan is evaluated; it does not authorize business effects. Keep business endpoints, persistence, idempotency, shadow, effect execution and authority behind their own pilot gates.

## Persistence And Demo Data

Operational migrations and deterministic demo data support proof; they do not define canonical platform semantics. Preserve resource relationships, lifecycle states, and representative data needed for filters, lookups, actions, analytics, governance, and negative paths. Update `docs/DEMO-DATABASE.md` when the operational model or seed assumptions change.

Do not make a test only pass by changing production-like seed data without proving the contract it represents. Keep sensitive business data fictional and respect published governance/visibility restrictions in fixtures, exports, and docs.

## Adherence Inventory

Before adding a path, DTO field, endpoint, filter, option source, stat, export, action, surface, migration, or domain materialization, classify the need:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only `lacuna-real-de-contrato` justifies a new contract. State the missing behavior, canonical owner, impacted consumers, derived artifacts, and minimum proof. In particular, inspect whether existing schema, action, capability, option-source, domain-governance, decision diagnostic, or materialization data simply is not being materialized well by the cockpit or Angular runtime.

## Proof Matrix And Validation

Choose the smallest focused proof that covers the changed contract:

| Changed behavior | Minimum local proof |
| --- | --- |
| resource identity, schema, groups, actions | `mvn "-Dtest=QuickstartMetadataMigrationIntegrationTest,EventosFolhaPilotIntegrationTest,OpenApiGroupResolutionIsolatedIntegrationTest" test` |
| cross-domain entity lookup/option-source contract | `mvn "-Dtest=FuncionarioEntityLookupIntegrationTest,ResourceEntityLookupGovernanceIntegrationTest" test` |
| dependent `RESOURCE_ENTITY` lookup | `mvn "-Dtest=ProcurementEntityLookupPilotIntegrationTest,ResourceEntityLookupGovernanceIntegrationTest" test` plus the affected pilot test |
| dependent provider-backed option source | `mvn "-Dtest=ProcurementExternalOptionSourceProviderIntegrationTest" test` plus the affected pilot test |
| analytical option-source dependency mapping | `mvn "-Dtest=StatsSchemaSmokeHttpTest,VwStatsSmokeHttpTest,VwAnalyticsFolhaPagamentoServiceStatsTest" test` |
| stats, analytics, or export | `mvn "-Dtest=StatsSchemaSmokeHttpTest,FuncionarioExportSmokeHttpTest" test` plus the affected pilot test |
| Domain Knowledge/config host wiring | `mvn "-Dtest=DomainKnowledgeProjectionWiringIntegrationTest" test`; use the config-starter smoke for authoring/publication lifecycle |
| governed snapshot loader/hot reload | focused runtime/health tests proving scope, hash, compatibility, monotonic activation, atomic last-known-good, invalid-candidate rejection and v1 → v2 → v1 rollback; then package/verify against released engine and Config Starter coordinates |
| persistent action lifecycle | focused HTTP proof for read-only query, contextual capabilities, ETag `428/412`, replay before stale ETag, actor/item-scoped idempotency, state transition, atomic ledger rollback and exactly-once effect; add mixed ordered batch proof when partial success is supported |
| one pilot implementation | its focused `*PilotIntegrationTest` plus any directly affected lookup/action/stats/export proof |
| `ApiPaths` or cross-domain public identity | focused proofs above and cockpit verification scripts; use `mvn test` only if those cannot cover the resulting identity graph |

For public cockpit evidence, run the relevant documented script, such as `scripts/verify-cockpit-inventory-doc.sh`, `scripts/verify-cockpit-action-contracts.sh`, `scripts/verify-cockpit-surface-contracts.sh`, `scripts/verify-cockpit-related-resource-contracts.sh`, `scripts/verify-cockpit-analytics-contracts.sh`, `scripts/verify-cockpit-option-source-contracts.sh`, or `scripts/verify-cockpit-structural-ui-contracts.sh`.

Review `README.md`, `docs/DEMO-DATABASE.md`, `docs/COCKPIT-QUICKSTART-REFERENCE.md`, relevant quickstart scripts, public landing docs, and executable HTTP examples when behavior is published. State explicitly when no derived artifact changes.

## Companion Skills

- Use `praxis-api-quickstart-operational-proof` for host/starter ownership, dependency versions, and host validation.
- Use `praxis-api-quickstart-cockpit-http-validation` for cockpit docs, HTTP scripts, and published proof.
- Use `praxis-metadata-resource-baseline` for resource controller/service/HATEOAS behavior.
- Use `praxis-metadata-schema-contracts` for `/schemas/filtered`, operation resolution, `x-ui`, ETag, and schema headers.
- Use `praxis-metadata-discovery-capabilities` for surfaces, actions, capabilities, availability, stats, export, and `_links` discovery.
- Use `praxis-metadata-domain-option-sources` for `@DomainGovernance`, semantic domain catalog, option-source, and lookup contracts.
- Use `praxis-config-domain-decisions` for governed domain rules, Domain Knowledge, publications, and runtime materializations.
