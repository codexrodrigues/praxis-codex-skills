#!/usr/bin/env python3
"""Sync Praxis Codex skills without PowerShell."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from codex_skills_common import (
    install_metadata,
    load_manifest,
    sha256_file,
    skill_file_hashes,
    skill_tree_hash,
    skills_root,
    validate_skill_structure,
)


def copy_skill(source: Path, destination: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"DRY-RUN copy: {source} -> {destination}")
        return

    destination.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            shutil.copytree(child, target, dirs_exist_ok=True)
        elif child.name != ".codex-skill-install.json":
            shutil.copy2(child, target)


def remove_extra_files(source: Path, destination: Path, dry_run: bool) -> None:
    source_map = skill_file_hashes(source)
    destination_map = skill_file_hashes(destination)
    for relative in sorted(set(destination_map) - set(source_map)):
        target = destination / relative
        resolved_destination = destination.resolve()
        resolved_target = target.resolve()
        if resolved_destination not in resolved_target.parents and resolved_target != resolved_destination:
            raise RuntimeError(f"Refusing to remove path outside skill destination: {resolved_target}")
        if dry_run:
            print(f"DRY-RUN remove extra file within managed skill: {resolved_target}")
        else:
            target.unlink()


def sync(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).resolve()
    requested_manifest = Path(args.manifest).resolve() if args.manifest else None
    manifest_path, manifest = load_manifest(repo_root, args.family, requested_manifest)
    destination_root = Path(args.skills_root).resolve() if args.skills_root else skills_root()

    if args.dry_run:
        print(f"DRY-RUN create directory: {destination_root}")
    else:
        destination_root.mkdir(parents=True, exist_ok=True)

    conflicts: list[str] = []

    for skill in manifest["skills"]:
        source = repo_root / skill["sourcePath"]
        destination = destination_root / skill["name"]

        if not source.is_dir():
            raise RuntimeError(f"Manifest source path not found for {skill['name']}: {source}")

        structure_errors = validate_skill_structure(source, skill["name"])
        if structure_errors:
            raise RuntimeError(f"Invalid source skill {skill['name']}: {'; '.join(structure_errors)}")

        source_skill_hash = sha256_file(source / "SKILL.md")
        if skill.get("skillMdSha256") and source_skill_hash != skill["skillMdSha256"]:
            raise RuntimeError(
                f"Source hash drift for {skill['name']}. "
                f"Manifest={skill['skillMdSha256']} Actual={source_skill_hash}"
            )

        source_tree_hash = skill_tree_hash(source)
        if skill.get("treeSha256") and source_tree_hash != skill["treeSha256"]:
            raise RuntimeError(
                f"Source tree hash drift for {skill['name']}. "
                f"Manifest={skill['treeSha256']} Actual={source_tree_hash}"
            )

        if destination.is_dir():
            source_map = skill_file_hashes(source)
            destination_map = skill_file_hashes(destination)
            different_files = sorted(
                name for name in set(source_map) & set(destination_map) if source_map[name] != destination_map[name]
            )
            extra_files = sorted(set(destination_map) - set(source_map))
            if (different_files or extra_files) and not args.force:
                conflicts.append(f"{skill['name']}: destination differs; rerun with --force to overwrite managed files")
                continue

        copy_skill(source, destination, args.dry_run)

        if args.delete_extraneous_within_manifest and destination.is_dir():
            remove_extra_files(source, destination, args.dry_run)

        if not args.dry_run:
            metadata = install_metadata(manifest, skill, manifest_path, source_tree_hash)
            metadata["installedAt"] = datetime.now(timezone.utc).isoformat()
            (destination / ".codex-skill-install.json").write_text(
                json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
            )

    if conflicts:
        print("Codex skills sync blocked by destination drift.")
        for conflict in conflicts:
            print(f" - {conflict}")
        raise RuntimeError(f"Sync blocked: {len(conflicts)} conflict(s).")

    print("Codex skills sync dry-run complete." if args.dry_run else "Codex skills synced.")
    print(f"Family: {manifest['family']}")
    print(f"Manifest: {manifest_path}")
    print(f"Destination: {destination_root}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=["praxis", "ergon-migration"], default="praxis")
    parser.add_argument("--manifest")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--skills-root")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--delete-extraneous-within-manifest",
        "--delete-extraneous",
        action="store_true",
        help="Remove files under managed skill destinations that are absent from the canonical source skill.",
    )
    return sync(parser.parse_args())


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)

