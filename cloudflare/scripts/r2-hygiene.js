#!/usr/bin/env node
// r2-hygiene.js — Detect double-prefix anti-pattern (e.g. qnfo/qnfo/... inside the qnfo bucket)
// Usage: node r2-hygiene.js <bucket> [prefix-to-check]
// Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID env vars

const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID;

async function checkR2Hygiene(bucket, badPrefix) {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  if (!ACCOUNT) throw new Error('CLOUDFLARE_ACCOUNT_ID not set');
  badPrefix = badPrefix || (bucket + '/');
  let cursor, all = [];
  do {
    const url = `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/r2/buckets/${bucket}/objects?prefix=${encodeURIComponent(badPrefix)}&per_page=1000` + (cursor ? `&cursor=${cursor}` : '');
    const r = await fetch(url, { headers: { Authorization: `Bearer ${T}` } });
    const d = await r.json();
    all = all.concat(d.result || []);
    cursor = d.result_info?.cursor;
  } while (cursor);

  const bad = all.filter(o => o.key.startsWith(badPrefix));
  if (bad.length > 0) {
    console.log(`FOUND ${bad.length} double-prefixed objects in bucket "${bucket}":`);
    bad.forEach(o => console.log('  FIX:', o.key));
    process.exitCode = 1;
  } else {
    console.log(`Clean — no "${badPrefix}" double-prefix objects found in bucket "${bucket}".`);
  }
  return bad;
}

if (require.main === module) {
  const [bucket, badPrefix] = process.argv.slice(2);
  if (!bucket) {
    console.error('Usage: node r2-hygiene.js <bucket> [prefix-to-check]');
    process.exit(1);
  }
  checkR2Hygiene(bucket, badPrefix).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { checkR2Hygiene };
