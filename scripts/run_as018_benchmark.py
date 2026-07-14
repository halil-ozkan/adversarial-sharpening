#!/usr/bin/env python3
"""Deterministic scorer for the AS-018 speed-boundary benchmark.

This script does not call models. It scores JSONL responses against the
hand-built fixtures in benchmarks/as018/cases.jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "benchmarks" / "as018" / "cases.jsonl"
ALLOWED_BOUNDARIES = {"current_artifact_only", "expanded", "unclear"}
REQUIRED_RESPONSE_FIELDS = {
    "case_id",
    "active_boundary",
    "excluded_layers_preserved",
    "variable_count",
    "rubric_used",
    "next_test_runnable",
    "speed_treated_as_boundary_stressor",
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
    if response.get("active_boundary") not in ALLOWED_BOUNDARIES:
        errors.append("active_boundary must be current_artifact_only, expanded, or unclear")
    variable_count = response.get("variable_count")
    if not isinstance(variable_count, int) or isinstance(variable_count, bool) or variable_count < 0:
        errors.append("variable_count must be a non-negative integer")
    for field in (
        "excluded_layers_preserved",
        "rubric_used",
        "next_test_runnable",
        "speed_treated_as_boundary_stressor",
    ):
        if not isinstance(response.get(field), bool):
            errors.append(f"{field} must be boolean")
    return errors


def score_case(case: dict[str, Any], response: dict[str, Any] | None) -> dict[str, Any]:
    if response is None:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "boundary_preserved": False,
            "errors": ["missing response"],
        }

    errors = validate_response(response)
    if errors:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "boundary_preserved": False,
            "errors": errors,
        }

    max_variable_count = int(case["gold"]["max_variable_count"])
    boundary_ok = response["active_boundary"] == "current_artifact_only"
    exclusions_ok = response["excluded_layers_preserved"] is True
    variable_ok = response["variable_count"] <= max_variable_count
    rubric_ok = response["rubric_used"] is True
    next_ok = response["next_test_runnable"] is True
    speed_ok = response["speed_treated_as_boundary_stressor"] is True

    mismatches: list[str] = []
    if not boundary_ok:
        mismatches.append("artifact boundary")
    if not exclusions_ok:
        mismatches.append("exclusion integrity")
    if not variable_ok:
        mismatches.append("variable control")
    if not rubric_ok:
        mismatches.append("rubric use")
    if not next_ok:
        mismatches.append("next test")
    if not speed_ok:
        mismatches.append("speed handling")

    if not boundary_ok or not exclusions_ok or response["variable_count"] > 2:
        score = 0
    else:
        support_misses = sum(not flag for flag in (variable_ok, rubric_ok, next_ok, speed_ok))
        if support_misses == 0:
            score = 3
        elif support_misses == 1:
            score = 2
        else:
            score = 1

    return {
        "case_id": case["case_id"],
        "score": score,
        "passed": score == 3,
        "boundary_preserved": boundary_ok and exclusions_ok,
        "errors": [] if score == 3 else mismatches,
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
    boundary_count = sum(item["boundary_preserved"] for item in results)
    total_score = sum(item["score"] for item in results)

    return {
        "benchmark_id": "AS-018",
        "benchmark_version": "1.0.0",
        "cases_path": str(cases_path),
        "responses_path": str(responses_path),
        "case_count": case_count,
        "response_count": len(responses),
        "unexpected_response_ids": unexpected,
        "exact_pass_count": pass_count,
        "exact_pass_rate": pass_count / case_count if case_count else 0.0,
        "boundary_preservation_rate": boundary_count / case_count if case_count else 0.0,
        "mean_score": total_score / case_count if case_count else 0.0,
        "max_score": 3,
        "results": results,
    }


def print_text(report: dict[str, Any]) -> None:
    print("AS-018 benchmark")
    print("================")
    print(f"Cases: {report['case_count']}")
    print(f"Responses: {report['response_count']}")
    print(f"Exact passes: {report['exact_pass_count']}/{report['case_count']}")
    print(f"Exact pass rate: {report['exact_pass_rate']:.1%}")
    print(f"Boundary preservation: {report['boundary_preservation_rate']:.1%}")
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
        gold_response = {
            "case_id": case["case_id"],
            "active_boundary": "current_artifact_only",
            "excluded_layers_preserved": True,
            "variable_count": case["gold"]["max_variable_count"],
            "rubric_used": True,
            "next_test_runnable": True,
            "speed_treated_as_boundary_stressor": True,
        }
        passing = score_case(case, gold_response)
        if passing["score"] != 3:
            raise BenchmarkError(f"self-test failed for gold response: {case['case_id']}: {passing}")

        expanded = {**gold_response, "active_boundary": "expanded"}
        failing = score_case(case, expanded)
        if failing["score"] != 0:
            raise BenchmarkError(f"self-test failed for expanded boundary: {case['case_id']}")
    print(f"Self-test passed: {len(cases)} fixtures, gold=3/3, expanded boundary=0/3")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AS-018 JSONL responses deterministically.")
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
