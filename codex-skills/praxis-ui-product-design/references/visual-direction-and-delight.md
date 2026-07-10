# Visual Direction And Delight

Use this reference when creating or materially redesigning Praxis UI, or when the user asks for a
modern, delightful, elegant, premium, memorable, distinctive, polished, or non-generic result.

## Contents

- Read The Product Before Styling
- Direction Contract
- Calibrated Expression
- Enterprise Delight
- Product-Specific Signatures
- Generic Defaults To Reject
- Two-Pass Design And Critique
- Screenshot Tests

## Read The Product Before Styling

Do not start from a component inventory or an aesthetic trend. Inspect the real workflow, current
content and states, domain language, existing brand/theme evidence, nearby Praxis patterns, and the
functional owner contract. Identify:

- the actual operator, their environment, and the task they must complete
- what they did immediately before this surface and what must happen next
- the information they compare, manipulate, approve, or recover
- the domain's artifacts, materials, diagrams, vocabulary, and characteristic data shapes
- the emotional requirement: calm, exact, urgent, exploratory, accountable, or collaborative

Words such as `clean`, `modern`, and `professional` do not define a direction. Translate them into
observable decisions, such as compact and exact typography, a stable three-region workstation,
quiet neutral surfaces, one high-contrast action accent, and motion reserved for selection continuity.

## Direction Contract

Write this compact contract before implementation. Keep it in task notes unless the user asks to
review or choose the direction.

```text
Operator and job: [specific person and verb]
Surface archetype: [workstation, list-detail, canvas-inspector, focused form, analytics, runtime]
Visual thesis: [mood + material + rhythm + energy]
Domain sources: [5+ concrete artifacts, concepts, or data shapes]
Signature: [one spatial, informational, typographic, or interaction idea unique to this workflow]
Rejecting:
  [generic default] -> [specific replacement]
  [generic default] -> [specific replacement]
  [generic default] -> [specific replacement]
Token plan: [existing Material/Praxis tokens and any private composition variables]
Composition sketch: [one-sentence layout or small ASCII wireframe]
Interaction thesis: [1-3 transitions or direct-manipulation moments and why they help]
Calibration: distinction [1-5], motion [1-5], density [1-5]
```

The contract must be specific enough that removing the product name still leaves clues about the
workflow. If it could describe any admin panel, revise it.

Do not ask the user to approve the direction when the brief and repository evidence make it clear.
Ask only when two materially different directions remain equally plausible.

## Calibrated Expression

Use three independent scales instead of treating `modern` as a single style:

- Distinction: `1` institutional-neutral, `3` recognizable product character, `5` deliberately expressive.
- Motion: `1` state feedback only, `3` visible continuity and shared transitions, `5` choreographed experience.
- Density: `1` focused and spacious, `3` balanced application UI, `5` cockpit-like comparison and control.

For an ordinary Praxis authoring workstation, start near `3 / 2 / 4`, then change the values from
operator evidence. Do not import a landing-page baseline into a dense operational surface.

The scales describe intensity, not quality. A distinction level of `1` still requires excellent
typography and rhythm. A motion level of `1` still requires immediate feedback. A density level of
`5` still requires hierarchy and breathing points.

## Enterprise Delight

Create delight through capability and fluency before decoration:

- preserve context while navigating, selecting, editing, previewing, and saving
- let related regions respond together so cause and effect remain obvious
- expose state changes exactly where attention already is
- use typography and alignment to make scanning feel effortless
- make direct manipulation feel immediate, reversible, and safe
- turn empty, invalid, loading, permission-limited, and recovery states into clear next actions
- use one memorable transition or visual behavior when it strengthens the task model
- make narrow layouts feel intentionally recomposed, not merely stacked

Decorative delight is allowed only when it supports the direction, remains tokenized and
host-themeable, respects reduced motion, and does not compete with operational state.

## Product-Specific Signatures

Choose one signature and execute it deeply. Examples are prompts for reasoning, not components to
copy:

- Spatial: a decision trail that remains aligned with the canvas or inspector as selection changes.
- Informational: a preview that foregrounds semantic change, impact, or before/after evidence.
- Interaction: selection travels coherently from list or canvas into the exact editable property.
- Typographic: identifiers, states, and values use a disciplined type treatment derived from the domain.
- Data expression: relationships, completeness, or confidence are shown in a form native to the task.
- State transition: apply/save visibly resolves the affected region without a disconnected generic toast.

Use only information and capabilities already provided by the canonical contract. If the signature
requires missing data or behavior, classify the contract gap before inventing frontend-only state.

Spend aesthetic risk in this signature. Keep the rest of the interface restrained, accessible, and
consistent so the signature feels intentional rather than noisy.

## Generic Defaults To Reject

Name at least three relevant defaults before implementation:

- untouched Angular Material appearance with no Praxis product character
- generic blue accent on neutral gray surfaces without domain or brand evidence
- fixed sidebar plus equal card mosaic regardless of workflow
- a card, border, icon, chip, or helper paragraph for every concept
- identical widths, weights, and spacing for controls with different importance
- purple/blue gradients, glass panels, oversized radii, and floating widgets used as shorthand for AI
- sparse composition that wastes operational space in the name of elegance
- dense composition with no dominant task, breathing point, or state hierarchy
- animation sprinkled across controls instead of one coherent continuity model
- imitating Linear, Notion, Stripe, Apple, or another product instead of understanding the principle

Replacing a default requires an alternative. Merely deleting cards or gradients does not create a
direction.

## Two-Pass Design And Critique

First pass:

1. Produce the direction contract.
2. Sketch the major regions and visual hierarchy before styling individual components.
3. Materialize the signature early enough that it can shape the composition.
4. Derive visual decisions from existing Material/Praxis tokens and the host theme.
5. Implement real content and representative states; placeholder content hides weak design.

Second pass:

1. Capture representative desktop and narrow screenshots.
2. Compare the screenshot to the visual thesis, not only to code intent.
3. Identify the three strongest signs of genericity or unfinished craft.
4. Fix the highest-impact compositional defect before polishing micro-details.
5. Remove one decorative element that is not earning its place.
6. Recapture and repeat until the signature, hierarchy, and product specificity survive the tests.

## Screenshot Tests

- Genericity test: could this be mistaken for an untouched Material demo or a generic AI admin template?
- Swap test: could the typography, palette, layout, or signature be swapped for a common default without changing the product meaning?
- Squint test: when blurred or viewed at thumbnail size, are the primary task and major regions still obvious?
- Signature test: can one point to a concrete element or behavior that expresses this exact workflow?
- Coherence test: do color, type, shape, spacing, iconography, and motion tell the same visual story?
- Craft test: are alignment, optical spacing, control geometry, icon weight, truncation, and transitions finished at screenshot scale?
- State test: does the direction remain coherent in empty, busy, invalid, selected, readonly, and narrow states?
- Restraint test: would removing a decorative element make the result clearer and more premium?

Fail and iterate when the request explicitly asks for delight or distinction but only correctness is
visible. Correct and generic is not the requested outcome.

