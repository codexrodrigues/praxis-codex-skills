# Flexible visual authoring: scope and evidence

Classification: documentation only. This review improves existing skill routing
and operational references; it adds no skill, public component contract or runtime
patch. Analytical, customized registration and selection/detail pages remain
equally valid compositions. Component owners retain their document semantics.

## Evidence boundaries

- Canonical skills were inspected from remote main in an isolated worktree; the
  active primary checkout had unrelated changes and was preserved.
- Hero HQ at the official local origin `http://127.0.0.1:4302` was inspected through
  visible browser editors with `@praxisui/*` package declarations at rc.32.
  Child content editors, page sources and one existing connection were inspected
  without applying/saving altered values or generating a screen.
- Angular source and installed packages were read to understand contracts. Source
  inspection is not a new browser round-trip. Historical rc.17/22/26 rehearsals
  in browser-workflows references retain their version/date and proof limits.
- No new complete page, business record mutation, recording or timed end-to-end
  take was performed. The Studio was left empty with customization off.

## Capability ledger

| Capability | Evidence from this investigation | Remaining proof / owner |
| --- | --- | --- |
| Palette, page and child editors | Registered presets and content/widget/page settings inspected | New insertion through acknowledged save/reopen remains a separate authorized exercise |
| Chart discovery | Remote resource selector listed relevant resources; source/operation controls observed | Existing payroll chart opened with a rejected selected resource and blocked Apply/Save; diagnose in Charts, then compare a new canonical preset |
| Table/List connection | Widget editors exposed manual resource paths and preference/page configuration origins | Do not assume standalone Quick Connect is present in every wrapper; prove chosen connection and persistence scope |
| Content/cards | Guided nested card content, icon/badge/progress, binding and navigation controls observed | No generic `cardClick` output inferred; choose actual List/KPI/action capabilities when a card must filter |
| Page sources and derived values | Guided controls/JSON and response previews observed | Three previews returned transformed data; employees preview showed HTTP 520; some derived comparisons showed diagnostics. Root causes unproven |
| Existing chart-to-table connection | Graph showed Cross Filter -> query context, exact link identity and descriptions; 13 widgets, one link, zero graph diagnostics at inspection | Structural/read-only evidence only; new wiring, execution, clear and persistence were not exercised in this step |
| Filter alternatives | Source metadata inspected: `praxis-filter` DTO change/requestSearch; `praxis-filter-form` valueChange/submit envelope `{ formData }` | New browser filter wiring and partial/full clear remain unproved on this host |
| Guided screen composer | Control and required fields observed; installed code generates mixed-case IDs such as `praxis-Card`, `praxis-StatCard`, `praxis-Table` | Registry resolution mismatch indicated by static inspection; generator not executed. Page Builder must verify IDs, schema assumptions and replacement semantics before recommending it |
| Embedded host media | Host radar metadata has inputs and no own configEditor | Record host scope and prove the actual embedding/editor path; do not institutionalize it in universal component guidance |

These observations are not permanent product limitations. Reproduce against the
intended installed version before fixing or adopting a later implementation.
The five-minute composer label and historical rehearsal durations do not certify
the current page or a new ten-minute demonstration.

## Guidance changes

The generic browser workflow now routes by registered capability to Page Builder,
component, filter, composition, persistence and design owners. Existing owner
skills gain browser-operation references. They distinguish shell/content/canvas,
data/preview provenance, exact event envelopes, query ownership, configuration
preferences and parent autosave. No dashboard-specific dependency or widget set
is introduced.

## Validation scenarios and handoff

| Scenario | Guidance review | Browser acceptance still required |
| --- | --- | --- |
| Analytical view | Chart catalog/fields, data origin, event-specific target and clear are routed to their owners | New chart, linked query, clear and save/reopen |
| Customized registration | Operation schema/mode, layout/validation, record context and configuration Save versus domain Submit are distinct | Authorized form operation, invalid/cancel and permitted submit with receipt |
| Search/selection/detail | One effective query owner, DTO/envelope projection, stable identity and empty selection are explicit | Search, partial/full clear, pagination, selection/detail and fresh reopen |

Skill structure, references, manifest hashes, generated issue drafts and both
families' source audits are checked before publication. Functional widget/browser
acceptance is not claimed by those checks. No source repair or host package
adoption belongs to this documentation increment. Owner follow-ups above must be
resolved or explicitly scoped before a new recording promises those behaviors.

## Documentation validation

- All 12 edited skill entrypoints pass the skill-creator `quick_validate.py`
  under Python UTF-8 mode. Five pre-existing unquoted descriptions containing
  colon-space were quoted as YAML scalars without changing their meaning.
- Repository structure validation passes for both families. Manifest content/tree
  hashes were recomputed using the canonical normalized hashing functions.
- An isolated installation passes both PowerShell audits with `-FailOnDrift`:
  Praxis 168 OK and Ergon migration 19 OK, zero drift/missing/source errors.
- Generated review drafts are regenerated and checked by the repository tools.
- Independent read-only review covered the 12 entrypoints, ten references and
  this evidence ledger. Its corrections scope acceptance to applicable operations
  and add same-identity detail refresh alongside A -> B -> empty selection.
- Manual routing review: "create an analytical page in the visual editors",
  "compose a customized registration form", and "connect search/selection/detail"
  select the generic browser workflow and corresponding functional owners.
  "Implement a Chart editor validator" selects the Charts implementation owner;
  "add a Java stats endpoint" selects the backend owner, without invoking browser
  operation as the implementation route. This is a guidance review, not a model
  routing benchmark or an executed browser scenario.

The existing local installation is older than remote main: its initial full
Praxis comparison was 78 OK, 89 drift and one missing, with no source errors.
Only the 12 reviewed skills are selected for installation in this task; the
remaining older installed skills are outside this synchronization scope. Source
audit cleanliness and selected installation parity do not certify the entire
local installation against the newer remote inventory.
