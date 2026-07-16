---
name: praxis-java-option-source-provider-authoring
description: Use when implementing, auditing, or migrating a non-JPA or host-specific Praxis option source: OptionSourceDescriptor execution mode, OptionSourceProvider and registry resolution, private execution context, external catalogs, provider ordering, filter/by-ids reload, dependency payloads, request policy, dataset versioning, and x-ui runtime proof.
---

# Praxis Java Option Source Provider Authoring

Use a provider when a governed Praxis option source must execute against an
external catalog, registered query, table function, remote service, or another
host-specific backend. A provider is private execution behind the canonical
option-source contract; it is not a new public lookup endpoint.

## Establish The Source Contract First

Inspect the consuming DTO field, `OptionSourceDescriptor`, option-source
registry/configuration, resource service/controller, schema projection,
authorization/tenant constraints, expected runtime consumer, and focused tests.
Classify whether the need is a reusable `RESOURCE_ENTITY`, `LIGHT_LOOKUP`,
`DISTINCT_DIMENSION`, `CATEGORICAL_BUCKET`, or an existing static source before
adding a provider.

Classify any new source type, metadata field, endpoint, execution policy,
dependency, or reload behavior as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. Keep the public
`x-ui.optionSource`, descriptor, runtime contract, and canonical controller path
in `praxis-metadata-starter`; host code supplies only execution.

## Implement The Provider Path

1. Define a stable source key, type, semantic entity identity, display contract,
   policy, capabilities, dependencies, and `OptionSourceRuntimeContract`. Use
   canonical filter and by-ids paths. New reusable sources normally publish
   `selectedReloadPolicy=required` and `invalidSortPolicy=reject`.
2. Set `OptionSourceExecutionMode.PROVIDER_REQUIRED` when JPA must never attempt
   to execute the descriptor. Leave JPA fallback eligible only when the
   descriptor is truly JPA-executable. Do not use a JPA failure, missing table,
   or `id`/`label` alias as implicit provider selection.
3. Implement `OptionSourceProvider.supports`, `filter`, and `byIds`. Make
   `supports` precise by descriptor, private context, and operation. If more
   than one provider can support a source, declare `Ordered` or `@Order`; a
   host provider precedes JPA fallback, while equal-priority matches are a
   configuration error.
4. Receive public values through the already validated
   `OptionSourceExecutionRequest`: search, structured filters, sort key,
   pageable, include IDs, by-ids IDs, and effective filter payload. Map those
   values to a typed backend query; never interpolate them into SQL, Oracle
   order clauses, remote URLs, package names, or provider-specific query text.
5. Use `OptionSourceContextResolver` and `OptionSourceExecutionContext` for
   tenant, user, session, datasource, credential, or host-private execution
   attributes. Never publish those attributes in `x-ui`, OpenAPI, option extras,
   logs intended for consumers, examples, or errors. Treat public
   `filterPayload`, structured filters, `includeIds`, and by-ids IDs only as
   query criteria; they are never proof of authorization or row scope.
6. Apply each published `dependsOn` / `dependencyFilterMap` value to provider
   execution. If a dependency is not executable, remove it from public metadata
   or resolve the platform gap. A provider that ignores a declared dependency is
   incorrect even when its first-page search looks plausible.
7. Implement `byIds` as a separate selected-value reload path. Return concrete
   options for found IDs; the executor preserves requested order and omits
   missing IDs. When reload needs the same public dependencies as filtering,
   prove the contextual POST by-ids path carries them into the provider. Resolve
   private context and enforce access even when the requested ID list is empty;
   an early empty response must not bypass authorization.
8. Override source dataset versioning when an external source would otherwise
   inherit a resource-level JPA count or timestamp query. A version header may
   remain public, but external availability must not depend on a base table.

Read [provider-contract-matrix.md](references/provider-contract-matrix.md) when
choosing execution mode, reload policy, dependency behavior, ordering, or proof.

## Let Praxis Validate Public Requests

`CompositeOptionSourceQueryExecutor` resolves context, builds a request,
validates it through `OptionSourceRequestValidator`, then resolves a provider.
Do not bypass this flow or register a second `OptionSourceQueryExecutor` bean.
Invalid capability, includeIds, search, page size, structured filter, sort, or
dependency metadata must fail before provider resolution. Provider code may trust
the declared policy but must still keep backend query construction typed and
safe.

For option-source sorting, accept only the published validated sort key. Simple
sources may use the documented legacy `id`/`label` aliases; structured sources
must use their declared sort options. Do not copy general resource pagination
rules into a provider.

## Preserve Boundaries And Prove Them

- `praxis-metadata-starter` owns the descriptor, provider SPI, composite
  executor, registry, public endpoint contract, `x-ui.optionSource`, runtime
  policy, schema projection, and normalization of by-ids output.
- The host owns private catalog access, context resolution, authorization and
  typed backend execution. Do not leak its datasource, query language, package,
  or credentials through metadata.
- JPA-backed resource owners apply server-resolved row scope through
  `normalizeOptionSourceFilter(...)`, which must govern filter, `includeIds`,
  GET by-ids, POST by-ids, and empty-ID requests before the `Specification`
  executes. Provider-backed sources apply the equivalent policy from the
  private `OptionSourceExecutionContext`; do not assume the JPA hook rewrites a
  provider-specific public payload.
- `praxis-ui-angular` consumes filter and by-ids endpoints. It must not invent a
  fallback reload path or infer dependency semantics from labels.

Prove: descriptor/schema runtime projection; correct provider selection; filter
results; by-ids rehydration in requested order; dependency effect; private
context use without leakage; scoped `includeIds`; empty-ID authorization; and
rejection of invalid input before `supports`, `filter`, or `byIds` is called.
Add dataset-version proof for external sources.
Run the focused provider/registry/composite/validator tests and a host or
quickstart HTTP integration test for published sources. Review Angular option
consumer tests when public runtime metadata changes.

## Companion Skills

- `praxis-resource-entity-lookup-backend`: governed `RESOURCE_ENTITY` contract
  and JPA/provider handoff.
- `praxis-metadata-domain-option-sources`: source taxonomy, domain governance,
  descriptors, and schema materialization.
- `praxis-java-filter-query-authoring`: filter payload, query semantics, and
  sort boundaries outside option sources.
- `praxis-java-resource-authoring`: resource identity, host integration, and
  cross-consumer proof.

Close with source classification, descriptor/runtime contract, execution mode,
provider ordering, dependency/reload evidence, private-context boundary, tests,
and any genuine platform follow-up. A provider is complete only when its source
is indistinguishable from a native Praxis option source to public consumers.
