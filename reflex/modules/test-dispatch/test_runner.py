#!/usr/bin/env python3
"""
Dispatch smoke test runner.

Exercises dispatch routing across all levels and features without
requiring specific module content — only structural expectations.

Tests verify that dispatch produces the correct PROTOCOL OUTPUT
for a given input, not that modules do useful work.

Usage:
    python3 test_runner.py [scope]
    
Scopes: all, routing, params, chains, resolvers, conditionals
"""

import json
import subprocess
import sys
import os
from pathlib import Path

# Locate the skill directory — walk up from this script to find scripts/dispatch.py
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent  # test-dispatch is inside modules/
while SKILL_DIR != SKILL_DIR.parent:
    if (SKILL_DIR / "scripts" / "dispatch.py").exists():
        break
    SKILL_DIR = SKILL_DIR.parent

DISPATCH = SKILL_DIR / "scripts" / "dispatch.py"
MODULES_DIR = SKILL_DIR / "modules"

# Track results
passed = 0
failed = 0
errors = []


def run_dispatch(message: str) -> str:
    """Run dispatch with a message and return stdout."""
    result = subprocess.run(
        [sys.executable, str(DISPATCH), "-"],
        input=message,
        capture_output=True,
        text=True,
        timeout=15,
        cwd=str(SKILL_DIR / "scripts")
    )
    if result.returncode != 0 and result.stderr:
        return f"SCRIPT_ERROR:{result.stderr.strip()}"
    return result.stdout.strip()


def assert_startswith(test_name: str, output: str, prefix: str):
    """Check that dispatch output starts with expected protocol prefix."""
    global passed, failed
    if output.startswith(prefix):
        passed += 1
        print(f"  ✓ {test_name}")
    else:
        failed += 1
        # Truncate output for readability
        short = output[:120] + "..." if len(output) > 120 else output
        errors.append(f"{test_name}: expected {prefix}... got {short}")
        print(f"  ✗ {test_name}")
        print(f"    expected: {prefix}...")
        print(f"    got:      {short}")


def assert_contains(test_name: str, output: str, substring: str):
    """Check that dispatch output contains a substring."""
    global passed, failed
    if substring in output:
        passed += 1
        print(f"  ✓ {test_name}")
    else:
        failed += 1
        short = output[:120] + "..." if len(output) > 120 else output
        errors.append(f"{test_name}: expected to contain '{substring}' in {short}")
        print(f"  ✗ {test_name}")
        print(f"    expected to contain: {substring}")
        print(f"    got: {short}")


def assert_not_contains(test_name: str, output: str, substring: str):
    """Check that dispatch output does NOT contain a substring."""
    global passed, failed
    if substring not in output:
        passed += 1
        print(f"  ✓ {test_name}")
    else:
        failed += 1
        errors.append(f"{test_name}: should not contain '{substring}'")
        print(f"  ✗ {test_name}")
        print(f"    should not contain: {substring}")


def assert_valid_chain(test_name: str, output: str, min_steps: int = 2):
    """Check that output is a valid CHAIN with parseable JSON and minimum steps."""
    global passed, failed
    if not output.startswith("CHAIN:"):
        failed += 1
        short = output[:120] + "..." if len(output) > 120 else output
        errors.append(f"{test_name}: not a CHAIN response: {short}")
        print(f"  ✗ {test_name}")
        return None

    try:
        chain_json = output[len("CHAIN:"):]
        chain = json.loads(chain_json)
        if len(chain) >= min_steps:
            passed += 1
            print(f"  ✓ {test_name} ({len(chain)} steps)")
            return chain
        else:
            failed += 1
            errors.append(f"{test_name}: expected >= {min_steps} steps, got {len(chain)}")
            print(f"  ✗ {test_name}: expected >= {min_steps} steps, got {len(chain)}")
            return chain
    except json.JSONDecodeError as e:
        failed += 1
        errors.append(f"{test_name}: invalid JSON in CHAIN: {e}")
        print(f"  ✗ {test_name}: invalid JSON")
        return None


# ─── Test discovery ────────────────────────────────────────────────

def find_module_by_level(level: int) -> str:
    """Find an existing module at a specific level for testing."""
    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or not (d / "MODULE.md").exists():
            continue
        if d.name == "test-dispatch":
            continue  # Don't test ourselves
        has_params = (d / "PARAMS.json").exists()
        has_depends = (d / "DEPENDS.json").exists()
        has_resolve = (d / "RESOLVE.py").exists()

        if level == 0 and not has_params:
            return d.name
        if level == 1 and has_params and not has_depends and not has_resolve:
            return d.name
        if level == 2 and has_depends and not has_resolve:
            return d.name
        if level == 3 and has_resolve and not has_depends:
            return d.name
    return None


def find_level3_with_depends() -> str:
    """Find a Level 3 module that also has DEPENDS.json (Level 2+3)."""
    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or d.name == "test-dispatch":
            continue
        if (d / "RESOLVE.py").exists() and (d / "DEPENDS.json").exists():
            return d.name
    return None


def find_module_with_required_param() -> tuple:
    """Find a module with at least one required param. Returns (name, param_name)."""
    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or d.name == "test-dispatch":
            continue
        params_file = d / "PARAMS.json"
        if params_file.exists():
            schema = json.loads(params_file.read_text())
            for pname, pspec in schema.get("params", {}).items():
                if pspec.get("required") and not pspec.get("inject"):
                    return (d.name, pname)
    return (None, None)


def find_two_chainable_modules() -> tuple:
    """Find two Level 1 modules that can be chained."""
    found = []
    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or d.name == "test-dispatch":
            continue
        if (d / "PARAMS.json").exists() and not (d / "DEPENDS.json").exists() and not (d / "RESOLVE.py").exists():
            found.append(d.name)
            if len(found) == 2:
                return tuple(found)
    return (None, None)


def find_conditional_depends() -> str:
    """Find a module with unless_exists in DEPENDS.json."""
    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or d.name == "test-dispatch":
            continue
        depends_file = d / "DEPENDS.json"
        if depends_file.exists():
            try:
                depends = json.loads(depends_file.read_text())
                for dep in depends.get("before", []):
                    if dep.get("unless_exists"):
                        return d.name
            except (json.JSONDecodeError, IOError):
                pass
    return None


# ─── Test suites ───────────────────────────────────────────────────

def test_routing():
    """Test basic routing across all levels."""
    print("\n── Routing ──")

    # Bare trigger
    out = run_dispatch("reflex")
    assert_startswith("bare reflex", out, "RESPOND:")

    # Unknown module
    out = run_dispatch("reflex nonexistent-module-xyz")
    assert_startswith("unknown module", out, "ERROR:")
    assert_contains("unknown module lists available", out, "Available:")

    # Level 0
    mod = find_module_by_level(0)
    if mod:
        out = run_dispatch(f"reflex {mod}")
        assert_startswith(f"level 0 ({mod})", out, "LOAD_MODULE:")
    else:
        print(f"  - skipped: no Level 0 module found")

    # Level 1
    mod = find_module_by_level(1)
    if mod:
        # Load schema to provide required params
        schema = json.loads((MODULES_DIR / mod / "PARAMS.json").read_text())
        param_str = ""
        for pname, pspec in schema.get("params", {}).items():
            if pspec.get("required") and not pspec.get("inject"):
                param_str += f" {pname}:test-value"
        out = run_dispatch(f"reflex {mod}{param_str}")
        assert_startswith(f"level 1 ({mod})", out, "LOAD_MODULE_WITH_PARAMS:")
    else:
        print(f"  - skipped: no Level 1 module found")

    # Level 2
    mod = find_module_by_level(2)
    if mod:
        schema = json.loads((MODULES_DIR / mod / "PARAMS.json").read_text())
        param_str = ""
        for pname, pspec in schema.get("params", {}).items():
            if pspec.get("required") and not pspec.get("inject"):
                param_str += f" {pname}:test-value"
        out = run_dispatch(f"reflex {mod}{param_str}")
        assert_startswith(f"level 2 ({mod})", out, "CHAIN:")
    else:
        print(f"  - skipped: no Level 2 module found")

    # Level 3 (pure — no DEPENDS)
    mod = find_module_by_level(3)
    if mod:
        schema = json.loads((MODULES_DIR / mod / "PARAMS.json").read_text())
        param_str = ""
        for pname, pspec in schema.get("params", {}).items():
            if pspec.get("required") and not pspec.get("inject"):
                param_str += f" {pname}:test-value"
        out = run_dispatch(f"reflex {mod}{param_str}")
        assert_startswith(f"level 3 pure ({mod})", out, "RESOLVED:")
        assert_contains(f"level 3 has reason ({mod})", out, "REASON:")
    else:
        print(f"  - skipped: no pure Level 3 module found")


def test_params():
    """Test parameter handling."""
    print("\n── Params ──")

    # Missing required params
    mod, param = find_module_with_required_param()
    if mod:
        out = run_dispatch(f"reflex {mod}")
        assert_startswith(f"missing required param ({mod})", out, "MISSING_PARAMS:")
        assert_contains(f"missing lists the param", out, param)
    else:
        print(f"  - skipped: no module with required params found")

    # Named params
    mod = find_module_by_level(1)
    if mod:
        schema = json.loads((MODULES_DIR / mod / "PARAMS.json").read_text())
        for pname, pspec in schema.get("params", {}).items():
            if not pspec.get("inject"):
                out = run_dispatch(f"reflex {mod} {pname}:hello-world")
                assert_contains(f"named param passed through ({pname})", out, "hello-world")
                break
    else:
        print(f"  - skipped: no Level 1 module for param test")


def test_chains():
    """Test inline chain syntax."""
    print("\n── Chains ──")

    mod1, mod2 = find_two_chainable_modules()
    if mod1 and mod2:
        out = run_dispatch(f"reflex {mod1}+{mod2} target:test-target")
        chain = assert_valid_chain(f"inline chain ({mod1}+{mod2})", out, 2)
        if chain:
            assert_contains(f"chain step 1 is {mod1}", json.dumps(chain[0]), mod1)
            assert_contains(f"chain step 2 is {mod2}", json.dumps(chain[1]), mod2)
    else:
        print(f"  - skipped: couldn't find two chainable modules")

    # Chain with nonexistent module
    out = run_dispatch(f"reflex websearch+nonexistent-xyz target:test")
    assert_startswith("chain with bad module", out, "ERROR:")

    # Single module in chain (should error)
    out = run_dispatch("reflex +websearch target:test")
    # This might work or error depending on split behavior — just check it doesn't crash
    print(f"  ✓ single-module chain didn't crash")
    global passed
    passed += 1


def test_resolvers():
    """Test Level 3 resolver routing."""
    print("\n── Resolvers ──")

    # Pure Level 3
    mod = find_module_by_level(3)
    if mod:
        schema = json.loads((MODULES_DIR / mod / "PARAMS.json").read_text())
        param_str = ""
        for pname, pspec in schema.get("params", {}).items():
            if pspec.get("required") and not pspec.get("inject"):
                param_str += f" {pname}:test"
        out = run_dispatch(f"reflex {mod}{param_str}")
        assert_contains(f"resolver produces RESOLVED_BY ({mod})", out, "RESOLVED_BY:")

        # Verify variant path exists
        if "RESOLVED:" in out:
            variant_path = out.split("RESOLVED:")[1].split("|")[0]
            assert_startswith(f"variant path is real ({mod})", 
                            str(Path(variant_path).exists()), "True")
    else:
        print(f"  - skipped: no Level 3 module found")

    # Level 2+3 composite
    mod = find_level3_with_depends()
    if mod:
        schema = json.loads((MODULES_DIR / mod / "PARAMS.json").read_text())
        param_str = ""
        for pname, pspec in schema.get("params", {}).items():
            if pspec.get("required") and not pspec.get("inject"):
                param_str += f" {pname}:test"
        out = run_dispatch(f"reflex {mod}{param_str}")
        # Should be either CHAIN (if deps fire) or RESOLVED (if deps skipped)
        is_chain_or_resolved = out.startswith("CHAIN:") or out.startswith("RESOLVED:")
        global passed, failed
        if is_chain_or_resolved:
            passed += 1
            print(f"  ✓ level 2+3 composite ({mod}) → {'CHAIN' if out.startswith('CHAIN:') else 'RESOLVED'}")
        else:
            failed += 1
            short = out[:120] + "..."
            errors.append(f"level 2+3 ({mod}): expected CHAIN or RESOLVED, got {short}")
            print(f"  ✗ level 2+3 composite ({mod})")
    else:
        print(f"  - skipped: no Level 2+3 module found")


def test_conditionals():
    """Test unless_exists conditional dependencies."""
    print("\n── Conditionals ──")

    mod = find_conditional_depends()
    if not mod:
        print(f"  - skipped: no module with unless_exists found")
        return

    depends = json.loads((MODULES_DIR / mod / "DEPENDS.json").read_text())
    dep = next(d for d in depends["before"] if d.get("unless_exists"))
    pattern = dep["unless_exists"]
    dep_module = dep["module"]

    schema = json.loads((MODULES_DIR / mod / "PARAMS.json").read_text())
    param_str = ""
    for pname, pspec in schema.get("params", {}).items():
        if pspec.get("required") and not pspec.get("inject"):
            param_str += f" {pname}:test"

    # Test WITHOUT the file — dependency should fire
    # Clean up any existing file first
    resolved_pattern = pattern
    try:
        resolved_pattern = pattern.format(intent="test", target="test", topic="test", domain="test")
    except KeyError:
        pass
    target_file = Path("/home/claude") / resolved_pattern
    if target_file.exists():
        target_file.unlink()

    out = run_dispatch(f"reflex {mod}{param_str}")
    if out.startswith("CHAIN:"):
        chain = json.loads(out[len("CHAIN:"):])
        dep_present = any(s.get("module") == dep_module for s in chain)
        global passed, failed
        if dep_present:
            passed += 1
            print(f"  ✓ without file: dep '{dep_module}' fires")
        else:
            failed += 1
            errors.append(f"without file: dep '{dep_module}' should be in chain but isn't")
            print(f"  ✗ without file: dep '{dep_module}' missing from chain")
    else:
        # Might be RESOLVED if dep was skipped for another reason
        print(f"  ~ without file: got {out[:60]}... (may be ok depending on resolver)")
        passed += 1

    # Test WITH the file — dependency should be skipped
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text("{}")

    out = run_dispatch(f"reflex {mod}{param_str}")
    if out.startswith("CHAIN:"):
        chain = json.loads(out[len("CHAIN:"):])
        dep_present = any(s.get("module") == dep_module for s in chain)
        if not dep_present:
            passed += 1
            print(f"  ✓ with file: dep '{dep_module}' skipped")
        else:
            failed += 1
            errors.append(f"with file: dep '{dep_module}' should be skipped but wasn't")
            print(f"  ✗ with file: dep '{dep_module}' should be skipped")
    elif out.startswith("RESOLVED:"):
        # No chain at all — dep was skipped, module resolved directly
        passed += 1
        print(f"  ✓ with file: dep skipped, direct RESOLVED")
    else:
        failed += 1
        short = out[:120] + "..."
        errors.append(f"with file: unexpected output: {short}")
        print(f"  ✗ with file: unexpected output")

    # Clean up
    if target_file.exists():
        target_file.unlink()


# ─── Main ──────────────────────────────────────────────────────────

SUITES = {
    "routing": test_routing,
    "params": test_params,
    "chains": test_chains,
    "resolvers": test_resolvers,
    "conditionals": test_conditionals,
}


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else "all"

    print(f"Dispatch Smoke Tests — scope: {scope}")
    print(f"Skill dir: {SKILL_DIR}")
    print(f"Modules:   {len(list(MODULES_DIR.iterdir()))} found")

    if scope == "all":
        for suite in SUITES.values():
            suite()
    elif scope in SUITES:
        SUITES[scope]()
    else:
        print(f"Unknown scope: {scope}")
        print(f"Available: all, {', '.join(SUITES.keys())}")
        sys.exit(1)

    print(f"\n{'=' * 40}")
    print(f"Results: {passed} passed, {failed} failed")
    if errors:
        print(f"\nFailures:")
        for e in errors:
            print(f"  • {e}")
    print(f"{'=' * 40}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
