# Web Search Module

Research a target using web search and produce structured findings.

- **Target**: {target}
- **Focus**: {focus}

## Instructions

1. Use `web_search` and `web_fetch` to research `{target}`. Conduct 3-6 searches to build a comprehensive picture.
2. Focus your research through the lens of `{focus}`:
   - **general**: Broad overview — what is it, what does it do, who uses it, recent news
   - **competitive**: Market position, competitors, differentiators, pricing
   - **swot**: Strengths, weaknesses, opportunities, threats — gather raw evidence for each
   - **technical**: Tech stack, architecture, integrations, developer experience
3. Write your structured findings to `/home/claude/research_{target}.json` using this format:

```json
{
  "target": "{target}",
  "focus": "{focus}",
  "searched_at": "ISO timestamp",
  "sources": ["url1", "url2"],
  "findings": [
    {
      "category": "string",
      "point": "one-sentence finding",
      "evidence": "supporting detail from sources",
      "source": "url"
    }
  ],
  "summary": "2-3 sentence synthesis"
}
```

4. After writing the file, output a brief confirmation listing how many findings you gathered and the key themes.

## Output

A brief confirmation of what was found and where it was saved. The real output is the JSON file on disk — downstream modules will read it.
