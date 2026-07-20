#!/usr/bin/env python3
"""
check-pdf.py -- PDF rendering + integrity verification (kaizen fix B4/B5)

FIX B4: Verifies PyMuPDF (`fitz`) is actually installed before importing it,
with a clear remediation message, instead of a raw ModuleNotFoundError
traceback that looks like a build failure.

FIX B5: When (re)writing/replacing a PDF that a viewer application has open
for reading, `os.replace()` can raise PermissionError on Windows. This script
does not itself replace files, but the build pipeline that calls it should
follow the retry pattern documented in `replace_with_retry()` below. Import
and reuse this helper from your build script instead of calling
`os.replace()` directly.

Checks performed on the target PDF:
1. Opens without error (corrupt PDF detection)
2. Zero pages containing U+FFFD (replacement character -- Unicode glyph miss)
3. Zero completely empty pages (get_text() returns only whitespace)
4. Page count > 0
5. Reports per-page character count for a quick sanity skim

Usage:
    python check-pdf.py paper.pdf
"""
import sys
import time
import os
import shutil


def _require_fitz():
    try:
        import fitz  # PyMuPDF
        return fitz
    except ImportError:
        print('[BLOCKED] PyMuPDF is not installed. Install it first:')
        print('    pip install PyMuPDF')
        print('Verify with: pip show PyMuPDF')
        sys.exit(2)


def replace_with_retry(src, dst, attempts=3, delay_s=2):
    """Replace dst with src, retrying if dst is locked (e.g. open in a PDF
    viewer on Windows raises PermissionError on os.replace). Falls back to
    writing a timestamped sibling file if all retries fail, so the build
    never silently appears to succeed while leaving stale content in place.
    """
    last_err = None
    for i in range(attempts):
        try:
            os.replace(src, dst)
            return dst
        except PermissionError as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(delay_s)
    # All retries failed -- likely a PDF viewer holds a lock on dst.
    fallback = dst.rsplit('.', 1)[0] + f'.{int(time.time())}.pdf'
    shutil.copy2(src, fallback)
    print(f'[WARN] Could not replace {dst} (locked by another process, e.g. an open PDF '
          f'viewer). Wrote to {fallback} instead. Close the viewer and re-run the build, '
          f'or manually rename {fallback} -> {dst}.')
    raise last_err


def check_pdf(path):
    fitz = _require_fitz()
    try:
        doc = fitz.open(path)
    except Exception as e:
        print(f'[BLOCKED] PDF failed to open (corrupt or invalid): {e}')
        return 1

    if doc.page_count == 0:
        print('[BLOCKED] PDF has zero pages.')
        return 1

    errors = []
    empty_pages = []
    for page in doc:
        text = page.get_text()
        if '\ufffd' in text:
            count = text.count('\ufffd')
            errors.append(f'Page {page.number}: {count} REPLACEMENT CHARACTER(s) found '
                           f'(Unicode glyph missing from XeLaTeX font -- run '
                           f'unicode-latex-preprocess.py and rebuild)')
        if not text.strip():
            empty_pages.append(page.number)

    print(f'[INFO] Pages: {doc.page_count}')
    for page in doc:
        print(f'[INFO] Page {page.number}: {len(page.get_text())} chars')

    if empty_pages:
        errors.append(f'Empty pages (no extractable text): {empty_pages}')

    if errors:
        print('[BLOCKED] PDF verification failed:')
        for e in errors:
            print(f'  - {e}')
        return 1

    print('[OK] PDF rendering verified -- no replacement characters, no empty pages.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python check-pdf.py <path-to-pdf>')
        sys.exit(2)
    sys.exit(check_pdf(sys.argv[1]))
