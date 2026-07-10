# AGENTS.md - Praxis Codex Skills

Escopo: este arquivo vale para todo o repositório `praxis-codex-skills`.

## Fonte Canônica

Este repositório é a fonte canônica versionada das skills Codex da plataforma Praxis e da migração Ergon/Archon.

- Skills gerais da plataforma ficam na família `praxis`.
- Skills específicas da migração Ergon/Archon ficam na família `ergon-migration`.
- Skills `praxis-*` não podem depender de skills `ergon-*`.
- Skills `ergon-*` podem depender de skills `praxis-*`.

## Manifestos

Toda skill versionada deve estar em exatamente um manifesto:

- `codex-skills/praxis-skills.manifest.json`
- `codex-skills/ergon-migration-skills.manifest.json`

Cada entrada deve manter:

- `skillMdSha256`: hash do `SKILL.md`;
- `treeSha256`: hash da árvore completa da skill;
- `dependencies`: dependências explícitas entre skills.

Depois de alterar qualquer arquivo de skill, atualize o manifesto correspondente e rode auditoria.

## Validação Mínima

Antes de concluir mudanças:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\audit-praxis-skills.ps1 -Family praxis
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\audit-praxis-skills.ps1 -Family ergon-migration
```

Se PowerShell não estiver disponível, use os fallbacks Python canônicos:

```bash
python3 scripts/preflight-python-fallbacks.py
python3 scripts/audit-praxis-skills.py --family praxis
python3 scripts/audit-praxis-skills.py --family ergon-migration
```

Quando `SKILL.md` for alterado, valide a skill com `quick_validate.py` se ele estiver disponível no ambiente Codex local. Se `quick_validate.py` estiver indisponível por dependência local, use `python3 scripts/validate-praxis-skills.py` no menor escopo suficiente.

## Separação Praxis x Ergon

Não coloque orientação Ergon, Archon, HADES, `docs-legado`, `ERGadm*`, `PCK_*`, `C_ERGON` ou regras de migração específicas dentro de skills `praxis-*`. Esses detalhes pertencem às skills `ergon-*`.

Orientação genérica de plataforma sobre hosts legados, bancos restritos, DTOs, schemas, UI runtime, options, actions, surfaces e capabilities pode permanecer nas skills `praxis-*`.
