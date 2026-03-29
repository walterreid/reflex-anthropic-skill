# Reframe Module

Take existing findings or analysis and reshape them for a different audience. The evidence doesn't change — the emphasis, vocabulary, structure, and implied action do.

- **Target**: {target}
- **Audience**: {audience}
- **Purpose**: {purpose}

## Available Workspace Data

{workspace}

## Instructions

1. Locate the richest artifact for `{target}` in the workspace. Priority order: whitepaper > evaluation > research > comparison > distill. Read the best available source.

2. Identify the core argument — the 2-3 claims that everything else supports. These survive the reframe intact.

3. Reshape for `{audience}` with `{purpose}` in mind:

   **executive** — Lead with the decision to be made. State the recommendation first, then the 2-3 supporting points. No methodology unless it affects confidence. Numbers matter more than process. If purpose is "decide", end with a clear recommended action and what it costs to wait.

   **engineer** — Lead with the architecture. Technical specifics are welcome — name the components, the patterns, the tradeoffs. Show how things work, not just what they conclude. If purpose is "build", end with implementation priorities and known constraints.

   **investor** — Lead with the market opportunity or risk. Frame everything in terms of value creation, competitive position, and timing. Quantify where possible. If purpose is "fund", end with what the investment enables and what comparable outcomes look like.

   **non-technical** — Lead with the "so what." Use analogies for technical concepts. Avoid jargon entirely — if a term needs explaining, replace it with a plain description. If purpose is "understand", end with the one thing they should remember.

   **regulator** — Lead with compliance implications. Frame in terms of risk, precedent, and standards. Cite specific frameworks or requirements where relevant. If purpose is "approve", end with what conditions are met and what gaps remain.

   **academic** — Lead with the research question. Frame as contribution to existing literature. Note methodology limitations explicitly. If purpose is "understand", end with open questions and suggested further research.

4. Preserve evidence fidelity. You may change emphasis, order, vocabulary, and structure. You may not add claims, remove contradicting evidence, or change numbers. If the original analysis had caveats, they must survive in some form even if abbreviated.

## Output

The reframed content, written as a polished standalone piece that the target audience can read without needing the original. State the audience and purpose at the top, then deliver. Do not write to disk unless the output exceeds 500 words — short reframes are conversational, long ones should be saved to `/home/claude/reframe_{target}_{audience}.md`.
