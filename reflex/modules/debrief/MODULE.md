# Debrief Module

Audit the information fidelity of work produced in this session. Track what evidence entered the pipeline, what survived into the final output, what was lost, and what was invented.

- **Target**: {target}
- **Scope**: {scope}
- **Upstream findings**: {findings}

## Available Workspace Data

{workspace}

## Instructions

1. Review the workspace data above. Identify all artifacts related to `{target}`. Read every JSON and markdown file that matches. These represent the pipeline stages.
2. Also read any upstream context from `{findings}` passed by the chain.
3. Based on `{scope}`:

### If scope is "chain"

Trace the information flow across pipeline stages:

**Stage inventory**: List every file produced, in order of creation. For each: filename, what module likely produced it, how many distinct findings/claims it contains.

**Evidence tracking**: Take the 5-8 strongest findings from the earliest stage (the source). For each one, trace it forward:
- Was it present in the analysis stage? (verbatim, paraphrased, or absent)
- Was it present in the final output? (verbatim, paraphrased, or absent)
- If absent: at which stage did it drop out?

**Invention check**: Identify any claims in the final output that cannot be traced back to any upstream source file. These are either Claude's general knowledge additions or hallucinations. List each with a confidence assessment: justified addition (Claude's knowledge is likely reliable here) vs. unsupported claim (no evidence trail, uncertain reliability).

**Fidelity score**: What percentage of source-stage findings survived to the final output? What percentage of final-output claims can be traced to source evidence?

### If scope is "output"

Evaluate the final deliverable only:

**Completeness**: Does the output address the original intent? What's missing?
**Internal consistency**: Do claims in the output contradict each other?
**Evidence density**: What ratio of claims are supported by cited evidence vs. asserted without support?
**Actionability**: Could a reader act on this output without needing to ask clarifying questions?

4. End with a **process recommendation**: one specific change that would improve the pipeline's information fidelity for this type of work. Be concrete — name the module, the step, or the convention that should change.

## Output

A structured audit. Not a grade — a diagnostic. The goal is to make the next pipeline run better, not to judge this one. Keep it factual: what survived, what didn't, what appeared from nowhere, and what one thing would improve the process.
