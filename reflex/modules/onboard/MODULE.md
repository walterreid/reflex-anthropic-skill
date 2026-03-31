# Onboard Module

Create a handoff document from accumulated findings. The `recap` dependency has summarized what was produced. This module restructures that into what a new person needs to *know and do* — not a history of the session, but a reference they'll come back to.

- **Target**: {target}
- **Audience**: {audience}
- **Depth**: {depth}
- **Session recap**: {session_recap}

## How This Differs from recap

`recap` answers "what happened?" — it's a session summary. `onboard` answers "what do I need to know?" — it's a reference document. A recap lists artifacts chronologically. An onboard document organizes knowledge by what the reader needs first.

## Instructions

### Step 1: Determine Reader's Starting Point

Based on `{audience}`, calibrate what to assume and what to explain:

- **New team member**: Assume domain knowledge, explain project-specific decisions and context
- **Contractor**: Assume technical skill, explain brand/voice/standards and what "good" looks like
- **AI system**: Explain everything — constraints, conventions, vocabulary, what's been tried, what to avoid. Be explicit about things a human would intuit
- **Executive**: Assume no time. Lead with decisions and status. Put details in appendix
- **Partner**: Assume different context. Explain your terminology, goals, and constraints

### Step 2: Structure the Handoff

Organize into sections (adjust depth per `{depth}`):

**1. Context** (What is this and why does it matter?)
- The project/domain in 2-3 sentences
- Why this work was done — the triggering question or goal
- Current status: where things stand right now

**2. Key Decisions** (What was decided and why?)
- The 3-5 most important decisions or conclusions from the work
- For each: the decision, the reasoning, and what alternatives were considered
- At `deep` depth: include the evidence that supported each decision

**3. Vocabulary & Conventions** (How do we talk about this?)
- Terms that have specific meaning in this context
- Naming conventions, categorizations, or frameworks that were established
- Things that sound similar but mean different things here

**4. What's Been Done** (Don't repeat this work)
- Summary of research, analysis, and artifacts produced
- Where to find them (file names, locations)
- What each artifact contains and when to reference it

**5. What's Next** (Pick up here)
- Open questions that haven't been answered
- Planned but unexecuted work
- Known risks or concerns flagged during the work

**6. Gotchas** (What I wish someone had told me)
- Non-obvious things that caused confusion or wasted time
- Assumptions that turned out to be wrong
- Things that look simple but aren't

### Step 3: Write to Disk

Write to `/home/claude/onboard_{target_slug}.md` as a readable markdown document (not JSON — this is meant to be read by humans or AI systems directly).

## Output

Present the handoff document in full. It should pass the "cold start test": could someone who has never seen this project read this document and start contributing the same day? If the answer is no, something is missing.
