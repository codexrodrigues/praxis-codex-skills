---
name: praxis-metadata-domain-option-sources
description: Use when Codex must work on praxis-metadata-starter semantic domain and option-source contracts: @DomainGovernance, /schemas/domain, semantic metadata reviewer, @UISchema presets, fieldAccess, OptionSourceDescriptor, RESOURCE_ENTITY, filter/by-ids endpoints, selectedReloadPolicy, invalidSortPolicy, entity lookup metadata, or x-ui optionSource publication.
---

# Praxis Metadata Domain Option Sources

Use this skill for semantic domain grounding and governed option sources in `praxis-metadata-starter`. These contracts let AI and runtimes understand resource vocabulary, data governance, field access, and remote lookup semantics before authoring decisions.

## Source Audit

Inspect the owner before editing:

- `praxis-metadata-starter/AGENTS.md`
- `src/main/java/org/praxisplatform/uischema/annotation/DomainGovernance.java`
- `src/main/java/org/praxisplatform/uischema/annotation/AiUsagePolicy.java`
- `src/main/java/org/praxisplatform/uischema/domain/**`
- `src/main/java/org/praxisplatform/uischema/authoring/SemanticMetadataReviewer.java`
- `src/main/java/org/praxisplatform/uischema/extension/annotation/UISchema.java`
- `src/main/java/org/praxisplatform/uischema/options/**`
- `docs/guides/SEMANTIC-METADATA-AUTHORING.md`
- `docs/guides/OPTIONS-ENDPOINT.md`
- `docs/guides/OPTION-SOURCE-PROVIDER-SPI.md`
- `docs/spec/x-ui-field.schema.json` and option-source examples

## Canonical Boundary

`@DomainGovernance` materializes `x-domain-governance` in OpenAPI and republishes governance in `/schemas/domain`. It is the preferred explicit declaration for privacy, security, compliance, data category, AI usage policy, reason, and confidence.

`@UISchema` presets and field access metadata publish presentation and access hints, but they do not replace domain descriptions, security enforcement, or governance declarations.

`x-ui.optionSource` and option-source runtime contracts own remote lookup semantics: source key, type, resource path, display/value fields, dependency filters, `includeIds`, `filterEndpoint`, `byIdsEndpoint`, `selectedReloadPolicy`, and `invalidSortPolicy`.

`RESOURCE_ENTITY` option sources must publish enough governed lookup evidence for agents and runtimes to preserve entity identity: `entityKey`, value/label/status paths, dependency filter map, selection policy, filtering contract, canonical `filterEndpoint`, and canonical `byIdsEndpoint`. Do not substitute this with frontend autocomplete URLs, label parsing, or inferred entity names.

Selected-value reload is part of the backend contract. Use GET `/by-ids` only when ids are self-contained; use POST `/by-ids` with the same structural filter context when dependencies or provider-required context affect visibility. If the contract cannot reload selected ids safely, publish an explicit partial/waived policy instead of letting Angular silently drop or guess selected values.

## Decision Rules

- Do not create local Angular lookup routes when `OptionSourceRuntimeContract` can publish canonical filter/by-ids endpoints.
- Do not treat labels as domain descriptions. `@Schema(description=...)` should explain business meaning; `@UISchema` should drive UI behavior.
- Prefer explicit `@DomainGovernance` in self-describing hosts and examples; fallback heuristics are not the preferred canonical authoring path.
- Field access hints guide runtimes and assistants, but host services/security still enforce access.
- Entity lookup, async select, and selected-value reload should be solved through `RESOURCE_ENTITY` option-source semantics, not host-local autocomplete conventions.
- If selected IDs are not self-contained, by-ids reload needs contextual contract or an explicit partial/waived policy.

## No Keyword Routing

Do not infer domain, field access, option source, entity lookup, dependency, or selected-value behavior from labels, field names, regexes, aliases, or local fuzzy matching as the primary decision. Use `@DomainGovernance`, OpenAPI/schema metadata, `x-ui.optionSource`, declared option-source keys, resource keys, and governed semantic catalogs for grounding; textual matching may only rank already-scoped candidates.

## Aderence Inventory

Before adding option-source fields, governance categories, field access semantics, presets, reviewer diagnostics, or lookup endpoints, classify:

- `ja-suportado-so-ux`
- `ja-suportado-mal-nomeado-ou-mal-materializado`
- `suportado-parcialmente`
- `lacuna-real-de-contrato`

Only real contract gaps justify new public metadata. Otherwise improve publication, diagnostics, docs, or consumer materialization of existing semantics.

## Validation

Use focused local gates:

- domain catalog/governance: domain catalog and semantic metadata reviewer tests
- option sources: option-source registry/provider/executor/request validator tests and docs/spec examples
- schema projection: `ApiDocsControllerTest`, filtered schema resolver tests, and spec schema validation where present
- downstream Angular proof when lookup behavior changes: `GenericCrudService` option-source tests, dynamic-fields option-source tests, and dynamic-form submit/value tests

Review `docs/spec/x-ui-field.schema.json`, option-source examples, guides, quickstart fixtures, and HTTP examples when public metadata changes.

## Companion Skills

- Use `praxis-metadata-schema-contracts` for structural projection into `/schemas/filtered`.
- Use `praxis-api-quickstart-domain-pilots` and `praxis-api-quickstart-cockpit-http-validation` for downstream proof of option-source, entity lookup, domain governance, and cockpit materialization.
- Use `praxis-fields-option-sources`, `praxis-fields-selection-lookup-controls`, and `praxis-resource-entity-lookup-backend` for Angular/backend lookup consumption.
- Use `praxis-core-domain-governance-runtime` when domain governance feeds config-starter semantic decision authoring or Angular runtime decision clients.
