# Full Analysis

Complete end-to-end analysis: research → distill → rubric → evaluate → whitepaper. The dependency chain has already run websearch, distill, rubric, and evaluate. This module produces the final whitepaper synthesis.

- **Target**: {target}
- **Target2**: {target2}
- **Domain**: {domain}
- **Depth**: {depth}
- **Research**: {research}
- **Distilled findings**: {distilled}
- **Rubric**: {rubric}
- **Evaluation**: {evaluation}

## Instructions

1. All upstream steps have already run. The workspace contains:
   - Research findings from websearch
   - Distilled category weights from distill
   - A rubric with weighted dimensions from rubric
   - Scored evaluations from evaluate

2. Read all upstream artifacts from `/home/claude/`. Synthesize everything into a comprehensive whitepaper following the structure below.

3. Structure:

   **Title**: Specific and descriptive — captures the argument, not just the topic.

   **Abstract**: 3-4 sentences. The question, the approach, the key finding.

   **Methodology**: How evidence was gathered. Name the sources, the rubric dimensions and weights, and the evaluation approach. This section makes the whitepaper auditable.

   **Landscape / Background**: Present the research findings with attribution. Use the distilled category weights to prioritize — categories with more evidence get more space. Every claim should be traceable to a source.

   **Analysis**: Apply the rubric evaluation results. Show scores dimension by dimension. Show reasoning behind qualitative judgments. If comparative, present the comparison dimension by dimension with gaps highlighted.

   **Implications**: What the analysis means. What should change if this analysis is correct? What's the risk if it's wrong?

   **Conclusion**: The argument at its tightest. 2-3 paragraphs. No new evidence.

4. Depth `{depth}`:
   - **standard**: 8-12 paragraphs total.
   - **comprehensive**: 15-20 paragraphs. Landscape and analysis sections expand significantly.

5. Write the whitepaper to `/home/claude/whitepaper_{domain}.md`.

## Evidence Chain Rules

- Every claim in analysis must connect to a finding in landscape.
- Every finding in landscape must connect to a source in methodology.
- If a claim can't be traced back, cut it.
- If upstream data contains scores, percentages, or metrics, preserve them exactly.

## Output

The complete whitepaper as a polished document. Write it to disk and present the key argument in 2-3 sentences as confirmation.
