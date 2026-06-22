from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Branch_Selector_Lookback_Audit import percent, ranked
from Range_Selector_Confirmation_Audit import enriched_cases
from Weak_World_Selector_Upgrade_Audit import (
    LIVE_SAFE_FEATURE_RECIPES,
    feature_key,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "motion_range_resolver_audit_min2_2015-10-07.json"
)

DEFAULT_HORIZONS = (2, 3, 5, 8, 13, 21, 34)

MOTION_RANGE_RECIPES: dict[str, tuple[str, ...]] = {
    "WORLD": ("topology_name",),
    "WORLD_PRESSURE_TOPOLOGY": (
        "topology_name",
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "WORLD_PRESSURE_BODY": (
        "topology_name",
        "pressure_shape",
        "set_relation",
        "middle_pressure",
        "edge_pressure",
    ),
    "WORLD_BURDEN": (
        "topology_name",
        "highest_burden_seat",
        "highest_burden_level",
        "highest_burden_state",
    ),
    "WORLD_BURDEN_FACE": (
        "topology_name",
        "highest_burden_seat",
        "highest_burden_state",
        "face_family",
        "turn_lanes",
    ),
    "WORLD_DOMINANT_ORIGIN_INCOMING": (
        "topology_name",
        "dominant_origin_seat",
        "authority_origin",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "WORLD_AUTHORITY_INCOMING": (
        "topology_name",
        "authority_seat",
        "authority_origin",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "WORLD_FACE_INCOMING": (
        "topology_name",
        "face_family",
        "turn_lanes",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "WORLD_FUSION_INCOMING": (
        "topology_name",
        "pressure_fusion",
        "pressure_fusion_profile",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "WORLD_HISTORY_BURDEN": (
        "topology_name",
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
        "highest_burden_seat",
        "highest_burden_state",
    ),
}

for name, features in LIVE_SAFE_FEATURE_RECIPES.items():
    MOTION_RANGE_RECIPES[f"GLOBAL_{name}"] = features


def motion_profile(rows: list[dict[str, Any]]) -> dict[str, Any]:
    motions = [int(row["actual_motion"]) for row in rows]
    abs_motions = [abs(value) for value in motions]
    signed_min = min(motions)
    signed_max = max(motions)
    abs_min = min(abs_motions)
    abs_max = max(abs_motions)
    signed_median = median(motions)
    abs_median = median(abs_motions)
    return {
        "signed_motion_min": signed_min,
        "signed_motion_max": signed_max,
        "signed_motion_median": signed_median,
        "signed_width": signed_max - signed_min,
        "abs_motion_min": abs_min,
        "abs_motion_max": abs_max,
        "abs_motion_median": abs_median,
        "abs_width": abs_max - abs_min,
        "sign_rank": ranked(Counter(str(row["actual_motion_sign"]) for row in rows)),
        "band_rank": ranked(Counter(str(row["actual_motion_band"]) for row in rows)),
        "top_motion_values": ranked(Counter(str(value) for value in motions))[:10],
    }


def predicted_interval(
    rows: list[dict[str, Any]],
    *,
    strategy: str,
) -> dict[str, Any]:
    profile = motion_profile(rows)
    center = int(round(float(profile["signed_motion_median"])))
    if strategy == "FULL_RANGE":
        low = int(profile["signed_motion_min"])
        high = int(profile["signed_motion_max"])
    elif strategy == "MEDIAN_RADIUS_3":
        low = center - 3
        high = center + 3
    elif strategy == "MEDIAN_RADIUS_5":
        low = center - 5
        high = center + 5
    elif strategy == "MEDIAN_RADIUS_8":
        low = center - 8
        high = center + 8
    elif strategy == "MEDIAN_RADIUS_10":
        low = center - 10
        high = center + 10
    elif strategy.startswith("SIGN_LOCKED_"):
        dominant_sign = profile["sign_rank"][0]["value"] if profile["sign_rank"] else "0"
        sign_rows = [
            row
            for row in rows
            if str(row["actual_motion_sign"]) == dominant_sign
        ]
        if sign_rows:
            sign_profile = motion_profile(sign_rows)
            profile = sign_profile
            center = int(round(float(profile["signed_motion_median"])))
            if strategy == "SIGN_LOCKED_FULL_RANGE":
                low = int(profile["signed_motion_min"])
                high = int(profile["signed_motion_max"])
            elif strategy == "SIGN_LOCKED_RADIUS_5":
                low = center - 5
                high = center + 5
            elif strategy == "SIGN_LOCKED_RADIUS_8":
                low = center - 8
                high = center + 8
            elif strategy == "SIGN_LOCKED_RADIUS_10":
                low = center - 10
                high = center + 10
            else:
                raise ValueError(f"Unknown interval strategy: {strategy}")
        else:
            low = int(profile["signed_motion_min"])
            high = int(profile["signed_motion_max"])
    elif strategy == "BAND_LOCKED_FULL_RANGE":
        dominant_band = profile["band_rank"][0]["value"] if profile["band_rank"] else "NONE"
        band_rows = [
            row
            for row in rows
            if str(row["actual_motion_band"]) == dominant_band
        ]
        if band_rows:
            profile = motion_profile(band_rows)
            center = int(round(float(profile["signed_motion_median"])))
        low = int(profile["signed_motion_min"])
        high = int(profile["signed_motion_max"])
    elif strategy == "SIGN_BAND_LOCKED_FULL_RANGE":
        dominant_sign = profile["sign_rank"][0]["value"] if profile["sign_rank"] else "0"
        dominant_band = profile["band_rank"][0]["value"] if profile["band_rank"] else "NONE"
        locked_rows = [
            row
            for row in rows
            if str(row["actual_motion_sign"]) == dominant_sign
            and str(row["actual_motion_band"]) == dominant_band
        ]
        if locked_rows:
            profile = motion_profile(locked_rows)
            center = int(round(float(profile["signed_motion_median"])))
        low = int(profile["signed_motion_min"])
        high = int(profile["signed_motion_max"])
    else:
        raise ValueError(f"Unknown interval strategy: {strategy}")
    return {
        "strategy": strategy,
        "predicted_motion_low": low,
        "predicted_motion_high": high,
        "predicted_motion_midpoint": center,
        "predicted_width": high - low,
        "profile": profile,
    }


def interval_record(
    case: dict[str, Any],
    *,
    recipe_name: str,
    source: str,
    horizon: int,
    features: tuple[str, ...],
    interval: dict[str, Any] | None,
    prior_count: int,
) -> dict[str, Any]:
    actual_motion = int(case["actual_motion"])
    if interval is None:
        return {
            "date": case["date"],
            "index": case["index"],
            "topology_name": case["topology_name"],
            "status": "NO_CALL",
            "recipe": recipe_name,
            "source": source,
            "horizon": horizon,
            "features": list(features),
            "strategy": None,
            "prior_count": prior_count,
            "actual_motion": actual_motion,
            "actual_motion_sign": case["actual_motion_sign"],
            "actual_motion_band": case["actual_motion_band"],
            "range_result": "NO_CALL",
            "exact_midpoint_result": "NO_CALL",
        }
    low = int(interval["predicted_motion_low"])
    high = int(interval["predicted_motion_high"])
    midpoint = int(interval["predicted_motion_midpoint"])
    return {
        "date": case["date"],
        "index": case["index"],
        "topology_name": case["topology_name"],
        "status": "CALL",
        "recipe": recipe_name,
        "source": source,
        "horizon": horizon,
        "features": list(features),
        "strategy": interval["strategy"],
        "prior_count": prior_count,
        "actual_motion": actual_motion,
        "actual_motion_sign": case["actual_motion_sign"],
        "actual_motion_band": case["actual_motion_band"],
        "predicted_motion_low": low,
        "predicted_motion_high": high,
        "predicted_motion_midpoint": midpoint,
        "predicted_width": int(interval["predicted_width"]),
        "range_result": "MATCH" if low <= actual_motion <= high else "MISS",
        "exact_midpoint_result": "MATCH" if midpoint == actual_motion else "MISS",
        "absolute_error_to_midpoint": abs(actual_motion - midpoint),
        "profile": interval["profile"],
    }


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    calls = [row for row in records if row["status"] == "CALL"]
    hits = sum(1 for row in calls if row["range_result"] == "MATCH")
    exact = sum(1 for row in calls if row["exact_midpoint_result"] == "MATCH")
    widths = [int(row["predicted_width"]) for row in calls]
    errors = [int(row["absolute_error_to_midpoint"]) for row in calls]
    return {
        "test_count": len(records),
        "call_count": len(calls),
        "call_rate": percent(len(calls), len(records)),
        "range_hits": hits,
        "range_hit_rate": percent(hits, len(calls)),
        "exact_midpoint_hits": exact,
        "exact_midpoint_rate": percent(exact, len(calls)),
        "avg_width": round(sum(widths) / len(widths), 2) if widths else 0.0,
        "median_width": median(widths) if widths else 0.0,
        "avg_abs_error": round(sum(errors) / len(errors), 2) if errors else 0.0,
        "median_abs_error": median(errors) if errors else 0.0,
    }


def evaluate_recipe(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    recipe_name: str,
    features: tuple[str, ...],
    source: str,
    horizon: int,
    strategy: str,
    min_prior: int,
) -> list[dict[str, Any]]:
    records = []
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        key = feature_key(case, features)
        if case["topology_name"] == target_world:
            prior_rows = seen_by_key[key][-horizon:]
            if len(prior_rows) >= min_prior:
                interval = predicted_interval(prior_rows, strategy=strategy)
            else:
                interval = None
            records.append(
                interval_record(
                    case,
                    recipe_name=recipe_name,
                    source=source,
                    horizon=horizon,
                    features=features,
                    interval=interval,
                    prior_count=len(prior_rows),
                )
            )
        if source == "BORROWED" or case["topology_name"] == target_world:
            seen_by_key[key].append(case)
    return records


def evaluate_recipe_summary(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    recipe_name: str,
    features: tuple[str, ...],
    source: str,
    horizon: int,
    strategy: str,
    min_prior: int,
) -> dict[str, Any]:
    test_count = 0
    call_count = 0
    range_hits = 0
    exact_hits = 0
    widths: list[int] = []
    errors: list[int] = []
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        key = feature_key(case, features)
        if case["topology_name"] == target_world:
            test_count += 1
            prior_rows = seen_by_key[key][-horizon:]
            if len(prior_rows) >= min_prior:
                interval = predicted_interval(prior_rows, strategy=strategy)
                actual_motion = int(case["actual_motion"])
                low = int(interval["predicted_motion_low"])
                high = int(interval["predicted_motion_high"])
                midpoint = int(interval["predicted_motion_midpoint"])
                width = int(interval["predicted_width"])
                call_count += 1
                if low <= actual_motion <= high:
                    range_hits += 1
                if midpoint == actual_motion:
                    exact_hits += 1
                widths.append(width)
                errors.append(abs(actual_motion - midpoint))
        if source == "BORROWED" or case["topology_name"] == target_world:
            seen_by_key[key].append(case)
    return {
        "test_count": test_count,
        "call_count": call_count,
        "call_rate": percent(call_count, test_count),
        "range_hits": range_hits,
        "range_hit_rate": percent(range_hits, call_count),
        "exact_midpoint_hits": exact_hits,
        "exact_midpoint_rate": percent(exact_hits, call_count),
        "avg_width": round(sum(widths) / len(widths), 2) if widths else 0.0,
        "median_width": median(widths) if widths else 0.0,
        "avg_abs_error": round(sum(errors) / len(errors), 2) if errors else 0.0,
        "median_abs_error": median(errors) if errors else 0.0,
    }


def candidate_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -float(row["range_hit_rate"]),
        float(row["avg_width"]),
        float(row["avg_abs_error"]),
        -float(row["exact_midpoint_rate"]),
        -int(row["call_count"]),
        row["recipe"],
        row["source"],
        row["horizon"],
        row["strategy"],
    )


def practical_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -float(row["range_hit_rate"]),
        float(row["avg_width"]),
        float(row["avg_abs_error"]),
        -float(row["exact_midpoint_rate"]),
        -int(row["call_count"]),
        row["recipe"],
        row["source"],
        row["horizon"],
        row["strategy"],
    )


def build_audit(
    cases: list[dict[str, Any]],
    *,
    target_worlds: list[str],
    recipe_names: tuple[str, ...],
    horizons: tuple[int, ...],
    strategies: tuple[str, ...],
    min_prior: int,
    min_calls: int,
    max_practical_width: int,
) -> dict[str, Any]:
    world_reports = []
    recipes = {
        name: MOTION_RANGE_RECIPES[name]
        for name in recipe_names
        if name in MOTION_RANGE_RECIPES
    }
    for world in target_worlds:
        world_candidates = []
        for recipe_name, features in recipes.items():
            for source in ("WORLD", "BORROWED"):
                for horizon in horizons:
                    for strategy in strategies:
                        summary = evaluate_recipe_summary(
                            cases,
                            target_world=world,
                            recipe_name=recipe_name,
                            features=features,
                            source=source,
                            horizon=horizon,
                            strategy=strategy,
                            min_prior=min_prior,
                        )
                        world_candidates.append(
                            {
                                "recipe": recipe_name,
                                "source": source,
                                "horizon": horizon,
                                "strategy": strategy,
                                "features": list(features),
                                **summary,
                            }
                        )
        world_candidates.sort(key=candidate_sort_key)
        useful = [
            row
            for row in world_candidates
            if int(row["call_count"]) >= min_calls
        ]
        useful.sort(key=candidate_sort_key)
        practical = [
            row
            for row in useful
            if float(row["avg_width"]) <= max_practical_width
        ]
        practical.sort(key=practical_sort_key)
        world_reports.append(
            {
                "topology_name": world,
                "selected_motion_range_candidate": world_candidates[0]
                if world_candidates
                else None,
                "selected_useful_motion_range_candidate": useful[0]
                if useful
                else None,
                "selected_practical_motion_range_candidate": practical[0]
                if practical
                else None,
                "top_motion_range_candidates": world_candidates[:50],
                "top_useful_motion_range_candidates": useful[:50],
                "top_practical_motion_range_candidates": practical[:50],
            }
        )
    world_reports.sort(
        key=lambda row: (
            candidate_sort_key(row["selected_useful_motion_range_candidate"])
            if row["selected_useful_motion_range_candidate"]
            else (999,),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "MOTION_RANGE_RESOLVER_AUDIT",
        "min_prior": min_prior,
        "min_calls": min_calls,
        "max_practical_width": max_practical_width,
        "horizons": list(horizons),
        "strategies": list(strategies),
        "world_count": len(world_reports),
        "world_reports": world_reports,
        "notes": [
            "This audit predicts signed outgoing motion intervals from prior matching rooms only.",
            "Range hit means actual_motion landed inside the predicted low/high interval.",
            "Exact midpoint hit means actual_motion equaled the rounded historical median.",
            "Best candidates are sorted by range hit rate first, then tightness.",
            "Large ranges can hit often but are less useful; avg_width must be reviewed.",
            "Practical candidates are filtered by max_practical_width before selection.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Motion Range Resolver Audit",
        description="Audit live-safe historical rooms for signed outgoing motion amount ranges.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument(
        "--worlds",
        default=(
            "Altera,Nova,Nyx,Citrine,Lumina,Nirvana,Alcides,Artoria,Nero,"
            "Rama,Suzuka,Tomoe Gozen,Karna,Medusa,Kurohime,Irisviel,Circe,Scathach"
        ),
    )
    parser.add_argument("--horizons", default="2,3,5,8,13,21,34")
    parser.add_argument(
        "--recipes",
        default="",
        help="Optional comma-separated recipe names. Empty means all recipes.",
    )
    parser.add_argument(
        "--strategies",
        default=(
            "FULL_RANGE,MEDIAN_RADIUS_3,MEDIAN_RADIUS_5,MEDIAN_RADIUS_8,"
            "MEDIAN_RADIUS_10,SIGN_LOCKED_FULL_RANGE,SIGN_LOCKED_RADIUS_5,"
            "SIGN_LOCKED_RADIUS_8,SIGN_LOCKED_RADIUS_10,BAND_LOCKED_FULL_RANGE,"
            "SIGN_BAND_LOCKED_FULL_RANGE"
        ),
    )
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--min-calls", type=int, default=10)
    parser.add_argument("--max-practical-width", type=int, default=30)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    worlds = [part.strip() for part in args.worlds.split(",") if part.strip()]
    horizons = tuple(
        int(part.strip())
        for part in args.horizons.split(",")
        if part.strip()
    )
    strategies = tuple(
        part.strip()
        for part in args.strategies.split(",")
        if part.strip()
    )
    recipe_names = tuple(
        part.strip()
        for part in args.recipes.split(",")
        if part.strip()
    ) or tuple(MOTION_RANGE_RECIPES)
    payload = build_audit(
        enriched_cases(args.csv_path, args.from_date),
        target_worlds=worlds,
        recipe_names=recipe_names,
        horizons=horizons,
        strategies=strategies,
        min_prior=args.min_prior,
        min_calls=args.min_calls,
        max_practical_width=args.max_practical_width,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.print_summary:
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "world_reports": [
                        {
                            "world": row["topology_name"],
                            "selected_useful": row[
                                "selected_useful_motion_range_candidate"
                            ],
                            "selected_practical": row[
                                "selected_practical_motion_range_candidate"
                            ],
                        }
                        for row in payload["world_reports"]
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
