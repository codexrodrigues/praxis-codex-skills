# AGENTS.md — Praxis Platform Monorepo

## 1. Escopo, Regra Anti-Inchaço e Herança
- **Escopo:** aplica-se à raiz `<WORKSPACE_ROOT>` e subpastas, complementado pelo `AGENTS.md` local de cada subprojeto (que adiciona regras locais sem anular as invariantes globais).
- **Orçamento de Contexto (Teto Rígido):** manter este arquivo **abaixo de 16 KB** (bem abaixo do limite de truncamento de `<user_rules>`). Checklists extensos, `PLAT-EVO-*` e detalhes de domínio pertencem aos guias canônicos, skills ou `AGENTS.md` locais — nunca em parágrafos longos aqui.
- **Checkout Parcial:** nem todos os repositórios irmãos ou `scripts/workspace/` precisam estar clonados localmente. Antes de assumir presença em disco, verifique; quando ausente, consulte `codexrodrigues/<repo>` via `gh` (leitura) ou registre explicitamente o gate/auditoria pendente.

## 2. Posicionamento e Solução de Plataforma
- A **Praxis Platform** é uma plataforma semanticamente orientada para aplicações corporativas **AI-native**: recursos, regras, ações, dados e políticas são descritos uma vez e operados por UI tradicional, UI generativa, agentes de IA e integrações dentro de limites determinísticos e *fail-closed*.
- **Regra de Ouro (Solução Correta de Plataforma):** priorizar sempre a solução canônica (`praxis-metadata-starter`, `praxis-config-starter`, `praxis-rules-engine`, `praxis-authz-*`, `praxis-ui-angular` ou regras estruturais) em vez de remendos locais, aliases ad hoc ou adaptações só de frontend. Contingências temporárias exigem explicitar por que não são a solução correta e qual débito introduzem.
- **Disciplina de Beta e Limpeza:** enquanto a plataforma e suas libs estiverem em beta, corrigir a fonte canônica e atualizar consumidores/exemplos/docs no mesmo ciclo; evitar `feature flags`, rotas `v1`/`v2` ou contratos paralelos preventivos sem necessidade operacional explícita e plano de remoção.

## 3. Router de Contexto (Carregamento Sob Demanda)
Antes de editar, identifique a frente e carregue os contratos/guias aplicáveis (no checkout local ou via `gh` em `codexrodrigues/<repo>`):

| Frente / Tarefa | O que ler antes de editar | Gate / Auditor Aplicável |
|---|---|---|
| **Recurso Java / DTO / Filtros / Bulk / Rules** | `praxis-metadata-starter/AGENTS.md`, `praxis-metadata-starter/src/main/resources/META-INF/praxis/AI-RESOURCE-BLUEPRINT.md`, `praxis-metadata-starter/docs/guides/QUICK-VIEW-360-E-CURADORIA-EXECUTIVA.md`, `API-PATHS-E-OPTION-SOURCES.md`, `DUPLICATE-DRAFT-ADOPTION.md` | `audit-java-resource-completeness.py <host> --strict` + `SemanticMetadataReviewer` + `PraxisExpressionStaticValidator` |
| **Libs `@praxisui/*` / Design System** | `praxis-ui-angular/AGENTS.md` + `AGENTS.md` da lib em `projects/*` + skill `praxis-ui-product-design` | `npm run audit:purity` + build/spec focal + E2E afetado |
| **Host Angular / Showcase UI** | `AGENTS.md` do host + `praxis-ui-angular/docs/AI-ANGULAR-HOST-BLUEPRINT.md` + `praxis-ui-product-design` | `audit-angular-host-completeness.py <host> --strict` + QA visual no `browser` |
| **Config / AI Registry / Rules Studio** | `praxis-config-starter/AGENTS.md` + `praxis-policy-studio/AGENTS.md` | Testes focais do starter + `ConfigOriginRestrictionFilter` |
| **Decisões & Autorização (`BUSINESS` vs `AUTHORIZATION`)** | `praxis-rules-engine` + `praxis-authz-starter/AGENTS.md` + `praxis-codex-skills/docs/platform-governance/` | `RuleCatalogExhaustivenessContractTest` / gates de enforcement |
| **Banco e Branches Neon** | `codexrodrigues/praxis-codex-skills` (`docs/platform-governance/ciclo-de-vida-neon.md`) | Nunca mutar branch base; descartáveis com TTL ≤ 24h e remoção após prova |
| **Release / Tag / Publicação** | `RELEASING.md` e `ACTIONS-RELEASE-POLICY.md` do repositório alvo | Workflow oficial (`workflow_dispatch`); nunca publicar localmente |

## 4. Modo de Execução no Antigravity
- **Pesquisa pesada (`docs-legado`, busca multi-repo, impacto):** delegar ao subagente `research` (ou consultar via `gh` em leitura quando o repo irmão não estiver clonado) para preservar o contexto principal.
- **Mudanças `transversal`, `arquitetural` ou `contrato-publico`:** parar antes de editar e registrar **Plano + Mapa de Impacto** em Artifact da conversa. Em entregas em fases (Fases 1–3), salvar checkpoints por fase.
- **Frentes paralelas (ex.: backend + frontend):** usar `swarm` (com `workspace: "share"` para escritores concorrentes) seguindo `codexrodrigues/praxis-codex-skills` (`docs/platform-governance/agentes-e-modelos.md`).
- **Gate Visual de UI (obrigatório em toda mudança visual, de KPI, filtro ou drawer):** delegar ao subagente `browser` para validar renderização real, viewports desktop/narrow, dark mode (quando aplicável) e ausência de erros de console/HTTP inesperados.
- **Gate de Revisão Independente:** entregas de recurso completo ou contrato público devem passar por revisão focada nos auditores estáticos e Scorecard de completude, nunca aprovadas apenas porque `mvn test` ou smoke test passou.

## 5. Hierarquia Canônica e Fronteiras de Arquitetura
- **`praxis-metadata-starter`:** fonte canônica metadata-driven (`x-ui`, `/schemas/filtered`, `/schemas/catalog`, `/schemas/surfaces`, `/schemas/actions`, `/capabilities`, `_links`, anotações públicas). Baseline obrigatório para recursos novos: `AbstractResourceController` / `AbstractReadOnlyResourceController`, `AbstractBaseResourceService` / `AbstractReadOnlyResourceService`, `ResourceMapper`, `BaseResourceRepository` e `@ApiResource(resourceKey=...)` (não reintroduzir `AbstractCrudController` / `BaseCrudService`). Duplicação assistida não-persistente usa `AbstractDuplicateDraftResourceController` + `DuplicateDraftResourceService` (ver `DUPLICATE-DRAFT-ADOPTION.md`).
- **`praxis-config-starter`:** fronteira canônica paralela de persistência e config (`ui_user_config`, `ai_registry`, `api_metadata`, templates, ETag) em `/api/praxis/config/**`.
- **`praxis-ui-angular`:** runtime oficial e superfície pública de `@praxisui/*`. Bibliotecas em `projects/` são universais e agnósticas a hosts.
- **Workstations e Derivados:** `praxis-policy-studio` (workstation 4-olhos), `praxis-api-quickstart` (host operacional), `praxis-ui-landing-page` (exemplos/docs públicas) e `praxisui-http-examples` (corpus HTTP derivado) não devem redefinir contratos canônicos nem institucionalizar desvios.

### Praxis Decision Platform (`BUSINESS` vs. `AUTHORIZATION`)
- **Control Plane e Proibição de `Policy` sem qualificador:** `DomainRuleDefinition` e `DomainRuleMaterialization` (`praxis-config-starter`) formam o Control Plane único, com `DecisionPoint` (`decisionKind = BUSINESS | AUTHORIZATION`, `resultModel = VALUE | GATE`). Nunca nomear módulos, pacotes, controllers ou classes públicas apenas como `Policy*` / `praxis-policy-*` genérico.
- **Trilha 1 — Regras de Negócio (`decisionKind = BUSINESS` → `praxis-rules-engine`):** `RuleSetDefinition`, `DecisionSlot` (5 estágios de `DecisionStage`, proibido `BYPASS_ALL` global), `DecisionBinding` e JSON Logic determinístico sem I/O (`422`/`409`). Superfícies de autoria/sandbox nos hosts usam nomenclatura `RulesStudio*` (`/api/praxis/rules-studio/**`) e convergem em 2 níveis: inspetor contextual in-app (`@praxisui/*`) + handoff para `praxis-policy-studio`.
- **Trilha 2 — Autorização e Privacidade (`decisionKind = AUTHORIZATION` → `praxis-authz-*` / `OPA`):** `AuthorizationPolicy*` / `AccessPolicy*` / `DataScope*` cobrindo `ACCESS`, `DATA_SCOPE` (RLS), `FIELD_USE`, `FIELD_WRITE` e `MASK` (LGPD/LAI). Proibido implementar validador ou compilador de `authorization_policy` dentro de `praxis-metadata-starter` (`BND-OWN-003`).
- **Convivência `@DomainGovernance` + `@DomainLineage`:** `@DomainLineage` enriquece proveniência e bloqueia enfraquecimento, mas não substitui `@DomainGovernance` explícito nos DTOs corporativos.

## 6. Fronteira de Pureza Pública e Desacoplamento de Domínio
- **Isolamento Público vs. Privado:** referências ao legado de cliente (`Ergon`, `ErgonX`, `HADES`, `PACK_HADES`, `Archon`, `Techne`, `ERG*`, `C_ERGON`, `PCK_*`) e consulta a `docs-legado` são **estritamente exclusivas dos repositórios privados de showcase/migração** (`praxis-ergon-showcase`, `praxis-ergon-showcase-ui`) e jamais podem vazar para os repositórios públicos da plataforma.
- **Tradução Semântica Obrigatória ao Promover Evoluções (`PLAT-EVO`):**
  - `ergon.*` → `workforce.*`, `human-resources.*` ou `payroll.*`
  - Códigos de regra legados (`ERG-*`) → `WF-00001` / `FIN-TETO-*`
  - Packages legados (`pack_hades.*` / `PCK_*`) → `pkg_legacy_rules.*`
  - Showcase privado → `praxis-api-quickstart` ou `praxis-workforce-showcase`
- **Proibição Absoluta em Repositórios Públicos:** nunca versionar caminhos locais de máquina (home de usuário macOS/Windows, pastas locais de workspace, `/mnt/<drive>` ou `file:///[A-Za-z]:`), URLs de feeds privados, o nome legado do Policy Studio ou IDs/branches/endpoints reais de projetos Neon em `.md`, `pom.xml`, `logback*.xml`, scripts ou `docs/**/evidence/`.
- **Auditoria Obrigatória:** antes de commit/push em repo público, executar `audit-public-repo-purity.py --repo <repo>` (e `--sanitize-evidence <caminho>` ao salvar evidências).

## 7. Invariantes de Contrato, Profundidade e UX
- **Anti-Minimalismo (20 Pilares em 3 Fases):** recursos corporativos não podem ser entregues com DTOs/filtros esqueléticos. Decompor construções amplas em **3 Fases verticais de profundidade 100%** (Fase 1: 100% Entity-to-DTO + `@UISchema` editorial + `@MicroVisualization` + Quick View 360° + Lookups ricos + Matriz `@Filterable`/Omnibox + `@QuickFilter` tipado; Fase 2: `@UiSurface` + `@ResourceIntent` + `@WorkflowAction` com `If-Match`/`Idempotency-Key` + `duplicate-draft` não-persistente + Bulking nos 3 modos + `@ResourceFact` + `StatsFieldRegistry`/`@UiAnalytics` + `CollectionExport`; Fase 3: invariantes transacionais, `@ReactiveDetermination`, grafo ontológico `PraxisFactTreeBuilder` nas 5 raízes + gates JUnit nativos).
- **ApiPaths & Option Sources:** centralizar caminhos reutilizados em `final ApiPaths` no host (construtor privado, `public static final String` constante de compilação; proibida interface de constantes, chamadas de método em annotations, concatenação em DTOs ou reconstrução no frontend) e preservar fixtures literais independentes de teste. Registrar `OptionSourceDescriptor` completo (proibido `RESOURCE_ENTITY` com subcontratos `null`).
- **Documentação Manual de DTOs e OpenAPI:** proibido introduzir scripts de preenchimento em lote de `@Schema` a partir de nomes/rótulos. Todo campo novo/alterado deve receber semântica real de negócio propriedade a propriedade.
- **Guardrails de `public-api` (`@praxisui/*`):** nenhuma lib pública pode reexportar no barrel raiz tipos cujo dono canônico seja outra lib pública; comparar com `main` se surgir nova aresta de dependência.
- **Pureza e Qualidade Visual em UI:** proibido hooks globais em `window` (`PAX_*`, `__praxis_*`), listeners ad-hoc em `window` ou leitura direta de chaves privadas em `localStorage`. Evitar **Efeito "Boneca Russa"** (conteúdo em shells deve ser *frameless*; proibido `mat-card` dentro de `mat-card` ou múltiplos scrolls). Em `SafeExpressionEvaluator`, usar `coalesce(a, b, '-')` (não `||`, que é booleano); em recursos remotos read-only de `@praxisui/crud`, usar `interactionMode: 'interactive'` (nunca `'inspect-only'` sem dados locais). Sincronizar libs locais (`npm run praxis:local-libs:sync`) antes de validar hosts.
- **Gate de Aceite por Fase vs. Aceite Final:** declarar recursos e fase antes de rodar o auditor; conservar saída integral e exit code. No parecer, separar obrigações da fase atual, dependências transversais necessárias, pendências exclusivas de fases futuras e achados isolados; falhas dos dois primeiros grupos, regressões e incertezas bloqueiam a fase. Um aceite restrito não altera `FAIL` para `PASS`, não reduz thresholds nem libera publicação/deploy/escritas sem prova.

## 8. Classificação, Validação, Builds e Encerramento
- **Classificar antes de editar:** `local-pequena` | `transversal` | `arquitetural` | `contrato-publico` | `docs-apenas`.
- **Áreas de Alto Risco Canônico (exigem Mapa de Impacto prévio):** `x-ui`, `/schemas/filtered`, `/api/praxis/config/**`, contratos AI, headers/`ETag`, `@praxisui/core`, `@praxisui/dynamic-form`, `@praxisui/table`, `public-api`, `examples.manifest.json`, corpus HTTP/LLM e docs/playgrounds oficiais.
- **Mapa Mínimo:** subprojeto canônico → consumidores → docs/exemplos afetados → validações mínimas → risco de breaking change.
- **Validação por Escopo Mínimo & Builds:** começar pela menor suíte focal positiva/negativa pelo impacto semântico; ampliar apenas para consolidar candidato ou atender gate obrigatório. Preferir builds incrementais; não rodar builds concorrentes no mesmo `target`/`dist`; em `public-api` alterada, validar ao menos build focal da lib + build focal de 1 consumidor direto + E2E focal crítico; no Windows, exclusões `!Neon*,!*PostgresTest` não substituem provas de integração/Neon exigidas; em `docs/examples/dynamic-page`, rodar `scripts/validate-dynamic-page-examples.ps1`.
- **Artefatos Derivados:** após alterações de contrato/superfície pública, verificar `README.md`, `docs/**`, `praxis-ui-landing-page`, `examples.manifest.json`, `LLM_SURFACE.md` e `ai-recipes/*` (ou declarar explicitamente que não há derivado afetado).
- **Regra de Honestidade e Encerramento:** distinguir compilação, unit, integração, E2E e QA visual; declarar exatamente o que foi validado e o que ficou pendente; não iniciar novas frentes além do escopo autorizado.

## 9. Release, Skills e Integrações Locais
- **Versionamento e Publicação:** não subir major por estética ou tempo de beta; major bump exige mapa de impacto e plano de migração. Publicação é exclusivamente via tag e workflow oficial do repositório (`RELEASING.md` / `ACTIONS-RELEASE-POLICY.md` — atenção às convenções distintas entre npm e Maven). **Economia de CI:** zero GitHub Actions em desenvolvimento normal.
- **Melhoria Contínua de Skills (`praxis-codex-skills`):** a fonte canônica versionada é `codexrodrigues/praxis-codex-skills` (quando montado localmente ou via `gh`), separando `praxis-skills.manifest.json` de `ergon-migration-skills.manifest.json` (`praxis-*` nunca depende de `ergon-*`). Ao corrigir drift objetivo de skill durante uma tarefa, atualizar a fonte canônica, manifestos/hashes e sincronizar seletivamente apenas as skills afetadas (sem `-Force` global).
- **Integrações e Helpers Locais:** respeitar portas/origins oficiais (nunca inventar aliases ou portas ad hoc); centralizar scripts operacionais do monorepo em `scripts/workspace/`.
