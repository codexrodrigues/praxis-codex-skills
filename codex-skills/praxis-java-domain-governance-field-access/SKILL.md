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
   classification, purpose, visibility, governance evidence, and AI implications.
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

- `praxis-dto-annotations`: semantic descriptions, UI metadata, and DTO roles.
- `praxis-java-stats-export-authoring`: analytics/export field eligibility.
- `praxis-java-option-source-provider-authoring`: lookup search/display exposure.
- `praxis-java-error-response-contracts`: sanitized errors and diagnostics.
- `praxis-java-contract-conformance`: final cross-consumer evidence.

Close with the field matrix, policy evidence, allowed/denied proof, consumer
coverage, and any unverified governance decision. A field is governed only when
the server and all published projections agree on its permitted use.
