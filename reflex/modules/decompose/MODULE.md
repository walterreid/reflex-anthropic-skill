# Decompose Module

Break a complex question into researchable sub-questions, each tagged with the best module and params to answer it.

- **Question**: {question}
- **Depth**: {depth}
- **Available modules**: {registry}

## Instructions

1. Read the question: `{question}`
2. Identify the implicit sub-questions. A complex question usually contains multiple independent dimensions that could each be researched separately. Look for:
   - **Comparison axes** — "Is X better than Y?" contains sub-questions per evaluation criterion
   - **Causal chains** — "Why did X happen?" contains sub-questions about each contributing factor
   - **Stakeholder perspectives** — "Should we do X?" contains sub-questions per affected party
   - **Temporal layers** — "What will happen with X?" contains sub-questions about current state, trends, and projections
   - **Definitional prerequisites** — "How does X compare to Y for Z?" requires first establishing what X and Y are before comparing

3. For each sub-question, determine:
   - A clear, specific, searchable formulation
   - Which module from the registry would best answer it (e.g., `research`, `websearch`, `compare`, `extract`)
   - What params that module would need
   - Whether the sub-question depends on another sub-question's answer (ordering)
   - A priority: **critical** (answer changes the conclusion), **supporting** (strengthens the argument), or **contextual** (nice to have)

4. Based on `{depth}`:
   - **quick**: 2-4 sub-questions, only critical ones
   - **standard**: 4-6 sub-questions, critical and supporting
   - **detailed**: 5-10 sub-questions, full decomposition including contextual

5. Write the decomposition to `/home/claude/decompose_{target}.json`:

```json
{
  "original_question": "{question}",
  "target": "short-slug",
  "decomposed_at": "ISO timestamp",
  "sub_questions": [
    {
      "id": "sq1",
      "question": "The specific sub-question",
      "priority": "critical|supporting|contextual",
      "suggested_module": "research",
      "suggested_params": {"topic": "...", "depth": "..."},
      "depends_on": [],
      "rationale": "Why this sub-question matters to the overall answer"
    }
  ],
  "suggested_execution": {
    "parallel": ["sq1", "sq2"],
    "sequential": [["sq3", "sq4"]],
    "merge_strategy": "How to combine the sub-answers into a final answer"
  },
  "coverage_note": "What aspects of the original question this decomposition covers and any deliberate omissions"
}
```

6. After writing the file, present the decomposition clearly: list each sub-question with its priority, suggested module, and dependencies. End with the suggested execution strategy.

## Output

A structured decomposition with sub-questions tagged for downstream execution. The file on disk is designed to be consumed by `plan` (to build a chain), `run` (to execute step-by-step), or a human (to selectively run individual sub-questions). Keep the conversational summary to 8-12 lines.
