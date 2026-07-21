---
name: documents
description: Create, edit, and analyze all document formats -- Word (.docx) with formatting and tracked changes, PowerPoint (.pptx) presentations from outlines, Excel (.xlsx/.csv/.tsv) spreadsheets with formulas and analysis, and PDF manipulation (form filling, merge, split, text/table extraction). For publication-grade LaTeX PDF builds, use the research skill.
version: "2.1"
triggers: ["docx", "Word", "document", "PowerPoint", "presentation", "slides", "Excel", "spreadsheet", "CSV", "TSV", "xlsx", "pptx", "PDF", "form", "fill form", "merge PDF", "split PDF", "extract PDF", "table extraction", "tracked changes", "comments", "speaker notes", "formula", "chart", "pivot table", "data analysis", "import", "export", "office", "formatting", "styles", "headers", "footers"]
related: ["research"]
priority: 2
platform: local
autonomous: false
self_sufficient: true
---

# DOCUMENTS -- v2.2 (Office + PDF + 4-D Export)

> **v2.2 UPDATE (2026-07-21, phantom-claim audit):** Added the
> **Tool-Call Execution Mandate** section below. A document is not
> "created"/"updated"/"filled" until it has been read back and its content
> verified in this turn — the write-tool's return value alone is not proof
> the file is correct.

> **Merges 2:** office-documents + pdf-documents
> **Related:** Load `research` for publication-grade PDFs + 4-D distribution. Load `cloudflare` for R2/IPFS archival.
> **Cloudflare Full-Stack:** Generated documents are ephemeral on local disk. Canonical storage is R2 with 4-D distribution. Published papers use the research pipeline.
> **4-D Mandate:** Every finalized document must be stored in ≥4 locations across ≥2 protocols.

## execute_plan

update_plan([
  {"step": "Identify document type: .docx, .pptx, .xlsx, .csv, or .pdf", "status": "pending"},
  {"step": "Read source data and create/edit document with appropriate tooling", "status": "pending"},
  {"step": "Verify: Test-Path output.ext AND (Get-Item output.ext).Length > 0", "status": "pending"},
])

---

## Tool-Call Execution Mandate (Anti-Phantom Gate — MANDATORY)

Claiming a document was "created", "updated", "filled", or "extracted"
without an invoked tool call showing evidence in this turn is a PHANTOM
CLAIM (`qnfo-agent` §9.11 Rule 14) — BLOCKED.

1. **Every creation/edit** — after writing, `Test-Path` (or `read`) the output file AND re-open/re-parse it (extract text or read cell values back) to confirm content matches intent. A successful write-tool return code is NOT proof the document is correct.
2. **.xlsx formula edits** — re-read the saved file and confirm formulas are still formulas (not baked-in values) before claiming "formulas preserved".
3. **PDF form fills** — re-extract the filled field values from the saved PDF and show them; do not claim "form filled" from the fill-call's return alone.
4. **.pptx/.docx from outline** — re-open the generated file and report the actual slide/paragraph count achieved vs the outline requested.
5. If the output cannot be re-verified in this turn, say `[NOT-VERIFIED: reason]` instead of "done"/"created"/"filled".

---

## Word Documents (.docx)

### Creation
- Create from markdown, structured data, or programmatic content
- Apply styles: Heading 1-3, Normal, List Bullet, List Number, Block Text
- Insert tables with header rows, alternating row shading
- Embed images with captions and alt text
- Set page margins (1 inch default), orientation (portrait/landscape)
- Add headers and footers (page numbers, document title, date)

### Editing
- Modify existing content while preserving formatting
- Apply style changes to selected paragraphs
- Replace text with formatting preservation
- Insert/delete paragraphs, tables, images

### Track Changes & Comments
- Enable tracked changes for review workflows
- Accept/reject individual changes or all changes
- Add comments to specific text ranges
- Read existing comments with author and timestamp
- Resolve/delete comments

### Text Extraction
- Extract plain text preserving paragraph structure
- Extract structured content (tables as arrays, images as metadata)
- Handle headers, footers, footnotes, endnotes

### Formatting Checklist
- [ ] Fonts consistent (headings + body)
- [ ] Heading hierarchy correct (H1 > H2 > H3)
- [ ] Table widths fit page margins
- [ ] Images have captions and are inline with text
- [ ] Page numbers in footer
- [ ] Spell check completed
- [ ] File size reasonable (<10MB for documents without images)

---

## PowerPoint Presentations (.pptx)

### Creation from Outline
```markdown
# Slide 1: Title
## Slide 2: Problem Statement
- Bullet 1
- Bullet 2
## Slide 3: Methodology
1. Step one
2. Step two
## Slide 4: Results
| Metric | Value |
|:-------|:------|
| Total | 42 |
```

Each `##` becomes a new slide. Lists become bullet points. Tables become formatted tables.

### Slide Operations
- Add/remove/reorder slides
- Change slide layout (Title, Title+Content, Two Content, Blank)
- Set background color or image
- Apply slide transitions

### Content Elements
- **Text:** Titles, body text, bullet lists, numbered lists
- **Tables:** Row/column counts, header formatting, alternating colors
- **Images:** Embedded with position and sizing
- **Charts:** Bar, line, pie, scatter (linked or embedded data)

### Speaker Notes
- Add per-slide speaker notes
- Read existing speaker notes
- Format notes with line breaks and emphasis

### Verification
- [ ] Slide count matches outline
- [ ] All slides have content (no empty slides)
- [ ] Reading order logical (title -> problem -> method -> results -> conclusion)
- [ ] Speaker notes present if presentation is for delivery
- [ ] File opens without errors in PowerPoint

---

## Excel Spreadsheets (.xlsx, .csv, .tsv)

### Creation
- Create workbooks with multiple named sheets
- Populate cells with values, formulas, and formatting
- Set column widths, row heights
- Apply number formatting (currency, percent, date, scientific)
- Conditional formatting (color scales, data bars, icon sets)

### Formulas
- Basic: SUM, AVERAGE, COUNT, MIN, MAX, IF
- Lookup: VLOOKUP, INDEX/MATCH, XLOOKUP
- Date: TODAY, DATE, DATEDIF
- Text: CONCAT, LEFT, RIGHT, MID
- Logic: IF, AND, OR, NOT
- Statistical: STDEV, CORREL, LINEST

**CRITICAL:** When editing .xlsx, use formula-preserving paths. NEVER read formulas as values and write them back -- the formulas are LOST.

### Data Analysis
- Pivot tables: row/column fields, value fields, aggregation (sum/count/average)
- Charts: bar, line, pie, scatter
- Filtering and sorting
- Statistical analysis (descriptive statistics, regression)

### CSV/TSV
- Import: auto-detect delimiter and data types
- Export: specify delimiter, quoting, encoding (UTF-8 with BOM for Excel compatibility)
- Handle: quoted fields, multi-line fields, null values

### Verification
- [ ] File opens without corruption warning
- [ ] Formulas recalculate correctly (press F9)
- [ ] Charts render with correct data
- [ ] Pivot tables refresh properly
- [ ] CSV encoding is UTF-8 (with BOM if Excel-bound)
- [ ] All sheets named and organized

---

## PDF Manipulation

### Operations
| Operation | Description | Tool Pattern |
|:----------|:------------|:-------------|
| **Fill Form** | Populate PDF form fields programmatically | Read field structure -> set values -> save |
| **Merge** | Combine multiple PDFs into one document | Concatenate pages preserving order |
| **Split** | Extract specific pages or page ranges | Copy pages 1-5, 10-15 to new PDF |
| **Extract Text** | Get plain text from all pages | Iterate pages -> get_text() |
| **Extract Tables** | Extract tabular data with structure | Parse table regions -> return as list of lists |
| **Create** | Generate new PDF from scratch | Add pages -> draw text/images -> save |

### Limitations
- **NOT for publication-grade builds.** Use `research` skill for Pandoc+XeLaTeX PDFs.
- Scanned PDFs need OCR for text extraction (not included -- handle as images).
- Complex formatting (multi-column, floating elements) may not extract perfectly.
- Encrypted/DRM PDFs cannot be processed.

### Verification
- [ ] `Test-Path output.pdf` -> file exists
- [ ] `(Get-Item output.pdf).Length -gt 500` -> non-trivial size (>500 bytes)
- [ ] Page count matches expected
- [ ] Text extraction produces readable content
- [ ] Form fields populated correctly (verify visually)

---

## Anti-Patterns
| Anti-Pattern | Fix |
|:-------------|:----|
| Creating documents without verification | Always Test-Path + check content |
| Losing formulas during .xlsx edits | Use formula-preserving edit paths |
| Wrong file extension | Match: .docx/.pptx/.xlsx/.csv/.pdf |
| Using this skill for publication PDFs | Use `research` skill for Pandoc+XeLaTeX |
| Cross-skill document confusion | Documents -> R2 archive -> Papers (via research pipeline) |
\n\n## R2 Archival Script\n`js\n// _r2_archive.js — Archive any document to R2 for durable storage\nconst TOKEN = process.env.CLOUDFLARE_API_TOKEN;\nconst ACCOUNT = '...';\nconst BUCKET = 'qnfo';\nconst KEY = 'documents/filename.ext';\nconst content = '...'; // file content\n\nawait fetch('https://api.cloudflare.com/client/v4/accounts/' + ACCOUNT + '/r2/buckets/' + BUCKET + '/objects/' + encodeURIComponent(KEY), {\n  method: 'PUT',\n  headers: { 'Authorization': 'Bearer ' + TOKEN },\n  body: content\n});\n// Verify: GET same URL returns 200 with content\n// Alt: npx wrangler r2 object put qnfo/{KEY} --file {path} --remote\n`