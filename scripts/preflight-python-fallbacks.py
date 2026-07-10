#!/usr/bin/env python3
"""Run the dependency-free Python fallback validation gate."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON_FILES = [
    "scripts/codex_skills_common.py",
    "scripts/audit-praxis-skills.py",
    "scripts/sync-praxis-skills.py",
    "scripts/validate-issue-drafts.py",
    "scripts/validate-praxis-skills.py",
    "scripts/preflight-python-fallbacks.py",
    "tests/test_python_skill_scripts.py",
]
FAMILIES = ["praxis", "ergon-migration"]


def run(command: list[str], *, capture_json: bool = False) -> dict | None:
    print(f"$ {' '.join(command)}", flush=True)
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=capture_json,
    )
    if capture_json:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        if completed.returncode != 0:
            if completed.stdout:
                print(completed.stdout, end="")
            raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")
        return json.loads(completed.stdout)

    if completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")
    return None


def assert_audit_clean(family: str, report: dict) -> None:
    summary = report["summary"]
    failures = {
        key: summary[key]
        for key in ("drift", "missing", "sourceInvalid", "sourceNotInManifest")
        if summary[key] != 0
    }
    if failures:
        raise RuntimeError(f"{family} audit is not clean: {failures}")

    print(
        "Audit summary "
        f"{family}: OK={summary['ok']} "
        f"DRIFT={summary['drift']} "
        f"MISSING={summary['missing']} "
        f"SOURCE_INVALID={summary['sourceInvalid']} "
        f"SOURCE_NOT_IN_MANIFEST={summary['sourceNotInManifest']} "
        f"SOURCE_IN_OTHER_FAMILY_MANIFEST={summary['sourceInOtherFamilyManifest']}"
    )


def main() -> int:
    try:
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests"])
        run([sys.executable, "-m", "py_compile", *PYTHON_FILES])
        run(
            [
                sys.executable,
                "scripts/validate-praxis-skills.py",
                "--family",
                "praxis",
                "--family",
                "ergon-migration",
            ]
        )
        run([sys.executable, "scripts/validate-issue-drafts.py"])
        with tempfile.TemporaryDirectory() as temporary_skills_root:
            for family in FAMILIES:
                run(
                    [
                        sys.executable,
                        "scripts/sync-praxis-skills.py",
                        "--family",
                        family,
                        "--skills-root",
                        temporary_skills_root,
                        "--force",
                        "--delete-extraneous-within-manifest",
                    ]
                )
            for family in FAMILIES:
                report = run(
                    [
                        sys.executable,
                        "scripts/audit-praxis-skills.py",
                        "--family",
                        family,
                        "--skills-root",
                        temporary_skills_root,
                        "--json",
                    ],
                    capture_json=True,
                )
                assert report is not None
                assert_audit_clean(family, report)
    except RuntimeError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Python fallback preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
