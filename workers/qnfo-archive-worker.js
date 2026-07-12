--4ed6babaff1c947297caf23b4a6af3b0cdf14affcaf7361f9c7aff20716c
Content-Disposition: form-data; name="_archive_worker.js"

var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// _archive_worker.js
var archive_worker_default = {
  async queue(batch, env, ctx) {
    console.log(`[ARCHIVE] Processing batch of ${batch.messages.length} messages`);
    for (const message of batch.messages) {
      try {
        const job = message.body;
        await processArchivalJob(env, job);
        message.ack();
      } catch (err) {
        console.error(`[ARCHIVE] Error processing job: ${err.message}`);
        message.retry({ delaySeconds: 60 });
      }
    }
  },
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok", worker: "qnfo-archive-worker" }), {
        headers: { "Content-Type": "application/json" }
      });
    }
    if (url.pathname === "/archive" && request.method === "POST") {
      const body = await request.json();
      await processArchivalJob(env, body);
      return new Response(JSON.stringify({ status: "archived", project: body.project }), {
        headers: { "Content-Type": "application/json" }
      });
    }
    return new Response("QNFO Archive Worker", { status: 200 });
  }
};
async function processArchivalJob(env, job) {
  const { project, sourcePath, targetPath } = job;
  console.log(`[ARCHIVE] Archiving ${project}: ${sourcePath} \u2192 ${targetPath}`);
  const objects = await listR2Objects(env, sourcePath);
  if (objects.length === 0) {
    console.log(`[ARCHIVE] No objects found at ${sourcePath} \u2014 project has no R2 files`);
  }
  let copied = 0;
  let failed = 0;
  for (const obj of objects) {
    try {
      const original = await env.QNFO_BUCKET.get(obj.key);
      if (!original) continue;
      const relativePath = obj.key.replace(sourcePath, "");
      const targetKey = `${targetPath}${relativePath}`.replace(/\/\//g, "/");
      await env.QNFO_BUCKET.put(targetKey, original.body, {
        httpMetadata: original.httpMetadata || {},
        customMetadata: {
          ...original.customMetadata || {},
          archived_at: (/* @__PURE__ */ new Date()).toISOString(),
          archived_from: obj.key
        }
      });
      await env.QNFO_BUCKET.delete(obj.key);
      copied++;
      console.log(`[ARCHIVE] Copied: ${obj.key} \u2192 ${targetKey}`);
    } catch (err) {
      console.error(`[ARCHIVE] Failed to copy ${obj.key}: ${err.message}`);
      failed++;
    }
  }
  console.log(`[ARCHIVE] Complete for ${project}: ${copied} copied, ${failed} failed, ${objects.length} total`);
  return { project, sourcePath, targetPath, copied, failed, total: objects.length };
}
__name(processArchivalJob, "processArchivalJob");
async function listR2Objects(env, prefix) {
  try {
    const result = await env.QNFO_BUCKET.list({ prefix });
    return result.objects || [];
  } catch (err) {
    console.error(`[ARCHIVE] Error listing R2 objects: ${err.message}`);
    return [];
  }
}
__name(listR2Objects, "listR2Objects");
export {
  archive_worker_default as default
};
//# sourceMappingURL=_archive_worker.js.map

--4ed6babaff1c947297caf23b4a6af3b0cdf14affcaf7361f9c7aff20716c--
