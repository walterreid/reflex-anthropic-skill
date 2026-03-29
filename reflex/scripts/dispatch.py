#!/usr/bin/env python3
"""
Reflex Dispatch Script — Convention-Based Meta-Skill Dispatcher

Resolves modules through filesystem convention across four levels:
  Level 0: MODULE.md
  Level 1: MODULE.md + PARAMS.json
  Level 2: MODULE.md + PARAMS.json + DEPENDS.json
  Level 3: MODULE.md + PARAMS.json + RESOLVE.py + variants/

Output protocols:
  LOAD_MODULE:/path
  LOAD_MODULE_WITH_PARAMS:/path|PARAMS:{...}
  CHAIN:[{step1},{step2}]
  RESOLVED:/path|PARAMS:{...}|RESOLVED_BY:resolver|REASON:text
  MISSING_PARAMS:name|required:[...]|provided:[...]|missing:[...]
  RESPOND:text
  ERROR:message
"""

import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
MODULES_DIR = SKILL_DIR / "modules"


def list_available_modules():
    if not MODULES_DIR.exists():
        return []
    return sorted([
        d.name for d in MODULES_DIR.iterdir()
        if d.is_dir() and (d / "MODULE.md").exists()
    ])


def get_module_level(module_path: Path) -> int:
    if (module_path / "RESOLVE.py").exists():
        return 3
    if (module_path / "DEPENDS.json").exists():
        return 2
    if (module_path / "PARAMS.json").exists():
        return 1
    return 0


def load_json(filepath: Path) -> dict:
    try:
        with open(filepath) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return {"error": str(e)}


def extract_params_from_message(words: list, schema: dict) -> dict:
    params = {}
    param_names = list(schema.get("params", {}).keys())
    param_specs = schema.get("params", {})

    kv_pattern = re.compile(r'^(\w[\w-]*):(.+)$')
    positional_words = []

    for word in words:
        match = kv_pattern.match(word)
        if match:
            key, value = match.group(1), match.group(2)
            if key in param_names:
                params[key] = value
        else:
            positional_words.append(word)

    unfilled = [name for name in param_names if name not in params]
    for i, param_name in enumerate(unfilled):
        if i < len(positional_words):
            # Greedy params absorb all remaining positional words
            if param_specs.get(param_name, {}).get("greedy", False):
                params[param_name] = " ".join(positional_words[i:])
                break
            else:
                params[param_name] = positional_words[i]

    return params


def apply_defaults(params: dict, schema: dict) -> dict:
    result = dict(params)
    for name, spec in schema.get("params", {}).items():
        if name not in result and spec.get("default") is not None:
            result[name] = spec["default"]
    return result


def validate_params(params: dict, schema: dict) -> tuple:
    missing = []
    for name, spec in schema.get("params", {}).items():
        if spec.get("required", False) and name not in params:
            missing.append(name)
    return (len(missing) == 0, missing)


def resolve_forward_params(forward_params: dict, parent_params: dict) -> dict:
    resolved = {}
    for key, value in forward_params.items():
        if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
            ref = value[1:-1]
            if ref in parent_params:
                resolved[key] = parent_params[ref]
            else:
                resolved[key] = value
        else:
            resolved[key] = value
    return resolved


def build_chain(module_name: str, module_path: Path, params: dict, visited=None) -> list:
    if visited is None:
        visited = set()
    if module_name in visited:
        return [{"error": f"Circular dependency detected: {module_name}"}]

    visited.add(module_name)
    steps = []

    depends_file = module_path / "DEPENDS.json"
    if depends_file.exists():
        depends = load_json(depends_file)
        if "error" in depends:
            return [{"error": f"Failed to read DEPENDS.json: {depends['error']}"}]

        for dep in depends.get("before", []):

            # Check conditional skip
            skip_condition = dep.get("unless_exists")
            if skip_condition:
                try:
                    pattern = skip_condition.format(**params)
                    matches = list(Path("/home/claude").glob(pattern))
                    if matches:
                        continue  # dependency output already exists, skip
                except (KeyError, ValueError):
                    pass  # if pattern can't resolve, run the dependency anyway

            dep_name = dep.get("module")
            dep_path = MODULES_DIR / dep_name

            if not dep_path.exists() or not (dep_path / "MODULE.md").exists():
                return [{"error": f"Dependency '{dep_name}' not found"}]

            forward = dep.get("forward_params", {})
            dep_params = resolve_forward_params(forward, params)

            dep_params_file = dep_path / "PARAMS.json"
            if dep_params_file.exists():
                dep_schema = load_json(dep_params_file)
                dep_params = apply_defaults(dep_params, dep_schema)

            sub_chain = build_chain(dep_name, dep_path, dep_params, visited.copy())
            if sub_chain and "error" in sub_chain[-1]:
                return sub_chain

            if sub_chain:
                sub_chain[-1]["output_key"] = dep.get("output_key", dep_name + "_output")

            steps.extend(sub_chain)

    steps.append({
        "module": module_name,
        "path": str(module_path / "MODULE.md"),
        "params": params,
        "output_key": module_name + "_output"
    })

    for i, step in enumerate(steps):
        step["step"] = i + 1

    return steps


def build_inline_chain(module_names: list, extra_words: list) -> str:
    """
    Build a chain from inline + syntax.
    
    The + operator IS the dependency specification — each module's own
    DEPENDS.json is ignored. Params are collected from all modules in
    chain order, with deduplication preserving first occurrence (so the
    first module's 'target' wins over a later module's 'target').
    
    Positional param filling uses a priority order:
    - Params unique to one module are filled by position within that context
    - Shared param names (like 'target') appear once, filled first
    """
    # Validate all modules exist
    for name in module_names:
        path = MODULES_DIR / name
        if not path.exists() or not (path / "MODULE.md").exists():
            available = list_available_modules()
            hint = f" Available: {', '.join(available)}" if available else ""
            return f"ERROR:No module found for '{name}' in chain.{hint}"

    # Collect all unique param names in chain order (first occurrence wins)
    all_param_names = {}
    for name in module_names:
        params_file = MODULES_DIR / name / "PARAMS.json"
        if params_file.exists():
            schema = load_json(params_file)
            for pname, pspec in schema.get("params", {}).items():
                if pname not in all_param_names:
                    all_param_names[pname] = pspec

    # Build a merged schema for param extraction
    merged_schema = {"params": all_param_names}
    extracted = extract_params_from_message(extra_words, merged_schema)
    extracted = apply_defaults(extracted, merged_schema)

    # Build the chain steps — IGNORE each module's DEPENDS.json
    steps = []
    prev_output_key = None
    for i, name in enumerate(module_names):
        path = MODULES_DIR / name
        module_md = path / "MODULE.md"

        # Each step gets all extracted params (modules use what they need)
        step_params = dict(extracted)

        # Inject previous step's output key as context reference
        if prev_output_key:
            step_params[prev_output_key] = f"{{{prev_output_key}}}"

        output_key = name + "_output"

        steps.append({
            "module": name,
            "path": str(module_md),
            "params": step_params,
            "output_key": output_key
        })

        prev_output_key = output_key

    # Renumber steps
    for i, step in enumerate(steps):
        step["step"] = i + 1

    return f"CHAIN:{json.dumps(steps)}"


def inject_params(extracted: dict, schema: dict) -> dict:
    """
    Fill any params that declare an 'inject' source.
    Delegates to sources.py — dispatch doesn't know what sources exist.
    """
    from sources import resolve as resolve_sources
    injected = resolve_sources(schema)
    result = dict(extracted)
    result.update(injected)
    return result


def run_resolver(module_path: Path, params: dict) -> tuple:
    """
    Run a module's RESOLVE.py with params as JSON argument.
    Returns (variant_name, reason_text) or (None, error_message).
    """
    resolver = module_path / "RESOLVE.py"
    params_json = json.dumps(params)

    try:
        result = subprocess.run(
            [sys.executable, str(resolver), params_json],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return (None, f"Resolver failed: {result.stderr.strip()}")

        # Parse output — expect "variant_name" or "variant_name|reason text"
        output = result.stdout.strip()
        if "|" in output:
            variant, reason = output.split("|", 1)
        else:
            variant = output
            reason = f"Resolved to '{variant}'"

        return (variant.strip(), reason.strip())

    except subprocess.TimeoutExpired:
        return (None, "Resolver timed out")
    except Exception as e:
        return (None, f"Resolver error: {e}")


def dispatch(message: str) -> str:
    import shlex
    try:
        words = shlex.split(message.strip().lower())
    except ValueError:
        # Fallback if quotes are unbalanced
        words = message.strip().lower().split()

    # Support multiple trigger words — skip if found at any position
    tango_idx = -1
    for trigger in ("callsign", "tango"):
        if trigger in words:
            tango_idx = words.index(trigger)
            break

    if not words:
        return "ERROR:No input provided"

    if tango_idx == -1:
        module_name = words[0]
        extra_words = words[1:]
    else:
        remaining = words[tango_idx + 1:]
        if not remaining:
            return "RESPOND:Foxtrot, Charlie."
        module_name = remaining[0]
        extra_words = remaining[1:]

    # --- Inline chain: module1+module2+module3 syntax ---
    if "+" in module_name:
        chain_modules = [m.strip() for m in module_name.split("+") if m.strip()]
        if len(chain_modules) < 2:
            return "ERROR:Chain requires at least two modules separated by +"
        return build_inline_chain(chain_modules, extra_words)

    module_path = MODULES_DIR / module_name

    if not module_path.exists() or not (module_path / "MODULE.md").exists():
        available = list_available_modules()
        hint = f" Available: {', '.join(available)}" if available else ""
        return f"ERROR:No module found for '{module_name}'.{hint}"

    level = get_module_level(module_path)
    module_md = module_path / "MODULE.md"

    # Level 0
    if level == 0:
        return f"LOAD_MODULE:{module_md}"

    # Level 1+: handle params
    schema = load_json(module_path / "PARAMS.json")
    if "error" in schema:
        return f"ERROR:Failed to read PARAMS.json: {schema['error']}"

    extracted = extract_params_from_message(extra_words, schema)
    extracted = apply_defaults(extracted, schema)
    extracted = inject_params(extracted, schema)

    is_valid, missing = validate_params(extracted, schema)
    if not is_valid:
        required = [n for n, s in schema.get("params", {}).items() if s.get("required")]
        provided = list(extracted.keys())
        return f"MISSING_PARAMS:{module_name}|required:{required}|provided:{provided}|missing:{missing}"

    # Level 1
    if level == 1:
        return f"LOAD_MODULE_WITH_PARAMS:{module_md}|PARAMS:{json.dumps(extracted)}"

    # Level 2
    if level == 2:
        chain = build_chain(module_name, module_path, extracted)
        for step in chain:
            if "error" in step:
                return f"ERROR:{step['error']}"
        if len(chain) == 1:
            return f"LOAD_MODULE_WITH_PARAMS:{module_md}|PARAMS:{json.dumps(extracted)}"
        return f"CHAIN:{json.dumps(chain)}"

    # Level 3: run resolver
    variant_name, reason = run_resolver(module_path, extracted)
    if variant_name is None:
        return f"ERROR:{reason}"

    # Resolve variant to filesystem
    variant_path = module_path / "variants" / variant_name / "MODULE.md"
    if not variant_path.exists():
        available_variants = [
            d.name for d in (module_path / "variants").iterdir()
            if d.is_dir() and (d / "MODULE.md").exists()
        ] if (module_path / "variants").exists() else []
        return f"ERROR:Variant '{variant_name}' not found. Available: {', '.join(available_variants)}"

    # Check if variant has its own PARAMS.json (inherit parent params if not)
    variant_params_file = module_path / "variants" / variant_name / "PARAMS.json"
    if variant_params_file.exists():
        variant_schema = load_json(variant_params_file)
        extracted = apply_defaults(extracted, variant_schema)

    return f"RESOLVED:{variant_path}|PARAMS:{json.dumps(extracted)}|RESOLVED_BY:RESOLVE.py|REASON:{reason}"


def main():
    if len(sys.argv) < 2:
        modules = list_available_modules()
        print("REFLEX — Convention-Based Meta-Skill Dispatcher")
        print(f"  Available modules: {', '.join(modules)}")
        print()
        for m in modules:
            mp = MODULES_DIR / m
            level = get_module_level(mp)
            info = ""
            if level >= 1 and (mp / "PARAMS.json").exists():
                schema = load_json(mp / "PARAMS.json")
                pnames = list(schema.get("params", {}).keys())
                info += f"params: {', '.join(pnames)}"
            if level == 2:
                deps = load_json(mp / "DEPENDS.json")
                dnames = [d["module"] for d in deps.get("before", [])]
                info += f" | deps: {', '.join(dnames)}"
            if level == 3:
                variants = [d.name for d in (mp / "variants").iterdir()
                           if d.is_dir() and (d / "MODULE.md").exists()
                           ] if (mp / "variants").exists() else []
                info += f" | variants: {', '.join(variants)}"
            print(f"  [{m}] Level {level}{' — ' + info if info else ''}")
        sys.exit(0)

    if sys.argv[1] == '-':
        message = sys.stdin.read().strip()
    else:
        message = " ".join(sys.argv[1:])
    result = dispatch(message)
    print(result)


if __name__ == "__main__":
    main()
