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
from Seat_Taxonomy import seat_family
from Weak_World_Selector_Upgrade_Audit import feature_key, select_branch
from World_Motion_Selector_Board import DEFAULT_OUTPUT_PATH as DEFAULT_WORLD_MOTION_BOARD


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "world_band_preference_audit_min2_2015-10-07.json"
)

DEFAULT_HORIZONS = (2, 3, 5, 8, 13, 21, 34)
CONTEXT_MODES = ("BRANCH_SIGN", "FAMILY_SIGN", "SIGN_ONLY")

BAND_PREFERENCE_RECIPES: dict[str, tuple[str, ...]] = {
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
    "AUTHORITY_ORIGIN": (
        "authority_seat",
        "authority_origin",
    ),
    "AUTH_BURDEN": (
        "authority_seat",
        "authority_origin",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "INCOMING_ENERGY": (
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_draw_family",
        "incoming_energy_class",
    ),
    "FACE_INCOMING": (
        "face_family",
        "turn_lanes",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "FUSION_BODY": (
        "pressure_fusion",
        "pressure_fusion_profile",
        "pressure_shape",
        "middle_pressure",
        "edge_pressure",
    ),
    "HISTORY_PRESSURE": (
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
        "map_pressure_type",
        "pressure_balance",
        "pressure_distribution",
    ),
    "HISTORY_BURDEN": (
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "COLLISION_PRESSURE": (
        "collision_seat",
        "collision_type",
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "COLLISION_BURDEN": (
        "collision_seat",
        "collision_type",
        "highest_burden_seat",
        "highest_burden_state",
    ),
}


def selector_source(source: str | None) -> str:
    if source in {"WORLD", "WEAK_WORLD_FEATURE_RECIPE"}:
        return "WORLD"
    return "BORROWED"


def prior_rows(
    cases: list[dict[str, Any]],
    current_pos: int,
    *,
    target_world: str,
    features: tuple[str, ...],
    source: str,
    horizon: int,
) -> list[dict[str, Any]]:
    current = cases[current_pos]
    key = feature_key(current, features)
    rows = []
    for prior in cases[:current_pos]:
        if source == "WORLD" and prior["topology_name"] != target_world:
            continue
        if feature_key(prior, features) == key:
            rows.append(prior)
    return rows[-horizon:]


def predict_branch(
    cases: list[dict[str, Any]],
    current_pos: int,
    branch_selector: dict[str, Any],
    *,
    target_world: str,
    min_prior: int,
) -> dict[str, Any]:
    rows = prior_rows(
        cases,
        current_pos,
        target_world=target_world,
        features=tuple(branch_selector.get("features", [])),
        source=selector_source(branch_selector.get("source")),
        horizon=int(branch_selector.get("horizon") or 1),
    )
    selection = select_branch(rows, min_prior=min_prior)
    branch = selection["predicted_branch"]
    return {
        "status": selection["status"],
        "predicted_branch": branch,
        "predicted_family": seat_family(str(branch)) if branch else None,
        "prior_count": selection["prior_count"],
        "rank": selection["rank"],
    }


def predict_range_confirmation_branch(
    cases: list[dict[str, Any]],
    current_pos: int,
    branch_board_row: dict[str, Any],
    *,
    target_world: str,
    min_prior: int,
) -> dict[str, Any]:
    base = branch_board_row["base_candidate"]
    range_candidate = branch_board_row["range_candidate"]
    branch_rows = prior_rows(
        cases,
        current_pos,
        target_world=target_world,
        features=tuple(base.get("features", [])),
        source=selector_source(base.get("source")),
        horizon=int(base.get("horizon") or 1),
    )
    branch_selection = select_branch(branch_rows, min_prior=min_prior)
    first_branch = branch_selection["predicted_branch"]
    first_family = seat_family(str(first_branch)) if first_branch else None
    range_rows = prior_rows(
        cases,
        current_pos,
        target_world=target_world,
        features=tuple(range_candidate.get("features", [])),
        source=selector_source(range_candidate.get("source")),
        horizon=int(range_candidate.get("horizon") or 1),
    )
    sign = majority_value(range_rows, "actual_motion_sign", min_prior=min_prior)
    band = majority_value(range_rows, "actual_motion_band", min_prior=min_prior)
    final_mode = str(range_candidate.get("final_mode") or "SIGN")
    if first_family is None or sign["value"] is None:
        return {
            "status": "NO_CALL",
            "predicted_branch": None,
            "predicted_family": first_family,
            "prior_count": min(branch_selection["prior_count"], sign["prior_count"]),
            "rank": [],
        }
    target_rows = [
        row
        for row in cases[:current_pos]
        if row["topology_name"] == target_world
        and row["actual_family"] == first_family
        and row["actual_motion_sign"] == sign["value"]
        and (
            final_mode != "SIGN_BAND"
            or band["value"] is None
            or row["actual_motion_band"] == band["value"]
        )
    ]
    analog_rows = [
        row
        for row in cases[:current_pos]
        if row["actual_family"] == first_family
        and row["actual_motion_sign"] == sign["value"]
        and (
            final_mode != "SIGN_BAND"
            or band["value"] is None
            or row["actual_motion_band"] == band["value"]
        )
    ]
    final = select_branch(
        target_rows if len(target_rows) >= min_prior else analog_rows,
        min_prior=min_prior,
    )
    final_branch = final["predicted_branch"]
    return {
        "status": (
            "CALL"
            if branch_selection["status"] == "CALL"
            and sign["status"] == "CALL"
            and final["status"] == "CALL"
            else "NO_CALL"
        ),
        "predicted_branch": final_branch,
        "predicted_family": seat_family(str(final_branch)) if final_branch else first_family,
        "prior_count": min(
            int(branch_selection["prior_count"] or 0),
            int(sign["prior_count"] or 0),
            int(final["prior_count"] or 0),
        ),
        "rank": final["rank"],
    }


def predict_sign(
    cases: list[dict[str, Any]],
    current_pos: int,
    sign_selector: dict[str, Any] | None,
    *,
    target_world: str,
    min_prior: int,
) -> dict[str, Any]:
    if sign_selector is None:
        return {"status": "NO_CALL", "value": None, "prior_count": 0, "rank": []}
    rows = prior_rows(
        cases,
        current_pos,
        target_world=target_world,
        features=tuple(sign_selector.get("features", [])),
        source=selector_source(sign_selector.get("source")),
        horizon=int(sign_selector.get("horizon") or 1),
    )
    return majority_value(rows, "actual_motion_sign", min_prior=min_prior)


def context_values(
    row: dict[str, Any],
    *,
    mode: str,
    branch: str | None,
    family: str | None,
    sign: str | None,
    actual: bool,
) -> tuple[str, ...] | None:
    if actual:
        branch = str(row["actual_branch"])
        family = str(row["actual_family"])
        sign = str(row["actual_motion_sign"])
    if mode == "BRANCH_SIGN":
        if branch is None or sign is None:
            return None
        return (str(branch), str(sign))
    if mode == "FAMILY_SIGN":
        if family is None or sign is None:
            return None
        return (str(family), str(sign))
    if mode == "SIGN_ONLY":
        if sign is None:
            return None
        return (str(sign),)
    raise ValueError(f"Unknown context mode: {mode}")


def preference_key(
    row: dict[str, Any],
    *,
    features: tuple[str, ...],
    source: str,
    context_mode: str,
    branch: str | None = None,
    family: str | None = None,
    sign: str | None = None,
    actual: bool,
) -> tuple[str, ...] | None:
    context = context_values(
        row,
        mode=context_mode,
        branch=branch,
        family=family,
        sign=sign,
        actual=actual,
    )
    if context is None:
        return None
    world_part = () if source == "BORROWED" else (str(row["topology_name"]),)
    return world_part + context + feature_key(row, features)


def evaluate_preference_candidate(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    prediction_contexts: dict[int, dict[str, Any]],
    recipe_name: str,
    features: tuple[str, ...],
    source: str,
    context_mode: str,
    horizon: int,
    min_prior: int,
) -> dict[str, Any]:
    test_count = 0
    call_count = 0
    branch_calls = 0
    branch_matches = 0
    family_matches = 0
    sign_calls = 0
    sign_matches = 0
    band_matches = 0
    memory: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    predicted_band_rank: Counter[str] = Counter()
    actual_band_rank: Counter[str] = Counter()
    miss_rank: Counter[str] = Counter()

    for pos, case in enumerate(cases):
        if case["topology_name"] == target_world:
            test_count += 1
            actual_band_rank[str(case["actual_motion_band"])] += 1
            context = prediction_contexts[pos]
            branch_read = context["branch"]
            sign_read = context["sign"]
            if branch_read["status"] == "CALL":
                branch_calls += 1
                if branch_read["predicted_branch"] == case["actual_branch"]:
                    branch_matches += 1
                if branch_read["predicted_family"] == case["actual_family"]:
                    family_matches += 1
            if sign_read["status"] == "CALL":
                sign_calls += 1
                if sign_read["value"] == case["actual_motion_sign"]:
                    sign_matches += 1
            key = preference_key(
                case,
                features=features,
                source=source,
                context_mode=context_mode,
                branch=branch_read["predicted_branch"],
                family=branch_read["predicted_family"],
                sign=sign_read["value"],
                actual=False,
            )
            rows = memory[key][-horizon:] if key is not None else []
            band = majority_value(rows, "actual_motion_band", min_prior=min_prior)
            if (
                branch_read["status"] == "CALL"
                and sign_read["status"] == "CALL"
                and band["status"] == "CALL"
            ):
                call_count += 1
                predicted_band = str(band["value"])
                predicted_band_rank[predicted_band] += 1
                if predicted_band == str(case["actual_motion_band"]):
                    band_matches += 1
                else:
                    miss_rank[
                        f"{predicted_band}->{case['actual_motion_band']}"
                    ] += 1

        actual_key = preference_key(
            case,
            features=features,
            source=source,
            context_mode=context_mode,
            actual=True,
        )
        if actual_key is not None:
            memory[actual_key].append(case)

    return {
        "recipe": recipe_name,
        "source": source,
        "context_mode": context_mode,
        "horizon": horizon,
        "features": list(features),
        "test_count": test_count,
        "call_count": call_count,
        "call_rate": percent(call_count, test_count),
        "band_matches": band_matches,
        "band_match_rate": percent(band_matches, call_count),
        "branch_calls": branch_calls,
        "branch_match_rate": percent(branch_matches, branch_calls),
        "family_match_rate": percent(family_matches, branch_calls),
        "sign_calls": sign_calls,
        "sign_match_rate": percent(sign_matches, sign_calls),
        "predicted_band_rank": ranked(predicted_band_rank),
        "actual_band_rank": ranked(actual_band_rank),
        "miss_rank": ranked(miss_rank)[:12],
    }


def build_prediction_contexts(
    cases: list[dict[str, Any]],
    motion_board: dict[str, Any],
    branch_board: dict[str, Any],
    *,
    min_prior: int,
) -> dict[int, dict[str, Any]]:
    selectors_by_world = {
        str(row["topology_name"]): row
        for row in motion_board.get("world_reports", [])
    }
    branch_board_by_world = {
        str(row["topology_name"]): row
        for row in branch_board.get("world_reports", [])
    }
    contexts: dict[int, dict[str, Any]] = {}
    for pos, case in enumerate(cases):
        world = str(case["topology_name"])
        if world not in selectors_by_world:
            continue
        row = selectors_by_world[world]
        branch_board_row = branch_board_by_world.get(world)
        if row["branch_selector"].get("layer") == "RANGE_CONFIRMATION" and branch_board_row:
            branch_read = predict_range_confirmation_branch(
                cases,
                pos,
                branch_board_row,
                target_world=world,
                min_prior=min_prior,
            )
        else:
            branch_read = predict_branch(
                cases,
                pos,
                row["branch_selector"],
                target_world=world,
                min_prior=min_prior,
            )
        sign_read = predict_sign(
            cases,
            pos,
            row.get("sign_selector"),
            target_world=world,
            min_prior=min_prior,
        )
        contexts[pos] = {
            "branch": branch_read,
            "sign": sign_read,
        }
    return contexts


def band_quality(row: dict[str, Any] | None) -> str:
    if row is None:
        return "NO_CALL"
    calls = int(row.get("call_count", 0) or 0)
    rate = float(row.get("band_match_rate", 0.0) or 0.0)
    if calls >= 25 and rate >= 65:
        return "STRONG_BAND"
    if calls >= 10 and rate >= 55:
        return "USABLE_BAND"
    if calls >= 5 and rate >= 45:
        return "SMALL_BAND"
    if calls >= 3 and rate >= 45:
        return "OBSERVE_BAND"
    return "WEAK_BAND"


QUALITY_RANK = {
    "STRONG_BAND": 4,
    "USABLE_BAND": 3,
    "SMALL_BAND": 2,
    "OBSERVE_BAND": 1,
    "WEAK_BAND": 0,
    "NO_CALL": 0,
}


def candidate_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    quality = band_quality(row)
    return (
        -QUALITY_RANK[quality],
        -float(row["band_match_rate"]),
        -float(row["sign_match_rate"]),
        -float(row["family_match_rate"]),
        -int(row["call_count"]),
        row["recipe"],
        row["source"],
        row["context_mode"],
        row["horizon"],
    )


def build_audit(
    cases: list[dict[str, Any]],
    motion_board: dict[str, Any],
    branch_board: dict[str, Any],
    *,
    recipe_names: tuple[str, ...],
    context_modes: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
    min_calls: int,
) -> dict[str, Any]:
    recipes = {
        name: BAND_PREFERENCE_RECIPES[name]
        for name in recipe_names
        if name in BAND_PREFERENCE_RECIPES
    }
    reports = []
    quality_counts: dict[str, int] = {}
    prediction_contexts = build_prediction_contexts(
        cases,
        motion_board,
        branch_board,
        min_prior=min_prior,
    )
    for row in motion_board.get("world_reports", []):
        world = str(row["topology_name"])
        branch_selector = row["branch_selector"]
        sign_selector = row.get("sign_selector")
        candidates = []
        for recipe_name, features in recipes.items():
            for source in ("WORLD", "BORROWED"):
                for context_mode in context_modes:
                    for horizon in horizons:
                        candidates.append(
                            evaluate_preference_candidate(
                                cases,
                                target_world=world,
                                prediction_contexts=prediction_contexts,
                                recipe_name=recipe_name,
                                features=features,
                                source=source,
                                context_mode=context_mode,
                                horizon=horizon,
                                min_prior=min_prior,
                            )
                        )
        useful = [candidate for candidate in candidates if candidate["call_count"] >= min_calls]
        useful.sort(key=candidate_sort_key)
        candidates.sort(key=candidate_sort_key)
        selected = useful[0] if useful else candidates[0] if candidates else None
        quality = band_quality(selected)
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
        reports.append(
            {
                "topology_name": world,
                "branch_selector": branch_selector,
                "sign_selector": sign_selector,
                "selected_preference_band": selected,
                "selected_quality": quality,
                "top_preference_band_candidates": useful[:30],
                "top_all_preference_band_candidates": candidates[:30],
            }
        )
    reports.sort(
        key=lambda row: (
            candidate_sort_key(row["selected_preference_band"])
            if row["selected_preference_band"]
            else (999,),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "WORLD_BAND_PREFERENCE_AUDIT",
        "min_prior": min_prior,
        "min_calls": min_calls,
        "horizons": list(horizons),
        "context_modes": list(context_modes),
        "quality_counts": quality_counts,
        "world_count": len(reports),
        "world_reports": reports,
        "notes": [
            "This audit treats history as world behavior evidence, not as a copy table.",
            "Prior rows store actual branch/sign/band because those outcomes are known after history happens.",
            "Current rows query that memory using predicted branch and predicted sign from the current world motion board.",
            "A band call therefore tests whether the current condition maps to a historical preference room.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="World Band Preference Audit",
        description="Learn world-specific broad-band motion preferences from live-safe conditions.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--motion-board", type=Path, default=DEFAULT_WORLD_MOTION_BOARD)
    parser.add_argument("--branch-board", type=Path, default=DEFAULT_BRANCH_BOARD)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--horizons", default="2,3,5,8,13,21,34")
    parser.add_argument("--context-modes", default="BRANCH_SIGN,FAMILY_SIGN,SIGN_ONLY")
    parser.add_argument(
        "--recipes",
        default="",
        help="Optional comma-separated recipe names. Empty means all recipes.",
    )
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--min-calls", type=int, default=3)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    horizons = tuple(
        int(part.strip())
        for part in args.horizons.split(",")
        if part.strip()
    )
    context_modes = tuple(
        part.strip()
        for part in args.context_modes.split(",")
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
        context_modes=context_modes,
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
                    "quality_counts": payload["quality_counts"],
                    "world_reports": [
                        {
                            "world": row["topology_name"],
                            "quality": row["selected_quality"],
                            "selected": row["selected_preference_band"],
                        }
                        for row in payload["world_reports"]
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
