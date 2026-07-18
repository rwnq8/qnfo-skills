#!/usr/bin/env node
// internet-archive-submit.js — Submit a URL to the Internet Archive Wayback Machine
// Usage: node internet-archive-submit.js <url>
// No auth required.

async function submitToInternetArchive(url) {
  const saveUrl = `https://web.archive.org/save/${url}`;
  const r = await fetch(saveUrl, { method: 'GET' });
  const contentLocation = r.headers.get('content-location');
  console.log(`Internet Archive snapshot request: HTTP ${r.status}`);
  if (contentLocation) {
    console.log('Archived at: https://web.archive.org' + contentLocation);
  } else {
    console.log('Verify manually: https://web.archive.org/web/*/' + url);
  }
  return { status: r.status, archivedPath: contentLocation };
}

if (require.main === module) {
  const [url] = process.argv.slice(2);
  if (!url) {
    console.error('Usage: node internet-archive-submit.js <url>');
    process.exit(1);
  }
  submitToInternetArchive(url).catch(e => { console.error('FATAL:', e.message); process.exitCode = 1; });
}

module.exports = { submitToInternetArchive };
