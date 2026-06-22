from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH, parse_draw_date
from Branch_Selector_Lookback_Audit import percent, ranked, summarize_records
from Weak_World_Selector_Upgrade_Audit import (
    DEFAULT_OUTPUT_PATH as DEFAULT_WEAK_AUDIT,
    LIVE_SAFE_FEATURE_RECIPES,
    add_history_features,
    build_cases,
    feature_key,
    select_branch,
)
from Seat_Taxonomy import seat_family


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "range_selector_confirmation_audit_min2_2015-10-07.json"
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def motion_sign(motion: int) -> str:
    if motion > 0:
        return "+"
    if motion < 0:
        return "-"
    return "0"


def motion_band(motion: int) -> str:
    amount = abs(motion)
    if amount <= 10:
        return "LIGHT_MOTION"
    if amount <= 20:
        return "CALM_MOTION"
    if amount <= 30:
        return "DIRECTED_MOTION"
    if amount <= 40:
        return "TRANSITIONAL_MOTION"
    if amount <= 50:
        return "CREST_ECHO_MOTION"
    if amount <= 60:
        return "FATIGUED_MOTION"
    return "CHAOTIC_MOTION"


def selected_recipes(path: Path) -> dict[str, dict[str, Any]]:
    payload = read_json(path)
    recipes: dict[str, dict[str, Any]] = {}
    for row in payload.get("world_reports", []):
        recipe = row.get("selected_upgrade_recipe")
        if recipe:
            recipes[str(row["topology_name"])] = recipe
    return recipes


def prior_matches(
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


def majority_value(rows: list[dict[str, Any]], field: str, min_prior: int) -> dict[str, Any]:
    if len(rows) < min_prior:
        return {
            "status": "NO_CALL",
            "value": None,
            "prior_count": len(rows),
            "rank": [],
        }
    counts = Counter(str(row[field]) for row in rows)
    value, count = counts.most_common(1)[0]
    return {
        "status": "CALL",
        "value": value,
        "prior_count": len(rows),
        "count": count,
        "rate": percent(count, len(rows)),
        "rank": ranked(counts),
    }


def enriched_cases(csv_path: Path, from_date: str) -> list[dict[str, Any]]:
    cases = build_cases(csv_path, parse_draw_date(from_date))
    rows = []
    for row in add_history_features(cases):
        row = dict(row)
        row["actual_motion_sign"] = motion_sign(int(row["actual_motion"]))
        row["actual_motion_band"] = motion_band(int(row["actual_motion"]))
        rows.append(row)
    return rows


def branch_family_prediction(
    cases: list[dict[str, Any]],
    current_pos: int,
    *,
    target_world: str,
    branch_recipe: dict[str, Any],
    min_prior: int,
) -> dict[str, Any]:
    source = (
        "WORLD"
        if branch_recipe["selector_source"] == "WEAK_WORLD_FEATURE_RECIPE"
        else "BORROWED"
    )
    features = tuple(branch_recipe["features"])
    horizon = int(branch_recipe["horizon"])
    rows = prior_matches(
        cases,
        current_pos,
        target_world=target_world,
        features=features,
        source=source,
        horizon=horizon,
    )
    selection = select_branch(rows, min_prior=min_prior)
    predicted_branch = selection["predicted_branch"]
    predicted_family = seat_family(str(predicted_branch)) if predicted_branch else None
    return {
        "status": selection["status"],
        "predicted_branch": predicted_branch,
        "predicted_family": predicted_family,
        "prior_count": selection["prior_count"],
        "rank": selection["rank"],
    }


def range_prediction(
    cases: list[dict[str, Any]],
    current_pos: int,
    *,
    target_world: str,
    recipe_name: str,
    features: tuple[str, ...],
    source: str,
    horizon: int,
    min_prior: int,
) -> dict[str, Any]:
    rows = prior_matches(
        cases,
        current_pos,
        target_world=target_world,
        features=features,
        source=source,
        horizon=horizon,
    )
    sign = majority_value(rows, "actual_motion_sign", min_prior=min_prior)
    band = majority_value(rows, "actual_motion_band", min_prior=min_prior)
    return {
        "range_recipe": recipe_name,
        "range_source": source,
        "range_horizon": horizon,
        "range_features": list(features),
        "predicted_sign": sign["value"],
        "predicted_band": band["value"],
        "range_prior_count": min(sign["prior_count"], band["prior_count"]),
        "sign_rank": sign["rank"],
        "band_rank": band["rank"],
        "status": "CALL" if sign["status"] == "CALL" else "NO_CALL",
    }


def final_branch_from_range(
    cases: list[dict[str, Any]],
    current_pos: int,
    *,
    target_world: str,
    predicted_family: str | None,
    predicted_sign: str | None,
    min_prior: int,
) -> dict[str, Any]:
    if not predicted_family or not predicted_sign:
        return {
            "status": "NO_CALL",
            "predicted_branch": None,
            "prior_count": 0,
            "rank": [],
            "source": "NONE",
        }
    target_rows = [
        row
        for row in cases[:current_pos]
        if row["topology_name"] == target_world
        and row["actual_family"] == predicted_family
        and row["actual_motion_sign"] == predicted_sign
    ]
    if len(target_rows) >= min_prior:
        selection = select_branch(target_rows, min_prior=min_prior)
        selection["source"] = "TARGET_WORLD_FAMILY_SIGN"
        return selection
    analog_rows = [
        row
        for row in cases[:current_pos]
        if row["actual_family"] == predicted_family
        and row["actual_motion_sign"] == predicted_sign
    ]
    selection = select_branch(analog_rows, min_prior=min_prior)
    selection["source"] = "BORROWED_FAMILY_SIGN"
    return selection


def evaluate_range_recipe(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    branch_recipe: dict[str, Any],
    range_recipe_name: str,
    range_features: tuple[str, ...],
    range_source: str,
    range_horizon: int,
    final_mode: str,
    min_prior: int,
) -> list[dict[str, Any]]:
    records = []
    branch_source = (
        "WORLD"
        if branch_recipe["selector_source"] == "WEAK_WORLD_FEATURE_RECIPE"
        else "BORROWED"
    )
    branch_features = tuple(branch_recipe["features"])
    branch_horizon = int(branch_recipe["horizon"])
    branch_seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    range_seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    target_family_sign_band_seen: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    analog_family_sign_band_seen: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    target_family_sign_seen: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    analog_family_sign_seen: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)

    for case in cases:
        branch_key = feature_key(case, branch_features)
        range_key = feature_key(case, range_features)
        if case["topology_name"] != target_world:
            if branch_source == "BORROWED":
                branch_seen_by_key[branch_key].append(case)
            if range_source == "BORROWED":
                range_seen_by_key[range_key].append(case)
            analog_family_sign_band_seen[
                (
                    str(case["actual_family"]),
                    str(case["actual_motion_sign"]),
                    str(case["actual_motion_band"]),
                )
            ].append(case)
            analog_family_sign_seen[
                (str(case["actual_family"]), str(case["actual_motion_sign"]))
            ].append(case)
            continue

        branch_rows = branch_seen_by_key[branch_key][-branch_horizon:]
        branch_selection = select_branch(branch_rows, min_prior=min_prior)
        predicted_branch = branch_selection["predicted_branch"]
        predicted_family = (
            seat_family(str(predicted_branch))
            if predicted_branch is not None
            else None
        )
        branch_read = {
            "status": branch_selection["status"],
            "predicted_branch": predicted_branch,
            "predicted_family": predicted_family,
            "prior_count": branch_selection["prior_count"],
            "rank": branch_selection["rank"],
        }

        range_rows = range_seen_by_key[range_key][-range_horizon:]
        sign = majority_value(range_rows, "actual_motion_sign", min_prior=min_prior)
        band = majority_value(range_rows, "actual_motion_band", min_prior=min_prior)
        range_read = {
            "range_recipe": range_recipe_name,
            "range_source": range_source,
            "range_horizon": range_horizon,
            "range_features": list(range_features),
            "predicted_sign": sign["value"],
            "predicted_band": band["value"],
            "range_prior_count": min(sign["prior_count"], band["prior_count"]),
            "sign_rank": sign["rank"],
            "band_rank": band["rank"],
            "status": "CALL" if sign["status"] == "CALL" else "NO_CALL",
        }

        final_band_key = (
            str(branch_read["predicted_family"]),
            str(range_read["predicted_sign"]),
            str(range_read["predicted_band"]),
        )
        final_key = (
            str(branch_read["predicted_family"]),
            str(range_read["predicted_sign"]),
        )
        target_band_rows = target_family_sign_band_seen[final_band_key]
        target_rows = target_family_sign_seen[final_key]
        if (
            final_mode == "SIGN_BAND"
            and branch_read["predicted_family"] is not None
            and range_read["predicted_sign"] is not None
            and range_read["predicted_band"] is not None
            and len(target_band_rows) >= min_prior
        ):
            final = select_branch(target_band_rows, min_prior=min_prior)
            final["source"] = "TARGET_WORLD_FAMILY_SIGN_BAND"
        elif (
            final_mode == "SIGN_BAND"
            and branch_read["predicted_family"] is not None
            and range_read["predicted_sign"] is not None
            and range_read["predicted_band"] is not None
            and len(analog_family_sign_band_seen[final_band_key]) >= min_prior
        ):
            final = select_branch(
                analog_family_sign_band_seen[final_band_key],
                min_prior=min_prior,
            )
            final["source"] = "BORROWED_FAMILY_SIGN_BAND"
        elif (
            branch_read["predicted_family"] is not None
            and range_read["predicted_sign"] is not None
            and len(target_rows) >= min_prior
        ):
            final = select_branch(target_rows, min_prior=min_prior)
            final["source"] = "TARGET_WORLD_FAMILY_SIGN"
        elif (
            branch_read["predicted_family"] is not None
            and range_read["predicted_sign"] is not None
        ):
            final = select_branch(
                analog_family_sign_seen[final_key],
                min_prior=min_prior,
            )
            final["source"] = "BORROWED_FAMILY_SIGN"
        else:
            final = {
                "status": "NO_CALL",
                "predicted_branch": None,
                "prior_count": 0,
                "rank": [],
                "source": "NONE",
            }
        predicted_branch = final["predicted_branch"]
        status = (
            "CALL"
            if branch_read["status"] == "CALL"
            and range_read["status"] == "CALL"
            and final["status"] == "CALL"
            else "NO_CALL"
        )
        branch_result = (
            "MATCH"
            if predicted_branch == case["actual_branch"]
            else "MISS"
            if predicted_branch is not None
            else "NO_CALL"
        )
        combined_prior_count = min(
            int(branch_read["prior_count"] or 0),
            int(range_read["range_prior_count"] or 0),
            int(final["prior_count"] or 0),
        )
        family_result = (
            "MATCH"
            if branch_read["predicted_family"] == case["actual_family"]
            else "MISS"
            if branch_read["predicted_family"] is not None
            else "NO_CALL"
        )
        sign_result = (
            "MATCH"
            if range_read["predicted_sign"] == case["actual_motion_sign"]
            else "MISS"
            if range_read["predicted_sign"] is not None
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
                "prior_count": combined_prior_count,
                "actual_branch": case["actual_branch"],
                "actual_family": case["actual_family"],
                "actual_motion": case["actual_motion"],
                "actual_motion_sign": case["actual_motion_sign"],
                "predicted_branch": predicted_branch,
                "predicted_branch_source": final["source"],
                "predicted_family": branch_read["predicted_family"],
                "predicted_sign": range_read["predicted_sign"],
                "predicted_band": range_read["predicted_band"],
                "branch_prior_count": branch_read["prior_count"],
                "range_prior_count": range_read["range_prior_count"],
                "final_prior_count": final["prior_count"],
            }
        )
        if branch_source == "WORLD":
            branch_seen_by_key[branch_key].append(case)
        elif branch_source == "BORROWED":
            branch_seen_by_key[branch_key].append(case)
        if range_source == "WORLD":
            range_seen_by_key[range_key].append(case)
        elif range_source == "BORROWED":
            range_seen_by_key[range_key].append(case)
        target_family_sign_band_seen[
            (
                str(case["actual_family"]),
                str(case["actual_motion_sign"]),
                str(case["actual_motion_band"]),
            )
        ].append(case)
        analog_family_sign_band_seen[
            (
                str(case["actual_family"]),
                str(case["actual_motion_sign"]),
                str(case["actual_motion_band"]),
            )
        ].append(case)
        target_family_sign_seen[
            (str(case["actual_family"]), str(case["actual_motion_sign"]))
        ].append(case)
        analog_family_sign_seen[
            (str(case["actual_family"]), str(case["actual_motion_sign"]))
        ].append(case)
    return records


def summarize_range_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    summary = summarize_records(records)
    calls = [row for row in records if row["status"] == "CALL"]
    sign_matches = sum(1 for row in calls if row["sign_result"] == "MATCH")
    summary["sign_matches"] = sign_matches
    summary["sign_match_rate"] = percent(sign_matches, len(calls))
    return summary


def build_audit(
    cases: list[dict[str, Any]],
    recipes: dict[str, dict[str, Any]],
    *,
    target_worlds: list[str],
    horizons: tuple[int, ...],
    min_prior: int,
    min_range_calls: int,
) -> dict[str, Any]:
    world_reports = []
    for world in target_worlds:
        branch_recipe = recipes[world]
        candidates = []
        for recipe_name, features in LIVE_SAFE_FEATURE_RECIPES.items():
            for source in ("WORLD", "BORROWED"):
                for horizon in horizons:
                    for final_mode in ("SIGN", "SIGN_BAND"):
                        records = evaluate_range_recipe(
                            cases,
                            target_world=world,
                            branch_recipe=branch_recipe,
                            range_recipe_name=recipe_name,
                            range_features=features,
                            range_source=source,
                            range_horizon=horizon,
                            final_mode=final_mode,
                            min_prior=min_prior,
                        )
                        summary = summarize_range_records(records)
                        candidates.append(
                            {
                                "range_recipe": recipe_name,
                                "range_source": source,
                                "range_horizon": horizon,
                                "range_final_mode": final_mode,
                                "range_features": list(features),
                                **summary,
                            }
                        )
        candidates.sort(
            key=lambda row: (
                -float(row["branch_match_rate"]),
                -float(row["family_match_rate"]),
                -float(row["sign_match_rate"]),
                -int(row["call_count"]),
                row["range_recipe"],
                row["range_source"],
                row["range_horizon"],
                row["range_final_mode"],
            )
        )
        useful_candidates = [
            row
            for row in candidates
            if int(row["call_count"]) >= min_range_calls
        ]
        useful_candidates.sort(
            key=lambda row: (
                -float(row["branch_match_rate"]),
                -float(row["family_match_rate"]),
                -float(row["sign_match_rate"]),
                -int(row["call_count"]),
                row["range_recipe"],
                row["range_source"],
                row["range_horizon"],
                row["range_final_mode"],
            )
        )
        world_reports.append(
            {
                "topology_name": world,
                "branch_recipe": branch_recipe,
                "top_range_candidates": candidates[:50],
                "top_useful_range_candidates": useful_candidates[:50],
                "selected_range_candidate": candidates[0] if candidates else None,
                "selected_useful_range_candidate": useful_candidates[0]
                if useful_candidates
                else None,
            }
        )
    return {
        "audit_name": "RANGE_SELECTOR_CONFIRMATION_AUDIT",
        "min_prior": min_prior,
        "min_range_calls": min_range_calls,
        "horizons": list(horizons),
        "target_worlds": target_worlds,
        "world_reports": world_reports,
        "notes": [
            "Branch family is predicted from the selected weak-world branch recipe.",
            "Motion sign/range is predicted from prior matching live-safe range recipes.",
            "Final exact branch uses prior target-world family+sign when available, otherwise borrowed family+sign.",
            "SIGN_BAND mode tests whether predicted motion band improves the final branch resolver.",
            "This audit does not use actual outgoing motion to pick the branch.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Range Selector Confirmation Audit",
        description="Test whether predicted motion sign/range can upgrade weak branch selectors.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--weak-audit", type=Path, default=DEFAULT_WEAK_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--worlds", default="Suzuka")
    parser.add_argument("--horizons", default="1,2,3,5,8,13,21,34")
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--min-range-calls", type=int, default=10)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    horizons = tuple(
        int(part.strip())
        for part in args.horizons.split(",")
        if part.strip()
    )
    worlds = [part.strip() for part in args.worlds.split(",") if part.strip()]
    if args.min_prior < 1:
        raise ValueError("--min-prior must be at least 1.")
    cases = enriched_cases(args.csv_path, args.from_date)
    recipes = selected_recipes(args.weak_audit)
    missing = [world for world in worlds if world not in recipes]
    if missing:
        raise ValueError(f"Missing branch recipe for worlds: {', '.join(missing)}")
    audit = build_audit(
        cases,
        recipes,
        target_worlds=worlds,
        horizons=horizons,
        min_prior=args.min_prior,
        min_range_calls=args.min_range_calls,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    if args.print_summary:
        print(json.dumps(
            {
                "output": str(args.output),
                "world_reports": [
                    {
                        "world": row["topology_name"],
                        "selected_range_candidate": row["selected_range_candidate"],
                        "selected_useful_range_candidate": row["selected_useful_range_candidate"],
                    }
                    for row in audit["world_reports"]
                ],
            },
            indent=2,
        ))


if __name__ == "__main__":
    main()
