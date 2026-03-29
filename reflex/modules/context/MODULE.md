# Context Module

Gather and structure content from the current conversation as findings.

- **Target**: {target}
- **Scope**: {scope}

## Instructions

1. Read through the conversation history available in your context window.
2. Focus on content related to `{target}` — this could be a topic discussed, a product mentioned, code that was pasted, notes shared, decisions made, or any subject the conversation has touched.
3. Scope your gathering with `{scope}`:
   - **last**: Only the most recent user message or content block
   - **recent**: The last 3-5 exchanges
   - **full**: Everything in the conversation
4. Extract structured findings from the conversation content. Look for:
   - Claims, assertions, or decisions that were made
   - Code, configurations, or technical content that was shared
   - Questions that were raised (answered or not)
   - Data, metrics, or evidence that was mentioned
   - Opinions, preferences, or constraints expressed
5. Write findings to `/home/claude/context_{target}.json` using this format:

```json
{
  "target": "{target}",
  "scope": "{scope}",
  "extracted_at": "ISO timestamp",
  "source_type": "conversation",
  "findings": [
    {
      "category": "claim/code/question/data/preference",
      "point": "one-sentence finding",
      "evidence": "what was actually said or shared",
      "speaker": "user or assistant"
    }
  ],
  "summary": "2-3 sentence synthesis of the conversation's key content related to target"
}
```

6. Output a brief confirmation of what you gathered and the key themes found.

## Output

Brief confirmation of what was extracted from the conversation. The structured data is on disk for downstream modules. Do not repeat the full conversation — just confirm what you found and its structure.
