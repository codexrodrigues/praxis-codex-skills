# Discovery Decision Matrix

## Choose The Contract

| Need | Canonical contract | Do not use |
| --- | --- | --- |
| Standard resource lifecycle | Resource operation and `_links` | Workflow action for ordinary CRUD |
| Explicit business transition | `@WorkflowAction` with command schemas | Hidden PATCH/PUT or client-side state flip |
| Composed task/journey | `@UiSurface` over real operations | Decorative route or button metadata |
| Current allowed operations | Resource/item capability snapshot | Second schema or manually assembled UI policy |
| Child navigation/workflow | Related-resource surface plus child capabilities | Parent endpoint that guesses child permissions |
| Aggregation/download | Stats/export support and capability discovery | Affordance without backend contract |

## Scope And Availability Packet

| Decision | Evidence |
| --- | --- |
| Scope | Collection or item resource identity and target operation |
| Schema | Existing request/response schema references |
| State | Snapshot fields needed for lifecycle/eligibility decision |
| Authorization | Verified host enforcement and availability consequence |
| Positive case | Fixture/state where it appears and executes |
| Negative case | Fixture/state where it is absent or unavailable and execution rejects |
| Consumer | Capability/catalog/`_links` and Angular or cockpit materialization path |

## Minimum Proof

| Change | Minimum proof |
| --- | --- |
| Surface | Registry, evaluator, catalog, schema reference, positive/negative E2E |
| Action | Registry, state/authorization evaluator, catalog, execution, rejection E2E |
| Capability | Collection/item consistency, hypermedia discovery, shared-state behavior |
| Related resource | Parent binding and supported child capability proof |
| Stats/export | Registry/support mode and collection capability proof |

Do not call an affordance unavailable merely because a consumer chooses not to
render it. Availability remains a canonical backend decision with an observable
reason and operation boundary.
