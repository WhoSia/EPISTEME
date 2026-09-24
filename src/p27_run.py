from __future__ import annotations

import argparse
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from p17_external_run import (
    MODELS,
    REPLICATE_SEEDS,
    TEMPERATURE,
    TOP_P,
    MAX_OUTPUT_TOKENS,
    call_model,
)
from p27_packets import blinded_packets

STAGE = "EPISTEME-P27"
MODEL_KEY = "gemini"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def model_offset() -> int:
    return int(hashlib.sha256(b"P27:gemini").hexdigest()[:8], 16) % 10000


def run() -> dict:
    rows = []
    packets = blinded_packets()
    off = model_offset()

    for rep, seed in enumerate(REPLICATE_SEEDS, 1):
        ordered = list(packets)
        random.Random(seed + off).shuffle(ordered)
        for item in ordered:
            started = now_iso()
            try:
                raw, parsed, attempts, repairs = call_model(
                    MODEL_KEY, item["packet"], seed
                )
                status = "OK"
            except Exception as exc:
                raw = {"error": repr(exc)}
                parsed = None
                attempts = 0
                repairs = 0
                status = "FORMAT_OR_API_FAIL"

            rows.append({
                "stage": STAGE,
                "provider": MODELS[MODEL_KEY]["provider"],
                "model": MODELS[MODEL_KEY]["model"],
                "packet_id": item["packet_id"],
                "replicate": rep,
                "seed": seed,
                "run_started_at": started,
                "sampling": {
                    "temperature": TEMPERATURE,
                    "top_p": TOP_P,
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
                },
                "http_attempts": attempts,
                "format_repairs": repairs,
                "status": status,
                "raw_response": raw,
                "parsed_response": parsed,
            })

    return {
        "stage": STAGE,
        "model_key": MODEL_KEY,
        "provider": MODELS[MODEL_KEY]["provider"],
        "model": MODELS[MODEL_KEY]["model"],
        "rows": rows,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(run(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
