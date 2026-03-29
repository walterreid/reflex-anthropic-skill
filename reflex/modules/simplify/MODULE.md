# Simplify Module

Rewrite findings or analysis for a specific audience.

- **Target**: {target}
- **Audience**: {audience}

## Instructions

1. Take the analysis from the previous step in the chain (or from `/home/claude/` files related to `{target}`).
2. Rewrite everything for `{audience}`:
   - **executive**: Strip all technical detail. Lead with business impact and decisions needed. Use metrics, not mechanisms. 3-5 bullet points max, then a recommendation.
   - **technical**: Keep technical depth but add implementation context. Include specific tools, APIs, versions. Assume the reader can code.
   - **non-technical**: Replace all jargon with plain language. Use analogies from everyday life. Explain why things matter, not how they work.
   - **board**: Highest level. One paragraph max per topic. Focus on risk, opportunity, and resource allocation. No details — just the strategic picture.
   - **journalist**: Newsworthy framing. Lead with the most surprising or impactful finding. Use concrete numbers. Write for someone who will rewrite this for a general audience.
3. Preserve all factual claims and evidence — simplification is about language, not about removing substance.
4. Maintain the structure of the upstream analysis (if it was a risk register, keep it as a risk register — just in simpler language).

## Output

The upstream analysis, fully rewritten for `{audience}`. Same substance, different language. No meta-commentary about the simplification — just deliver the rewritten version.
