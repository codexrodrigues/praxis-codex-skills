# Revisar skill ergon-migration: ergon-table-rule-audit

## Objetivo

Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill ergon-table-rule-audit para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos.

O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.

## Skill

- Familia: ergon-migration
- Caminho: codex-skills/ergon-table-rule-audit/
- Descricao atual: Audit Ergon legacy Oracle table rules for Java/Spring migration. Use when Codex needs, given an Ergon table name, to identify product rules, generated triggers/DML/audit infrastructure, client custom rules, active/inactive status, execution order, and nested dependencies across ALL_TRIGGERS, ALL_SOURCE, ALL_DEPENDENCIES, generated PCK table packages, generated PND packages, PCK_EXEC_EP_CERG, HADES.PACK_EXEC_SPROC, HADES.HAD_CAD_SPROC, HADES.HAD_CAD_MULT_EPS, and C_ERGON POA_/EP__ functions.

## Foco da revisao

- Confirmar que a skill conduz o processo Ergon/Archon sem redefinir contratos da plataforma Praxis.
- Verificar se cada uso de recurso Praxis chama a skill Praxis correta e preserva a direcao de dependencia ergon-* -> praxis-*.
- Validar que o fluxo de migracao mantem evidencia, gates, paridade, seguranca HADES/legado e handoff sem atalhos frageis.

## Checklist minimo

- [ ] Ler `SKILL.md` inteiro e os arquivos em `references/`, `scripts/` e `agents/` quando aplicavel.
- [ ] Confirmar que a descricao/frontmatter dispara a skill nos cenarios corretos e nao em cenarios amplos demais.
- [ ] Validar progressive disclosure: `SKILL.md` deve conter o fluxo essencial e apontar referencias sem carregar contexto excessivo.
- [ ] Verificar se a skill aponta para owners canonicos corretos da plataforma Praxis.
- [ ] Conferir se recursos ricos e atuais do Praxis sao usados antes de recomendar codigo customizado.
- [ ] Identificar guidance obsoleto, ambiguo, duplicado, local demais ou contrario ao contrato canonico.
- [ ] Confirmar interoperacao com skills relacionadas declaradas no manifesto.
- [ ] Revisar exemplos, templates, comandos e checklists para garantir que um agente consiga executar a tarefa sem lacunas criticas.
- [ ] Atualizar `skillMdSha256` e `treeSha256` no manifesto quando houver mudanca.
- [ ] Rodar scripts/audit-praxis-skills.ps1 -Family ergon-migration apos qualquer ajuste.

## Criterios de aceite

- A skill orienta implementacao/revisao com alto nivel de qualidade e velocidade.
- A skill nao incentiva remendos locais quando existe recurso Praxis canonico.
- Os recursos ricos do Praxis relacionados ao escopo da skill estao mencionados e roteados corretamente.
- O agente usuario da skill sabe quando aplicar, quando combinar com outra skill e quando abrir follow-up de plataforma.
- O manifesto permanece consistente, com hashes atualizados.
