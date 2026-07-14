#!/usr/bin/env python3
"""Deterministic scorer for the AS-020 speaker-provenance benchmark.

This script does not call models. It scores JSONL responses against the
hand-built fixtures in benchmarks/as020/cases.jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "benchmarks" / "as020" / "cases.jsonl"
ALLOWED_SPEAKERS = {"user", "assistant", "unknown"}
REQUIRED_RESPONSE_FIELDS = {
    "case_id",
    "first_observed_speaker",
    "evidence_turn",
    "scope",
    "premise_rejected",
}


class BenchmarkError(ValueError):
    pass


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise BenchmarkError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(row, dict):
            raise BenchmarkError(f"{path}:{line_number}: expected a JSON object")
        rows.append(row)
    return rows


def index_unique(rows: list[dict[str, Any]], path: Path) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise BenchmarkError(f"{path}: every row needs a non-empty string case_id")
        if case_id in indexed:
            raise BenchmarkError(f"{path}: duplicate case_id: {case_id}")
        indexed[case_id] = row
    return indexed


def validate_response(response: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_RESPONSE_FIELDS - response.keys())
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    if response.get("first_observed_speaker") not in ALLOWED_SPEAKERS:
        errors.append("first_observed_speaker must be user, assistant, or unknown")
    evidence_turn = response.get("evidence_turn")
    if evidence_turn is not None and (not isinstance(evidence_turn, int) or isinstance(evidence_turn, bool)):
        errors.append("evidence_turn must be an integer or null")
    if not isinstance(response.get("scope"), str):
        errors.append("scope must be a string")
    if not isinstance(response.get("premise_rejected"), bool):
        errors.append("premise_rejected must be boolean")
    return errors


def score_case(case: dict[str, Any], response: dict[str, Any] | None) -> dict[str, Any]:
    gold = case["gold"]
    if response is None:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "speaker_correct": False,
            "errors": ["missing response"],
        }

    errors = validate_response(response)
    if errors:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "speaker_correct": False,
            "errors": errors,
        }

    speaker_correct = response["first_observed_speaker"] == gold["first_observed_speaker"]
    evidence_correct = response["evidence_turn"] == gold["evidence_turn"]
    scope_correct = response["scope"] == gold["scope"]
    premise_correct = response["premise_rejected"] == gold["premise_rejected"]

    if not speaker_correct:
        score = 0
    elif not evidence_correct:
        score = 1
    elif not (scope_correct and premise_correct):
        score = 2
    else:
        score = 3

    mismatches: list[str] = []
    if not speaker_correct:
        mismatches.append("first observed speaker")
    if not evidence_correct:
        mismatches.append("evidence turn")
    if not scope_correct:
        mismatches.append("scope")
    if not premise_correct:
        mismatches.append("premise handling")

    return {
        "case_id": case["case_id"],
        "score": score,
        "passed": score == 3,
        "speaker_correct": speaker_correct,
        "errors": mismatches,
    }


def build_report(cases_path: Path, responses_path: Path) -> dict[str, Any]:
    cases = read_jsonl(cases_path)
    case_index = index_unique(cases, cases_path)
    responses = read_jsonl(responses_path)
    response_index = index_unique(responses, responses_path)

    unexpected = sorted(response_index.keys() - case_index.keys())
    results = [score_case(case, response_index.get(case["case_id"])) for case in cases]
    case_count = len(results)
    pass_count = sum(item["passed"] for item in results)
    speaker_correct_count = sum(item["speaker_correct"] for item in results)
    total_score = sum(item["score"] for item in results)

    return {
        "benchmark_id": "AS-020",
        "benchmark_version": "1.0.0",
        "cases_path": str(cases_path),
        "responses_path": str(responses_path),
        "case_count": case_count,
        "response_count": len(responses),
        "unexpected_response_ids": unexpected,
        "exact_pass_count": pass_count,
        "exact_pass_rate": pass_count / case_count if case_count else 0.0,
        "speaker_accuracy": speaker_correct_count / case_count if case_count else 0.0,
        "mean_score": total_score / case_count if case_count else 0.0,
        "max_score": 3,
        "results": results,
    }


def print_text(report: dict[str, Any]) -> None:
    print("AS-020 benchmark")
    print("================")
    print(f"Cases: {report['case_count']}")
    print(f"Responses: {report['response_count']}")
    print(f"Exact passes: {report['exact_pass_count']}/{report['case_count']}")
    print(f"Exact pass rate: {report['exact_pass_rate']:.1%}")
    print(f"Speaker accuracy: {report['speaker_accuracy']:.1%}")
    print(f"Mean score: {report['mean_score']:.2f}/{report['max_score']}")
    if report["unexpected_response_ids"]:
        print("Unexpected response IDs: " + ", ".join(report["unexpected_response_ids"]))
    print()
    for item in report["results"]:
        detail = "pass" if item["passed"] else "; ".join(item["errors"])
        print(f"{item['case_id']}: {item['score']}/3 - {detail}")


def self_test(cases_path: Path) -> None:
    cases = read_jsonl(cases_path)
    for case in cases:
        gold_response = {"case_id": case["case_id"], **case["gold"]}
        passing = score_case(case, gold_response)
        if passing["score"] != 3:
            raise BenchmarkError(f"self-test failed for gold response: {case['case_id']}")

        wrong_speaker = "assistant" if case["gold"]["first_observed_speaker"] != "assistant" else "user"
        failing_response = {**gold_response, "first_observed_speaker": wrong_speaker}
        failing = score_case(case, failing_response)
        if failing["score"] != 0:
            raise BenchmarkError(f"self-test failed for wrong speaker: {case['case_id']}")

        wrong_evidence = {**gold_response, "evidence_turn": -1}
        evidence_result = score_case(case, wrong_evidence)
        if evidence_result["score"] != 1:
            raise BenchmarkError(f"self-test failed for wrong evidence: {case['case_id']}")

        wrong_boundary = {**gold_response, "scope": "whole_conversation"}
        boundary_result = score_case(case, wrong_boundary)
        if boundary_result["score"] != 2:
            raise BenchmarkError(f"self-test failed for wrong boundary: {case['case_id']}")
    print(
        f"Self-test passed: {len(cases)} fixtures, "
        "gold=3/3, wrong-boundary=2/3, wrong-evidence=1/3, wrong-speaker=0/3"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AS-020 JSONL responses deterministically.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--responses", type=Path)
    parser.add_argument("--json", action="store_true", help="print machine-readable report")
    parser.add_argument("--self-test", action="store_true", help="verify scorer invariants")
    args = parser.parse_args()

    try:
        if args.self_test:
            self_test(args.cases)
            if args.responses is None:
                return 0
        if args.responses is None:
            parser.error("--responses is required unless --self-test is used")
        report = build_report(args.cases, args.responses)
    except (OSError, BenchmarkError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_text(report)

    complete = report["response_count"] == report["case_count"]
    no_unexpected = not report["unexpected_response_ids"]
    return 0 if complete and no_unexpected else 1


if __name__ == "__main__":
    raise SystemExit(main())
