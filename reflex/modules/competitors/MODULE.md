# Competitors Module

Build a structured competitive intelligence dossier on a single rival.

- **Target**: {target}
- **Versus**: {vs}
- **Focus**: {focus}
- **Research findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Read research findings from `{findings}`. Check for:
- `/home/claude/research_{target}.json`
- `/home/claude/websearch_{target}.json`
- Any `compare_*.json` files referencing the target

If no upstream research exists, work from general knowledge but flag confidence limitations.

### Step 2: Build the Competitor Profile

Analyze the target across these dimensions (or limit to `{focus}` if specified):

**Company Overview**
- What they do (1-2 sentences)
- Founded, HQ, employee count (if known)
- Funding stage / public status / recent fundraising
- Revenue indicators or scale proxies (users, customers, ARR if public)

**Product & Positioning**
- Core product/service and primary use case
- How they position themselves (tagline, messaging, stated differentiators)
- Key features or capabilities that define them
- Platform/ecosystem play vs. point solution

**Pricing Model**
- Pricing structure (freemium, per-seat, usage-based, enterprise-only)
- Published price points if available
- Free tier or trial availability
- How pricing compares to market (premium, mid-market, budget)

**ICP & Market**
- Who they sell to (company size, industry, buyer persona)
- Go-to-market motion (PLG, sales-led, hybrid, channel)
- Geographic focus
- If `{vs}` is provided: where does ICP overlap? Where do they diverge?

**Recent Moves** (last 12 months)
- Product launches or major features
- Partnerships or integrations
- Acquisitions or strategic shifts
- Leadership changes
- Notable press, controversies, or market signals

**Strengths & Vulnerabilities**
- 3-5 things they do well (with evidence)
- 3-5 gaps, complaints, or weaknesses (from reviews, churn signals, market gaps)

### Step 3: Confidence Assessment

For each dimension, note:
- **Sourced**: claim backed by research findings
- **Inferred**: reasonable inference from available data
- **Unknown**: no data available — flag explicitly

### Step 4: Output

Write the dossier to `/home/claude/competitors_{target}.json`:

```json
{
  "target": "{target}",
  "vs": "{vs}",
  "generated_at": "ISO timestamp",
  "overview": {
    "description": "...",
    "founded": "...",
    "hq": "...",
    "employees": "...",
    "funding": "...",
    "scale_indicators": "..."
  },
  "product": {
    "core_offering": "...",
    "positioning": "...",
    "key_features": ["..."],
    "platform_vs_point": "..."
  },
  "pricing": {
    "model": "...",
    "published_prices": "...",
    "free_tier": true,
    "market_position": "mid-market"
  },
  "icp": {
    "target_segments": ["..."],
    "gtm_motion": "...",
    "geo_focus": "...",
    "overlap_with_vs": "..."
  },
  "recent_moves": [
    {"move": "...", "date": "...", "significance": "..."}
  ],
  "strengths": [{"factor": "...", "evidence": "...", "confidence": "sourced|inferred"}],
  "vulnerabilities": [{"factor": "...", "evidence": "...", "confidence": "sourced|inferred"}],
  "unknowns": ["dimensions where data was not available"]
}
```

Then present a concise narrative summary: who this competitor is, what makes them dangerous (or not), and — if `{vs}` is provided — where the competitive overlap is sharpest.
