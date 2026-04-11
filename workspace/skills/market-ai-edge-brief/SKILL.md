---
name: market-ai-edge-brief
description: Produce a high-signal weekly brief covering AI engineering, developer tooling, banking and market structure, macro technology shifts, and selective blockchain developments, with explicit career and portfolio implications. Use when asked for a market brief, AI update, hedge-style summary, technology-and-finance synthesis, or a Telegram-friendly report explaining what matters and why.
---

# Market AI Edge Brief

Produce a compact strategic brief for someone operating at the intersection of engineering, AI, markets, and finance.

The goal is not broad news coverage. The goal is to surface changes that can affect career positioning, engineering priorities, and market or portfolio risk.

## Core workflow

### 1. Cover the right buckets
Always scan these buckets:
- AI models, AI infra, agents, and developer tooling
- Cloud, data, and platform shifts that matter to engineers
- Banks, exchanges, market structure, and fintech infrastructure
- Macro or policy moves that change technology or capital-allocation behavior
- Blockchain and digital assets only when the move is strategically meaningful

Read `references/source-map.md` when choosing sources.

### 2. Filter for signal
Keep items that have one or more of these properties:
- They change engineering demand or hiring behavior
- They alter the economics of AI or software delivery
- They affect banks, trading firms, exchanges, or capital markets
- They create non-trivial portfolio or hedging implications
- They reveal a meaningful second-order effect

Cut commodity headlines, product-launch spam, and market noise.

### 3. Explain why it matters
For each selected item, answer:
- What changed?
- Why does it matter?
- What is the second-order effect?
- What does it imply for career or portfolio positioning?

### 4. Keep the brief tight
Default format:

```markdown
📡 *MARKET + AI EDGE BRIEF — [DATE]*

*1) [Headline]*
• What changed: [1 line]
• Why it matters: [1 line]
• Second-order effect: [1 line]
• Career implication: [1 line]
• Market implication: [1 line]

🎯 *Bottom line*
• [3 concise takeaways]
```

Rules:
- Prefer 5-7 items max
- Single-line bullets
- Avoid filler summaries
- State uncertainty plainly when evidence is mixed

## Output variants

### Weekly brief
Return the top 5-7 items plus a short bottom-line section.

### AI-only or market-only brief
Narrow the buckets, but still include practical implications.

### Hedge-style read
Emphasize cross-asset and sector implications; avoid fake precision.

## Quality bar
Before sending, check:
- Did you pick signal over coverage?
- Did you explain second-order effects instead of summarizing headlines?
- Did you connect the brief to engineering careers, markets, or both?
- Would the user learn something non-obvious from each item?
