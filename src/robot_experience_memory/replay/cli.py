"""Command line interface for replaying stored experiences."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from robot_experience_memory.replay import ReplayConfig, ReplayEngine
from robot_experience_memory.store import (
    ExperienceFilter,
    Pagination,
    StoreConfig,
    create_memory_store,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the replay CLI parser."""
    parser = argparse.ArgumentParser(description="Replay stored robot experiences")
    parser.add_argument("--backend", choices=["jsonl", "sqlite"], required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--robot-id")
    parser.add_argument("--environment")
    parser.add_argument("--action-type")
    parser.add_argument("--success", action="store_true")
    parser.add_argument("--failure", action="store_true")
    parser.add_argument("--deterministic", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--output", choices=["json", "text"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the replay CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    success = None
    if args.success and args.failure:
        parser.error("--success and --failure are mutually exclusive")
    if args.success:
        success = True
    if args.failure:
        success = False

    store = create_memory_store(StoreConfig(backend=args.backend, path=Path(args.path)))
    filters = ExperienceFilter(
        robot_id=args.robot_id,
        environment=args.environment,
        action_type=args.action_type,
        success=success,
    )
    pagination = Pagination(limit=args.limit, offset=args.offset)
    report = ReplayEngine(store, ReplayConfig(deterministic=args.deterministic)).replay(
        filters=filters, pagination=pagination
    )
    if args.output == "json":
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(
            f"replayed {report.total_experiences} experiences "
            f"({report.success_count} success, {report.failure_count} failure)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
