---
name: ergon-rule-portfolio-catalog
description: Build, audit, and consume the governed read-only portfolio of Ergon legacy rules and atomic decision proposals. Use when Codex must explain RN identities such as RN-013a, measure discovered versus proposed versus migrated rules, refresh the rule cockpit or Praxis Domain Catalog v0.2 projection, check catalog determinism, select a rule for Parte 2 intake, or reconcile catalog state after a migration phase.
---

# Ergon Rule Portfolio Catalog

Treat the catalog as the migration portfolio and navigation surface. It is not
an executable rule contract, business homologation, or runtime authority.

## Step Zero: Readiness

1. Locate the migration workspace and read its root `AGENTS.md`.
2. Read
   `docs/migracao/rule-migration/factory-contracts/part2-foundation-readiness-v2.json`
   before selecting, advancing, or presenting the next action for a rule.
3. Require the active profile to admit the requested stage and action. A global
   corporate blocker must not stop development discovery when the active
   development profile explicitly admits it; development evidence must never
   be reused as homologation or production admission.
4. Read
   `docs/migracao/rule-migration/ergon-business-rule-catalog-and-cockpit-study-2026-07-21.md`
   when changing the catalog model or scope.
5. Read `references/catalog-phase-forward-tests.md` before changing state
   projection, aliases, authority, or next-action logic.

Preserve these separate identities and state axes:

- documentary rules such as `RN-013`;
- atomic decision proposals such as
  `regra-frequencia.periodo.ordem-valida`;
- working aliases such as `RN-013a`;
- legacy authority, target authority, semantic status and migration phase.

Never infer that an RN suffix is an ordinal of migrated work. Never promote a
technical proposal, description, draft, phase result or alias to
business-confirmed or target-authoritative state.

## Canonical Sources

In the migration repository, use these sources rather than copying their
content into the skill:

- `docs/migracao/rule-migration/rule-canonical-decision-inventory.md` for the
  reconciled documentary RN slice;
- `docs/migracao/rule-migration/factory-contracts/goldens/*.rule-decision-profile.json`
  for atomic technical proposals;
- governed semantic packages for per-decision semantic status;
- governed phase state/evidence for the current migration position;
- `docs/migracao/rule-migration/factory-contracts/reference/ergon-rule-migration-portfolio-v1.json`
  as the generated internal portfolio;
- `docs/migracao/rule-migration/factory-contracts/reference/ergon-rule-domain-catalog-v0.2.json`
  as the sanitized Praxis projection;
- `docs/migracao/rule-migration/ergon-rule-migration-cockpit.html` as the
  generated read-only visual surface.

The canonical Domain Catalog contract belongs to `praxis-config-starter`. Do
not introduce an Ergon-specific public catalog API or redefine
`praxis.domain-catalog/v0.2` in the migration repository.

## Workflow

### Audit or explain the portfolio

1. Run the repository checker before trusting generated artifacts:

   ```powershell
   tools/migration-factory/check-rule-portfolio-catalog.ps1
   ```

2. Report counts by artifact kind and state axis. Do not sum documentary rules
   and atomic proposals as though they were the same population.
3. Explain aliases through their `canonicalRuleId` and `decisionKey`.
4. State semantic status, current legacy authority and target authority
   separately.
5. Cite canonical source paths for claims about meaning, status or coverage.

### Refresh the catalog

1. Change a canonical source only when new governed evidence actually changes
   it.
2. Rebuild deterministically:

   ```powershell
   tools/migration-factory/build-rule-portfolio-catalog.ps1
   tools/migration-factory/test-rule-portfolio-catalog.ps1
   ```

3. Review the generated portfolio, Domain Catalog projection and cockpit in
   the same cycle.
4. Run `tools/migration-factory/test-rule-migration-factory-contracts.ps1`
   when the change affects identities, states, mappings, schemas or the
   assembler/checker.
5. Keep generated output byte-identical when inputs do not change.

### Select work for Parte 2

1. Filter candidates by bounded context, evidence coverage, semantic status,
   legacy authority and current migration state.
2. Record why the selected atomic decision is bounded enough for intake.
3. Invoke `$ergon-rule-migration-orchestration` for Phase 9 and later. This
   skill does not open, close or approve a migration phase.
4. After governed evidence or phase state changes, rebuild and recheck the
   catalog so the cockpit cannot drift from the factory artifacts.
5. If the phase is blocked, expose the blocker and its admissible recovery
   action; do not present a later phase as the next action.

## Fail-closed Rules

- Block refresh on duplicate RN IDs, duplicate decision keys, orphan
  proposals, unresolved generated-source references, invalid aliases, schema
  failure or non-deterministic output.
- Never copy an atomic phase/status onto its documentary parent or sibling.
- Block any generated promotion to target authority.
- Preserve `UNKNOWN`, `REVIEW_REQUIRED` and `KEEP_DB_BACKED`; do not synthesize
  missing business meaning, owner, effects, fact providers, outcomes, reason
  codes or evidence.
- Keep business homologation deferred to its later process. A technical catalog
  may guide development intake without pretending that domain specialists have
  approved the semantics.
- Do not expose credentials, client data, SQL session context, HADES internals
  or unsanitized source in the Domain Catalog projection or cockpit.

## Expected Handoff

Return:

- catalog/check status;
- exact counts separated by documentary rules and atomic proposals;
- selected canonical rule, decision key and aliases;
- evidence and unresolved blockers;
- semantic status, current authorities and allowed next action;
- changed generated artifacts and validation commands.
