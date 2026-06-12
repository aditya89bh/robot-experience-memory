"""Command line interface for inspecting similar experience retrieval."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from robot_experience_memory.retrieval import RetrievalEngine, RetrievalQuery
from robot_experience_memory.store import StoreConfig, create_memory_store


def build_parser() -> argparse.ArgumentParser:
    """Build the retrieval CLI parser."""
    parser = argparse.ArgumentParser(description="Retrieve similar robot experiences")
    parser.add_argument("--backend", choices=["jsonl", "sqlite"], required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--action-type")
    parser.add_argument("--robot-id")
    parser.add_argument("--environment")
    parser.add_argument("--operator")
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--success", action="store_true")
    parser.add_argument("--failure", action="store_true")
    parser.add_argument("--error-code")
    parser.add_argument("--top-k", type=int)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    return parser


def _success_value(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> bool | None:
    if args.success and args.failure:
        parser.error("--success and --failure are mutually exclusive")
    if args.success:
        return True
    if args.failure:
        return False
    return None


def _match_to_dict(match: Any) -> dict[str, Any]:
    explanation = match.explanation
    return {
        "experience_id": match.experience.experience.experience_id,
        "score": match.score,
        "action_type": match.experience.action.action_type,
        "robot_id": match.experience.metadata.robot_id,
        "environment": match.experience.metadata.environment,
        "success": match.experience.outcome.success,
        "stored_at": match.experience.stored_at.isoformat(),
        "explanation": explanation.to_dict() if explanation is not None else None,
    }


def _result_to_dict(result: Any) -> dict[str, Any]:
    return {
        "query": result.query.to_dict(),
        "matches": [_match_to_dict(match) for match in result.matches],
    }


def _print_text(result: Any) -> None:
    print(f"retrieved {len(result.matches)} matches")
    for match in result.matches:
        experience_id = match.experience.experience.experience_id
        action_type = match.experience.action.action_type
        robot_id = match.experience.metadata.robot_id
        environment = match.experience.metadata.environment
        print(
            f"{experience_id} score={match.score:.3f} "
            f"action={action_type} robot={robot_id} environment={environment}"
        )
        if match.explanation is not None:
            for reason in match.explanation.reasons:
                print(f"  - {reason}")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the retrieval CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    success = _success_value(args, parser)

    store = create_memory_store(StoreConfig(backend=args.backend, path=Path(args.path)))
    query = RetrievalQuery(
        action_type=args.action_type,
        robot_id=args.robot_id,
        environment=args.environment,
        operator=args.operator,
        success=success,
        error_code=args.error_code,
        tags=tuple(args.tag),
        top_k=args.top_k,
    )
    result = RetrievalEngine(store, cache_enabled=not args.no_cache).retrieve(query)

    if args.output == "json":
        print(json.dumps(_result_to_dict(result), indent=2, sort_keys=True))
    else:
        _print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
