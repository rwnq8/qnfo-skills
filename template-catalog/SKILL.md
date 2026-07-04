---
name: template-catalog
description: Template discovery and parameter documentation. Use when the agent needs to find the right template for a task or check template parameters.
version: "1.1"
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** See RED-TEAM-PROTOCOL.md.



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('template-catalog')` or `read()` with filesystem path.
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

# TEMPLATE CATALOG SKILL — v1.1 — v1.1

> **On-demand skill.** Load via `skill_view('template-catalog')` to discover available templates.
> Source: `prompts.json` + `templates/` directory

---

## Available Templates (20 total)

### Core Project Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `PROJECT-INITIATION` | New project setup | `project_name`, `description`, `domain`, `moscow_analysis` |
| `PROJECT-CHARTER` | Project charter document | `project_name`, `scope`, `success_criteria`, `constraints` |
| `DEFINITION-OF-DONE` | Quality gates | `project_name`, `deliverable_type`, `acceptance_criteria` |
| `HANDOFF` | Agent-to-agent handoff | `type`, `scope`, `success_criteria`, `research_trail`, `return_protocol` |
| `DISCOVERY-PROTOCOL` | **Unified ecosystem discovery** | `scope`, `topic`, `project_name` |
| `BLING-USABILITY-AUDIT` | BLING UI usability audit | `project_name`, `url`, `screenshots` |

### Publication Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `ZENODO-PUBLISH` | Zenodo upload | `title`, `authors`, `description`, `keywords`, `file_path` |
| `PDF-BUILDER-TEMPLATE` (⚠️ DEPRECATED — migrated to pdf-builder skill v1.4) | PDF gen → use `skill_view("pdf-builder")` and run `build_pdf.py --input <file> --output <file>` | `source`, `output` (all other params handled by build_pdf.py CLI) |
| `SOCIAL-ORCHESTRATOR-TEMPLATE` | Social media posts | `publication_title`, `url`, `abstract`, `channels` |

### Operations Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `CLOUDFLARE-DEPLOYMENT` | Cloudflare deploy | `action`, `project_name`, `branch`, `domain` |
| `CLOUDFLARE-AUDIT-EXPORT` | Session audit export | `agent`, `session_date`, `summary`, `decisions`, `files_changed` |
| `CLOSEOUT-CHECKLIST` | Session close-out | `project_name`, `session_type` |
| `KAIZEN-AUDIT` | Kaizen improvement report | `health_score`, `total_findings`, `auto_applied_count` |
| `KAIZEN-AUTONOMOUS-UPDATE` | Autonomous system-wide update | `trigger_type`, `components`, `auto_apply` |
| `EMAIL-AGENT-TEMPLATE` | Email composition | `to`, `subject`, `body`, `cc`, `bcc`, `attachments` |

### Research Templates

| Template | Use For | Parameters |
|:---------|:--------|:-----------|
| `RESEARCH-LAUNCH` | Research pipeline launch | `topic`, `scope`, `output_type`, `priority` |
| `RESEARCH-PROTOCOL` | Research methodology protocol | `topic`, `methodology`, `sources` |
| `PHYSICS-STYLE` | Physics/technical writing style enforcement (18-rule checklist) | (none — self-contained) |

---
## How to Use Templates

```python
# Get template parameters
get_prompt_template_parameters(templateName="HANDOFF")

# Fill a template
fill_prompt_template("HANDOFF", {
    type: "Program->Project",
    scope: "Research quantum error correction...",
    success_criteria: "Peer-review-ready paper...",
    ...
})

# List all templates
list_all_prompt_template_names()
```

---

## Template Discovery

For full parameter documentation of any template:
```python
get_prompt_template_parameters(templateName="<name>")
```

All templates stored in: `R2 qnfo/prompts/templates/`
Template registry: `R2 qnfo/prompts/prompts.json`

---

## Common Patterns

### Session Lifecycle
```
(Start) → DISCOVERY-PROTOCOL → RESEARCH-LAUNCH → ... → CLOSEOUT-CHECKLIST → CLOUDFLARE-AUDIT-EXPORT
```

### Autonomous Update
```
KAIZEN-AUDIT → KAIZEN-AUTONOMOUS-UPDATE → deploy → commit → discovery-update
```

### New Project
```
PROJECT-INITIATION → PROJECT-CHARTER → DEFINITION-OF-DONE → README → HANDOFF
```

### Publication
```
pdf-builder (skill) → ZENODO-PUBLISH → CLOUDFLARE-DEPLOYMENT → SOCIAL-ORCHESTRATOR-TEMPLATE
```

### Session Lifecycle
```
(Start) → RESEARCH-LAUNCH → ... → CLOSEOUT-CHECKLIST → CLOUDFLARE-AUDIT-EXPORT
```

---

*template-catalog v1.1 — QNFO custom skill. Load on-demand via skill_view() for template discovery*

---

*template-catalog v1.1 — QNFO custom skill. Load via read('R2 `qnfo/prompts/skills/template-catalog\\SKILL.md'). Not accessible via skill_view().*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

