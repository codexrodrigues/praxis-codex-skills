# Revisar skill praxis: praxis-landing-registries-sitemap-playgrounds

## Objetivo

Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill praxis-landing-registries-sitemap-playgrounds para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos.

O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.

## Skill

- Familia: praxis
- Caminho: codex-skills/praxis-landing-registries-sitemap-playgrounds/
- Descricao atual: Use when Codex must update or audit praxis-ui-landing-page registries, published guide frontmatter, sitemap, llms.txt/llms-full.txt/llm-index.json, dynamic examples, live playgrounds, decision playground, table manifests, vendor docs sync, generated docs, and local validation for public Praxis docs.

## Classificacao inicial

- Projeto canonico: praxis-ui-landing-page
- Area: landing
- Risco: medio
- Estado: backlog

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
- [ ] Mapear `AGENTS.md`, APIs publicas, implementacao, specs, docs, manifests, exemplos e consumidores diretamente relevantes.
- [ ] Classificar cada gap como `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente` ou `lacuna-real-de-contrato`.
- [ ] Atualizar `skillMdSha256` e `treeSha256` no manifesto quando houver mudanca.
- [ ] Rodar `python3 scripts/preflight-python-fallbacks.py` apos qualquer ajuste.
- [ ] Quando precisar de diagnostico focado, rodar `scripts/audit-praxis-skills.ps1 -Family praxis` ou `python3 scripts/audit-praxis-skills.py --family praxis`.

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
