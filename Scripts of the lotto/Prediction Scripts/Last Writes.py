from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PREDICTION_DIR = SCRIPT_PATH.parent
SCRIPTS_DIR = PREDICTION_DIR.parent
PROJECT_ROOT = SCRIPTS_DIR.parent
FOUNDATION_DIR = SCRIPTS_DIR / "Foundation Scripts"
DEFAULT_OUTPUT_DIR = PREDICTION_DIR / "Packets"
DEFAULT_MEMORY_PATH = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "hierarchical_conditional_motion_memory_levels_2_5_2015-10-07.json"
)
DEFAULT_SYNTHETIC_DIR = (
    PROJECT_ROOT
    / "Books of The Lotto"
    / "Books Of Complextity"
    / "Synthetic Memory"
)

if str(FOUNDATION_DIR) not in sys.path:
    sys.path.insert(0, str(FOUNDATION_DIR))


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


IIW = load_module("last_writes_iiw", FOUNDATION_DIR / "Infinite_Inner_World.py")
SEAT_TAXONOMY = load_module("last_writes_seat_taxonomy", FOUNDATION_DIR / "Seat_Taxonomy.py")
MEMORY_RESOLVER = load_module(
    "last_writes_conditional_memory_resolver",
    FOUNDATION_DIR / "Conditional_Memory_Resolver.py",
)
FAKE_IIW_HARNESS = load_module(
    "last_writes_fake_iiw_memory_harness",
    FOUNDATION_DIR / "Fake_IIW_Memory_Harness.py",
)


MODE_POLICIES: dict[str, dict[str, Any]] = {
    "utopia": {
        "purpose": "Normal guarded Last Rites route with Seat Taxonomy and Conditional Memory.",
        "operating_mode": "utopia",
        "overlay_modes": [],
        "uses_official_memory": True,
        "uses_synthetic_memory": True,
        "allows_target_context": False,
        "live_safety": "CURRENT_AND_PRIOR_ONLY",
    },
    "arcana": {
        "purpose": "Deeper explanation route with full memory-room reporting.",
        "operating_mode": "arcana",
        "legacy_alias": "arcania",
        "overlay_modes": [],
        "uses_official_memory": True,
        "uses_synthetic_memory": True,
        "allows_target_context": False,
        "live_safety": "CURRENT_AND_PRIOR_ONLY_DEEP_READ",
    },
    "arcania": {
        "purpose": "Legacy alias for arcana.",
        "operating_mode": "arcana",
        "alias_for": "arcana",
        "overlay_modes": [],
        "uses_official_memory": True,
        "uses_synthetic_memory": True,
        "allows_target_context": False,
        "live_safety": "CURRENT_AND_PRIOR_ONLY_DEEP_READ",
    },
    "nightfall": {
        "purpose": "Held-out live-safe overlay. Next draw truth is blocked from the read.",
        "operating_mode": "utopia",
        "overlay_modes": ["NIGHTFALL"],
        "legacy_alias": "lightless",
        "uses_official_memory": True,
        "uses_synthetic_memory": True,
        "allows_target_context": False,
        "live_safety": "STRICT_HELD_OUT",
        "blocked_promotions": [
            "next_draw_truth",
            "outgoing_contract_from_future",
            "exact_target_replay",
            "future_collision_validation",
        ],
    },
    "lightless": {
        "purpose": "Legacy alias for nightfall.",
        "operating_mode": "utopia",
        "alias_for": "nightfall",
        "overlay_modes": ["NIGHTFALL"],
        "uses_official_memory": True,
        "uses_synthetic_memory": True,
        "allows_target_context": False,
        "live_safety": "STRICT_HELD_OUT",
    },
    "short_circuit_historical": {
        "purpose": "Diagnostic replay/debug mode; kept for parity but not used for live trust.",
        "operating_mode": "short_circuit_historical",
        "overlay_modes": ["DIAGNOSTIC_REPLAY"],
        "uses_official_memory": True,
        "uses_synthetic_memory": False,
        "allows_target_context": True,
        "live_safety": "DIAGNOSTIC_ONLY",
    },
}

STAGE_ORDER = (
    "seat_taxonomy",
    "conditional_memory",
    "voice_of_hope",
    "gatherer",
    "proposal",
    "fake_iiw_harness",
)


def safe_name(value: str | None) -> str:
    return str(value or "latest").replace("-", "_").replace("/", "_").replace(" ", "_")


def mode_policy(mode: str) -> dict[str, Any]:
    if mode not in MODE_POLICIES:
        raise ValueError(f"Unsupported Last Writes mode: {mode}")
    return deepcopy(MODE_POLICIES[mode])


def write_packet(output_dir: Path, stage: str, mode: str, as_of: str | None, packet: dict[str, Any]) -> Path:
    stage_dir = output_dir / stage
    stage_dir.mkdir(parents=True, exist_ok=True)
    output = stage_dir / f"{stage}_{safe_name(mode)}_{safe_name(as_of)}.json"
    output.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return output


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def select_draw_index(draws: list[Any], as_of: str | None, latest: bool) -> int:
    if latest or as_of is None:
        return len(draws) - 1
    target = IIW.parse_draw_date(as_of)
    for draw in draws:
        if draw.draw_date == target:
            return draw.draw_index
    raise ValueError(f"No draw found for --as-of {as_of}.")


def build_seat_taxonomy_stage(
    csv_path: Path,
    as_of: str | None,
    latest: bool,
    policy: dict[str, Any],
) -> dict[str, Any]:
    draws = IIW.load_historical_draws(csv_path)
    index = select_draw_index(draws, as_of=as_of, latest=latest)
    current = IIW.build_draw_set_packet(draws, index)
    include_next = policy.get("allows_target_context") is True and index + 1 < len(draws)
    next_packet = IIW.build_draw_set_packet(draws, index + 1) if include_next else None
    packet = SEAT_TAXONOMY.build_seat_taxonomy_packet(current, next_packet)
    payload = packet.to_payload()
    payload["last_writes_stage"] = {
        "stage": "seat_taxonomy",
        "mode_policy": policy,
        "next_draw_included": include_next,
        "law": "Nightfall/Utopia block next draw truth; short_circuit_historical may include it for diagnostic replay.",
    }
    return payload


def build_conditional_memory_stage(
    seat_taxonomy: dict[str, Any],
    memory_path: Path,
    synthetic_dir: Path,
    policy: dict[str, Any],
) -> dict[str, Any]:
    official_memory = load_json(memory_path)
    official_resolution = MEMORY_RESOLVER.build_resolution(seat_taxonomy, official_memory)
    synthetic_manifest_path = synthetic_dir / "manifest.json"
    synthetic_manifest = (
        load_json(synthetic_manifest_path)
        if synthetic_manifest_path.exists()
        else {
            "status": "SYNTHETIC_MEMORY_NOT_FOUND",
            "path": str(synthetic_manifest_path),
        }
    )
    return {
        "schema": "last_writes.conditional_memory_stage.v1",
        "status": "CONDITIONAL_MEMORY_READY",
        "official_memory_path": str(memory_path),
        "synthetic_memory_dir": str(synthetic_dir),
        "uses_synthetic_memory": policy.get("uses_synthetic_memory") is True,
        "official_resolution": official_resolution,
        "synthetic_manifest": synthetic_manifest,
        "law": (
            "Official memory is proof of happened history. Synthetic memory is coverage. "
            "The live draw selects the address; memory supplies the outcome field."
        ),
    }


def top_rank(field: dict[str, Any], name: str) -> dict[str, Any] | None:
    rows = field.get(name) or []
    return rows[0] if rows else None


def build_voice_of_hope_stage(
    seat_taxonomy: dict[str, Any],
    conditional_memory: dict[str, Any],
) -> dict[str, Any]:
    resolution = conditional_memory["official_resolution"]
    read = resolution["memory_read"]
    field = read.get("outcome_field") or {}
    branch = top_rank(field, "branch_rank")
    family = top_rank(field, "family_rank")
    lane = top_rank(field, "lane_rank")
    flow = top_rank(field, "flow_rank")
    transfer = top_rank(field, "transfer_rank")
    return {
        "schema": "last_writes.voice_of_hope.v1",
        "status": "VOICE_OF_HOPE_READY" if field else "VOICE_OF_HOPE_NO_MEMORY_FIELD",
        "canonical_name": "Voice Of Hope",
        "source": "CONDITIONAL_MEMORY_RESOLVER",
        "draw": resolution["draw"],
        "memory_read_status": read["read_status"],
        "deepest_matched_level": read["deepest_matched_level"],
        "recommended_use": read["recommended_use"],
        "selected_outgoing_contract": {
            "branch": branch,
            "family": family,
            "lane": lane,
            "flow": flow,
            "transfer": transfer,
        },
        "truth_control": seat_taxonomy["truth_control"],
        "law": (
            "Last Writes Voice Of Hope manifests the outgoing-motion field selected "
            "by conditional memory. It does not invent a branch outside the memory read."
        ),
    }


def build_gatherer_stage(voice: dict[str, Any]) -> dict[str, Any]:
    contract = voice.get("selected_outgoing_contract") or {}
    ranked = []
    for key in ("family", "branch", "lane", "flow", "transfer"):
        row = contract.get(key)
        if row:
            ranked.append({"field": key, **row})
    return {
        "schema": "last_writes.gatherer.v1",
        "status": "GATHERER_READY" if ranked else "GATHERER_NO_MEMORY_FIELD",
        "canonical_name": "The Gatherer",
        "answer_identity": {
            "memory_read_status": voice.get("memory_read_status"),
            "deepest_matched_level": voice.get("deepest_matched_level"),
            "recommended_use": voice.get("recommended_use"),
        },
        "gathered_motion_fields": ranked,
        "gathered_body_count": len(ranked),
        "law": "The Gatherer collects the memory-selected motion fields without expanding them.",
    }


def build_proposal_stage(gatherer: dict[str, Any]) -> dict[str, Any]:
    fields = gatherer.get("gathered_motion_fields") or []
    branch = next((row for row in fields if row.get("field") == "branch"), None)
    family = next((row for row in fields if row.get("field") == "family"), None)
    return {
        "schema": "last_writes.proposal.v1",
        "status": "PROPOSAL_READY" if branch or family else "NO_PROPOSAL",
        "canonical_name": "The Proposal",
        "proposal_type": "OUTGOING_MOTION_CONTRACT",
        "proposal_branch": branch,
        "proposal_family": family,
        "proposal_record": {
            "branch": branch,
            "family": family,
            "all_fields": fields,
        },
        "law": (
            "Proposal publishes the rank-1 outgoing motion contract from Gatherer. "
            "It does not convert that contract into final numbers yet."
        ),
    }


def build_fake_harness_status(synthetic_dir: Path) -> dict[str, Any]:
    manifest = synthetic_dir / "manifest.json"
    if not manifest.exists():
        return {
            "schema": "last_writes.fake_iiw_harness_status.v1",
            "status": "FAKE_IIW_HARNESS_NO_MANIFEST",
            "synthetic_memory_dir": str(synthetic_dir),
        }
    payload = load_json(manifest)
    payload["schema"] = "last_writes.fake_iiw_harness_status.v1"
    payload["status"] = "FAKE_IIW_HARNESS_STATUS_READY"
    return payload


def maybe_run_fake_harness(args: argparse.Namespace) -> dict[str, Any]:
    if not args.run_fake_iiw_harness:
        return build_fake_harness_status(args.synthetic_memory_dir)
    FAKE_IIW_HARNESS.run_harness(
        output_dir=args.synthetic_memory_dir,
        stop_file=args.fake_stop_file,
        max_draws=args.fake_max_draws,
        checkpoint_every=args.fake_checkpoint_every,
        seed=args.fake_seed,
        sample_limit=args.fake_sample_limit,
    )
    return build_fake_harness_status(args.synthetic_memory_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Last Writes prediction orchestrator.")
    parser.add_argument("--mode", choices=sorted(MODE_POLICIES), default="utopia")
    parser.add_argument("--as-of")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--csv-path", type=Path, default=IIW.DEFAULT_CSV_PATH)
    parser.add_argument("--memory-path", type=Path, default=DEFAULT_MEMORY_PATH)
    parser.add_argument("--synthetic-memory-dir", type=Path, default=DEFAULT_SYNTHETIC_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--stop-after", choices=STAGE_ORDER, default="proposal")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--run-fake-iiw-harness", action="store_true")
    parser.add_argument("--fake-max-draws", type=int)
    parser.add_argument("--fake-checkpoint-every", type=int, default=250_000)
    parser.add_argument("--fake-seed", type=int, default=2026062202)
    parser.add_argument("--fake-sample-limit", type=int, default=5)
    parser.add_argument(
        "--fake-stop-file",
        type=Path,
        default=DEFAULT_SYNTHETIC_DIR / "STOP",
    )
    return parser


def finish(status: str, outputs: dict[str, str], payload: dict[str, Any], as_json: bool) -> None:
    summary = {
        "status": status,
        "outputs": outputs,
        "payload": payload,
    }
    print(json.dumps(summary, indent=2) if as_json else json.dumps({k: v for k, v in summary.items() if k != "payload"}, indent=2))


def main() -> None:
    args = build_parser().parse_args()
    policy = mode_policy(args.mode)
    outputs: dict[str, str] = {}

    seat_taxonomy = build_seat_taxonomy_stage(args.csv_path, args.as_of, args.latest, policy)
    outputs["seat_taxonomy"] = str(
        write_packet(args.output_dir, "seat_taxonomy", args.mode, args.as_of, seat_taxonomy)
    )
    if args.stop_after == "seat_taxonomy":
        finish("SEAT_TAXONOMY_READY", outputs, seat_taxonomy, args.json)
        return

    conditional_memory = build_conditional_memory_stage(
        seat_taxonomy,
        args.memory_path,
        args.synthetic_memory_dir,
        policy,
    )
    outputs["conditional_memory"] = str(
        write_packet(args.output_dir, "conditional_memory", args.mode, args.as_of, conditional_memory)
    )
    if args.stop_after == "conditional_memory":
        finish("CONDITIONAL_MEMORY_READY", outputs, conditional_memory, args.json)
        return

    voice = build_voice_of_hope_stage(seat_taxonomy, conditional_memory)
    outputs["voice_of_hope"] = str(
        write_packet(args.output_dir, "voice_of_hope", args.mode, args.as_of, voice)
    )
    if args.stop_after == "voice_of_hope":
        finish(str(voice["status"]), outputs, voice, args.json)
        return

    gatherer = build_gatherer_stage(voice)
    outputs["gatherer"] = str(
        write_packet(args.output_dir, "gatherer", args.mode, args.as_of, gatherer)
    )
    if args.stop_after == "gatherer":
        finish(str(gatherer["status"]), outputs, gatherer, args.json)
        return

    proposal = build_proposal_stage(gatherer)
    outputs["proposal"] = str(
        write_packet(args.output_dir, "proposal", args.mode, args.as_of, proposal)
    )
    if args.stop_after == "proposal":
        finish(str(proposal["status"]), outputs, proposal, args.json)
        return

    fake_status = maybe_run_fake_harness(args)
    outputs["fake_iiw_harness"] = str(
        write_packet(args.output_dir, "fake_iiw_harness", args.mode, args.as_of, fake_status)
    )
    finish(str(fake_status["status"]), outputs, fake_status, args.json)


if __name__ == "__main__":
    main()
