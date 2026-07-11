---
name: praxis-java-filter-query-authoring
description: Use when implementing, auditing, or migrating Praxis Java resource filters and queries: dedicated GenericFilterDTO contracts, @Filterable predicates and relations, ranges, relative periods, pageable sorting, query services, filtered schemas, option-source dependencies, and focused HTTP proof in a Spring host or praxis-metadata-starter.
---

# Praxis Java Filter Query Authoring

Treat a filter as a public query contract that expresses a business question.
Do not treat it as a form-shaped request object, a reduced create DTO, or a
collection of controller-specific query parameters.

## Start With Query Meaning

Inspect the resource operations, entity/view model, existing filter DTO, service,
repository, relevant database evidence, schema projection, UI consumer, and
focused tests. For a legacy screen, distinguish filters that affect result scope,
sort, option dependencies, authorization, or only local presentation.

Create a dedicated `GenericFilterDTO`. For every candidate criterion, record the
business question, target entity property, expected type/cardinality, predicate,
null/empty behavior, governing scope, permitted sort, and UI/option-source
consumer. Do not expose a filter merely because a database column exists.

Before adding a field, operator, payload form, query endpoint, or sort rule,
classify it as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. A new predicate or
public filter shape belongs in `praxis-metadata-starter`, not in a host-local
specification helper.

## Author The Canonical Query Contract

1. Use `@Filterable` only on a dedicated filter DTO field that the backend
   actually executes through the resource query path. Choose its
   `FilterOperation` from the verified business question, never from a field
   suffix or screen label.
2. Use `relation` for an entity relationship path or a readable DTO alias that
   targets a different entity property. For example, `statusIn` must declare
   `relation = "status"`; a relation identifier can target `employee.id`.
   Do not rely on a DTO alias being guessed from a property name.
3. Match payload shape to the selected operation: scalar for equality, text
   search or relative-day count; list for `IN`, `NOT_IN`, and ranges; explicit
   boolean activation for null/boolean predicates. Keep a range's boundary
   semantics and types documented in `@Schema` and UI metadata.
4. Use the starter's `GenericSpecificationsBuilder` through the canonical base
   service. It maps annotated fields to predicates and remaps sortable aliases
   using `relation`. Do not recreate Specifications in each controller unless
   source evidence establishes a genuine unsupported query need.
5. Use the registered filter payload normalizers for canonical range and
   relative-period payload forms. Keep time zone, clock, closed/open bounds, and
   invalid payload behavior covered by tests; do not normalize dates in a
   browser-only helper or silently reinterpret a legacy value.
6. Build pagination through the resource query controller and `PageableBuilder`.
   Preserve the resource default sort when the request omits sorting. Test each
   public sort alias against the target property and relation. An option-source
   request is a stricter contract: use its published sort key and
   `OptionSourceRequestValidator`; never pass unvalidated sort to a provider.
7. Connect relationship filters to their governed option source only when value,
   display, dependency, filter and by-ids reload contracts all exist. A filter
   DTO does not replace an option source descriptor.

Read [predicate-and-proof-matrix.md](references/predicate-and-proof-matrix.md)
when selecting operations, modeling aliases/ranges/relative periods, or choosing
the smallest proof.

## Preserve Semantic And Security Boundaries

- `praxis-metadata-starter` owns `GenericFilterDTO`, `@Filterable`, predicate
  semantics, normalizers, base query services, pagination integration, filtered
  schema projection, and `x-ui` query metadata.
- The host owns the verified domain meaning, repository/view eligibility,
  authorization context, and resource-specific default sort. Do not publish
  confidential, tenant-crossing, audit-only, or prohibited fields simply because
  JPA can filter them.
- `praxis-ui-angular` materializes published filter metadata. It does not infer
  a predicate from labels or construct an undocumented payload dialect.

Do not route primary user intent, filter selection, or target resolution through
keyword lists, regexes, aliases, or fuzzy matching. Resolve scope through the
resource, schema, governed catalog, filter contract, and option-source metadata;
text matching can only assist after that scope is established.

## Prove Query Behavior

Prove more than a non-empty page. Cover the annotated predicate against known
fixtures, the alias/relation target, null/empty behavior, pagination/default sort,
one invalid or unsupported payload, and authorization/dependency constraints when
applicable. For ranges or relative periods, test normalization and boundary/time
semantics. For public filter-schema changes, prove `/schemas/filtered` and the
direct runtime consumer or state why it is unaffected.

Use focused starter tests for `GenericSpecificationsBuilder`, range/relative
normalizers, `PageableBuilder`, `FilterRequestBodyAdvice`, and affected resource
services/controllers. Add a quickstart or host integration proof when the change
is public or legacy-derived. Review HTTP examples and docs only when they expose
the changed contract.

## Companion Skills

- `praxis-java-resource-authoring`: resource identity, selected base service,
  operation matrix, and end-to-end proof.
- `praxis-dto-annotations`: semantic descriptions, UI controls, governance, and
  filter DTO annotation quality.
- `praxis-metadata-resource-baseline`: query controller/service behavior,
  HATEOAS, stats, and export boundaries.
- `praxis-metadata-schema-contracts`: filtered schema, operation references,
  OpenAPI, ETag, and schema hash.
- `praxis-metadata-domain-option-sources` and
  `praxis-resource-entity-lookup-backend`: governed lookup and option-source
  filtering/reload contracts.

Close with a predicate matrix, source evidence, query/authorization decision,
schema and HTTP proof, and any real platform gap. A filter is ready when a
consumer can ask the intended business question predictably, not when a request
parameter happens to reach a repository.
