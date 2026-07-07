#!/usr/bin/env python3
"""Run the smallest useful QA spine for a synthetic assistant workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_CASE = Path("examples/spine_case.json")
ALLOWED_ACTIONS = {"summarize", "ask_clarifying_question"}


def validate_output(raw_output: str, source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        output = json.loads(raw_output)
    except json.JSONDecodeError as exc:
        return [f"output is not valid JSON: {exc.msg}"]

    if not isinstance(output, dict):
        return ["output must be a JSON object"]

    answer = output.get("answer")
    action = output.get("action")
    citations = output.get("citations")
    writes = output.get("writes")

    if not isinstance(answer, str) or not answer.strip():
        errors.append("answer must be non-empty text")
    if action not in ALLOWED_ACTIONS:
        errors.append(f"action must be one of: {', '.join(sorted(ALLOWED_ACTIONS))}")
    if not isinstance(citations, list) or not all(isinstance(item, str) for item in citations):
        errors.append("citations must be a list of source IDs")
        citations = []
    if not citations:
        errors.append("citations must not be empty")
    if not isinstance(writes, list):
        errors.append("writes must be a list")
    elif writes:
        errors.append("writes must be empty for this read-only spine")

    unknown = sorted(set(citations) - source_ids)
    if unknown:
        errors.append(f"unknown citations: {', '.join(unknown)}")
    return errors


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_spine(path: Path) -> int:
    case = json.loads(path.read_text(encoding="utf-8"))
    source_ids_raw = case["source_ids"]
    expected_text = case["expected_answer_contains"]
    known_bad_outputs = case["known_bad_outputs"]
    require(
        isinstance(source_ids_raw, list) and all(isinstance(item, str) for item in source_ids_raw),
        "source_ids must be a list of source IDs",
    )
    require(
        isinstance(expected_text, list) and all(isinstance(item, str) for item in expected_text),
        "expected_answer_contains must be a list of text snippets",
    )
    require(isinstance(known_bad_outputs, list), "known_bad_outputs must be a list")
    source_ids = set(source_ids_raw)

    happy_errors = validate_output(case["model_output"], source_ids)
    require(not happy_errors, "; ".join(happy_errors))
    print("PASS happy_path_contract")

    output = json.loads(case["model_output"])
    answer = output["answer"].casefold()
    for expected in expected_text:
        require(expected.casefold() in answer, f"answer missing expected text: {expected}")
    print("PASS happy_path_answer")

    for bad in known_bad_outputs:
        require(isinstance(bad, dict), "known_bad_outputs entries must be objects")
        bad_errors = validate_output(bad["model_output"], source_ids)
        require(bad_errors, f"known bad output passed: {bad['case']}")
    print("PASS known_bad_outputs")

    print("PASS green_spine")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=str(DEFAULT_CASE))
    args = parser.parse_args()
    try:
        return run_spine(Path(args.path))
    except (AssertionError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL green_spine: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
