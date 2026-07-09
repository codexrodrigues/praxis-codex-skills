# Template de Prompt para Fase 1 - Discovery

Use este template somente para executar Fase 1/discovery depois que a Fase 0 estiver fechada.

Ponto de entrada unico para tela nova ou retomada: `docs/migracao/backend-api-only-roadmap.md`. Este template nao cria pacote inicial, `migration-plan.md` nem `phase-0-execution-gate.md`.

```text
Use ergon-archon-screen-discovery para executar a Fase 1/discovery da tela <SCREEN_CODE>.

Pre-condicao obrigatoria:
- docs/migracao/<SCREEN_CODE>/migration-plan.md existe;
- docs/migracao/<SCREEN_CODE>/phase-0-execution-gate.md existe;
- o gate recomenda Fase 1 com ergon-archon-screen-discovery;
- fontes, acessos e riscos iniciais estao registrados.

Leia migration-plan.md e phase-0-execution-gate.md antes de investigar.

Caminho operacional preferido:
- execute `tools/migration-factory/run-phase1-discovery.ps1 -Screen <SCREEN_CODE> -Force` quando o runner existir;
- tente `tools/migration-factory/capture-browser-runtime.ps1 -Screen <SCREEN_CODE>` quando houver sessao/credenciais locais seguras;
- execute `tools/migration-factory/new-phase1-public-key-correlation.ps1 -Screen <SCREEN_CODE> -Force` quando Oracle estiver disponivel ou para registrar blocker padronizado;
- regenere `tools/migration-factory/new-phase1-runtime-parity-workbook.ps1 -Screen <SCREEN_CODE> -Force` depois da captura browser ou da correlacao de chave;
- gere `tools/migration-factory/new-phase1-corporate-baseline-plan.ps1 -Screen <SCREEN_CODE> -Force` para listar fixture, binds, chave publica e escopo/autorizacao pendentes;
- gere `tools/migration-factory/new-phase1-scope-authorization-decision-pack.ps1 -Screen <SCREEN_CODE> -Force` quando houver caso de escopo/autorizacao aberto;
- gere artefatos canonicos com `tools/migration-factory/phase1-canonical-artifacts-draft.ps1 -Screen <SCREEN_CODE> -Force -Canonical`, feche com `tools/migration-factory/phase-closeout-draft.ps1 -Screen <SCREEN_CODE> -Phase 1 -Force -Canonical` e valide com `tools/migration-factory/validate-phase-gate.ps1 -Screen <SCREEN_CODE> -Phase 1`.

Objetivo:
- observar tela/runtime/XML;
- mapear componentes relevantes para API;
- mapear SQL, binds, filtros, chaves, escopo, autorizacao, operacoes e links;
- resolver semantica de binds Cronos por XML + componente reutilizado + Oracle
  antes de bloquear por Chrome/browser, quando a pergunta for valor/escopo e nao
  comportamento visual;
- produzir operation-inventory.md;
- produzir matriz/contrato candidato suficiente para orientar recursos Java/API futuros, sem implementar nem finalizar contrato;
- fechar phase-1-execution-gate.md ou bloquear com lacunas concretas.

Saida esperada:
- investigation.md;
- browser-runtime.md;
- runtime-parity-workbook.md e factory/runtime-parity-workbook.json;
- public-key-correlation.md e factory/public-key-correlation.json;
- public-key-correlation.sql;
- phase1-corporate-baseline.md e factory/phase1-corporate-baseline.json;
- phase1-scope-authorization-decision-pack.md e factory/phase1-scope-authorization-decision-pack.json quando houver escopo/autorizacao aberto;
- runtime-capture-form.md quando o browser/workflow nao for completamente operado por Codex;
- cronos-source-of-truth.md quando houver XML runtime/local/HADES ou residual de XML;
- component-lineage-matrix.md como inventario componente -> API;
- closure-checklist.md;
- operation-inventory.md;
- read-parity-matrix.md;
- api-contract.md com contrato candidato/matriz suficiente para a proxima fase;
- oracle-confirmation.sql, hades-registry.sql e oracle-results quando Oracle estiver disponivel;
- write-risk.md e write-api-handoff.md quando houver acoes de escrita bloqueadas ou deferidas;
- phase-1-execution-gate.md.

Regras de fechamento:
- se `tools/migration-factory/run-phase1-discovery.ps1` existir, use esse runner antes da sequencia manual; ele deve extrair XML, gerar candidatos de API, workbook runtime, SQL Oracle/HADES e correlacao de chave publica quando possivel;
- se o runner agregado nao existir ou falhar, use a sequencia manual dos helpers antes de escrever SQL manual: extrair XML para `factory/extraction.json`, gerar `oracle-confirmation.sql`/`hades-registry.sql`, executar ambos, gerar `public-key-correlation.sql` e anexar outputs;
- use SQL manual apenas como suplemento quando o SQL padrao nao cobrir uma pergunta concreta, registrando o motivo no gate;
- para binds Cronos de empresa/sessao/constante/controle reutilizado, aplique
  `docs/migracao/phase1-cronos-bind-resolution-standard.md` quando existir:
  confirme `sqlParameters`, SQL onde o bind entra, componente ou tela equivalente
  e metadado Oracle da fonte; se isso fechar a semantica, registre
  `BIND_SEMANTICS_CLOSED_BY_XML_ORACLE` e nao bloqueie apenas por Chrome/browser
  indisponivel;
- nao marque Fase 1 como Ready se faltar `investigation.md`, `browser-runtime.md`, `runtime-parity-workbook.md`, `factory/runtime-parity-workbook.json`, `public-key-correlation.md`, `factory/public-key-correlation.json`, `component-lineage-matrix.md`, `cronos-source-of-truth.md`, `closure-checklist.md`, `operation-inventory.md`, `read-parity-matrix.md`, `api-contract.md`, `oracle-confirmation.sql`, `hades-registry.sql` ou outputs executados de Oracle/HADES em `oracle-results/`;
- se Oracle/HADES tiver apenas nota bloqueada, feche Fase 1 como `Blocked`;
- se `public-key-correlation` ficar em `blocked_*`, feche Fase 1 como `Blocked` com a causa e a menor acao de retomada;
- se o workbook estiver ausente, stale ou com placeholders de baseline legado para binds, filtros, chave publica, escopo ou autorizacao, feche Fase 1 como `Blocked`;
- aplique `docs/migracao/phase1-scope-authorization-standard.md`: `allowed-default-context` pode fechar com browser autenticado, fixture nao vazia, chave publica e contexto Oracle na mesma conexao; para telas API-only governadas por `ergon-hades-security-starter` e `ergon-legacy-bridge`, `company-scoped-context` e `restricted-user-context` fecham por contrato da ponte e nao bloqueiam por tela;
- reabra company/restricted como blocker apenas quando houver bypass do guard/executor da ponte, exposicao publica de empresa/usuario/perfil/seguranca, ou seguranca custom fora de HADES; nesses casos, use o decision pack como pedido estruturado ao dono de seguranca/dados, sem valores reais de empresa, usuario, perfil, sessao, cookie, token, senha ou connection string;
- nao exponha empresa, usuario, perfil, permissao ou binds de sessao como `FilterDTO`, schema, URL, option payload ou `x-ui`;
- para `Ready`, registre marcadores estruturados: `Read surface: Closed`, `Oracle confirmation: Executed`, `HADES coverage: Executed`, `API contract artifact: Candidate artifact generated; not Phase 2-ready` e `Write state: Blocked|Deferred|Not present`;
- use a evidencia Oracle/HADES para preencher recursos REST candidatos, DTO/FilterDTO/options, chaves, filtros, escopo/autorizacao, session context, related resources e operacoes bloqueadas/deferidas;
- nao avance para Fase 1.5 se `cronos-source-of-truth.md` estiver ausente quando XML runtime/local/HADES for relevante;
- nao avance se HADES registry/access/stored resources estiverem sem SQL/helper de retomada;
- nao use `Unknown` como estado de operacao em operation-inventory.md; use `Blocked`, `Deferred` ou `Not present` com proxima acao concreta;
- preserve UTF-8 e acentos em labels PT-BR.

Nao implemente API e nao finalize contrato de leitura/escrita nesta fase. Contrato candidato ou matriz de API preliminar e esperado quando houver evidencia suficiente.
```

Nao cole senhas no prompt quando ele puder ser salvo em tickets, documentos, commits ou historico compartilhado. Use credenciais apenas na sessao privada ativa ou por variaveis de ambiente.
