---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
version: "1.0"
license: Complete terms in LICENSE.txt
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.



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

## QNFO Design System Compliance (v3.0 — LOCKED 2026-07-01)

> **CRITICAL:** The user has locked the papers.qnfo.org design as THE canonical QNFO look and feel.
> **This section OVERRIDES all general frontend-design creative guidance for QNFO pages.**
> **For QNFO/QWAV pages: DO NOT be creative. MATCH the locked design exactly.**

### Scope

The locked design applies to:
- **papers.qnfo.org** (canonical — ALREADY MATCHES)
- **qnfo.org** (hub — MUST BE CONVERTED TO MATCH)
- **legal.qnfo.org** (MUST BE CONVERTED TO MATCH)
- **design.qnfo.org** (MUST BE CONVERTED TO MATCH)
- **archive.qnfo.org** (MUST BE CONVERTED TO MATCH)
- **All future QNFO/QWAV pages and publications**

This skill's general creative workflow (Phases 1-4) applies ONLY to non-QNFO artifacts.
For QNFO pages, the design is LOCKED — do not propose changes.

### Canonical Design Doc

The full design system specification is on R2:
```
npx wrangler r2 object get qnfo/design-system/QNFO-DESIGN-SYSTEM.md --remote --file=_design_system.md
```

### Locked Design Tokens (ABSOLUTE — DO NOT CHANGE)

```css
:root {
  --blue: #1a56db;        /* Links, buttons, brand accent */
  --blue-dark: #1040a8;   /* Hover states, h2 color */
  --blue-light: #dbeafe;  /* Borders, focus rings */
  --blue-subtle: #eff6ff; /* Backgrounds, blockquotes */
  --blue-mid: #6094e8;    /* Hover borders, filter pills */
  --text: #1a1a2e;        /* Body text, card headings */
  --text-muted: #6b7280;  /* Meta, nav, footer */
  --bg: #ffffff;          /* Page background */
  --border: #e5e7eb;      /* Card/table borders */
  --card-bg: #f9fafb;     /* Card bg, search input */
  --max-w: 960px;         /* Content width */
  --radius: 8px;          /* Border radius */
}
```

### Locked Fonts (ABSOLUTE — DO NOT CHANGE)

| Role | Font |
|:-----|:-----|
| Headings, nav, meta, badges | **Inter** (weights 400-700) |
| Body text | **Source Serif 4** (weights 400, 600, italic) |
| Code | JetBrains Mono / Fira Code / monospace |

**Font import URL:** `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap`

### Locked Components (MUST be present on all paper/research pages)

1. **Sticky Top Nav:** Backdrop-blur, Inter font, brand with blue accent, links: Index/Archive/QNFO Hub/AI Query
2. **AI Query Box:** Gradient `#eff6ff → #fff`, sparkle icon, input + button, opens ask.qwav.tech
3. **Related Papers Section:** Bordered cards with hover effect, paper title + author
4. **Paper Cards:** White bg, 1px border, hover shadow `0 2px 12px rgba(0,0,0,0.06)`
5. **Badges:** DOI (blue), Type (purple), Category (green), Tag (gray), License (orange)
6. **Search Input:** Full-width, search icon, blue focus ring `0 0 0 3px #dbeafe`
7. **Filter Pills:** Rounded, active = blue bg white text
8. **Footer:** Centered, border-top, muted text, Inter font

### Hard Rules

🚫 **DARK THEMES FORBIDDEN.** Light theme only.
🚫 **DO NOT change fonts.** Inter + Source Serif 4 are LOCKED.
🚫 **DO NOT change colors.** The blue palette is LOCKED.
🚫 **DO NOT change max-width.** 960px is LOCKED.
🚫 **DO NOT remove components.** AI Query box and Related Papers are MANDATORY.
🚫 **DO NOT apply Phase 1-4 creative workflow to QNFO pages.** Match the locked design instead.

### Verification

```bash
# Check any page for design compliance
python -c "import urllib.request;h=urllib.request.urlopen('URL').read().decode();print('DARK' if '#0a0a0f' in h or '#0d1117' in h else 'LIGHT')"
# Verify fonts: 'Source Serif 4' must be found in HTML
# Verify color token: '#1a56db' must be found in CSS
# Verify max-width: '960px' must be found in CSS
# Verify AI Query: 'ai-query' class must be found
# Verify Related Papers: 'related-section' class must be found
```

### Red-Team Self-Audit (Skill-Specific)

| Check | Criterion |
|:------|:----------|
| Font Audit | Inter + Source Serif 4 present, NO Roboto/Arial/system-ui as primary |
| Color Audit | `#1a56db` present, NO `#0a0a0f` or `#0d1117` |
| Component Audit | `.ai-query`, `.related-section`, `.topbar`, `.paper-card` present |
| Dark Theme Check | Page returns LIGHT |

Refer to RED-TEAM-PROTOCOL.md for full protocol.

