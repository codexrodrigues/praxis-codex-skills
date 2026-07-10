from __future__ import annotations

import argparse
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

from codex_skills_common import load_manifest, sha256_file, skill_tree_hash  # noqa: E402


def load_script_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load script module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT_MODULE = load_script_module("audit_praxis_skills", SCRIPTS_ROOT / "audit-praxis-skills.py")


def write_skill(root: Path, name: str) -> Path:
    skill_root = root / "codex-skills" / name
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Test skill {name}.\n---\n\n# {name}\n"
    )
    return skill_root


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


class PythonSkillScriptTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
