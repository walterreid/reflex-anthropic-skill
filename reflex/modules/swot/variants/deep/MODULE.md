# SWOT Deep Analysis Module

Principal-level strategic SWOT/TOWS analysis with evidence gating, confidence scoring, and a ranked recommendation.

- **Target**: {target}
- **Industry**: {industry}
- **Format**: {format}
- **Research findings**: {findings}
- **Horizon**: 24 months

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Evidence

Read research findings from `{findings}`. Check for:
- `/home/claude/research_{target}.json`
- `/home/claude/websearch_{target}.json`
- Any `compare_*.json` or `distill_*.json` files referencing the target

If no upstream research exists, state clearly that findings are limited to general knowledge and flag confidence accordingly.

### Step 2: Build the SWOT (Quality-Gated)

Categorize every finding into exactly one quadrant:

- **Strengths**: Internal positives — competitive advantages, strong metrics, positive reputation, defensible moats
- **Weaknesses**: Internal negatives — gaps, complaints, limitations, technical debt, poor reviews, talent issues
- **Opportunities**: External positives — market trends to exploit, partnerships, underserved segments, emerging tech, regulatory tailwinds
- **Threats**: External negatives — competitors gaining ground, regulation, market shifts, disruption risks, macro headwinds

**Quality Gates (enforce strictly):**

1. **Completeness gate**: ≥4 distinct factors per quadrant. If any quadrant has fewer than 4, you must either dig deeper into findings or mark the analysis as INCOMPLETE.
2. **Evidence ratio gate**: ≥70% of all factors must include at least one source reference from the research findings. Count them.
3. **Assumption handling**: If no credible source exists for a factor, mark it `[DATA_NOT_FOUND]` and record it as an assumption with a basis. Set its confidence at −0.3 relative to cited factors.
4. **No unsourced claims**: Do not make numeric or competitor claims without a source. If unsure, do not invent.

For each factor, assign:
- **confidence**: 0.0–1.0 (1.0 = multiple corroborating sources; 0.5 = single source; 0.2 = assumption)
- **evidence**: list of source references from the research data

### Step 3: Generate TOWS Initiatives

Cross-reference quadrants to produce strategic initiatives:

| TOWS | Formula | Question |
|------|---------|----------|
| **SO** | Strength + Opportunity | How can strengths exploit opportunities? |
| **WO** | Weakness + Opportunity | How can opportunities help overcome weaknesses? |
| **ST** | Strength + Threat | How can strengths counter threats? |
| **WT** | Weakness + Threat | How to minimize weaknesses and avoid threats? |

For each initiative, score:
- **impact**: 0–10 (potential value if executed)
- **feasibility**: 0–10 (realistic given current capabilities)
- **risk**: 0–10 (what could go wrong)
- **priority**: calculated as `(impact × feasibility) / (1 + risk)`

Include a 1-line justification per initiative.

### Step 4: Select Top Recommendation

The initiative with the highest priority score wins. If tied, prefer higher feasibility. Link back to the specific SWOT factors that support it.

### Step 5: Check Gates and Output

Count factors per quadrant and evidence ratio. If either gate fails:
- Return an INCOMPLETE status explaining what's missing
- List what additional research would be needed
- Suggest assumptions that could fill gaps (with explicit basis)

If gates pass, produce the full output.

## Output

### Part A: Structured JSON

Write to `/home/claude/swot_{target}.json`:

```json
{
  "target": "{target}",
  "industry": "{industry}",
  "horizon": "24 months",
  "generated_at": "ISO timestamp",
  "gates": {
    "completeness": { "passed": true, "factors_per_quadrant": {"S": 5, "W": 4, "O": 6, "T": 4} },
    "evidence_ratio": { "passed": true, "ratio": 0.78, "cited": 15, "total": 19 }
  },
  "swot": {
    "strengths": [{"factor": "...", "confidence": 0.8, "evidence": ["..."]}],
    "weaknesses": [{"factor": "...", "confidence": 0.8, "evidence": ["..."]}],
    "opportunities": [{"factor": "...", "confidence": 0.8, "evidence": ["..."]}],
    "threats": [{"factor": "...", "confidence": 0.8, "evidence": ["..."]}]
  },
  "tows": {
    "SO": [{"strategy": "...", "impact": 8, "feasibility": 7, "risk": 3, "priority": 4.0, "justification": "..."}],
    "WO": [],
    "ST": [],
    "WT": []
  },
  "top_recommendation": {
    "strategy": "...",
    "why": "...",
    "priority": 4.6,
    "linked_factors": ["verbatim factor strings from SWOT"]
  },
  "assumptions": [{"key": "...", "value": "...", "basis": "..."}],
  "sources": [{"source": "...", "type": "Report/News/Filing", "date": "YYYY-MM", "key_point": "...", "url": "..."}]
}
```

### Part B: Executive Narrative

After the JSON is written, produce a ≤200-word executive narrative in board-ready tone:
- Lead with the top recommendation
- Include one quantified proof point
- Summarize the strategic position
- Note key assumptions or evidence gaps

### Failure Output

If either quality gate fails, write to `/home/claude/swot_{target}.json`:

```json
{
  "status": "INCOMPLETE",
  "target": "{target}",
  "missing": { "quadrants_below_4": ["..."] },
  "evidence_ratio": { "ratio": 0.55, "cited": 11, "total": 20 },
  "needed_sources": ["..."],
  "suggested_assumptions": [{"key": "...", "basis": "..."}]
}
```

And explain to the user what's missing, what additional research (`/reflex websearch` or `/reflex research`) would help, and whether the analysis can proceed with explicit assumptions.
