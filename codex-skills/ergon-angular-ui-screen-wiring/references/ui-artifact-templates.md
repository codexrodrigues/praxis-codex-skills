# UI Migration Artifact Templates

Create these under `docs/migracao/<SCREEN>/`.

## ui-api-readiness.md

```markdown
# UI API Readiness - <SCREEN>

| Funcionalidade | Recurso/API | Estado | Evidencia | Gap |
|---|---|---|---|---|
| Listagem | `<resource>` `POST /filter` | ready/gap/blocked | `<test/doc/link>` | `<gap>` |
| Schema filtro | `/schemas/filtered` request | ready/gap/blocked | `<evidence>` | `<gap>` |
| Schema tabela | `/schemas/filtered` response | ready/gap/blocked | `<evidence>` | `<gap>` |
| Options/LOV | `<source>` | ready/gap/blocked | `<evidence>` | `<gap>` |
| Detalhe | `GET/findById` | ready/gap/blocked | `<evidence>` | `<gap>` |
| Escrita | commands | ready/gap/blocked/deferred | `<evidence>` | `<gap>` |

## Decisao

`GO/NO-GO/RESTRICTED-GO` para UI.
```

## ui-dto-contract-review.md

```markdown
# UI DTO Contract Review - <SCREEN>

| Campo legado | Classificacao | DTO/FilterDTO | Controle Praxis | Estado | Observacao |
|---|---|---|---|---|---|
| `<field>` | filter/grid/detail/context/action/layout-only | `<field>` | `<control>` | ok/gap/remove | `<notes>` |

## Semantica DTO/Praxis

| Campo DTO | Evidencia semantica | Estado | Label/help/tooltip/icon | Decisao |
|---|---|---|---|---|
| `<field>` | XML/runtime/docs-legado/DDL/fonte/Doc-Sistemas | CONFIRMED_SEMANTIC/TECHNICAL_ONLY/SEMANTIC_UNCONFIRMED | ok/gap | corrigir DTO/schema, aceitar conservador ou retornar investigacao |

## Campos codigo/descricao

| Campo codigo | Campo descricao/display | Estrategia de apresentacao | Owner |
|---|---|---|---|
| `<codigo>` | `<descricao>` | codigo/descricao/campo composto/valuePresentation/lookup | DTO/Praxis/UI layout |

## Campos de contexto nao publicados

| Campo | Origem | Como resolver |
|---|---|---|
| empresa | session/app context | backend session resolver |
```

## ui-translation-map.md

```markdown
# UI Translation Map - <SCREEN>

| XML/bloco legado | Novo componente Praxis | Recurso/API | Observacao |
|---|---|---|---|
| filtro | praxis-table inline filters | `<resource>` | schema-driven |
| grid | praxis-table | `<resource>` | response schema |
| detalhe | praxis dynamic form/read-only panel | `<resource>` | findById/selected row |
| aba detalhe mesmo recurso | tabs + schema groups | `<resource>` | same DTO/detail endpoint |
| aba tabela filha | nested praxis-table | `<child-resource>` | parent id filter, no legacy rowid |
| aba funcionalidade reutilizavel | shared component | `<shared-resource>` | reusable API/component |
| aba sem API pronta | disabled/deferred | `<none>` | document gap |
| acoes | toolbar actions | command APIs | gated |
```

## ui-implementation-plan.md

```markdown
# UI Implementation Plan - <SCREEN>

## Native Praxis Source Audit

| Runtime surface | Evidence inspected | Aderencia | Decision |
|---|---|---|---|
| `@praxisui/core` discovery/actions/surfaces/capabilities | `ResourceDiscoveryService`, adapters, materializer, `GlobalActionService` | ja-suportado-so-ux/ja-suportado-mal-nomeado-ou-mal-materializado/suportado-parcialmente/lacuna-real-de-contrato | use/fix metadata/platform follow-up |
| `@praxisui/crud` | `PraxisCrudComponent`, `CrudLauncherService`, openMode/drawer/refresh behavior | ja-suportado-so-ux/ja-suportado-mal-nomeado-ou-mal-materializado/suportado-parcialmente/lacuna-real-de-contrato | use/fix metadata/platform follow-up |
| `@praxisui/table` | schema filters, row/toolbar actions, `duplicate-draft`, `surface.open`, `queryContext` | ja-suportado-so-ux/ja-suportado-mal-nomeado-ou-mal-materializado/suportado-parcialmente/lacuna-real-de-contrato | use/fix metadata/platform follow-up |
| `@praxisui/dynamic-form` / `@praxisui/dynamic-fields` | schema detail/create/edit forms, option-source controls, selected reload | ja-suportado-so-ux/ja-suportado-mal-nomeado-ou-mal-materializado/suportado-parcialmente/lacuna-real-de-contrato | use/fix metadata/platform follow-up |

## Classificacao Native Praxis First

- Classe: `native-crud` | `native-table-detail` | `native-table-related-surfaces` | `workflow-action` | `manual-temporary-gap`
- Referencia usada: `ERGadm00034` | outro pacote | N/A
- Runtime Praxis nativo inventariado: `PraxisCrudComponent`, `PraxisTable`, `PraxisDynamicForm`, `CrudLauncherService`, action/surface adapters, materializer
- Workaround local: `nenhum` ou `<descricao + owner + gatilho de remocao + platform-issues.md>`

1. Ajustar DTO/FilterDTO/options metadata.
2. Adicionar ou ajustar testes schema/OpenAPI/x-ui.
3. Registrar resource config/route em `ergon-web`.
4. Compor tela com tabela, filtros, detalhe e acoes habilitadas pelo gate, usando runtime Praxis nativo primeiro.
5. Rodar build/testes e QA visual.
```

## ui-execution-gate.md

```markdown
# UI Execution Gate - <SCREEN>

| Gate | Estado | Evidencia |
|---|---|---|
| API reutilizada identificada | pass/fail | `<link>` |
| DTO/FilterDTO revisado para Praxis | pass/fail | `<link>` |
| Schemas request/response executados | pass/fail | `<link>` |
| Native Praxis First classificado | pass/fail | `<native-crud/native-table-detail/native-table-related-surfaces/workflow-action/manual-temporary-gap>` |
| Native Praxis source audit | pass/fail | `<ui-implementation-plan.md#native-praxis-source-audit>` |
| Aderencia de plataforma | pass/fail | `sem lacuna local` ou `<platform-issues.md>` |
| Actions/surfaces/capabilities nativos | pass/fail/n-a | `<evidence>` |
| Option sources e selected reload | pass/fail/n-a | `<evidence>` |
| Checker `check-angular-praxis-reference-pattern.ps1` | pass/fail/n-a | `<comando/output>` |
| Angular implementado | pass/fail | `<link>` |
| Build/testes frontend | pass/fail | `<link>` |
| QA visual desktop/mobile | pass/fail | `<link>` |

## Resultado

`PASS_READ_ONLY/PASS_WITH_DEFERRED_WRITES/PARTIAL_SESSION_REQUIRED_FOR_DATA/RETURN_TO_BACKEND_CONTRACT/RETURN_TO_DTO_SEMANTIC_HARDENING/BLOCKED_LEGACY_RUNTIME/BLOCKED_BACKEND_API`
```
