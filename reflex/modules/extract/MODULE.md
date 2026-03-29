# Extract Module

Read an uploaded file and produce structured findings in the standard format.

- **Target**: {target}
- **Focus**: {focus}

## Instructions

1. Look for the file referenced by `{target}` — check `/mnt/user-data/uploads/` for uploaded files. If `{target}` is a filename, read it. If it's a description, find the best match.
2. Read the file using the appropriate method (view for text, bash for PDFs/spreadsheets).
3. Extract findings through the lens of `{focus}`:
   - **general**: Key facts, claims, data points, and conclusions from the document
   - **swot**: Evidence for strengths, weaknesses, opportunities, threats
   - **competitive**: Market claims, positioning, differentiators mentioned
   - **technical**: Architecture, tools, methodologies, technical decisions
   - **financial**: Numbers, metrics, projections, costs, revenue data
4. Write structured findings to `/home/claude/extract_{target}.json` using this format:

```json
{
  "target": "{target}",
  "focus": "{focus}",
  "extracted_at": "ISO timestamp",
  "source_type": "pdf/docx/csv/txt/code",
  "findings": [
    {
      "category": "string",
      "point": "one-sentence finding",
      "evidence": "supporting detail or quote from document",
      "location": "page number or section if available"
    }
  ],
  "summary": "2-3 sentence synthesis of the document's key content"
}
```

5. Output a brief confirmation of what was extracted and key themes found.

## Output

Brief confirmation of extraction results. The structured data is on disk for downstream modules.
