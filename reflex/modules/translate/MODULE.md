# Translate Module

Take an internal document — a profile, an analysis, a portfolio of work, a self-assessment — and produce the version that an external audience needs to receive. Not a summary. Not a reframe. A translation across the gap between how you see yourself and how someone else needs to see you in order to act.

This is not `reframe`. Reframe preserves evidence and changes emphasis for a different reader. Translate solves a harder problem: the source material was written at one resolution and the audience operates at a different one. The information loss in that gap isn't just about vocabulary or structure — it's about what the source material *assumes the reader already knows* about why any of this matters.

- **Source**: {source}
- **Audience**: {audience}
- **Channel**: {channel}
- **Intent**: {intent}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## The Core Problem This Module Solves

Most internal documents fail externally not because they're wrong, but because they're *complete from the inside*. The author sees the connections, the transfer function, the "why this matters." The reader sees a list of things that happened. The gap isn't quality — it's legibility.

Translation means:
1. Identifying what the source material *proves* but doesn't *say*
2. Identifying what the audience needs to hear before they can understand why any of it matters
3. Building the bridge — not dumbing down, but supplying the missing context that makes the internal resolution accessible at the external bandwidth

## Instructions

### Step 1: Load the Source Material

Find the content to translate. Priority order:
1. Upstream chain context (`{findings}`) — output from a previous chain step
2. Uploaded files or conversation attachments matching `{source}`
3. Workspace files matching `{source}` — check `/home/claude/` for relevant JSON, markdown, or other artifacts
4. Content visible in the conversation

You need the actual content, not a description of it. If nothing is found, say so and suggest what to provide.

### Step 2: Read the Source Through the Audience's Eyes

Before touching a word, answer these five questions about the source material:

**What does it assume the reader already knows?**
Every document has load-bearing context that the author doesn't state because it's obvious to them. A resume assumes the reader knows what "product management" means in practice. A research paper assumes familiarity with the field. A partnership profile assumes the reader knows why any of this is worth reading. Identify the unstated prerequisites.

**What does it prove that it doesn't claim?**
The evidence trail often implies more than the author states. Five roles across four industries doesn't just mean "diverse experience" — it proves the ability to transfer mental models across domains. A vulnerability with 100% reproduction rate doesn't just mean "found a bug" — it proves systematic adversarial methodology. Name what the evidence proves but the document never says aloud.

**What's the transfer function?**
Why does thing A lead to thing B? If the source material lists accomplishments chronologically, the reader sees a timeline. If the translation shows the *pattern* — each role deepened a specific capability that the next role required — the reader sees trajectory. Find the thread.

**What decision does the audience need to make?**
A hiring manager needs to decide: interview or not. An investor needs to decide: take the meeting or not. A partner needs to decide: engage or not. Every audience has a binary gate they're trying to resolve. The translation should supply what that gate requires.

**What's the first thing they'll wonder — and does the source answer it?**
The audience's first question is rarely the author's first point. A hiring manager looking at an AI safety resume wonders "can this person actually do the work?" not "what's their career history?" A client looking at a portfolio wonders "have they solved a problem like mine?" If the source buries the answer to the audience's first question, the translation moves it forward.

### Step 3: Identify the Translation Type

Based on `{channel}` and `{audience}`, determine what you're producing:

**resume** — For ATS, hiring managers (HM), or AI screening. The source is likely a career history, portfolio, or profile. The translation must survive three reads: machine parsing (keywords, section headers, parseable structure), human scanning (6-second skim — does the top third answer "should I keep reading?"), and AI evaluation (semantic coherence, evidence of impact, career narrative). Produce a .docx with ATS-safe formatting (single column, standard fonts, standard section headings, no tables-as-layout, no graphics). Lead with what the evidence proves, not what happened chronologically.

**cover-letter** — For a specific role at a specific company. The source is likely a resume, profile, or research portfolio. The translation answers one question: "why should we interview this person for *this* role?" Not a summary of the resume — a targeted argument connecting specific evidence to specific requirements. Three paragraphs max. First paragraph: the single most legible credential for this role. Second: the transfer function — how your background produces the specific capability they need. Third: the ask.

**portfolio** — For showcasing work to a broad audience. The source is likely a collection of projects, research, or artifacts. The translation creates a narrative spine: what connects these pieces, what capability they collectively demonstrate, what problem the portfolio-holder is equipped to solve that others aren't. Each project gets: what it is (1 sentence), what it proves (1 sentence), why it matters to the viewer (1 sentence).

**pitch** — For someone who can give you what you need (job, funding, partnership). The source is likely analysis, research, or a profile. The translation is a Situation-Complication-Resolution compressed to the audience's attention span. If `{audience}` is a hiring manager: Situation = what the company needs, Complication = why it's hard to find, Resolution = here's why this person solves it. Evidence-backed, not aspirational.

**brief** — A short-form executive summary for stakeholders. Source can be anything. Translation compresses to: what this is, why it matters now, what to do about it. One page max.

**profile** — For a professional bio, LinkedIn summary, or "about" page. The source is likely a resume or partnership profile. The translation shifts from accomplishment-listing to identity-articulation: not "what I did" but "what I do and why it matters." Written in the person's voice if a voice profile exists in the workspace.

**auto** — Infer the best channel from the source material and audience. State your choice and why.

### Step 4: Build the Translation

Write the output document. Follow these principles:

**Lead with what the audience's gate requires.** If they need to decide "interview or not," the first thing they read should be the single strongest piece of evidence that the answer is yes.

**State the transfer function explicitly.** Don't make the reader infer why A leads to B. Say it: "Seven years building trust architectures in payments taught me how trust breaks at scale. That's why I found the vulnerability that Google classified P2/S2 — I was looking at AI summarization the way I look at payment flows: where does the system assume trust that hasn't been verified?"

**Translate resolution, don't reduce it.** The goal isn't to simplify — it's to supply context. If the source operates at a resolution the audience doesn't share, add the bridging context rather than dropping the nuance. "Designed segmented onboarding by business type" becomes "Designed onboarding that recognized different businesses need different entry points — a sole proprietor signing up shouldn't face the same flow as a franchise with 50 locations. This reduced partner integration time by 75%."

**Every claim should be traceable.** If the translation makes a claim the source doesn't support, flag it. If the translation drops a claim the source includes, it should be because the audience doesn't need it — not because it was inconvenient.

**Preserve what makes the person distinctive.** Generic translations are worse than no translation. If the source reveals something unusual — an adversarial thinker who's also a product builder, a systems designer who reasons through metaphor, a researcher who ships — that distinctiveness IS the value proposition. Don't sand it off.

### Step 5: Self-Assessment

Before delivering, run this checklist:

- [ ] Does the first sentence answer the audience's first question?
- [ ] Is the transfer function stated, not implied?
- [ ] Would the person recognize themselves in this, or has the translation become someone else?
- [ ] Does it survive the 6-second skim? (First third of the document should carry the core argument)
- [ ] Is every claim traceable to the source material?
- [ ] Does it supply the missing context, or does it assume the same prerequisites as the source?

### Step 6: Write to Disk

If the output is a document (resume, cover letter, portfolio), produce the actual file — not just text. Use the appropriate format:
- Resume → .docx (ATS-safe)
- Cover letter → .docx or conversational
- Portfolio, profile, brief → .md or conversational

Write metadata to `/home/claude/translate_{source_slug}_{channel}.json`:

```json
{
  "type": "translate",
  "source": "{source}",
  "audience": "{audience}",
  "channel": "{channel}",
  "intent": "{intent}",
  "generated_at": "ISO timestamp",
  "translation_decisions": {
    "assumed_knowledge_supplied": ["What context was added that the source assumed"],
    "unstated_proofs_surfaced": ["What the evidence proves that the source didn't say"],
    "transfer_function": "The thread connecting the source material",
    "audience_gate": "The decision the audience needs to make",
    "first_question_answered": "What the audience wonders first and where the answer now lives"
  },
  "lens_concern": {
    "lens": "which perspective lens would most likely find a problem",
    "prediction": "what specific weakness the lens would surface"
  }
}
```

## Output

The translated document — clean, complete, ready to use. Not revision notes. Not a comparison with the original. The actual deliverable the audience will see.

After the document, a brief (3-5 sentence) translation note explaining:
- What the biggest gap was between source and audience
- What the translation supplied to bridge it
- What was lost in translation (there's always something — name it honestly)

## Composition Patterns

This module works well at these points in a chain:

- `reflex extract+translate source:resume channel:cover-letter audience:hiring-manager` — Extract key patterns from a resume, then translate for a specific application
- `reflex partnership+translate channel:profile audience:recruiter` — Load a partnership profile and translate it into a professional bio
- `reflex websearch+translate target:company channel:cover-letter audience:hiring-manager` — Research a company, then translate your credentials for their specific context
- `reflex review+translate target:resume channel:resume audience:ats` — Review a resume for issues, then produce the translated/optimized version
- Standalone: `reflex translate source:resume channel:resume audience:hiring-manager` — Translate a resume directly
