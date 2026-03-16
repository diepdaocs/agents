# OpenClaw AI Agents

Personal OpenClaw agent setup — workspace docs, custom skills, and config.

## Prerequisites

- [OpenClaw](https://docs.openclaw.ai/cli) installed (`openclaw --version`)
- At least one model API key (Anthropic, Google, OpenAI, or a local Ollama instance)

## Setup

### 1. Point OpenClaw at this workspace

```bash
openclaw config set agents.defaults.workspace "$(pwd)/workspace"
```

### 2. Verify skills are loaded

Skills in `workspace/skills/` are auto-discovered — no install step needed.

```bash
openclaw skills list   # should show daily-briefing and file-organizer as ready
```

### 3. Configure your model

```bash
# Anthropic (Claude)
openclaw models auth anthropic

# Google (Gemini)
openclaw models auth google

# Or use Ollama locally (no auth needed if already running)
openclaw models set --primary ollama/llama3
```

### 4. (Optional) Copy and edit the example config

```bash
cp config/openclaw.example.json ~/.openclaw/openclaw.json
# Then edit to fill in tokens, channel settings, etc.
```

Run the interactive setup wizard instead if you prefer:

```bash
openclaw configure
```

## Running

### Start the gateway

```bash
openclaw gateway start
openclaw gateway status
```

### Run an agent turn

```bash
# One-shot
openclaw agent "What's on my plate today?"

# Interactive TUI
openclaw tui
```

### Check agent health

```bash
openclaw doctor
```

## Workspace

The `workspace/` directory is loaded into every agent session. Edit these files to shape agent behavior:

| File | Purpose |
|------|---------|
| `SOUL.md` | Core personality and values |
| `IDENTITY.md` | Agent name, avatar, vibe |
| `USER.md` | Notes about you (timezone, preferences, projects) |
| `TOOLS.md` | Local environment specifics (SSH hosts, devices) |
| `AGENTS.md` | Operating guidelines (memory, safety, proactivity) |
| `HEARTBEAT.md` | Periodic tasks run on each heartbeat |
| `MEMORY.md` | Curated long-term memory (agent-maintained) |

## Skills

Custom skills live in `workspace/skills/` — they're auto-discovered from the workspace, no install step needed.

```
workspace/skills/
├── daily-briefing/   # Morning digest: weather, tasks, memory summary
└── file-organizer/   # Organize files and directories by pattern
```

To create a new skill, ask the agent:
> "Create a new skill for [what it does]"

Or add a new directory with a `SKILL.md` and restart the gateway:
```bash
mkdir workspace/skills/my-skill
# write workspace/skills/my-skill/SKILL.md
openclaw gateway restart
```

## Updating

```bash
openclaw update
```
