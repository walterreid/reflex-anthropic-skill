# Launch Plan Module

Turn a GTM strategy into an operational execution playbook a founder can start this week.

- **Target**: {target}
- **Horizon**: {horizon} days
- **Budget**: {budget}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

This module takes a strategic GTM plan and produces the *tactical execution layer*: specific channels, keywords, communities, outreach scripts, budgets, and week-by-week milestones. It assumes `gtm-strategy` (or equivalent strategic direction) exists upstream.

If no GTM strategy is found in the workspace, do NOT proceed with guesses. Respond: "No GTM strategy found in workspace. Run `reflex gtm-strategy target:{target}` first, or chain: `reflex gtm-strategy+launch-plan target:{target}`."

### Step 1: Load Strategic Context

Read the GTM strategy from workspace. Extract:
- Beachhead vertical(s) and rationale
- Target customer profile (ICP)
- Pricing model and price points
- Founding customer program structure
- Phase 1 timeline and success criteria

Also read any available:
- `keywords_*.json` — keyword research with intent tiers, CPC estimates, competition levels. Use this directly for paid search planning — do not re-research keywords that are already on disk.
- `creative_brief_*.json` — messaging pillars, taglines, voice
- `positioning_*.json` — differentiation angles
- `audience_portrait_*.json` — psychographic detail
- `competitors_*.json` — competitive landscape for positioning context
- `research_*.json`, `websearch_*.json` — market data

### Step 2: Channel Strategy

For each beachhead vertical, research and recommend specific channels. **Use web search** to find real communities, associations, and events. Do not invent community names or assume they exist without checking.

#### Paid Search (Google Ads)
- Read keyword data from `keywords_*.json` — intent tiers, CPC estimates, and competition levels are already researched upstream
- Recommend landing page strategy: which keyword groups map to which pages
- Set budget allocation per vertical based on estimated CPCs from keyword data and `{budget}` constraint
- Flag any high-opportunity or high-competition keywords from the research

#### Organic Communities
- **Search for real communities**: Facebook groups, Reddit subreddits, trade forums, LinkedIn groups
- For each community: name, approximate size (if visible), activity level, relevance
- Engagement strategy: how long to build credibility before mentioning product (typically 2-3 weeks of genuine participation)
- Do NOT list communities without verifying they exist via web search

#### Trade Associations & Events
- Identify relevant national and regional associations for each beachhead vertical
- Membership costs if available
- Events calendar: upcoming conferences, trade shows, regional meetups
- Engagement strategy: membership, sponsorship, attendance, speaking

#### Content Marketing
- 5-8 article topics targeting beachhead vertical pain points
- Each topic: target keyword, strategic purpose, format (how-to, comparison, calculator, guide)
- SEO opportunity assessment: are competitors creating content for these terms?
- Content cadence: publishing frequency given `{budget}` constraints

#### Social / LinkedIn
- Organic LinkedIn strategy for founder personal brand
- Target audience for outreach (titles, company sizes, geographic focus)
- Paid LinkedIn consideration: CPC estimates, targeting parameters, budget threshold where it makes sense

### Step 3: Outreach Playbook

Build specific outreach materials:

**Founding Customer Outreach Email/Message**
- 2-3 variants targeting different buyer motivations (efficiency, professionalization, growth)
- Each variant: subject line, body (under 150 words), specific CTA
- Personalization hooks: what to reference about their specific business

**Follow-up Sequence**
- Timing: when to follow up (respect the ICP's time)
- Second touch: different angle, not a "just checking in"
- Maximum touches before stopping

**Community Engagement Templates**
- How to answer operational questions in forums/groups without pitching
- When and how to mention the product (only when genuinely relevant)
- Transition phrases from helpful advice to soft mention

### Step 4: Week-by-Week Timeline

Build a {horizon}-day operational plan broken into phases:

**For a 90-day plan:**

Weeks 1-2: Foundation
- Specific website changes with recommended copy
- Analytics and tracking setup
- Outreach target list building (how many, where to find them)
- Community accounts created and first contributions

Weeks 3-4: Outreach Launch
- Founding customer outreach begins (how many per week)
- Community engagement cadence
- First content pieces published
- Association membership applications

Weeks 5-8: First Customers
- Paid search campaigns launch (specific budget per week)
- Onboarding first founding customers (white-glove process)
- Content publishing cadence continues
- First feedback collection and product iteration

Weeks 9-12: Validation
- First case studies and testimonials collected
- Paid campaign optimization based on data
- Outbound outreach with social proof
- Decision framework: what metrics determine next phase

Each week should list 3-5 specific actions with estimated time investment.

### Step 5: Budget Breakdown

Provide a line-item budget for the full {horizon} period:

| Category | Low Estimate | High Estimate | Notes |
|----------|-------------|---------------|-------|
| Each channel | $X | $Y | Assumptions |
| **Total** | **$X** | **$Y** | |

Low estimate assumes founder does everything. High estimate assumes outsourcing content and design. Both must be realistic for `{budget}` constraint.

### Step 6: Milestone Metrics

Define measurable targets at 30-day intervals:

| Metric | 30 Days | 60 Days | 90 Days |
|--------|---------|---------|---------|
| Outreach conversations | X | Y | Z |
| Demo/pilot agreements | X | Y | Z |
| Active platform users | X | Y | Z |
| Testimonials collected | X | Y | Z |
| Published case studies | X | Y | Z |
| Monthly recurring revenue | $X | $Y | $Z |
| Website conversion rate | baseline | measure | optimize |
| CAC (if measurable) | — | estimate | refine |

Set targets that are ambitious but realistic for the `{budget}` and `{constraints}` context.

### Step 7: Decision Framework

At the end of {horizon} days, what questions should the founder be able to answer?
- Which vertical converts better?
- Which messaging resonates? (pillar, ad copy, landing page)
- What's the CAC? Is it sustainable?
- What product gaps surfaced from real users?
- Is the beachhead working, or should Phase 2 targets be reconsidered?

### Step 8: Output

Write the launch plan to `/home/claude/launch_plan_{target}.json`:

```json
{
  "target": "{target}",
  "horizon_days": {horizon},
  "budget": "{budget}",
  "generated_at": "ISO timestamp",
  "evidence_base": ["list of workspace files consumed"],
  "channels": {
    "paid_search": {
      "keywords": [{"keyword": "...", "intent": "...", "est_cpc": "...", "competition": "..."}],
      "budget_monthly": "...",
      "landing_page_strategy": "..."
    },
    "communities": [
      {"name": "...", "platform": "...", "size": "...", "relevance": "...", "verified": true}
    ],
    "associations": [
      {"name": "...", "membership_cost": "...", "events": ["..."], "strategy": "..."}
    ],
    "content": [
      {"topic": "...", "target_keyword": "...", "format": "...", "purpose": "..."}
    ],
    "linkedin": {
      "organic_strategy": "...",
      "paid_recommendation": "..."
    }
  },
  "outreach": {
    "founding_customer_templates": [
      {"variant": "...", "subject": "...", "body": "...", "cta": "..."}
    ],
    "followup_sequence": ["..."],
    "community_engagement": "..."
  },
  "timeline": [
    {
      "period": "Weeks 1-2",
      "name": "Foundation",
      "actions": [{"action": "...", "time_estimate": "...", "owner": "founder|outsourced"}]
    }
  ],
  "budget_breakdown": [
    {"category": "...", "low": "...", "high": "...", "notes": "..."}
  ],
  "milestones": {
    "30_day": {"metric": "target"},
    "60_day": {"metric": "target"},
    "90_day": {"metric": "target"}
  },
  "decision_framework": ["questions to answer at horizon end"],
  "summary": "3-5 sentence summary of the operational plan"
}
```

## Evidence Certification

If `certify_*.json` exists in the workspace, read the `appendix_for_formatter` section and embed it as an "Evidence & Confidence Assessment" appendix at the end of the document. Include the claim table, gaps disclosure, and methodology note as-is. Do not editorialize — present the certification exactly as produced.

## Delivery

After writing the launch plan JSON to disk, **deliver as a formatted Word document (.docx)** using Anthropic's document skill. A launch plan is an operational playbook a founder works from daily and shares with team and advisors. The JSON on disk is the evidence trail. The .docx is the deliverable. Both are required.

Present a narrative summary that a founder can read in 3 minutes and know exactly what to do this week. Lead with the first 2-3 actions. Don't list everything — highlight what matters most right now. The full detail is on disk and in the document.

End with the natural next step: "Once you've executed this plan, `reflex retro` can assess what worked, or `reflex gtm-strategy` can be re-run with updated evidence from real customer data."
