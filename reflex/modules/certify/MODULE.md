# Certify Module

Scan workspace evidence and produce a structured certification that downstream formatters embed in the final deliverable.

- **Target**: {target}
- **Scope**: {scope}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

This module does one thing: it reads every piece of evidence in the workspace and produces a structured assessment of what's proven, what's inferred, and what's assumed. It runs *before* a formatter module so the formatter can embed the certification as an appendix.

This is not an audit of writing quality. It's an audit of **epistemic honesty** — does the evidence support what the deliverable will claim?

### Step 1: Inventory the Evidence Base

Read all workspace files matching `{scope}` (or all if "all"). For each file, catalog:
- **Filename and type** (research, extract, competitors, positioning, gtm_strategy, etc.)
- **Generated timestamp** — when was this evidence collected?
- **Source URLs** — extract every URL cited in the file
- **Key claims** — the major findings or data points the file contains

Build a master list of all evidence available. This is the foundation everything else is checked against.

### Step 2: Extract Key Claims

From the workspace data, identify the **10-20 most consequential claims** — the ones that a deliverable would build strategic recommendations on. These typically include:

- Market size estimates
- Competitive landscape assertions (especially negative claims like "no software exists")
- Customer counts, revenue figures, growth rates
- Pricing data (competitor pricing, recommended pricing)
- ICP definitions and behavioral claims
- Channel recommendations and their rationale
- Beachhead or vertical selection rationale

For each claim, record:
- The claim itself (one sentence)
- Which workspace file contains it
- What source URL backs it (if any)

### Step 3: Classify Confidence

For each key claim, assign a confidence level:

**Sourced** — The claim traces to a specific URL or document that was fetched and read. The source is credible (SEC filings, company press releases, industry reports, official documentation, reputable review sites). The claim accurately represents what the source says.

**Cross-verified** — Multiple independent sources support the claim. This is stronger than single-sourced. Note which sources agree.

**Inferred** — The claim is a reasonable inference from available data but isn't directly stated in any source. Example: "operators aged 35-55" inferred from industry demographics but not specifically researched.

**Assumption** — The claim is a strategic judgment call with no direct evidence. It may be reasonable but could be wrong. Example: "pricing at $349/month will be accepted by the market" when no willingness-to-pay data exists.

**Unverified** — The claim was stated but never checked against any source. This is the most dangerous category. Example: "no software exists for this vertical" when nobody searched for "[vertical] software."

**Contradicted** — Evidence in the workspace actually contradicts this claim, or multiple sources give conflicting data. Flag what conflicts and which source is more credible.

### Step 4: Identify Gaps

Look for what's *missing* from the evidence base:

- **Claims without sources** — consequential claims that have no URL or research backing
- **Negative claims without verification** — "no competitor exists," "no software serves this market," "nobody is doing X." These require affirmative search to validate and are the most common source of strategic error.
- **Single-source dependencies** — claims where the entire strategic direction rests on one source. What if that source is wrong?
- **Stale evidence** — research that may have been accurate when collected but could have changed (competitive landscape, pricing, market conditions)
- **Missing perspectives** — customer voice, pricing validation, channel feasibility data that wasn't gathered

### Step 5: Check for Contradictions

Compare claims across workspace files:
- Do two research files give different market size estimates? Note the range.
- Does competitive analysis in one file contradict assessments in another?
- Do confidence levels assigned by upstream modules (like `audit`) conflict with what the evidence actually shows?

### Step 6: Produce the Certification

Write to `/home/claude/certify_{target}.json`:

```json
{
  "target": "{target}",
  "certified_at": "ISO timestamp",
  "evidence_inventory": [
    {
      "file": "filename.json",
      "type": "research|extract|competitors|positioning|gtm_strategy|etc",
      "generated_at": "timestamp",
      "source_urls": ["..."],
      "key_claims_count": 5
    }
  ],
  "claim_map": [
    {
      "claim": "One-sentence claim",
      "confidence": "sourced|cross-verified|inferred|assumption|unverified|contradicted",
      "source_file": "filename.json",
      "source_url": "URL or null",
      "note": "Any qualification, conflict, or context"
    }
  ],
  "confidence_summary": {
    "sourced": 8,
    "cross_verified": 2,
    "inferred": 4,
    "assumption": 3,
    "unverified": 1,
    "contradicted": 0,
    "total_claims": 18
  },
  "gaps": [
    {
      "gap": "Description of what's missing",
      "impact": "high|medium|low",
      "recommendation": "What would close this gap"
    }
  ],
  "contradictions": [
    {
      "claim": "The contested claim",
      "source_a": "File/source saying X",
      "source_b": "File/source saying Y",
      "assessment": "Which is more credible and why"
    }
  ],
  "overall_certification": {
    "evidence_strength": "strong|moderate|weak",
    "highest_risk_claims": ["The 1-3 claims that carry the most strategic weight with the least evidence"],
    "ready_for_publication": true,
    "caveats": "Any overarching concerns about the evidence base"
  },
  "appendix_for_formatter": {
    "title": "Evidence & Confidence Assessment",
    "introduction": "This document was produced from [X] research artifacts containing [Y] sourced claims. The following table maps key assertions to their evidence basis.",
    "claim_table": [
      {
        "claim": "...",
        "confidence": "...",
        "source": "URL or description"
      }
    ],
    "gaps_disclosure": "This analysis does not include: [list of gaps]. These represent areas where additional research would strengthen the recommendations.",
    "methodology": "Claims are classified as sourced (traced to a specific, credible source), inferred (reasonable conclusion from available data), or assumption (strategic judgment without direct evidence). Cross-verified claims have multiple independent sources. Unverified claims were stated but not checked."
  }
}
```

The `appendix_for_formatter` section is specifically structured for downstream formatter modules to embed directly into a document. It includes:
- A human-readable introduction
- A claim-to-source table
- A gaps disclosure
- A methodology note explaining the confidence levels

### Step 7: Output

Present a brief narrative summary:
- How many claims, what's the confidence distribution
- The 2-3 highest-risk claims (most strategic weight, least evidence)
- Any contradictions found
- Whether the evidence base is strong enough to support a deliverable

Do NOT dump the full JSON. The structured data is on disk for the formatter. The narrative should help the user decide: is this ready to ship, or does it need more research first?

## How Formatters Use This

When a formatter module (report, whitepaper, pitch, onboard) finds a `certify_*.json` in the workspace, it should:

1. Read the `appendix_for_formatter` section
2. Add an "Evidence & Confidence Assessment" section at the end of the document
3. Include the claim table, gaps disclosure, and methodology note
4. Do NOT editorialize — present the certification as-is

This means the chain `certify+report` produces a report with a built-in evidence appendix. The chain `websearch+gtm-strategy+certify+report` produces a fully researched, strategically assessed, evidence-certified deliverable.

The certification travels with the document. When someone drops the docx into another AI and asks "is this good?", the evaluator has the evidence structure to work with instead of evaluating prose on vibes.