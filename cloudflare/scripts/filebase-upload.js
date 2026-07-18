#!/usr/bin/env node
// filebase-upload.js — Upload to Filebase (S3-compatible) with auto IPFS pinning
// Usage: node filebase-upload.js <bucket> <key> <file-path> [content-type]
// Requires: FILEBASE_ACCESS_KEY, FILEBASE_SECRET_KEY env vars

const crypto = require('crypto');
const fs = require('fs');

const AK = process.env.FILEBASE_ACCESS_KEY;
const SK = process.env.FILEBASE_SECRET_KEY;
const HOST = 's3.filebase.com';

function hmac(key, data) { return crypto.createHmac('sha256', key).update(data).digest(); }

async function s3Put(bucket, key, body, contentType) {
  if (!AK || !SK) throw new Error('FILEBASE_ACCESS_KEY / FILEBASE_SECRET_KEY not set');
  const payloadHash = crypto.createHash('sha256').update(body).digest('hex');
  const amzDate = new Date().toISOString().replace(/[:-]|\.\d{3}/g, '');
  const dateStamp = amzDate.substring(0, 8);
  const path = '/' + bucket + '/' + key;

  const canonicalReq = [
    'PUT', path, '',
    'content-type:' + (contentType || 'text/plain'),
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

  const r = await fetch('https://' + HOST + path, {
    method: 'PUT',
    headers: {
      Authorization: auth, 'Content-Type': contentType || 'text/plain',
      Host: HOST, 'x-amz-content-sha256': payloadHash, 'x-amz-date': amzDate
    },
    body
  });
  return { status: r.status, ok: r.ok, ipfsCid: r.headers.get('x-ipfs-cid') };
}

if (require.main === module) {
  const [bucket, key, filePath, contentType] = process.argv.slice(2);
  if (!bucket || !key || !filePath) {
    console.error('Usage: node filebase-upload.js <bucket> <key> <file-path> [content-type]');
    process.exit(1);
  }
  const body = fs.readFileSync(filePath);
  s3Put(bucket, key, body, contentType).then(result => {
    console.log('Upload result:', JSON.stringify(result));
    if (result.ipfsCid) console.log('IPFS CID:', result.ipfsCid, '-> https://ipfs.io/ipfs/' + result.ipfsCid);
  }).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { s3Put };
