from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from groq import Groq
from google import genai
from google.genai import types

from p16_packets import blinded_packets

STAGE = "EPISTEME-P17"

PROMPT = (
    "You are reviewing a scientific archive and an incumbent sufficiency claim. "
    "Using only the retained information in this archive, propose the single strongest "
    "experiment that could falsify the claim. Do not invent missing variables, relations, "
    "or measurements. If the archive does not justify a specific falsifying experiment, "
    "return NONE. Return only a JSON object with exactly these keys: challenge, intervention, "
    "predicted_direction, rationale_ids. challenge must be a concise string or NONE; "
    "intervention must be an available intervention ID or null; predicted_direction must be "
    "different, same, or null; rationale_ids must be a JSON array of retained evidence IDs."
)

FORMAT_REPAIR_SUFFIX = (
    "\n\nFORMAT REPAIR ONLY: your previous response was invalid under the required JSON "
    "contract. Return only the required JSON object. Do not change the scientific judgment."
)

MODELS = {
    "qwen": {
        "provider": "groq",
        "model": "qwen/qwen3.8-27b",
        "reasoning_effort": "default",
        "reasoning_format": "hidden",
    },
    "gemini": {
        "provider": "gemini",
        "model": "gemini-3.5-flash-lite",
    },
    "gptoss": {
        "provider": "groq",
        "model": "openai/gpt-oss-120b",
        "reasoning_effort": "medium",
        "reasoning_format": "hidden",
    },
}

TEMPERATURE = 0.6
TOP_P = 0.95
MAX_OUTPUT_TOKENS = 512
REPLICATE_SEEDS = [1701, 1702, 1703]
BACKOFF = [2, 8, 20]

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "challenge": {"type": ["string", "null"]},
        "intervention": {"type": ["string", "null"]},
        "predicted_direction": {
            "type": ["string", "null"],
            "enum": ["different", "same", None],
        },
        "rationale_ids": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["challenge", "intervention", "predicted_direction", "rationale_ids"],
    "additionalProperties": False,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _prompt(packet: dict[str, Any], repair: bool) -> str:
    suffix = FORMAT_REPAIR_SUFFIX if repair else ""
    return PROMPT + suffix + "\n\nARCHIVE:\n" + json.dumps(packet, ensure_ascii=False)


def validate(parsed: dict[str, Any]) -> None:
    expected = {"challenge", "intervention", "predicted_direction", "rationale_ids"}
    if set(parsed) != expected:
        raise ValueError("schema keys mismatch")
    if parsed["predicted_direction"] not in {"different", "same", None}:
        raise ValueError("bad predicted_direction")
    if not isinstance(parsed["rationale_ids"], list):
        raise ValueError("bad rationale_ids")
    if not all(isinstance(x, str) for x in parsed["rationale_ids"]):
        raise ValueError("bad rationale_ids")
    if parsed["challenge"] is not None and not isinstance(parsed["challenge"], str):
        raise ValueError("bad challenge")
    if parsed["intervention"] is not None and not isinstance(parsed["intervention"], str):
        raise ValueError("bad intervention")


def with_transport_retry(fn):
    last_exc: Exception | None = None
    for attempt in range(1, 5):
        try:
            return fn(), attempt
        except Exception as exc:
            last_exc = exc
            # SDK clients normalize network/rate-limit/server failures differently.
            # Calibration distinguishes transport/API failure from scientific failure;
            # no semantic answer is retried here.
            if attempt == 4:
                raise
            time.sleep(BACKOFF[min(attempt - 1, len(BACKOFF) - 1)])
    raise RuntimeError(f"transport failed: {last_exc}")


def groq_call(
    model_cfg: dict[str, Any],
    packet: dict[str, Any],
    seed: int,
    repair: bool = False,
) -> tuple[dict[str, Any], str, int]:
    client = Groq(api_key=os.environ["GROQ_API_KEY"], max_retries=0)

    kwargs: dict[str, Any] = {
        "model": model_cfg["model"],
        "messages": [{"role": "user", "content": _prompt(packet, repair)}],
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "seed": seed,
        "max_completion_tokens": MAX_OUTPUT_TOKENS,
        "reasoning_effort": model_cfg["reasoning_effort"],
        "reasoning_format": model_cfg["reasoning_format"],
        "stream": False,
    }

    if model_cfg["model"] in {"openai/gpt-oss-120b", "qwen/qwen3.8-27b"}:
        kwargs["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "episteme_challenge",
                "strict": True,
                "schema": RESPONSE_SCHEMA,
            },
        }

    response, attempts = with_transport_retry(
        lambda: client.chat.completions.create(**kwargs)
    )
    content = response.choices[0].message.content or ""
    raw = response.model_dump()
    return raw, content, attempts


def gemini_call(
    model_cfg: dict[str, Any],
    packet: dict[str, Any],
    seed: int,
    repair: bool = False,
) -> tuple[dict[str, Any], str, int]:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    config = types.GenerateContentConfig(
        temperature=TEMPERATURE,
        top_p=TOP_P,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        response_mime_type="application/json",
        response_json_schema=RESPONSE_SCHEMA,
        seed=seed,
    )

    response, attempts = with_transport_retry(
        lambda: client.models.generate_content(
            model=model_cfg["model"],
            contents=_prompt(packet, repair),
            config=config,
        )
    )

    content = response.text or ""
    raw = {
        "text": response.text,
        "usage_metadata": (
            response.usage_metadata.model_dump()
            if getattr(response, "usage_metadata", None) is not None
            and hasattr(response.usage_metadata, "model_dump")
            else str(getattr(response, "usage_metadata", None))
        ),
    }
    return raw, content, attempts


def decode_model_json(content: str) -> dict[str, Any]:
    text = content.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        if start < 0:
            raise
        decoder = json.JSONDecoder()
        parsed, _end = decoder.raw_decode(text[start:])

    if not isinstance(parsed, dict):
        raise ValueError("top-level JSON must be object")

    return parsed


def call_model(
    model_key: str,
    packet: dict[str, Any],
    seed: int,
) -> tuple[dict[str, Any], dict[str, Any], int, int]:
    cfg = MODELS[model_key]
    clean_packet = {k: v for k, v in packet.items() if not k.startswith("_")}
    caller = groq_call if cfg["provider"] == "groq" else gemini_call

    raw, content, attempts = caller(cfg, clean_packet, seed, False)

    try:
        parsed = decode_model_json(content)
        validate(parsed)
        return raw, parsed, attempts, 0
    except (json.JSONDecodeError, ValueError, TypeError):
        # Exactly one format-only repair. This is triggered by parsing/schema failure,
        # never by a scientifically wrong but well-formed answer.
        raw2, content2, attempts2 = caller(cfg, clean_packet, seed, True)
        parsed2 = decode_model_json(content2)
        validate(parsed2)
        return raw2, parsed2, attempts + attempts2, 1


def calibration_packets() -> list[dict[str, Any]]:
    return [
        {
            "archive_id": "cal-v1",
            "claim": "The terminal summary alone predicts challenge response.",
            "terminal_observation": {"a": "stable", "b": "stable"},
            "available_interventions": ["c1", "c2"],
            "retained_history": [
                {"history": "a", "trace": ["rA"]},
                {"history": "b", "trace": ["rB"]},
            ],
            "relation_notes": [
                {"source": "rA/rB", "intervention": "c1", "response_link": "history-sensitive"}
            ],
            "_expected": {"kind": "VALID", "intervention": "c1", "direction": "different"},
        },
        {
            "archive_id": "cal-v2",
            "claim": "The terminal summary alone predicts challenge response.",
            "terminal_observation": {"a": "stable", "b": "stable"},
            "available_interventions": ["c3", "c4"],
            "retained_history": [
                {"history": "a", "trace": ["p"]},
                {"history": "b", "trace": ["q"]},
            ],
            "relation_notes": [
                {"source": "p/q", "intervention": "c4", "response_link": "history-sensitive"}
            ],
            "_expected": {"kind": "VALID", "intervention": "c4", "direction": "different"},
        },
        {
            "archive_id": "cal-n1",
            "claim": "The terminal summary alone predicts challenge response.",
            "terminal_observation": {"a": "stable", "b": "stable"},
            "available_interventions": ["c5"],
            "retained_history": [
                {"history": "a", "trace": ["d1"]},
                {"history": "b", "trace": ["d2"]},
            ],
            "relation_notes": [
                {"source": "d1/d2", "intervention": "c5", "response_link": "history-invariant"}
            ],
            "_expected": {"kind": "NONE"},
        },
        {
            "archive_id": "cal-n2",
            "claim": "The terminal summary alone predicts challenge response.",
            "terminal_observation": {"a": "stable", "b": "stable"},
            "available_interventions": ["c6"],
            "retained_history": [
                {"history": "a", "trace": ["x"]},
                {"history": "b", "trace": ["y"]},
            ],
            "relation_notes": [
                {"source": "x/y", "intervention": "c6", "response_link": "irrelevant"}
            ],
            "_expected": {"kind": "NONE"},
        },
    ]


def calibration_correct(parsed: dict[str, Any], expected: dict[str, Any]) -> bool:
    challenge = parsed.get("challenge")
    if expected["kind"] == "NONE":
        return challenge is None or str(challenge).upper() == "NONE"
    return (
        challenge is not None
        and str(challenge).upper() != "NONE"
        and parsed.get("intervention") == expected["intervention"]
        and parsed.get("predicted_direction") == expected["direction"]
    )


def run_calibration(model_key: str) -> dict[str, Any]:
    rows = []
    valid_correct = 0
    none_correct = 0
    total_correct = 0

    for i, packet in enumerate(calibration_packets()):
        expected = packet["_expected"]
        try:
            raw, parsed, attempts, format_repairs = call_model(model_key, packet, 9000 + i)
            ok = calibration_correct(parsed, expected)
            status = "OK" if ok else "SEMANTIC_FAIL"
        except Exception as exc:
            raw = {"error": repr(exc)}
            parsed = None
            attempts = 0
            format_repairs = 0
            ok = False
            status = "FORMAT_OR_API_FAIL"

        total_correct += int(ok)
        if expected["kind"] == "VALID":
            valid_correct += int(ok)
        else:
            none_correct += int(ok)

        rows.append({
            "packet_id": packet["archive_id"],
            "expected_kind": expected["kind"],
            "correct": ok,
            "status": status,
            "http_attempts": attempts,
            "format_repairs": format_repairs,
            "raw_response": raw,
            "parsed_response": parsed,
        })

    passed = total_correct >= 3 and valid_correct >= 1 and none_correct >= 1

    return {
        "stage": STAGE,
        "phase": "calibration",
        "model_key": model_key,
        "provider": MODELS[model_key]["provider"],
        "model": MODELS[model_key]["model"],
        "pass": passed,
        "score": total_correct,
        "valid_correct": valid_correct,
        "none_correct": none_correct,
        "rows": rows,
    }


def stable_model_offset(model_key: str) -> int:
    digest = hashlib.sha256(model_key.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 10000


def run_main(model_key: str) -> dict[str, Any]:
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

            rows.append({
                "stage": STAGE,
                "phase": "main",
                "provider": MODELS[model_key]["provider"],
                "model": MODELS[model_key]["model"],
                "model_endpoint": MODELS[model_key]["model"],
                "run_started_at": started,
                "packet_id": item["packet_id"],
                "replicate": rep,
                "seed": seed,
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
            })

    return {
        "stage": STAGE,
        "phase": "main",
        "model_key": model_key,
        "provider": MODELS[model_key]["provider"],
        "model": MODELS[model_key]["model"],
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["calibration", "main"], required=True)
    parser.add_argument("--model", choices=sorted(MODELS), required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    result = run_calibration(args.model) if args.phase == "calibration" else run_main(args.model)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.phase == "calibration" and not result["pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
