#!/usr/bin/env python3
"""Record an evidence-backed elapsed-time event in a migration scaffold."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


MILESTONES = {
    "implementation-started",
    "first-endpoint-executed",
    "schema-validated",
    "focused-tests-passed",
    "legacy-parity-assessed",
}
OUTCOMES = {"passed", "blocked", "deferred", "failed"}


def parse_utc(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{label} must be ISO-8601") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a UTC offset or Z")
    return parsed.astimezone(timezone.utc)


def utc_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--milestone", required=True, choices=sorted(MILESTONES))
    parser.add_argument("--outcome", required=True, choices=sorted(OUTCOMES))
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--at", help="ISO-8601 UTC timestamp; defaults to now")
    args = parser.parse_args()

    if not args.evidence.strip():
        parser.error("evidence is required")
    timing_path = args.packet.resolve() / "factory-timing.json"
    if not timing_path.is_file():
        print(f"Timing ledger not found: {timing_path}", file=sys.stderr)
        return 2
    try:
        timing = json.loads(timing_path.read_text(encoding="utf-8"))
        started_at = parse_utc(timing["startedAtUtc"], "startedAtUtc")
        at = parse_utc(args.at, "at") if args.at else datetime.now(timezone.utc)
    except (KeyError, ValueError, json.JSONDecodeError) as error:
        print(f"Invalid timing ledger: {error}", file=sys.stderr)
        return 2
    if at < started_at:
        print("Milestone cannot precede scaffold creation.", file=sys.stderr)
        return 2

    event = {
        "name": args.milestone,
        "atUtc": utc_text(at),
        "elapsedMinutes": round((at - started_at).total_seconds() / 60, 2),
        "outcome": args.outcome,
        "evidence": args.evidence,
    }
    existing = [item for item in timing.get("milestones", []) if item.get("name") == args.milestone]
    if existing:
        if existing[0] == event:
            print(f"Milestone already recorded: {args.milestone}")
            return 0
        print(f"Milestone already recorded with different evidence: {args.milestone}", file=sys.stderr)
        return 2

    timing.setdefault("milestones", []).append(event)
    timing_path.write_text(json.dumps(timing, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {args.milestone}: {event['elapsedMinutes']} minutes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
