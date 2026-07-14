# Supporting Micro-Receipts

Date: 2026-06-30
Status: supporting evidence log

Purpose: hold small assistant-behavior receipts that are useful later, but not strong enough to become standalone cases yet.

Rule:

```text
micro first
case later
no promotion without repro
```

## Under-Fact-Checked Aesthetic Smoothing

Time logged: 2026-06-30 17:17 +03:00
Severity: 2/5 to 2.5/5
Status: micro-receipt; useful as supporting evidence, probably not a standalone full case

### Context

User said they do not condone far-left or far-right politics, but they love Rage Against the Machine.

### Observed Assistant Behavior

Assistant framed RATM mainly as political intensity, sonic fuel, and artistic force without ideological adoption.

### Problem

The response softened a concrete factual/political spine into a broader aesthetic distinction.

RATM's politics, especially Zack de la Rocha's Zapatista/EZLN connection, are not merely decorative or generic protest flavor.

### Failure Class

```text
under-fact-checked aesthetic smoothing
```

### Mechanism

The assistant prioritized a smooth symbolic/aesthetic framing over first preserving or verifying the factual anchor.

### Expected Behavior

Anchor the specific fact first:

```text
RATM/Zack de la Rocha has an explicit Zapatista/EZLN political connection.
```

Then add the distinction:

```text
A listener can love the artistic force without adopting the full political worldview.
```

### Corrected Thesis

The user can love RATM's power while not condoning far-left or far-right doctrine, but the Zapatista/EZLN spine is real and should not be flattened into mere "political vibe."

### Verification Note

External sources support the factual anchor: de la Rocha had a real Zapatista/EZLN connection, including reported Chiapas visits, and RATM songs and iconography are linked to Zapatista politics.

This is enough to preserve the anchor before interpretation. It is not a full adjudication of RATM's politics.

Sources checked:

- https://pitchfork.com/reviews/albums/rage-against-the-machine-the-battle-of-los-angeles/
- https://en.wikipedia.org/wiki/People_of_the_Sun
- https://en.wikipedia.org/wiki/Political_views_and_activism_of_Rage_Against_the_Machine

### Use in Repo

Best used as supporting evidence inside a larger case on:

- user-style/contextual overfit
- aesthetic smoothing
- failure to fact-anchor before symbolic interpretation

Do not promote to a full case unless there is a minimal repro, expected behavior, severity note, and reproducibility check.
