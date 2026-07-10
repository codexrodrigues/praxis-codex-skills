#!/usr/bin/env python3
"""Create GitHub issues from generated skill review issue drafts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_REPOSITORY = "codexrodrigues/praxis-codex-skills"
DEFAULT_DRAFT_ROOT = Path("docs/issue-drafts/skill-reviews")


def draft_files(draft_root: Path) -> list[Path]:
    if not draft_root.exists():
        raise RuntimeError(f"Draft root not found: {draft_root}")
    return sorted(draft_root.glob("*.md"), key=lambda path: path.name)


def draft_title(content: str, path: Path) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
    raise RuntimeError(f"Draft has no H1 title: {path}")


def issue_payloads(draft_root: Path, limit: int | None = None) -> list[dict[str, str]]:
    payloads: list[dict[str, str]] = []
    for path in draft_files(draft_root):
        content = path.read_text()
        payloads.append({"path": str(path), "title": draft_title(content, path), "body": content})
        if limit is not None and len(payloads) >= limit:
            break
    return payloads


def existing_issues(repository: str) -> list[dict[str, str]]:
    completed = subprocess.run(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            repository,
            "--state",
            "all",
            "--limit",
            "1000",
            "--json",
            "number,title,url,state",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def duplicate_issue_reports(payloads: list[dict[str, str]], issues: list[dict[str, str]]) -> list[str]:
    issues_by_title = {issue["title"]: issue for issue in issues}
    reports: list[str] = []
    for payload in payloads:
        issue = issues_by_title.get(payload["title"])
        if issue:
            reports.append(
                f"{payload['title']} already exists as #{issue['number']} ({issue['state']}): {issue['url']}"
            )
    return reports


def create_issue(repository: str, title: str, body: str) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as temporary:
        temporary.write(body)
        temporary_path = Path(temporary.name)

    try:
        subprocess.run(
            ["gh", "issue", "create", "--repo", repository, "--title", title, "--body-file", str(temporary_path)],
            check=True,
        )
    finally:
        temporary_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPOSITORY)
    parser.add_argument("--draft-root", default=str(DEFAULT_DRAFT_ROOT))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check-existing", action="store_true", help="Fail before creating if a draft title already exists.")
    parser.add_argument("--limit", type=int, help="Maximum number of drafts to process.")
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        print("ERROR: --limit must be greater than zero.", file=sys.stderr)
        return 1

    try:
        payloads = issue_payloads(Path(args.draft_root), args.limit)
        if args.check_existing:
            duplicates = duplicate_issue_reports(payloads, existing_issues(args.repo))
            if duplicates:
                print("Existing GitHub issues match draft titles.", file=sys.stderr)
                for duplicate in duplicates:
                    print(f" - {duplicate}", file=sys.stderr)
                return 1

        for payload in payloads:
            if args.dry_run:
                print(f"DRY-RUN issue: {payload['title']}")
            else:
                create_issue(args.repo, payload["title"], payload["body"])
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
