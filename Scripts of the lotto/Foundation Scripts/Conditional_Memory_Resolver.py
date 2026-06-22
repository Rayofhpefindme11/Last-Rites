from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from Infinite_Inner_World import (
    DEFAULT_CSV_PATH,
    build_draw_set_packet,
    load_historical_draws,
    parse_draw_date,
)
from Seat_Taxonomy import (
    build_conditional_motion_memory_key,
    build_seat_taxonomy_packet,
    live_safe_pressure_context,
    percent,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MEMORY_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "hierarchical_conditional_motion_memory_levels_2_5_2015-10-07.json"
)


def load_memory(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_memory_index(memory: dict[str, Any]) -> dict[int, dict[str, dict[str, Any]]]:
    index: dict[int, dict[str, dict[str, Any]]] = {}
    for scenario in memory["scenarios"]:
        level = int(scenario["memory_level"])
        index.setdefault(level, {})[scenario["scenario_key"]] = scenario
    return index


def live_resolver_case(payload: dict[str, Any]) -> dict[str, Any]:
    live_pressure = live_safe_pressure_context(payload)
    transition = payload["draw_order_transition"]
    face = payload["draw_order_face_identity"]
    current_pressure = payload["current_pressure"]
    burden = payload["lane_burden"]
    pressure_origin = payload["pressure_origin"]
    pressure_authority = payload["pressure_authority"]
    return {
        "date": payload["draw"]["date"],
        "index": payload["draw"]["index"],
        "white_balls": payload["draw"]["white_balls"],
        "sorted_white_balls": payload["draw"]["sorted_white_balls"],
        "topology_name": live_pressure["world"]["topology_name"],
        "world_key": live_pressure["world"]["world_key"],
        "world_slot": live_pressure["world"]["world_slot"],
        "authority_seat": live_pressure["authority_seat"],
        "authority_origin": live_pressure["authority_origin"],
        "pressure_center": live_pressure["pressure_center"],
        "pressure_balance": live_pressure["pressure_balance"],
        "pressure_distribution": live_pressure["pressure_distribution"],
        "map_pressure_type": live_pressure["map_pressure_type"],
        "dominant_pressure_seat": live_pressure["dominant_pressure_seat"],
        "pressure_shape": live_pressure["pressure_shape"],
        "incoming_draw_sign": transition["incoming_draw_sign"],
        "dominant_incoming_draw_lane": transition["dominant_incoming_draw_lane"],
        "incoming_draw_family": transition["incoming_draw_family"],
        "incoming_energy_class": transition["incoming_energy_class"],
        "face_family": face["face_family"],
        "turn_lanes": "-".join(face["turn_lanes"]) if face["turn_lanes"] else "NONE",
        "set_relation": current_pressure["set_relation"],
        "middle_pressure": current_pressure["middle_pressure"],
        "edge_pressure": current_pressure["edge_pressure"],
        "pressure_fusion": current_pressure["pressure_fusion"],
        "pressure_fusion_profile": current_pressure["pressure_fusion_profile"],
        "technical_signature": current_pressure["technical_signature"],
        "highest_burden_seat": burden["highest_burden_seat"],
        "highest_burden_level": burden["highest_burden_level"],
        "highest_burden_state": burden["highest_burden_state"],
        "highest_burden_gauge": burden["highest_burden_gauge"],
        "dominant_origin_seat": pressure_origin["dominant_origin_seat"],
        "dominant_origin_score": pressure_origin["dominant_origin_score"],
        "authority_score": pressure_authority["authority_winner_score"],
        "authority_draw_lane": pressure_authority["authority_winner_draw_lane"],
    }


def pick_draw_index(
    draws: list[Any],
    draw_date: str | None,
    latest: bool,
) -> int:
    if latest or draw_date is None:
        return len(draws) - 1
    target_date = parse_draw_date(draw_date)
    matches = [
        draw.draw_index
        for draw in draws
        if draw.draw_date == target_date
    ]
    if not matches:
        raise ValueError(f"No draw found for --date {draw_date}.")
    return matches[0]


def ranked_outcome(rows: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    counter = Counter(str(row[field]) for row in rows)
    total = sum(counter.values())
    return [
        {"value": value, "count": count, "rate": percent(count, total)}
        for value, count in counter.most_common()
    ]


def matching_records_from_scenarios(
    scenarios: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int]] = set()
    for scenario in scenarios:
        for record in scenario["records"]:
            key = (
                str(record["date"]),
                int(record["index"]),
                int(scenario["memory_level"]),
            )
            if key in seen:
                continue
            seen.add(key)
            row = dict(record)
            row["memory_level"] = scenario["memory_level"]
            row["scenario_key"] = scenario["scenario_key"]
            records.append(row)
    return records


def build_memory_read(matches: list[dict[str, Any]]) -> dict[str, Any]:
    if not matches:
        return {
            "read_status": "NO_MEMORY_MATCH",
            "deepest_matched_level": None,
            "recommended_use": "NO_SYNTHETIC_OR_HISTORICAL_ROOM_YET",
            "outcome_field": {},
        }
    deepest = max(int(match["memory_level"]) for match in matches)
    deepest_matches = [
        match for match in matches
        if int(match["memory_level"]) == deepest
    ]
    repeated_matches = [
        match for match in matches
        if int(match["appearances"]) >= 3
    ]
    evidence_records = matching_records_from_scenarios(matches)
    deepest_records = matching_records_from_scenarios(deepest_matches)
    repeated_records = matching_records_from_scenarios(repeated_matches)
    strongest_repeated = max(
        repeated_matches,
        key=lambda item: (
            int(item["appearances"]),
            float(item["outcomes"]["primary_family_rate"]),
            float(item["outcomes"]["primary_branch_rate"]),
        ),
        default=None,
    )

    if deepest >= 4:
        read_status = "EXACT_MOMENT_MEMORY_AVAILABLE"
    elif strongest_repeated is not None:
        read_status = "REPEATED_FIELD_MEMORY_AVAILABLE"
    else:
        read_status = "BROAD_MEMORY_ONLY"

    if strongest_repeated is not None:
        recommended_use = strongest_repeated["live_use"]
    else:
        recommended_use = deepest_matches[0]["live_use"]

    return {
        "read_status": read_status,
        "deepest_matched_level": deepest,
        "recommended_use": recommended_use,
        "strongest_repeated_room": summarize_scenario(strongest_repeated)
        if strongest_repeated
        else None,
        "deepest_rooms": [summarize_scenario(match) for match in deepest_matches],
        "outcome_field": {
            "all_matched_records": len(evidence_records),
            "deepest_records": len(deepest_records),
            "repeated_records": len(repeated_records),
            "branch_rank": ranked_outcome(evidence_records, "actual_branch"),
            "family_rank": ranked_outcome(evidence_records, "actual_family"),
            "lane_rank": ranked_outcome(evidence_records, "actual_lane"),
            "flow_rank": ranked_outcome(evidence_records, "outgoing_flow"),
            "transfer_rank": ranked_outcome(evidence_records, "outgoing_transfer"),
            "sign_rank": ranked_outcome(evidence_records, "outgoing_sign_pattern"),
        },
    }


def summarize_scenario(scenario: dict[str, Any] | None) -> dict[str, Any] | None:
    if scenario is None:
        return None
    outcomes = scenario["outcomes"]
    condition = scenario["condition"]
    return {
        "memory_level": scenario["memory_level"],
        "scenario_key": scenario["scenario_key"],
        "appearances": scenario["appearances"],
        "truth_authority": scenario["truth_authority"],
        "live_use": scenario["live_use"],
        "topology_name": condition["topology_name"],
        "authority_seat": condition["authority_seat"],
        "authority_origin": condition["authority_origin"],
        "primary_family": outcomes["primary_family"],
        "primary_family_rate": outcomes["primary_family_rate"],
        "primary_branch": outcomes["primary_branch"],
        "primary_branch_rate": outcomes["primary_branch_rate"],
        "secondary_branch": outcomes["secondary_branch"],
        "secondary_branch_rate": outcomes["secondary_branch_rate"],
        "branch_counts": outcomes["branch_counts"],
        "family_counts": outcomes["family_counts"],
    }


def build_resolution(
    payload: dict[str, Any],
    memory: dict[str, Any],
) -> dict[str, Any]:
    case = live_resolver_case(payload)
    memory_index = build_memory_index(memory)
    level_queries: list[dict[str, Any]] = []
    matches: list[dict[str, Any]] = []
    for level in (2, 3, 4, 5):
        key = build_conditional_motion_memory_key(case, level=level)
        scenario = memory_index.get(level, {}).get(key)
        if scenario is not None:
            match = dict(scenario)
            match["memory_level"] = level
            matches.append(match)
        level_queries.append(
            {
                "level": level,
                "key": key,
                "matched": scenario is not None,
                "scenario": summarize_scenario(
                    dict(scenario, memory_level=level) if scenario else None
                ),
            }
        )

    return {
        "schema": "iiw.conditional_memory_resolver.v1",
        "rule": (
            "resolve current motion by matching live-safe Seat Taxonomy fields "
            "against historical/synthetic conditional memory rooms"
        ),
        "draw": {
            "date": payload["draw"]["date"],
            "index": payload["draw"]["index"],
            "white_balls": payload["draw"]["white_balls"],
            "sorted_white_balls": payload["draw"]["sorted_white_balls"],
        },
        "live_case": case,
        "level_queries": level_queries,
        "memory_read": build_memory_read(matches),
        "truth_doctrine": {
            "official_history": "proof of what happened",
            "synthetic_memory": "coverage evidence for possible motion rooms",
            "current_draw": "current truth used to select which memory room applies",
            "live_rule": (
                "use deepest matching memory as evidence; do not let synthetic "
                "coverage override official history when both exist"
            ),
        },
    }


def print_resolution(resolution: dict[str, Any]) -> None:
    draw = resolution["draw"]
    case = resolution["live_case"]
    read = resolution["memory_read"]
    print("=" * 72)
    print("Conditional Memory Resolver")
    print("=" * 72)
    print(f"Date                  {draw['date']}")
    print(f"White balls           {draw['white_balls']}")
    print(f"Sorted                {draw['sorted_white_balls']}")
    print(
        "Live room             "
        f"{case['topology_name']} | {case['map_pressure_type']} | "
        f"{case['pressure_center']} {case['pressure_balance']} "
        f"{case['pressure_distribution']}"
    )
    print(
        "Authority             "
        f"{case['authority_seat']} {case['authority_origin']} "
        f"score={case['authority_score']}"
    )
    print(
        "Incoming              "
        f"{case['incoming_draw_family']} | sign={case['incoming_draw_sign']} | "
        f"lane={case['dominant_incoming_draw_lane']}"
    )
    print(
        "Body                  "
        f"{case['set_relation']} | middle={case['middle_pressure']} | "
        f"edge={case['edge_pressure']}"
    )
    print()
    print("Memory Matches:")
    for query in resolution["level_queries"]:
        scenario = query["scenario"]
        if scenario is None:
            print(f"  L{query['level']} miss")
            continue
        print(
            f"  L{query['level']} match | n={scenario['appearances']} | "
            f"{scenario['truth_authority']} | {scenario['live_use']}"
        )
        print(
            "    field             "
            f"family={scenario['primary_family']} {scenario['primary_family_rate']}% | "
            f"branch={scenario['primary_branch']} {scenario['primary_branch_rate']}%"
        )
    print()
    print("Memory Read:")
    print(f"  status              {read['read_status']}")
    print(f"  deepest level       {read['deepest_matched_level']}")
    print(f"  recommended use     {read['recommended_use']}")
    strongest = read.get("strongest_repeated_room")
    if strongest:
        print(
            "  strongest repeated  "
            f"L{strongest['memory_level']} n={strongest['appearances']} "
            f"{strongest['truth_authority']}"
        )
    field = read["outcome_field"]
    if field:
        print(f"  matched records     {field['all_matched_records']}")
        print(f"  family rank         {field['family_rank'][:5]}")
        print(f"  branch rank         {field['branch_rank'][:5]}")
        print(f"  lane rank           {field['lane_rank'][:5]}")
        print(f"  flow rank           {field['flow_rank'][:5]}")
        print(f"  transfer rank       {field['transfer_rank'][:5]}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Conditional Memory Resolver",
        description="Resolve a current Seat Taxonomy room against conditional memory.",
    )
    parser.add_argument(
        "--csv-path",
        type=Path,
        default=DEFAULT_CSV_PATH,
        help="Path to the Powerball history CSV.",
    )
    parser.add_argument(
        "--memory-path",
        type=Path,
        default=DEFAULT_MEMORY_PATH,
        help="Path to hierarchical conditional memory JSON.",
    )
    parser.add_argument(
        "--date",
        help="Resolve a specific draw date. Defaults to latest draw.",
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Resolve the latest draw.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print resolver output as JSON.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    draws = load_historical_draws(args.csv_path)
    index = pick_draw_index(draws, args.date, latest=args.latest)
    current_packet = build_draw_set_packet(draws, index)
    taxonomy = build_seat_taxonomy_packet(current_packet, next_packet=None)
    memory = load_memory(args.memory_path)
    resolution = build_resolution(taxonomy.to_payload(), memory)
    if args.json:
        print(json.dumps(resolution, indent=2))
        return
    print_resolution(resolution)


if __name__ == "__main__":
    main()
