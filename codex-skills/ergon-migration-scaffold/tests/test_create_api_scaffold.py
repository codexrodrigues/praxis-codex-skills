from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "create_api_scaffold.py"
MILESTONE_SCRIPT = Path(__file__).parents[1] / "scripts" / "record_factory_milestone.py"


class CreateApiScaffoldTest(unittest.TestCase):
    def test_creates_conservative_read_write_packet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "packet"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--screen",
                    "ERGadm00033",
                    "--resource-key",
                    "administracao-pessoal.tipos-frequencia",
                    "--base-path",
                    "/api/administracao-pessoal/tipos-frequencia",
                    "--output",
                    str(output),
                    "--operations",
                    "list,detail,create,cancel",
                    "--started-at",
                    "2026-07-11T12:00:00Z",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads((output / "scaffold-manifest.json").read_text())
            self.assertEqual(manifest["resourceKey"], "administracao-pessoal.tipos-frequencia")
            self.assertEqual(manifest["basePath"], "/api/administracao-pessoal/tipos-frequencia")
            self.assertEqual(manifest["operations"], ["list", "detail", "create", "cancel"])
            timing = json.loads((output / "factory-timing.json").read_text())
            self.assertEqual(timing["startedAtUtc"], "2026-07-11T12:00:00Z")
            inventory = (output / "operation-inventory.md").read_text()
            self.assertIn("READ_EVIDENCE_REQUIRED", inventory)
            self.assertIn("/api/administracao-pessoal/tipos-frequencia/{id}", inventory)
            self.assertIn("WRITE_ROUTE_REQUIRED", inventory)
            self.assertIn("NO_MUTATION_PROOF_REQUIRED", inventory)

            milestone = subprocess.run(
                [
                    sys.executable,
                    str(MILESTONE_SCRIPT),
                    "--packet",
                    str(output),
                    "--milestone",
                    "first-endpoint-executed",
                    "--outcome",
                    "passed",
                    "--evidence",
                    "api-results/filter-smoke.json",
                    "--at",
                    "2026-07-11T12:17:30Z",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(milestone.returncode, 0, milestone.stderr)
            timing = json.loads((output / "factory-timing.json").read_text())
            self.assertEqual(timing["milestones"][-1]["elapsedMinutes"], 17.5)

    def test_refuses_unknown_operation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--screen",
                    "ERGadm00033",
                    "--resource-key",
                    "tipo-frequencia",
                    "--base-path",
                    "/api/administracao-pessoal/tipos-frequencia",
                    "--output",
                    str(Path(directory) / "packet"),
                    "--operations",
                    "list,approve",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown operations", result.stderr)
