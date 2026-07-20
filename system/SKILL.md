---
name: system
description: DeepChat application configuration, skill ecosystem management, and desktop automation -- settings and preferences (theme, language, font, model config), MCP server configuration, skill creation/deployment/sync, skill lifecycle management, and Computer Use tools for desktop GUI automation (launch apps, click, type, inspect windows).
version: "2.0"
triggers: ["settings", "preferences", "theme", "language", "font", "config", "DeepChat settings", "MCP config", "skill", "create skill", "new skill", "update skill", "deploy skill", "sync skill", "skill lifecycle", "Kaizen", "system update", "improve", "desktop", "app", "GUI", "automate", "click", "type", "window", "Computer Use", "CUA", "launch", "screen", "screenshot", "process", "notepad", "calculator", "browser app", "desktop app"]
related: ["cloudflare"]
priority: 3
platform: all
autonomous: false
self_sufficient: true
---

# SYSTEM -- v2.0 (Ultra-Consolidated Config + Skills + Desktop)

> **Merges 3:** deepchat-config + skill-management + computer-use
> **Related:** Load `cloudflare` for skill deployment to R2 bucket `qnfo-skills/prompts/skills/`. Desktop automation is platform-local only.
> **Cloudflare Full-Stack:** Skills deploy to R2. App settings reference Cloudflare MCP Workers. All config is Cloudflare-backed.

## execute_plan

update_plan([
  {"step": "Identify target: configuration, skill lifecycle, or desktop automation", "status": "pending"},
  {"step": "Execute with proper tooling", "status": "pending"},
  {"step": "Verify: settings persisted, skills deployed, or action confirmed", "status": "pending"},
])

---

## DeepChat Configuration

### App Settings
**Path:** `%APPDATA%\DeepChat\app-settings.json`

```json
{
  "theme": "light",
  "language": "en",
  "fontSize": 14,
  "fontFamily": "Inter",
  "modelConfig": {
    "temperature": 0.3,
    "maxTokens": 64000,
    "contextLength": 128000,
    "reasoning": true
  }
}
```

### MCP Server Configuration
**RAG Bridge (primary):** `qnfo-memory-mcp` at `https://qnfo-memory-mcp.q08.workers.dev/mcp`
- Tools: `search_papers`, `search_memories`, `remember_fact`, `recall_facts`, `get_paper_context`
- Bindings: MEMORY_DB, MEMORY_VZ, PAPER_VZ, AI
- Version: v1.2 (2026-07-14, red-team audited)

**AI Search (managed):** `qnfo-ai-search` -- Cloudflare AI Search
- Source: R2 bucket `qnfo/papers/`
- Embedding model: `bge-base-en-v1.5`

### Disaster Recovery
1. Settings lost -> restore from `deepchat-config` skill backup
2. GitHub backup -> `qnfo-skills` repo
3. R2 backup -> `prompts/skills/` on R2 bucket `qnfo-skills`
4. DeepChat restart: `taskkill /F /IM DeepChat.exe` -> auto-restart

---

## Skill Management

### SKILL.md Structure (MANDATORY)
```yaml
---
name: skill-name
description: Rich description with comprehensive trigger keywords for autonomous discovery
version: "1.0"
triggers: ["keyword1", "keyword2", ...]
related: ["other-skill"]
priority: 0-3
platform: all | cloudflare | local
autonomous: true | false
self_sufficient: true
---

# SKILL TITLE -- v1.0

> **Merges:** list of merged skills (if consolidated)

## execute_plan
update_plan([...])

## Core Content
[Complete unabridged instructions]

## Verification
[Post-execution gates]

## Anti-Patterns
[What NOT to do]
```

### Design Principles
1. **Self-sufficient:** No external file references. Embed ALL scripts, templates, and protocols inline.
2. **Verifiable:** Every workflow step produces tool evidence (Test-Path, git log, exec output).
3. **Chainable:** `related:` field lists subsidiary skills for auto-loading.
4. **Discoverable:** `triggers:` contains comprehensive keyword arrays for autonomous pattern matching.
5. **Concrete:** No vague instructions ("handle errors properly"). Specific, executable steps.

### Skill Lifecycle
```
CREATE -> WRITE (SKILL.md with complete content) -> DEPLOY -> VERIFY -> MAINTAIN
```

### Deployment
1. **Local disk:** Write to `%USERPROFILE%\.deepchat\skills\<name>\SKILL.md`
2. **GitHub:** Commit and push to `qnfo-skills` repo
3. **R2:** Upload to `qnfo-skills/prompts/skills/<name>/SKILL.md`
4. **Verify:** All three layers have identical content

### Verification
```bash
# Check local
Test-Path "$env:USERPROFILE\.deepchat\skills\<name>\SKILL.md"

# Check GitHub
git log -1 --oneline

# Check R2
npx wrangler r2 object get qnfo-skills/prompts/skills/<name>/SKILL.md --remote
```

---

## Desktop Automation (Computer Use)

### Available Tools
`list_apps` | `list_windows` | `get_window_state` | `click` | `double_click` | `right_click` | `type_text` | `press_key` | `hotkey` | `scroll` | `drag` | `launch_app` | `kill_app` | `bring_to_front` | `get_screen_size` | `get_desktop_state` | `get_cursor_position` | `move_cursor` | `set_value` | `debug_window_info`

### Standard Usage Pattern
```python
# 1. Find the app
list_apps()  # Returns: {name, pid, running, kind, launch_path}

# 2. Launch if not running, or get window handle
launch_app({name: "Notepad", start_minimized: True})
# Returns: {pid, name, windows: [{window_id, title, bounds}]}

# 3. Inspect the window
get_window_state({pid: 1234, window_id: 5678})
# Returns: {tree_markdown, structuredContent, screenshot}

# 4. Interact via element_index (background-safe)
click({pid: 1234, window_id: 5678, element_index: 5})
type_text({pid: 1234, text: "Hello", element_index: 3, window_id: 5678})

# 5. Verify result
get_window_state({pid: 1234, window_id: 5678})
```

### Windows Platform Notes
- **Element index preferred** for background-safe clicks (no focus steal, no window activation)
- **XAML/WinUI3/UWP apps** (modern Notepad, Calculator, Photos) -- require `element_index` for `type_text`
- **Legacy Win32 apps** -- `type_text` via PostMessage(WM_CHAR) works without element_index
- **`delivery_mode: "background"` FIRST** -- only escalate to `"foreground"` on `background_unavailable` error
- **Element index is per-snapshot** -- re-snapshot with `get_window_state` before each interact cycle
- **minimized windows** -- UIA works on minimized windows; `screenshot` and foreground delivery need restoration
- **Check permissions:** `check_permissions()`
- **Health:** `health_report()`

### Anti-Patterns (CUA)
| Anti-Pattern | Fix |
|:-------------|:----|
| Pixel click without element_index | Prefer element_index for background-safety |
| Foreground delivery without trying background first | Always try `background` first |
| Using stale element_index | Re-snapshot with `get_window_state` before each cycle |
| Click on XAML app without element_index | XAML requires element_index for type_text |
| Launching app without `start_minimized: true` | Launch hidden to not disrupt user |

## Reusable Scripts

### Worker Fleet Audit
```js
// _worker_audit.js — List all Workers + bindings + health
const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = "...";
const w = await (await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/workers/scripts', {
  headers: { 'Authorization': 'Bearer ' + T }
})).json();
for (const wr of (w.result||[])) {
  const b = await (await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/workers/scripts/' + wr.id + '/bindings', {
    headers: { 'Authorization': 'Bearer ' + T }
  })).json();
  let h = 'unknown';
  try { h = (await fetch('https://' + wr.id + '.workers.dev/health')).status === 200 ? 'healthy' : 'unhealthy'; } catch(e) {}
  console.log(wr.id + ': ' + h + ' [' + (b.result||[]).map(function(x){return x.type+':'+x.name}).join(',') + ']');
}
```

### Infrastructure Audit
```js
// _infra_audit.js — Full fleet audit (Workers, D1, R2, Vectorize, Queues, KV, DNS, Pages, 522-RISK)
// Run each resource count sequentially, report totals, flag anomalies vs baselines
```

### R2 Hygiene Check
```js
// _r2_hygiene.js — Check for qnfo/qnfo/ double-prefix anti-pattern
// Bucket name IS the namespace. Never prefix keys with bucket name inside that bucket.
```

### DNSLink Verification
```js
// _dnslink_verify.js — Check all DNSLink TXT records across all zones
const T = process.env.CLOUDFLARE_API_TOKEN;
const zones = await (await fetch('https://api.cloudflare.com/client/v4/zones', {
  headers: { 'Authorization': 'Bearer ' + T }
})).json();
for (const z of (zones.result||[])) {
  const dns = await (await fetch('https://api.cloudflare.com/client/v4/zones/' + z.id + '/dns_records?type=TXT', {
    headers: { 'Authorization': 'Bearer ' + T }
  })).json();
  const dnslink = (dns.result||[]).filter(function(r) { return r.content.includes('dnslink'); });
  dnslink.forEach(function(r) { console.log(z.name + ': ' + r.name + ' ' + r.content); });
}
```

---

## Verification
- [ ] Config changes persist across DeepChat restarts
- [ ] Skills synced to all 3 layers: disk -> GitHub -> R2
- [ ] Desktop automation result confirmed via window state
- [ ] `health_report()` returns all checks passing
- [ ] No skill has external file references (self-sufficiency)
- [ ] No skill has fewer than 15 trigger keywords
- [ ] **4-D Gate:** Critical assets (ULA, publications, deliverables) verified across ≥4 distribution stores
- [ ] **IPFS:** Content pinned via Filebase (PRIMARY, free/unlimited) or Lighthouse (SECONDARY) — Pinata REMOVED 2026-07-20 (quota exceeded, blocked), CID logged in KG
- [ ] **DNSLink:** `_dnslink` TXT records exist for all publication subdomains
- [ ] **Worker fleet:** ≤7 Workers (consolidation pattern enforced), 0 orphaned Workers
- [ ] **R2 hygiene:** No `qnfo/qnfo/` double-prefix paths in qnfo bucket
\n\n### Skill Sync\n`js\n// _skill_sync.js — Sync all skills to GitHub + R2 after edits\nconst { execSync } = require('child_process');\nconst TOKEN = process.env.CLOUDFLARE_API_TOKEN;\nconst ACCOUNT = '...';\nconst HOME = process.env.USERPROFILE + '/.deepchat/skills';\n\n// 1. Git commit + push\nexecSync('git add -A && git commit -m skills-update && git push', { cwd: HOME });\n\n// 2. R2 sync (all 23 skills)\nconst skills = fs.readdirSync(HOME).filter(d => fs.existsSync(HOME + '/' + d + '/SKILL.md'));\nfor (const s of skills) {\n  const content = fs.readFileSync(HOME + '/' + s + '/SKILL.md', 'utf8');\n  await fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/r2/buckets/qnfo-skills/objects/' + encodeURIComponent('prompts/skills/' + s + '/SKILL.md'), {\n    method: 'PUT',\n    headers: { 'Authorization': 'Bearer ' + TOKEN },\n    body: content\n  });\n}\nconsole.log('Synced ' + skills.length + ' skills to GitHub + R2');\n`