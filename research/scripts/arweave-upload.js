#!/usr/bin/env node
// arweave-upload.js — Permanent blockchain archival via Irys (Bundlr on Arweave)
// Usage: node arweave-upload.js <file-path>
// Requires: AR wallet configured for Irys node access (funded balance)
// One-time cost: ~$0.02 in AR tokens. Storage lasts 300+ years.

const fs = require('fs');

async function arweaveUpload(filePath) {
  const content = fs.readFileSync(filePath);
  const r = await fetch('https://node1.irys.xyz/tx/arweave', {
    method: 'POST',
    headers: { 'Content-Type': 'application/octet-stream' },
    body: content
  });
  const d = await r.json();
  if (d.id) {
    console.log('Arweave TX:', d.id);
    console.log('URL:', 'https://arweave.net/' + d.id);
  } else {
    console.error('Arweave upload failed:', JSON.stringify(d));
    process.exitCode = 1;
  }
  return d.id;
}

if (require.main === module) {
  const [filePath] = process.argv.slice(2);
  if (!filePath) {
    console.error('Usage: node arweave-upload.js <file-path>');
    process.exit(1);
  }
  arweaveUpload(filePath).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { arweaveUpload };
