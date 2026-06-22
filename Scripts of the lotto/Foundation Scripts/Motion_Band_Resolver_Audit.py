from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Branch_Selector_Lookback_Audit import percent, ranked
from Range_Selector_Confirmation_Audit import enriched_cases, majority_value
from Weak_World_Selector_Upgrade_Audit import (
    LIVE_SAFE_FEATURE_RECIPES,
    feature_key,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "motion_band_resolver_audit_min2_2015-10-07.json"
)

DEFAULT_HORIZONS = (2, 3, 5, 8, 13, 21, 34)

BAND_FEATURE_RECIPES: dict[str, tuple[str, ...]] = {
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
    world_name = f"WORLD_{name}"
    if world_name not in BAND_FEATURE_RECIPES:
        BAND_FEATURE_RECIPES[world_name] = ("topology_name",) + features
    BAND_FEATURE_RECIPES[f"GLOBAL_{name}"] = features


def evaluate_band_recipe(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    recipe_name: str,
    features: tuple[str, ...],
    source: str,
    horizon: int,
    min_prior: int,
) -> dict[str, Any]:
    test_count = 0
    call_count = 0
    matches = 0
    sign_matches = 0
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    predicted_rank: Counter[str] = Counter()
    actual_rank: Counter[str] = Counter()
    for case in cases:
        key = feature_key(case, features)
        if case["topology_name"] == target_world:
            test_count += 1
            actual_rank[str(case["actual_motion_band"])] += 1
            prior_rows = seen_by_key[key][-horizon:]
            band = majority_value(prior_rows, "actual_motion_band", min_prior=min_prior)
            sign = majority_value(prior_rows, "actual_motion_sign", min_prior=min_prior)
            if band["status"] == "CALL":
                call_count += 1
                predicted_band = str(band["value"])
                predicted_rank[predicted_band] += 1
                if predicted_band == str(case["actual_motion_band"]):
                    matches += 1
                if sign["value"] == str(case["actual_motion_sign"]):
                    sign_matches += 1
        if source == "BORROWED" or case["topology_name"] == target_world:
            seen_by_key[key].append(case)
    return {
        "recipe": recipe_name,
        "source": source,
        "horizon": horizon,
        "features": list(features),
        "test_count": test_count,
        "call_count": call_count,
        "call_rate": percent(call_count, test_count),
        "band_matches": matches,
        "band_match_rate": percent(matches, call_count),
        "sign_matches": sign_matches,
        "sign_match_rate": percent(sign_matches, call_count),
        "predicted_band_rank": ranked(predicted_rank),
        "actual_band_rank": ranked(actual_rank),
    }


def candidate_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -float(row["band_match_rate"]),
        -float(row["sign_match_rate"]),
        -int(row["call_count"]),
        row["recipe"],
        row["source"],
        row["horizon"],
    )


def build_audit(
    cases: list[dict[str, Any]],
    *,
    target_worlds: list[str],
    recipe_names: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
    min_calls: int,
) -> dict[str, Any]:
    recipes = {
        name: BAND_FEATURE_RECIPES[name]
        for name in recipe_names
        if name in BAND_FEATURE_RECIPES
    }
    world_reports = []
    for world in target_worlds:
        candidates = []
        for recipe_name, features in recipes.items():
            for source in ("WORLD", "BORROWED"):
                for horizon in horizons:
                    candidates.append(
                        evaluate_band_recipe(
                            cases,
                            target_world=world,
                            recipe_name=recipe_name,
                            features=features,
                            source=source,
                            horizon=horizon,
                            min_prior=min_prior,
                        )
                    )
        candidates.sort(key=candidate_sort_key)
        useful = [
            row
            for row in candidates
            if int(row["call_count"]) >= min_calls
        ]
        useful.sort(key=candidate_sort_key)
        world_reports.append(
            {
                "topology_name": world,
                "selected_band_candidate": candidates[0] if candidates else None,
                "selected_useful_band_candidate": useful[0] if useful else None,
                "top_band_candidates": candidates[:50],
                "top_useful_band_candidates": useful[:50],
            }
        )
    world_reports.sort(
        key=lambda row: (
            candidate_sort_key(row["selected_useful_band_candidate"])
            if row["selected_useful_band_candidate"]
            else (999,),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "MOTION_BAND_RESOLVER_AUDIT",
        "min_prior": min_prior,
        "min_calls": min_calls,
        "horizons": list(horizons),
        "world_count": len(world_reports),
        "world_reports": world_reports,
        "notes": [
            "This audit tests motion band prediction separately from branch selection.",
            "Motion amount becomes tight only after branch + sign + band are correct.",
            "Only prior matching rows are used; no future actual band is used as input.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Motion Band Resolver Audit",
        description="Audit live-safe historical rooms for outgoing motion band prediction.",
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
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--min-calls", type=int, default=10)
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
    recipe_names = tuple(
        part.strip()
        for part in args.recipes.split(",")
        if part.strip()
    ) or tuple(BAND_FEATURE_RECIPES)
    payload = build_audit(
        enriched_cases(args.csv_path, args.from_date),
        target_worlds=worlds,
        recipe_names=recipe_names,
        horizons=horizons,
        min_prior=args.min_prior,
        min_calls=args.min_calls,
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
                                "selected_useful_band_candidate"
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
