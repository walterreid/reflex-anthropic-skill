# Transcript Module

Structure extracted meeting data into an actionable meeting record with clear ownership and follow-up tracking.

- **Target**: {target}
- **Format**: {format}
- **Extracted data**: {extracted}

## Instructions

The `extract` dependency has already pulled raw data from the transcript. Your job is to structure it into a meeting record that someone who wasn't in the room could act on.

### Step 1: Organize into Sections

From the extracted data, build:

- **Decisions Made**: What was decided, by whom, with what authority (explicit vote, consensus, executive call). Flag any decisions that seemed assumed but not explicitly confirmed.
- **Action Items**: Each with owner, deadline (if stated), and dependency (blocked by what). If no owner was named, flag it as unassigned.
- **Open Questions**: Unresolved items that need follow-up. Note who raised them and whether a follow-up was promised.
- **Key Discussion Points**: The 3-5 most substantive topics discussed, with the range of positions expressed. Not a transcript summary — just the tensions and conclusions.
- **Missed Opportunities**: Moments where a question should have been asked, a decision should have been made, or a topic was dropped without resolution. This section is what makes this module more than a summary.

### Step 2: Tag Sentiment and Dynamics

For each major discussion point, note:
- **Alignment**: Was the group aligned, split, or did one person drive the conclusion?
- **Energy**: Was there genuine engagement or was this a rubber-stamp?
- **Risk signals**: Any moment where someone raised a concern that was acknowledged but not addressed

### Step 3: Write to Disk

Write to `/home/claude/transcript_{target_slug}.json`:

```json
{
  "type": "transcript_analysis",
  "target": "{target}",
  "generated_at": "ISO timestamp",
  "decisions": [
    {"decision": "...", "owner": "...", "authority": "explicit|consensus|assumed", "confidence": "high|medium|low"}
  ],
  "action_items": [
    {"action": "...", "owner": "...|unassigned", "deadline": "...|unstated", "blocked_by": "...|none"}
  ],
  "open_questions": [
    {"question": "...", "raised_by": "...", "followup_promised": true}
  ],
  "discussion_points": [
    {"topic": "...", "positions": "...", "conclusion": "...", "alignment": "aligned|split|driven", "energy": "high|low"}
  ],
  "missed_opportunities": ["..."],
  "risk_signals": ["..."]
}
```

## Output

If `{format}` is `structured`: present the JSON structure above with brief commentary.
If `{format}` is `narrative`: present as a readable meeting summary with sections, leading with decisions and actions, ending with missed opportunities and risks. The narrative should be useful to someone who needs to catch up in 2 minutes.
