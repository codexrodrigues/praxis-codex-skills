# Praxis Codex Skills

Canonical repository for Codex skills used by the Praxis platform and Ergon/Archon migration workflows.

## Families

- `praxis`: general Praxis platform skills.
- `ergon-migration`: Ergon/Archon migration skills. These may depend on `praxis` skills, but `praxis` skills must not depend on `ergon-*` skills.

## Audit

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\audit-praxis-skills.ps1 -Family praxis
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\audit-praxis-skills.ps1 -Family ergon-migration
```

## Sync

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\sync-praxis-skills.ps1 -Family praxis
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\sync-praxis-skills.ps1 -Family ergon-migration
```

The sync only manages skills listed in the selected manifest. It does not remove unrelated local skills from `$CODEX_HOME/skills`.

Use `-Force` only when intentionally replacing a locally modified managed skill with the canonical version from this repository.

## Manifests

Each family manifest lives in `codex-skills/` and records:

- family name and version;
- skill list and dependency direction;
- `skillMdSha256` for trigger/instruction drift;
- `treeSha256` for the complete skill tree, including `references/`, `scripts/`, and `agents/`.

When any file inside a skill changes, update the corresponding `treeSha256`; when `SKILL.md` changes, update both `skillMdSha256` and `treeSha256`.

Migration workspaces should pin these manifests by hash instead of vendoring skill contents.
