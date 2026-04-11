---
name: senior-role-matcher
description: Score senior engineering roles against a candidate with backend, data, AI/ML, and finance/trading experience, then generate positioning, tailored fit notes, recruiter replies, and resume-angle recommendations. Use when asked to evaluate a role, explain fit, tailor an application, produce outreach copy, or choose the best narrative for backend, platform, data, AI, fintech, or trading-tech jobs.
---

# Senior Role Matcher

Turn a strong but broad profile into a tighter market-facing story.

Use this skill to decide not just whether a job is good, but how to present the candidate so the fit is obvious to recruiters and hiring managers.

## Core workflow

### 1. Build the candidate thesis
Default thesis for this user:
- Senior backend / platform engineer with strong Java and Python depth
- Built production systems in finance, trading, risk, NLP/ML, and data platforms
- Better positioned for engineering-heavy roles than pure research or GTM roles
- Strongest wedges: financial systems, data/ML platforms, platform/backend reliability, real-time systems

Read `references/profile-thesis.md` for the default signature and evidence ladder.

### 2. Read the role and choose the angle
Choose one primary angle only, then optionally a secondary angle:
- Backend / platform
- Finance / trading technology
- Data platform / ML platform / AI infra
- Fintech / market data / risk systems

Do not present the candidate as everything at once.

### 3. Score the match
Evaluate:
- Technical overlap
- Domain overlap
- Seniority alignment
- Story credibility within 30 seconds
- Compensation / title alignment

Use this simple rubric:
- **90-100**: exceptional fit; pursue aggressively
- **75-89**: strong fit; tailor and apply
- **60-74**: plausible with framing; apply selectively
- **<60**: weak fit; avoid unless strategic

### 4. Produce action-oriented outputs
Depending on the request, return one or more of:
- Match score with explanation
- Best positioning angle
- 3-5 resume bullets to emphasize
- Recruiter reply draft
- Why-you summary for the application
- Gaps / risks / objections

Read `references/output-templates.md` when the user wants polished output.

## Output rules
- Be blunt about weak fit
- Prefer a sharper story over a broader one
- Tie claims to evidence from the profile
- Avoid generic praise or fluff
- Use concise bullets unless the user wants long-form prose

## Common tasks

### Evaluate a job
Return:
- Match score
- Best angle
- Why this works
- Biggest risk
- Apply / skip recommendation

### Tailor an application
Return:
- 1-line positioning summary
- 3-5 resume bullets to foreground
- short recruiter or hiring-manager note

### Compare multiple roles
Rank them by expected conversion, not prestige alone.

## Quality bar
Before sending, check:
- Did you choose one dominant narrative instead of mixing four?
- Did you convert experience into evidence instead of adjectives?
- Did you mention real objections when they exist?
- Would a recruiter understand the fit in under 30 seconds?
