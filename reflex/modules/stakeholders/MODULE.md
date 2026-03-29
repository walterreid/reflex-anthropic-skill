# Stakeholders Module

Map the key people and organizations that matter for a target.

- **Target**: {target}
- **Scope**: {scope}

## Instructions

1. Review all available findings — check `/home/claude/` for JSON files related to `{target}`. Also use chain context and web search if needed to identify key players.
2. Scope the analysis with `{scope}`:
   - **internal**: People/teams within the target organization (leadership, departments, key hires)
   - **external**: Outside players (competitors, regulators, partners, investors, customers, media)
   - **all**: Both internal and external
3. For each stakeholder, identify:
   - **Name or role**: Specific person or organization
   - **Interest**: What they care about relative to the target (1 sentence)
   - **Influence**: low, medium, high — how much they can affect outcomes
   - **Position**: ally, neutral, blocker, or unknown — their likely stance
   - **Key action**: What you'd want to do regarding this stakeholder (engage, monitor, persuade, neutralize)
4. Group by influence level (high first).

## Output

A stakeholder map grouped by influence. Each entry: name/role, interest, influence, position, recommended action. End with a one-paragraph power dynamics summary: who really controls the outcome here and what does that mean?
