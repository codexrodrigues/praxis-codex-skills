# Exemplos de Prompts para Fase 1 - Discovery

Estes exemplos sao apenas para Fase 1/discovery, depois que a Fase 0 estiver fechada.

Ponto de entrada unico para iniciar tela nova ou retomar migracao: `docs/migracao/backend-api-only-roadmap.md`.

## Pre-condicao Obrigatoria

Antes de usar qualquer prompt deste arquivo:

- `docs/migracao/<SCREEN>/migration-plan.md` existe;
- `docs/migracao/<SCREEN>/phase-0-execution-gate.md` existe;
- o gate de Fase 0 recomenda `ergon-archon-screen-discovery`;
- fontes, acessos e riscos iniciais foram registrados.

Se faltar qualquer item, volte para `ergon-migration-orchestration` e use o prompt canonico em `backend-api-only-roadmap.md`.

## Quick Discovery

Use quando a Fase 0 ja recomendou discovery e o objetivo e entender rapidamente a tela, seus componentes e principais objetos, sem fechar contrato Java ainda.

```text
Com a Fase 0 fechada e recomendando discovery, execute Quick Discovery da tela <SCREEN> com ergon-archon-screen-discovery.

Pre-condicao: phase-0-execution-gate.md recomenda Fase 1/discovery.

Leia migration-plan.md e phase-0-execution-gate.md.

Tarefas:
1. Observar a tela no navegador quando houver sessao disponivel.
2. Localizar XML/debug local ou runtime.
3. Identificar grids, filtros, combos, abas, links, botoes e acoes visiveis.
4. Extrair sqlSelect, sqlParameters, binds e objetos Oracle iniciais.
5. Criar ou atualizar browser-runtime.md, runtime-capture-form.md quando necessario, cronos-source-of-truth.md quando XML/source-of-truth estiver no escopo, component-lineage-matrix.md, investigation.md e operation-inventory.md.
6. Marcar lacunas como Missing, Partial, Blocked ou Deferred com proxima acao concreta; nao usar Unknown como estado de operacao.

Nao desenhe API e nao implemente codigo.
```

## Full Discovery

Use quando a Fase 0 ja recomendou discovery e a tela precisa ficar bem entendida antes de qualquer contrato ou implementacao.

```text
Com a Fase 0 fechada e recomendando discovery, execute Full Discovery da tela <SCREEN> com ergon-archon-screen-discovery.

Pre-condicao: phase-0-execution-gate.md recomenda Fase 1/discovery.

Leia migration-plan.md e phase-0-execution-gate.md.

Tarefas:
1. Observar workflow no navegador e registrar parametros, filtros, abas, links e acoes.
2. Confirmar XML/debug da tela e extrair SQL/binds/componentes.
3. Consultar HADES para registro da tela, transacao, permissoes e XML/recursos armazenados.
4. Gerar e executar oracle-confirmation.sql quando houver acesso Oracle.
5. Produzir cronos-source-of-truth.md e runtime-capture-form.md quando XML/source-of-truth ou browser parcial estiverem no escopo.
6. Resolver sinonimos, views, tabelas fisicas, constraints, grants, triggers e packages.
7. Criar component-lineage-matrix.md, closure-checklist.md, investigation.md, read-parity-matrix.md e operation-inventory.md.
8. Se houver acoes de escrita, criar write-risk.md e write-api-handoff.md.
9. Fechar phase-1-execution-gate.md ou bloquear com lacunas concretas.

Nao implemente codigo.
```

## Revisao de Handoff Da Fase 1

Use quando a investigacao ja existe e precisa saber se pode seguir para Fase 1.5 ou voltar para discovery.

```text
Use ergon-archon-screen-discovery para revisar o handoff da Fase 1 da tela <SCREEN>.

Leia docs/migracao/<SCREEN>.

Verifique:
1. investigation.md;
2. browser-runtime.md;
3. runtime-capture-form.md quando o browser estiver parcial;
4. cronos-source-of-truth.md quando houver XML/runtime/local/HADES;
5. component-lineage-matrix.md;
6. closure-checklist.md;
7. operation-inventory.md;
8. read-parity-matrix.md;
9. oracle-results e HADES registry quando houver;
10. write-risk.md e write-api-handoff.md quando houver escrita.

Nao implemente codigo. Diga se a Fase 1 esta Ready for next phase, Ready with adjustments, Blocked ou Deferred.

Antes de classificar como pronta, verifique explicitamente:
- cronos-source-of-truth.md existe quando ha XML runtime/local/HADES;
- HADES registry/access/stored resources foram executados ou ha SQL/helper de retomada;
- runtime-capture-form.md existe se o workflow browser estiver parcial;
- operation-inventory.md nao usa Unknown como estado de operacao;
- os Markdown preservam UTF-8 legivel em labels PT-BR.
```
