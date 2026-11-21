import importlib.util
import tempfile
import unittest
from pathlib import Path

WORKSPACE_SCRIPTS = Path(__file__).resolve().parent


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, WORKSPACE_SCRIPTS / filename)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PURITY = _load("audit_public_repo_purity", "audit-public-repo-purity.py")
ANGULAR = _load("audit_angular_host_completeness", "audit-angular-host-completeness.py")


class PublicRepoPurityTests(unittest.TestCase):
    def test_clean_public_repo_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Clean\n\nSee [Guide](docs/guide.md).\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            leaks, broken = PURITY.audit_repository(root)
            self.assertEqual(leaks, [])
            self.assertEqual(broken, [])

    def test_detects_leaks_and_broken_links_and_sanitizes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "Legacy Ergon ref + praxis-rules-studio + [Missing](docs/missing.md)\n"
                "Path C:/Users/dev/project and ep-xyz-123.us-east-1.aws.neon.tech\n",
                encoding="utf-8",
            )
            leaks, broken = PURITY.audit_repository(root)
            leak_codes = {item["code"] for item in leaks}
            self.assertIn("legacy-domain-term", leak_codes)
            self.assertIn("legacy-studio-name", leak_codes)
            self.assertIn("local-machine-path", leak_codes)
            self.assertIn("neon-project-or-endpoint-id", leak_codes)
            self.assertEqual(len(broken), 1)

            ev = root / "evidence.log"
            ev.write_text("Running at D:/Developer/secret on ep-abc.us-east-1.aws.neon.tech", encoding="utf-8")
            changed = PURITY.sanitize_evidence_path(ev)
            self.assertEqual(changed, 1)
            sanitized = ev.read_text(encoding="utf-8")
            self.assertNotIn("D:/Developer", sanitized)
            self.assertNotIn("aws.neon.tech", sanitized)

    def test_self_definition_negative_rule_docs_and_dual_family_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts" / "workspace").mkdir(parents=True)
            (root / "scripts" / "workspace" / "audit-public-repo-purity.py").write_text(
                (WORKSPACE_SCRIPTS / "audit-public-repo-purity.py").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (root / "docs" / "platform-governance").mkdir(parents=True)
            (root / "docs" / "platform-governance" / "workspace-root-AGENTS.md").write_text(
                "Proibido mencionar Ergon fora dos showcases privados e antigo ep-real-999.us-east-1.aws.neon.tech\n",
                encoding="utf-8",
            )
            (root / "codex-skills" / "ergon-demo").mkdir(parents=True)
            (root / "codex-skills" / "praxis-demo").mkdir(parents=True)
            (root / "codex-skills" / "ergon-migration-skills.manifest.json").write_text("{}\n", encoding="utf-8")
            (root / "codex-skills" / "ergon-demo" / "SKILL.md").write_text(
                "Legacy Ergon guidance only.\n",
                encoding="utf-8",
            )
            (root / "codex-skills" / "praxis-demo" / "SKILL.md").write_text(
                "Leaked Ergon guidance.\n",
                encoding="utf-8",
            )
            leaks, broken = PURITY.audit_repository(root)
            self.assertEqual(broken, [])
            leak_pairs = {(item["file"], item["code"]) for item in leaks}
            self.assertEqual(
                leak_pairs,
                {
                    ("docs/platform-governance/workspace-root-AGENTS.md", "neon-project-or-endpoint-id"),
                    ("codex-skills/praxis-demo/SKILL.md", "legacy-domain-term"),
                },
            )

    def test_synthetic_fixtures_cross_repo_and_skill_root_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text(
                "See [Sibling](../../praxis-ui-angular/README.md) and [Missing](missing.md) and [Sec](#pt-br-and-terminology).\n",
                encoding="utf-8",
            )
            (root / "src").mkdir()
            (root / "src" / "SampleTest.java").write_text(
                'String a = "PCK_TEST"; String b = "PCK_SAMPLE"; String c = "PCK_DEPENDENTES";\n'
                'String n1 = "br-isolated-123456"; String n2 = "ep-example-pooler.c-2.us-east-1.aws.neon.tech";\n'
                'String n3 = "br-twilight-breeze-adq1cqaq";\n',
                encoding="utf-8",
            )
            skill_refs = root / "codex-skills" / "praxis-sample" / "references"
            skill_refs.mkdir(parents=True)
            (root / "codex-skills" / "praxis-sample" / "SKILL.md").write_text("# Sample\n", encoding="utf-8")
            (skill_refs / "matrix.md").write_text("# Matrix\n", encoding="utf-8")
            (skill_refs / "guide.md").write_text("See [Matrix](references/matrix.md).\n", encoding="utf-8")

            leaks, broken = PURITY.audit_repository(root)
            self.assertEqual(len(broken), 1)
            self.assertEqual(broken[0]["file"], "docs/guide.md")
            leak_pairs = {(item["file"], item["code"]) for item in leaks}
            self.assertEqual(
                leak_pairs,
                {
                    ("src/SampleTest.java", "legacy-ergon-identifier"),
                    ("src/SampleTest.java", "neon-project-or-endpoint-id"),
                },
            )
            self.assertEqual(len(leaks), 2)


class AngularHostCompletenessTests(unittest.TestCase):
    def test_complete_host_passes_10_checks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src" / "app"
            src.mkdir(parents=True)
            providers = "\n".join(f"providePraxisWidget{i}Metadata()" for i in range(16))
            (src / "app.config.ts").write_text(
                f"""
                API_URL, PAX_FETCH_HEADERS, withInterceptors([praxisFetchHeadersInterceptor]),
                withPraxisHttpLoading(), providePraxisDynamicFieldsCore(), providePraxisHttpCollectionExport(),
                providePraxisQuickViewDialogPresenter(), providePraxisSurfaceDrawerBridge(),
                providePraxisSurfaceGlobalActions(), providePraxisSettingsPanelBridge(),
                {providers}
                ApiConfigStorage, API_CONFIG_STORAGE_OPTIONS, openGlobalConfigEditor,
                EnterpriseRuntimeContextService, 'X-Tenant-ID', 'X-Organization-ID',
                providePraxisRelatedResourceOutletMetadata(), providePraxisAnalyticalDrawerSchemas(),
                providePraxisCharts(), PraxisAnalyticsPresentationComponent, PraxisChartComponent,
                microVisualization, DynamicPageBuilderComponent, PraxisPageSaveAsComponent,
                PraxisPageCopyActionComponent, UiLayoutLifecycleService, ':pageId',
                AI_BACKEND_STORAGE_OPTIONS
                """,
                encoding="utf-8",
            )
            (src / "routes.ts").write_text(
                "export const R = [{ resourcePath: 'api/a' }, { resourcePath: 'api/b' }];",
                encoding="utf-8",
            )
            checks, routes = ANGULAR.evaluate_host(Path(tmp), expected_routes=2)
            self.assertEqual(routes, 2)
            self.assertTrue(all(c["passed"] for c in checks), checks)

    def test_custom_surface_opener_and_low_routes_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src" / "app"
            src.mkdir(parents=True)
            (src / "custom-surface-open.service.ts").write_text(
                "export class CustomSurfaceOpenService {}\n",
                encoding="utf-8",
            )
            checks, routes = ANGULAR.evaluate_host(Path(tmp), expected_routes=5)
            self.assertEqual(routes, 0)
            by_id = {c["id"]: c for c in checks}
            self.assertFalse(by_id[2]["passed"])
            self.assertFalse(by_id[6]["passed"])


if __name__ == "__main__":
    unittest.main()
