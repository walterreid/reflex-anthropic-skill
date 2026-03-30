# Trends Module

Scan a market or domain for signals: emerging technology, regulatory shifts, demand patterns, investment flows, and talent movements.

- **Target**: {target}
- **Horizon**: {horizon}
- **Focus**: {focus}
- **Research findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Read research findings from `{findings}`. Check for:
- `/home/claude/research_{target}.json`
- `/home/claude/websearch_{target}.json`

If no upstream research exists, work from general knowledge but flag confidence limitations. This module is designed to feed downstream analyzers (swot, scenario, opportunities) so structured output quality matters.

### Step 2: Scan for Trends

Identify 8-15 trends across these categories (or limit to `{focus}` if specified):

**Technology Trends**
- New tools, platforms, or paradigms gaining adoption
- Infrastructure shifts (cloud, edge, AI, blockchain)
- Developer/builder ecosystem movements

**Regulatory & Policy**
- Legislation in progress or recently passed
- Enforcement actions or precedent-setting cases
- Standards bodies or industry self-regulation

**Demand & Behavior**
- Buyer preference shifts
- New use cases or workflows emerging
- Channel or distribution changes

**Investment & Capital**
- Where VC/PE money is flowing
- M&A activity and consolidation patterns
- Public market signals (IPOs, valuations, multiples)

**Talent & Workforce**
- Skill demand shifts
- Hiring/layoff patterns
- Remote/hybrid/return-to-office dynamics

### Step 3: Tag Each Trend

For every identified trend, assess:

- **velocity**: `accelerating` | `stable` | `decelerating` — is this gaining or losing momentum?
- **impact_horizon**: `6mo` | `12mo` | `24mo` — when will this materially affect the domain?
- **impact_magnitude**: `high` | `medium` | `low` — how much will it move the market?
- **confidence**: `high` (multiple corroborating signals) | `medium` (single strong signal) | `low` (early/speculative)
- **category**: which of the five categories above
- **evidence**: source references from research findings
- **implication**: one sentence on what this means for companies in the space

### Step 4: Identify Trend Clusters

Group related trends into 2-4 macro themes. For each cluster:
- Name the theme
- List the component trends
- Describe the combined implication
- Flag whether trends in the cluster reinforce or conflict with each other

### Step 5: Output

Write to `/home/claude/trends_{target}.json`:

```json
{
  "target": "{target}",
  "horizon": "{horizon}",
  "generated_at": "ISO timestamp",
  "trends": [
    {
      "trend": "Short description of the trend",
      "category": "technology|regulatory|demand|investment|talent",
      "velocity": "accelerating|stable|decelerating",
      "impact_horizon": "6mo|12mo|24mo",
      "impact_magnitude": "high|medium|low",
      "confidence": "high|medium|low",
      "evidence": ["..."],
      "implication": "What this means for the domain"
    }
  ],
  "clusters": [
    {
      "theme": "Macro theme name",
      "trends": ["trend descriptions included in this cluster"],
      "combined_implication": "...",
      "internal_coherence": "reinforcing|mixed|conflicting"
    }
  ],
  "summary": {
    "accelerating_count": 5,
    "high_impact_count": 3,
    "top_signal": "The single most important trend to watch"
  }
}
```

Then present a concise narrative: the 2-3 most important trends, the dominant macro theme, and what a company in this space should be paying attention to over the next `{horizon}`. Flag any trend conflicts (e.g., regulation pushing one direction while demand pulls another).
