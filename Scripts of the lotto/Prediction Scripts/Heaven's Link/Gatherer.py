from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
HEAVENS_LINK_DIR = SCRIPT_PATH.parent
REALITY_MARBLE_SCRIPTS_DIR = HEAVENS_LINK_DIR.parent
IIW_PATH = REALITY_MARBLE_SCRIPTS_DIR / "Infinite_Inner_World.py"
SEATS = ("S1", "S2", "S3", "S4", "S5")


def packet_id(prefix: str, payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return f"{prefix}-{hashlib.sha1(raw).hexdigest()[:12]}"


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


IIW = load_module("serenity_gatherer_iiw", IIW_PATH)


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value or "").strip().replace(",", "")))
    except ValueError:
        return default


def valid_number(value: Any) -> bool:
    number = parse_int(value)
    return 1 <= number <= 69


def unique_numbers(values: Any) -> list[int]:
    numbers: list[int] = []
    for value in values or []:
        number = parse_int(value)
        if 1 <= number <= 69 and number not in numbers:
            numbers.append(number)
    return sorted(numbers)


def number_range(payload: dict[str, Any] | None) -> list[int]:
    payload = payload or {}
    low = parse_int(payload.get("min"))
    high = parse_int(payload.get("max"))
    if not (1 <= low <= 69 and 1 <= high <= 69):
        return []
    low, high = min(low, high), max(low, high)
    return list(range(low, high + 1))


def precise_answer(voice_of_hope_packet: dict[str, Any] | None) -> dict[str, Any]:
    return (voice_of_hope_packet or {}).get("precise_question_answer") or {}


def question_template(voice_of_hope_packet: dict[str, Any] | None) -> dict[str, Any]:
    voice_of_hope_packet = voice_of_hope_packet or {}
    precise = precise_answer(voice_of_hope_packet)
    sorted_answer = precise.get("sorted_seat_answer") or {}
    seat_templates: dict[str, dict[str, Any]] = {}
    for seat in SEATS:
        row = sorted_answer.get(seat) or {}
        seat_templates[seat] = {
            "seat": seat,
            "draw_lane": row.get("draw_lane"),
            "draw_lane_role": row.get("draw_lane_role"),
            "source_sorted_seat": row.get("source_sorted_seat"),
            "source_number": row.get("source_number"),
            "required_caste": row.get("required_caste"),
            "side_bias": row.get("side_bias"),
            "selected_delta": row.get("selected_delta"),
            "exact_number": parse_int(row.get("projected_number")) if valid_number(row.get("projected_number")) else None,
            "side_values": unique_numbers(row.get("side_projected_values") or []),
            "range_values": unique_numbers(number_range(row.get("projected_range") or {})),
            "projected_range": row.get("projected_range") or {},
        }
    return {
        "schema": "serenity.life_link.gatherer.question_template.v1",
        "status": "QUESTION_TEMPLATE_READY" if any(t.get("range_values") or t.get("side_values") for t in seat_templates.values()) else "QUESTION_TEMPLATE_EMPTY",
        "answer_identity": voice_of_hope_packet.get("answer_identity") or {},
        "delta_mode": precise.get("delta_mode"),
        "selected_delta_draw_order": precise.get("selected_delta_draw_order") or [],
        "projected_sorted_body": [parse_int(value) for value in precise.get("projected_sorted_body") or []],
        "voice_set_health_reflection": precise.get("voice_set_health_reflection") or {},
        "seat_templates": seat_templates,
        "law": "The Gatherer uses the Voice/Question template as the body-creation foreground. Garden only provides available bodies.",
    }


def body_key(body: list[int]) -> str:
    return "-".join(str(int(value)) for value in body)


def technical_body(body: list[int]) -> dict[str, Any]:
    if len(body) != 5 or any(not (1 <= int(value) <= 69) for value in body):
        return {"status": "NO_TECHNICAL_BODY"}
    return json.loads(json.dumps(IIW.build_full_set_technical_body(body)))


def technical_fit(body_technical: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    reflection = template.get("voice_set_health_reflection") or {}
    checks = [
        ("set_health", body_technical.get("middle_health"), reflection.get("set_health"), 18.0),
        ("full_set_relation", body_technical.get("full_relation"), reflection.get("full_set_relation"), 18.0),
        ("s1_starter_signature", body_technical.get("s1_signature"), reflection.get("s1_starter_signature"), 8.0),
        ("s5_endpoint_signature", body_technical.get("s5_signature"), reflection.get("s5_endpoint_signature"), 8.0),
        ("s2_middle_slot_signature", body_technical.get("s2_middle_slot_signature"), reflection.get("s2_middle_slot_signature"), 6.0),
        ("s3_middle_slot_signature", body_technical.get("s3_middle_slot_signature"), reflection.get("s3_middle_slot_signature"), 6.0),
        ("s4_middle_slot_signature", body_technical.get("s4_middle_slot_signature"), reflection.get("s4_middle_slot_signature"), 6.0),
    ]
    score = 0.0
    matches: list[str] = []
    misses: list[str] = []
    for name, actual, expected, weight in checks:
        if not expected:
            continue
        if actual == expected:
            score += weight
            matches.append(name)
        else:
            misses.append(f"{name}:{actual}!={expected}")
    return {
        "score": round(score, 6),
        "matches": matches,
        "misses": misses,
    }


def seat_fit(seat: str, value: int, template: dict[str, Any]) -> dict[str, Any]:
    seat_template = (template.get("seat_templates") or {}).get(seat) or {}
    exact = seat_template.get("exact_number")
    side_values = set(seat_template.get("side_values") or [])
    range_values = set(seat_template.get("range_values") or [])
    score = 0.0
    reasons: list[str] = []
    if exact and value == exact:
        score += 100.0
        reasons.append("exact_projected_number")
    if value in side_values:
        score += 50.0
        reasons.append("side_projected_value")
    if value in range_values:
        score += 20.0
        reasons.append("projected_range_value")
    if not reasons:
        score -= 25.0
        reasons.append("outside_question_template")
    return {
        "seat": seat,
        "number": value,
        "score": round(score, 6),
        "reasons": reasons,
        "template": seat_template,
    }


def score_body(body: list[int], template: dict[str, Any]) -> dict[str, Any]:
    seat_rows = [
        seat_fit(seat, int(body[index]), template)
        for index, seat in enumerate(SEATS)
    ]
    body_technical = technical_body(body)
    tech_fit = technical_fit(body_technical, template)
    exact_template = [parse_int(value) for value in template.get("projected_sorted_body") or []]
    exact_body_bonus = 250.0 if exact_template == body else 0.0
    sorted_bonus = 25.0 if body == sorted(body) and len(set(body)) == 5 else -100.0
    score = (
        sum(float(row.get("score") or 0.0) for row in seat_rows)
        + float(tech_fit.get("score") or 0.0)
        + exact_body_bonus
        + sorted_bonus
    )
    reasons = []
    if exact_body_bonus:
        reasons.append("matches_voice_projected_sorted_body")
    if sorted_bonus > 0:
        reasons.append("legal_sorted_unique_body")
    return {
        "sorted_body": body,
        "body_key": body_key(body),
        "gatherer_score": round(score, 6),
        "seat_template_fit": seat_rows,
        "technical_template_fit": tech_fit,
        "technical_body": body_technical,
        "reasons": reasons,
    }


def garden_bodies(garden_of_life_packet: dict[str, Any] | None) -> list[list[int]]:
    universe = (garden_of_life_packet or {}).get("answer_body_universe") or {}
    bodies: list[list[int]] = []
    for row in universe.get("bodies") or []:
        body = [parse_int(value) for value in row]
        if len(body) == 5 and body == sorted(body) and len(set(body)) == 5 and all(1 <= value <= 69 for value in body):
            bodies.append(body)
    return bodies


def build_gatherer_packet(
    garden_of_life_packet: dict[str, Any] | None,
    voice_of_hope_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    garden_of_life_packet = garden_of_life_packet or {}
    voice_of_hope_packet = voice_of_hope_packet or {}
    template = question_template(voice_of_hope_packet)
    bodies = garden_bodies(garden_of_life_packet)
    gathered = sorted(
        [score_body(body, template) for body in bodies],
        key=lambda row: (-float(row.get("gatherer_score") or 0.0), row.get("body_key") or ""),
    )
    leader = gathered[0] if gathered else {}
    output = {
        "schema": "serenity.life_link.gatherer.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "GATHERER_READY" if gathered else "GATHERER_EMPTY",
        "canonical_name": "The Gatherer",
        "input_law": "Garden of Life creates the available body universe; Voice/Question template decides fit.",
        "source_packet_ids": [
            garden_of_life_packet.get("packet_id"),
            voice_of_hope_packet.get("packet_id"),
        ],
        "answer_identity": voice_of_hope_packet.get("answer_identity") or {},
        "question_template": template,
        "garden_pool": (garden_of_life_packet.get("reduction") or {}).get("attractor_pool") or [],
        "garden_lane_lists": (garden_of_life_packet.get("reduction") or {}).get("answer_lane_lists") or {},
        "garden_body_count": len(bodies),
        "gathered_body_count": len(gathered),
        "gathered_bodies": gathered,
        "leader_body": leader.get("sorted_body"),
        "leader_body_key": leader.get("body_key"),
        "leader_score": leader.get("gatherer_score"),
        "downstream_policy": {
            "stage20_role": "USE_GATHERER_BODIES_BEFORE_ANY_BROAD_POOL",
            "hard_filter": "GATHERER_BODY_UNIVERSE_ONLY",
        },
        "law": (
            "The Gatherer does not invent numbers, expand ranges, or search history. "
            "It creates/ranks bodies from Garden using the full Voice/Question template."
        ),
    }
    output["packet_id"] = packet_id("gatherer", output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Build The Gatherer packet from Garden of Life and Voice of Hope.")
    parser.add_argument("--garden", required=True, help="Path to Garden of Life packet JSON.")
    parser.add_argument("--voice", required=True, help="Path to Voice of Hope packet JSON.")
    parser.add_argument("--output", required=True, help="Path to write Gatherer packet JSON.")
    args = parser.parse_args()
    garden = json.loads(Path(args.garden).read_text(encoding="utf-8"))
    voice = json.loads(Path(args.voice).read_text(encoding="utf-8"))
    packet = build_gatherer_packet(garden, voice)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(f"Wrote Gatherer packet: {output}")


if __name__ == "__main__":
    main()
