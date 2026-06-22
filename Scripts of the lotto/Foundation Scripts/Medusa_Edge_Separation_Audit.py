from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Branch_Selector_Lookback_Audit import percent, ranked, summarize_records
from Range_Selector_Confirmation_Audit import (
    enriched_cases,
    majority_value,
    selected_recipes,
)
from Weak_World_Selector_Upgrade_Audit import (
    DEFAULT_OUTPUT_PATH as DEFAULT_SELECTOR_AUDIT,
    feature_key,
    select_branch,
)
from Seat_Taxonomy import seat_family


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "medusa_edge_separation_audit_min2_2015-10-07.json"
)

EDGE_SEATS = {"S1", "S5"}
DEFAULT_HORIZONS = (2, 3, 5, 8, 13, 21, 34)

EDGE_FEATURE_RECIPES: dict[str, tuple[str, ...]] = {
    "EDGE_PRESSURE_BALANCE": (
        "pressure_balance",
        "edge_pressure",
    ),
    "EDGE_PRESSURE_BODY": (
        "pressure_shape",
        "set_relation",
        "middle_pressure",
        "edge_pressure",
    ),
    "EDGE_PRESSURE_TOPOLOGY": (
        "map_pressure_type",
        "pressure_center",
        "pressure_balance",
        "pressure_distribution",
    ),
    "EDGE_INCOMING": (
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "EDGE_FACE_INCOMING": (
        "face_family",
        "turn_lanes",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "EDGE_AUTHORITY_INCOMING": (
        "authority_seat",
        "authority_origin",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "EDGE_DOMINANT_ORIGIN_INCOMING": (
        "dominant_origin_seat",
        "authority_origin",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "EDGE_BURDEN": (
        "highest_burden_seat",
        "highest_burden_level",
        "highest_burden_state",
    ),
    "EDGE_BURDEN_FACE": (
        "highest_burden_seat",
        "highest_burden_state",
        "face_family",
        "turn_lanes",
    ),
    "EDGE_BURDEN_INCOMING": (
        "highest_burden_seat",
        "highest_burden_state",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "EDGE_BURDEN_ORIGIN": (
        "highest_burden_seat",
        "highest_burden_state",
        "dominant_origin_seat",
        "authority_origin",
    ),
    "EDGE_WORLD_HISTORY": (
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
    ),
    "EDGE_WORLD_HISTORY_INCOMING": (
        "world_previous_branch",
        "world_freshest_branch",
        "world_stalest_branch",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "EDGE_GLOBAL_HISTORY": (
        "global_previous_branch",
        "global_freshest_branch",
        "global_stalest_branch",
    ),
    "EDGE_GLOBAL_HISTORY_INCOMING": (
        "global_previous_branch",
        "global_freshest_branch",
        "global_stalest_branch",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
    "EDGE_COLLISION_AUTHORITY": (
        "collision_seat",
        "collision_type",
        "authority_seat",
        "authority_origin",
    ),
    "EDGE_COLLISION_BURDEN_FACE": (
        "collision_seat",
        "collision_type",
        "highest_burden_seat",
        "highest_burden_state",
        "face_family",
        "turn_lanes",
    ),
    "EDGE_FUSION_INCOMING": (
        "pressure_fusion",
        "pressure_fusion_profile",
        "incoming_draw_sign",
        "dominant_incoming_draw_lane",
    ),
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_branch_range_reads(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    branch_recipe: dict[str, Any],
    range_features: tuple[str, ...],
    range_horizon: int,
    min_prior: int,
) -> list[dict[str, Any]]:
    branch_source = (
        "WORLD"
        if branch_recipe["selector_source"] == "WEAK_WORLD_FEATURE_RECIPE"
        else "BORROWED"
    )
    branch_features = tuple(branch_recipe["features"])
    branch_horizon = int(branch_recipe["horizon"])
    branch_seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    range_seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)

    reads = []
    for case in cases:
        branch_key = feature_key(case, branch_features)
        range_key = feature_key(case, range_features)
        if case["topology_name"] != target_world:
            if branch_source == "BORROWED":
                branch_seen_by_key[branch_key].append(case)
            continue

        branch_rows = branch_seen_by_key[branch_key][-branch_horizon:]
        branch_selection = select_branch(branch_rows, min_prior=min_prior)
        predicted_branch = branch_selection["predicted_branch"]
        predicted_family = (
            seat_family(str(predicted_branch))
            if predicted_branch is not None
            else None
        )
        range_rows = range_seen_by_key[range_key][-range_horizon:]
        sign = majority_value(range_rows, "actual_motion_sign", min_prior=min_prior)
        reads.append(
            {
                **case,
                "branch_status": branch_selection["status"],
                "branch_prior_count": branch_selection["prior_count"],
                "predicted_base_branch": predicted_branch,
                "predicted_family": predicted_family,
                "range_status": sign["status"],
                "range_prior_count": sign["prior_count"],
                "predicted_sign": sign["value"],
            }
        )
        if branch_source == "WORLD":
            branch_seen_by_key[branch_key].append(case)
        range_seen_by_key[range_key].append(case)
    return reads


def edge_selection(rows: list[dict[str, Any]], min_prior: int) -> dict[str, Any]:
    edge_rows = [row for row in rows if str(row["actual_branch"]) in EDGE_SEATS]
    if len(edge_rows) < min_prior:
        return {
            "status": "NO_CALL",
            "predicted_branch": None,
            "prior_count": len(edge_rows),
            "rank": [],
        }
    counts = Counter(str(row["actual_branch"]) for row in edge_rows)
    branch, count = counts.most_common(1)[0]
    return {
        "status": "CALL",
        "predicted_branch": branch,
        "prior_count": len(edge_rows),
        "predicted_count": count,
        "predicted_rate": percent(count, len(edge_rows)),
        "rank": ranked(counts),
    }


def evaluate_edge_recipe(
    cases: list[dict[str, Any]],
    reads_by_index: dict[int, dict[str, Any]],
    *,
    target_world: str,
    recipe_name: str,
    features: tuple[str, ...],
    source: str,
    horizon: int,
    min_prior: int,
) -> list[dict[str, Any]]:
    records = []
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)

    for case in cases:
        key = feature_key(case, features)
        if case["topology_name"] != target_world:
            if source == "BORROWED":
                seen_by_key[key].append(case)
            continue

        read = reads_by_index[int(case["index"])]
        base_branch = read["predicted_base_branch"]
        predicted_branch = base_branch
        edge_override = {
            "status": "SKIPPED",
            "predicted_branch": None,
            "prior_count": 0,
            "rank": [],
        }
        if (
            read["branch_status"] == "CALL"
            and read["range_status"] == "CALL"
            and read["predicted_family"] == "EDGE_FAMILY"
        ):
            prior_rows = [
                row
                for row in seen_by_key[key][-horizon:]
                if row.get("actual_family") == "EDGE_FAMILY"
                and (
                    not read["predicted_sign"]
                    or row.get("actual_motion_sign") == read["predicted_sign"]
                )
            ]
            edge_override = edge_selection(prior_rows, min_prior=min_prior)
            if edge_override["status"] == "CALL":
                predicted_branch = edge_override["predicted_branch"]

        status = (
            "CALL"
            if read["branch_status"] == "CALL"
            and read["range_status"] == "CALL"
            and predicted_branch is not None
            else "NO_CALL"
        )
        branch_result = (
            "MATCH"
            if predicted_branch == case["actual_branch"]
            else "MISS"
            if predicted_branch is not None
            else "NO_CALL"
        )
        family_result = (
            "MATCH"
            if read["predicted_family"] == case["actual_family"]
            else "MISS"
            if read["predicted_family"] is not None
            else "NO_CALL"
        )
        sign_result = (
            "MATCH"
            if read["predicted_sign"] == case["actual_motion_sign"]
            else "MISS"
            if read["predicted_sign"] is not None
            else "NO_CALL"
        )
        records.append(
            {
                "date": case["date"],
                "index": case["index"],
                "topology_name": target_world,
                "status": status,
                "branch_result": branch_result,
                "family_result": family_result,
                "sign_result": sign_result,
                "prior_count": min(
                    int(read["branch_prior_count"] or 0),
                    int(read["range_prior_count"] or 0),
                    int(edge_override["prior_count"] or 0)
                    if edge_override["status"] == "CALL"
                    else int(read["range_prior_count"] or 0),
                ),
                "actual_branch": case["actual_branch"],
                "actual_family": case["actual_family"],
                "actual_motion": case["actual_motion"],
                "actual_motion_sign": case["actual_motion_sign"],
                "base_predicted_branch": base_branch,
                "predicted_branch": predicted_branch,
                "predicted_family": read["predicted_family"],
                "predicted_sign": read["predicted_sign"],
                "edge_override_status": edge_override["status"],
                "edge_override_prior_count": edge_override["prior_count"],
                "edge_override_rank": edge_override["rank"][:5],
            }
        )
        if source == "WORLD":
            seen_by_key[key].append(case)
    return records


def summarize_edge_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    summary = summarize_records(records)
    calls = [row for row in records if row["status"] == "CALL"]
    edge_calls = [
        row
        for row in calls
        if row["predicted_family"] == "EDGE_FAMILY"
    ]
    edge_exact = sum(1 for row in edge_calls if row["branch_result"] == "MATCH")
    sign_matches = sum(1 for row in calls if row["sign_result"] == "MATCH")
    overrides = [
        row
        for row in records
        if row["edge_override_status"] == "CALL"
    ]
    return {
        **summary,
        "edge_call_count": len(edge_calls),
        "edge_exact_matches": edge_exact,
        "edge_exact_match_rate": percent(edge_exact, len(edge_calls)),
        "sign_matches": sign_matches,
        "sign_match_rate": percent(sign_matches, len(calls)),
        "override_count": len(overrides),
    }


def build_audit(
    cases: list[dict[str, Any]],
    *,
    selector_audit: Path,
    target_world: str,
    horizons: tuple[int, ...],
    min_prior: int,
    min_calls: int,
) -> dict[str, Any]:
    branch_recipe = selected_recipes(selector_audit)[target_world]
    range_features = (
        "highest_burden_seat",
        "highest_burden_state",
        "face_family",
        "turn_lanes",
    )
    reads = build_branch_range_reads(
        cases,
        target_world=target_world,
        branch_recipe=branch_recipe,
        range_features=range_features,
        range_horizon=3,
        min_prior=min_prior,
    )
    reads_by_index = {int(row["index"]): row for row in reads}
    candidates = []
    for recipe_name, features in EDGE_FEATURE_RECIPES.items():
        for source in ("WORLD", "BORROWED"):
            for horizon in horizons:
                records = evaluate_edge_recipe(
                    cases,
                    reads_by_index,
                    target_world=target_world,
                    recipe_name=recipe_name,
                    features=features,
                    source=source,
                    horizon=horizon,
                    min_prior=min_prior,
                )
                candidates.append(
                    {
                        "edge_recipe": recipe_name,
                        "edge_source": source,
                        "edge_horizon": horizon,
                        "edge_features": list(features),
                        **summarize_edge_records(records),
                    }
                )
    candidates.sort(
        key=lambda row: (
            -float(row["branch_match_rate"]),
            -float(row["edge_exact_match_rate"]),
            -float(row["family_match_rate"]),
            -float(row["sign_match_rate"]),
            -int(row["call_count"]),
            row["edge_recipe"],
            row["edge_source"],
            row["edge_horizon"],
        )
    )
    useful = [
        row
        for row in candidates
        if int(row["call_count"]) >= min_calls
    ]
    useful.sort(
        key=lambda row: (
            -float(row["branch_match_rate"]),
            -float(row["edge_exact_match_rate"]),
            -float(row["family_match_rate"]),
            -float(row["sign_match_rate"]),
            -int(row["call_count"]),
            row["edge_recipe"],
            row["edge_source"],
            row["edge_horizon"],
        )
    )
    base_edge_cases = [
        row
        for row in reads
        if row["branch_status"] == "CALL"
        and row["range_status"] == "CALL"
        and row["predicted_family"] == "EDGE_FAMILY"
    ]
    edge_actual_rank = Counter(str(row["actual_branch"]) for row in base_edge_cases)
    return {
        "audit_name": "MEDUSA_EDGE_SEPARATION_AUDIT",
        "target_world": target_world,
        "min_prior": min_prior,
        "min_calls": min_calls,
        "branch_recipe": branch_recipe,
        "range_recipe": {
            "range_recipe": "BURDEN_FACE",
            "range_source": "WORLD",
            "range_horizon": 3,
            "range_features": list(range_features),
        },
        "base_edge_call_count": len(base_edge_cases),
        "base_edge_actual_rank": ranked(edge_actual_rank),
        "selected_edge_candidate": candidates[0] if candidates else None,
        "selected_useful_edge_candidate": useful[0] if useful else None,
        "top_edge_candidates": candidates[:50],
        "top_useful_edge_candidates": useful[:50],
        "notes": [
            "This audit only tests live-safe fields.",
            "The edge override is only allowed when the branch selector predicts EDGE_FAMILY.",
            "Candidate rows are selected from prior matching rooms only; no future outgoing value is used.",
            "The current Medusa baseline is COLLISION_AUTHORITY branch family plus BURDEN_FACE signed range.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Medusa Edge Separation Audit",
        description="Find live-safe fields that separate Medusa S1/S5 edge flips.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--selector-audit", type=Path, default=DEFAULT_SELECTOR_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--world", default="Medusa")
    parser.add_argument("--horizons", default="2,3,5,8,13,21,34")
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--min-calls", type=int, default=10)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    horizons = tuple(
        int(part.strip())
        for part in args.horizons.split(",")
        if part.strip()
    )
    payload = build_audit(
        enriched_cases(args.csv_path, args.from_date),
        selector_audit=args.selector_audit,
        target_world=args.world,
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
                    "base_edge_call_count": payload["base_edge_call_count"],
                    "base_edge_actual_rank": payload["base_edge_actual_rank"],
                    "selected_edge_candidate": payload["selected_edge_candidate"],
                    "selected_useful_edge_candidate": payload[
                        "selected_useful_edge_candidate"
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
