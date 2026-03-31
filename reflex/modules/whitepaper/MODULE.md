# Whitepaper Module

Format findings as a long-form whitepaper that preserves the full evidence chain from research through analysis to conclusion.

- **Domain**: {domain}
- **Depth**: {depth}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Gather all upstream findings from `{findings}`. Also review the workspace data above to identify all structured JSON files related to `{domain}` — research files, distill files, comparison files, rubric files, evaluation files. Read all of them. The whitepaper should synthesize everything available, not just the most recent step's output.
2. **Pre-commit — name your weakness.** Before writing, consider the available evaluation lenses:

{lenses}

Which lens would most likely find a problem in what you're about to produce? Name it specifically. A whitepaper is long — be precise about which section and which analytical choice you're least confident in. Write it to the `lens_concern` field in your output JSON.

3. Structure the whitepaper with these sections:

   **Title**: A specific, descriptive title — not "Whitepaper on {domain}" but something that captures the argument (e.g. "Convention Over Configuration: How Reflex's Composition Grammar Addresses the Skill Chaining Gap").

   **Abstract**: 3-4 sentences. The question, the approach, the key finding. A reader should know whether to continue after this paragraph.

   **Methodology**: How the evidence was gathered. What was searched, what was compared, what framework was applied. If a rubric was used, name the dimensions and weights. If web research was conducted, note the sources and their recency. This section is what makes the whitepaper auditable — a reader should be able to trace any later claim back through this section to its origin.

   **Landscape / Background**: What the current state of affairs looks like. Present the research findings here with attribution. Every claim should be traceable to a specific source or finding from the upstream data. Do not generalize — be specific about what was found and where.

   **Analysis**: This is where interpretation lives. Apply whatever analytical framework was used upstream (SWOT, rubric evaluation, competitive comparison) and present the results in detail. Show scores if they exist. Show the reasoning behind qualitative judgments. If two things were compared, present the comparison dimension by dimension, not as a summary.

   **Implications**: What the analysis means. This section bridges findings and recommendations. What should an observer understand? What changes if this analysis is correct? What changes if it's wrong?

   **Conclusion**: The argument in its tightest form. 2-3 paragraphs. No new evidence — only synthesis of what was already presented.

4. Apply `{depth}`:
   - **standard**: 8-12 paragraphs total. Each section gets 1-2 paragraphs. Prioritize analysis and implications.
   - **comprehensive**: 15-20 paragraphs. Each section gets 2-4 paragraphs. Landscape and analysis sections expand significantly with more evidence detail.

5. Write the whitepaper to `/home/claude/whitepaper_{domain}.md`.

6. Write metadata to `/home/claude/whitepaper_{domain}.json`:

```json
{
  "type": "whitepaper",
  "domain": "{domain}",
  "depth": "{depth}",
  "generated_at": "ISO timestamp",
  "lens_concern": {
    "lens": "the lens name",
    "prediction": "specific prediction — which section, which analytical choice you're least confident in"
  }
}
```

## Evidence Chain Rules

- Every claim in the analysis must connect to a specific finding in the landscape section.
- Every finding in the landscape section must connect to a source named in the methodology.
- If a claim cannot be traced back through this chain, cut it.
- If upstream data contains scores, percentages, or metrics, include them — do not round or approximate.

## Output

The complete whitepaper as a polished document. Write it to disk and present the key argument in 2-3 sentences as confirmation. This is a deliverable, not conversation.
