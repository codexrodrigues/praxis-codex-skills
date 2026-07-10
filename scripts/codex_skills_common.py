"""Shared helpers for Praxis Codex skill audit and sync scripts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


MANIFEST_BY_FAMILY = {
    "praxis": "praxis-skills.manifest.json",
    "ergon-migration": "ergon-migration-skills.manifest.json",
}
ISSUE_DRAFTS_README_VALIDATION_LINE = "Validacao local: `python3 scripts/validate-issue-drafts.py`"


def sha256_file(path: Path) -> str:
    """Hash UTF-8 text with normalized line endings and binary files byte-for-byte."""
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        payload = raw
    else:
        payload = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()


def skill_file_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not root.exists():
        return hashes

    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.name == ".codex-skill-install.json":
            continue
        relative = path.relative_to(root).as_posix()
        hashes[relative] = sha256_file(path)

    return hashes


def skill_tree_hash(root: Path) -> str:
    hashes = skill_file_hashes(root)
    payload = "\n".join(f"{hashes[name]}  {name}" for name in sorted(hashes))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()


def manifest_for_family(repo_root: Path, family: str) -> Path:
    return repo_root / "codex-skills" / MANIFEST_BY_FAMILY[family]


def skills_root() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


def load_manifest(repo_root: Path, family: str, manifest_path: Path | None = None) -> tuple[Path, dict[str, Any]]:
    resolved = manifest_path.resolve() if manifest_path else manifest_for_family(repo_root, family)
    manifest: dict[str, Any] = json.loads(resolved.read_text(encoding="utf-8"))
    if manifest.get("family") != family:
        raise RuntimeError(f"Manifest family {manifest.get('family')!r} does not match {family!r}")

    names = [skill.get("name") for skill in manifest.get("skills", [])]
    duplicates = sorted(name for name in set(names) if names.count(name) > 1)
    if duplicates:
        raise RuntimeError(f"Duplicate skill names in manifest {resolved}: {', '.join(duplicates)}")

    for skill in manifest.get("skills", []):
        for key in ("name", "sourcePath", "version", "treeSha256"):
            if not str(skill.get(key, "")).strip():
                raise RuntimeError(f"Manifest skill {skill.get('name')!r} has no {key}: {resolved}")
        if family == "praxis":
            ergon_deps = [dep for dep in skill.get("dependencies", []) if dep.startswith("ergon-")]
            if ergon_deps:
                raise RuntimeError(
                    f"Praxis skill {skill['name']!r} cannot depend on Ergon skills: {', '.join(ergon_deps)}"
                )

    return resolved, manifest


def validate_skill_structure(skill_root: Path, expected_name: str) -> list[str]:
    errors: list[str] = []
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"]

    head = skill_md.read_text(encoding="utf-8").splitlines()[:20]
    if len(head) < 3 or head[0] != "---":
        return ["SKILL.md missing YAML frontmatter start"]

    try:
        end_index = head.index("---", 1)
    except ValueError:
        return ["SKILL.md missing YAML frontmatter end"]

    frontmatter = head[1:end_index]
    name_lines = [line for line in frontmatter if line.startswith("name:")]
    description_lines = [line for line in frontmatter if line.startswith("description:")]

    if not name_lines:
        errors.append("SKILL.md frontmatter missing name")
    else:
        actual_name = name_lines[0].split(":", 1)[1].strip().strip("\"'")
        if actual_name != expected_name:
            errors.append(f"SKILL.md name {actual_name!r} does not match manifest name {expected_name!r}")

    if not description_lines:
        errors.append("SKILL.md frontmatter missing description")

    return errors


def install_metadata(manifest: dict[str, Any], skill: dict[str, Any], manifest_path: Path, source_hash: str) -> dict[str, Any]:
    return {
        "managedBy": "praxis-plataform",
        "family": manifest["family"],
        "manifestVersion": manifest["version"],
        "manifestPath": str(manifest_path),
        "skill": skill["name"],
        "skillVersion": skill["version"],
        "sourcePath": skill["sourcePath"],
        "sourceHash": source_hash,
    }

