---
name: praxis-ai-semantic-intent
description: Use when auditing or changing Praxis AI intent handling, governed decision routing, authoring scope policy, consult/edit boundaries, quick reply semantics, clarification handling, semantic grounding, runtime observation grounding, or any assistant code that might route user intent through local keywords, regexes, aliases, fuzzy matching, or command strings.
---

# Praxis AI Semantic Intent

Use this skill to enforce the Praxis rule: user intent is resolved semantically through governed AI/LLM contracts, manifests, capabilities, catalogs, context, and declared tools. Browser keyword routing is not the primary decision mechanism.

Pair with `praxis-ai-composer-attachments-quick-replies` when quick replies, recommended intents, or clarification options carry semantic payloads; pair with `praxis-ai-turn-orchestration-transport` when the resolved intent moves through turn streams; pair with `praxis-ai-shell-session-context` when context snapshots or session identity affect grounding.

## Canonical Boundary

- `@praxisui/ai` may carry context, display state, ask clarifications, and materialize resolved decisions.
- `praxis-config-starter` owns the backend semantic intent resolver, LLM fast intent pass,
  pre-intent tool planning, governed resource discovery evidence, Domain Catalog grounding,
  semantic decision policy, repair classification, and turn-level quick reply payloads.
- The backend intent resolver currently has a fast LLM pass and a full LLM pass. The fast pass is valid only when it returns a complete route/resource/visualization decision; otherwise the resolver must fall back to the full semantic pass or a safe unresolved/provider-error result, never to a materializing lexical route.
- Backend/LLM/tool contracts decide the primary authoring intent; Angular may only send
  structured context and render/materialize the returned semantic decision.
- Local text matching may rank candidates only after semantic scope is resolved and must not decide intent.
- When a needed tool or contract is missing, model or create the canonical tool/contract; do not replace it with local keyword heuristics.

## Required Inventory

Inspect:

- `projects/praxis-ai/AGENTS.md`
- `src/lib/core/authoring/governed-decision-routing.ts`
- `src/lib/core/authoring/authoring-scope-policy.ts`
- their specs
- assistant quick reply utilities and turn models
- AI adapters/context packs in the affected component lib
- the component authoring manifest that should govern the intent
- `praxis-config-starter/AGENTS.md`
- `AgenticAuthoringIntentResolverService`
- `AgenticAuthoringLlmIntentResolverService`
- `AgenticAuthoringLlmPreIntentToolPlanningService`
- `AgenticAuthoringSemanticDecisionPolicy`
- `AgenticAuthoringCandidateProvenancePolicy`
- `AgenticAuthoringRepairClassificationPolicy`
- `AgenticAuthoringDomainCatalogCandidateEnhancer`
- `AgenticAuthoringDomainCatalogHints`
- `AgenticAuthoringQuickReply`
- `praxis-api-quickstart/docs/AGENTIC-AUTHORING-SEVEN-STEP-REVIEW-PROMPT.md`
- focused backend tests for intent resolver, LLM intent, pre-intent tool planning,
  semantic decision policy, Domain Catalog grounding, provenance, repair classification,
  and quick reply canonicalization.

Also inspect direct consumers of the shared policy when the change can alter
cross-library routing. Current consumers include manual form, list, table,
expansion, tabs, stepper, and page builder authoring flows.

## Classify Text Handling Before Changing It

Classify every keyword, regex, alias, normalization, or fuzzy match by the
decision it controls:

- **Primary intent routing**: decides consult versus edit, selects an operation,
  chooses a governed handoff, or authorizes a patch. This is prohibited locally.
- **Post-resolution grounding**: ranks a field, option, resource, or target only
  after canonical semantic context resolved the scope. This is allowed only when
  the final decision remains governed and the candidate source is canonical.
- **Interaction materialization**: matches a returned clarification option,
  normalizes a URL, formats a label, or selects presentation. This does not decide
  primary intent, but must preserve the returned semantic payload.

Do not report all uses of `includes()` or regex as equivalent. Record which
decision each match controls and whether canonical context exists before it runs.

Treat component identity separately from user intent. The assistant currently
falls back from explicit `adapter.componentId` to text matching on
`adapter.componentName`. This does not classify the prompt, but it is weak
materialization of canonical identity. Prefer explicit `componentId` and
`componentType`; do not extend the name-based fallback to new components.

Treat manifest target resolvers separately from intent routing. Backend resolvers such as
`normalized-control-type-alias` run only after the semantic resolver has selected a component
manifest operation such as `controlType.alias.add` or `controlType.alias.remove`. They may normalize
and match a target inside the operation's config, but they must not be reused as a pre-manifest
shortcut for deciding that the user's prompt is an alias-authoring request.

Treat backend lexical checks with the same care. Residual `contains`, prompt
shape checks, provider-error string classification, and artifact-name matching
may support diagnostics, provider failure classification, post-resolution
candidate ranking, or guarded compatibility only when semantic scope/evidence
already exists. `AgenticAuthoringSemanticDecisionPolicy` still inspects prompt
shape for materialization nuance, optional data source hints, broad discovery,
and artifact-kind repair; those branches are acceptable only when combined with
LLM resolution, selected/context-hint candidates, governed resource confirmation,
or explicit clarification/resource-choice evidence. They must not become a new
primary intent route. When auditing, record which semantic evidence enables each
lexical branch, such as LLM-authored resource focus, Domain Catalog grounding,
semantic retrieval, quick-reply context, selected candidate evidence, or
authoring scope policy.

Audit intent overrides through candidate provenance, not only through the route
label. `domainCatalog.recommendedAuthoringFlow`, pre-intent tool plans, repair
classification, deterministic overrides, and quick-reply continuations must be
backed by explicit semantic evidence such as `domain_catalog`,
`semantic_retrieval`, `context_hint`, `deterministic_override` with prior LLM/tool
failure, selected candidate evidence, governed resource confirmation, or
structured `semanticDecision`. `lexical_fallback`, `unknown`, `none`, stale
Domain Catalog hints, or copied display labels cannot by themselves authorize a
shared-rule route, component edit, preview, apply, or repair retry.

Treat missing registry/RAG/provider projection evidence as unresolved grounding,
not as semantic absence. If component registry, ingestion corpus, backend snapshot,
runtime observation, or package AI asset evidence is missing or lossy, the resolver
must re-ground through the canonical source/provider/backend contract or ask a
clarification. Do not use the missing projection to infer that a component,
capability, manifest operation, resource, surface, action, or permission does not
exist, and do not recover by keyword-routing the prompt.

When `recommendedAuthoringFlow=shared_rule_authoring` conflicts with an explicit
local/editorial UI composition request, the backend semantic resolver must decide
the conflict using the current prompt, selected candidate, and provenance. Angular
may honor the returned structured hint only as already-governed context; it must
not use the hint as a browser-side shortcut that bypasses the backend decision,
manifest operation evidence, or clarification flow.

Provider failures, invalid or partial LLM JSON, unsupported route classes, and
low confidence must fail closed: unresolved decision, `provider_error` or
equivalent safe follow-up, user-facing clarification, sanitized warnings, and
`canApply=false`. Do not leak provider bodies, API keys, quota details, stack
traces, or internal diagnostics into assistant text or quick replies.

Clarification display text must not be promoted back into executable semantics.
Preserve structured `contextHints` returned with an option. Do not infer an
`optionSelected` operation, mask mode, field id, canonical action, or edit target
from the option label or prompt text. Local parsing may validate or display an
already explicit structured value; it must not create the semantic payload.

## Consult/Edit Rules

- `consult/answer`: factual or explanatory answer grounded in active component context; no patch.
- `edit/componentEditPlan`: governed edit with operation, target, validation, preview, and apply payload.
- Out-of-scope prompts return informational guidance, not fabricated patches.
- Clarify only for real component-authoring ambiguity that blocks a safe semantic decision.
- Quick replies may carry canonical action/context hints returned by the contract; they must not be local command strings disguised as natural language.
- Clarification options and quick replies must preserve `contextHints`, `canonicalAction`, and `semanticDecision`; labels and prompts are display material, not intent authority.
- Normalization helpers are allowed for display/search support, not intent classification.
- Domain Catalog `recommendedAuthoringFlow=shared_rule_authoring` can require the shared-rule route only when the request is not explicit local/editorial UI composition. Stale Domain Catalog hints must not override a semantically local composition request.

The shared `shouldRoutePromptToGovernedDecision` implementation must ignore
prompt wording and may honor only explicit canonical context such as
`domainCatalog.recommendedAuthoringFlow`. The authoring scope policy must travel
with both system guidance and structured context hints so downstream AI/tooling
can resolve scope semantically.

## Red Flags

Reject or refactor:

- `includes`, regex command parsing, localized label matching, hardcoded aliases, or fuzzy matching deciding authoring intent
- frontend deciding between consult/edit based only on prompt words
- assistant applying a patch without manifest operation evidence
- quick replies that bypass backend/manifest validation
- component-specific intent routers when a shared scope policy or manifest can govern the decision
- clarification helpers that reconstruct operation or target semantics from labels when the backend/tool could return structured context

## Validation

Use scope-policy and governed-routing specs first:

```bash
npx ng test praxis-ai --watch=false --progress=false \
  --include=projects/praxis-ai/src/lib/core/authoring/authoring-scope-policy.spec.ts \
  --include=projects/praxis-ai/src/lib/core/authoring/governed-decision-routing.spec.ts
```

For component assistants, also run the focused adapter/agentic-turn-flow specs
that prove off-scope prompts stay informational and in-scope prompts reach
governed edit planning. Add a negative scenario proving prompt wording alone
cannot authorize a governed handoff, plus a positive scenario driven by explicit
canonical context.

Include a regression case that passes the deprecated `localCompositionTerms`
option and proves matching terms still cannot authorize the handoff. Treat
`normalizeAuthoringPrompt` as display/search support only; its presence in the
public routing module is not permission to classify intent locally.

For backend semantic intent changes, run the smallest focused gate:

```bash
mvn "-Dtest=AgenticAuthoringIntentResolverServiceTest,AgenticAuthoringLlmIntentResolverServiceTest,AgenticAuthoringLlmPreIntentToolPlanningServiceTest,AgenticAuthoringSemanticDecisionPolicyTest,AgenticAuthoringIntentResolverDomainCatalogGroundingTest,AgenticAuthoringCandidateProvenancePolicyTest,AgenticAuthoringRepairClassificationPolicyTest,AgenticAuthoringDomainCatalogCandidateEnhancerTest,AgenticAuthoringDomainCatalogHintsTest" test
```

When the change touches provider payload parsing, quick replies, or fast intent
fallback, include a case proving incomplete LLM intent payloads fail closed and
structured quick reply/context hints remain authoritative over display labels.
When the change touches pre-intent shortcuts, include a case proving governed
tool evidence can satisfy an open narrative without keyword fallback and another
case where weak lexical evidence cannot override stronger semantic grounding.
