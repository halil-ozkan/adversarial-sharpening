# Adversarial Sharpening

Proof-of-concept corpus for documenting assistant failure modes and converting them into bounded eval cases.

This repo is an evidence-first workbench. It collects observed assistant behavior, turns it into small public-safe artifacts, and adds runnable benchmark slices where the case shape is narrow enough to score.

It is not a finished benchmark suite, a broad model comparison, or a claim that a full AI safety system has been built.

## Current Snapshot

Local checkpoint: 2026-07-14

```text
public files: 108
public size: 588.9 KiB
public lines: 15,131
markdown evals: 10
JSON fixture files: 1
runnable benchmark slices: 9
benchmark cases: 108
model baseline: Gemini Flash signed-out, one run per runnable slice
```

Current validation:

```text
artifact audit: 0 failures, 1 warning
eval structure check: 0 failures
benchmark exact passes: 102/108
overall benchmark exact pass rate: 94.4%
overall mean benchmark score: 2.87/3
```

The remaining audit warning is a stale optional delivery zip. Manual file upload is the active delivery mode, so the zip is not the source of truth.

## What This Is

The repo follows a simple pipeline:

```text
chat/share receipt
bounded case
eval protocol
benchmark fixture when appropriate
scorer
baseline run
audit receipt
```

The strongest signal is not a single claim. It is the repeated conversion of messy assistant interactions into narrow, inspectable test objects with explicit boundaries.

## What This Is Not

This repo does not claim:

- broad model performance
- production-grade benchmark coverage
- clinical, legal, financial, or safety authority
- proof of model intent
- proof of system-wide behavior
- that all cases are runnable benchmarks
- that private source material is included

Some artifacts are human-scored case notes. Some are eval protocols. Nine currently have runnable benchmark slices.

## Provenance Note

This project was backfilled from real assistant interactions. It was not designed from day one as a formal benchmark suite.

Early chronology is reconstructed from available receipts, shared chats, filenames, and later date anchors. In the available shared-chat receipts, chronological metadata was not consistently sufficient for audit work, so dates are stated conservatively.

The earliest currently documented project-start date is 2026-06-08, based on a later shared-chat date receipt.

The local repo workflow accelerated later: on 2026-06-30, the project was not yet being handled as a working local repo; by 2026-07-13, it had been structured, audited, scored, and validated as a proof-of-concept corpus.

## Repository Map

```text
cases/        observed case notes and public-safe incident artifacts
evals/        eval protocols and human-scored eval drafts
benchmarks/   JSONL fixtures, response contracts, scorers, and baseline runs
protocols/    reusable operating protocols
scripts/      local audit and scoring scripts
private/      omitted source context; not for public upload
delivery/     optional/stale packaging output; not source of truth
```

Start with:

```text
REPO_OVERVIEW.md
PROJECT_STATUS.md
ARTIFACT_INDEX.md
ARTIFACT_TIMELINE.md
```

## Runnable Benchmark Slices

Each runnable slice has:

- 12 JSONL cases
- a strict response contract
- a deterministic 0-3 scorer
- synthetic smoke responses
- one Gemini Flash signed-out baseline run

Current baseline table:

| Slice | Focus | Gemini baseline |
|---|---|---:|
| AS-010 humor | humor-embedded factual claim checking | 8/12, mean 2.00/3 |
| AS-011 | mental-hopscotch chain preservation | 11/12, mean 2.92/3 |
| AS-013 | legal-name boundary preservation | 12/12, mean 3.00/3 |
| AS-014 | Switzerland / suicide ambiguity handling | 12/12, mean 3.00/3 |
| AS-015 | handholdy overvalidation avoidance | 12/12, mean 3.00/3 |
| AS-016 | new-GPT protocol handoff response order | 12/12, mean 3.00/3 |
| AS-018 | speed-pressure boundary preservation | 12/12, mean 3.00/3 |
| AS-019 | date accuracy / timeline drift | 11/12, mean 2.92/3 |
| AS-020 | speaker provenance preservation | 12/12, mean 3.00/3 |

These are first baselines, not broad claims about Gemini or any other model.

## Run Checks

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\audit_artifacts.ps1
python scripts/eval_cases.py
```

Run one benchmark scorer:

```powershell
python scripts/run_as010_humor_benchmark.py --self-test
python scripts/run_as010_humor_benchmark.py --responses benchmarks/as010_humor/runs/gemini_flash_signedout_2026-07-13.jsonl
```

Repeat with the other benchmark scorer scripts:

```text
scripts/run_as011_benchmark.py
scripts/run_as013_benchmark.py
scripts/run_as014_benchmark.py
scripts/run_as015_benchmark.py
scripts/run_as016_benchmark.py
scripts/run_as018_benchmark.py
scripts/run_as019_benchmark.py
scripts/run_as020_benchmark.py
```

## Public Boundary

The public repo should include the working artifacts, benchmark fixtures, scorers, and public-safe notes.

The public repo should not include:

- `private/`
- `delivery/`
- `AGENTS.md`
- zip bundles
- local binaries
- raw private chat links
- personal source context that is not already sanitized

## License

This repository is licensed under the Business Source License 1.1.

```text
SPDX-License-Identifier: BUSL-1.1
Change Date: 2030-07-14
Change License: MIT
Additional Use Grant: None
```

This means the repository is source-available, not open-source. Non-production use is allowed under BUSL 1.1. Broader rights become available under the MIT License on the Change Date or the fourth anniversary of first public distribution for a given version, whichever comes first.

## Claim Ceiling

Clean wording:

```text
This is a proof-of-concept corpus for assistant-behavior eval work. It documents recurring failure modes, preserves provenance limits, and provides several runnable benchmark slices with first baseline runs.
```

Do not overstate it as a finished benchmark suite.
