#!/usr/bin/env node
// filebase-pin.js — Pin a file to IPFS via Filebase (S3-compatible, auto-pins on PUT)
// PRIMARY IPFS pinner as of 2026-07-20 (replaces Pinata, whose free quota was exceeded).
// Free tier: 5GB storage, no request-volume rate limit.
// Usage: node filebase-pin.js <file-path> <bucket> [key]
// Requires: FILEBASE_ACCESS_KEY, FILEBASE_SECRET_KEY env vars (or ~/.filebase_access_key, ~/.filebase_secret_key)

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const AK = process.env.FILEBASE_ACCESS_KEY;
const SK = process.env.FILEBASE_SECRET_KEY;
const HOST = 's3.filebase.com';

function hmac(key, data) {
  return crypto.createHmac('sha256', key).update(data).digest();
}

function contentTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.md': 'text/markdown',
    '.pdf': 'application/pdf',
    '.zip': 'application/zip',
    '.json': 'application/json',
    '.txt': 'text/plain',
    '.html': 'text/html',
  };
  return map[ext] || 'application/octet-stream';
}

async function s3Put(bucket, key, body, contentType) {
  const payloadHash = crypto.createHash('sha256').update(body).digest('hex');
  const amzDate = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
  const dateStamp = amzDate.substring(0, 8);
  const objPath = '/' + bucket + '/' + key;

  const canonicalReq = [
    'PUT', objPath, '',
    'content-type:' + contentType,
    'host:' + HOST,
    'x-amz-content-sha256:' + payloadHash,
    'x-amz-date:' + amzDate + '\n',
    'content-type;host;x-amz-content-sha256;x-amz-date',
    payloadHash
  ].join('\n');

  const credentialScope = dateStamp + '/us-east-1/s3/aws4_request';
  const stringToSign = [
    'AWS4-HMAC-SHA256', amzDate, credentialScope,
    crypto.createHash('sha256').update(canonicalReq).digest('hex')
  ].join('\n');

  const kDate = hmac('AWS4' + SK, dateStamp);
  const kRegion = hmac(kDate, 'us-east-1');
  const kService = hmac(kRegion, 's3');
  const kSigning = hmac(kService, 'aws4_request');
  const signature = hmac(kSigning, stringToSign).toString('hex');

  const auth = 'AWS4-HMAC-SHA256 Credential=' + AK + '/' + credentialScope +
    ',SignedHeaders=content-type;host;x-amz-content-sha256;x-amz-date,Signature=' + signature;

  const r = await fetch('https://' + HOST + objPath, {
    method: 'PUT',
    headers: {
      Authorization: auth,
      'Content-Type': contentType,
      Host: HOST,
      'x-amz-content-sha256': payloadHash,
      'x-amz-date': amzDate
    },
    body
  });

  return { status: r.status, ok: r.ok, ipfsCid: r.headers.get('x-ipfs-cid') };
}

async function filebasePin(filePath, bucket, key) {
  if (!AK || !SK) throw new Error('FILEBASE_ACCESS_KEY / FILEBASE_SECRET_KEY not set');
  const content = fs.readFileSync(filePath);
  const objectKey = key || path.basename(filePath);
  const contentType = contentTypeFor(filePath);

  const result = await s3Put(bucket, objectKey, content, contentType);

  if (result.ok && result.ipfsCid) {
    console.log('Filebase upload: HTTP', result.status);
    console.log('IPFS CID:', result.ipfsCid);
    console.log('Gateway (ipfs.io):', 'https://ipfs.io/ipfs/' + result.ipfsCid);
    console.log('Gateway (cloudflare):', 'https://cloudflare-ipfs.com/ipfs/' + result.ipfsCid);
    console.log('Gateway (dweb.link):', 'https://dweb.link/ipfs/' + result.ipfsCid);
  } else if (result.ok) {
    console.warn('Filebase upload OK (HTTP ' + result.status + ') but no x-ipfs-cid header returned yet.');
    console.warn('Filebase pins asynchronously — check the object headers again in a few seconds via a HEAD request,');
    console.warn('or use `wrangler`/S3 HEAD on s3.filebase.com/' + bucket + '/' + objectKey);
  } else {
    console.error('Filebase upload FAILED: HTTP', result.status);
    console.error('Falling back: try scripts/lighthouse-pin.js next. Do NOT retry Pinata (quota exceeded, blocked).');
    process.exitCode = 1;
  }
  return result.ipfsCid;
}

if (require.main === module) {
  const [filePath, bucket, key] = process.argv.slice(2);
  if (!filePath || !bucket) {
    console.error('Usage: node filebase-pin.js <file-path> <bucket> [key]');
    process.exit(1);
  }
  filebasePin(filePath, bucket, key).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { filebasePin, s3Put };
