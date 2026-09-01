from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCREEN_DISCOVERY = ROOT / "ergon-archon-screen-discovery" / "SKILL.md"
RULE_ORCHESTRATION = ROOT / "ergon-rule-migration-orchestration" / "SKILL.md"


class CustomerCustomizationPromptContractTest(unittest.TestCase):
    def test_short_write_prompt_is_owned_by_rule_orchestration(self):
        screen = SCREEN_DISCOVERY.read_text(encoding="utf-8")
        rules = RULE_ORCHESTRATION.read_text(encoding="utf-8")

        self.assertIn("active customer customizations or business rules on a write operation belong to", screen)
        self.assertIn("must use that skill before issuing", screen)
        self.assertIn("do not finish the request inside screen", screen)
        self.assertIn("active customer customizations or business rules in a screen's write flow", rules)
        self.assertIn("routing is mandatory", rules)

    def test_explicit_ui_rule_remains_distinct(self):
        screen = SCREEN_DISCOVERY.read_text(encoding="utf-8")
        rules = RULE_ORCHESTRATION.read_text(encoding="utf-8")

        self.assertIn("client-side screen rule", screen)
        self.assertIn("unless the user explicitly asks for a\nclient-side/UI rule", rules)
        self.assertIn("never use them\nas a substitute", rules)


if __name__ == "__main__":
    unittest.main()
