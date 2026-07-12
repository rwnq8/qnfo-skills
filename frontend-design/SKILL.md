---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
version: "1.1"
license: Complete terms in LICENSE.txt
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('frontend-design')` or `read()` with filesystem path.
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

> **Related:** bling-usability-audit

---

## execute_plan (MANDATORY -- Before Any Execution)

**This skill involves execution-heavy workflows.** Before executing, use update_plan to populate a concrete, verifiable checklist. Every item must be short, specific, and testable with tool evidence.

### Execution Protocol

1. **Populate update_plan** with workflow phases as concrete checklist items
2. **Execute one item at a time** -- at most ONE in_progress
3. **Mark items completed ONLY with tool evidence** (Test-Path, exec output, git log)
4. **Never claim completion without execution evidence** -- Rule 14 enforcement
5. **If blocked:** Flag as [BLOCKED: reason] and move to the next item

### Example Plan

update_plan([
  {"step": "Define design requirements and aesthetic direction", "status": "pending"},
  {"step": "Create React/HTML/CSS component structure", "status": "pending"},
  {"step": "Implement distinctive visual design (no generic AI aesthetics)", "status": "pending"},
  {"step": "Add responsive layout and interactive states", "status": "pending"},
  {"step": "Run BLING usability audit on finished design", "status": "pending"}
])


# FRONTEND DESIGN SKILL — v1.0

> **On-demand skill.** Load via `skill_view('frontend-design')` for distinctive, production-grade UI creation.

---

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Build a landing page" | Full creative workflow |
| "Create a dashboard" | Data-focused UI with strong hierarchy |
| "Design a component" | Single-component creative design |
| "Style this page" | Aesthetic overlay on existing code |

---

## Workflow — 4 Phases

### Phase 1: Design Thinking & Concept

Before coding, understand context and commit to a **BOLD aesthetic direction**:

| Aspect | Question |
|:-------|:---------|
| **Purpose** | What problem does this interface solve? Who uses it? |
| **Tone** | Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian |
| **Constraints** | Technical requirements (framework, performance, accessibility) |
| **Differentiation** | What makes this UNFORGETTABLE? What's the one thing someone will remember? |

**CRITICAL:** Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

### Phase 2: Implementation

Implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

#### Typography
- Choose fonts that are beautiful, unique, and interesting
- Avoid generic fonts: Inter, Roboto, Arial, system fonts
- Pair a distinctive display font with a refined body font

#### Color & Theme
- Commit to a cohesive aesthetic
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes

#### Motion
- Use animations for effects and micro-interactions
- Prioritize CSS-only solutions for HTML. Use Motion library for React when available
- Focus on high-impact moments: one well-orchestrated page load with staggered reveals (`animation-delay`) creates more delight than scattered micro-interactions

#### Spatial Composition
- Unexpected layouts: asymmetry, overlap, diagonal flow, grid-breaking elements
- Generous negative space OR controlled density

#### Backgrounds & Visual Details
- Create atmosphere and depth rather than defaulting to solid colors
- Apply: gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, grain overlays

### Phase 3: Anti-Pattern Enforcement

**NEVER use these generic AI-generated aesthetics:**
- Overused font families: Inter, Roboto, Arial, system fonts, Space Grotesk
- Clichéd color schemes (especially purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design lacking context-specific character

### Phase 4: Verification

Before delivering:
1. **Uniqueness check:** Would another generation produce the same design? If yes, iterate.
2. **Tone check:** Does it match the chosen aesthetic direction?
3. **Functionality check:** Does the code actually work? (Test if possible)
4. **Variety rule:** Vary between light and dark themes, different fonts, different aesthetics across generations.

---

## Design Principles

- Interpret creatively and make unexpected choices that feel genuinely designed for the context
- Match implementation complexity to aesthetic vision:
  - Maximalist designs → elaborate code with extensive animations and effects
  - Minimalist/refined designs → restraint, precision, spacing, typography, subtle details
- Elegance comes from executing the vision well
- No design should be the same as previous generations

---

*frontend-design v1.0 — Distinctive, production-grade interfaces that avoid generic AI aesthetics.*

---

## Complex Artifacts (React) — Merged from web-artifacts-builder

For elaborate, multi-component artifacts requiring state management, routing, or shadcn/ui:

**Stack:** React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

```bash
# Initialize a React artifact project
bash scripts/init-artifact.sh <project-name>
cd <project-name>

# Develop the artifact (edit generated files)

# Bundle to single HTML file
bash scripts/bundle-artifact.sh
# → bundle.html (self-contained, all JS/CSS/inlined)
```

> **Platform Note:** Scripts use `bash`. Use Git Bash or WSL on Windows.

> **Version:** (Kaizen-audited 2026-07-08)
