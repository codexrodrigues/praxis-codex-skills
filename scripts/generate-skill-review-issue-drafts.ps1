[CmdletBinding()]
param(
    [string]$Repository = 'codexrodrigues/praxis-codex-skills',
    [string]$DraftRoot = 'docs/issue-drafts/skill-reviews'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

New-Item -ItemType Directory -Path $DraftRoot -Force | Out-Null

$skills = Get-ChildItem -LiteralPath 'codex-skills' -Directory |
    Where-Object { $_.Name -like 'praxis-*' -or $_.Name -like 'ergon-*' } |
    Sort-Object Name |
    ForEach-Object {
        $skill = $_.Name
        $skillMd = Join-Path $_.FullName 'SKILL.md'
        $description = (Select-String -Path $skillMd -Pattern '^description:' | Select-Object -First 1).Line -replace '^description:\s*', ''
        $family = if ($skill -like 'praxis-*') { 'praxis' } else { 'ergon-migration' }

        [pscustomobject]@{
            Family = $family
            Skill = $skill
            Description = $description
            Path = "codex-skills/$skill/"
        }
    }

foreach ($skill in $skills) {
    $title = "Revisar skill $($skill.Family): $($skill.Skill)"
    $focus = if ($skill.Family -eq 'praxis') {
        @(
            '- Confirmar aderencia aos recursos oficiais e atuais da plataforma Praxis.'
            '- Remover ou corrigir guidance que incentive workaround local, API paralela ou abstracao fora do owner canonico.'
            '- Verificar se a skill usa recursos ricos do Praxis: metadata, schemas, x-ui, actions, surfaces, capabilities, option sources, runtime Angular, starters e contratos publicos aplicaveis.'
        )
    }
    else {
        @(
            '- Confirmar que a skill conduz o processo Ergon/Archon sem redefinir contratos da plataforma Praxis.'
            '- Verificar se cada uso de recurso Praxis chama a skill Praxis correta e preserva a direcao de dependencia ergon-* -> praxis-*.'
            '- Validar que o fluxo de migracao mantem evidencia, gates, paridade, seguranca HADES/legado e handoff sem atalhos frageis.'
        )
    }

    $body = @(
        "# $title"
        ''
        '## Objetivo'
        ''
        "Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill $($skill.Skill) para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos."
        ''
        'O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.'
        ''
        '## Skill'
        ''
        "- Familia: $($skill.Family)"
        "- Caminho: $($skill.Path)"
        "- Descricao atual: $($skill.Description)"
        ''
        '## Foco da revisao'
        ''
        $focus
        ''
        '## Checklist minimo'
        ''
        '- [ ] Ler `SKILL.md` inteiro e os arquivos em `references/`, `scripts/` e `agents/` quando aplicavel.'
        '- [ ] Confirmar que a descricao/frontmatter dispara a skill nos cenarios corretos e nao em cenarios amplos demais.'
        '- [ ] Validar progressive disclosure: `SKILL.md` deve conter o fluxo essencial e apontar referencias sem carregar contexto excessivo.'
        '- [ ] Verificar se a skill aponta para owners canonicos corretos da plataforma Praxis.'
        '- [ ] Conferir se recursos ricos e atuais do Praxis sao usados antes de recomendar codigo customizado.'
        '- [ ] Identificar guidance obsoleto, ambiguo, duplicado, local demais ou contrario ao contrato canonico.'
        '- [ ] Confirmar interoperacao com skills relacionadas declaradas no manifesto.'
        '- [ ] Revisar exemplos, templates, comandos e checklists para garantir que um agente consiga executar a tarefa sem lacunas criticas.'
        '- [ ] Atualizar `skillMdSha256` e `treeSha256` no manifesto quando houver mudanca.'
        "- [ ] Rodar `scripts/audit-praxis-skills.ps1 -Family $($skill.Family)` apos qualquer ajuste."
        ''
        '## Criterios de aceite'
        ''
        '- A skill orienta implementacao/revisao com alto nivel de qualidade e velocidade.'
        '- A skill nao incentiva remendos locais quando existe recurso Praxis canonico.'
        '- Os recursos ricos do Praxis relacionados ao escopo da skill estao mencionados e roteados corretamente.'
        '- O agente usuario da skill sabe quando aplicar, quando combinar com outra skill e quando abrir follow-up de plataforma.'
        '- O manifesto permanece consistente, com hashes atualizados.'
    ) -join "`n"

    Set-Content -LiteralPath (Join-Path $DraftRoot "$($skill.Skill).md") -Value $body -Encoding UTF8
}

$index = @(
    '# Skill Review Issue Drafts'
    ''
    'A criacao direta de issues pelo conector falhou com `403 Resource not accessible by integration`. Estes drafts foram gerados para criacao manual ou via script quando a permissao de Issues estiver habilitada.'
    ''
    "Repo alvo: $Repository"
    ''
)

foreach ($skill in $skills) {
    $index += "- [$($skill.Skill)](skill-reviews/$($skill.Skill).md)"
}

Set-Content -LiteralPath 'docs/issue-drafts/README.md' -Value ($index -join "`n") -Encoding UTF8

Write-Host "Generated $($skills.Count) issue draft(s)."
