# Moat Module

Evaluate the defensibility of a company's competitive position across established moat categories.

- **Target**: {target}
- **Format**: {format}
- **Research findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Read research findings from `{findings}`. Check for:
- `/home/claude/research_{target}.json`
- `/home/claude/websearch_{target}.json`
- `/home/claude/competitors_*.json` (competitor profiles provide contrast)
- `/home/claude/swot_{target}.json` (strengths map directly to moat sources)

### Step 2: Evaluate Each Moat Category

Assess the target across these seven moat types. For each, determine if it is **Strong**, **Emerging**, **Weak**, or **Absent**, with evidence:

**1. Network Effects**
Does the product become more valuable as more people use it? Direct (user-to-user) or indirect (platform/marketplace)? How far along the adoption curve?

**2. Switching Costs**
How painful is it to leave? Consider data lock-in, workflow integration, retraining costs, contractual obligations, migration complexity.

**3. Scale Economies**
Does unit cost decrease meaningfully with scale? Consider infrastructure, R&D amortization, go-to-market efficiency, purchasing power.

**4. Brand & Trust**
Is the brand a decision shortcut for buyers? Consider category association, trust premium, word-of-mouth, NPS signals, employer brand.

**5. Data Advantages**
Does the company accumulate proprietary data that improves the product or creates insights competitors can't replicate? Consider feedback loops, training data, behavioral data, benchmarking datasets.

**6. Regulatory / Legal Capture**
Are there licenses, certifications, patents, compliance requirements, or government relationships that create barriers? Consider regulatory moats vs. regulatory risks.

**7. Cost Advantages / Efficiency**
Structural cost advantages from proprietary technology, process innovation, geographic positioning, or vertical integration that competitors can't easily match.

### Step 3: Assess Overall Defensibility

- Count strong moats vs. weak/absent
- Identify the **primary moat** (the single strongest source of defensibility)
- Identify the **moat at risk** (the one most likely to erode in 24 months and why)
- Rate overall defensibility: **Fortress** (3+ strong) / **Defended** (1-2 strong) / **Exposed** (0 strong)

### Step 4: Output

Write to `/home/claude/moat_{target}.json`:

```json
{
  "target": "{target}",
  "generated_at": "ISO timestamp",
  "moats": [
    {
      "category": "Network Effects",
      "rating": "Strong|Emerging|Weak|Absent",
      "evidence": ["..."],
      "details": "One sentence explaining the rating"
    }
  ],
  "overall": {
    "defensibility": "Fortress|Defended|Exposed",
    "primary_moat": "...",
    "moat_at_risk": "...",
    "risk_reason": "...",
    "strong_count": 3,
    "weak_or_absent_count": 4
  }
}
```

**Format output based on `{format}`:**

- **scorecard**: Table with each moat category, rating (with emoji: 🟢 Strong, 🟡 Emerging, 🔴 Weak, ⚫ Absent), and a one-line summary. End with overall defensibility rating and a 2-sentence strategic takeaway.
- **narrative**: Flowing prose organized by moat strength (strongest first). End with a paragraph on durability — which moats are deepening and which are eroding.
