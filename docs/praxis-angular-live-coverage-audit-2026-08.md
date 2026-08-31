# Praxis Angular Live Coverage Audit - August 2026

## Scope And Coordinates

This reconciliation updates the July audit without using a skill-per-component
target. It compares the immutable Angular head from PR #462,
`cffbf82c859c61ac06877a7c93f13d19ceafcd57`, with the canonical Praxis skill
portfolio at `praxis-codex-skills` main commit
`263904908fc5de8b0ba74fc9ca6354a674ca0e3f`.

The question remains whether each repeated implementation decision routes to a
canonical owner, source inventory, prohibited shortcut, and focused proof. Raw
export count alone is not a reason to create a skill.

## Current Inventory

| Metric | August 2026 | July audit | Delta |
| --- | ---: | ---: | ---: |
| Angular library packages | 22 | 22 | 0 |
| Public `public-api.ts` surfaces | 24 | 24 | 0 |
| Public export statements | 824 | 800 | +24 |
| Components | 258 | 249 | +9 |
| Services | 130 | 125 | +5 |
| Directives | 9 | 8 | +1 |
| Specs | 769 | 599 | +170 |
| Markdown docs under package `docs/` | 161 | 149 | +12 |
| `*.json-api.md` files | 85 | 85 | 0 |
| Authoring manifests | 24 | 20 | +4 |
| Active Praxis skills | 167 | 146 reconciled | +21 |

Counts use file suffixes and root/secondary `public-api.ts` surfaces from the
immutable Angular tree. Between the July baseline and this head, 557 commits
touched `projects/` or `tools/ai-registry`, so source drift was evaluated by
new semantic areas rather than by names only.

## High-Risk Package Signals

| Package | Exports | Components | Services | Specs | Docs | Authoring manifests |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `praxis-core` | 247 | 18 | 49 | 157 | 47 | 1 |
| `praxis-dynamic-fields` | 193 | 83 | 5 | 127 | 15 | 1 |
| `praxis-dynamic-form` | 42 | 20 | 9 | 86 | 7 | 2 |
| `praxis-charts` | 39 | 7 | 13 | 30 | 1 | 2 |
| `praxis-table` | 39 | 18 | 8 | 125 | 33 | 2 |
| `praxis-ai` | 25 | 6 | 13 | 20 | 4 | 0 |
| `praxis-page-builder` | 21 | 11 | 1 | 37 | 4 | 1 |

## Reconciliation Findings

| Finding | Classification | Action |
| --- | --- | --- |
| Core runtime profiles, related-resource composition, record opening, conditional accessible surfaces, Reactive Determinations, selection/lookup overlays, analytics authoring, and Page Builder production-like certification all route to dedicated current skills. | `already-supported` | Keep the existing task-oriented families; do not create component/export skills. |
| `@praxisui/ai` now exports `PraxisGovernedAudioTranscriptionService` and the shell supports `voiceInputMode="governed-transcription"`, but composer guidance still described only browser speech as the voice path. | `migration-skill-gap` and `ja-suportado-mal-nomeado-ou-mal-materializado` | Update the composer, Angular backend-contract, and Config provider-operations skills together. |
| The governed service has shell and `AiBackendApiService` coverage, but no focused MediaRecorder lifecycle spec. Config has a controller test, but no focused provider-management/provider-adapter transcription test. | `supported-partially` | Track Angular issue [#470](https://github.com/codexrodrigues/praxis-ui-angular/issues/470) and Config issue [#394](https://github.com/codexrodrigues/praxis-config-starter/issues/394); do not invent a new contract or claim Angular HTTP mocks prove provider execution. |
| The governed transcription platform boundary already exists in Angular, Config, OpenAPI/docs, and the public export. | Not `platform-gap` | Do not create a standalone transcription skill now. Existing owner skills have coherent triggers and proofs once corrected. |

## Governed Transcription Boundary

The reusable decision is split by canonical owner:

- `@praxisui/ai` owns accessible capture state, `getUserMedia`/`MediaRecorder`,
  track cleanup, scoped multipart client use, transcript insertion, and explicit
  user submission;
- `praxis-config-starter` owns `/api/praxis/config/ai/transcriptions`, principal
  scope, the 12 MiB server bound, provider/model configuration, capability
  checking, credentials, safe errors, and provider execution;
- transcript text remains editable user input. It is not a semantic decision,
  assistant result, turn, preview, apply authority, or business evidence.

`browser-speech` remains an explicit compatibility option for approved
low-risk environments. It is not the enterprise/default architecture and must
not become a frontend provider-routing fallback.

## Recommendation

Keep the portfolio at 167 active Praxis skills after correcting the three
existing skills. The evidence does not justify a broad new Angular wave or a
standalone audio skill. The next promotion criterion is a second recurring
transcription task whose workflow cannot be completed by the composer,
backend-contract, and provider-operations owners without loading unrelated
guidance.

Track the two focused test gaps in Angular issue
[#470](https://github.com/codexrodrigues/praxis-ui-angular/issues/470) and
Config issue
[#394](https://github.com/codexrodrigues/praxis-config-starter/issues/394).
Re-run this audit
when a package adds a public contract/authoring manifest without a matching
owner skill, or when another real implementation demonstrates routing or proof
friction not covered by the corrected portfolio.
