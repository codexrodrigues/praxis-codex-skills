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

Em gates automatizados ou de readiness, acrescente `-FailOnDrift`; o modo sem
esse switch é diagnóstico e preserva compatibilidade para revisão de inventário.

Se PowerShell não estiver disponível, use os fallbacks Python canônicos:

```bash
python3 scripts/preflight-python-fallbacks.py
python3 scripts/audit-praxis-skills.py --family praxis
python3 scripts/audit-praxis-skills.py --family ergon-migration
```

No fallback Python, use `--fail-on-drift` para o mesmo comportamento bloqueante.

Quando `SKILL.md` for alterado, valide a skill com `quick_validate.py` se ele estiver disponível no ambiente Codex local. Se `quick_validate.py` estiver indisponível por dependência local, use `python3 scripts/validate-praxis-skills.py` no menor escopo suficiente.

## Separação Praxis x Ergon

Não coloque orientação Ergon, Archon, HADES, `docs-legado`, `ERGadm*`, `PCK_*`, `C_ERGON` ou regras de migração específicas dentro de skills `praxis-*`. Esses detalhes pertencem às skills `ergon-*`.

Orientação genérica de plataforma sobre hosts legados, bancos restritos, DTOs, schemas, UI runtime, options, actions, surfaces e capabilities pode permanecer nas skills `praxis-*`.

## Economia de GitHub Actions

O padrão durante desenvolvimento é zero execuções remotas. Valide localmente o escopo alterado; commits, PRs, documentação interna e conclusão de tarefas não são motivos para iniciar Actions. Use os workflows manuais somente no fechamento autorizado de uma versão/publicação ou na prova necessária do host já implantado. Não use `[skip ci]` como mecanismo principal nem desabilite checks/proteções para economizar.

Antes de push, tag ou dispatch, confira os gatilhos reais de `.github/workflows/`. Tags de release publicam artefatos: não criá-las para testar a automação. Diagnostique localmente antes de repetir um job; conserve a evidência da revisão e dos artefatos usados. Monitores operacionais explicitamente mantidos são independentes do CI de commits. Consulte [ACTIONS-RELEASE-POLICY.md](ACTIONS-RELEASE-POLICY.md) para os pontos de entrada e recuperação.
