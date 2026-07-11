---
name: praxis-java-stats-export-authoring
description: Use when implementing, auditing, or migrating Praxis Java analytics or collection export: StatsFieldRegistry, StatsSupportMode, metrics and dimensions, stats schema/capabilities, CollectionExportRequest and Result, formats, scopes, selected IDs, filters, sort, field allowlists, row limits, async/deferred results, export headers, and table/chart runtime proof.
---

# Praxis Java Stats Export Authoring

Treat stats and export as governed resource operations. They must reuse canonical
filter, selection, field governance, capability, and discovery contracts; never
become browser aggregation, ad hoc CSV endpoints, or a way to bypass exposure policy.

## Establish The Analytic Or Export Question

Inspect resource semantics, query/service, filters, field governance, existing
stats registry/support mode, collection export capability, consumer, fixtures,
and focused tests. Decide whether a field is a dimension, measure, bucket,
exportable value, or explicitly excluded. Do not infer aggregation from Java type:
an identifier, document, amount, rate, or status needs business evidence.

Classify a metric, dimension, stat endpoint, export field, format, scope, limit,
or header as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. A missing analytical
operation belongs in the canonical starter/service owner, not in a table component.

## Author The Resource Operation

1. Register analytics through `StatsFieldRegistry` and the resource's
   `StatsSupportMode`. Publish only fields whose domain meaning, aggregation,
   visibility, filters, and precision are verified. Do not let a chart choose
   database columns by string or derive metrics in Angular.
2. Keep stats requests tied to the resource query contract. Apply the same
   authorized filters, scope, and field governance as the collection; publish
   stats capability only when the service can execute it.
3. Use `CollectionExportRequest` and `CollectionExportResult` for collection
   export. Define format, scope, selected IDs, filters, sort, page/current/all
   behavior, field allowlist, server-effective limit, async/deferred behavior,
   and result metadata. Do not add a second download request shape.
4. Publish export details through collection capabilities only when supported:
   formats, scopes, per-format max rows, and async state. Keep `_links`,
   `/capabilities`, request behavior, and `X-Export-*` headers consistent.
5. Enforce server-side field allowlists and governance for all scopes. Client
   `maxRows` is a suggestion bounded by server policy. Unknown fields must not
   silently broaden export. Preserve CSV/XLSX formula-injection protection.
6. Keep export and stats errors structured and sanitized. A denied field, scope,
   size, filter, or unavailable operation is a public policy outcome, not a
   generic empty file or a browser fallback.

Read [analytics-export-matrix.md](references/analytics-export-matrix.md) when
choosing field role, scope, capability, result policy, or proof.

## Preserve Boundaries

- `praxis-metadata-starter` owns stats/export contracts, registry/support mode,
  collection capability projection, request/result semantics, and headers.
- The host owns domain eligibility, query implementation, server limits,
  authorization, and data classifications. Do not expose sensitive or internal
  fields because a caller requests them.
- `praxis-ui-angular` consumes published stats/export contracts. It must not
  calculate authoritative analytics or invent export scopes locally.

Do not choose metrics, dimensions, export fields, or source resource through
labels, keywords, regexes, or fuzzy matching. Use registered fields, canonical
resource metadata, governance, stats capabilities, and declared operations.

## Prove Policy And Result

Prove one allowed stats/export path plus one policy negative path. For stats,
prove metric/dimension semantics and filter scope. For export, prove selected and
filtered behavior where published, field allowlist, effective row limit, format,
headers, and formula protection. Prove capability/`_links` alignment and direct
table/analytics runtime materialization without consumer-local rules.

Use focused stats, export, capability, schema, and HTTP tests. Add quickstart
proof for public resource operations and Angular table/analytics/export consumer
tests when their published contract changes. Review docs and corpus only when
they expose the changed operation.

## Companion Skills

- `praxis-java-resource-authoring`: resource operation, filters, and DTO meaning.
- `praxis-java-filter-query-authoring`: query scope and predicate proof.
- `praxis-metadata-discovery-capabilities`: stats/export capability and discovery.
- `praxis-java-error-response-contracts`: policy denial and safe errors.
- `praxis-java-contract-conformance`: final HTTP and runtime evidence.

Close with field-role matrix, capability contract, server policy, result evidence,
consumer proof, and excluded fields. Stats/export is ready when it answers the
business question or produces governed data without widening resource exposure.
