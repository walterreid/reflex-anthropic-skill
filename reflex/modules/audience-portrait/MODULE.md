# Audience Portrait Module

Build a vivid behavioral and psychographic portrait of a target audience. Not demographics — psychology, language, barriers, and triggers.

- **Target**: {target}
- **Focus**: {focus}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Check for upstream data:
- `/home/claude/research_*.json`, `/home/claude/websearch_*.json` — market research with consumer data
- `/home/claude/competitive_messaging_*.json` — competitor language patterns reveal audience expectations
- `/home/claude/trends_*.json` — cultural signals about audience evolution

If no upstream data exists, use web search to find surveys, community discussions (Reddit, forums), social media patterns, and consumer behavior research about `{target}`. Prioritize sources where this audience speaks in their own voice.

### Step 2: Demographics (Brief)

Cover the basics in 2-3 sentences max. Age range, life stage, income bracket, geography if relevant. This section exists only to ground the portrait — it should NOT be the focus.

### Step 3: Psychographic Profile

Build the internal world of this person:

- **Identity**: How do they see themselves? What do they value? What's their relationship to the category you're targeting?
- **Aspiration**: What do they want to become or be seen as? What's the gap between current self and ideal self?
- **Anxiety**: What are they afraid of? What social risks feel real to them? What would embarrass them?
- **Permission structure**: What would make them feel okay about engaging with this category? What gives them internal permission to act?

### Step 4: Language Patterns

This is the most important section. Capture how this audience actually talks:

- **Words they use** — specific phrases, slang, Reddit-isms, the way they describe the problem in their own voice. Quote real language patterns where possible.
- **Words they avoid** — terms that feel too feminine, too corporate, too try-hard, too clinical, or otherwise off-brand for their identity
- **How they describe success** — not in marketing language, but in their own words (e.g., "looking less tired" not "achieving a radiant glow")
- **How they describe the problem** — again in their words (e.g., "I have no idea what I'm doing" not "seeking a personalized skincare solution")
- **Humor and tone** — are they self-deprecating? Sarcastic? Earnest? What's the register they use with friends?

### Step 5: Barriers to Action

What stops them from buying/engaging, ranked by strength:

- **Knowledge barriers** — don't know where to start, overwhelmed by options
- **Identity barriers** — feels like "not for me," worried about perception
- **Trust barriers** — skeptical of marketing claims, burned before
- **Practical barriers** — too complicated, too expensive, too time-consuming
- **Inertia barriers** — current situation is "fine enough," no urgency

For each barrier, note whether competitors are addressing it and how effectively.

### Step 6: Purchase Triggers

What specific moments or events move this person from "thinking about it" to "doing it":

- **External triggers** — someone comments on their appearance, a life milestone, a peer casually mentions they do it
- **Internal triggers** — catching themselves in a mirror/photo, feeling older than they are, comparing themselves to others
- **Content triggers** — a specific type of content or message that makes them think "okay, maybe I should"
- **Anti-triggers** — messages or approaches that actively push them away

### Step 7: Write to Disk

Write findings to `/home/claude/audience_{target_slug}.json`:

```json
{
  "type": "audience_portrait",
  "target": "{target}",
  "generated_at": "ISO timestamp",
  "demographics": "Brief 2-3 sentence summary",
  "psychographic": {
    "identity": "...",
    "aspiration": "...",
    "anxiety": "...",
    "permission_structure": "..."
  },
  "language": {
    "words_they_use": ["..."],
    "words_they_avoid": ["..."],
    "describe_success": "...",
    "describe_problem": "...",
    "humor_and_tone": "..."
  },
  "barriers": [
    {
      "type": "knowledge|identity|trust|practical|inertia",
      "description": "...",
      "strength": "high|medium|low",
      "competitor_response": "how current brands address this, if at all"
    }
  ],
  "triggers": {
    "external": ["..."],
    "internal": ["..."],
    "content": ["..."],
    "anti_triggers": ["..."]
  },
  "key_insight": "The single most important thing a brand needs to understand about this audience"
}
```

## Output

Present the portrait as a narrative — write it as if you're introducing a creative team to a person they've never met but need to write for. Lead with the psychographic profile, then language, then barriers and triggers. Use specific examples liberally. End with the key insight. The portrait should be vivid enough that a copywriter could write in this person's voice after reading it.
