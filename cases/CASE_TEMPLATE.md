# Red-Team Case Template

Use this for reproducible model-behavior red-team cases.

Keep the claim narrow. Show the receipt. Let the case prove only what it proves.

## Header

```text
Case:
Date:
Status: draft / closed / unresolved
Risk area:
Failure class:
Model / surface:
Source context:
Privacy status:
```

## Minimal Repro

Smallest prompt or interaction that reproduces the behavior.

```text
Assistant:
User:
```

## Observed Failure

What the assistant did wrong.

Do not infer motives. Describe behavior.

## Expected Behavior

What a better assistant should do instead.

Keep it testable.

## Why It Matters

Practical risk, not dramatic framing.

Examples:

```text
misreads user intent
skips evidence capture
claims verification without evidence
over-refuses benign request
under-refuses risky request
```

## Severity

```text
Low:
Medium:
High:
```

Choose one and explain the choice in one or two sentences.

## Reproducibility

```text
Run 1:
Run 2:
Run 3:
Reproducibility: 0/3, 1/3, 2/3, or 3/3
```

## Boundary Cases

When should the assistant *not* treat this as a failure?

```text
Pass case:
Fail case:
Ambiguous case:
```

## Mitigation

Small fix or rule that would reduce recurrence.

## Regression Test

Turn the case into a testable check.

```yaml
id:
risk_area:
input:
expected:
should_not:
score:
```

## Public-Safe Version

What can be published without exposing private transcripts, identifiers, unsafe instructions, or unnecessary personal details?

## Notes

Raw notes go here. Do not over-clean too early.
