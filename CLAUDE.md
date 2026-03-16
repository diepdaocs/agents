# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal [OpenClaw](https://docs.openclaw.ai/cli) AI agent setup — workspace docs, custom skills, and config templates.

## Key Commands

```bash
# Start/stop the gateway
openclaw gateway start
openclaw gateway stop
openclaw gateway status

# Run an agent turn
openclaw agent "your message"

# Install a skill from this repo
openclaw skills install ./skills/<skill-name>

# List all skills (shows which are ready vs missing deps)
openclaw skills list

# Health check (use --fix to auto-repair)
openclaw doctor

# Interactive setup
openclaw configure
```

## Architecture

### Workspace (`workspace/`)
Markdown files loaded into every agent session. The agent reads these at startup to understand who they are, who they're helping, and how to behave. Edit these to shape agent personality and operating rules.

- `SOUL.md` / `IDENTITY.md` — personality and persona
- `USER.md` / `TOOLS.md` — context about the human and local environment
- `AGENTS.md` — operating guidelines (memory system, safety, proactivity rules)
- `HEARTBEAT.md` — periodic tasks; keep empty to disable heartbeat API calls
- `MEMORY.md` — agent-maintained long-term memory (private, not quoted to group chats)

Point OpenClaw at this workspace:
```bash
openclaw config set agents.defaults.workspace "$(pwd)/workspace"
```

### Skills (`workspace/skills/`)
Each skill is a directory containing a `SKILL.md` with YAML frontmatter and markdown instructions. The agent loads a skill's body when the trigger conditions match the user's request.

Frontmatter fields:
- `name`, `description` — used for skill matching and `openclaw skills list`
- `metadata.openclaw.emoji` — UI indicator
- `metadata.openclaw.requires.bins` — binaries that must be present for the skill to be "ready"

Optional subdirectories: `scripts/` (executable helpers), `references/` (large docs loaded on demand).

### Config (`config/openclaw.example.json`)
Template for `~/.openclaw/openclaw.json`. Contains gateway settings, model/auth profiles, and channel configuration. Copy and fill in API keys — never commit real tokens.

## Skill Development

Ask the agent:
> "Create a new skill for [X]"

Or scaffold manually:
```bash
mkdir workspace/skills/my-skill
# Create workspace/skills/my-skill/SKILL.md with frontmatter + instructions
openclaw gateway restart
openclaw skills info my-skill
```
