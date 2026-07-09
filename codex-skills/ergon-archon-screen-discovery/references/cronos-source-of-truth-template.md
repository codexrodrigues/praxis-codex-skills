# Cronos Source Of Truth Template

Use this template for `docs/migracao/<SCREEN>/cronos-source-of-truth.md` during Phase 1 when a Cronos/Archon screen has runtime XML, local XML, HADES/stored XML candidates, or an XML-export residual.

## Header

- Screen: `<SCREEN>`
- Module/application: `<MODULE>`
- Decision: `RUNTIME_EXPORTED_XML_MATCH` / `RUNTIME_EXPORTED_XML_DIVERGED_FROM_LOCAL` / `RUNTIME_XML_EXPORT_FORBIDDEN` / `RUNTIME_XML_EXPORT_AUTH_BLOCKED` / `RUNTIME_XML_EXPORT_NOT_FOUND` / `LOCAL_XML_ONLY_UNCONFIRMED` / `Blocked` / `Partial`
- Current source for Phase 1 structural discovery: runtime XML / local XML / HADES stored XML / blocked
- Last updated: `<YYYY-MM-DD>`

## Evidence Matrix

| Source | Path or query/output | Status | Date/version | SHA-256 | Parser result | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Authenticated runtime XML | `runtime/<SCREEN>.authenticated.xml` | available / missing / forbidden / blocked |  |  |  |  |
| Local XML | `docs-legado/.../<SCREEN>.xml` | available / missing / divergent / unconfirmed |  |  |  |  |
| HADES registry | `oracle-results/...` | executed / blocked / not applicable |  |  |  |  |
| HADES/stored resource XML | `oracle-results/...` | executed / blocked / not found / not applicable |  |  |  |  |
| Browser/debug XML | `browser-runtime.md` | captured / partial / missing |  |  |  |  |

## Comparison

Record only concise facts:

- Runtime vs local hash/date/version comparison.
- Whether both XMLs have the same root transaction and screen code.
- Whether HADES confirms the transaction, screen pattern, access mapping, or stored resource candidate.
- Whether any divergence affects components, SQL, binds, links, `dataTable`, hidden fields, or write surface.

Do not paste full XML.

## Decision

State the source accepted for the current Phase 1 pass and why. If the decision is blocked or partial, list exactly what must be run next.

## Required Next Checks

| Check | Owner/phase | Command or artifact |
| --- | --- | --- |
| Re-run runtime XML export | Phase 0/1 | `tools/migration-factory/download-runtime-xml.ps1 -Screen <SCREEN>` |
| Run HADES registry discovery | Phase 1 | `hades-registry.sql` or `find_hades_screen_definition.ps1` |
| Compare local/runtime XML structurally | Phase 1 | parser/hash/targeted component diff |

## Gate Rule

Phase 1 cannot close as `Ready for next phase` while this file is absent for a screen with XML evidence. If HADES/Oracle is unavailable, this file may close as `Partial` or `Blocked`, but the phase gate must carry the blocker.
