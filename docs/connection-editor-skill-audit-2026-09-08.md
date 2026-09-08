# Auditoria das skills após a evolução do Editor de conexões

Data: 2026-09-08. Classe: `docs-apenas`. Escopo: alterações desta sequência de
trabalho no Editor de conexões, incluindo a projeção editorial do filtro e a
validação no Dynamic Page Lab. Não atribui à tarefa alterações concorrentes em
formulários, shell de widgets, charts ou outros editores.

## Conclusão

Sete skills existentes precisavam de atualização. A cobertura anterior era boa
para arquitetura, tokens, i18n e round-trip, mas insuficiente para preservar
invariantes descobertas durante a implementação. A conclusão anterior de
“nenhum drift de skill identificado” foi ampla demais: não havia contradição
com os princípios gerais, porém havia lacunas procedimentais recorrentes.

As lacunas foram corrigidas na fonte canônica e nas sete instalações locais.
Nenhuma skill nova, contrato público, dependência entre famílias ou alteração
de runtime foi necessária. A referência detalhada ficou na skill de composição
do Page Builder, evitando duplicar o algoritmo em skills genéricas de design.

## Fonte, baseline e método

- Repositório canônico identificado por seu AGENTS: `praxis-codex-skills`,
  checkout `.worktrees/actions-economy/praxis-codex-skills`, HEAD `4290898`
  mais alterações locais. O `codex-skills/` da raiz do workspace é um
  subconjunto e não contém as skills especializadas auditadas.
- Implementação inspecionada: checkout `praxis-ui-angular-corporate-gate`,
  fontes atuais de Page Builder e Table, README, AGENTS, specs focais e
  `projects/praxis-page-builder/test-dev/research/2026-09-07-connection-editor-ux.md`.
- A auditoria cruzou o histórico de evidências com o código atual. O histórico
  registra estados intermediários que foram substituídos; não foi copiado como
  regra atual. Por exemplo, o corredor superior fixo tornou-se reserva adaptativa,
  e o retorno ao radial de origem tornou-se restauração do catálogo iniciador.
- Baseline das instalações: Praxis 167/167 e Ergon 19/19, sem drift, ausência
  ou fonte inválida. Isso prova igualdade de arquivos, não completude do conteúdo.
- Skills vizinhas foram avaliadas por responsabilidade e cobertura. A revisão
  não é uma certificação semântica de todo o portfólio de 186 skills.

## Inventário de aderência das mudanças

| Mudança / evidência do editor | O que a plataforma já sabia | Classificação | Orientação necessária |
| --- | --- | --- | --- |
| Contraste do catálogo e tooltip sob os radiais | Tokens, tema, seleção e camadas do editor | `ja-suportado-so-ux` | Superfície opaca, ordem de pintura/hit testing, detalhe fora da transformação e ausência de overlays concorrentes |
| Cor de identificação, direção e movimento | Identidade de nó, intent e endpoints | `ja-suportado-mal-nomeado-ou-mal-materializado` | Separar acento de componente, categoria da conexão e seleção; não depender só de cor ou simular execução com animação decorativa |
| Rótulos de change/contextChange | Descritor editorial, PraxisTextValue, registry e payloads do filtro | `ja-suportado-mal-nomeado-ou-mal-materializado` | Resolver o texto no owner; valores e contexto de apresentação são saídas diferentes, sem mudar ids/payloads |
| Nomeação do estado | Descrição em schema/derived, camadas e histórico | `ja-suportado-mal-nomeado-ou-mal-materializado` | Editar descrição existente, preservar endpoint/valor, manter Cancelar/Undo/Redo e Save explícito; não inventar nomes para configurações antigas |
| Percurso de um evento e fan-out | Links, identidade exata do endpoint e regras de entrega em estado | `ja-suportado-mal-nomeado-ou-mal-materializado` | Separar percurso estrutural de execução; respeitar porta, filho aninhado, camada e diagnósticos, sem inferir output a partir de input |
| Distribuição de terminais em hubs | Incidências das conexões e posições dos nós | `suportado-parcialmente`, completado na projeção interna | Alocar âncoras visuais sem duplicar portas, estado ou vínculos canônicos |
| Legendas adaptativas e roteamento | Corpos, conexões e reservas geométricas | `suportado-parcialmente`, completado na projeção interna | Uma geometria compartilhada para DOM, reserva angular, obstáculos e enquadramento; evitar correção somente por CSS |
| Zoom, minimapa e faixa de controles | Viewport, limites do grafo e projeção SVG | `ja-suportado-mal-nomeado-ou-mal-materializado` | Estabilidade durante zoom, fit independente do histórico, compensação de margens SVG e clipping separado dos controles |
| Lista compacta | Nós, relações, catálogo e inspetor existentes | `ja-suportado-so-ux` | Trocar a representação sem criar outra semântica; considerar altura e largura disponíveis, inclusive com painéis abertos |
| Retorno entre catálogo e inspetor | Seleção, invocador e identificadores estáveis | `ja-suportado-mal-nomeado-ou-mal-materializado` | Exclusividade, contexto do destino, Escape em camadas, alvo visível e sequência pointerdown/click |
| Benchmark e browser interrompido | Fonte da geometria, processo do host, registros de validação | Lacuna de procedimento de prova | Não transportar métricas antigas para a revisão atual; separar simulação, browser, entrega real e pesquisa com participantes |

Nenhuma linha representa `lacuna-real-de-contrato`. A investigação não justifica
estender PortContract, criar DSL de grafo, adicionar aliases de negócio ou
alterar uma skill como substituto de implementação ausente.

## Skills atualizadas

| Skill | Lacuna concreta | Atualização |
| --- | --- | --- |
| [praxis-page-builder-composition](../codex-skills/praxis-page-builder-composition/SKILL.md) | Citava graph/layout/trace, sem invariantes suficientes para evitar regressões de geometria e causalidade | Nova [referência do editor](../codex-skills/praxis-page-builder-composition/references/connection-editor-ux.md): fontes, resolução editorial, percurso exato, âncoras por incidência, captions/routing, zoom, minimapa, modo compacto, inspeção e provas |
| [praxis-page-builder-authoring](../codex-skills/praxis-page-builder-authoring/SKILL.md) | A distinção entre inspecionar, iniciar draft e nomear informação persistível não estava explícita | Define ausência de pageChange na navegação e uso das descrições canônicas para nomeação com histórico/Save |
| [praxis-authoring-editors](../codex-skills/praxis-authoring-editors/SKILL.md) | O mapa genérico de editores não encaminhava a jornada específica de conexões | Encaminha para composição/authoring do Page Builder; evita confusão com RuleBuilderState e salvamento desnecessário em prova de inspeção |
| [praxis-ui-product-design](../codex-skills/praxis-ui-product-design/SKILL.md) | Regras gerais não orientavam conjuntamente identidade visual, conexões, legendas e hit testing | Referências de padrões e screenshot QA passam a incluir diagramas, catálogo longo, zoom alto, lista compacta e limites da evidência visual |
| [praxis-angular-accessibility-governance](../codex-skills/praxis-angular-accessibility-governance/SKILL.md) | “Voltar ao invocador” era insuficiente quando o DOM era destruído ou o radial estava recortado | Restaura contexto semântico por id, dispensa uma camada por vez, valida visibilidade real e cobre pointerdown antes de click |
| [praxis-angular-validation-gates](../codex-skills/praxis-angular-validation-gates/SKILL.md) | Faltava protocolo para watcher compartilhado, proxy efetivo e rolagem nativa em canvas | Vincula evidência ao processo/estado renderizado, invalida trecho interrompido e distingue transform, scroll, foco, execução e compreensão humana |
| [praxis-table-filter-actions](../codex-skills/praxis-table-filter-actions/SKILL.md) | Não explicava explicitamente o contexto enriquecido nem o caminho editorial usado pelo editor | Diferencia change/contextChange/requestSearch e aponta descritor, provider e testes de tradução/fallback/override, preservando contratos |

Os detalhes numéricos de resultados anteriores não viraram gates permanentes.
A referência registra o limite atual de texto de 16px como política interna a
conferir no código, não como token público ou requisito universal de design.

## Skills examinadas e preservadas

| Skill | Decisão e motivo |
| --- | --- |
| `praxis-core-component-registry-contracts` | Já descreve ownership vertical, resolveEditorial, descritores localizados, precedência e proibição de mapas locais. A lacuna estava no consumidor e na orientação específica do filtro |
| `praxis-core-i18n-resource-copy` | A fronteira do serviço e da cópia compartilhada continua adequada; não houve API nova de localização |
| `praxis-visual-builder-graph-runtime` | Trata RuleBuilderState, nós de regras e JSON Logic. O diagrama de composition.links não pertence a essa skill; não transplantar invariantes de outro owner |
| `praxis-landing-dynamic-page-studio` | Já delimita a superfície pública de aprendizado e exclui runtime interno do Page Builder. O host 4003 não é o Studio da Landing |
| `praxis-skill-authoring-governance` | Já exige detectar fricção recorrente, escolher a menor skill, validar e auditar instalação. O problema anterior foi a aplicação superficial desse processo, não ausência da regra |

Skills de contratos AI, transporte, backend e persistência não foram alteradas:
o inventário desta tarefa não mostrou mudança dessas responsabilidades. Alterações
preexistentes em `praxis-core-resource-runtime`, `praxis-form-editor-document-roundtrip`
e `praxis-settings-panel-shell` foram preservadas e não são entregas desta auditoria.

## Revisão de seleção e limites

Revisão manual de prompts para cada skill tocada, sem alegar benchmark de
seleção por LLM:

| Skill | Deve orientar | Não deve ser o owner primário |
| --- | --- | --- |
| composição Page Builder | “A legenda faz a linha contornar o nó; revise o roteamento” | “Corrija o grafo de regras do Visual Builder” |
| authoring Page Builder | “Nomeie esta informação da página sem mudar seu caminho” | “Altere o DTO de filtro no backend” |
| authoring genérico | “Qual editor canônico deve abrir para esta configuração?” | “Otimize o algoritmo de caminho sem alterar authoring” |
| design de produto | “Cores e overlays tornam o diagrama difícil de ler” | “Mude a entrega de eventos do runtime” |
| acessibilidade | “Escape me devolve a um controle invisível” | “Escolha uma paleta de marca sem mudança funcional” |
| validação Angular | “Como provar esta correção com o watcher recarregando?” | “Publique uma versão agora” sem autorização de release |
| filtros/ações Table | “Explique os dois outputs do filtro no editor” | “Distribua os terminais dos radiais” |

As descrições existentes já abrangem esses gatilhos; não foram ampliadas para
capturar tarefas vizinhas indiscriminadamente. As dependências do manifesto
permaneceram iguais; referências cruzadas são encaminhamento condicional,
não criação de uma nova família ou dependência artificial de runtime.

## Validação e instalação

1. Atualizados `skillMdSha256` e `treeSha256` pelo auditor canônico. Preservadas
   as entradas e alterações concorrentes do manifesto.
2. Validadas as sete skills pelo `validate-praxis-skills.py` e ambas as famílias
   pelo preflight. `quick_validate.py` foi tentado, mas o Python local não tem
   PyYAML; usado o fallback oficial sem instalar dependência.
3. `preflight-python-fallbacks.py` aprovado: 41 testes das ferramentas,
   compilação Python, estrutura, drafts, instalação temporária e auditoria
   das duas famílias. A primeira tentativa detectou hashes ainda não atualizados;
   após atualização do manifesto, o preflight foi repetido e aprovado.
4. Drafts de revisão conferidos com `--check` e validados: já atualizados,
   pois não houve mudança de inventário/descrição/dependências que os alterasse.
   Nenhuma issue foi enviada ou criada em serviço externo.
5. Ausência de PowerShell confirmada. Considerados sync/bootstrap oficiais;
   usado `sync-praxis-skills.py`, fallback canônico, sem alterar scripts.
6. Antes do sync, cada uma das sete árvores instaladas ainda coincidiu com seu
   baseline limpo. Um manifesto temporário contendo somente essas entradas foi
   derivado do manifesto canônico e usado no dry-run e no sync com `--force`.
   Não houve exclusão de arquivo extra nem sobrescrita de customização local.
7. Auditoria final contra a instalação real, com `--fail-on-drift`: Praxis
   167/167 e Ergon 19/19, zero drift, zero ausências e zero fontes inválidas.
   Diretórios instalados fora dessas famílias não foram removidos.

Nenhum teste Angular foi repetido nesta entrega de skills. Os 145 testes e o
build do editor pertencem à rodada de implementação anterior; não são prova
nova produzida pela edição das instruções. Não houve commit, push ou publicação.

## Fechamento da revisão para integração — 2026-09-08

A revisão de integração foi preparada em checkout isolado do `main` (`4290898`).
Foram incluídas somente as sete skills desta fase e seus hashes; alterações
concorrentes em três outras skills ficaram preservadas no checkout original.
O preflight foi repetido nesse conjunto: 41 testes das ferramentas, estrutura,
drafts e auditorias Praxis 167/167 e Ergon 19/19 em instalação temporária, sem
drift. As sete árvores locais instaladas foram comparadas diretamente com
este conjunto; não foi necessário sincronizá-las novamente.

As duas pendências técnicas abaixo foram encerradas pela evidência final do
host registrada no relatório UX do Page Builder:

- Jornada completa em 390×844: catálogo de destino → vínculo recebido →
  inspetor → Escape → mesmo catálogo/vínculo, incluindo clique no toggle
  da barra com pointerdown e segundo Escape ao controle iniciador.
- Mapa em zoom 1.8: scrollLeft/scrollTop em zero e transform idêntico durante
  inspeção; o catálogo longo manteve sua rolagem nativa independente.

A integração também revisou a preservação das camadas `values`, `derived` e
`transient` no grafo, necessária para que nomes não sejam aplicados à camada
errada. A orientação existente já exige essa identidade; não foi criado
contrato nem alterada a semântica do runtime. As provas anteriores continuam
registros históricos, e não devem ser confundidas com testes deste checkout.

## Pendências que não devem virar falsas garantias nas skills

- Medir compreensão com analistas de negócio. Revisão técnica e simulação por
  agente não fornecem taxa de sucesso ou tempo de tarefa humano.
- Reexecutar comparações de roteamento se for proposta troca de algoritmo.
  O experimento ELK anterior não cobre todas as revisões atuais de captions.
- Não declarar certificação de leitor de tela, forced-colors, execução de
  eventos ou gate agentic com base nas capturas e testes de navegação.

Esses itens ficam como limites de produto e prova, não como contratos novos,
promessas de acessibilidade integral ou recomendações para inventar atalhos.
