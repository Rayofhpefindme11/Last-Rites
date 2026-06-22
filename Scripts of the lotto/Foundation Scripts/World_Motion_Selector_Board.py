from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Motion_Band_Resolver_Audit import (
    BAND_FEATURE_RECIPES,
    DEFAULT_HORIZONS,
    evaluate_band_recipe,
)
from Range_Selector_Confirmation_Audit import enriched_cases
from Selector_Priority_Board import (
    DEFAULT_OUTPUT_PATH as DEFAULT_BRANCH_BOARD,
    branch_quality,
    count,
    rate,
    read_json,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "world_motion_selector_board_min2_2015-10-07.json"
)

QUALITY_RANK = {
    "NO_CALL": 0,
    "OBSERVE_SIGN": 1,
    "OBSERVE_BAND": 1,
    "SMALL_SIGN": 2,
    "SMALL_BAND": 2,
    "USABLE_SIGN": 3,
    "USABLE_BAND": 3,
    "STRONG_SIGN": 4,
    "STRONG_BAND": 4,
}


def metric_quality(metric: str, row: dict[str, Any] | None) -> str:
    calls = count(row)
    if row is None or calls == 0:
        return "NO_CALL"
    if metric == "sign":
        value = rate(row, "sign_match_rate")
        if calls >= 25 and value >= 85:
            return "STRONG_SIGN"
        if calls >= 10 and value >= 75:
            return "USABLE_SIGN"
        if calls >= 5 and value >= 70:
            return "SMALL_SIGN"
        return "OBSERVE_SIGN"
    if metric == "band":
        value = rate(row, "band_match_rate")
        if calls >= 25 and value >= 60:
            return "STRONG_BAND"
        if calls >= 10 and value >= 45:
            return "USABLE_BAND"
        if calls >= 5 and value >= 35:
            return "SMALL_BAND"
        return "OBSERVE_BAND"
    raise ValueError(f"Unknown metric: {metric}")


def selector_entry(
    row: dict[str, Any] | None,
    *,
    selector_type: str,
    quality: str,
) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "selector_type": selector_type,
        "quality": quality,
        "recipe": row.get("recipe"),
        "source": row.get("source"),
        "horizon": row.get("horizon"),
        "features": row.get("features", []),
        "call_count": row.get("call_count", 0),
        "call_rate": row.get("call_rate", 0.0),
        "sign_match_rate": row.get("sign_match_rate", 0.0),
        "band_match_rate": row.get("band_match_rate", 0.0),
        "predicted_band_rank": row.get("predicted_band_rank", []),
        "actual_band_rank": row.get("actual_band_rank", []),
    }


def branch_entry(row: dict[str, Any]) -> dict[str, Any]:
    candidate = row["chosen_candidate"]
    return {
        "selector_type": "BRANCH",
        "quality": row["chosen_quality"],
        "layer": row["chosen_layer"],
        "signal": candidate.get("signal"),
        "source": candidate.get("source"),
        "horizon": candidate.get("horizon"),
        "final_mode": candidate.get("final_mode"),
        "features": candidate.get("features", []),
        "call_count": candidate.get("call_count", 0),
        "branch_match_rate": candidate.get("branch_match_rate", 0.0),
        "family_match_rate": candidate.get("family_match_rate", 0.0),
        "sign_match_rate": candidate.get("sign_match_rate"),
    }


def sign_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    quality = metric_quality("sign", row)
    return (
        -QUALITY_RANK[quality],
        -rate(row, "sign_match_rate"),
        -rate(row, "band_match_rate"),
        -count(row),
        row.get("recipe"),
        row.get("source"),
        row.get("horizon"),
    )


def band_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    quality = metric_quality("band", row)
    return (
        -QUALITY_RANK[quality],
        -rate(row, "band_match_rate"),
        -rate(row, "sign_match_rate"),
        -count(row),
        row.get("recipe"),
        row.get("source"),
        row.get("horizon"),
    )


def build_world_candidates(
    cases: list[dict[str, Any]],
    *,
    world: str,
    recipe_names: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
) -> list[dict[str, Any]]:
    recipes = {
        name: BAND_FEATURE_RECIPES[name]
        for name in recipe_names
        if name in BAND_FEATURE_RECIPES
    }
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
    return candidates


def build_board(
    cases: list[dict[str, Any]],
    branch_board: dict[str, Any],
    *,
    recipe_names: tuple[str, ...],
    horizons: tuple[int, ...],
    min_prior: int,
    min_calls: int,
) -> dict[str, Any]:
    rows = []
    branch_quality_counts: dict[str, int] = {}
    sign_quality_counts: dict[str, int] = {}
    band_quality_counts: dict[str, int] = {}
    for branch_row in branch_board.get("world_reports", []):
        world = str(branch_row["topology_name"])
        candidates = build_world_candidates(
            cases,
            world=world,
            recipe_names=recipe_names,
            horizons=horizons,
            min_prior=min_prior,
        )
        useful = [row for row in candidates if count(row) >= min_calls]
        useful_sign = sorted(useful, key=sign_sort_key)
        useful_band = sorted(useful, key=band_sort_key)
        sign_winner = useful_sign[0] if useful_sign else None
        band_winner = useful_band[0] if useful_band else None
        branch = branch_entry(branch_row)
        sign_quality = metric_quality("sign", sign_winner)
        band_quality = metric_quality("band", band_winner)
        branch_quality_counts[branch["quality"]] = (
            branch_quality_counts.get(branch["quality"], 0) + 1
        )
        sign_quality_counts[sign_quality] = sign_quality_counts.get(sign_quality, 0) + 1
        band_quality_counts[band_quality] = band_quality_counts.get(band_quality, 0) + 1
        rows.append(
            {
                "topology_name": world,
                "branch_selector": branch,
                "sign_selector": selector_entry(
                    sign_winner,
                    selector_type="SIGN",
                    quality=sign_quality,
                ),
                "band_selector": selector_entry(
                    band_winner,
                    selector_type="BROAD_BAND",
                    quality=band_quality,
                ),
                "top_sign_candidates": [
                    selector_entry(row, selector_type="SIGN", quality=metric_quality("sign", row))
                    for row in useful_sign[:20]
                ],
                "top_band_candidates": [
                    selector_entry(
                        row,
                        selector_type="BROAD_BAND",
                        quality=metric_quality("band", row),
                    )
                    for row in useful_band[:20]
                ],
            }
        )
    rows.sort(
        key=lambda row: (
            -rate(row["branch_selector"], "branch_match_rate"),
            -rate(row["sign_selector"], "sign_match_rate"),
            -rate(row["band_selector"], "band_match_rate"),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "WORLD_MOTION_SELECTOR_BOARD",
        "min_prior": min_prior,
        "min_calls": min_calls,
        "horizons": list(horizons),
        "world_count": len(rows),
        "quality_counts": {
            "branch": branch_quality_counts,
            "sign": sign_quality_counts,
            "broad_band": band_quality_counts,
        },
        "world_reports": rows,
        "notes": [
            "Each world receives separate branch, sign, and broad-band selectors.",
            "Branch comes from the existing selector priority board.",
            "Sign and broad band are selected independently from the full live-safe recipe grid.",
            "This board is the staging layer before the 35-class motion gauge selector.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="World Motion Selector Board",
        description="Build per-world branch, sign, and broad-band selector winners.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--branch-board", type=Path, default=DEFAULT_BRANCH_BOARD)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--horizons", default="2,3,5,8,13,21,34")
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
    recipe_names = tuple(
        part.strip()
        for part in args.recipes.split(",")
        if part.strip()
    ) or tuple(BAND_FEATURE_RECIPES)
    payload = build_board(
        enriched_cases(args.csv_path, args.from_date),
        read_json(args.branch_board),
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
                    "quality_counts": payload["quality_counts"],
                    "world_reports": [
                        {
                            "world": row["topology_name"],
                            "branch": {
                                "quality": row["branch_selector"]["quality"],
                                "signal": row["branch_selector"]["signal"],
                                "exact": row["branch_selector"]["branch_match_rate"],
                                "family": row["branch_selector"]["family_match_rate"],
                            },
                            "sign": {
                                "quality": row["sign_selector"]["quality"]
                                if row["sign_selector"]
                                else "NO_CALL",
                                "recipe": row["sign_selector"]["recipe"]
                                if row["sign_selector"]
                                else None,
                                "source": row["sign_selector"]["source"]
                                if row["sign_selector"]
                                else None,
                                "horizon": row["sign_selector"]["horizon"]
                                if row["sign_selector"]
                                else None,
                                "calls": row["sign_selector"]["call_count"]
                                if row["sign_selector"]
                                else 0,
                                "rate": row["sign_selector"]["sign_match_rate"]
                                if row["sign_selector"]
                                else 0,
                            },
                            "band": {
                                "quality": row["band_selector"]["quality"]
                                if row["band_selector"]
                                else "NO_CALL",
                                "recipe": row["band_selector"]["recipe"]
                                if row["band_selector"]
                                else None,
                                "source": row["band_selector"]["source"]
                                if row["band_selector"]
                                else None,
                                "horizon": row["band_selector"]["horizon"]
                                if row["band_selector"]
                                else None,
                                "calls": row["band_selector"]["call_count"]
                                if row["band_selector"]
                                else 0,
                                "rate": row["band_selector"]["band_match_rate"]
                                if row["band_selector"]
                                else 0,
                            },
                        }
                        for row in payload["world_reports"]
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
