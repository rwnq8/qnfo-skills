#!/usr/bin/env python3
"""
credential-scan.py -- Pre-commit credential leak scanner (kaizen fix A4/C1/D2)

PROBLEM: Ephemeral helper scripts (e.g. `_zenodo_upload.py`) written during a
session sometimes contain hardcoded API tokens for convenience. If such a
script is `git add`-ed and committed, GitHub push protection blocks the push
-- or worse, on a repo without push protection, the token leaks permanently
into git history.

FIX: Scan staged (or explicitly given) files for known token shapes before
commit. BLOCK the commit if any match is found. This is a standalone script
with zero dependencies (stdlib only) so it always runs, even in a fresh venv.

Token patterns covered:
  - Cloudflare API tokens        (cfat_...)
  - GitHub personal access token (ghp_..., github_pat_...)
  - OpenAI-style secret keys      (sk-...)
  - Generic long Bearer token     (Bearer <20+ alnum/._-  chars>)
  - Zenodo-style tokens           (40-hex-char bearer values in a header)
  - AWS access key id             (AKIA...)
  - Generic ".env"-style KEY=VALUE with SECRET/TOKEN/KEY in the name and a
    non-empty, non-placeholder value

Usage:
    python credential-scan.py <file1> [file2] ...
    python credential-scan.py --staged      # scan `git diff --cached` files

Exit code 0 = clean, 1 = credentials found (BLOCK commit), 2 = usage error.
"""
import sys
import re
import subprocess

PATTERNS = [
    ('Cloudflare API token', re.compile(r'\bcfat_[A-Za-z0-9_\-]{20,}\b')),
    ('GitHub PAT (classic)', re.compile(r'\bghp_[A-Za-z0-9]{36}\b')),
    ('GitHub PAT (fine-grained)', re.compile(r'\bgithub_pat_[A-Za-z0-9_]{20,}\b')),
    ('OpenAI/Anthropic-style secret key', re.compile(r'\bsk-[A-Za-z0-9]{20,}\b')),
    ('AWS access key id', re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
    ('Generic long Bearer token', re.compile(r'Bearer\s+[A-Za-z0-9._\-]{20,}')),
    ('Hardcoded 40-hex secret (e.g. Buffer/Zenodo token literal)',
     re.compile(r'["\']([0-9a-f]{40})["\']')),
    ('Hardcoded KEY/TOKEN/SECRET assignment',
     re.compile(r'(?i)\b([A-Z0-9_]*(?:API_?KEY|TOKEN|SECRET)[A-Z0-9_]*)\s*=\s*["\'](?!<|\$\{|process\.env|os\.environ|YOUR_|xxx|placeholder)([A-Za-z0-9._\-]{16,})["\']')),
]

# Files that are allowed to contain the *word* "token"/"secret" as
# documentation prose without triggering a false positive (skill docs that
# describe the pattern, not an actual leaked value).
DOC_EXTENSIONS = {'.md'}


def scan_text(text, filename):
    hits = []
    if any(filename.endswith(ext) for ext in DOC_EXTENSIONS):
        # Still scan docs -- a real token pasted into a doc is just as bad --
        # but skip the low-precision "KEY/TOKEN/SECRET assignment" pattern
        # since docs legitimately show `TOKEN = "<OSF_PERSONAL_ACCESS_TOKEN>"`
        # style placeholders that would otherwise false-positive.
        patterns = [p for p in PATTERNS if p[0] != 'Hardcoded KEY/TOKEN/SECRET assignment']
    else:
        patterns = PATTERNS
    for label, pat in patterns:
        for m in pat.finditer(text):
            line_no = text.count('\n', 0, m.start()) + 1
            hits.append((label, line_no, m.group(0)[:12] + '...'))
    return hits


def get_staged_files():
    out = subprocess.run(['git', 'diff', '--cached', '--name-only'],
                          capture_output=True, text=True, check=True)
    return [f for f in out.stdout.splitlines() if f.strip()]


def main():
    args = sys.argv[1:]
    if not args:
        print('Usage: python credential-scan.py <file1> [file2] ...')
        print('       python credential-scan.py --staged')
        sys.exit(2)

    if args == ['--staged']:
        files = get_staged_files()
    else:
        files = args

    total_hits = 0
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
                text = fh.read()
        except (FileNotFoundError, IsADirectoryError):
            continue
        hits = scan_text(text, f)
        for label, line_no, snippet in hits:
            print(f'[CREDENTIAL-LEAK] {f}:{line_no} -- {label} (starts: {snippet})')
            total_hits += 1

    if total_hits:
        print(f'\n[BLOCKED] {total_hits} potential credential leak(s) found. '
              f'Remove hardcoded secrets before committing -- use env vars, '
              f'~/.{{service}}_token files, or Windows Credential Manager instead. '
              f'If this is a false positive, redact and re-run.')
        sys.exit(1)

    print(f'[OK] No credential patterns found in {len(files)} file(s).')
    sys.exit(0)


if __name__ == '__main__':
    main()
