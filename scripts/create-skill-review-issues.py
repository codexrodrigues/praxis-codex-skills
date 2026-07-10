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


def draft_family(content: str, path: Path) -> str:
    for line in content.splitlines():
        if line.startswith("- Familia:"):
            family = line.split(":", 1)[1].strip()
            if family:
                return family
    raise RuntimeError(f"Draft has no Familia field: {path}")


def issue_payloads(draft_root: Path, limit: int | None = None) -> list[dict[str, str]]:
    payloads: list[dict[str, str]] = []
    for path in draft_files(draft_root):
        content = path.read_text()
        payloads.append(
            {
                "path": str(path),
                "title": draft_title(content, path),
                "family": draft_family(content, path),
                "body": content,
            }
        )
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


def missing_payloads(payloads: list[dict[str, str]], issues: list[dict[str, str]]) -> list[dict[str, str]]:
    existing_titles = {issue["title"] for issue in issues}
    return [payload for payload in payloads if payload["title"] not in existing_titles]


def issue_coverage_rows(payloads: list[dict[str, str]], issues: list[dict[str, str]]) -> list[dict[str, str]]:
    issues_by_title = {issue["title"]: issue for issue in issues}
    rows: list[dict[str, str]] = []
    for payload in payloads:
        issue = issues_by_title.get(payload["title"])
        if issue:
            rows.append(
                {
                    "status": "FOUND",
                    "title": payload["title"],
                    "path": payload["path"],
                    "number": str(issue["number"]),
                    "state": issue["state"],
                    "url": issue["url"],
                }
            )
        else:
            rows.append(
                {
                    "status": "MISSING",
                    "title": payload["title"],
                    "path": payload["path"],
                    "number": "",
                    "state": "",
                    "url": "",
                }
            )
    return rows


def print_issue_coverage(rows: list[dict[str, str]]) -> None:
    for row in rows:
        if row["status"] == "FOUND":
            print(f"FOUND\t#{row['number']}\t{row['state']}\t{row['title']}\t{row['url']}")
        else:
            print(f"MISSING\t-\t-\t{row['title']}\t{row['path']}")

    found = sum(1 for row in rows if row["status"] == "FOUND")
    missing = sum(1 for row in rows if row["status"] == "MISSING")
    print(f"Summary: total={len(rows)} found={found} missing={missing}")


def issue_labels(payload: dict[str, str], extra_labels: list[str], default_labels: bool) -> list[str]:
    labels: list[str] = []
    if default_labels:
        labels.extend(["skill-review", payload["family"]])
    labels.extend(extra_labels)
    return list(dict.fromkeys(label for label in labels if label))


def create_issue(repository: str, title: str, body: str, labels: list[str]) -> None:
    with tempfile.NamedTemporaryFile("w", delete=False) as temporary:
        temporary.write(body)
        temporary_path = Path(temporary.name)

    try:
        command = ["gh", "issue", "create", "--repo", repository, "--title", title, "--body-file", str(temporary_path)]
        for label in labels:
            command.extend(["--label", label])
        subprocess.run(
            command,
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
    parser.add_argument("--report-existing", action="store_true", help="Report draft coverage against existing issues.")
    parser.add_argument("--missing-only", action="store_true", help="Process only drafts without an existing issue title.")
    parser.add_argument("--label", action="append", default=[], help="Additional label to apply when creating issues.")
    parser.add_argument("--no-default-labels", action="store_true", help="Do not apply skill-review and family labels.")
    parser.add_argument("--limit", type=int, help="Maximum number of drafts to process.")
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        print("ERROR: --limit must be greater than zero.", file=sys.stderr)
        return 1

    try:
        payloads = issue_payloads(Path(args.draft_root), None if args.missing_only else args.limit)
        issues = existing_issues(args.repo) if args.report_existing or args.check_existing or args.missing_only else []

        if args.report_existing:
            rows = issue_coverage_rows(payloads, issues)
            if args.missing_only:
                missing_titles = {payload["title"] for payload in missing_payloads(payloads, issues)}
                rows = [row for row in rows if row["title"] in missing_titles]
                if args.limit is not None:
                    rows = rows[: args.limit]
            print_issue_coverage(rows)
            return 0

        if args.check_existing:
            duplicates = duplicate_issue_reports(payloads, issues)
            if duplicates:
                print("Existing GitHub issues match draft titles.", file=sys.stderr)
                for duplicate in duplicates:
                    print(f" - {duplicate}", file=sys.stderr)
                return 1

        if args.missing_only:
            payloads = missing_payloads(payloads, issues)
            if args.limit is not None:
                payloads = payloads[: args.limit]

        for payload in payloads:
            labels = issue_labels(payload, args.label, not args.no_default_labels)
            if args.dry_run:
                label_text = f" [labels: {', '.join(labels)}]" if labels else ""
                print(f"DRY-RUN issue: {payload['title']}{label_text}")
            else:
                create_issue(args.repo, payload["title"], payload["body"], labels)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
