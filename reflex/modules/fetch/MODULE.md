# Fetch

Fetch a URL and produce a structured summary of its content, writing findings to disk for downstream modules.

- **URL**: {url}
- **Focus**: {focus}
- **Depth**: {depth}

## Instructions

1. **Fetch the URL.** Use the `web_fetch` tool to retrieve the content at `{url}`. If the fetch fails (404, blocked, timeout), tell the user clearly and stop — do not guess at the content.

2. **Identify the content type.** Assess what kind of page this is:
   - **News article** — who, what, when, where, why
   - **Blog post / essay** — thesis, supporting arguments, conclusion
   - **Documentation** — key concepts, usage patterns, important caveats
   - **Product / landing page** — what it does, who it's for, pricing, differentiators
   - **Research paper** — abstract, methodology, key findings, implications
   - **Other** — adapt to whatever structure the content has

3. **Extract and summarize.** Respect copyright — paraphrase everything, never reproduce more than a few words verbatim.

   **If focus is not "auto"**, prioritize content related to `{focus}` and downweight everything else. The summary should be oriented around the focus area.

   **If depth is "summary":**
   - Title and source
   - 1-2 sentence overview
   - 3-5 key points, each one sentence
   - One "so what" takeaway

   **If depth is "detailed":**
   - Title, source, author (if identifiable), date (if available)
   - 2-3 sentence overview
   - All major points with supporting evidence (paraphrased)
   - Notable claims or data points
   - What's missing or left unsaid
   - 2-3 sentence assessment of quality/reliability

4. **Write findings to disk** at `/home/claude/fetch_{slug}.json` where `{slug}` is derived from the URL's domain and path (e.g., `fetch_nytimes-ai-regulation.json`). Structure:

```json
{
  "type": "fetch",
  "url": "{url}",
  "title": "Page title",
  "source": "Domain or publication name",
  "author": "Author if available, null otherwise",
  "date": "Publication date if available, null otherwise",
  "content_type": "article|blog|docs|product|paper|other",
  "focus": "{focus}",
  "summary": "1-2 sentence overview",
  "key_points": [
    "Point 1",
    "Point 2"
  ],
  "notable_data": ["Any specific numbers, stats, or claims worth preserving"],
  "takeaway": "The single most important thing from this page",
  "reliability_note": "Brief assessment of source quality"
}
```

5. **Respond conversationally.** Present the summary in the conversation — lead with the takeaway, then the key points. Keep it scannable. Mention that findings have been saved for downstream use.

## Output

A conversational summary in the chat, plus structured JSON written to disk. The summary should feel like a knowledgeable colleague telling you "here's what that page says" — concise, opinionated about what matters, and honest about limitations.

The JSON on disk enables chaining: `reflex fetch+swot`, `reflex fetch+actions`, `reflex fetch+linkedin`, etc.