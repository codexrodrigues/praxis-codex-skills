#!/usr/bin/env python3
"""Audit Praxis Codex skill manifest hashes without PowerShell."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from codex_skills_common import (
    MANIFEST_BY_FAMILY,
    load_manifest,
    sha256_file,
    skill_file_hashes,
    skill_tree_hash,
    skills_root,
)


def update_manifest_text(text: str, replacements: list[tuple[str, str]]) -> str:
    updated = text
    for old, new in replacements:
        if old == new:
            continue
        marker = f'"{old}"'
        if marker not in updated:
            raise RuntimeError(f"Could not find hash in manifest text: {old}")
        updated = updated.replace(marker, f'"{new}"', 1)
    return updated


def other_family_source_names(repo_root: Path, selected_family: str) -> set[str]:
    names: set[str] = set()
    for family in MANIFEST_BY_FAMILY:
        if family == selected_family:
            continue
        _, manifest = load_manifest(repo_root, family)
        names.update(skill["name"] for skill in manifest["skills"])
    return names


def audit(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    requested_manifest = Path(args.manifest).resolve() if args.manifest else None
    manifest_path, manifest = load_manifest(repo_root, args.family, requested_manifest)
    manifest_text = manifest_path.read_text()
    destination = Path(args.skills_root).resolve() if args.skills_root else skills_root()

    replacements: list[tuple[str, str]] = []
    results: list[dict[str, Any]] = []

    for skill in manifest["skills"]:
        source = repo_root / skill["sourcePath"]
        installed = destination / skill["name"]
        result: dict[str, Any] = {
            "skill": skill["name"],
            "status": "OK",
            "sourcePath": str(source),
            "installedPath": str(installed),
            "errors": [],
            "differentFiles": [],
            "missingFiles": [],
            "extraFiles": [],
        }

        if not source.is_dir():
            result["status"] = "SOURCE_MISSING"
            result["errors"].append(f"source path not found: {source}")
            results.append(result)
            continue

        skill_md = source / "SKILL.md"
        source_skill_hash = sha256_file(skill_md)
        source_tree_hash = skill_tree_hash(source)
        result["sourceHash"] = source_skill_hash
        result["sourceTreeHash"] = source_tree_hash
        result["manifestHash"] = skill.get("skillMdSha256")
        result["manifestTreeHash"] = skill.get("treeSha256")

        if skill.get("skillMdSha256") and source_skill_hash != skill.get("skillMdSha256"):
            result["status"] = "SOURCE_DRIFT"
            result["errors"].append(f"SKILL.md hash differs from manifest: {source_skill_hash}")
            replacements.append((skill["skillMdSha256"], source_skill_hash))
        if skill.get("treeSha256") and source_tree_hash != skill.get("treeSha256"):
            result["status"] = "SOURCE_DRIFT"
            result["errors"].append(f"skill tree hash differs from manifest: {source_tree_hash}")
            replacements.append((skill["treeSha256"], source_tree_hash))

        if installed.is_dir():
            source_files = skill_file_hashes(source)
            installed_files = skill_file_hashes(installed)
            source_names = set(source_files)
            installed_names = set(installed_files)
            result["missingFiles"] = sorted(source_names - installed_names)
            result["extraFiles"] = sorted(installed_names - source_names)
            result["differentFiles"] = sorted(
                name for name in source_names & installed_names if source_files[name] != installed_files[name]
            )
            if result["status"] == "OK" and (
                result["missingFiles"] or result["extraFiles"] or result["differentFiles"]
            ):
                result["status"] = "DRIFT"
        elif result["status"] == "OK":
            result["status"] = "MISSING"

        results.append(result)

    source_names = {skill["name"] for skill in manifest["skills"]}
    other_source_names = other_family_source_names(repo_root, args.family)
    source_root = repo_root / "codex-skills"
    source_dirs = sorted(
        p.name
        for p in source_root.iterdir()
        if p.is_dir() and p.name not in {"__pycache__"}
    )
    source_in_other_family_manifest = sorted(
        name for name in source_dirs if name not in source_names and name in other_source_names
    )
    source_not_in_manifest = sorted(
        name for name in source_dirs if name not in source_names and name not in other_source_names
    )
    installed_only = sorted(
        p.name for p in destination.iterdir() if destination.exists() and p.is_dir() and p.name not in source_names
    )

    summary = {
        "totalManifestSkills": len(results),
        "ok": sum(1 for r in results if r["status"] == "OK"),
        "drift": sum(1 for r in results if r["status"] == "DRIFT"),
        "missing": sum(1 for r in results if r["status"] == "MISSING"),
        "sourceInvalid": sum(1 for r in results if r["status"].startswith("SOURCE_")),
        "installedOnly": len(installed_only),
        "sourceNotInManifest": len(source_not_in_manifest),
        "sourceInOtherFamilyManifest": len(source_in_other_family_manifest),
    }

    if args.fix_manifest and replacements:
        manifest_path.write_text(update_manifest_text(manifest_text, replacements))

    if args.json:
        print(
            json.dumps(
                {
                    "family": args.family,
                    "manifestPath": str(manifest_path),
                    "sourceRoot": str(source_root),
                    "skillsRoot": str(destination),
                    "summary": summary,
                    "results": results,
                    "installedOnly": installed_only,
                    "sourceNotInManifest": source_not_in_manifest,
                    "sourceInOtherFamilyManifest": source_in_other_family_manifest,
                },
                indent=2,
            )
        )
    else:
        print("Codex skills audit")
        print(f"Family: {args.family}")
        print(f"Manifest: {manifest_path}")
        print(f"Source: {source_root}")
        print(f"Destination: {destination}")
        print(
            "Summary: "
            f"OK={summary['ok']} "
            f"DRIFT={summary['drift']} "
            f"MISSING={summary['missing']} "
            f"SOURCE_INVALID={summary['sourceInvalid']} "
            f"INSTALLED_ONLY={summary['installedOnly']} "
            f"SOURCE_NOT_IN_MANIFEST={summary['sourceNotInManifest']} "
            f"SOURCE_IN_OTHER_FAMILY_MANIFEST={summary['sourceInOtherFamilyManifest']}"
        )
        for item in results:
            if item["status"] == "OK":
                continue
            print(f"[{item['status']}] {item['skill']}")
            for error in item["errors"]:
                print(f"  source error: {error}")
            if item["missingFiles"]:
                print(f"  missing: {', '.join(item['missingFiles'])}")
            if item["extraFiles"]:
                print(f"  extra: {', '.join(item['extraFiles'])}")
            if item["differentFiles"]:
                print(f"  different: {', '.join(item['differentFiles'])}")
        if installed_only:
            print(f"Installed-only directories outside family manifest: {', '.join(installed_only)}")
        if source_not_in_manifest:
            print(f"Source directories outside selected manifest: {', '.join(source_not_in_manifest)}")
        if source_in_other_family_manifest:
            print(
                "Source directories tracked by another family manifest: "
                f"{', '.join(source_in_other_family_manifest)}"
            )

    return 1 if any(r["status"].startswith("SOURCE_") for r in results) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=["praxis", "ergon-migration"], default="praxis")
    parser.add_argument("--manifest")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--skills-root")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fix-manifest", action="store_true")
    return audit(parser.parse_args())


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)
