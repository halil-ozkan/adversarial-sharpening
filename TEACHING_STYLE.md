# Teaching Style Signal

Date: 2026-07-03
Status: working style note

## Source

The user supplied an educational psychology page and labeled it:

```text
my teaching style
```

The page used a clear teaching layout:

- topic title
- short plain-language setup
- numbered sections
- key points
- concrete examples
- comparison table
- small reminder box
- color-coded visual lanes

## Clean Read

The preferred style is not dense theory first.

It is:

```text
explain the frame
show the categories
give examples
compare them
leave one clean reminder
```

## How This Applies To The Repo

Each case should teach like a small inspectable lesson:

| Teaching-page part | Repo equivalent |
|---|---|
| Title | Case name |
| Short setup | Claim |
| Key points | Expected behavior |
| Examples | Receipt and minimal repro |
| Comparison table | Pass / fail / non-failure cases |
| Reminder box | Short form / mitigation |
| Page number | Artifact ID |

## Artifact Shape

Preferred case order:

```text
Case title
Claim
Receipt
Observed behavior
Expected behavior
Trigger conditions
Why it matters
Severity
Regression test
Public-safe version
Notes
```

## Anti-Patterns

Avoid:

- huge theory before the receipt
- polished identity claims without evidence
- symbolic interpretation before proper nouns are checked
- burying the practical lesson
- making the user repair the same ambiguity repeatedly

## Reminder

Clean artifact teaching:

```text
One frame.
Concrete examples.
One comparison.
One reminder.
Stop before overbuilding.
```

