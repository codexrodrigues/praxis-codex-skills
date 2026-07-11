#!/usr/bin/env python3
"""Create a bounded, evidence-led Praxis API migration packet."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


OPERATION_SHAPES = {
    "list": ("POST {basePath}/filter", "READ_EVIDENCE_REQUIRED"),
    "detail": ("GET {basePath}/{id}", "READ_EVIDENCE_REQUIRED"),
    "options": ("POST {basePath}/options/filter", "READ_EVIDENCE_REQUIRED"),
    "create": ("POST {basePath}", "WRITE_ROUTE_REQUIRED"),
    "update": ("PUT {basePath}/{id}", "WRITE_ROUTE_REQUIRED"),
    "delete": ("DELETE {basePath}/{id}", "WRITE_ROUTE_REQUIRED"),
    "duplicate": ("POST {basePath}/{id}/duplicate-draft, then POST {basePath}", "WRITE_ROUTE_REQUIRED"),
    "cancel": ("No backend mutation", "NO_MUTATION_PROOF_REQUIRED"),
}


def checked_identifier(value: str, label: str, allow_dots: bool = False) -> str:
    tail = r"[A-Za-z0-9_.-]*" if allow_dots else r"[A-Za-z0-9_-]*"
    if not re.fullmatch(r"[A-Za-z0-9]" + tail, value):
        raise ValueError(f"{label} must contain only letters, digits, hyphens, or underscores")
    return value


def parse_operations(value: str) -> list[str]:
    operations = [part.strip().lower() for part in value.split(",") if part.strip()]
    unknown = sorted(set(operations) - OPERATION_SHAPES.keys())
    if unknown:
        raise ValueError(f"unknown operations: {', '.join(unknown)}")
    if not operations:
        raise ValueError("at least one operation is required")
    return list(dict.fromkeys(operations))


def checked_base_path(value: str) -> str:
    if not re.fullmatch(r"/[A-Za-z0-9_./-]+", value):
        raise ValueError("base path must start with / and contain only path-safe letters, digits, dots, underscores, or hyphens")
    return value.rstrip("/")


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("started-at must include a UTC offset or Z")
    return parsed.astimezone(timezone.utc)


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screen", required=True)
    parser.add_argument("--resource-key", required=True)
    parser.add_argument("--base-path", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--operations", default="list,detail,options")
    parser.add_argument("--started-at", help="ISO-8601 UTC timestamp for reproducible generation")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    try:
        screen = checked_identifier(args.screen, "screen")
        resource_key = checked_identifier(args.resource_key, "resource key", allow_dots=True)
        base_path = checked_base_path(args.base_path)
        operations = parse_operations(args.operations)
        started_at = parse_utc(args.started_at) if args.started_at else datetime.now(timezone.utc)
    except ValueError as error:
        parser.error(str(error))

    output = args.output.resolve()
    if output.exists() and any(output.iterdir()) and not args.force:
        print(f"Refusing to overwrite non-empty packet: {output}. Use --force after review.", file=sys.stderr)
        return 2
    output.mkdir(parents=True, exist_ok=True)

    operation_rows = []
    for operation in operations:
        endpoint, state = OPERATION_SHAPES[operation]
        operation_rows.append(
            f"| `{operation}` | `{endpoint.replace('{basePath}', base_path)}` | `{state}` | TODO: discovery source and parity case |"
        )

    manifest = {
        "schemaVersion": 1,
        "screen": screen,
        "resourceKey": resource_key,
        "basePath": base_path,
        "operations": operations,
        "generatedBy": "ergon-migration-scaffold",
        "evidenceState": "not-executed",
    }
    write(output / "scaffold-manifest.json", json.dumps(manifest, indent=2) + "\n")
    timing = {
        "schemaVersion": 1,
        "screen": screen,
        "resourceKey": resource_key,
        "basePath": base_path,
        "startedAtUtc": utc_text(started_at),
        "milestones": [
            {
                "name": "scaffold-created",
                "atUtc": utc_text(started_at),
                "elapsedMinutes": 0.0,
                "outcome": "passed",
                "evidence": "scaffold-manifest.json",
            }
        ],
    }
    write(output / "factory-timing.json", json.dumps(timing, indent=2) + "\n")
    write(
        output / "README.md",
        f"# {screen} API Scaffold\n\n"
        f"Resource key: `{resource_key}`. Base path: `{base_path}`. Generated packet only; it is not endpoint or parity evidence.\n\n"
        "Fill each TODO from the closed discovery package before Java implementation.\n",
    )
    write(
        output / "operation-inventory.md",
        f"# {screen} Operation Inventory\n\n"
        "| Operation | Praxis route | Initial state | Required evidence |\n"
        "| --- | --- | --- | --- |\n"
        + "\n".join(operation_rows)
        + "\n\nWrites require table-rule audit and an explicit route decision.\n",
    )
    write(
        output / "praxis-contract-outline.md",
        f"# {screen} Praxis Contract Outline\n\n"
        f"- Resource key: `{resource_key}`\n"
        f"- Base path: `{base_path}`\n"
        "- Required review: DTO, FilterDTO, options, `/schemas/filtered`, surfaces, actions, capabilities, HATEOAS.\n"
        "- Public identity: TODO: stable business key; keep `ROWID` internal unless evidence approves otherwise.\n"
        "- Reuse inventory: TODO: classify native Praxis support before adding a contract.\n"
        "- Security/context: TODO: authenticated user, company, tenant, and legacy bridge requirements.\n",
    )
    write(
        output / "implementation-slice.md",
        "# Implementation Slice\n\n"
        "1. Link discovery evidence for the smallest read operation.\n"
        "2. Inspect the target Java module and implement the canonical resource baseline.\n"
        "3. Prove endpoint execution, then compare legacy/API/database behavior with the same context.\n"
        "4. Add options or the next read operation only after the prior slice closes.\n"
        "5. Route each write to table-rule audit and legacy-backed/direct-safe decision before code.\n"
        "6. Record phase gate, residuals, cleanup evidence, and next skill.\n",
    )
    print(f"Created API scaffold: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
