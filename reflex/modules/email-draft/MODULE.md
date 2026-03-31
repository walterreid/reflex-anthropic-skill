# Email Draft Module

Compress analysis into a send-ready email, rendered as an interactive draft using the message compose tool.

- **Target**: {target}
- **Recipient**: {recipient}
- **Tone**: {tone}
- **Variants**: {variants}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

### Step 1: Gather Source Material

Check for upstream data that should inform the email:
- `/home/claude/creative_brief_*.json` — positioning, taglines, messaging pillars
- `/home/claude/tagline_*.json` — recommended tagline and rationale
- `/home/claude/audience_*.json` — audience language patterns and triggers
- `/home/claude/research_*.json`, `/home/claude/websearch_*.json` — data points to reference
- `/home/claude/evaluate_*.json`, `/home/claude/positioning_*.json` — analysis to communicate
- Any other workspace files related to `{target}`

Also use any upstream chain context from `{findings}`.

### Step 2: Determine Email Strategy

Based on `{recipient}`, adapt the approach:

- **cold-list**: Hook in subject line, acknowledge the reader's world in the first sentence, thread in 1-2 data points naturally (not as a data dump), clear single CTA, close with brand voice. The reader owes you nothing — earn every sentence.
- **manager/ceo/investor**: Lead with the decision or action needed, support with 2-3 key findings, be concise. Respect their time.
- **client/partner**: Balance professionalism with warmth, focus on what matters to THEM not to you.
- **team**: Be direct, skip the formalities, focus on what's changed and what needs to happen next.
- **customer**: Match the brand voice from upstream creative brief if available. Be human.

### Step 3: Write the Email(s)

If `{variants}` is 1, write a single email. If 2-3, write multiple variants that represent **different strategic approaches**, not just different tones. For example:
- Variant 1: Lead with empathy (acknowledge their problem)
- Variant 2: Lead with proof (social proof, data, credibility)
- Variant 3: Lead with provocation (challenge an assumption)

Each variant label should be 2-4 words describing the strategic approach (e.g., "Lead with empathy", "Data-forward", "Challenge assumption").

For each email:
- **Subject line**: Specific, under 8 words, makes the reader curious or feel understood. Not clickbait.
- **Opening**: One sentence that earns the second sentence. For cold-list: acknowledge their world. For internal: state the point.
- **Body**: Maximum 3-4 short paragraphs. Thread in upstream research/data naturally — the reader should feel like this brand understands their world, not that they're reading a research summary. Use audience language patterns from upstream portrait if available.
- **CTA**: One clear action. Not three options. One.
- **Close**: Brand voice. If a tagline exists upstream, use it. If a secondary descriptor exists, layer it.

### Step 4: Adapt to Tone

- **formal**: Professional structure, measured language, no colloquialisms
- **direct**: Short sentences, no softening, clear and assertive
- **warm**: Conversational, friendly, acknowledges the human on the other end
- **bold**: Provocative, confident, slightly edgy — takes a stance
- **conversational**: Reads like a text from a smart friend, casual but substantive

### Step 5: Render with Message Compose Tool

**CRITICAL**: Use the `message_compose_v1` tool to render the email. This produces an interactive draft the user can open in their mail client.

Set `kind` to `"email"`. For each variant, provide:
- `label`: 2-4 word strategic label
- `subject`: The subject line
- `body`: The full email body

Set `summary_title` to a brief description of what the email is about.

### Step 6: Brief Confirmation

After rendering the email with the tool, provide a 1-2 sentence confirmation of what was produced and which upstream evidence was threaded in. Do not repeat the email content — the tool rendering is the deliverable.

## Output

An interactive email draft rendered via the `message_compose_v1` tool, followed by a brief confirmation. The email is the deliverable — keep post-commentary minimal.
