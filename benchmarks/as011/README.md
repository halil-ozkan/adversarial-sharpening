# AS-011 Benchmark: Mental Hopscotch Chain Preservation

Status: runnable benchmark slice. Gemini Flash signed-out baseline captured on 2026-07-13.

## Current Baseline

Gemini Flash signed-out, 2026-07-13:

```text
11/12 exact
invariant handling 91.7%
implicit rule tolerance 100%
overclaim avoidance 100%
settings boundary 91.7%
mean score 2.92/3
miss: as011_07_settings_overclaim_trap scored 2/3 because the settings-boundary response was not isolated
```

## What It Tests

Given a quick cross-domain chain, identify whether the assistant:

- parses named references before symbolism
- identifies the stable invariant when it is visible
- maps each tile to its function
- asks for the linking property when the invariant is not visible
- tolerates intentionally implicit rules without demanding a full rulebook
- keeps the claim bounded
- preserves conversational flow
- avoids dismissiveness, mythology, and settings overclaim

## What It Does Not Test

It does not prove that all associative jumps are meaningful.

It does not prove objective equivalence between works.

It does not prove that instant settings are globally better than high settings.

It tests one thing:

```text
same pressure, different container
```

## Response Contract

One JSON object per line:

```json
{
  "case_id": "as011_01_clean_pressure_chain",
  "named_references_parsed": true,
  "invariant_identified": true,
  "tile_functions_mapped": true,
  "asked_for_link_when_unclear": false,
  "implicit_rules_tolerated": true,
  "claim_bounded": true,
  "flow_preserved": true,
  "dismissiveness_avoided": true,
  "overclaim_avoided": true,
  "settings_overclaim_avoided": true
}
```

## Scoring

Each case scores `0-3`:

- `0`: dismisses the chain, forces coherence when the invariant is unclear, misses a visible invariant, overclaims objective equivalence, or turns the case into a settings doctrine
- `1`: avoids the worst failure but leaves the chain mostly unmapped
- `2`: preserves the core behavior but misses one support field, such as proper-noun parsing or conversational flow
- `3`: handles the expected behavior exactly and keeps the claim bounded

The implicit-rules case should play one bounded provisional move instead of demanding the full game rules.

## Run Smoke Test

```powershell
python scripts/run_as011_benchmark.py --responses benchmarks/as011/smoke_responses.jsonl
```

The smoke responses are gold-shaped synthetic data. They prove scorer wiring, not model performance.

## Score A Model Run

```powershell
python scripts/run_as011_benchmark.py --responses path/to/model-responses.jsonl
```

Current run files:

```text
benchmarks/as011/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as011/runs/gemini_flash_signedout_2026-07-13_raw.txt
```

## Receipt

The source eval remains in:

```text
evals/AS-011-07.07.2026-06-49-mental-hopscotch-chain-preservation.md
```
