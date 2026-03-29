# Job Search Module

Search for open positions at a specific company and produce structured job listings.

- **Company**: {company}
- **Role filter**: {role_filter}
- **Location**: {location}

## Instructions

1. Use `web_search` and `web_fetch` to find the official careers page for `{company}`.
2. Fetch the full careers page and extract all open roles. If `{role_filter}` is provided, filter to roles matching that keyword or domain (e.g., "product management", "safety", "engineering"). If `{location}` is provided, further filter to roles available in that location.
3. For each matching role, extract:
   - **title**: The exact job title
   - **team**: The team or department (e.g., "Safeguards", "Engineering & Design - Product")
   - **location**: Where the role is based
   - **url**: Direct application link
   - **requirements**: Key qualifications mentioned (experience level, skills, background)
   - **summary**: 1-2 sentence description of the role's focus
4. Write structured findings to `/home/claude/jobs_{company}.json`:

```json
{
  "company": "{company}",
  "searched_at": "ISO timestamp",
  "role_filter": "{role_filter}",
  "location_filter": "{location}",
  "source_url": "careers page URL",
  "total_open_roles": 0,
  "matched_roles": [
    {
      "title": "string",
      "team": "string",
      "location": "string",
      "url": "string",
      "requirements": ["string"],
      "summary": "string"
    }
  ]
}
```

5. Output a brief confirmation of how many roles were found and the key teams represented.

## Output

Brief confirmation of search results. The structured job listings are on disk for downstream modules (evaluate, match, grade).
