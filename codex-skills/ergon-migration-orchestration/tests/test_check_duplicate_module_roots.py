import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_duplicate_module_roots.py"


def write_pom(path: Path, artifact_id: str) -> None:
    path.write_text(
        f"""<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>example</groupId>
  <artifactId>{artifact_id}</artifactId>
  <version>1.0.0</version>
</project>
""",
        encoding="utf-8",
    )


class DuplicateModuleRootGuardTests(unittest.TestCase):
    def test_blocks_duplicate_migracao_package_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            canonical = base / "migracao" / "ms-administracao-pessoal"
            package = base / "migracao-package" / "ms-administracao-pessoal"
            canonical.mkdir(parents=True)
            package.mkdir(parents=True)
            (base / "migracao" / ".git").mkdir()
            write_pom(canonical / "pom.xml", "ms-administracao-pessoal")
            write_pom(package / "pom.xml", "ms-administracao-pessoal")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--workspace-root",
                    str(base / "migracao"),
                    "--module",
                    "ms-administracao-pessoal",
                    "--current-root",
                    str(package),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("MIGRATION_MODULE_ROOT_GUARD_BLOCKED", result.stderr)
            self.assertIn("migracao/ms-administracao-pessoal", result.stderr)
            self.assertIn("migracao-package/ms-administracao-pessoal", result.stderr)
            self.assertIn("current root is not inside the canonical module root", result.stderr)
            self.assertNotIn("Authorization", result.stderr)
            self.assertNotIn("Cookie", result.stderr)

    def test_allows_single_canonical_git_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            canonical = base / "migracao" / "ms-administracao-pessoal"
            canonical.mkdir(parents=True)
            (base / "migracao" / ".git").mkdir()
            write_pom(canonical / "pom.xml", "ms-administracao-pessoal")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--workspace-root",
                    str(base / "migracao"),
                    "--module",
                    "ms-administracao-pessoal",
                    "--current-root",
                    str(canonical),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("MIGRATION_MODULE_ROOT_GUARD_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
