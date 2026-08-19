import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "classify_hades_activation.py"
SPEC = importlib.util.spec_from_file_location("classify_hades_activation", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class HadesActivationClassificationTest(unittest.TestCase):
    def test_direct_parent_is_active_independently_of_multi_ep_flag(self):
        self.assertEqual("DIRECT_ACTIVE", MODULE.classify("S", "N", True, 0))

    def test_unreachable_child_does_not_activate_disabled_parent(self):
        self.assertEqual("NO_CHAIN", MODULE.classify("N", "N", True, 1))

    def test_multi_parent_requires_an_enabled_child(self):
        self.assertEqual("MULTI_ENABLED_NO_ACTIVE_CHILD", MODULE.classify("N", "S", True, 0))
        self.assertEqual("MULTI_ACTIVE", MODULE.classify("N", "S", True, 1))

    def test_enabled_flag_does_not_invent_a_missing_route(self):
        self.assertEqual(
            "DIRECT_ENABLED_ROUTE_UNRESOLVED",
            MODULE.classify("S", "N", False, 0),
        )


if __name__ == "__main__":
    unittest.main()
