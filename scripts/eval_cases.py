#!/usr/bin/env python3
"""Structural inventory for markdown eval cases.

This script does not run model calls and does not score model outputs.
It checks whether the eval drafts expose the pieces a human evaluator needs:
trigger/repro, expected behavior, failure behavior, and scoring.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "evals"

SECTION_PATTERNS = {
    "trigger_or_repro": re.compile(r"^(Trigger|Trigger Conditions|Minimal Repro|Minimum Reproducible Prompt)", re.I),
    "expected_or_target": re.compile(r"^(Expected Behavior|Passing Behavior|Correct Behavior|Target Response|Required Assistant Moves)", re.I),
    "failure_behavior": re.compile(r"^(Failing Behavior|Failure Signatures|Core Failure)", re.I),
    "scoring": re.compile(r"^Scoring", re.I),
    "boundary": re.compile(r"^(Boundary|Boundary Cases|Public-Safe Version|Current Limitation|What This Does Not Prove)", re.I),
    "source_or_privacy": re.compile(r"^(Source Context|Source Notes|Public-Safe Version)", re.I),
}

REQUIRED = ("trigger_or_repro", "expected_or_target", "failure_behavior", "scoring")


def markdown_files() -> list[Path]:
    return sorted(EVAL_DIR.glob("*.md"))


def json_files() -> list[Path]:
    return sorted(EVAL_DIR.glob("*.json"))


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.*\S)\s*$", line)
        if match:
            headings.append(match.group(1))
    return headings


def check_markdown(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    headings = extract_headings(text)
    title = headings[0] if headings else "(missing title)"
    section_hits = {name: False for name in SECTION_PATTERNS}

    for heading in headings:
        clean = heading.strip("# ")
        for name, pattern in SECTION_PATTERNS.items():
            if pattern.search(clean):
                section_hits[name] = True

    missing_required = [name for name in REQUIRED if not section_hits[name]]
    advisory_missing = [name for name in ("boundary", "source_or_privacy") if not section_hits[name]]

    return {
        "path": path.relative_to(ROOT).as_posix(),
        "title": title,
        "lines": len(text.splitlines()),
        "bytes": path.stat().st_size,
        "required_present": {name: section_hits[name] for name in REQUIRED},
        "missing_required": missing_required,
        "advisory_present": {
            "boundary": section_hits["boundary"],
            "source_or_privacy": section_hits["source_or_privacy"],
        },
        "advisory_missing": advisory_missing,
        "status": "pass" if not missing_required else "fail",
    }


def check_json(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        ok = isinstance(data, (dict, list))
        error = None
    except json.JSONDecodeError as exc:
        ok = False
        error = f"line {exc.lineno}: {exc.msg}"

    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "valid_json": ok,
        "error": error,
        "status": "pass" if ok else "fail",
    }


def build_report() -> dict[str, object]:
    markdown = [check_markdown(path) for path in markdown_files()]
    fixtures = [check_json(path) for path in json_files()]
    failures = [item for item in markdown if item["status"] != "pass"]
    failures.extend(item for item in fixtures if item["status"] != "pass")

    return {
        "root": str(ROOT),
        "markdown_eval_count": len(markdown),
        "json_fixture_count": len(fixtures),
        "failures": len(failures),
        "markdown_evals": markdown,
        "json_fixtures": fixtures,
    }


def print_text(report: dict[str, object]) -> None:
    print("Eval case structural check")
    print("==========================")
    print(f"Root: {report['root']}")
    print(f"Markdown evals: {report['markdown_eval_count']}")
    print(f"JSON fixtures: {report['json_fixture_count']}")
    print(f"Failures: {report['failures']}")
    print()

    print("Markdown evals")
    print("--------------")
    for item in report["markdown_evals"]:
        status = item["status"]
        advisory = ", ".join(item["advisory_missing"]) or "none"
        missing = ", ".join(item["missing_required"]) or "none"
        print(f"{status}: {item['path']}")
        print(f"  title: {item['title']}")
        print(f"  lines: {item['lines']}; bytes: {item['bytes']}")
        print(f"  missing required: {missing}")
        print(f"  advisory missing: {advisory}")

    if report["json_fixtures"]:
        print("JSON fixtures")
        print("-------------")
        for item in report["json_fixtures"]:
            detail = "valid" if item["valid_json"] else item["error"]
            print(f"{item['status']}: {item['path']} ({detail})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check eval draft structure without running model calls.")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_text(report)

    return 0 if report["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())