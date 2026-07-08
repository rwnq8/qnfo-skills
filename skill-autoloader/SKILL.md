---
name: skill-autoloader
description: "AUTOMATICALLY loads relevant skills based on task detection. User NEVER manually loads skills. Cross-references all skills and handles fallback chains. Use when skill loading is needed, task patterns must be detected, or skill_view() resolution fails and requires fallback recovery."
pinned: true
version: "1.1"
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
  {"step": "Detect task patterns from user input", "status": "pending"},
  {"step": "Cross-reference against skill trigger table (Rule 1)", "status": "pending"},
  {"step": "Load matching skills via skill_view()", "status": "pending"},
  {"step": "Verify skills loaded — check for SKILL-UNAVAILABLE fallbacks", "status": "pending"},
  {"step": "Report loading status to execution guard", "status": "pending"}
])


# SKILL — v1.0 AUTO-LOADER -- v2.0

> **Version:** v1.0 (Kaizen-audited 2026-07-05)

> **Version:** v1.0 (Kaizen-audited 2026-07-05)


> **PRIORITY 0 — pinned, always active. User NEVER manually loads skills.**

## Purpose

The LLM system automatically detects what skills are needed for any task and loads them without user prompting. The user should NEVER say "load the cloudflare-deployer skill" — the LLM detects the task and loads it.

### Rule 0: Embedded Shared Protocols (v4.0 — SELF-SUFFICIENT)

**The autoloader is self-sufficient.** All shared protocols are embedded inline in this document. No external `skill_view()` calls, no filesystem reads for protocol content. The shared reference files on disk are REDUNDANT BACKUPS — they are NOT loaded at runtime.

**Embedded Red-Team Protocol:** Before claiming any task complete, autonomously run: (1) Output Verification — negative verification, try to prove claims are FALSE. (2) Assumption Challenge — state and test every assumption. (3) Edge Case Check — empty/null/max/boundary/desync. (4) DoD Integration — verify all criteria met with tool evidence. (5) Iteration — retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

**Embedded Design System (LOCKED v3.0):** Design tokens: `--blue: #1a56db; --blue-dark: #1040a8; --blue-light: #dbeafe; --blue-subtle: #eff6ff; --blue-mid: #6094e8; --text: #1a1a2e; --text-muted: #6b7280; --bg: #ffffff; --border: #e5e7eb; --card-bg: #f9fafb; --max-w: 960px; --radius: 8px;` Fonts: Inter (headings/nav/meta), Source Serif 4 (body), JetBrains Mono (code). 🚫 Dark themes forbidden. Light theme only. Mandatory components: Sticky Top Nav (backdrop-blur), AI Query box, Related Papers section, Paper cards (hover shadow), Badges (DOI blue, Type purple, Category green, Tag gray, License orange).

These inline embeddings are the canonical source. Skills that reference external shared files are operating from stale/at-risk copies.

## Core Rules

### Rule 1: Auto-Detect by Task Pattern

When the user's message or the LLM's planned task matches a pattern, auto-load the relevant skill:

| Task Pattern | Auto-Load |
|-------------|-----------|
| deploy, upload, wrangler, Pages, Workers, R2, D1, DNS, KV, Vectorize, Queues, Cloudflare, migrate, thin client | `cloudflare-deployer` |
| publish, Zenodo, DOI, PDF, paper, manuscript, LaTeX, build PDF | `publication-publisher` |
| close out, terminate, done, session end, HANDOFF, handoff, QACP | `closeout-manager` |
| git error, detached HEAD, merge conflict, rebase, commit, conventional commit | `git-hygiene` |
| email, send, Outlook, compose | `email-composer` |
| knowledge graph, KG, graph-api, dependencies, impact, neighbors, nodes, edges | `knowledge-graph` |
| audit, infrastructure, health check, orphan, stale, lifecycle, worker route, route conflict | `infrastructure-audit` |
| ipfs, pinata, cid, pinning, paper hash, content-addressing | `ipfs-pinning` |
| UI, design, frontend, page, styling, BLING, visual | `bling-usability-audit` |
| research, paper search, literature, preprint, Semantic Scholar | `literature-search` |
| SEO, sitemap, robots.txt, discoverability, llms.txt | `seo-discoverability` |
| Kaizen, improve, update system, deploy prompts | `kaizen-autonomous-update` |
| skill sync, backup skills, restore skills | `skill-sync` |
| cite, citation, BibTeX, bibliography | `citation-manager` |
| social media, tweet, post, Buffer, LinkedIn, Bluesky | `buffer-integration` |
| user story, "as a researcher", "I need to", remember, recall, memory, durable learning, tape | `qnfo-agent` |
| code review, security audit, best practices, code quality assessment | `code-review` |
| art, generative art, algorithmic art, p5.js, flow field, particle | `algorithmic-art` |
| docx, Word document, .docx, tracked changes, comments | `docx` |
| pptx, PowerPoint, presentation, slides, .pptx | `pptx` |
| xlsx, Excel, spreadsheet, CSV, .xlsx, data analysis | `xlsx` |
| PDF form, fill PDF, merge PDF, split PDF | `pdf` |
| documentation, proposal, spec, technical writing, co-author | `doc-coauthoring` |
| MCP, Model Context Protocol, FastMCP, API integration | `mcp-builder` |
| settings, preferences, theme, language, font size, DeepChat settings | `deepchat-settings` |
| artifact, React component, Tailwind, shadcn, web app, dashboard, landing page | `frontend-design` |
| create skill, new skill, skill creator, update skill, prompt audit | `skill-creator` |
| red team, DoD, definition of done, quality check, verify | `red-team-dod` |
| test, verify, test suite, enforce | `test-enforcement` |
| ultrametric, p-adic, tree | `ultrametric-engine` |


### Rule 2: Fallback When skill_view() Fails

If `skill_view('name')` returns an error, try these fallbacks in order:
1. `read('%USERPROFILE%\.deepchat\skills\<name>\SKILL.md')`
2. `npx wrangler r2 object get qnfo/prompts/skills/<name>/SKILL.md --remote --file=_skill.md` then read
3. Report `[SKILL-UNAVAILABLE: <name>]` and continue with best-effort knowledge

NEVER ask the user to manually load a skill. NEVER silently continue without the skill's critical instructions.

### Rule 3: Cross-Link Skills — Subsidiary Skill Chain Loading (v3.0)

**HARD GATE: When a primary skill references a subsidiary skill via `Related:` header, the subsidiary skill MUST be loaded BEFORE the primary skill's workflow execution begins.**

#### 3.1 Related: Header Format (MANDATORY)

Every QNFO skill MUST reference related skills in its header using this exact format:
```
> **Related:** skill-a, skill-b, skill-c
```

Skills with no dependencies use:
```
> **Related:** —
```

The autoloader parses this header to build the loading chain. Skills with missing or malformed `Related:` headers are flagged `[SKILL-GAP: <skill> missing Related header]`.

#### 3.2 Subsidiary Loading Trigger Protocol

When the autoloader loads a primary skill for execution:

1. **PARSE:** Scan the loaded skill content for `> **Related:**` and extract the comma-separated skill names.
2. **FORCE-LOAD:** For each listed subsidiary skill, call `skill_view('<name>')`. If `skill_view` fails, use the retry protocol (Rule 2). Do NOT skip any listed skill — even if it seems "not relevant."
3. **VERIFY:** Confirm every subsidiary skill loaded successfully (content returned, no fallback errors). Flag any failures as `[SKILL-CHAIN-BROKEN: <parent> → <missing-subsidiary>]`.
4. **MERGE PLANS:** For each subsidiary skill, extract its `execute_plan` items and merge them into the primary skill's `update_plan` with `[SUB: <skill-name>]` prefix (see execution-guard §1.9.2).
5. **CACHE:** Mark all loaded skills as cached for the session (Rule 5).

#### 3.3 Chain Integrity Check

Before claiming ANY skill workflow complete, verify:
- All subsidiary skills in the `Related:` chain were loaded
- All subsidiary `[SUB: ...]` plan items are completed
- No subsidiary item is `pending` while the primary claims completion

**HARD GATE:** If ANY subsidiary item in the chain is `pending`, the primary workflow is NOT complete. Flag `[CHAIN-BROKEN: subsidiary tasks not executed]`.

### Rule 4: Self-Sufficiency Verification (v3.0 — HARD GATE)

**Before loading any skill for execution, verify it is a self-sufficient standalone document.** Skills that reference external files, scripts, or shared protocols at runtime are brittle — they break under parallel thread updates, R2 unavailability, and thin-client cleanup.

#### 4.1 Self-Sufficiency Scan

When loading a skill, scan its content for these BANNED patterns:

| Pattern | Violation | Severity |
|:--------|:----------|:---------|
| `read('%APPDATA%\\DeepChat\\skills\\...')` | External read dependency | HIGH |
| `skill_view('...', 'references/...')` | Shared reference dependency | HIGH |
| `npx wrangler r2 object get qnfo/tools/...` | R2 script dependency | CRITICAL |
| `read('templates/...')` or `read('agents/...')` | Template/agent file dependency | MEDIUM |
| Reference to `.md` protocol file without inline content | Protocol pointer dependency | MEDIUM |

#### 4.2 Decision Matrix

| Scan Result | Action |
|:------------|:-------|
| **0 violations** | ✅ Load and execute normally |
| **1-3 violations, content available** | 🟠 Load skill, extract the referenced content from shared files/R2 and embed inline for this session. Flag `[SELF-SUFFICIENCY-GAP]` for Kaizen. |
| **4+ violations OR content unavailable** | 🔴 Flag `[SELF-SUFFICIENCY-CRITICAL: <skill>]`. Attempt best-effort execution with available content. The skill needs rewrite. |

#### 4.3 Embedding Protocol

When a loaded skill has external dependencies, resolve them by embedding:

1. **Shared protocol references:** Read the shared file ONCE, embed the content into the skill's working copy for this session
2. **R2 script dependencies:** Pull the script ONCE from R2, embed as inline code block, write to temp `_<name>.py`, execute, delete
3. **Template dependencies:** Read the template ONCE, embed the content inline

**The goal:** After loading, the skill's in-memory representation contains ALL needed content. No further external I/O for instructions or scripts.

### Rule 5: Pre-Task Skill Check

Before executing any task, check:
1. What skills does this task require?
2. Have they been loaded this session?
3. If not: load them now (auto-detect + fallback)

### Rule 6: Load Once, Use Many

Once a skill is loaded, cache its content for the session. Don't re-load the same skill multiple times.

## Skill Inventory (27 skills)

| Skill | Trigger Pattern | Related Skills |
|-------|----------------|---------------|
| `skill-autoloader` | (always active) | all |
| `execution-guard` | (always active) | closeout-manager, qnfo-agent |
| `qnfo-agent` | (always active) | all |
| `cloudflare-deployer` | deploy, upload, wrangler, Pages, Workers, R2, D1, DNS, KV, migrate, thin client | infrastructure-audit, closeout-manager |
| `closeout-manager` | close, terminate, handoff, done, QACP | execution-guard, cloudflare-deployer, knowledge-graph |
| `publication-publisher` | publish, Zenodo, DOI, PDF, paper, manuscript, LaTeX, build PDF | cloudflare-deployer, citation-manager, seo-discoverability |
| `knowledge-graph` | KG, graph-api, dependencies, neighbors | qnfo-agent, infrastructure-audit |
| `infrastructure-audit` | audit, health check, orphan, stale, worker route, route conflict | cloudflare-deployer, knowledge-graph |
| `ipfs-pinning` | ipfs, pinata, cid, pinning, paper hash, content-addressing | cloudflare-deployer, publication-publisher |
| `literature-search` | research, preprint, Semantic Scholar | publication-publisher, citation-manager |
| `git-hygiene` | git error, detached HEAD, merge, commit, conventional commit | closeout-manager |
| `email-composer` | email, send, Outlook | — |
| `citation-manager` | cite, BibTeX, bibliography | publication-publisher, literature-search |
| `bling-usability-audit` | UI, design, frontend, styling | cloudflare-deployer, frontend-design |
| `seo-discoverability` | SEO, sitemap, robots.txt, llms.txt | cloudflare-deployer |
| `buffer-integration` | social media, tweet, post | publication-publisher |
| `kaizen-autonomous-update` | Kaizen, improve, update | closeout-manager, skill-sync |
| `skill-sync` | sync skills, backup | kaizen-autonomous-update |
| `ultrametric-engine` | ultrametric, p-adic, tree | knowledge-graph |
| `test-enforcement` | (always active — Priority 1) | execution-guard, closeout-manager |
| `red-team-dod` | (always active — Priority 0) | execution-guard, closeout-manager |
| `code-review` | code review, security audit, best practices, code quality | test-enforcement |
| `frontend-design` | UI, design, web component, React, HTML, CSS, dashboard, artifact, Tailwind, shadcn | bling-usability-audit |
| `algorithmic-art` | art, generative, p5.js, flow field, particle system | frontend-design |
| `docx` | docx, Word, document, tracked changes | — |
| `pptx` | pptx, PowerPoint, presentation, slides | — |
| `xlsx` | xlsx, Excel, spreadsheet, CSV, data analysis | — |
| `pdf` | PDF, form, merge, split, extract | publication-publisher |
| `doc-coauthoring` | documentation, proposal, spec, co-author, technical writing | — |
| `mcp-builder` | MCP server, Model Context Protocol, FastMCP, API integration | — |
| `deepchat-settings` | settings, preferences, theme, language, font | — |
| `skill-creator` | create skill, new skill, update skill, prompt audit | skill-sync |

## Anti-Patterns

| Anti-Pattern | Fix |
|:-------------|:----|
| User says "load the cloudflare-deployer skill" | Should never happen — auto-detected |
| LLM says "I don't know how to deploy — which skill?" | Load cloudflare-deployer automatically |
| skill_view() fails, LLM silently continues | Run fallback chain: read() → R2 → report |
| Skill loaded but not used | Only load skills relevant to current task |
| Skills loaded multiple times | Cache: load once per session |
| **Primary skill loaded WITHOUT checking `Related:` header** | Parse Related header — auto-load ALL listed subsidiary skills (Rule 3.2) |
| **Subsidiary skills referenced but NOT loaded before execution** | Force-load chain BEFORE populating update_plan (Rule 3.2 step 2) |
| **Skill claims completion while subsidiary `[SUB: ...]` items pending** | Chain Integrity Check (Rule 3.3) blocks completion claim |
| **Skill references another skill but has NO `Related:` header** | Flag `[SKILL-GAP: <skill> missing Related header]` — fix in Kaizen |

---

*skill-autoloader v3.0 — Priority 0. Auto-detects task patterns and loads skills. Subsidiary Skill Chain Loading (Rule 3) — parses Related: headers, force-loads all subsidiary skills, merges their execute_plan items into primary update_plan with [SUB:] prefix. Chain Integrity Check blocks completion while subsidiary items pending. User never manually manages skills. Fallback recovery for load failures.*

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
**Skill-Specific Checks:** Verify all skill_view() calls resolve to existing skills. Verify fallback chain works for all 41 skills. Verify auto-loading triggers fire correctly.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

