# Test Dispatch Module

Run smoke tests against dispatch to verify routing, params, chains, resolvers, and conditionals all work correctly.

- **Scope**: {scope}

## Instructions

Run the test script at the same location as this MODULE.md:

```bash
python3 {MODULE_DIR}/test_runner.py {scope}
```

Where `{MODULE_DIR}` is the directory containing this file (i.e., the `test-dispatch` module folder).

The script will output results. Report them to the user as-is — do not interpret or summarize failures, just present the output. If all tests pass, confirm that. If any fail, show the failures.

## Output

The raw test results. No commentary needed beyond "all passed" or "N failures found."
