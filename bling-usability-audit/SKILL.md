---
name: bling-usability-audit
description: Executable usability audit — drives YoBrowser to navigate UI as a real user, tests all interactions, captures screenshots, evaluates visual polish, and fills out the BLING-USABILITY-AUDIT template. Combines functional testing with visual polish review. Use when user says "test my app," "check my website," "run usability test," "UI audit," "screenshot test," "browser test," "accessibility check."
version: "1.2"
---

> **INCLUDES AUTONOMOUS RED-TEAM SELF-AUDIT.** Before claiming this skill complete, autonomously run: (1) Output Verification -- negative verification. (2) Assumption Challenge -- state and test every assumption. (3) Edge Case Check -- empty/null/max/boundary/desync. (4) DoD Integration -- run _dod_enforce.py if exists. (5) Iteration -- retry on failure, max 3. ANTI-PATTERN: User should NEVER ask about quality.

### Programmatic Loading & Execution
This skill is loaded and executed **programmatically by the LLM system** 
during response generation. Loading is triggered automatically via 
`skill_view('bling-usability-audit')` or `read()` with filesystem path.
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

> **Related:** cloudflare-deployer, frontend-design

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
  {"step": "Launch YoBrowser and navigate to target page", "status": "pending"},
  {"step": "Test all UI interactions and states", "status": "pending"},
  {"step": "Capture screenshots at each state", "status": "pending"},
  {"step": "Evaluate visual polish (typography, color, spacing)", "status": "pending"},
  {"step": "Fill out BLING-USABILITY-AUDIT template", "status": "pending"},
  {"step": "Report BLOCKING/IMPROVEMENT findings", "status": "pending"}
])


# BLING USABILITY AUDIT SKILL — v1.0

> **Executable workflow skill.** Drives YoBrowser for real browser-based usability testing.
> Template: `templates/BLING-USABILITY-AUDIT.md`
> Persistent Preference: DEFAULT.md §3 Pref #9

---
---

## WHAT THIS SKILL DOES

Unlike the passive template, this skill **actively executes** a usability audit:

| Capability | Template Alone | With This Skill |
|:-----------|:--------------:|:---------------:|
| Navigate UI pages/flows | [NO] | [OK] YoBrowser `load_url` + `cdp_send` |
| Click buttons, test forms | [NO] | [OK] `Runtime.evaluate` + `Input.dispatchMouseEvent` |
| Capture screenshots | [NO] | [OK] `Page.captureScreenshot` |
| Test responsive breakpoints | [NO] | [OK] `cdp_send` with viewport changes |
| Check console for errors | [NO] | [OK] `Runtime.evaluate('console.error')` |
| Test keyboard navigation | [NO] | [OK] `Input.dispatchKeyEvent` (Tab, Enter, Escape) |
| Evaluate visual polish | [NO] (manual only) | [OK] Screenshot analysis + checklist audit |
| Fill audit template | [NO] (manual entry) | [OK] Auto-populated with tool evidence |

---
## PREREQUISITES

Before executing this skill:

1. **UI must be live and accessible** — either deployed URL (Cloudflare Pages, localhost) or local file://
2. **YoBrowser must be available** — verify with `get_browser_status`
3. **Template must exist** — `fill_prompt_template("BLING-USABILITY-AUDIT")` must return content
4. **Test paths defined** — list of pages/flows to exercise (auto-discovered if not provided)

---

## WORKFLOW — 6 Phases

### Phase 1: Discovery & Setup

```python
# 1.1 Pull the BLING audit template
fill_prompt_template("BLING-USABILITY-AUDIT", {
    project_name: "<project>",
    component_name: "<component>"
})

# 1.2 Verify YoBrowser is ready
get_browser_status()
# If no browser session, one will be created on first load_url

# 1.3 Define test matrix
TEST_URLS = ["<url>"]          # All pages/flows to test
VIEWPORTS = [
    {"width": 1920, "height": 1080},  # Desktop
    {"width": 1440, "height": 900},   # Laptop
    {"width": 1024, "height": 768},   # Tablet landscape
    {"width": 768, "height": 1024},   # Tablet portrait
    {"width": 375, "height": 812},    # Mobile (iPhone)
]
```

### Phase 2: Functional Testing (BLIND)

For each URL in TEST_URLS:

```python
# 2.1 Load the page
load_url(url="<url>")

# 2.2 Wait for page to fully render (check document.readyState)
cdp_send(method="Runtime.evaluate", params={
    "expression": "document.readyState"
})
# Should return "complete"

# 2.3 Capture full-page screenshot
cdp_send(method="Page.captureScreenshot", params={
    "format": "png",
    "fullPage": True
})

# 2.4 Test ALL interactive elements
# Find all clickable elements
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify(
        Array.from(document.querySelectorAll('a, button, [role="button"], input[type="submit"], [onclick]'))
            .map(el => ({
                tag: el.tagName,
                text: (el.textContent || '').trim().slice(0, 50),
                href: el.href || null,
                type: el.type || null,
                visible: el.offsetParent !== null,
                disabled: el.disabled || false
            }))
    )
    """
})

# 2.5 Test form inputs
# Find all input elements
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify(
        Array.from(document.querySelectorAll('input, textarea, select'))
            .map(el => ({
                tag: el.tagName,
                name: el.name || el.id || '',
                type: el.type || el.tagName.toLowerCase(),
                placeholder: el.placeholder || '',
                required: el.required || false,
                visible: el.offsetParent !== null
            }))
    )
    """
})

# 2.6 Check console for errors
cdp_send(method="Runtime.evaluate", params={
    "expression": "window.__consoleErrors || []"
})

# 2.7 Test keyboard navigation (Tab through interactive elements)
cdp_send(method="Input.dispatchKeyEvent", params={
    "type": "keyDown",
    "key": "Tab",
    "code": "Tab"
})
# Then check which element has focus:
cdp_send(method="Runtime.evaluate", params={
    "expression": "document.activeElement.tagName + '#' + (document.activeElement.id || '')"
})

# 2.8 Test modal/dialog interactions if they exist
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify(
        Array.from(document.querySelectorAll('[role="dialog"], .modal, [aria-modal="true"]'))
            .map(el => ({
                visible: el.offsetParent !== null,
                hasCloseButton: !!el.querySelector('[aria-label="Close"], .close, [data-dismiss]')
            }))
    )
    """
})
```

### Phase 3: Visual Polish Audit (BLING)

For each URL at EACH viewport:

```python
# 3.1 Set viewport
cdp_send(method="Runtime.evaluate", params={
    "expression": f"window.innerWidth + 'x' + window.innerHeight"
})

# 3.2 Capture screenshot at this viewport
cdp_send(method="Page.captureScreenshot", params={
    "format": "png"
})

# 3.3 Check typography
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify({
        fontFamilies: [...new Set(
            Array.from(document.querySelectorAll('*'))
                .map(el => getComputedStyle(el).fontFamily)
                .filter(f => f && f !== '')
        )],
        fontSizes: [...new Set(
            Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,span,li,a'))
                .map(el => getComputedStyle(el).fontSize)
        )].sort(),
        lineHeights: [...new Set(
            Array.from(document.querySelectorAll('p,li,div'))
                .map(el => getComputedStyle(el).lineHeight)
                .filter(lh => lh !== 'normal')
        )]
    })
    """
})

# 3.4 Check color contrast
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    (function() {
        function getContrastRatio(rgb1, rgb2) {
            function getLuminance(r, g, b) {
                let [rs, gs, bs] = [r/255, g/255, b/255].map(c =>
                    c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4)
                );
                return 0.2126*rs + 0.7152*gs + 0.0722*bs;
            }
            let l1 = getLuminance(rgb1[0], rgb1[1], rgb1[2]);
            let l2 = getLuminance(rgb2[0], rgb2[1], rgb2[2]);
            let lighter = Math.max(l1, l2);
            let darker = Math.min(l1, l2);
            return (lighter + 0.05) / (darker + 0.05);
        }

        let issues = [];
        document.querySelectorAll('p, span, a, h1, h2, h3, h4, h5, h6, li, button, label, div').forEach(el => {
            if (el.children.length > 0) return; // Skip containers
            let style = getComputedStyle(el);
            let color = style.color.match(/\\d+/g);
            let bg = style.backgroundColor.match(/\\d+/g);
            if (!color || !bg || bg[3] === '0') return;
            let ratio = getContrastRatio(
                [parseInt(color[0]), parseInt(color[1]), parseInt(color[2])],
                [parseInt(bg[0]), parseInt(bg[1]), parseInt(bg[2])]
            );
            if (ratio < 4.5 && parseFloat(style.fontSize) >= 14) {
                issues.push({
                    element: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
                    text: el.textContent.trim().slice(0, 30),
                    ratio: ratio.toFixed(2),
                    fontSize: style.fontSize,
                    status: ratio < 3 ? 'FAIL' : 'WARN'
                });
            }
        });
        return JSON.stringify(issues.slice(0, 20));
    })()
    """
})

# 3.5 Check layout — detect overflow and alignment issues
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify({
        horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth,
        bodyOverflow: document.body.scrollWidth > window.innerWidth,
        fixedElements: Array.from(document.querySelectorAll('[style*="position:fixed"], [style*="position: sticky"]'))
            .map(el => el.tagName + (el.className ? '.' + el.className.split(' ')[0] : '')),
        orphanedText: Array.from(document.querySelectorAll('body *'))
            .filter(el => el.children.length === 0 && el.textContent.trim() && el.offsetParent === null)
            .length
    })
    """
})

# 3.6 Check animation/motion
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify({
        animations: Array.from(document.querySelectorAll('*'))
            .filter(el => {
                let style = getComputedStyle(el);
                return style.animationName !== 'none' || style.transitionProperty !== 'all';
            })
            .map(el => ({
                tag: el.tagName,
                class: el.className?.split(' ')[0] || '',
                animation: getComputedStyle(el).animationName,
                duration: getComputedStyle(el).animationDuration,
                prefersReducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches
            }))
            .slice(0, 10)
    })
    """
})
```

### Phase 4: Responsive Testing

For each viewport size in VIEWPORTS:

```python
# Override viewport via CDP (using Emulation.setDeviceMetricsOverride if available)
# Otherwise, note that YoBrowser may not support viewport override directly.
# Fallback: test at different window sizes manually and note limitations.

# For each viewport:
#   1. Resize (or load at different size if viewport override unavailable)
#   2. Check: all content accessible? No horizontal scroll? Touch targets >= 44px?
#   3. Check: navigation transforms correctly? Menu becomes hamburger?
#   4. Screenshot at this breakpoint

cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify({
        viewport: window.innerWidth + 'x' + window.innerHeight,
        hasHorizontalScroll: document.documentElement.scrollWidth > window.innerWidth,
        touchTargets: Array.from(document.querySelectorAll('a, button, [role="button"]'))
            .filter(el => {
                let rect = el.getBoundingClientRect();
                return rect.width < 44 || rect.height < 44;
            })
            .map(el => ({
                tag: el.tagName,
                text: el.textContent.trim().slice(0, 20),
                width: Math.round(el.getBoundingClientRect().width),
                height: Math.round(el.getBoundingClientRect().height)
            }))
            .slice(0, 10)
    })
    """
})
```

### Phase 5: State Verification

Test ALL UI states for each page:

```python
# 5.1 Loading state — check for spinners/skeletons
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify({
        spinners: document.querySelectorAll('[role="progressbar"], .spinner, .loader, .skeleton, [aria-busy="true"]').length,
        loadingText: document.body.innerText.includes('Loading') || document.body.innerText.includes('loading')
    })
    """
})

# 5.2 Empty state — check if UI handles no-data gracefully
# (May need to navigate to a page with no data)

# 5.3 Error state — check error message clarity
# Trigger by navigating to 404 or providing invalid input

# 5.4 Edge cases — very long text, special characters, zero values
cdp_send(method="Runtime.evaluate", params={
    "expression": """
    JSON.stringify({
        longTextElements: Array.from(document.querySelectorAll('*'))
            .filter(el => el.children.length === 0 && el.textContent.length > 200)
            .map(el => ({ tag: el.tagName, length: el.textContent.length }))
            .slice(0, 5),
        zeroWidthChars: (document.body.innerHTML.match(/\\u200B/g) || []).length,
        overflowHidden: Array.from(document.querySelectorAll('*'))
            .filter(el => getComputedStyle(el).overflow === 'hidden' && el.scrollHeight > el.clientHeight)
            .length
    })
    """
})
```

### Phase 6: Template Population & Report

```python
# 6.1 Fill the BLING-USABILITY-AUDIT template with findings
# For each of the 4 questions, provide evidence from YoBrowser testing:

# WHAT'S WORKING:
# - List elements/functions verified via load_url + cdp_send testing
# - Attach screenshot references for each verified element

# WHAT'S NOT:
# - List elements that failed interaction tests
# - List console errors found
# - List contrast issues detected

# WHAT NEEDS TO BE FIXED:
# - BLOCKING: Any element that prevents task completion
# - MAJOR: Non-blocking but significant issues
# - MINOR: Visual defects, minor inconsistencies

# WHAT CAN BE IMPROVED:
# - Visual polish opportunities identified from screenshot analysis
# - UX flow improvements from navigation testing
# - Accessibility enhancements from keyboard/contrast testing

# 6.2 Populate FINDINGS REGISTER
# Fill template table with evidence from Phases 2-5

# 6.3 Set verdict
# PASS: Zero BLOCKING + zero MAJOR
# CONDITIONAL PASS: Zero BLOCKING, MAJOR documented
# FAIL: BLOCKING issues remain

# 6.4 Compile AUDIT EVIDENCE section
# - Screenshot count from Phases 2-4
# - Test paths exercised from Phase 2
# - Viewports tested from Phase 4
```

---

## OUTPUT — Completed BLING Audit

The final output is the filled `BLING-USABILITY-AUDIT` template with:

1. **All 4 questions answered** with YoBrowser evidence (not speculation)
2. **Screenshots attached** for each finding
3. **Findings register populated** from tool output
4. **Verdict set** based on evidence
5. **Audit evidence section** complete with test paths and screenshots

---

## EDGE CASES & RECOVERY

| Scenario | Action |
|:---------|:-------|
| **URL not accessible** | Report `[BLOCKED: URL unreachable]`, skip testing, flag in audit |
| **YoBrowser unavailable** | Fall back to `brave_web_search` for publicly accessible pages; flag `[LIMITED: no browser]` |
| **Page requires authentication** | Flag `[SKIPPED: auth-required]`, test only public pages |
| **Single-page app (SPA)** | Wait for `document.readyState === 'complete'` AND check for framework hydration |
| **Dynamic content (infinite scroll)** | Scroll via `window.scrollTo(0, document.body.scrollHeight)`, wait, re-capture |
| **Animation-heavy pages** | Wait for animations to settle (check `document.getAnimations().length`) before screenshot |
| **Viewport override unavailable** | Test at 3 viewports via manual resize; document limitation |
| **Cross-origin iframes** | Flag `[SKIPPED: cross-origin]`, audit parent page only |
| **Client-side routing (React Router, etc.)** | Navigate via clicking links, not direct URL loads, to test routing |
| **File inputs / drag-drop** | Flag `[LIMITED: no file system access]`, test label/button only |

---

## REFERENCE FILES

- Audit template: `templates/BLING-USABILITY-AUDIT.md`
- Persistent Preference: DEFAULT.md §3 Pref #9
- Definition of Done: `templates/DEFINITION-OF-DONE.md` UI TASK section
- QWAV quality gate: QWAV-DEFAULT.md Deliverable Review Protocol

---

*BLING Usability Audit Skill v1.0 — Drives YoBrowser for real browser-based UI testing. BLIND functional + BLING visual polish.*

---

*bling-usability-audit v1.0 — QNFO custom skill. Load via read('R2 `qnfo/prompts/skills/bling-usability-audit\\SKILL.md'). Not accessible via skill_view().*

> **Version:** (Kaizen-audited 2026-07-08)
## Handoff Protocol (MANDATORY at Closeout)

1. **Verify** ALL execute_plan items marked [EXECUTED] with tool evidence (Test-Path, exec output, git log)
2. **Archive** session artifacts to R2 canonical storage: `npx wrangler r2 object put qnfo/audit/... --remote --file=<artifact>`
3. **Generate** continuation prompt documenting pending work and current state for the next session
4. **Clean up** ephemeral _* files and __pycache__ directories: `Remove-Item _* -Recurse -Force`

### Continuation Prompt Template
```
TASK: [description of pending work from execute_plan]
STATE: [current state — what's executed, what's blocked, why]
NEXT: [first executable action for the next session]
R2: [canonical path for session artifacts]
```


## Closeout Protocol (MANDATORY)

Before declaring this skill workflow complete:
1. **Task Execution Verification:** Compare planned tasks ([PENDING] in execute_plan) vs executed tasks ([EXECUTED] with evidence)
2. **Filesystem Verification:** `Test-Path <file>` for every file claimed as created/modified. Never claim from memory.
3. **Git Verification:** `git log -1 --oneline` for every commit claimed. Verify commit hash exists.
4. **R2 State Upload:** Upload session audit trail to `qnfo/audit/` — conversations, decisions, state files.
5. **Discovery Index Update:** Update `qnfo/discovery/index.json` with any new resources created, projects modified, or publications generated.
6. **Ephemeral Cleanup:** Delete ALL _* prefixed files and __pycache__ directories. Session is not complete until `Get-ChildItem -File -Name | Where-Object { $_ -match '^_' }` returns zero results.
