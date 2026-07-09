---
name: research-planner
description: Generate phased research plans, abstracts, theses, and research questions from any seed idea or provocative observation. Deconstructs assumptions, identifies hidden scaffolds vs. invariants (epistemic hygiene), spirals out into cross-disciplinary themes, and outputs a complete LLM-executable research program. USE WHEN the user asks to "create a research plan," "develop a research agenda," "generate research questions," "write an abstract and thesis," "deconstruct this idea," "what assumptions are we making," "what are we doing wrong," "analyze this concept," "plan a research project," says "I have a weird thought about," "I keep wondering whether," "there's something off about," "what if everything we think about," "let's investigate," or presents any stream-of-consciousness observation they want turned into a systematic investigation.
version: "4.5"
---

> **Related:** prompt-audit, skill-creator

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

---

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('research-planner')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [On-demand — loads when triggered by task patterns].

### Skill Loading Retry Protocol
If `skill_view('name')` fails during programmatic loading, the LLM system 
MUST execute this fallback chain:
1. **Retry 1:** `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. **Retry 2:** Pull from Cloudflare R2: `npx wrangler r2 object get 
   qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md`
3. **Retry 3:** If R2 fails, search local filesystem for any cached copy
4. **Fallback:** If ALL retries fail, continue with `[SKILL-UNAVAILABLE: <name>]` 
   and best-effort knowledge
**NEVER silently proceed without a skill's critical instructions.** If a skill 
is required for the task and cannot be loaded after 3 retries, escalate to 
the user with the specific failure reason.

---

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan (Full Mode)

```python
update_plan([
  {"step": "Stage 1: Seed Clarification & Crisis of Confidence", "status": "pending"},
  {"step": "Stage 2: Emergent Domain Identification (3-5 lenses)", "status": "pending"},
  {"step": "Stage 3: Deconstruction Table + Narrative Synthesis", "status": "pending"},
  {"step": "Stage 4: Thematic Spiraling with Critical Tests", "status": "pending"},
  {"step": "Stage 5: Abstract, Thesis, Research Questions (6-10)", "status": "pending"},
  {"step": "Stage 6: Phased Research Plan (Phase 0 first)", "status": "pending"},
  {"step": "Stage 7: LLM-Executable MVP (standalone project)", "status": "pending"},
])
```

### Example Plan (Quick Mode)

```python
update_plan([
  {"step": "Stage 1: Identify 3 challenged assumptions", "status": "pending"},
  {"step": "Stage 2: Define 2 critical tests", "status": "pending"},
  {"step": "Stage 3: Generate 3 next steps", "status": "pending"},
])
```

### Verification

- **Content quality:** Verify each stage output exists as markdown in the response (not a claim in memory)
- **Plan completeness:** All 7 stages (or 3 for quick mode) have verifiable output
- **Source labels:** All claims carry [LLM-INFERRED], [WEB-SEARCH], or [CODE-EXECUTED] labels
- **Seed quality gate:** Verify pre-stage gate passed (no category errors detected)
- **Output saved:** If writing to file — `Test-Path <output_file>` must return True

**Stages 1-7 below become checklist items (Stage 8 optional with --self-critique). Mark each complete only after its output is fully written.**

---

# Deconstruction Spiral v4.0

Transform any seed observation into a rigorous, LLM-executable research program via Epistemic Hygiene: separating human-imposed **scaffolds** (arbitrary conventions) from **invariants** (relational structures that persist).

## Modes

**Scope modes** (default: LLM-Only — specify with `--mode`):
- **LLM-Only:** All tasks executable by LLM with web search, code interpreter, public APIs.
- **Hybrid:** Mix of `[LLM]` and `[Human]` tasks, clearly tagged.
- **Full:** Unrestricted plan; tasks tagged but not filtered.

**Depth modes** (default: Full — specify with `--quick` or `--self-critique`):
- **Full (default):** Complete 7-stage pipeline. Highest quality, highest token cost.
- **--quick:** Minimal Baseline — 3 assumptions, 2 critical tests, 3 next steps. 2x token-efficient.
- **--self-critique:** Adds optional Stage 8 self-critique section. Off by default (ablation study: +0.0 quality, costs ~40 tokens).

---

## Pipeline (7 Stages, +1 optional with --self-critique)

**Pre-Stage Gate: Seed Quality Check.** Before executing Stage 1, scan the seed for nonsense patterns (category errors, category fusion, non-applicable predicates). If the seed is fundamentally untestable or rests on a category error, output `[SEED-QUALITY-WARNING: category error detected]` and stop. Only proceed if the seed identifies a genuine conceptual tension.

### STAGE 1: Seed Clarification & Crisis of Confidence
- Restate the seed in your own words. Identify the central "wobble."
- Bullet-list all challenged assumptions.
- **Crisis of Confidence:** "If our current scaffold is wrong, then we should see X but we keep seeing Y. The most damaging observation would be Z." **This must be genuinely bold — if the crisis is safe and would never actually endanger the plan (e.g., 'however, the approach is sound'), it is performative scaffolding. A good crisis should specify what observation would force you to abandon the plan entirely.**

### STAGE 2: Emergent Domain Identification
- Analyze the seed and generate 3-5 thematic lenses that naturally arise from it. Do NOT force a fixed five; let the seed suggest its own domains.

### STAGE 3: Deconstruction Table
| Concept | Scaffold (Current) | Alternative Scaffold | Invariant | Map-Territory Confusion | How I Might Mislead Here |
|---------|---------------------|----------------------|-----------|--------------------------|---------------------------|
| ... | ... | ... | ... | ... | ... |

Follow with a narrative synthesis paragraph.

### STAGE 4: Thematic Spiraling with Critical Tests
For each emergent domain from Stage 2, write:
- One paragraph exploring implications.
- **Critical Test:** A concrete test the LLM can execute (computational experiment, literature synthesis, logic check, self-play dialogue). Tag: `[LLM-executable via: ...]`

### STAGE 5: Abstract, Thesis, Research Questions
- **Abstract:** One paragraph: seed insight, method, key invariant(s), broader significance.
- **Thesis:** Bold single sentence: "[The obvious thing] is not [what people think]; the genuine contact with reality is [the invariant]."
- **Research Questions:** 6-10, each tagged with domain and Executor: `[LLM]`, `[Human]`, `[Human+LLM]`. In LLM-Only mode, all must be `[LLM]`.

### STAGE 6: Phased Research Plan (6 Phases, Phase 0 first)
Each task includes: name, subtasks, executor tag, and (for LLM tasks) an Execution Path showing the sequence of LLM actions. Output type indicated. **Match plan complexity to seed complexity — simple seeds get 2-3 phases, complex seeds get all 6. Do not inflate.**

- **Phase 0: Immediate Critical Experiments** — Prioritized, all LLM-executable in LLM-Only mode.
- **Phase 1: Foundational Clarification** — Literature synthesis, scaffold taxonomy, formal definitions.
- **Phase 2: Core Case Studies** — Computational experiments, simulations, logical reconstructions.
- **Phase 3: Formal/Mathematical Generalization** — Category theory, automated theorem proving, symbolic manipulation.
- **Phase 4: Cognitive, Cultural, Philosophical Extensions** — In LLM-Only mode: LLM-roleplay panels, synthetic surveys, corpus analysis instead of human studies.
- **Phase 5: Synthesis & Dissemination** — Manuscripts, interactive tools, public-facing outputs.

### STAGE 7: LLM-Executable MVP
Output a concise "LLM-Executable Core" — essentially Phase 0 extracted into a standalone, self-contained project the LLM can start running immediately. Deliverable: reproducible notebook, report, or dataset. If Phase 0 already serves as the MVP, note this and skip.

### STAGE 8 (OPTIONAL — only with --self-critique flag): Self-Critique
> **Ablation study finding:** Stage 8 adds +0.0 quality for ~40 tokens. Off by default. Enable with `--self-critique`.
Section: **"What This Plan Likely Misses (And When To Ignore It)"** — list blind spots, especially regarding physical reality, tacit knowledge, embodied experience, and the possibility that the entire framework adds scaffolding rather than removing it.

---

## Interactive Refinement (After First Output)

User can refine with commands like:
- "Switch to Hybrid mode, add human studies."
- "Output only the LLM-Executable MVP."
- "Simulate the first critical experiment now."
- "Refine Phase 2 with more rigorous code."
- "Make the thesis more radical."

Respond by updating the relevant section and re-outputting if requested.

---

## Key Definitions (Embedded Reference)

- **Scaffold:** Any arbitrary human convention in a representation system (base, origin, qubit, gate, epoch, coordinate, unit, etc.).
- **Invariant:** The relational, structural, or quantitative property that persists when scaffolds are varied or removed.
- **Epistemic Hygiene:** Method: (1) identify all scaffolds in a model, (2) systematically vary or remove them, (3) express the idea purely in terms of invariants. Demand falsifiability: every scaffold removal must lead to a testable consequence.
- **Map-Territory Confusion:** Mistaking the scaffold (map) for reality (territory).

---

## Scope Constraint

This skill is an LLM-native tool. It cannot recruit humans, run physical labs, or access proprietary databases. Tasks requiring these are either replaced by computational surrogates (LLM-Only) or clearly labeled `[Human]` (Hybrid/Full). Execution Paths for all `[LLM]` tasks must describe concrete tool actions (e.g., "Search arXiv for X, write Python to extract Y, synthesize into table").

**Novelty limitation:** As an LLM, this skill generates exploration frameworks — structured ways to investigate a question — not genuinely novel discoveries. It remixes and reorganizes existing knowledge. Treat its outputs as scaffolding for human creativity, not as finished research.

---

## Activation

User triggers with a message starting with `Deconstruct:` followed by the seed idea. Flags (all optional):

```
Deconstruct: <seed> --mode [LLM-Only|Hybrid|Full] --quick --self-critique
```

Examples:
- `Deconstruct: Why does the placebo effect work? --quick` → Minimal Baseline (3+2+3)
- `Deconstruct: Is dark matter a scaffold? --mode LLM-Only --self-critique` → Full 7-stage + Stage 8
- `Deconstruct: What assumptions underlie peer review?` → Full 7-stage, LLM-Only, no self-critique

**--quick mode output format:** 3 assumptions challenged + 2 critical tests + 3 next steps. No deconstruction table, no thematic spiral, no phased plan. Designed for 2x token efficiency. **Recommended for time-pressed practitioners, quick explorations, and first-time users.**

The skill outputs Stages 1-7 in sequence (plus optional Stage 8), using update_plan to track progress.

> **Version:** (Kaizen-audited 2026-07-08)
