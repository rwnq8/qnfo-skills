#!/usr/bin/env python3
"""
QNFO SEO PHASE 2 — AI CRAWLER DISCOVERABILITY LAYER
=====================================================
Generates:
  1. llms.txt — AI crawler content manifest (llmstxt.org standard)
  2. llms-full.txt — Full content for AI ingestion (key sites)
  3. Enhanced JSON-LD with topic taxonomy, cross-references, sameAs
  4. Topic taxonomy bridging all disciplines
  5. ai.txt — AI agent permissions manifest

Usage:
  python seo_phase2.py --build    # Build all Phase 2 artifacts
  python seo_phase2.py --deploy   # Deploy to Cloudflare Pages
  python seo_phase2.py --site=qnfo-hub  # Single site
"""

import urllib.request
import urllib.error
import ssl
import re
import json
import os
import sys
import subprocess
import datetime
import html

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

WORK_DIR = os.path.join(os.environ.get('TEMP', '.'), 'qnfo-seo-build')

# ── TOPIC TAXONOMY ──────────────────────────────────────────────────
# This taxonomy bridges ALL QNFO/QWAV disciplines, enabling AI crawlers
# to discover content across seemingly unrelated domains

TOPIC_TAXONOMY = {
    # Core Research
    'quantum-computing': {
        'label': 'Quantum Computing',
        'keywords': ['quantum', 'qubit', 'error correction', 'QEC', 'fault tolerance',
                     'quantum hardware', 'quantum circuit', 'logical qubit', 'quantum gate'],
        'related': ['mathematics', 'physics', 'computer-science'],
        'sites': ['qwav.tech', 'deep.qwav.tech', 'score.qwav.tech',
                  'uqc-benchmark.pages.dev', 'ultrametric-benchmark.pages.dev',
                  'quantum.qnfo.org'],
    },
    'p-adic-mathematics': {
        'label': 'p-adic Mathematics',
        'keywords': ['p-adic', 'ultrametric', 'non-archimedean', 'hensel', 'adelic',
                     'prime number', 'valuation', 'completion', 'berkovich'],
        'related': ['mathematics', 'number-theory', 'quantum-computing', 'physics'],
        'sites': ['hensel.qnfo.org', 'adelic.qnfo.org', 'p-adic.qnfo.org',
                  'p-adic-hw.qnfo.org', 'paradigm.qnfo.org'],
    },
    'mathematics': {
        'label': 'Mathematics',
        'keywords': ['mathematics', 'geometry', 'algebra', 'topology', 'metric',
                     'distance', 'analysis', 'synthesis', 'measurement'],
        'related': ['p-adic-mathematics', 'physics', 'philosophy', 'quantum-computing'],
        'sites': ['laws.qnfo.org', 'measure.qnfo.org', 'paradigm.qnfo.org',
                  'unity.qnfo.org'],
    },
    'physics': {
        'label': 'Theoretical Physics',
        'keywords': ['physics', 'quantum mechanics', 'quantum field theory', 'cosmology',
                     'universe', 'hierarchy', 'scale', 'Planck', 'spacetime'],
        'related': ['mathematics', 'cosmology', 'quantum-computing', 'philosophy'],
        'sites': ['hierarchy.qnfo.org', 'different.qnfo.org', 'paradigm.qnfo.org',
                  'unity.qnfo.org', 'quantum.qnfo.org', 'laws.qnfo.org'],
    },
    'cosmology': {
        'label': 'Cosmology',
        'keywords': ['cosmology', 'universe', 'cosmic', 'scale', 'hierarchy',
                     'structure', 'emergence', 'big picture'],
        'related': ['physics', 'philosophy', 'spirituality'],
        'sites': ['hierarchy.qnfo.org', 'unity.qnfo.org', 'paradigm.qnfo.org'],
    },
    'philosophy': {
        'label': 'Philosophy of Science',
        'keywords': ['philosophy', 'epistemology', 'ontology', 'knowledge', 'truth',
                     'reality', 'measurement', 'observer', 'consciousness'],
        'related': ['self-help', 'spirituality', 'mathematics', 'physics', 'cognition'],
        'sites': ['laws.qnfo.org', 'knowing.qnfo.org', 'measure.qnfo.org',
                  'different.qnfo.org'],
    },
    'self-help': {
        'label': 'Self-Help & Personal Development',
        'keywords': ['playbook', 'force multiplier', 'solo scientist', 'productivity',
                     'tools', 'workflow', 'independent researcher', 'amplify',
                     'automation', 'systematic', 'patterns'],
        'related': ['philosophy', 'cognition', 'spirituality'],
        'sites': ['solo.qnfo.org', 'knowing.qnfo.org'],
    },
    'spirituality': {
        'label': 'Spirituality & Meaning',
        'keywords': ['spirituality', 'meaning', 'purpose', 'unity', 'connection',
                     'transcendence', 'wholeness', 'pattern', 'form', 'distinction'],
        'related': ['philosophy', 'cosmology', 'self-help', 'cognition'],
        'sites': ['laws.qnfo.org', 'cocyle.qnfo.org', 'knowing.qnfo.org',
                  'unity.qnfo.org', 'hierarchy.qnfo.org'],
    },
    'cognition': {
        'label': 'Cognition & Mind',
        'keywords': ['cognition', 'mind', 'thought', 'pattern recognition', 'decision',
                     'branch', 'shadow', 'consciousness', 'intelligence', 'AI'],
        'related': ['philosophy', 'self-help', 'spirituality', 'computer-science'],
        'sites': ['cocyle.qnfo.org', 'knowing.qnfo.org', 'lexicon.qnfo.org',
                  'ai-poc.qnfo.org'],
    },
    'computer-science': {
        'label': 'Computer Science & AI',
        'keywords': ['AI', 'machine learning', 'computation', 'algorithm', 'proof of concept',
                     'architecture', 'benchmark', 'protocol'],
        'related': ['quantum-computing', 'cognition', 'mathematics'],
        'sites': ['ai-poc.qnfo.org', 'uqc-benchmark.pages.dev',
                  'ultrametric-benchmark.pages.dev', 'living-paper.qnfo.org'],
    },
    'number-theory': {
        'label': 'Number Theory',
        'keywords': ['number theory', 'prime', 'rational', 'integer', 'code',
                     'arithmetic', 'exact', 'error-free'],
        'related': ['p-adic-mathematics', 'mathematics'],
        'sites': ['hensel.qnfo.org', 'adelic.qnfo.org'],
    },
    'research-methodology': {
        'label': 'Research Methodology',
        'keywords': ['research', 'methodology', 'infrastructure', 'archive', 'publication',
                     'library', 'discovery', 'momentum', 'design system'],
        'related': ['self-help', 'computer-science'],
        'sites': ['qnfo.org', 'papers.qnfo.org', 'archive.qnfo.org',
                  'momentum.qnfo.org', 'design.qnfo.org', 'legal.qnfo.org',
                  'solo.qnfo.org'],
    },
}

# ── SITE TOPIC MAPPING ──────────────────────────────────────────────
SITE_TOPICS = {
    'qnfo-hub': ['research-methodology', 'quantum-computing', 'p-adic-mathematics'],
    'qwav-marquee': ['quantum-computing', 'computer-science', 'p-adic-mathematics'],
    'qnfo-publications': ['research-methodology', 'quantum-computing', 'physics', 'mathematics'],
    'quantum-laws-of-form': ['mathematics', 'physics', 'philosophy', 'spirituality'],
    'solo-scientist': ['self-help', 'research-methodology'],
    'living-paper-standalone': ['computer-science', 'research-methodology'],
    'ultrametric-paradigm': ['p-adic-mathematics', 'physics', 'mathematics', 'cosmology'],
    'ultrametric-quantum': ['quantum-computing', 'physics', 'mathematics'],
    'hierarchical-universe': ['cosmology', 'physics', 'philosophy', 'spirituality'],
    'unity-of-ultrametric-physics': ['physics', 'mathematics', 'cosmology', 'spirituality'],
    'different-physics': ['physics', 'philosophy', 'mathematics'],
    'two-ways-of-measuring': ['mathematics', 'philosophy', 'physics'],
    'knowing-patterns': ['philosophy', 'self-help', 'cognition', 'spirituality'],
    'hensel-code': ['p-adic-mathematics', 'number-theory', 'computer-science'],
    'adelic-qft': ['p-adic-mathematics', 'number-theory', 'physics'],
    'cocyle': ['cognition', 'philosophy', 'spirituality'],
    'verb-lexicon': ['cognition', 'philosophy', 'self-help'],
    'ultrametric-ai-poc': ['computer-science', 'cognition', 'quantum-computing'],
    'qwav': ['quantum-computing', 'research-methodology', 'p-adic-mathematics'],
    'qlof-primer': ['mathematics', 'physics', 'philosophy'],
    'ask-qwav': ['quantum-computing', 'computer-science', 'research-methodology'],
    'qnfo-archive': ['research-methodology'],
    'discovery-momentum': ['research-methodology'],
    'qnfo-design-system': ['research-methodology', 'computer-science'],
    'qnfo-legal': ['research-methodology'],
    'qnfo-ipfs-archive': ['research-methodology', 'computer-science'],
    'uqc-benchmark': ['quantum-computing', 'computer-science'],
    'toward-p-adic-qec': ['quantum-computing', 'p-adic-mathematics', 'physics'],
    'ultrametric-benchmark': ['quantum-computing', 'computer-science'],
    'p-adic-hardware-co-design': ['quantum-computing', 'p-adic-mathematics', 'computer-science'],
    'adelic-qec-synthesis': ['quantum-computing', 'p-adic-mathematics', 'mathematics'],
}

# ── SITE REGISTRY (from Phase 1) ────────────────────────────────────
SITES = {
    'qnfo-hub': {
        'project': 'qnfo-hub',
        'primary': 'https://qnfo.org',
        'title': 'QNFO — Research Infrastructure',
        'description': 'QNFO is the research infrastructure behind QWAV — ultrametric quantum computing, quantum laws of form, p-adic physics, and the unified research library.',
    },
    'qwav-marquee': {
        'project': 'qwav-marquee',
        'primary': 'https://qwav.tech',
        'title': 'QWAV — Ultrametric Quantum Computing',
        'description': 'QWAV: computational evidence for ultrametric quantum computing. Zero logical errors at depth 7. 48× error reduction through passive fault tolerance.',
    },
    'qnfo-publications': {
        'project': 'qnfo-publications',
        'primary': 'https://papers.qnfo.org',
        'title': 'QNFO Publications — Unified Research Library',
        'description': 'QNFO research publications — unified library of papers on ultrametric physics, quantum laws of form, p-adic quantum error correction, and related topics.',
    },
    'quantum-laws-of-form': {
        'project': 'quantum-laws-of-form',
        'primary': 'https://laws.qnfo.org',
        'title': 'Quantum Laws of Form — A Syntactic Foundation for Physics',
        'description': 'From The Calculus of Distinction to Ultrametric Cosmology. A radical re-foundation of physics based on Spencer-Brown\'s Laws of Form.',
    },
    'solo-scientist': {
        'project': 'solo-scientist',
        'primary': 'https://solo.qnfo.org',
        'title': 'The Force-Multiplier Playbook — Solo Scientist',
        'description': 'A practical guide for independent researchers: how to amplify research output using AI tools, automated infrastructure, and systematic workflows.',
    },
    'living-paper-standalone': {
        'project': 'living-paper-standalone',
        'primary': 'https://living-paper.qnfo.org',
        'title': 'Living Paper — Interactive arXiv Reader',
        'description': 'Interactive reader for arXiv papers with live equation rendering, citation tracking, and cross-referencing.',
    },
    'ultrametric-paradigm': {
        'project': 'ultrametric-paradigm',
        'primary': 'https://paradigm.qnfo.org',
        'title': 'The Ultrametric Paradigm',
        'description': 'A comprehensive introduction to the ultrametric paradigm in physics: non-Archimedean geometry, p-adic numbers, and their implications for quantum theory and cosmology.',
    },
    'ultrametric-quantum': {
        'project': 'ultrametric-quantum',
        'primary': 'https://quantum.qnfo.org',
        'title': 'QNFO Quantum — Ultrametric Quantum Computing Research Portal',
        'description': 'Research portal for ultrametric quantum computing: p-adic quantum error correction, adelic synthesis, and experimental protocols.',
    },
    'hierarchical-universe': {
        'project': 'hierarchical-universe',
        'primary': 'https://hierarchy.qnfo.org',
        'title': 'The Hierarchical Universe',
        'description': 'Exploring the hierarchical structure of physical law: from Planck scale to cosmological scale through the lens of ultrametric geometry.',
    },
    'unity-of-ultrametric-physics': {
        'project': 'unity-of-ultrametric-physics',
        'primary': 'https://unity.qnfo.org',
        'title': 'Unity of Ultrametric Physics',
        'description': 'A unified framework connecting ultrametric geometry across quantum mechanics, quantum field theory, and cosmology.',
    },
    'different-physics': {
        'project': 'different-physics',
        'primary': 'https://different.qnfo.org',
        'title': 'The Road Not Taken: Ultrametric Quantum Mechanics',
        'description': 'What if quantum mechanics had been built on ultrametric rather than Archimedean foundations?',
    },
    'two-ways-of-measuring': {
        'project': 'two-ways-of-measuring',
        'primary': 'https://measure.qnfo.org',
        'title': 'Two Ways of Measuring',
        'description': 'A philosophical and mathematical exploration of measurement in Archimedean vs. ultrametric frameworks.',
    },
    'knowing-patterns': {
        'project': 'knowing-patterns',
        'primary': 'https://knowing.qnfo.org',
        'title': 'Knowing Patterns — An Epistemology for People Tired of Being Fixed',
        'description': 'A pattern-based epistemology: understanding knowledge as pattern recognition across scales, from quantum measurement to social cognition.',
    },
    'hensel-code': {
        'project': 'hensel-code',
        'primary': 'https://hensel.qnfo.org',
        'title': 'Hensel Code System — Exact Rational Arithmetic',
        'description': 'Hensel codes: an exact rational arithmetic system based on p-adic number theory.',
    },
    'adelic-qft': {
        'project': 'adelic-qft',
        'primary': 'https://adelic.qnfo.org',
        'title': 'Adelic Constraints on Quantum Field Theory',
        'description': 'Applying adelic analysis to constrain quantum field theories.',
    },
    'cocyle': {
        'project': 'cocyle',
        'primary': 'https://cocyle.qnfo.org',
        'title': 'The Branch and the Shadow — Cocyle Ultrametric Cognition',
        'description': 'Cocyle: an ultrametric model of cognition based on branching decision trees and shadow representations.',
    },
    'verb-lexicon': {
        'project': 'verb-lexicon',
        'primary': 'https://lexicon.qnfo.org',
        'title': 'The Verb Lexicon — Describing the Patterns We Mistake for People',
        'description': 'A lexicon of patterns observed in human behavior, reframed as verbs rather than nouns.',
    },
    'ultrametric-ai-poc': {
        'project': 'ultrametric-ai-poc',
        'primary': 'https://ai-poc.qnfo.org',
        'title': 'Ultrametric AI — Proof of Concept',
        'description': 'Proof of concept for ultrametric AI architectures: leveraging p-adic distance metrics for more robust machine learning.',
    },
    'qwav': {
        'project': 'qwav',
        'primary': 'https://deep.qwav.tech',
        'title': 'QWAV Deep — Research Feed',
        'description': 'QWAV Deep research feed: the latest papers, experimental results, and theoretical developments in ultrametric quantum computing.',
    },
    'qlof-primer': {
        'project': 'qlof-primer',
        'primary': 'https://primer.qwav.tech',
        'title': 'QLoF Primer — Quantum Laws of Form Introduction',
        'description': 'A gentle introduction to Quantum Laws of Form. No advanced mathematics required.',
    },
    'ask-qwav': {
        'project': 'ask-qwav',
        'primary': 'https://ask.qwav.tech',
        'title': 'Ask QWAV — Research Oracle',
        'description': 'Ask questions about ultrametric geometry, p-adic physics, quantum computing, and the QWAV research corpus.',
    },
    'qnfo-archive': {
        'project': 'qnfo-archive',
        'primary': 'https://archive.qnfo.org',
        'title': 'QNFO Archive',
        'description': 'Permanent archive of QNFO research publications, datasets, and computational artifacts.',
    },
    'discovery-momentum': {
        'project': 'discovery-momentum',
        'primary': 'https://momentum.qnfo.org',
        'title': 'Discovery Momentum — QNFO',
        'description': 'Tracking research discovery momentum across the QNFO ecosystem.',
    },
    'qnfo-design-system': {
        'project': 'qnfo-design-system',
        'primary': 'https://design.qnfo.org',
        'title': 'QNFO Design System',
        'description': 'QNFO Unified Navigation design system for all *.qnfo.org and *.qwav.tech sites.',
    },
    'qnfo-legal': {
        'project': 'qnfo-legal',
        'primary': 'https://legal.qnfo.org',
        'title': 'QNFO Unified License Agreement v2.0',
        'description': 'QNFO Unified License Agreement (QNFO-ULA) Version 2.0.',
    },
    'qnfo-ipfs-archive': {
        'project': 'qnfo-ipfs-archive',
        'primary': 'https://qnfo-ipfs-archive.pages.dev',
        'title': 'QNFO/QWAV Distributed Permanent Archive',
        'description': 'Distributed permanent archive for QNFO/QWAV research: IPFS-backed storage.',
    },
    'uqc-benchmark': {
        'project': 'uqc-benchmark',
        'primary': 'https://uqc-benchmark.pages.dev',
        'title': 'UQC Benchmark',
        'description': 'Ultrametric Quantum Computation benchmark for evaluating quantum hardware.',
    },
    'toward-p-adic-qec': {
        'project': 'toward-p-adic-qec',
        'primary': 'https://toward-p-adic-qec.pages.dev',
        'title': 'Toward p-adic Quantum Error Correction',
        'description': 'The metric mismatch hypothesis: current QEC uses Archimedean geometry, but quantum errors may follow ultrametric structure.',
    },
    'ultrametric-benchmark': {
        'project': 'ultrametric-benchmark',
        'primary': 'https://ultrametric-benchmark.pages.dev',
        'title': 'Testing for Ultrametric Error Structure',
        'description': 'Experimental protocol for detecting ultrametric error structure in quantum hardware.',
    },
    'p-adic-hardware-co-design': {
        'project': 'p-adic-hardware-co-design',
        'primary': 'https://p-adic-hardware-co-design.pages.dev',
        'title': 'p-adic Quantum Hardware Co-Design',
        'description': 'Designing quantum hardware layouts optimized for p-adic (ultrametric) error correction.',
    },
    'adelic-qec-synthesis': {
        'project': 'adelic-qec-synthesis',
        'primary': 'https://adelic-qec-synthesis.pages.dev',
        'title': 'Adelic Quantum Error Correction Synthesis',
        'description': 'A unified adelic framework for quantum error correction synthesizing p-adic codes across all primes.',
    },
}

# ── UTILITY FUNCTIONS ───────────────────────────────────────────────

def fetch_url(url, timeout=15):
    """Fetch a URL and return (status, content_type, body)"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; QNFO-SEO-Bot/2.0)'
        })
        r = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        ct = r.headers.get('Content-Type', 'unknown')
        body = r.read().decode('utf-8', errors='ignore')
        return r.status, ct, body
    except Exception as e:
        return None, None, str(e)


# ── LLMS.TXT GENERATION ─────────────────────────────────────────────

def generate_llms_txt(site_key):
    """Generate llms.txt — AI crawler content manifest following llmstxt.org standard.
    
    This tells AI crawlers (ChatGPT, Claude, Perplexity, Google AI) which pages
    contain important content and what context to extract.
    """
    site = SITES[site_key]
    primary = site['primary']
    title = site['title']
    desc = site['description']
    
    topics = SITE_TOPICS.get(site_key, [])
    topic_labels = [TOPIC_TAXONOMY[t]['label'] for t in topics if t in TOPIC_TAXONOMY]
    
    # Find related sites that share topics
    related_sites = set()
    for topic in topics:
        for rel_site in TOPIC_TAXONOMY.get(topic, {}).get('sites', []):
            # Map domain back to site key
            for sk, s in SITES.items():
                if s['primary'].replace('https://', '').replace('http://', '') == rel_site:
                    if sk != site_key:
                        related_sites.add(sk)
    
    # Find AI-query-relevant cross-discipline bridges
    bridge_topics = []
    all_related = set()
    for topic in topics:
        for rel_topic in TOPIC_TAXONOMY.get(topic, {}).get('related', []):
            if rel_topic not in topics:
                all_related.add(rel_topic)
    
    for rt in all_related:
        bridge_topics.append(f"{TOPIC_TAXONOMY[rt]['label']}")
    
    lines = []
    lines.append(f'# {title}')
    lines.append(f'')
    lines.append(f'> {desc}')
    lines.append(f'')
    
    if topic_labels:
        lines.append(f'**Topics:** {", ".join(topic_labels)}')
    if bridge_topics:
        lines.append(f'**Also relevant to:** {", ".join(bridge_topics[:5])}')
    lines.append(f'')
    lines.append(f'## Primary Content')
    lines.append(f'')
    lines.append(f'- [{title}]({primary}/): {desc}')
    lines.append(f'')
    
    # Add cross-discipline discovery section
    if bridge_topics:
        lines.append(f'## Cross-Discipline Connections')
        lines.append(f'')
        lines.append(f'This research connects to these broader domains:')
        for bt in bridge_topics[:5]:
            # Find a site that represents this bridge topic
            for sk, st in SITE_TOPICS.items():
                if sk != site_key:
                    for t in topics:
                        if t in TOPIC_TAXONOMY and bt in [TOPIC_TAXONOMY[x]['label'] for x in TOPIC_TAXONOMY[t].get('related', [])]:
                            if sk in SITES:
                                lines.append(f'- [{bt}]({SITES[sk]["primary"]}/): {SITES[sk]["description"][:120]}')
                                break
        lines.append(f'')
    
    if related_sites:
        lines.append(f'## Related Research')
        lines.append(f'')
        for rsk in list(related_sites)[:8]:
            if rsk in SITES:
                lines.append(f'- [{SITES[rsk]["title"]}]({SITES[rsk]["primary"]}/): {SITES[rsk]["description"][:120]}')
        lines.append(f'')
    
    # AI crawler hints
    lines.append(f'## For AI Crawlers')
    lines.append(f'')
    lines.append(f'- **Content type:** Research publication')
    lines.append(f'- **Audience:** Researchers, physicists, mathematicians, philosophers, independent thinkers')
    lines.append(f'- **Language:** English')
    lines.append(f'- **License:** CC BY-NC-SA 4.0 (see https://legal.qnfo.org)')
    lines.append(f'- **Canonical:** {primary}/')
    lines.append(f'- **Sitemap:** {primary}/sitemap.xml')
    lines.append(f'')
    lines.append(f'---')
    lines.append(f'*This llms.txt file follows the [llmstxt.org](https://llmstxt.org) standard for AI crawler content discovery.*')
    
    return '\n'.join(lines)


def generate_llms_full_txt(site_key):
    """Generate llms-full.txt — full content extract for AI ingestion.
    
    This provides a structured extract of the page content optimized for
    AI crawler comprehension, including the key concepts, claims, and context.
    """
    site = SITES[site_key]
    primary = site['primary']
    title = site['title']
    desc = site['description']
    
    topics = SITE_TOPICS.get(site_key, [])
    topic_labels = [TOPIC_TAXONOMY[t]['label'] for t in topics if t in TOPIC_TAXONOMY]
    
    # Fetch the actual page content
    status, ct, body = fetch_url(primary)
    if status != 200:
        body = ''
    
    # Extract text content
    text_content = ''
    if body:
        # Remove scripts, styles, and HTML tags
        clean = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.I | re.S)
        clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.I | re.S)
        clean = re.sub(r'<[^>]+>', '\n', clean)
        clean = re.sub(r'\n\s*\n', '\n\n', clean)
        clean = re.sub(r'&amp;', '&', clean)
        clean = re.sub(r'&lt;', '<', clean)
        clean = re.sub(r'&gt;', '>', clean)
        clean = re.sub(r'&quot;', '"', clean)
        clean = re.sub(r'&#\d+;', '', clean)
        clean = clean.strip()
        text_content = clean[:10000]  # Limit to 10KB
    
    lines = []
    lines.append(f'# {title}')
    lines.append(f'')
    lines.append(f'## Metadata')
    lines.append(f'')
    lines.append(f'- **URL:** {primary}/')
    lines.append(f'- **Topics:** {", ".join(topic_labels)}')
    lines.append(f'- **Description:** {desc}')
    lines.append(f'- **Author:** Rowan Brad Quni-Gudzinas (QNFO Research)')
    lines.append(f'- **License:** CC BY-NC-SA 4.0')
    lines.append(f'')
    
    # Add taxonomy context
    lines.append(f'## Topic Taxonomy Context')
    lines.append(f'')
    for topic in topics:
        if topic in TOPIC_TAXONOMY:
            t = TOPIC_TAXONOMY[topic]
            lines.append(f'### {t["label"]}')
            lines.append(f'- Keywords: {", ".join(t["keywords"])}')
            lines.append(f'- Related to: {", ".join(TOPIC_TAXONOMY[r]["label"] for r in t.get("related", []) if r in TOPIC_TAXONOMY)}')
            lines.append(f'')
    
    # Add cross-discipline bridges
    lines.append(f'## Cross-Discipline Discovery Pathways')
    lines.append(f'')
    lines.append(f'This content is discoverable through queries related to:')
    lines.append(f'')
    for topic in topics:
        if topic in TOPIC_TAXONOMY:
            t = TOPIC_TAXONOMY[topic]
            lines.append(f'- **{t["label"]}:** {", ".join(t["keywords"][:5])}')
            for rel in t.get('related', [])[:3]:
                if rel in TOPIC_TAXONOMY:
                    lines.append(f'  - Bridges to {TOPIC_TAXONOMY[rel]["label"]}: {", ".join(TOPIC_TAXONOMY[rel]["keywords"][:3])}')
    lines.append(f'')
    
    if text_content:
        lines.append(f'## Content Extract')
        lines.append(f'')
        lines.append(text_content)
        lines.append(f'')
    
    lines.append(f'---')
    lines.append(f'*Generated for AI crawler ingestion. For the full interactive experience, visit {primary}/*')
    
    return '\n'.join(lines)


def generate_ai_txt(site_key):
    """Generate ai.txt — AI agent permissions and content manifest.
    
    Based on the emerging agents.txt / ai.txt standard for AI agent access control.
    """
    site = SITES[site_key]
    primary = site['primary']
    
    lines = []
    lines.append(f'# AI Agent Permissions for {primary}/')
    lines.append(f'')
    lines.append(f'# Allow all AI crawlers and agents')
    lines.append(f'User-Agent: *')
    lines.append(f'Allow: /')
    lines.append(f'')
    lines.append(f'# Specific AI agents')
    lines.append(f'User-Agent: GPTBot')
    lines.append(f'Allow: /')
    lines.append(f'Disallow: /admin')
    lines.append(f'')
    lines.append(f'User-Agent: Claude-Web')
    lines.append(f'Allow: /')
    lines.append(f'')
    lines.append(f'User-Agent: anthropic-ai')
    lines.append(f'Allow: /')
    lines.append(f'')
    lines.append(f'User-Agent: PerplexityBot')
    lines.append(f'Allow: /')
    lines.append(f'')
    lines.append(f'User-Agent: Google-Extended')
    lines.append(f'Allow: /')
    lines.append(f'')
    lines.append(f'User-Agent: CCBot')
    lines.append(f'Allow: /')
    lines.append(f'')
    lines.append(f'# Content manifests for AI ingestion')
    lines.append(f'LLMs-TXT: {primary}/llms.txt')
    lines.append(f'LLMs-Full-TXT: {primary}/llms-full.txt')
    lines.append(f'Sitemap: {primary}/sitemap.xml')
    lines.append(f'')
    lines.append(f'# Content license: CC BY-NC-SA 4.0')
    lines.append(f'# Full license: https://legal.qnfo.org')
    
    return '\n'.join(lines)


# ── ENHANCED STRUCTURED DATA ────────────────────────────────────────

def generate_enhanced_jsonld(site_key):
    """Generate enhanced JSON-LD with topic taxonomy, cross-references, and sameAs links."""
    site = SITES[site_key]
    primary = site['primary']
    title = site['title']
    desc = site['description']
    topics = SITE_TOPICS.get(site_key, [])
    today = datetime.date.today().isoformat()
    
    # Build topic tags
    about_list = []
    for topic in topics:
        if topic in TOPIC_TAXONOMY:
            t = TOPIC_TAXONOMY[topic]
            about_list.append({
                '@type': 'Thing',
                'name': t['label'],
                'description': f'Content related to {t["label"].lower()}: {", ".join(t["keywords"][:5])}',
                'sameAs': f'https://qnfo.org/topics/{topic}',
            })
    
    # Build sameAs cross-references
    same_as = ['https://qnfo.org']
    for topic in topics:
        if topic in TOPIC_TAXONOMY:
            for rel_site in TOPIC_TAXONOMY[topic].get('sites', []):
                rel_url = 'https://' + rel_site if not rel_site.startswith('http') else rel_site
                if rel_url != primary + '/' and rel_url not in same_as:
                    same_as.append(rel_url)
    same_as = same_as[:10]  # Limit
    
    # Enhanced WebSite / Article schema
    ld = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebSite',
                '@id': primary + '/#website',
                'name': title,
                'description': desc,
                'url': primary + '/',
                'author': {
                    '@type': 'Person',
                    '@id': 'https://qnfo.org/#person',
                    'name': 'Rowan Brad Quni-Gudzinas',
                },
                'publisher': {
                    '@type': 'Organization',
                    '@id': 'https://qnfo.org/#organization',
                    'name': 'QNFO Research',
                    'url': 'https://qnfo.org',
                },
                'about': about_list[:5],
                'inLanguage': 'en',
                'license': 'https://legal.qnfo.org',
                'isAccessibleForFree': True,
                'potentialAction': {
                    '@type': 'SearchAction',
                    'target': {
                        '@type': 'EntryPoint',
                        'urlTemplate': 'https://qnfo.org/search?q={search_term_string}',
                    },
                    'query-input': 'required name=search_term_string',
                },
            },
            {
                '@type': 'WebPage',
                '@id': primary + '/#webpage',
                'url': primary + '/',
                'name': title,
                'description': desc,
                'isPartOf': {'@id': primary + '/#website'},
                'about': about_list[:5],
                'datePublished': today,
                'dateModified': today,
                'inLanguage': 'en',
                'mainEntity': {
                    '@type': 'Article',
                    '@id': primary + '/#article',
                    'headline': title,
                    'description': desc,
                    'author': {'@id': 'https://qnfo.org/#person'},
                    'publisher': {'@id': 'https://qnfo.org/#organization'},
                    'about': about_list[:5],
                    'datePublished': today,
                    'dateModified': today,
                    'inLanguage': 'en',
                    'isAccessibleForFree': True,
                    'license': 'https://legal.qnfo.org',
                },
            },
        ],
    }
    
    # Add sameAs if available
    if len(same_as) > 1:
        ld['@graph'][0]['sameAs'] = same_as
    
    return ld


def generate_enhanced_seo_tags(site_key):
    """Generate enhanced SEO meta tags including AI crawler hints."""
    site = SITES[site_key]
    primary = site['primary']
    title = site['title']
    desc = site['description']
    topics = SITE_TOPICS.get(site_key, [])
    
    topic_keywords = []
    for topic in topics:
        if topic in TOPIC_TAXONOMY:
            topic_keywords.extend(TOPIC_TAXONOMY[topic]['keywords'][:5])
    keywords = ', '.join(topic_keywords[:15])
    
    tags = []
    tags.append(f'<title>{title}</title>')
    tags.append(f'<meta name="description" content="{desc}">')
    tags.append(f'<meta name="keywords" content="{keywords}">')
    tags.append(f'<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">')
    
    # Open Graph
    tags.append(f'<meta property="og:title" content="{title}">')
    tags.append(f'<meta property="og:description" content="{desc}">')
    tags.append(f'<meta property="og:url" content="{primary}/">')
    tags.append(f'<meta property="og:type" content="website">')
    tags.append(f'<meta property="og:site_name" content="QNFO Research">')
    tags.append(f'<meta property="og:locale" content="en_US">')
    
    # Twitter
    tag_attr_value_pattern = '<meta name="{}" content="{}">'
    tags.append(f'<meta name="twitter:card" content="summary_large_image">')
    tags.append(f'<meta name="twitter:title" content="{title}">')
    tags.append(f'<meta name="twitter:description" content="{desc}">')
    
    # Canonical
    tags.append(f'<link rel="canonical" href="{primary}/">')
    
    # AI crawler hints
    tags.append(f'<meta name="ai-content-type" content="research-publication">')
    tags.append(f'<meta name="ai-topics" content="{", ".join(topic_keywords[:10])}">')
    tags.append(f'<link rel="llms-txt" href="{primary}/llms.txt">')
    tags.append(f'<link rel="llms-full-txt" href="{primary}/llms-full.txt">')
    
    # Enhanced JSON-LD
    ld = generate_enhanced_jsonld(site_key)
    tags.append(f'<script type="application/ld+json">\n{json.dumps(ld, indent=2)}\n</script>')
    
    return '\n'.join(tags)


# ── TOPIC TAXONOMY MANIFEST ─────────────────────────────────────────

def generate_topic_taxonomy_manifest():
    """Generate a master topic taxonomy file for AI crawlers.
    
    This manifest helps AI crawlers understand the full conceptual map
    and discover connections between seemingly unrelated topics.
    """
    lines = []
    lines.append('# QNFO/QWAV Topic Taxonomy')
    lines.append('')
    lines.append('## Overview')
    lines.append('')
    lines.append('This taxonomy maps all QNFO/QWAV research across 12 interconnected domains.')
    lines.append('AI crawlers: use this manifest to discover content across disciplines.')
    lines.append('')
    
    # Topic map
    lines.append('## Topic Map')
    lines.append('')
    for topic_id, topic in TOPIC_TAXONOMY.items():
        lines.append(f'### {topic["label"]} (`{topic_id}`)')
        lines.append(f'- **Keywords:** {", ".join(topic["keywords"])}')
        
        # Related topics with labels
        rel_labels = [TOPIC_TAXONOMY[r]["label"] for r in topic.get('related', []) if r in TOPIC_TAXONOMY]
        lines.append(f'- **Bridges to:** {", ".join(rel_labels)}')
        
        # Sites in this topic
        site_list = []
        for s in topic.get('sites', []):
            for sk, si in SITES.items():
                if si['primary'].replace('https://', '').replace('http://', '') == s:
                    site_list.append(f'[{si["title"]}]({si["primary"]}/)')
                    break
        if site_list:
            lines.append(f'- **Content:** {"; ".join(site_list[:4])}')
        lines.append('')
    
    # Discovery pathways
    lines.append('## AI Discovery Pathways')
    lines.append('')
    lines.append('### How users find QNFO/QWAV through AI queries')
    lines.append('')
    
    pathways = [
        ('Quantum Computing', 'quantum-computing', 'p-adic-mathematics',
         'Someone asking about "quantum error correction breakthroughs" or "why quantum computing is hard" might discover p-adic QEC research'),
        ('Mathematics → Physics', 'mathematics', 'physics',
         'Someone exploring "alternative geometries in physics" or "non-Euclidean spacetime" might discover ultrametric physics'),
        ('Physics → Spirituality', 'physics', 'spirituality',
         'Someone asking about "physics and consciousness" or "scientific spirituality" might discover Laws of Form and hierarchical universe research'),
        ('Self-Help → Research', 'self-help', 'research-methodology',
         'Someone asking "how to be a productive independent researcher" might discover the Solo Scientist playbook'),
        ('Cognition → AI', 'cognition', 'computer-science',
         'Someone exploring "alternative AI architectures" or "mathematical models of thought" might discover ultrametric AI research'),
        ('Philosophy → Mathematics', 'philosophy', 'mathematics',
         'Someone asking about "foundations of mathematics" or "epistemology of measurement" might discover Laws of Form'),
        ('Spirituality → Physics', 'spirituality', 'cosmology',
         'Someone exploring "universe as a unified whole" or "hierarchical cosmology" might discover the hierarchical universe framework'),
    ]
    
    for label, from_t, to_t, desc in pathways:
        from_label = TOPIC_TAXONOMY[from_t]['label'] if from_t in TOPIC_TAXONOMY else from_t
        to_label = TOPIC_TAXONOMY[to_t]['label'] if to_t in TOPIC_TAXONOMY else to_t
        lines.append(f'- **{label} Pathway:** {from_label} → {to_label}')
        lines.append(f'  {desc}')
        lines.append('')
    
    lines.append('---')
    lines.append(f'*Topic Taxonomy v1.0 — Generated {datetime.date.today().isoformat()}*')
    lines.append(f'*Full content: https://qnfo.org*')
    
    return '\n'.join(lines)


# ── MASTER LLMS.TXT FOR QNFO HUB ────────────────────────────────────

def generate_master_llms_txt():
    """Generate a master llms.txt for qnfo.org that covers the entire ecosystem."""
    lines = []
    lines.append('# QNFO/QWAV Research Ecosystem')
    lines.append('')
    lines.append('> Complete AI-crawler content manifest for the QNFO/QWAV research ecosystem.')
    lines.append('> This file helps AI crawlers (ChatGPT, Claude, Perplexity, Google AI) discover')
    lines.append('> all research across ultrametric quantum computing, p-adic mathematics,')
    lines.append('> theoretical physics, philosophy, cognition, and self-help.')
    lines.append('')
    
    # By topic
    lines.append('## Content by Topic')
    lines.append('')
    
    for topic_id, topic in TOPIC_TAXONOMY.items():
        lines.append(f'### {topic["label"]}')
        lines.append(f'> Keywords: {", ".join(topic["keywords"][:6])}')
        for s in topic.get('sites', [])[:5]:
            for sk, si in SITES.items():
                if si['primary'].replace('https://', '').replace('http://', '') == s:
                    lines.append(f'- [{si["title"]}]({si["primary"]}/): {si["description"][:100]}')
                    break
        lines.append('')
    
    # By site
    lines.append('## All Sites')
    lines.append('')
    for site_key in sorted(SITES.keys()):
        site = SITES[site_key]
        topics = SITE_TOPICS.get(site_key, [])
        topic_labels = [TOPIC_TAXONOMY[t]['label'] for t in topics if t in TOPIC_TAXONOMY]
        lines.append(f'- [{site["title"]}]({site["primary"]}/): {site["description"][:120]}')
        if topic_labels:
            lines.append(f'  Topics: {", ".join(topic_labels)}')
        lines.append(f'  llms.txt: {site["primary"]}/llms.txt')
        lines.append(f'  llms-full.txt: {site["primary"]}/llms-full.txt')
        lines.append('')
    
    lines.append('## For AI Crawlers')
    lines.append('')
    lines.append('- **Ecosystem:** QNFO/QWAV Research')
    lines.append('- **Total sites:** 31')
    lines.append('- **Topics:** 12 interconnected domains')
    lines.append('- **License:** CC BY-NC-SA 4.0')
    lines.append('- **Contact:** https://qnfo.org')
    lines.append('- **Sitemap:** https://qnfo.org/sitemap.xml')
    lines.append('')
    lines.append('---')
    lines.append(f'*Master llms.txt for QNFO/QWAV — Generated {datetime.date.today().isoformat()}*')
    
    return '\n'.join(lines)


# ── BUILD & DEPLOY ──────────────────────────────────────────────────

def build_phase2_site(site_key):
    """Build Phase 2 artifacts for a single site."""
    site = SITES[site_key]
    project = site['project']
    primary = site['primary']
    
    build_dir = os.path.join(WORK_DIR, project)
    os.makedirs(build_dir, exist_ok=True)
    
    print(f'\n{"="*60}')
    print(f'Phase 2: {site_key} ({project})')
    print(f'  Primary: {primary}')
    
    # Generate llms.txt
    llms_content = generate_llms_txt(site_key)
    llms_path = os.path.join(build_dir, 'llms.txt')
    with open(llms_path, 'w', encoding='utf-8') as f:
        f.write(llms_content)
    print(f'  [OK] llms.txt ({len(llms_content)} bytes)')
    
    # Generate llms-full.txt
    llms_full_content = generate_llms_full_txt(site_key)
    llms_full_path = os.path.join(build_dir, 'llms-full.txt')
    with open(llms_full_path, 'w', encoding='utf-8') as f:
        f.write(llms_full_content)
    print(f'  [OK] llms-full.txt ({len(llms_full_content)} bytes)')
    
    # Generate ai.txt
    ai_content = generate_ai_txt(site_key)
    ai_path = os.path.join(build_dir, 'ai.txt')
    with open(ai_path, 'w', encoding='utf-8') as f:
        f.write(ai_content)
    print(f'  [OK] ai.txt ({len(ai_content)} bytes)')
    
    # Update _headers to include new file types
    headers_path = os.path.join(build_dir, '_headers')
    headers_content = f"""/robots.txt
  Content-Type: text/plain

/sitemap.xml
  Content-Type: application/xml

/llms.txt
  Content-Type: text/plain; charset=utf-8

/llms-full.txt
  Content-Type: text/plain; charset=utf-8

/ai.txt
  Content-Type: text/plain; charset=utf-8

/*
  X-Robots-Tag: index, follow
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
"""
    with open(headers_path, 'w', encoding='utf-8') as f:
        f.write(headers_content)
    print(f'  [OK] _headers updated')
    
    # Update index.html with enhanced SEO tags
    html_path = os.path.join(build_dir, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Remove old JSON-LD
        html_content = re.sub(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>', '', html_content, flags=re.I | re.S)
        
        # Remove old meta description, OG, twitter, canonical (they'll be re-added)
        html_content = re.sub(r'<meta[^>]+name=["\']description["\'][^>]*>', '', html_content, flags=re.I)
        html_content = re.sub(r'<meta[^>]+property=["\']og:[^"\']+["\'][^>]*>', '', html_content, flags=re.I)
        html_content = re.sub(r'<meta[^>]+name=["\']twitter:[^"\']+["\'][^>]*>', '', html_content, flags=re.I)
        html_content = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>', '', html_content, flags=re.I)
        html_content = re.sub(r'<meta[^>]+name=["\']keywords["\'][^>]*>', '', html_content, flags=re.I)
        html_content = re.sub(r'<meta[^>]+name=["\']ai-[^"\']+["\'][^>]*>', '', html_content, flags=re.I)
        html_content = re.sub(r'<link[^>]+rel=["\']llms-[^"\']+["\'][^>]*>', '', html_content, flags=re.I)
        
        # Inject enhanced tags
        enhanced_tags = generate_enhanced_seo_tags(site_key)
        head_match = re.search(r'<head[^>]*>', html_content, re.I)
        if head_match:
            insert_pos = head_match.end()
            html_content = html_content[:insert_pos] + '\n' + enhanced_tags + '\n' + html_content[insert_pos:]
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f'  [OK] index.html updated with enhanced SEO ({len(html_content)} bytes)')
    
    return build_dir


def build_topic_taxonomy():
    """Build the master topic taxonomy manifest at qnfo-hub."""
    taxonomy_content = generate_topic_taxonomy_manifest()
    build_dir = os.path.join(WORK_DIR, 'qnfo-hub')
    os.makedirs(build_dir, exist_ok=True)
    
    taxonomy_path = os.path.join(build_dir, 'topic-taxonomy.md')
    with open(taxonomy_path, 'w', encoding='utf-8') as f:
        f.write(taxonomy_content)
    print(f'\n  [OK] topic-taxonomy.md ({len(taxonomy_content)} bytes)')
    
    return taxonomy_content


def build_master_llms():
    """Build the master llms.txt for qnfo.org."""
    master_content = generate_master_llms_txt()
    build_dir = os.path.join(WORK_DIR, 'qnfo-hub')
    os.makedirs(build_dir, exist_ok=True)
    
    # Overwrite llms.txt with master version for the hub
    llms_path = os.path.join(build_dir, 'llms.txt')
    with open(llms_path, 'w', encoding='utf-8') as f:
        f.write(master_content)
    print(f'  [OK] Master llms.txt ({len(master_content)} bytes)')
    
    return master_content


def deploy_site(site_key):
    """Deploy a site to Cloudflare Pages."""
    site = SITES[site_key]
    project = site['project']
    build_dir = os.path.join(WORK_DIR, project)
    
    if not os.path.isdir(build_dir):
        print(f'  [SKIP] Build directory not found: {build_dir}')
        return False
    
    node_dir = r'C:\Users\LENOVO\AppData\Local\Programs\DeepChat\resources\app.asar.unpacked\runtime\node'
    npx_cmd = os.path.join(node_dir, 'npx.cmd')
    deploy_cmd = f'"{npx_cmd}" wrangler pages deploy "{build_dir}" --project-name {project} --branch main'
    env = os.environ.copy()
    env['PATH'] = node_dir + os.pathsep + env.get('PATH', '')
    
    try:
        result = subprocess.run(deploy_cmd, capture_output=True, text=True, timeout=120,
                                cwd=WORK_DIR, env=env, shell=True)
        if 'Success' in result.stdout or 'Deployment complete' in result.stdout:
            # Extract deployment URL
            for line in result.stdout.split('\n'):
                if 'pages.dev' in line:
                    print(f'  Deploy URL: {line.strip()}')
            print(f'  [OK] Deployed')
            return True
        else:
            print(f'  [ERROR] {result.stderr[-200:] if result.stderr else "unknown"}')
            return False
    except Exception as e:
        print(f'  [ERROR] {e}')
        return False


# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='QNFO SEO Phase 2 — AI Crawler Discoverability')
    parser.add_argument('--build', action='store_true', help='Build Phase 2 artifacts for all sites')
    parser.add_argument('--deploy', action='store_true', help='Deploy all sites after building')
    parser.add_argument('--site', type=str, help='Process only this site key')
    parser.add_argument('--master-only', action='store_true', help='Only generate master/taxonomy files')
    args = parser.parse_args()
    
    if args.master_only:
        print('Building master topic taxonomy and master llms.txt...')
        build_topic_taxonomy()
        build_master_llms()
        if args.deploy:
            deploy_site('qnfo-hub')
        sys.exit(0)
    
    if args.site:
        sites_to_process = {args.site: SITES[args.site]} if args.site in SITES else {}
        if not sites_to_process:
            print(f'Unknown site: {args.site}')
            sys.exit(1)
    else:
        sites_to_process = SITES
    
    print(f'QNFO SEO Phase 2 — AI Crawler Discoverability')
    print(f'Processing {len(sites_to_process)} sites')
    print()
    
    # Build topic taxonomy and master llms first
    build_topic_taxonomy()
    build_master_llms()
    
    success = 0
    fail = 0
    
    for site_key in sorted(sites_to_process.keys()):
        try:
            build_dir = build_phase2_site(site_key)
            if args.deploy:
                ok = deploy_site(site_key)
                if ok:
                    success += 1
                else:
                    fail += 1
            else:
                success += 1
        except Exception as e:
            print(f'  [FAIL] {site_key}: {e}')
            fail += 1
    
    print(f'\n{"="*60}')
    print(f'Phase 2 DONE: {success} succeeded, {fail} failed')
    print(f'Build artifacts: {WORK_DIR}')
