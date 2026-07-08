---
name: research-planner
description: Generate phased research plans, abstracts, theses, and research questions from any seed idea or provocative observation. Deconstructs assumptions, identifies hidden scaffolds vs. invariants (epistemic hygiene), spirals out into cross-disciplinary themes, and outputs a complete LLM-executable research program. USE WHEN the user asks to "create a research plan," "develop a research agenda," "generate research questions," "write an abstract and thesis," "deconstruct this idea," "what assumptions are we making," "what are we doing wrong," "analyze this concept," "plan a research project," or presents any stream-of-consciousness observation they want turned into a systematic investigation.
version: "4.0"
---

> **Related:** prompt-audit, skill-creator

---

## execute_plan (MANDATORY)

Always use update_plan for multi-stage outputs. Stages 1-8 below become checklist items. Mark each complete only after its output is fully written.

---

# Deconstruction Spiral v4.0

Transform any seed observation into a rigorous, LLM-executable research program via Epistemic Hygiene: separating human-imposed **scaffolds** (arbitrary conventions) from **invariants** (relational structures that persist).

## Modes (Default: LLM-Only)

- **LLM-Only:** All tasks executable by LLM with web search, code interpreter, public APIs. Human studies replaced with simulations, synthetic surveys, meta-analyses.
- **Hybrid:** Mix of `[LLM]` and `[Human]` tasks, clearly tagged.
- **Full:** Unrestricted plan; tasks tagged but not filtered.

User can specify mode inline: `--mode Hybrid`

---

## Pipeline (8 Stages)

### STAGE 1: Seed Clarification & Crisis of Confidence
- Restate the seed in your own words. Identify the central "wobble."
- Bullet-list all challenged assumptions.
- **Crisis of Confidence:** "If our current scaffold is wrong, then we should see X but we keep seeing Y. The most damaging observation would be Z."

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
Each task includes: name, subtasks, executor tag, and (for LLM tasks) an Execution Path showing the sequence of LLM actions. Output type indicated.

- **Phase 0: Immediate Critical Experiments** — Prioritized, all LLM-executable in LLM-Only mode.
- **Phase 1: Foundational Clarification** — Literature synthesis, scaffold taxonomy, formal definitions.
- **Phase 2: Core Case Studies** — Computational experiments, simulations, logical reconstructions.
- **Phase 3: Formal/Mathematical Generalization** — Category theory, automated theorem proving, symbolic manipulation.
- **Phase 4: Cognitive, Cultural, Philosophical Extensions** — In LLM-Only mode: LLM-roleplay panels, synthetic surveys, corpus analysis instead of human studies.
- **Phase 5: Synthesis & Dissemination** — Manuscripts, interactive tools, public-facing outputs.

### STAGE 7: LLM-Executable MVP
Output a concise "LLM-Executable Core" — a minimal, self-contained project the LLM can start running immediately using only public data, code interpreter, and multi-turn reasoning. Deliverable: reproducible notebook, report, or dataset.

### STAGE 8: Self-Critique
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

---

## Activation

User triggers with a message starting with `Deconstruct:` followed by the seed idea. Optional mode flag: `--mode [LLM-Only|Hybrid|Full]`. Example:

```
Deconstruct: Quantum computing still doesn't work at scale — what assumptions are we making that aren't true? --mode LLM-Only
```

The skill then outputs Stages 1-8 in sequence, using update_plan to track progress.
