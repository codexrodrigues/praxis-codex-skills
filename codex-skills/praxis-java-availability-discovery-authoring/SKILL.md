---
name: praxis-java-availability-discovery-authoring
description: Use when implementing, auditing, or migrating Praxis Java actions, surfaces, capabilities, or contextual availability: @WorkflowAction, @UiSurface, ResourceStateSnapshot, availability context/evaluators, collection versus item operations, related-resource discovery, stats/export capability, HATEOAS, cockpit catalogs, and Angular materialization proof.
---

# Praxis Java Availability Discovery Authoring

Author discovery from executable resource operations. A surface describes a
composed business experience; an action describes an explicit command;
capabilities aggregate availability over those contracts. None of them is a
second schema, a button registry, or a frontend visibility workaround.

## Establish The Executable Operation

Inspect the resource key/path, controller method, request/response schema,
service state transition, authorization, entity/view state, existing actions and
surfaces, capabilities snapshot, direct runtime consumer, and focused tests.
Decide whether the need is collection or item scoped, ordinary CRUD, explicit
business command, composed journey, related-resource navigation, stats, export,
or only a runtime materialization gap.

Classify every proposed surface, action, availability input, capability field,
related resource, or catalog shape as `ja-suportado-so-ux`,
`ja-suportado-mal-nomeado-ou-mal-materializado`,
`suportado-parcialmente`, or `lacuna-real-de-contrato`. Do not add discovery
metadata until an actual operation and its canonical schema exist.

## Author Discovery And Availability

1. Keep ordinary create/read/update/delete on the resource baseline. Model a
   stateful or consequential business command as `@WorkflowAction`, with stable
   action ID, scope, input/output schemas, side effect, state and authorization
   conditions, HTTP outcome, and negative path. Do not conceal it in a generic
   PATCH/PUT or infer it from a method name.
2. Model a composed journey as `@UiSurface` over real operations and canonical
   schemas. State its scope, target resource/child binding, supported operations,
   and materialization purpose. Do not use a surface merely to name a route,
   drawer, tab, or button.
3. Keep `@UiSurface` and `@WorkflowAction` separate. Combining them on one
   method enters an explicit conflict-validation zone and requires a documented
   reason plus validation of `praxis.metadata.validation.*` behavior.
4. Define availability from a shared `ResourceStateSnapshot` and contextual
   availability resolvers/evaluators. Resolve state once per resource request and
   reuse it across action, surface, capability, and HATEOAS decisions. Do not
   add repeated N+1 loads or duplicate state predicates in controllers and Angular.
5. Preserve the distinction between absent catalog entry and unavailable
   capability. Catalogs report definitions; `GET /{resource}/capabilities` and
   `GET /{resource}/{id}/capabilities` publish aggregate collection/item snapshots.
   They do not redefine request payloads, schemas, or business rules.
6. Add related-resource surfaces only when child binding and child operations are
   backed by canonical child capabilities. Add stats/export only when actual
   `StatsFieldRegistry` / `StatsSupportMode` or collection export support exists.
7. Keep `RestApiResponse._links` aligned with available operations. Do not replace
   HATEOAS with host-local link fields or force the UI to rebuild URLs from labels.

Read [discovery-decision-matrix.md](references/discovery-decision-matrix.md)
when selecting discovery type, scope, availability evidence, or focused proof.

## Preserve The Platform Boundary

- `praxis-metadata-starter` owns annotations, catalogs, availability
  contexts/evaluators, resource state snapshots, capabilities, HATEOAS, and
  stats/export discovery.
- The host owns verified domain state, command implementation, authorization, and
  snapshot provider inputs. It must not create a separate action catalog or
  availability vocabulary.
- `praxis-ui-angular` consumes catalog/capability projections. It must not decide
  availability from labels, role-name strings, local regexes, or copied states.

Do not resolve primary user intent or choose an action/surface from keywords,
aliases, fuzzy matching, or route fragments. Use resource keys, action IDs,
surface IDs, schemas, capabilities, and governed context; text can only rank
already scoped candidates.

## Prove The Full Discovery Path

Prove definition, scope, positive availability, negative availability, correct
schemas, capability projection, and direct consumer materialization. For an item
decision, prove the state snapshot is shared instead of repeatedly loaded. For a
workflow action, prove execution and rejection in invalid state or authorization.
For related resources, prove binding and child capability alignment.

Use focused action, surface, capability, HATEOAS, stats/export, and cockpit tests
from the starter. Add quickstart HTTP/cockpit proof for public contracts and
review Angular action/surface/resource runtime tests. Review docs or HTTP examples
only when their published catalog/capability claim changes.

## Companion Skills

- `praxis-java-resource-authoring`: operations, resource hierarchy, DTOs, and proof.
- `praxis-metadata-discovery-capabilities`: canonical discovery, availability,
  capabilities, cockpit, stats, and export behavior.
- `praxis-metadata-schema-contracts`: operation schemas and filtered schema.
- `praxis-metadata-resource-baseline`: resource base, `_links`, query, export,
  and stats foundations.
- `praxis-api-quickstart-cockpit-http-validation`: published HTTP/cockpit proof.

Close with the operation-to-discovery matrix, snapshot inputs, availability
decisions, positive/negative evidence, consumer proof, and any platform gap.
Discovery is ready when the runtime can determine what is possible and why,
without reconstructing business semantics locally.
