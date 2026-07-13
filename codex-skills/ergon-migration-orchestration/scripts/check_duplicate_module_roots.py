#!/usr/bin/env python3
"""Detect ambiguous Ergon migration module roots before module-owned edits."""

from __future__ import annotations

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


BLOCK_EXIT = 2
SKIP_DIRS = {
    ".git",
    ".gradle",
    ".idea",
    ".mvn",
    "build",
    "dist",
    "node_modules",
    "out",
    "target",
}


@dataclass(frozen=True)
class Candidate:
    path: Path
    artifact_id: str | None
    directory_match: bool
    git_root: Path | None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect duplicate module roots such as migracao/<module> and migracao-package/<module> before migration edits."
    )
    parser.add_argument("--workspace-root", required=True, help="Canonical migration workspace root from AGENTS.md, for example .../migracao.")
    parser.add_argument("--module", required=True, help="Expected module directory name, for example ms-administracao-pessoal.")
    parser.add_argument("--artifact-id", help="Expected Maven artifactId. Defaults to --module.")
    parser.add_argument("--current-root", default=".", help="Current directory or intended edit root. Defaults to cwd.")
    parser.add_argument("--canonical-root", help="Expected canonical module root. Defaults to <workspace-root>/<module>.")
    parser.add_argument("--max-depth", type=int, default=4, help="Directory search depth from the workspace parent. Defaults to 4.")
    parser.add_argument("--allow-non-git", action="store_true", help="Allow the canonical module root to be outside a git checkout.")
    return parser.parse_args(argv)


def resolve(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def sanitize(path: Path) -> str:
    text = str(path)
    home = str(Path.home())
    if home and text.startswith(home):
        text = "~" + text[len(home) :]
    for key, value in os.environ.items():
        if not value or len(value) < 8:
            continue
        upper = key.upper()
        if any(token in upper for token in ("TOKEN", "SECRET", "PASSWORD", "PASS", "PWD", "AUTH", "COOKIE")):
            text = text.replace(value, f"<{upper}>")
    return text


def find_git_root(path: Path) -> Path | None:
    cursor = path if path.is_dir() else path.parent
    while True:
        if (cursor / ".git").exists():
            return cursor
        if cursor.parent == cursor:
            return None
        cursor = cursor.parent


def artifact_id_from_pom(pom: Path) -> str | None:
    try:
        root = ET.parse(pom).getroot()
    except (ET.ParseError, OSError):
        return None
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}", 1)[0] + "}"
    node = root.find(f"{ns}artifactId")
    if node is not None and node.text and node.text.strip():
        return node.text.strip()
    return None


def iter_dirs(base: Path, max_depth: int):
    if not base.exists() or not base.is_dir():
        return
    stack: list[tuple[Path, int]] = [(base, 0)]
    while stack:
        path, depth = stack.pop()
        yield path
        if depth >= max_depth:
            continue
        try:
            children = list(path.iterdir())
        except OSError:
            continue
        for child in reversed(children):
            if child.is_dir() and child.name not in SKIP_DIRS:
                stack.append((child, depth + 1))


def discover_candidates(workspace_root: Path, module: str, artifact_id: str, max_depth: int) -> list[Candidate]:
    search_root = workspace_root.parent
    candidates: dict[Path, Candidate] = {}
    for path in iter_dirs(search_root, max_depth):
        directory_match = path.name == module
        pom = path / "pom.xml"
        parsed_artifact = artifact_id_from_pom(pom) if pom.exists() else None
        artifact_match = parsed_artifact == artifact_id
        if directory_match or artifact_match:
            candidates[path] = Candidate(
                path=path,
                artifact_id=parsed_artifact,
                directory_match=directory_match,
                git_root=find_git_root(path),
            )
    return sorted(candidates.values(), key=lambda c: str(c.path).lower())


def build_block_message(
    *,
    workspace_root: Path,
    canonical_root: Path,
    current_root: Path,
    candidates: list[Candidate],
    blocking_duplicate_candidates: list[Candidate],
    external_duplicate_candidates: list[Candidate],
    current_inside_canonical: bool,
    canonical_git_root: Path | None,
    allow_non_git: bool,
) -> str | None:
    problems: list[str] = []
    if blocking_duplicate_candidates:
        problems.append("duplicate module roots were found inside the canonical workspace")
    if not current_inside_canonical:
        problems.append("current root is not inside the canonical module root")
    if canonical_git_root is None and not allow_non_git:
        problems.append("canonical module root is not inside a git checkout")
    if not problems:
        return None

    lines = [
        "MIGRATION_MODULE_ROOT_GUARD_BLOCKED: " + "; ".join(problems) + ".",
        f"workspace_root: {sanitize(workspace_root)}",
        f"canonical_root: {sanitize(canonical_root)}",
        f"current_root: {sanitize(current_root)}",
        "candidates:",
    ]
    for candidate in candidates:
        markers: list[str] = []
        if candidate.path == canonical_root:
            markers.append("canonical")
        if is_relative_to(current_root, candidate.path):
            markers.append("current")
        if candidate.path in {c.path for c in blocking_duplicate_candidates}:
            markers.append("duplicate-blocking")
        if candidate.path in {c.path for c in external_duplicate_candidates}:
            markers.append("duplicate-external")
        if candidate.git_root is None:
            markers.append("no-git")
        reason = []
        if candidate.directory_match:
            reason.append("dir")
        if candidate.artifact_id:
            reason.append(f"artifactId={candidate.artifact_id}")
        suffix = f" [{' '.join(markers)}]" if markers else ""
        detail = ", ".join(reason) if reason else "matched"
        lines.append(f"- {sanitize(candidate.path)} ({detail}){suffix}")
    lines.extend(
        [
            "action: switch to the canonical root from AGENTS.md or require an explicit human choice before a module-owned edit.",
            "safety: message intentionally omits credentials, headers, cookies, users, companies, and environment secret values.",
        ]
    )
    return "\n".join(lines)


def build_external_duplicate_advisory(
    *,
    canonical_root: Path,
    external_duplicate_candidates: list[Candidate],
) -> str:
    lines = [
        f"MIGRATION_MODULE_ROOT_GUARD_OK_WITH_EXTERNAL_DUPLICATES: {sanitize(canonical_root)}",
        "external_duplicates:",
    ]
    for candidate in external_duplicate_candidates:
        reason = []
        if candidate.directory_match:
            reason.append("dir")
        if candidate.artifact_id:
            reason.append(f"artifactId={candidate.artifact_id}")
        detail = ", ".join(reason) if reason else "matched"
        lines.append(f"- {sanitize(candidate.path)} ({detail}) [advisory]")
    lines.extend(
        [
            "action: continue only in canonical_root; do not edit the external duplicate roots.",
            "safety: canonical current root was proven, so external worktrees or historical clones are advisory rather than blocking.",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    workspace_root = resolve(args.workspace_root)
    module = args.module.strip()
    artifact_id = (args.artifact_id or module).strip()
    current_root = resolve(args.current_root)
    canonical_root = resolve(args.canonical_root) if args.canonical_root else workspace_root / module
    candidates = discover_candidates(workspace_root, module, artifact_id, args.max_depth)
    duplicate_candidates = [c for c in candidates if c.path != canonical_root]
    blocking_duplicate_candidates = [c for c in duplicate_candidates if is_relative_to(c.path, workspace_root)]
    external_duplicate_candidates = [c for c in duplicate_candidates if not is_relative_to(c.path, workspace_root)]
    current_inside_canonical = is_relative_to(current_root, canonical_root)
    canonical_git_root = find_git_root(canonical_root)
    message = build_block_message(
        workspace_root=workspace_root,
        canonical_root=canonical_root,
        current_root=current_root,
        candidates=candidates,
        blocking_duplicate_candidates=blocking_duplicate_candidates,
        external_duplicate_candidates=external_duplicate_candidates,
        current_inside_canonical=current_inside_canonical,
        canonical_git_root=canonical_git_root,
        allow_non_git=args.allow_non_git,
    )
    if message:
        print(message, file=sys.stderr)
        return BLOCK_EXIT
    if external_duplicate_candidates:
        print(
            build_external_duplicate_advisory(
                canonical_root=canonical_root,
                external_duplicate_candidates=external_duplicate_candidates,
            )
        )
        return 0
    print(f"MIGRATION_MODULE_ROOT_GUARD_OK: {sanitize(canonical_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
