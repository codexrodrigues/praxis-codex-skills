from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from codex_skills_common import (  # noqa: E402
    ISSUE_DRAFTS_README_VALIDATION_LINE,
    load_manifest,
    sha256_file,
    skill_tree_hash,
)


def load_script_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT_MODULE = load_script_module("audit_praxis_skills", SCRIPTS_ROOT / "audit-praxis-skills.py")
CREATE_ISSUES_MODULE = load_script_module("create_skill_review_issues", SCRIPTS_ROOT / "create-skill-review-issues.py")
GENERATE_DRAFTS_MODULE = load_script_module(
    "generate_skill_review_issue_drafts", SCRIPTS_ROOT / "generate-skill-review-issue-drafts.py"
)
SYNC_MODULE = load_script_module("sync_praxis_skills", SCRIPTS_ROOT / "sync-praxis-skills.py")
VALIDATE_MODULE = load_script_module("validate_praxis_skills", SCRIPTS_ROOT / "validate-praxis-skills.py")
ISSUE_DRAFTS_MODULE = load_script_module("validate_issue_drafts", SCRIPTS_ROOT / "validate-issue-drafts.py")
PREFLIGHT_MODULE = load_script_module("preflight_python_fallbacks", SCRIPTS_ROOT / "preflight-python-fallbacks.py")


def write_skill(root: Path, name: str) -> Path:
    skill_root = root / "codex-skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Test skill {name}.\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    return skill_root


def write_raw_skill(root: Path, directory_name: str, content: str) -> Path:
    skill_root = root / "codex-skills" / directory_name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(content, encoding="utf-8")
    return skill_root


def sync_args(
    repo_root: Path,
    skills_root: Path,
    *,
    force: bool = False,
    delete_extraneous: bool = False,
    dry_run: bool = False,
):
    return argparse.Namespace(
        repo_root=str(repo_root),
        family="praxis",
        manifest=None,
        skills_root=str(skills_root),
        dry_run=dry_run,
        force=force,
        delete_extraneous_within_manifest=delete_extraneous,
    )


def run_sync(args) -> int:
    with redirect_stdout(io.StringIO()):
        return SYNC_MODULE.sync(args)


def audit_args(repo_root: Path, skills_root: Path, *, fail_on_drift: bool = False):
    return argparse.Namespace(
        repo_root=str(repo_root),
        family="praxis",
        manifest=None,
        skills_root=str(skills_root),
        json=True,
        fix_manifest=False,
        fail_on_drift=fail_on_drift,
    )


def manifest_entry(repo_root: Path, skill_root: Path) -> dict[str, str]:
    return {
        "name": skill_root.name,
        "sourcePath": skill_root.relative_to(repo_root).as_posix(),
        "version": "0.0.0-test",
        "skillMdSha256": sha256_file(skill_root / "SKILL.md"),
        "treeSha256": skill_tree_hash(skill_root),
    }


def write_manifest(repo_root: Path, family: str, entries: list[dict[str, str]]) -> Path:
    manifest_name = {
        "praxis": "praxis-skills.manifest.json",
        "ergon-migration": "ergon-migration-skills.manifest.json",
    }[family]
    path = repo_root / "codex-skills" / manifest_name
    path.write_text(json.dumps({"family": family, "version": "0.0.0-test", "skills": entries}, indent=2))
    return path


def write_issue_draft(repo_root: Path, family: str, skill_name: str) -> None:
    drafts_root = repo_root / "docs" / "issue-drafts" / "skill-reviews"
    drafts_root.mkdir(parents=True, exist_ok=True)
    (drafts_root / f"{skill_name}.md").write_text(
        f"# Revisar skill {family}: {skill_name}\n\n"
        "## Skill\n\n"
        f"- Familia: {family}\n"
        f"- Caminho: codex-skills/{skill_name}/\n\n"
        "## Classificacao inicial\n\n"
        "- Projeto canonico: praxis-ui-angular\n"
        "- Risco: medio\n\n"
        "## Checklist minimo\n\n"
        "- [ ] Rodar `python3 scripts/preflight-python-fallbacks.py` apos qualquer ajuste.\n"
        "- [ ] Quando precisar de diagnostico focado, rodar "
        f"`scripts/audit-praxis-skills.ps1 -Family {family}` ou "
        f"`python3 scripts/audit-praxis-skills.py --family {family}`.\n\n"
        "## Prova operacional obrigatoria\n\n"
        "- [ ] Executar um cenario feliz representativo usando a skill revisada.\n"
        "- [ ] Executar um cenario adversarial em que a skill deve rejeitar workaround local.\n\n"
        "## Evidencias para encerramento\n\n"
        "- [ ] Associar PR ou commit e publicar a auditoria final na issue.\n"
    )


def write_issue_draft_readme(repo_root: Path, skill_names: list[str]) -> None:
    readme = repo_root / "docs" / "issue-drafts" / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    links = "\n".join(f"- [{name}](skill-reviews/{name}.md)" for name in sorted(skill_names))
    readme.write_text(f"# Skill Review Issue Drafts\n\n{ISSUE_DRAFTS_MODULE.README_VALIDATION_LINE}\n\n{links}\n")


def audit_report(**summary_overrides):
    summary = {
        "ok": 1,
        "drift": 0,
        "missing": 0,
        "sourceInvalid": 0,
        "sourceNotInManifest": 0,
        "sourceInOtherFamilyManifest": 0,
        "installedOnly": 0,
    }
    summary.update(summary_overrides)
    return {"summary": summary}


class PythonSkillScriptTests(unittest.TestCase):
    def test_validate_skill_structure_reads_utf8_skill_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_raw_skill(
                root,
                "praxis-test",
                "---\nname: praxis-test\ndescription: DireÃ§Ã£o encantadora para operaÃ§Ã£o.\n---\n\n# ExperiÃªncia\n",
            )

            self.assertEqual([], VALIDATE_MODULE.validate_directories([skill_root]))

    def test_manifest_hash_updates_are_scoped_to_the_named_skill(self) -> None:
        manifest = '''{
  "skills": [
    {
      "name": "praxis-first",
      "skillMdSha256": "AAAAAAAA",
      "treeSha256": "BBBBBBBB"
    },
    {
      "name": "praxis-second",
      "skillMdSha256": "AAAAAAAA",
      "treeSha256": "BBBBBBBB"
    }
  ]
}
'''

        updated = AUDIT_MODULE.update_manifest_text(
            manifest,
            {"praxis-second": {"skillMdSha256": "CCCCCCCC", "treeSha256": "DDDDDDDD"}},
        )

        self.assertIn('"name": "praxis-first",\n      "skillMdSha256": "AAAAAAAA"', updated)
        self.assertIn('"name": "praxis-second",\n      "skillMdSha256": "CCCCCCCC"', updated)
        self.assertIn('"treeSha256": "DDDDDDDD"', updated)

    def test_sha256_file_normalizes_text_line_endings_and_preserves_binary_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lf = root / "lf.md"
            crlf = root / "crlf.md"
            binary = root / "asset.bin"
            lf.write_bytes(b"first\nsecond\n")
            crlf.write_bytes(b"first\r\nsecond\r\n")
            binary_bytes = b"\x89PNG\r\n\x1a\n\x00\xff"
            binary.write_bytes(binary_bytes)

            self.assertEqual(sha256_file(lf), sha256_file(crlf))
            self.assertEqual(hashlib.sha256(binary_bytes).hexdigest().upper(), sha256_file(binary))

    def test_tree_hash_ignores_install_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_skill(root, "praxis-test")
            first_hash = skill_tree_hash(skill_root)

            (skill_root / ".codex-skill-install.json").write_text('{"managedBy":"test"}\n')

            self.assertEqual(first_hash, skill_tree_hash(skill_root))

    def test_load_manifest_rejects_duplicate_names_and_family_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_skill(root, "praxis-test")
            entry = manifest_entry(root, skill_root)

            duplicate_manifest = write_manifest(root, "praxis", [entry, entry])
            with self.assertRaisesRegex(RuntimeError, "Duplicate skill names"):
                load_manifest(root, "praxis", duplicate_manifest)

            mismatch_manifest = root / "codex-skills" / "mismatch.manifest.json"
            mismatch_manifest.write_text(
                json.dumps({"family": "ergon-migration", "version": "0.0.0-test", "skills": [entry]})
            )
            with self.assertRaisesRegex(RuntimeError, "does not match"):
                load_manifest(root, "praxis", mismatch_manifest)

    def test_audit_separates_other_family_sources_from_untracked_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "installed-skills"
            skills_root.mkdir()

            praxis_skill = write_skill(root, "praxis-test")
            ergon_skill = write_skill(root, "ergon-test")
            write_skill(root, "scratch-test")

            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [manifest_entry(root, ergon_skill)])

            args = argparse.Namespace(
                repo_root=str(root),
                family="praxis",
                manifest=None,
                skills_root=str(skills_root),
                json=True,
                fix_manifest=False,
            )
            output = io.StringIO()
            with redirect_stdout(output):
                result = AUDIT_MODULE.audit(args)

            report = json.loads(output.getvalue())
            self.assertEqual(0, result)
            self.assertEqual(["ergon-test"], report["sourceInOtherFamilyManifest"])
            self.assertEqual(["scratch-test"], report["sourceNotInManifest"])
            self.assertEqual(1, report["summary"]["sourceInOtherFamilyManifest"])
            self.assertEqual(1, report["summary"]["sourceNotInManifest"])

    def test_audit_allows_missing_skills_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "missing-installed-skills"
            praxis_skill = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [])

            args = argparse.Namespace(
                repo_root=str(root),
                family="praxis",
                manifest=None,
                skills_root=str(skills_root),
                json=True,
                fix_manifest=False,
            )
            output = io.StringIO()
            with redirect_stdout(output):
                result = AUDIT_MODULE.audit(args)

            report = json.loads(output.getvalue())
            self.assertEqual(0, result)
            self.assertEqual([], report["installedOnly"])
            self.assertEqual(1, report["summary"]["missing"])

    def test_validate_manifest_and_directories_accept_valid_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])

            self.assertEqual([], VALIDATE_MODULE.validate_manifest(root, "praxis", None))
            self.assertEqual([], VALIDATE_MODULE.validate_directories([skill_root]))

    def test_validate_directories_reports_frontmatter_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_raw_skill(
                root,
                "praxis-test",
                "---\nname: praxis-other\n---\n\n# Invalid\n",
            )

            errors = VALIDATE_MODULE.validate_directories([skill_root])

            self.assertIn("SKILL.md name 'praxis-other' does not match manifest name 'praxis-test'", errors[0])
            self.assertTrue(any("frontmatter missing description" in error for error in errors))

    def test_validate_manifest_reports_unknown_dependency_naming(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_skill(root, "praxis-test")
            entry = manifest_entry(root, skill_root)
            entry["dependencies"] = ["custom-helper"]
            write_manifest(root, "praxis", [entry])

            errors = VALIDATE_MODULE.validate_manifest(root, "praxis", None)

            self.assertEqual(["praxis-test: unknown dependency naming: custom-helper"], errors)

    def test_validate_issue_drafts_accepts_manifest_aligned_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            praxis_skill = write_skill(root, "praxis-test")
            ergon_skill = write_skill(root, "ergon-test")
            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [manifest_entry(root, ergon_skill)])
            write_issue_draft(root, "praxis", "praxis-test")
            write_issue_draft(root, "ergon-migration", "ergon-test")
            write_issue_draft_readme(root, ["praxis-test", "ergon-test"])

            errors = ISSUE_DRAFTS_MODULE.validate_drafts(root, ["praxis", "ergon-migration"])

            self.assertEqual([], errors)

    def test_validate_issue_drafts_reports_missing_and_extra_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            praxis_skill = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [])
            write_issue_draft(root, "praxis", "praxis-extra")
            write_issue_draft_readme(root, ["praxis-extra"])

            errors = ISSUE_DRAFTS_MODULE.validate_drafts(root, ["praxis", "ergon-migration"])

            self.assertIn("Missing skill review drafts: praxis-test", errors)
            self.assertIn("Skill review drafts without manifest entry: praxis-extra", errors)
            self.assertIn("README missing skill review draft links: praxis-test", errors)
            self.assertIn("README links skill review drafts without manifest entry: praxis-extra", errors)

    def test_validate_issue_drafts_reports_stale_draft_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])
            write_manifest(root, "ergon-migration", [])
            write_issue_draft(root, "ergon-migration", "praxis-test")
            write_issue_draft_readme(root, ["praxis-test"])

            errors = ISSUE_DRAFTS_MODULE.validate_drafts(root, ["praxis", "ergon-migration"])

            self.assertTrue(any("missing required text: # Revisar skill praxis: praxis-test" in error for error in errors))
            self.assertTrue(any("missing required text: - Familia: praxis" in error for error in errors))
            self.assertTrue(
                any("missing required text: python3 scripts/audit-praxis-skills.py --family praxis" in error for error in errors)
            )

    def test_validate_issue_drafts_requires_readme_validation_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_root = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])
            write_manifest(root, "ergon-migration", [])
            write_issue_draft(root, "praxis", "praxis-test")

            readme = root / "docs" / "issue-drafts" / "README.md"
            readme.parent.mkdir(parents=True, exist_ok=True)
            readme.write_text("# Skill Review Issue Drafts\n\n- [praxis-test](skill-reviews/praxis-test.md)\n")

            errors = ISSUE_DRAFTS_MODULE.validate_drafts(root, ["praxis", "ergon-migration"])

            self.assertIn(
                f"README missing local validation guidance: {ISSUE_DRAFTS_MODULE.README_VALIDATION_LINE}",
                errors,
            )

    def test_generate_issue_drafts_uses_manifests_and_removes_stale_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            praxis_skill = write_skill(root, "praxis-test")
            ergon_skill = write_skill(root, "ergon-test")
            write_skill(root, "praxis-untracked")
            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [manifest_entry(root, ergon_skill)])

            drafts_root = root / "docs" / "issue-drafts" / "skill-reviews"
            drafts_root.mkdir(parents=True)
            (drafts_root / "stale.md").write_text("stale\n")

            count = GENERATE_DRAFTS_MODULE.generate(
                root,
                "example/repo",
                Path("docs/issue-drafts/skill-reviews"),
                Path("docs/issue-drafts/README.md"),
                ["praxis", "ergon-migration"],
            )

            self.assertEqual(2, count)
            self.assertTrue((drafts_root / "praxis-test.md").is_file())
            self.assertTrue((drafts_root / "ergon-test.md").is_file())
            self.assertFalse((drafts_root / "praxis-untracked.md").exists())
            self.assertFalse((drafts_root / "stale.md").exists())

    def test_generate_issue_drafts_output_passes_issue_draft_validator(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            praxis_skill = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [])

            GENERATE_DRAFTS_MODULE.generate(
                root,
                "example/repo",
                Path("docs/issue-drafts/skill-reviews"),
                Path("docs/issue-drafts/README.md"),
                ["praxis", "ergon-migration"],
            )

            errors = ISSUE_DRAFTS_MODULE.validate_drafts(root, ["praxis", "ergon-migration"])

            self.assertEqual([], errors)

    def test_generate_issue_drafts_classifies_projects_and_risk(self) -> None:
        praxis_ai = {"family": "praxis", "name": "praxis-ai-semantic-intent"}
        metadata = {"family": "praxis", "name": "praxis-metadata-schema-contracts"}
        metadata_editor = {"family": "praxis", "name": "praxis-metadata-editor-ai-validation"}

        self.assertEqual("praxis-ui-angular", GENERATE_DRAFTS_MODULE.canonical_project(praxis_ai))
        self.assertEqual("alto", GENERATE_DRAFTS_MODULE.risk_level(praxis_ai))
        self.assertEqual("praxis-metadata-starter", GENERATE_DRAFTS_MODULE.canonical_project(metadata))
        self.assertEqual("praxis-ui-angular", GENERATE_DRAFTS_MODULE.canonical_project(metadata_editor))
        self.assertIn(
            "## Escopo especifico do piloto",
            GENERATE_DRAFTS_MODULE.draft_body({
                **praxis_ai,
                "path": "codex-skills/praxis-ai-semantic-intent/",
                "description": "Test",
            }),
        )

    def test_generate_issue_drafts_check_accepts_current_generated_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            praxis_skill = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [])
            draft_root = Path("docs/issue-drafts/skill-reviews")
            readme_path = Path("docs/issue-drafts/README.md")

            GENERATE_DRAFTS_MODULE.generate(root, "example/repo", draft_root, readme_path, ["praxis", "ergon-migration"])

            errors = GENERATE_DRAFTS_MODULE.check_generated_outputs(
                root,
                "example/repo",
                draft_root,
                readme_path,
                ["praxis", "ergon-migration"],
            )

            self.assertEqual([], errors)

    def test_generate_issue_drafts_check_reports_stale_and_extra_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            praxis_skill = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, praxis_skill)])
            write_manifest(root, "ergon-migration", [])
            draft_root = Path("docs/issue-drafts/skill-reviews")
            readme_path = Path("docs/issue-drafts/README.md")

            GENERATE_DRAFTS_MODULE.generate(root, "example/repo", draft_root, readme_path, ["praxis", "ergon-migration"])
            (root / draft_root / "praxis-test.md").write_text("stale\n")
            (root / draft_root / "extra.md").write_text("extra\n")

            errors = GENERATE_DRAFTS_MODULE.check_generated_outputs(
                root,
                "example/repo",
                draft_root,
                readme_path,
                ["praxis", "ergon-migration"],
            )

            self.assertIn("Generated file is stale: docs/issue-drafts/skill-reviews/praxis-test.md", errors)
            self.assertIn("Stale generated draft: docs/issue-drafts/skill-reviews/extra.md", errors)

    def test_generate_issue_drafts_uses_validator_readme_guidance(self) -> None:
        self.assertEqual(
            ISSUE_DRAFTS_README_VALIDATION_LINE,
            GENERATE_DRAFTS_MODULE.README_VALIDATION_LINE,
        )
        self.assertEqual(ISSUE_DRAFTS_README_VALIDATION_LINE, ISSUE_DRAFTS_MODULE.README_VALIDATION_LINE)

    def test_create_issue_payloads_reads_titles_in_stable_order_with_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            draft_root = root / "drafts"
            draft_root.mkdir()
            (draft_root / "b.md").write_text("# Title B\n\n- Familia: praxis\n\nBody B\n")
            (draft_root / "a.md").write_text("# Title A\n\n- Familia: ergon-migration\n\nBody A\n")

            payloads = CREATE_ISSUES_MODULE.issue_payloads(draft_root, limit=1)

            self.assertEqual(1, len(payloads))
            self.assertEqual("Title A", payloads[0]["title"])
            self.assertEqual("ergon-migration", payloads[0]["family"])
            self.assertEqual((draft_root / "a.md").as_posix(), payloads[0]["path"])

    def test_create_issue_payloads_requires_h1_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft_root = Path(tmp) / "drafts"
            draft_root.mkdir()
            (draft_root / "missing-title.md").write_text("No title\n")

            with self.assertRaisesRegex(RuntimeError, "Draft has no H1 title"):
                CREATE_ISSUES_MODULE.issue_payloads(draft_root)

    def test_create_issue_payloads_requires_family(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            draft_root = Path(tmp) / "drafts"
            draft_root.mkdir()
            (draft_root / "missing-family.md").write_text("# Title\n\nNo family\n")

            with self.assertRaisesRegex(RuntimeError, "Draft has no Familia field"):
                CREATE_ISSUES_MODULE.issue_payloads(draft_root)

    def test_create_issue_labels_include_defaults_and_extra_labels(self) -> None:
        payload = {"title": "Review A", "body": "A", "path": "a.md", "family": "praxis"}

        labels = CREATE_ISSUES_MODULE.issue_labels(payload, ["roadmap", "praxis"], True)

        self.assertEqual(["skill-review", "praxis", "roadmap"], labels)

    def test_create_issue_labels_can_disable_defaults(self) -> None:
        payload = {"title": "Review A", "body": "A", "path": "a.md", "family": "praxis"}

        labels = CREATE_ISSUES_MODULE.issue_labels(payload, ["roadmap"], False)

        self.assertEqual(["roadmap"], labels)

    def test_create_issue_duplicate_reports_match_titles(self) -> None:
        payloads = [
            {"title": "Review A", "body": "A", "path": "a.md"},
            {"title": "Review B", "body": "B", "path": "b.md"},
        ]
        issues = [
            {"number": 10, "title": "Review B", "url": "https://example.test/issues/10", "state": "OPEN"},
            {"number": 11, "title": "Other", "url": "https://example.test/issues/11", "state": "CLOSED"},
        ]

        reports = CREATE_ISSUES_MODULE.duplicate_issue_reports(payloads, issues)

        self.assertEqual(["Review B already exists as #10 (OPEN): https://example.test/issues/10"], reports)

    def test_create_issue_missing_payloads_excludes_existing_titles(self) -> None:
        payloads = [
            {"title": "Review A", "body": "A", "path": "a.md"},
            {"title": "Review B", "body": "B", "path": "b.md"},
            {"title": "Review C", "body": "C", "path": "c.md"},
        ]
        issues = [
            {"number": 10, "title": "Review B", "url": "https://example.test/issues/10", "state": "CLOSED"},
        ]

        missing = CREATE_ISSUES_MODULE.missing_payloads(payloads, issues)

        self.assertEqual(["Review A", "Review C"], [payload["title"] for payload in missing])

    def test_create_issue_coverage_reports_found_and_missing(self) -> None:
        payloads = [
            {"title": "Review A", "body": "A", "path": "a.md"},
            {"title": "Review B", "body": "B", "path": "b.md"},
        ]
        issues = [
            {"number": 10, "title": "Review B", "url": "https://example.test/issues/10", "state": "OPEN"},
        ]

        rows = CREATE_ISSUES_MODULE.issue_coverage_rows(payloads, issues)

        self.assertEqual("MISSING", rows[0]["status"])
        self.assertEqual("FOUND", rows[1]["status"])
        self.assertEqual("10", rows[1]["number"])

        output = io.StringIO()
        with redirect_stdout(output):
            CREATE_ISSUES_MODULE.print_issue_coverage(rows)

        self.assertIn("MISSING\t-\t-\tReview A\ta.md", output.getvalue())
        self.assertIn("FOUND\t#10\tOPEN\tReview B\thttps://example.test/issues/10", output.getvalue())
        self.assertIn("Summary: total=2 found=1 missing=1", output.getvalue())

    def test_preflight_audit_policy_allows_informational_counters(self) -> None:
        report = audit_report(installedOnly=3, sourceInOtherFamilyManifest=2)

        with redirect_stdout(io.StringIO()):
            PREFLIGHT_MODULE.assert_audit_clean("praxis", report)

    def test_preflight_audit_policy_fails_on_real_audit_problems(self) -> None:
        for key in ("drift", "missing", "sourceInvalid", "sourceNotInManifest"):
            with self.subTest(key=key):
                with self.assertRaisesRegex(RuntimeError, "audit is not clean"):
                    PREFLIGHT_MODULE.assert_audit_clean("praxis", audit_report(**{key: 1}))

    def test_sync_installs_skill_and_metadata_into_temporary_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "installed-skills"
            skill_root = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])
            write_manifest(root, "ergon-migration", [])

            result = run_sync(sync_args(root, skills_root))

            installed = skills_root / "praxis-test"
            metadata = json.loads((installed / ".codex-skill-install.json").read_text())
            self.assertEqual(0, result)
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertEqual("praxis", metadata["family"])
            self.assertEqual("praxis-test", metadata["skill"])
            self.assertEqual(skill_tree_hash(skill_root), metadata["sourceHash"])
            self.assertIn("installedAt", metadata)

    def test_sync_blocks_destination_drift_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "installed-skills"
            skill_root = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])
            write_manifest(root, "ergon-migration", [])

            self.assertEqual(0, run_sync(sync_args(root, skills_root)))
            (skills_root / "praxis-test" / "SKILL.md").write_text("local drift\n")

            with self.assertRaisesRegex(RuntimeError, "Sync blocked"):
                run_sync(sync_args(root, skills_root))

            self.assertEqual("local drift\n", (skills_root / "praxis-test" / "SKILL.md").read_text())

    def test_audit_reports_destination_drift_without_failing_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "installed-skills"
            skill_root = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])
            write_manifest(root, "ergon-migration", [])
            self.assertEqual(0, run_sync(sync_args(root, skills_root)))
            (skills_root / "praxis-test" / "SKILL.md").write_text("local drift\n")

            with redirect_stdout(io.StringIO()):
                result = AUDIT_MODULE.audit(audit_args(root, skills_root))

            self.assertEqual(0, result)

    def test_audit_fail_on_drift_returns_nonzero_for_destination_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "installed-skills"
            skill_root = write_skill(root, "praxis-test")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])
            write_manifest(root, "ergon-migration", [])
            self.assertEqual(0, run_sync(sync_args(root, skills_root)))
            (skills_root / "praxis-test" / "SKILL.md").write_text("local drift\n")

            with redirect_stdout(io.StringIO()):
                result = AUDIT_MODULE.audit(audit_args(root, skills_root, fail_on_drift=True))

            self.assertEqual(1, result)

    def test_sync_force_converges_removed_files_without_touching_other_skill_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skills_root = root / "installed-skills"
            skill_root = write_skill(root, "praxis-test")
            stale_source = skill_root / "references" / "obsolete.md"
            stale_source.parent.mkdir()
            stale_source.write_text("version one\n")
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])
            other_skill = write_skill(root, "ergon-test")
            write_manifest(root, "ergon-migration", [manifest_entry(root, other_skill)])

            self.assertEqual(0, run_sync(sync_args(root, skills_root)))
            installed = skills_root / "praxis-test"
            (installed / "SKILL.md").write_text("local drift\n")
            self.assertTrue((installed / "references" / "obsolete.md").is_file())
            installed_only = skills_root / "installed-only"
            installed_only.mkdir()
            (installed_only / "local.md").write_text("keep me\n")
            other_installed = skills_root / "ergon-test"
            other_installed.mkdir()
            (other_installed / "SKILL.md").write_text("other family\n")

            stale_source.unlink()
            stale_source.parent.rmdir()
            write_manifest(root, "praxis", [manifest_entry(root, skill_root)])

            dry_run_output = io.StringIO()
            with redirect_stdout(dry_run_output):
                self.assertEqual(0, SYNC_MODULE.sync(sync_args(root, skills_root, force=True, dry_run=True)))

            self.assertIn("DRY-RUN remove extra file within managed skill", dry_run_output.getvalue())
            self.assertTrue((installed / "references" / "obsolete.md").exists())

            sync_output = io.StringIO()
            with redirect_stdout(sync_output):
                result = SYNC_MODULE.sync(sync_args(root, skills_root, force=True))

            self.assertEqual(0, result)
            self.assertIn("Removed extra file within managed skill", sync_output.getvalue())
            self.assertEqual((skill_root / "SKILL.md").read_text(), (installed / "SKILL.md").read_text())
            self.assertFalse((installed / "references" / "obsolete.md").exists())
            self.assertFalse((installed / "references").exists())
            self.assertEqual("keep me\n", (installed_only / "local.md").read_text())
            self.assertEqual("other family\n", (other_installed / "SKILL.md").read_text())

            report_output = io.StringIO()
            with redirect_stdout(report_output):
                self.assertEqual(0, AUDIT_MODULE.audit(audit_args(root, skills_root)))
            report = json.loads(report_output.getvalue())
            self.assertEqual(0, report["summary"]["drift"])


if __name__ == "__main__":
    unittest.main()
