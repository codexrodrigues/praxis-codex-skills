#!/usr/bin/env python3
"""Audit public Praxis repositories for private domain leaks, machine paths, and broken relative Markdown links."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

IGNORED_DIRS = {".git", "node_modules", "dist", "target", ".angular", ".m2repo", "__pycache__", ".mvn"}
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".svg", ".pdf",
    ".jar", ".class", ".zip", ".gz", ".tar", ".woff", ".woff2", ".ttf",
    ".eot", ".bin", ".exe", ".dll", ".so", ".dylib",
}

_NEON_BRANCH_PAT = (
    r"\bbr-(?!(?:child|parent|test|example|mock|fake|sample|isolated|other|synthetic|and)\b)"
    r"[a-z0-9]+-[a-z0-9]+-[a-z0-9]{6,}\b"
)
_NEON_ENDPOINT_PAT = (
    r"\bep-(?!(?:child|parent|test|example|mock|fake|sample|isolated|other|synthetic)"
    r"(?:-[a-z0-9]+)*(?:\.[a-z0-9-]+)*\.aws\.neon\.tech)[a-z0-9.-]+\.aws\.neon\.tech\b"
)

LEGACY_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("legacy-domain-term", re.compile(r"\b(?:Ergon|ErgonX|HADES|PACK_HADES|Archon|Techne|C_ERGON|PCK_SUBST)\b")),
    ("legacy-ergon-identifier", re.compile(r"\b(?:ERGadm[A-Za-z0-9_]*|ERG-\d+|PCK_(?!(?:TEST|SAMPLE|MOCK|EXAMPLE|DUMMY)\b)[A-Z0-9_]+)\b")),
    ("local-machine-path", re.compile(r"(?:[A-Za-z]:[/\\](?:Users|Developer)[/\\][A-Za-z0-9_.-][^\s\"'`<>]*|/Users/[A-Za-z0-9_.-][^\s\"'`<>]*|/mnt/[a-z]/[A-Za-z0-9_.-][^\s\"'`<>]*|file:///[A-Za-z]:[/\\][A-Za-z0-9_.-][^\s\"'`<>]*)")),
    ("private-feed-url", re.compile(r"pkgs\.dev\.azure\.com/technecloud", re.IGNORECASE)),
    ("neon-project-or-endpoint-id", re.compile(rf"\b(?:ancient-leaf|dark-mountain|holy-mouse)\b|{_NEON_BRANCH_PAT}|{_NEON_ENDPOINT_PAT}")),
)

NEON_REAL_BRANCH_OR_ENDPOINT_RE = re.compile(rf"{_NEON_BRANCH_PAT}|{_NEON_ENDPOINT_PAT}")

LEGACY_MD_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("legacy-studio-name", re.compile(r"\bpraxis-rules-studio\b", re.IGNORECASE)),
)

SELF_DEFINITION_PATHS = frozenset({
    "scripts/audit-agents-governance.py",
    "scripts/audit-agents-governance.ps1",
    "scripts/workspace/audit-agents-governance.py",
    "scripts/workspace/audit-agents-governance.ps1",
    "scripts/workspace/audit-public-repo-purity.py",
    "scripts/workspace/test_workspace_auditors.py",
    "tests/test_audit_agents_governance.py",
})

NEGATIVE_RULE_DOC_PATHS = frozenset({
    "AGENTS.md",
    "docs/platform-governance/workspace-root-AGENTS.md",
    "docs/platform-governance/ciclo-de-vida-neon.md",
})

NEGATIVE_RULE_EXEMPT_CODES = frozenset({
    "legacy-domain-term",
    "legacy-ergon-identifier",
})

ERGON_FAMILY_EXEMPT_CODES = frozenset({
    "legacy-domain-term",
    "legacy-ergon-identifier",
})

ERGON_STRICT_ARCHIVE_EXEMPT_CODES = frozenset({
    "legacy-domain-term",
    "legacy-ergon-identifier",
    "local-machine-path",
    "legacy-studio-name",
    "neon-project-or-endpoint-id",
})

DUAL_FAMILY_GOVERNANCE_FILES = frozenset({
    "README.md",
    "codex-skills/ergon-migration-skills.manifest.json",
    "codex-skills/praxis-skills.manifest.json",
    "codex-skills/praxis-skill-authoring-governance/SKILL.md",
    "codex-skills/praxis-skill-authoring-governance/references/portfolio-and-review.md",
    "scripts/codex-skills-common.ps1",
    "scripts/codex_skills_common.py",
    "scripts/generate-skill-review-issue-drafts.py",
    "docs/praxis-skill-review-program.md",
    "docs/praxis-java-skill-coverage-reconciliation-2026-07.md",
    "docs/authoring-capability-review-2026-10-17.md",
    "docs/connection-editor-skill-audit-2026-09-08.md",
    "docs/editor-library-skills-closure-2026-09-08.md",
    "docs/editor-review-2026-09-10.md",
    "docs/engineering/payroll-g4-guidance-20261022.md",
})

MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\r\n]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\r\n]+`")


def _is_ergon_family_path(rel: str) -> bool:
    """Return True for files scoped to the ergon-migration family or dual-family governance."""
    return rel in DUAL_FAMILY_GOVERNANCE_FILES or rel.startswith((
        "codex-skills/ergon-",
        "docs/skill-reviews/ergon-",
        "docs/issue-drafts/skill-reviews/ergon-",
        "docs/engineering/handoffs/",
    ))


def _is_ergon_archive_path(rel: str) -> bool:
    """Return True for ergon skill family or hash-sealed historical patch files."""
    return rel.startswith("codex-skills/ergon-") or rel == "docs/engineering/handoffs/2026-10-13-real-bulk/changes.patch"


def _iter_repo_files(repo_root: Path, staged_only: bool = False) -> list[Path]:
    """Return tracked or non-ignored files under repo_root."""
    if staged_only and (repo_root / ".git").exists():
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return [repo_root / line.strip() for line in proc.stdout.splitlines() if line.strip()]

    if (repo_root / ".git").exists():
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "ls-files"],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode == 0:
            return [repo_root / line.strip() for line in proc.stdout.splitlines() if line.strip()]

    collected: list[Path] = []
    for root_str, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        for name in sorted(filenames):
            collected.append(Path(root_str) / name)
    return collected


def _check_broken_md_links(md_path: Path, text: str, repo_root: Path) -> list[dict[str, str]]:
    """Detect broken relative links inside Markdown prose outside fenced/inline code."""
    stripped = FENCE_RE.sub("", text)
    stripped = INLINE_CODE_RE.sub("", stripped)
    findings: list[dict[str, str]] = []

    for match in MD_LINK_RE.finditer(stripped):
        raw_target = match.group(1).strip().split()[0].strip("<>")
        if not raw_target or raw_target.startswith(("#", "http://", "https://", "mailto:", "javascript:")):
            continue
        if "<" in raw_target or ">" in raw_target or "{" in raw_target:
            continue
        clean_target = unquote(raw_target.split("#", 1)[0].split("?", 1)[0])
        if not clean_target or "apidocs" in Path(clean_target).parts:
            continue
        resolved = (md_path.parent / clean_target).resolve()
        if resolved.suffix.lower() == ".html" and not resolved.exists() and resolved.with_suffix(".md").exists():
            continue
        if not resolved.exists():
            if not resolved.is_relative_to(repo_root):
                continue
            skill_root_candidate = (md_path.parent.parent / clean_target).resolve()
            if (md_path.parent.parent / "SKILL.md").is_file() and skill_root_candidate.exists():
                continue
            try:
                rel = md_path.relative_to(repo_root).as_posix()
            except ValueError:
                rel = str(md_path)
            findings.append({
                "file": rel,
                "code": "broken-markdown-link",
                "detail": f"missing link target '{raw_target}'",
            })
    return findings


def audit_repository(repo_root: Path, *, staged_only: bool = False) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Audit repository files and return (leaks, broken_links)."""
    repo_root = repo_root.resolve()
    leaks: list[dict[str, str]] = []
    broken_links: list[dict[str, str]] = []
    is_workspace_subdir = repo_root.name == "workspace" and repo_root.parent.name == "scripts"
    is_dual_family_skills_repo = (repo_root / "codex-skills" / "ergon-migration-skills.manifest.json").is_file()

    for file_path in _iter_repo_files(repo_root, staged_only=staged_only):
        if not file_path.is_file() or file_path.suffix.lower() in BINARY_EXTENSIONS:
            continue
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue

        try:
            text = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        try:
            rel = file_path.relative_to(repo_root).as_posix()
        except ValueError:
            rel = str(file_path)

        normalized_rel = f"scripts/workspace/{rel}" if is_workspace_subdir else rel
        is_self_definition = normalized_rel in SELF_DEFINITION_PATHS
        is_negative_rule_doc = normalized_rel in NEGATIVE_RULE_DOC_PATHS
        ergon_exempt_codes: frozenset[str] = frozenset()
        if is_dual_family_skills_repo:
            if _is_ergon_archive_path(rel):
                ergon_exempt_codes = ERGON_STRICT_ARCHIVE_EXEMPT_CODES
            elif _is_ergon_family_path(rel):
                ergon_exempt_codes = ERGON_FAMILY_EXEMPT_CODES

        is_markdown = file_path.suffix.lower() == ".md"
        if not is_self_definition:
            for line_no, line in enumerate(text.splitlines(), start=1):
                for code, pattern in LEGACY_PATTERNS:
                    if is_negative_rule_doc:
                        if code in NEGATIVE_RULE_EXEMPT_CODES:
                            continue
                        if code == "neon-project-or-endpoint-id":
                            if NEON_REAL_BRANCH_OR_ENDPOINT_RE.search(line):
                                leaks.append({"file": rel, "code": code, "detail": f"line {line_no} matches {code}"})
                            continue
                    if code in ergon_exempt_codes:
                        continue
                    if pattern.search(line):
                        leaks.append({"file": rel, "code": code, "detail": f"line {line_no} matches {code}"})
                if is_markdown:
                    for code, pattern in LEGACY_MD_PATTERNS:
                        if code in ergon_exempt_codes:
                            continue
                        if pattern.search(line):
                            leaks.append({"file": rel, "code": code, "detail": f"line {line_no} matches {code}"})

        if is_markdown:
            broken_links.extend(_check_broken_md_links(file_path, text, repo_root))

    return leaks, broken_links


def sanitize_evidence_path(target: Path) -> int:
    """Sanitize machine paths, private feeds, and Neon IDs in an evidence file or directory."""
    files = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file() and p.suffix.lower() not in BINARY_EXTENSIONS]
    replacements: tuple[tuple[re.Pattern[str], str], ...] = (
        (re.compile(r"file:///[A-Za-z]:[^\s\"'`<>]+"), "<LOCAL_FILE_URI>"),
        (re.compile(r"(?:[A-Za-z]:[/\\](?:Users|Developer)[/\\][^\s\"'`<>]+|/Users/[^\s\"'`<>]+|/mnt/[a-z]/[^\s\"'`<>]+)"), "<LOCAL_PATH>"),
        (re.compile(r"https?://pkgs\.dev\.azure\.com/technecloud[^\s\"'`<>]*", re.IGNORECASE), "<PRIVATE_FEED_URL>"),
        (re.compile(r"\bep-[a-z0-9.-]+\.aws\.neon\.tech\b"), "<NEON_ENDPOINT>"),
        (re.compile(r"\bbr-[a-z0-9-]+-[a-z0-9]{6,}\b"), "<NEON_BRANCH>"),
        (re.compile(r"\b(?:ancient-leaf|dark-mountain|holy-mouse)(?:-\d+)?\b"), "<NEON_PROJECT>"),
    )
    updated_files = 0
    for f in files:
        try:
            original = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        sanitized = original
        for pattern, repl in replacements:
            sanitized = pattern.sub(repl, sanitized)
        if sanitized != original:
            f.write_text(sanitized, encoding="utf-8", newline="\n")
            updated_files += 1
    return updated_files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Repository path (optional when --repo is used)")
    parser.add_argument("--repo", help="Repository directory to audit")
    parser.add_argument("--staged", action="store_true", help="Audit only staged git files")
    parser.add_argument("--sanitize-evidence", help="Sanitize an evidence file or directory in place")
    args = parser.parse_args(argv)

    if args.sanitize_evidence:
        target = Path(args.sanitize_evidence).resolve()
        if not target.exists():
            print(f"[FAIL] sanitize target not found: {target}", file=sys.stderr)
            return 1
        changed = sanitize_evidence_path(target)
        print(f"Sanitized evidence ({changed} file(s) updated): {target}")
        return 0

    repo_path = Path(args.repo or args.path).resolve()
    if not repo_path.is_dir():
        print(f"[FAIL] repository directory not found: {repo_path}", file=sys.stderr)
        return 1

    leaks, broken_links = audit_repository(repo_path, staged_only=args.staged)
    for item in leaks + broken_links:
        print(f"[FAIL] {item['code']} | {item['file']} | {item['detail']}")

    summary = f"{len(leaks)} leaks, {len(broken_links)} broken links"
    status = "PASS" if (not leaks and not broken_links) else "FAIL"
    print(f"Public repo purity audit: {status} ({summary})")
    return 1 if (leaks or broken_links) else 0


if __name__ == "__main__":
    sys.exit(main())
