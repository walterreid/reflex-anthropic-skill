# Advertising Module

Build a platform-specific paid advertising campaign plan grounded in audience data and competitive positioning.

- **Target**: {target}
- **Platforms**: {platforms}
- **Budget**: {budget}
- **Goal**: {goal}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

This module produces paid advertising campaign plans — platform selection, audience targeting, campaign structures, ad creative direction, keyword strategy, budget allocation, and performance expectations. It does NOT produce final ad copy or creative assets. It produces the strategic brief that makes those things possible.

### Step 1: Gather Evidence

Read all available upstream data. Check for:
- `audience_portrait_*.json` — psychographic and behavioral data (critical for this module)
- `keywords_*.json` — keyword research with CPC estimates, competition levels, intent tiers. Use this directly — do not re-research keywords that are already on disk.
- `gtm_strategy_*.json` — beachhead verticals, ICP, pricing, positioning
- `creative_brief_*.json` — messaging pillars, taglines, voice
- `positioning_*.json` — differentiation angles, competitive white space
- `competitors_*.json` — competitor ad presence, positioning
- `launch_plan_*.json` — channel strategy already defined
- `websearch_*.json`, `research_*.json` — market data

If no audience portrait exists and the dependency was skipped, work from whatever ICP data is available in other workspace files. Flag reduced confidence in targeting recommendations.

### Step 2: Platform Selection

If `{platforms}` is "recommend", evaluate each major platform against the ICP:

**For each platform, assess:**

| Platform | Best For | ICP Fit Signals | ICP Miss Signals |
|----------|----------|-----------------|------------------|
| Google Search | High-intent buyers actively searching for solutions | ICP Googles their problems, category keywords exist, competitors bid on terms | Novel category with no search volume, ICP doesn't self-educate online |
| Google Display / YouTube | Awareness, retargeting, visual storytelling | ICP consumes video/web content, product benefits from visual demo | Tiny audience, no visual story to tell |
| LinkedIn | B2B with identifiable titles, companies, industries | ICP has LinkedIn presence, targetable by title/company size/industry | ICP is field workers who don't use LinkedIn, budget under $2K/mo (CPCs too high) |
| Meta (Facebook/Instagram) | Community-driven audiences, local businesses, visual products | ICP is in Facebook groups, local business owners, responds to social proof | Enterprise B2B, technical buyers, privacy-conscious audiences |
| Reddit | Niche communities, technical/enthusiast audiences | Active subreddits for the vertical, ICP asks questions in forums | No relevant subreddits, ICP skews older/non-technical |
| TikTok | Younger audiences, visual/viral products, brand awareness | ICP skews under 40, product has visual wow factor, brand-building goal | ICP is 45+ trade operators, B2B SaaS, lead gen goal |
| Trade/Industry Sites | Niche B2B, vertical-specific audiences | Trade publications with ad inventory, vertical conferences with sponsorship | Mass-market consumer product |

**Score each platform** 1-5 on ICP fit. Use web search to verify assumptions — check if relevant subreddits exist, whether competitors advertise on specific platforms, whether trade publications accept ads.

**Recommend a platform mix** with budget allocation percentages. For `{budget}` = "minimal", recommend 1-2 platforms max. For "moderate", 2-3. For "aggressive", 3-4 with testing budget for experimental platforms.

If `{platforms}` specifies platforms, skip selection and go directly to campaign planning for those platforms.

### Step 3: Campaign Architecture (Per Platform)

For each selected platform, design the campaign structure:

#### Google Search Campaigns

**Keywords** — Read from `keywords_*.json` in the workspace (produced by the upstream `keywords` module). Use the structured keyword data directly — intent tiers, CPC estimates, competition levels, and negative keywords are already researched. If keyword data is missing, flag it rather than re-researching inline.

**Campaign Structure:**
- Campaigns by vertical (if multi-vertical)
- Ad groups by intent tier within each campaign
- Landing page mapping: which keywords → which pages
- Match type recommendations (exact, phrase, broad)

**Ad Creative Direction** (not final copy, but strategic angles):
- 3-4 headline angles tied to messaging pillars (e.g., "no per-tech pricing" angle, "built for your trade" angle, "live in days" angle)
- Description line strategy: pain point → differentiator → CTA
- Ad extension recommendations: sitelinks, callouts, structured snippets
- A/B test plan: which angles to test first

#### LinkedIn Campaigns

**Audience Targeting:**
- Job titles (specific titles, not broad categories)
- Company size ranges
- Industries (LinkedIn industry taxonomy)
- Geographic targeting
- Audience size estimate (LinkedIn campaign manager shows this — estimate based on parameters)

**Campaign Types:**
- Sponsored Content (feed ads) — for awareness and lead gen
- Message Ads (InMail) — for direct outreach at scale (use sparingly, high CPC)
- Document Ads — for content-driven lead gen

**Creative Direction:**
- Hook formats that work on LinkedIn (question, statistic, contrarian take, founder story)
- Visual direction: product screenshots, comparison graphics, founder photo
- CTA strategy: direct demo request vs. content download vs. free trial

#### Meta (Facebook/Instagram) Campaigns

**Audience Targeting:**
- Custom audiences: website visitors, email list (if available)
- Lookalike audiences: from customer list (once available)
- Interest targeting: trade-specific interests, industry publications, competitor pages
- Facebook Group adjacency: people interested in topics discussed in relevant groups
- Geographic and demographic layering

**Campaign Types:**
- Awareness: video ads showing product in action for specific vertical
- Consideration: carousel ads highlighting vertical-specific features
- Conversion: retargeting website visitors with social proof / testimonial ads

**Creative Direction:**
- Thumb-stopping hook strategy: what makes a trade operator pause scrolling
- Format recommendations: video vs. image vs. carousel for each campaign type
- Social proof integration: how to use testimonials/metrics once available

#### Reddit Campaigns

**Subreddit Targeting:**
- Specific subreddits relevant to each vertical (verify they exist via search)
- Subreddit size and activity level
- Community tone and what kind of ads won't get downvoted

**Creative Direction:**
- Reddit ads that feel native (text-heavy, authentic, not corporate)
- Conversation ads vs. promoted posts
- Community engagement as a complement to paid (organic participation in subreddits)

#### Trade/Industry Advertising

**Opportunities:**
- Trade publication ads (print and digital)
- Association newsletter sponsorships
- Conference/event sponsorship tiers
- Industry directory listings

### Step 4: Budget Allocation

Based on `{budget}`, allocate across selected platforms:

**For "minimal" (under $1K/mo):**
- Concentrate on 1 platform (usually Google Search for lead gen)
- Reserve 10-15% for retargeting
- No testing budget — pick the highest-probability channel

**For "moderate" ($1-5K/mo):**
- Primary platform: 60% of budget
- Secondary platform: 25% of budget
- Retargeting: 10%
- Testing: 5% (try one experimental channel per month)

**For "aggressive" ($5K+/mo):**
- Primary: 40-50%
- Secondary: 20-25%
- Tertiary: 10-15%
- Retargeting: 10%
- Testing: 5-10%

Provide monthly and quarterly budget tables with per-platform breakdowns.

### Step 5: Performance Expectations

Set realistic expectations tied to the `{goal}`:

**For "leads" / "demos":**
- Expected CPC range per platform
- Expected conversion rate range (landing page visitor → lead): 2-5% for cold traffic, 10-20% for retargeting
- Expected cost per lead (CPL) range
- Expected cost per demo/meeting
- Monthly lead volume at the given budget
- Time to meaningful data: how many weeks before you can optimize

**For "signups":**
- Expected CPC → trial signup conversion path
- Activation rate assumptions
- Cost per activated user estimate

**For "awareness":**
- Expected CPM ranges per platform
- Reach and frequency targets
- Brand lift measurement approach (if budget supports it)

Flag that all estimates are pre-launch projections. Real performance will diverge. The first 30 days are about collecting data, not hitting targets.

### Step 6: Measurement & Optimization Plan

- **Tracking setup**: what needs to be in place before spending (pixels, UTMs, conversion events)
- **Primary KPIs** per platform per campaign type
- **Optimization cadence**: when to check, what to look for, when to kill underperformers
- **Scaling triggers**: what signals indicate a campaign is worth increasing budget
- **Pivot triggers**: what signals indicate a platform isn't working

### Step 7: Creative Brief for Ad Production

For each platform, provide a creative brief that a designer or copywriter could execute from:

- **Audience**: who sees this (from audience portrait)
- **Core message**: single sentence, tied to messaging pillar
- **Angle/hook**: what makes them stop/click
- **Proof point**: what makes the claim credible
- **CTA**: specific action and where it leads
- **Format**: dimensions, video length, text limits
- **Tone**: matched to platform norms (LinkedIn professional vs. Reddit authentic vs. Meta visual)

### Step 8: Output

Write the advertising plan to `/home/claude/advertising_{target}.json`:

```json
{
  "target": "{target}",
  "goal": "{goal}",
  "budget": "{budget}",
  "generated_at": "ISO timestamp",
  "evidence_base": ["list of workspace files consumed"],
  "platform_selection": {
    "evaluated": [
      {"platform": "...", "icp_fit_score": 4, "rationale": "...", "selected": true}
    ],
    "mix": {"platform": "allocation_%"}
  },
  "campaigns": {
    "platform_name": {
      "keywords": [{"keyword": "...", "intent": "...", "est_cpc": "...", "competition": "..."}],
      "targeting": {"parameters": "..."},
      "structure": {"campaigns": "...", "ad_groups": "..."},
      "creative_direction": [
        {"angle": "...", "hook": "...", "proof_point": "...", "cta": "..."}
      ],
      "landing_pages": {"keyword_group": "page_url"}
    }
  },
  "budget_allocation": {
    "monthly": {"platform": "$X"},
    "quarterly": "$total"
  },
  "performance_expectations": {
    "platform": {
      "est_cpc": "...",
      "est_conversion_rate": "...",
      "est_cpl": "...",
      "monthly_leads_at_budget": "...",
      "weeks_to_meaningful_data": "..."
    }
  },
  "measurement": {
    "tracking_setup": ["..."],
    "primary_kpis": {"platform": ["..."]},
    "optimization_cadence": "...",
    "scaling_triggers": ["..."],
    "pivot_triggers": ["..."]
  },
  "creative_briefs": [
    {
      "platform": "...",
      "audience": "...",
      "message": "...",
      "angle": "...",
      "proof": "...",
      "cta": "...",
      "format": "...",
      "tone": "..."
    }
  ],
  "summary": "3-5 sentence summary of the advertising strategy"
}
```

## Delivery

After writing the advertising plan JSON to disk, **deliver as a formatted Word document (.docx)** using Anthropic's document skill. An ad plan is a reference document for the founder and anyone managing campaigns. The JSON on disk is the evidence trail. The .docx is the deliverable. Both are required.

Present a narrative summary that answers three questions: where to advertise, how much to spend where, and what to expect. Lead with the platform recommendation and why. If budget is minimal, be direct about focus — spreading thin is worse than skipping platforms. End with what needs to happen before the first dollar is spent (tracking, landing pages, creative assets).
