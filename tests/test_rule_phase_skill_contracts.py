import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "codex-skills"
READINESS = "part2-foundation-readiness-v2.json"


class RulePhaseSkillContractsTest(unittest.TestCase):
    def test_orchestrator_reads_readiness_before_workflow(self) -> None:
        text = (SKILLS / "ergon-rule-migration-orchestration" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        readiness_index = text.index("## Mandatory Readiness First")
        workflow_index = text.index("## Workflow")
        self.assertLess(readiness_index, workflow_index)
        self.assertIn(READINESS, text)
        self.assertIn("exact requested stage/action", text)
        self.assertIn("corporateReadinessStatus", text)

    def test_specialized_skills_are_manifested_with_boundaries(self) -> None:
        manifest = json.loads(
            (SKILLS / "ergon-migration-skills.manifest.json").read_text(encoding="utf-8")
        )
        entries = {item["name"]: item for item in manifest["skills"]}
        required = {
            "ergon-rule-target-planning": ["MATERIALIZED_UNCHECKED", "Never create JSON Logic expressions"],
            "ergon-rule-executor-selection": ["KEEP_DB_BACKED", "do not implement it"],
            "ergon-rule-shadow-parity": ["shadow cannot decide", "Shadow Passed"],
            "ergon-rule-legacy-containment": ["Phase 16 promotion decision", "Do not use `BYPASS_ALL`"],
        }
        for name, markers in required.items():
            self.assertIn(name, entries)
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(READINESS, text)
            for marker in markers:
                self.assertIn(marker, text)

        orchestrator_dependencies = set(entries["ergon-rule-migration-orchestration"]["dependencies"])
        self.assertTrue(set(required).issubset(orchestrator_dependencies))

    def test_new_skills_have_forward_test_references(self) -> None:
        names = (
            "ergon-rule-target-planning",
            "ergon-rule-executor-selection",
            "ergon-rule-shadow-parity",
            "ergon-rule-legacy-containment",
        )
        for name in names:
            references = list((SKILLS / name / "references").glob("*.md"))
            self.assertEqual(1, len(references), name)
            self.assertIn("Forward Test", references[0].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
