---
name: praxis-product-evolution
description: Use when a real enterprise screen, workflow, workaround, or repeated customization may reveal a reusable Praxis platform capability: inventory native support, identify the canonical owner, distinguish application need from platform gap, compare abstraction options, and produce an evidence-backed platform RFC or owner follow-up.
---

# Praxis Product Evolution

Use this skill after understanding a concrete screen or workflow and before proposing a new Praxis component, token, config field, metadata shape, preset, public API, or authoring surface. It determines what permanent platform capability would let equivalent consumers build the experience naturally, with less customization and no loss of domain semantics.

This is not a UI redesign skill and not an implementation skill. Use `praxis-ui-product-design` for the experience in the current surface, then use the functional owner skill to implement an approved platform change.

## Outcome Classes

Classify the observed need before suggesting an abstraction:

| Class | Meaning and action |
| --- | --- |
| `application-domain` | Domain-specific workflow/data belongs in the consumer; keep it out of the shared platform. |
| `already-supported` | Existing Praxis component, metadata, composition, editor, token, capability, or guideline covers it; correct adoption/materialization. |
| `supported-partially` | Canonical support exists but misses an evidence-backed projection or small owner improvement; define the temporary bridge and removal trigger. |
| `platform-gap` | No canonical capability can produce the required cross-consumer result; create a governed platform RFC/follow-up. |
| `migration-skill-gap` | The platform is sufficient but migration guidance repeatedly hides its native path; improve the appropriate canonical skill. |

Never treat generic visual structure alone as evidence for a component. A header, grid, card, detail panel, tabs, toolbar, or empty state may be existing composition, metadata, or host domain content.

## Evidence-First Workflow

1. State the user job, observed friction, current workaround, and why it was necessary.
2. Inventory native Praxis support before naming a gap:
   - **Frontend (`@praxisui/*`):** `@praxisui/core`, dynamic fields, form/table/list/charts, navigation (`tabs`, `stepper`, `expansion`), settings/editor patterns, analytical drawer `calculationMemory` (`PraxisAnalyticalDrawerCalculationMemoryContent` / `PraxisAnalyticalDrawerCalculationTrail` + `hydrateRemoteCalculationMemory`, `PLAT-EVO-03` & `20`), contextual Decision Inspector (`providePraxisDecisionInspector`, `PraxisDecisionInspectorSurfaceComponent`, `PraxisRuleDecisionDagComponent`, `X-Ray` `422`/`409` diagnostics in `@praxisui/dynamic-form`), full-stack governed multi-widget pages (8 certified widgets, `PLAT-EVO-11`), manifests, presets, tokens, docs (`AI-ANGULAR-HOST-BLUEPRINT.md`), examples, and existing skills.
   - **Backend & Decision Engines (`praxis-metadata-starter`, `praxis-config-starter`, `praxis-rules-engine`, `praxis-authz-*`):** metadata/schema/`x-ui`, `@CalculationMemory` / `@CalculationTrail` (`CalculationMemoryMetadataResolver`, `PLAT-EVO-20`), `@ReactiveDetermination` / `AnnotationDrivenReactiveDeterminationDefinitionProvider` (`PLAT-EVO-16`), declarative `ResourceStateSnapshot.metadata()` availability keys (`action.<id>.*`, `surface.<id>.*`, `operation.<id>.*`, `PLAT-EVO-01`), `EffectiveDatedResourceSupport` (`PLAT-EVO-02`), `EntityLookupDescriptor.directoryBuilderFromDto` & `ScopedBatchReferenceHydrator` (`PLAT-EVO-09`), `DtoMetadataFactCatalogEnricher` (`PLAT-EVO-06`), `ResourceDecisionPointCatalogService` (`PLAT-EVO-07`), `DomainGovernancePreset` (including `PUBLIC_TRANSPARENCY_REMUNERATION`, `PLAT-EVO-13`), `GovernedRulesStudioAutoConfiguration`, `ProductBaselineGenesisInitializer`, `GovernedHostRuleBundleRuntime`, `GovernedRuleFamilyDescriptor` / `GovernedRuleFamilyRegistry` (`PLAT-EVO-04..05`), `RuleFactCatalogLoader`, `EffectiveDatedIntervalCalculator` (`PLAT-EVO-08`), `ProgressiveBracketAndCapCalculator` (`PLAT-EVO-12`), `EffectiveDatedBracketTable` / `EffectiveDatedMatrixMatcher` / `TriStateOverrideResolver` (`PLAT-EVO-18`), and `AuthzResourceGovernanceSpec.fromAnnotatedResource` (`PLAT-EVO-10`).
3. Identify the canonical owner and classify the need with the table above. If the owner is unclear, stop and use `praxis-angular-agents-governance` plus the relevant functional skill.
4. Compare alternatives in this order: existing composition; declarative layout/presentation schema; metadata/capability/action; preset/template; token/shared style; editor/authoring support; checker/skill; then new public component or contract.
5. Require recurrence across equivalent cases or demonstrable cross-consumer value before a public abstraction. Name at least two consumers or explain the measurable reuse hypothesis and how it will be tested.
6. For `platform-gap`, write a self-contained RFC/follow-up. For every other class, record the native adoption or owner correction and its validation.

## Three Neutral Cases

Use these to test reasoning; none presupposes a new component.

- **Enterprise header:** title, breadcrumb, description, active organization/context, global actions, favorites, help, and status. First test existing page composition, global actions, context metadata, navigation, and tokens. Recommend an Entity Workspace Header only if recurrence proves the same semantic contract cannot emerge from these primitives.
- **Collection with detail:** filters, search, toolbar, table, pagination, selection, and a detail region. First test table/list, dynamic filters, actions, selection, navigation/container composition, and metadata. It may be an existing composition or declarative preset; a Master Detail Workspace needs cross-consumer behavioral evidence.
- **Identity/scope/markers detail:** first test dynamic form/details primitives, presentation schema, metadata, capabilities, and runtime/editor materialization. A dedicated component is justified only when repeated semantics and lifecycle exceed those owners.

At least one forward test must conclude `already-supported` when native evidence warrants it, and at least one must show the threshold for a defensible `platform-gap`.

## Platform RFC / Follow-Up

For a true gap, produce:

- observed evidence, affected job, current workaround, and its cost;
- classification, canonical owner, consumers, and rejected alternatives;
- proposed semantic capability and smallest public/metadata/editor/runtime surface;
- compatibility, beta migration, adoption plan, and workaround-removal plan;
- docs/examples/registry/playground impact and focused validation;
- acceptance criteria reproducible outside the originating private application;
- success metric: reduced screen-specific customization and delivery cost in subsequent equivalent cases.

Do not measure success by abstractions shipped, number of components, or local visual similarity.

## Must-Fail Checks

Stop the recommendation when native capability inventory is absent; owner is unknown; recurrence/cross-consumer value is unsupported; generic layout is the only evidence; compatibility/adoption/removal is missing; acceptance cannot be verified outside the private consumer; or a “gap” is really a migration/UX/materialization problem.

## Handoffs And Validation

- `praxis-ui-product-design`: current-surface UX and visual evidence.
- `praxis-angular-agents-governance`: local owner and rules.
- `praxis-authoring-editors`, `praxis-angular-public-api-governance`, `praxis-angular-validation-gates`, and `praxis-angular-docs-playgrounds`: implementation gates when a capability is approved.
- Functional component, metadata, config, or backend skills: source owner implementation.

For this skill itself, forward-test the three cases with only their evidence, run the focused skill validator, verify manifest hashes/dependencies/cycles, sync the Praxis family, and audit it. The skill remains independent of legacy enterprise hosts, rule engines, private databases, and migration workspaces.
