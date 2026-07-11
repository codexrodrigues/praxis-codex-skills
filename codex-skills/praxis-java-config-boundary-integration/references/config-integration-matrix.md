# Config Integration Matrix

| Need | Canonical owner | Java host responsibility | Do not do |
| --- | --- | --- | --- |
| Resource structure, fields, surfaces, actions, capabilities | `praxis-metadata-starter` | Expose and consume resource contracts | Duplicate schema semantics in config |
| Shared decision authoring, simulation, approval, publication | `praxis-config-starter` | Consume only an in-scope applied materialization | Store drafts or approval state in resource DTOs |
| User runtime state, ETag, secret protection | `praxis-config-starter` | Supply authenticated context and preserve HTTP contract | Add parallel browser/host persistence as authority |
| API/schema grounding and AI registry | `praxis-config-starter` plus metadata evidence | Provide canonical resource evidence and enforce host policy | Route intent with keywords or treat RAG as source of truth |
| Authenticated context, authorization, Origin enforcement | Java host | Validate principal, tenant, environment, and protected routes | Trust caller identity headers in corporate mode |
| Runtime rendering and interaction | `praxis-ui-angular` | Publish stable contracts for clients | Move policy ownership to a screen |

An applied materialization must retain its stable key, target identity, source
hash, status, scope, diagnostics, and evidence provenance. Missing, stale,
unpublished, rejected, reverted, or cross-scope materializations remain
inactive and produce explicit diagnostics rather than host-local substitutions.
