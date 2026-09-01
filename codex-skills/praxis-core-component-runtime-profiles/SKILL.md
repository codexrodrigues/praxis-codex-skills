---
name: praxis-core-component-runtime-profiles
description: Use when authoring, resolving, auditing, projecting, or enforcing Praxis `ComponentRuntimeProfile` contracts: public-untrusted component execution, structural input constraints, declared runtime effects, CRUD inspect-only, Table/List/Dynamic Form safe profiles, registry projection, or Dynamic Page Studio execution policy. Do not use for ordinary component registry lookup without runtime-policy impact.
---

# Praxis Core Component Runtime Profiles

Use this skill when a component owner must describe which concrete JSON input
shapes are safe to materialize and which effects those shapes may attempt. A
runtime profile is owner-authored evidence for host policy; it never grants
authorization or replaces backend capabilities.

## Canonical Owner And Source Audit

`@praxisui/core` owns the public model and resolver. Inspect:

- `projects/praxis-core/AGENTS.md`
- `src/lib/models/component-runtime-profile.model.ts`
- `src/lib/services/component-runtime-profile.service.ts` and spec
- `src/lib/models/component-doc-metadata.interface.ts`
- `src/lib/services/component-metadata-registry.service.ts` and spec
- `src/lib/ai/component-registry-ai-capabilities.ts`
- `src/public-api.ts`

Then inspect the owning component metadata/profile specs and the real host
policy. Current reference consumers include CRUD, Dynamic Form, List, Table,
Page Builder, the AI registry generator, and Dynamic Page Studio.

## Contract Boundary

- `ComponentDocMeta.runtimeProfiles` is the component owner's declaration.
- `ComponentRuntimeProfileService` resolves the first profile whose complete
  structural constraints match the supplied inputs and reports mismatches.
- `audience: 'public-untrusted'` names the audited trust boundary; it does not
  turn arbitrary public JSON into trusted config.
- `effects` must enumerate the complete effect set for the matched shape.
  `effects: []` means local-only behavior.
- A host evaluates its own execution policy and resolves current backend
  capabilities independently. Profile match is necessary evidence where the
  host requires it, never sufficient authorization.

Do not infer safety from component id, selector, labels, prompts, example names,
or the absence of visible buttons. Do not maintain a host-owned allowlist that
redefines the owner's constraints or effects.

## Author A Profile

1. Inventory the actual runtime reads, writes, navigation, persistence, global
   actions, hooks, renderers, URLs, and compatibility fallbacks for the input
   shape.
2. Classify existing support before adding a public field. Prefer an owner
   profile over a Studio/host-local policy only when the component can state the
   effect truth canonically.
3. Give the profile a stable component-scoped id and the narrowest audited
   audience.
4. Close the input shape with explicit constraints. Use `$` and `keys-subset`
   for bounded records, wildcard paths for arrays, and allow/deny operators for
   values that change effects. Missing nested values must not accidentally pass
   an allowlist.
5. Declare every possible effect with canonical operation ids, exact HTTP
   methods, resource-path inputs, suffixes, and fallback roles. A fallback is
   still an effect and still requires host/backend permission.
6. Publish through the owning `ComponentDocMeta`; preserve profiles through
   defensive registry cloning, generated component docs, registry ingestion,
   AI grounding, and public package exports where those consumers need them.
7. Update the component runtime so a safe profile is behaviorally true. A
   metadata-only claim that runtime can escape the declared shape fails review.

## Reference Profiles

- CRUD `public-local-inspect-only` requires
  `metadata.interactionMode='inspect-only'`, inline data, volatile persistence,
  no resource paths/actions/forms/open modes/hooks, a bounded Table config, and
  `effects: []`. Residual create/view/edit/delete events must fail closed.
- Local Table/List/Form profiles require local data or a closed static config
  and prohibit unreviewed URL-, renderer-, hook-, or persistence-bearing keys.
- Remote-read profiles enumerate schema/filter/get compatibility attempts and
  keep capability resolution outside the profile.

These are patterns to inspect, not aliases to copy between libraries. Each
component owner must publish the effect truth for its own runtime.

## Proof

Prove three paths:

1. Happy: a closed owner-authored input matches the expected profile and the
   runtime performs only its declared effects.
2. Risk: a required input is absent or one constraint fails; resolution returns
   no match plus useful mismatches without falling back to a broader profile.
3. Adversarial: extra keys, unsafe renderers/URLs/hooks, remote paths in a local
   profile, or manually dispatched CRUD actions are rejected and produce no
   undeclared network/navigation/persistence/global-action effect.

Minimum Angular gates:

```bash
npm run test:core -- --include=projects/praxis-core/src/lib/services/component-runtime-profile.service.spec.ts --include=projects/praxis-core/src/lib/services/component-metadata-registry.service.spec.ts
npm run build:praxis-core
```

Add the owning component metadata/runtime specs and one real policy consumer.
For public registry changes, run `npm run generate:registry:ingestion` and
validate the projected entry. For Studio execution-policy changes, run its
focused service/network-policy specs and `e2e/dynamic-page-studio.spec.ts` when
browser behavior changed.

Review public API, README/JSON API docs, registry assets, Studio examples, and
host guidance. State explicitly when a derived artifact is unaffected.

## Companion Skills

- `praxis-core-component-registry-contracts`: registry identity, cloning, and projection fidelity.
- `praxis-angular-public-api-governance`: exported model/service and direct-consumer proof.
- `praxis-crud-runtime-openmodes`, `praxis-list-runtime-data`, `praxis-table-runtime-data`, and `praxis-form-schema-runtime-modes`: owner runtime truth.
- `praxis-ai-registry-ingestion`: generated component/AI registry projection.
- `praxis-landing-dynamic-page-studio`: public Studio policy and user-facing proof.

