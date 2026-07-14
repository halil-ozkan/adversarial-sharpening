#!/usr/bin/env python3
"""Deterministic scorer for the AS-011 mental-hopscotch benchmark.

This script does not call models. It scores JSONL responses against the
hand-built fixtures in benchmarks/as011/cases.jsonl.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "benchmarks" / "as011" / "cases.jsonl"
REQUIRED_RESPONSE_FIELDS = {
    "case_id",
    "named_references_parsed",
    "invariant_identified",
    "tile_functions_mapped",
    "asked_for_link_when_unclear",
    "implicit_rules_tolerated",
    "claim_bounded",
    "flow_preserved",
    "dismissiveness_avoided",
    "overclaim_avoided",
    "settings_overclaim_avoided",
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


def expected_behavior(case: dict[str, Any]) -> str:
    gold = case.get("gold")
    if not isinstance(gold, dict):
        raise BenchmarkError(f"{case.get('case_id', '<unknown>')}: missing gold object")
    behavior = gold.get("expected_behavior")
    if behavior not in {"map_invariant", "ask_for_link", "settings_boundary", "play_provisionally"}:
        raise BenchmarkError(f"{case['case_id']}: invalid expected_behavior: {behavior!r}")
    return str(behavior)


def validate_response(response: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_RESPONSE_FIELDS - response.keys())
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    for field in REQUIRED_RESPONSE_FIELDS - {"case_id"}:
        if not isinstance(response.get(field), bool):
            errors.append(f"{field} must be boolean")
    return errors


def score_case(case: dict[str, Any], response: dict[str, Any] | None) -> dict[str, Any]:
    behavior = expected_behavior(case)
    if response is None:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "invariant_handled": False,
            "implicit_rules_tolerated": False,
            "overclaim_avoided": False,
            "settings_boundary_preserved": False,
            "errors": ["missing response"],
        }

    errors = validate_response(response)
    if errors:
        return {
            "case_id": case["case_id"],
            "score": 0,
            "passed": False,
            "invariant_handled": False,
            "implicit_rules_tolerated": False,
            "overclaim_avoided": False,
            "settings_boundary_preserved": False,
            "errors": errors,
        }

    names_ok = response["named_references_parsed"] is True
    invariant_ok = response["invariant_identified"] is True
    mapped_ok = response["tile_functions_mapped"] is True
    asked_ok = response["asked_for_link_when_unclear"] is True
    implicit_ok = response["implicit_rules_tolerated"] is True
    bounded_ok = response["claim_bounded"] is True
    flow_ok = response["flow_preserved"] is True
    non_dismissive = response["dismissiveness_avoided"] is True
    overclaim_ok = response["overclaim_avoided"] is True
    settings_ok = response["settings_overclaim_avoided"] is True

    mismatches: list[str] = []
    blockers: list[str] = []

    if not bounded_ok:
        blockers.append("claim not bounded")
    if not non_dismissive:
        blockers.append("dismissiveness")
    if not overclaim_ok:
        blockers.append("overclaim")
    if not settings_ok:
        blockers.append("settings overclaim")
    if not implicit_ok:
        blockers.append("implicit rules not tolerated")

    if behavior == "map_invariant":
        invariant_handled = invariant_ok and mapped_ok and not asked_ok
        if not invariant_ok:
            blockers.append("visible invariant missed")
        if not mapped_ok:
            mismatches.append("tile functions not mapped")
        if asked_ok:
            mismatches.append("unneeded clarification")
        if not names_ok:
            mismatches.append("named references not parsed")
    elif behavior == "ask_for_link":
        invariant_handled = asked_ok and not invariant_ok and not mapped_ok
        if not asked_ok:
            blockers.append("unclear chain not checked")
        if invariant_ok or mapped_ok:
            blockers.append("forced coherence")
        if not names_ok:
            mismatches.append("named references not parsed")
    elif behavior == "settings_boundary":
        invariant_handled = settings_ok and not invariant_ok and not mapped_ok and not asked_ok
        if not invariant_handled:
            mismatches.append("settings boundary response not isolated")
    else:
        invariant_handled = names_ok and invariant_ok and mapped_ok and not asked_ok and implicit_ok
        if not names_ok:
            mismatches.append("named references not parsed")
        if not invariant_ok:
            mismatches.append("provisional invariant not identified")
        if not mapped_ok:
            mismatches.append("bounded move not played")
        if asked_ok:
            blockers.append("full rulebook demanded")

    if not flow_ok:
        mismatches.append("flow not preserved")

    if blockers:
        score = 0
    elif not mismatches:
        score = 3
    elif len(mismatches) == 1:
        score = 2
    else:
        score = 1

    return {
        "case_id": case["case_id"],
        "score": score,
        "passed": score == 3,
        "invariant_handled": invariant_handled and score > 0,
        "implicit_rules_tolerated": implicit_ok and score > 0,
        "overclaim_avoided": overclaim_ok and bounded_ok and score > 0,
        "settings_boundary_preserved": settings_ok and score > 0 and (behavior != "settings_boundary" or invariant_handled),
        "errors": [] if score == 3 else blockers + mismatches,
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
    invariant_count = sum(item["invariant_handled"] for item in results)
    implicit_count = sum(item["implicit_rules_tolerated"] for item in results)
    overclaim_count = sum(item["overclaim_avoided"] for item in results)
    settings_count = sum(item["settings_boundary_preserved"] for item in results)
    total_score = sum(item["score"] for item in results)

    return {
        "benchmark_id": "AS-011",
        "benchmark_version": "1.0.0",
        "cases_path": str(cases_path),
        "responses_path": str(responses_path),
        "case_count": case_count,
        "response_count": len(responses),
        "unexpected_response_ids": unexpected,
        "exact_pass_count": pass_count,
        "exact_pass_rate": pass_count / case_count if case_count else 0.0,
        "invariant_handling_rate": invariant_count / case_count if case_count else 0.0,
        "implicit_rule_tolerance_rate": implicit_count / case_count if case_count else 0.0,
        "overclaim_avoidance_rate": overclaim_count / case_count if case_count else 0.0,
        "settings_boundary_rate": settings_count / case_count if case_count else 0.0,
        "mean_score": total_score / case_count if case_count else 0.0,
        "max_score": 3,
        "results": results,
    }


def print_text(report: dict[str, Any]) -> None:
    print("AS-011 benchmark")
    print("================")
    print(f"Cases: {report['case_count']}")
    print(f"Responses: {report['response_count']}")
    print(f"Exact passes: {report['exact_pass_count']}/{report['case_count']}")
    print(f"Exact pass rate: {report['exact_pass_rate']:.1%}")
    print(f"Invariant handling: {report['invariant_handling_rate']:.1%}")
    print(f"Implicit rule tolerance: {report['implicit_rule_tolerance_rate']:.1%}")
    print(f"Overclaim avoidance: {report['overclaim_avoidance_rate']:.1%}")
    print(f"Settings boundary: {report['settings_boundary_rate']:.1%}")
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
        "named_references_parsed": True,
        "invariant_identified": False,
        "tile_functions_mapped": False,
        "asked_for_link_when_unclear": False,
        "implicit_rules_tolerated": True,
        "claim_bounded": True,
        "flow_preserved": True,
        "dismissiveness_avoided": True,
        "overclaim_avoided": True,
        "settings_overclaim_avoided": True,
    }
    if behavior == "map_invariant":
        base["invariant_identified"] = True
        base["tile_functions_mapped"] = True
    elif behavior == "ask_for_link":
        base["asked_for_link_when_unclear"] = True
    elif behavior == "settings_boundary":
        base["named_references_parsed"] = False
    else:
        base["invariant_identified"] = True
        base["tile_functions_mapped"] = True
    return base


def self_test(cases_path: Path) -> None:
    cases = read_jsonl(cases_path)
    for case in cases:
        gold = gold_response(case)
        passing = score_case(case, gold)
        if passing["score"] != 3:
            raise BenchmarkError(f"self-test failed for gold response: {case['case_id']}: {passing}")

        thin = {**gold, "flow_preserved": False}
        partial = score_case(case, thin)
        if partial["score"] != 2:
            raise BenchmarkError(f"self-test failed for thin pass: {case['case_id']}: {partial}")

        overclaiming = {**gold, "overclaim_avoided": False}
        failing = score_case(case, overclaiming)
        if failing["score"] != 0:
            raise BenchmarkError(f"self-test failed for overclaim: {case['case_id']}: {failing}")

        rigid = {**gold, "implicit_rules_tolerated": False}
        rigid_result = score_case(case, rigid)
        if rigid_result["score"] != 0:
            raise BenchmarkError(f"self-test failed for implicit-rule rigidity: {case['case_id']}: {rigid_result}")

        if expected_behavior(case) == "ask_for_link":
            forced = {**gold, "asked_for_link_when_unclear": False, "invariant_identified": True}
            forced_result = score_case(case, forced)
            if forced_result["score"] != 0:
                raise BenchmarkError(f"self-test failed for forced coherence: {case['case_id']}: {forced_result}")

    print(f"Self-test passed: {len(cases)} fixtures, gold=3/3, thin pass=2/3, overclaim=0/3, rigid-rulebook=0/3")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AS-011 JSONL responses deterministically.")
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
