# Revisar skill praxis: praxis-dto-annotations

## Objetivo

Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill praxis-dto-annotations para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos.

O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.

## Skill

- Familia: praxis
- Caminho: codex-skills/praxis-dto-annotations/
- Descricao atual: Annotate or review Java DTOs, FilterDTOs, command DTOs, and OpenAPI metadata for hosts that use praxis-metadata-starter. Use when Codex must fill or correct @Schema, @UISchema, @Filterable, @DomainGovernance, AiUsagePolicy, FieldControlType, x-ui labels/help text/icons/groups/order/visibility/valuePresentation/numericFormat/mask, table display formatting, option endpoints, optionSource/entityLookup metadata, or PT-BR domain documentation in Praxis backend projects.

## Foco da revisao

- Confirmar aderencia aos recursos oficiais e atuais da plataforma Praxis.
- Remover ou corrigir guidance que incentive workaround local, API paralela ou abstracao fora do owner canonico.
- Verificar se a skill usa recursos ricos do Praxis: metadata, schemas, x-ui, actions, surfaces, capabilities, option sources, runtime Angular, starters e contratos publicos aplicaveis.

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
- [ ] Rodar scripts/audit-praxis-skills.ps1 -Family praxis apos qualquer ajuste.

## Criterios de aceite

- A skill orienta implementacao/revisao com alto nivel de qualidade e velocidade.
- A skill nao incentiva remendos locais quando existe recurso Praxis canonico.
- Os recursos ricos do Praxis relacionados ao escopo da skill estao mencionados e roteados corretamente.
- O agente usuario da skill sabe quando aplicar, quando combinar com outra skill e quando abrir follow-up de plataforma.
- O manifesto permanece consistente, com hashes atualizados.
