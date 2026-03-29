# Quick Review

Fast scan of the code for bugs and logical errors only.

- **Language**: {language}

## Instructions

Focus exclusively on:
1. Bugs that would cause runtime errors
2. Logical errors that produce wrong results
3. Obvious performance traps (infinite loops, O(n²) where O(n) is trivial)

Skip style, naming, and readability. This is a triage pass.

## Output

If clean: "No critical issues found."
If issues: Numbered list, each with the problem and a one-line fix.
