# Partnership Module

Capture, load, and evolve a working relationship profile — not voice or style, but how to think together.

- **Mode**: {mode}
- **Workspace**: {workspace}

## What This Is

This module preserves the things a great collaborator learns over time: what you value, how you want to be challenged, what "good" means to you, what makes you trust the output. These are lost every session. This module makes them portable.

This is not voice-dna (how you write). This is not audience-portrait (who you're writing for). This is the space between — how the work should feel when it's happening.

## Modes

### If mode is empty or "status"

Check if `/home/claude/partnership.json` exists.
- If yes: read it, summarize it in 3-5 sentences. Note when it was last updated and what sections have content.
- If no: explain what the module does and suggest `reflex partnership capture` to create the initial profile.

### If mode is "capture"

Read the full conversation history. Extract patterns about how this person works, thinks, and wants to be collaborated with. Look for:

**Thinking style**
- Do they want options or recommendations? Do they like being asked or being told?
- How do they handle ambiguity — do they want it resolved immediately or held open?
- Do they think in frameworks, narratives, examples, or data?
- How much do they want to see the work vs. just the output?

**Quality signals**
- What made them say "that was excellent" or "that's exactly right"? What specifically triggered approval?
- What made them push back or ask for changes? What specifically triggered dissatisfaction?
- What do they call "good"? Not generically — the specific things they've praised in this conversation.

**Challenge preferences**
- How hard do they want to be pushed? Do they want devil's advocate or just honest opinion?
- Do they want you to flag when you're uncertain, or just make a call?
- How do they respond to being told they're wrong?

**Collaboration shape**
- Do they lead or do they want to be led? Does it shift depending on domain?
- Do they want to build together interactively, or hand off and receive?
- How do they signal when something is important vs. exploratory?
- What's their relationship with nuance — do they want it preserved or resolved?

**Meta-patterns**
- What's their relationship with their own system/product/project?
- What are they trying to get better at?
- What do they value that they might not say explicitly?

Write the profile to `/home/claude/partnership.json`:

```json
{
  "type": "partnership",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "version": 1,
  "profile": {
    "thinking_style": {
      "options_vs_recommendations": "...",
      "ambiguity_tolerance": "...",
      "reasoning_mode": "...",
      "process_visibility": "..."
    },
    "quality_signals": {
      "what_earns_approval": ["specific examples from conversation"],
      "what_triggers_pushback": ["specific examples from conversation"],
      "definition_of_good": "..."
    },
    "challenge_preferences": {
      "intensity": "...",
      "uncertainty_handling": "...",
      "response_to_disagreement": "..."
    },
    "collaboration_shape": {
      "lead_or_follow": "...",
      "interactive_vs_handoff": "...",
      "importance_signals": "...",
      "nuance_relationship": "..."
    },
    "meta_patterns": {
      "relationship_to_project": "...",
      "growth_edges": "...",
      "implicit_values": ["..."]
    }
  },
  "evidence": [
    {
      "pattern": "short description of observed pattern",
      "moment": "what happened in conversation that revealed this",
      "confidence": "high|medium|inferred"
    }
  ]
}
```

After writing, present the file for download using the present_files tool so the user can save it. Then summarize the profile in a few sentences — not a data dump, but the way you'd describe a colleague to someone about to work with them for the first time.

### If mode is "load"

Check for `/home/claude/partnership.json` in the workspace. If not found, check `/mnt/user-data/uploads/` for any file matching `partnership*.json`.

If found: read it, internalize the profile, and confirm in 2-3 sentences what you've loaded. Then apply it — don't just acknowledge it. The profile should shape how you respond for the rest of the conversation. Be specific about what you'll do differently: "I'll lead with recommendations instead of options. I'll flag uncertainty but make a call. I'll preserve nuance rather than resolving it."

If not found: tell the user no profile exists and suggest `reflex partnership capture` or uploading a previously saved profile.

### If mode is "update"

Read the existing `/home/claude/partnership.json`. Read the current conversation. Look for:

- New patterns not in the existing profile
- Existing patterns that should be revised based on new evidence
- Patterns in the profile that were contradicted by behavior in this conversation

Update the profile in place. Increment the version number. Update `updated_at`. Add new evidence entries. If revising an existing pattern, keep the old version in an `evolution` array so the history is visible.

Present the updated file for download. Summarize what changed and why in 2-3 sentences.

## Output

Depends on mode:
- **status**: Brief summary of current profile state
- **capture**: Full profile written to disk, presented for download, summarized conversationally
- **load**: Profile internalized, specific behavioral commitments stated
- **update**: Profile revised, changes summarized, presented for download