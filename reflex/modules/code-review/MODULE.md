# Code Review Module

Review the user's code with the following context:

- **Language**: {language}
- **Review style**: {style}

## Instructions

1. Apply language-specific idioms and best practices for `{language}`.
2. Apply the review approach from `{style}`:
   - **thorough**: Logic, edge cases, naming, structure, performance, readability
   - **quick**: Bugs and logical errors only
   - **security**: Injection, auth issues, data exposure, input validation

## Output

One-line summary, then findings by severity (critical, warning, suggestion). Every finding says what to fix.
