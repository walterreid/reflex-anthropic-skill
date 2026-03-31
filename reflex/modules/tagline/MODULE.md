# Tagline Module

Generate tagline options grounded in strategy, with extensibility analysis and a recommended pick.

- **Target**: {target}
- **Audience**: {audience}
- **Tone**: {tone}
- **Count**: {count}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Strategic Context

Check for upstream data that should inform the taglines:
- `/home/claude/creative_brief_*.json` — positioning, pillars, ICP, white space (richest source)
- `/home/claude/audience_*.json` — language patterns, barriers, triggers
- `/home/claude/competitive_messaging_*.json` — what competitors are saying, what's crowded
- `/home/claude/positioning_*.json` — existing positioning analysis
- `/home/claude/research_*.json`, `/home/claude/websearch_*.json` — raw research

If upstream data exists, every tagline must trace to a specific finding. If no upstream data exists, generate taglines from general knowledge but flag that they're not grounded in research.

### Step 2: Generate Taglines

Create {count} tagline options. Each tagline must:
- Be **under 8 words** (ideally 4-6)
- Feel **ownable** — not so generic it could belong to any brand
- Match the specified `{tone}` (or the tone implied by upstream audience/positioning data)
- Come from a **different strategic angle** — don't generate 5 variations of the same idea

For each tagline, provide:

- **The tagline**
- **Strategic root**: Which specific insight, pillar, or finding it draws from. Name the source explicitly (e.g., "From audience portrait: men describe success as 'looking less tired' not 'glowing'")
- **Emotional mechanism**: What it makes the reader feel and why (e.g., "Creates belonging by framing adoption as inevitable rather than courageous")
- **Extensibility test**: Demonstrate the tagline working in 3 different contexts:
  1. As a subject line in a cold email
  2. As a headline on a social ad
  3. As a repeatable framework (can you swap words and make variations?)
- **Competitive clearance**: Does any competitor use something similar? Is this lane crowded?
- **Risk**: What could go wrong (too subtle, too clever, easily misread, limited shelf life)

### Step 3: Select & Argue

Recommend ONE tagline. The argument must stand on three legs:

1. **Audience evidence**: A specific data point or language pattern from research showing this will resonate
2. **Competitive evidence**: A specific gap in the messaging landscape this tagline claims
3. **Creative evidence**: A concrete demonstration of why this tagline has legs as a platform (not just a one-off line)

If the evidence for any leg is weak, say so. A tagline recommendation with an honest weakness acknowledged is more useful than one with manufactured confidence.

### Step 4: Write to Disk

Write findings to `/home/claude/tagline_{target_slug}.json`:

```json
{
  "type": "tagline",
  "target": "{target}",
  "audience": "{audience}",
  "generated_at": "ISO timestamp",
  "evidence_base": ["list of upstream files consumed"],
  "options": [
    {
      "tagline": "...",
      "strategic_root": "...",
      "emotional_mechanism": "...",
      "extensibility": {
        "email_subject": "...",
        "social_headline": "...",
        "framework_variation": "..."
      },
      "competitive_clearance": "...",
      "risk": "..."
    }
  ],
  "recommended": {
    "tagline": "...",
    "argument": {
      "audience_evidence": "...",
      "competitive_evidence": "...",
      "creative_evidence": "..."
    }
  }
}
```

## Output

Present tagline options in a table for quick scanning, followed by the detailed rationale for each. End with the recommended pick and its three-leg argument. Keep the presentation crisp — this is a creative deliverable, not an analytical report.
