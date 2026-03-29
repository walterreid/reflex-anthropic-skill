# Match Module

Score a single candidate against multiple opportunities and produce a ranked fit matrix.

- **Candidate**: {candidate}
- **Opportunities**: {opportunities}
- **Lens**: {lens}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Load candidate data:
   - Check the workspace for files matching `{candidate}` (e.g., `extract_{candidate}.json`)
   - If the candidate is referenced in conversation context (e.g., an uploaded resume), use that
   - Extract: skills, experience, domain expertise, education, location, seniority level, and any unique differentiators

2. Load opportunity data:
   - Check the workspace for files matching `{opportunities}` (e.g., `jobs_{opportunities}.json`, `research_{opportunities}.json`)
   - Each opportunity should have: title, requirements, team, location, and a summary

3. For each opportunity, score the candidate on 5 dimensions (1-5 scale):
   - **Domain fit**: How well the candidate's expertise matches the role's core domain
   - **Technical fit**: Overlap between candidate's technical skills and role requirements
   - **Level fit**: Whether the candidate's seniority matches the role's expectations
   - **Location fit**: Whether the candidate can work where the role requires
   - **Differentiator fit**: Whether the candidate brings something distinctive beyond baseline requirements

4. Apply lens-specific weighting if `{lens}` is provided:
   - **career-change**: Weight domain and differentiator fit higher, level fit lower (career changers often shift levels)
   - **lateral**: Weight all dimensions equally
   - **stretch**: Weight technical and domain fit higher (candidate is reaching up)
   - **default**: Domain 5x, Technical 4x, Level 4x, Location 3x, Differentiator 3x

5. Calculate a weighted percentage for each opportunity. Rank from highest to lowest.

6. Write results to `/home/claude/match_{candidate}_vs_{opportunities}.json`:

```json
{
  "candidate": "{candidate}",
  "opportunities_source": "{opportunities}",
  "lens": "{lens}",
  "matched_at": "ISO timestamp",
  "rankings": [
    {
      "rank": 1,
      "title": "Role Title",
      "team": "Team Name",
      "location": "Location",
      "fit_percentage": 87.4,
      "scores": {
        "domain": 4,
        "technical": 3,
        "level": 4,
        "location": 5,
        "differentiator": 5
      },
      "top_strength": "One sentence on the strongest dimension",
      "top_gap": "One sentence on the weakest dimension",
      "url": "application URL"
    }
  ],
  "summary": "2-3 sentence synthesis of overall fit landscape"
}
```

## Output

A ranked fit matrix showing each opportunity with its fit percentage, top strength, and top gap. End with a clear recommendation: which 1-3 opportunities to pursue and why.
