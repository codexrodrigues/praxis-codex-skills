#!/usr/bin/env python3
"""Classify sanitized HADES parent/child activation facts."""

from __future__ import annotations

import argparse
import json


def _enabled(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().upper()
    if normalized not in {"S", "N"}:
        raise ValueError("activation flags must be S/N or boolean")
    return normalized == "S"


def classify(parent_exec: str | bool, parent_exec_mult_eps: str | bool,
             route_present: bool, enabled_children: int = 0) -> str:
    """Return the reachable activation mode without inferring missing routes."""
    if enabled_children < 0:
        raise ValueError("enabled_children must be non-negative")
    direct = _enabled(parent_exec)
    multiple = _enabled(parent_exec_mult_eps)
    if direct:
        return "DIRECT_ACTIVE" if route_present else "DIRECT_ENABLED_ROUTE_UNRESOLVED"
    if multiple:
        if enabled_children == 0:
            return "MULTI_ENABLED_NO_ACTIVE_CHILD"
        return "MULTI_ACTIVE" if route_present else "MULTI_ENABLED_ROUTE_UNRESOLVED"
    return "NO_CHAIN"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-exec", required=True)
    parser.add_argument("--parent-exec-mult-eps", required=True)
    parser.add_argument("--route-present", action="store_true")
    parser.add_argument("--enabled-children", type=int, default=0)
    args = parser.parse_args()
    result = classify(args.parent_exec, args.parent_exec_mult_eps,
                      args.route_present, args.enabled_children)
    print(json.dumps({"classification": result}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
