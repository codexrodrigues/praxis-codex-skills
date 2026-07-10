# Revisar skill praxis: praxis-fields-runtime-loader

## Objetivo

Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill praxis-fields-runtime-loader para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos.

O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.

## Skill

- Familia: praxis
- Caminho: codex-skills/praxis-fields-runtime-loader/
- Descricao atual: Use when changing or reviewing @praxisui/dynamic-fields or praxis-dynamic-fields package runtime rendering, DynamicFieldLoaderDirective behavior, ComponentRegistryService registrations, controlType normalization, selector mappings, package-owned field loading, host custom field registration, hot metadata updates, or runtime coverage claims for metadata-driven Angular fields.

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
- [ ] Rodar `python3 scripts/preflight-python-fallbacks.py` apos qualquer ajuste.
- [ ] Quando precisar de diagnostico focado, rodar `scripts/audit-praxis-skills.ps1 -Family praxis` ou `python3 scripts/audit-praxis-skills.py --family praxis`.

## Criterios de aceite

- A skill orienta implementacao/revisao com alto nivel de qualidade e velocidade.
- A skill nao incentiva remendos locais quando existe recurso Praxis canonico.
- Os recursos ricos do Praxis relacionados ao escopo da skill estao mencionados e roteados corretamente.
- O agente usuario da skill sabe quando aplicar, quando combinar com outra skill e quando abrir follow-up de plataforma.
- O manifesto permanece consistente, com hashes atualizados.
