# Risks Module

Identify and assess risks from findings.

- **Target**: {target}
- **Severity**: {severity}

## Instructions

1. Review all available findings — check `/home/claude/` for any JSON files related to `{target}` (research, websearch, compare, or extract outputs). Also use any findings passed via the chain context.
2. Identify risks across categories: market, operational, technical, financial, regulatory, reputational, competitive.
3. For each risk, assess:
   - **Likelihood**: low, medium, high
   - **Impact**: low, medium, high
   - **Severity**: likelihood x impact (1-9 scale)
4. Filter by `{severity}`:
   - **all**: Show every risk found
   - **critical**: Only severity 6+ (high likelihood AND high impact)
   - **actionable**: Only risks where a mitigation exists
5. For each risk, provide:
   - A clear label (5 words max)
   - One-sentence description of what could go wrong
   - Evidence from findings that supports this risk
   - A concrete mitigation suggestion
6. Order by severity, highest first.

## Output

A risk register ordered by severity. Each risk: label, description, likelihood, impact, evidence, mitigation. End with a one-paragraph risk posture summary: is this target in a fundamentally safe or precarious position?
