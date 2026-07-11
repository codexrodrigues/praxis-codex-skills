---
name: praxis-java-quickstart-proof
description: Use when creating, extending, or auditing a Praxis API Quickstart operational proof for a Java resource: real HTTP schemas, OpenAPI, filters, option sources, actions, surfaces, capabilities, errors, stats/export, test data, write readback/cleanup, Cockpit verification, and downstream starter/runtime evidence.
---

# Praxis Java Quickstart Proof

Treat Quickstart as an operational proof host, never the owner of starter semantics.
Choose one representative resource and prove a canonical path by HTTP with fixtures
that demonstrate both success and an important negative condition.

## Build The Proof Slice

Inspect `ApiPaths`, controller, service, DTO/filter/action, mapper, option source,
test fixtures, security/origin setup, and existing pilot integration tests. Reuse
an existing pilot when it proves the same capability; do not copy a domain only
to make a new example. Fix a starter gap in the starter, then add the smallest
downstream proof here.

## Required Evidence

1. Prove resource identity in OpenAPI and `/schemas/filtered`, including stable
   path/resource key, request/response operation schemas, `x-ui`, ETag and hash.
2. Exercise each published operation in scope: filter/read, lookup reload,
   action/surface/capabilities, stats/export, or write. Verify `_links` and
   collection/item discovery agree.
3. Include a negative case: invalid payload, missing resource, denied state,
   invalid filter/option request, conflict, or policy limit. Prove no mutation
   follows a rejected write.
4. For writes, use controlled fixtures, read-after-write, side-effect evidence,
   and cleanup. Development mutation authority is available, but fixtures must
   remain reproducible and cleaned.
5. Run the relevant `QuickstartMetadataMigrationIntegrationTest`,
   `EventosFolhaPilotIntegrationTest`, focused pilot test, or Cockpit verifier.
   Review direct Angular runtime proof when the published contract changes.

Read [proof-slice-matrix.md](references/proof-slice-matrix.md) when selecting
the smallest representative resource and required evidence.

## Boundaries

- Quickstart owns host wiring, data, security, paths, and operational evidence.
- Metadata starter owns schemas, discovery, capabilities, option contracts, and
  resource semantics. Angular owns runtime materialization.
- Do not add aliases, schema patches, duplicate Cockpit assets, or host-local
  decision logic to make a smoke pass.

Close with resource key, operations proved, fixtures, commands, sanitized HTTP
outcomes, cleanup state, and unresolved owner follow-up. A pilot is useful only
when another host can reproduce the platform behavior from its evidence.
