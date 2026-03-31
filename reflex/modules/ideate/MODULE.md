# Ideate Module

Generate divergent angles for a topic. The `decompose` dependency has broken the topic into sub-questions. This module transforms those sub-questions into creative framings — not answers, but *ways of looking at the problem* that downstream modules can pursue.

- **Target**: {target}
- **Count**: {count}
- **Lens**: {lens}
- **Sub-questions**: {sub_questions}

## How This Differs from creative-brief

`creative-brief` synthesizes upstream research into ONE strategic direction. `ideate` generates MANY directions before research begins. This is pre-strategy divergence — the point is to expand the possibility space, not narrow it.

## Instructions

### Step 1: Use Sub-Questions as Seeds

The decomposed sub-questions are your raw material. For each, ask: what's a surprising or non-obvious way to approach this?

### Step 2: Apply Framing Lenses

Generate {count} angles using the `{lens}` approach:

**If mixed** (default): Use 1-2 from each framework below for variety.

**Inversion**: Flip the core assumption. If the topic assumes X is good, explore what happens if X is harmful. If it assumes the audience wants Y, what if they're running from Y?

**Analogy**: Import a framework from a completely different domain. How would a game designer approach this? A chef? An urban planner? The best analogies feel wrong for 2 seconds then obvious forever.

**Audience shift**: Reframe the topic from a perspective nobody's asked for. What does this look like to a skeptic? A regulator? A 10-year-old? Someone in 2035?

**Constraint**: Remove a key resource or assumption. What if you had no budget? No website? Only 10 words? Had to launch tomorrow? Constraints breed creativity.

**Jobs-to-be-Done**: What job is the user actually hiring this topic/product/idea to do? Not the functional job — the social and emotional job.

### Step 3: Quality-Check Each Angle

For each angle, ask:
- Is this genuinely different from the others, or a rephrasing?
- Could someone build a strategy, campaign, or argument on this?
- Would a smart person disagree with this framing? (If not, it's too obvious)

Cut any angle that fails these checks and replace it.

### Step 4: Format Output

For each angle:
- **Angle title**: 4-8 words, evocative, memorable
- **The reframe**: 1-2 sentences describing how this angle sees the topic differently
- **Why it's interesting**: 1 sentence on what this opens up that the default framing doesn't
- **Best next step**: Which Reflex module would you chain next to pursue this angle? (e.g., "research to validate," "audience-portrait to test," "challenge to stress-test")

### Step 5: Write to Disk

Write to `/home/claude/ideate_{target_slug}.json`:

```json
{
  "type": "ideation",
  "target": "{target}",
  "lens": "{lens}",
  "generated_at": "ISO timestamp",
  "angles": [
    {
      "title": "...",
      "reframe": "...",
      "why_interesting": "...",
      "suggested_next": "module_name"
    }
  ]
}
```

## Output

Present the angles as a numbered list — scannable, with bold titles. End with a recommendation: "The strongest angle for [target] is #X because [reason]. To pursue it: `reflex [suggested chain]`."

This module is a starting gun, not a finish line. Its output should make the user want to pick an angle and run.
