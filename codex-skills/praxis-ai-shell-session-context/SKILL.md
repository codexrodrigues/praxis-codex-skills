---
name: praxis-ai-shell-session-context
description: Use when implementing, auditing, or consuming the `@praxisui/ai` assistant shell, dock, session host or registry, `PraxisAssistantContextSnapshot`, context normalization/redaction, safe summaries, session identity and visibility, governance/risk hints, attachments summaries, or public shell/context exports.
---

# Praxis AI Shell Session Context

Use this skill for the canonical Angular assistant context and session surfaces. The shell is a cockpit that displays and carries governed evidence; it does not become a store for raw business state, a semantic-intent router, or a source of apply permission.

## Canonical Boundary

| Owner | Responsibility |
| --- | --- |
| component lib or host | produces domain-safe context, manifests, metadata/capability references, and a snapshot candidate |
| `assistant-context.models.ts` | validates, redacts, bounds, and normalizes `PraxisAssistantContextSnapshot` |
| `PraxisAssistantSessionRegistryService` | in-memory canonical session registry, identity consistency, visibility, presence, ordering, and session lookup |
| assistant shell, dock, and session host | accessible presentation and interaction over normalized state; no backend policy or primary intent routing |
| `praxis-config-starter` | provider execution, semantic intent, authorization, persisted AI configuration, tool evidence, and apply policy |

Read `projects/praxis-ai/AGENTS.md`, workspace governance, and `codex-rules.md` before editing. Read the producer's local AGENTS, manifest, adapter, README, and focused specs when the change starts outside `@praxisui/ai`.

## Snapshot Is The Only Context Envelope

Create or accept context through `normalizePraxisAssistantContextSnapshot`; do not define a parallel host-specific context type or store arbitrary objects in a session descriptor.

The required identity is the stable tuple `sessionId`, `ownerId`, and `ownerType`. A target, component/route identity, tenant/environment/user scope, mode, manifest reference, resource path, schema fields, safe digests, capabilities, governance/risk hints, attachment summaries, and declared actions are optional evidence.

- A session descriptor that carries a snapshot must match all three identity values exactly. Reject mismatches instead of silently merging owners or sessions.
- Context text is sanitized, redacted, whitespace-normalized, and bounded. Preserve those limits; do not bypass them for a convenient label, diagnostic, or preview.
- The current normalizer bounds context items, schema fields, attachments, capabilities, hints, actions, digest fields, and text length. Expand a limit only with a measured privacy/performance reason and a focused spec.
- Target metadata accepts scalar values only and excludes raw `file`, `blob`, `bytes`, `base64`, `previewUrl`, `currentState`, `runtimeState`, form values, rows, pending patch, diagnostics, payload, and config keys. Keep the blacklist protective rather than copying raw data to a differently named field.
- Attachments in the snapshot are serializable summaries only: identity/name, kind, MIME type, size, source, and preview availability. `File`, bytes, base64, blob URLs, and rich payloads stay on the composer/upload path.
- Digests are summaries, hashes, sources, fields, and counts. A digest is evidence, not a serialized runtime object.

Before adding a snapshot field, inventory existing metadata schemas, `x-ui`, actions, surfaces, capabilities, option sources, manifests, runtime observations, diagnostics, and context hints. Classify the need as `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente`, or `lacuna-real-de-contrato`. Only a real missing canonical evidence path warrants a new public field.

## Session Registry And Presence

Use `PraxisAssistantSessionRegistryService` rather than host-local arrays, service clones, or dock-only state.

- `upsertContextSession` normalizes the snapshot, derives identity and default title/mode, and stores the normalized result.
- The registry has at most one active session. Opening or upserting one as active minimizes every other session, then sorts sessions by `updatedAt`.
- Visibility is `active` or `minimized`; presence is `global-dock` or `origin-anchor`. Presence describes where an affordance belongs, not who owns semantic authority.
- The session host renders minimized sessions by default and omits origin-anchored ones unless explicitly asked. Filter by owner only for presentation; never use a dock filter as an authorization boundary.
- Open, minimize, remove, and lookup context sessions by the canonical session identity. Do not derive a new ID from a title, target label, route string, or prompt text.
- The registry is an Angular in-memory interaction registry. Do not add local persistence, cross-user reuse, or server synchronization as a convenience. A persistence requirement belongs to the canonical backend/config owner and must preserve tenant, user, environment, retention, redaction, and authorization semantics.

## Shell And Dock Materialization

- The shell renders messages, structured assistant content, context items, attachments, quick replies, status, and declared actions. It may choose accessible presentation, icon, tone, layout, and recovery affordances; it must not reinterpret displayed text into a decision.
- Dock tone is derived from shell state (`processing`/`applying`, `review`, `clarification`, error, ready). Keep this projection separate from risk/governance authority.
- Use shell defaults and the shared i18n path for framework chrome. Do not expose raw errors, provider diagnostics, sensitive summaries, or untranslated ad hoc text. Use `praxis-angular-i18n-governance` when changing internal labels.
- Preserve explicit semantic action/quick-reply presentation and the structured payload. Do not parse labels, summaries, chips, resource paths, or context hints with keywords/regex to infer intent, resources, actions, or permissions.
- Runtime observations crossing toward backend grounding remain untrusted frontend evidence; use `praxis-core-widget-observations` and `praxis-ai-turn-orchestration-transport` for their contract and lifecycle.

## Impact Map And Derived Artifacts

For `transversal`, `arquitetural`, or `contrato-publico` work, map the snapshot owner, session/shell consumers, backend/config effects, public exports, manifests/registry, docs/recipes/playgrounds, data sensitivity, and breaking risk before editing.

- Snapshot/model or public export change: review `src/public-api.ts`, direct consumers, docs, generated AI artifacts, and backend contract implications with `praxis-angular-public-api-governance`.
- Producer/manifest change: use `praxis-ai-authoring-manifests` and `praxis-ai-registry-ingestion`; a manifest/registry should refer to canonical evidence rather than copy it into UI state.
- Turn, quick-reply, clarification, or backend context change: use `praxis-ai-turn-orchestration-transport`, `praxis-ai-composer-attachments-quick-replies`, and the config streaming skill.
- UI-only layout or accessibility change: retain the same snapshot and registry ownership; validate the actual shell/dock/host surface and state explicitly why public docs or registry output is unchanged.

## Validation

Run the smallest command covering the changed behavior. This focused suite proves normalizing/redacting context, registry identity/visibility, dock projection, session-host filtering, and shell materialization:

```sh
npm exec -- ng test praxis-ai --watch=false --progress=false \
  --include='projects/praxis-ai/src/lib/core/models/assistant-context.models.spec.ts' \
  --include='projects/praxis-ai/src/lib/core/services/assistant-session-registry.service.spec.ts' \
  --include='projects/praxis-ai/src/lib/ui/assistant-dock/assistant-dock.component.spec.ts' \
  --include='projects/praxis-ai/src/lib/ui/assistant-session-host/assistant-session-host.component.spec.ts' \
  --include='projects/praxis-ai/src/lib/ui/assistant-shell/assistant-shell.component.spec.ts'
```

Exercise normal context session creation; sensitive/raw input redaction; missing or mismatched identity; active-to-minimized transition; origin-anchor filtering; structured action/quick-reply rendering; and a hostile label or context hint that must not create authority. Public API changes also require an AI library build, a direct consumer, and the local-AGENTS E2E evidence. State when docs, examples, manifests, or registry artifacts are unaffected.

## Companion Skills

- `praxis-ai-semantic-intent` for the semantic-routing boundary.
- `praxis-core-runtime-contracts` and `praxis-core-widget-observations` for shared context/observation contracts.
- `praxis-ai-composer-attachments-quick-replies` for live attachments and structured continuations.
- `praxis-ai-turn-orchestration-transport` for a snapshot carried into a backend turn.
- `praxis-ai-backend-config-contracts` and `praxis-config-agentic-authoring-streaming` for backend/config semantics.
- `praxis-angular-i18n-governance`, `praxis-angular-public-api-governance`, and `praxis-angular-validation-gates` for cross-cutting work.
