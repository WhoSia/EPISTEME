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
from p21_packets import blinded_packets

STAGE = "EPISTEME-P21"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_model_offset(model_key: str) -> int:
    digest = hashlib.sha256(("P21:" + model_key).encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 10000


def run(model_key: str) -> dict:
    rows = []
    packets = blinded_packets()
    offset = stable_model_offset(model_key)

    for rep, seed in enumerate(REPLICATE_SEEDS, 1):
        ordered = list(packets)
        random.Random(seed + offset).shuffle(ordered)

        for item in ordered:
            started = now_iso()
            try:
                raw, parsed, attempts, format_repairs = call_model(
                    model_key, item["packet"], seed
                )
                status = "OK"
            except Exception as exc:
                raw = {"error": repr(exc)}
                parsed = None
                attempts = 0
                format_repairs = 0
                status = "FORMAT_OR_API_FAIL"

            rows.append(
                {
                    "stage": STAGE,
                    "provider": MODELS[model_key]["provider"],
                    "model": MODELS[model_key]["model"],
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
                    "format_repairs": format_repairs,
                    "status": status,
                    "raw_response": raw,
                    "parsed_response": parsed,
                }
            )

    return {
        "stage": STAGE,
        "model_key": model_key,
        "provider": MODELS[model_key]["provider"],
        "model": MODELS[model_key]["model"],
        "rows": rows,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=sorted(MODELS), required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    result = run(args.model)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
