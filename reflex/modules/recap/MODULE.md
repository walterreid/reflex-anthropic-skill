# Recap Module

Compress the current workspace into something a human can absorb in 30 seconds. Not an audit (that's `debrief`), not a status check (that's `status`) — a summary of what was found, concluded, and recommended.

- **Target**: {target}
- **Length**: {length}

## Available Workspace Data

{workspace}

## Instructions

1. Read all workspace artifacts. If `{target}` is not "all", filter to files containing `{target}` in their filename or target field.

2. For each artifact, extract the conclusion — not the methodology, not the evidence, just the bottom line:
   - Research files → what was the most important finding?
   - Rubric files → what dimensions were weighted highest and why?
   - Evaluation files → who won, by how much, on what dimensions?
   - Whitepaper/report files → what was the argument in its tightest form?
   - Distill files → what categories had the most evidence weight?
   - Comparison files → what was the key differentiator?

3. Apply `{length}`:
   - **oneliner**: The entire session's work in one sentence. Ruthlessly compress. If forced to pick one takeaway, what is it?
   - **short**: 3-4 sentences covering the key findings, the verdict (if any), and the most important implication. This is what you'd paste into Slack.
   - **full**: One paragraph per artifact in pipeline order. Each paragraph states what the artifact found and why it matters. This is what you'd read aloud in a standup.

4. End with a single "next step" recommendation — what should the user do with these findings? Be specific: name a module, a chain, or an action.

## Output

The recap, conversationally. Do not write to disk — this is a terminal output meant to be read, not stored. Keep it clean and tight. No headers for `oneliner` or `short`. Headers only for `full`.
