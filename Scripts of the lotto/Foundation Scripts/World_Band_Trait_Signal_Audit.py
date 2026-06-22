from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Branch_Selector_Lookback_Audit import percent, ranked
from Range_Selector_Confirmation_Audit import enriched_cases, majority_value


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "world_band_trait_signal_audit_min2_2015-10-07.json"
)

DEFAULT_WORLDS = (
    "Altera",
    "Nova",
    "Citrine",
    "Lumina",
    "Alcides",
    "Artoria",
    "Medusa",
    "Suzuka",
    "Circe",
    "Nirvana",
)
DEFAULT_HORIZONS = (2, 3, 5, 8, 13, 21, 34)

CURRENT_SIGNAL_RECIPES: dict[str, tuple[str, ...]] = {
    "CURRENT_AUTHORITY": ("authority_seat", "authority_origin"),
    "CURRENT_PRESSURE_TOPOLOGY": (
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "CURRENT_PRESSURE_BODY": (
        "pressure_shape",
        "set_relation",
        "middle_pressure",
        "edge_pressure",
    ),
    "CURRENT_BURDEN": (
        "highest_burden_seat",
        "highest_burden_level",
        "highest_burden_state",
    ),
    "CURRENT_BURDEN_ORIGIN": (
        "highest_burden_seat",
        "highest_burden_state",
        "dominant_origin_seat",
        "authority_origin",
    ),
    "CURRENT_INCOMING": (
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_draw_family",
        "incoming_energy_class",
    ),
    "CURRENT_INCOMING_35": (
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_motion_gauge_pattern",
        "incoming_motion_class_pattern",
    ),
    "CURRENT_AUTHORITY_INCOMING_35": (
        "authority_seat",
        "authority_origin",
        "authority_draw_lane",
        "authority_incoming_gauge",
        "authority_incoming_class",
    ),
    "CURRENT_DRAW_FACE_35": (
        "draw_order_band_pattern",
        "draw_transfer_pattern",
        "draw_direction_pattern",
        "draw_max_abs_lane",
    ),
    "CURRENT_DRAW_ROUTE_35": (
        "draw_lane_band_path",
        "draw_transfer_pattern",
        "draw_style",
    ),
    "CURRENT_PRESSURE_GAUGE_35": (
        "pressure_gauge_shape",
        "burden_gauge_shape",
        "dominant_pressure_gauge",
        "smallest_pressure_gauge",
    ),
    "CURRENT_BURDEN_GAUGE_35": (
        "highest_burden_seat",
        "highest_burden_gauge",
        "highest_burden_state",
        "smallest_burden_seat",
        "smallest_burden_gauge",
    ),
    "CURRENT_DRAW_PRESSURE_35": (
        "sorted_pressure",
        "draw_pressure",
        "pressure_flow",
        "pressure_gauge_shape",
        "burden_gauge_shape",
    ),
    "CURRENT_FACE": ("face_family", "turn_lanes"),
    "CURRENT_FUSION": ("pressure_fusion", "pressure_fusion_profile"),
    "CURRENT_COLLISION": ("collision_seat", "collision_type"),
    "CURRENT_TECHNICAL": ("technical_signature",),
    "CURRENT_HISTORY": (
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
    ),
}

REFERENCE_SIGNAL_RECIPES: dict[str, tuple[str, ...]] = {
    "REF_BAND": ("ref_last_band",),
    "REF_BAND_BRANCH": ("ref_last_band", "ref_last_branch"),
    "REF_BAND_FAMILY": ("ref_last_band", "ref_last_family"),
    "REF_BAND_LANE": ("ref_last_band", "ref_last_lane"),
    "REF_BAND_SIGN": ("ref_last_band", "ref_last_sign"),
    "REF_BAND_AGE": ("ref_last_band", "ref_age_band"),
    "REF_TRAIT": (
        "ref_last_band",
        "ref_last_branch",
        "ref_last_lane",
        "ref_last_sign",
    ),
    "REF_BAND_CURRENT_AUTHORITY": (
        "ref_last_band",
        "authority_seat",
        "authority_origin",
    ),
    "REF_BAND_CURRENT_PRESSURE": (
        "ref_last_band",
        "map_pressure_type",
        "pressure_balance",
        "pressure_distribution",
    ),
    "REF_BAND_CURRENT_BURDEN": (
        "ref_last_band",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "REF_BAND_CURRENT_INCOMING": (
        "ref_last_band",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_energy_class",
    ),
    "REF_BAND_CURRENT_INCOMING_35": (
        "ref_last_band",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_motion_gauge_pattern",
        "incoming_motion_class_pattern",
    ),
    "REF_BAND_CURRENT_AUTHORITY_INCOMING_35": (
        "ref_last_band",
        "authority_seat",
        "authority_origin",
        "authority_draw_lane",
        "authority_incoming_gauge",
        "authority_incoming_class",
    ),
    "REF_BAND_CURRENT_DRAW_FACE_35": (
        "ref_last_band",
        "draw_order_band_pattern",
        "draw_transfer_pattern",
        "draw_direction_pattern",
        "draw_max_abs_lane",
    ),
    "REF_BAND_CURRENT_DRAW_ROUTE_35": (
        "ref_last_band",
        "draw_lane_band_path",
        "draw_transfer_pattern",
        "draw_style",
    ),
    "REF_BAND_CURRENT_PRESSURE_GAUGE_35": (
        "ref_last_band",
        "pressure_gauge_shape",
        "burden_gauge_shape",
        "dominant_pressure_gauge",
        "smallest_pressure_gauge",
    ),
    "REF_BAND_CURRENT_BURDEN_GAUGE_35": (
        "ref_last_band",
        "highest_burden_seat",
        "highest_burden_gauge",
        "highest_burden_state",
        "smallest_burden_seat",
        "smallest_burden_gauge",
    ),
    "REF_BAND_CURRENT_FACE": (
        "ref_last_band",
        "face_family",
        "turn_lanes",
    ),
    "REF_BAND_CURRENT_COLLISION": (
        "ref_last_band",
        "collision_seat",
        "collision_type",
    ),
    "REF_TRAIT_CURRENT_AUTHORITY": (
        "ref_last_band",
        "ref_last_branch",
        "ref_last_lane",
        "authority_seat",
        "authority_origin",
    ),
    "REF_TRAIT_CURRENT_PRESSURE": (
        "ref_last_band",
        "ref_last_branch",
        "ref_last_lane",
        "map_pressure_type",
        "pressure_balance",
        "pressure_distribution",
    ),
    "REF_TRAIT_CURRENT_BURDEN": (
        "ref_last_band",
        "ref_last_branch",
        "ref_last_lane",
        "highest_burden_seat",
        "highest_burden_state",
    ),
    "REF_TRAIT_CURRENT_INCOMING_35": (
        "ref_last_band",
        "ref_last_branch",
        "ref_last_lane",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
        "incoming_motion_gauge_pattern",
    ),
    "REF_TRAIT_CURRENT_DRAW_FACE_35": (
        "ref_last_band",
        "ref_last_branch",
        "ref_last_lane",
        "draw_order_band_pattern",
        "draw_transfer_pattern",
        "draw_max_abs_lane",
    ),
    "REF_TRAIT_CURRENT_BURDEN_GAUGE_35": (
        "ref_last_band",
        "ref_last_branch",
        "ref_last_lane",
        "highest_burden_seat",
        "highest_burden_gauge",
        "highest_burden_state",
    ),
}


def age_band(age: int | None) -> str:
    if age is None:
        return "NO_REF"
    if age <= 3:
        return "FRESH_1_3"
    if age <= 8:
        return "ACTIVE_4_8"
    if age <= 21:
        return "STALE_9_21"
    if age <= 55:
        return "OLD_22_55"
    return "DEEP_56_PLUS"


def value_tuple(row: dict[str, Any], features: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(str(row.get(feature, "NONE")) for feature in features)


def augmented_for_reference(
    case: dict[str, Any],
    *,
    ref_world: str | None,
    last_by_world: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    row = dict(case)
    ref = last_by_world.get(ref_world or "") if ref_world else None
    if ref is None:
        row.update(
            {
                "ref_world": ref_world or "NONE",
                "ref_last_band": "NO_REF",
                "ref_last_branch": "NO_REF",
                "ref_last_family": "NO_REF",
                "ref_last_lane": "NO_REF",
                "ref_last_sign": "NO_REF",
                "ref_last_motion": "NO_REF",
                "ref_age": "NO_REF",
                "ref_age_band": "NO_REF",
            }
        )
        return row
    age = int(case["index"]) - int(ref["index"])
    row.update(
        {
            "ref_world": ref_world,
            "ref_last_band": str(ref["actual_motion_band"]),
            "ref_last_branch": str(ref["actual_branch"]),
            "ref_last_family": str(ref["actual_family"]),
            "ref_last_lane": str(ref["actual_lane"]),
            "ref_last_sign": str(ref["actual_motion_sign"]),
            "ref_last_motion": str(ref["actual_motion"]),
            "ref_age": str(age),
            "ref_age_band": age_band(age),
        }
    )
    return row


def signal_quality(row: dict[str, Any] | None) -> str:
    if row is None:
        return "NO_CALL"
    calls = int(row.get("call_count", 0) or 0)
    call_rate = float(row.get("call_rate", 0.0) or 0.0)
    band_rate = float(row.get("band_match_rate", 0.0) or 0.0)
    if calls < 3:
        return "NO_CALL"
    if call_rate >= 60 and band_rate >= 65:
        return "TRAIT_STRONG"
    if call_rate >= 40 and band_rate >= 60:
        return "TRAIT_USABLE"
    if call_rate >= 25 and band_rate >= 55:
        return "TRAIT_DEVELOPING"
    if calls >= 5 and band_rate >= 70:
        return "TRAIT_SHARP_LOW_COVERAGE"
    if calls >= 5 and band_rate >= 60:
        return "TRAIT_SMALL"
    if calls >= 3 and band_rate >= 50:
        return "TRAIT_OBSERVE"
    return "TRAIT_WEAK"


QUALITY_RANK = {
    "TRAIT_STRONG": 7,
    "TRAIT_USABLE": 6,
    "TRAIT_DEVELOPING": 5,
    "TRAIT_SHARP_LOW_COVERAGE": 4,
    "TRAIT_SMALL": 3,
    "TRAIT_OBSERVE": 2,
    "TRAIT_WEAK": 1,
    "NO_CALL": 0,
}


def candidate_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    quality = signal_quality(row)
    return (
        -QUALITY_RANK[quality],
        -float(row["band_match_rate"]),
        -float(row["call_rate"]),
        -int(row["call_count"]),
        row["recipe"],
        row.get("ref_world") or "",
        row["source"],
        row["horizon"],
    )


def evaluate_signal_candidate(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    ref_world: str | None,
    recipe_name: str,
    features: tuple[str, ...],
    source: str,
    horizon: int,
    min_prior: int,
) -> dict[str, Any]:
    test_count = 0
    call_count = 0
    matches = 0
    prior_counts: list[int] = []
    predicted_rank: Counter[str] = Counter()
    actual_rank: Counter[str] = Counter()
    miss_rank: Counter[str] = Counter()
    key_rank: Counter[str] = Counter()
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    last_by_world: dict[str, dict[str, Any]] = {}

    for case in cases:
        row = augmented_for_reference(case, ref_world=ref_world, last_by_world=last_by_world)
        key = value_tuple(row, features)
        if str(case["topology_name"]) == target_world:
            test_count += 1
            actual_band = str(case["actual_motion_band"])
            actual_rank[actual_band] += 1
            prior_rows = seen_by_key[key][-horizon:]
            band = majority_value(prior_rows, "actual_motion_band", min_prior=min_prior)
            if band["status"] == "CALL":
                call_count += 1
                prior_counts.append(int(band.get("prior_count") or 0))
                predicted = str(band["value"])
                predicted_rank[predicted] += 1
                key_rank["|".join(key)] += 1
                if predicted == actual_band:
                    matches += 1
                else:
                    miss_rank[f"{predicted}->{actual_band}"] += 1

        if source == "BORROWED" or str(case["topology_name"]) == target_world:
            seen_by_key[key].append(case)
        last_by_world[str(case["topology_name"])] = case

    report = {
        "recipe": recipe_name,
        "ref_world": ref_world,
        "source": source,
        "horizon": horizon,
        "features": list(features),
        "test_count": test_count,
        "call_count": call_count,
        "call_rate": percent(call_count, test_count),
        "band_matches": matches,
        "band_match_rate": percent(matches, call_count),
        "avg_prior_count": round(sum(prior_counts) / len(prior_counts), 2)
        if prior_counts
        else 0.0,
        "predicted_band_rank": ranked(predicted_rank),
        "actual_band_rank": ranked(actual_rank),
        "key_rank": ranked(key_rank)[:10],
        "miss_rank": ranked(miss_rank)[:12],
    }
    report["quality"] = signal_quality(report)
    return report


def build_audit(
    cases: list[dict[str, Any]],
    *,
    target_worlds: tuple[str, ...],
    ref_worlds: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
    min_calls: int,
) -> dict[str, Any]:
    reports = []
    quality_counts: Counter[str] = Counter()
    for target_world in target_worlds:
        candidates = []
        for recipe_name, features in CURRENT_SIGNAL_RECIPES.items():
            for source in ("WORLD", "BORROWED"):
                for horizon in horizons:
                    candidates.append(
                        evaluate_signal_candidate(
                            cases,
                            target_world=target_world,
                            ref_world=None,
                            recipe_name=recipe_name,
                            features=features,
                            source=source,
                            horizon=horizon,
                            min_prior=min_prior,
                        )
                    )
        for ref_world in ref_worlds:
            for recipe_name, features in REFERENCE_SIGNAL_RECIPES.items():
                for source in ("WORLD", "BORROWED"):
                    for horizon in horizons:
                        candidates.append(
                            evaluate_signal_candidate(
                                cases,
                                target_world=target_world,
                                ref_world=ref_world,
                                recipe_name=recipe_name,
                                features=features,
                                source=source,
                                horizon=horizon,
                                min_prior=min_prior,
                            )
                        )
        useful = [row for row in candidates if int(row["call_count"]) >= min_calls]
        useful.sort(key=candidate_sort_key)
        candidates.sort(key=candidate_sort_key)
        selected = useful[0] if useful else candidates[0] if candidates else None
        quality = signal_quality(selected)
        quality_counts[quality] += 1
        reports.append(
            {
                "topology_name": target_world,
                "selected_trait_signal": selected,
                "selected_quality": quality,
                "top_trait_signal_candidates": useful[:40],
                "top_all_trait_signal_candidates": candidates[:40],
            }
        )
    reports.sort(
        key=lambda row: (
            candidate_sort_key(row["selected_trait_signal"])
            if row["selected_trait_signal"]
            else (999,),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "WORLD_BAND_TRAIT_SIGNAL_AUDIT",
        "min_prior": min_prior,
        "min_calls": min_calls,
        "horizons": list(horizons),
        "world_count": len(reports),
        "quality_counts": dict(quality_counts),
        "world_reports": reports,
        "notes": [
            "This audit looks for the small signal that chooses between split broad motion bands.",
            "Current recipes test the target world's current body, pressure, burden, face, collision, and history traits.",
            "Reference recipes test whether another world's last known motion trait helps select the target world's current band.",
            "Reference-world traits are live-safe because only prior historical outcomes are visible to the current row.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="World Band Trait Signal Audit",
        description="Find per-world signals that discriminate split broad motion bands.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument(
        "--worlds",
        default=",".join(DEFAULT_WORLDS),
        help="Comma-separated target worlds to audit.",
    )
    parser.add_argument(
        "--ref-worlds",
        default="",
        help="Comma-separated reference worlds. Empty means all topology names in the data.",
    )
    parser.add_argument("--horizons", default="2,3,5,8,13,21,34")
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--min-calls", type=int, default=3)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cases = enriched_cases(args.csv_path, args.from_date)
    target_worlds = tuple(part.strip() for part in args.worlds.split(",") if part.strip())
    ref_worlds = tuple(part.strip() for part in args.ref_worlds.split(",") if part.strip())
    if not ref_worlds:
        ref_worlds = tuple(sorted({str(row["topology_name"]) for row in cases}))
    horizons = tuple(int(part.strip()) for part in args.horizons.split(",") if part.strip())
    payload = build_audit(
        cases,
        target_worlds=target_worlds,
        ref_worlds=ref_worlds,
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
                            "selected": row["selected_trait_signal"],
                        }
                        for row in payload["world_reports"]
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
