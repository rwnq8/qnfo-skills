#!/usr/bin/env python3
"""
unicode-latex-preprocess.py -- Pandoc+XeLaTeX pre-build fixer (kaizen fix A1/A2)

PROBLEM (A1): XeLaTeX's default font (Latin Modern) lacks glyphs for many
Unicode math/Greek/symbol characters used in physics prose written outside
$...$ delimiters (omega, alpha, phi, pi, subscript/superscript digits,
bra-ket notation, blackboard-bold letters). These render as U+FFFD
replacement characters ("tofu") in the final PDF.

PROBLEM (A2): Pandoc's YAML `keywords:` frontmatter field is passed through
to the XeLaTeX template's XMP metadata module, which calls an undefined
\\xmpquote macro on some Pandoc/LaTeX template combinations, aborting the
build with a hard LaTeX error.

FIX:
1. Split YAML frontmatter from body. Strip `keywords:` (and any block-style
   continuation lines) from the frontmatter -- keywords are not required by
   Zenodo/D1 metadata and are not worth a broken build.
2. Convert Unicode Greek/symbol/subscript/superscript/bra-ket characters to
   their LaTeX math equivalents, but ONLY outside existing $...$ / $$...$$
   math spans (never double-convert characters a human already wrapped in
   math delimiters -- that would emit literal backslashes inside math mode).
3. Write the corrected file back (in place, or to a --out path).

Usage:
    python unicode-latex-preprocess.py paper.md
    python unicode-latex-preprocess.py paper.md --out paper.build.md

This is NOT a substitute for writing math correctly in $...$ from the start.
It is a safety net for prose Unicode characters (e.g. "the phase omega_0 is
measured in radians") that are common in physics writing outside display
math. Always re-run _check_pdf.py after building to confirm zero replacement
characters remain.
"""
import re
import sys
import argparse

# Ordered so multi-codepoint sequences (bra-ket) are handled before single
# character substitution passes over their component characters.
GREEK = {
    '\u03b1': r'\alpha', '\u03b2': r'\beta', '\u03b3': r'\gamma', '\u03b4': r'\delta',
    '\u03b5': r'\epsilon', '\u03b6': r'\zeta', '\u03b7': r'\eta', '\u03b8': r'\theta',
    '\u03b9': r'\iota', '\u03ba': r'\kappa', '\u03bb': r'\lambda', '\u03bc': r'\mu',
    '\u03bd': r'\nu', '\u03be': r'\xi', '\u03c0': r'\pi', '\u03c1': r'\rho',
    '\u03c3': r'\sigma', '\u03c4': r'\tau', '\u03c5': r'\upsilon', '\u03c6': r'\phi',
    '\u03c7': r'\chi', '\u03c8': r'\psi', '\u03c9': r'\omega',
    '\u0391': r'\Alpha', '\u0392': r'\Beta', '\u0393': r'\Gamma', '\u0394': r'\Delta',
    '\u0395': r'\Epsilon', '\u0396': r'\Zeta', '\u0397': r'\Eta', '\u0398': r'\Theta',
    '\u0399': r'\Iota', '\u039a': r'\Kappa', '\u039b': r'\Lambda', '\u039c': r'\Mu',
    '\u039d': r'\Nu', '\u039e': r'\Xi', '\u03a0': r'\Pi', '\u03a1': r'\Rho',
    '\u03a3': r'\Sigma', '\u03a4': r'\Tau', '\u03a5': r'\Upsilon', '\u03a6': r'\Phi',
    '\u03a7': r'\Chi', '\u03a8': r'\Psi', '\u03a9': r'\Omega',
}

SYMBOLS = {
    '\u221e': r'\infty', '\u2211': r'\sum', '\u220f': r'\prod', '\u222b': r'\int',
    '\u2207': r'\nabla', '\u2202': r'\partial', '\u00b1': r'\pm', '\u2213': r'\mp',
    '\u2248': r'\approx', '\u2260': r'\neq', '\u2264': r'\leq', '\u2265': r'\geq',
    '\u2192': r'\rightarrow', '\u2190': r'\leftarrow', '\u21d2': r'\Rightarrow',
    '\u2194': r'\leftrightarrow', '\u2205': r'\emptyset', '\u2229': r'\cap',
    '\u222a': r'\cup', '\u2208': r'\in', '\u2209': r'\notin', '\u2286': r'\subseteq',
    '\u00d7': r'\times', '\u00f7': r'\div', '\u00b7': r'\cdot', '\u221a': r'\sqrt{}',
    '\u2295': r'\oplus', '\u2297': r'\otimes', '\u27e8': r'\langle', '\u27e9': r'\rangle',
    '\u2124': r'\mathbb{Z}', '\u211d': r'\mathbb{R}', '\u2102': r'\mathbb{C}',
    '\u211a': r'\mathbb{Q}', '\u2115': r'\mathbb{N}',
}

SUBSCRIPT_DIGITS = {
    '\u2080': '0', '\u2081': '1', '\u2082': '2', '\u2083': '3', '\u2084': '4',
    '\u2085': '5', '\u2086': '6', '\u2087': '7', '\u2088': '8', '\u2089': '9',
}
SUPERSCRIPT_DIGITS = {
    '\u2070': '0', '\u00b9': '1', '\u00b2': '2', '\u00b3': '3', '\u2074': '4',
    '\u2075': '5', '\u2076': '6', '\u2077': '7', '\u2078': '8', '\u2079': '9',
    '\u207a': '+', '\u207b': '-',
}

# Bra-ket notation: |x>, <x|, <x|y> -- must run before generic symbol pass
BRAKET_PATTERNS = [
    (re.compile(r'\u27e8([^\u27e8\u27e9]+)\|([^\u27e8\u27e9]+)\u27e9'), r'\\langle \1 | \2 \\rangle'),
    (re.compile(r'\|([^\u27e8\u27e9|]+)\u27e9'), r'|\1\\rangle'),
    (re.compile(r'\u27e8([^\u27e8\u27e9|]+)\|'), r'\\langle \1|'),
]


def _split_math_spans(text):
    """Split text into a list of (segment, is_math) tuples on $$...$$ and $...$."""
    # Non-greedy match, allow escaped \$ to pass through unaffected.
    pattern = re.compile(r'(\$\$.*?\$\$|\$[^$\n]*?\$)', re.DOTALL)
    parts = []
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            parts.append((text[last:m.start()], False))
        parts.append((m.group(0), True))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], False))
    return parts


def convert_prose_unicode(segment):
    """Convert Unicode math characters to LaTeX ONLY within a non-math segment,
    wrapping each converted run in $...$ so LaTeX renders it as math."""
    out = []
    buf = []
    convertible = set(GREEK) | set(SYMBOLS) | set(SUBSCRIPT_DIGITS) | set(SUPERSCRIPT_DIGITS)

    i = 0
    n = len(segment)
    while i < n:
        # Try bra-ket multi-char patterns first at this position
        matched_braket = False
        for pat, repl in BRAKET_PATTERNS:
            m = pat.match(segment, i)
            if m:
                if buf:
                    out.append(''.join(buf))
                    buf = []
                out.append('$' + pat.sub(repl, m.group(0)) + '$')
                i = m.end()
                matched_braket = True
                break
        if matched_braket:
            continue

        ch = segment[i]
        if ch in convertible:
            run = []
            while i < n and segment[i] in convertible:
                c = segment[i]
                if c in GREEK:
                    run.append(GREEK[c])
                elif c in SYMBOLS:
                    run.append(SYMBOLS[c])
                elif c in SUBSCRIPT_DIGITS:
                    run.append('_{' + SUBSCRIPT_DIGITS[c] + '}')
                elif c in SUPERSCRIPT_DIGITS:
                    run.append('^{' + SUPERSCRIPT_DIGITS[c] + '}')
                i += 1
            if buf:
                out.append(''.join(buf))
                buf = []
            out.append('$' + ''.join(run) + '$')
        else:
            buf.append(ch)
            i += 1
    if buf:
        out.append(''.join(buf))
    return ''.join(out)


def strip_keywords_field(frontmatter):
    """Remove a top-level `keywords:` YAML key and any indented continuation
    lines (block scalar or list items) that belong to it."""
    lines = frontmatter.split('\n')
    out = []
    skipping = False
    for line in lines:
        if re.match(r'^keywords\s*:', line):
            skipping = True
            continue
        if skipping:
            # Continuation lines are indented or a list item (- ...)
            if re.match(r'^(\s+\S|\s*-\s)', line):
                continue
            skipping = False
        out.append(line)
    return '\n'.join(out)


def process_file(path, out_path=None):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split frontmatter (--- ... ---) from body. Guard against a body table
    # separator row also being literally "---" by only treating the FIRST
    # two "---" delimiters at the very start of the file as frontmatter.
    fm_match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = text[fm_match.end():]
        frontmatter = strip_keywords_field(frontmatter)
        header = f'---\n{frontmatter}\n---\n'
    else:
        header = ''
        body = text

    segments = _split_math_spans(body)
    new_segments = []
    for seg, is_math in segments:
        if is_math:
            new_segments.append(seg)
        else:
            new_segments.append(convert_prose_unicode(seg))
    new_body = ''.join(new_segments)

    result = header + new_body
    target = out_path or path
    with open(target, 'w', encoding='utf-8') as f:
        f.write(result)
    return target


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='Path to paper.md')
    ap.add_argument('--out', default=None, help='Output path (default: overwrite input)')
    args = ap.parse_args()

    target = process_file(args.input, args.out)
    print(f'[OK] Unicode-to-LaTeX preprocessing complete: {target}')
    print('[NOTE] Run _check_pdf.py after building to verify zero replacement characters remain.')


if __name__ == '__main__':
    main()
