# Voice DNA Module

Build a reusable voice profile from extracted writing patterns. The `extract` dependency has pulled raw style data from the samples. This module structures it into a profile that downstream formatters can consume.

- **Target**: {target}
- **Label**: {label}
- **Raw patterns**: {raw_patterns}

## Instructions

### Step 1: Analyze the Extraction

From the raw patterns, identify:

**Sentence Rhythm**
- Average sentence length tendency (short/punchy, medium/varied, long/flowing)
- Does the writer vary length deliberately? (e.g., long setup → short punch)
- Fragment usage (never, occasionally for effect, frequently)

**Tone Markers**
- Where on the spectrum: formal ↔ casual, confident ↔ hedging, warm ↔ detached, earnest ↔ ironic
- Humor style: none, dry/understated, self-deprecating, sharp/witty
- How do they handle uncertainty? (acknowledge directly, soften with qualifiers, ignore)

**Vocabulary Fingerprint**
- Signature words/phrases that recur — the words that feel like *them*
- Words they never use — notable absences that define the voice by exclusion
- Jargon comfort: do they use technical terms, translate them, or avoid them?
- Profanity/colloquialism level

**Structural Preferences**
- How do they open? (thesis-first, anecdote, question, provocation)
- How do they close? (summary, call to action, open question, circular return)
- Paragraph density: short paragraphs (1-2 sentences) or developed blocks (4-6)?
- List/bullet usage vs. prose preference

**Personality Through Writing**
- What do they care about? (what topics get the most energy/detail)
- What irritates them? (what do they push back against)
- Confidence pattern: do they state or qualify? Assert or invite?

### Step 2: Write the Voice Profile

Write to `/home/claude/voice_profile_{label}.json`:

```json
{
  "type": "voice_profile",
  "label": "{label}",
  "source": "{target}",
  "generated_at": "ISO timestamp",
  "rhythm": {
    "sentence_length": "short|medium|long|varied",
    "variation_pattern": "description",
    "fragment_usage": "never|occasional|frequent"
  },
  "tone": {
    "formality": "formal|semiformal|casual",
    "confidence": "assertive|balanced|hedging",
    "warmth": "warm|neutral|detached",
    "humor": "none|dry|self-deprecating|sharp",
    "uncertainty_handling": "direct|qualified|avoided"
  },
  "vocabulary": {
    "signature_words": ["..."],
    "avoided_words": ["..."],
    "jargon_comfort": "high|medium|low",
    "colloquialism_level": "none|light|moderate|heavy"
  },
  "structure": {
    "opening_style": "thesis|anecdote|question|provocation",
    "closing_style": "summary|cta|open_question|circular",
    "paragraph_density": "sparse|moderate|dense",
    "lists_vs_prose": "lists|mixed|prose"
  },
  "personality": {
    "cares_about": ["..."],
    "pushes_back_on": ["..."],
    "confidence_pattern": "states|qualifies|invites"
  },
  "usage_note": "To apply this profile: match the rhythm and tone markers. Use signature words naturally. Avoid the avoided words. Open and close in their style. The personality traits should inflect the content priorities, not just the language."
}
```

## Output

Present the voice profile as a readable character sketch — not a data dump. Write it as if you're briefing a ghostwriter: "This person writes like [X]. They tend to [Y]. You'll know you've got the voice right when [Z]." Then confirm the JSON was written and note which downstream modules can consume it (email, linkedin, pitch, report, whitepaper).
