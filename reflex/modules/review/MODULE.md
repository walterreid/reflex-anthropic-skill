# Review Module

Review and critique any content — code, documents, designs, or processes.

- **Target**: {target}
- **Type**: {type}
- **Style**: {style}

## Instructions

1. Identify the content to review. Check in order:
   - Chain context from a previous step (context, extract, or websearch output)
   - Files in `/home/claude/` related to `{target}`
   - Content visible in the conversation (pasted code, shared text, uploaded files)
2. Apply the review lens based on `{type}`:
   - **code**: Treat content as source code. Look at logic, patterns, naming, error handling.
   - **document**: Treat content as a written document. Look at clarity, structure, completeness, accuracy.
   - **design**: Treat content as a system or product design. Look at architecture, scalability, user experience, trade-offs.
   - **process**: Treat content as a workflow or procedure. Look at efficiency, bottlenecks, failure modes, missing steps.
   - **strategy**: Treat content as a plan or proposal. Look at assumptions, feasibility, risks, alignment with goals.
3. Apply the review approach from `{style}`:
   - **thorough**: Full review — logic, edge cases, naming, structure, performance, readability. Leave no stone unturned.
   - **quick**: Bugs, errors, and critical issues only. Skip style and best-practice concerns.
   - **security**: Injection, auth issues, data exposure, input validation, cryptographic misuse. (Most relevant for code type.)
   - **architecture**: Structure, separation of concerns, scalability, maintainability, coupling. Big-picture view.
   - **readability**: Naming, documentation, clarity, cognitive load, consistency. How easy is this to understand?

## Output

One-line summary, then findings by severity (critical, warning, suggestion). Every finding states what's wrong and how to fix it. End with a "top 3 improvements" prioritized by impact. Ground every finding in specific evidence from the content.
