#!/usr/bin/env node
// pinata-pin.js — Pin a file to IPFS via Pinata
// Usage: node pinata-pin.js <file-path> [name]
// Requires: PINATA_API_KEY, PINATA_API_SECRET env vars

const fs = require('fs');
const path = require('path');

const PKEY = process.env.PINATA_API_KEY;
const PSEC = process.env.PINATA_API_SECRET;

async function pinataPin(filePath, name) {
  if (!PKEY || !PSEC) throw new Error('PINATA_API_KEY / PINATA_API_SECRET not set');
  const content = fs.readFileSync(filePath);
  const fileName = name || path.basename(filePath);

  const form = new FormData();
  form.append('file', new Blob([content]), fileName);
  form.append('pinataMetadata', JSON.stringify({
    name: fileName,
    keyvalues: { type: 'publication', uploaded_at: new Date().toISOString() }
  }));
  form.append('pinataOptions', JSON.stringify({ cidVersion: 1, wrapWithDirectory: false }));

  const r = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
    method: 'POST',
    headers: { pinata_api_key: PKEY, pinata_secret_api_key: PSEC },
    body: form
  });
  const d = await r.json();
  if (d.IpfsHash) {
    console.log('IPFS CID:', d.IpfsHash);
    console.log('Gateway:', 'https://ipfs.io/ipfs/' + d.IpfsHash);
    console.log('Pinata Gateway:', 'https://gateway.pinata.cloud/ipfs/' + d.IpfsHash);
  } else {
    console.error('Pinata pin failed:', JSON.stringify(d));
    process.exitCode = 1;
  }
  return d.IpfsHash;
}

if (require.main === module) {
  const [filePath, name] = process.argv.slice(2);
  if (!filePath) {
    console.error('Usage: node pinata-pin.js <file-path> [name]');
    process.exit(1);
  }
  pinataPin(filePath, name).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { pinataPin };
