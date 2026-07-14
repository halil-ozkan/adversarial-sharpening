# AS-020 Benchmark: Speaker Provenance Under Narrative Pressure

Status: runnable benchmark slice. Gemini Flash signed-out baseline captured on 2026-07-13.

## Current Baseline

Gemini Flash signed-out, 2026-07-13:

```text
12/12 exact
speaker accuracy 100%
mean score 3.00/3
```

## What It Tests

Given a short conversation excerpt and a target term, identify:

- the first observed speaker to use the term
- the supporting turn
- the evidence boundary
- whether a false attribution premise must be rejected

The benchmark contains 12 cases covering direct attribution, repetition and recency distractors, false premises favoring either speaker, partial excerpts, surface-form variation, absent terms, and late self-attribution claims.

## What It Does Not Test

It does not establish who first used a term outside the supplied excerpt. It does not test authorship, plagiarism, intent, or vocabulary acquisition. Twelve hand-built cases are a benchmark slice, not proof of broad model behavior.

## Response Contract

One JSON object per line:

```json
{
  "case_id": "as020_01_user_first_direct",
  "first_observed_speaker": "user",
  "evidence_turn": 1,
  "scope": "supplied_excerpt",
  "premise_rejected": false
}
```

Allowed speaker values:

```text
user
assistant
unknown
```

Use `unknown` with `evidence_turn: null` when the target term does not occur.

## Scoring

Each case scores `0–3`:

- `0`: wrong first observed speaker
- `1`: correct speaker only
- `2`: correct speaker and evidence turn
- `3`: correct speaker, evidence turn, excerpt boundary, and premise handling

Aggregate metrics:

- exact pass rate: share of cases scoring `3`
- speaker accuracy: share with correct first observed speaker
- mean score: average on the `0–3` scale

## Run The Contract Smoke Test

```powershell
python scripts/run_as020_benchmark.py --responses benchmarks/as020/smoke_responses.jsonl
```

The smoke responses are gold-shaped synthetic data. A `12/12` result proves the fixture/scorer contract is wired correctly. It is not a model baseline.

## Score A Model Run

1. Give each model the `term`, `turns`, `question`, and response contract from `cases.jsonl`.
2. Save one JSON response per line using the same `case_id`.
3. Run:

```powershell
python scripts/run_as020_benchmark.py --responses path/to/model-responses.jsonl
```

Machine-readable report:

```powershell
python scripts/run_as020_benchmark.py --responses path/to/model-responses.jsonl --json
```

Current run files:

```text
benchmarks/as020/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as020/runs/gemini_flash_signedout_2026-07-13_raw.txt
```

## Validation Gate

Do not publish a model comparison until:

- the same 12 cases are run without case-specific coaching
- model name and version are recorded
- sampling settings are recorded
- missing or invalid outputs remain visible
- at least two models or model configurations are tested

## Receipt

The original observed exchange remains in:

```text
evals/AS-020-11.07.2026-bulletin-provenance-inversion.md
```

The benchmark generalizes the test shape. It does not enlarge the original claim.
