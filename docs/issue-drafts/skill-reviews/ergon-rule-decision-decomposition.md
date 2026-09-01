# Revisar skill ergon-migration: ergon-rule-decision-decomposition

## Objetivo

Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill ergon-rule-decision-decomposition para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos.

O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.

## Skill

- Familia: ergon-migration
- Caminho: codex-skills/ergon-rule-decision-decomposition/
- Descricao atual: Build and review evidence-bound RF-03 decision-pack drafts for Ergon rule migration. Use after RF-01 source extraction and an RF-02 preliminary profile when Codex must map every structural occurrence exactly once into explicit atomic decision proposals, preserve source provenance, outcomes, facts, order, dependencies and unknowns, run the canonical RF-03 generator and tests, or prepare a governed review queue without inventing business semantics, recording human approval, selecting a runtime target, or generating code.

## Classificacao inicial

- Projeto canonico: ergon-migration
- Area: migration
- Risco: medio
- Estado: backlog

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
- [ ] Mapear `AGENTS.md`, APIs publicas, implementacao, specs, docs, manifests, exemplos e consumidores diretamente relevantes.
- [ ] Classificar cada gap como `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente` ou `lacuna-real-de-contrato`.
- [ ] Atualizar `skillMdSha256` e `treeSha256` no manifesto quando houver mudanca.
- [ ] Rodar `python3 scripts/preflight-python-fallbacks.py` apos qualquer ajuste.
- [ ] Quando precisar de diagnostico focado, rodar `scripts/audit-praxis-skills.ps1 -Family ergon-migration` ou `python3 scripts/audit-praxis-skills.py --family ergon-migration`.

## Prova operacional obrigatoria

- [ ] Executar um cenario feliz representativo usando a skill revisada.
- [ ] Executar um cenario de risco, ambiguidade ou edge case relevante para o escopo.
- [ ] Executar um cenario adversarial em que a skill deve rejeitar workaround local, contrato paralelo ou decisao fora do owner canonico.
- [ ] Rodar a menor validacao focal confiavel do codigo Praxis auditado e registrar comando e resultado.
- [ ] Comparar o resultado produzido com as decisoes canonicas esperadas, sem considerar apenas o preflight estrutural.

## Evidencias para encerramento

- [ ] Registrar arquivos-fonte e contratos inspecionados.
- [ ] Registrar alteracoes realizadas na skill, referencias, scripts ou metadata.
- [ ] Registrar comandos locais, resultados, limitacoes e validacoes nao executadas.
- [ ] Associar PR ou commit e publicar a auditoria final na issue.
- [ ] Declarar se a skill ficou `aprovada-com-evidencia`, `implementada-sem-auditoria-funcional`, `precisa-reabertura` ou `skill-desatualizada-por-drift`.

## Criterios de aceite

- A skill orienta implementacao/revisao com alto nivel de qualidade e velocidade.
- A skill nao incentiva remendos locais quando existe recurso Praxis canonico.
- Os recursos ricos do Praxis relacionados ao escopo da skill estao mencionados e roteados corretamente.
- O agente usuario da skill sabe quando aplicar, quando combinar com outra skill e quando abrir follow-up de plataforma.
- O manifesto permanece consistente, com hashes atualizados.
- A prova operacional demonstra que a skill conduz pelo menos um fluxo real e rejeita um antipadrao relevante.
- A issue contem evidencia suficiente para que outra pessoa reproduza a auditoria local.
