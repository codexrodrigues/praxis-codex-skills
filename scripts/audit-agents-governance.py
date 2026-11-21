#!/usr/bin/env python3
"""Audit AGENTS.md files for size budgets, UTF-8 integrity, mojibake, and public-repo hygiene."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MOJIBAKE_TOKENS = (
    "\u00c3\u00a3",  # ã double-encoded
    "\u00c3\u00a7",  # ç
    "\u00c3\u00a1",  # á
    "\u00c3\u00a9",  # é
    "\u00c3\u00ad",  # í
    "\u00c3\u00b3",  # ó
    "\u00c3\u00ba",  # ú
    "\u00c3\u00b5",  # õ
    "\u00c3\u00aa",  # ê
    "\u00c3\u00a2",  # â
    "\u00c3\u0083",  # Ã
    "\u00e2\u20ac\u201d",  # —
    "\u00e2\u20ac\u201c",  # –
    "\ufffd",
)

PUBLIC_FORBIDDEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("legacy-studio-name", re.compile(r"\bpraxis-rules-studio\b", re.IGNORECASE)),
    ("neon-branch-or-endpoint-id", re.compile(r"\b(?:ep-[a-z0-9-]+\.aws\.neon\.tech|br-[a-z0-9-]+-[a-z0-9]{6,})\b")),
    ("local-machine-path", re.compile(r"(?:[A-Za-z]:[/\\](?:Users|Developer)[/\\]|/Users/|/mnt/[a-z]/)")),
)


def audit_agents_file(
    path: Path,
    *,
    is_root: bool = False,
    max_root_bytes: int = 16384,
    max_local_bytes: int = 18432,
    allow_private: bool = False,
) -> list[dict[str, str]]:
    """Return a list of governance findings for a single AGENTS.md file."""
    findings: list[dict[str, str]] = []
    raw = path.read_bytes()
    limit = max_root_bytes if is_root else max_local_bytes
    if len(raw) > limit:
        findings.append({
            "file": str(path),
            "code": "size-budget-exceeded",
            "detail": f"{len(raw)} bytes > limit {limit} bytes",
        })

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        findings.append({
            "file": str(path),
            "code": "invalid-utf8",
            "detail": str(exc),
        })
        return findings

    for idx, line in enumerate(text.splitlines(), start=1):
        for token in MOJIBAKE_TOKENS:
            if token in line:
                findings.append({
                    "file": str(path),
                    "code": "utf8-mojibake",
                    "detail": f"line {idx} contains mojibake token {token!r}",
                })
                break

        if not allow_private:
            for code, pattern in PUBLIC_FORBIDDEN_PATTERNS:
                if pattern.search(line):
                    findings.append({
                        "file": str(path),
                        "code": code,
                        "detail": f"line {idx} matches {code}",
                    })

    return findings


def collect_agents_files(root: Path, include_nested: bool = True) -> list[Path]:
    """Collect AGENTS.md files under root, ignoring node_modules/dist/target/.git."""
    ignored = {".git", "node_modules", "dist", "target", ".angular", ".m2repo"}
    if not include_nested:
        candidate = root / "AGENTS.md"
        return [candidate] if candidate.is_file() else []

    files: list[Path] = []
    for path in root.rglob("AGENTS.md"):
        if any(part in ignored for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".", help="Repository root or AGENTS.md file")
    parser.add_argument("--root-agents", action="store_true", help="Apply root AGENTS.md budget to target")
    parser.add_argument("--max-root-bytes", type=int, default=16384)
    parser.add_argument("--max-local-bytes", type=int, default=18432)
    parser.add_argument("--allow-private", action="store_true", help="Skip public-repo hygiene checks")
    parser.add_argument("--no-nested", action="store_true", help="Check only root AGENTS.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)

    target = Path(args.target).resolve()
    if target.is_file():
        files = [target]
        root_file = target if args.root_agents else None
    else:
        files = collect_agents_files(target, include_nested=not args.no_nested)
        root_file = (target / "AGENTS.md") if args.root_agents else None

    all_findings: list[dict[str, str]] = []
    for f in files:
        all_findings.extend(
            audit_agents_file(
                f,
                is_root=(root_file is not None and f == root_file),
                max_root_bytes=args.max_root_bytes,
                max_local_bytes=args.max_local_bytes,
                allow_private=args.allow_private,
            )
        )

    if args.json:
        print(json.dumps({"checked": len(files), "findings": all_findings}, indent=2, ensure_ascii=False))
    else:
        for item in all_findings:
            print(f"[FAIL] {item['code']} | {item['file']} | {item['detail']}")
        status = "PASS" if not all_findings else "FAIL"
        print(f"AGENTS governance audit: {status} (files={len(files)}, findings={len(all_findings)})")

    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main())
