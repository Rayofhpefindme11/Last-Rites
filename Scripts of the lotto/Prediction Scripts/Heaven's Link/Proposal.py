from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value or "").strip().replace(",", "")))
    except ValueError:
        return default


def clean_body(values: Any) -> list[int]:
    body = [parse_int(value) for value in values or []]
    if len(body) != 5:
        return []
    if any(not (1 <= value <= 69) for value in body):
        return []
    if body != sorted(body) or len(set(body)) != 5:
        return []
    return body


def body_key(body: list[int]) -> str:
    return "-".join(str(value) for value in body)


def packet_id(prefix: str, payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return f"{prefix}-{hashlib.sha1(raw).hexdigest()[:12]}"


def rank_one_from_gatherer(gatherer_packet: dict[str, Any] | None) -> dict[str, Any]:
    gatherer_packet = gatherer_packet or {}
    gathered = gatherer_packet.get("gathered_bodies") or []
    if gathered and isinstance(gathered[0], dict):
        return gathered[0]
    leader = clean_body(gatherer_packet.get("leader_body") or [])
    if leader:
        return {
            "sorted_body": leader,
            "body_key": gatherer_packet.get("leader_body_key") or body_key(leader),
            "gatherer_score": gatherer_packet.get("leader_score"),
            "reasons": ["leader_body_fallback"],
        }
    return {}


def build_proposal_packet(gatherer_packet: dict[str, Any] | None) -> dict[str, Any]:
    gatherer_packet = gatherer_packet or {}
    rank_one = rank_one_from_gatherer(gatherer_packet)
    proposal_body = clean_body(rank_one.get("sorted_body") or [])
    proposal_key = body_key(proposal_body) if proposal_body else ""
    output = {
        "schema": "serenity.life_link.proposal.v1",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PROPOSAL_READY" if proposal_body else "NO_PROPOSAL",
        "canonical_name": "The Proposal",
        "source_packet_ids": [
            gatherer_packet.get("packet_id"),
        ],
        "answer_identity": gatherer_packet.get("answer_identity") or {},
        "rank_source": "gatherer_rank_1",
        "proposal_rank": 1 if proposal_body else None,
        "proposal_body": proposal_body,
        "proposal_body_key": proposal_key,
        "proposal_score_from_gatherer": rank_one.get("gatherer_score"),
        "proposal_record": rank_one,
        "gatherer_body_count": gatherer_packet.get("gathered_body_count"),
        "downstream_policy": {
            "next_stage": "TAKE_PROPOSAL_BODY_AS_RANK_1",
            "hard_filter": "PROPOSAL_BODY_ONLY",
        },
        "law": (
            "Proposal does not rank, cut, score, rescue, or expand. "
            "It simply publishes Gatherer's rank 1 body."
        ),
    }
    output["packet_id"] = packet_id("proposal", output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Proposal packet from Gatherer output.")
    parser.add_argument("--gatherer", required=True, help="Path to Gatherer packet JSON.")
    parser.add_argument("--output", required=True, help="Path to write Proposal packet JSON.")
    args = parser.parse_args()
    gatherer = json.loads(Path(args.gatherer).read_text(encoding="utf-8"))
    packet = build_proposal_packet(gatherer)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(f"Wrote Proposal packet: {output}")


if __name__ == "__main__":
    main()
