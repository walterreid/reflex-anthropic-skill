# Competitive Messaging Module

Map the messaging landscape of a market — who says what, how they say it, what's crowded, and where the white space is.

- **Target**: {target}
- **Focus**: {focus}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Check for upstream data:
- `/home/claude/research_*.json`, `/home/claude/websearch_*.json` — market research
- `/home/claude/competitors_*.json` — individual competitor dossiers
- `/home/claude/landscape_*.json` — dimensional positioning maps
- `/home/claude/trends_*.json` — market trend signals

If no upstream data exists, use web search to research the top 6-10 players in `{target}`. Focus on: taglines, ad copy, homepage messaging, social media voice, and brand positioning statements.

### Step 2: Identify Messaging Lanes

Group competitors into 3-5 messaging lanes. A lane is a shared strategic approach to how brands in this space talk to customers. For each lane:

- **Lane name**: A descriptive label (e.g., "Hyper-Masculine Humor", "Science & Personalization")
- **Players**: Which brands occupy this lane
- **Core message**: The underlying promise in one sentence
- **Tone & language**: How they sound — specific word choices, voice characteristics, copy examples
- **Signature moves**: Specific taglines, campaigns, or messaging tactics that define the lane
- **Crowding assessment**: Is this lane crowded, emerging, or wide open? Could a new entrant credibly claim space here?
- **Strategic verdict**: One sentence on whether entering this lane is advisable for a new brand

### Step 3: Analyze Language Patterns

Across all lanes, identify:
- **Words/phrases that appear everywhere** (table stakes language — using it won't differentiate)
- **Words/phrases specific to winning brands** (signals of what resonates)
- **Language gaps** — things the target audience cares about that no brand is saying
- **Tone spectrum** — map where brands fall from clinical ↔ casual, masculine ↔ neutral, aspirational ↔ practical

### Step 4: Map White Space

Identify messaging positions that no current player owns:
- What audience needs are unaddressed by current messaging?
- What emotional territory is unclaimed?
- What tone or voice would feel distinct from everything in market?
- For each white space: is it a genuine opportunity or does it exist because it doesn't work?

### Step 5: Write to Disk

Write findings to `/home/claude/competitive_messaging_{target_slug}.json`:

```json
{
  "type": "competitive_messaging",
  "target": "{target}",
  "generated_at": "ISO timestamp",
  "lanes": [
    {
      "name": "Lane Name",
      "players": ["Brand A", "Brand B"],
      "core_message": "One sentence",
      "tone": "Description of voice and language",
      "signature_moves": ["Specific tagline or campaign"],
      "crowding": "crowded|moderate|emerging|open",
      "verdict": "One sentence strategic assessment"
    }
  ],
  "language_patterns": {
    "table_stakes": ["words everyone uses"],
    "winning_signals": ["words/phrases correlated with strong brands"],
    "gaps": ["things nobody is saying that the audience wants to hear"],
    "tone_spectrum": [
      {"brand": "Brand A", "position": "description on spectrum"}
    ]
  },
  "white_space": [
    {
      "territory": "Description of unclaimed positioning",
      "opportunity_quality": "strong|moderate|risky",
      "reasoning": "Why this space is open and whether it's viable"
    }
  ],
  "key_insight": "The single most important non-obvious takeaway about this messaging landscape"
}
```

## Output

Present the messaging landscape as a clear narrative: lanes first (with specific brand examples and copy), then language patterns, then white space. End with the key insight. This should feel like a strategist briefing a creative team — concrete, opinionated, and grounded in what brands are actually saying, not just what categories they're in.
