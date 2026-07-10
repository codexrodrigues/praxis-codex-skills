#!/usr/bin/env python3
"""Validate generated skill review issue drafts against the canonical manifests."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from codex_skills_common import (
    ISSUE_DRAFTS_README_VALIDATION_LINE as README_VALIDATION_LINE,
    MANIFEST_BY_FAMILY,
    load_manifest,
)


DRAFTS_ROOT = Path("docs/issue-drafts/skill-reviews")
README_PATH = Path("docs/issue-drafts/README.md")


def manifest_skills(repo_root: Path, families: list[str]) -> dict[str, dict[str, str]]:
    skills: dict[str, dict[str, str]] = {}
    for family in families:
        _, manifest = load_manifest(repo_root, family, None)
        for skill in manifest["skills"]:
            skills[skill["name"]] = {
                "family": family,
                "name": skill["name"],
                "sourcePath": skill["sourcePath"].rstrip("/") + "/",
            }
    return skills


def draft_names(drafts_root: Path) -> set[str]:
    if not drafts_root.exists():
        return set()
    return {path.stem for path in drafts_root.glob("*.md")}


def readme_links(readme_path: Path) -> set[str]:
    if not readme_path.exists():
        return set()

    content = readme_path.read_text(encoding="utf-8")
    return set(re.findall(r"\]\(skill-reviews/([^)]+)\.md\)", content))


def validate_drafts(repo_root: Path, families: list[str]) -> list[str]:
    skills = manifest_skills(repo_root, families)
    drafts_root = repo_root / DRAFTS_ROOT
    readme_path = repo_root / README_PATH
    actual_drafts = draft_names(drafts_root)
    errors: list[str] = []

    missing = sorted(set(skills) - actual_drafts)
    extra = sorted(actual_drafts - set(skills))
    if missing:
        errors.append(f"Missing skill review drafts: {', '.join(missing)}")
    if extra:
        errors.append(f"Skill review drafts without manifest entry: {', '.join(extra)}")

    for name in sorted(set(skills) & actual_drafts):
        expected = skills[name]
        draft_path = drafts_root / f"{name}.md"
        content = draft_path.read_text(encoding="utf-8")
        required_snippets = [
            f"# Revisar skill {expected['family']}: {name}",
            f"- Familia: {expected['family']}",
            f"- Caminho: {expected['sourcePath']}",
            "## Classificacao inicial",
            "- Projeto canonico:",
            "- Risco:",
            "## Prova operacional obrigatoria",
            "Executar um cenario feliz representativo",
            "Executar um cenario adversarial",
            "## Evidencias para encerramento",
            "Associar PR ou commit",
            "python3 scripts/preflight-python-fallbacks.py",
            f"python3 scripts/audit-praxis-skills.py --family {expected['family']}",
        ]
        for snippet in required_snippets:
            if snippet not in content:
                errors.append(f"{draft_path.relative_to(repo_root)}: missing required text: {snippet}")

    linked = readme_links(readme_path)
    readme_content = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    if README_VALIDATION_LINE not in readme_content:
        errors.append(f"README missing local validation guidance: {README_VALIDATION_LINE}")

    missing_links = sorted(set(skills) - linked)
    extra_links = sorted(linked - set(skills))
    if missing_links:
        errors.append(f"README missing skill review draft links: {', '.join(missing_links)}")
    if extra_links:
        errors.append(f"README links skill review drafts without manifest entry: {', '.join(extra_links)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--family", choices=sorted(MANIFEST_BY_FAMILY), action="append")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    families = args.family or sorted(MANIFEST_BY_FAMILY)
    errors = validate_drafts(repo_root, families)

    if errors:
        print("Skill review issue draft validation failed.")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Skill review issue draft validation passed: {', '.join(families)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)

