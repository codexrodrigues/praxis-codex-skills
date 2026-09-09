# Fechamento das skills para editores e componentes — 2026-09-08

> Revisão crítica posterior: o fechamento abaixo registra a consolidação inicial
> `6b6746a`. A seção **Revisão crítica e limites de encerramento** amplia a janela
> para 4–8 de setembro e prevalece sobre qualquer leitura de certificação geral.
> Igualdade de hashes certifica instalação, não cobertura semântica nem produto.

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

## Revisão crítica e limites de encerramento

Classificação desta revisão: `docs-apenas`. Fonte Angular inspecionada:
worktree `praxis-ui-angular-corporate-gate`, HEAD
`df274485ec0240a47bbf2e95ffca84159e84012a`, mais mudanças locais e arquivos ainda
não rastreados. Fonte de skills antes desta revisão: `c08e86d`, posterior ao
fechamento inicial; esse commit acrescentou orientação de navegação em painel,
leitura do editor de widget e contraste dos eixos. Não foi atribuído à validação
anterior. As árvores locais de outras tarefas foram preservadas.

### Correções do fechamento

- A janela anterior enfatizava relatórios de 7–8 de setembro. A revisão consultou
  também o histórico relevante de 4–8 de setembro, incluindo `929c943ff`
  (composição), `1346ad3f4` (resize e integridade), `49cbc7c09`
  (master-detail), `edb8c2565` (authoring governado), `8c70458a1` e
  `0e2b49edb` (tabela). O inventário de commits inclui trabalho de outras tarefas;
  presença no histórico não implica autoria desta tarefa ou certificação nova.
- Orientações genéricas não bastavam para preservar três decisões concretas:
  margem lateral da página, apresentação governada de filtros e preenchimento
  de `gapBottom`. As skills existentes foram detalhadas, sem novo contrato.
- A skill de governança passou a exigir separação explícita entre cobertura
  semântica, paridade instalada, validação recente e integração remota.
- As 17 árvores e os 41 testes citados acima são resultados da primeira rodada.
  Esta revisão altera quatro skills existentes; não são 21 skills distintas,
  pois três delas já pertenciam ao conjunto anterior.

### Rastreabilidade das lacunas corrigidas

Os caminhos abaixo são relativos ao repositório Angular e apontam para fonte,
documentação e testes inspecionados; os testes não foram reexecutados nesta revisão.

| Comportamento | Fonte e documentação | Prova existente inspecionada | Skill corrigida |
| --- | --- | --- | --- |
| Margem lateral, zero e herança | `projects/praxis-page-builder/src/lib/page-layout-spacing.ts`; README Page Builder, seção Margem lateral compartilhada; Core `dynamic-widget-page.component.ts` | `page-config-editor.component.spec.ts` e `dynamic-page-config-editor.component.spec.ts`: limpar, preservar siblings e Reset | `praxis-page-builder-authoring` |
| Resize, limites e tamanho de conteúdo | README Page Builder, Direct canvas manipulation; `projects/praxis-core/docs/rfc-dynamic-page-canvas-runtime.md` | `canvas-content-size.spec.ts`, `canvas-resize-placement.spec.ts`; cenário `remote-canvas-resize-real-backend.playwright.spec.ts` como roteiro de integração | `praxis-page-builder-authoring` |
| Título/ícone do filtro e preferências | `projects/praxis-table/src/lib/praxis-table.json-api.md`, Filter presentation; `PraxisFilterComponent` e Filter Settings | `praxis-filter.component.spec.ts`: ícone vazio, texto herdado, apresentação persistida e persistência desabilitada | `praxis-table-filter-actions` |
| Espaço após seção, preservando zero | `LayoutEditorComponent.canApplyAll/applyGapToAll`; `projects/praxis-dynamic-form/docs/section-spacing-authoring-2026-09-08.md`; JSON API do Layout Editor | `layout-editor-toolbar.spec.ts`: zero, valor explícito, proposta sem emissão, ausência de `gapCustomized` | `praxis-form-layout-canvas` |
| Retrospectiva sem superestimar aceite | Este relatório e a divergência entre paridade de instalação e cobertura documental | Auditorias de manifesto e inspeção semântica são evidências separadas | `praxis-skill-authoring-governance` |

Avatar, título/subtítulo formatado, falha de seleção e fronteira do shorthand
agentic já têm orientação específica em `praxis-core-widget-observations`,
`praxis-core-composition-runtime/references/selection-presentation.md` e
`praxis-form-schema-runtime-modes`. Conferidos contra
`projects/praxis-core/docs/composition-value-format.md` e
`widget-identity-documentation-review.md`; não se duplicaram essas regras.
O estudo de contraste e os limites de navegação já estão refletidos no commit
posterior `c08e86d`; sua existência não resolve os defeitos que ele documenta.

### Pendências que impedem afirmar encerramento integral do produto

1. O estudo `projects/praxis-page-builder/test-dev/research/2026-09-08-editor-visual-coherence-study.md`
   registra gráficos com fundo escuro e parte do texto de tema claro. A causa
   de precedência não estava provada nesse registro. A skill de ECharts preserva
   explicitamente essa pendência; corrigir nomes de eixos não certifica contraste
   da composição. Exige investigação e prova focal no owner Charts.
2. `2026-09-08-widget-authoring-validation-summary.md`, no mesmo diretório,
   limita as provas de lifecycle/concorrência e leitor de tela. Evidência de ETag
   do laboratório não certifica toda combinação de editor, usuário e backend.
3. Código e parte da documentação Angular continuam em mudanças locais, inclusive
   arquivos não rastreados. A fonte das skills pode estar consolidada enquanto
   a integração e os artefatos públicos da implementação ainda precisam de um
   fechamento próprio. Esta revisão não afirma que o site publicado ou o pacote
   distribuído já contém o estado local.

O resultado é cobertura documental melhor rastreada no escopo inspecionado,
sem certificação exaustiva de todas as funcionalidades ou de produção. Nenhuma
alteração de runtime, manifesto AI, corpus HTTP ou registry foi feita nesta
revisão; esse fato não dispensa a integração dos derivados do trabalho original.

### Validação desta revisão crítica

- Validador estrutural canônico: quatro skills aprovadas; usado o fallback já
  estabelecido para o ambiente sem PyYAML. Não se repetiu a suite de 41 testes
  das ferramentas, pois nenhum script foi alterado.
- Drafts de revisão gerados continuam atuais; validador dos drafts e
  `git diff --check` aprovados.
- Manifesto: apenas hashes das quatro árvores alterados, sem novos contratos,
  descrições de ativação, dependências ou entradas.
- Antes da edição: 167/167 Praxis em paridade. Após revisar o dry-run e sincronizar
  apenas as quatro árvores: auditoria bloqueante Praxis 167/167 e Ergon 19/19,
  zero drift, ausência ou fonte inválida.
- Nenhum teste Angular, build ou percurso de navegador foi executado nesta rodada
  documental. Os caminhos de provas na tabela são evidência inspecionada e roteiro
  reproduzível, não novos resultados de execução.
