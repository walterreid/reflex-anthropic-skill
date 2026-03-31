# LinkedIn

Convert analysis, findings, or a story into a LinkedIn-ready post or article with platform-native formatting.

- **Target**: {target}
- **Tone**: {tone}
- **Length**: {length}
- **Hook**: {hook}

## Instructions

1. **Gather source material.** Check the conversation context for upstream findings (from chained modules like `research`, `swot`, `challenge`, `distill`, etc.). If upstream data exists, use it as the evidence base. If not, work from `{target}` directly using your own knowledge.

2. **Pre-commit — name your weakness.** Before writing, consider the available evaluation lenses:

{lenses}

LinkedIn rewards provocation and concision — which lens would most likely find a problem? Name where you'll play it safe when you shouldn't, or compress past something that needed space. Write it to the `lens_concern` field in your output JSON.

3. **Extract the core insight.** Every good LinkedIn post orbits a single non-obvious takeaway. Find it. It should be something the reader didn't expect, challenges a common assumption, or reframes a familiar topic. If the source material has multiple insights, pick the one with the most tension — the one that makes someone stop scrolling.

4. **Craft the hook.** If `{hook}` is not "auto", use it as the opening. Otherwise, write an opening line that creates a gap — a counterintuitive claim, a surprising number, a question that implies the reader's assumption is wrong. The hook must work in the LinkedIn feed preview (first ~2 lines visible before "...see more").

   Hook patterns that work:
   - Contrarian opener: "Most people think X. They're wrong."
   - Surprising stat: "87% of Y do Z. Here's why that matters."
   - Personal story entry: "Three years ago, I made a mistake that..."
   - Direct challenge: "Stop doing X. Here's what to do instead."

5. **Write the body.** Follow LinkedIn's native format conventions:

   **If length is "post" (~150-300 words):**
   - Short paragraphs — 1-2 sentences max per paragraph
   - Line breaks between every paragraph (LinkedIn collapses dense text)
   - Personal-to-universal arc: start with a specific experience or observation, zoom out to the principle
   - End with a clear takeaway or call to action
   - 3-5 relevant hashtags at the bottom
   - No headers, no bullet lists (these feel corporate on LinkedIn)

   **If length is "article" (~800-1500 words):**
   - A compelling title (separate from the hook)
   - Section headers that read as mini-hooks themselves
   - Mix of short paragraphs and slightly longer ones for depth
   - Evidence and examples woven throughout — reference the source material
   - A "so what" conclusion that gives the reader something actionable
   - 3-5 hashtags at the end

6. **Apply the tone:**
   - **professional** — authoritative but approachable, first-person, shares expertise without lecturing
   - **conversational** — casual, uses "you" and "we", feels like talking to a colleague over coffee
   - **provocative** — takes a strong stance, challenges orthodoxy, invites debate (but stays substantive, not clickbait)
   - **storytelling** — narrative-driven, uses scene-setting and dialogue, draws the lesson from the story

7. **Self-edit.** LinkedIn rewards concision. Cut every sentence that doesn't earn its place. Remove hedge words ("I think", "perhaps", "it seems like"). Replace jargon with plain language. Read the hook again — would *you* click "see more"?

8. **Write metadata** to `/home/claude/linkedin_{target_slug}.json`:

```json
{
  "type": "linkedin",
  "target": "{target}",
  "tone": "{tone}",
  "length": "{length}",
  "generated_at": "ISO timestamp",
  "lens_concern": {
    "lens": "the lens name",
    "prediction": "specific prediction — where you played it safe or compressed past something"
  }
}
```

9. **Present the post.** Output the final post as plain text, ready to copy-paste into LinkedIn. Do NOT write to a file — LinkedIn content is conversational output. After the post, add a brief note (2-3 sentences) explaining the angle you chose and why, so the user can request adjustments.

## Output

The LinkedIn post or article as plain text in the conversation, formatted exactly as it would appear on LinkedIn (short paragraphs, line breaks, hashtags). Not written to disk — this is a final deliverable meant to be copied directly.

After the post, briefly note the angle and any alternative approaches the user might want (e.g., "I went with the contrarian hook — I could also frame this as a personal story if you'd prefer").