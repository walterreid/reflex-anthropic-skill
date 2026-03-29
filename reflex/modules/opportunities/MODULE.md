# Opportunities Module

Identify opportunities, gaps, and white space from findings.

- **Target**: {target}
- **Lens**: {lens}

## Instructions

1. Review all available findings — check `/home/claude/` for any JSON files related to `{target}`. Also use any findings passed via chain context.
2. Look through the lens of `{lens}`:
   - **market**: Underserved segments, unmet needs, growing demand, geographic gaps
   - **product**: Missing features, integration possibilities, UX improvements, platform extensions
   - **strategic**: Partnerships, acquisitions, pivots, new business models, timing advantages
   - **all**: All of the above
3. For each opportunity, provide:
   - A clear label (5 words max)
   - One-sentence description of the opportunity
   - Evidence from findings that supports it
   - Difficulty estimate: easy, moderate, hard
   - A "first move" — the single next step to explore this opportunity
4. Order by impact potential, highest first.

## Output

An opportunity register. Each opportunity: label, description, evidence, difficulty, first move. End with a one-paragraph synthesis: what's the biggest unlock here and why?
