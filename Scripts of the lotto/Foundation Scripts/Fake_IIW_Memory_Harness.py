from __future__ import annotations

import argparse
import base64
import json
import pickle
import random
import time
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from Infinite_Inner_World import HistoricalDraw, build_draw_set_packet
from Seat_Taxonomy import (
    build_conditional_motion_memory_key,
    build_seat_taxonomy_packet,
    conditional_motion_memory_case,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "Synthetic Memory"
)
LEVELS = (2, 3, 4, 5)
SYNTHETIC_DATE_SPAN_DAYS = 2_500_000


def synthetic_draw(index: int, rng: random.Random) -> HistoricalDraw:
    synthetic_date = date(2100, 1, 1) + timedelta(days=index % SYNTHETIC_DATE_SPAN_DAYS)
    return HistoricalDraw(
        draw_date=synthetic_date,
        draw_index=index,
        jackpot_usd=None,
        white_balls=tuple(rng.sample(range(1, 70), 5)),  # type: ignore[arg-type]
        powerball=rng.randint(1, 39),
        powerplay=None,
    )


def draw_from_payload(payload: dict[str, Any]) -> HistoricalDraw:
    return HistoricalDraw(
        draw_date=date.fromisoformat(str(payload["draw_date"])),
        draw_index=int(payload["draw_index"]),
        jackpot_usd=payload.get("jackpot_usd"),
        white_balls=tuple(payload["white_balls"]),  # type: ignore[arg-type]
        powerball=int(payload["powerball"]),
        powerplay=payload.get("powerplay"),
    )


def encode_rng_state(rng: random.Random) -> str:
    return base64.b64encode(pickle.dumps(rng.getstate())).decode("ascii")


def decode_rng_state(payload: str) -> object:
    return pickle.loads(base64.b64decode(payload.encode("ascii")))


def empty_room(level: int, key: str, case: dict[str, Any]) -> dict[str, Any]:
    return {
        "memory_source": "SYNTHETIC_FAKE_IIW",
        "memory_level": level,
        "scenario_key": key,
        "appearances": 0,
        "condition": {
            "topology_name": case["topology_name"],
            "world_key": case["world_key"],
            "world_slot": case["world_slot"],
            "map_pressure_type": case["map_pressure_type"],
            "pressure_center": case["pressure_center"],
            "pressure_balance": case["pressure_balance"],
            "pressure_distribution": case["pressure_distribution"],
            "pressure_shape": case["pressure_shape"],
            "authority_seat": case["authority_seat"],
            "authority_origin": case["authority_origin"],
            "dominant_pressure_seat": case["dominant_pressure_seat"],
            "dominant_incoming_draw_lane": case["dominant_incoming_draw_lane"],
            "incoming_draw_sign": case["incoming_draw_sign"],
            "incoming_draw_family": case["incoming_draw_family"],
            "incoming_energy_class": case["incoming_energy_class"],
            "face_family": case["face_family"],
            "turn_lanes": case["turn_lanes"],
            "set_relation": case["set_relation"],
            "middle_pressure": case["middle_pressure"],
            "edge_pressure": case["edge_pressure"],
            "pressure_fusion": case["pressure_fusion"],
            "highest_burden_seat": case["highest_burden_seat"],
            "highest_burden_level": case["highest_burden_level"],
            "highest_burden_state": case["highest_burden_state"],
            "dominant_origin_seat": case["dominant_origin_seat"],
        },
        "counts": {
            "branch": {},
            "family": {},
            "lane": {},
            "flow": {},
            "transfer": {},
            "sign": {},
        },
        "samples": [],
        "first_seen_fake_index": case["index"],
        "last_seen_fake_index": case["index"],
    }


def increment(counter_payload: dict[str, int], value: Any) -> None:
    key = str(value)
    counter_payload[key] = int(counter_payload.get(key, 0)) + 1


def update_room(room: dict[str, Any], case: dict[str, Any], sample_limit: int) -> None:
    room["appearances"] += 1
    room["last_seen_fake_index"] = case["index"]
    counts = room["counts"]
    increment(counts["branch"], case["actual_branch"])
    increment(counts["family"], case["actual_family"])
    increment(counts["lane"], case["actual_lane"])
    increment(counts["flow"], case["outgoing_flow"])
    increment(counts["transfer"], case["outgoing_transfer"])
    increment(counts["sign"], case["outgoing_sign_pattern"])
    if len(room["samples"]) < sample_limit:
        room["samples"].append(
            {
                "fake_index": case["index"],
                "white_balls": case.get("white_balls"),
                "actual_branch": case["actual_branch"],
                "actual_family": case["actual_family"],
                "actual_lane": case["actual_lane"],
                "actual_motion": case["actual_motion"],
                "outgoing_flow": case["outgoing_flow"],
                "outgoing_transfer": case["outgoing_transfer"],
                "outgoing_sign_pattern": case["outgoing_sign_pattern"],
            }
        )


def ranked(counter_payload: dict[str, int]) -> list[dict[str, Any]]:
    counter = Counter(counter_payload)
    total = sum(counter.values())
    if total == 0:
        return []
    return [
        {
            "value": value,
            "count": count,
            "rate": round((count / total) * 100, 2),
        }
        for value, count in counter.most_common()
    ]


def finalize_room(room: dict[str, Any]) -> dict[str, Any]:
    payload = dict(room)
    payload["outcomes"] = {
        "branch_rank": ranked(room["counts"]["branch"]),
        "family_rank": ranked(room["counts"]["family"]),
        "lane_rank": ranked(room["counts"]["lane"]),
        "flow_rank": ranked(room["counts"]["flow"]),
        "transfer_rank": ranked(room["counts"]["transfer"]),
        "sign_rank": ranked(room["counts"]["sign"]),
    }
    return payload


def write_json(path: Path, payload: Any) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temp.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest(output_dir: Path) -> dict[str, Any] | None:
    path = output_dir / "manifest.json"
    if not path.exists():
        return None
    return read_json(path)


def load_existing_rooms(output_dir: Path) -> dict[int, dict[str, dict[str, Any]]]:
    rooms_by_level: dict[int, dict[str, dict[str, Any]]] = {
        level: {}
        for level in LEVELS
    }
    for level in LEVELS:
        path = output_dir / f"level_{level}" / "synthetic_memory.json"
        if not path.exists():
            continue
        payload = read_json(path)
        for room in payload.get("rooms", []):
            room = dict(room)
            room.pop("outcomes", None)
            rooms_by_level[level][room["scenario_key"]] = room
    return rooms_by_level


def prepare_resume_draws(
    *,
    manifest: dict[str, Any],
    rng: random.Random,
    fake_index: int,
) -> list[HistoricalDraw]:
    tail_payload = manifest.get("tail_draws")
    if isinstance(tail_payload, list) and len(tail_payload) == 2:
        return [draw_from_payload(row) for row in tail_payload]

    # Older checkpoints did not save the tail window. Rebuild only the rolling
    # two-draw window while advancing the RNG to the next fake index.
    tail: list[HistoricalDraw] = []
    for index in range(fake_index):
        draw = synthetic_draw(index, rng)
        tail.append(draw)
        if len(tail) > 2:
            tail.pop(0)
    if len(tail) != 2:
        raise ValueError("Cannot resume synthetic harness without two prior fake draws.")
    return tail


def write_checkpoint(
    output_dir: Path,
    rooms_by_level: dict[int, dict[str, dict[str, Any]]],
    manifest: dict[str, Any],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    levels_payload: dict[str, Any] = {}
    for level in LEVELS:
        level_dir = output_dir / f"level_{level}"
        level_dir.mkdir(parents=True, exist_ok=True)
        rooms = [
            finalize_room(room)
            for room in rooms_by_level[level].values()
        ]
        rooms.sort(key=lambda row: (-row["appearances"], row["scenario_key"]))
        level_payload = {
            "memory_source": "SYNTHETIC_FAKE_IIW",
            "memory_level": level,
            "scenario_count": len(rooms),
            "appearance_count": sum(row["appearances"] for row in rooms),
            "rooms": rooms,
        }
        write_json(level_dir / "synthetic_memory.json", level_payload)
        levels_payload[str(level)] = {
            "scenario_count": len(rooms),
            "appearance_count": level_payload["appearance_count"],
        }
    manifest["levels"] = levels_payload
    manifest["last_checkpoint_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    write_json(output_dir / "manifest.json", manifest)


def run_harness(
    output_dir: Path,
    stop_file: Path,
    max_draws: int | None,
    checkpoint_every: int,
    seed: int,
    sample_limit: int,
    resume: bool,
) -> None:
    prior_manifest = load_manifest(output_dir) if resume else None
    rng = random.Random(seed)
    rooms_by_level = load_existing_rooms(output_dir) if prior_manifest else {
        level: {}
        for level in LEVELS
    }
    started = time.perf_counter()
    processed = int(prior_manifest.get("processed_fake_draws", 0)) if prior_manifest else 0
    initial_processed = processed
    fake_index = int(prior_manifest.get("next_fake_index", processed + 2)) if prior_manifest else 0
    last_checkpoint = processed
    target_processed = processed + max_draws if max_draws is not None else None

    if prior_manifest:
        seed = int(prior_manifest.get("seed", seed))
        rng = random.Random(seed)
        rng_state = prior_manifest.get("rng_state_b64")
        tail_payload = prior_manifest.get("tail_draws")
        if isinstance(rng_state, str) and rng_state and isinstance(tail_payload, list):
            rng.setstate(decode_rng_state(rng_state))
            draws = prepare_resume_draws(
                manifest=prior_manifest,
                rng=rng,
                fake_index=fake_index,
            )
        else:
            rng = random.Random(seed)
            draws = prepare_resume_draws(
                manifest=prior_manifest,
                rng=rng,
                fake_index=fake_index,
            )
        manifest: dict[str, Any] = dict(prior_manifest)
        manifest["resumed_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        manifest["resume_from_processed_fake_draws"] = processed
        manifest["resume_from_next_fake_index"] = fake_index
        manifest.pop("stop_reason", None)
    else:
        draws = [synthetic_draw(fake_index, rng), synthetic_draw(fake_index + 1, rng)]
        fake_index += 2
        manifest = {
            "memory_source": "SYNTHETIC_FAKE_IIW",
            "schema": "iiw.synthetic_memory.v2",
            "seed": seed,
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "stop_file": str(stop_file),
            "checkpoint_every": checkpoint_every,
            "processed_fake_draws": 0,
        }
    manifest["schema"] = "iiw.synthetic_memory.v2"
    manifest["stop_file"] = str(stop_file)
    manifest["checkpoint_every"] = checkpoint_every

    while True:
        if target_processed is not None and processed >= target_processed:
            break
        if stop_file.exists():
            manifest["stop_reason"] = "STOP_FILE"
            break

        draws.append(synthetic_draw(fake_index, rng))
        fake_index += 1
        current_index = len(draws) - 2
        packet = build_draw_set_packet(draws, current_index)
        next_packet = build_draw_set_packet(draws, current_index + 1)
        taxonomy = build_seat_taxonomy_packet(packet, next_packet)
        case = conditional_motion_memory_case(taxonomy.to_payload())
        if case is not None:
            case["white_balls"] = list(draws[current_index].white_balls)
            for level in LEVELS:
                key = build_conditional_motion_memory_key(case, level=level)
                rooms = rooms_by_level[level]
                if key not in rooms:
                    rooms[key] = empty_room(level, key, case)
                update_room(rooms[key], case, sample_limit=sample_limit)

        processed += 1
        manifest["processed_fake_draws"] = processed
        manifest["processed_this_run"] = processed - initial_processed
        manifest["next_fake_index"] = fake_index
        manifest["tail_draws"] = [draw.to_payload() for draw in draws[-2:]]
        manifest["rng_state_b64"] = encode_rng_state(rng)
        if processed - last_checkpoint >= checkpoint_every:
            elapsed = max(time.perf_counter() - started, 0.001)
            manifest["draws_per_second"] = round((processed - initial_processed) / elapsed, 2)
            write_checkpoint(output_dir, rooms_by_level, manifest)
            last_checkpoint = processed

    elapsed = max(time.perf_counter() - started, 0.001)
    manifest["processed_fake_draws"] = processed
    manifest["processed_this_run"] = processed - initial_processed
    manifest["next_fake_index"] = fake_index
    manifest["tail_draws"] = [draw.to_payload() for draw in draws[-2:]]
    manifest["rng_state_b64"] = encode_rng_state(rng)
    manifest["draws_per_second"] = round((processed - initial_processed) / elapsed, 2)
    manifest.setdefault("stop_reason", "MAX_DRAWS" if max_draws is not None else "FINISHED")
    write_checkpoint(output_dir, rooms_by_level, manifest)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Fake IIW Memory Harness",
        description="Generate synthetic IIW draw chains and write Level 2-5 memory rooms.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where synthetic memory shards are written.",
    )
    parser.add_argument(
        "--stop-file",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / "STOP",
        help="Create this file to stop the harness at the next loop check.",
    )
    parser.add_argument(
        "--max-draws",
        type=int,
        default=None,
        help="Optional maximum fake draws to process. Defaults to unlimited.",
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=25_000,
        help="Write memory shards after this many processed fake draws.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260622,
        help="Random seed for reproducible synthetic draw generation.",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=5,
        help="Maximum sample records stored inside each synthetic room.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Reload existing synthetic memory rooms and continue from manifest state.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.max_draws is not None and args.max_draws < 1:
        raise ValueError("--max-draws must be at least 1 when provided.")
    if args.checkpoint_every < 1:
        raise ValueError("--checkpoint-every must be at least 1.")
    run_harness(
        output_dir=args.output_dir,
        stop_file=args.stop_file,
        max_draws=args.max_draws,
        checkpoint_every=args.checkpoint_every,
        seed=args.seed,
        sample_limit=args.sample_limit,
        resume=args.resume,
    )


if __name__ == "__main__":
    main()
