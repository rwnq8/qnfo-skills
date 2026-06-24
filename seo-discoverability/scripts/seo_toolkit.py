#!/usr/bin/env python3
"""
QNFO SEO IMPROVEMENT TOOLKIT v1.0
==================================
Generates proper robots.txt, sitemap.xml, and injects SEO meta tags
into all QNFO/QWAV Cloudflare Pages sites.

Usage:
  python seo_toolkit.py --audit      # Re-audit all sites
  python seo_toolkit.py --generate   # Generate SEO files for all sites
  python seo_toolkit.py --deploy     # Deploy all generated sites
  python seo_toolkit.py --site=qnfo.org  # Target single site
"""

import urllib.request
import urllib.error
import ssl
import re
import json
import os
import sys
import subprocess
import shutil
import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# ── Configuration ──────────────────────────────────────────────────
ACCOUNT_ID = 'edb167b78c9fb901ea5bca3ce58ccc4b'
WORK_DIR = os.path.join(os.environ.get('TEMP', '.'), 'qnfo-seo-build')
os.makedirs(WORK_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# ── Site Registry ──────────────────────────────────────────────────
SITES = {
    # Tier 1: Hub sites (highest priority)
    'qnfo-hub': {
        'project': 'qnfo-hub',
        'domains': ['qnfo.org', 'hub.qnfo.org', 'www.qnfo.org'],
        'primary': 'https://qnfo.org',
        'title': 'QNFO — Research Infrastructure',
        'description': 'QNFO is the research infrastructure behind QWAV — ultrametric quantum computing, quantum laws of form, p-adic physics, and the unified research library.',
        'type': 'WebSite',
        'tier': 1,
    },
    'qwav-marquee': {
        'project': 'qwav-marquee',
        'domains': ['qwav.tech', 'score.qwav.tech'],
        'primary': 'https://qwav.tech',
        'title': 'QWAV — Ultrametric Quantum Computing',
        'description': 'QWAV: computational evidence for ultrametric quantum computing. Zero logical errors at depth 7. 48× error reduction through passive fault tolerance.',
        'type': 'WebSite',
        'tier': 1,
    },
    'qnfo-publications': {
        'project': 'qnfo-publications',
        'domains': ['papers.qnfo.org', 'adelic-qec.qnfo.org', 'benchmark.qnfo.org',
                     'p-adic-hw.qnfo.org', 'p-adic.qnfo.org', 'uqc.qnfo.org'],
        'primary': 'https://papers.qnfo.org',
        'title': 'QNFO Publications — Unified Research Library',
        'description': 'QNFO research publications — unified library of papers on ultrametric physics, quantum laws of form, p-adic quantum error correction, and related topics.',
        'type': 'WebSite',
        'tier': 1,
    },
    # Tier 2: Publication pages (high priority)
    'quantum-laws-of-form': {
        'project': 'quantum-laws-of-form',
        'domains': ['laws.qnfo.org'],
        'primary': 'https://laws.qnfo.org',
        'title': 'Quantum Laws of Form — A Syntactic Foundation for Physics',
        'description': 'From The Calculus of Distinction to Ultrametric Cosmology. A radical re-foundation of physics based on Spencer-Brown\'s Laws of Form.',
        'type': 'Article',
        'tier': 2,
    },
    'solo-scientist': {
        'project': 'solo-scientist',
        'domains': ['solo.qnfo.org'],
        'primary': 'https://solo.qnfo.org',
        'title': 'The Force-Multiplier Playbook — Solo Scientist',
        'description': 'A practical guide for independent researchers: how to amplify research output using AI tools, automated infrastructure, and systematic workflows.',
        'type': 'Article',
        'tier': 2,
    },
    'living-paper-standalone': {
        'project': 'living-paper-standalone',
        'domains': ['living-paper.qnfo.org'],
        'primary': 'https://living-paper.qnfo.org',
        'title': 'Living Paper — Interactive arXiv Reader',
        'description': 'Interactive reader for arXiv papers with live equation rendering, citation tracking, and cross-referencing — part of the QNFO research infrastructure.',
        'type': 'WebApplication',
        'tier': 2,
    },
    'ultrametric-paradigm': {
        'project': 'ultrametric-paradigm',
        'domains': ['paradigm.qnfo.org'],
        'primary': 'https://paradigm.qnfo.org',
        'title': 'The Ultrametric Paradigm',
        'description': 'A comprehensive introduction to the ultrametric paradigm in physics: non-Archimedean geometry, p-adic numbers, and their implications for quantum theory and cosmology.',
        'type': 'Article',
        'tier': 2,
    },
    'ultrametric-quantum': {
        'project': 'ultrametric-quantum',
        'domains': ['quantum.qnfo.org'],
        'primary': 'https://quantum.qnfo.org',
        'title': 'QNFO Quantum — Ultrametric Quantum Computing Research Portal',
        'description': 'Research portal for ultrametric quantum computing: p-adic quantum error correction, adelic synthesis, and experimental protocols for non-Archimedean quantum hardware.',
        'type': 'WebSite',
        'tier': 2,
    },
    'hierarchical-universe': {
        'project': 'hierarchical-universe',
        'domains': ['hierarchy.qnfo.org'],
        'primary': 'https://hierarchy.qnfo.org',
        'title': 'The Hierarchical Universe',
        'description': 'Exploring the hierarchical structure of physical law: from Planck scale to cosmological scale through the lens of ultrametric geometry and p-adic analysis.',
        'type': 'Article',
        'tier': 2,
    },
    'unity-of-ultrametric-physics': {
        'project': 'unity-of-ultrametric-physics',
        'domains': ['unity.qnfo.org'],
        'primary': 'https://unity.qnfo.org',
        'title': 'Unity of Ultrametric Physics',
        'description': 'A unified framework connecting ultrametric geometry across quantum mechanics, quantum field theory, and cosmology — revealing deep structural commonalities.',
        'type': 'Article',
        'tier': 2,
    },
    'different-physics': {
        'project': 'different-physics',
        'domains': ['different.qnfo.org'],
        'primary': 'https://different.qnfo.org',
        'title': 'The Road Not Taken: Ultrametric Quantum Mechanics',
        'description': 'What if quantum mechanics had been built on ultrametric rather than Archimedean foundations? Exploring an alternative history of physics and its modern implications.',
        'type': 'Article',
        'tier': 2,
    },
    'two-ways-of-measuring': {
        'project': 'two-ways-of-measuring',
        'domains': ['measure.qnfo.org'],
        'primary': 'https://measure.qnfo.org',
        'title': 'Two Ways of Measuring',
        'description': 'A philosophical and mathematical exploration of measurement in Archimedean vs. ultrametric frameworks — why the choice of metric changes everything.',
        'type': 'Article',
        'tier': 2,
    },
    'knowing-patterns': {
        'project': 'knowing-patterns',
        'domains': ['knowing.qnfo.org'],
        'primary': 'https://knowing.qnfo.org',
        'title': 'Knowing Patterns — An Epistemology for People Tired of Being Fixed',
        'description': 'A pattern-based epistemology: understanding knowledge as pattern recognition across scales, from quantum measurement to social cognition.',
        'type': 'Article',
        'tier': 2,
    },
    'hensel-code': {
        'project': 'hensel-code',
        'domains': ['hensel.qnfo.org'],
        'primary': 'https://hensel.qnfo.org',
        'title': 'Hensel Code System — Exact Rational Arithmetic',
        'description': 'Hensel codes: an exact rational arithmetic system based on p-adic number theory. Applications to error-free computation in quantum simulations.',
        'type': 'Article',
        'tier': 2,
    },
    'adelic-qft': {
        'project': 'adelic-qft',
        'domains': ['adelic.qnfo.org'],
        'primary': 'https://adelic.qnfo.org',
        'title': 'Adelic Constraints on Quantum Field Theory',
        'description': 'Applying adelic analysis to constrain quantum field theories: deriving observable predictions from the simultaneous application of all p-adic completions.',
        'type': 'Article',
        'tier': 2,
    },
    'cocyle': {
        'project': 'cocyle',
        'domains': ['cocyle.qnfo.org'],
        'primary': 'https://cocyle.qnfo.org',
        'title': 'The Branch and the Shadow — Cocyle Ultrametric Cognition',
        'description': 'Cocyle: an ultrametric model of cognition based on branching decision trees and shadow representations — bridging mathematics and cognitive science.',
        'type': 'Article',
        'tier': 2,
    },
    'verb-lexicon': {
        'project': 'verb-lexicon',
        'domains': ['lexicon.qnfo.org'],
        'primary': 'https://lexicon.qnfo.org',
        'title': 'The Verb Lexicon — Describing the Patterns We Mistake for People',
        'description': 'A lexicon of patterns observed in human behavior, reframed as verbs rather than nouns: moving from identity-based to process-based understanding.',
        'type': 'Article',
        'tier': 2,
    },
    'ultrametric-ai-poc': {
        'project': 'ultrametric-ai-poc',
        'domains': ['ai-poc.qnfo.org'],
        'primary': 'https://ai-poc.qnfo.org',
        'title': 'Ultrametric AI — Proof of Concept',
        'description': 'Proof of concept for ultrametric AI architectures: leveraging p-adic distance metrics for more robust and interpretable machine learning models.',
        'type': 'Article',
        'tier': 2,
    },
    'qwav': {
        'project': 'qwav',
        'domains': ['deep.qwav.tech'],
        'primary': 'https://deep.qwav.tech',
        'title': 'QWAV Deep — Research Feed',
        'description': 'QWAV Deep research feed: the latest papers, experimental results, and theoretical developments in ultrametric quantum computing from the QWAV project.',
        'type': 'WebSite',
        'tier': 2,
    },
    'qlof-primer': {
        'project': 'qlof-primer',
        'domains': ['primer.qwav.tech'],
        'primary': 'https://primer.qwav.tech',
        'title': 'QLoF Primer — Quantum Laws of Form Introduction',
        'description': 'A gentle introduction to Quantum Laws of Form: Spencer-Brown\'s calculus of indications applied to quantum mechanics. No advanced mathematics required.',
        'type': 'Article',
        'tier': 2,
    },
    'ask-qwav': {
        'project': 'ask-qwav',
        'domains': ['ask.qwav.tech'],
        'primary': 'https://ask.qwav.tech',
        'title': 'Ask QWAV — Research Oracle',
        'description': 'Ask questions about ultrametric geometry, p-adic physics, quantum computing, and the QWAV research corpus. AI-powered research assistant.',
        'type': 'WebApplication',
        'tier': 2,
    },
    'qnfo-archive': {
        'project': 'qnfo-archive',
        'domains': ['archive.qnfo.org'],
        'primary': 'https://archive.qnfo.org',
        'title': 'QNFO Archive',
        'description': 'Permanent archive of QNFO research publications, datasets, and computational artifacts. Preserved for long-term scientific access.',
        'type': 'WebSite',
        'tier': 2,
    },
    'discovery-momentum': {
        'project': 'discovery-momentum',
        'domains': ['momentum.qnfo.org'],
        'primary': 'https://momentum.qnfo.org',
        'title': 'Discovery Momentum — QNFO',
        'description': 'Tracking research discovery momentum across the QNFO ecosystem: metrics, trends, and impact analysis for ultrametric physics research.',
        'type': 'WebSite',
        'tier': 2,
    },
    'qnfo-design-system': {
        'project': 'qnfo-design-system',
        'domains': ['design.qnfo.org'],
        'primary': 'https://design.qnfo.org',
        'title': 'QNFO Design System',
        'description': 'QNFO Unified Navigation design system — shared navigation components, analytics, and visual language for all *.qnfo.org and *.qwav.tech sites.',
        'type': 'WebSite',
        'tier': 2,
    },
    'qnfo-legal': {
        'project': 'qnfo-legal',
        'domains': ['legal.qnfo.org'],
        'primary': 'https://legal.qnfo.org',
        'title': 'QNFO Unified License Agreement v2.0',
        'description': 'QNFO Unified License Agreement (QNFO-ULA) Version 2.0. CC BY-NC-SA 4.0 base with enhanced protections for research integrity.',
        'type': 'WebSite',
        'tier': 2,
    },
    # Tier 3: pages.dev only sites
    'qnfo-ipfs-archive': {
        'project': 'qnfo-ipfs-archive',
        'domains': ['qnfo-ipfs-archive.pages.dev'],
        'primary': 'https://qnfo-ipfs-archive.pages.dev',
        'title': 'QNFO/QWAV Distributed Permanent Archive',
        'description': 'Distributed permanent archive for QNFO/QWAV research: IPFS-backed storage ensuring long-term availability and content-addressable access.',
        'type': 'WebSite',
        'tier': 3,
    },
    'uqc-benchmark': {
        'project': 'uqc-benchmark',
        'domains': ['uqc-benchmark.pages.dev'],
        'primary': 'https://uqc-benchmark.pages.dev',
        'title': 'UQC Benchmark — Ultrametric Quantum Computation Challenge',
        'description': 'Ultrametric Quantum Computation benchmark: a standardized challenge for evaluating quantum hardware against ultrametric error correction predictions.',
        'type': 'Article',
        'tier': 3,
    },
    'toward-p-adic-qec': {
        'project': 'toward-p-adic-qec',
        'domains': ['toward-p-adic-qec.pages.dev'],
        'primary': 'https://toward-p-adic-qec.pages.dev',
        'title': 'Toward p-adic Quantum Error Correction: The Metric Mismatch Hypothesis',
        'description': 'Quantum error correction has not yet been demonstrated at scale. We propose the metric mismatch hypothesis: current QEC uses Archimedean geometry, but quantum errors may follow ultrametric structure.',
        'type': 'ScholarlyArticle',
        'tier': 3,
    },
    'ultrametric-benchmark': {
        'project': 'ultrametric-benchmark',
        'domains': ['ultrametric-benchmark.pages.dev'],
        'primary': 'https://ultrametric-benchmark.pages.dev',
        'title': 'Testing for Ultrametric Error Structure in Quantum Hardware: An Experimental Protocol',
        'description': 'Experimental protocol for detecting ultrametric error structure in quantum hardware. Statistical tests and measurement procedures for validating the metric mismatch hypothesis.',
        'type': 'ScholarlyArticle',
        'tier': 3,
    },
    'p-adic-hardware-co-design': {
        'project': 'p-adic-hardware-co-design',
        'domains': ['p-adic-hardware-co-design.pages.dev'],
        'primary': 'https://p-adic-hardware-co-design.pages.dev',
        'title': 'p-adic Quantum Hardware: Qubit Layouts for Ultrametric Error Correction',
        'description': 'Designing quantum hardware layouts optimized for p-adic (ultrametric) error correction: qubit connectivity graphs, gate architectures, and fabrication considerations.',
        'type': 'ScholarlyArticle',
        'tier': 3,
    },
    'adelic-qec-synthesis': {
        'project': 'adelic-qec-synthesis',
        'domains': ['adelic-qec-synthesis.pages.dev'],
        'primary': 'https://adelic-qec-synthesis.pages.dev',
        'title': 'Adelic Quantum Error Correction: A Synthesis Across All Primes',
        'description': 'A unified adelic framework for quantum error correction synthesizing p-adic codes across all primes — achieving universal protection through simultaneous ultrametric encoding.',
        'type': 'ScholarlyArticle',
        'tier': 3,
    },
}

# ── Utility Functions ──────────────────────────────────────────────

def fetch_url(url, timeout=15):
    """Fetch a URL and return (status, content_type, body)"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; QNFO-SEO-Bot/1.0)'
        })
        r = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        ct = r.headers.get('Content-Type', 'unknown')
        body = r.read().decode('utf-8', errors='ignore')
        return r.status, ct, body
    except Exception as e:
        return None, None, str(e)

def generate_robots_txt(site_key):
    """Generate proper robots.txt content"""
    site = SITES[site_key]
    primary = site['primary']
    domain = primary.replace('https://', '').replace('http://', '')
    
    lines = [
        'User-agent: *',
        'Allow: /',
        '',
        f'Sitemap: {primary}/sitemap.xml',
        '',
        '# AI Crawlers — all QNFO research is open access',
        'User-agent: GPTBot',
        'Allow: /',
        'User-agent: Claude-Web',
        'Allow: /',
        'User-agent: anthropic-ai',
        'Allow: /',
        'User-agent: PerplexityBot',
        'Allow: /',
        'User-agent: Google-Extended',
        'Allow: /',
        'User-agent: CCBot',
        'Allow: /',
        '',
        '# Crawl-delay: polite crawling requested',
        'Crawl-delay: 2',
    ]
    return '\n'.join(lines)

def generate_sitemap_xml(site_key, urls=None):
    """Generate proper sitemap.xml content"""
    site = SITES[site_key]
    primary = site['primary']
    
    if urls is None:
        urls = [primary + '/']
        for d in site.get('domains', []):
            if d != primary.replace('https://', '').replace('http://', ''):
                alt = 'https://' + d if not d.startswith('http') else d
                if alt != primary:
                    urls.append(alt + '/')
    
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    today = datetime.date.today().isoformat()
    
    for i, url in enumerate(urls):
        url_el = SubElement(urlset, 'url')
        loc = SubElement(url_el, 'loc')
        loc.text = url
        lastmod = SubElement(url_el, 'lastmod')
        lastmod.text = today
        changefreq = SubElement(url_el, 'changefreq')
        changefreq.text = 'weekly' if i == 0 else 'monthly'
        priority = SubElement(url_el, 'priority')
        priority.text = '1.0' if i == 0 else '0.8'
    
    xml_str = minidom.parseString(tostring(urlset, 'utf-8')).toprettyxml(indent='  ')
    return xml_str

def generate_seo_meta_tags(site_key):
    """Generate SEO meta tags HTML snippet"""
    site = SITES[site_key]
    primary = site['primary']
    title = site['title']
    desc = site['description']
    site_type = site.get('type', 'WebSite')
    
    # Build the meta tags as a string
    tags = []
    tags.append(f'<title>{title}</title>')
    tags.append(f'<meta name="description" content="{desc}">')
    tags.append(f'<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">')
    
    # Open Graph
    tags.append(f'<meta property="og:title" content="{title}">')
    tags.append(f'<meta property="og:description" content="{desc}">')
    tags.append(f'<meta property="og:url" content="{primary}/">')
    tags.append(f'<meta property="og:type" content="{site_type.lower()}">')
    tags.append(f'<meta property="og:site_name" content="QNFO Research">')
    tags.append(f'<meta property="og:locale" content="en_US">')
    
    # Twitter Card
    tags.append(f'<meta name="twitter:card" content="summary_large_image">')
    tags.append(f'<meta name="twitter:title" content="{title}">')
    tags.append(f'<meta name="twitter:description" content="{desc}">')
    
    # Canonical
    tags.append(f'<link rel="canonical" href="{primary}/">')
    
    today = datetime.date.today().isoformat()
    
    # Structured Data (JSON-LD)
    if site_type == 'ScholarlyArticle':
        ld = {
            '@context': 'https://schema.org',
            '@type': 'ScholarlyArticle',
            'headline': title,
            'description': desc,
            'url': primary + '/',
            'author': {
                '@type': 'Person',
                'name': 'Rowan Brad Quni-Gudzinas'
            },
            'publisher': {
                '@type': 'Organization',
                'name': 'QNFO Research',
                'url': 'https://qnfo.org'
            },
            'datePublished': today,
            'dateModified': today,
            'inLanguage': 'en',
            'isAccessibleForFree': True,
            'license': 'https://legal.qnfo.org'
        }
    elif site_type == 'Article':
        ld = {
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': title,
            'description': desc,
            'url': primary + '/',
            'author': {
                '@type': 'Person',
                'name': 'Rowan Brad Quni-Gudzinas'
            },
            'publisher': {
                '@type': 'Organization',
                'name': 'QNFO Research',
                'url': 'https://qnfo.org'
            },
            'datePublished': today,
            'dateModified': today,
            'inLanguage': 'en',
            'isAccessibleForFree': True
        }
    else:
        ld = {
            '@context': 'https://schema.org',
            '@type': 'WebSite',
            'name': title,
            'description': desc,
            'url': primary + '/',
            'author': {
                '@type': 'Organization',
                'name': 'QNFO Research'
            }
        }
    
    tags.append(f'<script type="application/ld+json">\n{json.dumps(ld, indent=2)}\n</script>')
    
    return '\n'.join(tags)


def inject_seo_into_html(html_content, site_key):
    """Inject SEO meta tags into existing HTML"""
    site = SITES[site_key]
    seo_tags = generate_seo_meta_tags(site_key)
    primary = site['primary']
    
    # Strategy: replace/add tags in <head>
    # 1. Remove any existing <title> tag
    html_content = re.sub(r'<title>[^<]*</title>', '', html_content, flags=re.I)
    # 2. Remove any existing meta description
    html_content = re.sub(r'<meta[^>]+name=["\']description["\'][^>]*>', '', html_content, flags=re.I)
    # 3. Remove any existing og: tags
    html_content = re.sub(r'<meta[^>]+property=["\']og:[^"\']+["\'][^>]*>', '', html_content, flags=re.I)
    # 4. Remove any existing twitter: tags
    html_content = re.sub(r'<meta[^>]+name=["\']twitter:[^"\']+["\'][^>]*>', '', html_content, flags=re.I)
    # 5. Remove any existing canonical
    html_content = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', '', html_content, flags=re.I)
    # 6. Remove any existing JSON-LD
    html_content = re.sub(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>', '', html_content, flags=re.I | re.S)
    # 7. Remove any existing robots meta
    html_content = re.sub(r'<meta[^>]+name=["\']robots["\'][^>]*>', '', html_content, flags=re.I)
    
    # Insert SEO tags right after <head> or after <meta charset>
    head_match = re.search(r'<head[^>]*>', html_content, re.I)
    if head_match:
        insert_pos = head_match.end()
        html_content = html_content[:insert_pos] + '\n' + seo_tags + '\n' + html_content[insert_pos:]
    else:
        # No head tag — prepend
        html_content = '<head>\n' + seo_tags + '\n</head>\n' + html_content
    
    return html_content


def build_site_directory(site_key, download_html=True):
    """Build a complete deployable directory for a site"""
    site = SITES[site_key]
    project = site['project']
    primary = site['primary']
    
    build_dir = os.path.join(WORK_DIR, project)
    os.makedirs(build_dir, exist_ok=True)
    
    print(f'\n{"="*60}')
    print(f'Building: {site_key} ({project})')
    print(f'  Primary: {primary}')
    
    # Generate robots.txt
    robots_content = generate_robots_txt(site_key)
    robots_path = os.path.join(build_dir, 'robots.txt')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print(f'  [OK] robots.txt ({len(robots_content)} bytes)')
    
    # Generate sitemap.xml
    sitemap_content = generate_sitemap_xml(site_key)
    sitemap_path = os.path.join(build_dir, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f'  [OK] sitemap.xml ({len(sitemap_content)} bytes)')
    
    # Generate _headers file for Cloudflare Pages
    headers_content = f"""/robots.txt
  Content-Type: text/plain

/sitemap.xml
  Content-Type: application/xml

/*
  X-Robots-Tag: index, follow
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
"""
    headers_path = os.path.join(build_dir, '_headers')
    with open(headers_path, 'w', encoding='utf-8') as f:
        f.write(headers_content)
    print(f'  [OK] _headers file')
    
    # Try to download and inject SEO into HTML
    if download_html:
        print(f'  Downloading HTML from {primary}...')
        status, ct, body = fetch_url(primary)
        if status == 200 and body:
            # Check if robots/sitemap currently return HTML (broken)
            r_status, r_ct, r_body = fetch_url(primary + '/robots.txt')
            s_status, s_ct, s_body = fetch_url(primary + '/sitemap.xml')
            
            current_robots_ok = r_status == 200 and 'text/plain' in str(r_ct)
            current_sitemap_ok = s_status == 200 and 'xml' in str(s_ct).lower()
            
            print(f'  Current robots.txt: {"OK" if current_robots_ok else "BROKEN (HTML)"}')
            print(f'  Current sitemap.xml: {"OK" if current_sitemap_ok else "BROKEN (HTML)"}')
            
            # Inject SEO tags
            modified_html = inject_seo_into_html(body, site_key)
            
            # Also create a _redirects file if the site is an SPA
            html_path = os.path.join(build_dir, 'index.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(modified_html)
            print(f'  [OK] index.html with SEO tags ({len(modified_html)} bytes)')
            
            # Create 404.html fallback
            notfound_path = os.path.join(build_dir, '404.html')
            with open(notfound_path, 'w', encoding='utf-8') as f:
                f.write(modified_html)  # SPA fallback
            print(f'  [OK] 404.html fallback')
    
    return build_dir


def deploy_site(site_key, dry_run=False):
    """Deploy a built site to Cloudflare Pages"""
    site = SITES[site_key]
    project = site['project']
    build_dir = os.path.join(WORK_DIR, project)
    
    if not os.path.isdir(build_dir):
        print(f'  [SKIP] Build directory not found: {build_dir}')
        return False
    
    print(f'\n  Deploying {project} to Cloudflare Pages...')
    
    if dry_run:
        print(f'  [DRY RUN] Would deploy: wrangler pages deploy {build_dir} --project-name {project} --branch main')
        return True
    
    try:
        node_dir = r'C:\Users\LENOVO\AppData\Local\Programs\DeepChat\resources\app.asar.unpacked\runtime\node'
        npx_cmd = os.path.join(node_dir, 'npx.cmd')
        deploy_cmd = f'"{npx_cmd}" wrangler pages deploy "{build_dir}" --project-name {project} --branch main'
        env = os.environ.copy()
        env['PATH'] = node_dir + os.pathsep + env.get('PATH', '')
        result = subprocess.run(deploy_cmd, capture_output=True, text=True, timeout=120,
                                cwd=WORK_DIR, env=env, shell=True)
        print(result.stdout[-500:] if result.stdout else '')
        if result.returncode != 0:
            print(f'  [ERROR] Deploy failed: {result.stderr[-300:]}')
            return False
        print(f'  [OK] Deployed successfully')
        return True
    except subprocess.TimeoutExpired:
        print(f'  [ERROR] Deploy timed out')
        return False
    except Exception as e:
        print(f'  [ERROR] {e}')
        return False


# ── Main ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='QNFO SEO Improvement Toolkit')
    parser.add_argument('--tier', type=int, default=0, help='Process only this tier (1-3, 0=all)')
    parser.add_argument('--site', type=str, help='Process only this site key')
    parser.add_argument('--deploy', action='store_true', help='Deploy after building')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (no actual deploy)')
    parser.add_argument('--audit-only', action='store_true', help='Only audit, no changes')
    args = parser.parse_args()
    
    sites_to_process = SITES
    if args.site:
        if args.site in SITES:
            sites_to_process = {args.site: SITES[args.site]}
        else:
            print(f'Unknown site: {args.site}')
            print(f'Available: {", ".join(SITES.keys())}')
            sys.exit(1)
    elif args.tier > 0:
        sites_to_process = {k: v for k, v in SITES.items() if v['tier'] == args.tier}
    
    print(f'QNFO SEO Improvement Toolkit v1.0')
    print(f'Processing {len(sites_to_process)} sites (tier filter: {args.tier or "all"})')
    print(f'Work directory: {WORK_DIR}')
    print()
    
    success_count = 0
    fail_count = 0
    
    for site_key in sorted(sites_to_process.keys(), key=lambda k: SITES[k]['tier']):
        try:
            build_dir = build_site_directory(site_key)
            if args.deploy or args.dry_run:
                ok = deploy_site(site_key, dry_run=args.dry_run)
                if ok:
                    success_count += 1
                else:
                    fail_count += 1
            else:
                success_count += 1
        except Exception as e:
            print(f'  [FAIL] {site_key}: {e}')
            fail_count += 1
    
    print(f'\n{"="*60}')
    print(f'DONE: {success_count} succeeded, {fail_count} failed')
    print(f'Build artifacts: {WORK_DIR}')
