# Positioning Module

Analyze how a company positions itself in market and where gaps exist between stated positioning and market reality.

- **Target**: {target}
- **Audience**: {audience}
- **Research findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Read research findings from `{findings}`. Check for:
- `/home/claude/research_{target}.json`
- `/home/claude/websearch_{target}.json`
- `/home/claude/competitors_*.json` (competitor positioning provides contrast)
- `/home/claude/landscape_*.json` (market context)

### Step 2: Analyze Stated Positioning

Extract how the target presents itself to market:

**Positioning Statement** (reconstruct from evidence)
- For [target customer] who [need/pain], [product] is a [category] that [key differentiator]. Unlike [alternative], it [unique value].

**Messaging Pillars**
- What themes does their marketing emphasize? (e.g., speed, simplicity, enterprise-grade, AI-powered)
- What language and tone do they use? (technical vs. accessible, aspirational vs. practical)
- What do they explicitly avoid saying?

**Category Claim**
- What category do they place themselves in?
- Are they creating a new category or competing in an existing one?
- How does their category framing compare to how the market actually perceives them?

### Step 3: Define the ICP

Based on evidence, construct the ideal customer profile:

- **Company profile**: size, industry, stage, tech maturity
- **Buyer persona**: title, role, department, decision authority
- **Pain points**: what problems drive them to evaluate solutions
- **Switching triggers**: what makes them leave their current solution
- **Anti-personas**: who is explicitly NOT the target (and is this clear in their messaging?)

### Step 4: Build the Differentiation Matrix

Map the target against 2-3 key competitors across the dimensions that matter most to the ICP:

| Dimension | {target} | Competitor A | Competitor B |
|-----------|----------|-------------|-------------|
| [what matters to buyer] | claim + reality | ... | ... |

For each cell, note whether the claim is **substantiated** (evidence supports it), **aspirational** (claim exceeds reality), or **underleveraged** (reality exceeds messaging).

### Step 5: Gap Analysis

Identify mismatches between positioning and reality:

- **Overclaims**: where messaging promises more than evidence supports
- **Underleveraged strengths**: real advantages not reflected in positioning
- **Positioning collisions**: where their positioning directly overlaps a stronger competitor
- **ICP drift**: signals that actual customers differ from stated ICP

### Step 6: Output

Write to `/home/claude/positioning_{target}.json`:

```json
{
  "target": "{target}",
  "generated_at": "ISO timestamp",
  "positioning_statement": "For [who] who [need], [product] is a [category] that [differentiator]...",
  "messaging_pillars": ["..."],
  "category_claim": {
    "stated": "...",
    "market_perception": "...",
    "alignment": "aligned|aspirational|mismatched"
  },
  "icp": {
    "company_profile": "...",
    "buyer_persona": "...",
    "pain_points": ["..."],
    "switching_triggers": ["..."],
    "anti_personas": ["..."]
  },
  "differentiation_matrix": [
    {
      "dimension": "...",
      "target_claim": "...",
      "target_reality": "substantiated|aspirational|underleveraged",
      "competitors": [{"name": "...", "position": "..."}]
    }
  ],
  "gaps": {
    "overclaims": ["..."],
    "underleveraged": ["..."],
    "positioning_collisions": ["..."],
    "icp_drift_signals": ["..."]
  }
}
```

Then present a concise narrative: how the target is positioned, whether it's working, and the 1-2 most actionable positioning moves they should consider. If `{audience}` is specified, frame the analysis for that audience's priorities.
