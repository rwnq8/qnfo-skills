# QNFO Design System Compliance (Shared Protocol — v3.0 LOCKED 2026-07-01)

> **ALL QNFO/QWAV publications, pages, PDFs, and web artifacts MUST use the papers.qnfo.org canonical design (LOCKED v3.0).**
> **Loaded once per session by skill-autoloader Rule 0.**

## Locked Design Tokens (ABSOLUTE — DO NOT CHANGE)

```css
--blue: #1a56db; --blue-dark: #1040a8; --blue-light: #dbeafe;
--blue-subtle: #eff6ff; --blue-mid: #6094e8;
--text: #1a1a2e; --text-muted: #6b7280; --bg: #ffffff;
--border: #e5e7eb; --card-bg: #f9fafb; --max-w: 960px; --radius: 8px;
```

## Locked Fonts

| Role | Font |
|:-----|:-----|
| Headings, nav, meta, badges | **Inter** (weights 400-700) |
| Body text | **Source Serif 4** (weights 400, 600, italic) |
| Code | JetBrains Mono / Fira Code / monospace |

## Locked Components (MANDATORY on all paper/research pages)

1. Sticky Top Nav with backdrop-blur
2. AI Query box on all paper pages
3. Related Papers section on all paper pages
4. Paper cards with hover shadow
5. Badges (DOI blue, Type purple, Category green, Tag gray, License orange)

## Hard Rules

🚫 **DARK THEMES FORBIDDEN.** Light theme only.
🚫 **DO NOT change fonts, colors, or max-width.** Locked.
🚫 **DO NOT remove components.** AI Query + Related Papers mandatory.

## Resources

| Resource | Location |
|:---------|:---------|
| Design doc (full spec) | `qnfo/design-system/QNFO-DESIGN-SYSTEM.md` |
| PDF builder (v3.0) | `qnfo/design-system/build_pdf.py` |
| Canonical CSS | `https://qnfo.org/design-system/qnfo-light.css` |

## Verification

```bash
python -c "import urllib.request;h=urllib.request.urlopen('URL').read().decode();print('DARK' if '#0a0a0f' in h or '#0d1117' in h else 'LIGHT')"
```
