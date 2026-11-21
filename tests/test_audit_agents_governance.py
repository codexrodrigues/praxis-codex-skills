import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit-agents-governance.py"
SPEC = importlib.util.spec_from_file_location("audit_agents_governance", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class AuditAgentsGovernanceTests(unittest.TestCase):
    def test_clean_file_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "AGENTS.md"
            p.write_text("# AGENTS\n\nTexto válido em UTF-8.\n", encoding="utf-8")
            findings = MOD.audit_agents_file(p, is_root=True)
            self.assertEqual(findings, [])

    def test_detects_size_mojibake_and_legacy_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "AGENTS.md"
            p.write_text("Se\u00c3\u00a7\u00c3\u00a3o com praxis-rules-studio\n" + ("x" * 20000), encoding="utf-8")
            findings = MOD.audit_agents_file(p, is_root=True)
            codes = {item["code"] for item in findings}
            self.assertIn("size-budget-exceeded", codes)
            self.assertIn("utf8-mojibake", codes)
            self.assertIn("legacy-studio-name", codes)


if __name__ == "__main__":
    unittest.main()
