# Help Module

Explain the callsign system, its modules, and how to compose them.

- **Topic**: {topic}

## Available Modules

{registry}

## Instructions

Based on `{topic}`, respond appropriately:

### If topic is "overview"
Give a concise introduction to the system:
- What `/callsign` is (a module-based dispatch system)
- The four module groups: sources gather data, analyzers interpret it, transformers reshape it, formatters deliver it
- How to chain with `+`: `/callsign websearch+challenge+pitch target:anthropic audience:investors`
- How params work: positional (`/callsign swot anthropic`) or named (`target:anthropic`)
- Mention `/callsign plan "your goal"` for help composing chains

### If topic is a module name (matches something in the registry)
Explain that specific module: what it does, its params, what group it belongs to, and 2-3 example chains it works well in.

### If topic is a concept ("chains", "sources", "params", "groups")
Explain that concept with examples.

### If topic doesn't match anything
Say what's available and suggest the closest match.

## Output

A clear, concise explanation. Use examples liberally — they teach better than descriptions. Keep it under 15 lines unless the user asked for detail.
