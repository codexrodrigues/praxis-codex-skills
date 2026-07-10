# Praxis Codex Skills

Canonical repository for Codex skills used by the Praxis platform and Ergon/Archon migration workflows.

## Families

- `praxis`: general Praxis platform skills.
- `ergon-migration`: Ergon/Archon migration skills. These may depend on `praxis` skills, but `praxis` skills must not depend on `ergon-*` skills.

## Discovery And Routing

Do not assume migration roadmaps, host docs, or one orchestration skill will enumerate every `praxis-*` skill by name.

The intended operating model is:

- roadmap or orchestration skill closes phase gates and task class;
- the agent then routes by domain and surface, not by remembering a fixed list of skill names;
- the canonical discovery source is the family manifest plus the skill frontmatter/descriptions in `codex-skills/`;
- `ergon-*` flows may call into `praxis-*` skills when the work touches shared platform runtime, contracts, authoring, validation, or UX;
- `praxis-*` skills must stay free of Ergon-specific guidance even when they are used during migration.

When the runtime environment exposes skill inventory/discovery, the agent should search the Praxis family by topic such as `table`, `form`, `crud`, `list`, `rich-content`, `files-upload`, `page-builder`, `settings`, `charts`, `metadata-editor`, `ai`, `i18n`, `public-api`, or `validation`, instead of relying on explicit mentions in migration documentation.

When the runtime environment does not expose discovery, the fallback is to consult this repository canonically: start from the most relevant gateway skill, then fan out through manifest dependencies and companion-skill sections.

## Audit

Preferred local Python fallback preflight:

```bash
python3 scripts/preflight-python-fallbacks.py
```

The same preflight runs in GitHub Actions on pull requests and pushes to `main`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\audit-praxis-skills.ps1 -Family praxis
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\audit-praxis-skills.ps1 -Family ergon-migration
```

When PowerShell is unavailable, use the Python fallback. It computes `skillMdSha256`
from `SKILL.md` bytes and `treeSha256` from sorted `SHA256  relative/path` entries,
matching the manifest semantics used by the PowerShell scripts.

```bash
python3 scripts/audit-praxis-skills.py --family praxis
python3 scripts/audit-praxis-skills.py --family ergon-migration
```

Family-scoped audits report source directories from other known family manifests separately as
`sourceInOtherFamilyManifest`. `sourceNotInManifest` is reserved for directories not tracked by
any known family manifest.

## Structure Validation

When `quick_validate.py` is unavailable because local Python lacks optional packages,
use the repository validator:

```bash
python3 scripts/validate-praxis-skills.py --family praxis
python3 scripts/validate-praxis-skills.py --family ergon-migration
python3 scripts/validate-praxis-skills.py codex-skills/praxis-ai-assistant-runtime
```

Focused Python fallback tests:

```bash
python3 -m unittest discover -s tests
```

## Issue Drafts

Generate skill review issue drafts from the canonical manifests:

```bash
python3 scripts/generate-skill-review-issue-drafts.py
python3 scripts/generate-skill-review-issue-drafts.py --check
python3 scripts/validate-issue-drafts.py
```

The PowerShell generator delegates to the Python generator for compatibility.

## Sync

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\sync-praxis-skills.ps1 -Family praxis
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\sync-praxis-skills.ps1 -Family ergon-migration
```

Python fallback:

```bash
python3 scripts/sync-praxis-skills.py --family praxis
python3 scripts/sync-praxis-skills.py --family ergon-migration
```

The sync only manages skills listed in the selected manifest. It does not remove unrelated local skills from `$CODEX_HOME/skills`.

Use `-Force` / `--force` only when intentionally replacing a locally modified managed skill with the canonical version from this repository.

## Manifests

Each family manifest lives in `codex-skills/` and records:

- family name and version;
- skill list and dependency direction;
- `skillMdSha256` for trigger/instruction drift;
- `treeSha256` for the complete skill tree, including `references/`, `scripts/`, and `agents/`.

When any file inside a skill changes, update the corresponding `treeSha256`; when `SKILL.md` changes, update both `skillMdSha256` and `treeSha256`.

Migration workspaces should pin these manifests by hash instead of vendoring skill contents.
