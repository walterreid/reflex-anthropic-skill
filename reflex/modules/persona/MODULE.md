# Persona Module

Evaluate findings from the perspective of a specific stakeholder, simulating their reaction, priorities, concerns, and likely questions.

- **Target**: {target}
- **Role**: {role}
- **Tone**: {tone}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. **Gather the findings.** Scan the workspace for files matching `{target}`: research, compare, evaluate, grade, scenario, distill, or filter JSONs. Read them. Also use any upstream context from `{findings}`. If no upstream data is found, respond with an error — persona needs something to react to.

2. **Establish the persona.** Based on `{role}`, define:
   - **What they care about most** — their primary objectives and success metrics (e.g., a CFO cares about ROI, cash flow, risk exposure; a developer cares about DX, maintainability, performance)
   - **What they're skeptical of** — their common objections and trust barriers
   - **What they'd ask first** — the questions this person would lead with
   - **Their decision style** — data-driven, consensus-seeking, intuition-led, risk-averse, etc.

3. **React to each major finding.** For every key claim or dimension in the upstream data, assess through the persona's lens:
   - **Reaction**: Would they find this compelling, concerning, irrelevant, or incomplete?
   - **Weight**: How much would this factor into their decision? (high/medium/low)
   - **Follow-up**: What question would they ask next about this finding?

4. **Synthesize the persona's overall position:**
   - **Verdict**: Given everything, what would this person likely decide or recommend?
   - **Champions**: Which findings would they use to advocate for action?
   - **Objections**: Which findings would make them push back or hesitate?
   - **Blind spots**: What does this persona typically underweight or miss?
   - **Persuasion strategy**: What framing or evidence would be most effective in getting this persona on board?

5. **Adjust voice based on `{tone}`:**
   - **analytical**: Third-person assessment of how the persona would react
   - **voice**: First-person — write as if the persona is speaking directly ("As your CFO, here's what concerns me...")
   - **brief**: Bullet-point summary of reactions only, no narrative

6. **Write to disk** at `/home/claude/persona_{target}_{role_slug}.json`:

```json
{
  "target": "{target}",
  "role": "{role}",
  "tone": "{tone}",
  "generated_at": "ISO timestamp",
  "persona_profile": {
    "priorities": ["..."],
    "skepticisms": ["..."],
    "decision_style": "..."
  },
  "reactions": [
    {
      "finding": "The upstream finding",
      "reaction": "compelling|concerning|irrelevant|incomplete",
      "weight": "high|medium|low",
      "follow_up_question": "What they'd ask next"
    }
  ],
  "synthesis": {
    "verdict": "What they'd likely decide",
    "champions": ["Findings they'd advocate with"],
    "objections": ["Findings that give them pause"],
    "blind_spots": ["What they'd underweight"],
    "persuasion_strategy": "How to bring them on board"
  }
}
```

7. **Present conversationally.** Lead with the persona's verdict, then their top 2-3 objections and what would persuade them. Keep it to 8-12 lines.

## Output

A stakeholder reaction assessment grounded in upstream evidence. The file on disk is designed for downstream consumption by `email` (write a message that addresses this persona's concerns), `pitch` (structure an argument tailored to this persona), `actions` (extract next steps that account for this persona's objections), or run multiple personas in sequence to map the full decision landscape. Keep the conversational summary to 8-12 lines.
