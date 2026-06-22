from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Branch_Selector_Lookback_Audit import percent, ranked
from Range_Selector_Confirmation_Audit import enriched_cases, majority_value
from Selector_Priority_Board import (
    DEFAULT_OUTPUT_PATH as DEFAULT_BRANCH_BOARD,
    read_json,
)
from World_Band_Preference_Audit import (
    BAND_PREFERENCE_RECIPES,
    build_prediction_contexts,
)
from World_Motion_Selector_Board import DEFAULT_OUTPUT_PATH as DEFAULT_MOTION_BOARD


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "world_band_coverage_ladder_audit_min2_2015-10-07.json"
)

DEFAULT_HORIZONS = (2, 3, 5, 8, 13, 21, 34)
TOPOLOGY_FIELDS = (
    "map_pressure_type",
    "pressure_center",
    "pressure_balance",
    "pressure_distribution",
)

LADDER_LEVELS: tuple[dict[str, Any], ...] = (
    {
        "name": "WORLD_BRANCH_SIGN_FULL",
        "source": "WORLD",
        "context": "BRANCH_SIGN",
        "features": "RECIPE",
    },
    {
        "name": "WORLD_FAMILY_SIGN_FULL",
        "source": "WORLD",
        "context": "FAMILY_SIGN",
        "features": "RECIPE",
    },
    {
        "name": "WORLD_SIGN_FULL",
        "source": "WORLD",
        "context": "SIGN_ONLY",
        "features": "RECIPE",
    },
    {
        "name": "BORROWED_BRANCH_SIGN_FULL",
        "source": "BORROWED",
        "context": "BRANCH_SIGN",
        "features": "RECIPE",
    },
    {
        "name": "BORROWED_FAMILY_SIGN_FULL",
        "source": "BORROWED",
        "context": "FAMILY_SIGN",
        "features": "RECIPE",
    },
    {
        "name": "BORROWED_SIGN_FULL",
        "source": "BORROWED",
        "context": "SIGN_ONLY",
        "features": "RECIPE",
    },
    {
        "name": "WORLD_BRANCH_SIGN_BASELINE",
        "source": "WORLD",
        "context": "BRANCH_SIGN",
        "features": (),
    },
    {
        "name": "WORLD_FAMILY_SIGN_BASELINE",
        "source": "WORLD",
        "context": "FAMILY_SIGN",
        "features": (),
    },
    {
        "name": "WORLD_SIGN_BASELINE",
        "source": "WORLD",
        "context": "SIGN_ONLY",
        "features": (),
    },
    {
        "name": "TOPOLOGY_SIGN_BASELINE",
        "source": "TOPOLOGY",
        "context": "SIGN_ONLY",
        "features": TOPOLOGY_FIELDS,
    },
    {
        "name": "BORROWED_FAMILY_SIGN_BASELINE",
        "source": "BORROWED",
        "context": "FAMILY_SIGN",
        "features": (),
    },
    {
        "name": "WORLD_BASELINE",
        "source": "WORLD",
        "context": "NONE",
        "features": (),
    },
    {
        "name": "TOPOLOGY_BASELINE",
        "source": "TOPOLOGY",
        "context": "NONE",
        "features": TOPOLOGY_FIELDS,
    },
    {
        "name": "GLOBAL_BASELINE",
        "source": "BORROWED",
        "context": "NONE",
        "features": (),
    },
)


def value_tuple(row: dict[str, Any], features: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(str(row.get(feature, "NONE")) for feature in features)


def context_tuple(
    row: dict[str, Any],
    *,
    context: str,
    branch: str | None,
    family: str | None,
    sign: str | None,
    actual: bool,
) -> tuple[str, ...] | None:
    if actual:
        branch = str(row["actual_branch"])
        family = str(row["actual_family"])
        sign = str(row["actual_motion_sign"])
    if context == "BRANCH_SIGN":
        if branch is None or sign is None:
            return None
        return (str(branch), str(sign))
    if context == "FAMILY_SIGN":
        if family is None or sign is None:
            return None
        return (str(family), str(sign))
    if context == "SIGN_ONLY":
        if sign is None:
            return None
        return (str(sign),)
    if context == "NONE":
        return ()
    raise ValueError(f"Unknown context: {context}")


def level_features(
    level: dict[str, Any],
    recipe_features: tuple[str, ...],
) -> tuple[str, ...]:
    features = level["features"]
    if features == "RECIPE":
        return recipe_features
    return tuple(features)


def ladder_key(
    row: dict[str, Any],
    level: dict[str, Any],
    *,
    recipe_features: tuple[str, ...],
    branch: str | None,
    family: str | None,
    sign: str | None,
    actual: bool,
) -> tuple[str, ...] | None:
    context = context_tuple(
        row,
        context=str(level["context"]),
        branch=branch,
        family=family,
        sign=sign,
        actual=actual,
    )
    if context is None:
        return None
    source = str(level["source"])
    source_part = ()
    if source == "WORLD":
        source_part = (str(row["topology_name"]),)
    elif source == "TOPOLOGY":
        source_part = value_tuple(row, TOPOLOGY_FIELDS)
    elif source != "BORROWED":
        raise ValueError(f"Unknown source: {source}")
    features = level_features(level, recipe_features)
    return source_part + context + value_tuple(row, features)


def band_quality(row: dict[str, Any]) -> str:
    calls = int(row["call_count"])
    call_rate = float(row["call_rate"])
    band = float(row["band_match_rate"])
    if calls < 3:
        return "NO_CALL"
    if call_rate >= 60 and band >= 60:
        return "STRONG_COVERAGE_BAND"
    if call_rate >= 40 and band >= 55:
        return "USABLE_COVERAGE_BAND"
    if call_rate >= 25 and band >= 50:
        return "DEVELOPING_COVERAGE_BAND"
    if calls >= 5 and band >= 65:
        return "SHARP_LOW_COVERAGE_BAND"
    if calls >= 5 and band >= 55:
        return "SMALL_BAND"
    if call_rate >= 60 and band >= 35:
        return "COVERAGE_WEAK_BAND"
    if calls >= 3 and band >= 45:
        return "OBSERVE_BAND"
    return "WEAK_BAND"


QUALITY_RANK = {
    "STRONG_COVERAGE_BAND": 8,
    "USABLE_COVERAGE_BAND": 7,
    "DEVELOPING_COVERAGE_BAND": 6,
    "SHARP_LOW_COVERAGE_BAND": 5,
    "SMALL_BAND": 4,
    "COVERAGE_WEAK_BAND": 3,
    "OBSERVE_BAND": 2,
    "WEAK_BAND": 1,
    "NO_CALL": 0,
}


def candidate_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    quality = band_quality(row)
    return (
        -QUALITY_RANK[quality],
        -float(row["band_match_rate"]),
        -float(row["call_rate"]),
        -float(row["sign_match_rate"]),
        -int(row["call_count"]),
        row["recipe"],
        row["horizon"],
    )


def evaluate_ladder_candidate(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    prediction_contexts: dict[int, dict[str, Any]],
    recipe_name: str,
    recipe_features: tuple[str, ...],
    horizon: int,
    min_prior: int,
) -> dict[str, Any]:
    test_count = 0
    call_count = 0
    matches = 0
    sign_calls = 0
    sign_matches = 0
    branch_calls = 0
    branch_matches = 0
    family_matches = 0
    prior_counts: list[int] = []
    memory: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    level_counts: Counter[str] = Counter()
    level_matches: Counter[str] = Counter()
    predicted_rank: Counter[str] = Counter()
    actual_rank: Counter[str] = Counter()
    miss_rank: Counter[str] = Counter()

    for pos, case in enumerate(cases):
        context = prediction_contexts.get(pos)
        if case["topology_name"] == target_world:
            test_count += 1
            actual_rank[str(case["actual_motion_band"])] += 1
            if context is None:
                branch = family = sign = None
                branch_status = sign_status = "NO_CALL"
            else:
                branch_read = context["branch"]
                sign_read = context["sign"]
                branch = branch_read["predicted_branch"]
                family = branch_read["predicted_family"]
                sign = sign_read["value"]
                branch_status = branch_read["status"]
                sign_status = sign_read["status"]
                if branch_status == "CALL":
                    branch_calls += 1
                    if branch == case["actual_branch"]:
                        branch_matches += 1
                    if family == case["actual_family"]:
                        family_matches += 1
                if sign_status == "CALL":
                    sign_calls += 1
                    if sign == case["actual_motion_sign"]:
                        sign_matches += 1

            selected_band = None
            selected_level = None
            selected_prior_count = 0
            selected_rank: list[dict[str, Any]] = []
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
                    selected_band = str(band["value"])
                    selected_level = str(level["name"])
                    selected_prior_count = int(band["prior_count"] or 0)
                    selected_rank = band["rank"]
                    break

            if selected_band is not None and selected_level is not None:
                call_count += 1
                prior_counts.append(selected_prior_count)
                predicted_rank[selected_band] += 1
                level_counts[selected_level] += 1
                if selected_band == str(case["actual_motion_band"]):
                    matches += 1
                    level_matches[selected_level] += 1
                else:
                    miss_rank[f"{selected_band}->{case['actual_motion_band']}"] += 1

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

    level_reports = []
    for level, count in level_counts.most_common():
        level_reports.append(
            {
                "level": level,
                "count": count,
                "rate": percent(count, call_count),
                "matches": level_matches[level],
                "match_rate": percent(level_matches[level], count),
            }
        )
    return {
        "recipe": recipe_name,
        "horizon": horizon,
        "features": list(recipe_features),
        "quality": "",
        "test_count": test_count,
        "call_count": call_count,
        "call_rate": percent(call_count, test_count),
        "band_matches": matches,
        "band_match_rate": percent(matches, call_count),
        "avg_prior_count": round(sum(prior_counts) / len(prior_counts), 2)
        if prior_counts
        else 0.0,
        "branch_calls": branch_calls,
        "branch_match_rate": percent(branch_matches, branch_calls),
        "family_match_rate": percent(family_matches, branch_calls),
        "sign_calls": sign_calls,
        "sign_match_rate": percent(sign_matches, sign_calls),
        "level_reports": level_reports,
        "predicted_band_rank": ranked(predicted_rank),
        "actual_band_rank": ranked(actual_rank),
        "miss_rank": ranked(miss_rank)[:12],
    }


def build_audit(
    cases: list[dict[str, Any]],
    motion_board: dict[str, Any],
    branch_board: dict[str, Any],
    *,
    recipe_names: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
) -> dict[str, Any]:
    recipes = {
        name: BAND_PREFERENCE_RECIPES[name]
        for name in recipe_names
        if name in BAND_PREFERENCE_RECIPES
    }
    prediction_contexts = build_prediction_contexts(
        cases,
        motion_board,
        branch_board,
        min_prior=min_prior,
    )
    reports = []
    quality_counts: Counter[str] = Counter()
    for row in motion_board.get("world_reports", []):
        world = str(row["topology_name"])
        candidates = []
        for recipe_name, features in recipes.items():
            for horizon in horizons:
                candidate = evaluate_ladder_candidate(
                    cases,
                    target_world=world,
                    prediction_contexts=prediction_contexts,
                    recipe_name=recipe_name,
                    recipe_features=features,
                    horizon=horizon,
                    min_prior=min_prior,
                )
                candidate["quality"] = band_quality(candidate)
                candidates.append(candidate)
        candidates.sort(key=candidate_sort_key)
        selected = candidates[0]
        quality_counts[str(selected["quality"])] += 1
        reports.append(
            {
                "topology_name": world,
                "selected_ladder_band": selected,
                "top_ladder_band_candidates": candidates[:30],
            }
        )
    reports.sort(
        key=lambda row: (
            candidate_sort_key(row["selected_ladder_band"]),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "WORLD_BAND_COVERAGE_LADDER_AUDIT",
        "min_prior": min_prior,
        "horizons": list(horizons),
        "quality_counts": dict(quality_counts),
        "world_count": len(reports),
        "ladder_levels": [
            {
                "name": str(level["name"]),
                "source": str(level["source"]),
                "context": str(level["context"]),
                "features": "RECIPE"
                if level["features"] == "RECIPE"
                else list(level["features"]),
            }
            for level in LADDER_LEVELS
        ],
        "world_reports": reports,
        "notes": [
            "The ladder tries sharp world rooms first, then broader world rooms, borrowed analogs, topology baselines, and final baselines.",
            "Coverage means the selector can speak; band_match_rate means it was correct when it spoke.",
            "This audit is designed to blend coverage and accuracy before the 35-class motion gauge layer.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="World Band Coverage Ladder Audit",
        description="Audit fallback ladders that trade sharp band rooms for broader coverage.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--motion-board", type=Path, default=DEFAULT_MOTION_BOARD)
    parser.add_argument("--branch-board", type=Path, default=DEFAULT_BRANCH_BOARD)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--horizons", default="2,3,5,8,13,21,34")
    parser.add_argument(
        "--recipes",
        default="",
        help="Optional comma-separated recipe names. Empty means all recipes.",
    )
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    horizons = tuple(
        int(part.strip())
        for part in args.horizons.split(",")
        if part.strip()
    )
    recipe_names = tuple(
        part.strip()
        for part in args.recipes.split(",")
        if part.strip()
    ) or tuple(BAND_PREFERENCE_RECIPES)
    payload = build_audit(
        enriched_cases(args.csv_path, args.from_date),
        read_json(args.motion_board),
        read_json(args.branch_board),
        recipe_names=recipe_names,
        horizons=horizons,
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
                    "world_reports": [
                        {
                            "world": row["topology_name"],
                            "selected": row["selected_ladder_band"],
                        }
                        for row in payload["world_reports"]
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
