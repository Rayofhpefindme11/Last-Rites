from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
HEAVENS_LINK_CORE_DIR = SCRIPT_PATH.parent
REALITY_MARBLE_SCRIPTS_DIR = HEAVENS_LINK_CORE_DIR.parent
SET_RANGE_GLOSSARY_PATH = HEAVENS_LINK_CORE_DIR / "Set_Range_Glossary.py"
CONTRADICTION_ANSWER_MAP_PATH = HEAVENS_LINK_CORE_DIR / "Contradiction_Answer_Map.py"
IIW_PATH = REALITY_MARBLE_SCRIPTS_DIR / "Infinite_Inner_World.py"

SEATS = ("S1", "S2", "S3", "S4", "S5")
ADJACENT_PAIRS = (
    ("S1", "S2", "entry_pair"),
    ("S2", "S3", "middle_left_pair"),
    ("S3", "S4", "middle_right_pair"),
    ("S4", "S5", "exit_pair"),
)
DUO_TRIO_FORMS = (
    ("S1_S2", "S3_S4_S5", "front_duo_to_back_trio"),
    ("S1_S2_S3", "S4_S5", "front_trio_to_back_duo"),
    ("S1_S3", "S4_S5", "front_anchor_to_exit_duo"),
    ("S1_S5", "S2_S3_S4", "span_anchor_to_middle_engine"),
)


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SET_RANGE_GLOSSARY = load_module("serenity_voice_of_hope_set_range_glossary", SET_RANGE_GLOSSARY_PATH)
CONTRADICTION_ANSWER_MAP = load_module(
    "serenity_voice_of_hope_contradiction_answer_map",
    CONTRADICTION_ANSWER_MAP_PATH,
)
IIW = load_module("serenity_voice_of_hope_iiw", IIW_PATH)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def packet_id(prefix: str, payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return f"{prefix}-{hashlib.sha1(raw).hexdigest()[:12]}"


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value or "").strip()))
    except (TypeError, ValueError):
        return default


def unique(values: Any) -> list[Any]:
    if not isinstance(values, list):
        values = [values] if values not in (None, "") else []
    out: list[Any] = []
    seen: set[str] = set()
    for value in values:
        key = str(value)
        if key in seen or value in (None, ""):
            continue
        seen.add(key)
        out.append(value)
    return out


def compact_terms(payload: Any) -> list[str]:
    terms: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            terms.append(str(key))
            terms.extend(compact_terms(value))
    elif isinstance(payload, list):
        for value in payload:
            terms.extend(compact_terms(value))
    elif payload not in (None, ""):
        terms.append(str(payload))
    return unique([term for term in terms if str(term).strip()])


def numbers(values: Any) -> list[int]:
    return sorted({parse_int(value) for value in values or [] if parse_int(value)})


def ordered_numbers(values: Any) -> list[int]:
    return [parse_int(value) for value in values or [] if parse_int(value)]


def numbers_from_range_definitions(definitions: dict[str, Any]) -> list[int]:
    values: set[int] = set()
    for definition in definitions.values():
        if not isinstance(definition, dict):
            continue
        for low, high in definition.get("number_bands") or []:
            start = parse_int(low)
            end = parse_int(high)
            if start and end:
                values.update(range(start, end + 1))
    return sorted(values)


def range_midpoint(definition: dict[str, Any]) -> float:
    bands = definition.get("number_bands") or []
    if not bands:
        return 0.0
    low, high = bands[0]
    return (parse_int(low) + parse_int(high)) / 2


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_safe(payload) for key, payload in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(payload) for payload in value]
    return value


def canonical_micro_range_glossary() -> dict[str, Any]:
    full = json_safe(SET_RANGE_GLOSSARY.canonical_range_glossary())
    middle = full.get("middle_slot_ranges") or {}
    s2_core = {
        name: definition
        for name, definition in middle.items()
        if str(name).startswith("S2_CORE_")
    }
    s3_hinge = {
        name: definition
        for name, definition in middle.items()
        if str(name).startswith("S3_HINGE_")
    }
    s4_exit = {
        name: definition
        for name, definition in middle.items()
        if str(name).startswith("S4_EXIT_")
    }
    return {
        "status": "CANONICAL_MICRO_RANGE_GLOSSARY_READY",
        "schema": full.get("schema"),
        "s1_starter_ranges": full.get("s1_starter_ranges") or {},
        "s2_core_ranges": s2_core,
        "s3_hinge_ranges": s3_hinge,
        "s4_exit_ranges": s4_exit,
        "s5_endpoint_ranges": full.get("s5_endpoint_ranges") or {},
        "entry_exit_gap_ranges": full.get("entry_exit_gap_ranges") or {},
        "set_health_middle_gap_ranges": full.get("set_health_middle_gap_ranges") or {},
        "range_counts": {
            "s1_starter": len(full.get("s1_starter_ranges") or {}),
            "s2_core": len(s2_core),
            "s3_hinge": len(s3_hinge),
            "s4_exit": len(s4_exit),
            "s5_endpoint": len(full.get("s5_endpoint_ranges") or {}),
        },
        "seat_language": {
            "S1": "starter ranges: LOW/MID/HIGH/EXT_HIGH + HOLLOW/GALLEON/ARRANCAR",
            "S2": "core ranges: BABE through HIGH_KING",
            "S3": "hinge ranges: BABE through HIGH_KING",
            "S4": "exit ranges: BABE through HIGH_KING",
            "S5": "endpoint ranges: EXT_LOW through HIGH endpoint titles",
        },
        "law": (
            "This is the full named lane vocabulary. A draw-specific question may call only a few terms, "
            "but downstream scripts must read these names before deciding which numbers qualify for the job."
        ),
    }


def stage20_contract(condition_packet: dict[str, Any]) -> dict[str, Any]:
    requirements = condition_packet.get("requirements") or {}
    construction = requirements.get("construction_profile") or {}
    contract = construction.get("stage20_question_contract") or {}
    return contract if isinstance(contract, dict) else {}


def construction_profile(condition_packet: dict[str, Any]) -> dict[str, Any]:
    return ((condition_packet.get("requirements") or {}).get("construction_profile") or {})


def relation_demand(condition_packet: dict[str, Any]) -> dict[str, Any]:
    return (construction_profile(condition_packet).get("relation_demand") or {})


def range_contract(condition_packet: dict[str, Any]) -> dict[str, Any]:
    relation = relation_demand(condition_packet)
    contract = relation.get("range_question_contract") or construction_profile(condition_packet).get("range_question_contract") or {}
    return contract if isinstance(contract, dict) else {}


def canonical_contradiction_packet(condition_packet: dict[str, Any]) -> dict[str, Any]:
    active = condition_packet.get("active_question") or {}
    requirements = condition_packet.get("requirements") or {}
    construction = construction_profile(condition_packet)
    stage20 = construction.get("stage20_question_contract") or {}
    adaptive = requirements.get("adaptive_question_context") or {}
    active_adaptive = adaptive.get("active_adaptive_question") or {}
    explicit = active_adaptive.get("explicit_question_contract") or {}
    return (
        active.get("canonical_contradiction_packet")
        or requirements.get("canonical_contradiction_packet")
        or construction.get("canonical_contradiction_packet")
        or stage20.get("canonical_contradiction_packet")
        or active_adaptive.get("contradiction_glossary")
        or explicit.get("contradiction_glossary")
        or {}
    )


def answer_requirement_packet(
    condition_packet: dict[str, Any],
    source_body: list[int] | None = None,
    situation_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active = condition_packet.get("active_question") or {}
    requirements = condition_packet.get("requirements") or {}
    construction = construction_profile(condition_packet)
    stage20 = construction.get("stage20_question_contract") or {}
    existing = (
        requirements.get("answer_requirement_packet")
        or construction.get("answer_requirement_packet")
        or stage20.get("answer_requirement_packet")
        or {}
    )
    if existing and existing.get("answer_subtype_profile"):
        return existing
    return CONTRADICTION_ANSWER_MAP.build_answer_requirement_packet(
        question_id=active.get("question_id"),
        contradiction_packet=canonical_contradiction_packet(condition_packet),
        source_body=source_body or [],
        situation_context=situation_context or {"condition_packet": condition_packet},
    )


def canonical_contradiction_score(
    *,
    seat: str,
    range_name: str,
    definition: dict[str, Any],
    range_numbers: set[int],
    source_value: int,
    source_body: list[int],
    seat_answer: dict[str, Any],
    contradiction_packet: dict[str, Any],
    question_id: str,
    answer_subtype_profile: dict[str, Any] | None = None,
) -> tuple[float, list[str]]:
    return CONTRADICTION_ANSWER_MAP.score_range_from_answer_map(
        seat=seat,
        range_name=range_name,
        definition=definition,
        range_numbers=range_numbers,
        source_value=source_value,
        source_body=source_body,
        seat_answer=seat_answer,
        contradiction_packet=contradiction_packet,
        question_id=question_id,
        answer_subtype_profile=answer_subtype_profile,
    )


def source_answer(iiw_packet: dict[str, Any], transference_packet: dict[str, Any]) -> dict[str, Any]:
    live_safe = iiw_packet.get("live_safe") or {}
    scope = iiw_packet.get("address_scope") or {}
    source_technical = (
        transference_packet.get("source_technical_context")
        or live_safe.get("full_set_technical_body")
        or scope.get("full_set_technical_body")
        or {}
    )
    return {
        "status": "SOURCE_ANSWER_READY",
        "as_of": live_safe.get("as_of") or (transference_packet.get("source") or {}).get("date"),
        "sorted_body": numbers(scope.get("sorted_body") or live_safe.get("current_numbers") or []),
        "draw_order_body": ordered_numbers(live_safe.get("current_draw_order") or []),
        "sorted_birth_path": scope.get("sorted_birth_path") or live_safe.get("current_birth_path"),
        "motion_bp": scope.get("motion_bp") or live_safe.get("draw_order_motion", {}).get("motion_bp"),
        "set_style": live_safe.get("current_set_style"),
        "gap_symbols": live_safe.get("current_gap_symbols"),
        "source_set_health": scope.get("set_health") or live_safe.get("current_set_health"),
        "source_full_set_relation": scope.get("full_set_relation") or live_safe.get("current_full_set_relation"),
        "source_full_set_technical_signature": (
            scope.get("full_set_technical_signature")
            or live_safe.get("current_full_set_technical_signature")
            or source_technical.get("full_set_technical_signature")
        ),
        "source_technical_body": source_technical,
        "law": "The Answer starts by naming the current body so later stages can decide what must continue, break, reverse, or be countered.",
    }


def transference_motion_contract(condition_packet: dict[str, Any]) -> dict[str, Any]:
    active = condition_packet.get("active_question") or {}
    requirements = condition_packet.get("requirements") or {}
    construction = construction_profile(condition_packet)
    contracts = [
        active.get("explicit_question_contract") or {},
        requirements.get("explicit_question_contract") or {},
        construction.get("explicit_question_contract") or {},
    ]
    for contract in contracts:
        required = contract.get("required") or {}
        motion_contract = required.get("transference_motion_contract") or {}
        if motion_contract:
            return motion_contract
    return {}


def precise_question_answer(
    *,
    condition_packet: dict[str, Any],
    transference_packet: dict[str, Any],
    source: dict[str, Any],
) -> dict[str, Any]:
    contract = transference_motion_contract(condition_packet)
    if not contract:
        return {
            "schema": "serenity.life_link.precise_question_answer.v1",
            "status": "NO_PRECISE_QUESTION_CONTRACT",
            "law": "Precise Answer requires Question's D-lane caste-side transference contract.",
        }
    crystallization = transference_packet.get("motion_to_sorted_crystallization") or {}
    draw_lane_to_sorted = crystallization.get("draw_lane_to_sorted_seat") or {}
    produced_by_draw_lane = {
        str(row.get("draw_lane") or ""): parse_int(row.get("produced_number"))
        for row in crystallization.get("lane_number_production") or []
        if isinstance(row, dict)
    }
    source_sorted = [parse_int(value) for value in source.get("sorted_body") or []]
    source_by_seat = {
        f"S{index + 1}": value
        for index, value in enumerate(source_sorted)
    }
    source_draw_order = [parse_int(value) for value in source.get("draw_order_body") or []]
    source_by_draw_lane = {
        f"D{index + 1}": value
        for index, value in enumerate(source_draw_order[:5])
    }

    rows: list[dict[str, Any]] = []
    for lane in contract.get("lane_questions") or []:
        if not isinstance(lane, dict):
            continue
        draw_lane = str(lane.get("draw_lane") or "")
        source_sorted_seat = str(lane.get("sorted_seat") or draw_lane_to_sorted.get(draw_lane) or "")
        if not source_sorted_seat:
            source_sorted_seat = str(draw_lane_to_sorted.get(draw_lane) or "")
        selected_delta = parse_int(lane.get("selected_delta"))
        window = lane.get("caste_window") or {}
        min_delta = parse_int(window.get("min_delta"))
        max_delta = parse_int(window.get("max_delta"))
        low_delta = min(min_delta, max_delta)
        high_delta = max(min_delta, max_delta)
        source_number = (
            produced_by_draw_lane.get(draw_lane)
            or source_by_draw_lane.get(draw_lane)
            or source_by_seat.get(source_sorted_seat, 0)
        )
        projected_number = source_number + selected_delta if source_number else 0
        projected_min = source_number + low_delta if source_number else 0
        projected_max = source_number + high_delta if source_number else 0
        side_projected_values = [
            source_number + parse_int(value)
            for value in lane.get("side_values") or []
            if source_number and parse_int(value)
        ]
        row = {
            "draw_lane": draw_lane,
            "draw_lane_role": lane.get("draw_lane_role"),
            "source_sorted_seat": source_sorted_seat,
            "future_sorted_seat": None,
            "source_number": source_number,
            "required_caste": lane.get("required_caste"),
            "caste_window": window,
            "side_bias": lane.get("side_bias"),
            "side_values": lane.get("side_values") or [],
            "selected_delta": selected_delta,
            "projected_range": {
                "min": projected_min,
                "max": projected_max,
            },
            "side_projected_values": side_projected_values,
            "projected_number": projected_number,
            "valid_number": 1 <= projected_number <= 69,
            "question": lane.get("question"),
            "law": "D-lane output is solved first. Future S1-S5 is assigned only after projected D outputs are sorted.",
        }
        rows.append(row)

    future_rows = sorted(
        [row for row in rows if row.get("valid_number")],
        key=lambda row: (parse_int(row.get("projected_number")), str(row.get("draw_lane") or "")),
    )
    by_future_sorted_seat: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(future_rows[:5]):
        future_seat = f"S{index + 1}"
        row["future_sorted_seat"] = future_seat
        by_future_sorted_seat[future_seat] = row

    source_to_future_map = {
        str(row.get("draw_lane") or ""): {
            "source_sorted_seat": row.get("source_sorted_seat"),
            "future_sorted_seat": row.get("future_sorted_seat"),
            "source_number": row.get("source_number"),
            "projected_number": row.get("projected_number"),
            "projected_range": row.get("projected_range"),
        }
        for row in rows
    }
    projected_body = [
        parse_int((by_future_sorted_seat.get(seat) or {}).get("projected_number"))
        for seat in SEATS
    ]
    complete = len(projected_body) == 5 and all(1 <= value <= 69 for value in projected_body)
    technical_body = (
        json_safe(IIW.build_full_set_technical_body(projected_body))
        if complete
        else {"status": "NO_PRECISE_PROJECTED_TECHNICAL_BODY"}
    )
    return {
        "schema": "serenity.life_link.precise_question_answer.v1",
        "status": "PRECISE_QUESTION_ANSWER_READY" if complete else "PRECISE_QUESTION_ANSWER_INCOMPLETE",
        "delta_mode": contract.get("delta_mode"),
        "selected_delta_draw_order": contract.get("selected_delta") or [],
        "d_to_s_crystallization": {
            "draw_lane_to_sorted_seat": draw_lane_to_sorted,
            "sorted_seat_to_draw_lane": crystallization.get("sorted_seat_to_draw_lane") or {},
            "law": "This is source-draw crystallization only. It cannot be used as future S1-S5 authority.",
        },
        "draw_lane_answer": rows,
        "source_to_future_seat_map": source_to_future_map,
        "sorted_seat_answer": {
            seat: by_future_sorted_seat.get(seat) or {}
            for seat in SEATS
        },
        "projected_sorted_body": projected_body,
        "projected_body_key": "-".join(str(value) for value in projected_body if value),
        "voice_set_health_reflection": {
            "set_health": technical_body.get("middle_health"),
            "s2_s4_form": technical_body.get("s2_s4_form"),
            "middle_slot_signature": technical_body.get("middle_slot_signature"),
            "s2_middle_slot_signature": technical_body.get("s2_middle_slot_signature"),
            "s3_middle_slot_signature": technical_body.get("s3_middle_slot_signature"),
            "s4_middle_slot_signature": technical_body.get("s4_middle_slot_signature"),
            "full_set_relation": technical_body.get("full_relation"),
            "entry_exit_form": technical_body.get("entry_exit_form"),
            "s1_starter_signature": technical_body.get("s1_signature"),
            "s5_endpoint_signature": technical_body.get("s5_signature"),
            "full_set_technical_signature": technical_body.get("technical_signature"),
            "full_set_technical_body": technical_body,
        },
        "new_garden_contract": {
            "status": "PRECISE_ANSWER_READY_FOR_NEW_GARDEN" if complete else "PRECISE_ANSWER_NOT_READY_FOR_GARDEN",
            "lane_lists": {
                seat.lower(): [parse_int((by_future_sorted_seat.get(seat) or {}).get("projected_number"))]
                for seat in SEATS
                if parse_int((by_future_sorted_seat.get(seat) or {}).get("projected_number"))
            },
            "body": projected_body,
            "set_health": technical_body.get("middle_health"),
            "full_set_relation": technical_body.get("full_relation"),
            "law": (
                "New Garden may materialize this precise Answer directly; old Garden still uses committed_answer. "
                "Future S1-S5 is sorted from D-lane projected outputs, not inherited from the source draw map."
            ),
        },
        "law": (
            "Answer consumes Question's DS/D-lane caste-side contract, solves D-lane output first, "
            "then derives future sorted seats from those outputs, "
            "and translates the result into Voice's set health and relation language."
        ),
    }


def body_shape_answer(condition_packet: dict[str, Any], gap_geometry_packet: dict[str, Any], convergence_packet: dict[str, Any]) -> dict[str, Any]:
    construction = construction_profile(condition_packet)
    relation = relation_demand(condition_packet)
    counters = relation.get("relation_counter_candidates") or {}
    return {
        "status": "BODY_SHAPE_ANSWER_READY",
        "target_set_classes": unique(construction.get("target_set_classes") or []),
        "target_postures": unique(construction.get("target_postures") or []),
        "preferred_gap_families": unique(construction.get("preferred_gap_families") or []),
        "preferred_set_styles": unique(construction.get("preferred_set_styles") or []),
        "allowed_gap_families": unique([row.get("gap_family") for row in gap_geometry_packet.get("allowed_gap_families") or [] if isinstance(row, dict)]),
        "allowed_set_styles": unique([row.get("set_style") for row in gap_geometry_packet.get("allowed_set_styles") or [] if isinstance(row, dict)]),
        "set_health_candidates": unique(counters.get("set_health") or []),
        "full_relation_candidates": unique(counters.get("full_set_relation") or []),
        "technical_signature_candidates": unique(counters.get("full_set_technical_signature") or []),
        "burden": convergence_packet.get("required_burden") or {},
        "source_relation_context": {
            "source_s1_starter_signature": relation.get("source_s1_starter_signature"),
            "source_entry_exit_form": relation.get("source_entry_exit_form"),
            "source_s2_s4_form": relation.get("source_s2_s4_form"),
            "source_set_health": relation.get("source_set_health"),
            "source_full_set_relation": relation.get("source_full_set_relation"),
            "source_s5_endpoint_signature": relation.get("source_s5_endpoint_signature"),
        },
        "law": "Body shape answer names the body the draw is asking for before number selection; it is the first major reduction layer.",
    }


def relation_answer(condition_packet: dict[str, Any]) -> dict[str, Any]:
    relation = relation_demand(condition_packet)
    contract = range_contract(condition_packet)
    requested = contract.get("requested_range_glossary") or {}
    lane_precision = contract.get("lane_precision_contract") or {}
    micro_intent = contract.get("micro_range_intent") or {}
    return {
        "status": "RELATION_ANSWER_READY",
        "source_relation": {
            "s1": relation.get("source_s1_starter_signature"),
            "entry_exit": relation.get("source_entry_exit_form"),
            "middle": relation.get("source_s2_s4_form"),
            "set_health": relation.get("source_set_health"),
            "full_relation": relation.get("source_full_set_relation"),
            "s5": relation.get("source_s5_endpoint_signature"),
        },
        "requested_range_glossary": requested,
        "lane_precision_contract": lane_precision,
        "micro_range_intent": micro_intent,
        "relation_counter_candidates": relation.get("relation_counter_candidates") or {},
        "relation_questions": {
            "entry_exit": "How far should S1-S2 and S4-S5 open or contain?",
            "middle_health": "What S2-S4 middle body is being asked?",
            "full_relation": "Does the whole set tilt, balance, bridge, lock, or stretch?",
            "endpoint": "What endpoint burden is required to finish the body?",
        },
        "law": "Relation answer is the grammar of the body. It prevents a set from passing only because its individual numbers are legal.",
    }


def micro_range_answer(condition_packet: dict[str, Any], seats: dict[str, Any]) -> dict[str, Any]:
    contract = range_contract(condition_packet)
    requested = contract.get("requested_range_glossary") or {}
    lane_contract = contract.get("lane_precision_contract") or {}
    canonical = canonical_micro_range_glossary()
    seat_to_contract_key = {
        "S1": "s1",
        "S2": "s2",
        "S3": "s3",
        "S4": "s4",
        "S5": "s5",
    }
    glossary_groups = {
        "S1": requested.get("s1_starter_ranges") or {},
        "S2": requested.get("middle_slot_ranges") or {},
        "S3": requested.get("middle_slot_ranges") or {},
        "S4": requested.get("middle_slot_ranges") or {},
        "S5": requested.get("s5_endpoint_ranges") or {},
    }
    canonical_lane_ranges = {
        "S1": canonical.get("s1_starter_ranges") or {},
        "S2": canonical.get("s2_core_ranges") or {},
        "S3": canonical.get("s3_hinge_ranges") or {},
        "S4": canonical.get("s4_exit_ranges") or {},
        "S5": canonical.get("s5_endpoint_ranges") or {},
    }
    canonical_family = {
        "S1": "S1_STARTER",
        "S2": "S2_CORE",
        "S3": "S3_HINGE",
        "S4": "S4_EXIT",
        "S5": "S5_ENDPOINT",
    }
    by_seat: dict[str, Any] = {}
    called_vs_canonical: dict[str, Any] = {}
    for seat in SEATS:
        called_names = unique((seats.get(seat) or {}).get("explicit_range_names") or [])
        glossary = glossary_groups.get(seat) or {}
        lane_payload = lane_contract.get(seat_to_contract_key[seat]) or {}
        contract_lane_ranges = lane_payload.get("ranges") or {}
        full_lane_ranges = canonical_lane_ranges.get(seat) or {}
        called_defs = {
            name: (glossary.get(name) or contract_lane_ranges.get(name) or full_lane_ranges.get(name) or {})
            for name in called_names
        }
        unresolved = [name for name, definition in called_defs.items() if not definition]
        called_vs_canonical[seat] = {
            "canonical_family": canonical_family[seat],
            "called_for_range_names": called_names,
            "called_for_range_definitions": called_defs,
            "unresolved_called_ranges": unresolved,
            "canonical_available_range_count": len(full_lane_ranges),
        }
        by_seat[seat] = {
            "status": "MICRO_RANGE_SEAT_READY" if called_names else "NO_MICRO_RANGE_ASK",
            "canonical_family": canonical_family[seat],
            "committed_range_name": (seats.get(seat) or {}).get("committed_range_name"),
            "committed_numbers": (seats.get(seat) or {}).get("committed_numbers") or [],
            "commitment_confidence": (seats.get(seat) or {}).get("commitment_confidence"),
            "called_for_range_names": called_names,
            "called_for_range_definitions": called_defs,
            "called_for_numbers": (seats.get(seat) or {}).get("explicit_numbers") or [],
            "contract_lane_range_count": len(contract_lane_ranges),
            "contract_lane_ranges": contract_lane_ranges,
            "available_lane_range_count": len(full_lane_ranges),
            "available_lane_ranges": full_lane_ranges,
            "job": (seats.get(seat) or {}).get("job"),
            "law": "Called-for ranges are the micro-range language this draw explicitly asks this seat to solve.",
        }
    return {
        "status": "MICRO_RANGE_ANSWER_READY",
        "by_seat": by_seat,
        "entry_exit_gap_ranges": requested.get("entry_exit_gap_ranges") or {},
        "set_health_middle_gap_ranges": requested.get("set_health_middle_gap_ranges") or {},
        "middle_slot_ranges": requested.get("middle_slot_ranges") or {},
        "s1_starter_ranges": requested.get("s1_starter_ranges") or {},
        "s5_endpoint_ranges": requested.get("s5_endpoint_ranges") or {},
        "lane_precision_contract": lane_contract,
        "canonical_micro_range_glossary": canonical,
        "called_vs_canonical": called_vs_canonical,
        "law": (
            "Micro Range Answer publishes the S1-S5 range calls and their numeric bands in one place. "
            "Downstream should read this before treating broad seat numbers as equally valid."
        ),
    }


def seat_answer_demands(
    *,
    condition_packet: dict[str, Any],
    affinity_packet: dict[str, Any],
) -> dict[str, Any]:
    contract = stage20_contract(condition_packet)
    lanes = contract.get("lanes") or {}
    seat_roles = affinity_packet.get("seat_roles") or {}
    result: dict[str, Any] = {}
    for seat in SEATS:
        lane = lanes.get(seat) or {}
        role = seat_roles.get(seat) or {}
        role_fit = numbers([row.get("number") for row in role.get("role_fit_numbers") or [] if isinstance(row, dict)])
        explicit_numbers = numbers(lane.get("explicit_numbers") or [])
        result[seat] = {
            "status": "SEAT_ANSWER_READY" if lane or role else "NO_SEAT_ANSWER",
            "seat": seat,
            "job": {
                "S1": "starter / entry ignition",
                "S2": "second-seat core / front handoff",
                "S3": "hinge / middle turn",
                "S4": "exit body / tail handoff",
                "S5": "endpoint / final burden",
            }[seat],
            "ask_strength": lane.get("ask_strength"),
            "explicit_range_names": unique(lane.get("explicit_range_names") or []),
            "surgical_range_names": unique(lane.get("surgical_range_names") or []),
            "contradiction_range_names": unique(lane.get("contradiction_range_names") or []),
            "committed_range_name": lane.get("committed_range_name"),
            "committed_numbers": numbers(lane.get("committed_numbers") or []),
            "commitment_score": lane.get("commitment_score"),
            "commitment_confidence": lane.get("commitment_confidence"),
            "commitment_reasons": lane.get("commitment_reasons") or [],
            "explicit_numbers": explicit_numbers,
            "role_fit_numbers": role_fit[:20],
            "range_to_role_logic": {
                "committed_range_is_first_class_answer": bool(lane.get("committed_range_name")),
                "explicit_range_names_are_required_language": bool(lane.get("explicit_range_names") or []),
                "surgical_range_names_are_precision_language": bool(lane.get("surgical_range_names") or []),
                "role_fit_numbers_are_support_language": bool(role_fit),
            },
            "required_if_present": numbers(lane.get("committed_numbers") or []) or explicit_numbers[:],
            "support_if_present": sorted(set(role_fit[:20]) - set(explicit_numbers)),
            "law": "A seat answer names what kind of inhabitant the draw is asking for before any full body is built.",
        }
    return result


def adjacent_pair_demands(seats: dict[str, Any], condition_packet: dict[str, Any]) -> dict[str, Any]:
    contract = range_contract(condition_packet)
    requested = contract.get("requested_range_glossary") or {}
    entry_exit = requested.get("entry_exit_gap_ranges") or {}
    health = requested.get("set_health_middle_gap_ranges") or {}
    pair_gap_language = {
        "entry_pair": unique(list(entry_exit.keys())),
        "middle_left_pair": unique(list(health.keys())),
        "middle_right_pair": unique(list(health.keys())),
        "exit_pair": unique(list(entry_exit.keys())),
    }
    result: dict[str, Any] = {}
    for left, right, label in ADJACENT_PAIRS:
        left_payload = seats.get(left) or {}
        right_payload = seats.get(right) or {}
        result[label] = {
            "status": "PAIR_ANSWER_READY",
            "left_seat": left,
            "right_seat": right,
            "left_ranges": left_payload.get("explicit_range_names") or [],
            "right_ranges": right_payload.get("explicit_range_names") or [],
            "left_numbers": left_payload.get("explicit_numbers") or [],
            "right_numbers": right_payload.get("explicit_numbers") or [],
            "gap_language": pair_gap_language.get(label) or [],
            "pair_question": {
                "entry_pair": "Which S1-S2 opening best starts the answer?",
                "middle_left_pair": "Which S2-S3 handoff best carries pressure into the hinge?",
                "middle_right_pair": "Which S3-S4 turn best converts the hinge into the exit?",
                "exit_pair": "Which S4-S5 finish best completes the endpoint burden?",
            }[label],
            "candidate_reduction_logic": {
                "must_respect_left_seat": True,
                "must_respect_right_seat": True,
                "must_respect_gap_language": bool(pair_gap_language.get(label)),
                "single_number_fit_is_not_enough": True,
            },
            "law": "A pair answer rejects numbers that are individually legal but relationally wrong.",
        }
    return result


def duo_trio_demands(seats: dict[str, Any], adjacent_pairs: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for left_group, right_group, label in DUO_TRIO_FORMS:
        left_seats = left_group.split("_")
        right_seats = right_group.split("_")
        left_ranges = unique([
            term
            for seat in left_seats
            for term in ((seats.get(seat) or {}).get("explicit_range_names") or [])
        ])
        right_ranges = unique([
            term
            for seat in right_seats
            for term in ((seats.get(seat) or {}).get("explicit_range_names") or [])
        ])
        result[label] = {
            "status": "DUO_TRIO_ANSWER_READY",
            "left_group": left_group,
            "right_group": right_group,
            "left_ranges": left_ranges,
            "right_ranges": right_ranges,
            "adjacent_pair_dependencies": [
                name
                for name, pair in adjacent_pairs.items()
                if pair.get("left_seat") in left_seats or pair.get("right_seat") in right_seats
            ],
            "question": {
                "front_duo_to_back_trio": "Which S1-S2 duo correctly attaches to S3-S5 to form the draw body?",
                "front_trio_to_back_duo": "Which S1-S3 engine correctly hands into the S4-S5 endpoint duo?",
                "front_anchor_to_exit_duo": "Which front anchor pair best matches the exit duo?",
                "span_anchor_to_middle_engine": "Which S1-S5 span allows the middle engine to exist lawfully?",
            }[label],
            "candidate_reduction_logic": {
                "group_fit_required": True,
                "reject_loud_group_if_other_side_cannot_complete": True,
                "front_back_agreement_required": label in {"front_duo_to_back_trio", "front_trio_to_back_duo"},
                "span_agreement_required": label == "span_anchor_to_middle_engine",
            },
            "law": "The Answer must judge group relationships, because correct single seats can still make the wrong body together.",
        }
    return result


def motion_answer(transference_packet: dict[str, Any], condition_packet: dict[str, Any]) -> dict[str, Any]:
    terms = compact_terms(transference_packet)
    lowered = " ".join(terms).lower()
    flags = {
        "rise": any(word in lowered for word in ("lift", "rise", "expansion", "upper recovery")),
        "fall": any(word in lowered for word in ("drop", "fall", "discharge", "lower")),
        "hold": any(word in lowered for word in ("hold", "stable", "locked", "stickiness")),
        "release": any(word in lowered for word in ("release", "burst", "separation")),
        "reset": any(word in lowered for word in ("reset", "volcanic")),
        "crisis": any(word in lowered for word in ("crisis", "extreme")),
    }
    construction = construction_profile(condition_packet)
    mana = transference_packet.get("incoming_motion_mana") or {}
    crystallization = transference_packet.get("motion_to_sorted_crystallization") or {}
    lane_permission = transference_packet.get("afterlife_lane_permission") or {}
    outgoing = transference_packet.get("outgoing_motion_power") or {}
    transference_status = str(transference_packet.get("status") or "")
    transference_ready = bool(transference_packet) and transference_status not in {
        "OUTGOING_MOTION_BRIDGE_NOT_INSTALLED",
        "TRANSFERENCE_REMOVED_FROM_ACTIVE_SPINE",
    }
    return {
        "status": "MOTION_ANSWER_READY" if transference_ready else "NO_ACTIVE_TRANSFERENCE_PACKET",
        "transference_status": transference_status,
        "active_motion_flags": [key for key, value in flags.items() if value],
        "incoming_motion_mana": {
            "delta": mana.get("delta"),
            "motion_budget": mana.get("motion_budget"),
            "fatigue_state": mana.get("fatigue_state"),
            "drift_class": mana.get("drift_class"),
            "primary_lanes": mana.get("primary_lanes"),
            "lane_load_tiers": mana.get("lane_load_tiers"),
            "stickiness_tiers": mana.get("stickiness_tiers"),
        },
        "motion_to_sorted_crystallization": {
            "status": crystallization.get("status"),
            "draw_lane_to_sorted_seat": crystallization.get("draw_lane_to_sorted_seat"),
            "sorted_seat_to_draw_lane": crystallization.get("sorted_seat_to_draw_lane"),
            "sorted_inherited_motion": crystallization.get("sorted_inherited_motion"),
            "warning": crystallization.get("motion_sorted_misread_warning"),
        },
        "lane_permission": lane_permission,
        "outgoing_motion_power": outgoing,
        "target_postures": unique(construction.get("target_postures") or []),
        "target_set_classes": unique(construction.get("target_set_classes") or []),
        "law": "Motion answer says how the next body must move away from the source; it prevents pretty sorted bodies from being motion-wrong.",
    }


def boundary_answer(
    *,
    condition_packet: dict[str, Any],
    gap_geometry_packet: dict[str, Any],
    empress_packet: dict[str, Any],
) -> dict[str, Any]:
    construction = construction_profile(condition_packet)
    surfaces = [
        str(surface.get("birth_path") or "")
        for surface in ((empress_packet.get("live_safe") or {}).get("authority_surfaces") or [])
        if surface.get("birth_path")
    ]
    return {
        "status": "ANSWER_BOUNDARY_READY",
        "target_set_classes": unique(construction.get("target_set_classes") or []),
        "target_postures": unique(construction.get("target_postures") or []),
        "preferred_gap_families": unique(construction.get("preferred_gap_families") or []),
        "preferred_set_styles": unique(construction.get("preferred_set_styles") or []),
        "geometry_allowed_gaps": unique([row.get("gap_family") for row in gap_geometry_packet.get("allowed_gap_families") or [] if isinstance(row, dict)]),
        "geometry_allowed_styles": unique([row.get("set_style") for row in gap_geometry_packet.get("allowed_set_styles") or [] if isinstance(row, dict)]),
        "empress_authority_surfaces": unique(surfaces),
        "law": "The boundary answer defines what can exist before any construction script tries to rank bodies.",
    }


def number_climate_answer(iiw_packet: dict[str, Any], condition_packet: dict[str, Any]) -> dict[str, Any]:
    climate = (iiw_packet.get("live_safe") or {}).get("number_climate") or {}
    summary = climate.get("number_climate_summary") or {}
    construction = construction_profile(condition_packet)
    return {
        "status": "NUMBER_CLIMATE_ANSWER_READY" if climate else "NO_NUMBER_CLIMATE",
        "current_birth_path": climate.get("current_birth_path"),
        "current_set_style": climate.get("current_set_style"),
        "birth_transition_number_climate_key": climate.get("birth_transition_number_climate_key"),
        "overall_temperature_counts": summary.get("overall_temperature_counts") or {},
        "recent_temperature_counts": summary.get("recent_temperature_counts") or {},
        "source_temperature_counts": summary.get("source_temperature_counts") or {},
        "source_hot_numbers": numbers(summary.get("source_hot_numbers") or []),
        "source_warm_numbers": numbers(summary.get("source_warm_numbers") or []),
        "source_cold_numbers": numbers(summary.get("source_cold_numbers") or []),
        "hot_return_candidates": numbers(summary.get("hot_return_candidates") or []),
        "dormant_cold_return_candidates": numbers(summary.get("dormant_cold_return_candidates") or []),
        "source_number_climate": [
            {
                "number": parse_int(row.get("number")),
                "zone": row.get("zone"),
                "overall_temperature": row.get("overall_temperature"),
                "recent_temperature": row.get("recent_temperature"),
                "life_role": row.get("life_role"),
                "climate_pressure": row.get("climate_pressure"),
                "source_sorted_seat": row.get("source_sorted_seat"),
                "source_draw_lane": row.get("source_draw_lane"),
            }
            for row in climate.get("source_numbers") or []
            if isinstance(row, dict)
        ],
        "climate_gates": construction.get("climate_gates") or {},
        "law": "Number climate tells the Answer which numbers are hot, warm, cold, returning, exhausted, or climate-supported before construction.",
    }


def committed_question_answer(
    *,
    active_question: dict[str, Any],
    source: dict[str, Any],
    micro_ranges: dict[str, Any],
    seats: dict[str, Any],
    motion: dict[str, Any],
    support: dict[str, Any],
    body_shape: dict[str, Any],
    relation: dict[str, Any],
    contradiction_packet: dict[str, Any],
    answer_requirements: dict[str, Any],
) -> dict[str, Any]:
    source_body = source.get("sorted_body") or []
    inherited_motion = (motion.get("motion_to_sorted_crystallization") or {}).get("sorted_inherited_motion") or {}
    affinity_numbers = support.get("affinity_role_numbers_by_seat") or {}
    upstream_committed_terms = {
        seat: str((seats.get(seat) or {}).get("committed_range_name") or "")
        for seat in SEATS
    }
    burden = body_shape.get("burden") or {}
    fp_delta_required = parse_int(burden.get("fp_delta_required"))
    active_contradiction_keys = set(contradiction_packet.get("active_glossary_keys") or [])
    normalized_question_id = str(active_question.get("question_id") or "").replace("PREDRAW_", "")
    upstream_commit_weight = float(
        answer_requirements.get("upstream_commit_weight")
        if answer_requirements.get("upstream_commit_weight") is not None
        else CONTRADICTION_ANSWER_MAP.upstream_commit_weight(normalized_question_id, contradiction_packet)
    )
    lane_commit_weights = answer_requirements.get("lane_upstream_commit_weight") or {}
    answer_subtype = answer_requirements.get("answer_subtype_profile") or {}
    committed_by_seat: dict[str, Any] = {}
    committed_numbers: set[int] = set()
    support_numbers: set[int] = set()
    context_numbers: set[int] = set()
    unresolved: list[str] = []

    for index, seat in enumerate(SEATS):
        seat_answer = seats.get(seat) or {}
        micro_seat = (micro_ranges.get("by_seat") or {}).get(seat) or {}
        available_definitions = micro_seat.get("available_lane_ranges") or {}
        forced_range_names = unique((answer_subtype.get("forced_range_names_by_seat") or {}).get(seat) or [])
        definitions = {
            **available_definitions,
            **(micro_seat.get("called_for_range_definitions") or {}),
        }
        surgical_names = set(seat_answer.get("surgical_range_names") or [])
        explicit_names = unique((seat_answer.get("explicit_range_names") or []) + forced_range_names)
        role_numbers = set(affinity_numbers.get(seat) or [])
        source_value = parse_int(source_body[index] if index < len(source_body) else 0)
        motion_delta = parse_int(inherited_motion.get(seat))
        expected_value = source_value + motion_delta if source_value else 0
        fp_expected_value = source_value + fp_delta_required if seat == "S2" and source_value and fp_delta_required else 0

        scored: list[dict[str, Any]] = []
        for name in explicit_names:
            definition = definitions.get(name) or {}
            range_numbers = set(numbers_from_range_definitions({name: definition}))
            if not range_numbers:
                continue
            score = 0.0
            reasons: list[str] = []
            if upstream_committed_terms.get(seat) == name:
                lane_weight = float(
                    lane_commit_weights.get(seat)
                    if lane_commit_weights.get(seat) is not None
                    else CONTRADICTION_ANSWER_MAP.lane_upstream_commit_weight(
                        normalized_question_id,
                        contradiction_packet,
                        seat,
                        answer_subtype,
                    )
                )
                score += lane_weight
                reasons.append("UPSTREAM_COMMITTED_ANSWER")
            if name in forced_range_names:
                score += 26.0
                reasons.append("ANSWER_SUBTYPE_AUTHORIZED_RANGE")
            if name in surgical_names:
                score += 24.0
                reasons.append("SURGICAL_QUESTION_LANGUAGE")
            else:
                score += 10.0
                reasons.append("EXPLICIT_SUPPORT_LANGUAGE")
            if role_numbers & range_numbers:
                score += min(18.0, len(role_numbers & range_numbers) * 3.0)
                reasons.append("AFFINITY_ROLE_SUPPORT")
            if expected_value:
                midpoint = range_midpoint(definition)
                distance = abs(midpoint - expected_value)
                score += max(0.0, 38.0 - (distance * 2.0))
                reasons.append("MOTION_PROXIMITY")
            if fp_expected_value and fp_expected_value in range_numbers:
                score += 70.0
                reasons.append("FP_DELTA_COMMITTED_PROXIMITY")
            if source_value in range_numbers and CONTRADICTION_ANSWER_MAP.source_continuity_allowed(
                normalized_question_id,
                contradiction_packet,
                seat,
                answer_subtype,
            ):
                score += 34.0
                reasons.append("SOURCE_CONTINUITY")
            elif source_value in range_numbers:
                reasons.append("SOURCE_CONTINUITY_CONTEXT_ONLY")
            contradiction_score, contradiction_reasons = canonical_contradiction_score(
                seat=seat,
                range_name=name,
                definition=definition,
                range_numbers=range_numbers,
                source_value=source_value,
                source_body=source_body,
                seat_answer=seat_answer,
                contradiction_packet=contradiction_packet,
                question_id=str(active_question.get("question_id") or "").replace("PREDRAW_", ""),
                answer_subtype_profile=answer_subtype,
            )
            score += contradiction_score
            reasons.extend(contradiction_reasons)
            scored.append(
                {
                    "range_name": name,
                    "definition": definition,
                    "numbers": sorted(range_numbers),
                    "score": round(score, 3),
                    "reasons": reasons,
                }
            )

        scored = sorted(scored, key=lambda row: (-row["score"], range_midpoint(row["definition"]), row["range_name"]))
        committed = scored[0] if scored else {}
        if not committed:
            unresolved.append(seat)
        committed_set = set(committed.get("numbers") or [])
        seat_support_numbers = set()
        seat_context_numbers = set()
        for row in scored[1:]:
            row_numbers = set(row.get("numbers") or [])
            if "SURGICAL_QUESTION_LANGUAGE" in (row.get("reasons") or []):
                seat_support_numbers.update(row_numbers)
            else:
                seat_context_numbers.update(row_numbers)
        committed_numbers.update(committed_set)
        support_numbers.update(seat_support_numbers - committed_set)
        context_numbers.update(seat_context_numbers - committed_set - seat_support_numbers)
        committed_by_seat[seat] = {
            "status": "COMMITTED_SEAT_READY" if committed else "NO_COMMITTED_SEAT",
            "committed_range_name": committed.get("range_name"),
            "committed_range_definition": committed.get("definition") or {},
            "committed_numbers": committed.get("numbers") or [],
            "source_number": source_value,
            "inherited_motion_delta": motion_delta,
            "motion_expected_value": expected_value,
            "selection_score": committed.get("score"),
            "selection_reasons": committed.get("reasons") or [],
            "support_range_names": [
                row.get("range_name")
                for row in scored[1:]
                if "SURGICAL_QUESTION_LANGUAGE" in (row.get("reasons") or [])
            ],
            "context_range_names": [
                row.get("range_name")
                for row in scored[1:]
                if "SURGICAL_QUESTION_LANGUAGE" not in (row.get("reasons") or [])
            ],
            "candidate_range_scores": scored,
        }

    return {
        "schema": "serenity.life_link.committed_question_answer.v1",
        "status": "COMMITTED_QUESTION_ANSWER_READY" if len(unresolved) < len(SEATS) else "NO_COMMITTED_QUESTION_ANSWER",
        "mode": "ONE_COMMITTED_ANSWER_NO_EQUAL_SUPPORT_CLOUD",
        "canonical_contradiction_packet": contradiction_packet,
        "answer_requirement_packet": answer_requirements,
        "answer_subtype_profile": answer_subtype,
        "active_contradiction_keys": sorted(active_contradiction_keys),
        "upstream_commit_weight": upstream_commit_weight,
        "committed_by_seat": committed_by_seat,
        "committed_number_field": sorted(committed_numbers),
        "committed_number_count": len(committed_numbers),
        "support_number_field": sorted(support_numbers),
        "support_number_count": len(support_numbers),
        "context_number_field": sorted(context_numbers),
        "context_number_count": len(context_numbers),
        "unresolved_seats": unresolved,
        "body_commitment": {
            "target_set_classes": body_shape.get("target_set_classes") or [],
            "target_postures": body_shape.get("target_postures") or [],
            "relation_source": relation.get("source_relation") or {},
        },
        "downstream_law": (
            "Downstream should treat committed_number_field as the Answer field. Support/context may explain or score, "
            "but they must not carry equal authority unless a later script explicitly proves the committed answer wrong."
        ),
        "failure_law": (
            "If the committed answer misses, the miss belongs upstream. Do not hide uncertainty by expanding all support "
            "ranges into equal candidate authority."
        ),
    }


def contradiction_answer(
    *,
    condition_packet: dict[str, Any],
    situation_counter_branch_guard: dict[str, Any],
) -> dict[str, Any]:
    construction = construction_profile(condition_packet)
    relation = relation_demand(condition_packet)
    canonical_packet = canonical_contradiction_packet(condition_packet)
    requirements = answer_requirement_packet(condition_packet)
    branch = situation_counter_branch_guard.get("branch_test_formula") or {}
    guard = situation_counter_branch_guard.get("over_selection_guard_formula") or {}
    active_tests = unique(branch.get("required_branch_tests") or [])
    active_guards = unique(guard.get("active_guards") or [])
    false_answer_risks: list[str] = []
    if "mid_high_default_bias" in active_guards:
        false_answer_risks.append("MID_HIGH_LOUD_CLONE")
    if "burst_separation_over_selection" in active_guards:
        false_answer_risks.append("BURST_SEPARATION_OVERANSWER")
    if "FINAL_POCKET_PRESERVATION" in active_tests:
        false_answer_risks.append("FINAL_POCKET_BODY_CAN_BE_LOST_BY_LOUD_LEGAL_SIBLINGS")
    if construction.get("target_postures") and len(construction.get("target_postures") or []) > 2:
        false_answer_risks.append("MULTI_POSTURE_CONFUSION")
    return {
        "status": "CONTRADICTION_ANSWER_READY",
        "family_id": situation_counter_branch_guard.get("family_id"),
        "canonical_status": canonical_packet.get("status"),
        "active_glossary_keys": canonical_packet.get("active_glossary_keys") or [],
        "possible_glossary_family_count": canonical_packet.get("possible_glossary_family_count"),
        "answer_requirement_packet": requirements,
        "must_carry": canonical_packet.get("must_carry") or [],
        "support_signals": canonical_packet.get("support_signals") or [],
        "required_branch_tests": active_tests,
        "active_guards": active_guards,
        "blockers": unique((stage20_contract(condition_packet).get("blockers") or []) + (canonical_packet.get("blockers") or [])),
        "relation_counter_candidates": relation.get("relation_counter_candidates") or {},
        "false_answer_risks": unique(false_answer_risks + (canonical_packet.get("false_clone_patterns") or [])),
        "law": (
            "The contradiction answer is now canonical: Condition/Question publishes Atlas/Glossary families, "
            "and Voice uses them to choose committed ranges before downstream arbitration."
        ),
    }


def support_answer(
    *,
    equinox_packet: dict[str, Any],
    convergence_packet: dict[str, Any],
    affinity_packet: dict[str, Any],
) -> dict[str, Any]:
    revised = equinox_packet.get("revised_equinox_framework") or {}
    role_numbers = {}
    for seat, payload in (affinity_packet.get("seat_roles") or {}).items():
        if isinstance(payload, dict):
            role_numbers[seat] = numbers([row.get("number") for row in payload.get("role_fit_numbers") or [] if isinstance(row, dict)])[:20]
    return {
        "status": "SUPPORT_ANSWER_READY",
        "equinox_budget": (revised.get("budget") or {}),
        "equinox_lane_saturation": (revised.get("lane_saturation") or {}),
        "convergence_required_burden": convergence_packet.get("required_burden") or {},
        "affinity_role_numbers_by_seat": role_numbers,
        "law": "Support answer records why a number or relation is supported, not merely allowed.",
    }


def reduction_answer(
    *,
    seats: dict[str, Any],
    pairs: dict[str, Any],
    duos: dict[str, Any],
    condition_packet: dict[str, Any],
) -> dict[str, Any]:
    construction = construction_profile(condition_packet)
    explicit_seat_counts = {
        seat: len((payload or {}).get("explicit_numbers") or [])
        for seat, payload in seats.items()
    }
    return {
        "status": "ANSWER_REDUCTION_READY",
        "reduction_order": [
            "room_answer",
            "body_shape_answer",
            "relation_answer",
            "micro_range_answer",
            "seat_answer",
            "pair_answer",
            "duo_trio_answer",
            "motion_answer",
            "number_climate_answer",
            "contradiction_answer",
        ],
        "explicit_seat_number_counts": explicit_seat_counts,
        "pair_gate_count": len(pairs),
        "duo_trio_gate_count": len(duos),
        "candidate_bloat_controls": construction.get("candidate_bloat_controls") or {},
        "field_warning": (
            "If a technical answer still allows millions of bodies, a downstream script is ignoring pair/duo/relation gates "
            "or treating broad allowed language as required language."
        ),
        "law": "The Answer is supposed to reduce by meaning: room -> body -> relation -> seats -> pairs -> duos -> motion -> climate -> contradiction.",
    }


def build_voice_of_hope_answer(
    *,
    iiw_packet: dict[str, Any],
    condition_packet: dict[str, Any],
    transference_packet: dict[str, Any],
    equinox_packet: dict[str, Any],
    gap_geometry_packet: dict[str, Any],
    convergence_packet: dict[str, Any],
    affinity_packet: dict[str, Any],
    empress_packet: dict[str, Any],
    situation_counter_branch_guard: dict[str, Any],
) -> dict[str, Any]:
    seats = seat_answer_demands(condition_packet=condition_packet, affinity_packet=affinity_packet)
    pairs = adjacent_pair_demands(seats, condition_packet)
    duos = duo_trio_demands(seats, pairs)
    active_question = condition_packet.get("active_question") or {}
    source = source_answer(iiw_packet, transference_packet)
    precise = precise_question_answer(
        condition_packet=condition_packet,
        transference_packet=transference_packet,
        source=source,
    )
    body_shape = body_shape_answer(condition_packet, gap_geometry_packet, convergence_packet)
    relation = relation_answer(condition_packet)
    micro_ranges = micro_range_answer(condition_packet, seats)
    room = boundary_answer(
        condition_packet=condition_packet,
        gap_geometry_packet=gap_geometry_packet,
        empress_packet=empress_packet,
    )
    motion = motion_answer(transference_packet, condition_packet)
    climate = number_climate_answer(iiw_packet, condition_packet)
    support = support_answer(
        equinox_packet=equinox_packet,
        convergence_packet=convergence_packet,
        affinity_packet=affinity_packet,
    )
    answer_requirements = answer_requirement_packet(
        condition_packet,
        source.get("sorted_body") or [],
        {
            "condition_packet": condition_packet,
            "transference_packet": transference_packet,
            "source_answer": source,
        },
    )
    committed = committed_question_answer(
        active_question=active_question,
        source=source,
        micro_ranges=micro_ranges,
        seats=seats,
        motion=motion,
        support=support,
        body_shape=body_shape,
        relation=relation,
        contradiction_packet=canonical_contradiction_packet(condition_packet),
        answer_requirements=answer_requirements,
    )
    contradiction = contradiction_answer(
        condition_packet=condition_packet,
        situation_counter_branch_guard=situation_counter_branch_guard,
    )
    answer = {
        "schema": "serenity.life_link.voice_of_hope_answer.v1",
        "created_at": utc_now(),
        "status": "VOICE_OF_HOPE_READY",
        "diagnostic_only": False,
        "may_influence_later_stages": True,
        "name": "Voice Of Hope",
        "answer_identity": {
            "question_id": active_question.get("question_id"),
            "question_label": active_question.get("question_label"),
            "draw_singularity": (
                ((transference_packet.get("outgoing_motion_discovery") or {}).get("draw_singularity") or {})
                .get("proposed_draw_singularity")
            ),
            "recommended_container": active_question.get("recommended_container"),
            "recommended_family": active_question.get("recommended_family"),
            "source_as_of": (iiw_packet.get("source") or {}).get("as_of") or iiw_packet.get("as_of"),
        },
        "source_answer": source,
        "precise_question_answer": precise,
        "room_answer": room,
        "body_shape_answer": body_shape,
        "relation_answer": relation,
        "micro_range_answer": micro_ranges,
        "committed_answer": committed,
        "seat_answer": seats,
        "pair_answer": pairs,
        "duo_trio_answer": duos,
        "motion_answer": motion,
        "number_climate_answer": climate,
        "support_answer": support,
        "answer_requirement_map": answer_requirements,
        "contradiction_answer": contradiction,
        "reduction_answer": reduction_answer(
            seats=seats,
            pairs=pairs,
            duos=duos,
            condition_packet=condition_packet,
        ),
        "answer_field_policy": {
            "body_generation": "NOT_OWNED_BY_VOICE_OF_HOPE",
            "candidate_count_expectation": "COMMITTED_ANSWER_FIELD_FIRST_THEN_SUPPORT_CONTEXT",
            "downstream_instruction": (
                "Later scripts should consume committed_answer.committed_number_field as the first-class answer field. "
                "Support and context may explain, but they do not carry equal authority. New Garden should consume "
                "precise_question_answer.new_garden_contract when it is rebuilt for D-lane caste-side answers."
            ),
        },
        "law": (
            "Voice Of Hope receives the question and manifests the Answer: room, seats, pairs, duos, motion, "
            "support, contradiction, and boundaries. It does not crown the final five numbers."
        ),
    }
    answer["packet_id"] = packet_id("voice-of-hope", answer)
    return answer
