from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Branch_Selector_Lookback_Audit import percent, ranked
from Motion_Band_Resolver_Audit import BAND_FEATURE_RECIPES
from Range_Selector_Confirmation_Audit import enriched_cases, majority_value
from Selector_Priority_Board import (
    DEFAULT_OUTPUT_PATH as DEFAULT_BRANCH_BOARD,
    read_json,
)
from Weak_World_Selector_Upgrade_Audit import feature_key
from World_Band_Coverage_Ladder_Audit import (
    DEFAULT_OUTPUT_PATH as DEFAULT_LADDER_AUDIT,
    LADDER_LEVELS,
    band_quality as ladder_quality,
    ladder_key,
)
from World_Band_Preference_Audit import build_prediction_contexts
from World_Motion_Selector_Board import DEFAULT_OUTPUT_PATH as DEFAULT_MOTION_BOARD


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "world_band_blended_resolver_audit_min2_2015-10-07.json"
)

QUALITY_RANK = {
    "STRONG_BLEND": 8,
    "USABLE_BLEND": 7,
    "DEVELOPING_BLEND": 6,
    "SHARP_LOW_COVERAGE_BLEND": 5,
    "SMALL_BLEND": 4,
    "COVERAGE_WEAK_BLEND": 3,
    "OBSERVE_BLEND": 2,
    "WEAK_BLEND": 1,
    "NO_CALL": 0,
}

FALLBACK_ALLOWED_QUALITIES = {
    "STRONG_COVERAGE_BAND",
    "USABLE_COVERAGE_BAND",
    "DEVELOPING_COVERAGE_BAND",
}


def source_allows(source: str | None, case: dict[str, Any], target_world: str) -> bool:
    return str(source) == "BORROWED" or str(case["topology_name"]) == target_world


def selector_features(selector: dict[str, Any] | None) -> tuple[str, ...]:
    if not selector:
        return ()
    return tuple(str(feature) for feature in selector.get("features", []))


def predict_sharp_band(
    rows: list[dict[str, Any]],
    *,
    min_prior: int,
) -> dict[str, Any]:
    band = majority_value(rows, "actual_motion_band", min_prior=min_prior)
    if band["status"] != "CALL":
        return {
            "status": "NO_CALL",
            "value": None,
            "prior_count": int(band.get("prior_count") or 0),
            "rank": band.get("rank", []),
        }
    return {
        "status": "CALL",
        "value": str(band["value"]),
        "prior_count": int(band.get("prior_count") or 0),
        "rank": band.get("rank", []),
    }


def predict_ladder_band(
    memory: dict[tuple[str, tuple[str, ...]], list[dict[str, Any]]],
    case: dict[str, Any],
    *,
    ladder_candidate: dict[str, Any] | None,
    prediction_context: dict[str, Any] | None,
    min_prior: int,
) -> dict[str, Any]:
    if not ladder_candidate:
        return {
            "status": "NO_CALL",
            "value": None,
            "level": None,
            "prior_count": 0,
            "rank": [],
        }
    branch = family = sign = None
    if prediction_context is not None:
        branch_read = prediction_context["branch"]
        sign_read = prediction_context["sign"]
        branch = branch_read.get("predicted_branch")
        family = branch_read.get("predicted_family")
        sign = sign_read.get("value")
    recipe_features = tuple(str(feature) for feature in ladder_candidate.get("features", []))
    horizon = int(ladder_candidate.get("horizon") or 1)
    for level in LADDER_LEVELS:
        key = ladder_key(
            case,
            level,
            recipe_features=recipe_features,
            branch=branch,
            family=family,
            sign=sign,
            actual=False,
        )
        if key is None:
            continue
        rows = memory[(str(level["name"]), key)][-horizon:]
        band = majority_value(rows, "actual_motion_band", min_prior=min_prior)
        if band["status"] == "CALL":
            return {
                "status": "CALL",
                "value": str(band["value"]),
                "level": str(level["name"]),
                "prior_count": int(band.get("prior_count") or 0),
                "rank": band.get("rank", []),
            }
    return {
        "status": "NO_CALL",
        "value": None,
        "level": None,
        "prior_count": 0,
        "rank": [],
    }


def add_ladder_memory(
    memory: dict[tuple[str, tuple[str, ...]], list[dict[str, Any]]],
    case: dict[str, Any],
    *,
    ladder_candidate: dict[str, Any] | None,
) -> None:
    if not ladder_candidate:
        return
    recipe_features = tuple(str(feature) for feature in ladder_candidate.get("features", []))
    for level in LADDER_LEVELS:
        key = ladder_key(
            case,
            level,
            recipe_features=recipe_features,
            branch=None,
            family=None,
            sign=None,
            actual=True,
        )
        if key is not None:
            memory[(str(level["name"]), key)].append(case)


def empty_metrics() -> dict[str, Any]:
    return {
        "calls": 0,
        "matches": 0,
        "predicted_rank": Counter(),
        "miss_rank": Counter(),
        "source_rank": Counter(),
        "level_rank": Counter(),
    }


def record_call(
    metrics: dict[str, Any],
    *,
    prediction: dict[str, Any],
    actual_band: str,
    source: str,
) -> None:
    if prediction["status"] != "CALL":
        return
    predicted = str(prediction["value"])
    metrics["calls"] += 1
    metrics["predicted_rank"][predicted] += 1
    metrics["source_rank"][source] += 1
    if prediction.get("level"):
        metrics["level_rank"][str(prediction["level"])] += 1
    if predicted == actual_band:
        metrics["matches"] += 1
    else:
        metrics["miss_rank"][f"{predicted}->{actual_band}"] += 1


def blended_quality(report: dict[str, Any]) -> str:
    calls = int(report["call_count"])
    call_rate = float(report["call_rate"])
    band_rate = float(report["band_match_rate"])
    if calls < 3:
        return "NO_CALL"
    if call_rate >= 60 and band_rate >= 60:
        return "STRONG_BLEND"
    if call_rate >= 40 and band_rate >= 55:
        return "USABLE_BLEND"
    if call_rate >= 25 and band_rate >= 50:
        return "DEVELOPING_BLEND"
    if calls >= 5 and band_rate >= 65:
        return "SHARP_LOW_COVERAGE_BLEND"
    if calls >= 5 and band_rate >= 55:
        return "SMALL_BLEND"
    if call_rate >= 60 and band_rate >= 35:
        return "COVERAGE_WEAK_BLEND"
    if calls >= 3 and band_rate >= 45:
        return "OBSERVE_BLEND"
    return "WEAK_BLEND"


def finalize_metrics(
    name: str,
    metrics: dict[str, Any],
    *,
    test_count: int,
) -> dict[str, Any]:
    report = {
        "strategy": name,
        "test_count": test_count,
        "call_count": int(metrics["calls"]),
        "call_rate": percent(int(metrics["calls"]), test_count),
        "band_matches": int(metrics["matches"]),
        "band_match_rate": percent(int(metrics["matches"]), int(metrics["calls"])),
        "predicted_band_rank": ranked(metrics["predicted_rank"]),
        "source_rank": ranked(metrics["source_rank"]),
        "ladder_level_rank": ranked(metrics["level_rank"]),
        "miss_rank": ranked(metrics["miss_rank"])[:12],
    }
    report["quality"] = blended_quality(report)
    return report


def strategy_sort_key(report: dict[str, Any]) -> tuple[Any, ...]:
    quality = str(report["quality"])
    return (
        -QUALITY_RANK.get(quality, 0),
        -float(report["band_match_rate"]),
        -float(report["call_rate"]),
        -int(report["call_count"]),
        str(report["strategy"]),
    )


def evaluate_world(
    cases: list[dict[str, Any]],
    *,
    world: str,
    sharp_selector: dict[str, Any] | None,
    ladder_candidate: dict[str, Any] | None,
    prediction_contexts: dict[int, dict[str, Any]],
    min_prior: int,
) -> dict[str, Any]:
    test_count = 0
    actual_rank: Counter[str] = Counter()
    sharp_seen: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    ladder_memory: dict[tuple[str, tuple[str, ...]], list[dict[str, Any]]] = defaultdict(list)
    sharp_features = selector_features(sharp_selector)
    sharp_horizon = int((sharp_selector or {}).get("horizon") or 1)
    sharp_source = str((sharp_selector or {}).get("source") or "WORLD")
    ladder_candidate_quality = (
        ladder_quality(ladder_candidate) if ladder_candidate else "NO_CALL"
    )
    allow_quality_fallback = ladder_candidate_quality in FALLBACK_ALLOWED_QUALITIES
    metrics_by_strategy = {
        "SHARP_ONLY": empty_metrics(),
        "LADDER_ONLY": empty_metrics(),
        "SHARP_THEN_LADDER_ANY": empty_metrics(),
        "SHARP_THEN_LADDER_QUALITY_GATED": empty_metrics(),
    }

    for pos, case in enumerate(cases):
        actual_band = str(case["actual_motion_band"])
        sharp_key = feature_key(case, sharp_features)
        sharp_prediction = predict_sharp_band(
            sharp_seen[sharp_key][-sharp_horizon:],
            min_prior=min_prior,
        )
        ladder_prediction = predict_ladder_band(
            ladder_memory,
            case,
            ladder_candidate=ladder_candidate,
            prediction_context=prediction_contexts.get(pos),
            min_prior=min_prior,
        )

        if str(case["topology_name"]) == world:
            test_count += 1
            actual_rank[actual_band] += 1
            record_call(
                metrics_by_strategy["SHARP_ONLY"],
                prediction=sharp_prediction,
                actual_band=actual_band,
                source="SHARP",
            )
            record_call(
                metrics_by_strategy["LADDER_ONLY"],
                prediction=ladder_prediction,
                actual_band=actual_band,
                source="LADDER",
            )
            blended = (
                sharp_prediction
                if sharp_prediction["status"] == "CALL"
                else ladder_prediction
            )
            record_call(
                metrics_by_strategy["SHARP_THEN_LADDER_ANY"],
                prediction=blended,
                actual_band=actual_band,
                source="SHARP" if sharp_prediction["status"] == "CALL" else "LADDER",
            )
            gated = sharp_prediction
            gated_source = "SHARP"
            if gated["status"] != "CALL" and allow_quality_fallback:
                gated = ladder_prediction
                gated_source = "LADDER"
            record_call(
                metrics_by_strategy["SHARP_THEN_LADDER_QUALITY_GATED"],
                prediction=gated,
                actual_band=actual_band,
                source=gated_source,
            )

        if source_allows(sharp_source, case, world):
            sharp_seen[sharp_key].append(case)
        add_ladder_memory(ladder_memory, case, ladder_candidate=ladder_candidate)

    strategy_reports = [
        finalize_metrics(name, metrics, test_count=test_count)
        for name, metrics in metrics_by_strategy.items()
    ]
    selected = sorted(strategy_reports, key=strategy_sort_key)[0]
    return {
        "topology_name": world,
        "test_count": test_count,
        "actual_band_rank": ranked(actual_rank),
        "sharp_selector": sharp_selector,
        "ladder_candidate": ladder_candidate,
        "ladder_candidate_quality": ladder_candidate_quality,
        "quality_gated_fallback_allowed": allow_quality_fallback,
        "selected_blended_strategy": selected,
        "strategy_reports": sorted(strategy_reports, key=strategy_sort_key),
    }


def build_audit(
    cases: list[dict[str, Any]],
    motion_board: dict[str, Any],
    branch_board: dict[str, Any],
    ladder_audit: dict[str, Any],
    *,
    min_prior: int,
) -> dict[str, Any]:
    prediction_contexts = build_prediction_contexts(
        cases,
        motion_board,
        branch_board,
        min_prior=min_prior,
    )
    motion_by_world = {
        str(row["topology_name"]): row
        for row in motion_board.get("world_reports", [])
    }
    ladder_by_world = {
        str(row["topology_name"]): row
        for row in ladder_audit.get("world_reports", [])
    }
    reports = []
    quality_counts: Counter[str] = Counter()
    strategy_counts: Counter[str] = Counter()
    for world, motion_row in sorted(motion_by_world.items()):
        ladder_row = ladder_by_world.get(world, {})
        report = evaluate_world(
            cases,
            world=world,
            sharp_selector=motion_row.get("band_selector"),
            ladder_candidate=ladder_row.get("selected_ladder_band"),
            prediction_contexts=prediction_contexts,
            min_prior=min_prior,
        )
        selected = report["selected_blended_strategy"]
        quality_counts[str(selected["quality"])] += 1
        strategy_counts[str(selected["strategy"])] += 1
        reports.append(report)
    reports.sort(
        key=lambda row: (
            strategy_sort_key(row["selected_blended_strategy"]),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "WORLD_BAND_BLENDED_RESOLVER_AUDIT",
        "min_prior": min_prior,
        "world_count": len(reports),
        "quality_counts": dict(quality_counts),
        "selected_strategy_counts": dict(strategy_counts),
        "world_reports": reports,
        "notes": [
            "Sharp means the original world broad-band selector.",
            "Ladder means the coverage fallback ladder from sharp rooms down to broader baselines.",
            "The blended read is measured row by row so coverage and band rate are not guessed from summary totals.",
            "Quality-gated fallback only allows ladder fallback when the selected ladder is DEVELOPING_COVERAGE_BAND or better.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="World Band Blended Resolver Audit",
        description="Measure sharp band selectors, ladder coverage, and blended fallback per world.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--motion-board", type=Path, default=DEFAULT_MOTION_BOARD)
    parser.add_argument("--branch-board", type=Path, default=DEFAULT_BRANCH_BOARD)
    parser.add_argument("--ladder-audit", type=Path, default=DEFAULT_LADDER_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = build_audit(
        enriched_cases(args.csv_path, args.from_date),
        read_json(args.motion_board),
        read_json(args.branch_board),
        read_json(args.ladder_audit),
        min_prior=args.min_prior,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.print_summary:
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "quality_counts": payload["quality_counts"],
                    "selected_strategy_counts": payload["selected_strategy_counts"],
                    "world_reports": [
                        {
                            "world": row["topology_name"],
                            "ladder_quality": row["ladder_candidate_quality"],
                            "selected": row["selected_blended_strategy"],
                        }
                        for row in payload["world_reports"]
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
