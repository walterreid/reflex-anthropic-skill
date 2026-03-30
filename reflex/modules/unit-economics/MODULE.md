# Unit Economics Module

Structure what is known (and not known) about a company's business model and unit economics.

- **Target**: {target}
- **Model type**: {model_type}
- **Research findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Read research findings from `{findings}`. Check for:
- `/home/claude/research_{target}.json`
- `/home/claude/websearch_{target}.json`
- `/home/claude/competitors_*.json` (for comparative benchmarks)

Public companies will have more data (SEC filings, earnings calls). Private companies require more inference. Flag everything accordingly.

### Step 2: Detect Business Model

If `{model_type}` is `auto`, determine the primary model from evidence:
- **SaaS**: recurring subscription revenue
- **Marketplace**: take rate on transactions between parties
- **E-commerce**: product sales with inventory/fulfillment
- **Fintech**: interchange, interest spread, or transaction fees
- **Hardware**: device sales with optional services layer
- **Advertising**: monetizing attention/data
- **Hybrid**: multiple revenue streams (identify primary and secondary)

### Step 3: Extract Unit Economics

Assess each metric below. For every metric, classify the data quality:
- **Reported**: directly from company disclosures, filings, or official statements
- **Estimated**: inferred from available data points with stated methodology
- **Unknown**: no reliable data — state explicitly, do not fabricate

**Revenue Metrics**
- Revenue (annual/quarterly, growth rate)
- Revenue per customer / ARPU / ACV
- Revenue mix (by product, segment, or geography if available)
- Net Revenue Retention (NRR) / Gross Revenue Retention

**Acquisition Metrics**
- Customer Acquisition Cost (CAC)
- CAC by channel if distinguishable
- Payback period (months to recover CAC)
- Sales efficiency (new ARR / S&M spend)

**Lifetime Value**
- LTV (or LTV estimate based on churn and ARPU)
- LTV:CAC ratio
- Gross margin-adjusted LTV

**Margin Structure**
- Gross margin (and what's included in COGS)
- Contribution margin (unit-level profitability)
- Operating margin
- Free cash flow margin (if public)

**Scale Indicators**
- Revenue per employee
- Burn rate / runway (if private and data available)
- Rule of 40 score (growth rate + profit margin)

### Step 4: Benchmark Context

Where possible, compare key ratios against:
- Industry medians for the model type
- Direct competitors if `/home/claude/competitors_*.json` exists
- Stage-appropriate benchmarks (seed vs. growth vs. scale)

Flag where the target is notably above or below benchmarks.

### Step 5: Identify Red Flags and Bright Spots

- **Red flags**: metrics that suggest unsustainable economics (e.g., LTV:CAC < 1, negative gross margin, accelerating burn with decelerating growth)
- **Bright spots**: metrics that suggest strong underlying economics (e.g., NRR > 120%, improving margins at scale, efficient CAC)

### Step 6: Output

Write to `/home/claude/unit_economics_{target}.json`:

```json
{
  "target": "{target}",
  "model_type": "saas|marketplace|ecommerce|fintech|hardware|advertising|hybrid",
  "generated_at": "ISO timestamp",
  "metrics": {
    "revenue": {
      "annual_revenue": {"value": "...", "quality": "reported|estimated|unknown"},
      "growth_rate": {"value": "...", "quality": "..."},
      "arpu": {"value": "...", "quality": "..."},
      "nrr": {"value": "...", "quality": "..."}
    },
    "acquisition": {
      "cac": {"value": "...", "quality": "..."},
      "payback_months": {"value": "...", "quality": "..."},
      "sales_efficiency": {"value": "...", "quality": "..."}
    },
    "ltv": {
      "ltv": {"value": "...", "quality": "..."},
      "ltv_cac_ratio": {"value": "...", "quality": "..."}
    },
    "margins": {
      "gross_margin": {"value": "...", "quality": "..."},
      "operating_margin": {"value": "...", "quality": "..."},
      "fcf_margin": {"value": "...", "quality": "..."}
    },
    "scale": {
      "revenue_per_employee": {"value": "...", "quality": "..."},
      "rule_of_40": {"value": "...", "quality": "..."}
    }
  },
  "benchmarks": [
    {"metric": "...", "target_value": "...", "benchmark_value": "...", "benchmark_source": "...", "assessment": "above|at|below"}
  ],
  "red_flags": ["..."],
  "bright_spots": ["..."],
  "data_coverage": {
    "reported": 4,
    "estimated": 6,
    "unknown": 5,
    "coverage_pct": 0.67
  }
}
```

Then present a concise narrative: what business model they run, the 2-3 most telling metrics, where the economics look strong or concerning, and what data gaps make the picture incomplete. Be explicit about what's sourced vs. estimated — this module's value is honesty about what we actually know.
