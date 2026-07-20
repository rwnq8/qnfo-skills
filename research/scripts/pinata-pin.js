#!/usr/bin/env node
// pinata-pin.js — DEPRECATED 2026-07-20. DO NOT USE.
//
// Pinata's free-tier quota was exceeded and the account is blocked.
// This script is retained on disk ONLY for historical reference (prior
// publications that were pinned via Pinata before the quota exceeded event).
//
// For all NEW IPFS pinning, use:
//   - scripts/filebase-pin.js   (PRIMARY — free 5GB, no request-volume limit)
//   - scripts/lighthouse-pin.js (SECONDARY — free Filecoin tier)
//
// See research/SKILL.md v2.7 "IPFS Pinning" section for the full
// Filebase-primary workflow and multi-pinner fallback order.

throw new Error(
  'pinata-pin.js is DEPRECATED (2026-07-20, free quota exceeded, account blocked). ' +
  'Use scripts/filebase-pin.js (primary) or scripts/lighthouse-pin.js (secondary) instead. ' +
  'Do not retry Pinata for any new publication.'
);

// --- Original implementation preserved below for historical reference only ---
// const fs = require('fs');
// const path = require('path');
// const PKEY = process.env.PINATA_API_KEY;
// const PSEC = process.env.PINATA_API_SECRET;
// async function pinataPin(filePath, name) {
//   if (!PKEY || !PSEC) throw new Error('PINATA_API_KEY / PINATA_API_SECRET not set');
//   const content = fs.readFileSync(filePath);
//   const fileName = name || path.basename(filePath);
//   const form = new FormData();
//   form.append('file', new Blob([content]), fileName);
//   form.append('pinataMetadata', JSON.stringify({
//     name: fileName,
//     keyvalues: { type: 'publication', uploaded_at: new Date().toISOString() }
//   }));
//   form.append('pinataOptions', JSON.stringify({ cidVersion: 1, wrapWithDirectory: false }));
//   const r = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
//     method: 'POST',
//     headers: { pinata_api_key: PKEY, pinata_secret_api_key: PSEC },
//     body: form
//   });
//   const d = await r.json();
//   return d.IpfsHash;
// }
// module.exports = { pinataPin };
