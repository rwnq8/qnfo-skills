---
name: skill-autoloader
description: AUTOMATICALLY loads relevant QNFO skills based on task detection. User NEVER manually loads skills. Cross-references all skills. Handles fallback when skill_view() fails.
pinned: true
---

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('skill-autoloader')` or `read()` with filesystem path.
**The user NEVER manually loads this skill.** The `skill-autoloader` 
detects task patterns and handles all skill loading. If this skill fails 
to load, the LLM system automatically retries via the fallback chain 
documented below.
**Pinning:** This skill is [Priority 0 — always active, cannot be disabled].

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


# SKILL AUTO-LOADER -- v2.0

> **PRIORITY 0 — pinned, always active. User NEVER manually loads skills.**

## Purpose

The LLM system automatically detects what skills are needed for any task and loads them without user prompting. The user should NEVER say "load the cloudflare-deployer skill" — the LLM detects the task and loads it.

## Core Rules

### Rule 1: Auto-Detect by Task Pattern

When the user's message or the LLM's planned task matches a pattern, auto-load the relevant skill:

| Task Pattern | Auto-Load |
|-------------|-----------|
| deploy, upload, wrangler, Pages, Workers, R2, D1, DNS, KV, Vectorize, Queues, Cloudflare | `cloudflare-deployer` |
| publish, Zenodo, DOI, PDF, paper, manuscript, LaTeX | `publication-publisher` |
| close out, terminate, done, session end, HANDOFF, handoff | `closeout-manager` |
| git error, detached HEAD, merge conflict, rebase | `git-hygiene` |
| email, send, Outlook, compose | `email-composer` |
| PDF build, convert markdown, LaTeX compile | `pdf-builder` (via cloudflare-deployer) |
| knowledge graph, KG, graph-api, dependencies, impact, neighbors, nodes, edges | `knowledge-graph` |
| audit, infrastructure, health check, orphan, stale, lifecycle | `infrastructure-audit` |
| UI, design, frontend, page, styling, BLING, visual | `bling-usability-audit` |
| research, paper search, literature, arXiv, Semantic Scholar | `literature-search` |
| SEO, sitemap, robots.txt, discoverability, llms.txt | `seo-discoverability` |
| Kaizen, improve, update system, deploy prompts | `kaizen-autonomous-update` |
| skill sync, backup skills, restore skills | `skill-sync` |
| cite, citation, BibTeX, bibliography | `citation-manager` |
| social media, tweet, post, Buffer, LinkedIn, Bluesky | `buffer-integration` |
| template, fill_prompt_template | `template-catalog` |
| migrate, local to R2, cleanup, thin client | `local-to-r2-migration` |
| prompt audit, self-audit, skill audit | `prompt-audit` |
| user story, "as a researcher", "I need to" | `user-story-separation` |
| code review, security audit, best practices, code quality assessment | `code-review` |
| commit, conventional commit, git commit | `git-commit` |
| art, generative art, algorithmic art, p5.js, flow field, particle | `algorithmic-art` |
| docx, Word document, .docx, tracked changes, comments | `docx` |
| pptx, PowerPoint, presentation, slides, .pptx | `pptx` |
| xlsx, Excel, spreadsheet, CSV, .xlsx, data analysis | `xlsx` |
| PDF form, fill PDF, merge PDF, split PDF | `pdf` |
| documentation, proposal, spec, technical writing, co-author | `doc-coauthoring` |
| infographic, AntV, chart visualization | `infographic-syntax-creator` |
| MCP, Model Context Protocol, FastMCP, API integration | `mcp-builder` |
| settings, preferences, theme, language, font size, DeepChat settings | `deepchat-settings` |
| remember, recall, memory, durable learning, tape | `memory-management` |
| create skill, new skill, skill creator, update skill | `skill-creator` |
| artifact, React component, Tailwind, shadcn, web app | `web-artifacts-builder` |
| red team, DoD, definition of done, quality check, verify | `red-team-dod` |
| test, verify, test suite, enforce | `test-enforcement` |
| pdf builder, convert markdown, LaTeX compile | `pdf-builder` |


### Rule 2: Fallback When skill_view() Fails

If `skill_view('name')` returns an error, try these fallbacks in order:
1. `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. `npx wrangler r2 object get qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md` then read
3. Report `[SKILL-UNAVAILABLE: <name>]` and continue with best-effort knowledge

NEVER ask the user to manually load a skill. NEVER silently continue without the skill's critical instructions.

### Rule 3: Cross-Link Skills

Every QNFO skill MUST reference related skills in its header:
```
> **Related:** execution-guard, closeout-manager, cloudflare-deployer
```

When loading skill A, auto-load any skills it cross-references that are relevant to the current task.

### Rule 4: Pre-Task Skill Check

Before executing any task, check:
1. What skills does this task require?
2. Have they been loaded this session?
3. If not: load them now (auto-detect + fallback)

### Rule 5: Load Once, Use Many

Once a skill is loaded, cache its content for the session. Don't re-load the same skill multiple times.

## Skill Inventory (41 skills)

| Skill | Trigger Pattern | Related Skills |
|-------|----------------|---------------|
| `skill-autoloader` | (always active) | all |
| `execution-guard` | (always active) | closeout-manager, qnfo-agent |
| `user-story-separation` | user stories | qnfo-agent, execution-guard |
| `qnfo-agent` | (always active) | all |
| `cloudflare-deployer` | deploy, upload, wrangler, Pages, Workers, R2, D1, DNS, KV | infrastructure-audit, closeout-manager |
| `closeout-manager` | close, terminate, handoff, done | execution-guard, cloudflare-deployer, knowledge-graph |
| `publication-publisher` | publish, Zenodo, DOI, PDF, paper | cloudflare-deployer, citation-manager |
| `knowledge-graph` | KG, graph-api, dependencies, neighbors | qnfo-agent, infrastructure-audit |
| `infrastructure-audit` | audit, health check, orphan, stale | cloudflare-deployer, knowledge-graph |
| `literature-search` | research, arXiv, Semantic Scholar | publication-publisher, citation-manager |
| `git-hygiene` | git error, detached HEAD, merge | closeout-manager |
| `email-composer` | email, send, Outlook | — |
| `template-catalog` | template, fill_prompt_template | all |
| `citation-manager` | cite, BibTeX, bibliography | publication-publisher, literature-search |
| `bling-usability-audit` | UI, design, frontend, styling | cloudflare-deployer |
| `seo-discoverability` | SEO, sitemap, robots.txt | cloudflare-deployer |
| `buffer-integration` | social media, tweet, post | publication-publisher |
| `kaizen-autonomous-update` | Kaizen, improve, update | closeout-manager, skill-sync |
| `skill-sync` | sync skills, backup | kaizen-autonomous-update |
| `prompt-audit` | prompt audit, self-audit | skill-sync |
| `local-to-r2-migration` | migrate, cleanup, thin client | cloudflare-deployer |
| `handoff-protocol` | handoff, QACP | closeout-manager |
| `ultrametric-engine` | ultrametric, p-adic, tree | knowledge-graph |
| `test-enforcement` | (always active — Priority 1) | execution-guard, closeout-manager |
| `red-team-dod` | (always active — Priority 0) | execution-guard, closeout-manager |
| `code-review` | code review, security audit, best practices, code quality | test-enforcement |
| `git-commit` | commit, conventional commit, commit message | git-hygiene |
| `frontend-design` | UI, design, web component, React, HTML, CSS, dashboard, landing page | bling-usability-audit |
| `algorithmic-art` | art, generative, p5.js, flow field, particle system | frontend-design |
| `web-artifacts-builder` | artifact, React component, Tailwind, shadcn | frontend-design |
| `docx` | docx, Word, document, tracked changes | — |
| `pptx` | pptx, PowerPoint, presentation, slides | — |
| `xlsx` | xlsx, Excel, spreadsheet, CSV, data analysis | — |
| `pdf` | PDF, form, merge, split, extract | pdf-builder |
| `pdf-builder` | PDF build, convert markdown, LaTeX compile, publication PDF | publication-publisher |
| `doc-coauthoring` | documentation, proposal, spec, co-author, technical writing | — |
| `infographic-syntax-creator` | infographic, AntV, chart, visualization | frontend-design |
| `mcp-builder` | MCP server, Model Context Protocol, FastMCP, API integration | — |
| `deepchat-settings` | settings, preferences, theme, language, font | — |
| `memory-management` | remember, recall, memory, learning, tape | qnfo-agent |
| `skill-creator` | create skill, new skill, update skill | skill-sync |

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| User says "load the cloudflare-deployer skill" | Should never happen — auto-detected |
| LLM says "I don't know how to deploy — which skill?" | Load cloudflare-deployer automatically |
| skill_view() fails, LLM silently continues | Run fallback chain: read() → R2 → report |
| Skill loaded but not used | Only load skills relevant to current task |
| Skills loaded multiple times | Cache: load once per session |

---

*skill-autoloader v2.0 — Priority 0. Auto-detects task patterns and loads skills. User never manually manages skills. Fallback recovery for load failures.*
