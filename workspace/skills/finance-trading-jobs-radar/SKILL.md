---
name: finance-trading-jobs-radar
description: Discover, rank, and package high-signal finance, trading, banking, market-infrastructure, and selective fintech engineering roles for a senior backend/data/AI candidate. Use when asked to search jobs, build a shortlist, monitor banks or trading firms, create a Telegram-friendly jobs radar, or find direct apply links with Singapore-first and high-compensation bias.
---

# Finance Trading Jobs Radar

Find fewer, better jobs.

Prioritize direct career pages and public ATS feeds over generic job boards. Optimize for a candidate with 10+ years across backend, data, AI/ML, fintech, and some blockchain work, with strongest fit in Java/Python-heavy engineering roles around financial systems, risk, trading, market data, and platform infrastructure.

## Core workflow

### 1. Start with the candidate thesis
Assume this default positioning unless the user gives a narrower target:
- Senior / Staff / Principal backend or platform engineer
- Strong fit for finance, trading, risk, and market-infrastructure engineering
- Strong secondary fit for data platform, ML platform, and AI engineering infra
- Blockchain is a differentiator, not the default center of gravity
- Singapore-first, then APAC or strong remote roles

Read `references/target-companies.md` when you need the target-company ladder and search order.

### 2. Collect from direct sources first
Use this source ladder:
1. Public ATS APIs and direct hosted job pages
2. Bank and trading-firm career pages
3. Market-infrastructure and exchange employers
4. MyCareersFuture for salary calibration and Singapore-local roles
5. LinkedIn / web search only as discovery layers

Run the bundled script first when you need a fast shortlist:

```bash
python3 ~/code/agents/workspace/skills/finance-trading-jobs-radar/scripts/search_finance_jobs.py --location singapore --limit 12
```

Then refine manually with named firms from `references/target-companies.md`.

### 3. Filter hard
Keep roles that satisfy most of these:
- Backend, platform, infrastructure, data, ML platform, AI platform, or trading-tech content
- Real overlap with finance, markets, exchanges, banking tech, or market data
- Seniority aligned with 10+ years
- Compensation signal consistent with senior Singapore hiring
- Direct apply URL exists

Downgrade or exclude:
- Generic analyst roles
- Pure support or commodity SRE unless strategically strong
- Pure frontend/mobile
- Solutions engineering, sales engineering, recruiter roles
- Thin-quality crypto roles unless the employer is clearly strong

### 4. Rank for decision quality
Score each role on:
- Fit
- Credibility of story
- Compensation potential
- Brand / learning value
- Market timing

Do not let one employer dominate the shortlist. Cap any single employer at 2 roles unless the user asks otherwise.

### 5. Format for action
Default output should be concise and decision-oriented:

```markdown
💼 *FINANCE / TRADING JOBS RADAR — [DATE]*

🎯 *Thesis*
• [1-line positioning]
• [1-line strongest angle]

🏆 *Top Matches*
*1) [Role] — [Company]*
• Why it fits: [1 line]
• Comp signal: [1 line]
• Confidence: [High/Med/Low]
• Apply: [direct URL]

📈 *Market Read*
• [where hiring is active]
• [where the market is cautious]

🧭 *Next Move*
• [best application / networking action this week]
```

Rules:
- Prefer 5-8 roles max
- Every shortlisted role should have a direct apply URL whenever possible
- Separate best-shot roles from stretch roles when useful
- Use single-line bullets; avoid long paragraphs

## On-demand patterns

### Shortlist request
Return the top 5 roles max with direct apply links and a blunt ranking.

### Employer-specific request
Search the named employer deeply, but still state whether it is actually a good fit.

### Weekly recurring radar
Produce a Telegram-friendly shortlist with market context and 1-3 recommended next actions.

## Quality bar

Before sending, check:
- Is the ranking personalized to a senior Java/Python finance-platform candidate?
- Did you diversify beyond one employer?
- Did you use direct job links instead of generic search pages?
- Did you cut weak listings instead of padding the list?
- Did you make the output useful for action, not just browsing?
