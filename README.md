# state-analysis

Claude Code skill for generating and viewing state/screen transition diagrams using Mermaid `stateDiagram-v2`.

## Features

- **State transition diagrams** - Generate diagrams from codebase analysis or natural language descriptions
- **Screen transition diagrams** - Visualize page/screen navigation flows
- **Browser viewer** - View generated diagrams in a browser with mermaid.js rendering
- **Mermaid Live Editor integration** - Open diagrams directly in mermaid.live for editing

## Installation

Add this skill to your Claude Code skills directory:

```
~/.claude/skills/state-analysis/
```

## Usage

### Generating diagrams

Ask Claude Code to generate a state or screen transition diagram:

- "This project's screen transitions to a state diagram"
- "Generate a state diagram for the authentication flow"
- "Create a screen transition diagram from the routing definitions"

Claude will analyze your codebase (routing, state management, navigation) or your description and produce a Mermaid `stateDiagram-v2` diagram.

### Viewing diagrams

Use the `/state-analysis:show` command to find and display all previously generated state diagrams in your project. The viewer opens in your browser with:

- Rendered Mermaid diagrams
- Links to edit each diagram in [Mermaid Live Editor](https://mermaid.live)
- Source file references

## Diagram Rules

- Uses `stateDiagram-v2` format
- Default `direction LR` (horizontal layout)
- Alphanumeric state IDs with display name aliases
- Labeled transitions with actions/events
- Supports `<<choice>>`, `<<fork>>`, `<<join>>` constructs
- Nested `state` grouping for complex diagrams (10+ states)

## File Structure

```
state-analysis/
  SKILL.md          # Skill definition and instructions
  scripts/
    viewer.py       # Browser-based diagram viewer
```

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3.10+ (for the viewer script)

## License

MIT
