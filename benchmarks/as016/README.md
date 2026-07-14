# AS-016 Benchmark: New GPT Protocol Handoff Response Order

Status: runnable benchmark slice.

## What It Tests

Given a fresh-context handoff after a protocol seed, identify whether the assistant preserves:

- the protocol handoff as the first move
- the active protocol by name or rule
- incidental context as incidental
- workflow reassurance only after the handoff
- a concise next-step order
- no permanent-memory or visual-content overclaim

## What It Does Not Test

It does not test image interpretation, visual content, permanent memory, or whether a protocol is installed forever.

It tests one thing:

```text
handoff first, reassurance second
```

## Response Contract

One JSON object per line:

```json
{
  "case_id": "as016_01_no_upload_direct_continue",
  "handoff_position": "first",
  "protocol_preserved": true,
  "incidental_context_bounded": true,
  "workflow_reassurance_position": "absent",
  "next_order_stated": true,
  "overclaim_avoided": true,
  "visual_content_not_evaluated": true,
  "refusal_due_to_missing_visual": false
}
```

Allowed `handoff_position` values:

```text
first
late
missing
```

Allowed `workflow_reassurance_position` values:

```text
after_handoff
before_handoff
absent
```

## Scoring

Each case scores `0-3`:

- `0`: drops the protocol, misses the handoff, centralizes visual content, refuses because images are unavailable, or overclaims permanent memory
- `1`: preserves the protocol weakly but misses multiple support fields
- `2`: preserves the protocol but the handoff is late, the next order is missing, or context handling is incomplete
- `3`: handoff first, protocol preserved, context bounded, reassurance not first, next order stated, no overclaim

## Run Smoke Test

```powershell
python scripts/run_as016_benchmark.py --responses benchmarks/as016/smoke_responses.jsonl
```

The smoke responses are gold-shaped synthetic data. They prove scorer wiring, not model performance.

## Current Baseline

```text
Gemini Flash signed-out, 2026-07-13
12/12 exact
first-move preservation 100%
context bounding 100%
mean score 3.00/3
```

This is one signed-out batch run. It is not a broad model comparison.

## Score A Model Run

```powershell
python scripts/run_as016_benchmark.py --responses path/to/model-responses.jsonl
```

## Receipt

The source eval remains in:

```text
evals/AS-016-07.07.2026-new-gpt-protocol-handoff-response-order.md
```
