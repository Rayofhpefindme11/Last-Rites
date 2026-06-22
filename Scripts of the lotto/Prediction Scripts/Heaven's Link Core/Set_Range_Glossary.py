from __future__ import annotations

from typing import Any


S1_STARTER_RANGE_GLOSSARY: dict[str, dict[str, Any]] = {
    "LOW_STARTER_HOLLOW": {"number_bands": [(1, 3)], "range_label": "1-3", "family": "LOW_STARTER", "slot": "HOLLOW"},
    "LOW_STARTER_GALLEON": {"number_bands": [(4, 6)], "range_label": "4-6", "family": "LOW_STARTER", "slot": "GALLEON"},
    "LOW_STARTER_ARRANCAR": {"number_bands": [(7, 10)], "range_label": "7-10", "family": "LOW_STARTER", "slot": "ARRANCAR"},
    "MID_STARTER_HOLLOW": {"number_bands": [(11, 13)], "range_label": "11-13", "family": "MID_STARTER", "slot": "HOLLOW"},
    "MID_STARTER_GALLEON": {"number_bands": [(14, 16)], "range_label": "14-16", "family": "MID_STARTER", "slot": "GALLEON"},
    "MID_STARTER_ARRANCAR": {"number_bands": [(17, 20)], "range_label": "17-20", "family": "MID_STARTER", "slot": "ARRANCAR"},
    "HIGH_STARTER_HOLLOW": {"number_bands": [(21, 23)], "range_label": "21-23", "family": "HIGH_STARTER", "slot": "HOLLOW"},
    "HIGH_STARTER_GALLEON": {"number_bands": [(24, 26)], "range_label": "24-26", "family": "HIGH_STARTER", "slot": "GALLEON"},
    "HIGH_STARTER_ARRANCAR": {"number_bands": [(27, 30)], "range_label": "27-30", "family": "HIGH_STARTER", "slot": "ARRANCAR"},
    "EXT_HIGH_STARTER_HOLLOW": {"number_bands": [(31, 40)], "range_label": "31-40", "family": "EXT_HIGH_STARTER", "slot": "HOLLOW"},
    "EXT_HIGH_STARTER_GALLEON": {"number_bands": [(41, 50)], "range_label": "41-50", "family": "EXT_HIGH_STARTER", "slot": "GALLEON"},
    "EXT_HIGH_STARTER_ARRANCAR": {"number_bands": [(51, 60)], "range_label": "51-60", "family": "EXT_HIGH_STARTER", "slot": "ARRANCAR"},
}

ENTRY_EXIT_RANGE_GLOSSARY: dict[str, dict[str, Any]] = {
    "MIN": {"gap_range": "1-5", "number_bands": [(1, 5)], "role": "touching_or_near_touching_gate"},
    "SHORT": {"gap_range": "5-10", "number_bands": [(5, 10)], "role": "short_gate"},
    "MID": {"gap_range": "10-15", "number_bands": [(10, 15)], "role": "middle_gate"},
    "LARGE": {"gap_range": "15-20", "number_bands": [(15, 20)], "role": "large_gate"},
    "FAR": {"gap_range": "20-25", "number_bands": [(20, 25)], "role": "far_gate"},
    "DISTANT": {"gap_range": "25-35", "number_bands": [(25, 35)], "role": "distant_gate"},
    "EXTREME": {"gap_range": "35+", "number_bands": [(35, 69)], "role": "extreme_gate"},
}

SET_HEALTH_RANGE_GLOSSARY: dict[str, dict[str, Any]] = {
    "COMPRESS": {
        "gap_range": "1-5",
        "gap_min": 1,
        "gap_max": 5,
        "role": "tight_middle",
        "motion_read": "contained_pressure",
        "question_use": "Use when the question asks for a dense middle that keeps S2-S4 close.",
        "clone_risk": "Too-clean compression can become a loud clone when support is weak.",
        "supports": ["contained_release", "front_control", "lower_lane_discharge"],
        "penalizes": ["unasked_bridge", "unsupported_tail_extension"],
    },
    "LOCK": {
        "gap_range": "6-10",
        "gap_min": 6,
        "gap_max": 10,
        "role": "locked_middle",
        "motion_read": "held_pressure",
        "question_use": "Use when the question asks for a close middle with enough room to breathe.",
        "clone_risk": "Lock clones can look lawful while refusing the required release.",
        "supports": ["hold", "stable_pressure", "contained_transition"],
        "penalizes": ["forced_expansion", "unsupported_upper_lift"],
    },
    "BALANCE": {
        "gap_range": "11-15",
        "gap_min": 11,
        "gap_max": 15,
        "role": "balanced_middle",
        "motion_read": "centered_completion",
        "question_use": "Use when the question asks for the middle to carry pressure without leaning too low or too high.",
        "clone_risk": "Balance clones can lose to louder constructions unless support is separated from explicit match.",
        "supports": ["center_completion", "mixed_drift", "burden_balance"],
        "penalizes": ["over_compression", "over_extension"],
    },
    "STRETCH": {
        "gap_range": "16-20",
        "gap_min": 16,
        "gap_max": 20,
        "role": "stretched_middle",
        "motion_read": "upper_recovery",
        "question_use": "Use when the question asks for the middle to open while staying connected.",
        "clone_risk": "Stretch clones can over-express lift and outrank supported survivors.",
        "supports": ["upper_recovery", "tail_release", "lane_lift"],
        "penalizes": ["unasked_lock", "endpoint_overreach"],
    },
    "BRIDGE": {
        "gap_range": "21-25",
        "gap_min": 21,
        "gap_max": 25,
        "role": "bridged_middle",
        "motion_read": "span_connection",
        "question_use": "Use when the question asks the middle to connect separated lanes.",
        "clone_risk": "Bridge clones can satisfy shape while skipping inhabitant support.",
        "supports": ["lane_bridge", "separation_repair", "long_middle_transition"],
        "penalizes": ["unasked_compress", "unsupported_void_span"],
    },
    "EXTREME": {
        "gap_range": "25+",
        "gap_min": 26,
        "gap_max": 69,
        "role": "extreme_middle",
        "motion_read": "hard_separation",
        "question_use": "Use only when the question explicitly asks for severe middle separation.",
        "clone_risk": "Extreme clones are often loud and must prove support before they dominate.",
        "supports": ["hard_reset", "separation_break", "extreme_lane_relocation"],
        "penalizes": ["ordinary_balance", "unsupported_extreme_jump"],
    },
}

SET_HEALTH_ALIASES: dict[str, str] = {
    "MIDDLE_COMPRESSED": "COMPRESS",
    "MIDDLE_COMPRESS": "COMPRESS",
    "COMPRESSED": "COMPRESS",
    "MIDDLE_STRESSED": "LOCK",
    "STRESSED": "LOCK",
    "MIDDLE_LOCK": "LOCK",
    "MIDDLE_STABLE": "BALANCE",
    "STABLE": "BALANCE",
    "MIDDLE_BALANCED": "BALANCE",
    "BALANCED": "BALANCE",
    "MIDDLE_EXPANDING": "STRETCH",
    "EXPANDING": "STRETCH",
    "MIDDLE_STRETCH": "STRETCH",
    "MIDDLE_HINGE": "BRIDGE",
    "HINGE": "BRIDGE",
    "MIDDLE_BRIDGE": "BRIDGE",
    "MIDDLE_EXTREME": "EXTREME",
}

MIDDLE_SLOT_RANGE_GLOSSARY: dict[str, dict[str, Any]] = {
    "S2_CORE_BABE": {"number_bands": [(2, 4)], "range_label": "2-4", "seat": "S2", "family": "S2_CORE", "slot": "BABE"},
    "S2_CORE_KID": {"number_bands": [(6, 8)], "range_label": "6-8", "seat": "S2", "family": "S2_CORE", "slot": "KID"},
    "S2_CORE_TEEN": {"number_bands": [(9, 10)], "range_label": "9-10", "seat": "S2", "family": "S2_CORE", "slot": "TEEN"},
    "S2_CORE_GRUNT": {"number_bands": [(11, 13)], "range_label": "11-13", "seat": "S2", "family": "S2_CORE", "slot": "GRUNT"},
    "S2_CORE_MENOUS": {"number_bands": [(14, 16)], "range_label": "14-16", "seat": "S2", "family": "S2_CORE", "slot": "MENOUS"},
    "S2_CORE_GRANDE": {"number_bands": [(17, 20)], "range_label": "17-20", "seat": "S2", "family": "S2_CORE", "slot": "GRANDE"},
    "S2_CORE_GALLEON": {"number_bands": [(21, 23)], "range_label": "21-23", "seat": "S2", "family": "S2_CORE", "slot": "GALLEON"},
    "S2_CORE_FIGHTER": {"number_bands": [(24, 26)], "range_label": "24-26", "seat": "S2", "family": "S2_CORE", "slot": "FIGHTER"},
    "S2_CORE_ARCHER": {"number_bands": [(27, 30)], "range_label": "27-30", "seat": "S2", "family": "S2_CORE", "slot": "ARCHER"},
    "S2_CORE_HARBINGER": {"number_bands": [(31, 33)], "range_label": "31-33", "seat": "S2", "family": "S2_CORE", "slot": "HARBINGER"},
    "S2_CORE_WRESTLER": {"number_bands": [(34, 36)], "range_label": "34-36", "seat": "S2", "family": "S2_CORE", "slot": "WRESTLER"},
    "S2_CORE_FIGHTER_HIGH": {"number_bands": [(37, 40)], "range_label": "37-40", "seat": "S2", "family": "S2_CORE", "slot": "FIGHTER_HIGH"},
    "S2_CORE_HOLLOW": {"number_bands": [(41, 43)], "range_label": "41-43", "seat": "S2", "family": "S2_CORE", "slot": "HOLLOW"},
    "S2_CORE_BRAGA": {"number_bands": [(44, 46)], "range_label": "44-46", "seat": "S2", "family": "S2_CORE", "slot": "BRAGA"},
    "S2_CORE_KILLER": {"number_bands": [(47, 50)], "range_label": "47-50", "seat": "S2", "family": "S2_CORE", "slot": "KILLER"},
    "S2_CORE_ARRANCAR": {"number_bands": [(51, 53)], "range_label": "51-53", "seat": "S2", "family": "S2_CORE", "slot": "ARRANCAR"},
    "S2_CORE_CERO": {"number_bands": [(54, 56)], "range_label": "54-56", "seat": "S2", "family": "S2_CORE", "slot": "CERO"},
    "S2_CORE_SKY": {"number_bands": [(57, 60)], "range_label": "57-60", "seat": "S2", "family": "S2_CORE", "slot": "SKY"},
    "S2_CORE_GOD": {"number_bands": [(61, 63)], "range_label": "61-63", "seat": "S2", "family": "S2_CORE", "slot": "GOD"},
    "S2_CORE_HIGH_KING": {"number_bands": [(64, 66)], "range_label": "64-66", "seat": "S2", "family": "S2_CORE", "slot": "HIGH_KING"},
    "S3_HINGE_BABE": {"number_bands": [(3, 5)], "range_label": "3-5", "seat": "S3", "family": "S3_HINGE", "slot": "BABE"},
    "S3_HINGE_KID": {"number_bands": [(7, 9)], "range_label": "7-9", "seat": "S3", "family": "S3_HINGE", "slot": "KID"},
    "S3_HINGE_TEEN": {"number_bands": [(10, 11)], "range_label": "10-11", "seat": "S3", "family": "S3_HINGE", "slot": "TEEN"},
    "S3_HINGE_GRUNT": {"number_bands": [(12, 14)], "range_label": "12-14", "seat": "S3", "family": "S3_HINGE", "slot": "GRUNT"},
    "S3_HINGE_MENOUS": {"number_bands": [(15, 17)], "range_label": "15-17", "seat": "S3", "family": "S3_HINGE", "slot": "MENOUS"},
    "S3_HINGE_GRANDE": {"number_bands": [(18, 21)], "range_label": "18-21", "seat": "S3", "family": "S3_HINGE", "slot": "GRANDE"},
    "S3_HINGE_GALLEON": {"number_bands": [(22, 24)], "range_label": "22-24", "seat": "S3", "family": "S3_HINGE", "slot": "GALLEON"},
    "S3_HINGE_FIGHTER": {"number_bands": [(25, 27)], "range_label": "25-27", "seat": "S3", "family": "S3_HINGE", "slot": "FIGHTER"},
    "S3_HINGE_ARCHER": {"number_bands": [(28, 31)], "range_label": "28-31", "seat": "S3", "family": "S3_HINGE", "slot": "ARCHER"},
    "S3_HINGE_HARBINGER": {"number_bands": [(32, 34)], "range_label": "32-34", "seat": "S3", "family": "S3_HINGE", "slot": "HARBINGER"},
    "S3_HINGE_WRESTLER": {"number_bands": [(35, 37)], "range_label": "35-37", "seat": "S3", "family": "S3_HINGE", "slot": "WRESTLER"},
    "S3_HINGE_FIGHTER_HIGH": {"number_bands": [(38, 41)], "range_label": "38-41", "seat": "S3", "family": "S3_HINGE", "slot": "FIGHTER_HIGH"},
    "S3_HINGE_HOLLOW": {"number_bands": [(42, 44)], "range_label": "42-44", "seat": "S3", "family": "S3_HINGE", "slot": "HOLLOW"},
    "S3_HINGE_BRAGA": {"number_bands": [(45, 47)], "range_label": "45-47", "seat": "S3", "family": "S3_HINGE", "slot": "BRAGA"},
    "S3_HINGE_KILLER": {"number_bands": [(48, 51)], "range_label": "48-51", "seat": "S3", "family": "S3_HINGE", "slot": "KILLER"},
    "S3_HINGE_ARRANCAR": {"number_bands": [(52, 54)], "range_label": "52-54", "seat": "S3", "family": "S3_HINGE", "slot": "ARRANCAR"},
    "S3_HINGE_CERO": {"number_bands": [(55, 57)], "range_label": "55-57", "seat": "S3", "family": "S3_HINGE", "slot": "CERO"},
    "S3_HINGE_SKY": {"number_bands": [(58, 61)], "range_label": "58-61", "seat": "S3", "family": "S3_HINGE", "slot": "SKY"},
    "S3_HINGE_GOD": {"number_bands": [(62, 64)], "range_label": "62-64", "seat": "S3", "family": "S3_HINGE", "slot": "GOD"},
    "S3_HINGE_HIGH_KING": {"number_bands": [(65, 67)], "range_label": "65-67", "seat": "S3", "family": "S3_HINGE", "slot": "HIGH_KING"},
    "S4_EXIT_BABE": {"number_bands": [(4, 6)], "range_label": "4-6", "seat": "S4", "family": "S4_EXIT", "slot": "BABE"},
    "S4_EXIT_KID": {"number_bands": [(8, 10)], "range_label": "8-10", "seat": "S4", "family": "S4_EXIT", "slot": "KID"},
    "S4_EXIT_TEEN": {"number_bands": [(11, 12)], "range_label": "11-12", "seat": "S4", "family": "S4_EXIT", "slot": "TEEN"},
    "S4_EXIT_GRUNT": {"number_bands": [(13, 15)], "range_label": "13-15", "seat": "S4", "family": "S4_EXIT", "slot": "GRUNT"},
    "S4_EXIT_MENOUS": {"number_bands": [(16, 18)], "range_label": "16-18", "seat": "S4", "family": "S4_EXIT", "slot": "MENOUS"},
    "S4_EXIT_GRANDE": {"number_bands": [(19, 22)], "range_label": "19-22", "seat": "S4", "family": "S4_EXIT", "slot": "GRANDE"},
    "S4_EXIT_GALLEON": {"number_bands": [(23, 25)], "range_label": "23-25", "seat": "S4", "family": "S4_EXIT", "slot": "GALLEON"},
    "S4_EXIT_FIGHTER": {"number_bands": [(26, 28)], "range_label": "26-28", "seat": "S4", "family": "S4_EXIT", "slot": "FIGHTER"},
    "S4_EXIT_ARCHER": {"number_bands": [(29, 32)], "range_label": "29-32", "seat": "S4", "family": "S4_EXIT", "slot": "ARCHER"},
    "S4_EXIT_HARBINGER": {"number_bands": [(33, 35)], "range_label": "33-35", "seat": "S4", "family": "S4_EXIT", "slot": "HARBINGER"},
    "S4_EXIT_WRESTLER": {"number_bands": [(36, 38)], "range_label": "36-38", "seat": "S4", "family": "S4_EXIT", "slot": "WRESTLER"},
    "S4_EXIT_FIGHTER_HIGH": {"number_bands": [(39, 42)], "range_label": "39-42", "seat": "S4", "family": "S4_EXIT", "slot": "FIGHTER_HIGH"},
    "S4_EXIT_HOLLOW": {"number_bands": [(43, 45)], "range_label": "43-45", "seat": "S4", "family": "S4_EXIT", "slot": "HOLLOW"},
    "S4_EXIT_BRAGA": {"number_bands": [(46, 48)], "range_label": "46-48", "seat": "S4", "family": "S4_EXIT", "slot": "BRAGA"},
    "S4_EXIT_KILLER": {"number_bands": [(49, 52)], "range_label": "49-52", "seat": "S4", "family": "S4_EXIT", "slot": "KILLER"},
    "S4_EXIT_ARRANCAR": {"number_bands": [(53, 55)], "range_label": "53-55", "seat": "S4", "family": "S4_EXIT", "slot": "ARRANCAR"},
    "S4_EXIT_CERO": {"number_bands": [(56, 58)], "range_label": "56-58", "seat": "S4", "family": "S4_EXIT", "slot": "CERO"},
    "S4_EXIT_SKY": {"number_bands": [(59, 62)], "range_label": "59-62", "seat": "S4", "family": "S4_EXIT", "slot": "SKY"},
    "S4_EXIT_GOD": {"number_bands": [(63, 65)], "range_label": "63-65", "seat": "S4", "family": "S4_EXIT", "slot": "GOD"},
    "S4_EXIT_HIGH_KING": {"number_bands": [(66, 68)], "range_label": "66-68", "seat": "S4", "family": "S4_EXIT", "slot": "HIGH_KING"},
}

SET_HEALTH_TO_MIDDLE_SLOT_RANGES: dict[str, list[str]] = {
    "MIDDLE_COMPRESSED": [
        "S2_CORE_GRANDE",
        "S2_CORE_GALLEON",
        "S3_HINGE_HARBINGER",
        "S4_EXIT_HOLLOW",
    ],
    "MIDDLE_STRESSED": ["S2_CORE_ARCHER", "S3_HINGE_KILLER", "S4_EXIT_BRAGA"],
    "MIDDLE_EXPANDING": ["S2_CORE_ARCHER", "S3_HINGE_HARBINGER", "S4_EXIT_CERO"],
    "MIDDLE_HINGE": ["S2_CORE_GALLEON", "S2_CORE_FIGHTER", "S3_HINGE_HARBINGER", "S3_HINGE_WRESTLER", "S3_HINGE_FIGHTER_HIGH", "S4_EXIT_HOLLOW", "S4_EXIT_BRAGA", "S4_EXIT_KILLER"],
    "MIDDLE_STABLE": ["S2_CORE_GALLEON", "S2_CORE_FIGHTER", "S3_HINGE_HARBINGER", "S4_EXIT_HOLLOW"],
}

S5_ENDPOINT_RANGE_GLOSSARY: dict[str, dict[str, Any]] = {
    "EXT_LOW_ENDPOINT_GRUNT": {"number_bands": [(10, 13)], "range_label": "10-13", "family": "EXT_LOW_ENDPOINT", "slot": "GRUNT"},
    "EXT_LOW_ENDPOINT_HEALER": {"number_bands": [(14, 16)], "range_label": "14-16", "family": "EXT_LOW_ENDPOINT", "slot": "HEALER"},
    "EXT_LOW_ENDPOINT_HELPER": {"number_bands": [(17, 20)], "range_label": "17-20", "family": "EXT_LOW_ENDPOINT", "slot": "HELPER"},
    "EXT_LOW_ENDPOINT_CREATOR": {"number_bands": [(21, 23)], "range_label": "21-23", "family": "EXT_LOW_ENDPOINT", "slot": "CREATOR"},
    "EXT_LOW_ENDPOINT_DAECON": {"number_bands": [(24, 26)], "range_label": "24-26", "family": "EXT_LOW_ENDPOINT", "slot": "DAECON"},
    "EXT_LOW_ENDPOINT_WRAITH": {"number_bands": [(27, 30)], "range_label": "27-30", "family": "EXT_LOW_ENDPOINT", "slot": "WRAITH"},
    "LOW_ENDPOINT_GRUNT": {"number_bands": [(31, 33)], "range_label": "31-33", "family": "LOW_ENDPOINT", "slot": "GRUNT"},
    "LOW_ENDPOINT_SOLDIER": {"number_bands": [(34, 36)], "range_label": "34-36", "family": "LOW_ENDPOINT", "slot": "SOLDIER"},
    "LOW_ENDPOINT_LEADER": {"number_bands": [(37, 40)], "range_label": "37-40", "family": "LOW_ENDPOINT", "slot": "LEADER"},
    "LOW_ENDPOINT_CHIEF": {"number_bands": [(41, 43)], "range_label": "41-43", "family": "LOW_ENDPOINT", "slot": "CHIEF"},
    "LOW_ENDPOINT_GOD": {"number_bands": [(44, 45)], "range_label": "44-45", "family": "LOW_ENDPOINT", "slot": "GOD"},
    "MID_ENDPOINT_WAR_CHIEF": {"number_bands": [(46, 49)], "range_label": "46-49", "family": "MID_ENDPOINT", "slot": "WAR_CHIEF"},
    "MID_ENDPOINT_NOBLE": {"number_bands": [(50, 53)], "range_label": "50-53", "family": "MID_ENDPOINT", "slot": "NOBLE"},
    "MID_ENDPOINT_GREAT_NOBLE": {"number_bands": [(54, 55)], "range_label": "54-55", "family": "MID_ENDPOINT", "slot": "GREAT_NOBLE"},
    "HIGH_ENDPOINT_EMPEROR": {"number_bands": [(56, 59)], "range_label": "56-59", "family": "HIGH_ENDPOINT", "slot": "EMPEROR"},
    "HIGH_ENDPOINT_KING": {"number_bands": [(60, 63)], "range_label": "60-63", "family": "HIGH_ENDPOINT", "slot": "KING"},
    "HIGH_ENDPOINT_HIGH_KING": {"number_bands": [(64, 66)], "range_label": "64-66", "family": "HIGH_ENDPOINT", "slot": "HIGH_KING"},
    "HIGH_ENDPOINT_MONARCH": {"number_bands": [(67, 69)], "range_label": "67-69", "family": "HIGH_ENDPOINT", "slot": "MONARCH"},
}


def canonical_range_glossary() -> dict[str, Any]:
    return {
        "schema": "serenity.life_link.set_range_glossary.v1",
        "s1_starter_ranges": S1_STARTER_RANGE_GLOSSARY,
        "entry_exit_gap_ranges": ENTRY_EXIT_RANGE_GLOSSARY,
        "set_health_middle_gap_ranges": SET_HEALTH_RANGE_GLOSSARY,
        "middle_slot_ranges": MIDDLE_SLOT_RANGE_GLOSSARY,
        "s5_endpoint_ranges": S5_ENDPOINT_RANGE_GLOSSARY,
        "law": (
            "The upstream question must name range terms with this glossary before Garden selects inhabitants. "
            "Garden may score numbers inside named ranges, but it should not infer the range vocabulary on its own."
        ),
    }


def range_terms_for_values(
    values: list[str],
    glossary: dict[str, dict[str, Any]],
    *,
    match_mode: str = "exact",
) -> dict[str, dict[str, Any]]:
    requested: dict[str, dict[str, Any]] = {}
    tokens = {str(value or "").upper() for value in values}
    for name, definition in glossary.items():
        upper_name = name.upper()
        if upper_name in tokens:
            requested[name] = definition
            continue
        if match_mode == "embedded" and any(token and (token in upper_name or upper_name in token) for token in tokens):
            requested[name] = definition
    return requested


def middle_slot_terms_for_set_health(values: list[str]) -> dict[str, dict[str, Any]]:
    requested: dict[str, dict[str, Any]] = {}
    for value in values:
        for term in SET_HEALTH_TO_MIDDLE_SLOT_RANGES.get(str(value or "").upper(), []):
            if term in MIDDLE_SLOT_RANGE_GLOSSARY:
                requested[term] = MIDDLE_SLOT_RANGE_GLOSSARY[term]
    return requested


def middle_slot_terms_for_values(values: list[str]) -> dict[str, dict[str, Any]]:
    return range_terms_for_values(values, MIDDLE_SLOT_RANGE_GLOSSARY, match_mode="exact")


def starter_bridge_terms_for_values(values: list[str]) -> dict[str, dict[str, Any]]:
    tokens = {str(value or "").upper() for value in values}
    bridge_terms: list[str] = []
    if {"MID_STARTER_HOLLOW", "MID_STARTER_ARRANCAR"}.issubset(tokens):
        bridge_terms.append("MID_STARTER_GALLEON")
    if {"LOW_STARTER_HOLLOW", "LOW_STARTER_ARRANCAR"}.issubset(tokens):
        bridge_terms.append("LOW_STARTER_GALLEON")
    if {"HIGH_STARTER_HOLLOW", "HIGH_STARTER_ARRANCAR"}.issubset(tokens):
        bridge_terms.append("HIGH_STARTER_GALLEON")
    return range_terms_for_values(bridge_terms, S1_STARTER_RANGE_GLOSSARY, match_mode="exact")


def starter_family_completion_terms_for_values(values: list[str]) -> dict[str, dict[str, Any]]:
    tokens = {str(value or "").upper() for value in values}
    requested: list[str] = []
    families: dict[str, list[str]] = {}
    for name, definition in S1_STARTER_RANGE_GLOSSARY.items():
        if name in tokens:
            families.setdefault(str(definition.get("family") or ""), []).append(str(definition.get("slot") or ""))
    for family, active_slots in families.items():
        if len(set(active_slots)) < 2:
            continue
        for name, definition in S1_STARTER_RANGE_GLOSSARY.items():
            if str(definition.get("family") or "") == family:
                requested.append(name)
    return range_terms_for_values(requested, S1_STARTER_RANGE_GLOSSARY, match_mode="exact")
