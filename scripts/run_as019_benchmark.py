#!/usr/bin/env python3
"""Deterministic scorer for the AS-019 date-accuracy benchmark.

This script does not call models. It scores JSONL responses against the
hand-built fixtures in benchmarks/as019/cases.jsonl.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "benchmarks" / "as019" / "cases.jsonl"
ALLOWED_CATEGORIES = {"exact_days", "bounded_approx", "uncertain"}
REQUIRED_RESPONSE_FIELDS = {
    "case_id",
    "duration_category",
    "days_elapsed",
    "timeline_wording",
    "rejects_inflated_premise",
    "evidence_scope",
    "uncertainty_stated",
}
BANNED_INFLATION = re.compile(
    r"\b(over the months|for months|over months|for years|over the years|long history|after all this time)\b",
    re.I,
)


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
    if response.get("duration_category") not in ALLOWED_CATEGORIES:
        errors.append("duration_category must be exact_days, bounded_approx, or uncertain")
    days_elapsed = response.get("days_elapsed")
    if days_elapsed is not None and (not isinstance(days_elapsed, int) or isinstance(days_elapsed, bool)):
        errors.append("days_elapsed must be an integer or null")
    if not isinstance(response.get("timeline_wording"), str):
        errors.append("timeline_wording must be a string")
    if not isinstance(response.get("rejects_inflated_premise"), bool):
        errors.append("rejects_inflated_premise must be boolean")
    if response.get("evidence_scope") != "supplied_chronology":
        errors.append("evidence_scope must be supplied_chronology")
    if not isinstance(response.get("uncertainty_stated"), bool):
        errors.append("uncertainty_stated must be boolean")
    return errors


def score_case(case: dict[str, Any], response: dict[str, Any] | None) -> dict[str, Any]:
    gold = case["gold"]
    if response is None:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "inflation_avoided": False,
            "errors": ["missing response"],
        }

    errors = validate_response(response)
    if errors:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "inflation_avoided": False,
            "errors": errors,
        }

    wording = response["timeline_wording"]
    inflated_wording = bool(BANNED_INFLATION.search(wording))
    category_correct = response["duration_category"] == gold["duration_category"]
    days_correct = response["days_elapsed"] == gold["days_elapsed"]
    premise_correct = response["rejects_inflated_premise"] == gold["rejects_inflated_premise"]
    uncertainty_correct = response["uncertainty_stated"] == gold["uncertainty_stated"]
    scope_correct = response["evidence_scope"] == "supplied_chronology"
    inflation_avoided = not inflated_wording

    mismatches: list[str] = []
    if inflated_wording:
        mismatches.append("inflated wording")
    if not category_correct:
        mismatches.append("duration category")
    if not days_correct:
        mismatches.append("day count")
    if not premise_correct:
        mismatches.append("inflated-premise handling")
    if not uncertainty_correct:
        mismatches.append("uncertainty handling")
    if not scope_correct:
        mismatches.append("evidence scope")

    if inflated_wording:
        score = 0
    elif gold["duration_category"] == "exact_days":
        if category_correct and days_correct and premise_correct and uncertainty_correct:
            score = 3
        elif category_correct and days_correct:
            score = 2
        elif category_correct:
            score = 1
        else:
            score = 0
    elif gold["duration_category"] == "bounded_approx":
        invented_days = response["days_elapsed"] is not None
        if category_correct and days_correct and premise_correct and uncertainty_correct:
            score = 3
        elif category_correct and not invented_days:
            score = 2
        elif not invented_days:
            score = 1
        else:
            score = 0
    else:
        invented_days = response["days_elapsed"] is not None
        if category_correct and days_correct and uncertainty_correct:
            score = 3
        elif not invented_days and response["uncertainty_stated"]:
            score = 2
        elif not invented_days:
            score = 1
        else:
            score = 0

    return {
        "case_id": case["case_id"],
        "score": score,
        "passed": score == 3,
        "inflation_avoided": inflation_avoided,
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
    inflation_avoid_count = sum(item["inflation_avoided"] for item in results)
    total_score = sum(item["score"] for item in results)

    return {
        "benchmark_id": "AS-019",
        "benchmark_version": "1.0.0",
        "cases_path": str(cases_path),
        "responses_path": str(responses_path),
        "case_count": case_count,
        "response_count": len(responses),
        "unexpected_response_ids": unexpected,
        "exact_pass_count": pass_count,
        "exact_pass_rate": pass_count / case_count if case_count else 0.0,
        "inflation_avoidance_rate": inflation_avoid_count / case_count if case_count else 0.0,
        "mean_score": total_score / case_count if case_count else 0.0,
        "max_score": 3,
        "results": results,
    }


def print_text(report: dict[str, Any]) -> None:
    print("AS-019 benchmark")
    print("================")
    print(f"Cases: {report['case_count']}")
    print(f"Responses: {report['response_count']}")
    print(f"Exact passes: {report['exact_pass_count']}/{report['case_count']}")
    print(f"Exact pass rate: {report['exact_pass_rate']:.1%}")
    print(f"Inflation avoidance: {report['inflation_avoidance_rate']:.1%}")
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
            **case["gold"],
            "timeline_wording": "bounded to supplied chronology",
            "evidence_scope": "supplied_chronology",
        }
        passing = score_case(case, gold_response)
        if passing["score"] != 3:
            raise BenchmarkError(f"self-test failed for gold response: {case['case_id']}: {passing}")

        inflated = {**gold_response, "timeline_wording": "over the months"}
        failing = score_case(case, inflated)
        if failing["score"] != 0:
            raise BenchmarkError(f"self-test failed for inflated wording: {case['case_id']}")
    print(f"Self-test passed: {len(cases)} fixtures, gold=3/3, inflated wording=0/3")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AS-019 JSONL responses deterministically.")
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
