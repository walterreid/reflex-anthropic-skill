# Landscape

Map competitors across strategic dimensions, producing a positioned competitive landscape with clusters, white space, and movement vectors.

- **Domain**: {domain}
- **Dimensions**: {dimensions}
- **Players**: {players}
- **Format**: {format}

## Instructions

1. **Gather players.** If `{players}` is not "auto", use the provided list. Otherwise, check for upstream findings in the conversation context (from chained modules like `websearch`, `research`, or `compare`). If neither exists, identify 6–12 key players in `{domain}` from your knowledge.

2. **Select dimensions.** If `{dimensions}` is not "auto", parse the two axes from the "X vs Y" format. If "auto", analyze the players and domain to select two dimensions that create the most strategic separation — dimensions where players cluster interestingly rather than lining up on a diagonal. Good axes reveal trade-offs, not just "better/worse." Consider: price vs. capability, breadth vs. depth, enterprise vs. consumer, innovation pace vs. reliability, scale vs. specialization, open vs. proprietary.

3. **Position each player.** For each player, assign a position on both axes using a 1–10 scale. Justify each placement in one sentence referencing evidence (from upstream findings) or reasoning (from domain knowledge). Be honest about uncertainty — flag positions that are judgment calls.

4. **Identify patterns:**
   - **Clusters** — groups of players occupying similar positions. Name each cluster with a strategic archetype (e.g., "Premium Incumbents", "Lean Disruptors", "Broad Generalists").
   - **White space** — quadrant areas with few or no players. Assess whether each gap is a genuine opportunity or exists because the combination is unviable.
   - **Movement vectors** — which players are shifting position and in what direction? This reveals strategic intent and competitive pressure.

5. **Produce the landscape map.** Create a visual representation using the Visualizer tool — an SVG or interactive HTML scatter plot with the two axes, player positions as labeled dots/markers, cluster boundaries, and white space annotations. Make it clear and readable.

6. **If format is "full"**, add strategic analysis:
   - **Competitive dynamics** — who threatens whom, where are collision courses?
   - **Strategic implications** — what does this landscape mean for someone entering or competing?
   - **Key insight** — the single most non-obvious takeaway from the map.

7. **Write findings to disk** at `/home/claude/landscape_{domain_slug}.json` where `{domain_slug}` is the domain name slugified (lowercased, spaces to hyphens). Structure:

```json
{
  "type": "landscape",
  "domain": "{domain}",
  "dimensions": { "x": "axis_name", "y": "axis_name" },
  "players": [
    {
      "name": "Player Name",
      "x": 7,
      "y": 4,
      "rationale": "One sentence",
      "cluster": "Cluster Name",
      "movement": "direction or stable"
    }
  ],
  "clusters": [
    {
      "name": "Cluster Name",
      "archetype": "Strategic archetype",
      "members": ["Player A", "Player B"]
    }
  ],
  "white_space": [
    {
      "region": "high-X, low-Y",
      "opportunity": true,
      "reasoning": "Why this gap exists and whether it's viable"
    }
  ],
  "key_insight": "The single most important non-obvious takeaway"
}
```

## Output

A visual competitive landscape map (via Visualizer) with labeled axes, positioned players, clusters, and white space annotations. Accompanied by conversational strategic analysis (if format is "full"). JSON written to disk for downstream modules.

The map should be the centerpiece — show first, analyze second.