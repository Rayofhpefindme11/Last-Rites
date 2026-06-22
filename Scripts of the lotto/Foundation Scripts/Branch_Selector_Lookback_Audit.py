from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from statistics import median
from typing import Any

from Infinite_Inner_World import DEFAULT_CSV_PATH, load_historical_draws, parse_draw_date
from Seat_Taxonomy import (
    build_conditional_motion_memory_key,
    build_seat_taxonomy_packets,
    conditional_motion_memory_case,
    seat_family,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "branch_selector_lookback_audit_2015-10-07.json"
)
DEFAULT_HORIZONS = (1, 2, 3, 5, 8, 13, 21, 34)
SEATS = ("S1", "S2", "S3", "S4", "S5")


def percent(numerator: int | float, denominator: int | float) -> float:
    if not denominator:
        return 0.0
    return round((numerator / denominator) * 100, 2)


def ranked(counter: Counter[str]) -> list[dict[str, Any]]:
    total = sum(counter.values())
    return [
        {"value": value, "count": count, "rate": percent(count, total)}
        for value, count in counter.most_common()
    ]


def case_signal_key(case: dict[str, Any], signal: str) -> tuple[Any, ...]:
    if signal == "WORLD":
        return (case["topology_name"],)
    if signal == "WORLD_AUTHORITY":
        return (case["topology_name"], case["authority_seat"])
    if signal == "WORLD_AUTHORITY_ORIGIN":
        return (case["topology_name"], case["authority_seat"], case["authority_origin"])
    if signal == "WORLD_AUTHORITY_INCOMING":
        return (
            case["topology_name"],
            case["authority_seat"],
            case["incoming_draw_sign"],
            case["dominant_incoming_draw_lane"],
        )
    if signal == "LEVEL2_ROOM":
        return (build_conditional_motion_memory_key(case, level=2),)
    if signal == "LEVEL3_ROOM":
        return (build_conditional_motion_memory_key(case, level=3),)
    if signal == "LEVEL4_ROOM":
        return (build_conditional_motion_memory_key(case, level=4),)
    raise ValueError(f"Unknown signal: {signal}")


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


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    calls = [row for row in records if row["status"] == "CALL"]
    matches = sum(1 for row in calls if row["branch_result"] == "MATCH")
    family_matches = sum(1 for row in calls if row["family_result"] == "MATCH")
    prior_values = [
        int(row["prior_count"])
        for row in calls
        if row.get("prior_count") is not None
    ]
    return {
        "test_count": len(records),
        "call_count": len(calls),
        "call_rate": percent(len(calls), len(records)),
        "branch_matches": matches,
        "branch_match_rate": percent(matches, len(calls)),
        "family_matches": family_matches,
        "family_match_rate": percent(family_matches, len(calls)),
        "avg_prior_count": round(
            sum(prior_values) / len(prior_values),
            2,
        )
        if prior_values
        else 0.0,
    }


def build_cases(csv_path: Path, from_date: date) -> list[dict[str, Any]]:
    draws = [
        draw
        for draw in load_historical_draws(csv_path)
        if draw.draw_date >= from_date
    ]
    packets = build_seat_taxonomy_packets(
        draws,
        from_date=from_date,
        to_date=None,
        limit=None,
        latest=False,
        use_resolution_bias=False,
    )
    cases: list[dict[str, Any]] = []
    for packet in packets:
        case = conditional_motion_memory_case(packet.to_payload())
        if case is not None:
            cases.append(case)
    cases.sort(key=lambda row: int(row["index"]))
    return cases


def build_draw_lookback_records(
    cases: list[dict[str, Any]],
    signal: str,
    horizons: tuple[int, ...],
    min_prior: int,
) -> dict[str, list[dict[str, Any]]]:
    records_by_horizon: dict[str, list[dict[str, Any]]] = {str(h): [] for h in horizons}
    for pos, case in enumerate(cases):
        current_key = case_signal_key(case, signal)
        for horizon in horizons:
            prior_window = [
                prior
                for prior in cases[max(0, pos - horizon):pos]
                if case_signal_key(prior, signal) == current_key
            ]
            selection = select_branch(prior_window, min_prior=min_prior)
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
            records_by_horizon[str(horizon)].append(
                {
                    "date": case["date"],
                    "index": case["index"],
                    "topology_name": case["topology_name"],
                    "signal": signal,
                    "horizon_type": "DRAW_LOOKBACK",
                    "horizon": horizon,
                    "status": selection["status"],
                    "prior_count": selection["prior_count"],
                    "predicted_branch": predicted_branch,
                    "actual_branch": case["actual_branch"],
                    "branch_result": branch_result,
                    "family_result": family_result,
                    "rank": selection["rank"][:5],
                }
            )
    return records_by_horizon


def build_occurrence_lookback_records(
    cases: list[dict[str, Any]],
    signal: str,
    horizons: tuple[int, ...],
    min_prior: int,
) -> dict[str, list[dict[str, Any]]]:
    records_by_horizon: dict[str, list[dict[str, Any]]] = {str(h): [] for h in horizons}
    seen_by_key: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        current_key = case_signal_key(case, signal)
        prior_matches = seen_by_key[current_key]
        for horizon in horizons:
            selection = select_branch(prior_matches[-horizon:], min_prior=min_prior)
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
            records_by_horizon[str(horizon)].append(
                {
                    "date": case["date"],
                    "index": case["index"],
                    "topology_name": case["topology_name"],
                    "signal": signal,
                    "horizon_type": "OCCURRENCE_LOOKBACK",
                    "horizon": horizon,
                    "status": selection["status"],
                    "prior_count": selection["prior_count"],
                    "predicted_branch": predicted_branch,
                    "actual_branch": case["actual_branch"],
                    "branch_result": branch_result,
                    "family_result": family_result,
                    "rank": selection["rank"][:5],
                }
            )
        prior_matches.append(case)
    return records_by_horizon


def build_range_profile(rows: list[dict[str, Any]]) -> dict[str, Any]:
    motions = [int(row["actual_motion"]) for row in rows]
    abs_motions = [abs(value) for value in motions]
    lanes = Counter(str(row["actual_lane"]) for row in rows)
    signs = Counter("+" if value > 0 else "-" if value < 0 else "0" for value in motions)
    return {
        "count": len(rows),
        "signed_motion_min": min(motions),
        "signed_motion_max": max(motions),
        "signed_motion_median": median(motions),
        "abs_motion_min": min(abs_motions),
        "abs_motion_max": max(abs_motions),
        "abs_motion_median": median(abs_motions),
        "lane_rank": ranked(lanes),
        "sign_rank": ranked(signs),
        "top_motion_values": ranked(Counter(str(value) for value in motions))[:10],
    }


def build_range_profiles(cases: list[dict[str, Any]], min_sample: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        grouped[(case["topology_name"], case["actual_branch"])].append(case)
    profiles = []
    for (topology_name, branch), rows in grouped.items():
        if len(rows) < min_sample:
            continue
        profile = build_range_profile(rows)
        profile["topology_name"] = topology_name
        profile["branch"] = branch
        profiles.append(profile)
    profiles.sort(key=lambda row: (-row["count"], row["topology_name"], row["branch"]))
    return profiles


def choose_freshest(last_seen: dict[str, int], current_index: int) -> tuple[str | None, int | None]:
    seen = {seat: index for seat, index in last_seen.items() if index >= 0}
    if not seen:
        return None, None
    seat, index = max(seen.items(), key=lambda item: (item[1], item[0]))
    return seat, current_index - index


def choose_stalest(last_seen: dict[str, int], current_index: int) -> tuple[str | None, int | None]:
    seen = {seat: index for seat, index in last_seen.items() if index >= 0}
    if not seen:
        return None, None
    seat, index = min(seen.items(), key=lambda item: (item[1], item[0]))
    return seat, current_index - index


def build_signal_probe_records(cases: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    records: dict[str, list[dict[str, Any]]] = defaultdict(list)
    global_last = {seat: -1 for seat in SEATS}
    world_last: dict[str, dict[str, int]] = defaultdict(lambda: {seat: -1 for seat in SEATS})
    world_authority_last: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {seat: -1 for seat in SEATS}
    )

    for pos, case in enumerate(cases):
        world = str(case["topology_name"])
        world_authority = (world, str(case["authority_seat"]))
        freshest_global, freshest_global_age = choose_freshest(global_last, pos)
        stalest_global, stalest_global_age = choose_stalest(global_last, pos)
        freshest_world, freshest_world_age = choose_freshest(world_last[world], pos)
        stalest_world, stalest_world_age = choose_stalest(world_last[world], pos)
        freshest_world_authority, freshest_world_authority_age = choose_freshest(
            world_authority_last[world_authority],
            pos,
        )
        stalest_world_authority, stalest_world_authority_age = choose_stalest(
            world_authority_last[world_authority],
            pos,
        )
        candidates = {
            "AUTHORITY_SEAT": (case.get("authority_seat"), None),
            "DOMINANT_PRESSURE_SEAT": (case.get("dominant_pressure_seat"), None),
            "HIGHEST_BURDEN_SEAT": (case.get("highest_burden_seat"), None),
            "DOMINANT_ORIGIN_SEAT": (case.get("dominant_origin_seat"), None),
            "COLLISION_SEAT": (case.get("collision_seat"), None),
            "GLOBAL_FRESHEST_BRANCH": (freshest_global, freshest_global_age),
            "GLOBAL_STALEST_BRANCH": (stalest_global, stalest_global_age),
            "WORLD_FRESHEST_BRANCH": (freshest_world, freshest_world_age),
            "WORLD_STALEST_BRANCH": (stalest_world, stalest_world_age),
            "WORLD_AUTHORITY_FRESHEST_BRANCH": (
                freshest_world_authority,
                freshest_world_authority_age,
            ),
            "WORLD_AUTHORITY_STALEST_BRANCH": (
                stalest_world_authority,
                stalest_world_authority_age,
            ),
        }
        for signal, (predicted_branch, age) in candidates.items():
            predicted_branch = str(predicted_branch) if predicted_branch else None
            status = "CALL" if predicted_branch in SEATS else "NO_CALL"
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
                and seat_family(predicted_branch) == case["actual_family"]
                else "MISS"
                if predicted_branch is not None
                else "NO_CALL"
            )
            records[signal].append(
                {
                    "date": case["date"],
                    "index": case["index"],
                    "topology_name": world,
                    "signal": signal,
                    "status": status,
                    "age": age,
                    "predicted_branch": predicted_branch,
                    "actual_branch": case["actual_branch"],
                    "branch_result": branch_result,
                    "family_result": family_result,
                    "authority_seat": case.get("authority_seat"),
                    "authority_origin": case.get("authority_origin"),
                    "pressure_balance": case.get("pressure_balance"),
                    "pressure_distribution": case.get("pressure_distribution"),
                    "map_pressure_type": case.get("map_pressure_type"),
                }
            )
        actual_branch = str(case["actual_branch"])
        global_last[actual_branch] = pos
        world_last[world][actual_branch] = pos
        world_authority_last[world_authority][actual_branch] = pos
    return records


def build_signal_probe_summary(
    cases: list[dict[str, Any]],
    min_world_calls: int,
) -> dict[str, Any]:
    probe_records = build_signal_probe_records(cases)
    tests = []
    world_leaders = []
    world_selector_candidates = []
    for signal, records in probe_records.items():
        tests.append({"signal": signal, **summarize_records(records)})
        leaders = best_by_world(records, min_calls=min_world_calls)[:10]
        if leaders:
            world_leaders.append({"signal": signal, "worlds": leaders})
        world_selector_candidates.extend(
            candidate_rows_from_records(
                records,
                min_calls=min_world_calls,
                selector_source="SIGNAL_PROBE",
                signal=signal,
            )
        )
    tests.sort(key=lambda row: (-row["branch_match_rate"], -row["call_count"], row["signal"]))
    world_leaders.sort(
        key=lambda row: (
            -row["worlds"][0]["branch_match_rate"],
            -row["worlds"][0]["call_count"],
            row["signal"],
        )
    )
    return {
        "signal_tests": tests,
        "top_signal_tests": tests[:25],
        "signal_world_leaders": world_leaders[:50],
        "world_selector_candidates": world_selector_candidates,
    }


def best_by_world(records: list[dict[str, Any]], min_calls: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record["topology_name"])].append(record)
    rows = []
    for topology_name, world_records in grouped.items():
        summary = summarize_records(world_records)
        if summary["call_count"] < min_calls:
            continue
        rows.append({"topology_name": topology_name, **summary})
    rows.sort(key=lambda row: (-row["branch_match_rate"], -row["call_count"], row["topology_name"]))
    return rows


def selector_promotion(summary: dict[str, Any]) -> str:
    branch_rate = float(summary["branch_match_rate"])
    family_rate = float(summary["family_match_rate"])
    call_count = int(summary["call_count"])
    if call_count < 5:
        return "NO_PROMOTION"
    if branch_rate >= 55.0:
        return "EXACT_SELECTOR"
    if family_rate >= 65.0 and branch_rate >= 30.0:
        return "FAMILY_SELECTOR"
    if family_rate >= 55.0:
        return "DIRECTIONAL_SELECTOR"
    return "OBSERVATION_ONLY"


def selector_sample_warning(summary: dict[str, Any]) -> str:
    call_count = int(summary["call_count"])
    if call_count < 10:
        return "SMALL_SAMPLE"
    if call_count < 25:
        return "MODERATE_SAMPLE"
    return "STABLE_SAMPLE"


def candidate_rows_from_records(
    records: list[dict[str, Any]],
    *,
    min_calls: int,
    selector_source: str,
    signal: str,
    horizon_type: str | None = None,
    horizon: int | None = None,
) -> list[dict[str, Any]]:
    rows = []
    for row in best_by_world(records, min_calls=min_calls):
        candidate = {
            "selector_source": selector_source,
            "signal": signal,
            "horizon_type": horizon_type,
            "horizon": horizon,
            **row,
        }
        candidate["promotion"] = selector_promotion(candidate)
        candidate["sample_warning"] = selector_sample_warning(candidate)
        rows.append(candidate)
    return rows


def recipe_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    promotion_rank = {
        "EXACT_SELECTOR": 4,
        "FAMILY_SELECTOR": 3,
        "DIRECTIONAL_SELECTOR": 2,
        "OBSERVATION_ONLY": 1,
        "NO_PROMOTION": 0,
    }
    sample_rank = {
        "STABLE_SAMPLE": 3,
        "MODERATE_SAMPLE": 2,
        "SMALL_SAMPLE": 1,
    }
    return (
        -promotion_rank.get(str(row["promotion"]), 0),
        -float(row["branch_match_rate"]),
        -float(row["family_match_rate"]),
        -sample_rank.get(str(row["sample_warning"]), 0),
        -int(row["call_count"]),
        str(row["selector_source"]),
        str(row["signal"]),
        str(row.get("horizon_type")),
        int(row["horizon"]) if row.get("horizon") is not None else 0,
    )


def build_world_selector_recipes(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_world: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        by_world[str(candidate["topology_name"])].append(candidate)

    recipes = []
    for topology_name, world_candidates in by_world.items():
        world_candidates.sort(key=recipe_sort_key)
        selected = world_candidates[0]
        recipes.append(
            {
                "topology_name": topology_name,
                "selected_recipe": selected,
                "top_candidates": world_candidates[:8],
                "candidate_count": len(world_candidates),
            }
        )
    recipes.sort(
        key=lambda row: (
            recipe_sort_key(row["selected_recipe"]),
            row["topology_name"],
        )
    )
    return recipes


def selector_recipe_status_counts(recipes: list[dict[str, Any]]) -> dict[str, int]:
    return dict(Counter(str(row["selected_recipe"]["promotion"]) for row in recipes))


def build_audit(
    cases: list[dict[str, Any]],
    horizons: tuple[int, ...],
    min_prior: int,
    min_world_calls: int,
    range_min_sample: int,
) -> dict[str, Any]:
    signals = (
        "WORLD",
        "WORLD_AUTHORITY",
        "WORLD_AUTHORITY_ORIGIN",
        "WORLD_AUTHORITY_INCOMING",
        "LEVEL2_ROOM",
        "LEVEL3_ROOM",
        "LEVEL4_ROOM",
    )
    selector_tests: list[dict[str, Any]] = []
    world_leaders: list[dict[str, Any]] = []
    world_selector_candidates: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    for signal in signals:
        for horizon_type, builder in (
            ("DRAW_LOOKBACK", build_draw_lookback_records),
            ("OCCURRENCE_LOOKBACK", build_occurrence_lookback_records),
        ):
            records_by_horizon = builder(cases, signal, horizons, min_prior)
            for horizon, records in records_by_horizon.items():
                summary = summarize_records(records)
                selector_tests.append(
                    {
                        "signal": signal,
                        "horizon_type": horizon_type,
                        "horizon": int(horizon),
                        **summary,
                    }
                )
                leaders = best_by_world(records, min_calls=min_world_calls)[:10]
                if leaders:
                    world_leaders.append(
                        {
                            "signal": signal,
                            "horizon_type": horizon_type,
                            "horizon": int(horizon),
                            "worlds": leaders,
                        }
                    )
                world_selector_candidates.extend(
                    candidate_rows_from_records(
                        records,
                        min_calls=min_world_calls,
                        selector_source="LOOKBACK",
                        signal=signal,
                        horizon_type=horizon_type,
                        horizon=int(horizon),
                    )
                )
                all_records.extend(records)

    selector_tests.sort(
        key=lambda row: (
            -row["branch_match_rate"],
            -row["call_count"],
            row["signal"],
            row["horizon_type"],
            row["horizon"],
        )
    )
    world_leaders.sort(
        key=lambda row: (
            -row["worlds"][0]["branch_match_rate"],
            -row["worlds"][0]["call_count"],
            row["signal"],
            row["horizon_type"],
            row["horizon"],
        )
    )

    signal_probe = build_signal_probe_summary(cases, min_world_calls=min_world_calls)
    world_selector_candidates.extend(signal_probe["world_selector_candidates"])
    world_selector_recipes = build_world_selector_recipes(world_selector_candidates)

    return {
        "audit_name": "BRANCH_SELECTOR_LOOKBACK_AUDIT",
        "case_count": len(cases),
        "date_start": cases[0]["date"] if cases else None,
        "date_end": cases[-1]["date"] if cases else None,
        "horizons": list(horizons),
        "min_prior": min_prior,
        "selector_tests": selector_tests,
        "top_selector_tests": selector_tests[:25],
        "world_leaders": world_leaders[:50],
        "signal_probe": signal_probe,
        "world_selector_recipe_status_counts": selector_recipe_status_counts(world_selector_recipes),
        "world_selector_recipes": world_selector_recipes,
        "range_profiles": build_range_profiles(cases, min_sample=range_min_sample),
        "notes": [
            "DRAW_LOOKBACK means last N chronological historical transitions.",
            "OCCURRENCE_LOOKBACK means last N prior appearances of the same signal key.",
            "Branch selector is judged walk-forward only: each row can see prior cases, never future cases.",
            "Signal probe tests direct live-safe selector candidates and branch recency/denial candidates.",
            "Range profiles are descriptive only; they show what motion amount a winning branch historically received.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Branch Selector Lookback Audit",
        description="Walk-forward test for pressure-world branch selector lookback horizons.",
    )
    parser.add_argument("--csv-path", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--from-date", default="2015-10-07")
    parser.add_argument("--horizons", default="1,2,3,5,8,13,21,34")
    parser.add_argument("--min-prior", type=int, default=1)
    parser.add_argument("--min-world-calls", type=int, default=5)
    parser.add_argument("--range-min-sample", type=int, default=5)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--print-summary", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    from_date = parse_draw_date(args.from_date)
    horizons = tuple(
        int(part.strip())
        for part in args.horizons.split(",")
        if part.strip()
    )
    if not horizons or any(horizon < 1 for horizon in horizons):
        raise ValueError("--horizons must contain positive integers.")
    if args.min_prior < 1:
        raise ValueError("--min-prior must be at least 1.")

    cases = build_cases(args.csv_path, from_date)
    audit = build_audit(
        cases,
        horizons=horizons,
        min_prior=args.min_prior,
        min_world_calls=args.min_world_calls,
        range_min_sample=args.range_min_sample,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    if args.print_summary:
        print(json.dumps(
            {
                "output": str(args.output),
                "case_count": audit["case_count"],
                "date_start": audit["date_start"],
                "date_end": audit["date_end"],
                "top_selector_tests": audit["top_selector_tests"][:10],
                "top_world_leaders": audit["world_leaders"][:5],
                "top_signal_tests": audit["signal_probe"]["top_signal_tests"][:10],
                "top_signal_worlds": audit["signal_probe"]["signal_world_leaders"][:5],
                "world_selector_recipe_status_counts": audit["world_selector_recipe_status_counts"],
                "top_world_selector_recipes": audit["world_selector_recipes"][:12],
            },
            indent=2,
        ))


if __name__ == "__main__":
    main()
