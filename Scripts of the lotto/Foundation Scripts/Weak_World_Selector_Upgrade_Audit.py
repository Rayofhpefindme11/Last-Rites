from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH, parse_draw_date
from Branch_Selector_Lookback_Audit import (
    SEATS,
    build_cases,
    percent,
    ranked,
    recipe_sort_key,
    selector_promotion,
    selector_sample_warning,
    summarize_records,
)
from Seat_Taxonomy import seat_family


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_AUDIT = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "branch_selector_lookback_audit_2015-10-07.json"
)
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "weak_world_selector_upgrade_audit_2015-10-07.json"
)
DEFAULT_HORIZONS = (1, 2, 3, 5, 8, 13, 21, 34)


LIVE_SAFE_FEATURE_RECIPES: dict[str, tuple[str, ...]] = {
    "AUTHORITY": ("authority_seat",),
    "AUTHORITY_ORIGIN": ("authority_seat", "authority_origin"),
    "AUTHORITY_INCOMING": (
        "authority_seat",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "DOMINANT_ORIGIN_INCOMING": (
        "dominant_origin_seat",
        "authority_origin",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "AUTHORITY_INCOMING_FAMILY": (
        "authority_seat",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_draw_family",
        "incoming_energy_class",
    ),
    "PRESSURE_TOPOLOGY": (
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "PRESSURE_BODY": (
        "pressure_shape",
        "set_relation",
        "middle_pressure",
        "edge_pressure",
    ),
    "PRESSURE_FUSION_BODY": (
        "pressure_fusion",
        "pressure_shape",
        "middle_pressure",
        "edge_pressure",
    ),
    "BURDEN": (
        "highest_burden_seat",
        "highest_burden_level",
        "highest_burden_state",
    ),
    "BURDEN_ORIGIN": (
        "highest_burden_seat",
        "highest_burden_state",
        "dominant_origin_seat",
        "authority_origin",
    ),
    "COLLISION": ("collision_seat", "collision_type"),
    "COLLISION_AUTHORITY": (
        "collision_seat",
        "collision_type",
        "authority_seat",
        "authority_origin",
    ),
    "COLLISION_INCOMING": (
        "collision_seat",
        "collision_type",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "COLLISION_FACE": (
        "collision_seat",
        "collision_type",
        "face_family",
        "turn_lanes",
    ),
    "COLLISION_BURDEN": (
        "collision_seat",
        "collision_type",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "COLLISION_BURDEN_ORIGIN": (
        "collision_seat",
        "collision_type",
        "highest_burden_seat",
        "highest_burden_state",
        "dominant_origin_seat",
        "authority_origin",
    ),
    "COLLISION_PRESSURE_TOPOLOGY": (
        "collision_seat",
        "collision_type",
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "COLLISION_PRESSURE_BODY": (
        "collision_seat",
        "collision_type",
        "pressure_shape",
        "set_relation",
        "middle_pressure",
        "edge_pressure",
    ),
    "FACE_TURNS": ("face_family", "turn_lanes"),
    "FACE_INCOMING": (
        "face_family",
        "turn_lanes",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "BURDEN_FACE": (
        "highest_burden_seat",
        "highest_burden_state",
        "face_family",
        "turn_lanes",
    ),
    "BURDEN_PRESSURE_TOPOLOGY": (
        "highest_burden_seat",
        "highest_burden_state",
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "ORIGIN_PRESSURE_TOPOLOGY": (
        "dominant_origin_seat",
        "authority_origin",
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "AUTH_FACE": (
        "authority_seat",
        "authority_origin",
        "face_family",
        "turn_lanes",
    ),
    "AUTH_PRESSURE_BODY": (
        "authority_seat",
        "authority_origin",
        "pressure_shape",
        "set_relation",
        "middle_pressure",
        "edge_pressure",
    ),
    "PRESSURE_INCOMING": (
        "pressure_balance",
        "pressure_distribution",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "BODY_INCOMING": (
        "set_relation",
        "middle_pressure",
        "edge_pressure",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "AUTH_PRESSURE_INCOMING": (
        "authority_seat",
        "authority_origin",
        "pressure_balance",
        "pressure_distribution",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "AUTH_COLLISION_PRESSURE": (
        "authority_seat",
        "authority_origin",
        "collision_seat",
        "pressure_balance",
        "pressure_distribution",
    ),
    "AUTH_BURDEN_INCOMING": (
        "authority_seat",
        "authority_origin",
        "highest_burden_seat",
        "highest_burden_state",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "BURDEN_FACE_INCOMING": (
        "highest_burden_seat",
        "highest_burden_state",
        "face_family",
        "turn_lanes",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "PRESSURE_FUSION": (
        "pressure_fusion",
        "pressure_fusion_profile",
    ),
    "PRESSURE_FUSION_INCOMING": (
        "pressure_fusion",
        "pressure_fusion_profile",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "DRAW_FACE_35": (
        "draw_order_band_pattern",
        "draw_transfer_pattern",
        "draw_direction_pattern",
        "draw_max_abs_lane",
    ),
    "DRAW_ROUTE_35": (
        "draw_lane_band_path",
        "draw_transfer_pattern",
        "draw_style",
    ),
    "INCOMING_MOTION_35": (
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_motion_gauge_pattern",
        "incoming_motion_class_pattern",
    ),
    "AUTHORITY_INCOMING_35": (
        "authority_seat",
        "authority_origin",
        "authority_draw_lane",
        "authority_incoming_gauge",
        "authority_incoming_class",
    ),
    "PRESSURE_GAUGE_35": (
        "pressure_gauge_shape",
        "burden_gauge_shape",
        "dominant_pressure_gauge",
        "smallest_pressure_gauge",
    ),
    "BURDEN_GAUGE_35": (
        "highest_burden_seat",
        "highest_burden_gauge",
        "highest_burden_state",
        "smallest_burden_seat",
        "smallest_burden_gauge",
    ),
    "DRAW_PRESSURE_35": (
        "sorted_pressure",
        "draw_pressure",
        "pressure_flow",
        "pressure_gauge_shape",
        "burden_gauge_shape",
    ),
    "DRAW_INCOMING_PRESSURE_35": (
        "incoming_motion_gauge_pattern",
        "draw_order_band_pattern",
        "pressure_gauge_shape",
        "burden_gauge_shape",
    ),
    "TECHNICAL_SIGNATURE": ("technical_signature",),
    "WORLD_PREVIOUS_BRANCH": ("world_previous_branch",),
    "WORLD_PREVIOUS_FAMILY": ("world_previous_family",),
    "WORLD_PREVIOUS_BRANCH_INCOMING": (
        "world_previous_branch",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "WORLD_PREVIOUS_FAMILY_INCOMING": (
        "world_previous_family",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "WORLD_PREVIOUS_BRANCH_BURDEN": (
        "world_previous_branch",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "WORLD_PREVIOUS_FAMILY_BURDEN": (
        "world_previous_family",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "WORLD_FRESHEST_BRANCH_BURDEN": (
        "world_freshest_branch",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "WORLD_STALEST_BRANCH_BURDEN": (
        "world_stalest_branch",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "WORLD_BRANCH_STATE_COLLISION": (
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
        "collision_seat",
        "collision_type",
    ),
    "WORLD_BRANCH_STATE_PRESSURE": (
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
        "map_pressure_type",
        "pressure_balance",
        "pressure_distribution",
    ),
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def branch_family_or_none(branch: str | None) -> str:
    if branch in SEATS:
        return seat_family(str(branch))
    return "NONE"


def newest_seen(seen: dict[str, int], current_pos: int) -> tuple[str, int | None]:
    valid = {seat: pos for seat, pos in seen.items() if pos >= 0}
    if not valid:
        return "NONE", None
    seat, pos = max(valid.items(), key=lambda item: (item[1], item[0]))
    return seat, current_pos - pos


def oldest_seen(seen: dict[str, int], current_pos: int) -> tuple[str, int | None]:
    valid = {seat: pos for seat, pos in seen.items() if pos >= 0}
    if not valid:
        return "NONE", None
    seat, pos = min(valid.items(), key=lambda item: (item[1], item[0]))
    return seat, current_pos - pos


def age_band(age: int | None) -> str:
    if age is None:
        return "NONE"
    if age <= 1:
        return "AGE_1"
    if age <= 3:
        return "AGE_2_3"
    if age <= 5:
        return "AGE_4_5"
    if age <= 8:
        return "AGE_6_8"
    if age <= 13:
        return "AGE_9_13"
    return "AGE_14_PLUS"


def add_history_features(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    world_last_branch: dict[str, str] = {}
    world_last_seen: dict[str, dict[str, int]] = defaultdict(lambda: {seat: -1 for seat in SEATS})
    global_last_branch = "NONE"
    global_last_seen = {seat: -1 for seat in SEATS}

    for pos, case in enumerate(cases):
        world = str(case["topology_name"])
        world_seen = world_last_seen[world]
        world_freshest, world_freshest_age = newest_seen(world_seen, pos)
        world_stalest, world_stalest_age = oldest_seen(world_seen, pos)
        global_freshest, global_freshest_age = newest_seen(global_last_seen, pos)
        global_stalest, global_stalest_age = oldest_seen(global_last_seen, pos)
        row = dict(case)
        row.update(
            {
                "global_previous_branch": global_last_branch,
                "global_previous_family": branch_family_or_none(global_last_branch),
                "world_previous_branch": world_last_branch.get(world, "NONE"),
                "world_previous_family": branch_family_or_none(world_last_branch.get(world)),
                "world_freshest_branch": world_freshest,
                "world_freshest_family": branch_family_or_none(world_freshest),
                "world_freshest_age_band": age_band(world_freshest_age),
                "world_stalest_branch": world_stalest,
                "world_stalest_family": branch_family_or_none(world_stalest),
                "world_stalest_age_band": age_band(world_stalest_age),
                "global_freshest_branch": global_freshest,
                "global_freshest_family": branch_family_or_none(global_freshest),
                "global_freshest_age_band": age_band(global_freshest_age),
                "global_stalest_branch": global_stalest,
                "global_stalest_family": branch_family_or_none(global_stalest),
                "global_stalest_age_band": age_band(global_stalest_age),
            }
        )
        enriched.append(row)
        actual_branch = str(case["actual_branch"])
        world_last_branch[world] = actual_branch
        world_seen[actual_branch] = pos
        global_last_branch = actual_branch
        global_last_seen[actual_branch] = pos
    return enriched


def weak_worlds_from_audit(path: Path, promotions: set[str]) -> list[str]:
    payload = read_json(path)
    worlds = []
    for row in payload.get("world_selector_recipes", []):
        recipe = row.get("selected_recipe", {})
        if recipe.get("promotion") in promotions:
            worlds.append(str(row["topology_name"]))
    return worlds


def feature_key(case: dict[str, Any], features: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(str(case.get(feature, "NONE")) for feature in features)


def select_branch(rows: list[dict[str, Any]], min_prior: int) -> dict[str, Any]:
    if len(rows) < min_prior:
        return {
            "status": "NO_CALL",
            "predicted_branch": None,
            "prior_count": len(rows),
            "rank": [],
        }
    counts = Counter(str(row["actual_branch"]) for row in rows)
    branch, count = counts.most_common(1)[0]
    return {
        "status": "CALL",
        "predicted_branch": branch,
        "prior_count": len(rows),
        "predicted_count": count,
        "predicted_rate": percent(count, len(rows)),
        "rank": ranked(counts),
    }


def prediction_record(
    case: dict[str, Any],
    *,
    recipe_name: str,
    features: tuple[str, ...],
    horizon: int,
    selection: dict[str, Any],
) -> dict[str, Any]:
    predicted_branch = selection["predicted_branch"]
    branch_result = (
        "MATCH"
        if predicted_branch == case["actual_branch"]
        else "MISS"
        if predicted_branch is not None
        else "NO_CALL"
    )
    family_result = (
        "MATCH"
        if predicted_branch is not None
        and seat_family(str(predicted_branch)) == case["actual_family"]
        else "MISS"
        if predicted_branch is not None
        else "NO_CALL"
    )
    return {
        "date": case["date"],
        "index": case["index"],
        "topology_name": case["topology_name"],
        "recipe": recipe_name,
        "features": list(features),
        "horizon_type": "WORLD_FEATURE_OCCURRENCE",
        "horizon": horizon,
        "status": selection["status"],
        "prior_count": selection["prior_count"],
        "predicted_branch": predicted_branch,
        "actual_branch": case["actual_branch"],
        "branch_result": branch_result,
        "family_result": family_result,
        "rank": selection["rank"][:5],
    }


def evaluate_world_recipe(
    world_cases: list[dict[str, Any]],
    recipe_name: str,
    features: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
) -> list[dict[str, Any]]:
    records_by_horizon: dict[int, list[dict[str, Any]]] = {horizon: [] for horizon in horizons}
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)

    for case in world_cases:
        key = feature_key(case, features)
        prior_matches = seen_by_key[key]
        for horizon in horizons:
            selection = select_branch(prior_matches[-horizon:], min_prior=min_prior)
            records_by_horizon[horizon].append(
                prediction_record(
                    case,
                    recipe_name=recipe_name,
                    features=features,
                    horizon=horizon,
                    selection=selection,
                )
            )
        prior_matches.append(case)
    rows = []
    for horizon, records in records_by_horizon.items():
        summary = summarize_records(records)
        candidate = {
            "selector_source": "WEAK_WORLD_FEATURE_RECIPE",
            "signal": recipe_name,
            "horizon_type": "WORLD_FEATURE_OCCURRENCE",
            "horizon": horizon,
            "topology_name": world_cases[0]["topology_name"],
            "features": list(features),
            **summary,
        }
        candidate["promotion"] = selector_promotion(candidate)
        candidate["sample_warning"] = selector_sample_warning(candidate)
        rows.append(candidate)
    return rows


def evaluate_borrowed_recipe(
    cases: list[dict[str, Any]],
    target_world: str,
    recipe_name: str,
    features: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
) -> list[dict[str, Any]]:
    records_by_horizon: dict[int, list[dict[str, Any]]] = {horizon: [] for horizon in horizons}
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)

    for case in cases:
        key = feature_key(case, features)
        prior_matches = seen_by_key[key]
        if case["topology_name"] == target_world:
            for horizon in horizons:
                selection = select_branch(prior_matches[-horizon:], min_prior=min_prior)
                record = prediction_record(
                    case,
                    recipe_name=recipe_name,
                    features=features,
                    horizon=horizon,
                    selection=selection,
                )
                record["horizon_type"] = "BORROWED_ANALOG_OCCURRENCE"
                records_by_horizon[horizon].append(record)
        prior_matches.append(case)

    rows = []
    for horizon, records in records_by_horizon.items():
        summary = summarize_records(records)
        candidate = {
            "selector_source": "BORROWED_ANALOG_FEATURE_RECIPE",
            "signal": recipe_name,
            "horizon_type": "BORROWED_ANALOG_OCCURRENCE",
            "horizon": horizon,
            "topology_name": target_world,
            "features": list(features),
            **summary,
        }
        candidate["promotion"] = selector_promotion(candidate)
        candidate["sample_warning"] = selector_sample_warning(candidate)
        rows.append(candidate)
    return rows


def motion_range(rows: list[dict[str, Any]]) -> dict[str, Any]:
    motions = [int(row["actual_motion"]) for row in rows]
    abs_motions = [abs(value) for value in motions]
    signs = Counter("+" if value > 0 else "-" if value < 0 else "0" for value in motions)
    lanes = Counter(str(row["actual_lane"]) for row in rows)
    return {
        "count": len(rows),
        "signed_motion_min": min(motions),
        "signed_motion_max": max(motions),
        "signed_motion_median": median(motions),
        "abs_motion_min": min(abs_motions),
        "abs_motion_max": max(abs_motions),
        "abs_motion_median": median(abs_motions),
        "sign_rank": ranked(signs),
        "lane_rank": ranked(lanes),
        "top_motion_values": ranked(Counter(str(value) for value in motions))[:10],
    }


def world_range_profiles(world_cases: list[dict[str, Any]], min_sample: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in world_cases:
        grouped[str(case["actual_branch"])].append(case)
    profiles = []
    for branch, rows in grouped.items():
        if len(rows) < min_sample:
            continue
        profile = motion_range(rows)
        profile["branch"] = branch
        profiles.append(profile)
    profiles.sort(key=lambda row: (-row["count"], row["branch"]))
    return profiles


def build_upgrade_audit(
    cases: list[dict[str, Any]],
    worlds: list[str],
    horizons: tuple[int, ...],
    min_prior: int,
    range_min_sample: int,
) -> dict[str, Any]:
    cases = add_history_features(cases)
    cases_by_world: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        if case["topology_name"] in worlds:
            cases_by_world[str(case["topology_name"])].append(case)

    world_reports = []
    status_counts: Counter[str] = Counter()
    for world in sorted(worlds):
        world_cases = cases_by_world.get(world, [])
        if not world_cases:
            continue
        candidates = []
        for recipe_name, features in LIVE_SAFE_FEATURE_RECIPES.items():
            candidates.extend(
                evaluate_world_recipe(
                    world_cases,
                    recipe_name,
                    features,
                    horizons=horizons,
                    min_prior=min_prior,
                )
            )
            candidates.extend(
                evaluate_borrowed_recipe(
                    cases,
                    world,
                    recipe_name,
                    features,
                    horizons=horizons,
                    min_prior=min_prior,
                )
            )
        candidates.sort(key=recipe_sort_key)
        selected = candidates[0] if candidates else None
        if selected is not None:
            status_counts[str(selected["promotion"])] += 1
        world_reports.append(
            {
                "topology_name": world,
                "case_count": len(world_cases),
                "actual_branch_rank": ranked(Counter(str(row["actual_branch"]) for row in world_cases)),
                "actual_family_rank": ranked(Counter(str(row["actual_family"]) for row in world_cases)),
                "selected_upgrade_recipe": selected,
                "top_upgrade_candidates": candidates[:12],
                "range_profiles": world_range_profiles(
                    world_cases,
                    min_sample=range_min_sample,
                ),
            }
        )
    world_reports.sort(
        key=lambda row: (
            recipe_sort_key(row["selected_upgrade_recipe"])
            if row["selected_upgrade_recipe"]
            else (999,),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "WEAK_WORLD_SELECTOR_UPGRADE_AUDIT",
        "case_count": sum(len(rows) for rows in cases_by_world.values()),
        "world_count": len(world_reports),
        "worlds": worlds,
        "horizons": list(horizons),
        "min_prior": min_prior,
        "upgrade_status_counts": dict(status_counts),
        "world_reports": world_reports,
        "feature_recipe_catalog": {
            name: list(features)
            for name, features in LIVE_SAFE_FEATURE_RECIPES.items()
        },
        "notes": [
            "Only live-safe selector fields are tested.",
            "Future-only outgoing fields are excluded from selector recipes.",
            "WORLD_FEATURE_OCCURRENCE means last N prior appearances of the same feature key inside that world.",
            "Promotion means the candidate is useful enough to guide the branch selector, not that the world is solved permanently.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Weak World Selector Upgrade Audit",
        description="Find per-world missing branch selector signals for weak pressure worlds.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--input-audit", type=Path, default=DEFAULT_INPUT_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--horizons", default="1,2,3,5,8,13,21,34")
    parser.add_argument("--min-prior", type=int, default=1)
    parser.add_argument("--range-min-sample", type=int, default=5)
    parser.add_argument(
        "--promotions",
        default="DIRECTIONAL_SELECTOR,OBSERVATION_ONLY",
        help="Comma-separated selected-recipe promotions to upgrade.",
    )
    parser.add_argument(
        "--worlds",
        default=None,
        help="Optional comma-separated world list. Overrides --promotions.",
    )
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    horizons = tuple(
        int(part.strip())
        for part in args.horizons.split(",")
        if part.strip()
    )
    if not horizons or any(horizon < 1 for horizon in horizons):
        raise ValueError("--horizons must contain positive integers.")
    if args.min_prior < 1:
        raise ValueError("--min-prior must be at least 1.")

    if args.worlds:
        worlds = [part.strip() for part in args.worlds.split(",") if part.strip()]
    else:
        promotions = {part.strip() for part in args.promotions.split(",") if part.strip()}
        worlds = weak_worlds_from_audit(args.input_audit, promotions)

    cases = build_cases(args.csv_path, parse_draw_date(args.from_date))
    audit = build_upgrade_audit(
        cases,
        worlds=worlds,
        horizons=horizons,
        min_prior=args.min_prior,
        range_min_sample=args.range_min_sample,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    if args.print_summary:
        print(json.dumps(
            {
                "output": str(args.output),
                "world_count": audit["world_count"],
                "case_count": audit["case_count"],
                "upgrade_status_counts": audit["upgrade_status_counts"],
                "selected": [
                    {
                        "world": row["topology_name"],
                        "case_count": row["case_count"],
                        "recipe": row["selected_upgrade_recipe"],
                    }
                    for row in audit["world_reports"]
                ],
            },
            indent=2,
        ))


if __name__ == "__main__":
    main()
