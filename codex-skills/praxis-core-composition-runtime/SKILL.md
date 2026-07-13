---
name: praxis-core-composition-runtime
description: Use when Codex must inspect, change, or rely on @praxisui/core composition and widget runtime contracts: DynamicWidgetPageComponent, widget definitions, widget events, widget shell, composition links, nested ports, connection/link execution, transform runtime, surface hosts, related-resource outlets, runtime observations, or dynamic page materialization.
---

# Praxis Core Composition Runtime

Use this skill for `@praxisui/core` composition, widget, dynamic page, connection, and surface-host runtime contracts.

This area materializes governed component and page decisions. It should not become a local page-builder dialect, host-only composition language, or keyword-routed action system. Page Builder and Visual Builder may author decisions, but core owns the shared runtime structures that execute them.

## Source Audit

Inspect the affected source before changing guidance or code:

- `projects/praxis-core/AGENTS.md`
- `projects/praxis-core/src/public-api.ts` when composition models, widget contracts, ports, surface hosts, runtime observations, or composition services are exported or public consumption changes
- `projects/praxis-core/docs/connection-editor.md`
- `projects/praxis-core/docs/rfc-dynamic-page-canvas-runtime.md`
- `projects/praxis-core/src/lib/composition/**`
- `projects/praxis-core/src/lib/widgets/**`
- `projects/praxis-core/src/lib/surfaces/praxis-surface-host.component.ts`
- `projects/praxis-core/src/lib/surfaces/praxis-related-resource-outlet.component.ts`
- `projects/praxis-core/src/lib/models/composition-*.ts`
- `projects/praxis-core/src/lib/models/port-contract.model.ts`
- `projects/praxis-core/src/lib/models/runtime-component-observation.model.ts`
- `projects/praxis-core/src/lib/services/runtime-component-observation-registry.service.ts`
- `projects/praxis-core/src/lib/services/surface-binding-runtime.service.ts`

Read the focused specs for composition runtime, link execution, nested ports, widget loader, dynamic widget page, runtime observations, and surface hosts before deciding a contract is missing.

## Canonical Boundary

Core owns:

- `WidgetDefinition`, `WidgetPageDefinition`, widget shell contracts, widget events, nested widget config access
- dynamic widget loading and materialized widget runtime
- composition link model, transform pipeline, diagnostics, runtime traces, link execution, nested ports
- surface host and related-resource outlet runtime
- runtime component observation and event propagation
- bridge points used by Page Builder agentic authoring, including observations, surface handoff, and component-port grounding

Page Builder, Visual Builder, component libraries, and host apps consume these contracts. They should not redefine the same config/event/link semantics locally.

## Canonical Read And Execution Path

- Persist new page composition in `WidgetPageDefinition.composition.links`. `page.connections` is legacy and `DynamicWidgetPageComponent` rejects it; do not save both shapes or reintroduce a compatibility branch in a host.
- Use `WidgetPageCompositionFactory` to materialize widget order, indexed widgets, links, state, derived definitions, and context before bootstrapping `CompositionRuntimeEngine`.
- Treat `CompositionRuntimeEngine.bootstrap()` as semantic validation plus state materialization. Blocking diagnostics produce a `degraded` snapshot with trace evidence; do not convert every diagnostic into an exception or silently mark the page ready.
- Dispatch a `CompositionDispatchEvent` from an exact canonical endpoint. Matching includes owner widget, port, direction, and `nestedPath` when present. Let the engine execute condition, transform, policy, target delivery, state update, diagnostics, and trace as one cycle.
- Consume the immutable `RuntimeSnapshot` from the facade/store as execution evidence. Do not maintain a second host state for link status, trace, or diagnostics.
- Treat feedback-cycle detection as part of semantic validation and runtime safety, not as an editor-only lint. Unguarded cycles produce `SEMANTIC_FEEDBACK_CYCLE_UNGUARDED`, degrade bootstrap, and cause involved matched links to be skipped during dispatch with `RUNTIME_FEEDBACK_CYCLE_BLOCKED`; unrelated matched links may still execute.
- An intentional feedback loop must be explicit and guarded on every link in the cycle: use `metadata.tags: ['intentional-feedback']` plus at least one canonical guard per link (`condition`, `policy.distinct`, `policy.distinctBy`, or `policy.debounceMs`). Guarded intentional cycles produce `SEMANTIC_FEEDBACK_CYCLE_GUARDED` warnings, not blocking errors. Do not suppress cycle diagnostics or invent host-local loop breakers.

Legacy migration is an explicit ingress concern. Use `CompositionLinkLegacyMigrator` for supported legacy condition/policy shapes, then persist the canonical result. Unsupported legacy conditions fail explicitly; do not keep an open-ended legacy interpreter in runtime code.

## Implemented Contract Limits

Do not infer executable support from a public union or serialized field alone:

- Link policy currently executes `missingValuePolicy`, `distinct`, `distinctBy`, and `debounceMs`.
- `LinkPolicy.delivery` and `LinkPolicy.errorPolicy` are modeled, serialized, and authorable, but the core executor does not currently schedule `microtask`/`batched` delivery or apply `drop`/`halt-page`. Classify behavior that depends on them as `suportado-parcialmente` and open a core follow-up instead of simulating it in a host.
- The stable transform catalog currently executes `identity`, `constant`, `pick-path`, `template`, `object-template`, `array-template`, `coalesce`, `merge-objects`, and `select-case`. Other `TransformKind` members are declared future surface and produce `RUNTIME_TRANSFORM_UNSUPPORTED`; never create a host transform dialect to bypass the catalog. For value formatting, first inventory the canonical derived-state `format-value` operator in `WidgetPageStateRuntimeService` instead of assuming the pipeline transform with the same name is executable.
- A link-level `condition` is canonical Json Logic with explicit roots and no implicit root. A transform step `when` currently permits the implicit `source` root. Preserve this distinction when validating or migrating conditions.

For nested component ports, resolve the child through `NestedPortCatalogService`, component metadata, and a `nestedPath` that terminates in a stable `childWidgetKey`. New nested endpoints must not use `bindingPath`; that field is only a migration bridge. `NestedWidgetConfigAccessor` currently materializes nested widget inputs for tabs/nav and expansion containers. Other path segment kinds in the model require concrete proof in the owning container runtime; the union alone does not prove that input patching works.

Runtime component observations are redacted, time-bounded, untrusted grounding evidence. They may expose active page/widget refs, declared link ids, valid selected widget, surfaces, actions, warnings, and digests. They must omit business state values, full inputs, raw events, rendered DOM, and intent decisions. Never route intent or authorize an action from an observation.

## Decision Rules

- If the task is about authoring a page/editor graph, use the builder skill as the functional owner and this skill for the runtime contract.
- If the task is about Page Builder surface handoff or runtime observation evidence, keep Page Builder as the authoring owner and core as the execution/trust-boundary owner.
- If the task is specifically about `@praxisui/page-builder`, pair with `praxis-page-builder-composition` for palette, canvas, graph, connection editor, and page-builder-owned authoring semantics.
- If the task is about rich-content widgets, presets, host-mediated actions, or `RichContentDocument` materialization inside dynamic pages, pair with `praxis-rich-content-runtime` and `praxis-rich-content-integration-adapters`.
- If the task is about container widgets such as `@praxisui/tabs`, `@praxisui/stepper`, or `@praxisui/expansion`, pair with the owning runtime skill before changing widget event paths, nested widgets, registry metadata, or dynamic page materialization.
- If the task is about `SettingsValueProvider`, apply/save/reset, or config editor round-trip, use `praxis-authoring-editors` as well.
- If the task is about a specific widget's visual/product UX, use `praxis-ui-product-design` with the owning component skill.
- If a host composes a page by copying local event buses, action routers, or link transforms, prefer the core composition runtime or open a core follow-up.
- Do not persist local command strings such as `showAlert:...`, `surface.open:...`, or `navigate:...` when `GlobalActionRef`, surface metadata, or composition links can express the decision.

## Runtime Evidence

Before declaring composition complete, identify:

- source of the widget/component catalog entry
- canonical config shape being materialized
- event and output contract
- link or transform that moves data between widgets
- diagnostics when a target, port, or transform cannot resolve
- runtime observation evidence when behavior is user-visible
- redaction/serializability proof when observations feed AI or diagnostics
- public API and AI manifest impact when the component is public

Classify gaps before adding contracts:

- `ja-suportado-so-ux`: the link executes and trace/diagnostics exist, but the host does not present them.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: the page still saves `connections`, uses `bindingPath` for new nested links, hides feedback-cycle diagnostics, or duplicates runtime snapshot state.
- `suportado-parcialmente`: the public model contains a policy, transform, or nested segment that the executor/accessor does not yet materialize.
- `lacuna-real-de-contrato`: no canonical endpoint, port metadata, transform, action, surface, or diagnostic can represent the required behavior.

Only the last category justifies a new shared contract. Extend the canonical owner and its consumers together; do not add an event bus, command-string router, custom transform registry, or host-only nested path convention.

## Operational Proof

Before declaring composition guidance current, prove:

1. Happy path: a widget output matches one `composition.links` source, passes a supported transform, delivers to a canonical port or writable state, and records link status plus trace phases.
2. Risk path: a missing nested widget/port, incompatible semantic kind, invalid condition, unsupported transform, derived-state write, or unguarded feedback cycle produces the expected structured diagnostic and a non-divergent snapshot.
3. Feedback path: prove an unguarded component/component or component/state/component cycle degrades bootstrap and skips involved matched links with `RUNTIME_FEEDBACK_CYCLE_BLOCKED`; prove an intentional guarded cycle remains a warning by using `intentional-feedback` plus canonical guards.
4. Adversarial path: reject `page.connections`, new `bindingPath` links, local event buses, command strings, raw callback transforms, host-local loop breakers, and host implementations of unexecuted policy fields.

Use a focused Angular gate from the `praxis-ui-angular` root:

```bash
npm run test:core -- \
  --include=projects/praxis-core/src/lib/composition/composition-runtime.engine.spec.ts \
  --include=projects/praxis-core/src/lib/composition/composition-runtime.facade.spec.ts \
  --include=projects/praxis-core/src/lib/composition/link-executor.service.spec.ts \
  --include=projects/praxis-core/src/lib/composition/transform-runtime.service.spec.ts \
  --include=projects/praxis-core/src/lib/composition/composition-validator.service.spec.ts \
  --include=projects/praxis-core/src/lib/composition/composition-link-legacy-migrator.spec.ts \
  --include=projects/praxis-core/src/lib/composition/nested-port-catalog.service.spec.ts \
  --include=projects/praxis-core/src/lib/services/surface-binding-runtime.service.spec.ts \
  --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page.component.spec.ts \
  --include=projects/praxis-core/src/lib/widgets/dynamic-widget-loader.directive.spec.ts \
  --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-runtime-observation.spec.ts \
  --include=projects/praxis-core/src/lib/widgets/dynamic-widget-page-record-surface-open.spec.ts \
  --include=projects/praxis-core/src/lib/services/runtime-component-observation-registry.service.spec.ts \
  --include=projects/praxis-core/src/lib/surfaces/praxis-surface-host.component.spec.ts \
  --include=projects/praxis-core/src/lib/surfaces/praxis-related-resource-outlet.component.spec.ts
npm run build:praxis-core
```

These gates prove the shared Angular runtime. Record Page Builder/Visual Builder authoring, owning-container nested paths, real global-action side effects, metadata-backed surface discovery, and browser UX as unverified unless their focused consumers were also exercised.

When the change is authored or exercised through Page Builder, add the focused authoring proof:

```bash
npm run ng -- test praxis-page-builder --watch=false --progress=false \
  --include=projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor.component.spec.ts \
  --include=projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor-graph.util.spec.ts \
  --include=projects/praxis-page-builder/src/lib/editor/connection-editor/connection-editor-trace.util.spec.ts \
  --include=projects/praxis-page-builder/src/lib/ai/page-builder-ui-composition-plan.spec.ts \
  --include=projects/praxis-page-builder/src/lib/ai/page-builder-agentic-authoring-turn-flow.spec.ts
```

When nested composition flows through container widgets, add the owning-container proof instead of inferring from the core union alone:

```bash
npm run ng -- test praxis-tabs --watch=false --progress=false --include=projects/praxis-tabs/src/lib/praxis-tabs-widget-event.spec.ts --include=projects/praxis-tabs/src/lib/praxis-tabs-widget-config-editor.spec.ts
npm run ng -- test praxis-stepper --watch=false --progress=false --include=projects/praxis-stepper/src/lib/praxis-stepper-widget-config-editor.spec.ts
npm run ng -- test praxis-expansion --watch=false --progress=false --include=projects/praxis-expansion/src/lib/praxis-expansion-widget-config-editor.spec.ts
```

## Validation Guidance

Prefer focused specs:

- composition runtime engine/facade/store specs
- composition validator specs for semantic compatibility, nested endpoints, and feedback-cycle diagnostics
- link executor and transform runtime specs
- nested port catalog specs
- dynamic widget loader and dynamic widget page specs
- widget recipe specs for rich table, nested path, actions workspace, and record surface open
- surface host and related-resource outlet specs

For visual/editor flows, add screenshot or browser validation through the official host route when feasible.

## Companion Skills

- Use `praxis-core-runtime-contracts` for public API, shared models, tokens, i18n, logging, and providers.
- Use `praxis-core-widget-observations` for dynamic widget models, loader, widget events, dynamic widget page, runtime observations, observation registry, and redaction/serializability proof.
- Use `praxis-core-global-action-payloads` when widget events or composition links execute structured global actions, payloadExpr, `surface.result`, or `dynamicPage.composition.dispatch`.
- Use `praxis-core-surface-materialization` when composition opens resource-derived surfaces or materialized related-resource payloads.
- Use `praxis-core-component-registry-contracts` when composition depends on component metadata registry entries, ports, insertion presets, or AI component context.
- Use `praxis-core-global-actions-metadata` for the broader global action and metadata-services umbrella.
- Use `praxis-core-providers-bootstrap` when composition runtime requires provider, token, or registry wiring.
- Use `praxis-authoring-editors` for editor/runtime round-trip and Settings Panel behavior.
- Use `praxis-page-builder-composition`, `praxis-page-builder-authoring`, and `praxis-page-builder-ai-agentic` when the shared runtime contract is being authored or exercised through `@praxisui/page-builder`.
- Use `praxis-tabs-runtime-authoring`, `praxis-stepper-wizard-runtime`, and `praxis-expansion-runtime-panels` when composition flows through those container widgets; use `praxis-navigation-containers-ai-validation` when their AI manifests, capabilities, context packs, or registry projection are involved.
- Use `praxis-navigation-container-composition-events` for cross-container nested widget event paths, dynamic page embedding, lazy container materialization, and composition-link proof across tabs, stepper/wizard, and expansion.
- Use `praxis-rich-content-runtime`, `praxis-rich-content-integration-adapters`, and `praxis-rich-content-ai-security-validation` when composition flows through structured rich-content documents or rich-content widgets.
- Use `praxis-ui-product-design` for visual hierarchy, accessibility, and screenshot QA.
