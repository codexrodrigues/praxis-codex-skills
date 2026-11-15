---
name: praxis-java-domain-governance-field-access
description: Use when implementing, auditing, or migrating Praxis Java domain governance and field access: @DomainGovernance, AiUsagePolicy, x-ui.fieldAccess, personal/sensitive/financial/security data, masking, export and analytics eligibility, filters and option sources, audit/provenance fields, semantic domain catalog, and backend enforcement with Angular materialization.
---

# Praxis Java Domain Governance Field Access

Treat governance as canonical domain semantics with backend enforcement. Metadata
explains and materializes safe behavior; it never makes Angular visibility,
`x-ui.fieldAccess`, masking hints, or capabilities a substitute for authorization.

## Classify The Field In Its Business Context

Inspect product documentation, DTO operation role, entity/view source, existing
annotations, authorization, export/stats/filter/lookup behavior, AI consumers,
logs, and tests. Record purpose, data category, sensitivity, source of truth,
who may read/edit/export it, masking expectation, AI use, retention evidence,
and analytic eligibility. Do not infer legal basis or retention when evidence is absent.

Classify a proposed governance field or policy as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or
`lacuna-real-de-contrato`. Reuse `@DomainGovernance`, `AiUsagePolicy`, filtered
schema, domain catalog, field access, export/stats and option-source contracts
before proposing a parallel host-specific metadata model.

## Author The Governed Contract

1. Use `@Schema` for verified business meaning and `@DomainGovernance` for
   classification, purpose, visibility, export eligibility, governance
   evidence, and AI implications using only its 9 real canonical attributes:
   `preset` (`DomainGovernancePreset`), `kind` (`DomainGovernanceKind`),
   `classification` (`DomainClassification`), `dataCategory` (`DomainDataCategory`),
   `complianceTags`, `exportable` (`boolean`, default `true`),
   `aiUsage = @AiUsagePolicy(visibility = AiVisibilityMode..., trainingUse = AiTrainingUseMode..., ruleAuthoring = AiControlledUseMode..., reasoningUse = AiControlledUseMode...)`,
   `reason`, and `confidence` (never invent non-existent attributes on `@DomainGovernance` like `owner`, `steward`, `retentionPolicy`, `sensitive`,
   `lgpdPurpose`, or `maskingPattern`). `@DomainGovernance` also supports
   `@Target(ElementType.TYPE)`, allowing class/interface-level baseline governance
   that merges monotonically (`DomainLineageResolver.mergeRestrictive`) with field-level
   declarations.
   - **Selective Financial Governance — Active Public Transparency vs. Private Deductions (`PLAT-EVO-13`):** `DomainGovernancePreset` includes `PUBLIC_TRANSPARENCY_REMUNERATION` (`DomainClassification.PUBLIC`, `DomainDataCategory.FINANCIAL`, `exportable = true`, `AiVisibilityMode.ALLOW`, `complianceTags = {"LAI", "LGPD_ART_23", "PUBLIC_TRANSPARENCY_REMUNERATION"}`) alongside `CONFIDENTIAL_FINANCIAL` (`CONFIDENTIAL`, `exportable = false`, `AiVisibilityMode.MASK`). In public-sector payroll and career DTOs, never blanket-mark an entire financial DTO as `CONFIDENTIAL_FINANCIAL` (`exportable = false`) when statutory gross pay, career table values, and constitutional cap abatements are subject to active public transparency (`ACTIVE_PUBLIC_TRANSPARENCY_LAI`), nor blanket-expose private third-party/personal deductions: combine `PUBLIC_TRANSPARENCY_REMUNERATION` on public remuneration columns with `CONFIDENTIAL_FINANCIAL` on alimony, payroll consignments, union dues, private health copayments, and bank-account coordinates in the same DTO so collection export (`allExportableFields()`), AI grounding, and `praxis-authz-*` masking enforce selective column-level compliance automatically.
   - **Deterministic Lineage (`@DomainLineage`):** When a DTO or read projection maps an Entity or canonical attribute, annotate the property with `@DomainLineage(attributeId = "...", sourceClass = ..., sourcePaths = {...}, sourceResourceKey = "...", transformation = DomainLineageTransformation.DIRECT | MASKED | AGGREGATED | DERIVED)` while keeping `@DomainGovernance` on the DTO property. `SemanticMetadataReviewer` flags `lineage-governance-weakened` if the DTO weakens the source's classification/AI/export restrictions, and `review(dtoClass, optionSources, statsRegistry)` enforces the `P50` gate (`restricted-field-in-analytics-or-option-source`) when a `RESTRICTED`/`CREDENTIAL`/`SENSITIVE_PERSONAL` field is exposed in `StatsFieldRegistry` or `OptionSourceDescriptor`.
   - **LGPD Treatment Purpose (`LegalTreatmentPurpose`):** On `@UiSurface` and `@WorkflowAction`, declare `legalPurpose = LegalTreatmentPurpose.*` (`UNSPECIFIED`, `HUMAN_RESOURCES_ADMINISTRATION`, `PAYROLL_AND_TAX_COMPLIANCE`, `OFFICIAL_HEALTH_EXPERTISE`, `SOCIAL_SECURITY_AND_BENEFITS`, `ACTIVE_PUBLIC_TRANSPARENCY_LAI`, `EXTERNAL_AUDIT_CONTROL`, `EMPLOYEE_SELF_SERVICE`, `STATUTORY_LEGAL_OBLIGATION`) and `legalBasisRef = "..."` when a surface or command operates under a specific legal basis (validated by `legal-basis-without-legal-purpose` and `legal-purpose-without-legal-basis-ref`).
   - **Praxis Decision Platform (`praxis-authz-*` vs. `praxis-rules-engine`) Architectural Boundary:** In `praxis-metadata-starter`, `@DomainGovernance`, `@DomainLineage`, `LegalTreatmentPurpose`, and `@UISchema(visibleForAuthorities = {...}, editableForAuthorities = {...}, fieldAccessReason = "...")` are **declarative semantic contracts** published in `/schemas/filtered` (`x-domain-governance`, `x-domain-governance.lineage`, `x-ui.fieldAccess`) and `/schemas/domain` (`?strict=true`) for AI assistants, export allowlists, and `praxis-authz-starter` / `praxis-authz-enforcement-core` / `praxis-authz-opa` (`decisionKind = AUTHORIZATION`, `ruleType = "authorization_policy"`). Do not build ad-hoc Jackson payload redaction or field-level write-blocking filters inside the metadata starter or host DTOs.
   Do not use a generic label or database column as domain explanation.
2. Set AI usage deliberately. Secrets, credentials, raw private notes, health,
   payroll, disciplinary, security, and high-risk personal data are excluded or
   masked unless a governed use case proves otherwise. Do not expose them to RAG,
   reasoning, training, summaries, or automated action by default.
3. Publish `x-ui.fieldAccess` only as a materialization of a backend-governed
   policy. Enforce read/edit/filter/export/action access on the server and test a
   denied caller. Capabilities are not implicit field authorities.
4. Apply least exposure across response DTOs, create/update DTOs, filters,
   option labels/search, analytics, exports, logs, errors, and generated docs.
   A field may be allowed in one surface and excluded in another only with an
   explicit purpose and consumer proof.
5. Treat audit/provenance and technical legacy fields deliberately: normally
   read-only, grouped, hidden from write forms, and excluded from AI/export/stats
   unless the business need is verified. Never publish tokens, session, SQL,
   ROWID, package, or provider internals.
6. Keep masking/redaction semantics consistent with raw access. A mask is not
   authorization; do not return raw data in hidden payloads, exports, filters,
   option source search, analytics, or error text after a UI mask is declared.

Read [field-governance-matrix.md](references/field-governance-matrix.md) when
deciding exposure across operations and consumers.

## Prove Enforcement And Materialization

Prove one allowed and one denied context for sensitive fields. Verify emitted
schema/domain governance/field-access metadata, backend read/write/filter/export
enforcement, masking behavior, AI policy, logs/errors sanitization, and direct
Angular materialization. When the field is excluded from stats/export/options,
prove that those paths reject or omit it without silently widening data exposure.

Use focused DTO/schema/governance tests plus affected resource, option-source,
stats/export, and quickstart HTTP evidence. Run Angular schema-normalizer or
field-access consumer specs when public metadata changes. Review docs/corpus only
when they publish the changed governance claim.

## Companion Skills

- `praxis-authz-decision-platform`: runtime authorization (`ACCESS`), `DataScopePlan` (`DATA_SCOPE`), `FIELD_USE`/`FIELD_WRITE`, detached DTO masking (`MASK`), and obligation barriers across `praxis-authz-*`.
- `praxis-dto-annotations`: semantic descriptions, UI metadata, and DTO roles.
- `praxis-java-stats-export-authoring`: analytics/export field eligibility.
- `praxis-java-option-source-provider-authoring`: lookup search/display exposure.
- `praxis-java-error-response-contracts`: sanitized errors and diagnostics.
- `praxis-java-contract-conformance`: final cross-consumer evidence.

Close with the field matrix, policy evidence, allowed/denied proof, consumer
coverage, and any unverified governance decision. A field is governed only when
the server and all published projections agree on its permitted use.
