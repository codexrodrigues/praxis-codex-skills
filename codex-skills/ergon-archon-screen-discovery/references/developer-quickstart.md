# Guia Rapido para Desenvolvedores

Use este guia somente depois que a Fase 0 tiver fechado `phase-0-execution-gate.md` recomendando `ergon-archon-screen-discovery`.

Ponto de entrada unico para tela nova ou retomada: `docs/migracao/backend-api-only-roadmap.md`. Nao use este guia para iniciar migracao do zero.

## Pre-condicoes

- `docs/migracao/<SCREEN>/migration-plan.md` existe.
- `docs/migracao/<SCREEN>/phase-0-execution-gate.md` existe.
- O gate de Fase 0 recomenda Fase 1 com `ergon-archon-screen-discovery`.
- Repositorios, Oracle/banco, XML/debug, app legado/browser e riscos iniciais foram registrados na Fase 0.

Se qualquer item acima faltar, volte para `ergon-migration-orchestration` usando o prompt canonico em `docs/migracao/backend-api-only-roadmap.md`.

## Caminho Padrao

Para execucao operacional ou simulacao por desenvolvedor, comece pelo runner
agregado da factory quando ele existir:

```powershell
.\tools\migration-factory\run-phase1-discovery.ps1 -Screen <SCREEN> -Force
```

Se a Fase 1 ficar bloqueada por fixture, binds runtime/debug, chave publica ou
escopo/autorizacao, nao retome interpretando o workbook manualmente. Use o
runner de baseline:

```powershell
.\tools\migration-factory\run-phase1-runtime-baseline.ps1 -Screen <SCREEN> -Force
```

Ele valida Fase 0, tenta captura browser, regenera chave publica, workbook,
`phase1-corporate-baseline.md`, decision pack de escopo/autorizacao, artefatos
canonicos, gate e validacao.

Depois complete a captura runtime/browser, correlacione a chave publica,
regenere o workbook e feche artefatos canonicos:

```powershell
.\tools\migration-factory\capture-browser-runtime.ps1 -Screen <SCREEN>
.\tools\migration-factory\new-phase1-public-key-correlation.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-runtime-parity-workbook.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-corporate-baseline-plan.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-scope-authorization-decision-pack.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\phase1-canonical-artifacts-draft.ps1 -Screen <SCREEN> -Force -Canonical
.\tools\migration-factory\phase-closeout-draft.ps1 -Screen <SCREEN> -Phase 1 -Force -Canonical
.\tools\migration-factory\validate-phase-gate.ps1 -Screen <SCREEN> -Phase 1
```

Se Oracle ou browser estiverem indisponiveis, registre a causa como blocker
padronizado e mantenha a Fase 1 `Blocked`. A sequencia manual abaixo existe
para diagnostico ou para ambientes onde o runner agregado nao esteja disponivel.

## Como Executar Discovery

1. Abra a tela legada no navegador integrado quando possivel.
2. Faca login manualmente se a sessao exigir autenticacao humana.
3. Use o proximo prompt recomendado no `phase-0-execution-gate.md`.
4. Produza os artefatos de Fase 1: `investigation.md`, `browser-runtime.md`, `runtime-parity-workbook.md`, `public-key-correlation.md`, `component-lineage-matrix.md`, `cronos-source-of-truth.md`, `closure-checklist.md`, `operation-inventory.md`, `read-parity-matrix.md` e `phase-1-execution-gate.md`.
5. Quando Codex nao conseguir operar totalmente o browser, crie tambem `runtime-capture-form.md` para orientar a captura manual de grid, filtros, selecao, botoes, mensagens e debug/runtime SQL.
6. Quando houver credenciais locais seguras, tente a captura automatizada com `tools/migration-factory/capture-browser-runtime.ps1 -Screen <SCREEN>` antes de pedir observacao manual. O helper usa Node/Playwright, grava evidencia estruturada em `browser-evidence/` com URL/titulo, rodape de contagem/paginacao, colunas, `controlSnapshot` sanitizado de inputs/selects/hidden locators, `filterProbeResults` para probes read-only de filtros publicos, controles de filtro, acoes candidatas e linha candidata quando o DOM permite, e atualiza `runtime-parity-workbook.md`/`factory/runtime-parity-workbook.json` automaticamente, salvo com `-SkipWorkbookRefresh`. Se nao conseguir atualizar o workbook apos captura bem-sucedida, trate a falha como blocker operacional para evitar evidencia stale. Fallback `text-only` para filtros/acoes e candidato, nao prova final de acao habilitada ou regra de API. `captured_empty_fixture` significa tela carregada com grade principal vazia; continue bloqueado ate encontrar fixture representativa ou aceitar formalmente o vazio.
7. Use `tools/migration-factory/new-phase1-runtime-parity-workbook.ps1 -Screen <SCREEN> -Force` depois de gerar `factory/filter-payload-candidates.json` apenas quando precisar regenerar manualmente o workbook ou quando a captura browser tiver sido executada com `-SkipWorkbookRefresh`. O workbook padroniza os casos de baseline legado: bind runtime, payloads de filtro/options, chave publica e escopo/autorizacao corporativa. Quando houver `controlSnapshot`, ele preenche defaults de binds cujo nome/id coincida com `sqlParameters`; quando houver `filterProbeResults` com sucesso, ele preenche `captureChangedValue` para os binds do controle testado. Options search e chave publica estavel continuam exigindo evidencia executada ou blocker explicito. Escopo/autorizacao segue `docs/migracao/phase1-scope-authorization-standard.md`: `allowed-default-context` pode fechar com browser autenticado, fixture nao vazia, chave publica e contexto Oracle na mesma conexao. Para telas API-only governadas por `ergon-hades-security-starter` e `ergon-legacy-bridge`, `company-scoped-context` e `restricted-user-context` fecham por contrato da ponte e nao bloqueiam por tela; reabra como blocker apenas quando houver bypass do guard/executor da ponte, exposicao publica de contexto ou seguranca custom fora de HADES. Ele tambem carrega sementes futuras de paridade API, mas endpoint Java nao e exigido na Fase 1. Enquanto houver placeholders de baseline legado ou `allowed-default-context` aberto, a Fase 1 continua `Blocked`.
8. Quando houver Oracle, gere primeiro o SQL padronizado com `tools/migration-factory/new-phase1-oracle-sql.ps1` a partir de `factory/extraction.json`; depois execute `oracle-confirmation.sql` e `hades-registry.sql`. Em seguida rode `tools/migration-factory/new-phase1-public-key-correlation.ps1` para gerar `public-key-correlation.sql`, `public-key-correlation.md` e `factory/public-key-correlation.json`; regenere o workbook para consumir o status da correlacao. Se Oracle falhar, salvar um artefato bloqueado em `oracle-results/` e manter a Fase 1 `Blocked`.
9. Para entrega/simulacao operacional, gere artefatos e gate canonicos com `tools/migration-factory/phase1-canonical-artifacts-draft.ps1 -Screen <SCREEN> -Force -Canonical`, `tools/migration-factory/phase-closeout-draft.ps1 -Screen <SCREEN> -Phase 1 -Force -Canonical` e `tools/migration-factory/validate-phase-gate.ps1 -Screen <SCREEN> -Phase 1`; use `.prelim.md` apenas para diagnostico intermediario.

Nao crie pacote de tela por script nesta fase. O pacote inicial, `migration-plan.md` e `phase-0-execution-gate.md` pertencem ao prompt canonico da Fase 0.

## Responsabilidades

O desenvolvedor deve:

- informar ou confirmar a tela alvo registrada na Fase 0;
- fazer login no navegador integrado quando necessario;
- manter as variaveis Oracle disponiveis em `secrets/ergon.env.ps1`;
- responder perguntas objetivas quando o Codex nao conseguir observar algum detalhe visual/debug;
- revisar `closure-checklist.md` antes de avancar para contrato de API.

O Codex deve executar consultas read-only quando houver acesso ao Oracle e salvar os resultados no pacote da tela.

## Sequencia Oracle/HADES Padrao

Nao escreva consultas Oracle da Fase 1 do zero quando os helpers da factory
estiverem disponiveis. Use:

```powershell
.\tools\migration-factory\extract-xml.ps1 -Screen <SCREEN> -XmlPath docs\migracao\<SCREEN>\runtime\<SCREEN>.authenticated.xml -Force
.\tools\migration-factory\new-phase1-api-candidates.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-runtime-parity-workbook.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-oracle-sql.ps1 -Screen <SCREEN> -Force
. .\secrets\ergon.env.ps1
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query_jdbc.ps1 `
  -SqlFile docs\migracao\<SCREEN>\oracle-confirmation.sql `
  -OutputPath docs\migracao\<SCREEN>\oracle-results\oracle-confirmation.out.txt `
  -MaxRows 500
D:\CodexHome\skills\ergon-archon-screen-discovery\scripts\run_oracle_query_jdbc.ps1 `
  -SqlFile docs\migracao\<SCREEN>\hades-registry.sql `
  -OutputPath docs\migracao\<SCREEN>\oracle-results\hades-registry.out.txt `
  -MaxRows 500
.\tools\migration-factory\new-phase1-public-key-correlation.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-runtime-parity-workbook.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-corporate-baseline-plan.ps1 -Screen <SCREEN> -Force
.\tools\migration-factory\new-phase1-scope-authorization-decision-pack.ps1 -Screen <SCREEN> -Force
```

Use SQL manual apenas como suplemento quando o padrao nao cobrir uma pergunta
concreta. Registre no gate qual consulta padrao foi insuficiente e por que o
suplemento foi necessario.

O objetivo desses SQLs e alimentar APIs Java futuras. Ao revisar os outputs,
promova para os artefatos canonicos somente achados que ajudem a definir:
recurso REST candidato, DTO, FilterDTO, options, chave publica, filtros,
ordenacao/paginacao, autorizacao, contexto de sessao Oracle, related resources,
operacoes bloqueadas/deferidas e riscos de escrita.

Para chave publica, use `public-key-correlation.md/json` como artefato padrao.
Ele deve mostrar a view de leitura, a linha selecionada no browser, campos
publicos candidatos, output Oracle e decisao `candidate_*` ou `blocked_*`.
`ROWID`, `ROWID_REG`, `P_ROWID_REG` e equivalentes ficam internos por padrao e
nao devem aparecer como id publico em DTO, FilterDTO, schema OpenAPI, option
payload ou URL.

## Criterios Minimos De Handoff Da Fase 1

- `cronos-source-of-truth.md` existe quando ha XML runtime/local/HADES ou residual de XML.
- `investigation.md`, `browser-runtime.md`, `runtime-parity-workbook.md`, `public-key-correlation.md`, `component-lineage-matrix.md`, `closure-checklist.md`, `operation-inventory.md`, `read-parity-matrix.md` e `api-contract.md` existem antes de qualquer gate `Ready`.
- `hades-registry.sql` existe quando o gate mencionar HADES como blocker ou quando a Fase 1 estiver sendo fechada como `Ready`.
- `oracle-results/` contem outputs executados de Oracle e HADES para gate `Ready`; nota bloqueada explicita exige gate `Blocked`.
- `oracle-confirmation.sql` e `hades-registry.sql` foram gerados pelo helper padrao quando `factory/extraction.json` existia, ou o gate explica por que foi necessario usar SQL manual/suplementar.
- `runtime-capture-form.md` existe quando `browser-runtime.md` disser que o workflow nao foi operado.
- Captura browser automatizada ou manual registra default load, filtros, fixture representativa, selecao/chave publica, estado de acoes e lacunas. A captura estruturada do helper pode preencher row count, colunas, filtros, defaults de binds via `controlSnapshot`, valores alterados de filtros publicos via `filterProbeResults` e acoes nos artefatos canonicos, mas nao fecha por si so options search, chave publica, escopo/autorizacao nem as sementes futuras de paridade. XML/factory sozinho nao substitui esses fatos para API.
- `runtime-parity-workbook.md` e `factory/runtime-parity-workbook.json` registram os casos padronizados que devem ser executados ou bloqueados na Fase 1: binds reais, payloads de filtro/options, chave publica e escopo/autorizacao. A comparacao legado x API fica como semente para fases futuras.
- `phase1-corporate-baseline.md` e `factory/phase1-corporate-baseline.json` existem quando a factory estiver disponivel e listam os casos restantes. Em telas API-only cobertas pela ponte, `company-scoped-context` e `restricted-user-context` devem aparecer como `closed_by_bridge_security_contract`; o blocker por tela permanece em `allowed-default-context` quando faltar baseline permitido.
- `phase1-scope-authorization-decision-pack.md` e `factory/phase1-scope-authorization-decision-pack.json` existem quando escopo/autorizacao estiver aberto, sem valores reais de empresa/usuario/perfil/sessao e com templates de decisao para dono de seguranca/dados.
- `public-key-correlation.md` e `factory/public-key-correlation.json` registram a correlacao da linha selecionada com Oracle read-only, ou um blocker explicito quando o Oracle/contexto/amostra nao confirma a chave. Um status `blocked_*` impede handoff `Ready`.
- `phase-1-execution-gate.md` existe e valida. Um pacote apenas com `phase-1-execution-gate.prelim.md` nao esta pronto para outro desenvolvedor continuar.
- `operation-inventory.md` usa estados deterministas: `Implemented`, `Ready`, `Candidate`, `Blocked`, `Deferred` ou `Not present`; nao use `Unknown`.
- A Fase 1 pode entregar contrato candidato/matriz de API, mas nao implementa nem finaliza contrato Java; isso pertence as fases seguintes.
- Um gate `Ready` deve conter, no gate ou nos artefatos canonicos, os marcadores: `Read surface: Closed`, `Oracle confirmation: Executed`, `HADES coverage: Executed`, `API contract artifact: Candidate artifact generated; not Phase 2-ready` e `Write state: Blocked|Deferred|Not present`.
- Os Markdown estao em UTF-8 legivel e preservam acentos de labels PT-BR.
