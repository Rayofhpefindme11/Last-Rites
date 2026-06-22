from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE_AUDIT = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "all_world_selector_upgrade_audit_min2_2015-10-07.json"
)
DEFAULT_RANGE_AUDIT = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "range_selector_confirmation_audit_all_worlds_min2_2015-10-07.json"
)
DEFAULT_EDGE_AUDIT = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "medusa_edge_separation_audit_min2_2015-10-07.json"
)
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "selector_priority_board_exact_family_range_min2_2015-10-07.json"
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rate(row: dict[str, Any] | None, key: str) -> float:
    if row is None:
        return 0.0
    return float(row.get(key, 0.0) or 0.0)


def count(row: dict[str, Any] | None, key: str = "call_count") -> int:
    if row is None:
        return 0
    return int(row.get(key, 0) or 0)


def branch_quality(row: dict[str, Any]) -> str:
    calls = count(row)
    exact = rate(row, "branch_match_rate")
    family = rate(row, "family_match_rate")
    if calls >= 25 and exact >= 70 and family >= 90:
        return "COMPLETE_EXACT"
    if calls >= 10 and exact >= 60 and family >= 80:
        return "STRONG_EXACT"
    if calls >= 10 and exact >= 55 and family >= 65:
        return "USABLE_EXACT"
    if exact >= 60:
        return "SMALL_EXACT"
    if family >= 80:
        return "FAMILY_STRONG"
    if family >= 65:
        return "FAMILY_USABLE"
    return "OBSERVE"


def base_candidate(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "layer": "BRANCH_SELECTOR",
        "signal": row.get("signal"),
        "source": row.get("selector_source"),
        "horizon": row.get("horizon"),
        "features": row.get("features", []),
        "call_count": row.get("call_count", 0),
        "branch_match_rate": row.get("branch_match_rate", 0.0),
        "family_match_rate": row.get("family_match_rate", 0.0),
        "sign_match_rate": None,
        "promotion": row.get("promotion"),
        "sample_warning": row.get("sample_warning"),
    }


def range_candidate(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "layer": "RANGE_CONFIRMATION",
        "signal": row.get("range_recipe"),
        "source": row.get("range_source"),
        "horizon": row.get("range_horizon"),
        "final_mode": row.get("range_final_mode"),
        "features": row.get("range_features", []),
        "call_count": row.get("call_count", 0),
        "branch_match_rate": row.get("branch_match_rate", 0.0),
        "family_match_rate": row.get("family_match_rate", 0.0),
        "sign_match_rate": row.get("sign_match_rate", 0.0),
        "promotion": None,
        "sample_warning": None,
    }


def edge_candidate(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "layer": "EDGE_SEPARATION",
        "signal": row.get("edge_recipe"),
        "source": row.get("edge_source"),
        "horizon": row.get("edge_horizon"),
        "final_mode": "EDGE_OVERRIDE",
        "features": row.get("edge_features", []),
        "call_count": row.get("call_count", 0),
        "branch_match_rate": row.get("branch_match_rate", 0.0),
        "family_match_rate": row.get("family_match_rate", 0.0),
        "sign_match_rate": row.get("sign_match_rate", 0.0),
        "edge_exact_match_rate": row.get("edge_exact_match_rate", 0.0),
        "override_count": row.get("override_count", 0),
        "promotion": None,
        "sample_warning": None,
    }


def choose_candidate(
    base: dict[str, Any],
    *candidates: dict[str, Any] | None,
    min_range_calls: int,
) -> dict[str, Any]:
    viable = [base]
    viable.extend(
        candidate
        for candidate in candidates
        if candidate is not None and count(candidate) >= min_range_calls
    )
    best = base
    best_key = (
        rate(base, "branch_match_rate"),
        rate(base, "family_match_rate"),
        rate(base, "sign_match_rate"),
        count(base),
    )
    for candidate in viable[1:]:
        candidate_key = (
            rate(candidate, "branch_match_rate"),
            rate(candidate, "family_match_rate"),
            rate(candidate, "sign_match_rate"),
            count(candidate),
        )
        if candidate_key > best_key:
            best = candidate
            best_key = candidate_key
    return best


def build_board(
    base_payload: dict[str, Any],
    range_payload: dict[str, Any],
    edge_payload: dict[str, Any] | None,
    *,
    min_range_calls: int,
) -> dict[str, Any]:
    base_by_world = {
        str(row["topology_name"]): row.get("selected_upgrade_recipe")
        for row in base_payload.get("world_reports", [])
        if row.get("selected_upgrade_recipe")
    }
    range_by_world = {
        str(row["topology_name"]): row.get("selected_useful_range_candidate")
        for row in range_payload.get("world_reports", [])
    }
    edge_by_world = {}
    if edge_payload:
        edge_by_world[str(edge_payload["target_world"])] = edge_payload.get(
            "selected_useful_edge_candidate"
        )
    rows = []
    quality_counts: dict[str, int] = {}
    layer_counts: dict[str, int] = {}
    for world in sorted(base_by_world):
        base = base_candidate(base_by_world[world])
        confirmed = range_candidate(range_by_world.get(world))
        edge = edge_candidate(edge_by_world.get(world))
        chosen = choose_candidate(
            base,
            confirmed,
            edge,
            min_range_calls=min_range_calls,
        )
        quality = branch_quality(chosen)
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
        layer_counts[str(chosen["layer"])] = layer_counts.get(str(chosen["layer"]), 0) + 1
        rows.append(
            {
                "topology_name": world,
                "chosen_layer": chosen["layer"],
                "chosen_quality": quality,
                "chosen_candidate": chosen,
                "base_candidate": base,
                "range_candidate": confirmed,
                "edge_candidate": edge,
                "exact_delta_from_base": round(
                    rate(chosen, "branch_match_rate")
                    - rate(base, "branch_match_rate"),
                    2,
                ),
                "family_delta_from_base": round(
                    rate(chosen, "family_match_rate")
                    - rate(base, "family_match_rate"),
                    2,
                ),
            }
        )
    rows.sort(
        key=lambda row: (
            -rate(row["chosen_candidate"], "branch_match_rate"),
            -rate(row["chosen_candidate"], "family_match_rate"),
            -rate(row["chosen_candidate"], "sign_match_rate"),
            -count(row["chosen_candidate"]),
            row["topology_name"],
        )
    )
    return {
        "audit_name": "SELECTOR_PRIORITY_BOARD",
        "priority_order": [
            "exact branch match rate",
            "family match rate",
            "motion sign/range match rate",
            "call count",
        ],
        "min_range_calls": min_range_calls,
        "world_count": len(rows),
        "quality_counts": quality_counts,
        "layer_counts": layer_counts,
        "world_reports": rows,
        "notes": [
            "Range confirmation is only promoted when it has at least min_range_calls.",
            "Edge separation is only promoted when it has at least min_range_calls.",
            "The board chooses exact first, then family, then sign/range.",
            "Small exact selectors remain marked as small; they are useful but need more evidence.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Selector Priority Board",
        description="Merge branch-selector and range-confirmation audits into one exact-first board.",
    )
    parser.add_argument("--base-audit", type=Path, default=DEFAULT_BASE_AUDIT)
    parser.add_argument("--range-audit", type=Path, default=DEFAULT_RANGE_AUDIT)
    parser.add_argument("--edge-audit", type=Path, default=DEFAULT_EDGE_AUDIT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--min-range-calls", type=int, default=10)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = build_board(
        read_json(args.base_audit),
        read_json(args.range_audit),
        read_json(args.edge_audit) if args.edge_audit.exists() else None,
        min_range_calls=args.min_range_calls,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.print_summary:
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "quality_counts": payload["quality_counts"],
                    "layer_counts": payload["layer_counts"],
                    "world_reports": [
                        {
                            "world": row["topology_name"],
                            "layer": row["chosen_layer"],
                            "quality": row["chosen_quality"],
                            "signal": row["chosen_candidate"]["signal"],
                            "calls": row["chosen_candidate"]["call_count"],
                            "exact": row["chosen_candidate"]["branch_match_rate"],
                            "family": row["chosen_candidate"]["family_match_rate"],
                            "sign": row["chosen_candidate"]["sign_match_rate"],
                            "exact_delta": row["exact_delta_from_base"],
                            "family_delta": row["family_delta_from_base"],
                        }
                        for row in payload["world_reports"]
                    ],
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
