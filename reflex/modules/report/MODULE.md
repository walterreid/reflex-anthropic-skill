# Write Report Module

Write a structured report based on research findings.

- **Topic**: {topic}
- **Format**: {format}
- **Research findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Use the research findings in `{findings}` as your factual basis. Do not invent beyond them.

2. **Pre-commit — name your weakness.** Before writing, consider the available evaluation lenses:

{lenses}

Which lens would most likely find a problem in what you're about to produce? Name it specifically. Write it to the `lens_concern` field in your output JSON.

3. Format:
   - **brief**: Executive summary. 2-3 paragraphs, no headers.
   - **full**: Structured report with introduction, findings, analysis, conclusion.
   - **memo**: Internal memo with TO/FROM/RE/DATE fields, then concise body.

4. Write the report to `/home/claude/report_{topic_slug}.json`:

```json
{
  "type": "report",
  "topic": "{topic}",
  "format": "{format}",
  "generated_at": "ISO timestamp",
  "lens_concern": {
    "lens": "the lens name",
    "prediction": "specific prediction about where this output is weakest"
  }
}
```

## Delivery

After writing the report content and JSON to disk, **deliver the document using Anthropic's document skill** (docx, pptx, or the appropriate format tool). The module's job isn't done when the JSON is saved — it's done when the user has a professional document they can download or share.

- **brief** or **memo** format → deliver as a Word document (.docx)
- **full** format → deliver as a Word document (.docx) with proper headings, sections, and formatting

The structured JSON on disk is the evidence trail. The delivered document is the work product. Both are required.

## Output

The report delivered as a formatted document. The user should receive a downloadable file, not just text in the chat.
