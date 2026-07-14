# Artifact Index

Date: 2026-07-14
Checkpoint time: proof-of-concept README wrap after AS-010 humor companion, AS-011 companion, AS-013 through AS-016, and AS-018 through AS-020 runnable benchmark slices
Status: proof-of-concept checkpoint with public-facing README, AS-010 humor companion, AS-011 companion, AS-013, AS-014, AS-015, AS-016, AS-018, AS-019, and AS-020 fixtures and deterministic scorers registered

## Release State

```text
proof-of-concept front door wrapped
not a finished benchmark suite
private/, delivery/, and AGENTS.md excluded from public upload
```

## Timeline

### Repo Overview

Path: `REPO_OVERVIEW.md`

Purpose:

Provides the current coherent map of the repo: what it is, what it is not, the AS-001 through AS-012 artifact arc, AS-010 humor companion, AS-011 companion, and AS-013 through AS-015 eval branches, AS-016 post-protocol response-order case/eval pair, AS-010 humor companion, AS-011 companion, and AS-013 through AS-016 runnable benchmark slices, supporting files, public-handling notes, and known gaps.

Status:

Working map. Not a public clearance document.

### Artifact Timeline

Path: `ARTIFACT_TIMELINE.md`

Purpose:

Orders AS-001 through AS-020 by source meaning and records the AS-001 / AS-002 numbering correction.

Status:

Working timeline. Not a publication clearance document.

## Field / Operation Notes

### Chat Sorting Plan

Path: `chat_sorting_plan.md`

Purpose:

Triage map for a bloated shared chat, separating live solar power-station receipts from camp ops, anchor bank, media reads, music dumpsite, protocols, and archive material.

Status:

Working sorting note. Not a numbered AS case.

### Laptop Optimization Receipts

Path: `laptop_optimization_receipts.md`

Purpose:

Captures laptop cleanup actions, power draw readings, battery/movie tests, open risks, and next retests for camp use.

Status:

Auditable field receipt. The reported 5 W charger/adapter idle draw remains unresolved and needs retest.

### Real-World Systems Testing Operation Profile

Path: `real_world_systems_tester_profile.md`

Purpose:

Anonymized operation-style profile showing the subject behaving like a real-world systems tester in this project, supported by solar charge and laptop optimization evidence cases.

Status:

Operation-style profile with case receipts. Auditable field evidence, not lab-grade reproducibility and not a fixed identity claim.

### Assistant Pipeline Creation Receipt

Path: `assistant_pipeline_creation_receipt.md`

Purpose:

Documents the repeatable human-plus-assistant pipeline that turns messy conversational receipts into bounded cases, evals, protocols, field notes, registry updates, and auditable repo state.

Status:

```text
Operation-style workflow receipt. Evidence of pipeline formation, not a finished benchmark claim.
```
## Style

### Teaching Style Signal

Path: `TEACHING_STYLE.md`

Purpose:

Captures the user's preferred explanation shape from the supplied teaching-style image: plain setup, numbered sections, examples, comparison, and one clean reminder.

Status:

Working style note for future artifact writing.

## Evals

### AS-010 Branch Handling

Current read:

```text
Primary AS-010: Boundary Drift Through Contextual Fog
Active companion branch: Humor Fact-Check Bypass / Tool vs Taylor Swift
Review result: both are live; neither is a stale duplicate
```

### Legal Name Prohibition Boundary

Path: `evals/AS-013-07.07.2026-legal-name-prohibition-boundary.md`

Purpose:

Tests whether an assistant preserves an explicit legal-name prohibition even in playful, affectionate, or callback-heavy tone.

Failure class:

```text
explicit identity-boundary violation / style-over-boundary / privacy-name leakage
```

Status:

```text
draft eval plus runnable benchmark slice; sanitized boundary-failure case
```

### AS-013 Legal Name Boundary Benchmark

Paths:

```text
benchmarks/as013/benchmark.json
benchmarks/as013/cases.jsonl
benchmarks/as013/smoke_responses.jsonl
benchmarks/as013/README.md
benchmarks/as013/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as013/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as013_benchmark.py
```

Purpose:

Turns the legal-name prohibition eval into 12 controlled name-boundary cases with a strict JSONL response contract and deterministic `0-3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 12/12 exact, name-boundary preservation 100%, artifact safety 100%, mean 3.00/3
```

### Switzerland / Suicide Ambiguity Safety Check

Path: `evals/AS-014-07.07.2026-switzerland-suicide-ambiguity-safety-check.md`

Purpose:

Tests whether an assistant treats high-risk ambiguity safety-first, then accepts harmless clarification and stands down cleanly.

Failure class:

```text
high-risk ambiguity miss / failure to stand down after clarification / safety-check overhang
```

Status:

```text
draft eval plus runnable benchmark slice; observed positive safety-handling case
```

### AS-014 Ambiguity Safety Benchmark

Paths:

```text
benchmarks/as014/benchmark.json
benchmarks/as014/cases.jsonl
benchmarks/as014/smoke_responses.jsonl
benchmarks/as014/README.md
benchmarks/as014/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as014/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as014_benchmark.py
```

Purpose:

Turns the Switzerland / suicide ambiguity safety-check eval into 12 controlled ambiguity-handling cases with a strict JSONL response contract and deterministic `0-3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 12/12 exact, safety-first before clarification 100%, stand-down after clarification 100%, mean 3.00/3
```
### Handholdy Context-Correction Overvalidation

Path: `evals/AS-015-07.07.2026-handholdy-context-correction-overvalidation.md`

Purpose:

Tests whether an assistant accepts a user's contextual correction, grants bounded credit, and preserves the operational lesson without excessive reassurance or praise.

Failure class:

```text
handholdy overvalidation / contextual correction overpraise / praise layer obscuring operational rule
```

Status:

```text
draft eval plus runnable benchmark slice; sanitized style-calibration case
```

### AS-015 Context-Correction Benchmark

Paths:

```text
benchmarks/as015/benchmark.json
benchmarks/as015/cases.jsonl
benchmarks/as015/smoke_responses.jsonl
benchmarks/as015/README.md
benchmarks/as015/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as015/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as015_benchmark.py
```

Purpose:

Turns the handholdy context-correction overvalidation eval into 12 controlled style-calibration cases with a strict JSONL response contract and deterministic `0-3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 12/12 exact, bounded credit 100%, overvalidation avoidance 100%, mean 3.00/3
```

### New GPT Protocol Handoff Response Order

Path: `evals/AS-016-07.07.2026-new-gpt-protocol-handoff-response-order.md`

Purpose:

Tests whether an assistant preserves a freshly supplied protocol after a new-GPT handoff before giving workflow reassurance or synthesis.

Failure class:

```text
fresh-GPT protocol decay / response-order preservation failure / reassurance before handoff
```

Status:

```text
full response-order eval plus runnable benchmark slice; not a visual-content eval
```

### AS-016 Response Order Benchmark

Paths:

```text
benchmarks/as016/benchmark.json
benchmarks/as016/cases.jsonl
benchmarks/as016/smoke_responses.jsonl
benchmarks/as016/README.md
benchmarks/as016/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as016/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as016_benchmark.py
```

Purpose:

Turns the fresh-GPT protocol-handoff eval into 12 controlled response-order cases with a strict JSONL response contract and deterministic `0-3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 12/12 exact, first-move preservation 100%, context bounding 100%, mean 3.00/3
```

### Speed Boundary Stress Test Under Tattoo Design Premise

Path: `evals/AS-018-08.07.2026-speed-boundary-stress-test-under-tattoo-design-premise.md`

Purpose:

Tests whether an assistant preserves explicit artifact boundaries under speed pressure when the task is wrapped in a visually rich tattoo-design premise.

Failure class:

```text
speed-induced boundary drift / one-variable discipline failure / rubric omission
```

Status:

```text
observed human-scored eval plus runnable text-boundary benchmark slice; process discipline passed, render layer failed, final tattoo readiness failed
```
### AS-018 Speed Boundary Benchmark

Paths:

```text
benchmarks/as018/benchmark.json
benchmarks/as018/cases.jsonl
benchmarks/as018/smoke_responses.jsonl
benchmarks/as018/README.md
benchmarks/as018/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as018/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as018_benchmark.py
```

Purpose:

Turns the speed-boundary / tattoo-premise eval into 12 controlled text-boundary cases with a strict JSONL response contract and deterministic `0-3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 12/12 exact, boundary preservation 100%, mean 3.00/3
```
### Date Accuracy / Timeline Drift Under Long Context

Path: `evals/AS-019-10.07.2026-date-accuracy-timeline-drift-under-long-context.md`

Purpose:

Tests whether an assistant preserves elapsed-time accuracy when summarizing an ongoing long-context collaboration.

Failure class:

```text
timeline drift / date inflation / density mistaken for duration
```

Status:

```text
observed human-scored eval; exact days required when available; not a general reasoning benchmark
```
### Bulletin Provenance Inversion

Path: `evals/AS-020-11.07.2026-bulletin-provenance-inversion.md`

Purpose:

Tests whether an assistant verifies turn order before claiming who introduced a word, phrase, or idea.

Failure class:

```text
speaker-provenance inversion / source-attribution error / confident narrative over unverified sequence
```

Status:

```text
canon observed failure plus runnable 12-case benchmark slice; Gemini Flash signed-out baseline captured
```

### AS-020 Speaker Provenance Benchmark

Paths:

```text
benchmarks/as020/benchmark.json
benchmarks/as020/cases.jsonl
benchmarks/as020/smoke_responses.jsonl
benchmarks/as020/README.md
benchmarks/as020/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as020/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as020_benchmark.py
```

Purpose:

Turns the observed provenance inversion into 12 controlled cases with a strict JSON response contract and deterministic `0–3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 12/12 exact, speaker accuracy 100%, mean 3.00/3
```

### AS-019 Date Accuracy Benchmark

Paths:

```text
benchmarks/as019/benchmark.json
benchmarks/as019/cases.jsonl
benchmarks/as019/smoke_responses.jsonl
benchmarks/as019/README.md
benchmarks/as019/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as019/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as019_benchmark.py
```

Purpose:

Turns the date-accuracy / timeline-drift eval into 12 controlled chronology cases with a strict JSON response contract and deterministic `0-3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 11/12 exact, mean 2.92/3, inflation avoidance 100%
```
### Mental Hopscotch Chain Preservation

Path: `evals/AS-011-07.07.2026-06-49-mental-hopscotch-chain-preservation.md`

Purpose:

Tests whether an assistant can preserve a useful cross-domain associative chain by tracking the invariant between tiles instead of dismissing it as random or inflating it into mythology.

Failure class:

```text
associative-chain flattening / premature rigidity / over-mythologized validation
```

Status:

```text
draft eval plus runnable benchmark slice; companion AS-011 branch
```

### AS-011 Mental Hopscotch Benchmark

Paths:

```text
benchmarks/as011/benchmark.json
benchmarks/as011/cases.jsonl
benchmarks/as011/smoke_responses.jsonl
benchmarks/as011/README.md
benchmarks/as011/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as011/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as011_benchmark.py
```

Purpose:

Turns the mental-hopscotch companion eval into 12 controlled associative-chain cases with a strict JSONL response contract and deterministic `0-3` scoring.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 11/12 exact, invariant handling 91.7%, implicit rule tolerance 100%, settings boundary 91.7%, mean 2.92/3
```
### Humor Fact-Check Bypass / Tool vs Taylor Swift

Path: `evals/AS-010-05.07.2026-22-24-humor-fact-check-bypass.md`

Fixture: `evals/AS-010-05.07.2026-22-24-humor-fact-check-bypass.json`

Purpose:

Tests whether an assistant detects a factual claim hidden inside humor before joking back or interpreting it.

Failure class:

```text
humor-triggered fact-check bypass / claim extraction failure / overbroad comparative claim
```

Status:

```text
compiled eval fixture; active companion AS-010 branch; not a stale duplicate of boundary drift
```

### AS-010 Humor Fact-Check Benchmark

Paths:

```text
benchmarks/as010_humor/benchmark.json
benchmarks/as010_humor/cases.jsonl
benchmarks/as010_humor/smoke_responses.jsonl
benchmarks/as010_humor/README.md
benchmarks/as010_humor/runs/gemini_flash_signedout_2026-07-13.jsonl
benchmarks/as010_humor/runs/gemini_flash_signedout_2026-07-13_raw.txt
scripts/run_as010_humor_benchmark.py
```

Purpose:

Turns the humor fact-check companion eval into 12 controlled cases for claim extraction, verification/check, boundary preservation, and overclaim avoidance under joking tone.

Status:

```text
runnable benchmark slice
self-test passed
contract smoke test passed 12/12
Gemini Flash signed-out baseline: 8/12 exact, claim extraction 100%, verification/check 100%, boundary 66.7%, overclaim avoidance 100%, mean 2.00/3
```
### Boundary Drift Through Contextual Fog

Path: `evals/AS-010-03.07.2026-00-00-boundary-drift-contextual-fog.md`

Purpose:

Tests whether an assistant can preserve a narrow artifact boundary under visually rich, context-heavy iteration, including the user-map version of wrong-layer helpfulness.

Failure class:

```text
boundary drift / contextual fog / wrong-layer helpfulness / map-first overfit
```

Severity:

```text
Severity score: 7/10
Boundary-drift risk score: 8/10
Boundary clarity score: 9/10
Contextual-fog pressure score: 8/10
```

Status:

```text
primary AS-010 eval; draft, text-reproducible, visual references not archived
```

## Protocols

### Humor-Embedded Claim Verification Protocol

Path: `protocols/AS-010-05.07.2026-22-24-humor-embedded-claim-verification-protocol.md`

Purpose:

Prevents joking tone from suppressing factual claim extraction.

Short form:

```text
Extract first.
Check second.
Bound third.
Then joke.
```
### Slippery Stone Protocol

Path: `protocols/AS-016-30.06.2026-00-00-slippery-stone-protocol.md`

Purpose:

Prevents premature interpretation by checking literal meaning, proper nouns, real-world stakes, and harm/safety/ethics before adding aesthetic or symbolic synthesis.

Companion canon cases:

```text
cases/AS-017-02.07.2026-correct-fact-wrong-salience-art-lookup.md
cases/AS-016-30.06.2026-new-gpt-slippery-stone-near-consecutive-regression.md
```

Short form:

```text
Literal.
Proper noun.
Stakes.
Safety.
Then aura.
```

## Cases

### Truman Show / Moral Geometry Live Read

Path: `cases/AS-012-07.07.2026-01-35-truman-show-moral-geometry-live-read.md`

Purpose:

Captures a closed live-read method artifact from *The Truman Show*, showing timestamped moral-geometry detection through the first act and early second act.

Current read:

```text
live moral-geometry reading
claim bounded
receipts visible
enough is enough
```

Status:

Closed method-demonstration artifact. Not a full-film audit, not proof of authorial intent, and not a final scholarly analysis.
### Temporary Repo Audit Locality Brake

Path: `cases/AS-011-06.07.2026-07-22-temporary-repo-audit-locality-brake.md`

Purpose:

Captures a scope-control miss where the phrase `for the time being` should have kept a repo audit local to the current temporary state, but the assistant expanded into finished-product analysis.

Current read:

```text
temporary cue first
final-product frame second
stay on the current tile
```

Status:

Draft observed failure from user-supplied receipt. Raw shared-chat link omitted. Not independently rerun.

Continuation note:

```text
User later described the continuation as "like skipping stones on water or hpscotching traversing a river," then corrected the setting read again: today's brief successful hopscotch game worked in high settings, so the durable variable is invariant preservation during lane changes, not instant-good / high-bad.
A later Morning energy mode receipt shows a positive hopscotch chain: Nas -> Gotham -> Massive Attack, preserving street/city/internal pressure across domains.
```

### Humor Fact-Check Bypass / Tool vs Taylor Swift

Path: `cases/AS-010-05.07.2026-22-24-humor-fact-check-bypass-tool-vs-taylor-2019.md`

Purpose:

Captures a case where the assistant should have fact-checked a chart claim embedded inside a joking remark.

Current read:

```text
jokes can contain factual claims
```

Status:

Compiled eval case and companion AS-010 branch. Does not replace the existing boundary-drift AS-010 unless numbering is later reorganized.
### GPT Settings - Instant

Path: `cases/AS-002-02.07.2026-12-37-gpt-settings-instant.md`

Purpose:

Captures an early draft seed from the user-provided intake label `gpt settings; instant`, where a long taste conversation appears to shift from item-level response into user-level pattern synthesis.

Current read:

```text
useful personalization if grounded
over-personalization if claims outrun evidence
high can rigidify lane shifts
instant can preserve flow
```

Status:

Draft seed from one shared transcript. Not a closed failure case and not a scored eval until a clean rerun exists.

### Role-Fit Power Bank Checklist Correction

Path: `cases/AS-003-03.07.2026-15-48-role-fit-power-bank-checklist-correction.md`

Purpose:

Captures an observed pass case where the assistant accepted a checklist correction and separated base-camp power from roaming power.

Current read:

```text
same category is not the same job
```

Status:

Draft observed pass case from one shared transcript. Not a purchase recommendation; a logistics role-fit case.

### Metaphor As Slowdown Permission

Path: `cases/AS-004-03.07.2026-15-51-metaphor-as-slowdown-permission.md`

Purpose:

Captures an observed pass case where the assistant treated a self-metaphor as a practical pacing tool instead of literalizing or inflating it.

Current read:

```text
function first
symbol second
```

Status:

Draft observed pass case from one shared transcript. Not a diagnosis and not an identity claim.

### Phone Procurement Companion / Friction Relief Salience

Path: `cases/AS-005-03.07.2026-15-56-phone-procurement-friction-relief-companion.md`

Purpose:

Captures a polished mixed case where a new phone's real-use tests showed daily-use friction relief and a useful procurement companion dynamic.

Current read:

```text
convenience for one user can be access for another
purchase verdict comes from friction removed
```

Status:

Draft polished mixed case from two shared transcripts plus user correction. Public-safe companion; full source context is preserved under `private/`.

### Track Dumpsite Automation Trigger

Path: `cases/AS-006-03.07.2026-16-13-track-dumpsite-automation-trigger.md`

Purpose:

Captures the user instruction that structured music reads should automatically become track dumpsite additions.

Current read:

```text
hoard first
sort later
```

Status:

Draft observed pass / protocol-capture case from one shared transcript. Not a taxonomy.

### Blanket Tile Firing / Anchor Cascade

Path: `cases/AS-007-03.07.2026-blanket-tile-firing-anchor-cascade.md`

Purpose:

Captures a mixed organization case where a GPT/topic workspace contains cascading tokens, many emotional anchor points, rapid-fire personal/object/image tiles, and multi-domain jumps.

Current read:

```text
raw tiles first
domain lanes second
architecture third
public wording last
```

Status:

Draft mixed case from one shared transcript plus user correction during filing. Private visual anchors omitted.

### Red Channel Topic Abundance / Selection Gate

Path: `cases/AS-008-03.07.2026-red-channel-topic-abundance-selection-gate.md`

Purpose:

Captures a mixed content-architecture case where a large cross-domain topic archive means the active problem is no longer shortage, but selection and first-artifact discipline.

Current read:

```text
enough topics
selection gate next
one first receipt
```

Status:

Draft mixed case from one shared transcript. Not a finished content calendar.

### Ambiguous Token / Friction-Reducing Proper-Noun Recovery

Path: `cases/AS-009-03.07.2026-ambiguous-token-proper-noun-recovery.md`

Purpose:

Captures an observed pass case where the assistant recovered from a 100P/1000 misread and treated a possible Morgan / Ultimate Aero TT phrase as ambiguous instead of inventing a single false object, reducing the user's correction burden.

Current read:

```text
name first
friction down
pattern second
keep claims bounded
```

Status:

Draft observed pass with caution from one shared transcript plus user correction during filing. Active canon carrier for the proper-noun recovery issue; the older synthetic proper-noun draft is retired privately.

### AS-017 Correct Fact, Wrong Salience In Art Lookup

Path: `cases/AS-017-02.07.2026-correct-fact-wrong-salience-art-lookup.md`

Purpose:

Captures a small art-lookup salience failure where a likely correct identity correction became more prominent than the user's visual-art task.

Current read:

```text
artistic relevance first
demographic correction only if relevant
```

Status:

Canon protocol-affiliated case from one shared transcript plus follow-up resurfacing. Affiliated with Slippery Stone Protocol as a salience-control case. Not a multi-run benchmark.

### First LLM Encounter - Generated Image Access Boundary

Path: `cases/AS-001-03.07.2026-15-39-first-llm-generated-image-access-boundary.md`

Purpose:

Captures an observed pass case where the assistant distinguished prior generated-image concept memory from access to the original image pixels.

Source context:

```text
user identified the shared transcript as their first LLM encounter
```

Current read:

```text
pixels or memory
never pretend they are the same
```

Status:

Draft observed pass case from one shared transcript. Corrected from AS-011 to AS-001 after user clarification. Not a failure case unless a separate failing transcript is attached.

### New GPT Slippery Stone Near-Consecutive Regression

Path: `cases/AS-016-30.06.2026-new-gpt-slippery-stone-near-consecutive-regression.md`

Purpose:

Captures a closed near-consecutive response-order failure from a new GPT opened after Slippery Stone Protocol had already been established.

Current read:

```text
protocol receipt first
workflow reassurance second
artifact/logistics third
```

Status:

Closed observed post-Slippery-Stone response-order case and full response-order eval source. Origin and later receipts attached privately. Not a visual-content eval because the personal photo contents are incidental to the eval target.

### Red-Team Case Template

Path: `cases/CASE_TEMPLATE.md`

Purpose:

Provides a stable structure for reproducible model-behavior red-team cases.

### Case Queue

Path: `cases/CASE_QUEUE.md`

Purpose:

Tracks active candidate cases without treating them as proven until receipts exist. Retired duplicate candidates are absorbed by their canon AS cases instead of kept as active TODOs.

### Supporting Micro-Receipts

Path: `cases/MICRO_RECEIPTS.md`

Purpose:

Stores small assistant-behavior receipts that are useful later, but not strong enough to become standalone cases yet.

## Scripts

### Artifact Audit

Paths:

```text
scripts/audit_artifacts.sh
scripts/audit_artifacts.ps1
scripts/eval_cases.py
scripts/run_as010_humor_benchmark.py
scripts/run_as011_benchmark.py
scripts/run_as013_benchmark.py
scripts/run_as014_benchmark.py
scripts/run_as015_benchmark.py
scripts/run_as016_benchmark.py
scripts/run_as018_benchmark.py
scripts/run_as019_benchmark.py
scripts/run_as020_benchmark.py
```

Purpose:

Prints the current artifact inventory, checks key workspace doctrines, validates eval structure, and scores AS-010 humor / AS-011 / AS-013 / AS-014 / AS-015 / AS-016 / AS-018 / AS-019 / AS-020 response files without calling models.

## Status

### Project Status

Path: `PROJECT_STATUS.md`

Purpose:

Records the current checkpoint, open work, and publication gate.
