# Fechamento das skills para editores e componentes — 2026-09-08

## Escopo

Classificação: `docs-apenas` neste repositório de skills, derivada de uma
mudança transversal e de contratos públicos no workspace Angular. A auditoria
cruzou o estado atual da worktree `praxis-ui-angular-corporate-gate`, seu diff,
os relatórios de implementação e interação de 7–8 de setembro e as fontes
canônicas do portfólio `praxis-codex-skills`.

O workspace Angular auditado possui mudanças em Core, Settings Panel, Page
Builder, Dynamic Form, Table, List, Charts e Dynamic Fields. Esta rodada não
reescreve runtime nem apresenta os resultados históricos como testes recém
executados. O objetivo é preservar nas skills as decisões repetíveis que o
trabalho revelou.

## Fonte canônica reconciliada

O `codex-skills/` reduzido da raiz do monorepo não contém o portfólio
especializado atual. A fonte escolhida foi a worktree limpa
`widget-identity-skills-integration`, que já continha:

- o fechamento do Editor de Conexões;
- identidade/avatar de widget e carregamento seguro do detalhe;
- a orientação de Save após Apply no Settings Panel.

Uma worktree anterior, `actions-economy/praxis-codex-skills`, continha
orientações ainda não integradas sobre Form, Table, i18n, transporte de schema,
Surface JSON e seleção. Os arquivos foram comparados com a linha mais recente e
somente diferenças respaldadas pelo código e pelos relatórios foram
reconciliadas. Alterações locais das worktrees de origem foram preservadas.

## Cobertura consolidada

| Área implementada | Skill dona ou complementar | Regra consolidada |
| --- | --- | --- |
| Editor de Conexões | `praxis-page-builder-composition`, `praxis-page-builder-authoring`, `praxis-ui-product-design`, `praxis-angular-accessibility-governance` | Separação de inspeção e mutação, mapa/lista compacta, geometria, zoom, foco, camadas, catálogos, legendas, estado transient e Surface draft inválido |
| Sessões de editores de widget | `praxis-settings-panel-shell`, `praxis-page-builder-authoring` | Owner transitório, árvore pai/filho, substituição mediada, reentrada, backdrop assíncrono, inputs tardios, cancelamento após destruição e continuidade do draft |
| Shell, avatar e ações | `praxis-core-widget-observations`, `praxis-core-composition-runtime` | Identidade por bindings/transient, fallback seguro de avatar, comando estável, disponibilidade transitória, guard de execução e limpeza após destruição |
| Charts no shell | `praxis-charts-authoring-settings` | `openConfigEditor` por comando, disponibilidade localizada, rechecagem após contexto assíncrono e owner `DestroyRef` |
| Form document e apresentação | `praxis-form-editor-document-roundtrip`, `praxis-form-schema-runtime-modes` | Bindings de modo/apresentação/empty state, baseline de Apply separado de Reset, isolamento de DI, schema parcial, atributos server-owned, Automático/true/false e reload |
| Layout do Form | `praxis-form-layout-canvas` | Grade inteira, ocupação responsiva, visibilidade sem perda de geometria, mover campo por teclado, destinos por IDs, visual blocks, continuidade de foco, rename/empty section e serviço por draft |
| Ações Form/List/Table | `praxis-core-surface-materialization`, skills de authoring dos três owners | Raw Surface JSON participa de dirty/valid, sobrevive a navegação, bloqueia Apply/Save e é descartado explicitamente sem publicar o último payload válido |
| Table authoring | `praxis-table-authoring-settings`, `praxis-table-filter-actions` | Config sparse sem defaults incidentais, projeção de disponibilidade fora do documento, origem de disabled, sincronização visual/JSON, explicação de ações e i18n do filtro |
| Seleção e paginação | `praxis-table-selection-export-runtime` | Evento semântico único do radio, separação de row click e limpeza antes da paginação conforme a política persistida |
| Persistência remota | `praxis-config-runtime-persistence` | Scope de resposta é proveniência, ownership vem do request, ETag não cruza USER/TENANT e PUT só fecha o aceite após materialização em reload |
| Transporte de schema | `praxis-core-resource-runtime` | Timeout/cancelamento por consumidor, deduplicação, 304/refetch, headers, late response e distinção entre bloqueio do cliente e latência backend |
| i18n em editores | `praxis-core-i18n-resource-copy` | Lookup direto sem reconstrução do catálogo por texto, precedência de camadas, masking vazio e atualização dinâmica sem cache obsoleto |
| Date range acessível | `praxis-fields-text-number-time-controls` | Nomes distintos e localizados para início/fim, overrides explícitos e prova no DOM Material após renderização |

## Skills atualizadas nesta reconciliação

Foram alteradas 17 árvores existentes:

- `praxis-charts-authoring-settings`
- `praxis-config-runtime-persistence`
- `praxis-core-i18n-resource-copy`
- `praxis-core-resource-runtime`
- `praxis-core-surface-materialization`
- `praxis-core-widget-observations`
- `praxis-fields-text-number-time-controls`
- `praxis-form-actions-hooks-runtime`
- `praxis-form-editor-document-roundtrip`
- `praxis-form-layout-canvas`
- `praxis-list-authoring-settings`
- `praxis-page-builder-authoring`
- `praxis-page-builder-composition`
- `praxis-settings-panel-shell`
- `praxis-table-authoring-settings`
- `praxis-table-filter-actions`
- `praxis-table-selection-export-runtime`

O manifesto teve somente os hashes correspondentes atualizados. Descrições e
dependências não mudaram, portanto os drafts gerados de revisão não precisaram
ser alterados.

As skills `praxis-form-authoring-settings`,
`praxis-settings-roundtrip-authoring`,
`praxis-angular-i18n-governance`, `praxis-angular-docs-playgrounds`,
`praxis-list-docs-evidence` e as skills de runtime/AI de Charts foram
revisadas e preservadas: elas já encaminham corretamente para os owners acima e
não precisam duplicar regras específicas.

## Classificação de aderência

Não foi encontrada uma nova `lacuna-real-de-contrato` de skill. Os gaps eram:

- `ja-suportado-so-ux`: hierarquia, foco, copy, previews e identificação;
- `ja-suportado-mal-nomeado-ou-mal-materializado`: scope de fallback,
  apresentação automática, disponibilidade transitória e defaults de editor;
- `suportado-parcialmente`: round-trip entre editor, runtime, persistência,
  reload, consumidores e validação de rascunhos.

As responsabilidades cabem nas skills existentes. Criar uma skill nova
fragmentaria os mesmos fluxos de Page Builder, Form, Table e Settings Panel.

## Validação

- `validate-praxis-skills.py` aprovou as 17 árvores atualizadas.
- `preflight-python-fallbacks.py` aprovou 41 testes das ferramentas,
  compilação Python, estrutura das duas famílias, drafts, instalação temporária
  e auditorias.
- Manifesto Praxis: 167 entradas, zero fonte inválida, zero ausência e zero
  diretório de fonte fora do manifesto.
- Sincronização focal atualizou somente as 10 árvores que ainda divergiam da
  instalação; sete já coincidiam com a orientação recuperada.
- Auditoria final instalada com `--fail-on-drift`: Praxis 167/167 e Ergon
  19/19, zero drift, zero ausência e zero fonte inválida.
- `git diff --check` passou.
- O `quick_validate.py` do ambiente foi tentado para as 17 skills, mas não
  executa sem PyYAML. Conforme o AGENTS deste repositório, foi usado o validador
  Python canônico sem dependências, que passou.

Nenhum teste Angular foi repetido por esta alteração documental. Os testes,
builds e provas de navegador permanecem nos relatórios dos respectivos owners;
esta auditoria verificou que suas decisões estão representadas nas skills, sem
transformar contagens históricas em gates permanentes.

## Estado para encerramento

A fonte versionável, o manifesto e a instalação local estão coerentes. Nenhuma
skill paralela foi criada, nenhum contrato Angular/backend foi alterado, e não
há manifesto AI, registry, corpus HTTP ou documentação pública gerada a
regenerar por causa desta rodada de skills. Commit, push e publicação remota
permanecem operações separadas; esta auditoria será registrada apenas em um
commit local, sem envio ao remoto.
