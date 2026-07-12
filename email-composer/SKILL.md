---
name: email-composer
description: "Outlook email composition, sending, reading, and management via COM automation. Use when user says compose email, draft email, send email, read inbox, reply to email, search email, or when the agent needs to send, read, search, or manage emails through Outlook."
version: "2.2"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('email-composer')` or `read()` with filesystem path.
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

> **Related:** —
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
  {"step": "Compose email body and subject", "status": "pending"},
  {"step": "Set recipients, CC, BCC", "status": "pending"},
  {"step": "Attach files if needed", "status": "pending"},
  {"step": "Verify all fields populated", "status": "pending"},
  {"step": "Send email via Outlook COM", "status": "pending"}
])


# EMAIL COMPOSER SKILL — v2.1

> **On-demand skill.** Load via `skill_view('email-composer')` when email operations are needed.
> Source: `EMAIL-AGENT-v1.3.md` (template) + email-composer skill

---

## Quick Start

For sending email, use `fill_prompt_template("EMAIL-AGENT", {...})` with all required parameters.
For reading/searching email, use the Python scripts in `qnfo/projects/email-agent\`.

---

## Email Operations

### Read Inbox
```powershell
python "qnfo/projects/email-agent\email_inbox.py" --folder "Inbox" --count 20
```

### Search Email
```powershell
python "qnfo/projects/email-agent\email_search.py" --query "quantum computing" --folder "Inbox"
```

### Send Email
Use `fill_prompt_template("EMAIL-AGENT", {to, subject, body, cc, bcc, attachments})` then execute the generated script:
```powershell
python "qnfo/projects/email-agent\email_send.py"
```

### Reply to Email
```powershell
python "qnfo/projects/email-agent\email_reply.py" --message-id "<id>" --body "Response text"
```

### Archive Email
```powershell
python "qnfo/projects/email-agent\email_archive.py" --message-id "<id>" --folder "Archive"
```

---

## Pre-Send Validation (MANDATORY)

Before sending ANY email, run through DEFAULT.md §E.5.1 checklist:
1. **WHO Gate:** Right person? Checked prior threads?
2. **WHEN Gate:** Right time? Recent activity? Trigger event?
3. **WHAT Gate:** Clear, concise, actionable? Appropriate tone?
4. **SOURCE AUDIT:** Every claim traceable to source?
5. **FABRICATION CHECK:** No invented papers, DOIs, paths?
6. **FILESYSTEM VERIFICATION:** All referenced files exist?

---

## Account Configuration

- **Default account:** rowan.quni@qnfo.org
- **Profile:** Outlook COM automation via `win32com.client`
- **Scripts:** `qnfo/projects/email-agent\`

---

## Common Patterns

### Checking for Prior Threads
```powershell
python "qnfo/projects/email-agent\email_search.py" --query "<contact-name>" --folder "Inbox"
python "qnfo/projects/email-agent\email_search.py" --query "<contact-name>" --folder "Sent Items"
```

### Drafting Without Sending
Set `confirm_send: false` in the EMAIL-AGENT template parameters. The script will save to Drafts.

---

## Failure Recovery

| Error | Cause | Fix |
|:------|:------|:----|
| `COM error: Outlook not running` | Outlook closed | Start Outlook manually |
| `Access denied` | Another process locking Outlook | Wait 5s, retry |
| `Recipient not found` | Invalid email address | Verify address format |
| `Attachment not found` | File path wrong | `Test-Path` the file first |

---

## Embedded Scripts

> **SELF-CONTAINED:** Email scripts live in `qnfo/projects/email-agent\`. Before executing, verify they exist.

| Script | R2 Canonical | Execution Cache | Purpose |
|:-------|:-------------|:----------------|:--------|
| `email_inbox.py` | `qnfo/projects/email-agent\email_inbox.py` | Read inbox |
| `email_search.py` | `qnfo/projects/email-agent\email_search.py` | Search email |
| `email_send.py` | `qnfo/projects/email-agent\email_send.py` | Send email |
| `email_reply.py` | `qnfo/projects/email-agent\email_reply.py` | Reply to email |
| `email_archive.py` | `qnfo/projects/email-agent\email_archive.py` | Archive email |

### Bootstrap Protocol
```bash
Test-Path "qnfo/projects/email-agent\<script>.py"
```
If MISSING: these are project-level scripts. Check the `email-agent` project in `qnfo/projects/email-agent\`. Scripts are version-controlled in that project's git repo.

---

## Reference Files

- Agent template: `qnfo/prompts/email\EMAIL-AGENT-v1.3.md`
- Test suite: `qnfo/prompts/email\EMAIL-TEST-SUITE.md`
- Scripts: `qnfo/projects/email-agent\email_*.py`
- Shared utilities: `qnfo/projects/email-agent\_email_utils.py`

---

*email-composer skill v2.1 — Load on-demand via skill_view(). Email scripts moved to projects/email-agent/.*

---

*email-composer v2.1 — QNFO custom skill. Load via read('R2 `qnfo/prompts/skills/email-composer\\SKILL.md'). Not accessible via skill_view().*

> **Version:** (Kaizen-audited 2026-07-08)
