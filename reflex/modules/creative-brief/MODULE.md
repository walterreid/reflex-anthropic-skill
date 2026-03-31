# Creative Brief Module

Synthesize upstream research into a complete creative strategy for a brand. This is the bridge between research and execution.

- **Target**: {target}
- **Audience**: {audience}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather All Upstream Evidence

This module is most powerful when chained after research modules. Read everything available:
- `/home/claude/research_*.json`, `/home/claude/websearch_*.json` — market research
- `/home/claude/competitive_messaging_*.json` — messaging lanes, language patterns, white space
- `/home/claude/audience_*.json` — audience portrait, language, barriers, triggers
- `/home/claude/trends_*.json` — macro trends with velocity and impact
- `/home/claude/landscape_*.json` — competitive positioning maps
- `/home/claude/competitors_*.json` — individual competitor dossiers

If no upstream data exists, work from general knowledge but note this in the output. The brief will be significantly stronger with upstream research.

### Step 2: Core Insight

Synthesize all research into ONE core insight — the strategic truth that the entire brand should be built on. This is not a summary of the research. It's the single non-obvious connection between what the audience needs, what competitors miss, and what the brand can own.

Format: "[Audience] doesn't need [what competitors offer]. They need [the real thing]."

### Step 3: Positioning Statement

Write a positioning statement that flows directly from the core insight:

"For [specific audience] who [specific situation/tension], [Brand] is a [category frame] that [unique promise]. Unlike [competitive alternative], [Brand] [key differentiator]."

Every word should be traceable to upstream evidence. If the audience portrait identified specific language, use it. If competitive messaging identified white space, claim it.

### Step 4: Messaging Pillars

Define 3-5 messaging pillars. Each pillar is a strategic theme the brand can build content, copy, and campaigns around. For each:

- **Pillar name**: 2-4 words, memorable enough to use internally (e.g., "Obvious, Not Brave")
- **What it means**: One sentence definition
- **Why it works**: Which research finding supports this pillar
- **What it sounds like**: 1-2 example sentences in the brand's voice using this pillar
- **What it's NOT**: One sentence clarifying the boundary (e.g., "This is not bro-comedy. It's confidence without performance.")

### Step 5: White Space Claim

Based on competitive messaging analysis, explicitly state:
- What positioning territory the brand is claiming
- Which competitors own adjacent territory (and why this is distinct)
- Why this territory is credible for a new entrant
- The risk of this positioning (what could go wrong)

### Step 6: ICP Summary

Synthesize the audience portrait into a concise, actionable ICP:
- **Who they are**: 2-3 sentences combining demographics and psychographics
- **What they want**: In their own words (pull from audience language patterns)
- **What they don't want**: Specific turn-offs and anti-triggers
- **What makes them buy**: The top 3 purchase triggers
- **The one sentence that would stop them scrolling**: Based on everything above, what's the hook?

### Step 7: Tagline Options

Generate 5 tagline options. For each:
- **The tagline**: Under 8 words
- **Strategic rationale**: Which insight, pillar, or white space it draws from (cite the specific upstream finding)
- **Extensibility**: Can this work as a repeatable framework across channels? Give one example variation.
- **Risk**: What could go wrong with this line (too subtle, too clever, too similar to X competitor)

Select a **recommended tagline** with a 3-point argument for why it wins. The argument must reference:
1. A specific audience insight (from portrait or research)
2. A specific competitive gap (from messaging analysis)
3. A specific creative advantage (extensibility, emotional resonance, or memorability)

### Step 8: Write to Disk

Write findings to `/home/claude/creative_brief_{target_slug}.json`:

```json
{
  "type": "creative_brief",
  "target": "{target}",
  "audience": "{audience}",
  "generated_at": "ISO timestamp",
  "evidence_base": ["list of upstream files consumed"],
  "core_insight": "One sentence",
  "positioning_statement": "Full positioning statement",
  "messaging_pillars": [
    {
      "name": "Pillar Name",
      "meaning": "...",
      "evidence": "Which finding supports this",
      "sounds_like": "Example copy",
      "not_this": "Boundary clarification"
    }
  ],
  "white_space": {
    "claim": "...",
    "adjacent_competitors": ["..."],
    "credibility": "...",
    "risk": "..."
  },
  "icp": {
    "who": "...",
    "wants": "...",
    "doesnt_want": "...",
    "triggers": ["..."],
    "scroll_stopper": "..."
  },
  "taglines": [
    {
      "tagline": "...",
      "rationale": "...",
      "extensibility": "...",
      "risk": "..."
    }
  ],
  "recommended_tagline": {
    "tagline": "...",
    "argument": {
      "audience_insight": "...",
      "competitive_gap": "...",
      "creative_advantage": "..."
    }
  }
}
```

## Output

Present the creative brief as a structured narrative document. Use clear section headers. This should read like something a founder could hand to a creative agency or copywriter and they'd have everything they need to start executing — positioning, voice, audience, competitive context, and a recommended tagline with rationale. End with the recommended tagline and its three-point argument.
