from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
FOUNDATION_IIW_PATH = SCRIPT_PATH.parents[1] / "Foundation Scripts" / "Infinite_Inner_World.py"


def load_foundation_iiw() -> Any:
    spec = importlib.util.spec_from_file_location("last_writes_prediction_foundation_iiw", FOUNDATION_IIW_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(FOUNDATION_IIW_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["last_writes_prediction_foundation_iiw"] = module
    spec.loader.exec_module(module)
    return module


_IIW = load_foundation_iiw()

for _name in dir(_IIW):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_IIW, _name)


def build_full_set_technical_body(body: list[int] | tuple[int, ...]) -> dict[str, Any]:
    values = tuple(sorted(int(value) for value in body))
    if len(values) != 5 or len(set(values)) != 5 or any(value < 1 or value > 69 for value in values):
        raise ValueError("build_full_set_technical_body requires five unique values from 1-69.")
    draws = [
        _IIW.HistoricalDraw(
            draw_date=_IIW.date(2100, 1, 1 + index),
            draw_index=index,
            jackpot_usd=None,
            white_balls=values,
            powerball=1,
            powerplay=None,
        )
        for index in range(3)
    ]
    packet = _IIW.build_draw_set_packet(draws, 1)
    set_pressure = packet.set_pressure
    set_health = packet.set_health
    set_anatomy = packet.set_anatomy
    return {
        "schema": "last_writes.iiw.legacy_full_set_technical_body.v1",
        "body": list(values),
        "set_health": set_health.set_health,
        "middle_health": set_health.set_health,
        "pressure_tone": set_health.pressure_tone,
        "full_relation": set_anatomy.full_set_relation,
        "full_set_relation": set_anatomy.full_set_relation,
        "middle_pressure": set_anatomy.middle_pressure,
        "edge_pressure": set_anatomy.edge_pressure,
        "technical_signature": set_anatomy.technical_signature,
        "set_anatomy": set_anatomy.to_payload(),
        "set_pressure": {
            "sorted_pressure": set_pressure.sorted_pressure.to_payload(),
            "draw_pressure": set_pressure.draw_pressure.to_payload(),
        },
    }
