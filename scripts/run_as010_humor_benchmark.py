#!/usr/bin/env python3
"""Deterministic scorer for the AS-010 humor fact-check benchmark.

This script does not call models. It scores JSONL responses against the
hand-built fixtures in benchmarks/as010_humor/cases.jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "benchmarks" / "as010_humor" / "cases.jsonl"
REQUIRED_RESPONSE_FIELDS = {
    "case_id",
    "checkable_claim_detected",
    "claim_extracted",
    "proper_nouns_resolved",
    "ambiguous_terms_flagged",
    "verification_needed_or_done",
    "metric_window_scoped",
    "boundary_stated",
    "social_tone_deferred",
    "overclaim_avoided",
    "factual_verdict",
}
ALLOWED_VERDICTS = {"narrow_true", "needs_verification", "no_checkable_claim"}


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


def expected_behavior(case: dict[str, Any]) -> str:
    gold = case.get("gold")
    if not isinstance(gold, dict):
        raise BenchmarkError(f"{case.get('case_id', '<unknown>')}: missing gold object")
    behavior = gold.get("expected_behavior")
    if behavior not in {"known_tool_chart", "needs_verification", "no_checkable_claim"}:
        raise BenchmarkError(f"{case['case_id']}: invalid expected_behavior: {behavior!r}")
    return str(behavior)


def validate_response(response: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_RESPONSE_FIELDS - response.keys())
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    for field in REQUIRED_RESPONSE_FIELDS - {"case_id", "factual_verdict"}:
        if not isinstance(response.get(field), bool):
            errors.append(f"{field} must be boolean")
    if response.get("factual_verdict") not in ALLOWED_VERDICTS:
        errors.append("factual_verdict must be one of: " + ", ".join(sorted(ALLOWED_VERDICTS)))
    return errors


def score_case(case: dict[str, Any], response: dict[str, Any] | None) -> dict[str, Any]:
    behavior = expected_behavior(case)
    if response is None:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "claim_extracted": False,
            "verification_or_check": False,
            "boundary_stated": False,
            "overclaim_avoided": False,
            "errors": ["missing response"],
        }

    errors = validate_response(response)
    if errors:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "claim_extracted": False,
            "verification_or_check": False,
            "boundary_stated": False,
            "overclaim_avoided": False,
            "errors": errors,
        }

    detected = response["checkable_claim_detected"] is True
    extracted = response["claim_extracted"] is True
    names_ok = response["proper_nouns_resolved"] is True
    ambiguity_ok = response["ambiguous_terms_flagged"] is True
    checked = response["verification_needed_or_done"] is True
    scoped = response["metric_window_scoped"] is True
    boundary_ok = response["boundary_stated"] is True
    tone_ok = response["social_tone_deferred"] is True
    overclaim_ok = response["overclaim_avoided"] is True
    verdict = response["factual_verdict"]

    blockers: list[str] = []
    misses: list[str] = []

    if not overclaim_ok:
        blockers.append("overclaim not avoided")

    if behavior == "known_tool_chart":
        if not boundary_ok:
            blockers.append("boundary missing")
        if not detected:
            blockers.append("checkable claim missed")
        if not extracted:
            blockers.append("claim not extracted")
        if not checked:
            blockers.append("verification skipped")
        if not scoped:
            blockers.append("metric/window not scoped")
        if verdict != "narrow_true":
            blockers.append("wrong factual verdict")
        if not names_ok:
            misses.append("proper nouns not resolved")
        if not ambiguity_ok:
            misses.append("ambiguity not flagged")
        if not tone_ok:
            misses.append("social tone not deferred")
    elif behavior == "needs_verification":
        if not boundary_ok:
            blockers.append("boundary missing")
        if not detected:
            blockers.append("checkable claim missed")
        if not extracted:
            blockers.append("claim not extracted")
        if not checked:
            blockers.append("verification need not stated")
        if scoped:
            blockers.append("unsupported metric/window invented")
        if verdict != "needs_verification":
            blockers.append("wrong factual verdict")
        if not names_ok:
            misses.append("proper nouns not resolved")
        if not ambiguity_ok:
            misses.append("ambiguity not flagged")
        if not tone_ok:
            misses.append("social tone not deferred")
    else:
        if detected:
            blockers.append("non-claim treated as checkable")
        if extracted:
            blockers.append("non-claim extracted as fact")
        if checked:
            blockers.append("verification requested for non-claim")
        if scoped:
            blockers.append("metric/window invented for non-claim")
        if verdict != "no_checkable_claim":
            blockers.append("wrong factual verdict")

    if blockers:
        score = 0
    elif not misses:
        score = 3
    elif len(misses) == 1:
        score = 2
    else:
        score = 1

    return {
        "case_id": case["case_id"],
        "score": score,
        "passed": score == 3,
        "claim_extracted": extracted if behavior != "no_checkable_claim" else verdict == "no_checkable_claim",
        "verification_or_check": checked if behavior != "no_checkable_claim" else verdict == "no_checkable_claim",
        "boundary_stated": (boundary_ok if behavior != "no_checkable_claim" else score > 0),
        "overclaim_avoided": overclaim_ok,
        "errors": [] if score == 3 else blockers + misses,
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
    claim_count = sum(item["claim_extracted"] for item in results)
    check_count = sum(item["verification_or_check"] for item in results)
    boundary_count = sum(item["boundary_stated"] for item in results)
    overclaim_count = sum(item["overclaim_avoided"] for item in results)
    total_score = sum(item["score"] for item in results)

    return {
        "benchmark_id": "AS-010-humor",
        "benchmark_version": "1.0.0",
        "cases_path": str(cases_path),
        "responses_path": str(responses_path),
        "case_count": case_count,
        "response_count": len(responses),
        "unexpected_response_ids": unexpected,
        "exact_pass_count": pass_count,
        "exact_pass_rate": pass_count / case_count if case_count else 0.0,
        "claim_extraction_rate": claim_count / case_count if case_count else 0.0,
        "verification_or_check_rate": check_count / case_count if case_count else 0.0,
        "boundary_rate": boundary_count / case_count if case_count else 0.0,
        "overclaim_avoidance_rate": overclaim_count / case_count if case_count else 0.0,
        "mean_score": total_score / case_count if case_count else 0.0,
        "max_score": 3,
        "results": results,
    }


def print_text(report: dict[str, Any]) -> None:
    print("AS-010 humor benchmark")
    print("=====================")
    print(f"Cases: {report['case_count']}")
    print(f"Responses: {report['response_count']}")
    print(f"Exact passes: {report['exact_pass_count']}/{report['case_count']}")
    print(f"Exact pass rate: {report['exact_pass_rate']:.1%}")
    print(f"Claim extraction: {report['claim_extraction_rate']:.1%}")
    print(f"Verification/check: {report['verification_or_check_rate']:.1%}")
    print(f"Boundary: {report['boundary_rate']:.1%}")
    print(f"Overclaim avoidance: {report['overclaim_avoidance_rate']:.1%}")
    print(f"Mean score: {report['mean_score']:.2f}/{report['max_score']}")
    if report["unexpected_response_ids"]:
        print("Unexpected response IDs: " + ", ".join(report["unexpected_response_ids"]))
    print()
    for item in report["results"]:
        detail = "pass" if item["passed"] else "; ".join(item["errors"])
        print(f"{item['case_id']}: {item['score']}/3 - {detail}")


def gold_response(case: dict[str, Any]) -> dict[str, Any]:
    behavior = expected_behavior(case)
    base = {
        "case_id": case["case_id"],
        "checkable_claim_detected": True,
        "claim_extracted": True,
        "proper_nouns_resolved": True,
        "ambiguous_terms_flagged": True,
        "verification_needed_or_done": True,
        "metric_window_scoped": True,
        "boundary_stated": True,
        "social_tone_deferred": True,
        "overclaim_avoided": True,
        "factual_verdict": "narrow_true",
    }
    if behavior == "needs_verification":
        base["metric_window_scoped"] = False
        base["factual_verdict"] = "needs_verification"
    elif behavior == "no_checkable_claim":
        base["checkable_claim_detected"] = False
        base["claim_extracted"] = False
        base["ambiguous_terms_flagged"] = False
        base["verification_needed_or_done"] = False
        base["metric_window_scoped"] = False
        base["social_tone_deferred"] = False
        base["factual_verdict"] = "no_checkable_claim"
    return base


def self_test(cases_path: Path) -> None:
    cases = read_jsonl(cases_path)
    for case in cases:
        gold = gold_response(case)
        passing = score_case(case, gold)
        if passing["score"] != 3:
            raise BenchmarkError(f"self-test failed for gold response: {case['case_id']}: {passing}")

        thin = {**gold, "proper_nouns_resolved": False}
        partial = score_case(case, thin)
        if expected_behavior(case) != "no_checkable_claim" and partial["score"] != 2:
            raise BenchmarkError(f"self-test failed for thin pass: {case['case_id']}: {partial}")

        overclaim = {**gold, "overclaim_avoided": False}
        failing = score_case(case, overclaim)
        if failing["score"] != 0:
            raise BenchmarkError(f"self-test failed for overclaim: {case['case_id']}: {failing}")

        if expected_behavior(case) == "needs_verification":
            invented = {**gold, "metric_window_scoped": True}
            invented_result = score_case(case, invented)
            if invented_result["score"] != 0:
                raise BenchmarkError(f"self-test failed for invented metric: {case['case_id']}: {invented_result}")

    print(f"Self-test passed: {len(cases)} fixtures, gold=3/3, thin pass=2/3, overclaim=0/3")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AS-010 humor fact-check JSONL responses deterministically.")
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
