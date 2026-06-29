/**
 * QNFO CMS Client v3.0 — Unified Design System + Central Theme + Full Stack
 * - Dark + Light theme with QNFO Design System
 * - Full article rendering for CMS content
 * - Living Papers section on every page
 * - Unified API gateway integration
 * - Cross-service stats display
 */
(function(){
  'use strict';

  var UNIFIED_API = 'https://api-gateway.q08.workers.dev';
  var CMS_API = 'https://cms-api.q08.workers.dev/api';
  var LP_API = 'https://living-papers-api.q08.workers.dev/api';
  var QNFO = window.QNFO = window.QNFO || {};
  var QDS = {};
﻿
  // === v3.0: Central Theme Architecture ===
  var CENTRAL_THEME_URL = '/theme.json';
  var EMBEDDED_THEME = {
    version: '1.0',
    base: {
      dark: {'--qds-bg':'#0a0a0f','--qds-surface':'#13131a','--qds-surface-raised':'#1a1a24','--qds-border':'#252532','--qds-text':'#e4e4ed','--qds-text-secondary':'#8b8b9e','--qds-text-muted':'#8888a0','--qds-accent':'#818cf8','--qds-accent-hover':'#a5b4fc','--qds-accent-dim':'rgba(129,140,248,0.10)'},
      light: {'--qds-bg':'#fafbfc','--qds-surface':'#ffffff','--qds-surface-raised':'#f4f5f7','--qds-border':'#e1e4e8','--qds-text':'#1a1a2e','--qds-text-secondary':'#4a4a6a','--qds-text-muted':'#6b6b82','--qds-accent':'#4f46e5','--qds-accent-hover':'#4338ca','--qds-accent-dim':'rgba(79,70,229,0.08)'}
    },
    overrides: {}
  };

  function applyThemeVars(themeObj) {
    var root = document.documentElement;
    var scheme = 'dark';
    if (themeObj && themeObj.default_mode === 'light') scheme = 'light';
    else if (!themeObj || !themeObj.default_mode) {
      scheme = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    }
    var vars = themeObj.base[scheme] || themeObj.base.dark;
    // Apply base vars
    for (var k in vars) { root.style.setProperty(k, vars[k]); }
    // Apply site overrides
    var host = window.location.hostname;
    var overrides = themeObj.overrides[host];
    if (overrides) { for (var k in overrides) { root.style.setProperty(k, overrides[k]); } }
  }

  function fetchCentralTheme() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', CENTRAL_THEME_URL, true);
    xhr.timeout = 5000;
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          var theme = JSON.parse(xhr.responseText);
          if (theme && theme.base) {
            applyThemeVars(theme);
            if (window.console) console.log('%c\u2B22 QDS Central Theme v' + (theme.version || '?') + '%c — loaded from hub',
              'color:#818cf8;font-weight:bold', 'color:#8888a0');
            return;
          }
        } catch(e) {}
      }
      if (window.console) console.log('%c\u2B22 QDS%c — using baked-in theme (central fetch failed)',
        'color:#818cf8', 'color:#8888a0');
    };
    xhr.onerror = function() {};
    xhr.ontimeout = function() {};
    xhr.send();
  }

 // QNFO Design System

  var DOMAIN_MAP = {
    'laws.qnfo.org': 'quantum-laws-of-form',
    'archive.qnfo.org': 'qnfo-archive',
    'papers.qnfo.org': 'qnfo-publications',
    'hub.qnfo.org': 'qnfo-hub',
    'qnfo.org': 'hub',
    'deep.qwav.tech': 'qwav',
    'adelic-qec.qnfo.org': 'adelic-qft',
    'adelic-qft.qnfo.org': 'adelic-qft',
    'benchmark.qnfo.org': 'benchmark',
    'knowing.qnfo.org': 'knowing',
    'solo.qnfo.org': 'solo',
    'unity.qnfo.org': 'unity-of-ultrametric-physics',
    'quantum.qnfo.org': 'ultrametric-quantum',
    'paradigm.qnfo.org': 'ultrametric-paradigm',
    'living-papers.qnfo.org': 'living-papers',
  };

  function detectProperty() {
    var host = window.location.hostname;
    if (DOMAIN_MAP[host]) return DOMAIN_MAP[host];
    return host.split('.')[0];
  }

  function esc(text) { var d = document.createElement('div'); d.textContent = text || ''; return d.innerHTML; }

  function md2html(md) {
    if (!md) return '';
    var h = md;
    h = h.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="qds-code-block"><code>$2</code></pre>');
    h = h.replace(/`([^`]+)`/g, '<code class="qds-inline-code">$1</code>');
    h = h.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    h = h.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    h = h.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="qds-link" target="_blank">$1</a>');
    h = h.replace(/^#### (.+)$/gm, '<h4 class="qds-h4">$1</h4>');
    h = h.replace(/^### (.+)$/gm, '<h3 class="qds-h3">$1</h3>');
    h = h.replace(/^## (.+)$/gm, '<h2 class="qds-h2">$1</h2>');
    h = h.replace(/^# (.+)$/gm, '<h1 class="qds-h1">$1</h1>');
    h = h.replace(/^- (.+)$/gm, '<li class="qds-li">$1</li>');
    h = h.replace(/(<li class="qds-li">[\s\S]*?<\/li>)/g, '<ul class="qds-ul">$1</ul>');
    h = h.replace(/\n\n+/g, '</p><p class="qds-p">');
    return '<p class="qds-p">' + h + '</p>';
  }

  // Inject the QNFO Design System CSS
  function injectCSS() {
    if (document.getElementById('qds-styles')) return;
    var style = document.createElement('style');
    style.id = 'qds-styles';
    style.textContent = '' +
    ':root{' +
    '--qds-bg:#0a0a0f;--qds-surface:#13131a;--qds-surface-raised:#1a1a24;--qds-border:#252532;' +
    '--qds-text:#e4e4ed;--qds-text-secondary:#8b8b9e;--qds-text-muted:#8888a0;' +
    '--qds-accent:#818cf8;--qds-accent-hover:#a5b4fc;--qds-accent-dim:rgba(129,140,248,0.10);' +
    '--qds-green:#22c55e;--qds-green-dim:rgba(34,197,94,0.12);' +
    '--qds-amber:#f59e0b;--qds-amber-dim:rgba(245,158,11,0.12);' +
    '--qds-red:#ef4444;--qds-red-dim:rgba(239,68,68,0.12);' +
    '--qds-purple:#a855f7;--qds-purple-dim:rgba(168,85,247,0.12);' +
    '--qds-radius-sm:6px;--qds-radius:8px;--qds-radius-lg:12px;' +
    '--qds-shadow:0 4px 32px rgba(0,0,0,0.4);--qds-shadow-sm:0 2px 12px rgba(0,0,0,0.3);' +
    '--qds-font:"Charter","Georgia",-apple-system,Palatino,serif;' +
    '--qds-font-mono:"JetBrains Mono","Fira Code","SF Mono",monospace;' +
    '--qds-transition:0.15s ease' +
    '}' +
    '@media(prefers-color-scheme:light){:root{--qds-bg:#fafbfc;--qds-surface:#fff;--qds-surface-raised:#f4f5f7;--qds-border:#e1e4e8;--qds-text:#1a1a2e;--qds-text-secondary:#4a4a6a;--qds-text-muted:#6b6b82;--qds-accent:#4f46e5;--qds-accent-hover:#4338ca;--qds-accent-dim:rgba(79,70,229,0.08);--qds-green:#059669;--qds-green-dim:rgba(5,150,105,0.08);--qds-amber:#d97706;--qds-amber-dim:rgba(217,119,6,0.08);--qds-red:#dc2626;--qds-red-dim:rgba(220,38,38,0.08);--qds-purple:#7c3aed;--qds-purple-dim:rgba(124,58,237,0.08);--qds-shadow:0 4px 32px rgba(0,0,0,0.08);--qds-shadow-sm:0 2px 12px rgba(0,0,0,0.06)}}' +
    '*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}' +
    'html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}' +
    'body{font-family:var(--qds-font);background:var(--qds-bg);color:var(--qds-text);line-height:1.7;min-height:100vh}' +
    '.qds-container{max-width:960px;margin:0 auto;padding:0 1.5rem}' +
    '.qds-header{padding:2rem 0 1.5rem;border-bottom:1px solid var(--qds-border)}' +
    '.qds-header-inner{display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:1rem}' +
    '.qds-title{font-size:1.75rem;font-weight:700;letter-spacing:-0.02em;color:var(--qds-text)}' +
    '.qds-subtitle{font-size:0.9rem;color:var(--qds-text-secondary)}' +
    '.qds-badge{display:inline-flex;align-items:center;gap:0.35rem;padding:0.2rem 0.6rem;border-radius:var(--qds-radius-sm);font-size:0.75rem;font-weight:500;white-space:nowrap}' +
    '.qds-badge-page{background:var(--qds-accent-dim);color:var(--qds-accent)}' +
    '.qds-badge-pub{background:var(--qds-purple-dim);color:var(--qds-purple)}' +
    '.qds-badge-doi{background:var(--qds-amber-dim);color:var(--qds-amber);font-family:var(--qds-font-mono)}' +
    '.qds-badge-ok{background:var(--qds-green-dim);color:var(--qds-green)}' +
    '.qds-nav{display:flex;gap:0.25rem;flex-wrap:wrap;margin:1rem 0 0}' +
    '.qds-nav a{color:var(--qds-text-secondary);text-decoration:none;font-size:0.85rem;padding:0.35rem 0.65rem;border-radius:var(--qds-radius-sm);transition:all var(--qds-transition)}' +
    '.qds-nav a:hover,.qds-nav a.active{color:var(--qds-accent);background:var(--qds-accent-dim)}' +
    '.qds-main{padding-top:2rem;padding-bottom:3rem}' +
    '.qds-article{max-width:780px}' +
    '.qds-article-title{font-size:2.25rem;font-weight:800;letter-spacing:-0.03em;line-height:1.2;margin-bottom:0.75rem}' +
    '.qds-article-meta{display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:2.5rem;padding-bottom:1.5rem;border-bottom:1px solid var(--qds-border)}' +
    '.qds-article-body{font-size:1.05rem;line-height:1.8;color:var(--qds-text)}' +
    '.qds-article-body .qds-p{margin-bottom:1.2rem}'+
    '.qds-article-body .qds-h1{font-size:1.6rem;font-weight:700;margin:2.5rem 0 1rem;color:var(--qds-text)}'+
    '.qds-article-body .qds-h2{font-size:1.3rem;font-weight:600;margin:2rem 0 0.8rem;color:var(--qds-accent)}'+
    '.qds-article-body .qds-h3{font-size:1.1rem;font-weight:600;margin:1.5rem 0 0.5rem}'+
    '.qds-article-body .qds-h4{font-size:1rem;font-weight:600;margin:1.2rem 0 0.4rem;color:var(--qds-text-secondary)}'+
    '.qds-article-body .qds-ul{margin:0 0 1rem 1.5rem}'+
    '.qds-article-body .qds-li{margin-bottom:0.4rem}'+
    '.qds-article-body .qds-inline-code{background:var(--qds-surface-raised);padding:0.1rem 0.35rem;border-radius:3px;font-size:0.9em;font-family:var(--qds-font-mono);color:var(--qds-amber)}'+
    '.qds-article-body .qds-code-block{background:var(--qds-surface-raised);padding:1.2rem;border-radius:var(--qds-radius);overflow-x:auto;margin-bottom:1.2rem;border:1px solid var(--qds-border)}'+
    '.qds-article-body .qds-code-block code{font-family:var(--qds-font-mono);font-size:0.9rem;color:var(--qds-text)}'+
    '.qds-article-body .qds-link{color:var(--qds-accent);text-decoration:underline;text-underline-offset:2px}'+
    '.qds-article-body .qds-link:hover{color:var(--qds-accent-hover)}'+
    '.qds-article-body strong{color:var(--qds-text);font-weight:600}'+
    '.qds-article-body em{color:var(--qds-text-secondary)}'+
    '.qds-section-title{font-size:1.3rem;font-weight:700;color:var(--qds-accent);margin-bottom:0.3rem}'+
    '.qds-section-meta{font-size:0.85rem;color:var(--qds-text-muted);margin-bottom:1.2rem}'+
    '.qds-paper-grid{display:grid;gap:0.75rem}'+
    '.qds-paper-card{background:var(--qds-surface);border:1px solid var(--qds-border);border-radius:var(--qds-radius);padding:1.2rem 1.5rem;transition:all var(--qds-transition)}'+
    '.qds-paper-card:hover{border-color:var(--qds-accent);box-shadow:var(--qds-shadow-sm);transform:translateY(-1px)}'+
    '.qds-paper-title{font-size:1.05rem;font-weight:600;color:var(--qds-text);margin-bottom:0.3rem}'+
    '.qds-paper-meta{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:0.5rem;font-size:0.82rem;color:var(--qds-text-secondary)}'+
    '.qds-paper-meta span{display:inline-flex;align-items:center;gap:0.25rem}'+
    '.qds-paper-abstract{font-size:0.88rem;color:var(--qds-text-secondary);line-height:1.6;margin-bottom:0.5rem}'+
    '.qds-paper-links{display:flex;gap:0.75rem;flex-wrap:wrap;margin-top:0.5rem;font-size:0.82rem}'+
    '.qds-paper-links a{color:var(--qds-accent);text-decoration:none;transition:color var(--qds-transition)}'+
    '.qds-paper-links a:hover{color:var(--qds-accent-hover)}'+
    '.qds-cid{font-family:var(--qds-font-mono);font-size:0.78rem;color:var(--qds-text-muted)}'+
    '.qds-divider{height:1px;background:var(--qds-border);margin:2.5rem 0}'+
    '.qds-footer{border-top:1px solid var(--qds-border);padding:1.5rem 0 2rem;color:var(--qds-text-muted);font-size:0.8rem;text-align:center}'+
    '.qds-footer-links{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin-bottom:0.75rem}'+
    '.qds-footer-links a{color:var(--qds-text-secondary);text-decoration:none;transition:color var(--qds-transition)}'+
    '.qds-footer-links a:hover{color:var(--qds-accent)}'+
    '.qds-status{display:inline-flex;align-items:center;gap:0.35rem;padding:0.2rem 0.6rem;border-radius:var(--qds-radius-sm);font-size:0.78rem}'+
    '.qds-status-loading{background:var(--qds-accent-dim);color:var(--qds-accent)}'+
    '.qds-status-ok{background:var(--qds-green-dim);color:var(--qds-green)}'+
    '.qds-status-err{background:var(--qds-red-dim);color:var(--qds-red)}'+
    '.qds-empty,.qds-error{text-align:center;padding:3rem 1.5rem;border:1px dashed var(--qds-border);border-radius:var(--qds-radius-lg)}'+
    '.qds-empty h3,.qds-error h3{font-size:1.1rem;margin-bottom:0.5rem;color:var(--qds-text)}'+
    '.qds-empty p,.qds-error p{color:var(--qds-text-secondary);font-size:0.9rem}'+
    '.qds-error{border-color:var(--qds-red);background:var(--qds-red-dim)}'+
    '.qds-card{background:var(--qds-surface);border:1px solid var(--qds-border);border-radius:var(--qds-radius);padding:1.5rem;transition:all var(--qds-transition)}'+
    '.qds-card:hover{border-color:var(--qds-accent);box-shadow:var(--qds-shadow-sm)}'+
    '.qds-card-title{font-size:1.15rem;font-weight:600;margin-bottom:0.5rem}'+
    '.qds-card-meta{margin-bottom:0.75rem;display:flex;gap:0.5rem;flex-wrap:wrap}'+
    '.qds-card-body{color:var(--qds-text-secondary);font-size:0.92rem}'+
    '@media(max-width:640px){.qds-title{font-size:1.4rem}.qds-article-title{font-size:1.6rem}.qds-paper-grid{grid-template-columns:1fr}}';
    document.head.appendChild(style);
  }

  QNFO.cms = {
    fetch: function(path) { return fetch(CMS_API + path).then(function(r){ return r.json(); }); },
    getContent: function(type) {
      var p = '/content';
      if (type) p += '?type=' + encodeURIComponent(type);
      return this.fetch(p);
    },
    getPropertyContent: function(prop) {
      var s = this;
      return this.getContent().then(function(r) {
        if (!r || !r.success) return r;
        r.data = (r.data || []).filter(function(e) { return e.pages_project === prop; });
        r.count = r.data.length;
        return r;
      });
    },
    renderArticle: function(container, entry) {
      var body = entry.body_html || (entry.body_md ? md2html(entry.body_md) : '');
      var h = '<article class="qds-article">';
      h += '<h1 class="qds-article-title">' + esc(entry.title || 'Untitled') + '</h1>';
      h += '<div class="qds-article-meta">';
      if (entry.content_type) h += '<span class="qds-badge qds-badge-page">' + entry.content_type + '</span>';
      if (entry.doi) h += '<span class="qds-badge qds-badge-doi">' + esc(entry.doi) + '</span>';
      h += '</div><div class="qds-article-body">' + body + '</div></article>';
      container.innerHTML = h;
      document.title = (entry.title || 'QNFO') + ' \u2014 QNFO';
      var h1 = document.querySelector('.qds-title');
      if (h1 && entry.title) h1.textContent = entry.title;
    },
    renderCards: function(container, entries, opts) {
      opts = opts || {};
      var show = entries.slice(0, opts.limit || entries.length);
      container.innerHTML = '';
      if (!show.length) { container.innerHTML = '<div class="qds-empty"><h3>No content yet</h3><p>Check back soon.</p></div>'; return; }
      if (show.length === 1) { this.renderArticle(container, show[0]); return; }
      var html = '';
      show.forEach(function(e) {
        var body = e.body_html || (e.body_md ? md2html(e.body_md) : '');
        var preview = body.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim().substring(0, 280);
        html += '<div class="qds-card"><h3 class="qds-card-title">'+esc(e.title||'Untitled')+'</h3>';
        html += '<div class="qds-card-body">'+preview+'...</div></div>';
      });
      container.innerHTML = html;
    },
    autoRender: function() {
      var self = this, prop = detectProperty();
      var st = document.getElementById('qds-status');
      if (st) { st.textContent = 'Loading...'; st.className = 'qds-status qds-status-loading'; }
      var els = document.querySelectorAll('[data-cms-content]');
      if (!els.length) {
        var m = document.querySelector('.qds-main') || document.querySelector('main') || document.body;
        m.setAttribute('data-cms-content', prop);
        els = [m];
      }
      els.forEach(function(el) {
        el.setAttribute('data-cms-content', prop);
        self.getPropertyContent(prop).then(function(r) {
          if (!r || !r.success || !r.data || !r.data.length) {
            self.getContent().then(function(all) {
              if (all && all.success && all.data && all.data.length) { self.renderCards(el, all.data, {limit: 20}); if (st) { st.textContent = 'Ready'; st.className = 'qds-status qds-status-ok'; } }
              else el.innerHTML = '<div class="qds-error"><h3>Content Unavailable</h3><p>No entries for <strong>'+esc(prop)+'</strong>.</p></div>';
            });
            return;
          }
          self.renderCards(el, r.data, {limit: 20});
          if (st) { st.textContent = 'Ready'; st.className = 'qds-status qds-status-ok'; }
        }).catch(function(err) {
          el.innerHTML = '<div class="qds-error"><h3>Loading Failed</h3><p>'+esc(err.message)+'</p></div>';
          if (st) st.className = 'qds-status qds-status-err';
        });
      });
    }
  };

  QNFO.lp = {
    loadPapers: function(container, opts) {
      opts = opts || {};
      var q = opts.query || '';
      var lim = opts.limit || 12;
      var url = LP_API + '/papers?limit=' + lim + '&offset=' + (opts.offset || 0);
      container.innerHTML = '<p style="color:var(--qds-text-secondary);text-align:center;padding:2rem">Loading Living Papers...</p>';
      fetch(url).then(function(r){return r.json()}).then(function(r){
        if (!r || !r.success){ container.innerHTML='<div class="qds-error"><h3>LP Unavailable</h3></div>'; return; }
        var papers = r.data || [];
        var h = '';
        h += '<h2 class="qds-section-title">Living Papers</h2>';
        h += '<p class="qds-section-meta">' + (r.total||papers.length) + ' papers indexed. ' + lim + ' shown. All with IPFS content addressing.</p>';
        h += '<div class="qds-paper-grid">';
        papers.forEach(function(p){
          var title = p.title || 'Untitled';
          var authors = (typeof p.authors === 'string' ? p.authors : Array.isArray(p.authors) ? p.authors.join(', ') : '');
          var abs = (p.abstract || '').substring(0, 300);
          var doi = p.doi || '';
          var cid = p.ipfs_cid || '';
          var pub = p.published || '';
          h += '<div class="qds-paper-card">';
          h += '<h3 class="qds-paper-title">'+esc(title)+'</h3>';
          h += '<div class="qds-paper-meta">';
          if (authors) h += '<span>'+esc(authors.substring(0,80))+'</span>';
          if (pub) h += '<span>'+esc(pub)+'</span>';
          h += '</div>';
          if (abs) h += '<p class="qds-paper-abstract">'+esc(abs)+'...</p>';
          h += '<div class="qds-paper-links">';
          if (doi) h += '<a href="https://doi.org/'+doi+'" target="_blank">DOI: '+esc(doi)+'</a>';
          if (cid) h += '<span class="qds-cid">CID: '+esc(cid.substring(0,24))+'...</span>';
          h += '</div></div>';
        });
        h += '</div>';
        container.innerHTML = h;
      }).catch(function(e){
        container.innerHTML = '<div class="qds-error"><h3>Loading Failed</h3><p>'+esc(e.message)+'</p></div>';
      });
    },
    autoLoad: function() {
      var s = this;
      document.querySelectorAll('[data-lp-papers]').forEach(function(el){
        var lim = parseInt(el.getAttribute('data-lp-limit')||'12');
        var q = el.getAttribute('data-lp-search')||'';
        s.loadPapers(el, {limit:lim, query:q});
      });
    }
  };

  // Cross-service stats
  function loadStats() {
    fetch(UNIFIED_API + '/stats').then(function(r){return r.json()}).then(function(s){
      var c = document.getElementById('qds-footer-stats');
      if (c) c.textContent = s.papers?.total+' papers | '+s.knowledge_graph?.nodes+' nodes | '+s.cms?.total+' CMS entries';
    }).catch(function(){});
  }

  function init() {
    injectCSS();
    if (QNFO.cms) QNFO.cms.autoRender();
    if (QNFO.lp) QNFO.lp.autoLoad();
    loadStats();
    fetchCentralTheme();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
