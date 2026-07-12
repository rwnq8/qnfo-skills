---
name: deepchat-settings
description: DeepChat app settings modification (DeepChat u8bbeu7f6e/u504fu597d) skill. Activate ONLY when the user explicitly asks to change DeepChat's own settings/preferences (e.g., theme, language, font size...). Do NOT activate for OS/system settings, editor settings, or other apps.
version: "1.1"
allowedTools:
  - deepchat_settings_toggle
  - deepchat_settings_set_language
  - deepchat_settings_set_theme
  - deepchat_settings_set_font_size
  - deepchat_settings_open
---
> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

> **Related:** —



### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('deepchat-settings')` or `read()` with filesystem path.
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
  {"step": "Identify target setting to modify", "status": "pending"},
  {"step": "Validate setting value against constraints", "status": "pending"},
  {"step": "Apply setting change", "status": "pending"},
  {"step": "Verify change persisted in app-settings.json", "status": "pending"}
])


# DeepChat Settings Modification Skill

Use this skill to safely change DeepChat *application* settings during a conversation.

## Core rules

- Only change settings when the user is asking to change **DeepChat** settings.
- Use the dedicated settings tools; never attempt arbitrary key/value writes.
- These tools are intended to be available only when this skill is active.
- Viewing the main `deepchat-settings` `SKILL.md` activates this skill for the current conversation and exposes the `deepchat_settings_*` tools in the next tool loop iteration.
- Viewing linked files under this skill does **not** activate the skill.
- If the request is ambiguous, ask a clarifying question before applying.
- For unsupported or high-risk settings (MCP, prompts, providers, API keys, paths): do **not** apply changes; instead explain where to change it and open Settings.

## Supported settings (initial allowlist)

Toggles:

- `soundEnabled`: enable/disable sound effects.
- `copyWithCotEnabled`: enable/disable copying COT details.

Enums:

- `language`: DeepChat locale, including `system`, `zh-CN`, `en-US`, `zh-TW`, `zh-HK`, `ko-KR`, `ru-RU`, `ja-JP`, `fr-FR`, `fa-IR`, `pt-BR`, `da-DK`, `he-IL`.
- `theme`: `dark | light | system`.
- `fontSizeLevel`: integer level within supported range.

Settings navigation (open-only):

- Use `deepchat_settings_open` only when the request cannot be fulfilled by the settings tools, and avoid calling it if the change is already applied.
- `section` hints: `common`, `display`, `provider`, `mcp`, `prompt`, `acp`, `skills`, `knowledge-base`, `database`, `shortcut`, `about`.

## Workflow

1. Confirm the user is requesting a DeepChat settings change.
2. If the settings tools are not yet present, inspect the main `deepchat-settings` skill document first so the skill becomes active for this conversation.
3. Determine the target setting and the intended value.
4. If the setting is supported, call the matching tool:
   - toggles: `deepchat_settings_toggle`
   - language: `deepchat_settings_set_language`
   - theme: `deepchat_settings_set_theme`
   - font size: `deepchat_settings_set_font_size`
5. Confirm back to the user what changed (include the final value).
6. If the setting is unsupported, call `deepchat_settings_open` (with `section`) and provide a short pointer to the correct Settings section. Do not call it if the requested change has already been applied.
7. **MANDATORY RESTART**: After any supported settings change, execute the DeepChat restart script to ensure the new settings take full effect:
   ```powershell
   powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.deepchat\skills\deepchat-settings\scripts\restart_deepchat.ps1"
   ```
   This kills all old DeepChat processes and launches a fresh instance. The current conversation will terminate. Warn the user briefly before executing.

## Mandatory Restart Policy

**Rule:** Any successful settings change via this skill MUST be followed by a programmatic DeepChat restart (kill + relaunch). Settings may not fully propagate without a restart. The restart script is embedded at `scripts\restart_deepchat.ps1` within this skill.

## Examples (activate this skill)

- "把主题改成深色"
- "Turn off sound effects"
- "语言改成英文"
- "复制时不要带 COT"
- "Open the MCP settings page"
- "Edit my prompts"

## Examples (do NOT activate this skill)

- "把 Windows 的系统代理改成..."
- "帮我改 VS Code 的字体"
- "把电脑的声音关掉"

## RT: RED-TEAM SELF-AUDIT

Before claiming this skill complete, autonomously run:

1. Output Verification (negative verification)
2. Assumption Challenge (state and test every assumption)
3. Edge Case Check (empty/null/max/boundary/desync)
4. DoD Integration (run _dod_enforce.py if exists)
5. Iteration (retry on failure, max 3)

ANTI-PATTERN: User should NEVER ask about quality.
Refer to RED-TEAM-PROTOCOL.md for full protocol.

> **Version:** (Kaizen-audited 2026-07-08)
