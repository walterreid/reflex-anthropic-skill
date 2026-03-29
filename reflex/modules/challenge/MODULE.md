# Challenge Module

Stress-test an analysis by steelmanning the opposite position.

- **Target**: {target}
- **Intensity**: {intensity}

## Instructions

1. Take the analysis from the previous step in the chain (or from `/home/claude/` files related to `{target}`).
2. For every major claim or finding, ask:
   - What evidence would disprove this?
   - What unstated assumption does this rely on?
   - Who would disagree, and what's their strongest argument?
   - If this is wrong, what follows?
3. Apply `{intensity}`:
   - **gentle**: Note potential weaknesses. Suggest areas for further investigation. Constructive tone.
   - **rigorous**: Actively argue the other side. Present counter-evidence from your knowledge. Identify logical gaps. Direct tone.
   - **adversarial**: Full red-team. Assume the analysis is wrong and build the strongest case against it. Find the single point of failure that would collapse the entire argument.
4. Structure each challenge as:
   - **Claim being challenged**: The original finding (1 sentence)
   - **Challenge**: The counter-argument or weakness (2-3 sentences)
   - **If wrong, then what**: The implication if this challenge holds (1 sentence)
5. End with an overall confidence assessment: after challenging everything, how much of the original analysis still stands?

## Output

A structured critique. Each challenge: original claim, counter-argument, implication. End with an overall verdict: what percentage of the analysis survives scrutiny, what's the single biggest vulnerability, and what one thing should be verified before acting on this analysis?
