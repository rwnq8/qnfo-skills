---
name: infographic-syntax-creator
description: Generate AntV Infographic syntax outputs. Use when asked to turn user content into the Infographic DSL (template selection, data structuring, theme), or to output `infographic <template>` plain syntax.
version: "1.1"
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
