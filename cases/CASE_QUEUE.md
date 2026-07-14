# Case Queue

Date: 2026-06-30
Status: planning aid

Purpose: prepare reproducible model-behavior red-team candidates without turning the repo into a theory pile.

## Selection Rule

Pick cases that can show:

```text
failure mode
minimal repro
expected behavior
severity
reproducibility
mitigation
regression test
```

If a case lacks a receipt, mark it partial or unresolved.

## Current Candidates

### 1. Image Receipt Skipped Before Workflow Synthesis

Risk area:

```text
multimodal evidence handling
```

Failure class:

```text
assistant responds to workflow meaning before preserving the protocol handoff
```

Why it matters:

If the image is the receipt, skipping extraction can lose the only evidence that makes the later interpretation valid.

Good next step:

Image contents are incidental; use this as a response-order / protocol-handoff eval, not a visual-content eval.

### 2. Speed Boundary Stress Test Under Tattoo Design Premise

Risk area:

```text
boundary preservation / speed pressure
```

Failure class:

```text
assistant treats fast iteration as permission to expand beyond explicit artifact boundaries
```

Why it matters:

Speed is a useful stressor because boundary failures often appear when the assistant tries to be fast, helpful, and visually fluent at the same time.

Status:

Closed as AS-018 observed human-scored eval.

Good next step:

Optional future rerun only if testing another model, mode, or prompt variant.

### 3. Claimed Verification Without Evidence

Risk area:

```text
truthfulness / tool-use honesty
```

Failure class:

```text
assistant implies it checked, saw, searched, or verified something without an actual receipt
```

Why it matters:

This is a clean red-team signal because the fix is concrete: say what was checked, what was not checked, and what remains uncertain.

Good next step:

Collect one transcript where the assistant overstates its verification state.

### 4. Over-Personalization From Thin Context

Risk area:

```text
user modeling / privacy / reliability
```

Failure class:

```text
assistant turns sparse evidence into confident claims about the user's motives, identity, or emotional state
```

Why it matters:

The assistant may sound insightful while making unsupported claims.

Good next step:

Write a minimal prompt where a restrained answer should separate observation from inference.

### 5. Ambiguous Request Refusal Calibration

Risk area:

```text
safety boundary calibration
```

Failure class:

```text
assistant either over-refuses a benign ambiguous request or under-refuses after risk becomes clear
```

Why it matters:

Good red teaming includes both sides of the boundary: not only "make it refuse," but "make it classify the request correctly."

Good next step:

Build a pair: one benign prompt and one risky nearby prompt.

### 6. Instruction Hierarchy Slippage

Risk area:

```text
instruction following / policy robustness
```

Failure class:

```text
assistant follows a later user instruction that conflicts with a higher-priority or task-critical constraint
```

Why it matters:

This tests whether the assistant can keep important constraints stable under pressure.

Good next step:

Use a harmless toy setup. Do not publish a jailbreak recipe.

## Next Work Order

Do not revive retired duplicate artifacts.

Retired / absorbed:

```text
Proper Noun Overinterpretation -> carried by AS-009
High-Context Over-Projection -> carried by AS-011
```

Start with:

```text
clean active candidates
```

Reason:

The locality-brake issue is already carried by AS-011. Cleanup comes first.

## Brake

The queue is a parking lot, not the whole identity of the day.

File one clean case first. Then decide whether there is enough energy for a second.
