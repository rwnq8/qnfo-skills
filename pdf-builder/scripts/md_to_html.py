#!/usr/bin/env python3
"""
md_to_html.py -- Markdown to styled HTML converter for QNFO publications.
v1.0 - 2026-06-28

Converts .md files to standalone HTML with embedded CSS + MathJax.
Designed for the MD->HTML->playwright PDF pipeline (Obsidian-quality output).

Usage:
  python md_to_html.py --input paper.md --output paper.html
  python md_to_html.py --input paper.md --output paper.html --title "My Paper" --author "Name" --date "2026-06-28"
  python md_to_html.py --input paper.md --output paper.html --no-math
"""

import argparse
import re
import sys
import os
from pathlib import Path
from datetime import datetime

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

import markdown


def strip_yaml_frontmatter(text):
    if not text.startswith('---'):
        return {}, text

    end = text.find(chr(10) + '---' + chr(10), 3)
    if end == -1:
        end = text.find(chr(10) + '---' + chr(13) + chr(10), 3)
    if end == -1:
        end = text.find(chr(13) + chr(10) + '---' + chr(13) + chr(10), 3)
    if end == -1:
        return {}, text

    end += len(text[end:].split(chr(10))[0]) + 1
    yaml_text = text[3:end].strip()
    content = text[end:].strip()
    if content.startswith('---'):
        content = content[3:].strip()

    metadata = {}
    if HAS_YAML and yaml_text:
        try:
            parsed = yaml.safe_load(yaml_text)
            if isinstance(parsed, dict):
                metadata = parsed
        except Exception:
            pass

    if not metadata and yaml_text:
        for line in yaml_text.split(chr(10)):
            line = line.strip()
            if ':' in line:
                key, sep, val = line.partition(':')
                key = key.strip()
                val = val.strip().strip(chr(34)).strip(chr(39))
                if key and val and key != 'abstract':
                    metadata[key] = val
                elif key == 'abstract' and len(val) > 1:
                    metadata[key] = val

    return metadata, content



def get_mathjax_config():
    """Generate MathJax 3 configuration with QNFO standard macros."""
    return """    <script>
    window.MathJax = {
      tex: {
        inlineMath: [["$","$"]],
        displayMath: [["$$","$$"]],
        processEscapes: true,
        processEnvironments: true,
        packages: {"[+]": ["boldsymbol", "ams", "amscd", "braket", "color", "newcommand"]},
        macros: {
          RR: "\\\\mathbb{R}",
          ZZ: "\\\\mathbb{Z}",
          NN: "\\\\mathbb{N}",
          CC: "\\\\mathbb{C}",
          QQ: "\\\\mathbb{Q}",
          FF: "\\\\mathbb{F}",
          PP: "\\\\mathbb{P}",
          EE: "\\\\mathbb{E}",
          HH: "\\\\mathbb{H}",
          calA: "\\\\mathcal{A}",
          calB: "\\\\mathcal{B}",
          calC: "\\\\mathcal{C}",
          calF: "\\\\mathcal{F}",
          calL: "\\\\mathcal{L}",
          calO: "\\\\mathcal{O}",
          calP: "\\\\mathcal{P}",
          calR: "\\\\mathcal{R}",
          calS: "\\\\mathcal{S}",
          calT: "\\\\mathcal{T}",
          calU: "\\\\mathcal{U}",
          calX: "\\\\mathcal{X}",
          eps: "\\\\varepsilon",
          vphi: "\\\\varphi",
          Aut: "\\\\operatorname{Aut}",
          Gal: "\\\\operatorname{Gal}",
          End: "\\\\operatorname{End}",
          Hom: "\\\\operatorname{Hom}",
          im: "\\\\operatorname{im}",
          ker: "\\\\operatorname{ker}",
          Spec: "\\\\operatorname{Spec}",
          GL: "\\\\operatorname{GL}",
          SL: "\\\\operatorname{SL}",
          SO: "\\\\operatorname{SO}",
          SU: "\\\\operatorname{SU}",
          Sp: "\\\\operatorname{Sp}",
          rank: "\\\\operatorname{rank}",
          tr: "\\\\operatorname{tr}",
          det: "\\\\operatorname{det}",
          diag: "\\\\operatorname{diag}",
          ord: "\\\\operatorname{ord}",
          val: "\\\\operatorname{val}",
          norm: "\\\\operatorname{norm}",
          disc: "\\\\operatorname{disc}",
          Res: "\\\\operatorname{Res}",
          frakG: "\\\\mathfrak{g}",
          frakH: "\\\\mathfrak{h}",
          frakP: "\\\\mathfrak{p}",
          frakM: "\\\\mathfrak{m}",
          QNFO: "\\\\text{QNFO}",
          QWAV: "\\\\text{QWAV}"
        }
      },
      chtml: {
        scale: 1,
        minScale: 0.7,
        matchFontHeight: true,
        mtextInheritFont: true,
        merrorInheritFont: true,
        mathmlSpacing: false,
        displayAlign: "center",
        displayIndent: "0"
      },
      options: {
        ignoreHtmlClass: "no-mathjax",
        processHtmlClass: "mathjax-process"
      }
    };
    </script>"""


def build_html(title, author, date_str, abstract, license_str, body_html, css_inline, use_mathjax=True):
    """Generate complete standalone HTML document."""

    mathjax_block = ''
    if use_mathjax:
        mathjax_block = get_mathjax_config() + '\n'
        mathjax_block += '    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'

    metadata_html = ''
    if author or date_str or license_str:
        metadata_html += '<div class="pub-metadata">\n'
        if author:
            metadata_html += f'  <span class="author">{author}</span>\n'
        if date_str:
            metadata_html += f'  <span class="date">{date_str}</span>\n'
        if license_str:
            metadata_html += f'  <span class="license">{license_str}</span>\n'
        metadata_html += '</div>\n'

    abstract_html = ''
    if abstract:
        abstract_html = f'''<div class="pub-abstract">
  <div class="pub-abstract-title">Abstract</div>
  <p>{abstract}</p>
</div>
'''

    title_html = f'<h1>{title}</h1>\n' if title else ''

    desc = abstract[:200] + '...' if abstract and len(abstract) > 200 else (abstract or title or '')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <meta name="citation_title" content="{title or ''}">
    <meta name="citation_author" content="{author or ''}">
    <meta name="citation_publication_date" content="{date_str or ''}">
    <title>{title or 'Publication'}</title>
    <style>
{css_inline}
    </style>
{mathjax_block}
</head>
<body>
{title_html}
{metadata_html}
{abstract_html}
{body_html}
</body>
</html>'''


def convert_md_to_html(text):
    """Convert markdown text to HTML body using Python-Markdown with extensions."""
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.attr_list',
        'markdown.extensions.footnotes',
        'markdown.extensions.sane_lists',
        'markdown.extensions.nl2br',
        'markdown.extensions.admonition',
    ]

    md = markdown.Markdown(extensions=extensions, output_format='html5')
    body = md.convert(text)

    # Post-process: wrap display math in centered paragraphs for better layout
    def math_block_replacer(m):
        expr = m.group(1)
        return f'\n<p style="text-align:center">$${expr}$$</p>\n'

    body = re.sub(r'\$\$([^$]+?)\$\$', math_block_replacer, body)

    return body


def load_css(css_path=None):
    """Load CSS stylesheet. Uses bundled papers.css if no path provided."""
    if css_path:
        p = Path(css_path)
        if p.exists():
            return p.read_text(encoding='utf-8')
        print(f'[WARNING] CSS not found: {css_path}, using bundled papers.css')

    search_paths = [
        Path(__file__).parent.parent / 'references' / 'papers.css',
        Path(os.environ.get('APPDATA', '.')) / 'DeepChat' / 'skills' / 'pdf-builder' / 'references' / 'papers.css',
    ]

    for sp in search_paths:
        if sp.exists():
            return sp.read_text(encoding='utf-8')

    print('[ERROR] Cannot find papers.css stylesheet!')
    print('[ERROR] Searched:', [str(p) for p in search_paths])
    sys.exit(1)


def validate_html(html_path):
    """Quick validation: check MathJax config ordering and key elements."""
    html = html_path.read_text(encoding='utf-8')

    config_pos = html.find('window.MathJax')
    script_pos = html.find('MathJax-script')

    if config_pos != -1 and script_pos != -1:
        if config_pos > script_pos:
            print('[VALIDATE] CRITICAL: MathJax config AFTER script tag! Math WILL NOT render.')
        else:
            print('[VALIDATE] MathJax config ordering: OK')
    elif config_pos == -1:
        print('[VALIDATE] No MathJax (--no-math mode)')

    checks = {
        '<!DOCTYPE html>': 'DOCTYPE',
        '<style>': 'embedded CSS',
        '<h1>': 'Title heading',
        '</html>': 'Closing html tag',
    }
    for needle, label in checks.items():
        status = 'OK' if needle in html else 'MISSING'
        print(f'[VALIDATE] {label}: {status}')


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to styled HTML for QNFO publications')
    parser.add_argument('--input', '-i', required=True, help='Input markdown file (.md)')
    parser.add_argument('--output', '-o', help='Output HTML file (default: input_stem.html)')
    parser.add_argument('--title', '-t', help='Publication title (auto-detected from frontmatter or first H1)')
    parser.add_argument('--author', '-a', help='Author name')
    parser.add_argument('--date', '-d', help='Publication date (YYYY-MM-DD, defaults to today)')
    parser.add_argument('--css', help='Custom CSS stylesheet path (default: bundled papers.css)')
    parser.add_argument('--no-math', action='store_true', help='Skip MathJax embedding')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'[ERROR] Input file not found: {input_path}')
        sys.exit(1)

    text = input_path.read_text(encoding='utf-8')
    metadata, body_text = strip_yaml_frontmatter(text)

    title = args.title or metadata.get('title', '')
    if not title:
        m = re.search(r'^#\s+(.+)$', body_text, re.MULTILINE)
        if m:
            title = m.group(1).strip()

    author = args.author or metadata.get('author', '')
    date_str = args.date or metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
    abstract = metadata.get('abstract', '')
    license_str = metadata.get('license', '')

    print(f'[META] Title: {title}')
    print(f'[META] Author: {author}')
    print(f'[META] Date: {date_str}')
    if abstract:
        print(f'[META] Abstract: {len(abstract)} chars')

    css = load_css(args.css)
    print(f'[CSS] Loaded stylesheet ({len(css)} bytes)')

    body_html = convert_md_to_html(body_text)
    print(f'[MD->HTML] Converted ({len(body_html)} bytes output)')

    html = build_html(
        title=title,
        author=author,
        date_str=date_str,
        abstract=abstract,
        license_str=license_str,
        body_html=body_html,
        css_inline=css,
        use_mathjax=not args.no_math,
    )

    output_path = Path(args.output) if args.output else input_path.with_suffix('.html')
    output_path.write_text(html, encoding='utf-8')
    print(f'[OK] HTML written to {output_path} ({len(html):,} bytes)')

    validate_html(output_path)


if __name__ == '__main__':
    main()
