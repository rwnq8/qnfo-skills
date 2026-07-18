#!/usr/bin/env node
// r2-upload.js — Upload a file to a Cloudflare R2 bucket via REST API
// Usage: node r2-upload.js <bucket> <key> <file-path>
// Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID env vars
// Alt: npx wrangler r2 object put {BUCKET}/{KEY} --file path --remote

const fs = require('fs');
const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID;

async function r2Upload(bucket, key, content) {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  if (!ACCOUNT) throw new Error('CLOUDFLARE_ACCOUNT_ID not set');
  const r = await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/r2/buckets/${bucket}/objects/${encodeURIComponent(key)}`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${T}` },
    body: content
  });
  return { status: r.status, ok: r.ok };
}

if (require.main === module) {
  const [bucket, key, filePath] = process.argv.slice(2);
  if (!bucket || !key || !filePath) {
    console.error('Usage: node r2-upload.js <bucket> <key> <file-path>');
    process.exit(1);
  }
  const content = fs.readFileSync(filePath);
  r2Upload(bucket, key, content).then(result => {
    console.log(result.ok ? `Uploaded ${key} to ${bucket}` : `Failed: HTTP ${result.status}`);
    if (!result.ok) process.exitCode = 1;
  }).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { r2Upload };
