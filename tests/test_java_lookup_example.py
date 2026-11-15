"""Run with JAVA_HOME and PRAXIS_METADATA_CLASSPATH for the Java snippet gate.

Unconfigured discovery skips these artifact-dependent cases, which does not close
the gate. The direct check-java-lookup-example.py command requires both inputs.
"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
GUIDE = REPO / 'codex-skills/praxis-java-host-project/references/resource-baseline.md'


@unittest.skipUnless(os.environ.get('JAVA_HOME') and os.environ.get('PRAXIS_METADATA_CLASSPATH'),
                     'Requires JAVA_HOME and PRAXIS_METADATA_CLASSPATH; gate is not validated by a skip')
class JavaLookupExampleTest(unittest.TestCase):
    def run_guide(self, content):
        with tempfile.TemporaryDirectory() as temp:
            guide = Path(temp) / 'guide.md'
            guide.write_text(content, encoding='utf-8')
            return subprocess.run([sys.executable, str(REPO / 'scripts/check-java-lookup-example.py'),
                                   '--java-home', os.environ['JAVA_HOME'],
                                   '--classpath', os.environ['PRAXIS_METADATA_CLASSPATH'],
                                   '--guide', str(guide)], capture_output=True, text=True)

    def test_canonical_snippets_compile_and_preserve_contract(self):
        result = self.run_guide(GUIDE.read_text(encoding='utf-8'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('descriptor contract verified', result.stdout)

    def test_original_constructor_mismatch_is_rejected(self):
        content = GUIDE.read_text(encoding='utf-8')
        before = 'new LookupSortOption("name-asc", "name", "asc", "Name (A-Z)")'
        self.assertEqual(content.count(before), 1)
        result = self.run_guide(content.replace(before, 'new LookupSortOption("name,asc", "Name (A-Z)")'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('LookupSortOption', result.stderr)

    def test_type_correct_but_wrong_field_binding_is_rejected(self):
        content = GUIDE.read_text(encoding='utf-8')
        before = '"human-resources.positions",\n            "code",'
        self.assertEqual(content.count(before), 1)
        result = self.run_guide(content.replace(before, '"human-resources.positions",\n            "id",'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('AssertionError: code field', result.stderr)


if __name__ == '__main__':
    unittest.main()
