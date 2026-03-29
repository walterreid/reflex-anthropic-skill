# SWOT Analysis Module

Produce a SWOT analysis from web research findings.

- **Target**: {target}
- **Format**: {format}
- **Research findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Read the research findings from `{findings}`. If a file exists at `/home/claude/research_{target}.json`, read it for structured data.
2. Categorize every finding into exactly one quadrant:
   - **Strengths**: Internal positives — what the target does well, competitive advantages, strong metrics, positive reputation
   - **Weaknesses**: Internal negatives — gaps, complaints, limitations, technical debt, poor reviews
   - **Opportunities**: External positives — market trends they could exploit, partnerships, underserved segments, emerging tech
   - **Threats**: External negatives — competitors gaining ground, regulation, market shifts, disruption risks
3. For each finding, keep the evidence trail — cite the source.
4. Format based on `{format}`:
   - **grid**: Clean 2x2 layout. 3-5 bullet points per quadrant, each with a bold label and one-sentence explanation.
   - **narrative**: Flowing prose. One paragraph per quadrant, weaving findings into a story. End with a strategic synthesis paragraph.
   - **brief**: Executive summary only. One sentence per quadrant, then a 2-sentence "so what."

## Output

The SWOT analysis in the requested format. Ground every claim in the research findings — do not invent beyond them. End with a one-paragraph strategic implication: given this SWOT, what should an observer understand about this target's position?
