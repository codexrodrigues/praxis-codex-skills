# Resource Delivery Matrix

## Resource Packet

Prepare this compact packet before implementation. Unknown business meaning is a
discovery task, not permission to invent metadata.

| Decision | Evidence to record |
| --- | --- |
| Domain job and owner | Product documentation, legacy/runtime behavior, and responsible resource key |
| Resource mode | Read-only, mutable, create/update-only, or unit-delete and why |
| Identity | Path constant, `resourceKey`, API group, ID type, route-owned technical keys, mapper preservation rule, and compatibility impact |
| Operations | Query, get, create, update, delete, explicit actions, export, stats |
| DTO semantics | Response/create/update/filter/command fields, business meaning, governance, AI exposure |
| Relations | Source key, option type, filter/by-ids reload, display and dependency policy |
| Discovery | Surfaces, actions, capabilities, availability and related-resource needs |
| Proof | Focused test, HTTP evidence, direct runtime consumer, cleanup for data mutation |

## Feature Decision Matrix

| Need | Canonical route | Do not use |
| --- | --- | --- |
| Ordinary record lifecycle | Resource base and operation DTOs | Bespoke controller envelope or generic map payload |
| Business transition | `@WorkflowAction` and command DTO | Hidden PATCH/PUT convention |
| Composed journey | `@UiSurface` over real operations | Decorative frontend route metadata |
| Relationship selection | Registered option source and lookup contract | Host autocomplete endpoint or opaque foreign key only |
| Context-dependent availability | Resource state snapshot and capability/action/surface evaluators | N+1 controller checks or UI-only disable rule |
| Aggregation or download | Canonical stats/export support | Browser-calculated metric or ungoverned export route |
| Configurable domain policy | Config-starter applied materialization | Host-local rule engine or assistant text parsing |
| Mutable resource identity | Load by route id, map only editable fields, and preserve every route-owned technical key | Copying payload `id`, repairing identity in Angular, or restoring it after an unsafe merge |

## Identity-Preserving Update Packet

For every mutable resource, classify fields before implementing the mapper:

| Field class | Examples | Update authority |
| --- | --- | --- |
| Route-owned technical identity | JPA `id`, tenant partition key, immutable parent/resource key | Loaded entity and authorized route context only; mapper ignores payload values |
| Editable business state | Name, description, status when the operation permits it | Operation-specific update DTO plus service validation |
| Server-managed state | Audit timestamps, version, derived totals | Service, persistence, or governed domain operation; never copied blindly from the DTO |

A MapStruct update contract should make the exclusion visible at the mapper
boundary, for example:

```java
@Mapping(target = "id", ignore = true)
@Mapping(target = "version", ignore = true)
void updateEntity(UpdateRequest source, @MappingTarget Entity target);
```

The exact keys are resource-specific. The invariant is not the annotation
syntax: payload conversion must be unable to clear or replace identity already
resolved by the route. Record the equivalent deliberate contract when the
mapper is handwritten or uses another generator.

## Minimum Proof Selection

Use the narrowest applicable proof first, then expand only when the change
crosses the contract boundary.

| Changed surface | Minimum proof |
| --- | --- |
| Resource base or `_links` | Resource controller/service tests for the selected base |
| Mutable mapper or scaffold | Update with absent and divergent payload ids, followed by read; generated-source assertion rejects assignment to route-owned technical keys |
| DTO/schema contract | Filtered schema and canonical operation resolver tests |
| Actions or surfaces | Registry, availability, catalog, and negative-path tests |
| Capabilities | Capability consistency and hypermedia discovery tests |
| Option source | Filter and by-ids integration proof, including dependencies when published |
| Public host contract | Quickstart migration/pilot HTTP proof plus direct runtime review |

Do not run a broad suite in place of a missing focused assertion. A broad green
build cannot prove an action, option reload, availability decision, or schema
projection that its tests never exercise.
