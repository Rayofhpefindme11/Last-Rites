from __future__ import annotations

import argparse
import csv
import json
import math
import os
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterator


WHITE_BALL_COUNT = 5
WHITE_BALL_MIN = 1
WHITE_BALL_MAX = 69
POWERBALL_MIN = 1
POWERBALL_MAX = 39
SET_STYLE_CONNECTION_LIMIT = 10
TRUSTED_DRAW_ORDER_START_DATE = date(2015, 10, 7)
ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_CSV_PATH = Path(
    os.environ.get("IIW_POWERBALL_CSV", ROOT_DIR / "Powerball records" / "PB_All.csv")
)
NUMBER_BANDS: tuple[tuple[range, str], ...] = (
    (range(1, 3), "Air"),
    (range(3, 5), "sky"),
    (range(5, 7), "light"),
    (range(7, 9), "feather"),
    (range(9, 11), "Life"),
    (range(11, 13), "Greed"),
    (range(13, 15), "Gravity"),
    (range(15, 17), "nova"),
    (range(17, 19), "Star"),
    (range(19, 21), "Polar"),
    (range(21, 23), "Water"),
    (range(23, 25), "Ying"),
    (range(25, 27), "yang"),
    (range(27, 29), "Dark"),
    (range(29, 31), "Volt"),
    (range(31, 33), "tree"),
    (range(33, 35), "leaf"),
    (range(35, 37), "beach"),
    (range(37, 39), "stem"),
    (range(39, 41), "truth"),
    (range(41, 43), "lie"),
    (range(43, 45), "red"),
    (range(45, 47), "blue"),
    (range(47, 49), "green"),
    (range(49, 51), "jester"),
    (range(51, 53), "king"),
    (range(53, 55), "knight"),
    (range(55, 57), "pope"),
    (range(57, 59), "emperor"),
    (range(59, 61), "prince"),
    (range(61, 63), "high king"),
    (range(63, 65), "high queen"),
    (range(65, 67), "noble Prince"),
    (range(67, 69), "high priest"),
    (range(69, 71), "monarch"),
)
GAP_ALPHABET: tuple[tuple[range, str], ...] = (
    (range(1, 3), "A"),
    (range(3, 5), "B"),
    (range(5, 7), "C"),
    (range(7, 9), "D"),
    (range(9, 11), "E"),
    (range(11, 13), "F"),
    (range(13, 15), "G"),
    (range(15, 17), "H"),
    (range(17, 19), "I"),
    (range(19, 21), "J"),
    (range(21, 23), "K"),
    (range(23, 25), "L"),
    (range(25, 27), "M"),
    (range(27, 29), "N"),
    (range(29, 31), "O"),
    (range(31, 33), "P"),
    (range(33, 35), "Q"),
    (range(35, 37), "R"),
    (range(37, 39), "S"),
    (range(39, 41), "T"),
    (range(41, 43), "U"),
    (range(43, 45), "V"),
    (range(45, 47), "W"),
    (range(47, 49), "X"),
    (range(49, 51), "Y"),
    (range(51, 53), "Z"),
    (range(53, 55), "Aa"),
    (range(55, 57), "bb"),
    (range(57, 59), "cc"),
    (range(59, 61), "dd"),
    (range(61, 63), "ee"),
    (range(63, 65), "ff"),
    (range(65, 67), "gg"),
    (range(67, 69), "hh"),
    (range(69, 71), "ii"),
)
PRESSURE_ROMAN_35: tuple[tuple[range, str], ...] = (
    (range(1, 3), "I"),
    (range(3, 5), "II"),
    (range(5, 7), "III"),
    (range(7, 9), "IV"),
    (range(9, 11), "V"),
    (range(11, 13), "VI"),
    (range(13, 15), "VII"),
    (range(15, 17), "VIII"),
    (range(17, 19), "IX"),
    (range(19, 21), "X"),
    (range(21, 23), "XI"),
    (range(23, 25), "XII"),
    (range(25, 27), "XIII"),
    (range(27, 29), "XIV"),
    (range(29, 31), "XV"),
    (range(31, 33), "XVI"),
    (range(33, 35), "XVII"),
    (range(35, 37), "XVIII"),
    (range(37, 39), "XIX"),
    (range(39, 41), "XX"),
    (range(41, 43), "XXI"),
    (range(43, 45), "XXII"),
    (range(45, 47), "XXIII"),
    (range(47, 49), "XXIV"),
    (range(49, 51), "XXV"),
    (range(51, 53), "XXVI"),
    (range(53, 55), "XXVII"),
    (range(55, 57), "XXVIII"),
    (range(57, 59), "XXIX"),
    (range(59, 61), "XXX"),
    (range(61, 63), "XXXI"),
    (range(63, 65), "XXXII"),
    (range(65, 67), "XXXIII"),
    (range(67, 69), "XXXIV"),
    (range(69, 71), "XXXV"),
)
OLYMPUS_APEX_CLASSES: tuple[str, ...] = (
    "Zeus",
    "Hera",
    "Poseidon",
    "Demeter",
    "Athena",
    "Apollo",
    "Artemis",
    "Ares",
    "Aphrodite",
    "Hephaestus",
    "Hermes",
    "Dionysus",
)
RELATION_CLASSES: tuple[tuple[range, str], ...] = (
    (range(1, 3), "BABE"),
    (range(3, 5), "KID"),
    (range(5, 7), "TEEN"),
    (range(7, 9), "GRUNT"),
    (range(9, 11), "MENOUS"),
    (range(11, 13), "GRANDE"),
    (range(13, 15), "GALLEON"),
    (range(15, 17), "FIGHTER"),
    (range(17, 19), "ARCHER"),
    (range(19, 21), "HARBINGER"),
    (range(21, 23), "WRESTLER"),
    (range(23, 25), "FIGHTER_HIGH"),
    (range(25, 27), "HOLLOW"),
    (range(27, 29), "BRAGA"),
    (range(29, 31), "KILLER"),
    (range(31, 33), "ARRANCAR"),
    (range(33, 35), "CERO"),
    (range(35, 37), "EXT_LOW_ENDPOINT_GRUNT"),
    (range(37, 39), "EXT_LOW_ENDPOINT_HEALER"),
    (range(39, 41), "EXT_LOW_ENDPOINT_HELPER"),
    (range(41, 43), "EXT_LOW_ENDPOINT_CREATOR"),
    (range(43, 45), "EXT_LOW_ENDPOINT_DAECON"),
    (range(45, 47), "EXT_LOW_ENDPOINT_WRAITH"),
    (range(47, 49), "LOW_ENDPOINT_GRUNT"),
    (range(49, 51), "LOW_ENDPOINT_SOLDIER"),
    (range(51, 53), "LOW_ENDPOINT_LEADER"),
    (range(53, 55), "LOW_ENDPOINT_CHIEF"),
    (range(55, 57), "LOW_ENDPOINT_GOD"),
    (range(57, 59), "MID_ENDPOINT_WAR_CHIEF"),
    (range(59, 61), "MID_ENDPOINT_NOBLE"),
    (range(61, 63), "MID_ENDPOINT_GREAT_NOBLE"),
    (range(63, 65), "HIGH_ENDPOINT_EMPEROR"),
    (range(65, 67), "HIGH_ENDPOINT_KING"),
    (range(67, 69), "HIGH_ENDPOINT_HIGH_KING"),
    (range(69, 71), "HIGH_ENDPOINT_MONARCH"),
)
MOTION_GAUGE_CLASSES: tuple[tuple[range, str], ...] = (
    (range(1, 3), "grunt"),
    (range(3, 5), "peasant"),
    (range(5, 7), "medic"),
    (range(7, 9), "noble"),
    (range(9, 11), "noble medic"),
    (range(11, 13), "Herald"),
    (range(13, 15), "fighter"),
    (range(15, 17), "Herald fighter"),
    (range(17, 19), "brawler"),
    (range(19, 21), "Scrappy Brawler"),
    (range(21, 23), "grand brawler"),
    (range(23, 25), "healer"),
    (range(25, 27), "sacred healer"),
    (range(27, 29), "true healer"),
    (range(29, 31), "queen"),
    (range(31, 33), "False queen"),
    (range(33, 35), "lost queen"),
    (range(35, 37), "King"),
    (range(37, 39), "true king"),
    (range(39, 41), "High king"),
    (range(41, 43), "Monarch"),
    (range(43, 45), "Dark king"),
    (range(45, 47), "dark queen"),
    (range(47, 49), "dark prince"),
    (range(49, 51), "dark monarch"),
    (range(51, 53), "dark princess"),
    (range(53, 55), "dark emperor"),
    (range(55, 57), "dark priest"),
    (range(57, 59), "dark priestess"),
    (range(59, 61), "Light queen"),
    (range(61, 63), "light king"),
    (range(63, 65), "light hero"),
    (range(65, 67), "dark hero"),
    (range(67, 69), "light monarch"),
    (range(69, 71), "light empresses"),
)
MOTION_BROAD_CLASSES: tuple[tuple[range, str], ...] = (
    (range(1, 11), "Light Motion"),
    (range(11, 21), "Calm Motion"),
    (range(21, 31), "Directed Motion"),
    (range(31, 41), "Transitional Motion"),
    (range(41, 51), "Crest Echo Motion"),
    (range(51, 61), "Fatigued Motion"),
    (range(61, 70), "Chaotic Motion"),
)
PATH_ENERGY_SPECTRUM_CLASSES: tuple[tuple[range, str], ...] = (
    (range(1, 3), "Infrared"),
    (range(3, 5), "Deep Red"),
    (range(5, 7), "Red"),
    (range(7, 9), "Scarlet"),
    (range(9, 11), "Vermilion"),
    (range(11, 13), "Red Orange"),
    (range(13, 15), "Orange"),
    (range(15, 17), "Amber"),
    (range(17, 19), "Gold"),
    (range(19, 21), "Yellow"),
    (range(21, 23), "Lemon"),
    (range(23, 25), "Chartreuse"),
    (range(25, 27), "Yellow Green"),
    (range(27, 29), "Green"),
    (range(29, 31), "Emerald"),
    (range(31, 33), "Spring Green"),
    (range(33, 35), "Mint"),
    (range(35, 37), "Aqua"),
    (range(37, 39), "Cyan"),
    (range(39, 41), "Sky Blue"),
    (range(41, 43), "Azure"),
    (range(43, 45), "Blue"),
    (range(45, 47), "Royal Blue"),
    (range(47, 49), "Indigo"),
    (range(49, 51), "Deep Indigo"),
    (range(51, 53), "Violet"),
    (range(53, 55), "Deep Violet"),
    (range(55, 57), "Purple"),
    (range(57, 59), "Lavender"),
    (range(59, 61), "Magenta"),
    (range(61, 63), "Rose"),
    (range(63, 65), "Prism White"),
    (range(65, 67), "Ultraviolet"),
    (range(67, 69), "Deep Ultraviolet"),
    (range(69, 71), "Apex Violet"),
)
FLOW_STRENGTH_ELEMENT_CLASSES: tuple[tuple[range, str], ...] = (
    (range(1, 3), "Hydrogen"),
    (range(3, 5), "Helium"),
    (range(5, 7), "Lithium"),
    (range(7, 9), "Beryllium"),
    (range(9, 11), "Boron"),
    (range(11, 13), "Carbon"),
    (range(13, 15), "Nitrogen"),
    (range(15, 17), "Oxygen"),
    (range(17, 19), "Fluorine"),
    (range(19, 21), "Neon"),
    (range(21, 23), "Sodium"),
    (range(23, 25), "Magnesium"),
    (range(25, 27), "Aluminum"),
    (range(27, 29), "Silicon"),
    (range(29, 31), "Phosphorus"),
    (range(31, 33), "Sulfur"),
    (range(33, 35), "Chlorine"),
    (range(35, 37), "Argon"),
    (range(37, 39), "Potassium"),
    (range(39, 41), "Calcium"),
    (range(41, 43), "Scandium"),
    (range(43, 45), "Titanium"),
    (range(45, 47), "Vanadium"),
    (range(47, 49), "Chromium"),
    (range(49, 51), "Manganese"),
    (range(51, 53), "Iron"),
    (range(53, 55), "Cobalt"),
    (range(55, 57), "Nickel"),
    (range(57, 59), "Copper"),
    (range(59, 61), "Zinc"),
    (range(61, 63), "Gallium"),
    (range(63, 65), "Germanium"),
    (range(65, 67), "Arsenic"),
    (range(67, 69), "Selenium"),
    (range(69, 71), "Bromine"),
)
PRESSURE_FUSION_CONSTELLATIONS: dict[str, str] = {
    "MATCHED_FUSION": "Orion",
    "TYPE_FUSION": "Lyra",
    "FAMILY_FUSION": "Cygnus",
    "REDISTRIBUTED_FUSION": "Draco",
    "INVERTED_FUSION": "Phoenix",
}
PRESSURE_SHAPE_TYPES: dict[str, str] = {
    "----": "RESET",
    "---+": "DOWNFALL",
    "--+-": "YIELD",
    "--++": "NEUTRAL",
    "-+--": "PRESSED",
    "-+-+": "SEPERATION",
    "-++-": "FLOW",
    "-+++": "EXPANSION",
    "+---": "CRISIS",
    "+--+": "STRETCH",
    "+-+-": "COMPLUSION",
    "+-++": "TENSION",
    "++-+": "LINK",
    "++--": "STILLNESS",
    "+++-": "SURGE",
    "++++": "UPLIFT",
}
SET_HEALTH_TONES: dict[str, str] = {
    "RESET": "Resetting",
    "DOWNFALL": "Downfall",
    "YIELD": "Yielding",
    "NEUTRAL": "Neutral",
    "PRESSED": "Pressed",
    "SEPERATION": "Seperating",
    "FLOW": "Flowing",
    "EXPANSION": "Expanding",
    "CRISIS": "Crisis",
    "STRETCH": "Stretching",
    "COMPLUSION": "Complusion",
    "TENSION": "Tensioned",
    "LINK": "Linking",
    "STILLNESS": "Still",
    "SURGE": "Surging",
    "UPLIFT": "Uplifting",
}
INVERTED_PRESSURE_SHAPE_PAIRS: frozenset[frozenset[str]] = frozenset(
    {
        frozenset(("RESET", "UPLIFT")),
        frozenset(("DOWNFALL", "SURGE")),
        frozenset(("NEUTRAL", "STILLNESS")),
        frozenset(("EXPANSION", "CRISIS")),
    }
)
SORTED_LANES: tuple[tuple[str, str, int, int], ...] = (
    ("S1", "Core", 1, 65),
    ("S2", "Entry", 2, 66),
    ("S3", "Bridge", 3, 67),
    ("S4", "Exit", 4, 68),
    ("S5", "Endpoint", 5, 69),
)
DRAW_LANES: tuple[tuple[str, str, int, int], ...] = (
    ("D1", "starter", WHITE_BALL_MIN, WHITE_BALL_MAX),
    ("D2", "hold", WHITE_BALL_MIN, WHITE_BALL_MAX),
    ("D3", "stability", WHITE_BALL_MIN, WHITE_BALL_MAX),
    ("D4", "control", WHITE_BALL_MIN, WHITE_BALL_MAX),
    ("D5", "ender", WHITE_BALL_MIN, WHITE_BALL_MAX),
)


@dataclass(frozen=True)
class HistoricalDraw:
    draw_date: date
    draw_index: int
    jackpot_usd: int | None
    white_balls: tuple[int, int, int, int, int]
    powerball: int
    powerplay: int | None

    @property
    def sorted_white_balls(self) -> tuple[int, int, int, int, int]:
        return tuple(sorted(self.white_balls))  # type: ignore[return-value]

    def to_payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["draw_date"] = self.draw_date.isoformat()
        payload["white_balls"] = list(self.white_balls)
        payload["sorted_white_balls"] = list(self.sorted_white_balls)
        return payload


@dataclass(frozen=True)
class LaneForm:
    lane: str
    role: str
    number: int
    number_band: str
    allowed_start: int
    allowed_end: int
    in_lane_range: bool

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DrawMotion:
    lane: str
    role: str
    incoming_motion: int | None
    incoming_motion_class: str | None
    incoming_motion_gauge: str | None
    incoming_motion_gauge_range: str | None
    outgoing_motion: int | None
    outgoing_motion_class: str | None
    outgoing_motion_gauge: str | None
    outgoing_motion_gauge_range: str | None

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DrawStepMotion:
    lane: str
    role: str
    from_lane: str
    from_role: str
    from_number: int
    to_number: int
    distance: int

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GapForm:
    section: str
    from_lane: str
    to_lane: str
    from_number: int
    to_number: int
    distance: int
    gap: int
    gap_letter: str
    gap_range: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SetRelation:
    section: str
    relation: str
    from_lane: str
    to_lane: str
    from_role: str
    to_role: str
    from_number: int
    to_number: int
    distance: int
    gap: int
    gap_letter: str
    gap_range: str
    relation_class: str
    relation_class_range: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SetStyleGroup:
    group_style: str
    start_lane: str
    end_lane: str
    lanes: tuple[str, ...]
    numbers: tuple[int, ...]
    size: int

    def to_payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["lanes"] = list(self.lanes)
        payload["numbers"] = list(self.numbers)
        return payload


@dataclass(frozen=True)
class SetStyle:
    section: str
    set_style: str
    set_signature: str
    connection_rule: str
    connected_pattern: str
    group_signature: str
    groups: tuple[SetStyleGroup, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "section": self.section,
            "set_style": self.set_style,
            "set_signature": self.set_signature,
            "connection_rule": self.connection_rule,
            "connected_pattern": self.connected_pattern,
            "group_signature": self.group_signature,
            "groups": [group.to_payload() for group in self.groups],
        }


@dataclass(frozen=True)
class DrawStyleTransferStep:
    draw_lane: str
    draw_role: str
    draw_number: int
    sorted_lane: str
    sorted_role: str
    sorted_position: int

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DrawStyle:
    section: str
    draw_style: str
    draw_style_family: str
    rule: str
    direction_pattern: str
    transfer_pattern: str
    sorted_position_path: tuple[int, ...]
    sorted_position_deltas: tuple[int, ...]
    sorted_position_energy: int
    turn_count: int
    turn_lanes: tuple[str, ...]
    steps: tuple[DrawStyleTransferStep, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "section": self.section,
            "draw_style": self.draw_style,
            "draw_style_family": self.draw_style_family,
            "rule": self.rule,
            "direction_pattern": self.direction_pattern,
            "transfer_pattern": self.transfer_pattern,
            "sorted_position_path": list(self.sorted_position_path),
            "sorted_position_deltas": list(self.sorted_position_deltas),
            "sorted_position_energy": self.sorted_position_energy,
            "turn_count": self.turn_count,
            "turn_lanes": list(self.turn_lanes),
            "steps": [step.to_payload() for step in self.steps],
        }


@dataclass(frozen=True)
class SortedPressure:
    pressure_shape: str
    pressure_type: str
    set_arc: str
    set_arc_35: str
    set_arc_family: str
    set_arc_type: str
    sorted_style: str
    fp: int
    total: int
    edge_pressure: int
    middle_pressure: int
    middle_minus_edge: int
    largest_gap: int
    largest_gap_relation: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DrawPressure:
    pressure_shape: str
    pressure_type: str
    set_arc: str
    set_arc_35: str
    set_arc_family: str
    set_arc_type: str
    draw_style: str
    draw_style_family: str
    direction_pattern: str
    transfer_pattern: str
    draw_path_energy: int
    draw_path_energy_average: float
    draw_path_energy_class: str
    draw_path_energy_spectrum: str
    draw_path_energy_spectrum_range: str
    draw_path_energy_gauge: str
    draw_path_energy_gauge_range: str
    sorted_position_energy: int
    incoming_energy: int | None
    incoming_energy_average: float | None
    incoming_energy_class: str | None
    incoming_energy_gauge: str | None
    incoming_energy_gauge_range: str | None
    outgoing_energy: int | None
    outgoing_energy_average: float | None
    outgoing_energy_class: str | None
    outgoing_energy_gauge: str | None
    outgoing_energy_gauge_range: str | None
    energy_delta: int | None
    flow_strength: int | None
    flow_strength_average: float | None
    flow_strength_class: str | None
    flow_strength_element: str | None
    flow_strength_element_range: str | None
    pressure_flow: str
    pressure_fusion: str
    pressure_fusion_profile: str
    pressure_fusion_constellation: str
    containment_state: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SetPressure:
    metric: str
    rule: str
    sorted_pressure: SortedPressure
    draw_pressure: DrawPressure

    def to_payload(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "rule": self.rule,
            "sorted_pressure": self.sorted_pressure.to_payload(),
            "draw_pressure": self.draw_pressure.to_payload(),
        }


@dataclass(frozen=True)
class SetHealth:
    set_health: str
    pressure_tone: str
    core_band: str
    middle_entry_bridge: str
    middle_bridge_exit: str
    endpoint_band: str
    rule: str

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SetAnatomy:
    set_anatomy: str
    starter_slot: str
    starter_number: int
    starter_band: str
    entry_relation: str
    entry_gap: int
    entry_gap_class: str
    middle_body: str
    middle_span: int
    middle_zone: str
    middle_gap_signature: str
    middle_slot_signature: str
    middle_pressure: str
    exit_relation: str
    exit_gap: int
    exit_gap_class: str
    edge_form: str
    edge_balance: str
    edge_pressure: str
    full_set_relation: str
    endpoint_slot: str
    endpoint_number: int
    endpoint_band: str
    technical_signature: str
    anatomy_order: tuple[str, ...]
    rule: str

    def to_payload(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["anatomy_order"] = list(self.anatomy_order)
        return payload


@dataclass(frozen=True)
class ApexPoint:
    total: int
    total_sum_gauge: str
    total_sum_gauge_range: str
    fp: int
    smallest_number: int
    largest_number: int
    fp_gauge: str
    fp_gauge_range: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "metric": "Apex Point",
            "total": self.total,
            "total_sum_gauge": self.total_sum_gauge,
            "total_sum_gauge_range": self.total_sum_gauge_range,
            "fp": self.fp,
            "fp_name": "finality point",
            "fp_gauge": self.fp_gauge,
            "fp_gauge_range": self.fp_gauge_range,
            "smallest_number": self.smallest_number,
            "largest_number": self.largest_number,
            "rule": "total is all five numbers added together; fp is largest number minus smallest number",
        }


@dataclass(frozen=True)
class DrawOrderAuthority:
    authority_start_date: date
    is_trusted_draw_order: bool
    authority_status: str
    rule: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "authority_start_date": self.authority_start_date.isoformat(),
            "is_trusted_draw_order": self.is_trusted_draw_order,
            "authority_status": self.authority_status,
            "rule": self.rule,
        }


@dataclass(frozen=True)
class DrawSetPacket:
    draw: HistoricalDraw
    previous_draw: HistoricalDraw | None
    next_draw: HistoricalDraw | None
    draw_order_authority: DrawOrderAuthority
    apex_point: ApexPoint
    set_pressure: SetPressure
    set_health: SetHealth
    set_anatomy: SetAnatomy
    sorted_form: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm]
    draw_form: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm]
    sorted_style: SetStyle
    draw_style: DrawStyle
    sorted_gaps: tuple[GapForm, GapForm, GapForm, GapForm]
    draw_gaps: tuple[GapForm, GapForm, GapForm, GapForm]
    sorted_relations: tuple[SetRelation, SetRelation, SetRelation, SetRelation]
    draw_relations: tuple[SetRelation, SetRelation, SetRelation, SetRelation]
    draw_motion: tuple[DrawMotion, DrawMotion, DrawMotion, DrawMotion, DrawMotion]
    draw_step_motion: tuple[DrawStepMotion, DrawStepMotion, DrawStepMotion, DrawStepMotion]

    def to_payload(self) -> dict[str, Any]:
        return {
            "schema": "iiw.draw_and_sorted_set_form.v1",
            "draw": self.draw.to_payload(),
            "continuity": {
                "previous_date": (
                    self.previous_draw.draw_date.isoformat()
                    if self.previous_draw
                    else None
                ),
                "current_date": self.draw.draw_date.isoformat(),
                "next_date": (
                    self.next_draw.draw_date.isoformat() if self.next_draw else None
                ),
            },
            "draw_order_authority": self.draw_order_authority.to_payload(),
            "shared_metrics": {
                "apex_point": self.apex_point.to_payload(),
                "set_pressure": self.set_pressure.to_payload(),
                "set_health": self.set_health.to_payload(),
                "set_anatomy": self.set_anatomy.to_payload(),
            },
            "sorted_section": {
                "set_style": self.sorted_style.to_payload(),
                "lanes": [lane.to_payload() for lane in self.sorted_form],
                "gaps": [gap.to_payload() for gap in self.sorted_gaps],
                "relations": [
                    relation.to_payload() for relation in self.sorted_relations
                ],
            },
            "draw_section": {
                "draw_style": self.draw_style.to_payload(),
                "lanes": [lane.to_payload() for lane in self.draw_form],
                "gaps": [gap.to_payload() for gap in self.draw_gaps],
                "relations": [
                    relation.to_payload() for relation in self.draw_relations
                ],
            },
            "draw_motion": {
                "rule": "date_to_date_by_draw_lane",
                "lanes": [motion.to_payload() for motion in self.draw_motion],
            },
            "d2_d5_motion": {
                "rule": "inside_current_draw_form",
                "lanes": [motion.to_payload() for motion in self.draw_step_motion],
            },
        }


def parse_draw_date(value: str) -> date:
    text = value.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported draw date: {value!r}")


def parse_optional_int(value: str | None) -> int | None:
    if value is None:
        return None
    text = value.strip().replace(",", "")
    if not text:
        return None
    return int(text)


def parse_int(value: str | None, field_name: str) -> int:
    parsed = parse_optional_int(value)
    if parsed is None:
        raise ValueError(f"Missing required field: {field_name}")
    return parsed


def validate_white_balls(values: tuple[int, int, int, int, int], row_label: str) -> None:
    if len(values) != WHITE_BALL_COUNT:
        raise ValueError(f"{row_label}: expected {WHITE_BALL_COUNT} white balls.")
    out_of_range = [
        value for value in values if value < WHITE_BALL_MIN or value > WHITE_BALL_MAX
    ]
    if out_of_range:
        raise ValueError(f"{row_label}: white ball out of range: {out_of_range}")
    if len(set(values)) != WHITE_BALL_COUNT:
        raise ValueError(f"{row_label}: duplicate white balls: {values}")


def validate_powerball(value: int, row_label: str) -> None:
    if value < POWERBALL_MIN or value > POWERBALL_MAX:
        raise ValueError(f"{row_label}: powerball out of range: {value}")


def historical_draw_from_row(row: dict[str, str], row_number: int) -> HistoricalDraw:
    row_label = f"CSV row {row_number}"
    white_balls = (
        parse_int(row.get("w1"), "w1"),
        parse_int(row.get("w2"), "w2"),
        parse_int(row.get("w3"), "w3"),
        parse_int(row.get("w4"), "w4"),
        parse_int(row.get("w5"), "w5"),
    )
    powerball = parse_int(row.get("pb"), "pb")
    validate_white_balls(white_balls, row_label)
    validate_powerball(powerball, row_label)
    return HistoricalDraw(
        draw_date=parse_draw_date(row.get("draw_date", "")),
        draw_index=parse_int(row.get("draw_index"), "draw_index"),
        jackpot_usd=parse_optional_int(row.get("jackpot_usd")),
        white_balls=white_balls,
        powerball=powerball,
        powerplay=parse_optional_int(row.get("powerplay")),
    )


def validate_draw_sequence(draws: list[HistoricalDraw]) -> None:
    if not draws:
        raise ValueError("No draw rows were loaded.")

    seen_indexes: set[int] = set()
    previous_date: date | None = None
    previous_index: int | None = None

    for draw in draws:
        if draw.draw_index in seen_indexes:
            raise ValueError(f"Duplicate draw index: {draw.draw_index}")
        seen_indexes.add(draw.draw_index)

        if previous_date is not None and draw.draw_date < previous_date:
            raise ValueError(
                f"Draw dates are not ascending: {draw.draw_date} follows {previous_date}"
            )
        if previous_index is not None and draw.draw_index <= previous_index:
            raise ValueError(
                f"Draw indexes are not ascending: {draw.draw_index} follows {previous_index}"
            )

        previous_date = draw.draw_date
        previous_index = draw.draw_index


def number_band(number: int) -> str:
    for band_range, label in NUMBER_BANDS:
        if number in band_range:
            return label
    raise ValueError(f"Number has no band label: {number}")


def gap_letter(gap: int) -> tuple[str, str]:
    if gap < 1:
        return "ZERO", "0"
    for gap_range, label in GAP_ALPHABET:
        if gap in gap_range:
            return label, f"{gap_range.start}-{gap_range.stop - 1}"
    raise ValueError(f"Gap has no alphabet label: {gap}")


def pressure_roman(gap: int) -> tuple[str, str]:
    if gap < 1:
        return "ZERO", "0"
    for gap_range, label in PRESSURE_ROMAN_35:
        if gap in gap_range:
            return label, f"{gap_range.start}-{gap_range.stop - 1}"
    raise ValueError(f"Pressure gap has no Roman label: {gap}")


def relation_class(gap: int) -> tuple[str, str]:
    for class_range, label in RELATION_CLASSES:
        if gap in class_range:
            return label, f"{class_range.start}-{class_range.stop - 1}"
    raise ValueError(f"Relation gap has no class label: {gap}")


def pressure_symbol(gap: int) -> str:
    if gap <= 10:
        return "S"
    if gap <= 16:
        return "M"
    if gap <= 24:
        return "B"
    return "E"


def pressure_family_from_arc(pressure_arc: str) -> str:
    e_count = pressure_arc.count("E")
    b_count = pressure_arc.count("B")
    if e_count >= 2 or (e_count >= 1 and b_count >= 1):
        return "Volcanic"
    if e_count == 1 and b_count == 0:
        return "Extreme"
    if b_count >= 1 and e_count == 0:
        return "Burst"
    return "Canonical"


def pressure_type_from_arc(pressure_arc: str, pressure_family: str) -> str:
    if pressure_family == "Volcanic":
        return "RESET"
    if pressure_family == "Extreme":
        return "CRISIS"
    if pressure_family == "Burst":
        return "SEPARATION"
    s_count = pressure_arc.count("S")
    m_count = pressure_arc.count("M")
    if s_count > m_count:
        return "COMPRESSION"
    if m_count > s_count:
        return "EXPANSION"
    if pressure_arc in {"SMSM", "MSMS"}:
        return "EXPANSION"
    return "COMPRESSION"


def motion_gauge(value: int | None) -> tuple[str | None, str | None]:
    if value is None:
        return None, None
    magnitude = abs(value)
    if magnitude == 0:
        return "still", "0"
    for gauge_range, label in MOTION_GAUGE_CLASSES:
        if magnitude in gauge_range:
            return label, f"{gauge_range.start}-{gauge_range.stop - 1}"
    return "light empresses", "71+"


def magnitude_bucket(value: float | int | None) -> tuple[int | None, str | None]:
    if value is None:
        return None, None
    magnitude = abs(float(value))
    if magnitude == 0:
        return 0, "0"
    bucket = math.ceil(magnitude)
    if bucket > WHITE_BALL_MAX:
        return WHITE_BALL_MAX, f"{WHITE_BALL_MAX}+"
    return bucket, str(bucket)


def broad_motion_class(value: float | int | None) -> tuple[str | None, str | None]:
    bucket, bucket_range = magnitude_bucket(value)
    if bucket is None:
        return None, None
    if bucket == 0:
        return "Still Motion", bucket_range
    for motion_range, label in MOTION_BROAD_CLASSES:
        if bucket in motion_range:
            return label, f"{motion_range.start}-{motion_range.stop - 1}"
    return "Chaotic Motion", f"{WHITE_BALL_MAX}+"


def spectrum_class(value: float | int | None) -> tuple[str | None, str | None]:
    bucket, bucket_range = magnitude_bucket(value)
    if bucket is None:
        return None, None
    if bucket == 0:
        return "Black", bucket_range
    for spectrum_range, label in PATH_ENERGY_SPECTRUM_CLASSES:
        if bucket in spectrum_range:
            return label, f"{spectrum_range.start}-{spectrum_range.stop - 1}"
    return "Apex Violet", f"{WHITE_BALL_MAX}+"


def element_class(value: float | int | None) -> tuple[str | None, str | None]:
    bucket, bucket_range = magnitude_bucket(value)
    if bucket is None:
        return None, None
    if bucket == 0:
        return "Stable Zero", bucket_range
    for element_range, label in FLOW_STRENGTH_ELEMENT_CLASSES:
        if bucket in element_range:
            return label, f"{element_range.start}-{element_range.stop - 1}"
    return "Bromine", f"{WHITE_BALL_MAX}+"


def health_words(label: str) -> str:
    return label.replace("_", " ").title()


def anatomy_token(label: str) -> str:
    return label.upper().replace(" ", "_").replace("-", "_")


def middle_number_zone(number: int) -> str:
    if number <= 23:
        return "LOW"
    if number <= 46:
        return "MID"
    return "HIGH"


def total_sum_gauge(total: int) -> tuple[str, str]:
    if total < 1:
        return "still", "0"
    class_index = ((total - 1) // 2) % len(MOTION_GAUGE_CLASSES)
    gauge_range, label = MOTION_GAUGE_CLASSES[class_index]
    cycle_start = ((total - 1) // (2 * len(MOTION_GAUGE_CLASSES))) * (
        2 * len(MOTION_GAUGE_CLASSES)
    )
    return label, f"{cycle_start + gauge_range.start}-{cycle_start + gauge_range.stop - 1}"


def apex_olympus_gauge(value: int) -> tuple[str, str]:
    if value < 1:
        return "Olympus Zero", "0"
    class_index = ((value - 1) // 2) % len(OLYMPUS_APEX_CLASSES)
    cycle_start = ((value - 1) // (2 * len(OLYMPUS_APEX_CLASSES))) * (
        2 * len(OLYMPUS_APEX_CLASSES)
    )
    range_start = cycle_start + (class_index * 2) + 1
    return OLYMPUS_APEX_CLASSES[class_index], f"{range_start}-{range_start + 1}"


def energy_gauge(energy: int | None) -> tuple[str | None, str | None]:
    if energy is None:
        return None, None
    return total_sum_gauge(energy)


def normalized_energy(total: int | None, divisor: int) -> float | None:
    if total is None:
        return None
    return round(total / divisor, 2)


def pressure_shape_from_gaps(gaps: tuple[GapForm, GapForm, GapForm, GapForm]) -> str:
    return "".join("+" if gap.distance > 0 else "-" for gap in gaps)


def pressure_type_from_shape(pressure_shape: str) -> str:
    return PRESSURE_SHAPE_TYPES.get(pressure_shape, "UNMAPPED_PRESSURE_SHAPE")


def pressure_fusion_label(
    sorted_pressure_type: str,
    sorted_family: str,
    draw_pressure_type: str,
    draw_family: str,
) -> str:
    if sorted_pressure_type == draw_pressure_type and sorted_family == draw_family:
        return "MATCHED_FUSION"
    if sorted_pressure_type == draw_pressure_type:
        return "TYPE_FUSION"
    if sorted_family == draw_family:
        return "FAMILY_FUSION"
    if frozenset((sorted_pressure_type, draw_pressure_type)) in INVERTED_PRESSURE_SHAPE_PAIRS:
        return "INVERTED_FUSION"
    return "REDISTRIBUTED_FUSION"


def containment_state(
    pressure_flow: str,
    draw_path_energy_average: float,
    flow_strength_average: float | None,
) -> str:
    if pressure_flow == "UNKNOWN_BOUNDARY" or flow_strength_average is None:
        return "BOUNDARY_UNKNOWN"
    if flow_strength_average <= 10 and draw_path_energy_average <= 20:
        return "CONTAINED_MOTION"
    if flow_strength_average <= 20:
        return "CONTROLLED_VOLATILE_MOTION"
    if flow_strength_average <= 40:
        return "STRAINED_MOTION"
    return "BROKEN_MOTION"


def build_lane_form(
    lane: str,
    role: str,
    number: int,
    allowed_start: int,
    allowed_end: int,
) -> LaneForm:
    return LaneForm(
        lane=lane,
        role=role,
        number=number,
        number_band=number_band(number),
        allowed_start=allowed_start,
        allowed_end=allowed_end,
        in_lane_range=allowed_start <= number <= allowed_end,
    )


def build_sorted_form(
    draw: HistoricalDraw,
) -> tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm]:
    return tuple(
        build_lane_form(lane, role, number, allowed_start, allowed_end)
        for (lane, role, allowed_start, allowed_end), number in zip(
            SORTED_LANES, draw.sorted_white_balls
        )
    )  # type: ignore[return-value]


def build_draw_form(
    draw: HistoricalDraw,
) -> tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm]:
    return tuple(
        build_lane_form(lane, role, number, allowed_start, allowed_end)
        for (lane, role, allowed_start, allowed_end), number in zip(
            DRAW_LANES, draw.white_balls
        )
    )  # type: ignore[return-value]


def style_group_name(size: int) -> str:
    if size == 1:
        return "Lone"
    if size == 2:
        return "Duo"
    if size == 3:
        return "Trio"
    if size == 4:
        return "Quad"
    if size == 5:
        return "Noble"
    raise ValueError(f"Unsupported set style group size: {size}")


def classify_set_style_from_group_sizes(group_sizes: list[int]) -> str:
    connected_sizes = [size for size in group_sizes if size >= 2]
    if 5 in connected_sizes:
        return "Noble"
    if 4 in connected_sizes:
        return "Quad"
    if 3 in connected_sizes and 2 in connected_sizes:
        return "Blended Family"
    if 3 in connected_sizes:
        return "Trio"
    if connected_sizes.count(2) >= 2:
        return "Third-Wheel"
    if 2 in connected_sizes:
        return "Duo"
    return "Altogether"


def build_set_style(
    section: str,
    lane_forms: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm],
) -> SetStyle:
    connected_pattern = "".join(
        "C"
        if abs(lane_forms[index + 1].number - lane_forms[index].number)
        < SET_STYLE_CONNECTION_LIMIT
        else "X"
        for index in range(WHITE_BALL_COUNT - 1)
    )
    group_ranges: list[tuple[int, int]] = []
    group_start = 0
    for index, marker in enumerate(connected_pattern):
        if marker == "X":
            group_ranges.append((group_start, index))
            group_start = index + 1
    group_ranges.append((group_start, WHITE_BALL_COUNT - 1))

    groups: list[SetStyleGroup] = []
    for start, end in group_ranges:
        forms = lane_forms[start : end + 1]
        size = len(forms)
        groups.append(
            SetStyleGroup(
                group_style=style_group_name(size),
                start_lane=forms[0].lane,
                end_lane=forms[-1].lane,
                lanes=tuple(form.lane for form in forms),
                numbers=tuple(form.number for form in forms),
                size=size,
            )
        )

    group_sizes = [group.size for group in groups]
    set_style = classify_set_style_from_group_sizes(group_sizes)
    group_signature = "-".join(group.group_style for group in groups)
    set_signature = (
        f"{anatomy_token(section)}_STYLE_"
        f"{anatomy_token(set_style)}_"
        f"PATTERN_{connected_pattern}_"
        f"GROUPS_{anatomy_token(group_signature)}"
    )
    return SetStyle(
        section=section,
        set_style=set_style,
        set_signature=set_signature,
        connection_rule="adjacent gap under 10 spaces; connected gaps are 1-9",
        connected_pattern=connected_pattern,
        group_signature=group_signature,
        groups=tuple(groups),
    )


def direction_marker(distance: int) -> str:
    if distance > 0:
        return "+"
    if distance < 0:
        return "-"
    return "0"


def draw_route_code(transfer_pattern: str) -> str:
    return "DRAW_ROUTE_" + transfer_pattern.replace("-", "_")


def draw_style_family(direction_pattern: str) -> str:
    signs = [marker for marker in direction_pattern if marker in {"+", "-"}]
    if not signs:
        return "Still"
    turn_count = sum(
        1 for index in range(len(signs) - 1) if signs[index] != signs[index + 1]
    )
    if turn_count == 0:
        return "Clean Climb" if signs[0] == "+" else "Clean Drop"
    if turn_count == 3:
        return "Full Pendulum"
    if turn_count == 2:
        return "Crest Valley" if signs[0] == "+" else "Valley Crest"

    turn_index = next(
        index for index in range(len(signs) - 1) if signs[index] != signs[index + 1]
    )
    timing = ("Early", "Middle", "Late")[turn_index]
    turn_name = "Crest" if signs[0] == "+" else "Valley"
    return f"{timing} {turn_name}"


def draw_turn_lanes(direction_pattern: str) -> tuple[str, ...]:
    return tuple(
        DRAW_LANES[index + 1][0]
        for index in range(len(direction_pattern) - 1)
        if direction_pattern[index] != direction_pattern[index + 1]
    )


def build_draw_style(
    draw_form: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm],
    sorted_form: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm],
) -> DrawStyle:
    sorted_by_number = {lane.number: lane for lane in sorted_form}
    sorted_position_by_number = {
        lane.number: position for position, lane in enumerate(sorted_form, start=1)
    }
    steps: list[DrawStyleTransferStep] = []
    for draw_lane in draw_form:
        sorted_lane = sorted_by_number[draw_lane.number]
        steps.append(
            DrawStyleTransferStep(
                draw_lane=draw_lane.lane,
                draw_role=draw_lane.role,
                draw_number=draw_lane.number,
                sorted_lane=sorted_lane.lane,
                sorted_role=sorted_lane.role,
                sorted_position=sorted_position_by_number[draw_lane.number],
            )
        )

    direction_pattern = "".join(
        direction_marker(draw_form[index + 1].number - draw_form[index].number)
        for index in range(WHITE_BALL_COUNT - 1)
    )
    transfer_pattern = "-".join(step.sorted_lane for step in steps)
    sorted_position_path = tuple(step.sorted_position for step in steps)
    sorted_position_deltas = tuple(
        sorted_position_path[index + 1] - sorted_position_path[index]
        for index in range(WHITE_BALL_COUNT - 1)
    )
    turn_lanes = draw_turn_lanes(direction_pattern)
    return DrawStyle(
        section="draw",
        draw_style=draw_route_code(transfer_pattern),
        draw_style_family=draw_style_family(direction_pattern),
        rule="draw style is the exact D1-D5 transfer route through S1-S5 sorted lanes",
        direction_pattern=direction_pattern,
        transfer_pattern=transfer_pattern,
        sorted_position_path=sorted_position_path,
        sorted_position_deltas=sorted_position_deltas,
        sorted_position_energy=sum(abs(delta) for delta in sorted_position_deltas),
        turn_count=len(turn_lanes),
        turn_lanes=turn_lanes,
        steps=tuple(steps),
    )


def build_adjacent_gaps(
    section: str,
    lane_forms: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm],
) -> tuple[GapForm, GapForm, GapForm, GapForm]:
    rows: list[GapForm] = []
    for index in range(WHITE_BALL_COUNT - 1):
        left = lane_forms[index]
        right = lane_forms[index + 1]
        distance = right.number - left.number
        gap = abs(distance)
        letter, letter_range = gap_letter(gap)
        rows.append(
            GapForm(
                section=section,
                from_lane=left.lane,
                to_lane=right.lane,
                from_number=left.number,
                to_number=right.number,
                distance=distance,
                gap=gap,
                gap_letter=letter,
                gap_range=letter_range,
            )
        )
    return tuple(rows)  # type: ignore[return-value]


def build_set_relations(
    section: str,
    lane_forms: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm],
) -> tuple[SetRelation, SetRelation, SetRelation, SetRelation]:
    rows: list[SetRelation] = []
    for index in range(WHITE_BALL_COUNT - 1):
        left = lane_forms[index]
        right = lane_forms[index + 1]
        distance = right.number - left.number
        gap = abs(distance)
        letter, letter_range = gap_letter(gap)
        class_label, class_range = relation_class(gap)
        rows.append(
            SetRelation(
                section=section,
                relation=f"{left.role}_to_{right.role}",
                from_lane=left.lane,
                to_lane=right.lane,
                from_role=left.role,
                to_role=right.role,
                from_number=left.number,
                to_number=right.number,
                distance=distance,
                gap=gap,
                gap_letter=letter,
                gap_range=letter_range,
                relation_class=class_label,
                relation_class_range=class_range,
            )
        )
    return tuple(rows)  # type: ignore[return-value]


def pressure_arc_from_gaps(gaps: tuple[GapForm, GapForm, GapForm, GapForm]) -> str:
    return "".join(pressure_symbol(gap.gap) for gap in gaps)


def pressure_arc_35_from_gaps(gaps: tuple[GapForm, GapForm, GapForm, GapForm]) -> str:
    return "-".join(pressure_roman(gap.gap)[0] for gap in gaps)


def classify_pressure_flow(incoming_energy: int | None, outgoing_energy: int | None) -> str:
    if incoming_energy is None or outgoing_energy is None:
        return "UNKNOWN_BOUNDARY"
    if outgoing_energy > incoming_energy:
        return "RELEASE"
    if incoming_energy > outgoing_energy:
        return "RETENTION"
    return "BALANCED_TRANSFER"


def build_set_pressure(
    apex_point: ApexPoint,
    sorted_style: SetStyle,
    draw_style: DrawStyle,
    sorted_gaps: tuple[GapForm, GapForm, GapForm, GapForm],
    draw_gaps: tuple[GapForm, GapForm, GapForm, GapForm],
    draw_motion: tuple[DrawMotion, DrawMotion, DrawMotion, DrawMotion, DrawMotion],
) -> SetPressure:
    sorted_arc = pressure_arc_from_gaps(sorted_gaps)
    sorted_family = pressure_family_from_arc(sorted_arc)
    sorted_shape = pressure_shape_from_gaps(sorted_gaps)
    sorted_gap_values = [gap.gap for gap in sorted_gaps]
    largest_sorted_gap_index = max(
        range(len(sorted_gaps)), key=lambda index: sorted_gaps[index].gap
    )

    draw_arc = pressure_arc_from_gaps(draw_gaps)
    draw_family = pressure_family_from_arc(draw_arc)
    draw_shape = pressure_shape_from_gaps(draw_gaps)
    draw_path_energy = sum(gap.gap for gap in draw_gaps)
    draw_path_energy_average = normalized_energy(draw_path_energy, len(draw_gaps))
    assert draw_path_energy_average is not None
    draw_path_energy_class, _ = broad_motion_class(draw_path_energy_average)
    draw_path_energy_spectrum, draw_path_energy_spectrum_range = spectrum_class(
        draw_path_energy_average
    )
    draw_energy_gauge, draw_energy_gauge_range = energy_gauge(draw_path_energy)

    incoming_energy = (
        None
        if any(motion.incoming_motion is None for motion in draw_motion)
        else sum(abs(int(motion.incoming_motion)) for motion in draw_motion)
    )
    incoming_energy_average = normalized_energy(incoming_energy, len(draw_motion))
    incoming_energy_class, _ = broad_motion_class(incoming_energy_average)
    outgoing_energy = (
        None
        if any(motion.outgoing_motion is None for motion in draw_motion)
        else sum(abs(int(motion.outgoing_motion)) for motion in draw_motion)
    )
    outgoing_energy_average = normalized_energy(outgoing_energy, len(draw_motion))
    outgoing_energy_class, _ = broad_motion_class(outgoing_energy_average)
    incoming_gauge, incoming_gauge_range = energy_gauge(incoming_energy)
    outgoing_gauge, outgoing_gauge_range = energy_gauge(outgoing_energy)
    pressure_flow = classify_pressure_flow(incoming_energy, outgoing_energy)
    energy_delta = (
        None if incoming_energy is None or outgoing_energy is None else outgoing_energy - incoming_energy
    )
    flow_strength = None if energy_delta is None else abs(energy_delta)
    flow_strength_average = normalized_energy(flow_strength, len(draw_motion))
    flow_strength_class, _ = broad_motion_class(flow_strength_average)
    flow_strength_element, flow_strength_element_range = element_class(
        flow_strength_average
    )
    sorted_arc_type = pressure_type_from_arc(sorted_arc, sorted_family)
    draw_arc_type = pressure_type_from_arc(draw_arc, draw_family)
    sorted_pressure_type = pressure_type_from_shape(sorted_shape)
    draw_pressure_type = pressure_type_from_shape(draw_shape)
    pressure_fusion = pressure_fusion_label(
        sorted_pressure_type,
        sorted_family,
        draw_pressure_type,
        draw_family,
    )
    pressure_fusion_profile = f"{sorted_pressure_type}_TO_{draw_pressure_type}"
    pressure_fusion_constellation = PRESSURE_FUSION_CONSTELLATIONS[pressure_fusion]
    containment = containment_state(
        pressure_flow,
        draw_path_energy_average,
        flow_strength_average,
    )

    return SetPressure(
        metric="Set Pressure",
        rule=(
            "motion explains behavior, structure explains form, pressure explains "
            "tension inside form, and energy measures cost"
        ),
        sorted_pressure=SortedPressure(
            pressure_shape=sorted_shape,
            pressure_type=sorted_pressure_type,
            set_arc=sorted_arc,
            set_arc_35=pressure_arc_35_from_gaps(sorted_gaps),
            set_arc_family=sorted_family,
            set_arc_type=sorted_arc_type,
            sorted_style=sorted_style.set_style,
            fp=apex_point.fp,
            total=apex_point.total,
            edge_pressure=sorted_gap_values[0] + sorted_gap_values[3],
            middle_pressure=sorted_gap_values[1] + sorted_gap_values[2],
            middle_minus_edge=(
                sorted_gap_values[1]
                + sorted_gap_values[2]
                - sorted_gap_values[0]
                - sorted_gap_values[3]
            ),
            largest_gap=sorted_gaps[largest_sorted_gap_index].gap,
            largest_gap_relation=(
                f"{sorted_gaps[largest_sorted_gap_index].from_lane}->"
                f"{sorted_gaps[largest_sorted_gap_index].to_lane}"
            ),
        ),
        draw_pressure=DrawPressure(
            pressure_shape=draw_shape,
            pressure_type=draw_pressure_type,
            set_arc=draw_arc,
            set_arc_35=pressure_arc_35_from_gaps(draw_gaps),
            set_arc_family=draw_family,
            set_arc_type=draw_arc_type,
            draw_style=draw_style.draw_style,
            draw_style_family=draw_style.draw_style_family,
            direction_pattern=draw_style.direction_pattern,
            transfer_pattern=draw_style.transfer_pattern,
            draw_path_energy=draw_path_energy,
            draw_path_energy_average=draw_path_energy_average,
            draw_path_energy_class=str(draw_path_energy_class),
            draw_path_energy_spectrum=str(draw_path_energy_spectrum),
            draw_path_energy_spectrum_range=str(draw_path_energy_spectrum_range),
            draw_path_energy_gauge=str(draw_energy_gauge),
            draw_path_energy_gauge_range=str(draw_energy_gauge_range),
            sorted_position_energy=draw_style.sorted_position_energy,
            incoming_energy=incoming_energy,
            incoming_energy_average=incoming_energy_average,
            incoming_energy_class=incoming_energy_class,
            incoming_energy_gauge=incoming_gauge,
            incoming_energy_gauge_range=incoming_gauge_range,
            outgoing_energy=outgoing_energy,
            outgoing_energy_average=outgoing_energy_average,
            outgoing_energy_class=outgoing_energy_class,
            outgoing_energy_gauge=outgoing_gauge,
            outgoing_energy_gauge_range=outgoing_gauge_range,
            energy_delta=energy_delta,
            flow_strength=flow_strength,
            flow_strength_average=flow_strength_average,
            flow_strength_class=flow_strength_class,
            flow_strength_element=flow_strength_element,
            flow_strength_element_range=flow_strength_element_range,
            pressure_flow=pressure_flow,
            pressure_fusion=pressure_fusion,
            pressure_fusion_profile=pressure_fusion_profile,
            pressure_fusion_constellation=pressure_fusion_constellation,
            containment_state=containment,
        ),
    )


def build_draw_motion(
    previous_draw: HistoricalDraw | None,
    current_draw: HistoricalDraw,
    next_draw: HistoricalDraw | None,
) -> tuple[DrawMotion, DrawMotion, DrawMotion, DrawMotion, DrawMotion]:
    rows: list[DrawMotion] = []
    for index, (lane, role, _, _) in enumerate(DRAW_LANES):
        incoming_motion = (
            current_draw.white_balls[index] - previous_draw.white_balls[index]
            if previous_draw
            else None
        )
        outgoing_motion = (
            next_draw.white_balls[index] - current_draw.white_balls[index]
            if next_draw
            else None
        )
        incoming_gauge, incoming_gauge_range = motion_gauge(incoming_motion)
        outgoing_gauge, outgoing_gauge_range = motion_gauge(outgoing_motion)
        incoming_class, _ = broad_motion_class(incoming_motion)
        outgoing_class, _ = broad_motion_class(outgoing_motion)
        rows.append(
            DrawMotion(
                lane=lane,
                role=role,
                incoming_motion=incoming_motion,
                incoming_motion_class=incoming_class,
                incoming_motion_gauge=incoming_gauge,
                incoming_motion_gauge_range=incoming_gauge_range,
                outgoing_motion=outgoing_motion,
                outgoing_motion_class=outgoing_class,
                outgoing_motion_gauge=outgoing_gauge,
                outgoing_motion_gauge_range=outgoing_gauge_range,
            )
        )
    return tuple(rows)  # type: ignore[return-value]


def build_draw_step_motion(
    current_draw: HistoricalDraw,
) -> tuple[DrawStepMotion, DrawStepMotion, DrawStepMotion, DrawStepMotion]:
    rows: list[DrawStepMotion] = []
    for index in range(1, WHITE_BALL_COUNT):
        from_lane, from_role, _, _ = DRAW_LANES[index - 1]
        lane, role, _, _ = DRAW_LANES[index]
        from_number = current_draw.white_balls[index - 1]
        to_number = current_draw.white_balls[index]
        rows.append(
            DrawStepMotion(
                lane=lane,
                role=role,
                from_lane=from_lane,
                from_role=from_role,
                from_number=from_number,
                to_number=to_number,
                distance=to_number - from_number,
            )
        )
    return tuple(rows)  # type: ignore[return-value]


def build_apex_point(draw: HistoricalDraw) -> ApexPoint:
    smallest_number = min(draw.white_balls)
    largest_number = max(draw.white_balls)
    total = sum(draw.white_balls)
    fp = largest_number - smallest_number
    total_gauge, total_gauge_range = apex_olympus_gauge(total)
    fp_gauge, fp_gauge_range = apex_olympus_gauge(fp)
    return ApexPoint(
        total=total,
        total_sum_gauge=total_gauge,
        total_sum_gauge_range=total_gauge_range,
        fp=fp,
        smallest_number=smallest_number,
        largest_number=largest_number,
        fp_gauge=str(fp_gauge),
        fp_gauge_range=str(fp_gauge_range),
    )


def build_set_health(
    set_pressure: SetPressure,
    sorted_form: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm],
    sorted_relations: tuple[SetRelation, SetRelation, SetRelation, SetRelation],
) -> SetHealth:
    pressure_type = set_pressure.draw_pressure.pressure_type
    pressure_tone = SET_HEALTH_TONES.get(pressure_type, health_words(pressure_type))
    core_band = health_words(sorted_form[0].number_band)
    middle_entry_bridge = health_words(sorted_relations[1].relation_class)
    middle_bridge_exit = health_words(sorted_relations[2].relation_class)
    endpoint_band = health_words(sorted_form[4].number_band)
    set_health = " ".join(
        (
            pressure_tone,
            core_band,
            middle_entry_bridge,
            middle_bridge_exit,
            endpoint_band,
        )
    )
    return SetHealth(
        set_health=set_health,
        pressure_tone=pressure_tone,
        core_band=core_band,
        middle_entry_bridge=middle_entry_bridge,
        middle_bridge_exit=middle_bridge_exit,
        endpoint_band=endpoint_band,
        rule=(
            "set health is natural draw pressure tone plus S1 core band, "
            "S2->S3 middle relation, S3->S4 middle relation, and S5 endpoint band"
        ),
    )


def gap_openness(gap: int) -> str:
    if gap <= 10:
        return "CONTAINED"
    if gap <= 24:
        return "BALANCED"
    return "OPEN"


def classify_middle_pressure(
    middle_minus_edge: int,
    s2_s3_gap: int,
    s3_s4_gap: int,
) -> str:
    if middle_minus_edge >= 16:
        return "MIDDLE_EXPANSION_PRESSURE"
    if middle_minus_edge <= -12:
        return "MIDDLE_COMPRESSION_PRESSURE"
    if s2_s3_gap > 24 and s3_s4_gap <= 10:
        return "S3_S4_RECOVERY_AFTER_S2_STRETCH"
    if s2_s3_gap <= 10 and s3_s4_gap > 24:
        return "S2_S3_LOCK_BEFORE_S4_STRETCH"
    return "MIDDLE_STABLE_PRESSURE"


def classify_edge_pressure(entry_gap: int, exit_gap: int) -> str:
    entry_open = gap_openness(entry_gap)
    exit_open = gap_openness(exit_gap)
    if entry_open == exit_open:
        return f"EDGE_{entry_open}"
    return f"ENTRY_{entry_open}_EXIT_{exit_open}"


def classify_full_set_relation(middle_minus_edge: int, edge_balance: str) -> str:
    if middle_minus_edge >= 16:
        return "MIDDLE_WIDER_THAN_OUTER_EDGES"
    if middle_minus_edge <= -12:
        return "OUTER_EDGES_WIDER_THAN_MIDDLE"
    if edge_balance in {"EDGE_BALANCED", "EDGE_NEAR_BALANCED"}:
        return "ENTRY_EXIT_BALANCED_AROUND_MIDDLE"
    return "ENTRY_EXIT_TILTED_AROUND_MIDDLE"


def build_set_anatomy(
    set_pressure: SetPressure,
    sorted_form: tuple[LaneForm, LaneForm, LaneForm, LaneForm, LaneForm],
    sorted_relations: tuple[SetRelation, SetRelation, SetRelation, SetRelation],
) -> SetAnatomy:
    s1, s2, s3, s4, s5 = sorted_form
    entry_relation, s2_s3_relation, s3_s4_relation, exit_relation = sorted_relations
    starter_slot = f"S1_CORE_{anatomy_token(s1.number_band)}"
    endpoint_slot = f"S5_ENDPOINT_{anatomy_token(s5.number_band)}"
    middle_span = s4.number - s2.number
    middle_zone = "_".join(
        middle_number_zone(lane.number) for lane in (s2, s3, s4)
    )
    if s2_s3_relation.relation_class == s3_s4_relation.relation_class:
        middle_body = f"S2_S4_DUAL_{s2_s3_relation.relation_class}"
    else:
        middle_body = (
            f"S2_S4_{s2_s3_relation.relation_class}_THEN_"
            f"{s3_s4_relation.relation_class}"
        )
    middle_gap_signature = (
        f"{s2_s3_relation.relation_class}_THEN_"
        f"{s3_s4_relation.relation_class}"
    )
    middle_slot_signature = " | ".join(
        f"{lane.lane}_{anatomy_token(lane.role)}_{anatomy_token(lane.number_band)}"
        for lane in (s2, s3, s4)
    )
    middle_pressure = classify_middle_pressure(
        set_pressure.sorted_pressure.middle_minus_edge,
        s2_s3_relation.gap,
        s3_s4_relation.gap,
    )
    edge_delta = entry_relation.gap - exit_relation.gap
    edge_form = (
        f"ENTRY_{entry_relation.relation_class}_EXIT_"
        f"{exit_relation.relation_class}"
    )
    if entry_relation.relation_class == exit_relation.relation_class:
        edge_balance = "EDGE_BALANCED"
    elif abs(edge_delta) <= 3:
        edge_balance = "EDGE_NEAR_BALANCED"
    elif edge_delta > 0:
        edge_balance = "ENTRY_HEAVIER"
    else:
        edge_balance = "EXIT_HEAVIER"
    edge_pressure = classify_edge_pressure(entry_relation.gap, exit_relation.gap)
    full_set_relation = classify_full_set_relation(
        set_pressure.sorted_pressure.middle_minus_edge,
        edge_balance,
    )
    technical_parts = (
        starter_slot,
        edge_form,
        middle_body,
        middle_pressure,
        full_set_relation,
        endpoint_slot,
    )
    set_anatomy = " :: ".join(technical_parts)
    return SetAnatomy(
        set_anatomy=set_anatomy,
        starter_slot=starter_slot,
        starter_number=s1.number,
        starter_band=health_words(s1.number_band),
        entry_relation=entry_relation.relation,
        entry_gap=entry_relation.gap,
        entry_gap_class=entry_relation.relation_class,
        middle_body=middle_body,
        middle_span=middle_span,
        middle_zone=middle_zone,
        middle_gap_signature=middle_gap_signature,
        middle_slot_signature=middle_slot_signature,
        middle_pressure=middle_pressure,
        exit_relation=exit_relation.relation,
        exit_gap=exit_relation.gap,
        exit_gap_class=exit_relation.relation_class,
        edge_form=edge_form,
        edge_balance=edge_balance,
        edge_pressure=edge_pressure,
        full_set_relation=full_set_relation,
        endpoint_slot=endpoint_slot,
        endpoint_number=s5.number,
        endpoint_band=health_words(s5.number_band),
        technical_signature=" | ".join(technical_parts),
        anatomy_order=(
            "S1_STARTER_SLOT",
            "S1_S2_ENTRY_EDGE",
            "S2_S4_MIDDLE_BODY",
            "S4_S5_EXIT_EDGE",
            "S5_ENDPOINT_SLOT",
        ),
        rule=(
            "set anatomy expands Set Health with starter slot, entry/exit edge, "
            "S2-S4 middle body, edge-vs-middle pressure, and endpoint slot"
        ),
    )


def build_draw_order_authority(draw: HistoricalDraw) -> DrawOrderAuthority:
    is_trusted = draw.draw_date >= TRUSTED_DRAW_ORDER_START_DATE
    return DrawOrderAuthority(
        authority_start_date=TRUSTED_DRAW_ORDER_START_DATE,
        is_trusted_draw_order=is_trusted,
        authority_status=(
            "TRUSTED_DRAW_ORDER" if is_trusted else "SORTED_RECORD_ONLY"
        ),
        rule=(
            "Draw-order style, draw pressure, and date-to-date draw motion are "
            "trusted only on or after 2015-10-07."
        ),
    )


def build_draw_set_packet(draws: list[HistoricalDraw], index: int) -> DrawSetPacket:
    draw = draws[index]
    previous_draw = draws[index - 1] if index > 0 else None
    next_draw = draws[index + 1] if index < len(draws) - 1 else None
    sorted_form = build_sorted_form(draw)
    draw_form = build_draw_form(draw)
    apex_point = build_apex_point(draw)
    sorted_style = build_set_style("sorted", sorted_form)
    draw_style = build_draw_style(draw_form, sorted_form)
    sorted_gaps = build_adjacent_gaps("sorted", sorted_form)
    draw_gaps = build_adjacent_gaps("draw", draw_form)
    draw_motion = build_draw_motion(previous_draw, draw, next_draw)
    set_pressure = build_set_pressure(
        apex_point,
        sorted_style,
        draw_style,
        sorted_gaps,
        draw_gaps,
        draw_motion,
    )
    sorted_relations = build_set_relations("sorted", sorted_form)
    draw_relations = build_set_relations("draw", draw_form)
    set_health = build_set_health(set_pressure, sorted_form, sorted_relations)
    set_anatomy = build_set_anatomy(set_pressure, sorted_form, sorted_relations)
    return DrawSetPacket(
        draw=draw,
        previous_draw=previous_draw,
        next_draw=next_draw,
        draw_order_authority=build_draw_order_authority(draw),
        apex_point=apex_point,
        set_pressure=set_pressure,
        set_health=set_health,
        set_anatomy=set_anatomy,
        sorted_form=sorted_form,
        draw_form=draw_form,
        sorted_style=sorted_style,
        draw_style=draw_style,
        sorted_gaps=sorted_gaps,
        draw_gaps=draw_gaps,
        sorted_relations=sorted_relations,
        draw_relations=draw_relations,
        draw_motion=draw_motion,
        draw_step_motion=build_draw_step_motion(draw),
    )


def selected_draw_indexes(
    draws: list[HistoricalDraw],
    from_date: date | None = None,
    to_date: date | None = None,
    limit: int | None = None,
) -> list[int]:
    indexes = [
        index
        for index, draw in enumerate(draws)
        if (from_date is None or draw.draw_date >= from_date)
        and (to_date is None or draw.draw_date <= to_date)
    ]
    if limit is not None:
        return indexes[:limit]
    return indexes


def build_draw_set_packets(
    draws: list[HistoricalDraw],
    from_date: date | None = None,
    to_date: date | None = None,
    limit: int | None = None,
) -> list[DrawSetPacket]:
    return [
        build_draw_set_packet(draws, index)
        for index in selected_draw_indexes(
            draws,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
        )
    ]


def load_historical_draws(csv_path: Path = DEFAULT_CSV_PATH) -> list[HistoricalDraw]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Powerball CSV not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        draws = [
            historical_draw_from_row(row, row_number)
            for row_number, row in enumerate(reader, start=2)
        ]

    validate_draw_sequence(draws)
    return draws


def historical_powerball_generator(
    csv_path: Path = DEFAULT_CSV_PATH,
) -> Iterator[HistoricalDraw]:
    yield from load_historical_draws(csv_path)


def filter_draws(
    draws: list[HistoricalDraw],
    from_date: date | None = None,
    to_date: date | None = None,
    limit: int | None = None,
) -> list[HistoricalDraw]:
    filtered = [
        draw
        for draw in draws
        if (from_date is None or draw.draw_date >= from_date)
        and (to_date is None or draw.draw_date <= to_date)
    ]
    if limit is not None:
        return filtered[:limit]
    return filtered


def build_foundation_summary(draws: list[HistoricalDraw]) -> dict[str, Any]:
    first = draws[0]
    latest = draws[-1]
    return {
        "schema": "iiw.foundation_summary.v1",
        "draw_count": len(draws),
        "first_draw": first.to_payload(),
        "latest_draw": latest.to_payload(),
        "white_ball_count": WHITE_BALL_COUNT,
        "white_ball_range": [WHITE_BALL_MIN, WHITE_BALL_MAX],
        "powerball_historical_range": [POWERBALL_MIN, POWERBALL_MAX],
        "status": "FOUNDATION_READY",
        "foundation_scope": "draw_history_with_draw_and_sorted_forms",
        "motion_sections": {
            "d2_d5_motion": "inside_current_draw_form",
            "date_motion": "incoming_and_outgoing_by_draw_lane",
        },
        "shared_metrics": {
            "apex_point": {
                "total": "sum of all five white-ball numbers",
                "fp": "finality point; largest white-ball number minus smallest white-ball number",
                "fp_gauge": "fp on the repeating Olympus gauge",
                "total_sum_gauge": "total sum on the repeating Olympus gauge",
            },
            "gap_alphabet": {
                "rule": "1-2 bands from 1 through 70; A-Z then Aa-ii",
                "classes": [
                    {
                        "letter": label,
                        "range": f"{gap_range.start}-{gap_range.stop - 1}",
                    }
                    for gap_range, label in GAP_ALPHABET
                ],
            },
            "set_relations": {
                "rule": "adjacent lane pair plus gap alphabet plus relation class",
                "classes": [
                    {
                        "class": label,
                        "range": f"{class_range.start}-{class_range.stop - 1}",
                    }
                    for class_range, label in RELATION_CLASSES
                ],
            },
            "motion_gauge": {
                "rule": "incoming/outgoing motion uses absolute value on the 1-2 through 69-70 scale; signed motion is preserved separately",
                "zero": {"class": "still", "range": "0"},
                "classes": [
                    {
                        "class": label,
                        "range": f"{gauge_range.start}-{gauge_range.stop - 1}",
                    }
                    for gauge_range, label in MOTION_GAUGE_CLASSES
                ],
            },
            "broad_motion": {
                "rule": "normalized lane or energy magnitude becomes the larger readable motion class",
                "zero": {"class": "Still Motion", "range": "0"},
                "classes": [
                    {
                        "class": label,
                        "range": f"{motion_range.start}-{motion_range.stop - 1}",
                    }
                    for motion_range, label in MOTION_BROAD_CLASSES
                ],
            },
            "path_energy_spectrum": {
                "rule": "path energy average uses the 35-class scale with spectrum-color names",
                "zero": {"class": "Black", "range": "0"},
                "classes": [
                    {
                        "class": label,
                        "range": f"{spectrum_range.start}-{spectrum_range.stop - 1}",
                    }
                    for spectrum_range, label in PATH_ENERGY_SPECTRUM_CLASSES
                ],
            },
            "flow_strength_elements": {
                "rule": "absolute incoming/outgoing difference average uses the 35-class scale with periodic-table names",
                "zero": {"class": "Stable Zero", "range": "0"},
                "classes": [
                    {
                        "class": label,
                        "range": f"{element_range.start}-{element_range.stop - 1}",
                    }
                    for element_range, label in FLOW_STRENGTH_ELEMENT_CLASSES
                ],
            },
            "pressure_shapes": {
                "rule": "set pressure type is the four-sign formation shape",
                "classes": [
                    {"shape": shape, "pressure_type": pressure_type}
                    for shape, pressure_type in PRESSURE_SHAPE_TYPES.items()
                ],
            },
            "pressure_roman_35": {
                "rule": "Set Arc uses Roman numerals for its 35-class gap reference",
                "classes": [
                    {
                        "roman": label,
                        "range": f"{roman_range.start}-{roman_range.stop - 1}",
                    }
                    for roman_range, label in PRESSURE_ROMAN_35
                ],
            },
            "pressure_fusion_constellations": {
                "rule": "sorted pressure and draw pressure describe the same set through redistributed pressure",
                "classes": [
                    {"fusion": fusion, "constellation": constellation}
                    for fusion, constellation in PRESSURE_FUSION_CONSTELLATIONS.items()
                ],
            },
            "set_anatomy": {
                "rule": (
                    "expands Set Health with starter slot, entry edge, S2-S4 "
                    "middle body, exit edge, endpoint slot, and edge-vs-middle pressure"
                ),
                "anatomy_order": [
                    "S1_STARTER_SLOT",
                    "S1_S2_ENTRY_EDGE",
                    "S2_S4_MIDDLE_BODY",
                    "S4_S5_EXIT_EDGE",
                    "S5_ENDPOINT_SLOT",
                ],
            }
        },
        "sections": {
            "sorted": {
                "lanes": [
                    {
                        "lane": lane,
                        "role": role,
                        "allowed_start": allowed_start,
                        "allowed_end": allowed_end,
                    }
                    for lane, role, allowed_start, allowed_end in SORTED_LANES
                ]
            },
            "draw": {
                "lanes": [
                    {
                        "lane": lane,
                        "role": role,
                        "allowed_start": allowed_start,
                        "allowed_end": allowed_end,
                    }
                    for lane, role, allowed_start, allowed_end in DRAW_LANES
                ]
            },
        },
    }


def format_delta(value: int | None) -> str:
    if value is None:
        return "NONE"
    if value > 0:
        return f"+{value}"
    return str(value)


def format_field(label: str, value: Any, indent: int = 2, width: int = 20) -> str:
    return f"{' ' * indent}{label:<{width}}: {value}"


def format_section(title: str) -> list[str]:
    return ["", f"{title}:"]


def format_lane_form(lane: LaneForm) -> str:
    range_status = "OK" if lane.in_lane_range else "OUT_OF_RANGE"
    return (
        f"{lane.lane} {lane.role}: {lane.number} {lane.number_band} "
        f"[{lane.allowed_start}-{lane.allowed_end} {range_status}]"
    )


def format_gap_form(gap: GapForm) -> str:
    return (
        f"{gap.from_lane}->{gap.to_lane}: "
        f"{gap.from_number}->{gap.to_number} "
        f"distance {format_delta(gap.distance)} | "
        f"gap {gap.gap} {gap.gap_letter} [{gap.gap_range}]"
    )


def format_set_relation(relation: SetRelation) -> str:
    return (
        f"{relation.from_lane}->{relation.to_lane} "
        f"({relation.from_role}->{relation.to_role}): "
        f"{relation.from_number}->{relation.to_number} "
        f"distance {format_delta(relation.distance)} | "
        f"gap {relation.gap} {relation.gap_letter} [{relation.gap_range}] | "
        f"class {relation.relation_class} [{relation.relation_class_range}]"
    )


def format_set_style(style: SetStyle) -> str:
    group_parts = [
        f"{group.group_style}({','.join(str(number) for number in group.numbers)})"
        for group in style.groups
    ]
    return (
        f"{style.set_style} | signature={style.set_signature} | "
        f"pattern={style.connected_pattern} | "
        f"groups={style.group_signature} | {' / '.join(group_parts)}"
    )


def format_draw_style(style: DrawStyle) -> str:
    step_parts = [
        f"{step.draw_lane}:{step.draw_number}->{step.sorted_lane}"
        for step in style.steps
    ]
    delta_text = ",".join(format_delta(delta) for delta in style.sorted_position_deltas)
    return (
        f"{style.draw_style} | family={style.draw_style_family} | "
        f"direction={style.direction_pattern} | transfer={style.transfer_pattern} | "
        f"sorted_path={'-'.join(str(position) for position in style.sorted_position_path)} | "
        f"sorted_moves={delta_text} | energy={style.sorted_position_energy} | "
        f"turns={style.turn_count} [{','.join(style.turn_lanes) or 'NONE'}] | "
        f"{' / '.join(step_parts)}"
    )


def format_set_pressure(pressure: SetPressure) -> list[str]:
    sorted_pressure = pressure.sorted_pressure
    draw_pressure = pressure.draw_pressure
    return [
        (
            "Sorted Pressure: "
            f"{sorted_pressure.pressure_type} | "
            f"shape={sorted_pressure.pressure_shape} | "
            f"set_arc={sorted_pressure.set_arc_type} / "
            f"{sorted_pressure.set_arc_family} "
            f"{sorted_pressure.set_arc} "
            f"[{sorted_pressure.set_arc_35}] | "
            f"edge={sorted_pressure.edge_pressure} "
            f"middle={sorted_pressure.middle_pressure} "
            f"middle_minus_edge={format_delta(sorted_pressure.middle_minus_edge)} | "
            f"largest_gap={sorted_pressure.largest_gap} "
            f"{sorted_pressure.largest_gap_relation}"
        ),
        (
            "Draw Pressure: "
            f"{draw_pressure.pressure_type} | "
            f"shape={draw_pressure.pressure_shape} | "
            f"set_arc={draw_pressure.set_arc_type} / "
            f"{draw_pressure.set_arc_family} "
            f"{draw_pressure.set_arc} "
            f"[{draw_pressure.set_arc_35}] | "
            f"path_energy={draw_pressure.draw_path_energy} "
            f"avg={draw_pressure.draw_path_energy_average} "
            f"{draw_pressure.draw_path_energy_class} / "
            f"{draw_pressure.draw_path_energy_spectrum} "
            f"[{draw_pressure.draw_path_energy_spectrum_range}] | "
            f"sorted_energy={draw_pressure.sorted_position_energy} | "
            f"incoming={draw_pressure.incoming_energy} "
            f"avg={draw_pressure.incoming_energy_average} "
            f"{draw_pressure.incoming_energy_class} | "
            f"outgoing={draw_pressure.outgoing_energy} "
            f"avg={draw_pressure.outgoing_energy_average} "
            f"{draw_pressure.outgoing_energy_class} | "
            f"strength={draw_pressure.flow_strength} "
            f"avg={draw_pressure.flow_strength_average} "
            f"{draw_pressure.flow_strength_class} / "
            f"{draw_pressure.flow_strength_element} "
            f"[{draw_pressure.flow_strength_element_range}] | "
            f"flow={draw_pressure.pressure_flow} | "
            f"containment={draw_pressure.containment_state} | "
            f"fusion={draw_pressure.pressure_fusion_profile} | "
            f"fusion_class={draw_pressure.pressure_fusion} "
            f"({draw_pressure.pressure_fusion_constellation})"
        ),
    ]


def print_draw_set_packets(packets: list[DrawSetPacket]) -> None:
    for packet in packets:
        draw = packet.draw
        previous_date = (
            packet.previous_draw.draw_date.isoformat() if packet.previous_draw else "NONE"
        )
        next_date = packet.next_draw.draw_date.isoformat() if packet.next_draw else "NONE"
        lines = [
            "=" * 72,
            "Infinite Inner World Packet",
            "=" * 72,
            "",
            "Draw:",
            format_field("Date", draw.draw_date.isoformat()),
            format_field("Index", draw.draw_index),
            format_field("White Balls", list(draw.white_balls)),
            format_field("Sorted White", list(draw.sorted_white_balls)),
            format_field("Powerball", draw.powerball),
            format_field("Power Play", draw.powerplay if draw.powerplay is not None else "NONE"),
            "",
            "Continuity:",
            format_field("Previous", previous_date),
            format_field("Current", draw.draw_date.isoformat()),
            format_field("Next", next_date),
            "",
            "Draw Order Authority:",
            format_field("Status", packet.draw_order_authority.authority_status),
            format_field(
                "Trusted Start",
                packet.draw_order_authority.authority_start_date.isoformat(),
            ),
            format_field(
                "Trusted",
                "YES" if packet.draw_order_authority.is_trusted_draw_order else "NO",
            ),
            "",
            "Apex Point:",
            format_field("Total", packet.apex_point.total),
            format_field(
                "Total Gauge",
                f"{packet.apex_point.total_sum_gauge} "
                f"[{packet.apex_point.total_sum_gauge_range}]",
            ),
            format_field(
                "FP",
                f"{packet.apex_point.fp} "
                f"({packet.apex_point.largest_number}-{packet.apex_point.smallest_number})",
            ),
            format_field(
                "FP Gauge",
                f"{packet.apex_point.fp_gauge} [{packet.apex_point.fp_gauge_range}]",
            ),
            "",
            "Set Health:",
            format_field("Health", packet.set_health.set_health),
            format_field(
                "Parts",
                (
                    f"{packet.set_health.pressure_tone} | "
                    f"{packet.set_health.core_band} | "
                    f"{packet.set_health.middle_entry_bridge} | "
                    f"{packet.set_health.middle_bridge_exit} | "
                    f"{packet.set_health.endpoint_band}"
                ),
            ),
            "",
            "Set Anatomy:",
            format_field("Signature", packet.set_anatomy.technical_signature),
            format_field(
                "Starter",
                (
                    f"{packet.set_anatomy.starter_slot} | "
                    f"{packet.set_anatomy.starter_number} "
                    f"{packet.set_anatomy.starter_band}"
                ),
            ),
            format_field(
                "Entry Edge",
                (
                    f"{packet.set_anatomy.entry_relation} | "
                    f"gap={packet.set_anatomy.entry_gap} "
                    f"{packet.set_anatomy.entry_gap_class}"
                ),
            ),
            format_field(
                "Middle Body",
                (
                    f"{packet.set_anatomy.middle_body} | "
                    f"span={packet.set_anatomy.middle_span} | "
                    f"zone={packet.set_anatomy.middle_zone} | "
                    f"{packet.set_anatomy.middle_pressure}"
                ),
            ),
            format_field("Middle Slots", packet.set_anatomy.middle_slot_signature),
            format_field(
                "Exit Edge",
                (
                    f"{packet.set_anatomy.exit_relation} | "
                    f"gap={packet.set_anatomy.exit_gap} "
                    f"{packet.set_anatomy.exit_gap_class}"
                ),
            ),
            format_field(
                "Edge Read",
                (
                    f"{packet.set_anatomy.edge_form} | "
                    f"{packet.set_anatomy.edge_balance} | "
                    f"{packet.set_anatomy.edge_pressure}"
                ),
            ),
            format_field(
                "Endpoint",
                (
                    f"{packet.set_anatomy.endpoint_slot} | "
                    f"{packet.set_anatomy.endpoint_number} "
                    f"{packet.set_anatomy.endpoint_band}"
                ),
            ),
            format_field("Full Relation", packet.set_anatomy.full_set_relation),
            "",
            "Set Pressure:",
        ]
        for line in format_set_pressure(packet.set_pressure):
            lines.append(f"  {line}")
        lines.extend(format_section("Sorted Side"))
        lines.append(format_field("Style", format_set_style(packet.sorted_style)))
        lines.append("  Form:")
        for lane in packet.sorted_form:
            lines.append(f"    {format_lane_form(lane)}")
        lines.append("  Gaps:")
        for gap in packet.sorted_gaps:
            lines.append(f"    {format_gap_form(gap)}")
        lines.append("  Relations:")
        for relation in packet.sorted_relations:
            lines.append(f"    {format_set_relation(relation)}")
        lines.extend(format_section("Draw Side"))
        lines.append(format_field("Style", format_draw_style(packet.draw_style)))
        lines.append("  Form:")
        for lane in packet.draw_form:
            lines.append(f"    {format_lane_form(lane)}")
        lines.append("  Gaps:")
        for gap in packet.draw_gaps:
            lines.append(f"    {format_gap_form(gap)}")
        lines.append("  Relations:")
        for relation in packet.draw_relations:
            lines.append(f"    {format_set_relation(relation)}")
        lines.extend(format_section("Motion"))
        lines.append("  D2-D5:")
        for motion in packet.draw_step_motion:
            lines.append(
                f"    {motion.from_lane}->{motion.lane} "
                f"({motion.from_role}->{motion.role}): "
                f"{motion.from_number}->{motion.to_number} "
                f"{format_delta(motion.distance)}"
            )
        lines.append("  Date Motion:")
        for motion in packet.draw_motion:
            lines.append(
                f"    {motion.lane} {motion.role}: "
                f"incoming_motion {format_delta(motion.incoming_motion)} "
                f"{motion.incoming_motion_class} / "
                f"{motion.incoming_motion_gauge} [{motion.incoming_motion_gauge_range}] | "
                f"outgoing_motion {format_delta(motion.outgoing_motion)} "
                f"{motion.outgoing_motion_class} / "
                f"{motion.outgoing_motion_gauge} [{motion.outgoing_motion_gauge_range}]"
            )
        lines.append("-" * 72)
        print("\n".join(lines))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Infinite Inner World",
        description=(
            "Clean-slate Infinite Inner World foundation. This version only loads, "
            "validates, filters, and prints Powerball draw history."
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
        help="Optional start date, for example 2026-01-01 or 1/1/2026.",
    )
    parser.add_argument(
        "--to-date",
        help="Optional end date, for example 2026-06-17 or 6/17/2026.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional number of rows to print after date filtering.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a JSON foundation summary instead of draw rows.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print draw and sorted form packets as JSON.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.limit is not None and args.limit < 1:
        raise ValueError("--limit must be at least 1.")

    from_date = parse_draw_date(args.from_date) if args.from_date else None
    to_date = parse_draw_date(args.to_date) if args.to_date else None
    if from_date and to_date and to_date < from_date:
        raise ValueError("--to-date must be the same as or later than --from-date.")

    draws = load_historical_draws(args.csv_path)

    if args.summary:
        print(
            json.dumps(
                build_foundation_summary(
                    filter_draws(
                        draws,
                        from_date=from_date,
                        to_date=to_date,
                        limit=args.limit,
                    )
                ),
                indent=2,
            )
        )
        return

    packets = build_draw_set_packets(
        draws,
        from_date=from_date,
        to_date=to_date,
        limit=args.limit,
    )
    if args.json:
        print(json.dumps([packet.to_payload() for packet in packets], indent=2))
        return

    print_draw_set_packets(packets)


if __name__ == "__main__":
    main()
