# Email Draft Module

Compress analysis into a send-ready email.

- **Target**: {target}
- **Recipient**: {recipient}
- **Tone**: {tone}

## Instructions

1. Take the analysis from the previous step in the chain (or from `/home/claude/` files related to `{target}`).
2. Compress into an email that `{recipient}` can read in under 2 minutes.
3. Structure:
   - **Subject line**: Specific, actionable, under 8 words. Not "Re: Analysis" — something like "Three risks in the vendor contract" or "Recommendation: switch to Tool B."
   - **Opening line**: Why you're writing, in one sentence. No "I hope this finds you well."
   - **Body**: The essential findings. Maximum 3 paragraphs. If the upstream analysis had 10 points, pick the 3 that matter most for this recipient. Link claims to evidence but don't include the full evidence chain.
   - **Close**: What you need from them — a decision, a meeting, approval, or just awareness. One sentence.
4. Adapt to `{tone}`:
   - **formal**: Professional, structured, slightly distant. For external or upward communication.
   - **direct**: Clear, concise, no softening. For peers or when urgency matters.
   - **warm**: Friendly but still professional. For team communication or delivering difficult news gently.
5. Strip all analytical framework language. Nobody wants to receive an email that says "per the SWOT analysis" or "the risk register indicates." Translate findings into natural business language.

## Output

A complete email with subject line, body, and closing. Ready to paste into an email client. No meta-commentary — just the email.
