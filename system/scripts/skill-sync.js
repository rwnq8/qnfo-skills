#!/usr/bin/env node
// skill-sync.js — Sync all local skills (SKILL.md + scripts/*) to GitHub + R2
// Usage: node skill-sync.js [skills-root-dir]
// Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID env vars; git configured with push access

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID;
const BUCKET = 'qnfo-skills';

function walkFiles(dir, base) {
  base = base || dir;
  let out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out = out.concat(walkFiles(full, base));
    } else {
      out.push(path.relative(base, full).replace(/\\/g, '/'));
    }
  }
  return out;
}

async function r2Put(key, content, contentType) {
  const r = await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/r2/buckets/${BUCKET}/objects/${encodeURIComponent(key)}`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${T}`, 'Content-Type': contentType || 'application/octet-stream' },
    body: content
  });
  return r.ok;
}

async function syncSkills(skillsRoot) {
  if (!T || !ACCOUNT) throw new Error('CLOUDFLARE_API_TOKEN / CLOUDFLARE_ACCOUNT_ID not set');
  skillsRoot = skillsRoot || process.env.USERPROFILE + '\\.deepchat\\skills';

  // 1. Git commit + push (best-effort; ignore if no changes)
  try {
    execSync('git add -A && git commit -m "chore: skill sync" && git push', { cwd: skillsRoot, stdio: 'inherit' });
  } catch (e) {
    console.log('Git commit/push skipped (no changes or push failed):', e.message.split('\n')[0]);
  }

  // 2. R2 sync — every file under each skill directory that has a SKILL.md
  const skills = fs.readdirSync(skillsRoot, { withFileTypes: true })
    .filter(d => d.isDirectory() && fs.existsSync(path.join(skillsRoot, d.name, 'SKILL.md')))
    .map(d => d.name);

  let uploaded = 0;
  for (const skill of skills) {
    const skillDir = path.join(skillsRoot, skill);
    const files = walkFiles(skillDir);
    for (const rel of files) {
      const full = path.join(skillDir, rel);
      const content = fs.readFileSync(full);
      const key = `prompts/skills/${skill}/${rel}`;
      const ct = rel.endsWith('.md') ? 'text/markdown' : rel.endsWith('.js') ? 'application/javascript' : 'application/octet-stream';
      const ok = await r2Put(key, content, ct);
      if (ok) uploaded++;
      else console.error('FAILED to upload:', key);
    }
  }
  console.log(`Synced ${skills.length} skills, ${uploaded} files uploaded to R2 bucket "${BUCKET}".`);
  return { skillCount: skills.length, filesUploaded: uploaded };
}

if (require.main === module) {
  syncSkills(process.argv[2]).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { syncSkills };
