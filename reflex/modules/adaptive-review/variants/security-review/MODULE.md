# Security Review

Security-focused audit of code handling sensitive operations.

- **Language**: {language}

## Instructions

Audit for:
1. Injection vulnerabilities (SQL, command, XSS, template)
2. Authentication and authorization flaws
3. Data exposure (logs, error messages, API responses)
4. Input validation gaps
5. Cryptographic misuse (weak hashing, hardcoded secrets, predictable tokens)
6. Dependency and supply-chain concerns

## Output

Findings by severity: CRITICAL (exploitable now), HIGH (exploitable with effort), MEDIUM (defense-in-depth gap), LOW (best practice). Each finding: what's wrong, how to exploit it, how to fix it.
