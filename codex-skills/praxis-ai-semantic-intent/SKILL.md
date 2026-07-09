---
name: praxis-ai-semantic-intent
description: Use when auditing or changing Praxis AI intent handling, governed decision routing, authoring scope policy, consult/edit boundaries, quick reply semantics, clarification handling, semantic grounding, runtime observation grounding, or any assistant code that might route user intent through local keywords, regexes, aliases, fuzzy matching, or command strings.
---

# Praxis AI Semantic Intent

Use this skill to enforce the Praxis rule: user intent is resolved semantically through governed AI/LLM contracts, manifests, capabilities, catalogs, context, and declared tools. Browser keyword routing is not the primary decision mechanism.

## Canonical Boundary

- `@praxisui/ai` may carry context, display state, ask clarifications, and materialize resolved decisions.
- Backend/LLM/tool contracts decide the primary authoring intent.
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

## Consult/Edit Rules

- `consult/answer`: factual or explanatory answer grounded in active component context; no patch.
- `edit/componentEditPlan`: governed edit with operation, target, validation, preview, and apply payload.
- Out-of-scope prompts return informational guidance, not fabricated patches.
- Clarify only for real component-authoring ambiguity that blocks a safe semantic decision.
- Quick replies may carry canonical action/context hints returned by the contract; they must not be local command strings disguised as natural language.
- Normalization helpers are allowed for display/search support, not intent classification.

## Red Flags

Reject or refactor:

- `includes`, regex command parsing, localized label matching, hardcoded aliases, or fuzzy matching deciding authoring intent
- frontend deciding between consult/edit based only on prompt words
- assistant applying a patch without manifest operation evidence
- quick replies that bypass backend/manifest validation
- component-specific intent routers when a shared scope policy or manifest can govern the decision

## Validation

Use scope-policy and governed-routing specs first. For component assistants, also run the focused adapter/agentic-turn-flow specs that prove off-scope prompts stay informational and in-scope prompts reach governed edit planning.
