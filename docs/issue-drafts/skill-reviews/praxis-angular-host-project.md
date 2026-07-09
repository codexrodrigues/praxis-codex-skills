# Revisar skill praxis: praxis-angular-host-project

## Objetivo

Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill praxis-angular-host-project para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos.

O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.

## Skill

- Familia: praxis
- Caminho: codex-skills/praxis-angular-host-project/
- Descricao atual: Create or evolve Angular host applications that consume Praxis UI packages. Use when Codex must scaffold a new Angular project using published @praxisui/* packages, adapt a host from praxis-ui-quickstart, wire API_URL/PAX_FETCH_HEADERS/GenericCrudService/providers, create resource-oriented table/form/crud/list routes, configure local or remote Praxis UI runtime config, validate resourcePath/schema-driven integration, or decide which Praxis UI companion skills apply for authoring, dynamic-fields, config storage, or visual QA.

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
