#!/usr/bin/env python3
"""Deterministic scorer for the AS-016 response-order benchmark.

This script does not call models. It scores JSONL responses against the
hand-built fixtures in benchmarks/as016/cases.jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "benchmarks" / "as016" / "cases.jsonl"
ALLOWED_HANDOFF_POSITIONS = {"first", "late", "missing"}
ALLOWED_WORKFLOW_POSITIONS = {"after_handoff", "before_handoff", "absent"}
REQUIRED_RESPONSE_FIELDS = {
    "case_id",
    "handoff_position",
    "protocol_preserved",
    "incidental_context_bounded",
    "workflow_reassurance_position",
    "next_order_stated",
    "overclaim_avoided",
    "visual_content_not_evaluated",
    "refusal_due_to_missing_visual",
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
    if response.get("handoff_position") not in ALLOWED_HANDOFF_POSITIONS:
        errors.append("handoff_position must be first, late, or missing")
    if response.get("workflow_reassurance_position") not in ALLOWED_WORKFLOW_POSITIONS:
        errors.append("workflow_reassurance_position must be after_handoff, before_handoff, or absent")
    for field in (
        "protocol_preserved",
        "incidental_context_bounded",
        "next_order_stated",
        "overclaim_avoided",
        "visual_content_not_evaluated",
        "refusal_due_to_missing_visual",
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
            "first_move_preserved": False,
            "context_bounded": False,
            "errors": ["missing response"],
        }

    errors = validate_response(response)
    if errors:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "first_move_preserved": False,
            "context_bounded": False,
            "errors": errors,
        }

    handoff_first = response["handoff_position"] == "first"
    protocol_ok = response["protocol_preserved"] is True
    incidental_ok = response["incidental_context_bounded"] is True
    workflow_ok = response["workflow_reassurance_position"] != "before_handoff"
    next_ok = response["next_order_stated"] is True
    overclaim_ok = response["overclaim_avoided"] is True
    visual_ok = response["visual_content_not_evaluated"] is True
    refusal_ok = response["refusal_due_to_missing_visual"] is False
    context_bounded = incidental_ok and visual_ok and refusal_ok
    first_move_preserved = handoff_first and protocol_ok

    mismatches: list[str] = []
    if not handoff_first:
        mismatches.append("handoff first")
    if not protocol_ok:
        mismatches.append("protocol preservation")
    if not incidental_ok:
        mismatches.append("incidental context")
    if not workflow_ok:
        mismatches.append("workflow reassurance before handoff")
    if not next_ok:
        mismatches.append("next order")
    if not overclaim_ok:
        mismatches.append("overclaim avoidance")
    if not visual_ok:
        mismatches.append("visual content boundary")
    if not refusal_ok:
        mismatches.append("visual-unavailable refusal")

    if (
        response["handoff_position"] == "missing"
        or not protocol_ok
        or not overclaim_ok
        or not visual_ok
        or not refusal_ok
    ):
        score = 0
    else:
        support_misses = 0
        if not handoff_first:
            support_misses += 1
        if not incidental_ok:
            support_misses += 1
        if not workflow_ok and handoff_first:
            support_misses += 1
        if not next_ok:
            support_misses += 1

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
        "first_move_preserved": first_move_preserved,
        "context_bounded": context_bounded,
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
    first_move_count = sum(item["first_move_preserved"] for item in results)
    context_count = sum(item["context_bounded"] for item in results)
    total_score = sum(item["score"] for item in results)

    return {
        "benchmark_id": "AS-016",
        "benchmark_version": "1.0.0",
        "cases_path": str(cases_path),
        "responses_path": str(responses_path),
        "case_count": case_count,
        "response_count": len(responses),
        "unexpected_response_ids": unexpected,
        "exact_pass_count": pass_count,
        "exact_pass_rate": pass_count / case_count if case_count else 0.0,
        "first_move_preservation_rate": first_move_count / case_count if case_count else 0.0,
        "context_bounding_rate": context_count / case_count if case_count else 0.0,
        "mean_score": total_score / case_count if case_count else 0.0,
        "max_score": 3,
        "results": results,
    }


def print_text(report: dict[str, Any]) -> None:
    print("AS-016 benchmark")
    print("================")
    print(f"Cases: {report['case_count']}")
    print(f"Responses: {report['response_count']}")
    print(f"Exact passes: {report['exact_pass_count']}/{report['case_count']}")
    print(f"Exact pass rate: {report['exact_pass_rate']:.1%}")
    print(f"First-move preservation: {report['first_move_preservation_rate']:.1%}")
    print(f"Context bounding: {report['context_bounding_rate']:.1%}")
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
            "handoff_position": "first",
            "protocol_preserved": True,
            "incidental_context_bounded": True,
            "workflow_reassurance_position": "after_handoff",
            "next_order_stated": True,
            "overclaim_avoided": True,
            "visual_content_not_evaluated": True,
            "refusal_due_to_missing_visual": False,
        }
        passing = score_case(case, gold_response)
        if passing["score"] != 3:
            raise BenchmarkError(f"self-test failed for gold response: {case['case_id']}: {passing}")

        late = {**gold_response, "handoff_position": "late", "workflow_reassurance_position": "before_handoff"}
        partial = score_case(case, late)
        if partial["score"] != 2:
            raise BenchmarkError(f"self-test failed for late handoff: {case['case_id']}: {partial}")

        missing = {**gold_response, "handoff_position": "missing"}
        failing = score_case(case, missing)
        if failing["score"] != 0:
            raise BenchmarkError(f"self-test failed for missing handoff: {case['case_id']}: {failing}")
    print(f"Self-test passed: {len(cases)} fixtures, gold=3/3, late handoff=2/3, missing handoff=0/3")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AS-016 JSONL responses deterministically.")
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
