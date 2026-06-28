---
name: prompt-audit
description: Self-audit skill — agents use this to evaluate their own system prompts, skills, and templates against 19 industry design patterns and anti-patterns. Checks Priority Stack, Decision Tree, Output Contract, Knowledge Boundary, Escalation Path, Persona Lock, Format Negotiation, Confidence Calibration, Context Management, Role+Constraints, Chain of Verification, Structured Output, Tool Selection, Error Recovery, Context Window, Guard Rails, Progressive Disclosure, Memory Integration, and Self-Evaluation Loop.
version: 1.0
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.


# PROMPT-AUDIT SKILL (v1.1)

> **Role:** Self-audit skill — agents use this to evaluate their own system prompts against industry best practices
> **RED-TEAM-DOD INTEGRATION.** This skill self-applies: after auditing a prompt, the auditor red-teams its own findings. Autonomous trigger: any time a prompt/skill/template is modified, run a prompt audit. See `skill_view('red-team-dod')`.
> **Generated from:** Research synthesis — pecollective.com (9 Patterns, Feb 2026), paxrel.com (10 Agent Prompt Patterns, Mar 2026), Anthropic (Prompting Best Practices for Claude Opus 4.8), promptingguide.ai (LLM Agents)
> **Date:** 2026-06-02 (v1.1: 2026-06-28)

---

## 1. WHEN TO USE THIS SKILL

Load this skill when:
- Auditing a system prompt for structural completeness
- Reviewing a skill's SKILL.md for quality
- Evaluating a template for parameterization quality
- Checking an agent prompt for known anti-patterns
- Running pre-deployment prompt quality assurance
- Responding to "audit my prompt" or "review this prompt"

**AUTONOMOUS TRIGGER:** The agent MUST self-audit ANY modified prompt/skill/template BEFORE committing the change. This is the prompt-audit instance of the RED-TEAM-DOD cycle (§Phase 1: Red-Team). No user prompting required.

---

## 2. AUDIT CHECKLIST — Architecture Patterns

For each pattern, score 0 (absent), 1 (partial), or 2 (fully implemented).

### 2.1 Priority Stack (Pattern 1)

| Check | Criteria |
|:------|:---------|
| Are rules organized in explicit priority tiers? | 0=no, 1=implicit, 2=explicit numbered tiers |
| Is the highest tier labeled "NEVER VIOLATE"? | 0=no, 2=yes |
| Is there a resolution rule for conflicts? | 0=no, 2=yes ("higher priority always wins") |
| Is there an override authority statement? | 0=no, 2=yes |

### 2.2 Decision Tree / Classification-Routing (Pattern 2)

| Check | Criteria |
|:------|:---------|
| Does the prompt route by input classification? | 0=flat rules, 1=implicit routing, 2=explicit "classify→act" |
| Are category-specific instructions present? | 0=no, 2=yes |

### 2.3 Output Contract (Pattern 3)

| Check | Criteria |
|:------|:---------|
| Is response format explicitly defined? | 0=no, 1=vague ("respond helpfully"), 2=exact schema/template |
| Are structured output schemas provided (if applicable)? | 0=no schema, 1=partial, 2=full schema with types and required fields |
| Is there a "no preamble, no markdown fences" rule for programmatic output? | 0=no, 2=yes |

### 2.4 Knowledge Boundary (Pattern 4)

| Check | Criteria |
|:------|:---------|
| Is the model's knowledge scope explicitly bounded? | 0=no, 2=yes |
| Is there a scripted response for out-of-scope queries? | 0=no, 2=yes |
| Is hallucination prevention addressed? | 0=no, 1=mentioned, 2=explicit rule with example |

### 2.5 Escalation Path (Pattern 5)

| Check | Criteria |
|:------|:---------|
| Are escalation triggers defined? | 0=no, 2=yes |
| Are there clear criteria for when to stop/handoff? | 0=no, 2=yes |

### 2.6 Persona Consistency Lock (Pattern 6)

| Check | Criteria |
|:------|:---------|
| Is there a scripted response for identity questions? | 0=no, 2=yes |
| Does the prompt prevent persona-breaking under probing? | 0=no, 2=yes |

### 2.7 Format Negotiation Rule (Pattern 7)

| Check | Criteria |
|:------|:---------|
| Is output format matched to context? | 0=flat format, 1=mentioned, 2=explicit context→format mapping |
| Are programmatic vs. user-facing formats distinguished? | 0=no, 2=yes |

### 2.8 Confidence Calibration (Pattern 8)

| Check | Criteria |
|:------|:---------|
| Are certainty labels defined and required? | 0=no, 1=defined, 2=defined+required |
| Is there a rule against presenting speculation as fact? | 0=no, 2=yes |

### 2.9 Conversation Reset / Context Management (Pattern 9)

| Check | Criteria |
|:------|:---------|
| For long-running agents: context management rules? | 0=no, 1=mentioned, 2=PRIORITIZE/SUMMARIZE/DISCARD rules |
| For chatbots: reset trigger defined? | 0=no, 2=yes |

---

## 3. AUDIT CHECKLIST — Agent-Specific Patterns (from Paxrel)

### 3.1 Role + Constraints (Paxrel Pattern 1)

| Check | Criteria |
|:------|:---------|
| Is the agent's role clearly defined? | 0=vague ("helpful assistant"), 2=specific domain+scope |
| Are constraints explicitly stated (what it CANNOT do)? | 0=no constraints, 2=explicit constraints list |
| Are constraints separated from role description? | 0=buried in prose, 2=separate labeled section |

### 3.2 Chain of Verification (Paxrel Pattern 2)

| Check | Criteria |
|:------|:---------|
| Is there a verification checklist before output? | 0=no, 1="double-check" (vague), 2=specific checklist |
| Are criteria specific and verifiable? | 0=no, 2=yes |
| Is there a "fail→rewrite→recheck" rule? | 0=no, 2=yes |

### 3.3 Structured Output Enforcement (Paxrel Pattern 3)

| Check | Criteria |
|:------|:---------|
| For pipeline outputs: exact JSON schema provided? | 0=no schema, 1=partial, 2=full schema |
| Is there a "no preamble, no markdown" rule? | 0=no, 2=yes |
| Are null handling rules provided? | 0=no, 2=yes |

### 3.4 Tool Selection Heuristics (Paxrel Pattern 4)

| Check | Criteria |
|:------|:---------|
| Are there priority-ordered rules for tool selection? | 0=no, 2=yes |
| Is there a "cheapest tool first" rule? | 0=no, 2=yes |
| Are expensive/risky tools gated? | 0=no, 2=yes |

### 3.5 Error Recovery Instructions (Paxrel Pattern 5)

| Check | Criteria |
|:------|:---------|
| Is there a RECOVERABLE vs UNRECOVERABLE distinction? | 0=no, 2=yes |
| Are retry limits specified? | 0=no, 2=yes |
| Is there a HALT pattern for unrecoverable errors? | 0=no, 2=yes |

### 3.6 Context Window Management (Paxrel Pattern 6)

| Check | Criteria |
|:------|:---------|
| Are PRIORITIZE/SUMMARIZE/DISCARD rules defined? | 0=no, 1=partial, 2=all three |
| Is there a compaction rule for long sessions? | 0=no, 2=yes |

### 3.7 Guard Rails (Paxrel Pattern 7)

| Check | Criteria |
|:------|:---------|
| Are HARD LIMITS defined and visually separated? | 0=no, 1=buried in prose, 2=separate section with clear heading |
| Are spending, scope, and external action limits specified? | 0=no, 1=partial, 2=comprehensive |

### 3.8 Progressive Disclosure (Paxrel Pattern 8)

| Check | Criteria |
|:------|:---------|
| Are instructions phase-gated? | 0=flat, 1=implied sequence, 2=explicit phases with gates |
| Is there a "complete Phase N before Phase N+1" rule? | 0=no, 2=yes |

### 3.9 Memory Integration (Paxrel Pattern 9)

| Check | Criteria |
|:------|:---------|
| Are persistent memory read/write rules defined? | 0=no, 2=yes |
| Is there a "read at start, write at end" pattern? | 0=no, 2=yes |
| Is missing/corrupt memory handled? | 0=no, 2=yes |

### 3.10 Self-Evaluation Loop (Paxrel Pattern 10)

| Check | Criteria |
|:------|:---------|
| Is there a numeric scoring rubric? | 0=no, 1=descriptive, 2=numeric with criteria per score |
| Are decision rules defined (publish/rewrite/skip thresholds)? | 0=no, 2=yes |
| Is there a max-rewrite limit? | 0=no, 2=yes |

---

## 4. AUDIT CHECKLIST — Text-Level Quality

### 4.1 Structure & Formatting

| Check | Criteria |
|:------|:---------|
| Is the prompt structured with headings/sections (not prose wall)? | 0=prose wall, 1=some structure, 2=clear section hierarchy |
| Are XML tags or Markdown headings used consistently? | 0=no, 1=inconsistent, 2=consistent |
| Are rules in numbered/bulleted lists (one rule per line)? | 0=prose paragraphs, 1=mixed, 2=one rule per line |
| Are gate keywords (HARD BLOCK, MANDATORY) in ALL CAPS? | 0=no, 1=some, 2=consistent |
| Are the most important rules FIRST and LAST? | 0=buried, 1=some, 2=strategic placement |

### 4.2 Writing Quality

| Check | Criteria |
|:------|:---------|
| Do instructions describe observable behavior (not internal state)? | 0=vague ("be helpful"), 1=mixed, 2=operational |
| Is politeness padding removed ("please try to maybe...")? | 0=heavy padding, 1=light, 2=clean imperative |
| One instruction per sentence (no compound instructions)? | 0=compound, 1=mixed, 2=one per line |
| Are negative instructions used only for hard gates? | 0=heavy negative, 1=mixed, 2=positive for behavior, negative for gates |
| Is implied knowledge eliminated (everything stated explicitly)? | 0=assumes knowledge, 1=partial, 2=fully explicit |

### 4.3 Examples (Few-Shot)

| Check | Criteria |
|:------|:---------|
| Are 2–4 examples provided? | 0=none, 1=1 example, 2=2+ examples |
| Does at least one example cover an edge case? | 0=no edge case, 2=yes |
| Do examples show behavior (not explain it)? | 0=explanation-only, 2=demonstration |

### 4.4 Cross-Referencing

| Check | Criteria |
|:------|:---------|
| Are cross-references named (not spatial)? | 0=("as described above"), 2=("see §7.1") |
| Are section references consistent? | 0=inconsistent, 2=consistent |

---

## 5. ANTI-PATTERN DETECTION

Flag ANY of these as `[BLOCKING]`:

| Anti-Pattern | Detection Signal |
|:-------------|:-----------------|
| **Wall of Text** | >500 consecutive chars without a heading, list, or table |
| **Contradictory Instructions** | "Be concise" + "provide detailed explanations" + "keep under 200 words" — flag all conflicts |
| **No Edge Case Structure** | Prompt works for normal queries but has no off-topic, malicious, or repeated-input handling |
| **Compound Instructions** | Multiple distinct actions in one sentence separated by "and" or "but" |
| **Assumed Knowledge** | Phrases like "as you know," "standard procedure," "as described above" without definition |
| **Politeness Dilution** | "Please try to maybe consider..." — flag all softening |
| **"Is this good?" Verification** | Vague self-check with no criteria → flag as ineffective |

---

## 6. SCORING & OUTPUT FORMAT

### 6.1 Composite Score

Calculate for each category:
- **Architecture Score** = (sum of 2.1–2.9) / 18 × 100
- **Agent Patterns Score** = (sum of 3.1–3.10) / 20 × 100
- **Text Quality Score** = (sum of 4.1–4.4 checks) / (max possible) × 100
- **Anti-Pattern Count** = number of BLOCKING flags detected

### 6.2 Overall Rating

| Score Range | Rating | Action |
|:------------|:-------|:-------|
| 85–100 | **STRONG** | Production-ready. Minor improvements possible. |
| 70–84 | **ADEQUATE** | Production-viable. Address MAJOR findings before next iteration. |
| 50–69 | **WEAK** | Not production-ready. Address BLOCKING findings. |
| <50 | **CRITICAL** | Fundamental restructure required. |

### 6.3 Output Format

```
# PROMPT AUDIT REPORT
**Audited:** [prompt/skill/template name]
**Date:** [YYYY-MM-DD]
**Auditor:** [agent name]

## Overall Rating: [STRONG/ADEQUATE/WEAK/CRITICAL] ([score]/100)

## Composite Scores
| Category | Score | Rating |
|:---------|:------|:-------|
| Architecture Patterns | XX/100 | ... |
| Agent Patterns | XX/100 | ... |
| Text Quality | XX/100 | ... |
| Anti-Patterns Found | N | ... |

## BLOCKING Issues
[List all anti-patterns and failed critical checks]

## MAJOR Issues (score 0 on high-weight checks)
[List with specific line/section references]

## MINOR Issues (score 1 on any check)
[List with recommendations]

## Improvement Recommendations (prioritized)
1. [Highest-impact change]
2. [Next-highest]
...

## Pattern Coverage Summary
[Table of all 19 patterns with scores and gaps]
```

---

## 7. SELF-VERIFICATION — Before Returning Audit

Before delivering the audit report, verify:

1. **Fabrication audit:** Did I invent any scores or findings without tracing them to specific prompt text? If yes, remove them.
2. **Evidence requirement:** Every BLOCKING/MAJOR finding must cite the specific line/section from the audited prompt.
3. **Completeness:** Did I check all 19 patterns? Cross-reference against the checklist.
4. **Calibration:** Are my scores realistic? A prompt that's been in production for months shouldn't score 30 — recalibrate if necessary.
5. **Actionability:** Can the prompt author act on every recommendation? If not, add specifics.

---

## 8. EMBEDDED SCRIPTS

This skill is self-contained — no external scripts required. All checks are manual/textual and performed by the agent using LLM reasoning.

---

*PROMPT-AUDIT Skill v1.1 — Self-audit for system prompts, skills, and templates against 19 industry patterns and anti-patterns. RED-TEAM-DOD integrated. Autonomous trigger on prompt modification. GIT: Skip. All output labeled [LLM-INFERRED].*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

