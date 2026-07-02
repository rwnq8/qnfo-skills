---
name: infographic-syntax-creator
description: Generate AntV Infographic syntax outputs. Use when asked to turn user content into the Infographic DSL (template selection, data structuring, theme), or to output `infographic <template>` plain syntax.
version: "1.1"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('infographic-syntax-creator')` or `read()` with filesystem path.
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

# INFOGRAPHIC SYNTAX CREATOR SKILL — v1.1

> **On-demand skill.** Load via `skill_view('infographic-syntax-creator')` for AntV Infographic DSL generation.

---

## When to Use

| Trigger | Action |
|:--------|:-------|
| "Create an infographic" | Full workflow below |
| "Visualize this data" | Identify best template, generate syntax |
| "Turn this into a comparison chart" | Use `compare-*` templates |

---

## Workflow — 5 Steps

### Step 1: Read Reference Rules

**MANDATORY:** Read `references/prompt.md` for syntax rules, template catalog, and output constraints before generating any output.

```python
read('references/prompt.md', base_directory=skill_root)
```

### Step 2: Extract User Content Structure

Analyze the user's input and identify:
- **Title**: Main topic/heading
- **Description**: Supporting context
- **Items**: List items, steps, features, metrics, or hierarchy
- **Relationships**: Comparisons, sequences, dependencies
- **Metrics**: Numbers, percentages, KPIs to highlight

Infer missing pieces conservatively — don't fabricate data.

### Step 3: Select Template

Match content structure to template type:

| Structure | Template |
|:----------|:---------|
| Linear sequence / steps | `sequence` |
| Bullet list / features | `list` |
| Two-way comparison | `compare-both` |
| A vs B (contrast) | `compare-A-vs-B` |
| Hierarchy / org chart | `hierarchy` |
| Metrics / KPI cards | `chart` |

### Step 4: Compose Syntax

Generate a single `infographic` markdown code block with these rules:

- First line: `infographic <template-name>`
- Two-space indentation
- Key/value pairs: `key value` (space-separated, no colon)
- Arrays: `- item` (dash-space)
- Compare templates: exactly two root nodes with children
- NO text outside the code block

### Step 5: Verify Output

Check before returning:
1. Single `infographic` code block only — no preamble, no markdown outside
2. First line is `infographic <template-name>` exactly
3. Consistent two-space indentation
4. Compare templates have exactly two root nodes
5. No fabricated data beyond what user provided

---

## Example Output

```
infographic list
title Key Features
desc Our platform offers the following capabilities
items
  - Real-time collaboration
  - Version control
  - Automated backups
  - Role-based access
theme professional
```

---

## Error Recovery

| Issue | Fix |
|:------|:----|
| Unclear content structure | Ask user to clarify: "Is this a list, comparison, or sequence?" |
| Unknown template needed | Default to `list` template |
| Missing title | Derive from first line of user content |
| User data contradicts template | Use template that matches, note data mismatch |

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|:-------------|:---------------|
| Adding explanatory text before/after code block | Output must be code block only |
| Using colons in key/value | Must be `key value`, not `key: value` |
| More than two root nodes in compare | Compare templates always A vs B |
| Fabricating metrics | Only include data user provides |
| Exporting without reading `references/prompt.md` first | Syntax rules may change |

---

## Reference Files

- `references/prompt.md` — **MANDATORY read:** syntax rules, template catalog, output constraints

---

*infographic-syntax-creator v1.1 — AntV Infographic DSL generation with template selection and format enforcement.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

