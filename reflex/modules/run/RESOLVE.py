#!/usr/bin/env python3
"""
Resolver for the run module.

Checks for an existing run_plan.json in the workspace:
  - If intent is "reset" → reset variant
  - If run_plan.json exists with pending steps → continue variant
  - If no plan exists → start variant (plan dependency ran upstream)
"""

import json
import sys
from pathlib import Path

PLAN_FILE = Path("/home/claude/run_plan.json")


def resolve(params: dict) -> tuple:
    intent = params.get("intent", "").strip().lower()

    # Explicit reset command
    if intent == "reset":
        return ("reset", "User requested plan reset")

    # Check for existing run plan
    if PLAN_FILE.exists():
        try:
            plan = json.loads(PLAN_FILE.read_text())
            steps = plan.get("steps", [])
            pending = [s for s in steps if s.get("status") == "pending"]
            completed = [s for s in steps if s.get("status") == "complete"]

            if not pending:
                return ("reset", "All steps complete — run is finished")

            if intent == "skip":
                return ("continue", f"Skipping step {len(completed) + 1} — {len(pending)} steps remaining")

            return ("continue", f"Resuming run — step {len(completed) + 1} of {len(steps)}")

        except (json.JSONDecodeError, IOError):
            return ("start", "Found corrupted run_plan.json — starting fresh")

    # No existing plan — plan dependency should have run upstream
    return ("start", "No active run — plan decomposition complete, beginning execution")


def main():
    if len(sys.argv) < 2:
        print("ERROR: No params provided")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    variant, reason = resolve(params)
    print(f"{variant}|{reason}")


if __name__ == "__main__":
    main()
