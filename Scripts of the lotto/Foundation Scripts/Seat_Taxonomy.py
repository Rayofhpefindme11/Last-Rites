from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from Infinite_Inner_World import (
    DEFAULT_CSV_PATH,
    TRUSTED_DRAW_ORDER_START_DATE,
    DrawMotion,
    DrawSetPacket,
    LaneForm,
    SetRelation,
    build_draw_set_packet,
    format_delta,
    load_historical_draws,
    motion_gauge as iiw_motion_gauge,
    parse_draw_date,
    selected_draw_indexes,
)


SCHEMA = "iiw.seat_taxonomy.transition_physics.v1"
NORSE_BURDEN_GAUGE: tuple[str, ...] = (
    "Odin",
    "Frigg",
    "Thor",
    "Sif",
    "Baldr",
    "Nanna",
    "Hodr",
    "Hermod",
    "Tyr",
    "Bragi",
    "Idun",
    "Heimdall",
    "Loki",
    "Sigyn",
    "Hel",
    "Fenrir",
    "Jormungandr",
    "Freyr",
    "Freyja",
    "Njord",
    "Skadi",
    "Ullr",
    "Forseti",
    "Vidar",
    "Vali",
    "Gefjon",
    "Eir",
    "Saga",
    "Fulla",
    "Gna",
    "Var",
    "Vor",
    "Syn",
    "Hlin",
    "Snotra",
)
CHINESE_PRESSURE_GAUGE: tuple[str, ...] = (
    "Pangu",
    "Nuwa",
    "Fuxi",
    "Shennong",
    "Huangdi",
    "Xiwangmu",
    "Dongwanggong",
    "Yuhuang",
    "Guanyin",
    "Mazu",
    "Chang'e",
    "Houyi",
    "Erlang Shen",
    "Nezha",
    "Lei Gong",
    "Dian Mu",
    "Feng Bo",
    "Yu Shi",
    "Zhurong",
    "Gonggong",
    "Houtu",
    "Wenchang",
    "Caishen",
    "Zao Jun",
    "Tudi Gong",
    "Chenghuang",
    "Long Wang",
    "Yanluo Wang",
    "Zhong Kui",
    "Lu Dongbin",
    "He Xiangu",
    "Li Tieguai",
    "Lan Caihe",
    "Han Xiangzi",
    "Zhang Guolao",
)
PRESSURE_WORLD_TYPES: tuple[str, ...] = (
    "STRUCTURAL_DOMINANT",
    "DYNAMIC_DOMINANT",
    "STRUCTURAL_DYNAMIC_BALANCED",
)
PRESSURE_WORLD_CENTERS: tuple[str, ...] = (
    "CORE",
    "MIDDLE",
    "ENDPOINT",
)
PRESSURE_WORLD_BALANCES: tuple[str, ...] = (
    "LEFT_HEAVY",
    "CENTER_HEAVY",
    "RIGHT_HEAVY",
    "EDGE_HEAVY",
)
PRESSURE_WORLD_DISTRIBUTIONS: tuple[str, ...] = (
    "FOCUSED",
    "SPLIT",
    "SPREAD",
)
PRESSURE_TOPOLOGY_NAMES: tuple[str, ...] = (
    "Altera",
    "Nova",
    "Nyx",
    "Citrine",
    "Lumina",
    "Nirvana",
    "Alcides",
    "Artoria",
    "Nero",
    "Rama",
    "Suzuka",
    "Tomoe Gozen",
    "Karna",
    "Medusa",
    "Kurohime",
    "Irisviel",
    "Circe",
    "Scathach",
    "Anastasia",
    "Izumo",
    "Hanasaka",
    "Stheno",
    "Sasaki",
    "Carmilla",
    "Semiramis",
    "Consort Yu",
    "Kashin",
)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESOLUTION_BRANCH_FINDINGS_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "resolution_bias_branch_findings_2015-10-07.json"
)
_RESOLUTION_BRANCH_FINDINGS_CACHE: dict[str, dict[str, Any]] | None = None


@dataclass(frozen=True)
class SeatTaxonomyPacket:
    packet: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return self.packet


def sign_marker(value: int | None) -> str:
    if value is None:
        return "N"
    if value > 0:
        return "+"
    if value < 0:
        return "-"
    return "0"


def sign_pattern(values: list[int | None]) -> str:
    return "".join(sign_marker(value) for value in values)


def lane_by_name(lanes: tuple[LaneForm, ...]) -> dict[str, LaneForm]:
    return {lane.lane: lane for lane in lanes}


def relation_by_pair(relations: tuple[SetRelation, ...]) -> dict[tuple[str, str], SetRelation]:
    return {(relation.from_lane, relation.to_lane): relation for relation in relations}


def sorted_lane_for_draw_lane(packet: DrawSetPacket) -> dict[str, str]:
    return {
        step.draw_lane: step.sorted_lane
        for step in packet.draw_style.steps
    }


def seat_zone(sorted_lane: str) -> str:
    if sorted_lane == "S1":
        return "CORE"
    if sorted_lane in {"S2", "S3", "S4"}:
        return "MIDDLE"
    if sorted_lane == "S5":
        return "ENDPOINT"
    return "UNKNOWN"


def motion_direction(value: int | None) -> str:
    marker = sign_marker(value)
    if marker == "+":
        return "LIFT"
    if marker == "-":
        return "DROP"
    if marker == "0":
        return "HOLD"
    return "UNKNOWN"


def label_token(value: str | None) -> str:
    if value is None:
        return "UNKNOWN"
    return value.upper().replace(" ", "_").replace("-", "_")


def address_token(value: Any) -> str:
    text = str(value).upper()
    chars = [char if char.isalnum() else "_" for char in text]
    token = "".join(chars).strip("_")
    while "__" in token:
        token = token.replace("__", "_")
    return token or "UNKNOWN"


def sign_address_token(value: Any) -> str:
    text = str(value)
    return "".join(
        {
            "+": "P",
            "-": "M",
            "0": "Z",
            "N": "N",
        }.get(char, address_token(char))
        for char in text
    ) or "UNKNOWN"


def load_resolution_branch_findings() -> dict[str, dict[str, Any]]:
    global _RESOLUTION_BRANCH_FINDINGS_CACHE
    if _RESOLUTION_BRANCH_FINDINGS_CACHE is not None:
        return _RESOLUTION_BRANCH_FINDINGS_CACHE
    if not RESOLUTION_BRANCH_FINDINGS_PATH.exists():
        _RESOLUTION_BRANCH_FINDINGS_CACHE = {}
        return _RESOLUTION_BRANCH_FINDINGS_CACHE
    payload = json.loads(RESOLUTION_BRANCH_FINDINGS_PATH.read_text(encoding="utf-8-sig"))
    findings: dict[str, dict[str, Any]] = {}
    for finding in payload.get("findings", []):
        law_key = finding.get("law_key")
        if law_key:
            findings[law_key] = finding
    _RESOLUTION_BRANCH_FINDINGS_CACHE = findings
    return _RESOLUTION_BRANCH_FINDINGS_CACHE


def two_number_gauge(value: int | None, labels: tuple[str, ...]) -> tuple[str | None, str | None]:
    if value is None:
        return None, None
    if value < 1:
        return "Zero", "0"
    class_index = ((value - 1) // 2) % len(labels)
    cycle_start = ((value - 1) // (2 * len(labels))) * (2 * len(labels))
    range_start = cycle_start + (class_index * 2) + 1
    return labels[class_index], f"{range_start}-{range_start + 1}"


def burden_gauge(value: int | None) -> tuple[str | None, str | None]:
    return two_number_gauge(value, NORSE_BURDEN_GAUGE)


def pressure_gauge(value: int | None) -> tuple[str | None, str | None]:
    return two_number_gauge(value, CHINESE_PRESSURE_GAUGE)


def total_abs_motion(motions: tuple[DrawMotion, ...], attr: str) -> int | None:
    values = [getattr(motion, attr) for motion in motions]
    if any(value is None for value in values):
        return None
    return sum(abs(int(value)) for value in values)


def dominant_motion_lane(motions: tuple[DrawMotion, ...], attr: str) -> DrawMotion | None:
    available = [motion for motion in motions if getattr(motion, attr) is not None]
    if not available:
        return None
    return max(available, key=lambda motion: abs(int(getattr(motion, attr))))


def motion_lane_rows(packet: DrawSetPacket, attr_prefix: str) -> list[dict[str, Any]]:
    draw_to_sorted = sorted_lane_for_draw_lane(packet)
    rows: list[dict[str, Any]] = []
    for motion in packet.draw_motion:
        value = getattr(motion, f"{attr_prefix}_motion")
        rows.append(
            {
                "lane": motion.lane,
                "role": motion.role,
                "sorted_seat": draw_to_sorted[motion.lane],
                "seat_zone": seat_zone(draw_to_sorted[motion.lane]),
                "motion": value,
                "sign": sign_marker(value),
                "broad_class": getattr(motion, f"{attr_prefix}_motion_class"),
                "gauge": getattr(motion, f"{attr_prefix}_motion_gauge"),
                "gauge_range": getattr(motion, f"{attr_prefix}_motion_gauge_range"),
            }
        )
    return rows


def build_seat_rows(packet: DrawSetPacket) -> list[dict[str, Any]]:
    relations = relation_by_pair(packet.sorted_relations)
    rows: list[dict[str, Any]] = []
    for lane in packet.sorted_form:
        left_relation = None
        right_relation = None
        if lane.lane != "S1":
            previous_lane = f"S{int(lane.lane[1:]) - 1}"
            relation = relations[(previous_lane, lane.lane)]
            left_relation = {
                "relation": relation.relation,
                "gap": relation.gap,
                "class": relation.relation_class,
                "range": relation.relation_class_range,
            }
        if lane.lane != "S5":
            next_lane = f"S{int(lane.lane[1:]) + 1}"
            relation = relations[(lane.lane, next_lane)]
            right_relation = {
                "relation": relation.relation,
                "gap": relation.gap,
                "class": relation.relation_class,
                "range": relation.relation_class_range,
            }
        rows.append(
            {
                "seat": lane.lane,
                "role": lane.role,
                "number": lane.number,
                "taxonomy": lane.number_band,
                "zone": seat_zone(lane.lane),
                "left_relation": left_relation,
                "right_relation": right_relation,
            }
        )
    return rows


def draw_order_numbers(draw: Any | None) -> list[int] | None:
    if draw is None:
        return None
    return list(draw.white_balls)


def draw_order_delta(left: Any | None, right: Any | None) -> list[int | None]:
    if left is None or right is None:
        return [None, None, None, None, None]
    return [
        right.white_balls[index] - left.white_balls[index]
        for index in range(len(right.white_balls))
    ]


def sorted_order_delta(left: Any | None, right: Any | None) -> list[int | None]:
    if left is None or right is None:
        return [None, None, None, None, None]
    return [
        right.sorted_white_balls[index] - left.sorted_white_balls[index]
        for index in range(len(right.sorted_white_balls))
    ]


def draw_motion_family(
    sign_text: str,
    energy_class: str | None,
    dominant_lane: str | None,
) -> str:
    if "N" in sign_text:
        base = "BOUNDARY_UNKNOWN"
    elif set(sign_text) == {"+"}:
        base = "FULL_LIFT"
    elif set(sign_text) == {"-"}:
        base = "FULL_DROP"
    elif sign_text.count("+") >= 4:
        base = "LIFT_DOMINANT"
    elif sign_text.count("-") >= 4:
        base = "DROP_DOMINANT"
    elif sign_text in {"+-+-+", "-+-+-"}:
        base = "ALTERNATING_COUNTER"
    else:
        base = "HYBRID_COUNTER"
    return f"{base}_{label_token(energy_class)}_{dominant_lane or 'NO_DOMINANT'}"


def max_abs_draw_step(packet: DrawSetPacket) -> dict[str, Any] | None:
    if not packet.draw_step_motion:
        return None
    step = max(packet.draw_step_motion, key=lambda item: abs(item.distance))
    return {
        "from_lane": step.from_lane,
        "from_role": step.from_role,
        "lane": step.lane,
        "role": step.role,
        "from_number": step.from_number,
        "to_number": step.to_number,
        "distance": step.distance,
        "abs_distance": abs(step.distance),
    }


def draw_order_face_identity(packet: DrawSetPacket) -> dict[str, Any]:
    max_step = max_abs_draw_step(packet)
    return {
        "order_pattern": "-".join(str(lane.number) for lane in packet.draw_form),
        "draw_order_band_pattern": "-".join(lane.number_band for lane in packet.draw_form),
        "sorted_position_path": list(packet.draw_style.sorted_position_path),
        "transfer_pattern": packet.draw_style.transfer_pattern,
        "direction_pattern": packet.draw_style.direction_pattern,
        "turn_count": packet.draw_style.turn_count,
        "turn_lanes": list(packet.draw_style.turn_lanes),
        "max_abs_lane": max_step,
        "face_family": packet.draw_style.draw_style_family,
        "draw_style": packet.draw_style.draw_style,
    }


def lane_caste_side(value: int | None) -> str:
    if value is None:
        return "UNKNOWN"
    magnitude = abs(int(value))
    if magnitude == 0:
        return "ZERO"
    low = ((magnitude - 1) // 2) * 2 + 1
    return "LOW" if magnitude == low else "HIGH"


def lane_caste_signature(
    values: list[int | None],
    prefix: str,
) -> dict[str, Any]:
    lanes: dict[str, Any] = {}
    for index, value in enumerate(values, start=1):
        lane = f"{prefix}{index}"
        gauge, gauge_range = iiw_motion_gauge(value)
        marker = sign_marker(value)
        signed_caste = f"{marker}{address_token(gauge)}"
        signed_side = f"{signed_caste}:{lane_caste_side(value)}"
        lanes[lane] = {
            "lane": lane,
            "delta": value,
            "sign": marker,
            "direction": motion_direction(value),
            "abs_delta": None if value is None else abs(int(value)),
            "caste": gauge,
            "caste_range": gauge_range,
            "caste_side": lane_caste_side(value),
            "signed_caste": signed_caste,
            "signed_caste_side": signed_side,
        }
    ordered = [lanes[f"{prefix}{index}"] for index in range(1, len(values) + 1)]
    return {
        "sign_pattern": sign_pattern(values),
        "caste_pattern": "|".join(row["signed_caste"] for row in ordered),
        "caste_side_pattern": "|".join(row["signed_caste_side"] for row in ordered),
        "lanes": lanes,
    }


def compact_motion_family(delta: list[int | None], prefix: str) -> str:
    sign_text = sign_pattern(delta)
    if "N" in sign_text:
        base = "BOUNDARY_UNKNOWN"
    elif set(sign_text) == {"0"}:
        base = "STILL_FIELD"
    elif set(sign_text) == {"+"}:
        base = "FULL_LIFT"
    elif set(sign_text) == {"-"}:
        base = "FULL_DROP"
    elif sign_text.count("+") >= 4:
        base = "LIFT_DOMINANT"
    elif sign_text.count("-") >= 4:
        base = "DROP_DOMINANT"
    elif sign_text in {"+-+-+", "-+-+-"}:
        base = "ALTERNATING_COUNTER"
    else:
        base = "HYBRID_COUNTER"
    dominant_index = None
    dominant_value = None
    for index, value in enumerate(delta, start=1):
        if value is None:
            continue
        if dominant_value is None or abs(value) > abs(dominant_value):
            dominant_index = index
            dominant_value = int(value)
    gauge, _range = iiw_motion_gauge(dominant_value)
    return f"{base}_{address_token(gauge)}_{prefix}{dominant_index or 'X'}"


def ds_branch_family(preference_universe: str) -> str:
    if preference_universe == "EDGE_BINARY":
        return "EDGE_BRANCH_SINGULARITY"
    if preference_universe == "HINGE_BINARY":
        return "HINGE_BRANCH_SINGULARITY"
    if preference_universe == "CENTER_MIXED":
        return "CENTER_MIXED_SINGULARITY"
    if preference_universe == "MIXED_FAMILY_FIELD":
        return "MIXED_BRANCH_SINGULARITY"
    return "UNMEASURED_BRANCH_SINGULARITY"


def build_draw_singularity_lens(
    packet: DrawSetPacket,
    draw_order_transition: dict[str, Any],
    pressure_map: dict[str, Any],
    pressure_authority: dict[str, Any],
    resolution_bias: dict[str, Any],
    collision_point: dict[str, Any],
    motion_state: dict[str, Any],
    motion_archetype: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> dict[str, Any]:
    incoming_sorted_delta = sorted_order_delta(packet.previous_draw, packet.draw)
    outgoing_sorted_delta = sorted_order_delta(packet.draw, packet.next_draw)
    incoming_draw_caste = lane_caste_signature(
        draw_order_transition["incoming_draw_delta"],
        "D",
    )
    outgoing_draw_caste = lane_caste_signature(
        draw_order_transition["outgoing_draw_delta"],
        "D",
    )
    incoming_sorted_caste = lane_caste_signature(incoming_sorted_delta, "S")
    outgoing_sorted_caste = lane_caste_signature(outgoing_sorted_delta, "S")
    preference = collision_point["pre_collision_preference_field"]
    world = pressure_map["pressure_world"]
    ds_family = ds_branch_family(preference["preference_universe"])
    subfamily = "::".join(
        [
            address_token(world["topology_name"]),
            address_token(world["base_world"]),
            address_token(pressure_map["pressure_center"]),
            address_token(pressure_map["pressure_balance"]),
            address_token(pressure_map["pressure_distribution"]),
            f"AUTH_{address_token(pressure_authority['authority_winner_seat'])}",
            address_token(pressure_authority["authority_winner_origin"]),
        ]
    )
    internal_profile = "::".join(
        [
            address_token(motion_state["motion_state"]),
            address_token(motion_archetype["motion_archetype"]),
            address_token(outgoing_contract["transfer"]),
            f"IN_{sign_address_token(draw_order_transition['incoming_draw_sign'])}",
            f"OUT_{sign_address_token(draw_order_transition['outgoing_draw_sign'])}",
            f"INLANE_{address_token(draw_order_transition['dominant_incoming_draw_lane'])}",
            f"OUTLANE_{address_token(outgoing_contract['dominant_lane'])}",
            f"BIAS_{address_token(resolution_bias['bias_type'])}",
            f"PREF_{address_token(preference['preference_universe'])}",
        ]
    )
    selector_profile = "::".join(
        [
            address_token(motion_state["motion_state"]),
            address_token(motion_archetype["motion_archetype"]),
            address_token(outgoing_contract["transfer"]),
            f"BIAS_{address_token(resolution_bias['bias_type'])}",
            f"PREF_{address_token(preference['preference_universe'])}",
        ]
    )
    profile_key = "||".join([ds_family, subfamily, internal_profile])
    return {
        "rule": (
            "Draw Singularity Lens names the active motion problem before branch "
            "selection; it is an IIW-native family/subfamily/internal-profile layer."
        ),
        "draw_singularity": ds_family,
        "subfamily": subfamily,
        "internal_profile": internal_profile,
        "selector_profile": selector_profile,
        "profile_key": profile_key,
        "branch_universe": preference["preference_universe"],
        "selection_problem": preference["selection_problem"],
        "incoming_draw_family_key": draw_order_transition["incoming_draw_family"],
        "outgoing_draw_family_key": draw_order_transition["outgoing_draw_family"],
        "incoming_sorted_family_key": compact_motion_family(incoming_sorted_delta, "S"),
        "outgoing_sorted_family_key": compact_motion_family(outgoing_sorted_delta, "S"),
        "incoming_draw_caste_pattern": incoming_draw_caste["caste_pattern"],
        "incoming_draw_caste_side_pattern": incoming_draw_caste["caste_side_pattern"],
        "outgoing_draw_caste_pattern": outgoing_draw_caste["caste_pattern"],
        "outgoing_draw_caste_side_pattern": outgoing_draw_caste["caste_side_pattern"],
        "incoming_sorted_caste_pattern": incoming_sorted_caste["caste_pattern"],
        "incoming_sorted_caste_side_pattern": incoming_sorted_caste["caste_side_pattern"],
        "outgoing_sorted_caste_pattern": outgoing_sorted_caste["caste_pattern"],
        "outgoing_sorted_caste_side_pattern": outgoing_sorted_caste["caste_side_pattern"],
        "source_micro_ranges": {
            row["seat"]: row["taxonomy"]
            for row in build_seat_rows(packet)
        },
        "authority_path": {
            "authority_seat": pressure_authority["authority_winner_seat"],
            "authority_origin": pressure_authority["authority_winner_origin"],
            "authority_draw_lane": pressure_authority["authority_winner_draw_lane"],
            "primary_bias_seat": resolution_bias["primary_bias_seat"],
            "secondary_bias_seat": resolution_bias["secondary_bias_seat"],
            "collision_seat": collision_point["collision_seat"],
            "observed_outgoing_seat": outgoing_contract["dominant_sorted_seat"],
        },
        "read": (
            "DS compresses the room between broad branch law and over-specific raw "
            "fields: family names the branch universe, subfamily names the pressure "
            "world and authority, internal profile names the motion condition."
        ),
    }


def draw_order_taxonomy_rows(packet: DrawSetPacket) -> list[dict[str, Any]]:
    draw_to_sorted = sorted_lane_for_draw_lane(packet)
    carry_rows = {
        row["lane"]: row
        for row in carry_reversal_rows(packet)
    }
    motion_by_lane = {motion.lane: motion for motion in packet.draw_motion}
    rows: list[dict[str, Any]] = []
    for lane in packet.draw_form:
        motion = motion_by_lane[lane.lane]
        rows.append(
            {
                "draw_lane": lane.lane,
                "draw_role": lane.role,
                "number": lane.number,
                "draw_order_band": lane.number_band,
                "mapped_sorted_seat": draw_to_sorted[lane.lane],
                "mapped_sorted_zone": seat_zone(draw_to_sorted[lane.lane]),
                "incoming_motion": motion.incoming_motion,
                "incoming_sign": sign_marker(motion.incoming_motion),
                "incoming_family": motion.incoming_motion_class,
                "incoming_gauge": motion.incoming_motion_gauge,
                "incoming_gauge_range": motion.incoming_motion_gauge_range,
                "outgoing_motion": motion.outgoing_motion,
                "outgoing_sign": sign_marker(motion.outgoing_motion),
                "outgoing_family": motion.outgoing_motion_class,
                "outgoing_gauge": motion.outgoing_motion_gauge,
                "outgoing_gauge_range": motion.outgoing_motion_gauge_range,
                "incoming_to_outgoing_transfer": carry_rows[lane.lane]["transfer"],
            }
        )
    return rows


def build_draw_order_transition(packet: DrawSetPacket) -> dict[str, Any]:
    incoming_delta = draw_order_delta(packet.previous_draw, packet.draw)
    outgoing_delta = draw_order_delta(packet.draw, packet.next_draw)
    incoming_dominant = dominant_motion_lane(packet.draw_motion, "incoming_motion")
    outgoing_dominant = dominant_motion_lane(packet.draw_motion, "outgoing_motion")
    incoming_sign = sign_pattern(incoming_delta)
    outgoing_sign = sign_pattern(outgoing_delta)
    draw_pressure = packet.set_pressure.draw_pressure
    return {
        "rule": "previous draw order -> current draw order -> outgoing contract -> next draw order -> sorted body result",
        "previous_draw_order": draw_order_numbers(packet.previous_draw),
        "current_draw_order": draw_order_numbers(packet.draw),
        "next_draw_order": draw_order_numbers(packet.next_draw),
        "incoming_draw_delta": incoming_delta,
        "outgoing_draw_delta": outgoing_delta,
        "incoming_draw_sign": incoming_sign,
        "outgoing_draw_sign": outgoing_sign,
        "incoming_draw_family": draw_motion_family(
            incoming_sign,
            draw_pressure.incoming_energy_class,
            incoming_dominant.lane if incoming_dominant else None,
        ),
        "outgoing_draw_family": draw_motion_family(
            outgoing_sign,
            draw_pressure.outgoing_energy_class,
            outgoing_dominant.lane if outgoing_dominant else None,
        ),
        "incoming_energy": draw_pressure.incoming_energy,
        "incoming_energy_class": draw_pressure.incoming_energy_class,
        "outgoing_energy": draw_pressure.outgoing_energy,
        "outgoing_energy_class": draw_pressure.outgoing_energy_class,
        "dominant_incoming_draw_lane": incoming_dominant.lane if incoming_dominant else None,
        "dominant_incoming_draw_motion": (
            incoming_dominant.incoming_motion if incoming_dominant else None
        ),
        "dominant_outgoing_draw_lane": outgoing_dominant.lane if outgoing_dominant else None,
        "dominant_outgoing_draw_motion": (
            outgoing_dominant.outgoing_motion if outgoing_dominant else None
        ),
    }


def carry_reversal_rows(packet: DrawSetPacket) -> list[dict[str, Any]]:
    draw_to_sorted = sorted_lane_for_draw_lane(packet)
    rows: list[dict[str, Any]] = []
    for motion in packet.draw_motion:
        incoming_sign = sign_marker(motion.incoming_motion)
        outgoing_sign = sign_marker(motion.outgoing_motion)
        if "N" in {incoming_sign, outgoing_sign}:
            transfer = "BOUNDARY_UNKNOWN"
        elif incoming_sign == "0" and outgoing_sign == "0":
            transfer = "STILL_HOLD"
        elif incoming_sign == outgoing_sign:
            transfer = "CARRY"
        elif "0" in {incoming_sign, outgoing_sign}:
            transfer = "HINGE"
        else:
            transfer = "REVERSAL"
        rows.append(
            {
                "lane": motion.lane,
                "role": motion.role,
                "sorted_seat": draw_to_sorted[motion.lane],
                "incoming_sign": incoming_sign,
                "outgoing_sign": outgoing_sign,
                "transfer": transfer,
            }
        )
    return rows


def carry_reversal_profile(rows: list[dict[str, Any]]) -> str:
    if any(row["transfer"] == "BOUNDARY_UNKNOWN" for row in rows):
        return "BOUNDARY_UNKNOWN"
    carry = sum(1 for row in rows if row["transfer"] == "CARRY")
    reversal = sum(1 for row in rows if row["transfer"] == "REVERSAL")
    hinge = sum(1 for row in rows if row["transfer"] == "HINGE")
    if reversal == 5:
        return "FULL_REVERSAL"
    if carry >= 4:
        return "CARRY_FORWARD"
    if reversal >= 3 and carry >= 1:
        return "HYBRID_COUNTER"
    if reversal >= 3:
        return "REVERSAL_PUSH"
    if carry >= 3:
        return "CARRY_PRESSURE"
    if hinge >= 2:
        return "HINGE_TRANSFER"
    return "MIXED_TRANSFER"


def burden_level(score: int) -> str:
    if score >= 90:
        return "EXTREME"
    if score >= 65:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def burden_state(
    sorted_lane: LaneForm,
    left_relation: dict[str, Any] | None,
    right_relation: dict[str, Any] | None,
    incoming_motion: int | None,
    packet: DrawSetPacket,
) -> str:
    left_gap = left_relation["gap"] if left_relation else None
    right_gap = right_relation["gap"] if right_relation else None
    direction = motion_direction(incoming_motion)
    anatomy = packet.set_anatomy

    if sorted_lane.lane in {"S2", "S3", "S4"}:
        if anatomy.middle_pressure == "MIDDLE_COMPRESSION_PRESSURE":
            if direction == "LIFT":
                return "HINGE_LOAD"
            return "COMPRESSED"
        if anatomy.middle_pressure == "MIDDLE_EXPANSION_PRESSURE":
            return "STRETCHED"
        if left_gap is not None and right_gap is not None and left_gap <= 10 and right_gap <= 10:
            return "TRAPPED"
        if left_gap is not None and right_gap is not None and max(left_gap, right_gap) >= 25:
            return "HINGE_LOAD"
        return "HOLD"

    if sorted_lane.lane == "S1":
        if anatomy.full_set_relation == "OUTER_EDGES_WIDER_THAN_MIDDLE":
            return "CORE_DRAG"
        if right_gap is not None and right_gap >= 25:
            return "CORE_STRETCHED"
        return "HOLD"

    if sorted_lane.lane == "S5":
        if left_gap is not None and left_gap <= 10 and abs(incoming_motion or 0) >= 25:
            return "ENDPOINT_SATURATED"
        if left_gap is not None and left_gap >= 25:
            return "TAIL_OPEN"
        return "HOLD"

    return "HOLD"


def origin_row(category: str, contribution: int, meaning: str) -> dict[str, Any]:
    return {
        "origin": category,
        "contribution": contribution,
        "meaning": meaning,
    }


STRUCTURAL_ORIGINS: frozenset[str] = frozenset(
    (
        "GAP_STRUCTURE",
        "MIDDLE_COMPRESSION",
        "EDGE_IMBALANCE",
        "HINGE_TRAP",
    )
)
DYNAMIC_ORIGINS: frozenset[str] = frozenset(
    (
        "INCOMING_MOTION",
        "TRANSFER_REVERSAL",
        "CARRY_FORWARD",
        "COUNTER_ROTATION",
    )
)


def aggregate_origins(origins: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for origin in origins:
        category = origin["origin"]
        if category not in grouped:
            grouped[category] = {
                "origin": category,
                "contribution": 0,
                "meaning": [],
            }
        grouped[category]["contribution"] += origin["contribution"]
        grouped[category]["meaning"].append(origin["meaning"])
    return [
        {
            "origin": category,
            "contribution": row["contribution"],
            "meaning": "; ".join(dict.fromkeys(row["meaning"])),
        }
        for category, row in grouped.items()
    ]


def pressure_type_split(origins: list[dict[str, Any]]) -> dict[str, Any]:
    structural = sum(
        origin["contribution"]
        for origin in origins
        if origin["origin"] in STRUCTURAL_ORIGINS
    )
    dynamic = sum(
        origin["contribution"]
        for origin in origins
        if origin["origin"] in DYNAMIC_ORIGINS
    )
    total = structural + dynamic
    if total == 0:
        dominant = "NONE"
    elif structural > dynamic:
        dominant = "STRUCTURAL"
    elif dynamic > structural:
        dominant = "DYNAMIC"
    else:
        dominant = "BALANCED"
    return {
        "structural_pressure": structural,
        "dynamic_pressure": dynamic,
        "total_pressure": total,
        "dominant_pressure_type": dominant,
        "structural_ratio": round(structural / total, 3) if total else 0,
        "dynamic_ratio": round(dynamic / total, 3) if total else 0,
        "structural_sources": [
            origin for origin in origins if origin["origin"] in STRUCTURAL_ORIGINS
        ],
        "dynamic_sources": [
            origin for origin in origins if origin["origin"] in DYNAMIC_ORIGINS
        ],
    }


def seat_origin_contributors(
    seat: dict[str, Any],
    incoming_value: int,
    packet: DrawSetPacket,
    transfer_by_seat: dict[str, str],
) -> list[dict[str, Any]]:
    left_gap = seat["left_relation"]["gap"] if seat["left_relation"] else 0
    right_gap = seat["right_relation"]["gap"] if seat["right_relation"] else 0
    adjacent_pressure = left_gap + right_gap
    origins = [
        origin_row(
            "INCOMING_MOTION",
            abs(incoming_value),
            "pressure inherited from previous draw motion mapped into this sorted seat",
        ),
        origin_row(
            "GAP_STRUCTURE",
            adjacent_pressure,
            "pressure created by left/right sorted gap geometry",
        ),
    ]

    if seat["zone"] == "MIDDLE":
        if packet.set_anatomy.middle_pressure == "MIDDLE_COMPRESSION_PRESSURE":
            origins.append(
                origin_row(
                    "MIDDLE_COMPRESSION",
                    20,
                    "middle body is carrying compression pressure",
                )
            )
        elif packet.set_anatomy.middle_pressure == "MIDDLE_EXPANSION_PRESSURE":
            origins.append(
                origin_row(
                    "GAP_STRUCTURE",
                    14,
                    "middle body is expanded by sorted body geometry",
                )
            )

    if (
        packet.set_anatomy.full_set_relation == "OUTER_EDGES_WIDER_THAN_MIDDLE"
        and seat["seat"] in {"S1", "S5"}
    ):
        origins.append(
            origin_row(
                "EDGE_IMBALANCE",
                12,
                "outer edges are wider than the middle body",
            )
        )
    if packet.set_anatomy.edge_balance == "ENTRY_HEAVIER" and seat["seat"] == "S1":
        origins.append(
            origin_row(
                "EDGE_IMBALANCE",
                8,
                "entry edge is heavier than exit edge",
            )
        )
    if packet.set_anatomy.edge_balance == "EXIT_HEAVIER" and seat["seat"] == "S5":
        origins.append(
            origin_row(
                "EDGE_IMBALANCE",
                8,
                "exit edge is heavier than entry edge",
            )
        )

    if max(left_gap, right_gap) >= 25:
        origins.append(
            origin_row(
                "GAP_STRUCTURE",
                10,
                "one adjacent side is over-open",
            )
        )
    if left_gap <= 10 and right_gap <= 10 and seat["zone"] == "MIDDLE":
        origins.append(
            origin_row(
                "HINGE_TRAP",
                10,
                "middle seat is trapped between two tight adjacent gaps",
            )
        )

    transfer = transfer_by_seat.get(seat["seat"], "BOUNDARY_UNKNOWN")
    if transfer == "REVERSAL":
        origins.append(
            origin_row(
                "TRANSFER_REVERSAL",
                13,
                "incoming and outgoing signs invert on the lane mapped to this seat",
            )
        )

    return aggregate_origins(origins)


def build_pressure_origin(packet: DrawSetPacket) -> dict[str, Any]:
    seat_rows = build_seat_rows(packet)
    draw_to_sorted = sorted_lane_for_draw_lane(packet)
    sorted_by_lane = lane_by_name(packet.sorted_form)
    incoming_by_sorted = {lane.lane: 0 for lane in packet.sorted_form}
    incoming_source_by_sorted: dict[str, str | None] = {
        lane.lane: None for lane in packet.sorted_form
    }
    direction_by_sorted = {lane.lane: "UNKNOWN" for lane in packet.sorted_form}
    transfer_by_seat = {
        row["sorted_seat"]: row["transfer"]
        for row in carry_reversal_rows(packet)
    }

    for motion in packet.draw_motion:
        sorted_lane = draw_to_sorted[motion.lane]
        incoming_by_sorted[sorted_lane] = motion.incoming_motion or 0
        incoming_source_by_sorted[sorted_lane] = motion.lane
        direction_by_sorted[sorted_lane] = motion_direction(motion.incoming_motion)

    rows: list[dict[str, Any]] = []
    for seat in seat_rows:
        lane = sorted_by_lane[seat["seat"]]
        incoming_value = incoming_by_sorted[seat["seat"]]
        left_gap = seat["left_relation"]["gap"] if seat["left_relation"] else 0
        right_gap = seat["right_relation"]["gap"] if seat["right_relation"] else 0
        adjacent_pressure = left_gap + right_gap
        origins = seat_origin_contributors(
            seat,
            incoming_value,
            packet,
            transfer_by_seat,
        )
        split = pressure_type_split(origins)
        score = split["total_pressure"]

        state = burden_state(
            lane,
            seat["left_relation"],
            seat["right_relation"],
            incoming_value,
            packet,
        )
        middle_edge_modifier = (
            packet.set_anatomy.middle_pressure
            if seat["zone"] == "MIDDLE"
            else packet.set_anatomy.edge_pressure
        )
        burden_gauge_name, burden_gauge_range = burden_gauge(score)
        pressure_gauge_name, pressure_gauge_range = pressure_gauge(adjacent_pressure)
        rows.append(
            {
                "seat": seat["seat"],
                "role": seat["role"],
                "number": seat["number"],
                "taxonomy": seat["taxonomy"],
                "source_draw_lane": incoming_source_by_sorted[seat["seat"]],
                "incoming_motion": incoming_value,
                "incoming_direction": direction_by_sorted[seat["seat"]],
                "adjacent_gap_pressure": adjacent_pressure,
                "gap_pressure": adjacent_pressure,
                "left_gap": left_gap if seat["left_relation"] else None,
                "right_gap": right_gap if seat["right_relation"] else None,
                "middle_edge_modifier": middle_edge_modifier,
                "pressure_origins": origins,
                "structural_pressure": split["structural_pressure"],
                "dynamic_pressure": split["dynamic_pressure"],
                "dominant_pressure_type": split["dominant_pressure_type"],
                "structural_ratio": split["structural_ratio"],
                "dynamic_ratio": split["dynamic_ratio"],
                "structural_sources": split["structural_sources"],
                "dynamic_sources": split["dynamic_sources"],
                "burden_score": score,
                "burden_level": burden_level(score),
                "burden_gauge": burden_gauge_name,
                "burden_gauge_range": burden_gauge_range,
                "burden_state": state,
                "pressure_level": burden_level(score),
                "pressure_gauge": pressure_gauge_name,
                "pressure_gauge_range": pressure_gauge_range,
                "pressure_role": state,
            }
        )

    highest = max(rows, key=lambda row: row["burden_score"])
    smallest = min(rows, key=lambda row: row["burden_score"])
    return {
        "rule": (
            "pressure origin explains why each sorted seat became pressured before pressure map and burden are read"
        ),
        "dominant_origin_seat": highest["seat"],
        "dominant_origin_score": highest["burden_score"],
        "smallest_origin_seat": smallest["seat"],
        "smallest_origin_score": smallest["burden_score"],
        "lanes": rows,
    }


def build_lane_burden(pressure_origin: dict[str, Any]) -> dict[str, Any]:
    rows = pressure_origin["lanes"]
    highest = max(rows, key=lambda row: row["burden_score"])
    smallest = min(rows, key=lambda row: row["burden_score"])
    return {
        "rule": (
            "burden is stored pressure on a sorted seat before it moves; "
            "incoming motion hits draw lanes, maps into sorted seats, and stores pressure there"
        ),
        "highest_burden_seat": highest["seat"],
        "highest_burden_state": highest["burden_state"],
        "highest_burden_level": highest["burden_level"],
        "highest_burden_score": highest["burden_score"],
        "highest_burden_gauge": highest["burden_gauge"],
        "highest_burden_gauge_range": highest["burden_gauge_range"],
        "smallest_burden_seat": smallest["seat"],
        "smallest_burden_state": smallest["burden_state"],
        "smallest_burden_level": smallest["burden_level"],
        "smallest_burden_score": smallest["burden_score"],
        "smallest_burden_gauge": smallest["burden_gauge"],
        "smallest_burden_gauge_range": smallest["burden_gauge_range"],
        "lanes": rows,
    }


def pressure_center(seat: str) -> str:
    if seat == "S1":
        return "CORE"
    if seat == "S5":
        return "ENDPOINT"
    return "MIDDLE"


def pressure_balance(rows: list[dict[str, Any]]) -> str:
    scores = {row["seat"]: row["burden_score"] for row in rows}
    left = scores["S1"] + scores["S2"]
    right = scores["S4"] + scores["S5"]
    edge = scores["S1"] + scores["S5"]
    middle = scores["S2"] + scores["S3"] + scores["S4"]
    center = scores["S3"]
    if edge > middle:
        return "EDGE_HEAVY"
    if center >= max(scores["S2"], scores["S4"]) and abs(left - right) <= 15:
        return "CENTER_HEAVY"
    if left > right + 15:
        return "LEFT_HEAVY"
    if right > left + 15:
        return "RIGHT_HEAVY"
    return "CENTER_HEAVY"


def pressure_distribution(rows: list[dict[str, Any]]) -> str:
    scores = sorted((row["burden_score"] for row in rows), reverse=True)
    total = sum(scores)
    if total == 0:
        return "SPREAD"
    if scores[0] >= total * 0.4 or scores[0] - scores[1] >= 25:
        return "FOCUSED"
    if scores[1] >= total * 0.22 or scores[0] - scores[1] <= 15:
        return "SPLIT"
    return "SPREAD"


def build_pressure_world(
    pressure_type: str,
    center: str,
    balance: str,
    distribution: str,
) -> dict[str, Any]:
    type_index = PRESSURE_WORLD_TYPES.index(pressure_type)
    center_index = PRESSURE_WORLD_CENTERS.index(center)
    balance_index = PRESSURE_WORLD_BALANCES.index(balance)
    distribution_index = PRESSURE_WORLD_DISTRIBUTIONS.index(distribution)
    world_number = (
        type_index
        * len(PRESSURE_WORLD_CENTERS)
        * len(PRESSURE_WORLD_BALANCES)
        * len(PRESSURE_WORLD_DISTRIBUTIONS)
        + center_index
        * len(PRESSURE_WORLD_BALANCES)
        * len(PRESSURE_WORLD_DISTRIBUTIONS)
        + balance_index
        * len(PRESSURE_WORLD_DISTRIBUTIONS)
        + distribution_index
        + 1
    )
    topology_number = (
        type_index
        * len(PRESSURE_WORLD_CENTERS)
        * len(PRESSURE_WORLD_DISTRIBUTIONS)
        + center_index
        * len(PRESSURE_WORLD_DISTRIBUTIONS)
        + distribution_index
        + 1
    )
    topology_name = PRESSURE_TOPOLOGY_NAMES[topology_number - 1]
    return {
        "world_slot": f"WORLD_{world_number:03d}",
        "topology_slot": f"TOPOLOGY_WORLD_{topology_number:02d}",
        "topology_name": topology_name,
        "base_world": pressure_type,
        "pressure_center": center,
        "pressure_balance": balance,
        "pressure_distribution": distribution,
        "world_key": f"{pressure_type}::{center}::{balance}::{distribution}",
        "topology_key": f"{pressure_type}::{center}::{distribution}",
        "naming_status": "TOPOLOGY_NAMED_EXACT_WORLD_UNNAMED",
        "rule": (
            "pressure world groups the draw by structural/dynamic authority, "
            "dominant pressure center, balance, and distribution"
        ),
    }


def iter_pressure_world_catalog() -> list[dict[str, Any]]:
    worlds: list[dict[str, Any]] = []
    for pressure_type in PRESSURE_WORLD_TYPES:
        for center in PRESSURE_WORLD_CENTERS:
            for balance in PRESSURE_WORLD_BALANCES:
                for distribution in PRESSURE_WORLD_DISTRIBUTIONS:
                    worlds.append(
                        build_pressure_world(
                            pressure_type,
                            center,
                            balance,
                            distribution,
                        )
                    )
    return worlds


def build_pressure_map(lane_burden: dict[str, Any]) -> dict[str, Any]:
    rows = lane_burden["lanes"]
    pressure_rows = [
        {
            "seat": row["seat"],
            "role": row["role"],
            "number": row["number"],
            "taxonomy": row["taxonomy"],
            "incoming_motion": row["incoming_motion"],
            "gap_pressure": row["gap_pressure"],
            "left_gap": row["left_gap"],
            "right_gap": row["right_gap"],
            "middle_edge_modifier": row["middle_edge_modifier"],
            "structural_pressure": row["structural_pressure"],
            "dynamic_pressure": row["dynamic_pressure"],
            "dominant_pressure_type": row["dominant_pressure_type"],
            "burden_score": row["burden_score"],
            "burden_gauge": row["burden_gauge"],
            "burden_gauge_range": row["burden_gauge_range"],
            "pressure_level": row["pressure_level"],
            "pressure_gauge": row["pressure_gauge"],
            "pressure_gauge_range": row["pressure_gauge_range"],
            "pressure_role": row["pressure_role"],
        }
        for row in rows
    ]
    dominant = max(pressure_rows, key=lambda row: row["burden_score"])
    smallest = min(pressure_rows, key=lambda row: row["burden_score"])
    structural_total = sum(row["structural_pressure"] for row in pressure_rows)
    dynamic_total = sum(row["dynamic_pressure"] for row in pressure_rows)
    if structural_total > dynamic_total:
        map_pressure_type = "STRUCTURAL_DOMINANT"
    elif dynamic_total > structural_total:
        map_pressure_type = "DYNAMIC_DOMINANT"
    else:
        map_pressure_type = "STRUCTURAL_DYNAMIC_BALANCED"
    center = pressure_center(dominant["seat"])
    balance = pressure_balance(rows)
    distribution = pressure_distribution(rows)
    pressure_world = build_pressure_world(
        map_pressure_type,
        center,
        balance,
        distribution,
    )
    return {
        "rule": "pressure map shows where the full sorted body is storing force",
        "dominant_pressure_seat": dominant["seat"],
        "dominant_pressure_score": dominant["burden_score"],
        "dominant_burden_gauge": dominant["burden_gauge"],
        "dominant_burden_gauge_range": dominant["burden_gauge_range"],
        "smallest_pressure_seat": smallest["seat"],
        "smallest_pressure_score": smallest["burden_score"],
        "smallest_burden_gauge": smallest["burden_gauge"],
        "smallest_burden_gauge_range": smallest["burden_gauge_range"],
        "structural_pressure_total": structural_total,
        "dynamic_pressure_total": dynamic_total,
        "map_pressure_type": map_pressure_type,
        "pressure_shape": "-".join(row["pressure_level"] for row in pressure_rows),
        "pressure_gauge_shape": "-".join(str(row["pressure_gauge"]) for row in pressure_rows),
        "burden_gauge_shape": "-".join(str(row["burden_gauge"]) for row in pressure_rows),
        "pressure_center": center,
        "pressure_balance": balance,
        "pressure_distribution": distribution,
        "pressure_world": pressure_world,
        "seats": pressure_rows,
    }


def classify_motion_state(
    packet: DrawSetPacket,
    lane_burden: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> dict[str, Any]:
    draw_pressure = packet.set_pressure.draw_pressure
    middle_pressure = packet.set_anatomy.middle_pressure
    transfer = outgoing_contract["transfer"]
    flow = draw_pressure.pressure_flow
    incoming_sign = sign_pattern([motion.incoming_motion for motion in packet.draw_motion])
    outgoing_sign = sign_pattern([motion.outgoing_motion for motion in packet.draw_motion])

    if transfer == "BOUNDARY_UNKNOWN" or flow == "UNKNOWN_BOUNDARY":
        state = "BOUNDARY_UNKNOWN"
    elif transfer in {"FULL_REVERSAL", "REVERSAL_PUSH", "HYBRID_COUNTER"}:
        state = "COUNTER_ROTATION"
    elif flow == "RELEASE":
        state = "RELEASING"
    elif flow == "RETENTION":
        state = "RETENTIVE"
    elif flow == "BALANCED_TRANSFER":
        state = "BALANCED_TRANSFER"
    else:
        state = "MIXED_TRANSFER"

    if transfer == "BOUNDARY_UNKNOWN" or flow == "UNKNOWN_BOUNDARY":
        body_state = "BOUNDARY_UNKNOWN"
    elif middle_pressure == "MIDDLE_COMPRESSION_PRESSURE":
        body_state = "COMPRESSED"
    elif middle_pressure == "MIDDLE_EXPANSION_PRESSURE":
        body_state = "EXPANDING"
    elif "REVERSAL" in transfer or incoming_sign != outgoing_sign:
        body_state = "REBOUNDING"
    elif flow == "RELEASE":
        body_state = "RELEASING"
    elif flow == "RETENTION":
        body_state = "RETENTIVE"
    else:
        body_state = "STABLE"

    return {
        "motion_state": state,
        "body_motion_state": body_state,
        "incoming_sign": incoming_sign,
        "outgoing_sign": outgoing_sign,
        "pressure_flow": flow,
        "transfer": transfer,
        "dominant_burden_seat": lane_burden["highest_burden_seat"],
        "dominant_burden_level": lane_burden["highest_burden_level"],
        "dominant_burden_state": lane_burden["highest_burden_state"],
        "law_phrase": (
            f"{state} + {body_state} + "
            f"{lane_burden['highest_burden_seat']}_{lane_burden['highest_burden_state']}"
        ),
        "rule": (
            "current motion state plus current technical body becomes the allowed outgoing state layer"
        ),
    }


def classify_motion_archetype(
    motion_state: dict[str, Any],
    pressure_map: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> dict[str, Any]:
    flow = outgoing_contract["flow"]
    transfer = outgoing_contract["transfer"]
    incoming_sign = motion_state["incoming_sign"]
    outgoing_sign = motion_state["outgoing_sign"]
    burden_seat = pressure_map["dominant_pressure_seat"]
    burden_center = pressure_map["pressure_center"]
    outgoing_lane = outgoing_contract["dominant_lane"]
    outgoing_zone = outgoing_contract["dominant_zone"]
    outgoing_motion = outgoing_contract.get("dominant_motion")

    if transfer == "BOUNDARY_UNKNOWN" or flow == "UNKNOWN_BOUNDARY":
        archetype = "BOUNDARY_UNKNOWN"
    elif "REVERSAL" in transfer and flow == "RELEASE":
        archetype = "COUNTER_RELEASE"
    elif flow == "RETENTION" and "CARRY" in transfer:
        archetype = "CARRY_LOCK"
    elif burden_center == "MIDDLE" and outgoing_zone == "MIDDLE":
        archetype = "MIDDLE_RELEASE"
    elif burden_seat == "S5" and outgoing_motion is not None and outgoing_motion < 0:
        archetype = "TAIL_RELEASE"
    elif outgoing_lane is not None and burden_seat != outgoing_contract["dominant_sorted_seat"]:
        archetype = "PRESSURE_TRANSFER"
    elif "REVERSAL" in transfer:
        archetype = "COUNTER"
    elif flow == "RELEASE":
        archetype = "RELEASE"
    elif flow == "RETENTION":
        archetype = "CARRY"
    elif incoming_sign != outgoing_sign:
        archetype = "EXCHANGE"
    elif "+" in outgoing_sign:
        archetype = "LIFT"
    elif "-" in outgoing_sign:
        archetype = "COLLAPSE"
    else:
        archetype = "TRANSFER"

    return {
        "motion_archetype": archetype,
        "rule": "motion archetype names the action/event created by state, flow, transfer, burden, and outgoing lane",
        "inputs": {
            "motion_state": motion_state["motion_state"],
            "pressure_flow": flow,
            "transfer": transfer,
            "incoming_sign": incoming_sign,
            "outgoing_sign": outgoing_sign,
            "dominant_burden_seat": burden_seat,
            "dominant_outgoing_lane": outgoing_lane,
        },
    }


def authority_origin_weight(
    origin: str,
    seat: str,
    pressure_map: dict[str, Any],
    motion_state: dict[str, Any],
    motion_archetype: dict[str, Any],
) -> float:
    base_world = pressure_map["pressure_world"]["base_world"]
    if base_world == "STRUCTURAL_DOMINANT":
        weights = {
            "GAP_STRUCTURE": 1.5,
            "MIDDLE_COMPRESSION": 1.8,
            "EDGE_IMBALANCE": 1.2,
            "HINGE_TRAP": 1.5,
            "INCOMING_MOTION": 0.8,
            "TRANSFER_REVERSAL": 1.0,
        }
    elif base_world == "DYNAMIC_DOMINANT":
        weights = {
            "GAP_STRUCTURE": 0.8,
            "MIDDLE_COMPRESSION": 1.1,
            "EDGE_IMBALANCE": 1.2,
            "HINGE_TRAP": 1.1,
            "INCOMING_MOTION": 1.7,
            "TRANSFER_REVERSAL": 1.6,
        }
    else:
        weights = {
            "GAP_STRUCTURE": 1.1,
            "MIDDLE_COMPRESSION": 1.2,
            "EDGE_IMBALANCE": 1.1,
            "HINGE_TRAP": 1.2,
            "INCOMING_MOTION": 1.2,
            "TRANSFER_REVERSAL": 1.2,
        }

    weight = weights.get(origin, 1.0)
    center = pressure_map["pressure_center"]
    balance = pressure_map["pressure_balance"]
    distribution = pressure_map["pressure_distribution"]
    seat_center = pressure_center(seat)

    if center == seat_center:
        weight += 0.15
    if distribution == "FOCUSED" and seat == pressure_map["dominant_pressure_seat"]:
        weight += 0.15
    elif distribution == "SPREAD":
        weight -= 0.05
    if balance == "LEFT_HEAVY" and seat in {"S1", "S2"}:
        weight += 0.1
    elif balance == "RIGHT_HEAVY" and seat in {"S4", "S5"}:
        weight += 0.1
    elif balance == "EDGE_HEAVY" and seat in {"S1", "S5"}:
        weight += 0.1
    elif balance == "CENTER_HEAVY" and seat == "S3":
        weight += 0.1

    state = motion_state["motion_state"]
    archetype = motion_archetype["motion_archetype"]
    if state == "COUNTER_ROTATION" and origin == "TRANSFER_REVERSAL":
        weight += 0.25
    if archetype == "MIDDLE_RELEASE" and origin in {"MIDDLE_COMPRESSION", "HINGE_TRAP"}:
        weight += 0.2
    if archetype in {"COUNTER_RELEASE", "COUNTER"} and origin in {"TRANSFER_REVERSAL", "INCOMING_MOTION"}:
        weight += 0.2
    if archetype == "TAIL_RELEASE" and seat == "S5":
        weight += 0.2

    return max(weight, 0.1)


def build_pressure_authority(
    pressure_origin: dict[str, Any],
    pressure_map: dict[str, Any],
    motion_state: dict[str, Any],
    motion_archetype: dict[str, Any],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for row in pressure_origin["lanes"]:
        breakdown: list[dict[str, Any]] = []
        for item in row["pressure_origins"]:
            raw = item["contribution"]
            weight = authority_origin_weight(
                item["origin"],
                row["seat"],
                pressure_map,
                motion_state,
                motion_archetype,
            )
            final = round(raw * weight, 2)
            breakdown.append(
                {
                    "origin": item["origin"],
                    "raw_pressure": raw,
                    "authority_weight": round(weight, 2),
                    "authority_pressure": final,
                    "meaning": item.get("meaning", ""),
                }
            )
        authority_pressure = round(
            sum(item["authority_pressure"] for item in breakdown),
            2,
        )
        winning_origin = max(
            breakdown,
            key=lambda item: item["authority_pressure"],
        )
        rows.append(
            {
                "seat": row["seat"],
                "role": row["role"],
                "number": row["number"],
                "taxonomy": row["taxonomy"],
                "source_draw_lane": row["source_draw_lane"],
                "raw_pressure": row["burden_score"],
                "authority_pressure": authority_pressure,
                "winning_origin": winning_origin["origin"],
                "winning_origin_pressure": winning_origin["authority_pressure"],
                "origin_breakdown": breakdown,
            }
        )

    authority_winner = max(rows, key=lambda row: row["authority_pressure"])
    raw_winner = max(rows, key=lambda row: row["raw_pressure"])
    return {
        "rule": "pressure authority weights existing pressure origins to decide which source has motion control",
        "authority_world": pressure_map["pressure_world"],
        "authority_winner_seat": authority_winner["seat"],
        "authority_winner_origin": authority_winner["winning_origin"],
        "authority_winner_score": authority_winner["authority_pressure"],
        "authority_winner_draw_lane": authority_winner["source_draw_lane"],
        "raw_pressure_winner_seat": raw_winner["seat"],
        "raw_pressure_winner_score": raw_winner["raw_pressure"],
        "authority_changed_winner": authority_winner["seat"] != raw_winner["seat"],
        "seats": rows,
    }


def opposite_seat(seat: str, balance: str) -> str:
    opposites = {
        "S1": "S5",
        "S2": "S4",
        "S4": "S2",
        "S5": "S1",
    }
    if seat == "S3":
        if balance == "LEFT_HEAVY":
            return "S4"
        if balance == "RIGHT_HEAVY":
            return "S2"
        if balance == "EDGE_HEAVY":
            return "S1"
        return "S3"
    return opposites.get(seat, seat)


def adjacent_collision_seat(seat: str, balance: str) -> str:
    if seat == "S1":
        return "S2"
    if seat == "S5":
        return "S4"
    if seat == "S2":
        return "S3" if balance != "LEFT_HEAVY" else "S1"
    if seat == "S4":
        return "S3" if balance != "RIGHT_HEAVY" else "S5"
    if seat == "S3":
        return "S2" if balance == "LEFT_HEAVY" else "S4"
    return seat


def seat_family(seat: str | None) -> str:
    if seat in {"S1", "S5"}:
        return "EDGE_FAMILY"
    if seat in {"S2", "S4"}:
        return "HINGE_FAMILY"
    if seat == "S3":
        return "CENTER_FAMILY"
    return "UNKNOWN_FAMILY"


def opposite_edge(seat: str) -> str:
    return "S5" if seat == "S1" else "S1"


def opposite_hinge(seat: str) -> str:
    return "S4" if seat == "S2" else "S2"


def draw_lane_for_sorted_seat(
    pressure_authority: dict[str, Any],
    sorted_seat: str,
) -> str | None:
    for row in pressure_authority["seats"]:
        if row["seat"] == sorted_seat:
            return row["source_draw_lane"]
    return None


def build_resolution_bias(
    pressure_authority: dict[str, Any],
    pressure_map: dict[str, Any],
    motion_state: dict[str, Any],
    motion_archetype: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> dict[str, Any]:
    authority_seat = pressure_authority["authority_winner_seat"]
    world = pressure_map["pressure_world"]
    base_world = world["base_world"]
    center = pressure_map["pressure_center"]
    balance = pressure_map["pressure_balance"]
    distribution = pressure_map["pressure_distribution"]
    transfer = motion_state["transfer"]
    state = motion_state["motion_state"]
    archetype = motion_archetype["motion_archetype"]

    primary = authority_seat
    secondary = opposite_seat(authority_seat, balance)
    tertiary = adjacent_collision_seat(authority_seat, balance)
    bias_type = "DIRECT_BIAS"
    reason = "default authority releases through itself"

    if authority_seat in {"S1", "S5"}:
        primary = authority_seat
        secondary = opposite_edge(authority_seat)
        tertiary = "S3"
        bias_type = "EDGE_BIAS"
        reason = "edge authority prefers edge-family resolution"
    elif authority_seat in {"S2", "S4"}:
        if base_world == "DYNAMIC_DOMINANT" and center == "MIDDLE" and distribution == "SPLIT":
            if transfer == "FULL_REVERSAL":
                primary = opposite_hinge(authority_seat)
                secondary = "S5" if authority_seat == "S2" else "S1"
                tertiary = "S1" if authority_seat == "S2" else "S5"
                bias_type = "HINGE_EDGE_SPLIT_BIAS"
                reason = "dynamic middle split full reversal first tests hinge opposite, then edge escape"
            else:
                primary = "S1" if authority_seat == "S2" else "S5"
                secondary = "S5" if authority_seat == "S2" else "S1"
                tertiary = opposite_hinge(authority_seat)
                bias_type = "EDGE_RESOLUTION_BIAS"
                reason = "dynamic middle split hybrid/carry motion prefers edge-family resolution"
        elif base_world == "STRUCTURAL_DOMINANT" and center == "MIDDLE":
            if balance == "RIGHT_HEAVY":
                primary = "S1" if authority_seat == "S4" else "S4"
                secondary = "S5" if authority_seat == "S4" else "S3"
            elif balance == "LEFT_HEAVY":
                primary = "S5" if authority_seat == "S2" else "S2"
                secondary = "S1" if authority_seat == "S2" else "S3"
            else:
                primary = opposite_hinge(authority_seat)
                secondary = adjacent_collision_seat(authority_seat, balance)
            tertiary = authority_seat
            bias_type = "STRUCTURAL_REPAIR_BIAS"
            reason = "structural middle authority prefers geometry repair before direct release"
        else:
            primary = opposite_hinge(authority_seat)
            secondary = adjacent_collision_seat(authority_seat, balance)
            tertiary = authority_seat
            bias_type = "HINGE_BIAS"
            reason = "hinge-family authority prefers opposite hinge or adjacent transfer"
    elif authority_seat == "S3":
        if distribution == "FOCUSED":
            primary = "S3"
            secondary = "S2" if balance != "RIGHT_HEAVY" else "S4"
            tertiary = "S4" if secondary == "S2" else "S2"
            bias_type = "CENTER_BIAS"
            reason = "focused center authority prefers center stabilization"
        else:
            primary = "S1" if balance in {"LEFT_HEAVY", "EDGE_HEAVY"} else "S5"
            secondary = opposite_edge(primary)
            tertiary = "S3"
            bias_type = "CENTER_TO_EDGE_BIAS"
            reason = "unfocused center authority resolves through edge family"

    if archetype == "TAIL_RELEASE" and authority_seat == "S5":
        primary = "S5"
        secondary = "S1"
        tertiary = "S4"
        bias_type = "TAIL_BIAS"
        reason = "tail release keeps endpoint as primary resolution"

    seats = [primary, secondary, tertiary]
    candidates = []
    for index, seat in enumerate(seats, start=1):
        candidates.append(
            {
                "rank": index,
                "seat": seat,
                "family": seat_family(seat),
                "draw_lane": draw_lane_for_sorted_seat(pressure_authority, seat),
            }
        )

    return {
        "rule": "resolution bias chooses the destination family before collision point is finalized",
        "bias_status": (
            "OPEN_BOUNDARY"
            if outgoing_contract["contract_status"] != "CONFIRMED_BY_NEXT_DRAW"
            else "HISTORICAL_VALIDATION"
        ),
        "authority_seat": authority_seat,
        "authority_family": seat_family(authority_seat),
        "bias_type": bias_type,
        "primary_bias_seat": primary,
        "primary_bias_family": seat_family(primary),
        "secondary_bias_seat": secondary,
        "secondary_bias_family": seat_family(secondary),
        "tertiary_bias_seat": tertiary,
        "tertiary_bias_family": seat_family(tertiary),
        "bias_reason": reason,
        "inputs": {
            "topology_name": world["topology_name"],
            "base_world": base_world,
            "pressure_center": center,
            "pressure_balance": balance,
            "pressure_distribution": distribution,
            "motion_state": state,
            "transfer": transfer,
            "motion_archetype": archetype,
        },
        "candidates": candidates,
    }


def collision_finding_key(
    pressure_authority: dict[str, Any],
    pressure_map: dict[str, Any],
    motion_state: dict[str, Any],
    collision_type: str,
) -> str:
    world = pressure_map["pressure_world"]
    topology = world["topology_name"].upper().replace(" ", "_")
    return "::".join(
        [
            topology,
            world["world_key"],
            f"AUTHSEAT_{pressure_authority['authority_winner_seat']}",
            f"AUTHORITY_{pressure_authority['authority_winner_origin']}",
            f"STATE_{motion_state['motion_state']}",
            f"TRANSFER_{motion_state['transfer']}",
            f"CTYPE_{collision_type}",
        ]
    )


def find_collision_branch_finding(
    pressure_authority: dict[str, Any],
    pressure_map: dict[str, Any],
    motion_state: dict[str, Any],
    collision_type: str,
) -> dict[str, Any] | None:
    law_key = collision_finding_key(
        pressure_authority,
        pressure_map,
        motion_state,
        collision_type,
    )
    return load_resolution_branch_findings().get(law_key)


def build_pre_collision_preference_field(
    branch_finding: dict[str, Any] | None,
    baseline_collision_seat: str,
    resolution_bias: dict[str, Any],
) -> dict[str, Any]:
    if branch_finding is None:
        return {
            "preference_status": "NO_HISTORICAL_FIELD",
            "preference_universe": "UNMEASURED",
            "selection_problem": "NO_BRANCH_FINDING_YET",
            "primary_seat": resolution_bias["primary_bias_seat"],
            "primary_rate": None,
            "secondary_seat": resolution_bias["secondary_bias_seat"],
            "secondary_rate": None,
            "primary_family": resolution_bias["primary_bias_family"],
            "secondary_family": resolution_bias["secondary_bias_family"],
            "family_field": [],
            "seat_field": [],
            "branch_gap": None,
            "read": "no historical branch field exists for this exact level-4 room yet",
        }

    seat_counts = Counter(branch_finding.get("observed_collision_seat_counts", {}))
    appearances = branch_finding["appearances"]
    seat_field = [
        {
            "seat": seat,
            "family": seat_family(seat),
            "count": count,
            "rate": percent(count, appearances),
        }
        for seat, count in seat_counts.most_common()
    ]
    family_counts: Counter[str] = Counter()
    for seat, count in seat_counts.items():
        family_counts[seat_family(seat)] += count
    family_field = [
        {
            "family": family,
            "count": count,
            "rate": percent(count, appearances),
        }
        for family, count in family_counts.most_common()
    ]

    primary_seat = branch_finding["primary_collision_seat"]
    secondary_seat = branch_finding["secondary_collision_seat"]
    primary_family = seat_family(primary_seat)
    secondary_family = seat_family(secondary_seat)
    primary_rate = branch_finding["primary_collision_rate"]
    secondary_rate = branch_finding["secondary_collision_rate"]
    branch_gap = round(primary_rate - secondary_rate, 2)

    if {primary_seat, secondary_seat} == {"S1", "S5"}:
        preference_universe = "EDGE_BINARY"
    elif {primary_seat, secondary_seat} == {"S2", "S4"}:
        preference_universe = "HINGE_BINARY"
    elif primary_seat == "S3" or secondary_seat == "S3":
        preference_universe = "CENTER_MIXED"
    elif primary_family == secondary_family:
        preference_universe = f"{primary_family}_BINARY"
    else:
        preference_universe = "MIXED_FAMILY_FIELD"

    if branch_gap <= 5:
        split_strength = "EVEN_SPLIT"
    elif branch_gap <= 15:
        split_strength = "LEANING_SPLIT"
    else:
        split_strength = "PRIMARY_LEAN"

    baseline_family = seat_family(baseline_collision_seat)
    if baseline_collision_seat == primary_seat:
        selection_problem = "PRIMARY_SELECTED"
    elif baseline_family == primary_family:
        selection_problem = "CORRECT_FAMILY_WRONG_SEAT"
    elif baseline_collision_seat == secondary_seat:
        selection_problem = "SECONDARY_SELECTED"
    elif baseline_family == secondary_family:
        selection_problem = "SECONDARY_FAMILY_SELECTED"
    else:
        selection_problem = "OUTSIDE_PREFERENCE_FIELD"

    return {
        "preference_status": "HISTORICAL_FIELD",
        "preference_universe": preference_universe,
        "split_strength": split_strength,
        "selection_problem": selection_problem,
        "primary_seat": primary_seat,
        "primary_rate": primary_rate,
        "secondary_seat": secondary_seat,
        "secondary_rate": secondary_rate,
        "tertiary_seat": branch_finding["tertiary_collision_seat"],
        "tertiary_rate": branch_finding["tertiary_collision_rate"],
        "primary_family": primary_family,
        "secondary_family": secondary_family,
        "family_field": family_field,
        "seat_field": seat_field,
        "branch_gap": branch_gap,
        "read": (
            f"{preference_universe} field: {primary_seat} first "
            f"({primary_rate}%), {secondary_seat} second ({secondary_rate}%), "
            f"{split_strength}, {selection_problem}"
        ),
    }


def baseline_collision_choice(
    pressure_authority: dict[str, Any],
    pressure_map: dict[str, Any],
    motion_state: dict[str, Any],
    motion_archetype: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> tuple[str, str, str]:
    authority_seat = pressure_authority["authority_winner_seat"]
    authority_origin = pressure_authority["authority_winner_origin"]
    archetype = motion_archetype["motion_archetype"]
    state = motion_state["motion_state"]
    balance = pressure_map["pressure_balance"]
    distribution = pressure_map["pressure_distribution"]
    flow = outgoing_contract["flow"]
    transfer = outgoing_contract["transfer"]

    if (
        state == "COUNTER_ROTATION"
        and "REVERSAL" in transfer
        and distribution == "SPLIT"
    ):
        return (
            "COUNTER_TERMINATION",
            opposite_seat(authority_seat, balance),
            "split reversal pushed authority across the body",
        )
    if archetype in {"COUNTER_RELEASE", "COUNTER"} or (
        state == "COUNTER_ROTATION"
        and authority_origin == "TRANSFER_REVERSAL"
    ):
        return (
            "COUNTER_TERMINATION",
            opposite_seat(authority_seat, balance),
            "authority pressure reversed across the body",
        )
    if authority_seat in {"S1", "S5"} or archetype == "TAIL_RELEASE":
        return (
            "EDGE_COLLISION",
            authority_seat,
            "authority pressure terminated at an edge or endpoint",
        )
    if distribution == "SPLIT" and authority_seat != pressure_map["dominant_pressure_seat"]:
        return (
            "TRANSFER_RELEASE",
            pressure_map["dominant_pressure_seat"],
            "split pressure moved authority toward the dominant pressure pole",
        )
    if distribution == "SPLIT" and flow == "RETENTION" and "REVERSAL" in transfer:
        return (
            "TRANSFER_RELEASE",
            adjacent_collision_seat(authority_seat, balance),
            "split retained reversal stepped pressure into a nearby seat",
        )
    if distribution == "FOCUSED" or archetype == "MIDDLE_RELEASE":
        return (
            "DIRECT_RELEASE",
            authority_seat,
            "focused or middle authority released through itself",
        )
    return (
        "TRANSFER_RELEASE",
        adjacent_collision_seat(authority_seat, balance),
        "pressure transferred to the nearest lawful seat",
    )


def build_collision_point(
    pressure_authority: dict[str, Any],
    pressure_map: dict[str, Any],
    motion_state: dict[str, Any],
    motion_archetype: dict[str, Any],
    resolution_bias: dict[str, Any],
    outgoing_contract: dict[str, Any],
    use_resolution_bias: bool = False,
) -> dict[str, Any]:
    authority_seat = pressure_authority["authority_winner_seat"]
    authority_origin = pressure_authority["authority_winner_origin"]

    if outgoing_contract["contract_status"] != "CONFIRMED_BY_NEXT_DRAW":
        status = "OPEN_BOUNDARY_NO_NEXT_DRAW"
    else:
        status = "HISTORICAL_VALIDATION"

    baseline_collision_type, baseline_collision_seat, baseline_reason = baseline_collision_choice(
        pressure_authority,
        pressure_map,
        motion_state,
        motion_archetype,
        outgoing_contract,
    )
    collision_type = baseline_collision_type
    collision_seat = baseline_collision_seat
    reason = baseline_reason

    branch_finding = find_collision_branch_finding(
        pressure_authority,
        pressure_map,
        motion_state,
        baseline_collision_type,
    )
    finding_used = False
    finding_source = "NO_FINDING"
    if branch_finding is not None:
        finding_source = "LEVEL_4_BRANCH_FINDING"
        if use_resolution_bias and branch_finding.get("primary_collision_seat"):
            collision_seat = branch_finding["primary_collision_seat"]
            finding_used = True
            reason = (
                f"{baseline_reason}; calibrated branch finding uses "
                f"{branch_finding['primary_collision_seat']} first "
                f"({branch_finding['primary_collision_rate']}%) and "
                f"{branch_finding['secondary_collision_seat']} second "
                f"({branch_finding['secondary_collision_rate']}%)"
            )

    preference_field = build_pre_collision_preference_field(
        branch_finding,
        baseline_collision_seat,
        resolution_bias,
    )

    collision_row = next(
        row for row in pressure_authority["seats"]
        if row["seat"] == collision_seat
    )
    observed_seat = outgoing_contract["dominant_sorted_seat"]
    observed_lane = outgoing_contract["dominant_lane"]
    expected_lane = collision_row["source_draw_lane"]
    if status != "HISTORICAL_VALIDATION":
        collision_seat_validation = "BOUNDARY_UNKNOWN"
        collision_lane_validation = "BOUNDARY_UNKNOWN"
    elif collision_seat == observed_seat:
        collision_seat_validation = "MATCH"
    else:
        collision_seat_validation = "MISS"

    if status != "HISTORICAL_VALIDATION":
        collision_lane_validation = "BOUNDARY_UNKNOWN"
    elif expected_lane == observed_lane:
        collision_lane_validation = "MATCH"
    else:
        collision_lane_validation = "MISS"

    if status != "HISTORICAL_VALIDATION":
        validation_result = "BOUNDARY_UNKNOWN"
    elif collision_seat_validation == "MATCH" and collision_lane_validation == "MATCH":
        validation_result = "MATCH"
    elif collision_seat_validation == "MATCH":
        validation_result = "SEAT_MATCH_LANE_MISS"
    elif collision_lane_validation == "MATCH":
        validation_result = "LANE_MATCH_SEAT_MISS"
    else:
        validation_result = "MISS"

    return {
        "rule": "collision point is where the winning authority terminates before number placement",
        "collision_status": status,
        "authority_seat": authority_seat,
        "authority_origin": authority_origin,
        "authority_score": pressure_authority["authority_winner_score"],
        "collision_seat": collision_seat,
        "collision_zone": seat_zone(collision_seat),
        "collision_type": collision_type,
        "collision_reason": reason,
        "baseline_collision_seat": baseline_collision_seat,
        "baseline_collision_type": baseline_collision_type,
        "baseline_collision_reason": baseline_reason,
        "resolution_bias_type": resolution_bias["bias_type"],
        "resolution_primary_family": resolution_bias["primary_bias_family"],
        "resolution_primary_seat": resolution_bias["primary_bias_seat"],
        "resolution_secondary_seat": resolution_bias["secondary_bias_seat"],
        "resolution_secondary_family": resolution_bias["secondary_bias_family"],
        "used_resolution_bias": use_resolution_bias,
        "finding_source": finding_source,
        "used_branch_finding": finding_used,
        "finding_law_key": branch_finding["law_key"] if branch_finding else None,
        "finding_conflict_type": branch_finding["conflict_type"] if branch_finding else None,
        "finding_appearances": branch_finding["appearances"] if branch_finding else None,
        "finding_primary_seat": (
            branch_finding["primary_collision_seat"] if branch_finding else None
        ),
        "finding_primary_rate": (
            branch_finding["primary_collision_rate"] if branch_finding else None
        ),
        "finding_secondary_seat": (
            branch_finding["secondary_collision_seat"] if branch_finding else None
        ),
        "finding_secondary_rate": (
            branch_finding["secondary_collision_rate"] if branch_finding else None
        ),
        "finding_tertiary_seat": (
            branch_finding["tertiary_collision_seat"] if branch_finding else None
        ),
        "finding_tertiary_rate": (
            branch_finding["tertiary_collision_rate"] if branch_finding else None
        ),
        "pre_collision_preference_field": preference_field,
        "expected_draw_lane": expected_lane,
        "observed_draw_lane": observed_lane,
        "observed_sorted_seat": observed_seat,
        "collision_seat_validation": collision_seat_validation,
        "collision_lane_validation": collision_lane_validation,
        "validation_result": validation_result,
    }


def build_technical_draw_address(
    packet: DrawSetPacket,
    draw_order_transition: dict[str, Any],
    draw_singularity_lens: dict[str, Any],
    motion_state: dict[str, Any],
    motion_archetype: dict[str, Any],
    pressure_map: dict[str, Any],
    pressure_authority: dict[str, Any],
    resolution_bias: dict[str, Any],
    collision_point: dict[str, Any],
    branch_selector: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> dict[str, Any]:
    face = draw_order_face_identity(packet)
    parts = [
        "TECH_DRAW",
        f"IN_{address_token(draw_order_transition['incoming_draw_family'])}",
        f"OUT_{address_token(draw_order_transition['outgoing_draw_family'])}",
        f"STATE_{address_token(motion_state['motion_state'])}",
        f"ARCHETYPE_{address_token(motion_archetype['motion_archetype'])}",
        (
            f"BURDEN_{address_token(pressure_map['dominant_pressure_seat'])}_"
            f"{address_token(pressure_map['seats'][0]['pressure_level'])}"
        ),
    ]

    dominant_pressure = next(
        row for row in pressure_map["seats"]
        if row["seat"] == pressure_map["dominant_pressure_seat"]
    )
    parts[-1] = (
        f"BURDEN_{address_token(dominant_pressure['seat'])}_"
        f"{address_token(dominant_pressure['pressure_level'])}_"
        f"{address_token(dominant_pressure['pressure_role'])}"
    )
    parts.extend(
        [
            f"AUTHORITY_{address_token(pressure_authority['authority_winner_origin'])}",
            f"AUTHSEAT_{address_token(pressure_authority['authority_winner_seat'])}",
            f"DS_{address_token(draw_singularity_lens['draw_singularity'])}",
            f"DSSUB_{address_token(draw_singularity_lens['subfamily'])}",
            f"DSPROFILE_{address_token(draw_singularity_lens['internal_profile'])}",
            f"RESBIAS_{address_token(resolution_bias['bias_type'])}",
            f"BIASFAM_{address_token(resolution_bias['primary_bias_family'])}",
            f"BIASSEAT_{address_token(resolution_bias['primary_bias_seat'])}",
            f"FINDSRC_{address_token(collision_point['finding_source'])}",
            f"FINDSEAT_{address_token(collision_point['finding_primary_seat'])}",
            (
                "PREF_"
                f"{address_token(collision_point['pre_collision_preference_field']['preference_universe'])}"
            ),
            (
                "SEL_"
                f"{address_token(collision_point['pre_collision_preference_field']['selection_problem'])}"
            ),
            f"BRANCH_{address_token(branch_selector['selector_result'])}",
            f"COLLISION_{address_token(collision_point['collision_seat'])}",
            f"CTYPE_{address_token(collision_point['collision_type'])}",
            f"FLOW_{address_token(outgoing_contract['flow'])}",
            f"TRANSFER_{address_token(outgoing_contract['transfer'])}",
            f"OUTLANE_{address_token(outgoing_contract['dominant_lane'])}",
            f"FACE_{address_token(face['face_family'])}",
            f"BODY_{address_token(packet.set_anatomy.full_set_relation)}",
            f"MIDDLE_{address_token(packet.set_anatomy.middle_pressure)}",
            f"CENTER_{address_token(pressure_map['pressure_center'])}",
            f"BALANCE_{address_token(pressure_map['pressure_balance'])}",
            f"DIST_{address_token(pressure_map['pressure_distribution'])}",
            f"PTYPE_{address_token(pressure_map['map_pressure_type'])}",
            f"WSLOT_{address_token(pressure_map['pressure_world']['world_slot'])}",
            f"TOPONAME_{address_token(pressure_map['pressure_world']['topology_name'])}",
        ]
    )
    return {
        "technical_draw_address": "::".join(parts),
        "rule": "compact reusable motion room identity",
        "inputs": {
            "incoming_draw_family": draw_order_transition["incoming_draw_family"],
            "outgoing_draw_family": draw_order_transition["outgoing_draw_family"],
            "motion_state": motion_state["motion_state"],
            "motion_archetype": motion_archetype["motion_archetype"],
            "highest_burden_seat": pressure_map["dominant_pressure_seat"],
            "highest_burden_level": dominant_pressure["pressure_level"],
            "highest_burden_state": dominant_pressure["pressure_role"],
            "authority_origin": pressure_authority["authority_winner_origin"],
            "authority_seat": pressure_authority["authority_winner_seat"],
            "authority_score": pressure_authority["authority_winner_score"],
            "draw_singularity": draw_singularity_lens["draw_singularity"],
            "ds_subfamily": draw_singularity_lens["subfamily"],
            "ds_internal_profile": draw_singularity_lens["internal_profile"],
            "resolution_bias_type": resolution_bias["bias_type"],
            "primary_bias_family": resolution_bias["primary_bias_family"],
            "primary_bias_seat": resolution_bias["primary_bias_seat"],
            "collision_seat": collision_point["collision_seat"],
            "collision_type": collision_point["collision_type"],
            "pressure_flow": outgoing_contract["flow"],
            "transfer": outgoing_contract["transfer"],
            "dominant_outgoing_lane": outgoing_contract["dominant_lane"],
            "face_family": face["face_family"],
            "set_relation": packet.set_anatomy.full_set_relation,
            "middle_pressure": packet.set_anatomy.middle_pressure,
            "pressure_center": pressure_map["pressure_center"],
            "pressure_balance": pressure_map["pressure_balance"],
            "pressure_distribution": pressure_map["pressure_distribution"],
            "map_pressure_type": pressure_map["map_pressure_type"],
            "pressure_world": pressure_map["pressure_world"],
            "technical_signature": packet.set_anatomy.technical_signature,
        },
    }


def build_origin_weight_validation(
    pressure_origin: dict[str, Any],
    pressure_map: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> dict[str, Any]:
    dominant_origin_seat = pressure_origin["dominant_origin_seat"]
    outgoing_sorted_seat = outgoing_contract["dominant_sorted_seat"]
    status = outgoing_contract["contract_status"]
    if status != "CONFIRMED_BY_NEXT_DRAW":
        result = "BOUNDARY_UNKNOWN"
    elif dominant_origin_seat == outgoing_sorted_seat:
        result = "MATCH"
    else:
        result = "MISS"

    if outgoing_sorted_seat is None:
        winning_row = None
    else:
        winning_row = next(
            (
                row for row in pressure_origin["lanes"]
                if row["seat"] == outgoing_sorted_seat
            ),
            None,
        )
    dominant_row = next(
        row for row in pressure_origin["lanes"]
        if row["seat"] == dominant_origin_seat
    )
    return {
        "rule": "validate whether highest pressure origin became dominant outgoing sorted seat",
        "validation_result": result,
        "dominant_origin_seat": dominant_origin_seat,
        "dominant_origin_score": pressure_origin["dominant_origin_score"],
        "dominant_origin_type": dominant_row["dominant_pressure_type"],
        "dominant_outgoing_lane": outgoing_contract["dominant_lane"],
        "dominant_outgoing_sorted_seat": outgoing_sorted_seat,
        "dominant_outgoing_score": (
            winning_row["burden_score"] if winning_row is not None else None
        ),
        "dominant_outgoing_type": (
            winning_row["dominant_pressure_type"] if winning_row is not None else None
        ),
        "pressure_type_total": pressure_map["map_pressure_type"],
        "structural_pressure_total": pressure_map["structural_pressure_total"],
        "dynamic_pressure_total": pressure_map["dynamic_pressure_total"],
        "debug_read": (
            "boundary unknown until next draw exists"
            if result == "BOUNDARY_UNKNOWN"
            else (
                "dominant pressure seat released through the dominant outgoing lane"
                if result == "MATCH"
                else "dominant outgoing lane came from a different pressure seat"
            )
        ),
    }


def build_branch_selector(
    collision_point: dict[str, Any],
    outgoing_contract: dict[str, Any],
) -> dict[str, Any]:
    preference = collision_point["pre_collision_preference_field"]
    observed_seat = outgoing_contract["dominant_sorted_seat"]
    if preference["preference_status"] != "HISTORICAL_FIELD":
        result = "NO_FIELD"
        selected_branch = None
        confidence = None
    elif observed_seat == preference["primary_seat"]:
        result = "PRIMARY_BRANCH_WON"
        selected_branch = preference["primary_seat"]
        confidence = preference["primary_rate"]
    elif observed_seat == preference["secondary_seat"]:
        result = "SECONDARY_BRANCH_WON"
        selected_branch = preference["secondary_seat"]
        confidence = preference["secondary_rate"]
    elif observed_seat == preference.get("tertiary_seat"):
        result = "TERTIARY_BRANCH_WON"
        selected_branch = preference["tertiary_seat"]
        confidence = preference["tertiary_rate"]
    elif any(row["seat"] == observed_seat for row in preference["seat_field"]):
        result = "FIELD_RIGHT_ALT_BRANCH"
        selected_branch = observed_seat
        confidence = next(
            row["rate"] for row in preference["seat_field"]
            if row["seat"] == observed_seat
        )
    else:
        result = "OUTSIDE_FIELD"
        selected_branch = observed_seat
        confidence = None

    if preference["preference_status"] != "HISTORICAL_FIELD":
        read = "no measured branch field exists for this room yet"
    elif result == "PRIMARY_BRANCH_WON":
        read = "historical primary branch won"
    elif result == "SECONDARY_BRANCH_WON":
        read = "secondary branch beat the primary branch"
    elif result == "TERTIARY_BRANCH_WON":
        read = "tertiary branch beat both primary and secondary branches"
    elif result == "FIELD_RIGHT_ALT_BRANCH":
        read = "measured field was right, but a lower branch won"
    else:
        read = "observed branch landed outside the measured preference field"

    return {
        "rule": "branch selector learns which side of the pre-collision preference field wins",
        "selector_status": (
            "OPEN_BOUNDARY"
            if outgoing_contract["contract_status"] != "CONFIRMED_BY_NEXT_DRAW"
            else "HISTORICAL_VALIDATION"
        ),
        "preference_universe": preference["preference_universe"],
        "selection_problem": preference["selection_problem"],
        "split_strength": preference.get("split_strength"),
        "primary_seat": preference["primary_seat"],
        "primary_rate": preference["primary_rate"],
        "secondary_seat": preference["secondary_seat"],
        "secondary_rate": preference["secondary_rate"],
        "observed_branch_seat": observed_seat,
        "observed_branch_lane": outgoing_contract["dominant_lane"],
        "selected_branch": selected_branch,
        "selected_branch_confidence": confidence,
        "selector_result": result,
        "read": read,
    }


def classify_body_effect(packet: DrawSetPacket) -> dict[str, Any]:
    dominant = dominant_motion_lane(packet.draw_motion, "incoming_motion")
    if dominant is None:
        return {
            "effect": "NO_PREVIOUS_DRAW_BOUNDARY",
            "dominant_lane": None,
            "dominant_sorted_seat": None,
            "seat_zone": None,
            "direction": "UNKNOWN",
            "rule": "incoming body effect requires previous draw motion",
        }

    draw_to_sorted = sorted_lane_for_draw_lane(packet)
    sorted_seat = draw_to_sorted[dominant.lane]
    zone = seat_zone(sorted_seat)
    direction = motion_direction(dominant.incoming_motion)
    anatomy = packet.set_anatomy

    if zone == "MIDDLE":
        if anatomy.middle_pressure == "MIDDLE_COMPRESSION_PRESSURE":
            effect = f"MIDDLE_{direction}_UNDER_COMPRESSION"
        elif anatomy.middle_pressure == "MIDDLE_EXPANSION_PRESSURE":
            effect = f"MIDDLE_{direction}_IN_EXPANSION"
        elif "STRETCH" in anatomy.middle_pressure:
            effect = f"MIDDLE_{direction}_HINGE_STRETCH"
        else:
            effect = f"MIDDLE_{direction}_STABLE_BODY"
    elif zone == "ENDPOINT":
        effect = f"ENDPOINT_{direction}_{anatomy.endpoint_band.upper().replace(' ', '_')}"
    elif zone == "CORE":
        effect = f"CORE_{direction}_{anatomy.starter_band.upper().replace(' ', '_')}"
    else:
        effect = f"UNKNOWN_{direction}"

    return {
        "effect": effect,
        "dominant_lane": dominant.lane,
        "dominant_role": dominant.role,
        "dominant_motion": dominant.incoming_motion,
        "dominant_sorted_seat": sorted_seat,
        "seat_zone": zone,
        "direction": direction,
        "middle_pressure": anatomy.middle_pressure,
        "edge_pressure": anatomy.edge_pressure,
        "full_set_relation": anatomy.full_set_relation,
        "rule": "dominant incoming draw-lane motion is mapped onto its current sorted seat",
    }


def classify_outgoing_contract(packet: DrawSetPacket) -> dict[str, Any]:
    dominant = dominant_motion_lane(packet.draw_motion, "outgoing_motion")
    rows = carry_reversal_rows(packet)
    profile = carry_reversal_profile(rows)
    draw_pressure = packet.set_pressure.draw_pressure
    if dominant is None:
        return {
            "contract_status": "OPEN_BOUNDARY_NO_NEXT_DRAW",
            "family": "UNKNOWN_OUTGOING_CONTRACT",
            "sign_pattern": sign_pattern([motion.outgoing_motion for motion in packet.draw_motion]),
            "dominant_lane": None,
            "dominant_sorted_seat": None,
            "dominant_zone": None,
            "energy": draw_pressure.outgoing_energy,
            "energy_class": draw_pressure.outgoing_energy_class,
            "flow": draw_pressure.pressure_flow,
            "transfer": profile,
            "body_search_rule": "next draw is missing, so no lawful outgoing contract can be confirmed yet",
            "carry_reversal": rows,
        }

    draw_to_sorted = sorted_lane_for_draw_lane(packet)
    sorted_seat = draw_to_sorted[dominant.lane]
    zone = seat_zone(sorted_seat)
    flow = draw_pressure.pressure_flow
    if flow == "RELEASE" and "REVERSAL" in profile:
        family = "REVERSAL_RELEASE"
    elif flow == "RELEASE":
        family = "MOTION_RELEASE"
    elif flow == "RETENTION" and "CARRY" in profile:
        family = "CARRY_RETENTION"
    elif flow == "RETENTION":
        family = "COUNTER_RETENTION"
    elif flow == "BALANCED_TRANSFER":
        family = "BALANCED_TRANSFER"
    else:
        family = "UNKNOWN_BOUNDARY"

    return {
        "contract_status": "CONFIRMED_BY_NEXT_DRAW",
        "family": family,
        "sign_pattern": sign_pattern([motion.outgoing_motion for motion in packet.draw_motion]),
        "dominant_lane": dominant.lane,
        "dominant_role": dominant.role,
        "dominant_motion": dominant.outgoing_motion,
        "dominant_sorted_seat": sorted_seat,
        "dominant_zone": zone,
        "energy": draw_pressure.outgoing_energy,
        "energy_average": draw_pressure.outgoing_energy_average,
        "energy_class": draw_pressure.outgoing_energy_class,
        "energy_gauge": draw_pressure.outgoing_energy_gauge,
        "energy_gauge_range": draw_pressure.outgoing_energy_gauge_range,
        "flow": flow,
        "transfer": profile,
        "body_search_rule": (
            "admit only bodies whose sorted body can express this outgoing sign pattern, "
            "dominant lane, energy class, flow, and carry/reversal profile"
        ),
        "carry_reversal": rows,
    }


def compact_body(packet: DrawSetPacket | None) -> dict[str, Any] | None:
    if packet is None:
        return None
    return {
        "date": packet.draw.draw_date.isoformat(),
        "white_balls": list(packet.draw.white_balls),
        "sorted_white_balls": list(packet.draw.sorted_white_balls),
        "set_health": packet.set_health.set_health,
        "technical_signature": packet.set_anatomy.technical_signature,
        "sorted_style": packet.sorted_style.set_style,
        "draw_style": packet.draw_style.draw_style,
        "draw_pressure": packet.set_pressure.draw_pressure.pressure_type,
        "sorted_pressure": packet.set_pressure.sorted_pressure.pressure_type,
    }


def build_truth_control(payload: dict[str, Any]) -> dict[str, Any]:
    outgoing = payload["outgoing_contract"]
    collision = payload["collision_point"]
    selector = payload["branch_selector"]
    has_confirmed_next = outgoing["contract_status"] == "CONFIRMED_BY_NEXT_DRAW"
    live_pressure = live_safe_pressure_context(payload)

    if not has_confirmed_next:
        exact_branch_authority = "NO_CALL_OPEN_BOUNDARY"
        exact_branch_read = "next draw is missing, so no exact outgoing branch can be truth-scored"
    elif collision["used_branch_finding"]:
        exact_branch_authority = "DISCOVERY_ONLY"
        exact_branch_read = (
            "collision branch used historical branch findings; treat as a discovery "
            "or explanation field until walk-forward proof upgrades it"
        )
    else:
        exact_branch_authority = "DIAGNOSTIC_INFERENCE"
        exact_branch_read = (
            "collision branch came from current diagnostic rules; it is not an exact "
            "live answer unless a separate prior-only memory layer proves it"
        )

    if has_confirmed_next:
        observed_outgoing_authority = "OBSERVED_HISTORICAL_FACT"
    else:
        observed_outgoing_authority = "NO_OBSERVED_NEXT_DRAW"

    return {
        "rule": (
            "truth control separates observed facts, live-safe inference, historical "
            "explanation, discovery memory, and exact-answer authority"
        ),
        "truth_levels": {
            "OBSERVED_FACT": "directly read from the current or previous/current draw",
            "LIVE_SAFE_INFERENCE": "computed from current/prior information only",
            "HISTORICAL_FACT": "known only because the next historical draw exists",
            "HISTORICAL_EXPLANATION": "explains how the known next draw resolved",
            "DISCOVERY_ONLY": "learned from historical fields and not trusted live by itself",
            "UNPROVEN": "pattern exists but exact answer authority is not proven",
            "NO_CALL": "not enough live-safe evidence to make the claim",
        },
        "claim_authority": {
            "current_draw": "OBSERVED_FACT",
            "sorted_body": "OBSERVED_FACT",
            "incoming_motion": "OBSERVED_FACT",
            "current_pressure": "OBSERVED_FACT",
            "live_safe_pressure_context": "LIVE_SAFE_INFERENCE",
            "pressure_origin_live_safe_sources": sorted(LIVE_SAFE_ORIGINS),
            "outgoing_contract": observed_outgoing_authority,
            "motion_state": (
                "HISTORICAL_EXPLANATION"
                if has_confirmed_next
                else "UNPROVEN_OPEN_BOUNDARY"
            ),
            "motion_archetype": (
                "HISTORICAL_EXPLANATION"
                if has_confirmed_next
                else "UNPROVEN_OPEN_BOUNDARY"
            ),
            "resolution_bias": (
                "HISTORICAL_EXPLANATION"
                if has_confirmed_next
                else "UNPROVEN_OPEN_BOUNDARY"
            ),
            "collision_point": exact_branch_authority,
            "branch_selector": (
                "HISTORICAL_VALIDATION"
                if selector["selector_status"] == "HISTORICAL_VALIDATION"
                else "NO_CALL"
            ),
            "technical_draw_address": (
                "HISTORICAL_ROOM_ID"
                if has_confirmed_next
                else "OPEN_BOUNDARY_ROOM_ID"
            ),
        },
        "live_safe_claims": {
            "world": live_pressure["world"],
            "authority_seat": live_pressure["authority_seat"],
            "authority_origin": live_pressure["authority_origin"],
            "dominant_pressure_seat": live_pressure["dominant_pressure_seat"],
            "pressure_shape": live_pressure["pressure_shape"],
            "pressure_type": live_pressure["map_pressure_type"],
            "pressure_center": live_pressure["pressure_center"],
            "pressure_balance": live_pressure["pressure_balance"],
            "pressure_distribution": live_pressure["pressure_distribution"],
        },
        "exact_branch_claim": {
            "authority": exact_branch_authority,
            "read": exact_branch_read,
            "collision_seat": collision["collision_seat"],
            "observed_outgoing_seat": outgoing["dominant_sorted_seat"],
            "observed_outgoing_lane": outgoing["dominant_lane"],
            "validation_result": collision["validation_result"],
            "selector_result": selector["selector_result"],
            "doctrine": (
                "Seat Taxonomy may describe exact branch history, but exact branch "
                "live authority must come from prior-only conditional memory proof."
            ),
        },
        "blocked_from_live_prediction": [
            "outgoing_contract",
            "outgoing motion state",
            "outgoing motion archetype",
            "branch_selector observed result",
            "collision validation result",
            "transfer reversal built from current-to-next motion",
        ],
    }


def build_seat_taxonomy_packet(
    packet: DrawSetPacket,
    next_packet: DrawSetPacket | None,
    use_resolution_bias: bool = False,
) -> SeatTaxonomyPacket:
    incoming_values = [motion.incoming_motion for motion in packet.draw_motion]
    outgoing_values = [motion.outgoing_motion for motion in packet.draw_motion]
    incoming_dominant = dominant_motion_lane(packet.draw_motion, "incoming_motion")
    outgoing_contract = classify_outgoing_contract(packet)
    draw_to_sorted = sorted_lane_for_draw_lane(packet)

    body_effect = classify_body_effect(packet)
    pressure_origin = build_pressure_origin(packet)
    lane_burden = build_lane_burden(pressure_origin)
    pressure_map = build_pressure_map(lane_burden)
    motion_state = classify_motion_state(packet, lane_burden, outgoing_contract)
    motion_archetype = classify_motion_archetype(
        motion_state,
        pressure_map,
        outgoing_contract,
    )
    pressure_authority = build_pressure_authority(
        pressure_origin,
        pressure_map,
        motion_state,
        motion_archetype,
    )
    resolution_bias = build_resolution_bias(
        pressure_authority,
        pressure_map,
        motion_state,
        motion_archetype,
        outgoing_contract,
    )
    collision_point = build_collision_point(
        pressure_authority,
        pressure_map,
        motion_state,
        motion_archetype,
        resolution_bias,
        outgoing_contract,
        use_resolution_bias=use_resolution_bias,
    )
    draw_order_transition = build_draw_order_transition(packet)
    draw_singularity_lens = build_draw_singularity_lens(
        packet,
        draw_order_transition,
        pressure_map,
        pressure_authority,
        resolution_bias,
        collision_point,
        motion_state,
        motion_archetype,
        outgoing_contract,
    )
    branch_selector = build_branch_selector(collision_point, outgoing_contract)
    technical_draw_address = build_technical_draw_address(
        packet,
        draw_order_transition,
        draw_singularity_lens,
        motion_state,
        motion_archetype,
        pressure_map,
        pressure_authority,
        resolution_bias,
        collision_point,
        branch_selector,
        outgoing_contract,
    )
    origin_weight_validation = build_origin_weight_validation(
        pressure_origin,
        pressure_map,
        outgoing_contract,
    )
    payload = {
        "schema": SCHEMA,
        "doctrine": {
            "law": "Draw order is cause/motion. Sorted order is result/body.",
            "read_order": [
                "previous_draw_order",
                "current_draw_order",
                "outgoing_motion_contract",
                "next_draw_order",
                "sorted_body_result",
            ],
            "rule": "do not read sorted body as a guess for draw order; read draw order as transition physics first",
        },
        "draw": {
            "date": packet.draw.draw_date.isoformat(),
            "index": packet.draw.draw_index,
            "white_balls": list(packet.draw.white_balls),
            "sorted_white_balls": list(packet.draw.sorted_white_balls),
        },
        "continuity": {
            "previous_date": (
                packet.previous_draw.draw_date.isoformat()
                if packet.previous_draw
                else None
            ),
            "current_date": packet.draw.draw_date.isoformat(),
            "next_date": (
                packet.next_draw.draw_date.isoformat()
                if packet.next_draw
                else None
            ),
        },
        "draw_order_transition": draw_order_transition,
        "draw_order_face_identity": draw_order_face_identity(packet),
        "draw_order_taxonomy": {
            "rule": "D1-D5 are read as cause/motion lanes before sorted body result",
            "lanes": draw_order_taxonomy_rows(packet),
        },
        "incoming_motion": {
            "rule": "previous draw -> current draw by D1-D5 lane",
            "sign_pattern": sign_pattern(incoming_values),
            "total_abs_energy": total_abs_motion(packet.draw_motion, "incoming_motion"),
            "dominant_lane": incoming_dominant.lane if incoming_dominant else None,
            "dominant_sorted_seat": (
                draw_to_sorted[incoming_dominant.lane] if incoming_dominant else None
            ),
            "dominant_motion": (
                incoming_dominant.incoming_motion if incoming_dominant else None
            ),
            "lanes": motion_lane_rows(packet, "incoming"),
        },
        "current_pressure": {
            "set_health": packet.set_health.set_health,
            "set_relation": packet.set_anatomy.full_set_relation,
            "middle_pressure": packet.set_anatomy.middle_pressure,
            "edge_pressure": packet.set_anatomy.edge_pressure,
            "technical_signature": packet.set_anatomy.technical_signature,
            "sorted_pressure": packet.set_pressure.sorted_pressure.pressure_type,
            "draw_pressure": packet.set_pressure.draw_pressure.pressure_type,
            "pressure_flow": packet.set_pressure.draw_pressure.pressure_flow,
            "pressure_fusion_profile": packet.set_pressure.draw_pressure.pressure_fusion_profile,
            "pressure_fusion": packet.set_pressure.draw_pressure.pressure_fusion,
        },
        "pressure_origin": pressure_origin,
        "lane_burden": lane_burden,
        "pressure_map": pressure_map,
        "pressure_authority": pressure_authority,
        "draw_singularity_lens": draw_singularity_lens,
        "resolution_bias": resolution_bias,
        "motion_state": motion_state,
        "motion_archetype": motion_archetype,
        "collision_point": collision_point,
        "branch_selector": branch_selector,
        "technical_draw_address": technical_draw_address,
        "origin_weight_validation": origin_weight_validation,
        "incoming_body_effect": body_effect,
        "outgoing_contract": outgoing_contract,
        "next_technical_body": compact_body(next_packet),
        "motion_law_candidate": {
            "rule": "highest burden lane + pressure relation + incoming transfer = likely outgoing motion lane",
            "candidate": (
                f"{lane_burden['highest_burden_seat']} "
                f"{lane_burden['highest_burden_level']} "
                f"{lane_burden['highest_burden_state']} + "
                f"{packet.set_anatomy.full_set_relation} + "
                f"{outgoing_contract['transfer']} -> "
                f"{outgoing_contract['dominant_lane']}"
            ),
            "motion_state": motion_state["motion_state"],
            "body_motion_state": motion_state["body_motion_state"],
            "expected_outgoing_lane": outgoing_contract["dominant_lane"],
            "expected_outgoing_sign": outgoing_contract["sign_pattern"],
            "status": outgoing_contract["contract_status"],
        },
        "sorted_result_body": {
            "rule": "sorted S1-S5 body is the result/body after draw order motion is read",
            "seats": build_seat_rows(packet),
        },
        "lawful_search_rule": (
            "motion first, body second, proposal last; do not admit bodies unless "
            "their sorted body can express the outgoing contract"
        ),
        "raw_outgoing_sign_pattern": sign_pattern(outgoing_values),
    }
    payload["truth_control"] = build_truth_control(payload)
    return SeatTaxonomyPacket(payload)


def selected_indexes(
    draws: list[Any],
    from_date: date | None,
    to_date: date | None,
    limit: int | None,
    latest: bool,
) -> list[int]:
    indexes = selected_draw_indexes(draws, from_date=from_date, to_date=to_date)
    if latest:
        indexes = list(reversed(indexes))
    if limit is not None:
        indexes = indexes[:limit]
    if latest:
        indexes = list(reversed(indexes))
    return indexes


def build_seat_taxonomy_packets(
    draws: list[Any],
    from_date: date | None = TRUSTED_DRAW_ORDER_START_DATE,
    to_date: date | None = None,
    limit: int | None = None,
    latest: bool = False,
    use_resolution_bias: bool = False,
) -> list[SeatTaxonomyPacket]:
    packets: list[SeatTaxonomyPacket] = []
    for index in selected_indexes(draws, from_date, to_date, limit, latest):
        current_packet = build_draw_set_packet(draws, index)
        next_packet = (
            build_draw_set_packet(draws, index + 1)
            if index + 1 < len(draws)
            else None
        )
        packets.append(
            build_seat_taxonomy_packet(
                current_packet,
                next_packet,
                use_resolution_bias=use_resolution_bias,
            )
        )
    return packets


def build_collision_law_key(payload: dict[str, Any], level: int = 4) -> str:
    world = payload["pressure_map"]["pressure_world"]
    authority = payload["pressure_authority"]
    motion_state = payload["motion_state"]
    collision = payload["collision_point"]
    topology = world["topology_name"].upper().replace(" ", "_")
    if level == 1:
        parts = [
            topology,
            f"BASE_{world['base_world']}",
            f"AUTHSEAT_{authority['authority_winner_seat']}",
            f"AUTHORITY_{authority['authority_winner_origin']}",
        ]
    elif level == 2:
        parts = [
            topology,
            f"BASE_{world['base_world']}",
            f"AUTHSEAT_{authority['authority_winner_seat']}",
            f"AUTHORITY_{authority['authority_winner_origin']}",
            f"STATE_{motion_state['motion_state']}",
            f"TRANSFER_{motion_state['transfer']}",
        ]
    elif level == 3:
        parts = [
            topology,
            f"BASE_{world['base_world']}",
            f"AUTHSEAT_{authority['authority_winner_seat']}",
            f"AUTHORITY_{authority['authority_winner_origin']}",
            f"STATE_{motion_state['motion_state']}",
            f"TRANSFER_{motion_state['transfer']}",
            f"CTYPE_{collision['collision_type']}",
        ]
    elif level == 4:
        parts = [
            topology,
            world["world_key"],
            f"AUTHSEAT_{authority['authority_winner_seat']}",
            f"AUTHORITY_{authority['authority_winner_origin']}",
            f"STATE_{motion_state['motion_state']}",
            f"TRANSFER_{motion_state['transfer']}",
            f"CTYPE_{collision['collision_type']}",
        ]
    else:
        raise ValueError("collision law audit level must be 1, 2, 3, or 4.")
    return "::".join(parts)


def percent(part: int, whole: int) -> float:
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, 2)


def most_common_value(counter: Counter[str]) -> str | None:
    if not counter:
        return None
    return counter.most_common(1)[0][0]


def ranked_counter(counter: Counter[str], total: int) -> list[dict[str, Any]]:
    return [
        {
            "value": value,
            "count": count,
            "rate": percent(count, total),
        }
        for value, count in counter.most_common()
    ]


def build_conflict_signature(
    observed_counter: Counter[str],
    lane_counter: Counter[str],
    branch_counter: Counter[str],
    appearances: int,
) -> dict[str, Any]:
    seat_rank = ranked_counter(observed_counter, appearances)
    lane_rank = ranked_counter(lane_counter, appearances)
    branch_rank = ranked_counter(branch_counter, appearances)
    primary = seat_rank[0] if seat_rank else {"value": None, "count": 0, "rate": 0.0}
    secondary = (
        seat_rank[1]
        if len(seat_rank) > 1
        else {"value": None, "count": 0, "rate": 0.0}
    )
    tertiary = (
        seat_rank[2]
        if len(seat_rank) > 2
        else {"value": None, "count": 0, "rate": 0.0}
    )
    if appearances < 3:
        conflict_type = "LOW_SAMPLE_CONFLICT"
    elif primary["rate"] >= 60:
        conflict_type = "CONVERGENT"
    elif primary["rate"] >= 45 and secondary["rate"] <= 25:
        conflict_type = "LEANING_CONVERGENT"
    elif abs(primary["rate"] - secondary["rate"]) <= 15 or secondary["rate"] >= 25:
        conflict_type = "DIVERGENT"
    else:
        conflict_type = "SPLIT_FIELD"
    return {
        "conflict_type": conflict_type,
        "primary_collision_seat": primary["value"],
        "primary_collision_count": primary["count"],
        "primary_collision_rate": primary["rate"],
        "secondary_collision_seat": secondary["value"],
        "secondary_collision_count": secondary["count"],
        "secondary_collision_rate": secondary["rate"],
        "tertiary_collision_seat": tertiary["value"],
        "tertiary_collision_count": tertiary["count"],
        "tertiary_collision_rate": tertiary["rate"],
        "seat_rank": seat_rank,
        "lane_rank": lane_rank,
        "branch_rank": branch_rank,
        "read": (
            f"{conflict_type}: primary={primary['value']} "
            f"{primary['rate']}%, secondary={secondary['value']} "
            f"{secondary['rate']}%"
        ),
    }


def build_collision_law_report(
    packets: list[SeatTaxonomyPacket],
    level: int = 4,
) -> dict[str, Any]:
    grouped: dict[str, dict[str, Any]] = {}
    skipped_boundary = 0
    for packet in packets:
        payload = packet.to_payload()
        collision = payload["collision_point"]
        if collision["collision_status"] != "HISTORICAL_VALIDATION":
            skipped_boundary += 1
            continue
        law_key = build_collision_law_key(payload, level=level)
        if law_key not in grouped:
            world = payload["pressure_map"]["pressure_world"]
            authority = payload["pressure_authority"]
            grouped[law_key] = {
                "law_key": law_key,
                "law_level": level,
                "topology_name": world["topology_name"],
                "world_key": world["world_key"],
                "authority_seat": authority["authority_winner_seat"],
                "authority_origin": authority["authority_winner_origin"],
                "motion_state": payload["motion_state"]["motion_state"],
                "transfer": payload["motion_state"]["transfer"],
                "collision_type": collision["collision_type"],
                "appearances": 0,
                "collision_seat_match_count": 0,
                "collision_lane_match_count": 0,
                "both_match_count": 0,
                "predicted_collision_seats": Counter(),
                "expected_draw_lanes": Counter(),
                "observed_collision_seats": Counter(),
                "observed_draw_lanes": Counter(),
                "observed_branches": Counter(),
                "dates": [],
            }
        row = grouped[law_key]
        row["appearances"] += 1
        if collision["collision_seat_validation"] == "MATCH":
            row["collision_seat_match_count"] += 1
        if collision["collision_lane_validation"] == "MATCH":
            row["collision_lane_match_count"] += 1
        if collision["validation_result"] == "MATCH":
            row["both_match_count"] += 1
        row["predicted_collision_seats"][collision["collision_seat"]] += 1
        if collision["expected_draw_lane"] is not None:
            row["expected_draw_lanes"][collision["expected_draw_lane"]] += 1
        if collision["observed_sorted_seat"] is not None:
            row["observed_collision_seats"][collision["observed_sorted_seat"]] += 1
        if collision["observed_draw_lane"] is not None:
            row["observed_draw_lanes"][collision["observed_draw_lane"]] += 1
        if (
            collision["observed_sorted_seat"] is not None
            and collision["observed_draw_lane"] is not None
        ):
            branch = (
                f"{collision['observed_sorted_seat']}/"
                f"{collision['observed_draw_lane']}"
            )
            row["observed_branches"][branch] += 1
        row["dates"].append(payload["draw"]["date"])

    rows: list[dict[str, Any]] = []
    for row in grouped.values():
        appearances = row["appearances"]
        predicted_counter = row.pop("predicted_collision_seats")
        expected_lane_counter = row.pop("expected_draw_lanes")
        observed_counter = row.pop("observed_collision_seats")
        lane_counter = row.pop("observed_draw_lanes")
        branch_counter = row.pop("observed_branches")
        row["collision_seat_match_rate"] = percent(
            row["collision_seat_match_count"],
            appearances,
        )
        row["collision_lane_match_rate"] = percent(
            row["collision_lane_match_count"],
            appearances,
        )
        row["both_match_rate"] = percent(row["both_match_count"], appearances)
        row["most_common_predicted_collision_seat"] = most_common_value(
            predicted_counter
        )
        row["most_common_expected_lane"] = most_common_value(expected_lane_counter)
        row["most_common_observed_collision_seat"] = most_common_value(
            observed_counter
        )
        row["most_common_observed_lane"] = most_common_value(lane_counter)
        row["most_common_observed_branch"] = most_common_value(branch_counter)
        row["predicted_collision_seat_counts"] = dict(predicted_counter)
        row["expected_lane_counts"] = dict(expected_lane_counter)
        row["observed_collision_seat_counts"] = dict(observed_counter)
        row["observed_lane_counts"] = dict(lane_counter)
        row["observed_branch_counts"] = dict(branch_counter)
        row["conflict_signature"] = build_conflict_signature(
            observed_counter,
            lane_counter,
            branch_counter,
            appearances,
        )
        rows.append(row)

    rows.sort(
        key=lambda row: (
            row["appearances"],
            row["both_match_rate"],
            row["collision_seat_match_rate"],
        ),
        reverse=True,
    )
    return {
        "rule": (
            "collision law report groups historical draws by pressure world, "
            "authority, motion state, transfer, and collision type"
        ),
        "historical_draws": sum(row["appearances"] for row in rows),
        "skipped_boundary_draws": skipped_boundary,
        "law_count": len(rows),
        "law_level": level,
        "laws": rows,
    }


def print_collision_law_report(
    report: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy Collision Law Report")
    print("=" * 72)
    print(f"Historical draws       {report['historical_draws']}")
    print(f"Boundary skipped       {report['skipped_boundary_draws']}")
    print(f"Law keys               {report['law_count']}")
    print(f"Law level              {report['law_level']}")
    print()
    rows = report["laws"] if limit is None else report["laws"][:limit]
    for row in rows:
        print(row["law_key"])
        print(
            f"  appearances          {row['appearances']} | "
            f"both={row['both_match_count']} ({row['both_match_rate']}%) | "
            f"seat={row['collision_seat_match_count']} "
            f"({row['collision_seat_match_rate']}%) | "
            f"lane={row['collision_lane_match_count']} "
            f"({row['collision_lane_match_rate']}%)"
        )
        print(
            "  common               "
            f"predicted={row['most_common_predicted_collision_seat']} | "
            f"expected_lane={row['most_common_expected_lane']} | "
            f"observed_seat={row['most_common_observed_collision_seat']} | "
            f"observed_lane={row['most_common_observed_lane']}"
        )
        signature = row["conflict_signature"]
        print(
            "  conflict             "
            f"{signature['conflict_type']} | "
            f"primary={signature['primary_collision_seat']} "
            f"{signature['primary_collision_rate']}% | "
            f"secondary={signature['secondary_collision_seat']} "
            f"{signature['secondary_collision_rate']}%"
        )
        print(f"  expected lanes      {row['expected_lane_counts']}")
        print(f"  observed seats       {row['observed_collision_seat_counts']}")
        print(f"  observed lanes       {row['observed_lane_counts']}")
        print()


def collision_law_status(row: dict[str, Any]) -> str:
    appearances = row["appearances"]
    both_rate = row["both_match_rate"]
    seat_rate = row["collision_seat_match_rate"]
    lane_rate = row["collision_lane_match_rate"]
    if appearances >= 5 and both_rate >= 80:
        return "PROVEN"
    if appearances >= 3 and both_rate >= 60:
        return "PROMISING"
    if appearances < 3 and both_rate <= 20:
        return "UNSTABLE"
    if appearances < 3:
        return "LOW_SAMPLE"
    if both_rate < 50:
        return "FAILED"
    if abs(seat_rate - lane_rate) >= 25:
        return "UNSTABLE"
    return "UNSTABLE"


def collision_failure_pattern(row: dict[str, Any]) -> str:
    if row["both_match_rate"] >= 75:
        return "CONSISTENT_MATCH"
    signature = row.get("conflict_signature")
    if signature and signature["conflict_type"] in {"DIVERGENT", "SPLIT_FIELD"}:
        return (
            f"{signature['conflict_type']}::"
            f"PRIMARY_{signature['primary_collision_seat']}_"
            f"{signature['primary_collision_rate']}::"
            f"SECONDARY_{signature['secondary_collision_seat']}_"
            f"{signature['secondary_collision_rate']}"
        )
    predicted_seat = row["most_common_predicted_collision_seat"]
    observed_seat = row["most_common_observed_collision_seat"]
    expected_lane = row["most_common_expected_lane"]
    observed_lane = row["most_common_observed_lane"]
    seat_part = (
        "SEAT_OK"
        if predicted_seat == observed_seat
        else f"SEAT_DRIFTS_{predicted_seat}_TO_{observed_seat}"
    )
    lane_part = (
        "LANE_OK"
        if expected_lane == observed_lane
        else f"LANE_DRIFTS_{expected_lane}_TO_{observed_lane}"
    )
    if (
        predicted_seat == observed_seat
        and expected_lane == observed_lane
        and row["both_match_rate"] < 50
    ):
        return "COMMON_OUTCOME_MATCHES_BUT_FIELD_IS_SPLIT"
    if row["collision_seat_match_rate"] >= 60 and row["collision_lane_match_rate"] < 40:
        return f"SEAT_RIGHT_LANE_WRONG::{lane_part}"
    if row["collision_lane_match_rate"] >= 60 and row["collision_seat_match_rate"] < 40:
        return f"LANE_RIGHT_SEAT_WRONG::{seat_part}"
    return f"{seat_part}::{lane_part}"


def collision_recommended_action(row: dict[str, Any], status: str) -> str:
    if status == "PROVEN":
        return "KEEP_AS_LAW_CANDIDATE"
    if status == "PROMISING":
        return "KEEP_AND_VALIDATE_MORE_WINDOWS"
    if status == "LOW_SAMPLE":
        return "COLLECT_MORE_APPEARANCES_BEFORE_CHANGING_RULE"
    if status == "FAILED":
        return "REBUILD_COLLISION_RULE_FOR_THIS_WORLD_AUTHORITY_PATTERN"
    return "INSPECT_SEAT_LANE_SPLIT_AND_ADD_CONFLICT_RULE"


def build_collision_law_audit(
    packets: list[SeatTaxonomyPacket],
    level: int = 4,
) -> dict[str, Any]:
    report = build_collision_law_report(packets, level=level)
    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for row in report["laws"]:
        audited = dict(row)
        status = collision_law_status(audited)
        audited["law_status"] = status
        audited["dominant_failure_pattern"] = collision_failure_pattern(audited)
        audited["recommended_action"] = collision_recommended_action(audited, status)
        status_counts[status] += 1
        rows.append(audited)

    status_rank = {
        "FAILED": 0,
        "UNSTABLE": 1,
        "PROMISING": 2,
        "PROVEN": 3,
        "LOW_SAMPLE": 4,
    }
    rows.sort(
        key=lambda row: (
            status_rank.get(row["law_status"], 9),
            -row["appearances"],
            row["both_match_rate"],
        )
    )
    return {
        "rule": (
            "collision law audit classifies law keys by repeat count, seat/lane "
            "match rates, and dominant failure pattern"
        ),
        "historical_draws": report["historical_draws"],
        "skipped_boundary_draws": report["skipped_boundary_draws"],
        "law_count": report["law_count"],
        "law_level": level,
        "status_counts": dict(status_counts),
        "laws": rows,
    }


def print_collision_law_audit(
    audit: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy Collision Law Audit")
    print("=" * 72)
    print(f"Historical draws       {audit['historical_draws']}")
    print(f"Boundary skipped       {audit['skipped_boundary_draws']}")
    print(f"Law keys               {audit['law_count']}")
    print(f"Law level              {audit['law_level']}")
    print(f"Status counts          {audit['status_counts']}")
    print()
    rows = audit["laws"] if limit is None else audit["laws"][:limit]
    for row in rows:
        print(row["law_key"])
        print(
            f"  status               {row['law_status']} | "
            f"appearances={row['appearances']} | "
            f"both={row['both_match_rate']}% | "
            f"seat={row['collision_seat_match_rate']}% | "
            f"lane={row['collision_lane_match_rate']}%"
        )
        print(f"  failure pattern      {row['dominant_failure_pattern']}")
        print(f"  action               {row['recommended_action']}")
        print(
            "  common               "
            f"predicted={row['most_common_predicted_collision_seat']} | "
            f"expected_lane={row['most_common_expected_lane']} | "
            f"observed_seat={row['most_common_observed_collision_seat']} | "
            f"observed_lane={row['most_common_observed_lane']}"
        )
        signature = row["conflict_signature"]
        print(
            "  conflict             "
            f"{signature['conflict_type']} | "
            f"primary={signature['primary_collision_seat']} "
            f"{signature['primary_collision_rate']}% | "
            f"secondary={signature['secondary_collision_seat']} "
            f"{signature['secondary_collision_rate']}%"
        )
        print(f"  observed seats       {row['observed_collision_seat_counts']}")
        print(f"  observed lanes       {row['observed_lane_counts']}")
        print()


def build_branch_selector_key(payload: dict[str, Any], level: int = 3) -> str:
    pressure_map = payload["pressure_map"]
    world = pressure_map["pressure_world"]
    authority = payload["pressure_authority"]
    preference = payload["collision_point"]["pre_collision_preference_field"]
    transition = payload["draw_order_transition"]
    face = payload["draw_order_face_identity"]
    if level == 5:
        ds = payload["draw_singularity_lens"]
        return "::".join(
            [
                f"UNIVERSE_{preference['preference_universe']}",
                f"DS_{address_token(ds['draw_singularity'])}",
                f"DSSUB_{address_token(ds['subfamily'])}",
                f"DSPROFILE_{address_token(ds['selector_profile'])}",
                f"AUTHSEAT_{authority['authority_winner_seat']}",
                f"AUTHORITY_{authority['authority_winner_origin']}",
            ]
        )
    dominant_pressure = next(
        row for row in pressure_map["seats"]
        if row["seat"] == pressure_map["dominant_pressure_seat"]
    )
    parts = [
        f"UNIVERSE_{preference['preference_universe']}",
        f"TOPOLOGY_{address_token(world['topology_name'])}",
        f"AUTHSEAT_{authority['authority_winner_seat']}",
        f"AUTHORITY_{authority['authority_winner_origin']}",
    ]
    if level >= 2:
        parts.extend(
            [
                f"WORLD_{world['world_key']}",
                f"CENTER_{pressure_map['pressure_center']}",
                f"BALANCE_{pressure_map['pressure_balance']}",
                f"DIST_{pressure_map['pressure_distribution']}",
                f"PTYPE_{pressure_map['map_pressure_type']}",
            ]
        )
    if level >= 3:
        parts.extend(
            [
                f"DOMPRESS_{pressure_map['dominant_pressure_seat']}",
                f"BURDEN_{dominant_pressure['pressure_role']}",
                f"INLANE_{transition['dominant_incoming_draw_lane']}",
                f"INSIGN_{transition['incoming_draw_sign']}",
                f"FACE_{address_token(face['face_family'])}",
            ]
        )
    if level >= 4:
        current_pressure = payload["current_pressure"]
        parts.extend(
            [
                f"SHAPE_{pressure_map['pressure_shape']}",
                f"BODY_{address_token(current_pressure['set_relation'])}",
                f"MIDDLE_{address_token(current_pressure['middle_pressure'])}",
                f"EDGE_{address_token(current_pressure['edge_pressure'])}",
                f"FUSION_{address_token(current_pressure['pressure_fusion'])}",
            ]
        )
    return "::".join(parts)


def branch_selector_status(row: dict[str, Any]) -> str:
    appearances = row["appearances"]
    top_rate = row["selected_branch_rate"]
    branch_gap = row["branch_gap"]
    if appearances < 3:
        return "LOW_SAMPLE"
    if appearances >= 5 and top_rate >= 80:
        return "PROVEN"
    if appearances >= 3 and top_rate >= 60:
        return "PROMISING"
    if branch_gap is not None and branch_gap <= 10:
        return "SPLIT"
    return "UNSTABLE"


def build_branch_selector_audit(
    packets: list[SeatTaxonomyPacket],
    level: int = 3,
) -> dict[str, Any]:
    grouped: dict[str, dict[str, Any]] = {}
    skipped = 0
    for packet in packets:
        payload = packet.to_payload()
        selector = payload["branch_selector"]
        preference = payload["collision_point"]["pre_collision_preference_field"]
        if (
            selector["selector_status"] != "HISTORICAL_VALIDATION"
            or preference["preference_status"] != "HISTORICAL_FIELD"
            or selector["observed_branch_seat"] is None
        ):
            skipped += 1
            continue
        key = build_branch_selector_key(payload, level=level)
        if key not in grouped:
            grouped[key] = {
                "selector_key": key,
                "selector_level": level,
                "preference_universe": preference["preference_universe"],
                "topology_name": payload["pressure_map"]["pressure_world"]["topology_name"],
                "world_key": payload["pressure_map"]["pressure_world"]["world_key"],
                "authority_seat": payload["pressure_authority"]["authority_winner_seat"],
                "authority_origin": payload["pressure_authority"]["authority_winner_origin"],
                "appearances": 0,
                "observed_branch_seats": Counter(),
                "observed_branch_lanes": Counter(),
                "selector_results": Counter(),
                "selection_problems": Counter(),
                "dates": [],
            }
        row = grouped[key]
        row["appearances"] += 1
        row["observed_branch_seats"][selector["observed_branch_seat"]] += 1
        if selector["observed_branch_lane"] is not None:
            row["observed_branch_lanes"][selector["observed_branch_lane"]] += 1
        row["selector_results"][selector["selector_result"]] += 1
        row["selection_problems"][selector["selection_problem"]] += 1
        row["dates"].append(payload["draw"]["date"])

    rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for row in grouped.values():
        appearances = row["appearances"]
        branch_counter = row.pop("observed_branch_seats")
        lane_counter = row.pop("observed_branch_lanes")
        result_counter = row.pop("selector_results")
        problem_counter = row.pop("selection_problems")
        ranked = branch_counter.most_common()
        primary = ranked[0] if ranked else (None, 0)
        secondary = ranked[1] if len(ranked) > 1 else (None, 0)
        row["selected_branch"] = primary[0]
        row["selected_branch_count"] = primary[1]
        row["selected_branch_rate"] = percent(primary[1], appearances)
        row["secondary_branch"] = secondary[0]
        row["secondary_branch_count"] = secondary[1]
        row["secondary_branch_rate"] = percent(secondary[1], appearances)
        row["branch_gap"] = round(
            row["selected_branch_rate"] - row["secondary_branch_rate"],
            2,
        )
        row["observed_branch_counts"] = dict(branch_counter)
        row["observed_lane_counts"] = dict(lane_counter)
        row["selector_result_counts"] = dict(result_counter)
        row["selection_problem_counts"] = dict(problem_counter)
        row["selector_status"] = branch_selector_status(row)
        row["read"] = (
            f"{row['preference_universe']} selects {row['selected_branch']} "
            f"at {row['selected_branch_rate']}% over {row['secondary_branch']} "
            f"at {row['secondary_branch_rate']}%"
        )
        status_counts[row["selector_status"]] += 1
        rows.append(row)

    status_rank = {
        "UNSTABLE": 0,
        "SPLIT": 1,
        "PROMISING": 2,
        "PROVEN": 3,
        "LOW_SAMPLE": 4,
    }
    rows.sort(
        key=lambda row: (
            status_rank.get(row["selector_status"], 9),
            -row["appearances"],
            -row["selected_branch_rate"],
        )
    )
    return {
        "rule": (
            "branch selector audit learns which branch wins inside the "
            "pre-collision preference field"
        ),
        "historical_draws": sum(row["appearances"] for row in rows),
        "skipped_draws": skipped,
        "selector_level": level,
        "selector_count": len(rows),
        "status_counts": dict(status_counts),
        "selectors": rows,
    }


def print_branch_selector_audit(
    audit: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy Branch Selector Audit")
    print("=" * 72)
    print(f"Historical draws       {audit['historical_draws']}")
    print(f"Skipped draws          {audit['skipped_draws']}")
    print(f"Selector keys          {audit['selector_count']}")
    print(f"Selector level         {audit['selector_level']}")
    print(f"Status counts          {audit['status_counts']}")
    print()
    rows = audit["selectors"] if limit is None else audit["selectors"][:limit]
    for row in rows:
        print(row["selector_key"])
        print(
            f"  status               {row['selector_status']} | "
            f"appearances={row['appearances']} | "
            f"selected={row['selected_branch']} {row['selected_branch_rate']}% | "
            f"secondary={row['secondary_branch']} {row['secondary_branch_rate']}% | "
            f"gap={row['branch_gap']}"
        )
        print(f"  universe             {row['preference_universe']}")
        print(f"  read                 {row['read']}")
        print(f"  observed branches    {row['observed_branch_counts']}")
        print(f"  selector results     {row['selector_result_counts']}")
        print(f"  selection problems   {row['selection_problem_counts']}")
        print()


WORLD_ACCURACY_FIELDS: tuple[tuple[str, str], ...] = (
    ("preference_universe", "Preference universe"),
    ("ds_family", "DS family"),
    ("ds_selector_profile", "DS selector profile"),
    ("authority_seat", "Authority seat"),
    ("authority_origin", "Authority origin"),
    ("pressure_center", "Pressure center"),
    ("pressure_balance", "Pressure balance"),
    ("pressure_distribution", "Pressure distribution"),
    ("map_pressure_type", "Pressure type"),
    ("dominant_pressure_seat", "Dominant pressure seat"),
    ("pressure_shape", "Pressure shape"),
    ("burden_gauge_shape", "Burden gauge shape"),
    ("motion_state", "Motion state"),
    ("motion_archetype", "Motion archetype"),
    ("transfer", "Transfer"),
    ("resolution_bias_type", "Resolution bias"),
    ("incoming_draw_sign", "Incoming draw sign"),
    ("dominant_incoming_draw_lane", "Dominant incoming draw lane"),
    ("incoming_draw_caste_side_pattern", "Incoming draw caste side"),
    ("face_family", "Draw face family"),
    ("turn_lanes", "Turn lanes"),
    ("set_relation", "Set relation"),
    ("middle_pressure", "Middle pressure"),
    ("edge_pressure", "Edge pressure"),
    ("pressure_fusion", "Pressure fusion"),
)


def world_accuracy_case(payload: dict[str, Any]) -> dict[str, Any] | None:
    selector = payload["branch_selector"]
    preference = payload["collision_point"]["pre_collision_preference_field"]
    if (
        selector["selector_status"] != "HISTORICAL_VALIDATION"
        or preference["preference_status"] != "HISTORICAL_FIELD"
        or selector["observed_branch_seat"] is None
    ):
        return None
    pressure_map = payload["pressure_map"]
    world = pressure_map["pressure_world"]
    authority = payload["pressure_authority"]
    transition = payload["draw_order_transition"]
    ds = payload["draw_singularity_lens"]
    face = payload["draw_order_face_identity"]
    current_pressure = payload["current_pressure"]
    return {
        "date": payload["draw"]["date"],
        "topology_name": world["topology_name"],
        "world_key": world["world_key"],
        "world_slot": world["world_slot"],
        "observed_branch": selector["observed_branch_seat"],
        "observed_lane": selector["observed_branch_lane"],
        "selection_problem": selector["selection_problem"],
        "selector_result": selector["selector_result"],
        "preference_universe": preference["preference_universe"],
        "ds_family": ds["draw_singularity"],
        "ds_subfamily": ds["subfamily"],
        "ds_selector_profile": ds["selector_profile"],
        "authority_seat": authority["authority_winner_seat"],
        "authority_origin": authority["authority_winner_origin"],
        "pressure_center": pressure_map["pressure_center"],
        "pressure_balance": pressure_map["pressure_balance"],
        "pressure_distribution": pressure_map["pressure_distribution"],
        "map_pressure_type": pressure_map["map_pressure_type"],
        "dominant_pressure_seat": pressure_map["dominant_pressure_seat"],
        "pressure_shape": pressure_map["pressure_shape"],
        "burden_gauge_shape": pressure_map["burden_gauge_shape"],
        "motion_state": payload["motion_state"]["motion_state"],
        "motion_archetype": payload["motion_archetype"]["motion_archetype"],
        "transfer": payload["outgoing_contract"]["transfer"],
        "resolution_bias_type": payload["resolution_bias"]["bias_type"],
        "incoming_draw_sign": transition["incoming_draw_sign"],
        "dominant_incoming_draw_lane": transition["dominant_incoming_draw_lane"],
        "incoming_draw_caste_side_pattern": ds["incoming_draw_caste_side_pattern"],
        "face_family": face["face_family"],
        "turn_lanes": "-".join(face["turn_lanes"]) if face["turn_lanes"] else "NONE",
        "set_relation": current_pressure["set_relation"],
        "middle_pressure": current_pressure["middle_pressure"],
        "edge_pressure": current_pressure["edge_pressure"],
        "pressure_fusion": current_pressure["pressure_fusion"],
    }


def branch_distribution(cases: list[dict[str, Any]]) -> dict[str, Any]:
    counter = Counter(str(case["observed_branch"]) for case in cases)
    appearances = len(cases)
    ranked = counter.most_common()
    primary = ranked[0] if ranked else (None, 0)
    secondary = ranked[1] if len(ranked) > 1 else (None, 0)
    primary_rate = percent(primary[1], appearances)
    secondary_rate = percent(secondary[1], appearances)
    return {
        "appearances": appearances,
        "selected_branch": primary[0],
        "selected_branch_count": primary[1],
        "selected_branch_rate": primary_rate,
        "secondary_branch": secondary[0],
        "secondary_branch_count": secondary[1],
        "secondary_branch_rate": secondary_rate,
        "branch_gap": round(primary_rate - secondary_rate, 2),
        "branch_counts": dict(counter),
    }


def world_discriminator_status(
    appearances: int,
    predicted_rate: float,
    lift: float,
    coverage_rate: float,
    low_sample_groups: int,
) -> str:
    if appearances < 6:
        return "LOW_SAMPLE"
    if coverage_rate < 35 and predicted_rate >= 80:
        return "NARROW_MICRO_POCKET"
    if predicted_rate >= 80 and lift >= 10 and coverage_rate >= 60 and low_sample_groups <= 1:
        return "STRONG_DISCRIMINATOR"
    if predicted_rate >= 65 and lift >= 7 and coverage_rate >= 50:
        return "USEFUL_DISCRIMINATOR"
    if lift >= 4 and coverage_rate >= 40:
        return "WEAK_SIGNAL"
    return "NO_HELP"


def test_world_discriminator(
    cases: list[dict[str, Any]],
    field: str,
    label: str,
    base_rate: float,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        grouped.setdefault(str(case.get(field) or "NONE"), []).append(case)

    correct = 0
    covered = 0
    low_sample_groups = 0
    group_rows: list[dict[str, Any]] = []
    for value, group_cases in grouped.items():
        dist = branch_distribution(group_cases)
        if dist["appearances"] < 3:
            low_sample_groups += 1
        else:
            correct += int(dist["selected_branch_count"])
            covered += int(dist["appearances"])
        group_rows.append({"value": value, **dist})
    predicted_rate = percent(correct, covered) if covered else 0.0
    coverage_rate = percent(covered, len(cases))
    lift = round(predicted_rate - base_rate, 2)
    group_rows.sort(
        key=lambda row: (
            -row["appearances"],
            -row["selected_branch_rate"],
            row["value"],
        )
    )
    return {
        "field": field,
        "label": label,
        "group_count": len(grouped),
        "usable_group_count": len(grouped) - low_sample_groups,
        "low_sample_group_count": low_sample_groups,
        "covered_cases": covered,
        "coverage_rate": coverage_rate,
        "predicted_branch_rate": predicted_rate,
        "lift_over_world_baseline": lift,
        "status": world_discriminator_status(
            len(cases),
            predicted_rate,
            lift,
            coverage_rate,
            low_sample_groups,
        ),
        "top_groups": group_rows[:8],
    }


def world_accuracy_status(summary: dict[str, Any]) -> str:
    appearances = summary["appearances"]
    base_rate = summary["selected_branch_rate"]
    best = summary.get("best_discriminator") or {}
    best_rate = float(best.get("predicted_branch_rate") or 0.0)
    if appearances < 10:
        return "LOW_SAMPLE_WORLD"
    if base_rate >= 70:
        return "WORLD_ALREADY_DIRECTIONAL"
    best_coverage = float(best.get("coverage_rate") or 0.0)
    if best_rate >= 75 and best_coverage >= 50:
        return "WORLD_FIXABLE_WITH_DISCRIMINATOR"
    if best_rate >= 65 and best_coverage >= 40:
        return "WORLD_HAS_WEAK_DISCRIMINATOR"
    if summary["branch_gap"] <= 10:
        return "TRUE_SPLIT_WORLD"
    return "WORLD_NEEDS_NEW_DISCRIMINATOR"


def build_world_accuracy_audit(
    packets: list[SeatTaxonomyPacket],
) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    skipped = 0
    for packet in packets:
        case = world_accuracy_case(packet.to_payload())
        if case is None:
            skipped += 1
            continue
        cases.append(case)

    world_cases: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        world_cases.setdefault(str(case["topology_name"]), []).append(case)

    worlds: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for topology_name, grouped_cases in world_cases.items():
        base = branch_distribution(grouped_cases)
        discriminators = [
            test_world_discriminator(
                grouped_cases,
                field,
                label,
                float(base["selected_branch_rate"]),
            )
            for field, label in WORLD_ACCURACY_FIELDS
        ]
        discriminator_rank = {
            "STRONG_DISCRIMINATOR": 0,
            "USEFUL_DISCRIMINATOR": 1,
            "WEAK_SIGNAL": 2,
            "NARROW_MICRO_POCKET": 3,
            "NO_HELP": 4,
            "LOW_SAMPLE": 5,
        }
        discriminators.sort(
            key=lambda row: (
                discriminator_rank.get(row["status"], 9),
                -row["lift_over_world_baseline"],
                -row["predicted_branch_rate"],
                -row["coverage_rate"],
                row["field"],
            )
        )
        best = discriminators[0] if discriminators else None
        summary = {
            "topology_name": topology_name,
            "world_slots": sorted({case["world_slot"] for case in grouped_cases}),
            "world_keys": dict(Counter(str(case["world_key"]) for case in grouped_cases)),
            **base,
            "preference_universes": dict(Counter(str(case["preference_universe"]) for case in grouped_cases)),
            "authority_seats": dict(Counter(str(case["authority_seat"]) for case in grouped_cases)),
            "authority_origins": dict(Counter(str(case["authority_origin"]) for case in grouped_cases)),
            "selection_problems": dict(Counter(str(case["selection_problem"]) for case in grouped_cases)),
            "best_discriminator": best,
            "discriminators": discriminators[:10],
        }
        summary["world_accuracy_status"] = world_accuracy_status(summary)
        if best:
            summary["recommended_action"] = (
                f"Use {best['field']} as the next branch discriminator"
                if best["status"] in {"STRONG_DISCRIMINATOR", "USEFUL_DISCRIMINATOR", "WEAK_SIGNAL"}
                else (
                    f"Treat {best['field']} as a narrow micro-pocket, not a world-level rule"
                    if best["status"] == "NARROW_MICRO_POCKET"
                    else "Do not tune yet; inspect split by hand or add a new discriminator"
                )
            )
        else:
            summary["recommended_action"] = "No discriminator evidence"
        status_counts[summary["world_accuracy_status"]] += 1
        worlds.append(summary)

    worlds.sort(
        key=lambda row: (
            -row["appearances"],
            row["world_accuracy_status"],
            row["topology_name"],
        )
    )
    return {
        "rule": (
            "world accuracy audit tests which current-draw fields improve branch "
            "selection inside each pressure topology world"
        ),
        "historical_draws": len(cases),
        "skipped_draws": skipped,
        "world_count": len(worlds),
        "status_counts": dict(status_counts),
        "tested_discriminator_fields": [
            {"field": field, "label": label}
            for field, label in WORLD_ACCURACY_FIELDS
        ],
        "worlds": worlds,
    }


def print_world_accuracy_audit(
    audit: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy World Accuracy Audit")
    print("=" * 72)
    print(f"Historical draws       {audit['historical_draws']}")
    print(f"Skipped draws          {audit['skipped_draws']}")
    print(f"Worlds                 {audit['world_count']}")
    print(f"Status counts          {audit['status_counts']}")
    print()
    worlds = audit["worlds"] if limit is None else audit["worlds"][:limit]
    for world in worlds:
        best = world.get("best_discriminator") or {}
        print(world["topology_name"])
        print(
            f"  status               {world['world_accuracy_status']} | "
            f"appearances={world['appearances']} | "
            f"selected={world['selected_branch']} {world['selected_branch_rate']}% | "
            f"secondary={world['secondary_branch']} {world['secondary_branch_rate']}% | "
            f"gap={world['branch_gap']}"
        )
        print(f"  branch counts        {world['branch_counts']}")
        print(f"  universes            {world['preference_universes']}")
        print(f"  authority seats      {world['authority_seats']}")
        print(f"  selection problems   {world['selection_problems']}")
        print(
            "  best discriminator   "
            f"{best.get('field')} | {best.get('status')} | "
            f"rate={best.get('predicted_branch_rate')}% | "
            f"lift={best.get('lift_over_world_baseline')} | "
            f"coverage={best.get('coverage_rate')}%"
        )
        if best.get("top_groups"):
            group_read = "; ".join(
                (
                    f"{group['value']} -> {group['selected_branch']} "
                    f"{group['selected_branch_rate']}% n={group['appearances']}"
                )
                for group in best["top_groups"][:4]
            )
            print(f"  top groups           {group_read}")
        print(f"  action               {world['recommended_action']}")
        print()


LIVE_SAFE_ORIGINS: frozenset[str] = frozenset(
    (
        "INCOMING_MOTION",
        "GAP_STRUCTURE",
        "MIDDLE_COMPRESSION",
        "EDGE_IMBALANCE",
        "HINGE_TRAP",
    )
)


def live_safe_pressure_context(payload: dict[str, Any]) -> dict[str, Any]:
    safe_rows: list[dict[str, Any]] = []
    for row in payload["pressure_origin"]["lanes"]:
        origins = [
            origin for origin in row["pressure_origins"]
            if origin["origin"] in LIVE_SAFE_ORIGINS
        ]
        score = sum(int(origin["contribution"]) for origin in origins)
        structural = sum(
            int(origin["contribution"])
            for origin in origins
            if origin["origin"] in STRUCTURAL_ORIGINS
        )
        dynamic = sum(
            int(origin["contribution"])
            for origin in origins
            if origin["origin"] == "INCOMING_MOTION"
        )
        safe_row = dict(row)
        safe_row["pressure_origins"] = origins
        safe_row["burden_score"] = score
        safe_row["structural_pressure"] = structural
        safe_row["dynamic_pressure"] = dynamic
        safe_row["dominant_pressure_type"] = (
            "STRUCTURAL" if structural > dynamic
            else "DYNAMIC" if dynamic > structural
            else "BALANCED"
        )
        safe_rows.append(safe_row)

    dominant = max(safe_rows, key=lambda row: row["burden_score"])
    smallest = min(safe_rows, key=lambda row: row["burden_score"])
    structural_total = sum(row["structural_pressure"] for row in safe_rows)
    dynamic_total = sum(row["dynamic_pressure"] for row in safe_rows)
    if structural_total > dynamic_total:
        map_type = "STRUCTURAL_DOMINANT"
    elif dynamic_total > structural_total:
        map_type = "DYNAMIC_DOMINANT"
    else:
        map_type = "STRUCTURAL_DYNAMIC_BALANCED"
    center = pressure_center(dominant["seat"])
    balance = pressure_balance(safe_rows)
    distribution = pressure_distribution(safe_rows)
    world = build_pressure_world(map_type, center, balance, distribution)
    winning_origin = max(
        dominant["pressure_origins"],
        key=lambda origin: int(origin["contribution"]),
    ) if dominant["pressure_origins"] else {"origin": "NONE", "contribution": 0}
    return {
        "rule": "live-safe pressure context excludes outgoing transfer/reversal evidence",
        "world": world,
        "dominant_pressure_seat": dominant["seat"],
        "dominant_pressure_score": dominant["burden_score"],
        "smallest_pressure_seat": smallest["seat"],
        "smallest_pressure_score": smallest["burden_score"],
        "authority_seat": dominant["seat"],
        "authority_origin": winning_origin["origin"],
        "authority_origin_score": winning_origin["contribution"],
        "pressure_shape": "-".join(row["burden_level"] for row in safe_rows),
        "structural_pressure_total": structural_total,
        "dynamic_pressure_total": dynamic_total,
        "map_pressure_type": map_type,
        "pressure_center": center,
        "pressure_balance": balance,
        "pressure_distribution": distribution,
    }


def walk_forward_case(payload: dict[str, Any]) -> dict[str, Any] | None:
    outgoing = payload["outgoing_contract"]
    if (
        outgoing["contract_status"] != "CONFIRMED_BY_NEXT_DRAW"
        or outgoing["dominant_sorted_seat"] is None
    ):
        return None
    live_pressure = live_safe_pressure_context(payload)
    transition = payload["draw_order_transition"]
    face = payload["draw_order_face_identity"]
    current_pressure = payload["current_pressure"]
    return {
        "date": payload["draw"]["date"],
        "index": payload["draw"]["index"],
        "actual_branch": outgoing["dominant_sorted_seat"],
        "actual_lane": outgoing["dominant_lane"],
        "actual_motion": outgoing["dominant_motion"],
        "actual_family": seat_family(outgoing["dominant_sorted_seat"]),
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
        "live_safe_pressure": live_pressure,
    }


def build_walk_forward_key(case: dict[str, Any], level: int = 3) -> str:
    parts = [
        f"TOPOLOGY_{address_token(case['topology_name'])}",
    ]
    if level >= 2:
        parts.extend(
            [
                f"WORLD_{case['world_key']}",
                f"AUTHSEAT_{case['authority_seat']}",
                f"AUTHORITY_{case['authority_origin']}",
            ]
        )
    if level >= 3:
        parts.extend(
            [
                f"INSIGN_{sign_address_token(case['incoming_draw_sign'])}",
                f"INLANE_{case['dominant_incoming_draw_lane']}",
                f"FACE_{address_token(case['face_family'])}",
            ]
        )
    if level >= 4:
        parts.extend(
            [
                f"SHAPE_{address_token(case['pressure_shape'])}",
                f"BODY_{address_token(case['set_relation'])}",
                f"MIDDLE_{address_token(case['middle_pressure'])}",
            ]
        )
    return "::".join(parts)


def build_walk_forward_audit(
    packets: list[SeatTaxonomyPacket],
    level: int = 3,
    min_sample: int = 3,
) -> dict[str, Any]:
    memory: dict[str, Counter[str]] = {}
    records: list[dict[str, Any]] = []
    skipped_boundary = 0
    for taxonomy_packet in sorted(
        packets,
        key=lambda item: item.to_payload()["draw"]["index"],
    ):
        case = walk_forward_case(taxonomy_packet.to_payload())
        if case is None:
            skipped_boundary += 1
            continue
        key = build_walk_forward_key(case, level=level)
        prior = memory.setdefault(key, Counter())
        prior_total = sum(prior.values())
        ranked = prior.most_common()
        if prior_total >= min_sample and ranked:
            predicted_branch = ranked[0][0]
            predicted_count = ranked[0][1]
            predicted_rate = percent(predicted_count, prior_total)
            prediction_status = "PREDICTED"
            branch_result = "MATCH" if predicted_branch == case["actual_branch"] else "MISS"
            family_result = (
                "MATCH"
                if seat_family(predicted_branch) == case["actual_family"]
                else "MISS"
            )
        else:
            predicted_branch = None
            predicted_count = 0
            predicted_rate = 0.0
            prediction_status = "LOW_PRIOR"
            branch_result = "NO_CALL"
            family_result = "NO_CALL"
        records.append(
            {
                "date": case["date"],
                "index": case["index"],
                "walk_forward_key": key,
                "walk_forward_level": level,
                "prediction_status": prediction_status,
                "prior_sample": prior_total,
                "prior_branch_counts": dict(prior),
                "predicted_branch": predicted_branch,
                "predicted_branch_prior_count": predicted_count,
                "predicted_branch_prior_rate": predicted_rate,
                "actual_branch": case["actual_branch"],
                "actual_lane": case["actual_lane"],
                "actual_motion": case["actual_motion"],
                "branch_result": branch_result,
                "family_result": family_result,
                "topology_name": case["topology_name"],
                "world_key": case["world_key"],
                "authority_seat": case["authority_seat"],
                "authority_origin": case["authority_origin"],
                "incoming_draw_sign": case["incoming_draw_sign"],
                "dominant_incoming_draw_lane": case["dominant_incoming_draw_lane"],
                "face_family": case["face_family"],
            }
        )
        prior[case["actual_branch"]] += 1

    predicted_records = [
        record for record in records
        if record["prediction_status"] == "PREDICTED"
    ]
    branch_hits = sum(1 for record in predicted_records if record["branch_result"] == "MATCH")
    family_hits = sum(1 for record in predicted_records if record["family_result"] == "MATCH")
    world_rows: list[dict[str, Any]] = []
    by_world: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_world.setdefault(record["topology_name"], []).append(record)
    for topology_name, world_records in by_world.items():
        world_predicted = [
            record for record in world_records
            if record["prediction_status"] == "PREDICTED"
        ]
        world_branch_hits = sum(
            1 for record in world_predicted
            if record["branch_result"] == "MATCH"
        )
        world_family_hits = sum(
            1 for record in world_predicted
            if record["family_result"] == "MATCH"
        )
        actual_counter = Counter(str(record["actual_branch"]) for record in world_records)
        predicted_counter = Counter(
            str(record["predicted_branch"]) for record in world_predicted
        )
        world_rows.append(
            {
                "topology_name": topology_name,
                "total_cases": len(world_records),
                "predicted_cases": len(world_predicted),
                "low_prior_cases": len(world_records) - len(world_predicted),
                "coverage_rate": percent(len(world_predicted), len(world_records)),
                "branch_hits": world_branch_hits,
                "branch_hit_rate": percent(world_branch_hits, len(world_predicted)),
                "family_hits": world_family_hits,
                "family_hit_rate": percent(world_family_hits, len(world_predicted)),
                "actual_branch_counts": dict(actual_counter),
                "predicted_branch_counts": dict(predicted_counter),
            }
        )
    world_rows.sort(
        key=lambda row: (
            -row["predicted_cases"],
            -row["branch_hit_rate"],
            row["topology_name"],
        )
    )
    return {
        "rule": (
            "walk-forward audit predicts each branch using only prior rows with "
            "the same live-safe key; next draw is used only for scoring"
        ),
        "walk_forward_level": level,
        "min_prior_sample": min_sample,
        "total_cases": len(records),
        "skipped_boundary_draws": skipped_boundary,
        "predicted_cases": len(predicted_records),
        "low_prior_cases": len(records) - len(predicted_records),
        "coverage_rate": percent(len(predicted_records), len(records)),
        "branch_hits": branch_hits,
        "branch_hit_rate": percent(branch_hits, len(predicted_records)),
        "family_hits": family_hits,
        "family_hit_rate": percent(family_hits, len(predicted_records)),
        "worlds": world_rows,
        "records": records,
    }


def print_walk_forward_audit(
    audit: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy Walk-Forward Audit")
    print("=" * 72)
    print(f"Total cases            {audit['total_cases']}")
    print(f"Boundary skipped       {audit['skipped_boundary_draws']}")
    print(f"Walk level             {audit['walk_forward_level']}")
    print(f"Min prior sample       {audit['min_prior_sample']}")
    print(
        f"Predicted cases        {audit['predicted_cases']} "
        f"({audit['coverage_rate']}%)"
    )
    print(
        f"Branch hits            {audit['branch_hits']} "
        f"({audit['branch_hit_rate']}%)"
    )
    print(
        f"Family hits            {audit['family_hits']} "
        f"({audit['family_hit_rate']}%)"
    )
    print()
    worlds = audit["worlds"] if limit is None else audit["worlds"][:limit]
    for world in worlds:
        print(world["topology_name"])
        print(
            f"  cases                total={world['total_cases']} "
            f"predicted={world['predicted_cases']} "
            f"coverage={world['coverage_rate']}%"
        )
        print(
            f"  branch               hits={world['branch_hits']} "
            f"rate={world['branch_hit_rate']}%"
        )
        print(
            f"  family               hits={world['family_hits']} "
            f"rate={world['family_hit_rate']}%"
        )
        print(f"  actual branches      {world['actual_branch_counts']}")
        print(f"  predicted branches   {world['predicted_branch_counts']}")
        print()


def build_family_first_walk_forward_audit(
    packets: list[SeatTaxonomyPacket],
    level: int = 2,
    min_sample: int = 3,
    family_threshold: float = 50.0,
    exact_threshold: float = 65.0,
) -> dict[str, Any]:
    memory: dict[str, Counter[str]] = {}
    records: list[dict[str, Any]] = []
    skipped_boundary = 0
    for taxonomy_packet in sorted(
        packets,
        key=lambda item: item.to_payload()["draw"]["index"],
    ):
        case = walk_forward_case(taxonomy_packet.to_payload())
        if case is None:
            skipped_boundary += 1
            continue
        key = build_walk_forward_key(case, level=level)
        prior = memory.setdefault(key, Counter())
        prior_total = sum(prior.values())
        family_counter = Counter(
            seat_family(branch) for branch, count in prior.items()
            for _ in range(count)
        )
        predicted_family = None
        predicted_family_count = 0
        predicted_family_rate = 0.0
        predicted_branch = None
        predicted_branch_count = 0
        predicted_branch_rate = 0.0
        prediction_status = "LOW_PRIOR"
        family_result = "NO_CALL"
        branch_result = "NO_CALL"

        if prior_total >= min_sample and family_counter:
            predicted_family, predicted_family_count = family_counter.most_common(1)[0]
            predicted_family_rate = percent(predicted_family_count, prior_total)
            if predicted_family_rate < family_threshold:
                prediction_status = "FAMILY_UNSTABLE"
                family_result = "NO_CALL"
            else:
                family_result = (
                    "MATCH" if predicted_family == case["actual_family"] else "MISS"
                )
                family_branches = Counter(
                    {
                        branch: count
                        for branch, count in prior.items()
                        if seat_family(branch) == predicted_family
                    }
                )
                branch_ranked = family_branches.most_common()
                family_branch_total = sum(family_branches.values())
                if family_branch_total >= min_sample and branch_ranked:
                    predicted_branch, predicted_branch_count = branch_ranked[0]
                    predicted_branch_rate = percent(
                        predicted_branch_count,
                        family_branch_total,
                    )
                    if predicted_branch_rate >= exact_threshold:
                        prediction_status = "FAMILY_AND_EXACT_PREDICTED"
                        branch_result = (
                            "MATCH"
                            if predicted_branch == case["actual_branch"]
                            else "MISS"
                        )
                    else:
                        prediction_status = "FAMILY_PREDICTED_EXACT_UNSTABLE"
                        branch_result = "NO_CALL"
                else:
                    prediction_status = "FAMILY_PREDICTED_EXACT_LOW_PRIOR"
                    branch_result = "NO_CALL"

        records.append(
            {
                "date": case["date"],
                "index": case["index"],
                "walk_forward_key": key,
                "walk_forward_level": level,
                "prediction_status": prediction_status,
                "prior_sample": prior_total,
                "prior_branch_counts": dict(prior),
                "prior_family_counts": dict(family_counter),
                "predicted_family": predicted_family,
                "predicted_family_prior_count": predicted_family_count,
                "predicted_family_prior_rate": predicted_family_rate,
                "predicted_branch": predicted_branch,
                "predicted_branch_prior_count": predicted_branch_count,
                "predicted_branch_prior_rate": predicted_branch_rate,
                "actual_family": case["actual_family"],
                "actual_branch": case["actual_branch"],
                "actual_lane": case["actual_lane"],
                "actual_motion": case["actual_motion"],
                "family_result": family_result,
                "branch_result": branch_result,
                "topology_name": case["topology_name"],
                "world_key": case["world_key"],
                "authority_seat": case["authority_seat"],
                "authority_origin": case["authority_origin"],
                "incoming_draw_sign": case["incoming_draw_sign"],
                "dominant_incoming_draw_lane": case["dominant_incoming_draw_lane"],
                "face_family": case["face_family"],
            }
        )
        prior[case["actual_branch"]] += 1

    family_called = [
        record for record in records
        if record["family_result"] in {"MATCH", "MISS"}
    ]
    exact_called = [
        record for record in records
        if record["branch_result"] in {"MATCH", "MISS"}
    ]
    family_hits = sum(1 for record in family_called if record["family_result"] == "MATCH")
    branch_hits = sum(1 for record in exact_called if record["branch_result"] == "MATCH")
    status_counts = Counter(record["prediction_status"] for record in records)

    world_rows: list[dict[str, Any]] = []
    by_world: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_world.setdefault(record["topology_name"], []).append(record)
    for topology_name, world_records in by_world.items():
        world_family_called = [
            record for record in world_records
            if record["family_result"] in {"MATCH", "MISS"}
        ]
        world_exact_called = [
            record for record in world_records
            if record["branch_result"] in {"MATCH", "MISS"}
        ]
        world_family_hits = sum(
            1 for record in world_family_called
            if record["family_result"] == "MATCH"
        )
        world_branch_hits = sum(
            1 for record in world_exact_called
            if record["branch_result"] == "MATCH"
        )
        world_rows.append(
            {
                "topology_name": topology_name,
                "total_cases": len(world_records),
                "family_called_cases": len(world_family_called),
                "exact_called_cases": len(world_exact_called),
                "family_coverage_rate": percent(len(world_family_called), len(world_records)),
                "exact_coverage_rate": percent(len(world_exact_called), len(world_records)),
                "family_hits": world_family_hits,
                "family_hit_rate": percent(world_family_hits, len(world_family_called)),
                "branch_hits": world_branch_hits,
                "branch_hit_rate": percent(world_branch_hits, len(world_exact_called)),
                "status_counts": dict(Counter(record["prediction_status"] for record in world_records)),
                "actual_branch_counts": dict(Counter(str(record["actual_branch"]) for record in world_records)),
                "predicted_family_counts": dict(
                    Counter(
                        str(record["predicted_family"])
                        for record in world_family_called
                    )
                ),
                "predicted_branch_counts": dict(
                    Counter(
                        str(record["predicted_branch"])
                        for record in world_exact_called
                    )
                ),
            }
        )
    world_rows.sort(
        key=lambda row: (
            -row["exact_called_cases"],
            -row["family_called_cases"],
            -row["branch_hit_rate"],
            row["topology_name"],
        )
    )
    return {
        "rule": (
            "family-first walk-forward predicts branch family first and only "
            "calls exact branch when the prior family room has enough exact-seat strength"
        ),
        "walk_forward_level": level,
        "min_prior_sample": min_sample,
        "family_threshold": family_threshold,
        "exact_threshold": exact_threshold,
        "total_cases": len(records),
        "skipped_boundary_draws": skipped_boundary,
        "family_called_cases": len(family_called),
        "family_low_or_unstable_cases": len(records) - len(family_called),
        "family_coverage_rate": percent(len(family_called), len(records)),
        "family_hits": family_hits,
        "family_hit_rate": percent(family_hits, len(family_called)),
        "exact_called_cases": len(exact_called),
        "exact_unstable_or_low_cases": len(records) - len(exact_called),
        "exact_coverage_rate": percent(len(exact_called), len(records)),
        "branch_hits": branch_hits,
        "branch_hit_rate": percent(branch_hits, len(exact_called)),
        "status_counts": dict(status_counts),
        "worlds": world_rows,
        "records": records,
    }


def print_family_first_walk_forward_audit(
    audit: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy Family-First Walk-Forward Audit")
    print("=" * 72)
    print(f"Total cases            {audit['total_cases']}")
    print(f"Boundary skipped       {audit['skipped_boundary_draws']}")
    print(f"Walk level             {audit['walk_forward_level']}")
    print(f"Min prior sample       {audit['min_prior_sample']}")
    print(f"Family threshold       {audit['family_threshold']}%")
    print(f"Exact threshold        {audit['exact_threshold']}%")
    print(
        f"Family calls           {audit['family_called_cases']} "
        f"({audit['family_coverage_rate']}%)"
    )
    print(
        f"Family hits            {audit['family_hits']} "
        f"({audit['family_hit_rate']}%)"
    )
    print(
        f"Exact calls            {audit['exact_called_cases']} "
        f"({audit['exact_coverage_rate']}%)"
    )
    print(
        f"Exact hits             {audit['branch_hits']} "
        f"({audit['branch_hit_rate']}%)"
    )
    print(f"Status counts          {audit['status_counts']}")
    print()
    worlds = audit["worlds"] if limit is None else audit["worlds"][:limit]
    for world in worlds:
        print(world["topology_name"])
        print(
            f"  family               calls={world['family_called_cases']} "
            f"coverage={world['family_coverage_rate']}% "
            f"hits={world['family_hits']} rate={world['family_hit_rate']}%"
        )
        print(
            f"  exact                calls={world['exact_called_cases']} "
            f"coverage={world['exact_coverage_rate']}% "
            f"hits={world['branch_hits']} rate={world['branch_hit_rate']}%"
        )
        print(f"  statuses             {world['status_counts']}")
        print(f"  actual branches      {world['actual_branch_counts']}")
        print(f"  predicted families   {world['predicted_family_counts']}")
        print(f"  predicted branches   {world['predicted_branch_counts']}")
        print()


def conditional_motion_memory_case(payload: dict[str, Any]) -> dict[str, Any] | None:
    case = walk_forward_case(payload)
    if case is None:
        return None
    outgoing = payload["outgoing_contract"]
    truth = payload["truth_control"]
    pressure = payload["current_pressure"]
    burden = payload["lane_burden"]
    pressure_origin = payload["pressure_origin"]
    pressure_authority = payload["pressure_authority"]
    collision = payload["collision_point"]
    selector = payload["branch_selector"]
    transition = payload["draw_order_transition"]
    face = payload["draw_order_face_identity"]
    pressure_map = payload["pressure_map"]
    draw_taxonomy_lanes = payload["draw_order_taxonomy"]["lanes"]
    incoming_lanes = payload["incoming_motion"]["lanes"]
    incoming_by_lane = {row["lane"]: row for row in incoming_lanes}
    authority_lane = pressure_authority["authority_winner_draw_lane"]
    authority_incoming = incoming_by_lane.get(authority_lane, {})
    incoming_gauge_pattern = "-".join(
        str(row["gauge"] or "NO_GAUGE") for row in incoming_lanes
    )
    incoming_gauge_range_pattern = "-".join(
        str(row["gauge_range"] or "NO_RANGE") for row in incoming_lanes
    )
    incoming_class_pattern = "-".join(
        address_token(str(row["broad_class"] or "NO_CLASS")) for row in incoming_lanes
    )
    incoming_lane_seat_path = "-".join(
        f"{row['lane']}:{row['sorted_seat']}:{row['seat_zone']}"
        for row in incoming_lanes
    )
    draw_lane_band_path = "-".join(
        f"{row['draw_lane']}:{row['draw_order_band']}:{row['mapped_sorted_seat']}"
        for row in draw_taxonomy_lanes
    )
    scenario = dict(case)
    scenario.update(
        {
            "edge_pressure": pressure["edge_pressure"],
            "pressure_fusion": pressure["pressure_fusion"],
            "pressure_fusion_profile": pressure["pressure_fusion_profile"],
            "pressure_flow": pressure["pressure_flow"],
            "sorted_pressure": pressure["sorted_pressure"],
            "draw_pressure": pressure["draw_pressure"],
            "technical_signature": pressure["technical_signature"],
            "draw_order_band_pattern": face["draw_order_band_pattern"],
            "draw_order_pattern": face["order_pattern"],
            "draw_transfer_pattern": face["transfer_pattern"],
            "draw_direction_pattern": face["direction_pattern"],
            "draw_style": face["draw_style"],
            "draw_turn_count": face["turn_count"],
            "draw_max_abs_lane": face["max_abs_lane"]["lane"],
            "draw_max_abs_role": face["max_abs_lane"]["role"],
            "draw_max_abs_distance": face["max_abs_lane"]["abs_distance"],
            "draw_lane_band_path": draw_lane_band_path,
            "incoming_energy": transition["incoming_energy"],
            "incoming_motion_gauge_pattern": incoming_gauge_pattern,
            "incoming_motion_gauge_range_pattern": incoming_gauge_range_pattern,
            "incoming_motion_class_pattern": incoming_class_pattern,
            "incoming_lane_seat_path": incoming_lane_seat_path,
            "authority_incoming_gauge": authority_incoming.get("gauge"),
            "authority_incoming_gauge_range": authority_incoming.get("gauge_range"),
            "authority_incoming_class": authority_incoming.get("broad_class"),
            "authority_incoming_sign": authority_incoming.get("sign"),
            "pressure_gauge_shape": pressure_map["pressure_gauge_shape"],
            "burden_gauge_shape": pressure_map["burden_gauge_shape"],
            "dominant_pressure_gauge": pressure_map["dominant_burden_gauge"],
            "dominant_pressure_gauge_range": pressure_map[
                "dominant_burden_gauge_range"
            ],
            "smallest_pressure_gauge": pressure_map["smallest_burden_gauge"],
            "smallest_pressure_gauge_range": pressure_map[
                "smallest_burden_gauge_range"
            ],
            "structural_pressure_total": pressure_map["structural_pressure_total"],
            "dynamic_pressure_total": pressure_map["dynamic_pressure_total"],
            "highest_burden_seat": burden["highest_burden_seat"],
            "highest_burden_level": burden["highest_burden_level"],
            "highest_burden_state": burden["highest_burden_state"],
            "highest_burden_gauge": burden["highest_burden_gauge"],
            "highest_burden_gauge_range": burden["highest_burden_gauge_range"],
            "smallest_burden_seat": burden["smallest_burden_seat"],
            "smallest_burden_state": burden["smallest_burden_state"],
            "smallest_burden_gauge": burden["smallest_burden_gauge"],
            "smallest_burden_gauge_range": burden["smallest_burden_gauge_range"],
            "dominant_origin_seat": pressure_origin["dominant_origin_seat"],
            "dominant_origin_score": pressure_origin["dominant_origin_score"],
            "authority_score": pressure_authority["authority_winner_score"],
            "authority_draw_lane": pressure_authority["authority_winner_draw_lane"],
            "outgoing_family": outgoing["family"],
            "outgoing_sign_pattern": outgoing["sign_pattern"],
            "outgoing_energy_class": outgoing["energy_class"],
            "outgoing_flow": outgoing["flow"],
            "outgoing_transfer": outgoing["transfer"],
            "collision_seat": collision["collision_seat"],
            "collision_type": collision["collision_type"],
            "collision_truth_authority": truth["exact_branch_claim"]["authority"],
            "selector_result": selector["selector_result"],
        }
    )
    return scenario


def build_conditional_motion_memory_key(
    case: dict[str, Any],
    level: int = 4,
) -> str:
    parts = [
        f"TOPOLOGY_{address_token(case['topology_name'])}",
    ]
    if level >= 2:
        parts.extend(
            [
                f"WORLD_{case['world_key']}",
                f"AUTHSEAT_{case['authority_seat']}",
                f"AUTHORITY_{case['authority_origin']}",
            ]
        )
    if level >= 3:
        parts.extend(
            [
                f"INSIGN_{sign_address_token(case['incoming_draw_sign'])}",
                f"INLANE_{case['dominant_incoming_draw_lane']}",
                f"INFAMILY_{address_token(case['incoming_draw_family'])}",
                f"FACE_{address_token(case['face_family'])}",
            ]
        )
    if level >= 4:
        parts.extend(
            [
                f"SHAPE_{address_token(case['pressure_shape'])}",
                f"BODY_{address_token(case['set_relation'])}",
                f"MIDDLE_{address_token(case['middle_pressure'])}",
                f"EDGE_{address_token(case['edge_pressure'])}",
            ]
        )
    if level >= 5:
        parts.extend(
            [
                f"FUSION_{address_token(case['pressure_fusion'])}",
                f"BURDEN_{address_token(case['highest_burden_seat'])}",
                f"BURDENSTATE_{address_token(case['highest_burden_state'])}",
                f"TURNS_{address_token(case['turn_lanes'])}",
            ]
        )
    return "::".join(parts)


def conditional_memory_status(
    appearances: int,
    primary_family_rate: float,
    primary_branch_rate: float,
    min_sample: int,
    family_threshold: float,
    exact_threshold: float,
    exact_proven_threshold: float,
) -> str:
    if appearances < min_sample:
        return "LOW_SAMPLE"
    if primary_family_rate < family_threshold:
        return "FAMILY_UNSTABLE"
    if appearances >= 5 and primary_branch_rate >= exact_proven_threshold:
        return "EXACT_PROVEN"
    if primary_branch_rate >= exact_threshold:
        return "EXACT_PROMISING"
    return "FAMILY_ONLY_EXACT_UNSTABLE"


def build_conditional_memory_scenario(
    key: str,
    rows: list[dict[str, Any]],
    min_sample: int,
    family_threshold: float,
    exact_threshold: float,
    exact_proven_threshold: float,
) -> dict[str, Any]:
    appearances = len(rows)
    branch_counts = Counter(row["actual_branch"] for row in rows)
    family_counts = Counter(row["actual_family"] for row in rows)
    lane_counts = Counter(str(row["actual_lane"]) for row in rows)
    flow_counts = Counter(row["outgoing_flow"] for row in rows)
    transfer_counts = Counter(row["outgoing_transfer"] for row in rows)
    outgoing_family_counts = Counter(row["outgoing_family"] for row in rows)
    sign_counts = Counter(row["outgoing_sign_pattern"] for row in rows)
    primary_branch, primary_branch_count = branch_counts.most_common(1)[0]
    primary_family, primary_family_count = family_counts.most_common(1)[0]
    secondary_branch = None
    secondary_branch_count = 0
    if len(branch_counts) > 1:
        secondary_branch, secondary_branch_count = branch_counts.most_common(2)[1]
    primary_branch_rate = percent(primary_branch_count, appearances)
    primary_family_rate = percent(primary_family_count, appearances)
    secondary_branch_rate = percent(secondary_branch_count, appearances)
    branch_gap = round(primary_branch_rate - secondary_branch_rate, 2)
    if appearances < min_sample:
        split_type = "LOW_SAMPLE_SPLIT"
    elif primary_branch_rate >= exact_threshold:
        split_type = "EXACT_CONVERGENT"
    elif primary_family_rate >= family_threshold:
        split_type = "FAMILY_CONVERGENT_BRANCH_SPLIT"
    elif branch_gap <= 15:
        split_type = "DIVERGENT_SPLIT"
    else:
        split_type = "WEAK_LEAN"

    status = conditional_memory_status(
        appearances,
        primary_family_rate,
        primary_branch_rate,
        min_sample,
        family_threshold,
        exact_threshold,
        exact_proven_threshold,
    )
    exemplar = rows[-1]
    return {
        "scenario_key": key,
        "memory_status": status,
        "split_type": split_type,
        "appearances": appearances,
        "condition": {
            "topology_name": exemplar["topology_name"],
            "world_key": exemplar["world_key"],
            "world_slot": exemplar["world_slot"],
            "map_pressure_type": exemplar["map_pressure_type"],
            "pressure_center": exemplar["pressure_center"],
            "pressure_balance": exemplar["pressure_balance"],
            "pressure_distribution": exemplar["pressure_distribution"],
            "pressure_shape": exemplar["pressure_shape"],
            "authority_seat": exemplar["authority_seat"],
            "authority_origin": exemplar["authority_origin"],
            "dominant_pressure_seat": exemplar["dominant_pressure_seat"],
            "dominant_incoming_draw_lane": exemplar["dominant_incoming_draw_lane"],
            "incoming_draw_sign": exemplar["incoming_draw_sign"],
            "incoming_draw_family": exemplar["incoming_draw_family"],
            "incoming_energy_class": exemplar["incoming_energy_class"],
            "face_family": exemplar["face_family"],
            "turn_lanes": exemplar["turn_lanes"],
            "set_relation": exemplar["set_relation"],
            "middle_pressure": exemplar["middle_pressure"],
            "edge_pressure": exemplar["edge_pressure"],
            "pressure_fusion": exemplar["pressure_fusion"],
            "highest_burden_seat": exemplar["highest_burden_seat"],
            "highest_burden_level": exemplar["highest_burden_level"],
            "highest_burden_state": exemplar["highest_burden_state"],
            "dominant_origin_seat": exemplar["dominant_origin_seat"],
        },
        "outcomes": {
            "primary_family": primary_family,
            "primary_family_count": primary_family_count,
            "primary_family_rate": primary_family_rate,
            "primary_branch": primary_branch,
            "primary_branch_count": primary_branch_count,
            "primary_branch_rate": primary_branch_rate,
            "secondary_branch": secondary_branch,
            "secondary_branch_count": secondary_branch_count,
            "secondary_branch_rate": secondary_branch_rate,
            "branch_gap": branch_gap,
            "branch_counts": dict(branch_counts),
            "family_counts": dict(family_counts),
            "lane_counts": dict(lane_counts),
            "outgoing_family_counts": dict(outgoing_family_counts),
            "outgoing_flow_counts": dict(flow_counts),
            "outgoing_transfer_counts": dict(transfer_counts),
            "outgoing_sign_counts": dict(sign_counts),
        },
        "live_use": (
            "PROVEN_EXACT_PATTERN"
            if status == "EXACT_PROVEN"
            else "EXACT_PATTERN_EVIDENCE"
            if status == "EXACT_PROMISING"
            else "FAMILY_FIELD_EVIDENCE"
            if status == "FAMILY_ONLY_EXACT_UNSTABLE"
            else "SPLIT_FIELD_EVIDENCE"
            if status == "FAMILY_UNSTABLE"
            else "HISTORICAL_EXACT_MOMENT"
        ),
        "truth_authority": (
            "LIVE_SAFE_EXACT_PATTERN"
            if status == "EXACT_PROVEN"
            else "HISTORICAL_EXACT_PATTERN"
            if status == "EXACT_PROMISING"
            else "HISTORICAL_FAMILY_FIELD"
            if status == "FAMILY_ONLY_EXACT_UNSTABLE"
            else "HISTORICAL_SPLIT_FIELD"
            if status == "FAMILY_UNSTABLE"
            else "HISTORICAL_EXACT_MOMENT"
        ),
        "records": [
            {
                "date": row["date"],
                "index": row["index"],
                "actual_branch": row["actual_branch"],
                "actual_family": row["actual_family"],
                "actual_lane": row["actual_lane"],
                "actual_motion": row["actual_motion"],
                "outgoing_flow": row["outgoing_flow"],
                "outgoing_transfer": row["outgoing_transfer"],
                "outgoing_sign_pattern": row["outgoing_sign_pattern"],
            }
            for row in rows
        ],
    }


def build_hierarchical_conditional_motion_memory(
    packets: list[SeatTaxonomyPacket],
    levels: tuple[int, ...] = (2, 3, 4, 5),
    min_sample: int = 3,
    family_threshold: float = 50.0,
    exact_threshold: float = 65.0,
    exact_proven_threshold: float = 80.0,
) -> dict[str, Any]:
    level_memories = [
        build_conditional_motion_memory(
            packets,
            level=level,
            min_sample=min_sample,
            family_threshold=family_threshold,
            exact_threshold=exact_threshold,
            exact_proven_threshold=exact_proven_threshold,
        )
        for level in levels
    ]
    all_scenarios: list[dict[str, Any]] = []
    for memory in level_memories:
        for scenario in memory["scenarios"]:
            row = dict(scenario)
            row["memory_level"] = memory["memory_level"]
            all_scenarios.append(row)

    level_summaries = [
        {
            "memory_level": memory["memory_level"],
            "total_cases": memory["total_cases"],
            "scenario_count": memory["scenario_count"],
            "status_counts": memory["status_counts"],
            "truth_authority_counts": memory["truth_authority_counts"],
            "live_use_counts": memory["live_use_counts"],
        }
        for memory in level_memories
    ]
    world_rows: list[dict[str, Any]] = []
    by_world: dict[str, list[dict[str, Any]]] = {}
    for scenario in all_scenarios:
        by_world.setdefault(scenario["condition"]["topology_name"], []).append(scenario)
    for topology_name, scenarios in by_world.items():
        world_rows.append(
            {
                "topology_name": topology_name,
                "scenario_count": len(scenarios),
                "appearance_count": sum(row["appearances"] for row in scenarios),
                "level_counts": dict(Counter(str(row["memory_level"]) for row in scenarios)),
                "status_counts": dict(Counter(row["memory_status"] for row in scenarios)),
                "truth_authority_counts": dict(
                    Counter(row["truth_authority"] for row in scenarios)
                ),
                "live_use_counts": dict(Counter(row["live_use"] for row in scenarios)),
                "top_scenarios": [
                    {
                        "memory_level": row["memory_level"],
                        "scenario_key": row["scenario_key"],
                        "appearances": row["appearances"],
                        "memory_status": row["memory_status"],
                        "truth_authority": row["truth_authority"],
                        "live_use": row["live_use"],
                        "primary_family": row["outcomes"]["primary_family"],
                        "primary_family_rate": row["outcomes"]["primary_family_rate"],
                        "primary_branch": row["outcomes"]["primary_branch"],
                        "primary_branch_rate": row["outcomes"]["primary_branch_rate"],
                    }
                    for row in sorted(
                        scenarios,
                        key=lambda item: (
                            item["memory_level"],
                            -item["appearances"],
                            item["scenario_key"],
                        ),
                    )[:12]
                ],
            }
        )
    world_rows.sort(key=lambda row: (-row["appearance_count"], row["topology_name"]))

    return {
        "rule": (
            "hierarchical conditional motion memory keeps every draw as evidence "
            "at multiple depths: broad world memory, motion memory, body memory, "
            "and exact moment memory"
        ),
        "levels": list(levels),
        "min_sample": min_sample,
        "family_threshold": family_threshold,
        "exact_threshold": exact_threshold,
        "exact_proven_threshold": exact_proven_threshold,
        "total_cases": level_memories[0]["total_cases"] if level_memories else 0,
        "skipped_boundary_draws": (
            level_memories[0]["skipped_boundary_draws"] if level_memories else 0
        ),
        "scenario_count": len(all_scenarios),
        "level_summaries": level_summaries,
        "status_counts": dict(Counter(row["memory_status"] for row in all_scenarios)),
        "truth_authority_counts": dict(
            Counter(row["truth_authority"] for row in all_scenarios)
        ),
        "live_use_counts": dict(Counter(row["live_use"] for row in all_scenarios)),
        "worlds": world_rows,
        "scenarios": all_scenarios,
    }


def build_conditional_motion_memory(
    packets: list[SeatTaxonomyPacket],
    level: int = 4,
    min_sample: int = 3,
    family_threshold: float = 50.0,
    exact_threshold: float = 65.0,
    exact_proven_threshold: float = 80.0,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    records: list[dict[str, Any]] = []
    skipped_boundary = 0
    for taxonomy_packet in sorted(
        packets,
        key=lambda item: item.to_payload()["draw"]["index"],
    ):
        case = conditional_motion_memory_case(taxonomy_packet.to_payload())
        if case is None:
            skipped_boundary += 1
            continue
        key = build_conditional_motion_memory_key(case, level=level)
        row = dict(case)
        row["conditional_memory_key"] = key
        grouped.setdefault(key, []).append(row)
        records.append(row)

    scenarios = [
        build_conditional_memory_scenario(
            key,
            rows,
            min_sample=min_sample,
            family_threshold=family_threshold,
            exact_threshold=exact_threshold,
            exact_proven_threshold=exact_proven_threshold,
        )
        for key, rows in grouped.items()
    ]
    scenarios.sort(
        key=lambda row: (
            row["condition"]["topology_name"],
            -row["appearances"],
            row["scenario_key"],
        )
    )

    world_rows: list[dict[str, Any]] = []
    by_world: dict[str, list[dict[str, Any]]] = {}
    for scenario in scenarios:
        by_world.setdefault(scenario["condition"]["topology_name"], []).append(scenario)
    for topology_name, world_scenarios in by_world.items():
        world_rows.append(
            {
                "topology_name": topology_name,
                "scenario_count": len(world_scenarios),
                "appearance_count": sum(row["appearances"] for row in world_scenarios),
                "status_counts": dict(
                    Counter(row["memory_status"] for row in world_scenarios)
                ),
                "live_use_counts": dict(Counter(row["live_use"] for row in world_scenarios)),
                "top_scenarios": [
                    {
                        "scenario_key": row["scenario_key"],
                        "appearances": row["appearances"],
                        "memory_status": row["memory_status"],
                        "live_use": row["live_use"],
                        "primary_family": row["outcomes"]["primary_family"],
                        "primary_family_rate": row["outcomes"]["primary_family_rate"],
                        "primary_branch": row["outcomes"]["primary_branch"],
                        "primary_branch_rate": row["outcomes"]["primary_branch_rate"],
                    }
                    for row in sorted(
                        world_scenarios,
                        key=lambda item: (-item["appearances"], item["scenario_key"]),
                    )[:10]
                ],
            }
        )
    world_rows.sort(key=lambda row: (-row["appearance_count"], row["topology_name"]))

    return {
        "rule": (
            "conditional motion memory stores how each live-safe world/scenario "
            "historically resolved without using the current row before it exists"
        ),
        "memory_level": level,
        "min_sample": min_sample,
        "family_threshold": family_threshold,
        "exact_threshold": exact_threshold,
        "exact_proven_threshold": exact_proven_threshold,
        "total_cases": len(records),
        "skipped_boundary_draws": skipped_boundary,
        "scenario_count": len(scenarios),
        "status_counts": dict(Counter(row["memory_status"] for row in scenarios)),
        "truth_authority_counts": dict(
            Counter(row["truth_authority"] for row in scenarios)
        ),
        "live_use_counts": dict(Counter(row["live_use"] for row in scenarios)),
        "worlds": world_rows,
        "scenarios": scenarios,
    }


def print_conditional_motion_memory(
    memory: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy Conditional Motion Memory")
    print("=" * 72)
    print(f"Total cases            {memory['total_cases']}")
    print(f"Boundary skipped       {memory['skipped_boundary_draws']}")
    print(f"Memory level           {memory['memory_level']}")
    print(f"Min sample             {memory['min_sample']}")
    print(f"Family threshold       {memory['family_threshold']}%")
    print(f"Exact promising        {memory['exact_threshold']}%")
    print(f"Exact proven           {memory['exact_proven_threshold']}%")
    print(f"Scenario count         {memory['scenario_count']}")
    print(f"Status counts          {memory['status_counts']}")
    print(f"Truth authority        {memory['truth_authority_counts']}")
    print(f"Live use counts        {memory['live_use_counts']}")
    print()
    worlds = memory["worlds"] if limit is None else memory["worlds"][:limit]
    for world in worlds:
        print(world["topology_name"])
        print(
            f"  appearances          {world['appearance_count']} | "
            f"scenarios={world['scenario_count']}"
        )
        print(f"  statuses             {world['status_counts']}")
        print(f"  live use             {world['live_use_counts']}")
        for scenario in world["top_scenarios"][:3]:
            print(
                "  room                 "
                f"n={scenario['appearances']} {scenario['memory_status']} "
                f"{scenario['live_use']} | family={scenario['primary_family']} "
                f"{scenario['primary_family_rate']}% | branch={scenario['primary_branch']} "
                f"{scenario['primary_branch_rate']}%"
            )
        print()


def print_hierarchical_conditional_motion_memory(
    memory: dict[str, Any],
    limit: int | None = 25,
) -> None:
    print("=" * 72)
    print("Seat Taxonomy Hierarchical Conditional Motion Memory")
    print("=" * 72)
    print(f"Total cases            {memory['total_cases']}")
    print(f"Boundary skipped       {memory['skipped_boundary_draws']}")
    print(f"Levels                 {memory['levels']}")
    print(f"Min sample             {memory['min_sample']}")
    print(f"Family threshold       {memory['family_threshold']}%")
    print(f"Exact promising        {memory['exact_threshold']}%")
    print(f"Exact proven           {memory['exact_proven_threshold']}%")
    print(f"Scenario count         {memory['scenario_count']}")
    print(f"Status counts          {memory['status_counts']}")
    print(f"Truth authority        {memory['truth_authority_counts']}")
    print(f"Live use counts        {memory['live_use_counts']}")
    print()
    print("Level summaries:")
    for summary in memory["level_summaries"]:
        print(
            f"  L{summary['memory_level']} scenarios={summary['scenario_count']} "
            f"statuses={summary['status_counts']}"
        )
    print()
    worlds = memory["worlds"] if limit is None else memory["worlds"][:limit]
    for world in worlds:
        print(world["topology_name"])
        print(
            f"  appearances          {world['appearance_count']} | "
            f"scenarios={world['scenario_count']} | levels={world['level_counts']}"
        )
        print(f"  truth                {world['truth_authority_counts']}")
        print(f"  live use             {world['live_use_counts']}")
        for scenario in world["top_scenarios"][:4]:
            print(
                "  room                 "
                f"L{scenario['memory_level']} n={scenario['appearances']} "
                f"{scenario['truth_authority']} {scenario['live_use']} | "
                f"family={scenario['primary_family']} "
                f"{scenario['primary_family_rate']}% | branch={scenario['primary_branch']} "
                f"{scenario['primary_branch_rate']}%"
            )
        print()


def format_motion_row(row: dict[str, Any]) -> str:
    motion = row["motion"]
    gauge = row["gauge"] if row["gauge"] is not None else "None"
    gauge_range = row["gauge_range"] if row["gauge_range"] is not None else "None"
    broad = row["broad_class"] if row["broad_class"] is not None else "None"
    return (
        f"{row['lane']} {row['role']} -> {row['sorted_seat']} "
        f"{format_delta(motion)} {broad} / {gauge} [{gauge_range}]"
    )


def print_seat_taxonomy_packets(packets: list[SeatTaxonomyPacket]) -> None:
    for taxonomy_packet in packets:
        payload = taxonomy_packet.to_payload()
        print("=" * 72)
        print("Seat Taxonomy Transition Physics")
        print("=" * 72)
        draw = payload["draw"]
        continuity = payload["continuity"]
        print(f"Date       : {draw['date']}")
        print(f"White Balls: {draw['white_balls']}")
        print(f"Sorted     : {draw['sorted_white_balls']}")
        print(
            "Continuity : "
            f"{continuity['previous_date']} -> "
            f"{continuity['current_date']} -> "
            f"{continuity['next_date'] or 'NONE'}"
        )
        print()
        doctrine = payload["doctrine"]
        print("Doctrine:")
        print(f"  {doctrine['law']}")
        print("  previous draw order -> current draw order -> outgoing contract -> next draw order -> sorted body result")
        print()
        transition = payload["draw_order_transition"]
        print("Draw Order Transition:")
        print(f"  previous_order      {transition['previous_draw_order']}")
        print(f"  current_order       {transition['current_draw_order']}")
        print(f"  next_order          {transition['next_draw_order']}")
        print(f"  incoming_delta      {transition['incoming_draw_delta']}")
        print(f"  outgoing_delta      {transition['outgoing_draw_delta']}")
        print(f"  incoming_sign       {transition['incoming_draw_sign']}")
        print(f"  outgoing_sign       {transition['outgoing_draw_sign']}")
        print(f"  incoming_family     {transition['incoming_draw_family']}")
        print(f"  outgoing_family     {transition['outgoing_draw_family']}")
        print(f"  dominant_incoming   {transition['dominant_incoming_draw_lane']} {format_delta(transition['dominant_incoming_draw_motion'])}")
        print(f"  dominant_outgoing   {transition['dominant_outgoing_draw_lane']} {format_delta(transition['dominant_outgoing_draw_motion'])}")
        print()
        face = payload["draw_order_face_identity"]
        print("Draw Order Face Identity:")
        print(f"  order_pattern       {face['order_pattern']}")
        print(f"  band_pattern        {face['draw_order_band_pattern']}")
        print(f"  transfer_pattern    {face['transfer_pattern']}")
        print(f"  sorted_path         {face['sorted_position_path']}")
        print(f"  direction_pattern   {face['direction_pattern']}")
        print(f"  turns               {face['turn_count']} {face['turn_lanes']}")
        print(f"  face_family         {face['face_family']}")
        print(f"  max_abs_lane        {face['max_abs_lane']}")
        print()
        print("Draw Order Taxonomy:")
        for lane in payload["draw_order_taxonomy"]["lanes"]:
            print(
                f"  {lane['draw_lane']} {lane['draw_role']}: {lane['number']} "
                f"{lane['draw_order_band']} -> {lane['mapped_sorted_seat']} | "
                f"in {format_delta(lane['incoming_motion'])} {lane['incoming_family']} | "
                f"out {format_delta(lane['outgoing_motion'])} {lane['outgoing_family']} | "
                f"transfer={lane['incoming_to_outgoing_transfer']}"
            )
        print()
        incoming = payload["incoming_motion"]
        print("Incoming Motion:")
        print(f"  sign_pattern     {incoming['sign_pattern']}")
        print(f"  total_abs_energy {incoming['total_abs_energy']}")
        print(
            "  dominant         "
            f"{incoming['dominant_lane']} -> {incoming['dominant_sorted_seat']} "
            f"{format_delta(incoming['dominant_motion'])}"
        )
        for row in incoming["lanes"]:
            print(f"  {format_motion_row(row)}")
        print()
        pressure = payload["current_pressure"]
        print("Current Pressure:")
        print(f"  set_health        {pressure['set_health']}")
        print(f"  set_relation      {pressure['set_relation']}")
        print(f"  middle_pressure   {pressure['middle_pressure']}")
        print(f"  edge_pressure     {pressure['edge_pressure']}")
        print(f"  pressure_fusion   {pressure['pressure_fusion_profile']}")
        print()
        origin = payload["pressure_origin"]
        print("Pressure Origin:")
        print(
            "  dominant          "
            f"{origin['dominant_origin_seat']} score={origin['dominant_origin_score']}"
        )
        print(
            "  smallest          "
            f"{origin['smallest_origin_seat']} score={origin['smallest_origin_score']}"
        )
        for row in origin["lanes"]:
            pieces = ", ".join(
                f"{item['origin']} +{item['contribution']}"
                for item in row["pressure_origins"]
                if item["contribution"] != 0
            )
            print(
                f"  {row['seat']} {row['role']}: "
                f"score={row['burden_score']} | "
                f"struct={row['structural_pressure']} dyn={row['dynamic_pressure']} "
                f"type={row['dominant_pressure_type']} | {pieces}"
            )
        print()
        burden = payload["lane_burden"]
        print("Lane Burden:")
        print(
            "  highest           "
            f"{burden['highest_burden_seat']} "
            f"{burden['highest_burden_level']} "
            f"{burden['highest_burden_state']} "
            f"score={burden['highest_burden_score']} "
            f"{burden['highest_burden_gauge']} [{burden['highest_burden_gauge_range']}]"
        )
        print(
            "  smallest          "
            f"{burden['smallest_burden_seat']} "
            f"{burden['smallest_burden_level']} "
            f"{burden['smallest_burden_state']} "
            f"score={burden['smallest_burden_score']} "
            f"{burden['smallest_burden_gauge']} [{burden['smallest_burden_gauge_range']}]"
        )
        for row in burden["lanes"]:
            print(
                f"  {row['seat']} {row['role']}: "
                f"{row['burden_level']} / {row['burden_state']} | "
                f"{row['burden_gauge']} [{row['burden_gauge_range']}] | "
                f"in {format_delta(row['incoming_motion'])} "
                f"{row['incoming_direction']} | "
                f"gap_pressure={row['adjacent_gap_pressure']} | "
                f"score={row['burden_score']}"
            )
        print()
        pressure_map = payload["pressure_map"]
        print("Pressure Map:")
        print(f"  dominant          {pressure_map['dominant_pressure_seat']}")
        print(
            f"  smallest/largest  "
            f"{pressure_map['smallest_pressure_seat']}={pressure_map['smallest_pressure_score']} "
            f"to {pressure_map['dominant_pressure_seat']}={pressure_map['dominant_pressure_score']}"
        )
        print(f"  shape             {pressure_map['pressure_shape']}")
        print(f"  burden_gauges     {pressure_map['burden_gauge_shape']}")
        print(f"  pressure_gauges   {pressure_map['pressure_gauge_shape']}")
        print(
            f"  type totals       structural={pressure_map['structural_pressure_total']} "
            f"dynamic={pressure_map['dynamic_pressure_total']} "
            f"{pressure_map['map_pressure_type']}"
        )
        print(f"  center            {pressure_map['pressure_center']}")
        print(f"  balance           {pressure_map['pressure_balance']}")
        print(f"  distribution      {pressure_map['pressure_distribution']}")
        world = pressure_map["pressure_world"]
        print(
            f"  world             {world['world_slot']} | "
            f"{world['topology_slot']} {world['topology_name']} | "
            f"{world['world_key']}"
        )
        for row in pressure_map["seats"]:
            print(
                f"  {row['seat']}: {row['pressure_level']} / "
                f"{row['pressure_role']} | in={format_delta(row['incoming_motion'])} | "
                f"gap={row['gap_pressure']} | L={row['left_gap']} R={row['right_gap']} | "
                f"pressure={row['pressure_gauge']} [{row['pressure_gauge_range']}] | "
                f"burden={row['burden_gauge']} [{row['burden_gauge_range']}] | "
                f"struct={row['structural_pressure']} dyn={row['dynamic_pressure']} "
                f"type={row['dominant_pressure_type']} | "
                f"modifier={row['middle_edge_modifier']} | score={row['burden_score']}"
            )
        print()
        authority = payload["pressure_authority"]
        print("Pressure Authority:")
        print(
            "  winner           "
            f"{authority['authority_winner_seat']} "
            f"{authority['authority_winner_origin']} "
            f"score={authority['authority_winner_score']}"
        )
        print(
            "  raw winner       "
            f"{authority['raw_pressure_winner_seat']} "
            f"score={authority['raw_pressure_winner_score']} "
            f"changed={authority['authority_changed_winner']}"
        )
        for row in authority["seats"]:
            print(
                f"  {row['seat']} {row['role']}: "
                f"raw={row['raw_pressure']} auth={row['authority_pressure']} "
                f"win={row['winning_origin']} "
                f"draw_lane={row['source_draw_lane']}"
            )
        print()
        bias = payload["resolution_bias"]
        print("Resolution Bias:")
        print(f"  bias              {bias['bias_type']}")
        print(
            "  primary           "
            f"{bias['primary_bias_seat']} {bias['primary_bias_family']}"
        )
        print(
            "  secondary         "
            f"{bias['secondary_bias_seat']} {bias['secondary_bias_family']}"
        )
        print(
            "  tertiary          "
            f"{bias['tertiary_bias_seat']} {bias['tertiary_bias_family']}"
        )
        print(f"  reason            {bias['bias_reason']}")
        print()
        ds = payload["draw_singularity_lens"]
        print("Draw Singularity Lens:")
        print(f"  family            {ds['draw_singularity']}")
        print(f"  subfamily         {ds['subfamily']}")
        print(f"  internal_profile  {ds['internal_profile']}")
        print(f"  branch_universe   {ds['branch_universe']}")
        print(f"  incoming_sorted   {ds['incoming_sorted_family_key']}")
        print(f"  outgoing_sorted   {ds['outgoing_sorted_family_key']}")
        print(f"  incoming_caste    {ds['incoming_draw_caste_side_pattern']}")
        print(f"  outgoing_caste    {ds['outgoing_draw_caste_side_pattern']}")
        collision = payload["collision_point"]
        if collision["finding_source"] != "NO_FINDING":
            print(
                "  finding           "
                f"{collision['finding_conflict_type']} | "
                f"primary {collision['finding_primary_seat']} "
                f"{collision['finding_primary_rate']}% | "
                f"secondary {collision['finding_secondary_seat']} "
                f"{collision['finding_secondary_rate']}% | "
                f"n={collision['finding_appearances']}"
            )
            print(
                "  active            "
                f"{'YES' if collision['used_branch_finding'] else 'NO'}"
        )
        print()
        preference = collision["pre_collision_preference_field"]
        print("Pre-Collision Preference:")
        print(f"  universe          {preference['preference_universe']}")
        print(f"  selection         {preference['selection_problem']}")
        if preference["preference_status"] == "HISTORICAL_FIELD":
            print(
                "  primary/secondary "
                f"{preference['primary_seat']} {preference['primary_rate']}% -> "
                f"{preference['secondary_seat']} {preference['secondary_rate']}% "
                f"gap={preference['branch_gap']} "
                f"{preference['split_strength']}"
            )
            family_read = ", ".join(
                f"{row['family']} {row['rate']}%"
                for row in preference["family_field"]
            )
            print(f"  family field      {family_read}")
        print(f"  read              {preference['read']}")
        print()
        selector = payload["branch_selector"]
        print("Branch Selector:")
        print(f"  result            {selector['selector_result']}")
        print(
            "  observed          "
            f"{selector['observed_branch_seat']} via {selector['observed_branch_lane']}"
        )
        print(
            "  selected          "
            f"{selector['selected_branch']} "
            f"confidence={selector['selected_branch_confidence']}"
        )
        print(f"  read              {selector['read']}")
        print()
        truth = payload["truth_control"]
        exact = truth["exact_branch_claim"]
        live_claims = truth["live_safe_claims"]
        print("Truth Control:")
        print(
            "  exact authority   "
            f"{exact['authority']}"
        )
        print(
            "  live world        "
            f"{live_claims['world']['topology_name']} "
            f"{live_claims['pressure_type']} "
            f"{live_claims['pressure_center']} "
            f"{live_claims['pressure_balance']} "
            f"{live_claims['pressure_distribution']}"
        )
        print(
            "  live authority    "
            f"{live_claims['authority_seat']} "
            f"{live_claims['authority_origin']}"
        )
        print(
            "  branch read       "
            f"{exact['collision_seat']} -> {exact['observed_outgoing_seat']} "
            f"{exact['validation_result']}"
        )
        print(f"  doctrine          {exact['doctrine']}")
        print()
        motion_state = payload["motion_state"]
        print("Motion State:")
        print(f"  motion_state      {motion_state['motion_state']}")
        print(f"  body_state        {motion_state['body_motion_state']}")
        print(f"  burden            {motion_state['dominant_burden_seat']} {motion_state['dominant_burden_level']} {motion_state['dominant_burden_state']}")
        print(f"  law_phrase        {motion_state['law_phrase']}")
        print()
        archetype = payload["motion_archetype"]
        print("Motion Archetype:")
        print(f"  archetype         {archetype['motion_archetype']}")
        print(
            "  inputs            "
            f"state={archetype['inputs']['motion_state']} "
            f"flow={archetype['inputs']['pressure_flow']} "
            f"transfer={archetype['inputs']['transfer']}"
        )
        print()
        collision = payload["collision_point"]
        print("Collision Point:")
        print(f"  status            {collision['collision_status']}")
        print(
            "  authority         "
            f"{collision['authority_seat']} "
            f"{collision['authority_origin']} "
            f"score={collision['authority_score']}"
        )
        print(
            "  collision         "
            f"{collision['collision_seat']} {collision['collision_zone']} "
            f"{collision['collision_type']}"
        )
        print(
            "  baseline          "
            f"{collision['baseline_collision_seat']} "
            f"{collision['baseline_collision_type']}"
        )
        print(
            "  expected/observed "
            f"{collision['expected_draw_lane']} -> "
            f"{collision['observed_draw_lane']} "
            f"{collision['observed_sorted_seat']}"
        )
        print(
            "  validation        "
            f"{collision['validation_result']} | "
            f"seat={collision['collision_seat_validation']} | "
            f"lane={collision['collision_lane_validation']}"
        )
        print(f"  reason            {collision['collision_reason']}")
        print()
        address = payload["technical_draw_address"]
        print("Technical Draw Address:")
        print(f"  {address['technical_draw_address']}")
        print()
        effect = payload["incoming_body_effect"]
        print("Incoming Body Effect:")
        print(f"  effect            {effect['effect']}")
        print(
            "  target            "
            f"{effect['dominant_lane']} -> {effect['dominant_sorted_seat']} "
            f"zone={effect['seat_zone']} direction={effect['direction']}"
        )
        print()
        contract = payload["outgoing_contract"]
        print("Outgoing Contract:")
        print(f"  status            {contract['contract_status']}")
        print(f"  family            {contract['family']}")
        print(f"  sign_pattern      {contract['sign_pattern']}")
        print(f"  flow              {contract['flow']}")
        print(f"  transfer          {contract['transfer']}")
        print(f"  energy            {contract['energy']} {contract.get('energy_class')}")
        print(
            "  dominant          "
            f"{contract['dominant_lane']} -> {contract['dominant_sorted_seat']} "
            f"{format_delta(contract.get('dominant_motion'))}"
        )
        print()
        law = payload["motion_law_candidate"]
        print("Motion Law Candidate:")
        print(f"  candidate         {law['candidate']}")
        print(f"  status            {law['status']}")
        print()
        validation = payload["origin_weight_validation"]
        print("Origin Weight Validation:")
        print(f"  result            {validation['validation_result']}")
        print(
            "  origin->out       "
            f"{validation['dominant_origin_seat']} "
            f"score={validation['dominant_origin_score']} "
            f"-> {validation['dominant_outgoing_lane']} "
            f"{validation['dominant_outgoing_sorted_seat']}"
        )
        print(
            "  totals            "
            f"structural={validation['structural_pressure_total']} "
            f"dynamic={validation['dynamic_pressure_total']} "
            f"{validation['pressure_type_total']}"
        )
        print(f"  read              {validation['debug_read']}")
        print()
        next_body = payload["next_technical_body"]
        print("Next Technical Body:")
        if next_body is None:
            print("  NONE")
        else:
            print(f"  date              {next_body['date']}")
            print(f"  set_health        {next_body['set_health']}")
            print(f"  technical         {next_body['technical_signature']}")
        print()
        print("Sorted Result Body / Seat Taxonomy:")
        for seat in payload["sorted_result_body"]["seats"]:
            left = seat["left_relation"]["class"] if seat["left_relation"] else "START"
            right = seat["right_relation"]["class"] if seat["right_relation"] else "END"
            print(
                f"  {seat['seat']} {seat['role']}: {seat['number']} "
                f"{seat['taxonomy']} | zone={seat['zone']} | left={left} | right={right}"
            )
        print("-" * 72)


def print_pressure_world_catalog() -> None:
    worlds = iter_pressure_world_catalog()
    print("=" * 72)
    print("Seat Taxonomy Pressure Worlds")
    print("=" * 72)
    print("Base Worlds:")
    for pressure_type in PRESSURE_WORLD_TYPES:
        print(f"  {pressure_type}")
    print()
    print("Topology Worlds:")
    topology_seen: set[str] = set()
    for world in worlds:
        topology_key = world["topology_key"]
        if topology_key in topology_seen:
            continue
        topology_seen.add(topology_key)
        variants = [
            item for item in worlds
            if item["topology_key"] == topology_key
        ]
        variant_text = ", ".join(
            f"{item['pressure_balance']}={item['world_slot']}"
            for item in variants
        )
        print(
            f"  {world['topology_slot']} {world['topology_name']} | "
            f"{topology_key} | "
            f"balance variants: {variant_text}"
        )
    print()
    print(f"Exact world slots: {len(worlds)}")
    print("Naming status: topology named; exact world slots remain numeric.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Seat Taxonomy",
        description=(
            "Read IIW motion as transition physics: current sorted body, incoming "
            "motion, current pressure, body effect, and outgoing motion contract."
        ),
    )
    parser.add_argument(
        "--csv-path",
        type=Path,
        default=DEFAULT_CSV_PATH,
        help="Path to the Powerball history CSV.",
    )
    parser.add_argument(
        "--from-date",
        default=TRUSTED_DRAW_ORDER_START_DATE.isoformat(),
        help="Optional start date. Defaults to trusted draw-order start 2015-10-07.",
    )
    parser.add_argument(
        "--to-date",
        help="Optional end date, for example 2026-06-17 or 6/17/2026.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "Number of packets to print after date filtering. Defaults to 1 for "
            "packet output. With --collision-laws or --collision-law-audit, "
            "limits displayed law rows only."
        ),
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Use the latest rows in the selected date window.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print Seat Taxonomy packets as JSON.",
    )
    parser.add_argument(
        "--list-pressure-worlds",
        action="store_true",
        help="Print the unnamed pressure-world naming catalog and exit.",
    )
    parser.add_argument(
        "--collision-laws",
        action="store_true",
        help="Aggregate historical collision-law validation for the selected date window.",
    )
    parser.add_argument(
        "--collision-law-audit",
        action="store_true",
        help="Classify collision-law groups as proven, promising, unstable, failed, or low sample.",
    )
    parser.add_argument(
        "--branch-selector-audit",
        action="store_true",
        help="Learn which branch wins inside each pre-collision preference field.",
    )
    parser.add_argument(
        "--world-accuracy-audit",
        action="store_true",
        help="Audit which discriminator fields improve branch accuracy inside each topology world.",
    )
    parser.add_argument(
        "--walk-forward-audit",
        action="store_true",
        help="Prior-only branch audit using live-safe current-draw keys.",
    )
    parser.add_argument(
        "--family-first-walk-forward-audit",
        action="store_true",
        help="Prior-only audit that predicts family first and calls exact branch only when proven enough.",
    )
    parser.add_argument(
        "--conditional-motion-memory",
        action="store_true",
        help="Build the historical conditional motion memory library by live-safe world/scenario.",
    )
    parser.add_argument(
        "--hierarchical-conditional-motion-memory",
        action="store_true",
        help="Build Conditional Motion Memory across levels 2-5 so one-off exact rooms remain evidence.",
    )
    parser.add_argument(
        "--collision-law-level",
        type=int,
        choices=(1, 2, 3, 4),
        default=4,
        help=(
            "Collision law grouping width: 1 broad topology+authority, "
            "2 adds state/transfer, 3 adds collision type, 4 adds exact world balance."
        ),
    )
    parser.add_argument(
        "--branch-selector-level",
        type=int,
        choices=(1, 2, 3, 4, 5),
        default=3,
        help=(
            "Branch selector grouping width: 1 broad universe+topology+authority, "
            "2 adds pressure world, 3 adds burden/incoming/face, 4 adds body anatomy, "
            "5 uses the Draw Singularity family/subfamily/internal-profile lens."
        ),
    )
    parser.add_argument(
        "--walk-forward-level",
        type=int,
        choices=(1, 2, 3, 4),
        default=3,
        help=(
            "Walk-forward key width: 1 topology, 2 adds live-safe world+authority, "
            "3 adds incoming sign/lane/face, 4 adds pressure shape/body."
        ),
    )
    parser.add_argument(
        "--conditional-memory-level",
        type=int,
        choices=(1, 2, 3, 4, 5),
        default=2,
        help=(
            "Conditional memory key width: 1 topology, 2 adds live-safe world+authority, "
            "3 adds incoming/face, 4 adds pressure body, 5 adds fusion/burden/turns."
        ),
    )
    parser.add_argument(
        "--walk-forward-min-sample",
        type=int,
        default=3,
        help="Minimum prior same-key cases required before making a branch call.",
    )
    parser.add_argument(
        "--family-first-threshold",
        type=float,
        default=50.0,
        help="Minimum prior family rate required before making a family call.",
    )
    parser.add_argument(
        "--exact-branch-threshold",
        type=float,
        default=65.0,
        help="Minimum prior exact branch rate inside the predicted family before making an exact branch call.",
    )
    parser.add_argument(
        "--exact-proven-threshold",
        type=float,
        default=80.0,
        help="Exact branch rate required for Conditional Motion Memory to mark an exact room proven.",
    )
    parser.add_argument(
        "--use-resolution-bias",
        action="store_true",
        help="Use resolution_bias primary seat as the collision proposal instead of diagnostic-only mode.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        raise ValueError("--limit must be at least 1.")

    if args.list_pressure_worlds:
        print_pressure_world_catalog()
        return

    from_date = parse_draw_date(args.from_date) if args.from_date else None
    to_date = parse_draw_date(args.to_date) if args.to_date else None
    if from_date and to_date and to_date < from_date:
        raise ValueError("--to-date must be the same as or later than --from-date.")

    draws = load_historical_draws(args.csv_path)
    packet_limit = (
        None
        if (
            args.collision_laws
            or args.collision_law_audit
            or args.branch_selector_audit
            or args.world_accuracy_audit
            or args.walk_forward_audit
            or args.family_first_walk_forward_audit
            or args.conditional_motion_memory
            or args.hierarchical_conditional_motion_memory
        )
        else args.limit
    )
    if (
        packet_limit is None
        and not args.collision_laws
        and not args.collision_law_audit
        and not args.branch_selector_audit
        and not args.world_accuracy_audit
        and not args.walk_forward_audit
        and not args.family_first_walk_forward_audit
        and not args.conditional_motion_memory
        and not args.hierarchical_conditional_motion_memory
    ):
        packet_limit = 1
    packets = build_seat_taxonomy_packets(
        draws,
        from_date=from_date,
        to_date=to_date,
        limit=packet_limit,
        latest=args.latest,
        use_resolution_bias=args.use_resolution_bias,
    )

    if args.collision_laws:
        report = build_collision_law_report(
            packets,
            level=args.collision_law_level,
        )
        if args.json:
            print(json.dumps(report, indent=2))
            return
        print_collision_law_report(report, limit=args.limit or 25)
        return

    if args.collision_law_audit:
        audit = build_collision_law_audit(
            packets,
            level=args.collision_law_level,
        )
        if args.json:
            print(json.dumps(audit, indent=2))
            return
        print_collision_law_audit(audit, limit=args.limit or 25)
        return

    if args.branch_selector_audit:
        audit = build_branch_selector_audit(
            packets,
            level=args.branch_selector_level,
        )
        if args.json:
            print(json.dumps(audit, indent=2))
            return
        print_branch_selector_audit(audit, limit=args.limit or 25)
        return

    if args.world_accuracy_audit:
        audit = build_world_accuracy_audit(packets)
        if args.json:
            print(json.dumps(audit, indent=2))
            return
        print_world_accuracy_audit(audit, limit=args.limit or 25)
        return

    if args.walk_forward_audit:
        if args.walk_forward_min_sample < 1:
            raise ValueError("--walk-forward-min-sample must be at least 1.")
        audit = build_walk_forward_audit(
            packets,
            level=args.walk_forward_level,
            min_sample=args.walk_forward_min_sample,
        )
        if args.json:
            print(json.dumps(audit, indent=2))
            return
        print_walk_forward_audit(audit, limit=args.limit or 25)
        return

    if args.family_first_walk_forward_audit:
        if args.walk_forward_min_sample < 1:
            raise ValueError("--walk-forward-min-sample must be at least 1.")
        audit = build_family_first_walk_forward_audit(
            packets,
            level=args.walk_forward_level,
            min_sample=args.walk_forward_min_sample,
            family_threshold=args.family_first_threshold,
            exact_threshold=args.exact_branch_threshold,
            exact_proven_threshold=args.exact_proven_threshold,
        )
        if args.json:
            print(json.dumps(audit, indent=2))
            return
        print_family_first_walk_forward_audit(audit, limit=args.limit or 25)
        return

    if args.conditional_motion_memory:
        if args.walk_forward_min_sample < 1:
            raise ValueError("--walk-forward-min-sample must be at least 1.")
        memory = build_conditional_motion_memory(
            packets,
            level=args.conditional_memory_level,
            min_sample=args.walk_forward_min_sample,
            family_threshold=args.family_first_threshold,
            exact_threshold=args.exact_branch_threshold,
        )
        if args.json:
            print(json.dumps(memory, indent=2))
            return
        print_conditional_motion_memory(memory, limit=args.limit or 25)
        return

    if args.hierarchical_conditional_motion_memory:
        if args.walk_forward_min_sample < 1:
            raise ValueError("--walk-forward-min-sample must be at least 1.")
        memory = build_hierarchical_conditional_motion_memory(
            packets,
            levels=(2, 3, 4, 5),
            min_sample=args.walk_forward_min_sample,
            family_threshold=args.family_first_threshold,
            exact_threshold=args.exact_branch_threshold,
            exact_proven_threshold=args.exact_proven_threshold,
        )
        if args.json:
            print(json.dumps(memory, indent=2))
            return
        print_hierarchical_conditional_motion_memory(memory, limit=args.limit or 25)
        return

    if args.json:
        print(json.dumps([packet.to_payload() for packet in packets], indent=2))
        return

    print_seat_taxonomy_packets(packets)


if __name__ == "__main__":
    main()
