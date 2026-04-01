---
name: state-analysis
description: "Generate and view state/screen transition diagrams in Mermaid stateDiagram-v2 format. Use when the user asks for screen flows, state machines, page transitions, UI navigation, lifecycle diagrams, state visualization, or wants to view previously generated diagrams. Auto-generates from codebase analysis or natural language descriptions. Trigger on keywords: mermaid, state diagram, stateDiagram, transition, flow, lifecycle, navigation, screen transition."
user_invocable: show
---

# State Analysis

Generate and view state/screen transition diagrams using Mermaid `stateDiagram-v2`.

## Generating diagrams

### Diagram types

- **Screen transition**: states = screens/pages, transitions = user actions
- **State transition**: states = object/system states, transitions = events/triggers

### Input sources

**From codebase**: Use Glob/Grep to find routing definitions, state management, and navigation calls. Extract states and transitions.

**From user description**: Identify states (nodes), transitions (edges) with triggers, and start/end states. Ask if unclear.

### Output rules

1. Always use `stateDiagram-v2`
2. Default to `direction LR` (use `direction TB` if vertical fits better)
3. Use alphanumeric state IDs with localized display names as aliases (`id : DisplayName`) — never use non-ASCII characters directly as IDs
4. Mark start/end states with `[*]`
5. Always label transitions (`: action` or `: event`)
6. Use `state name <<choice>>` for conditional branching
7. Use `<<fork>>` / `<<join>>` for parallel processing
8. Use `note right of id ... end note` for supplementary info
9. For complex diagrams (10+ states), group with nested `state GroupName { ... }` or suggest splitting
10. Never use hyphens `-` or reserved words (`state`, `note`, `end`) as state names

### Output format

Brief description (1-2 sentences) → mermaid code block → supplementary notes if needed. Save as `.md` file when writing to disk.

## Showing diagrams (`/state-analysis:show`)

Find and display previously generated Mermaid stateDiagram blocks from `.md` files in the project.

1. Use Grep to find all files containing `stateDiagram-v2` in the project directory
2. Read each file and extract the mermaid code blocks
3. Run the viewer script:

```bash
python "<skill-dir>/scripts/viewer.py" <file1.md> <file2.md> ...
```

4. If no diagrams are found, inform the user

If Python is unavailable, output the mermaid code blocks directly in the terminal with file paths.
