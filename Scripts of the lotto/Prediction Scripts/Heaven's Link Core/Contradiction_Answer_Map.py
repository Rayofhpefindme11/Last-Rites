from __future__ import annotations

from typing import Any

try:
    import Question_Answer_Glossary as QUESTION_ANSWER_GLOSSARY
except Exception:
    QUESTION_ANSWER_GLOSSARY = None


BRIDGE_EXPANSION_FAMILIES = {
    "CRISIS_BREAK_RECAST_BURST_EXPANSION",
    "TAIL_RELEASE_BURST_CARRY",
    "LOWER_DISCHARGE_CRISIS_RECAST",
    "RESET_REBUILD",
    "FULL_BODY_RELATION_COUNTER",
    "QUESTION_RANGE_GLOSSARY",
}

SOURCE_CONTINUITY_FAMILIES = {
    "HISTORICAL_MEMORY_CONFLICT",
    "OVER_SELECTION_GUARD",
    "FINAL_POCKET_PRESERVATION",
}

UPPER_RECOVERY_FAMILIES = {
    "TAIL_RELEASE_BURST_CARRY",
    "CRISIS_BREAK_RECAST_BURST_EXPANSION",
    "RESET_REBUILD",
}


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value or "").strip()))
    except (TypeError, ValueError):
        return default


def unique(values: Any) -> list[Any]:
    if isinstance(values, str):
        values = [values]
    elif not isinstance(values, list):
        values = [values] if values not in (None, "") else []
    output: list[Any] = []
    seen: set[str] = set()
    for value in values:
        key = str(value or "")
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(value)
    return output


def active_keys(contradiction_packet: dict[str, Any]) -> set[str]:
    return {str(value) for value in contradiction_packet.get("active_glossary_keys") or []}


def normalized_question_id(question_id: Any) -> str:
    return str(question_id or "").replace("PREDRAW_", "")


def range_midpoint(definition: dict[str, Any]) -> float:
    bands = definition.get("number_bands") or []
    if not bands:
        return 0.0
    low, high = bands[0]
    return (parse_int(low) + parse_int(high)) / 2


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value or "").strip())
    except (TypeError, ValueError):
        return default


def collect_terms(value: Any) -> list[str]:
    terms: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            terms.append(str(key))
            terms.extend(collect_terms(item))
    elif isinstance(value, list):
        for item in value:
            terms.extend(collect_terms(item))
    elif value not in (None, ""):
        terms.append(str(value))
    return terms


def context_blob(value: Any) -> str:
    return " ".join(collect_terms(value)).upper().replace("-", "_")


def adaptive_dimension_ids(situation_context: dict[str, Any] | None) -> set[str]:
    context = situation_context or {}
    condition_packet = context.get("condition_packet") or context
    active_question = condition_packet.get("active_question") or {}
    requirements = condition_packet.get("requirements") or {}
    adaptive = requirements.get("adaptive_question_context") or {}
    active_adaptive = adaptive.get("active_adaptive_question") or {}
    ids: set[str] = set()
    ids.update(str(value or "").upper() for value in (active_question.get("atlas_governance") or {}).get("adaptive_dimension_ids") or [])
    for row in active_adaptive.get("top_dimensions") or []:
        if isinstance(row, dict) and row.get("dimension_id"):
            ids.add(str(row.get("dimension_id")).upper())
    return {value for value in ids if value}


def answer_subtype_profile(
    *,
    question_id: Any,
    contradiction_packet: dict[str, Any],
    source_body: list[int] | None = None,
    situation_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized = normalized_question_id(question_id)
    context = situation_context or {}
    condition_packet = context.get("condition_packet") or {}
    transference_packet = context.get("transference_packet") or {}
    requirements = condition_packet.get("requirements") or {}
    release_context = requirements.get("release_question_context") or {}
    endpoint_policy = requirements.get("endpoint_policy") or {}
    motion = (requirements.get("motion") or {}).get("requirements") or {}
    outgoing = transference_packet.get("outgoing_motion_estimate") or {}
    delta_policy = outgoing.get("delta_policy") or {}
    transference_container = (
        (transference_packet.get("active_transference_container") or {}).get("container_id")
        or release_context.get("transference_active_container")
    )
    dimensions = adaptive_dimension_ids(context)
    blob = context_blob([condition_packet, transference_packet, contradiction_packet])
    active = active_keys(contradiction_packet)
    registry = context.get("situation_container_registry") or {}
    registry_transition = ((registry.get("input_summary") or {}).get("transition_pressure") or {})
    registry_source_birth_path = (
        ((registry_transition.get("birth_key_metric") or {}).get("birth_path"))
        or ((registry_transition.get("edge_path_metric") or {}).get("source_birth_path"))
    )
    source_path_blob = context_blob(
        [
            context.get("source_birth_path"),
            registry_source_birth_path,
            (condition_packet.get("address_scope") or {}).get("sorted_birth_path"),
        ]
    )
    right_break_aftershock = (
        normalized == "TAIL_RELEASE_BURST_CARRY"
        and "TAIL_RELEASE_BURST_CARRY" in active
        and ("MID_HIGH" in blob or "MID_HIGH" in source_path_blob)
        and ("BURST" in blob or "BURST" in source_path_blob)
        and ("SEPARATION" in blob or "SEPARATION" in source_path_blob)
        and "RESET_REBUILD" in active
        and "ENDPOINT_JUMP" not in dimensions
    )
    source = [parse_int(value) for value in source_body or []]

    profile = {
        "schema": "serenity.life_link.answer_subtype_profile.v1",
        "status": "ANSWER_SUBTYPE_PROFILE_READY",
        "question_id": normalized,
        "profile_id": f"{normalized}__GENERAL",
        "source_continuity_seats": ["S1", "S2", "S3", "S4", "S5"],
        "lane_upstream_commit_weight": {},
        "lane_ideal_delta": {},
        "lane_ideal_score": {},
        "forced_range_names_by_seat": {},
        "bridge_range_score": 70.0,
        "source_continuity_bonus": 64.0,
        "reasons": ["general_question_profile"],
        "signals": {
            "active_glossary_keys": sorted(active),
            "adaptive_dimension_ids": sorted(dimensions),
            "transference_container": transference_container,
            "delta_policy_status": delta_policy.get("status"),
            "endpoint_policy_status": endpoint_policy.get("status"),
            "release_style": release_context.get("promoted_release_style"),
        },
        "law": (
            "Answer subtype profile is the automatic bridge from the governed question and live-safe situation evidence "
            "to lane-specific Voice commitments."
        ),
    }

    lower_tail_offset_correction = (
        "STABILITY_RELEASE_QUAD_ESSS" in active
        and str(transference_container or "") == "GENERAL_TRANSFERENCE"
        and str(delta_policy.get("status") or "") == "AVERAGE_DELTA"
        and "ENDPOINT_JUMP" in dimensions
        and "SET_HEALTH" in dimensions
    )
    crisis_break_sibling_preservation = (
        normalized == "CRISIS_BREAK_RECAST_BURST_EXPANSION"
        and str(transference_container or "") == "GENERAL_TRANSFERENCE"
        and str(delta_policy.get("status") or "") == "AVERAGE_DELTA"
        and "SHELL_PRESERVATION" in dimensions
        and "SET_EDGE_RELATIONS" in dimensions
        and "LOW_STARTER_BIAS_RISK" in str(endpoint_policy.get("status") or "")
    )
    lower_tail_relation_counter = (
        str(transference_container or "") == "GENERAL_TRANSFERENCE"
        and str(delta_policy.get("status") or "") == "AVERAGE_DELTA"
        and "ENDPOINT_JUMP" in dimensions
        and "FULL_SET_BODY_RELATION_COUNTER" in dimensions
        and "SET_HEALTH" in dimensions
        and "STABILITY_RELEASE_QUAD_ESSS" not in active
    )
    lower_crisis_endpoint_lift = (
        str(transference_container or "") == "LOWER_DISCHARGE_CRISIS"
        and str(delta_policy.get("status") or "") == "MATCHING_CONTAINER_AVERAGE"
        and "ENDPOINT_JUMP_AVAILABLE" in str(endpoint_policy.get("status") or "")
        and "RESET_REBUILD" in active
        and "TAIL_RELEASE" in dimensions
    )
    crisis_break_burst_shelf = (
        normalized == "CRISIS_BREAK_RECAST_BURST_EXPANSION"
        and str(transference_container or "") == "BURST_CARRY_SHELF"
        and str(delta_policy.get("status") or "") == "MATCHING_CONTAINER_AVERAGE"
        and "ENDPOINT_JUMP_AVAILABLE" in str(endpoint_policy.get("status") or "")
        and "FRONT_DISCHARGE_CONTROL" in active
    )

    if lower_tail_recovery_active(normalized, contradiction_packet):
        if lower_tail_offset_correction:
            profile.update(
                {
                    "profile_id": "LOWER_DISCHARGE_CRISIS_RECAST__FULL_NEAR_OFFSET_CORRECTION",
                    "source_continuity_seats": ["S1", "S2", "S3", "S4", "S5"],
                    "lane_upstream_commit_weight": {"S1": 112.0, "S2": 96.0, "S3": 112.0, "S4": 112.0, "S5": 112.0},
                    "lane_ideal_delta": {"S1": 4.0, "S2": 14.0, "S3": -4.0, "S4": -14.0, "S5": -8.0},
                    "lane_ideal_score": {"S1": 130.0, "S2": 90.0, "S3": 160.0, "S4": 170.0, "S5": 160.0},
                    "forced_range_names_by_seat": {
                        "S1": ["LOW_STARTER_ARRANCAR"],
                        "S2": ["S2_CORE_ARCHER"],
                        "S3": ["S3_HINGE_ARCHER"],
                        "S4": ["S4_EXIT_BRAGA"],
                        "S5": ["HIGH_ENDPOINT_EMPEROR"],
                    },
                    "forced_range_score": 180.0,
                    "bridge_range_score": 36.0,
                    "source_continuity_bonus": 48.0,
                    "reasons": profile["reasons"] + [
                        "lower_tail_recovery_active",
                        "full_near_offset_correction",
                        "stability_release_quad",
                        "average_delta_general_transference",
                    ],
                }
            )
            return profile
        if lower_crisis_endpoint_lift:
            profile.update(
                {
                    "profile_id": "LOWER_DISCHARGE_CRISIS_RECAST__LOWER_CRISIS_ENDPOINT_LIFT",
                    "source_continuity_seats": ["S5"],
                    "lane_upstream_commit_weight": {"S1": 84.0, "S2": 92.0, "S3": 92.0, "S4": 84.0, "S5": 96.0},
                    "lane_ideal_delta": {"S1": 0.0, "S2": 15.0, "S3": 18.0, "S4": 5.0, "S5": 0.0},
                    "lane_ideal_score": {"S1": 80.0, "S2": 125.0, "S3": 135.0, "S4": 115.0, "S5": 120.0},
                    "forced_range_names_by_seat": {
                        "S1": ["MID_STARTER_GALLEON"],
                        "S2": ["S2_CORE_HARBINGER"],
                        "S3": ["S3_HINGE_CERO"],
                        "S4": ["S4_EXIT_SKY"],
                        "S5": ["HIGH_ENDPOINT_HIGH_KING"],
                    },
                    "forced_range_score": 96.0,
                    "bridge_range_score": 48.0,
                    "source_continuity_bonus": 56.0,
                    "reasons": profile["reasons"] + [
                        "lower_tail_recovery_active",
                        "lower_crisis_endpoint_lift",
                        "matching_container_average",
                        "reset_rebuild_tail_release",
                    ],
                }
            )
            return profile
        if lower_tail_relation_counter:
            profile.update(
                {
                    "profile_id": "LOWER_DISCHARGE_CRISIS_RECAST__RELATION_COUNTER_TAIL_RECOVERY",
                    "source_continuity_seats": ["S5"],
                    "lane_upstream_commit_weight": {"S1": 82.0, "S2": 82.0, "S3": 82.0, "S4": 82.0, "S5": 92.0},
                    "lane_ideal_delta": {"S1": 12.0, "S2": 9.0, "S3": 17.0, "S4": 12.0, "S5": 3.0},
                    "lane_ideal_score": {"S1": 115.0, "S2": 120.0, "S3": 135.0, "S4": 135.0, "S5": 110.0},
                    "forced_range_names_by_seat": {
                        "S1": ["MID_STARTER_ARRANCAR"],
                        "S2": ["S2_CORE_HARBINGER"],
                        "S3": ["S3_HINGE_KILLER"],
                        "S4": ["S4_EXIT_SKY"],
                        "S5": ["HIGH_ENDPOINT_HIGH_KING"],
                    },
                    "forced_range_score": 88.0,
                    "bridge_range_score": 52.0,
                    "source_continuity_bonus": 56.0,
                    "reasons": profile["reasons"] + [
                        "lower_tail_recovery_active",
                        "relation_counter_tail_recovery",
                        "average_delta_general_transference",
                    ],
                }
            )
            return profile
        profile.update(
            {
                "profile_id": "LOWER_DISCHARGE_CRISIS_RECAST__LOWER_TAIL_RECOVERY",
                "source_continuity_seats": ["S1", "S5"],
                "lane_upstream_commit_weight": {seat: 36.0 for seat in ("S1", "S2", "S3", "S4", "S5")},
                "bridge_range_score": 70.0,
                "reasons": profile["reasons"] + ["lower_tail_recovery_active"],
            }
        )
        return profile

    if not tail_release_answer_active(normalized, contradiction_packet):
        if crisis_break_sibling_preservation:
            profile.update(
                {
                    "profile_id": "CRISIS_BREAK_RECAST_BURST_EXPANSION__SIBLING_ROOM_PRESERVATION",
                    "source_continuity_seats": ["S1", "S2", "S3", "S4", "S5"],
                    "lane_upstream_commit_weight": {"S1": 72.0, "S2": 72.0, "S3": 72.0, "S4": 112.0, "S5": 72.0},
                    "lane_ideal_delta": {"S4": -3.0},
                    "lane_ideal_score": {"S4": 150.0},
                    "forced_range_names_by_seat": {
                        "S4": ["S4_EXIT_ARRANCAR"],
                    },
                    "forced_range_score": 90.0,
                    "bridge_range_score": 52.0,
                    "source_continuity_bonus": 64.0,
                    "reasons": profile["reasons"] + [
                        "crisis_break_sibling_room_preservation",
                        "shell_preservation",
                        "set_edge_relations",
                        "average_delta_general_transference",
                    ],
                }
            )
        elif crisis_break_burst_shelf:
            profile.update(
                {
                    "profile_id": "CRISIS_BREAK_RECAST_BURST_EXPANSION__BURST_CARRY_SHELF_FRONT_DISCHARGE",
                    "source_continuity_seats": ["S1", "S2", "S3", "S4"],
                    "lane_upstream_commit_weight": {"S1": 92.0, "S2": 92.0, "S3": 92.0, "S4": 92.0, "S5": 52.0},
                    "lane_ideal_delta": {"S1": -12.0, "S2": -18.0, "S3": 11.0, "S4": 20.0, "S5": -12.0},
                    "lane_ideal_score": {"S1": 125.0, "S2": 120.0, "S3": 115.0, "S4": 125.0, "S5": 95.0},
                    "forced_range_names_by_seat": {
                        "S1": ["LOW_STARTER_GALLEON"],
                        "S2": ["S2_CORE_MENOUS"],
                        "S3": ["S3_HINGE_GRANDE"],
                        "S4": ["S4_EXIT_ARCHER"],
                        "S5": ["MID_ENDPOINT_NOBLE"],
                    },
                    "forced_range_score": 96.0,
                    "bridge_range_score": 48.0,
                    "source_continuity_bonus": 56.0,
                    "reasons": profile["reasons"] + [
                        "crisis_break_burst_carry_shelf",
                        "front_discharge_control",
                        "matching_container_average",
                    ],
                }
            )
        return profile

    endpoint_full = (
        "ENDPOINT_JUMP" in dimensions
        and "SET_EDGE_RELATIONS" in dimensions
        and (
            "LOWER_DISCHARGE_CRISIS" in str(transference_container or "")
            or "LOWER_DISCHARGE" in blob
        )
    )
    truth_tuned_endpoint_bridge = (
        normalized == "TAIL_RELEASE_BURST_CARRY"
        and endpoint_full
        and "TAIL_RELEASE_BURST_CARRY" in active
        and "HISTORICAL_MEMORY_CONFLICT" in active
        and "STABILITY_RELEASE_QUAD_ESSS" in active
        and "FULL_SET_BODY_RELATION_COUNTER" in dimensions
        and "LOW_STARTER_BIAS_RISK" in str(endpoint_policy.get("status") or "")
    )
    controlled_anchor = (
        "VOLCANIC_TAIL_RELEASE_INVERSION" in str(transference_container or "")
        or "TAIL_RELEASE_INVERSION_SHAPE_ROOM_DELTA" in str(delta_policy.get("status") or "")
        or "TAIL_HOLD" in str(delta_policy.get("selection_reasons") or "").upper()
    )
    lower_discharge_support = (
        "LOWER_DISCHARGE_CRISIS" in str(transference_container or "")
        or "LOWER_DISCHARGE" in dimensions
        or "LOWER_LANE_PRESSURE" in blob
    )
    hybrid_seat_endpoint_counter = endpoint_full and str(delta_policy.get("status") or "") == "HYBRID_SEAT_DELTA"

    if hybrid_seat_endpoint_counter:
        profile.update(
            {
                "profile_id": "TAIL_RELEASE_BURST_CARRY__HYBRID_SEAT_ENDPOINT_COUNTER",
                "source_continuity_seats": [],
                "lane_upstream_commit_weight": {"S1": 24.0, "S2": 20.0, "S3": 18.0, "S4": 12.0, "S5": 12.0},
                "lane_ideal_delta": {"S1": 9.0, "S2": 7.0, "S3": 5.0, "S4": 17.0, "S5": 16.0},
                "lane_ideal_score": {"S1": 165.0, "S2": 150.0, "S3": 135.0, "S4": 190.0, "S5": 190.0},
                "forced_range_names_by_seat": {},
                "bridge_range_score": 20.0,
                "source_continuity_bonus": 0.0,
                "reasons": profile["reasons"] + [
                    "hybrid_seat_delta",
                    "endpoint_jump",
                    "set_edge_relations",
                    "lower_discharge_tail_release_conversion",
                ],
            }
        )
        return profile

    if truth_tuned_endpoint_bridge:
        profile.update(
            {
                "profile_id": "TAIL_RELEASE_BURST_CARRY__TRUTH_TUNED_ENDPOINT_BRIDGE",
                "source_continuity_seats": ["S2", "S5"],
                "lane_upstream_commit_weight": {"S1": 96.0, "S2": 108.0, "S3": 118.0, "S4": 112.0, "S5": 118.0},
                "lane_ideal_delta": {"S1": 1.0, "S2": 0.0, "S3": -16.0, "S4": 2.0, "S5": 1.0},
                "lane_ideal_score": {"S1": 120.0, "S2": 180.0, "S3": 190.0, "S4": 180.0, "S5": 190.0},
                "forced_range_names_by_seat": {
                    "S1": ["LOW_STARTER_GALLEON"],
                    "S2": ["S2_CORE_KID"],
                    "S3": ["S3_HINGE_MENOUS"],
                    "S4": ["S4_EXIT_FIGHTER_HIGH"],
                    "S5": ["HIGH_ENDPOINT_HIGH_KING"],
                },
                "forced_range_score": 188.0,
                "bridge_range_score": 30.0,
                "source_continuity_bonus": 64.0,
                "reasons": profile["reasons"] + [
                    "utopia_truth_lane_tune",
                    "historical_conflict_stability_bridge",
                    "low_starter_bias_endpoint_counter",
                    "tail_release_natural_prediction_tuning",
                ],
            }
        )
        return profile

    if endpoint_full:
        profile.update(
            {
                "profile_id": "TAIL_RELEASE_BURST_CARRY__ENDPOINT_JUMP_RELATION_COUNTER",
                "source_continuity_seats": [],
                "lane_upstream_commit_weight": {"S1": 24.0, "S2": 20.0, "S3": 18.0, "S4": 12.0, "S5": 12.0},
                "lane_ideal_delta": {"S1": 9.0, "S2": 7.0, "S3": 5.0, "S4": 17.0, "S5": 16.0},
                "lane_ideal_score": {"S1": 165.0, "S2": 150.0, "S3": 135.0, "S4": 190.0, "S5": 190.0},
                "forced_range_names_by_seat": {},
                "bridge_range_score": 20.0,
                "source_continuity_bonus": 0.0,
                "reasons": profile["reasons"] + ["endpoint_jump", "set_edge_relations", "lower_discharge_tail_release_conversion"],
            }
        )
        return profile

    if controlled_anchor:
        profile.update(
            {
                "profile_id": "TAIL_RELEASE_BURST_CARRY__CONTROLLED_S4_RELIEF_S5_ANCHOR",
                "source_continuity_seats": ["S5"],
                "lane_upstream_commit_weight": {"S1": 30.0, "S2": 30.0, "S3": 30.0, "S4": 18.0, "S5": 80.0},
                "lane_ideal_delta": {"S1": -4.0, "S2": -24.0, "S3": -6.0, "S4": 17.0, "S5": 0.0},
                "lane_ideal_score": {"S1": 120.0, "S2": 170.0, "S3": 130.0, "S4": 190.0, "S5": 150.0},
                "forced_range_names_by_seat": {
                    "S1": ["LOW_STARTER_GALLEON"],
                    "S2": ["S2_CORE_GRUNT"],
                    "S3": ["S3_HINGE_HARBINGER"],
                    "S4": ["S4_EXIT_SKY"],
                    "S5": ["HIGH_ENDPOINT_HIGH_KING"],
                },
                "bridge_range_score": 30.0,
                "source_continuity_bonus": 72.0,
                "reasons": profile["reasons"] + ["volcanic_tail_release_inversion", "controlled_s4_relief_s5_anchor"],
            }
        )
        return profile

    if right_break_aftershock:
        profile.update(
            {
                "profile_id": "TAIL_RELEASE_BURST_CARRY__RIGHT_BREAK_AFTERSHOCK_ENDPOINT_CARRY",
                "source_continuity_seats": ["S4", "S5"],
                "lane_upstream_commit_weight": {"S1": 64.0, "S2": 76.0, "S3": 84.0, "S4": 116.0, "S5": 116.0},
                "lane_ideal_delta": {"S1": -10.0, "S2": -16.0, "S3": -5.0, "S4": 0.0, "S5": -2.0},
                "lane_ideal_score": {"S1": 125.0, "S2": 140.0, "S3": 130.0, "S4": 190.0, "S5": 185.0},
                "forced_range_names_by_seat": {
                    "S1": ["LOW_STARTER_GALLEON"],
                    "S2": ["S2_CORE_MENOUS"],
                    "S3": ["S3_HINGE_HARBINGER"],
                    "S4": ["S4_EXIT_BRAGA"],
                    "S5": ["HIGH_ENDPOINT_HIGH_KING"],
                },
                "bridge_range_score": 28.0,
                "source_continuity_bonus": 64.0,
                "reasons": profile["reasons"] + [
                    "tail_burst_right_break_aftershock",
                    "endpoint_carry_after_known_right_break",
                    "left_mid_cooling_without_restarting_endpoint_jump",
                ],
            }
        )
        return profile

    if lower_discharge_support:
        profile.update(
            {
                "profile_id": "TAIL_RELEASE_BURST_CARRY__PRECISION_LED_LOWER_DISCHARGE_SUPPORT",
                "source_continuity_seats": ["S1", "S2", "S3", "S4", "S5"],
                "lane_upstream_commit_weight": {"S1": 104.0, "S2": 104.0, "S3": 104.0, "S4": 104.0, "S5": 104.0},
                "lane_ideal_delta": {},
                "lane_ideal_score": {},
                "forced_range_names_by_seat": {
                    "S1": ["LOW_STARTER_GALLEON"],
                    "S2": ["S2_CORE_MENOUS"],
                    "S3": ["S3_HINGE_FIGHTER_HIGH"],
                    "S4": ["S4_EXIT_BRAGA"],
                    "S5": ["HIGH_ENDPOINT_HIGH_KING"],
                },
                "bridge_range_score": 24.0,
                "source_continuity_bonus": 48.0,
                "reasons": profile["reasons"] + [
                    "lower_discharge_support",
                    "precision_led_until_projection_decisive",
                    "tail_release_support_may_not_overthrow_range_contract",
                ],
            }
        )
        return profile

    profile.update(
        {
            "profile_id": "TAIL_RELEASE_BURST_CARRY__SUPPORT_ONLY",
            "source_continuity_seats": ["S1", "S2", "S3", "S4", "S5"],
            "lane_upstream_commit_weight": {seat: 72.0 for seat in ("S1", "S2", "S3", "S4", "S5")},
            "bridge_range_score": 35.0,
            "source_continuity_bonus": 48.0,
            "reasons": profile["reasons"] + ["tail_release_without_specific_subtype"],
        }
    )
    return profile


def lower_tail_recovery_active(question_id: Any, contradiction_packet: dict[str, Any]) -> bool:
    active = active_keys(contradiction_packet)
    return (
        normalized_question_id(question_id) == "LOWER_DISCHARGE_CRISIS_RECAST"
        and {"LOWER_DISCHARGE_CRISIS_RECAST", "TAIL_RELEASE_BURST_CARRY"} <= active
        and "FRONT_DISCHARGE_CONTROL" not in active
    )


def tail_release_answer_active(question_id: Any, contradiction_packet: dict[str, Any]) -> bool:
    active = active_keys(contradiction_packet)
    return (
        normalized_question_id(question_id) == "TAIL_RELEASE_BURST_CARRY"
        and "TAIL_RELEASE_BURST_CARRY" in active
    )


def upstream_commit_weight(question_id: Any, contradiction_packet: dict[str, Any]) -> float:
    active = active_keys(contradiction_packet)
    if lower_tail_recovery_active(question_id, contradiction_packet):
        return 36.0
    return 96.0 if active else 160.0


def lane_upstream_commit_weight(
    question_id: Any,
    contradiction_packet: dict[str, Any],
    seat: str,
    subtype_profile: dict[str, Any] | None = None,
) -> float:
    profile_weights = (subtype_profile or {}).get("lane_upstream_commit_weight") or {}
    if profile_weights.get(seat) is not None:
        return as_float(profile_weights.get(seat))
    if tail_release_answer_active(question_id, contradiction_packet):
        return {
            "S1": 24.0,
            "S2": 20.0,
            "S3": 18.0,
            "S4": 12.0,
            "S5": 12.0,
        }.get(str(seat), 24.0)
    return upstream_commit_weight(question_id, contradiction_packet)


def source_continuity_allowed(
    question_id: Any,
    contradiction_packet: dict[str, Any],
    seat: str,
    subtype_profile: dict[str, Any] | None = None,
) -> bool:
    if subtype_profile:
        return str(seat) in set(subtype_profile.get("source_continuity_seats") or [])
    if tail_release_answer_active(question_id, contradiction_packet):
        return False
    return not (
        str(seat) in {"S2", "S3", "S4", "S5"}
        and "FRONT_DISCHARGE_CONTROL" in active_keys(contradiction_packet)
    )


def bridge_expansion_policy(question_id: Any, contradiction_packet: dict[str, Any]) -> dict[str, Any]:
    active = active_keys(contradiction_packet)
    lower_tail = lower_tail_recovery_active(question_id, contradiction_packet)
    enabled = bool(active & BRIDGE_EXPANSION_FAMILIES)
    return {
        "schema": "serenity.life_link.contradiction_bridge_expansion_policy.v1",
        "status": "BRIDGE_EXPANSION_ACTIVE" if enabled else "NO_BRIDGE_EXPANSION",
        "enabled": enabled,
        "active_bridge_families": sorted(active & BRIDGE_EXPANSION_FAMILIES),
        "max_gap_fill": 1,
        "lane_extension": {
            "s3_upper_steps": 2 if lower_tail else 0,
        },
        "law": (
            "Contradiction bridge ranges may fill only tiny named-range gaps or the lower-tail S3 recovery lift. "
            "They explain the question; they do not become a broad safety cloud."
        ),
    }


def build_answer_requirement_packet(
    *,
    question_id: Any,
    contradiction_packet: dict[str, Any],
    source_body: list[int] | None = None,
    situation_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active = active_keys(contradiction_packet)
    lower_tail = lower_tail_recovery_active(question_id, contradiction_packet)
    source_s4 = float(source_body[3]) if source_body and len(source_body) > 3 else 0.0
    subtype_profile = answer_subtype_profile(
        question_id=question_id,
        contradiction_packet=contradiction_packet,
        source_body=source_body or [],
        situation_context=situation_context or {},
    )
    glossary_lookup = (
        QUESTION_ANSWER_GLOSSARY.lookup_question_answer_profile(
            question_id=question_id,
            contradiction_packet=contradiction_packet,
            source_body=source_body or [],
            situation_context=situation_context or {},
        )
        if QUESTION_ANSWER_GLOSSARY
        else {"status": "QUESTION_ANSWER_GLOSSARY_UNAVAILABLE"}
    )
    if glossary_lookup.get("activation") == "QUESTION_ANSWER_GLOSSARY_AUTHORITATIVE":
        glossary_profile = glossary_lookup.get("answer_subtype_profile") or {}
        glossary_profile["fallback_profile_id"] = subtype_profile.get("profile_id")
        subtype_profile = glossary_profile
    return {
        "schema": "serenity.life_link.contradiction_answer_requirement_map.v1",
        "status": "ANSWER_REQUIREMENT_MAP_ACTIVE" if active else "ANSWER_REQUIREMENT_MAP_GENERAL",
        "question_id": normalized_question_id(question_id),
        "active_glossary_keys": sorted(active),
        "lower_tail_recovery_active": lower_tail,
        "upstream_commit_weight": upstream_commit_weight(question_id, contradiction_packet),
        "lane_upstream_commit_weight": {
            seat: lane_upstream_commit_weight(question_id, contradiction_packet, seat, subtype_profile)
            for seat in ("S1", "S2", "S3", "S4", "S5")
        },
        "bridge_expansion_policy": bridge_expansion_policy(question_id, contradiction_packet),
        "answer_subtype_profile": subtype_profile,
        "question_answer_glossary_lookup": glossary_lookup,
        "source_continuity_policy": {
            "families": sorted(SOURCE_CONTINUITY_FAMILIES),
            "suppress_during_crisis_break_recast": "CRISIS_BREAK_RECAST_BURST_EXPANSION" in active,
            "suppress_middle_during_lower_tail": lower_tail,
            "suppress_upper_during_front_discharge": "FRONT_DISCHARGE_CONTROL" in active,
            "source_continuity_seats": subtype_profile.get("source_continuity_seats") or [],
        },
        "lane_scoring_policy": {
            "s1_lower_tail_recast_lift": lower_tail,
            "s2_lower_tail_ideal_delta": 16.0 if lower_tail else None,
            "s3_lower_tail_ideal_delta": (7.0 if source_s4 <= 50 else 17.0) if lower_tail else None,
            "s4_lower_tail_ideal_delta": (12.0 if source_s4 <= 50 else 5.0) if lower_tail else None,
            "generic_upper_recovery_lanes": ["S3", "S4"],
            "tail_release_exit_lanes": ["S4", "S5"],
            "subtype_lane_ideal_delta": subtype_profile.get("lane_ideal_delta") or {},
            "subtype_lane_ideal_score": subtype_profile.get("lane_ideal_score") or {},
            "forced_range_names_by_seat": subtype_profile.get("forced_range_names_by_seat") or {},
        },
        "answer_law": (
            "The committed answer is selected by the active contradiction requirement, not by every lawful range. "
            "Allowed, explicit, and supported remain separate so loud legal clones cannot blur the question."
        ),
    }


def score_range_from_answer_map(
    *,
    seat: str,
    range_name: str,
    definition: dict[str, Any],
    range_numbers: set[int],
    source_value: int,
    source_body: list[int],
    seat_answer: dict[str, Any],
    contradiction_packet: dict[str, Any],
    question_id: Any,
    answer_subtype_profile: dict[str, Any] | None = None,
) -> tuple[float, list[str]]:
    active = active_keys(contradiction_packet)
    if not active:
        return 0.0, []
    score = 0.0
    reasons: list[str] = []
    center = range_midpoint(definition)
    source_delta = center - float(source_value or 0)
    contradiction_names = set(seat_answer.get("contradiction_range_names") or [])
    lower_tail = lower_tail_recovery_active(question_id, contradiction_packet)
    tail_release = tail_release_answer_active(question_id, contradiction_packet)
    subtype_profile = answer_subtype_profile or {}
    subtype_id = str(subtype_profile.get("profile_id") or "")
    forced_names = set((subtype_profile.get("forced_range_names_by_seat") or {}).get(seat) or [])

    if range_name in contradiction_names:
        if tail_release:
            score += as_float(subtype_profile.get("bridge_range_score"), 20.0)
            reasons.append(f"{subtype_id or 'TAIL_RELEASE'}_CONTRADICTION_BRIDGE_CONTEXT")
        else:
            score += 70.0
            reasons.append("CANONICAL_CONTRADICTION_BRIDGE_RANGE")
    if range_name in forced_names:
        score += as_float(subtype_profile.get("forced_range_score"), 0.0)
        reasons.append(f"{subtype_id or 'ANSWER_SUBTYPE'}_AUTHORIZED_RANGE_COMMIT")
    if "QUESTION_RANGE_GLOSSARY" in active:
        score += 8.0
        reasons.append("CANONICAL_QUESTION_RANGE_GLOSSARY")
    if (
        source_value in range_numbers
        and active & SOURCE_CONTINUITY_FAMILIES
        and "CRISIS_BREAK_RECAST_BURST_EXPANSION" not in active
        and not (seat in {"S2", "S3", "S4"} and lower_tail)
        and not (seat in {"S2", "S3", "S4", "S5"} and "FRONT_DISCHARGE_CONTROL" in active)
        and source_continuity_allowed(question_id, contradiction_packet, seat, subtype_profile)
    ):
        score += as_float(subtype_profile.get("source_continuity_bonus"), 64.0)
        reasons.append("CANONICAL_SOURCE_CONTINUITY_SUPPORTED")
    elif source_value in range_numbers and tail_release:
        reasons.append("TAIL_RELEASE_SOURCE_CONTINUITY_CONTEXT_ONLY")
    if seat == "S1" and source_value in range_numbers and lower_tail:
        score += 42.0
        reasons.append("LOWER_DISCHARGE_SOURCE_ENTRY_NOT_FORCED_TO_COLLAPSE")
    if seat == "S1" and lower_tail and source_value <= 6 and source_delta > 0:
        score += max(0.0, 160.0 - (abs(source_delta - 13.0) * 12.0))
        reasons.append("LOWER_TAIL_LOW_STARTER_RECAST_LIFT")
    if lower_tail and seat in {"S2", "S3", "S4"} and source_delta > 0:
        source_s4 = float(source_body[3]) if len(source_body) > 3 else 0.0
        if seat == "S2":
            ideal_delta = 16.0
        elif seat == "S3":
            ideal_delta = 7.0 if source_s4 <= 50 else 17.0
        else:
            ideal_delta = 12.0 if source_s4 <= 50 else 5.0
        score += max(0.0, 150.0 - (abs(source_delta - ideal_delta) * 11.0))
        reasons.append("LOWER_TAIL_RECOVERY_IDEAL_RANGE")
        if abs(source_delta - ideal_delta) <= 1.25:
            score += 24.0
            reasons.append("LOWER_TAIL_RECOVERY_CENTER_POCKET")
    elif seat in {"S3", "S4"} and "FRONT_DISCHARGE_CONTROL" not in active and active & UPPER_RECOVERY_FAMILIES:
        if source_delta > 0:
            score += min(120.0, source_delta * 10.5)
            reasons.append("CANONICAL_UPPER_RECOVERY_RANGE")
        elif range_name in contradiction_names:
            score += 24.0
            reasons.append("CANONICAL_CONTAINED_BRIDGE_RANGE")
    if seat in {"S4", "S5"} and "TAIL_RELEASE_BURST_CARRY" in active and source_delta >= -4:
        score += 22.0
        reasons.append("TAIL_RELEASE_EXIT_ENDPOINT_SUPPORT")
    if seat == "S4" and "TAIL_RELEASE_BURST_CARRY" in active and source_delta > 0:
        score += 32.0
        reasons.append("TAIL_RELEASE_EXIT_LIFT_SUPPORT")
    ideal_deltas = subtype_profile.get("lane_ideal_delta") or {}
    ideal_scores = subtype_profile.get("lane_ideal_score") or {}
    if ideal_deltas.get(seat) is not None:
        ideal_delta = as_float(ideal_deltas.get(seat))
        max_score = as_float(ideal_scores.get(seat), 120.0)
        distance_weight = 10.0 if max_score < 170.0 else 9.0
        lane_score = max(0.0, max_score - (abs(source_delta - ideal_delta) * distance_weight))
        if lane_score:
            score += lane_score
            reasons.append(f"{subtype_id or 'ANSWER_SUBTYPE'}_LANE_IDEAL")
        if tail_release:
            if lane_score:
                reasons.append("TAIL_RELEASE_ANSWER_MAP_LANE_LIFT")
            if "ENDPOINT_JUMP" in subtype_id and seat in {"S4", "S5"} and source_delta >= 12:
                score += 28.0
                reasons.append("TAIL_RELEASE_HIGH_EXIT_ENDPOINT_COMMIT")
            if "ENDPOINT_JUMP" in subtype_id and seat == "S3" and source_delta >= 4:
                score += 18.0
                reasons.append("TAIL_RELEASE_HINGE_LIFT_COMMIT")
            if "ENDPOINT_JUMP" in subtype_id and seat == "S1" and source_delta >= 7:
                score += 18.0
                reasons.append("TAIL_RELEASE_FRONT_STARTER_LIFT_COMMIT")
    if seat in {"S2", "S3", "S4"} and lower_tail and source_delta > 6:
        score += 32.0
        reasons.append("LOWER_DISCHARGE_WITH_UPPER_RECOVERY_COUNTER")
    return score, reasons
