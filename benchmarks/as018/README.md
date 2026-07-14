# AS-018 Benchmark: Speed Boundary Stress Test

Status: runnable benchmark slice.

## What It Tests

Given a visually rich tattoo-design premise under speed pressure, identify whether the assistant preserves:

- the current artifact boundary
- hard exclusions
- one-variable discipline
- pass / half-pass / fail rubric use
- a runnable next test
- speed as a boundary stressor

## What It Does Not Test

It does not test tattoo quality, image generation, stencil quality, anatomy rendering, or final production readiness.

It tests one thing:

```text
speed is not permission to drift
```

## Response Contract

One JSON object per line:

```json
{
  "case_id": "as018_01_helmet_only_fast_pass",
  "active_boundary": "current_artifact_only",
  "excluded_layers_preserved": true,
  "variable_count": 1,
  "rubric_used": true,
  "next_test_runnable": true,
  "speed_treated_as_boundary_stressor": true
}
```

Allowed `active_boundary` values:

```text
current_artifact_only
expanded
unclear
```

## Scoring

Each case scores `0-3`:

- `0`: expands the boundary, reintroduces excluded layers, or changes more than two variables
- `1`: names the boundary but does not enforce it
- `2`: mostly bounded, with one missing support field
- `3`: boundary preserved, exclusions preserved, variable count within limit, rubric used, next test runnable, speed treated as a stressor

## Run Smoke Test

```powershell
python scripts/run_as018_benchmark.py --responses benchmarks/as018/smoke_responses.jsonl
```

The smoke responses are gold-shaped synthetic data. They prove scorer wiring, not model performance.

## Current Baseline

```text
Gemini Flash signed-out, 2026-07-13
12/12 exact
boundary preservation 100%
mean score 3.00/3
```

This is one signed-out batch run. It is not a broad model comparison.

## Score A Model Run

```powershell
python scripts/run_as018_benchmark.py --responses path/to/model-responses.jsonl
```

## Receipt

The source eval remains in:

```text
evals/AS-018-08.07.2026-speed-boundary-stress-test-under-tattoo-design-premise.md
```
