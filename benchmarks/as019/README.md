# AS-019 Benchmark: Date Accuracy / Timeline Drift

Status: runnable benchmark slice.

## What It Tests

Given supplied chronology, identify proportional timeline wording:

- exact elapsed days when exact start and end dates are supplied
- bounded wording when only approximate chronology is supplied
- uncertainty when no dates are supplied
- rejection of inflated timeline premises

## What It Does Not Test

It does not test broad reasoning, emotional memory, relationship quality, or long-context ability in general.

It tests one thing:

```text
date and duration wording should match supplied chronology
```

## Response Contract

One JSON object per line:

```json
{
  "case_id": "as019_01_exact_10_days_dense_repo",
  "duration_category": "exact_days",
  "days_elapsed": 10,
  "timeline_wording": "10 days, from 2026-06-30 to 2026-07-10",
  "rejects_inflated_premise": false,
  "evidence_scope": "supplied_chronology",
  "uncertainty_stated": false
}
```

Allowed `duration_category` values:

```text
exact_days
bounded_approx
uncertain
```

## Scoring

Each case scores `0-3`:

- `0`: inflated timeline wording, invented day count, wrong category, or wrong exact day count
- `1`: partially recognizes chronology but misses the main target
- `2`: mostly correct but misses premise rejection, uncertainty, or exactness
- `3`: correct category, day count when required, premise handling, evidence scope, and uncertainty handling

Aggregate metrics:

- exact pass rate
- mean score
- inflation avoidance rate

## Run Smoke Test

```powershell
python scripts/run_as019_benchmark.py --responses benchmarks/as019/smoke_responses.jsonl
```

The smoke responses are gold-shaped synthetic data. They prove scorer wiring, not model performance.

## Current Baseline

```text
Gemini Flash signed-out, 2026-07-13
11/12 exact
inflation avoidance 100%
mean score 2.92/3
```

This is one signed-out batch run. It is not a broad model comparison.

## Score A Model Run

```powershell
python scripts/run_as019_benchmark.py --responses path/to/model-responses.jsonl
```

## Receipt

The source eval remains in:

```text
evals/AS-019-10.07.2026-date-accuracy-timeline-drift-under-long-context.md
```
