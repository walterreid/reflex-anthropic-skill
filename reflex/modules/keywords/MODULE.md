# Keywords Module

Research keyword opportunities for a product or vertical using web search. Produces structured keyword data that downstream modules (advertising, launch-plan, content strategy) can consume.

- **Target**: {target}
- **Verticals**: {verticals}
- **Intent**: {intent}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Determine Verticals

If `{verticals}` is "infer", check the workspace for:
- `gtm_strategy_*.json` — extract beachhead verticals
- `positioning_*.json` — extract target segments
- `creative_brief_*.json` — extract ICP verticals

If no workspace data exists, research the target to identify 2-3 primary verticals it serves.

### Step 2: Research Keywords

For each vertical, use web search to find real keyword data. Search for:
- "[vertical] software" — the category search
- "[vertical] [core function] software" — the specific function (scheduling, dispatch, routing, etc.)
- "[competitor name] alternative" — competitor displacement terms
- "[vertical] business tips" / "how to manage [vertical]" — top-funnel content terms
- "[vertical] [pain point]" — problem-aware searches

**Do not invent keywords or CPC estimates.** Use web search to validate that these terms are actually searched. If you can find CPC or competition data from SEO tools in search results, include it. If not, estimate competition as low/medium/high based on the number of ads and SEO-optimized pages you see in results.

### Step 3: Structure by Intent Tier

Group every keyword into one of three intent tiers:

**Bottom-funnel (high intent, highest value):**
- "[vertical] software", "[vertical] dispatch software", "[competitor] alternative", "[competitor] vs", "best [vertical] app"
- These searchers are actively evaluating solutions. Highest conversion rate, often highest CPC.

**Mid-funnel (consideration):**
- "how to manage [vertical] routes", "best software for [vertical]", "[vertical] scheduling", "[vertical] fleet management"
- These searchers know they have a problem and are exploring solutions. Moderate conversion, moderate CPC.

**Top-funnel (awareness, content marketing):**
- "[vertical] business tips", "how to grow [vertical] company", "[vertical] efficiency", "[pain point] solutions"
- These searchers aren't looking for software yet. Low conversion from ads, but valuable for content marketing and SEO.

If `{intent}` is "bottom", focus research on bottom-funnel only. If "content", focus on top-funnel. If "all", research all three tiers.

### Step 4: Assess Competition

For each keyword group:
- **Low competition** — few ads showing, organic results are thin or non-specific. Opportunity.
- **Medium competition** — some ads, decent organic content. Standard.
- **High competition** — packed with ads, strong SEO competitors, high estimated CPC. Caution — needs higher budget or long-tail variants.

Flag any keywords where competition is unusually low (untapped opportunity) or unusually high (budget trap).

### Step 5: Negative Keywords

Identify 5-10 negative keywords per vertical — terms that look related but attract the wrong audience:
- "free [vertical] software" (if targeting paid customers)
- "[vertical] jobs" or "[vertical] salary" (job seekers, not buyers)
- "[vertical] DIY" (if targeting businesses, not consumers)
- Enterprise terms (if targeting SMBs)

### Step 6: Write to Disk

Write to `/home/claude/keywords_{target}.json`:

```json
{
  "target": "{target}",
  "researched_at": "ISO timestamp",
  "verticals": ["list of verticals researched"],
  "keywords": [
    {
      "keyword": "the search term",
      "vertical": "which vertical this serves",
      "intent": "bottom|mid|top",
      "est_cpc": "$X-$Y or unknown",
      "competition": "low|medium|high",
      "notes": "any context — opportunity flag, competition warning, etc."
    }
  ],
  "negative_keywords": ["terms to exclude"],
  "summary": "2-3 sentence overview of the keyword landscape"
}
```

## Output

Brief summary of the keyword landscape: how many keywords found per vertical, which intent tier has the most opportunity, any surprising gaps or crowded spaces. The structured data is on disk for downstream modules. Don't list every keyword — highlight the 3-5 most interesting findings.
