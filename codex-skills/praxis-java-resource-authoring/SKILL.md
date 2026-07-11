---
name: praxis-java-resource-authoring
description: Use when implementing, auditing, or migrating a complete Java/Spring Praxis resource in a host or praxis-api-quickstart: choose read-only versus mutable resource hierarchy, author resource identity and DTO contracts, controller/service/mapper integration, filters, lookups, actions, surfaces, capabilities, and focused HTTP or runtime proof.
---

# Praxis Java Resource Authoring

Build a resource as a governed semantic contract, not as a controller plus an
incidental CRUD screen. The canonical baseline is `resource + surfaces + actions + capabilities`; every projection must remain backed by an executable operation.

## Inspect Before Authoring

Read the host's `AGENTS.md`, the affected domain documentation, entity/query
source, existing resource keys and paths, controller/service/mapper, DTOs,
filters, tests, and direct consumers. In the starter, inspect the resource base,
schema resolution, and discovery contracts before adding a host convention.

Classify the work as `local-pequena`, `transversal`, `contrato-publico`, or
`arquitetural`. For a proposed field, endpoint, action, surface, capability,
lookup, stat, export, or metadata shape, classify adherence as
`ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`.

Only a real contract gap justifies a new platform contract. The quickstart is
operational proof, never the canonical owner of a starter or runtime semantic.

## Compose The Resource

1. Establish stable identity: `@ApiResource(resourceKey=...)`, the canonical
   path constant, `@ApiGroup`, resource intent, and a semantic name independent
   of a label or database table. Treat a path/key change as a public identity
   migration across schemas, links, option sources, actions, surfaces, tests,
   HTTP examples, and consumers.
2. Choose the smallest resource base that matches real operations:
   - read-only query/view: `AbstractReadOnlyResourceController` plus
     `AbstractReadOnlyResourceService`;
   - standard mutable resource: `AbstractResourceController` plus
     `AbstractBaseResourceService` and `ResourceMapper`;
   - create/update-only or unit-delete: use the canonical specialized base only
     when the resource genuinely lacks the omitted operation.
   Do not start new work on legacy CRUD/service hierarchies.
3. Define operation-specific response, create, update, filter, and explicit
   command DTOs. `@Schema` describes verified business meaning; `@UISchema`
   describes presentation/control behavior; governance and AI-use metadata are
   deliberate. A filter models predicates, not a reduced create DTO.
4. Implement mapper, service, validation, transactions, and controller as one
   coherent slice. Preserve `RestApiResponse`, canonical `idField`, and `_links`;
   do not introduce host envelopes, endpoint aliases, string-built schema maps,
   or frontend-only id fixes.
5. Add relations only through governed option/lookup contracts. A resource entity
   lookup must prove its source key, `x-ui.optionSource`, filter endpoint,
   selected-value reload, dependencies, authorization, and human display value.
6. Model an explicit business transition as `@WorkflowAction`, with request and
   response schemas, state/authorization checks, negative paths, and capability
   discovery. Model a composed journey as `@UiSurface`. Do not hide either in a
   generic update, method name, or UI button; do not combine action and surface
   on one method without reviewing conflict validation.
7. Add capabilities, availability, stats, export, governance, or related
   resources only when the domain operation exists and the relevant canonical
   contract is fully backed. `/capabilities` aggregates availability; it is not
   an alternate schema or payload definition.

Read [resource-delivery-matrix.md](references/resource-delivery-matrix.md) when
planning a resource packet, selecting a proof, or deciding whether an optional
enterprise feature belongs in this delivery.

## Preserve Canonical Boundaries

- `praxis-metadata-starter` owns annotations, resource bases, `/schemas/filtered`,
  `x-ui`, surfaces, actions, capabilities, option-source contracts, and HATEOAS.
- `praxis-config-starter` owns governed decision authoring and config persistence.
  A host may consume an applied materialization but must not recreate its
  authoring, publication, or inference lifecycle.
- `praxis-ui-angular` is the runtime consumer. When a resource publishes a
  public metadata/discovery change, prove its materializability through the
  relevant schema, option, surface/action/capability, error, and stats/export
  consumer path rather than assuming a browser will infer it.

Do not choose semantic scope or execute primary intent through labels, aliases,
keyword lists, route fragments, regexes, or fuzzy matching. Use resource keys,
schemas, actions, surfaces, capabilities, governed catalogs, and declared tools;
text can only help rank already-scoped candidates.

## Produce Evidence, Not Just Files

Before editing a `transversal`, `contrato-publico`, or `arquitetural` resource,
record the canonical owner, affected consumers, public/derived artifacts, focused
tests, and beta migration/breaking risk. For a legacy-backed development
migration, mutations authorized by the process can be performed, but retain a
scoped probe, before/after evidence, and cleanup or rollback plan.

Prove the smallest complete path:

- resource base, CRUD, identity, and `_links`: focused starter or host resource
  tests;
- schema/`x-ui` contract: `/schemas/filtered` and operation resolution proof;
- lookup: filter and by-ids, including dependency and selected-value reload;
- action/surface/capability: positive and negative availability/discovery proof;
- public metadata change: quickstart HTTP proof and relevant Angular consumer
  tests or an explicit reason they are unaffected.

Review docs, OpenAPI/HTTP corpus, quickstart pilots, and Angular materialization
only when the published contract they mirror changes. State explicitly when no
derived artifact applies.

## Companion Skills

- `praxis-metadata-resource-baseline`: resource hierarchy, response envelope,
  HATEOAS, filters, stats, and export base behavior.
- `praxis-dto-annotations`: semantic, UI, governance, AI, filter, and lookup
  annotations on DTOs.
- `praxis-metadata-schema-contracts`: `/schemas/filtered`, schema references,
  OpenAPI, ETag, and `X-Schema-Hash`.
- `praxis-metadata-discovery-capabilities`: actions, surfaces, availability,
  capabilities, cockpit, stats, and export discovery.
- `praxis-metadata-domain-option-sources` and
  `praxis-resource-entity-lookup-backend`: domain governance and option-source
  implementation.
- `praxis-java-host-project`: host bootstrap, dependencies, and local project
  integration.

Close with the resource packet, resolved classifications, canonical owner,
operation matrix, tests run, consumer proof, and outstanding platform gap. A
resource is not complete because its controller compiles; it is complete when
its semantic contract is discoverable and its intended operation is proven.
