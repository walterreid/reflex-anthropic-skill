# GTM Strategy Module

Build an evidence-backed go-to-market strategy for a product entering a competitive market.

- **Target**: {target}
- **Market**: {market}
- **Constraints**: {constraints}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

This module produces a *strategic* go-to-market plan — beachhead selection, phased expansion, pricing, founding customer program, and risk assessment. It does NOT produce tactical execution detail (ad keywords, outreach scripts, week-by-week timelines). That's the job of `launch-plan`, which depends on this module's output.

### Step 1: Gather Evidence

Read all available upstream data. Check for:
- `websearch_*.json`, `research_*.json` — market intelligence
- `competitors_*.json`, `compare_*.json`, `landscape_*.json` — competitive intel
- `positioning_*.json`, `creative_brief_*.json` — positioning and messaging
- `audience_portrait_*.json` — buyer persona, decision patterns, objections, where they congregate. This is critical for beachhead selection and founding customer program design.
- `trends_*.json` — market signals
- Any upstream `{findings}` from chained modules

Inventory what you have. If critical evidence is missing (no market data, no competitive intel), flag it explicitly in the output rather than inventing claims.

### Step 2: Beachhead Selection

This is the most important strategic decision. Evaluate potential market entry points against these criteria:

**For each candidate vertical or segment, assess:**
1. **Incumbent density** — Who already serves this segment? How entrenched are they? What are switching costs? (Must be sourced from research, not asserted.)
2. **Software gap validation** — Does vertical-specific software actually exist? Search for "[vertical] software" and "[vertical] scheduling software" before claiming a gap. Negative claims ("no software exists") require verification — they are the most dangerous unverified assertions in GTM strategy.
3. **Product-market fit signals** — Does the product already have depth in this vertical? What domain-specific features exist?
4. **Distribution channels** — Are there franchise networks, trade associations, online communities, or concentrated buyer pools?
5. **Stickiness mechanisms** — Compliance requirements, data accumulation patterns, workflow integration depth.
6. **Market size** — Use sourced estimates. If multiple estimates exist, present the range rather than cherry-picking the highest. Flag any estimate that appears to be an outlier.

**Score each candidate** on a 1-5 scale across all six criteria. Show the scoring. Recommend the top 1-2 as beachhead with explicit rationale tied to evidence.

**Anti-patterns to avoid:**
- Asserting "no competition exists" without searching for it
- Using the highest market size estimate without noting the range
- Selecting a beachhead because it sounds good rather than because the product has depth there
- Splitting focus across 3+ beachheads for a bootstrapped company

### Step 3: Phased Expansion Plan

Design a 3-phase market entry:

**Phase 1 (Months 1-6): Beachhead**
- Which 1-2 verticals/segments
- Target customer count (realistic for constraints)
- What "proof" looks like at end of phase
- Phase gate: what must be true to move to Phase 2

**Phase 2 (Months 6-12): Adjacent expansion**
- Which verticals are adjacent (similar workflows, shared buyer profiles)
- How Phase 1 proof translates to Phase 2 credibility
- Competitive landscape shifts to watch

**Phase 3 (Months 12-24): Incumbent territory**
- When and how to enter defended markets
- Migration tooling requirements
- Competitive positioning shifts needed

### Step 4: Pricing Strategy

Recommend a pricing model that aligns with:
- The competitive positioning (what are incumbents charging?)
- The constraint reality (bootstrapped vs. funded)
- The long-term moat thesis (if data-as-moat, pricing should reflect data value)

Provide specific price points or ranges. Include a competitive comparison calculation showing first-year cost vs. primary incumbent. If the founder's own pricing thesis exists in workspace data, engage with it directly.

### Step 5: Founding Customer Program

Design the zero-to-first-customers program:
- **Offer structure**: free period, discount, commitments expected
- **Target profile**: who specifically (company size, vertical, signals)
- **Distribution channels**: where to find them (associations, communities, franchise networks — be specific)
- **Pitch framework**: not scripts (that's launch-plan), but the strategic layers of the pitch (what objections to preempt, what identity to signal, what aspiration to invoke)
- **Proof artifacts**: what to collect (testimonials, metrics, case study format)

### Step 6: Risk Register

Identify 4-7 risks with:
- **Risk**: what could go wrong
- **Severity**: high / medium / low
- **Mitigation**: specific countermeasure
- **Signal**: how you'd detect this risk materializing early

At least one risk must address the beachhead choice itself — what if it's wrong?

### Step 7: Confidence Assessment

For each major recommendation, flag:
- **Sourced**: backed by research evidence on disk
- **Inferred**: reasonable inference from available data
- **Assumption**: strategic judgment call — could be wrong

This is not a weakness. It's the most valuable part of the output. A strategy that knows what it doesn't know is more trustworthy than one that states everything with equal confidence.

### Step 8: Output

Write the strategy to `/home/claude/gtm_strategy_{target}.json`:

```json
{
  "target": "{target}",
  "market": "{market}",
  "constraints": "{constraints}",
  "generated_at": "ISO timestamp",
  "evidence_base": ["list of workspace files consumed"],
  "beachhead": {
    "selected": ["vertical(s)"],
    "scoring": [
      {
        "vertical": "...",
        "incumbent_density": {"score": 3, "evidence": "..."},
        "software_gap": {"score": 4, "evidence": "...", "verified": true},
        "product_fit": {"score": 5, "evidence": "..."},
        "distribution": {"score": 3, "evidence": "..."},
        "stickiness": {"score": 4, "evidence": "..."},
        "market_size": {"score": 3, "evidence": "...", "range": "$X-$Y"}
      }
    ],
    "rationale": "Why this beachhead, in 2-3 sentences"
  },
  "phases": [
    {
      "phase": 1,
      "name": "Beachhead",
      "timeline": "Months 1-6",
      "verticals": ["..."],
      "target_customers": "5-15",
      "proof_definition": "What success looks like",
      "phase_gate": "What must be true to proceed"
    }
  ],
  "pricing": {
    "model": "...",
    "tiers": [{"name": "...", "price": "...", "includes": "..."}],
    "competitive_comparison": "...",
    "alignment_with_thesis": "..."
  },
  "founding_program": {
    "offer": "...",
    "target_profile": "...",
    "channels": ["..."],
    "pitch_layers": ["identity", "risk_elimination", "aspiration"],
    "proof_artifacts": ["..."]
  },
  "risks": [
    {
      "risk": "...",
      "severity": "high|medium|low",
      "mitigation": "...",
      "early_signal": "..."
    }
  ],
  "confidence": [
    {"recommendation": "...", "level": "sourced|inferred|assumption", "note": "..."}
  ],
  "summary": "3-5 sentence executive summary of the strategy"
}
```

## Evidence Certification

If `certify_*.json` exists in the workspace, read the `appendix_for_formatter` section and embed it as an "Evidence & Confidence Assessment" appendix at the end of the document. Include the claim table, gaps disclosure, and methodology note as-is. Do not editorialize — present the certification exactly as produced.

## Delivery

After writing the strategy JSON to disk, **deliver as a formatted Word document (.docx)** using Anthropic's document skill. A GTM strategy is something a founder shares with co-founders, advisors, and investors. The JSON on disk is the evidence trail. The .docx is the deliverable. Both are required.

Present a concise narrative summary. Lead with the beachhead decision and why. Don't dump the JSON — tell the story of the strategy, noting where confidence is high and where it's an informed bet. End with what the `launch-plan` module will need to operationalize next.
