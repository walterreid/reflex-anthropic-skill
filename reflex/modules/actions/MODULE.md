# Actions Module

Convert analysis findings into a prioritized action list.

- **Target**: {target}
- **Timeframe**: {timeframe}

## Available Workspace Data

{workspace}

## Instructions

1. Take the analysis from the previous step in the chain (or from `/home/claude/` files related to `{target}`).
2. For every finding, risk, opportunity, or recommendation in the analysis, derive a concrete action. An action is something a person can start doing this week — not a strategy, not a goal, not a hope.
3. For each action, provide:
   - **Action**: A verb-first imperative (e.g. "Schedule a call with..." not "Consider reaching out to...")
   - **Why**: Which specific finding or risk this addresses (1 sentence, linked to upstream evidence)
   - **Effort**: low (< 1 day), medium (1-5 days), high (1+ weeks)
   - **Impact**: low, medium, high
   - **Owner role**: Who should do this (e.g. "engineering lead", "CEO", "marketing team") — not a specific person
   - **Priority**: 1 (do first) through N, ordered by impact/effort ratio
4. Filter by `{timeframe}`:
   - **immediate**: Only actions that can start this week
   - **quarter**: Actions for the next 90 days
   - **strategic**: Longer-term moves that require planning
   - **all**: Everything, grouped by timeframe
5. Order by priority within each timeframe group.

## Output

A prioritized action list. Each action: imperative statement, rationale, effort, impact, owner, priority. End with a "start here" recommendation: the single highest-leverage action and why it should be first.
