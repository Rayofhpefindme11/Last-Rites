from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH
from Branch_Selector_Lookback_Audit import percent
from Range_Selector_Confirmation_Audit import enriched_cases


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "motion_range_ceiling_audit_min2_2015-10-07.json"
)


def evaluate_ceiling(
    cases: list[dict[str, Any]],
    *,
    target_world: str,
    key_mode: str,
    horizon: int,
    min_prior: int,
    radii: tuple[int, ...],
) -> dict[str, Any]:
    seen_by_key: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    rows = {
        radius: {
            "calls": 0,
            "hits": 0,
            "exact_midpoint_hits": 0,
            "errors": [],
        }
        for radius in radii
    }
    for case in cases:
        if case["topology_name"] != target_world:
            continue
        if key_mode == "BRANCH_SIGN":
            key = (
                str(case["topology_name"]),
                str(case["actual_branch"]),
                str(case["actual_motion_sign"]),
            )
        elif key_mode == "BRANCH_SIGN_BAND":
            key = (
                str(case["topology_name"]),
                str(case["actual_branch"]),
                str(case["actual_motion_sign"]),
                str(case["actual_motion_band"]),
            )
        else:
            raise ValueError(f"Unknown key mode: {key_mode}")
        prior = seen_by_key[key][-horizon:]
        if len(prior) >= min_prior:
            values = [int(row["actual_motion"]) for row in prior]
            midpoint = int(round(median(values)))
            actual = int(case["actual_motion"])
            for radius in radii:
                low = midpoint - radius
                high = midpoint + radius
                rows[radius]["calls"] += 1
                rows[radius]["hits"] += 1 if low <= actual <= high else 0
                rows[radius]["exact_midpoint_hits"] += 1 if midpoint == actual else 0
                rows[radius]["errors"].append(abs(actual - midpoint))
        seen_by_key[key].append(case)
    results = []
    for radius in radii:
        row = rows[radius]
        calls = int(row["calls"])
        errors = row["errors"]
        results.append(
            {
                "radius": radius,
                "width": radius * 2,
                "call_count": calls,
                "range_hits": row["hits"],
                "range_hit_rate": percent(row["hits"], calls),
                "exact_midpoint_hits": row["exact_midpoint_hits"],
                "exact_midpoint_rate": percent(row["exact_midpoint_hits"], calls),
                "avg_abs_error": round(sum(errors) / len(errors), 2)
                if errors
                else 0.0,
                "median_abs_error": median(errors) if errors else 0.0,
            }
        )
    return {
        "key_mode": key_mode,
        "horizon": horizon,
        "min_prior": min_prior,
        "results": results,
    }


def build_audit(
    cases: list[dict[str, Any]],
    *,
    worlds: list[str],
    horizon: int,
    min_prior: int,
    radii: tuple[int, ...],
) -> dict[str, Any]:
    reports = []
    for world in worlds:
        reports.append(
            {
                "topology_name": world,
                "branch_sign": evaluate_ceiling(
                    cases,
                    target_world=world,
                    key_mode="BRANCH_SIGN",
                    horizon=horizon,
                    min_prior=min_prior,
                    radii=radii,
                ),
                "branch_sign_band": evaluate_ceiling(
                    cases,
                    target_world=world,
                    key_mode="BRANCH_SIGN_BAND",
                    horizon=horizon,
                    min_prior=min_prior,
                    radii=radii,
                ),
            }
        )
    return {
        "audit_name": "MOTION_RANGE_CEILING_AUDIT",
        "horizon": horizon,
        "min_prior": min_prior,
        "radii": list(radii),
        "world_reports": reports,
        "notes": [
            "This is a diagnostic ceiling audit, not a live predictor.",
            "BRANCH_SIGN uses the actual historical branch and sign to test amount tightness.",
            "BRANCH_SIGN_BAND also uses the actual historical motion band.",
            "If BRANCH_SIGN_BAND is tight while live band prediction is weak, the next required layer is band selection.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Motion Range Ceiling Audit",
        description="Diagnostic ceiling for outgoing motion amount once branch/sign/band are known.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument(
        "--worlds",
        default="Medusa,Lumina,Citrine,Nova,Suzuka,Circe,Artoria",
    )
    parser.add_argument("--horizon", type=int, default=13)
    parser.add_argument("--min-prior", type=int, default=2)
    parser.add_argument("--radii", default="5,10,15,20")
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    worlds = [part.strip() for part in args.worlds.split(",") if part.strip()]
    radii = tuple(
        int(part.strip())
        for part in args.radii.split(",")
        if part.strip()
    )
    payload = build_audit(
        enriched_cases(args.csv_path, args.from_date),
        worlds=worlds,
        horizon=args.horizon,
        min_prior=args.min_prior,
        radii=radii,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.print_summary:
        print(json.dumps({"output": str(args.output), **payload}, indent=2))


if __name__ == "__main__":
    main()
