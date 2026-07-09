# Metadata Sources

## Goal

Answer "de onde vêm os metadados?" without hand-waving.

## Canonical Source Layers

When the question is about Praxis runtime metadata, separate the layers explicitly:

- `/schemas/filtered`: canonical structural schema for request/response plus `x-ui`
- `/schemas/domain`: derived semantic/domain vocabulary for AI, governance, aliases, bindings, and evidence
- `x-domain-governance`: explicit governance published on fields when the backend marks sensitive or policy-relevant data
- `x-ui.optionSource`: canonical metadata for remote/cascading option semantics; operational option endpoints execute it but do not replace it as the semantic source
- local component config: host-owned config such as `FormConfig`, `TableConfig`, or transient field metadata
- downstream editorial metadata: naming/discovery metadata projected through `ComponentMetadataRegistry` and `@praxisui/dynamic-fields`

Do not collapse these into a single answer like "vem do backend".

## Dynamic Form

Possible metadata sources:

- local `FormConfig.fieldMetadata`
- backend schema discovery from `/schemas/filtered` for runtime bootstrap
- backend semantic/governance context from `/schemas/domain` or field-level `x-domain-governance` when the question is about meaning, policy, or AI usage rather than only rendering
- canonical remote option semantics from `x-ui.optionSource` when a field depends on backend lookups or cascades
- editorial naming/presentation semantics resolved downstream through `ComponentMetadataRegistry` and `@praxisui/dynamic-fields`

## Table

Possible metadata sources:

- local `TableConfig`
- backend structural schema from `/schemas/filtered`
- backend semantic capability context from `/schemas/domain` when the table question is about governed meaning, domain vocabulary, or AI/RAG projection
- backend option-source/capability metadata when filters or optional collection actions depend on canonical published metadata
- runtime defaults and table-side normalization

## Rule

Always name the real source used in the scenario being discussed.

Do not say only "vem do backend" or only "vem da config" without distinguishing:

- local config
- runtime schema discovery
- semantic/governance discovery
- canonical option-source metadata
- downstream editorial metadata
