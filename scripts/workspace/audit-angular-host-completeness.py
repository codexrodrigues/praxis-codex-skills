#!/usr/bin/env python3
"""Audit an Angular host against the 12 Canonical Pillars (10 Checks) of AI-ANGULAR-HOST-BLUEPRINT.md."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

IGNORED_DIRS = {".git", "node_modules", "dist", "target", ".angular", ".local-praxis", "coverage", "e2e", "test-e2e"}
SOURCE_EXTENSIONS = {".ts", ".html"}

METADATA_PROVIDER_RE = re.compile(r"\bprovidePraxis[A-Za-z0-9_]*Metadata\s*\(")
CUSTOM_OPENER_RE = re.compile(r"\b(?:class|interface|export\s+(?:const|class|function))\s+[A-Za-z0-9_]*SurfaceOpenService\b")
RESOURCE_ROUTE_RE = re.compile(r"resourcePath\s*:\s*['\"][^'\"]+['\"]|component\s*:\s*PraxisResourcePage(?:Component)?\b|<praxis-crud\b")


def _collect_source_texts(host_root: Path) -> list[tuple[str, str]]:
    """Collect non-test Angular source files (.ts, .html) under src/ (or host_root)."""
    search_root = (host_root / "src") if (host_root / "src").is_dir() else host_root
    entries: list[tuple[str, str]] = []
    for root_str, dirnames, filenames in os.walk(search_root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        for name in sorted(filenames):
            p = Path(root_str) / name
            if p.suffix.lower() not in SOURCE_EXTENSIONS or name.endswith(".spec.ts"):
                continue
            try:
                entries.append((p.relative_to(host_root).as_posix(), p.read_text(encoding="utf-8")))
            except (OSError, UnicodeDecodeError):
                continue
    return entries


def _has_any(corpus: str, *tokens: str) -> bool:
    return any(tok in corpus for tok in tokens)


def evaluate_host(host_root: Path, *, expected_routes: int | None = None) -> tuple[list[dict[str, object]], int]:
    """Evaluate all 10 blueprint checks on host_root and return (results, discovered_routes)."""
    files = _collect_source_texts(host_root)
    corpus = "\n".join(text for _, text in files)

    checks: list[dict[str, object]] = []

    # Check 1 — Bootstrap Core (Pilar 1)
    missing_c1 = [
        label
        for label, ok in (
            ("API_URL", _has_any(corpus, "API_URL")),
            ("PAX_FETCH_HEADERS", _has_any(corpus, "PAX_FETCH_HEADERS")),
            ("HTTP header interceptor", _has_any(corpus, "withInterceptors", "praxisFetchHeadersInterceptor")),
            ("withPraxisHttpLoading", _has_any(corpus, "withPraxisHttpLoading")),
            ("providePraxisDynamicFieldsCore", _has_any(corpus, "providePraxisDynamicFieldsCore")),
            ("providePraxisHttpCollectionExport", _has_any(corpus, "providePraxisHttpCollectionExport", "providePraxisHttpCollectionExportProvider")),
        )
        if not ok
    ]
    checks.append({"id": 1, "name": "Bootstrap Core (Pilar 1)", "passed": not missing_c1, "detail": "ok" if not missing_c1 else f"missing: {', '.join(missing_c1)}"})

    # Check 2 — Bridges 360 & Zero Custom Surface Openers (Pilar 2)
    missing_c2 = [
        label
        for label, ok in (
            ("providePraxisQuickViewDialogPresenter", _has_any(corpus, "providePraxisQuickViewDialogPresenter")),
            ("providePraxisSurfaceDrawerBridge", _has_any(corpus, "providePraxisSurfaceDrawerBridge")),
            ("providePraxisSurfaceGlobalActions", _has_any(corpus, "providePraxisSurfaceGlobalActions")),
            ("providePraxisSettingsPanelBridge", _has_any(corpus, "providePraxisSettingsPanelBridge")),
        )
        if not ok
    ]
    custom_openers = [rel for rel, txt in files if CUSTOM_OPENER_RE.search(txt)]
    c2_ok = (not missing_c2) and (not custom_openers)
    c2_detail = "ok"
    if missing_c2:
        c2_detail = f"missing: {', '.join(missing_c2)}"
    if custom_openers:
        c2_detail = f"{c2_detail}; custom *SurfaceOpenService in: {', '.join(custom_openers)}".lstrip("; ")
    checks.append({"id": 2, "name": "Bridges 360 & Zero Custom Surface Openers (Pilar 2)", "passed": c2_ok, "detail": c2_detail})

    # Check 3 — Catálogo de Metadados de Widgets (Pilar 3)
    metadata_providers = sorted(set(METADATA_PROVIDER_RE.findall(corpus)))
    c3_ok = len(metadata_providers) >= 15
    checks.append({"id": 3, "name": "Catalogo de Metadados de Widgets (Pilar 3)", "passed": c3_ok, "detail": f"{len(metadata_providers)} metadata providers (min 15)"})

    # Check 4 — Global Config & Remote Storage (Pilar 4)
    missing_c4 = [
        label
        for label, ok in (
            ("ApiConfigStorage/ASYNC_CONFIG_STORAGE", _has_any(corpus, "ApiConfigStorage", "ASYNC_CONFIG_STORAGE")),
            ("API_CONFIG_STORAGE_OPTIONS", _has_any(corpus, "API_CONFIG_STORAGE_OPTIONS")),
            ("openGlobalConfigEditor", _has_any(corpus, "openGlobalConfigEditor")),
        )
        if not ok
    ]
    checks.append({"id": 4, "name": "Global Config & Remote Storage (Pilar 4)", "passed": not missing_c4, "detail": "ok" if not missing_c4 else f"missing: {', '.join(missing_c4)}"})

    # Check 5 — Context Switcher Multi-Tenant / Multi-Organização (Pilar 5)
    missing_c5 = [
        label
        for label, ok in (
            ("EnterpriseRuntimeContextService/CORPORATE_RUNTIME_AUTHORITY_PROVIDERS", _has_any(corpus, "EnterpriseRuntimeContextService", "CORPORATE_RUNTIME_AUTHORITY_PROVIDERS")),
            ("X-Tenant-ID/X-Organization-ID", _has_any(corpus, "X-Tenant-ID", "X-Organization-Id", "X-Organization-ID")),
        )
        if not ok
    ]
    checks.append({"id": 5, "name": "Context Switcher Multi-Tenant / Multi-Org (Pilar 5)", "passed": not missing_c5, "detail": "ok" if not missing_c5 else f"missing: {', '.join(missing_c5)}"})

    # Check 6 — Rotas Declarativas CRUD (Pilar 6)
    resource_paths = set(re.findall(r"resourcePath\s*:\s*['\"]([^'\"]+)['\"]", corpus))
    discovered_routes = len(resource_paths) if resource_paths else len(RESOURCE_ROUTE_RE.findall(corpus))
    if expected_routes is not None:
        c6_ok = discovered_routes >= expected_routes
        c6_detail = f"{discovered_routes} rotas descobertas (esperado >= {expected_routes})"
    else:
        c6_ok = discovered_routes > 0
        c6_detail = f"{discovered_routes} rotas descobertas"
    checks.append({"id": 6, "name": "Rotas Declarativas CRUD (Pilar 6)", "passed": c6_ok, "detail": c6_detail})

    # Check 7 — Dossiê Master-Detail 1:N (Pilares 7 e 8)
    missing_c7 = [
        label
        for label, ok in (
            ("RelatedResourceOutlet", _has_any(corpus, "praxis-related-resource-outlet", "PraxisRelatedResourceOutletComponent", "providePraxisRelatedResourceOutletMetadata")),
            ("AnalyticalDrawerSchemas", _has_any(corpus, "providePraxisAnalyticalDrawerSchemas", "PraxisAnalyticalDrawerSchema")),
        )
        if not ok
    ]
    checks.append({"id": 7, "name": "Dossie Master-Detail 1:N (Pilares 7 e 8)", "passed": not missing_c7, "detail": "ok" if not missing_c7 else f"missing: {', '.join(missing_c7)}"})

    # Check 8 — Cockpits Analíticos e Micro-Visualizações (Pilar 11)
    missing_c8 = [
        label
        for label, ok in (
            ("providePraxisCharts", _has_any(corpus, "providePraxisCharts")),
            ("PraxisAnalyticsPresentation", _has_any(corpus, "PraxisAnalyticsPresentationComponent", "praxis-analytics-presentation")),
            ("PraxisChart", _has_any(corpus, "PraxisChartComponent", "praxis-chart")),
            ("providePraxisAnalyticalDrawerSchemas", _has_any(corpus, "providePraxisAnalyticalDrawerSchemas")),
            ("microVisualization", _has_any(corpus, "microVisualization", "praxis-micro-visualization", "@MicroVisualization")),
        )
        if not ok
    ]
    checks.append({"id": 8, "name": "Cockpits Analiticos e Micro-Visualizacoes (Pilar 11)", "passed": not missing_c8, "detail": "ok" if not missing_c8 else f"missing: {', '.join(missing_c8)}"})

    # Check 9 — Studio Page Builder & Save-As Nova Rota (Pilar 12a)
    missing_c9 = [
        label
        for label, ok in (
            ("DynamicPageBuilder", _has_any(corpus, "DynamicPageBuilderComponent", "praxis-dynamic-page-builder")),
            ("PraxisPageSaveAs", _has_any(corpus, "PraxisPageSaveAsComponent", "praxis-page-save-as")),
            ("PraxisPageCopyAction", _has_any(corpus, "PraxisPageCopyActionComponent", "praxis-page-copy-action")),
            ("UiLayoutLifecycleService", _has_any(corpus, "UiLayoutLifecycleService")),
            ("DynamicPageRoute(:pageId/:studioKey)", _has_any(corpus, ":pageId", ":studioKey")),
        )
        if not ok
    ]
    checks.append({"id": 9, "name": "Studio Page Builder & Save-As Nova Rota (Pilar 12a)", "passed": not missing_c9, "detail": "ok" if not missing_c9 else f"missing: {', '.join(missing_c9)}"})

    # Check 10 — Assistente de IA In-App (Pilar 12b)
    c10_ok = _has_any(corpus, "AI_BACKEND_STORAGE_OPTIONS", "PAGE_BUILDER_AGENTIC_AUTHORING_OPTIONS", "enableAgenticAuthoring", "PraxisAiAssistantShellComponent")
    checks.append({"id": 10, "name": "Assistente de IA In-App (Pilar 12b)", "passed": c10_ok, "detail": "ok" if c10_ok else "missing @praxisui/ai integration tokens"})

    return checks, discovered_routes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host_dir", nargs="?", default=".", help="Angular host directory")
    parser.add_argument("--strict", action="store_true", help="Fail if any check does not pass (always strict)")
    parser.add_argument("--expected-routes", type=int, default=None, help="Minimum expected declarative CRUD routes")
    args = parser.parse_args(argv)

    host_root = Path(args.host_dir).resolve()
    if not host_root.is_dir():
        print(f"[FAIL] host directory not found: {host_root}", file=sys.stderr)
        return 1

    checks, discovered_routes = evaluate_host(host_root, expected_routes=args.expected_routes)
    passed = sum(1 for c in checks if c["passed"])
    for c in checks:
        tag = "PASS" if c["passed"] else "FAIL"
        print(f"[{tag}] Check {c['id']} — {c['name']}: {c['detail']}")

    print(f"Angular host completeness audit: {passed}/{len(checks)} Checks Passed ({discovered_routes} rotas descobertas)")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
