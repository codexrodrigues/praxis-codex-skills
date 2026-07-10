#!/usr/bin/env python3
"""Validate Praxis Codex skill structure without third-party Python packages."""

from __future__ import annotations

import argparse
from pathlib import Path

from codex_skills_common import load_manifest, validate_skill_structure


def validate_manifest(repo_root: Path, family: str, manifest_path: Path | None) -> list[str]:
    _, manifest = load_manifest(repo_root, family, manifest_path)
    errors: list[str] = []
    names = {skill["name"] for skill in manifest["skills"]}

    for skill in manifest["skills"]:
        source = repo_root / skill["sourcePath"]
        if not source.is_dir():
            errors.append(f"{skill['name']}: source path not found: {source}")
            continue

        for error in validate_skill_structure(source, skill["name"]):
            errors.append(f"{skill['name']}: {error}")

        dependencies = skill.get("dependencies", [])
        unknown = [dep for dep in dependencies if dep not in names and not dep.startswith(("praxis-", "ergon-"))]
        if unknown:
            errors.append(f"{skill['name']}: unknown dependency naming: {', '.join(sorted(unknown))}")

    return errors


def validate_directories(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        skill_dir = path.resolve()
        expected_name = skill_dir.name
        for error in validate_skill_structure(skill_dir, expected_name):
            errors.append(f"{skill_dir}: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=["praxis", "ergon-migration"], action="append")
    parser.add_argument("--manifest")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("skill_dirs", nargs="*", help="Explicit skill directories to validate.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []

    families = args.family or []
    if not families and not args.skill_dirs:
        families = ["praxis"]

    for family in families:
        manifest_path = Path(args.manifest).resolve() if args.manifest else None
        errors.extend(validate_manifest(repo_root, family, manifest_path))

    if args.skill_dirs:
        errors.extend(validate_directories([Path(path) for path in args.skill_dirs]))

    if errors:
        print("Codex skill structure validation failed.")
        for error in errors:
            print(f" - {error}")
        return 1

    validated = []
    if families:
        validated.extend(families)
    if args.skill_dirs:
        validated.extend(args.skill_dirs)
    print(f"Codex skill structure validation passed: {', '.join(validated)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)
