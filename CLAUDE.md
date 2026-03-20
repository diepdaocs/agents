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
openclaw gateway restart

# Run an agent turn (requires --agent main to target the main session)
openclaw agent -m "your message" --agent main

# List all skills (shows which are ready vs missing deps)
openclaw skills list
openclaw skills info <skill-name>
openclaw skills check

# Health check (use --repair to auto-fix)
openclaw doctor --repair

# Interactive setup
openclaw configure

# Cron jobs (gateway token required for add/delete)
openclaw cron list --token "<gateway-token>"
openclaw cron add --name <name> --cron "*/5 * * * *" --message "your prompt" --token "<gateway-token>"
openclaw cron delete --name <name>

# Sessions
openclaw sessions
openclaw sessions --json

# Config
openclaw config get <key>
openclaw config set <key> <value>

# DM pairing (approve inbound Telegram/Discord pair requests)
openclaw pairing list
openclaw pairing approve <code>
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
- `description` **must be quoted** with double quotes if it contains special characters like `>`, `:`, etc.
- `metadata` — use **multi-line JSON** format (matches working skills like daily-briefing); single-line also works
- `metadata.openclaw.requires.bins` — binaries that must be present for the skill to be "ready"

Example frontmatter (use this format — it matches the working skills):
```yaml
---
name: my-skill
description: "What this skill does. Use when: user asks X. NOT for: Y."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["python3"] },
      },
  }
---
```

Optional subdirectories: `scripts/` (executable helpers), `references/` (large docs loaded on demand).

### Auth Profiles
API keys are stored in **two places** — both must be updated when adding a new provider:
1. `~/.openclaw/openclaw.json` — provider profile declaration (mode only, no key)
2. `~/.openclaw/agents/main/agent/auth-profiles.json` — actual API keys per agent

Auth profile format in `auth-profiles.json`:
```json
{
  "profiles": {
    "openrouter:default": {
      "type": "api_key",
      "provider": "openrouter",
      "key": "sk-or-v1-..."
    }
  },
  "lastGood": { "openrouter": "openrouter:default" }
}
```

### Model Config
Models are set in `~/.openclaw/openclaw.json` under `agents.defaults.model`:
```json
{
  "primary": "openrouter/arcee-ai/trinity-large-preview:free",
  "fallbacks": [
    "openrouter/openrouter/hunter-alpha",
    "openrouter/stepfun/step-3.5-flash",
    "openrouter/deepseek/deepseek-v3.2",
    "openrouter/anthropic/claude-sonnet-4.6"
  ]
}
```

Model format: `openrouter/<provider>/<model-id>` — where the first `openrouter/` is the provider prefix for openclaw.
Special case: `openrouter/openrouter/hunter-alpha` — double prefix required because hunter-alpha lives in the `openrouter/` namespace on OpenRouter.

**Known limitation**: OpenRouter free-tier models (`:free` suffix, `openrouter/hunter-alpha`) require `HTTP-Referer` and `X-Title` headers that openclaw's embedded agent does not send. They will fail and fall through to paid models. This is an openclaw limitation, not a config error.

### Gateway Auth
The gateway uses token auth. The token is in `~/.openclaw/openclaw.json` under `gateway.auth.token`.
CLI commands that need it (e.g. `openclaw cron add`) require `--token <value>` flag.
The `gateway.remote.url` and `gateway.remote.token` fields allow the CLI to auto-authenticate:
```json
"gateway": {
  "remote": {
    "url": "ws://127.0.0.1:18789",
    "token": "<same-as-gateway.auth.token>"
  }
}
```

### Config
- Template: `config/openclaw.example.json`
- Live config: `~/.openclaw/openclaw.json`

The gateway **hot-reloads** most config changes automatically — no restart needed for model changes.
Restart is required after: auth changes, plugin changes, channel config changes.

## Installed Skills

| Skill | Trigger | Schedule |
|-------|---------|----------|
| `cpu-monitor` | CPU usage check | Every 10 min (cron) |
| `crypto-monitor` | Crypto portfolio + macro news | Every 4 hours (cron) |
| `daily-briefing` | Morning digest | — |
| `file-organizer` | File/directory cleanup | — |

### cpu-monitor
- Script: `workspace/skills/cpu-monitor/scripts/monitor_cpu.sh`
- Threshold: **50%** CPU usage
- Alerts to Telegram session key `telegram:6202550149`

### crypto-monitor
- Portfolio: ~$2k BTC (~0.027), ~$2k ETH (~0.86 ETH), ~$2k SOL (~21.4 SOL) = ~$6k total
- Alert threshold: ±$600 (10% of portfolio)
- Scripts: `fetch_portfolio.py` (prices/volatility), `fetch_news.py` (macro RSS news)
- Alerts to Telegram session key `telegram:6202550149`
- Provides hedging strategies (conservative / moderate / aggressive)

## Skill Development

Always use **Python scripts** (`.py`), not shell scripts (`.sh`), for new skill scripts.

Ask the agent:
> "Create a new skill for [X]"

Or scaffold manually:
```bash
mkdir workspace/skills/my-skill
# Create workspace/skills/my-skill/SKILL.md with frontmatter + instructions
# Add Python scripts to workspace/skills/my-skill/scripts/
openclaw gateway restart
openclaw skills info my-skill
```

After creating/editing skills, restart the gateway so OpenClaw picks them up:
```bash
openclaw gateway restart
```
