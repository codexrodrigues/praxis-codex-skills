# Praxis Java Skill Coverage Reconciliation - July 2026

## Purpose

This note reconciles the Java/Praxis skill roadmap observed in
`praxis-metadata-starter/docs/technical/CODEX-SKILLS-JAVA-PRAXIS-ROADMAP.md`
with the current canonical `praxis-codex-skills` repository.

The roadmap is useful planning evidence, but the inspected copy lives in a dirty
`praxis-metadata-starter` worktree and still states that the aggregator had only
four skills and no Java/Praxis core skills. That premise is no longer true for
the canonical skill repository.

## Current Canonical State

As of 2026-07-12, `codex-skills/praxis-skills.manifest.json` already includes a
substantial Java/Praxis skill family:

| Skill | Primary use |
| --- | --- |
| `praxis-java-host-project` | Java/Spring host bootstrap and starter composition |
| `praxis-java-resource-authoring` | Complete resource-oriented Java/Praxis API authoring |
| `praxis-dto-annotations` | DTO, filter, command, `x-ui`, governance, and semantic annotations |
| `praxis-java-filter-query-authoring` | Filter DTOs, predicates, cursor/locate/sort, and filtered schemas |
| `praxis-java-option-source-provider-authoring` | Provider-backed option sources behind canonical option contracts |
| `praxis-resource-entity-lookup-backend` | `RESOURCE_ENTITY` option sources and lookup contracts |
| `praxis-java-availability-discovery-authoring` | Actions, surfaces, capabilities, and contextual availability |
| `praxis-java-command-concurrency-authoring` | Governed commands, idempotency, ETag, and conflict semantics |
| `praxis-java-error-response-contracts` | Structured Java/Praxis API failures and Angular materialization |
| `praxis-java-stats-export-authoring` | Stats, export, analytic fields, filters, scopes, and capabilities |
| `praxis-java-domain-governance-field-access` | Domain governance, field access, masking, AI policy, and export eligibility |
| `praxis-java-autoconfiguration-starter-maintenance` | Starter auto-configuration and extension points |
| `praxis-java-config-boundary-integration` | Metadata/config starter boundary and governed materializations |
| `praxis-java-quickstart-proof` | Quickstart operational proof for Java resource contracts |
| `praxis-java-http-corpus-publication` | HTTP corpus publication after Java proof |
| `praxis-java-contract-conformance` | Final resource/host evidence pack before migration/API handoff |
| `praxis-dashboard-analytics` | Java dashboard, chart, KPI, stats, and metadata-driven analytics APIs |

## Interpretation

Classification: `ja-suportado-mal-nomeado-ou-mal-materializado`.

The platform-skill repository already supports the core Java/Praxis roadmap
shape. The remaining issue is not that Java skills are missing from the
canonical repository; it is that planning artifacts outside this repository can
still describe an older state.

Do not create a new Java skill-count wave from that older premise. Use the
existing family during real Java/Praxis or Ergon migration work, and record only
evidence-backed misses in #254.

## What Would Justify Follow-Up

Open a focused follow-up only when implementation evidence shows one of these
conditions:

- a Java task consistently routes to the wrong skill or canonical owner;
- a skill lets a Java API close without proving `/schemas/filtered`, actions,
  surfaces, capabilities, options, errors, stats/export, or config boundaries;
- an actual `praxis-metadata-starter` or `praxis-config-starter` source change
  drifts away from the current Java skill guidance;
- a repeated Ergon migration task needs reusable Java/Praxis guidance that is
  not specific to Ergon and is not already covered by the current family.

## Next Recommended Action

Keep #254 as the active ledger. If the dirty `praxis-metadata-starter` roadmap is
later promoted through that repository, update it there to reference the current
canonical Java skill family instead of treating Java/Praxis skills as absent.
