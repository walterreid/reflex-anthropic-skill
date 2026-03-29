# Pitch Module

Structure findings as a persuasive narrative.

- **Target**: {target}
- **Audience**: {audience}
- **Ask**: {ask}

## Available Workspace Data

{workspace}

## Instructions

1. Take the analysis from the previous step in the chain (or from `/home/claude/` files related to `{target}`).
2. Restructure everything into the Situation-Complication-Resolution framework:
   - **Situation**: What's the current state? (1-2 sentences, establish shared reality with `{audience}`)
   - **Complication**: What's changing, what's at risk, or what's being missed? (2-3 sentences, create urgency from the findings)
   - **Resolution**: What should be done, and why is this the right approach? (2-3 sentences, lead to the ask)
   - **Ask**: State `{ask}` clearly — what you want the audience to do (1 sentence)
3. Tailor language to `{audience}`:
   - **investors**: ROI, market size, traction, defensibility. Numbers first.
   - **board**: Strategic alignment, risk management, resource allocation. Brevity.
   - **client**: Their pain, your solution, proof it works. Empathy first.
   - **team**: Vision, their role in it, what's changing and why. Inspiration.
   - **partner**: Mutual benefit, complementary strengths, shared opportunity. Collaboration.
4. Every claim must trace back to evidence from the upstream analysis. Persuasion without substance is manipulation — this module persuades with evidence.
5. Keep it to one page. A pitch that can't fit on one page isn't focused enough.

## Output

A one-page persuasive narrative. Situation, complication, resolution, ask. No headers labeled "Situation" etc. — the structure should be invisible, the narrative should flow. End with the ask as its own short paragraph.
