---
name: research-planner
description: "Generates phased research plans, abstracts, theses, and research questions from a seed idea or provocative observation. Maps to standard research methodology— assumption analysis, hypothesis generation, literature gap identification, experimental design, and dissemination planning. Deconstructs assumptions to separate arbitrary conventions (scaffolds) from persistent relational structures (invariants), then spirals into cross-disciplinary themes. Outputs an LLM-executable research program in quick (3-stage) or full (7-stage) modes. USE WHEN the user asks to \"create a research plan,\" \"develop a research agenda,\" \"generate research questions,\" \"write an abstract and thesis,\" \"deconstruct this idea,\" \"what assumptions are we making,\" \"analyze this concept,\" \"plan a research project,\" says \"I have a weird thought about,\" \"I keep wondering whether,\" \"there is something off about,\" \"what if everything we think about,\" \"let us investigate,\" or presents a stream-of-consciousness observation they want turned into a systematic investigation. NOT for: literature-only searches, citation formatting, code debugging, factual QA, or tasks requiring physical lab access."
version: "5.0"
---

> **Related:** deep-research, prompt-audit, skill-creator, literature-search, citation-manager, red-team-dod, publication-publisher

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

---

## Genre-Bridging Preamble (READ THIS FIRST)

**If you're here because you need a research plan:** This skill is a structured idea-development framework. It does what a research methodology course teaches — assumption analysis, hypothesis generation, literature gap identification, experimental design, dissemination planning — but compressed into an LLM-executable pipeline. The vocabulary is non-standard (see translation table below) but the operations map directly to conventional research planning.

**If you're here because you already know the vocabulary:** Skip to the Decision Tree.

**This skill does NOT generate genuinely novel discoveries.** It remixes and reorganizes existing knowledge into exploration frameworks. Treat its outputs as scaffolding for human creativity, not as finished research. All claims carry source labels: [LLM-INFERRED], [WEB-SEARCH], or [CODE-EXECUTED].

---

## When NOT to Use This Skill

| Your Need | Use This Instead |
|:----------|:-----------------|
| Search for existing papers on a topic | `literature-search` skill |
| Format citations or build a bibliography | `citation-manager` skill |
| Debug code or fix a script | Standard code interpreter |
| Answer a factual question | Standard LLM capabilities |
| Conduct a physical experiment | Not LLM-executable — requires `[Human]` tags in Hybrid mode |
| Generate a simple list of ideas | Overkill — just ask directly |

---

## Vocabulary Translation Table

This skill uses specialized terms. Here's what they mean in standard research-methodology language:

| This Skill's Term | Standard Equivalent | Definition |
|:------------------|:--------------------|:-----------|
| **Deconstruction Spiral** | Structured idea-development / research planning framework | An 8-stage pipeline that separates arbitrary conventions from persistent structures. Equivalent to: assumption audit → gap analysis → hypothesis generation → experimental design → dissemination |
| **Scaffold** | Arbitrary convention / modeling choice | Any human-imposed convention in a representation system (base, origin, coordinate, unit, formalism, notation) |
| **Invariant** | Persistent structure / robust finding | The relational, structural, or quantitative property that persists when conventions are varied or removed |
| **Epistemic Hygiene** | Assumption audit / robustness check | Method: (1) identify all arbitrary conventions in a model, (2) systematically vary or remove them, (3) express the idea purely in terms of persistent structures |
| **Map-Territory Confusion** | Reification error / category mistake | Mistaking the representation convention (map) for the reality it represents (territory) |
| **Deconstruction Table** | Assumption analysis matrix | Systematic comparison of current conventions, alternatives, and persistent structures across key concepts |
| **Crisis of Confidence** | Falsification condition | What observation would force you to abandon the current framework entirely |

---

## Decision Tree: Which Mode?

```
You have a seed idea. How committed are you?

├─ Just exploring, 2 min → --quick (3 steps, ~2K tokens)
│   Output: 3 challenged assumptions + 2 critical tests + 3 next steps
│
├─ Serious investigation → Full (7 stages, ~8-12K tokens)
│   Output: Complete research program with phased plan
│
└─ Need human-involved tasks → Add --mode Hybrid or --mode Full
```

| Mode | Token Cost (approx.) | Output | Best For |
|:-----|:---------------------|:-------|:---------|
| `--quick` | ~2,000 | 3 assumptions + 2 tests + 3 steps | First exploration, time-pressed users |
| Full (default) | ~8,000–12,000 | 7-stage research program | Serious investigation, paper/proposal development |
| `--self-critique` | +~500 | Stage 8 blind-spot analysis | When you want the framework to critique itself |
| `--mode Hybrid` | Same as Full | Tasks tagged [LLM] or [Human] | Research involving physical experiments or human subjects |
| `--mode Full` | Same as Full | Unrestricted plan | When human tasks are acceptable |

**Recommended for first-time users:** Start with `--quick`. If the output is useful, re-run in Full mode on the same seed.

---

## execute_plan (MANDATORY — Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** — at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** — Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Verification

- **Content quality:** Verify each stage output exists as markdown in the response (not a claim in memory)
- **Plan completeness:** All stages have verifiable output
- **Source labels:** All claims carry [LLM-INFERRED], [WEB-SEARCH], or [CODE-EXECUTED] labels
- **Seed quality gate:** Verify pre-stage gate passed (no category errors detected)
- **Output saved:** If writing to file — `Test-Path <output_file>` must return True

---

## QUICK MODE (Recommended First Experience)

**Trigger:** Add `--quick` flag. Output: 3 assumptions challenged + 2 critical tests + 3 next steps.

### Example Plan (Quick Mode)

```python
update_plan([
  {"step": "Stage 1: Identify 3 challenged assumptions", "status": "pending"},
  {"step": "Stage 2: Define 2 critical tests", "status": "pending"},
  {"step": "Stage 3: Generate 3 next steps", "status": "pending"},
])
```

**`--quick` mode is 2x token-efficient.** No deconstruction table, no thematic spiral, no phased plan. Use for time-pressed practitioners, quick explorations, and first encounters with the skill.

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

# Deconstruction Spiral v5.0

A structured idea-development framework that separates arbitrary conventions (scaffolds) from persistent relational structures (invariants). Maps to standard research methodology: assumption audit → gap analysis → hypothesis generation → experimental design → dissemination.

---

## Modes

**Scope modes** (default: LLM-Only — specify with `--mode`):
- **LLM-Only:** All tasks executable by LLM with web search, code interpreter, public APIs.
- **Hybrid:** Mix of `[LLM]` and `[Human]` tasks, clearly tagged.
- **Full:** Unrestricted plan; tasks tagged but not filtered.

**Depth modes:**
- **`--quick`:** Minimal Baseline — 3 assumptions, 2 critical tests, 3 next steps. ~2K tokens. **Recommended for first-time users and quick explorations.**
- **Full (default):** Complete 7+1 stage pipeline. ~8-12K tokens. For serious investigations.
- **`--self-critique`:** Enabled by default in v5.0. Adds Stage 8 blind-spot analysis. Use `--no-self-critique` to disable.

---

## Pipeline (8 Stages, including Stage 0 and Stage 8)

### STAGE 0: Expectation Setting (NEW in v5.0)
Before the pipeline begins, orient the user:
- **What you'll get:** Brief summary of each upcoming stage in 1 sentence
- **Estimated output length:** Approximate token count
- **How to use the output:** Suggested next actions after the pipeline completes
- **Abort condition:** "If at any point the output stops being useful, say 'stop' and I'll give you the summary so far"

**Pre-Stage Gate: Seed Quality Check.** Before executing Stage 1, scan the seed for nonsense patterns:
- **Category errors:** Applying a predicate to the wrong type of entity (e.g., "What color is justice?")
- **Category fusion:** Conflating distinct ontological categories (e.g., treating a measurement as the thing measured)
- **Non-applicable predicates:** Asking about properties that don't apply to the subject

If the seed is fundamentally untestable or rests on a category error, output `[SEED-QUALITY-WARNING: <specific category error>]` and explain why. Offer to help reframe. Only proceed if the seed identifies a genuine conceptual tension.

**Examples of seeds that PASS:**
- "Why does the placebo effect work?" → genuine causal question, testable (PASS)
- "Is dark matter a convention rather than a substance?" → challenges an ontological assumption (PASS)
- "What if peer review optimizes for conformity rather than truth?" → falsifiable institutional claim (PASS)

**Examples of seeds that FAIL:**
- "What is the meaning of life?" → not a research question, no falsification pathway (FAIL — category error: treating normative question as empirical)
- "Prove that consciousness is quantum." → presupposes conclusion, not an open investigation (FAIL — non-applicable predicate: 'proof' applied to speculative domain)

### STAGE 1: Seed Clarification & Crisis of Confidence
- Restate the seed in your own words. Identify the central tension.
- Bullet-list all challenged assumptions, each tagged with source confidence: [LLM-INFERRED], [WEB-SEARCH], or [CODE-EXECUTED].
- **Crisis of Confidence:** "If our current framework is wrong, then we should see X but we keep seeing Y. The most damaging observation would be Z." **This must be genuinely bold — specify what observation would force you to abandon the framework entirely.** Performative crises (e.g., "however, the approach is sound") violate this requirement.
- **Digest:** End with a 1-sentence summary of this stage's key finding.

### STAGE 2: Emergent Domain Identification
- Analyze the seed and generate 3-5 thematic lenses that naturally arise from it. Do NOT force a fixed five; let the seed suggest its own domains.
- For each lens, name the relevant academic discipline or methodology it connects to.
- **Digest:** 1-sentence summary of cross-domain connections found.

### STAGE 3: Deconstruction Table
| Concept | Scaffold (Current Convention) | Alternative Convention | Invariant (Persistent Structure) | Reification Error | How I Might Mislead Here |
|---------|-------------------------------|------------------------|----------------------------------|-------------------|---------------------------|
| ... | ... | ... | ... | ... | ... |

Follow with a narrative synthesis paragraph connecting all rows.

**Worked Example — Seed: "Peer review optimizes for conformity, not truth"**

| Concept | Scaffold (Current Convention) | Alternative Convention | Invariant (Persistent Structure) | Reification Error | How I Might Mislead Here |
|---------|-------------------------------|------------------------|----------------------------------|-------------------|---------------------------|
| "Quality" | Reviewer agreement = quality signal | Citation impact after 5 years = quality signal | The work's ability to generate true predictions over time | Confusing inter-rater reliability with validity | Assuming reviewer agreement always indicates low quality — sometimes consensus is correct |
| "Reviewer" | Anonymous gatekeeper with domain expertise | Transparent collaborator with diverse expertise | Someone who assesses whether claims are supported by evidence | Confusing role identity (reviewer) with function (evidence assessment) | Romanticizing "diverse expertise" — domain expertise is genuinely useful |
| "Acceptance" | Binary decision at one journal | Continuous publication with post-hoc curation | Whether the work eventually influences the field's understanding | Confusing venue prestige with contribution value | Implying all rejected papers are valuable — most rejected papers are genuinely flawed |
| "Novelty" | Departure from existing literature | Problem-solving power regardless of novelty | Whether the work enables new predictions or explanations | Confusing "looks different" with "is different" | Equating novelty with value — some novel ideas are false |

*Narrative synthesis: The invariant that persists across all four concepts is **predictive or explanatory power over time**, not any specific institutional mechanism. The current peer review system is one possible instantiation of evidence assessment; alternative instantiations (post-publication review, registered reports, prediction markets) may serve the same invariant function with different tradeoffs. The primary reification error is confusing the current institutional form of peer review with the function it serves.*

- **Digest:** 1-sentence summary of the core invariant discovered.

### STAGE 4: Thematic Spiraling with Critical Tests
For each emergent domain from Stage 2, write:
- One paragraph exploring implications.
- **Critical Test:** A concrete, falsifiable test the LLM can execute. Tag: `[LLM-executable via: <specific tool/API/method>]`. Must specify: input, expected output under null hypothesis, and what would constitute a surprising result.
- **Digest:** 1-sentence summary of most surprising predicted finding.

### STAGE 5: Abstract, Thesis, Research Questions
- **Abstract:** One paragraph: seed insight, method, key invariant(s), broader significance. Write in standard academic abstract format so it can be directly reused.
- **Thesis:** Bold single sentence: "[The conventional view] is not [what it seems]; the genuine contact with reality is [the invariant]."
- **Research Questions:** 6-10, each tagged with domain and Executor: `[LLM]`, `[Human]`, `[Human+LLM]`. In LLM-Only mode, all must be `[LLM]`.
- **Digest:** Thesis statement alone.

### STAGE 6: Phased Research Plan
**Match plan complexity to seed complexity — simple seeds get 2-3 phases, complex seeds get all 6. Do not inflate.**

Each task includes: name, subtasks, executor tag, and (for LLM tasks) an Execution Path showing the sequence of LLM actions.

- **Phase 0: Immediate Critical Experiments** — Prioritized, all LLM-executable in LLM-Only mode.
- **Phase 1: Foundational Clarification** — Literature synthesis, convention taxonomy, formal definitions.
- **Phase 2: Core Case Studies** — Computational experiments, simulations, logical reconstructions.
- **Phase 3: Formal/Mathematical Generalization** — Category theory, automated theorem proving, symbolic manipulation.
- **Phase 4: Cognitive, Cultural, Philosophical Extensions** — In LLM-Only mode: LLM-roleplay panels, synthetic surveys, corpus analysis.
- **Phase 5: Synthesis & Dissemination** — Manuscripts, interactive tools, public-facing outputs.
- **Digest:** Total number of phases and tasks, with executor tag distribution.

### STAGE 7: LLM-Executable MVP
Output a concise "LLM-Executable Core" — Phase 0 extracted into a standalone, self-contained project the LLM can start running immediately. Deliverable: reproducible notebook, report, or dataset. If Phase 0 already serves as the MVP, note this and skip.
- **Digest:** What the MVP produces and how to run it.

### STAGE 8: Self-Critique (ON BY DEFAULT in v5.0)
> **Use `--no-self-critique` to disable.**

Section: **"What This Plan Likely Misses (And When To Ignore It)"** — list blind spots:
1. **Physical reality constraints:** What tacit, embodied, or physical knowledge is missing?
2. **Alternative frameworks:** What other approaches would reach different conclusions?
3. **Scaffolding risk:** Is there a possibility that the entire framework adds conventions rather than removing them?
4. **When to ignore this critique:** Under what conditions is the plan sound despite these blind spots?

---

## Common Failure Modes & Remedies

| Stage | Common Failure | Why It Happens | Remedy |
|:------|:---------------|:---------------|:-------|
| **Pre-Stage Gate** | Letting through untestable seeds disguised as profound | The seed sounds deep but can't be operationalized | Ask: "What observation would falsify this?" If none, reject |
| **Stage 1** | Performative crisis of confidence | Avoiding genuinely bold falsification conditions | The crisis must name a specific, observable event that would force abandonment |
| **Stage 2** | Forcing exactly 5 lenses when fewer are natural | Template compliance over genuine analysis | Accept 3-4 lenses if that's what the seed genuinely suggests |
| **Stage 3** | Filling the table with trivial or obvious entries | The table format incentivizes quantity over quality | Each row must challenge at least one non-obvious assumption |
| **Stage 4** | Critical tests that can't fail ("test if X exists" with no null hypothesis) | Avoiding falsifiable predictions | Every test must specify: null hypothesis, expected result under null, what counts as surprising |
| **Stage 5** | Safe thesis statements that nobody would dispute | Risk aversion | The thesis must be falsifiable — someone reasonable should be able to disagree |
| **Stage 6** | Inflating plan complexity for simple seeds | Template compliance | Match phases to seed complexity; simple seeds get 2-3 phases |
| **Stage 7** | MVP that requires resources the user doesn't have | Forgetting scope constraints | MVP must be executable with LLM + free public APIs only |
| **Stage 8** | Dismissive self-critique ("these are minor issues") | Defensiveness about the generated plan | Each blind spot must be genuine — if you can't find any, you're not looking hard enough |

---

## Interactive Refinement (After First Output)

User can refine with commands like:
- "Switch to Hybrid mode, add human studies."
- "Output only the LLM-Executable MVP."
- "Simulate the first critical experiment now."
- "Refine Phase 2 with more rigorous code."
- "Make the thesis more radical."
- "The thesis is too safe. Make it bolder — what's the strongest version of this claim?"
- "Apply the deconstruction table to one of my research questions."
- "Convert the whole plan to a single-page executive summary."
- "Cross-reference Stage 6 tasks with literature-search skill."
- "What would a hostile reviewer say about this plan? Simulate their critique."
- "Generate 3 alternative theses that a different school of thought would propose."
- "Quantify the expected effect sizes for Phase 0 experiments."
- "Add a timeline estimate (days/weeks) to each Phase 0 task."
- "Which of my assumptions is least supported by evidence? Flag it."

---

## Key Definitions (Embedded Reference)

- **Scaffold:** Any arbitrary human convention in a representation system (base, origin, qubit, gate, epoch, coordinate, unit, etc.). Equivalent to: modeling choice, representational convention, arbitrary parameterization.
- **Invariant:** The relational, structural, or quantitative property that persists when conventions are varied or removed. Equivalent to: robust finding, persistent structure, convention-independent property.
- **Epistemic Hygiene:** Method: (1) identify all arbitrary conventions in a model, (2) systematically vary or remove them, (3) express the idea purely in terms of persistent structures. Demand falsifiability: every convention removal must lead to a testable consequence. Equivalent to: assumption audit, robustness check, sensitivity analysis.
- **Map-Territory Confusion:** Mistaking the representational convention (map) for the reality it represents (territory). Equivalent to: reification error, category mistake, confusing measurement with measured.

---

## Scope Constraint

This skill is an LLM-native tool. It cannot recruit humans, run physical labs, or access proprietary databases. Tasks requiring these are either replaced by computational surrogates (LLM-Only) or clearly labeled `[Human]` (Hybrid/Full). Execution Paths for all `[LLM]` tasks must describe concrete tool actions (e.g., "Search arXiv for X, write Python to extract Y, synthesize into table").

**Novelty limitation:** As an LLM, this skill generates exploration frameworks — structured ways to investigate a question — not genuinely novel discoveries. It remixes and reorganizes existing knowledge. Treat its outputs as scaffolding for human creativity, not as finished research.

---

## Where This Fits in Research Methodology

This skill maps to standard phases of the research process:

| Standard Research Phase | This Skill's Equivalent | Output |
|:------------------------|:------------------------|:-------|
| Problem formulation | Stage 1: Seed Clarification | Challenged assumptions + crisis of confidence |
| Literature review / gap analysis | Stage 2: Domain Identification + Stage 3: Deconstruction | Cross-disciplinary lenses + convention-invariant analysis |
| Hypothesis generation | Stage 4: Thematic Spiraling + Stage 5: Thesis | Critical tests + thesis statement |
| Research design | Stage 6: Phased Research Plan | Task-sequenced plan with executor tags |
| Pilot study / feasibility | Stage 7: LLM-Executable MVP | Runnable experiment or dataset |
| Peer review / limitations | Stage 8: Self-Critique | Blind-spot analysis |

**Downstream integration:** After this skill completes, feed its output to:
- `literature-search` → For gap-filling literature on identified domains
- `citation-manager` → For formatting references in the research plan
- `prompt-audit` → For quality-checking the generated research questions

---

## Related Frameworks & References

This skill draws on (but does not require knowledge of) the following traditions:

| Framework | Connection to This Skill |
|:----------|:-------------------------|
| **Kuhn's paradigm shifts** (1962) | Pre-stage gate identifies when a seed challenges normal science assumptions |
| **Design Science Research** (Hevner et al., 2004) | Stage 7 MVP maps to design science artifact creation |
| **Grounded Theory** (Glaser & Strauss, 1967) | Stage 1-3 mirrors grounded theory's open coding and constant comparison |
| **TRIZ / Systematic Innovation** (Altshuller) | Deconstruction table mirrors contradiction matrix analysis |
| **Action Research** (Lewin, 1946) | Phase 0 critical experiments mirror action research cycles |
| **Boundary Objects** (Star & Griesemer, 1989) | Stage 2 domain identification maps to boundary object creation across disciplines |
| **Epistemic Vigilance** (Sperber et al., 2010) | Source labels [LLM-INFERRED]/[WEB-SEARCH]/[CODE-EXECUTED] implement epistemic vigilance |

---

## Activation

User triggers with a message starting with `Deconstruct:` followed by the seed idea. Flags (all optional):

```
Deconstruct: <seed> --mode [LLM-Only|Hybrid|Full] --quick --no-self-critique
```

Examples:
- `Deconstruct: Why does the placebo effect work? --quick` → Minimal Baseline (3+2+3). **Recommended first experience.**
- `Deconstruct: Is dark matter a convention? --mode LLM-Only` → Full 8-stage, LLM-Only
- `Deconstruct: What assumptions underlie peer review?` → Full 8-stage, LLM-Only, self-critique included
- `Deconstruct: How should we redesign clinical trials? --mode Hybrid --no-self-critique` → Hybrid, 7 stages

The skill outputs Stages 0-8 in sequence, using update_plan to track progress.

---

> **Version:** v5.0 — Kaizen-audited 2026-07-09. Self-applied deconstruction methodology. Changelog: Added genre-bridging preamble, vocabulary translation, when-NOT-to-use, decision tree, token cost estimates, Stage 0 expectation setting, digest summaries, improved pre-stage gate examples, self-critique on by default, methodology integration table, and external references.
