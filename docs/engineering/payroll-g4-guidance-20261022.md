# G4 skill guidance candidate — 22/10/2026

Status: local guidance validated; independent semantic review and canonical integration/publication pending. G4 product acceptance, generated HTTP schema, migration/transaction Neon proof and authenticated UI remain separate gates. No product code or installed skill was changed by this documentation package.

Writer: `g4_ui_finish`, inherited model/effort as assigned by coordinator; no model switch inferred. Reviewer: root/coordinator approved the initial two skill/reference edits in source; additional corpus/session deltas and integration remain separately reviewable. Classification: `docs-apenas`; four existing skills require `atualizar-existente`, no new skill or platform contract.

The supplied G1 skill checkout was on `docs/g2-governed-snapshot-migration`, HEAD `7b21ef56002412769f8966e5cd19aea33aa4a2b2`, with untracked Python cache directories; it was left untouched. After `git fetch origin main --no-tags`, a clean isolated worktree `.worktrees/payroll-g4-skills` was created on `docs/payroll-g4-guidance`, based on `origin/main` `8a9bdb2503a9f813c2dcd51cbcc1d821e6f9a738`. No commit, push, PR, publication, deployment, Actions or real installation was performed.

## Inventory, gap and impact

| Skill | Existing guidance and demonstrated gap | Change |
| --- | --- | --- |
| `praxis-reactive-determinations` | Canonical owners, chain execution, stale handling and unsatisfied runtime state exist; it did not teach the existing public form APIs for the domain-specific parent CAS bridge (`migration-skill-gap` / `ja-suportado-mal-materializado`) | Add a concise entry and referenced procedure for capture-before-mount, exact parent set, real metadata FormArray, root validation, reset/conflict and separate evidence gates |
| `praxis-api-quickstart-operational-proof` | One-snapshot protected bulk authorization already exists; ordinary financial reads/projections/analytics still need the same discipline (`suportado-parcialmente` in the candidate host) | Extend its existing temporal-read section with the actual candidate resolver/repository path, required proxy transaction boundary, no fallback and causal interleaving proof |
| `praxis-http-examples-contract-surfaces` | `origin/main` already contains both Reactive Determination and Versioned Resource Writes guidance; the reported absence was not confirmed. The real G4 gap is the host-specific parent list and unconfirmed corpus evidence flags (`migration-skill-gap`) | Extend the existing versioned-write section with joined event capture, exact parent-token transport, no generic decision version and candidate flags |
| `praxis-api-quickstart-security-config` | Existing SESSION admission and effective column-ACL guidance is correct; the official storage installation prerequisite was missing from the adoption procedure (`suportado-parcialmente` in the host, existing-skill gap) | Add the reviewed candidate forward, segregated migration/runtime identities, strict predecessor/catalogue acceptance and exact INSERT/UPDATE columns, preserving separate fixture/history/HTTP/G4 gates |

Canonical owners remain Quickstart financial domain/auth/session installation, Metadata schemas/CAS, Config governed decisions and Angular generic runtime. No framework API, business rule, endpoint, DTO, dependency edge or manifest family membership was added. The manifest changes only the four affected source/tree hash pairs. Domain-pilots guidance is owned by another chat and was not edited. Public product docs/examples/corpus remain part of the coordinator's G4 package, not certified by this skill patch.

Sources inspected: the workspace G4 plan and domain checkpoint; P0/P1 `DECISOES.md` and `FECHAMENTO-R1-R4.md`; D4 revised; Quickstart financial domain/evaluation, event read/mutation/projection, operational context resolver and principal grant repository; UI event host/page and their actual-runtime specs; published package usage already recorded by the UI work package. Quickstart source baseline during inspection was HEAD `d94789a04e4026bf36b30547be3a420f7b8123dc` plus ongoing G4 changes. Candidate method names are explicitly conditional on adoption; no unpublished host API is taught as a released capability.

For the corpus extension, additionally inspected `.worktrees/payroll-g4-http/PAYROLL_G4_CONTRACT.md`, payroll detail, event detail and event move requests plus its JSON payload, manifest candidate flags and Quickstart create/update event parent-precondition DTOs. The existing canonical paragraphs were retained, not copied from the installed projection. The corpus examples explicitly remain unconfirmed source-derived candidates.

## Semantic walkthrough and trigger checks

- Positive reactive prompt: implement event create/edit/move with official parent snapshots and keep submit blocked during capture. The procedure leads to existing public read/ETag/FormArray/validator APIs and canonical schema policy.
- Adjacent non-trigger: change a static chart label without a reactive form, governed evaluation or dependent resource. This does not require the Reactive Determinations workflow.
- Positive operational prompt: audit ordinary financial GET/analytics authorization under concurrent coverage and assignment changes. The temporal-read section requires one physically shared RR/RO snapshot and distinguishes writable command fences.
- Adjacent non-trigger: author a new Config decision without changing or proving a host. Config authoring owns that task; this operational proof procedure is not the authoring path.
- Positive corpus prompt: update the pending-event move HTTP example while preserving event/origin/destination captures. The versioned-write section requires the typed host body list and unconfirmed flags. An adjacent task to calculate financial outputs belongs to the governed host, not corpus authoring.
- Positive session prompt: diagnose signed SESSION rejection because the official operational bootstrap lacks its Store table. The guidance selects the reviewed forward, checks precise column ACLs and keeps the current SESSION security contract. An adjacent request to provision payroll coverage or enterprise memberships cannot be satisfied by this storage installation.
- Adversarial walkthrough: absent/visible transport metadata cannot be repaired by local fields or submit-policy overrides; weak/stale tokens cannot be synthesized/refreshed; missing snapshot holder or RO/READ COMMITTED cannot fall back to independent/owner reads. These are instructional checks against inspected source, not newly executed product tests.

The UI package's earlier consumer tests and source inspection informed this guidance. They do not prove current final backend source, physical ACL/lock interleavings, migrated state or a deployed UI. The causal snapshot case is deliberately stronger than a grant revoked after any valid read: old coverage A must never be combined with a later target assignment A when the target belonged to B until after that coverage was revoked.

## Validation and delivery state

PowerShell was unavailable. `quick_validate.py` was present but could not import local PyYAML; the repository's dependency-free fallback was used without installing another environment dependency.

- `python3 scripts/validate-praxis-skills.py codex-skills/praxis-reactive-determinations codex-skills/praxis-api-quickstart-operational-proof codex-skills/praxis-http-examples-contract-surfaces codex-skills/praxis-api-quickstart-security-config`: passed.
- `audit-praxis-skills.py --family praxis --skills-root codex-skills --fix-manifest`: updated only affected hash entries; subsequent blocking source audit passed, 168 skills, zero source drift/invalid/missing.
- `audit-praxis-skills.py --family ergon-migration --skills-root codex-skills --fail-on-drift`: passed, 19 skills; the opposite family's directories are recognized separately.
- `generate-skill-review-issue-drafts.py --check` and `validate-issue-drafts.py`: passed; no draft regeneration was needed because descriptions/inventory did not change.
- `PYTHONPYCACHEPREFIX=/tmp/payroll-g4-skills-pycache python3 scripts/preflight-python-fallbacks.py`: passed, including script tests, full structure/draft checks and official sync/audit of both families in disposable temporary directories. This is not a real local installation.
- `git diff --check`: passed.

The latest read-only audit of the actual installed target reports 18 Praxis drifts, including all four changed skills, and zero Ergon drifts. This inventory may also change through other tasks; no unrelated drift was attributed to this package or overwritten. Canonical integration/publication and subsequent selective synchronization of only these affected skills remain pending under the coordinator. Until then, use this candidate source with its explicit limits; do not claim local installation parity or G4 completion.

Review should assess procedure correctness against the final source and evidence, not merely hash/validator success. Any change to the candidate resolver transaction boundary, form lifecycle, metadata transport policy or final acceptance conditions requires rechecking the corresponding instruction before merge/adoption.

## SESSION prerequisite continuation

The coordinator assigned the existing operational-proof/security-config skills to cover the canonical session-installation prerequisite in the same cycle. Inspected the workspace `SESSION-PREREQUISITE.md` plan and the separate `.worktrees/payroll-g4-session-prerequisite` candidate's `docs/ENTERPRISE-SESSION-OPERATIONAL-PREREQUISITE.md`, Store SQL, guarded Neon harness and forward SQL. The reviewed SQL SHA-256 was `699f2b1deb72cc4582fda5596510a70adbaf8237ab9fa07362d61fd0f0c458bc`; this is an evidence binding for that candidate, not a permanent hash to copy into future assignments.

The host contract already required persisted SESSION issuance. The source change installs it through the existing separate operational lane; it neither reconstructs retired `20260905.002`–`.006` resources nor overrides strict missing-history validation. Guidance preserves the SQL's three INSERT and seven UPDATE columns, table SELECT, segregated non-superuser owner/runtime, strict catalogue/ownership/dependency checks, and rejection of unsafe PUBLIC/inherited/global permissions without automatic repair. Fixture DDL and TESTONLY snapshots remain explicitly insufficient as deployment/migration proof.

The source package records nine offline tests passed; this skill task did not execute product tests or connect to a database. The guarded Neon proof was initially in progress. The subsequently updated source document and coordinator's independent review now record **two Neon tests passed, zero failures/errors/skips, 94.073s**, bound to the unchanged SQL hash above. Full canonical fresh migration applied only `20261022.001`, then repeat-zero; real Store/Lifecycle, effective column rights and four denied writes (42501) passed. Thirteen same-resource catalogue/ACL adversaries rejected drift with rollback and preserved digests. The compatible predecessor was the newly installed forward table plus compatible column SELECT, not an arbitrary historic installation.

This is a reviewed candidate storage-installation proof on its exclusively assigned database; it is not main/public-artifact adoption, a final JAR/deployment, real HTTP, a deployed session journey, enterprise opt-in membership or G4 financial cutover. Full official migration + repeat-zero/lifecycle and same-resource rollback adversaries retain their different evidence scopes. The source document preserves raw evidence/assignment custody and reports the lease returned with no active synthetic session. Candidate integration/publication and selective local synchronization remain pending under custody; no push or installed skill update is authorized by this package.

Root approved the session skill delta and found one adjacent contradiction in operational-proof's Maven/bootstrap paragraph: it still allowed H2 profiles for new proof despite the remote-Neon rule. Only that paragraph was corrected. Profiles may disable unrelated services, but every database-backed validation requires its assigned remote Neon child and real role profile; H2/embedded fixtures remain historical. The post-review change used focal structure validation and official hash/audits rather than repeating the unchanged Python preflight suite.


## Checkpoint de transporte — 24/10/2026

Este documento preserva o histórico da implementação. Caminhos `.worktrees/`, `/tmp/` e diretórios de evidência identificam a máquina de origem; seus logs/recibos brutos não integram o checkpoint e não constituem validação reproduzida nesta publicação. Consultar a passagem `docs/engineering/payroll-reactive-g4-20261021/PASSAGEM-20261024.md` no checkpoint backend. Fontes preservadas em PR draft; reconciliação com main, aceite funcional e integração continuam pendentes. Nenhum ensaio, deploy ou release foi autorizado nesta etapa.
