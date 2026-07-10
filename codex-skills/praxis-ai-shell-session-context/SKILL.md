---
name: praxis-ai-shell-session-context
description: Use when changing or reviewing the `@praxisui/ai` assistant shell, dock, session host, session registry, `PraxisAssistantContextSnapshot`, context normalization, safe summaries, governance/risk hints, session identity, or public shell/context exports.
---

# Praxis AI Shell Session Context

Use this skill when the task is about the assistant surface and the canonical context snapshot it displays or carries. The shell is a cockpit for governed decisions, not the source of component business rules or primary intent routing.

## Canonical Boundary

- `@praxisui/ai` owns `PraxisAiAssistantShellComponent`, `PraxisAiAssistantDockComponent`, `PraxisAiAssistantSessionHostComponent`, `PraxisAssistantSessionRegistryService`, shell types, and assistant context normalization.
- Component libraries and host projects own domain semantics, authoring manifests, runtime state, and adapters that produce safe context.
- Praxis Config backend and governed AI contracts own provider execution, semantic intent resolution, and persisted AI configuration.
- `PraxisAssistantContextSnapshot` is the UI-agnostic context envelope. It may expose identity, target, safe context items, schema field summaries, data/runtime digests, capability refs, governance hints, risk hints, attachment summaries, and declared actions.

## Required Inventory

Inspect:

- `projects/praxis-ai/AGENTS.md`
- `projects/praxis-ai/README.md`
- `src/public-api.ts`
- `src/lib/core/models/assistant-context.models.ts`
- `src/lib/core/services/assistant-session-registry.service.ts`
- `src/lib/ui/assistant-shell/**`
- `src/lib/ui/assistant-dock/**`
- `src/lib/ui/assistant-session-host/**`
- focused specs for context normalization, shell, dock, and session host

For producer changes, also inspect the component adapter, manifest, or host code that builds the snapshot.

## Context Rules

- Always normalize snapshots through the canonical context helpers before storing or rendering them.
- Preserve the identity tuple `id`, `ownerType`, and `ownerId`; session registry descriptors must match the normalized snapshot identity.
- Keep session state explicit: active/minimized visibility, global-dock/origin-anchor presence, title, summary, mode, state, and timestamps.
- Use safe summaries and digests. Do not place full configs, form values, table rows, runtime state, pending patches, files, blob URLs, bytes, base64, or raw diagnostics in context.
- Governance hints and risk hints are display/grounding evidence. They do not authorize a patch by themselves.
- Runtime component observations are untrusted frontend evidence. Use `praxis-core-widget-observations` and the turn/transport skills when they cross into backend grounding.
- Root `public-api.ts` must expose intentional `@praxisui/ai` surfaces only and must not become a transitive facade for `@praxisui/core`.

## Aderencia Before Contract Changes

Classify requested changes before adding fields:

- `ja-suportado-so-ux`: snapshot or session data exists but shell/dock/session host does not render it well.
- `ja-suportado-mal-nomeado-ou-mal-materializado`: existing field is present but label, title, summary, or projection is misleading.
- `suportado-parcialmente`: snapshot carries only safe digest/evidence and needs producer/runtime adjustment.
- `lacuna-real-de-contrato`: a correct UX or backend grounding cannot be implemented because the canonical snapshot lacks required evidence.

Only create a new public field for `lacuna-real-de-contrato`, and name the source of truth, consumers, derived artifacts, and validation that prove it.

## Validation

Use the smallest focused checks:

- context helpers: focused assistant context spec
- session behavior: `assistant-session-registry.service.spec.ts`, `assistant-session-host.component.spec.ts`, `assistant-dock.component.spec.ts`
- shell rendering and accessibility: `assistant-shell.component.spec.ts`
- public exports: build `praxis-ai` and a direct consumer when `public-api.ts` changes

State explicitly when no derived docs, examples, manifests, or registry artifacts need updates.
