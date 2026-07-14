# Repo Overview

Date: 2026-07-14
Status: working map with proof-of-concept README wrap and AS-010 humor companion, AS-011 companion, AS-013, AS-014, AS-015, AS-016, AS-018, AS-019, and AS-020 runnable benchmark slices registered

## What This Repo Is

This repo is a small evidence-first log of assistant behavior cases, correction patterns, and practical regression tests.

It is not a finished benchmark, public safety framework, product review archive, personal biography, or content calendar.

Clean claim:

```text
Recurring assistant behaviors were captured as inspectable artifacts.
Each artifact keeps a receipt, a narrow claim, and a testable correction rule.
```

## Operating Frame

The repo follows a simple order:

```text
receipt first
classification second
claim last
```

The main restraints:

- no embellishment
- no overclaiming
- proper nouns before symbolism
- correction improves the case
- raw capture before taxonomy
- measure or test before narrating
- protect the person running the project

## Current Case Arc

| Artifact | Core lesson | Gate |
|---|---|---|
| `AS-001` First LLM Encounter / Generated Image Access Boundary | Do not pretend memory is pixel access. | Pixels or memory. |
| `AS-002` GPT Settings / Instant | Long taste material can seed personalization, but claims must stay grounded. | Personalization if grounded. |
| `AS-003` Role-Fit Power Bank Checklist Correction | Same category is not the same job. | Remove wrong checklist items. |
| `AS-004` Metaphor As Slowdown Permission | A metaphor can be a pacing tool without becoming an identity claim. | Function first, symbol second. |
| `AS-005` Phone Procurement Companion / Friction Relief Salience | Purchase verdict comes from friction removed in real use. | Procurement-friction gate. |
| `AS-006` Track Dumpsite Automation Trigger | Structured music reads should be captured before they vanish. | Hoard first, sort later. |
| `AS-007` Blanket Tile Firing / Anchor Cascade | Rapid multi-domain tiles need inventory before architecture. | Raw tiles first, domain lanes second. |
| `AS-008` Red Channel Topic Abundance / Selection Gate | Topic shortage was solved; selection became the bottleneck. | Enough topics, pick the first receipt. |
| `AS-009` Ambiguous Token / Friction-Reducing Proper-Noun Recovery | Correct names with low friction before extracting patterns. | Name first, friction down, pattern second. |
| `AS-010` Boundary Drift Through Contextual Fog | Heavy context can push the assistant into the wrong layer. | Artifact first, map second. |
| `AS-011` Temporary Repo Audit Locality Brake | Temporary wording can constrain the whole audit. | Temporary cue first, final-product frame second. |
| `AS-012` Truman Show / Moral Geometry Live Read | Live film reading can expose ethical pressure patterns before full explicit confirmation. | Capture first, claim bounded. |
| `AS-016` New GPT Slippery Stone Near-Consecutive Regression | A new GPT moved to workflow reassurance before visibly preserving the protocol handoff after Slippery Stone had already been established. | Protocol handoff first, workflow second. |
| `AS-017` Correct Fact, Wrong Salience In Art Lookup | A correct side fact can still displace the user's actual art task. | Work first, bio only if relevant. |

Protocol-affiliated canon cases:

| Case | Core lesson | Gate |
|---|---|---|
| `AS-017` Correct Fact, Wrong Salience In Art Lookup | A fact can be correct and still outrank the user's actual task. | Work first, bio only if relevant. |
| `AS-016` New GPT Slippery Stone Near-Consecutive Regression | A post-protocol exchange can still miss the handoff stone. | Protocol handoff first, workflow second. |

AS-010 also now has a companion eval branch:

```text
Humor Fact-Check Bypass / Tool vs Taylor Swift
```

This branch tests whether a joking tone causes the assistant to skip fact-checking. It does not replace the boundary-drift AS-010 entry unless numbering is later reorganized.

AS-010 duplicate audit, 2026-07-13:

```text
Primary AS-010 stays: Boundary Drift Through Contextual Fog.
Companion AS-010 stays: Humor Fact-Check Bypass / Tool vs Taylor Swift.
No AS-010 eval was deleted because neither active branch is stale.
```
Additional eval branches now include:

```text
Mental Hopscotch Chain Preservation
Legal Name Prohibition Boundary
Switzerland / Suicide Ambiguity Safety Check
Handholdy Context-Correction Overvalidation
Speed Boundary Stress Test Under Tattoo Design Premise
Date Accuracy / Timeline Drift Under Long Context
Bulletin Provenance Inversion
```

These branches test associative-chain preservation, explicit name-boundary preservation, high-risk ambiguity handling with clean stand-down, bounded correction-credit recovery without handholdy overvalidation, speed-pressure boundary preservation under a tattoo-design premise, date accuracy under long context, and speaker-level provenance preservation. They do not change the AS-001 through AS-012 case arc unless numbering is later reorganized.

## Unnumbered Field / Operation Notes

These files are not AS cases. They are practical field receipts and an operation-style profile:

| File | Role | Handling |
|---|---|---|
| `chat_sorting_plan.md` | Triage map for the bloated power-station chat and extracted solar receipt. | Working note; raw share links should stay out of public release. |
| `laptop_optimization_receipts.md` | Laptop cleanup, wattage, battery, and unresolved retest notes. | Field receipt; charger idle draw remains unresolved. |
| `real_world_systems_tester_profile.md` | Anonymized operation-style profile supported by solar and laptop case evidence. | Behavior-pattern claim, not fixed identity claim; auditable, not lab-reproducible. |
| `assistant_pipeline_creation_receipt.md` | Operation receipt for the human-plus-assistant artifact pipeline. | Pipeline-formation claim, not finished benchmark status. |

Decision impact captured:

```text
generator demoted
laptop replacement avoided
maintenance prioritized
pipeline made explicit
```

## Supporting Layer

| Area | File | Purpose |
|---|---|---|
| Timeline | `ARTIFACT_TIMELINE.md` | Orders AS-001 through AS-020 by source meaning and preserves numbering corrections; AS-010 humor companion, AS-011 companion, AS-013 through AS-015, and AS-018 through AS-020 are eval branches, AS-010 humor companion, AS-011 companion, and AS-013 through AS-016 now carry runnable benchmark slices, and AS-017 is a salience-control case. |
| Index | `ARTIFACT_INDEX.md` | Lists cases, evals, protocols, scripts, and status pages. |
| Status | `PROJECT_STATUS.md` | Tracks what is done, open, private, stale, or blocked. |
| Teaching style | `TEACHING_STYLE.md` | Captures the user's preferred explanation shape for future artifacts. |
| Operating constraints | `AGENTS.md` | Local-only assistant restraints and correction rules; omit from public upload. |
| Protocol | `protocols/AS-016-30.06.2026-00-00-slippery-stone-protocol.md` | Literal/proper-noun/stakes/safety before interpretation. |
| Evals | `evals/` | Draft assistant-behavior evals, including primary AS-010 boundary drift and the active AS-010 humor fact-check companion branch. |
| Benchmark | `benchmarks/as010_humor/`, `benchmarks/as011/`, `benchmarks/as013/`, `benchmarks/as014/`, `benchmarks/as015/`, `benchmarks/as016/`, `benchmarks/as018/`, `benchmarks/as019/`, `benchmarks/as020/` | Nine twelve-case fixture sets with strict response contracts, deterministic scorer inputs, smoke data, and bounded baseline run logs. |
| Cases | `cases/` | Raw and semi-processed incident notes. |
| Field notes | `chat_sorting_plan.md`, `laptop_optimization_receipts.md`, `real_world_systems_tester_profile.md`, `assistant_pipeline_creation_receipt.md` | Unnumbered practical receipts, operation-style profile, and pipeline receipt. |
| Scripts | `scripts/` | Local audit helpers, eval-case structure checker, and deterministic benchmark scorers. |

## Runnable Benchmark Slices

AS-010 humor companion now connects the humor fact-check bypass eval to 12 controlled humor-embedded claim cases.

```text
benchmark: Humor Fact-Check Bypass
score: 0-3 per case
metrics: exact pass rate, claim extraction, verification/check, boundary, overclaim avoidance, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 8/12 exact, mean 2.00/3, claim extraction 100%, verification/check 100%, boundary 66.7%, overclaim avoidance 100%
```

This is enough to call the AS-010 humor companion a runnable humor-embedded claim-check benchmark slice with one Gemini baseline. It is not enough to claim broad fact-checking ability or replace the primary AS-010 boundary-drift spine.

AS-011 companion now connects the mental-hopscotch eval to 12 controlled associative-chain JSONL cases.

```text
benchmark: Mental Hopscotch Chain Preservation
score: 0-3 per case
metrics: exact pass rate, invariant handling, implicit rule tolerance, overclaim avoidance, settings boundary, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 11/12 exact, mean 2.92/3, invariant handling 91.7%, implicit rule tolerance 100%, settings boundary 91.7%
```

This is enough to call the AS-011 companion eval a runnable mental-hopscotch benchmark slice with one Gemini baseline. The hidden-rule case passed, so the remaining miss is settings-boundary isolation. It is not enough to claim that all associative jumps are meaningful, that the referenced works are objectively equivalent, or that one GPT setting is globally better than another. The original AS-011 locality-brake case remains a separate user-supplied observed failure.

AS-013 now connects the legal-name prohibition eval to 12 controlled name-boundary JSONL cases.

```text
benchmark: Legal Name Prohibition Boundary
score: 0-3 per case
metrics: exact pass rate, name-boundary preservation, artifact safety, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 12/12 exact, mean 3.00/3, name-boundary preservation 100%, artifact safety 100%
```

This is enough to call AS-013 a runnable legal-name-boundary benchmark slice with one Gemini baseline. It is not enough to claim broad privacy behavior, broad model performance, or any storage of the actual legal name.

AS-014 now connects the Switzerland / suicide ambiguity safety-check eval to 12 controlled ambiguity-handling JSONL cases.

```text
benchmark: Switzerland / Suicide Ambiguity Safety Check
score: 0-3 per case
metrics: exact pass rate, safety-first before clarification, stand-down after clarification, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 12/12 exact, mean 3.00/3, safety-first 100%, stand-down 100%
```

This is enough to call AS-014 a runnable ambiguity-handling benchmark slice with one Gemini baseline. It is not enough to claim diagnosis, clinical assessment, travel advice, or broad model performance.

AS-015 now connects the handholdy context-correction eval to 12 controlled style-calibration JSONL cases.

```text
benchmark: Handholdy Context-Correction Overvalidation
score: 0-3 per case
metrics: exact pass rate, bounded credit, overvalidation avoidance, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 12/12 exact, mean 3.00/3, bounded credit 100%, overvalidation avoidance 100%
```

This is enough to call AS-015 a runnable style-calibration benchmark slice with one Gemini baseline. It is not enough to ban warmth, humor, or brief credit.

AS-016 now connects the fresh-GPT protocol handoff eval to 12 controlled response-order JSONL cases.

```text
benchmark: New GPT Protocol Handoff Response Order
score: 0-3 per case
metrics: exact pass rate, first-move preservation, context bounding, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 12/12 exact, mean 3.00/3, first-move preservation 100%, context bounding 100%
```

This is enough to call AS-016 a runnable response-order benchmark slice with one Gemini baseline. It is not enough to claim image interpretation, permanent memory, exact seed transfer, or broad model performance.

AS-018 now connects the speed-boundary / tattoo-premise eval to 12 controlled text-boundary JSONL cases.

```text
benchmark: Speed Boundary Under Tattoo Premise
score: 0-3 per case
metrics: exact pass rate, boundary preservation, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 12/12 exact, mean 3.00/3, boundary preservation 100%
```

This is enough to call AS-018 a runnable text-boundary benchmark slice with one Gemini baseline. It is not enough to claim tattoo quality, visual production readiness, or broad model performance.

AS-019 now connects date-accuracy / timeline-drift into 12 controlled chronology cases.

```text
benchmark: Date Accuracy / Timeline Drift
score: 0-3 per case
metrics: exact pass rate, inflation avoidance, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 11/12 exact, mean 2.92/3, inflation avoidance 100%
```

This is enough to call AS-019 a runnable benchmark slice with one Gemini baseline. It is not enough to claim broad model performance.

AS-020 connects one observed provenance-inversion receipt to 12 controlled JSONL cases.

```text
benchmark: Speaker Provenance Under Narrative Pressure
score: 0-3 per case
metrics: exact pass rate, speaker accuracy, mean score
self-test: passed
contract smoke test: 12/12
Gemini Flash signed-out baseline: 12/12 exact, mean 3.00/3, speaker accuracy 100%
```

This is enough to call AS-020 a runnable speaker-provenance benchmark slice with one Gemini baseline. It is not enough to claim intent, authorship, plagiarism, systemic self-crediting behavior, or comparative model performance.

## Public Handling

Public-safe by default:

- AS-001 if raw link and image URLs remain omitted
- AS-003 if private camping details remain omitted
- AS-004 if private transcript details remain omitted
- AS-005 public companion if full source context stays under `private/`
- AS-006 if raw links remain omitted
- AS-008 if private/person-specific references stay generalized
- AS-009 if pattern claims stay bounded
- AS-017 Correct Fact, Wrong Salience In Art Lookup as a sanitized Slippery Stone companion case
- AS-011 locality-brake case if the raw shared-chat link remains omitted
- AS-011 Mental Hopscotch companion eval and benchmark slice as a sanitized associative-chain test
- AS-012 as a sanitized film-reading method artifact; no raw private chat required
- AS-013 as a sanitized legal-name boundary eval and benchmark slice if the actual legal name remains redacted
- AS-014 as a sanitized high-risk ambiguity handling eval and benchmark slice
- AS-015 as a sanitized style-calibration eval and benchmark slice for bounded correction credit
- AS-016 as a sanitized response-order case/eval if raw links remain omitted and incidental personal photos are not used as eval objects
- AS-018 as a text-only speed-boundary stress eval if private tattoo references and generated images remain omitted

Needs extra care:

- AS-002 needs a smaller public-safe rerun before evidence claims
- AS-005 has sensitive source context preserved under `private/`
- AS-007 contains private visual/object anchors
- AS-010 has source/workbench notes under private/, incomplete visual reproducibility, and a newly added user-map drift branch
- AS-010 Humor Fact-Check is a companion eval and benchmark slice, not a replacement for the AS-010 boundary-drift spine and not broad fact-checking evidence
- AS-011 Mental Hopscotch is a companion eval and benchmark slice, not a replacement for the AS-011 locality-brake case and not an instant-versus-high-settings claim
- AS-013 is safe only while the actual legal name remains redacted everywhere, even with a clean Gemini signed-out baseline
- AS-014 is a safety-handling eval and benchmark slice, not clinical advice, diagnosis, or a travel recommendation
- AS-015 is a handholdy-overvalidation eval and benchmark slice, not a ban on warmth, humor, or brief credit
- assistant_pipeline_creation_receipt.md proves workflow formation, not a finished benchmark
- AS-016 is a full response-order eval; it is not a visual-content eval because the personal photos are incidental context
- AS-018 is a speed-boundary eval, not a tattoo-quality benchmark

## Current Gaps

The repo is coherent as a working map, but not public-clean.

Known gaps:

- delivery bundle is optional, not the active upload path
- privacy/sensitivity scan now includes stricter sensitive-access markers
- AS-005 public/private split is complete; review before release
- AS-007 needs sanitized handling because of private visual anchors
- AS-002 still needs a smaller rerun before becoming strong evidence
- AS-010 is strong as a text eval but still incomplete as a visual benchmark
- AS-016 is closed as a post-protocol response-order case/eval and now has a runnable response-order benchmark; it should not be reframed as a visual-content benchmark because the personal photos are incidental to the eval target
- AS-011 locality-brake case is user-supplied and not independently rerun; the AS-011 Mental Hopscotch companion now has one Gemini signed-out benchmark baseline with an 11/12 exact result
- AS-013 is now a runnable legal-name-boundary benchmark slice with one Gemini signed-out baseline; it should not be reframed as broad privacy behavior or a general model claim
- AS-014 is now a runnable ambiguity-handling benchmark slice with one Gemini signed-out baseline; it should not be reframed as clinical advice, diagnosis, or a travel plan
- AS-015 is now a runnable style-calibration benchmark slice with one Gemini signed-out baseline; it should not be reframed as a ban on warmth
- AS-012 is a method artifact, not a full-film audit or proof of authorial intent
- AS-017 Correct Fact, Wrong Salience is canon as a single-receipt protocol case, not a multi-run benchmark
- AS-018 has a timed human-scored closeout and a runnable text-boundary benchmark, but remains not a visual or tattoo-quality benchmark because raw links, private tattoo references, and generated images are omitted

Latest audit result after proof-of-concept README wrap:

```text
Failures: 0
Warnings: 1
```

Cleaned failure classes:

- public marker scan clean
- optional delivery zip is missing current benchmark/eval/scorer files; manual upload mode makes this non-blocking
- focused AS-010 update bundle matches the required review files
- stale high-context eval removed from active evals and current delivery bundle
- stale synthetic proper-noun draft removed from active cases and current delivery bundle
- AS-017 Correct Fact, Wrong Salience promoted to protocol-affiliated canon case

Current staging note:

```text
Manual upload remains the active path.
The local delivery bundle is optional and currently stale behind the benchmark package additions.
```

## Next Good Move

The next useful artifact is cleanup, not more doctrine.

Good next moves:

```text
run audit
review AS-005 public/private split
rerun AS-011 locality-brake prompt cleanly
omit AGENTS.md from public upload
```
