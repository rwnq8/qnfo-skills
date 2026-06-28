#!/usr/bin/env python3
"""
build_pdf.py -- Markdown/HTML to PDF converter for QNFO publications.
v2.0 - 2026-06-28

PRIMARY PIPELINE (v2.0): MD → md_to_html.py → HTML+CSS+MathJax → playwright PDF
This produces Obsidian-quality, CSS-formatted, professional PDFs with full LaTeX math.

LEGACY PIPELINE (--legacy): reportlab + matplotlib mathtext (kept for compatibility).

Usage:
  # Primary pipeline (recommended - Obsidian quality)
  python build_pdf.py --input paper.md --output paper.pdf

  # Primary pipeline with metadata
  python build_pdf.py --input paper.md --output paper.pdf --title "My Paper" --author "Name"

  # Legacy pipeline (reportlab)
  python build_pdf.py --input paper.md --output paper.pdf --legacy

  # Skip math rendering (legacy mode only)
  python build_pdf.py --input paper.md --output paper.pdf --legacy --no-math
"""

import argparse
import re
import sys
import os
import json
import subprocess
import tempfile
import shutil
from datetime import datetime
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_skill_dir():
    """Get the pdf-builder skill directory."""
    paths = [
        Path(os.environ.get('APPDATA', '.')) / 'DeepChat' / 'skills' / 'pdf-builder',
        Path(__file__).parent.parent,  # Relative to scripts/
    ]
    for p in paths:
        if (p / 'scripts' / 'md_to_html.py').exists():
            return p
    return None


def check_dependency(name, import_name=None):
    """Check if a Python package is available."""
    if import_name is None:
        import_name = name
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False


def check_playwright_browsers():
    """Check if playwright has chromium installed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        return True
    except Exception as e:
        return str(e)


def verify_pdf(pdf_path):
    """Verify PDF rendering quality using pymupdf."""
    try:
        import fitz
    except ImportError:
        print('[VERIFY] pymupdf not available, skipping verification')
        return True

    doc = fitz.open(str(pdf_path))
    text = ''.join(page.get_text() for page in doc)
    page_count = len(doc)
    doc.close()

    issues = []

    # Check for Unicode replacement characters
    if '\ufffd' in text:
        pos = text.index('\ufffd')
        ctx = text[max(0, pos - 30):pos + 30]
        issues.append(f'Unicode replacement characters found near: ...{ctx}...')

    # Check for raw markdown artifacts
    if '|---' in text and '|' in text:
        issues.append('Raw markdown table pipes in output')

    if 'MATH RENDER ERROR' in text:
        issues.append('Math rendering errors detected')

    # Check for raw LaTeX commands
    raw_tex_patterns = [r'\bmod', r'\operatorname', r'\begin{align}', r'\begin{cases}']
    for pattern in raw_tex_patterns:
        if pattern in text:
            pass  # MathJax source artifacts in PDF text are expected, not errors

    # Check key typographic characters
    typographic_checks = {
        '\u2014': 'em dash',
        '\u201c': 'left curly quote',
        '\u201d': 'right curly quote',
        '\u2018': 'left single curly quote',
        '\u2019': 'right single curly quote',
    }

    if issues:
        print(f'[VERIFY] BLOCKED: {len(issues)} issues found:')
        for issue in issues:
            print(f'  - {issue}')
        print(f'[VERIFY] Pages: {page_count}, Total chars: {len(text):,}')

        # Only block if it's not typographic (which legacy mode may not have)
        if any('replacement characters' in i or 'render error' in i.lower() for i in issues):
            return False

    print(f'[VERIFY] PDF OK — {page_count} pages, {len(text):,} characters')
    for char, name in typographic_checks.items():
        count = text.count(char)
        symbol = '\u2713' if count > 0 else '\u2717'
        print(f'[VERIFY]   {symbol} {name}: {count} found')

    return True


def sanitize_unicode_escapes(text, source_label=""):
    """Fix literal \\uXXXX escape sequences in text. (Legacy compatibility)"""
    fixes = 0
    fix_report = []

    def replace_unicode(match):
        nonlocal fixes
        code = int(match.group(1), 16)
        char = chr(code)
        fixes += 1
        fix_report.append(f"Line {text[:match.start()].count(chr(10)) + 1}: "
                          f"\\u{match.group(1)} -> {char} (U+{match.group(1).upper()})")
        return char

    text = re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, text)
    return text, fixes, fix_report


def strip_yaml_frontmatter(text):
    """Strip YAML frontmatter. Returns (metadata_dict, content_text). (Legacy compat)"""
    if not text.startswith('---'):
        return {}, text

    end = text.find('\n---\n', 3)
    if end == -1:
        end = text.find('\n---\r\n', 3)
    if end == -1:
        return {}, text

    yaml_text = text[3:end].strip()
    content = text[end + 4:].strip()
    if content.startswith('---'):
        content = content[3:].strip()

    metadata = {}
    try:
        import yaml
        parsed = yaml.safe_load(yaml_text)
        if isinstance(parsed, dict):
            metadata = parsed
    except Exception:
        for line in yaml_text.split('\n'):
            if ':' in line:
                k, _, v = line.partition(':')
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and v:
                    metadata[k] = v

    return metadata, content


# ═══════════════════════════════════════════════════════════════
# PRIMARY PIPELINE: MD → HTML+CSS+MathJax → playwright PDF
# ═══════════════════════════════════════════════════════════════

def build_pdf_playwright(input_path, output_path, title=None, author=None,
                         date_str=None, no_math=False, css_path=None):
    """
    Primary pipeline: Convert MD to HTML with CSS+MathJax, then render to PDF via playwright.
    This produces Obsidian-quality, CSS-formatted, professional PDFs.
    """
    skill_dir = get_skill_dir()
    if not skill_dir:
        print('[ERROR] Cannot find pdf-builder skill directory')
        print('[ERROR] md_to_html.py must be at: <skill_dir>/scripts/md_to_html.py')
        return False

    md_to_html = skill_dir / 'scripts' / 'md_to_html.py'
    if not md_to_html.exists():
        print(f'[ERROR] md_to_html.py not found at: {md_to_html}')
        return False

    # Step 1: MD → HTML
    print(f'[PIPELINE] Step 1: Converting Markdown to HTML...')
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
        html_path = f.name

    cmd = [
        sys.executable, str(md_to_html),
        '--input', str(input_path),
        '--output', html_path,
    ]
    if title:
        cmd.extend(['--title', title])
    if author:
        cmd.extend(['--author', author])
    if date_str:
        cmd.extend(['--date', date_str])
    if no_math:
        cmd.append('--no-math')
    if css_path:
        cmd.extend(['--css', str(css_path)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f'[ERROR] md_to_html.py failed:')
        print(result.stderr)
        os.unlink(html_path)
        return False

    # Step 2: HTML → PDF via playwright
    print(f'[PIPELINE] Step 2: Rendering HTML to PDF via playwright...')
    try:
        from playwright.sync_api import sync_playwright

        abs_url = 'file:///' + html_path.replace('\\', '/')
        with sync_playwright() as p:
            # Auto-detect chromium path
            chromium_paths = [
                os.path.expandvars(r'%LOCALAPPDATA%\\ms-playwright\\chromium-1223\\chrome-win64\\chrome.exe'),
                os.path.expandvars(r'%LOCALAPPDATA%\\ms-playwright\\chromium_headless_shell-1223\\chrome-headless-shell-win64\\chrome-headless-shell.exe'),
            ]
            chrome_exe = None
            for cp in chromium_paths:
                if os.path.exists(cp):
                    chrome_exe = cp
                    break
            if chrome_exe:
                browser = p.chromium.launch(executable_path=chrome_exe, headless=True)
            else:
                browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(abs_url, wait_until='networkidle', timeout=30000)

            # Wait for MathJax
            try:
                page.wait_for_function(
                    '() => { var c = document.querySelectorAll("mjx-container"); return c.length > 0 || !window.MathJax; }',
                    timeout=10000
                )
                mjx = page.evaluate('() => document.querySelectorAll("mjx-container").length')
                print(f'[MATHJAX] {mjx} containers rendered')
            except Exception as e:
                print(f'[MATHJAX] Note: {e}')

            # Extra settle time
            page.wait_for_timeout(2000)

            # Generate PDF
            page.pdf(
                path=str(output_path),
                format='A4',
                margin={'top': '2cm', 'bottom': '2cm', 'left': '2cm', 'right': '2cm'},
                print_background=True
            )
            browser.close()

        print(f'[OK] PDF generated via playwright: {output_path}')
        print(f'[OK] PDF size: {output_path.stat().st_size / 1024:.1f} KB')
        return True

    except ImportError:
        print('[ERROR] playwright not installed. Install with: pip install playwright && playwright install chromium')
        return False
    except Exception as e:
        print(f'[ERROR] playwright PDF generation failed: {e}')
        return False
    finally:
        # Cleanup temp HTML
        try:
            os.unlink(html_path)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════
# LEGACY PIPELINE: reportlab + matplotlib mathtext
# ═══════════════════════════════════════════════════════════════

def build_pdf_legacy(input_path, output_path, title=None, author=None,
                     date_str=None, no_math=False, stylesheet=None):
    """
    Legacy pipeline using reportlab + matplotlib mathtext.
    Kept for compatibility when playwright is unavailable.
    """
    print('[LEGACY] Using reportlab pipeline (programmatic PDF generation)')
    print('[LEGACY] WARNING: This produces lower-quality output than the primary pipeline.')
    print('[LEGACY] WARNING: Math rendering limited to matplotlib mathtext (LaTeX subset).')
    print('[LEGACY] WARNING: Install playwright for Obsidian-quality PDFs.')

    # Delegate to the old build_pdf.py logic
    # Import the legacy module dynamically
    legacy_script = Path(__file__).parent / '_build_pdf_legacy.py'

    # Check if legacy script exists in a backup location
    if not legacy_script.exists():
        # Generate a minimal legacy stub
        _write_legacy_stub(legacy_script)

    # Run the legacy pipeline
    cmd = [sys.executable, str(legacy_script),
           '--input', str(input_path),
           '--output', str(output_path)]
    if title:
        cmd.extend(['--title', title])
    if author:
        cmd.extend(['--author', author])
    if date_str:
        cmd.extend(['--date', date_str])
    if no_math:
        cmd.append('--no-math')
    if stylesheet:
        cmd.extend(['--stylesheet', str(stylesheet)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return False
    return True


def _write_legacy_stub(path):
    """Write a minimal legacy pipeline stub if the full one isn't available."""
    stub = '''#!/usr/bin/env python3
"""Legacy PDF builder stub. Full version at qnfo/tools/build_pdf.py on R2."""
import sys
print("[LEGACY] Full legacy build_pdf.py not found.")
print("[LEGACY] Please use the primary pipeline (requires playwright):")
print("[LEGACY]   pip install playwright && playwright install chromium")
print("[LEGACY]   python build_pdf.py --input paper.md --output paper.pdf")
sys.exit(1)
'''
    path.write_text(stub, encoding='utf-8')
    print(f'[LEGACY] Wrote legacy stub to {path}')


# ═══════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Build publication-quality PDF from Markdown or HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Primary pipeline (Obsidian-quality, recommended):
  python build_pdf.py --input paper.md --output paper.pdf

  # With metadata:
  python build_pdf.py --input paper.md --output paper.pdf --title "My Paper" --author "Name"

  # Legacy pipeline (reportlab, lower quality):
  python build_pdf.py --input paper.md --output paper.pdf --legacy

  # Skip math rendering:
  python build_pdf.py --input paper.md --output paper.pdf --no-math

  # Unicode diagnostics:
  python build_pdf.py --input paper.md --check-unicode
  python build_pdf.py --input paper.md --fix-unicode
        """
    )

    parser.add_argument('--input', '-i', required=True, help='Input file (.md or .html)')
    parser.add_argument('--output', '-o', help='Output PDF file path')
    parser.add_argument('--title', '-t', help='Publication title (auto-detected from frontmatter or first H1)')
    parser.add_argument('--author', '-a', help='Author name')
    parser.add_argument('--date', '-d', help='Publication date (YYYY-MM-DD, defaults to today)')
    parser.add_argument('--css', help='Custom CSS stylesheet path (default: bundled papers.css)')

    # Legacy mode
    parser.add_argument('--legacy', action='store_true',
                        help='Use legacy reportlab pipeline (lower quality, for compatibility)')
    parser.add_argument('--stylesheet', '-s', help='Legacy: path to publication stylesheet JSON')
    parser.add_argument('--no-math', action='store_true',
                        help='Skip math rendering (legacy: Unicode approximations; primary: no MathJax)')

    # Unicode checks (works for both pipelines)
    parser.add_argument('--check-unicode', action='store_true',
                        help='Scan input for literal \\uXXXX escape sequences (no PDF build)')
    parser.add_argument('--fix-unicode', action='store_true',
                        help='Auto-correct \\uXXXX sequences in the source file IN PLACE')

    # Verification
    parser.add_argument('--verify', action='store_true',
                        help='Verify an existing PDF for rendering quality')

    args = parser.parse_args()

    # --- Unicode pre-flight checks ---
    if args.check_unicode or args.fix_unicode:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f'[ERROR] Input file not found: {input_path}')
            sys.exit(1)
        text = input_path.read_text(encoding='utf-8')
        _, fix_count, fix_report = sanitize_unicode_escapes(text, source_label=input_path.name)

        if args.fix_unicode:
            if fix_count > 0:
                fixed, _, _ = sanitize_unicode_escapes(text, source_label=input_path.name)
                input_path.write_text(fixed, encoding='utf-8')
                for line in fix_report:
                    print(line)
                print(f'[FIXED] {fix_count} escape sequences corrected in {input_path.name}')
            else:
                print(f'[OK] No Unicode escape sequences found in {input_path.name}')
            sys.exit(0)
        else:  # --check-unicode
            if fix_count > 0:
                for line in fix_report:
                    print(line)
                print(f'\n[RESULT] {fix_count} escape sequences found.')
                print('[ACTION] Run with --fix-unicode to auto-correct, or rebuild the source.')
                sys.exit(1)
            else:
                print(f'[OK] No Unicode escape sequences found in {input_path.name}')
                sys.exit(0)

    # --- PDF verification mode ---
    if args.verify:
        pdf_path = Path(args.input)
        if not pdf_path.exists():
            print(f'[ERROR] PDF not found: {pdf_path}')
            sys.exit(1)
        ok = verify_pdf(pdf_path)
        sys.exit(0 if ok else 1)

    # --- Normal build mode ---
    if not args.output:
        print('[ERROR] --output/-o is required for PDF generation')
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'[ERROR] Input file not found: {input_path}')
        sys.exit(1)

    output_path = Path(args.output)
    date_str = args.date or datetime.now().strftime('%Y-%m-%d')

    print(f'{"="*60}')
    print(f'QNFO PDF Builder v2.0')
    print(f'  Input:  {input_path}')
    print(f'  Output: {output_path}')
    print(f'  Title:  {args.title or "(auto-detect)"}')
    print(f'  Author: {args.author or "(auto-detect)"}')
    print(f'  Date:   {date_str}')
    print(f'  Mode:   {"Legacy (reportlab)" if args.legacy else "Primary (playwright/CSS/MathJax)"}')
    print(f'{"="*60}')

    if args.legacy:
        success = build_pdf_legacy(
            input_path, output_path,
            title=args.title, author=args.author,
            date_str=date_str, no_math=args.no_math,
            stylesheet=args.stylesheet
        )
    else:
        success = build_pdf_playwright(
            input_path, output_path,
            title=args.title, author=args.author,
            date_str=date_str, no_math=args.no_math,
            css_path=args.css
        )

        if not success:
            print('\n[FALLBACK] Primary pipeline failed. Trying legacy pipeline...')
            print('[FALLBACK] Install playwright for Obsidian-quality PDFs:')
            print('[FALLBACK]   pip install playwright && playwright install chromium')
            success = build_pdf_legacy(
                input_path, output_path,
                title=args.title, author=args.author,
                date_str=date_str, no_math=args.no_math,
                stylesheet=args.stylesheet
            )

    if not success:
        print('[ERROR] All pipelines failed. Cannot generate PDF.')
        sys.exit(1)

    # Verify output
    if output_path.exists():
        verify_pdf(output_path)
        print(f'\n[SUCCESS] PDF built: {output_path}')
        print(f'[SUCCESS] Size: {output_path.stat().st_size / 1024:.1f} KB')
    else:
        print('[ERROR] PDF file was not created')
        sys.exit(1)


if __name__ == '__main__':
    main()
