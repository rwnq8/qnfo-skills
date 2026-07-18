#!/usr/bin/env node
// r2-archive.js — Archive a generated document (docx/pptx/xlsx/pdf) to R2
// Usage: node r2-archive.js <bucket> <archive-path> <local-file-path>
// Requires: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID env vars

const fs = require('fs');
const path = require('path');
const T = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT = process.env.CLOUDFLARE_ACCOUNT_ID;

const CONTENT_TYPES = {
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  '.pdf': 'application/pdf',
  '.csv': 'text/csv'
};

async function archiveToR2(bucket, archivePath, localFilePath) {
  if (!T) throw new Error('CLOUDFLARE_API_TOKEN not set');
  if (!ACCOUNT) throw new Error('CLOUDFLARE_ACCOUNT_ID not set');
  const content = fs.readFileSync(localFilePath);
  const ext = path.extname(localFilePath).toLowerCase();
  const contentType = CONTENT_TYPES[ext] || 'application/octet-stream';

  const r = await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT}/r2/buckets/${bucket}/objects/${encodeURIComponent(archivePath)}`, {
    method: 'PUT',
    headers: { Authorization: `Bearer ${T}`, 'Content-Type': contentType },
    body: content
  });
  if (r.ok) {
    console.log(`Archived ${localFilePath} -> r2://${bucket}/${archivePath} (${contentType})`);
  } else {
    console.error(`Archive FAILED: HTTP ${r.status}`);
    process.exitCode = 1;
  }
  return r.ok;
}

if (require.main === module) {
  const [bucket, archivePath, localFilePath] = process.argv.slice(2);
  if (!bucket || !archivePath || !localFilePath) {
    console.error('Usage: node r2-archive.js <bucket> <archive-path> <local-file-path>');
    process.exit(1);
  }
  archiveToR2(bucket, archivePath, localFilePath).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { archiveToR2 };
