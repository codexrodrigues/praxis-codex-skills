#!/usr/bin/env python3
"""Generate skill review issue drafts from the canonical skill manifests."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from codex_skills_common import (
    ISSUE_DRAFTS_README_VALIDATION_LINE as README_VALIDATION_LINE,
    MANIFEST_BY_FAMILY,
    load_manifest,
)


DEFAULT_REPOSITORY = "codexrodrigues/praxis-codex-skills"
DEFAULT_DRAFT_ROOT = Path("docs/issue-drafts/skill-reviews")
DEFAULT_README = Path("docs/issue-drafts/README.md")


def canonical_project(skill: dict[str, str]) -> str:
    name = skill["name"]
    if skill["family"] == "ergon-migration":
        return "ergon-migration"
    if name.startswith("praxis-config-"):
        return "praxis-config-starter"
    if name.startswith("praxis-api-quickstart-"):
        return "praxis-api-quickstart"
    if name.startswith("praxis-http-examples-"):
        return "praxisui-http-examples"
    if name.startswith("praxis-landing-"):
        return "praxis-ui-landing-page"
    if name.startswith("praxis-metadata-") and not name.startswith("praxis-metadata-editor-"):
        return "praxis-metadata-starter"
    if name in {
        "praxis-dto-annotations",
        "praxis-java-host-project",
        "praxis-resource-entity-lookup-backend",
    }:
        return "praxis-metadata-starter"
    if name in {"praxis-ai-backend-config-contracts", "praxis-files-upload-backend-contract"}:
        return "transversal"
    return "praxis-ui-angular"


def review_area(skill: dict[str, str]) -> str:
    name = skill["name"]
    if skill["family"] == "ergon-migration":
        return "migration"
    area_prefixes = (
        "ai",
        "angular",
        "api-quickstart",
        "charts",
        "config",
        "core",
        "cron",
        "crud",
        "dialog",
        "editorial-forms",
        "fields",
        "files-upload",
        "form",
        "http-examples",
        "landing",
        "list",
        "manual-form",
        "metadata-editor",
        "metadata",
        "navigation",
        "page-builder",
        "rich-content",
        "settings",
        "stepper",
        "table-rule",
        "table",
        "tabs",
        "visual-builder",
    )
    suffix = name.removeprefix("praxis-")
    return next((prefix for prefix in area_prefixes if suffix.startswith(prefix)), "transversal")


def risk_level(skill: dict[str, str]) -> str:
    project = canonical_project(skill)
    area = review_area(skill)
    if area in {"ai", "core", "fields", "form", "table", "table-rule", "metadata"}:
        return "alto"
    if project in {"praxis-config-starter", "praxis-metadata-starter", "transversal"}:
        return "alto"
    if area in {"charts", "metadata-editor", "page-builder", "visual-builder", "settings"}:
        return "medio-alto"
    return "medio"


def pilot_requirements(skill: dict[str, str]) -> list[str]:
    name = skill["name"]
    if name == "praxis-ai-semantic-intent":
        return [
            "## Escopo especifico do piloto",
            "",
            "Fontes minimas:",
            "",
            "- `projects/praxis-ai/AGENTS.md` e `src/public-api.ts`.",
            "- `core/authoring/governed-decision-routing.ts` e spec.",
            "- `core/authoring/authoring-scope-policy.ts` e spec.",
            "- `ui/ai-assistant/ai-assistant.component.ts`, com foco em clarifications, component identity e grounding textual.",
            "- Consumidores diretos em manual form, list, table, expansion, tabs, stepper e page builder.",
            "",
            "Cenarios obrigatorios:",
            "",
            "- Feliz: contexto canonico `recommendedAuthoringFlow=shared_rule_authoring` governa o handoff independentemente do wording.",
            "- Risco: matching textual usado depois da resolucao semantica apenas ranqueia alvo canonico ou materializa clarification.",
            "- Adversarial: prompt com termos de regra, acesso ou elegibilidade nao autoriza handoff nem patch sem contexto semantico explicito.",
            "",
            "Validacao focal minima:",
            "",
            "```bash",
            "npx ng test praxis-ai --watch=false --progress=false --include=projects/praxis-ai/src/lib/core/authoring/authoring-scope-policy.spec.ts --include=projects/praxis-ai/src/lib/core/authoring/governed-decision-routing.spec.ts",
            "```",
            "",
        ]
    if name == "praxis-charts-runtime-data":
        return [
            "## Escopo especifico do piloto",
            "",
            "Fontes minimas:",
            "",
            "- `projects/praxis-charts/AGENTS.md` e `src/public-api.ts`.",
            "- Modelos `x-ui-chart`, config e dataset.",
            "- Mapper, normalizer, validation, schema mapper e backend payload adapter.",
            "- Stats API, analytics contract/config adapters, providers e specs focais.",
            "",
            "Cenarios obrigatorios:",
            "",
            "- Feliz: `chartDocument` com `source.kind=praxis.stats` materializa config e request canonicamente.",
            "- Risco: `queryContext`, drilldown ou cross-filter preserva filtros sem inventar vocabulario frontend.",
            "- Adversarial: rejeitar raw ECharts, URL de stats montada por string ou metrica local quando `x-ui.chart`/stats ja possui owner canonico.",
            "",
            "Validacao focal minima: specs dos mappers/validators e stats adapters envolvidos; registrar qualquer smoke backend/dashboard nao executado.",
            "",
        ]
    if name == "praxis-core-composition-runtime":
        return [
            "## Escopo especifico do piloto",
            "",
            "Fontes minimas:",
            "",
            "- `projects/praxis-core/AGENTS.md`, docs de connection editor e canvas runtime.",
            "- `src/lib/composition/**`, `src/lib/widgets/**` e modelos de composition/ports.",
            "- Surface host, related-resource outlet, observation registry e binding runtime.",
            "- Consumidores em page builder, visual builder e container widgets.",
            "",
            "Cenarios obrigatorios:",
            "",
            "- Feliz: evento de widget percorre link/transform/port e produz observacao diagnostica reproduzivel.",
            "- Risco: nested port ou surface target ausente falha com diagnostico governado e sem estado silenciosamente divergente.",
            "- Adversarial: rejeitar event bus, action router, transform dialect ou command string local quando core ja expressa a composicao.",
            "",
            "Validacao focal minima: specs de composition runtime, link executor/transform, nested ports, dynamic widget page e surface host afetados.",
            "",
        ]
    return []


def skill_description(skill_root: Path) -> str:
    for line in (skill_root / "SKILL.md").read_text().splitlines()[:20]:
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def load_skills(repo_root: Path, families: list[str]) -> list[dict[str, str]]:
    skills: list[dict[str, str]] = []
    for family in families:
        _, manifest = load_manifest(repo_root, family, None)
        for skill in manifest["skills"]:
            source_path = skill["sourcePath"].rstrip("/") + "/"
            skills.append(
                {
                    "family": family,
                    "name": skill["name"],
                    "path": source_path,
                    "description": skill_description(repo_root / skill["sourcePath"]),
                }
            )
    return sorted(skills, key=lambda item: item["name"])


def review_focus(family: str) -> list[str]:
    if family == "praxis":
        return [
            "- Confirmar aderencia aos recursos oficiais e atuais da plataforma Praxis.",
            "- Remover ou corrigir guidance que incentive workaround local, API paralela ou abstracao fora do owner canonico.",
            "- Verificar se a skill usa recursos ricos do Praxis: metadata, schemas, x-ui, actions, surfaces, capabilities, option sources, runtime Angular, starters e contratos publicos aplicaveis.",
        ]

    return [
        "- Confirmar que a skill conduz o processo Ergon/Archon sem redefinir contratos da plataforma Praxis.",
        "- Verificar se cada uso de recurso Praxis chama a skill Praxis correta e preserva a direcao de dependencia ergon-* -> praxis-*.",
        "- Validar que o fluxo de migracao mantem evidencia, gates, paridade, seguranca HADES/legado e handoff sem atalhos frageis.",
    ]


def draft_body(skill: dict[str, str]) -> str:
    title = f"Revisar skill {skill['family']}: {skill['name']}"
    lines: list[Any] = [
        f"# {title}",
        "",
        "## Objetivo",
        "",
        f"Solicitar a um especialista em plataforma Praxis uma revisao criteriosa da skill {skill['name']} para garantir que ela esteja 100% em conformidade com os recursos disponiveis do Praxis e com as melhores praticas de uso desses recursos.",
        "",
        "O objetivo e que qualquer agente que use esta skill consiga implementar com excelencia, seguranca e velocidade a funcionalidade coberta por ela.",
        "",
        "## Skill",
        "",
        f"- Familia: {skill['family']}",
        f"- Caminho: {skill['path']}",
        f"- Descricao atual: {skill['description']}",
        "",
        "## Classificacao inicial",
        "",
        f"- Projeto canonico: {canonical_project(skill)}",
        f"- Area: {review_area(skill)}",
        f"- Risco: {risk_level(skill)}",
        "- Estado: backlog",
        "",
        "## Foco da revisao",
        "",
        review_focus(skill["family"]),
        "",
        "## Checklist minimo",
        "",
        "- [ ] Ler `SKILL.md` inteiro e os arquivos em `references/`, `scripts/` e `agents/` quando aplicavel.",
        "- [ ] Confirmar que a descricao/frontmatter dispara a skill nos cenarios corretos e nao em cenarios amplos demais.",
        "- [ ] Validar progressive disclosure: `SKILL.md` deve conter o fluxo essencial e apontar referencias sem carregar contexto excessivo.",
        "- [ ] Verificar se a skill aponta para owners canonicos corretos da plataforma Praxis.",
        "- [ ] Conferir se recursos ricos e atuais do Praxis sao usados antes de recomendar codigo customizado.",
        "- [ ] Identificar guidance obsoleto, ambiguo, duplicado, local demais ou contrario ao contrato canonico.",
        "- [ ] Confirmar interoperacao com skills relacionadas declaradas no manifesto.",
        "- [ ] Revisar exemplos, templates, comandos e checklists para garantir que um agente consiga executar a tarefa sem lacunas criticas.",
        "- [ ] Mapear `AGENTS.md`, APIs publicas, implementacao, specs, docs, manifests, exemplos e consumidores diretamente relevantes.",
        "- [ ] Classificar cada gap como `ja-suportado-so-ux`, `ja-suportado-mal-nomeado-ou-mal-materializado`, `suportado-parcialmente` ou `lacuna-real-de-contrato`.",
        "- [ ] Atualizar `skillMdSha256` e `treeSha256` no manifesto quando houver mudanca.",
        "- [ ] Rodar `python3 scripts/preflight-python-fallbacks.py` apos qualquer ajuste.",
        f"- [ ] Quando precisar de diagnostico focado, rodar `scripts/audit-praxis-skills.ps1 -Family {skill['family']}` ou `python3 scripts/audit-praxis-skills.py --family {skill['family']}`.",
        "",
        "## Prova operacional obrigatoria",
        "",
        "- [ ] Executar um cenario feliz representativo usando a skill revisada.",
        "- [ ] Executar um cenario de risco, ambiguidade ou edge case relevante para o escopo.",
        "- [ ] Executar um cenario adversarial em que a skill deve rejeitar workaround local, contrato paralelo ou decisao fora do owner canonico.",
        "- [ ] Rodar a menor validacao focal confiavel do codigo Praxis auditado e registrar comando e resultado.",
        "- [ ] Comparar o resultado produzido com as decisoes canonicas esperadas, sem considerar apenas o preflight estrutural.",
        "",
        "## Evidencias para encerramento",
        "",
        "- [ ] Registrar arquivos-fonte e contratos inspecionados.",
        "- [ ] Registrar alteracoes realizadas na skill, referencias, scripts ou metadata.",
        "- [ ] Registrar comandos locais, resultados, limitacoes e validacoes nao executadas.",
        "- [ ] Associar PR ou commit e publicar a auditoria final na issue.",
        "- [ ] Declarar se a skill ficou `aprovada-com-evidencia`, `implementada-sem-auditoria-funcional`, `precisa-reabertura` ou `skill-desatualizada-por-drift`.",
        "",
        pilot_requirements(skill),
        "## Criterios de aceite",
        "",
        "- A skill orienta implementacao/revisao com alto nivel de qualidade e velocidade.",
        "- A skill nao incentiva remendos locais quando existe recurso Praxis canonico.",
        "- Os recursos ricos do Praxis relacionados ao escopo da skill estao mencionados e roteados corretamente.",
        "- O agente usuario da skill sabe quando aplicar, quando combinar com outra skill e quando abrir follow-up de plataforma.",
        "- O manifesto permanece consistente, com hashes atualizados.",
        "- A prova operacional demonstra que a skill conduz pelo menos um fluxo real e rejeita um antipadrao relevante.",
        "- A issue contem evidencia suficiente para que outra pessoa reproduza a auditoria local.",
    ]

    flattened: list[str] = []
    for line in lines:
        if isinstance(line, list):
            flattened.extend(line)
        else:
            flattened.append(line)
    return "\n".join(flattened) + "\n"


def readme_body(repository: str, skills: list[dict[str, str]]) -> str:
    lines = [
        "# Skill Review Issue Drafts",
        "",
        "A criacao direta de issues pelo conector falhou com `403 Resource not accessible by integration`. Estes drafts foram gerados para criacao manual ou via script quando a permissao de Issues estiver habilitada.",
        "",
        f"Repo alvo: {repository}",
        "",
        README_VALIDATION_LINE,
        "",
    ]
    lines.extend(f"- [{skill['name']}](skill-reviews/{skill['name']}.md)" for skill in skills)
    return "\n".join(lines) + "\n"


def expected_outputs(repo_root: Path, repository: str, draft_root: Path, readme_path: Path, families: list[str]) -> dict[Path, str]:
    skills = load_skills(repo_root, families)
    outputs = {readme_path: readme_body(repository, skills)}
    for skill in skills:
        outputs[draft_root / f"{skill['name']}.md"] = draft_body(skill)
    return outputs


def check_generated_outputs(
    repo_root: Path, repository: str, draft_root: Path, readme_path: Path, families: list[str]
) -> list[str]:
    outputs = expected_outputs(repo_root, repository, draft_root, readme_path, families)
    errors: list[str] = []

    for relative_path, expected in outputs.items():
        path = repo_root / relative_path
        if not path.exists():
            errors.append(f"Missing generated file: {relative_path.as_posix()}")
        elif path.read_text() != expected:
            errors.append(f"Generated file is stale: {relative_path.as_posix()}")

    expected_drafts = {path.name for path in outputs if path.parent == draft_root}
    resolved_draft_root = repo_root / draft_root
    if resolved_draft_root.exists():
        for stale in sorted(resolved_draft_root.glob("*.md")):
            if stale.name not in expected_drafts:
                errors.append(f"Stale generated draft: {stale.relative_to(repo_root).as_posix()}")

    return errors


def generate(repo_root: Path, repository: str, draft_root: Path, readme_path: Path, families: list[str]) -> int:
    outputs = expected_outputs(repo_root, repository, draft_root, readme_path, families)
    resolved_draft_root = repo_root / draft_root
    resolved_readme = repo_root / readme_path
    resolved_draft_root.mkdir(parents=True, exist_ok=True)
    resolved_readme.parent.mkdir(parents=True, exist_ok=True)

    expected_files = {path.name for path in outputs if path.parent == draft_root}
    for stale in resolved_draft_root.glob("*.md"):
        if stale.name not in expected_files:
            stale.unlink()

    for relative_path, content in outputs.items():
        (repo_root / relative_path).write_text(content)

    return len(expected_files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--draft-root", default=str(DEFAULT_DRAFT_ROOT))
    parser.add_argument("--readme", default=str(DEFAULT_README))
    parser.add_argument("--family", choices=sorted(MANIFEST_BY_FAMILY), action="append")
    parser.add_argument("--check", action="store_true", help="Check generated files without writing.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    families = args.family or sorted(MANIFEST_BY_FAMILY)
    draft_root = Path(args.draft_root)
    readme_path = Path(args.readme)

    if args.check:
        errors = check_generated_outputs(repo_root, args.repository, draft_root, readme_path, families)
        if errors:
            print("Skill review issue drafts are not up to date.")
            for error in errors:
                print(f" - {error}")
            return 1
        print("Skill review issue drafts are up to date.")
        return 0

    count = generate(repo_root, args.repository, draft_root, readme_path, families)
    print(f"Generated {count} issue draft(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)
