// Frontend ↔ backend integration check against a RUNNING backend.
// Uses the same contract module the Next.js /api/triage route uses, and verifies the /v1/search
// fields the research UI renders.  Usage:
//   BACKEND_API_URL=http://127.0.0.1:8000 node scripts/check-backend-integration.mjs
//   (optional) NEXT_APP_URL=http://127.0.0.1:3000 to also exercise the Next.js API routes end-to-end.
import assert from "node:assert/strict";
import { requestBackendTriage } from "../lib/triage-contract.mjs";

const backend = (process.env.BACKEND_API_URL ?? "").replace(/\/$/, "");
const nextApp = (process.env.NEXT_APP_URL ?? "").replace(/\/$/, "");
if (!backend) {
  console.log("SKIP backend integration — set BACKEND_API_URL to a running backend.");
  process.exit(0);
}

const health = await fetch(`${backend}/health`).then((r) => r.json());
assert.equal(health.status, "ok", "backend /health");
console.log("PASS backend health");

// 1. Triage through the frontend contract adapter (same code path as app/api/triage/route.ts).
const cases = [
  { description: "Mere chacha ne hamari inherited property par qabza kar liya hai aur kaghzat nahi dikhate.", language: "roman-ur" },
  { description: "My landlord is trying to evict me from the house I rent without any written notice.", language: "en" },
  { description: "پولیس نے میرے بھائی کو بغیر وارنٹ کے گرفتار کر لیا ہے اور ایف آئی آر نہیں دکھائی۔", language: "ur" }
];
for (const request of cases) {
  const result = await requestBackendTriage({ backendUrl: backend, request, timeoutMs: 20000 });
  assert.ok(result.ok, `triage contract failed (${result.reason}) for ${request.language}`);
  const t = result.result;
  assert.ok(["backend", "backend-fallback"].includes(t.mode));
  assert.ok(t.category && t.summary && t.guardrail);
  assert.ok(Array.isArray(t.followUpQuestions) && t.followUpQuestions.every((q) => q.id && q.prompt && q.type === "text"));
  assert.ok(["low", "medium", "high", "critical", "unknown"].includes(t.urgency));
  console.log(`PASS triage contract [${request.language}] → ${t.category} / urgency=${t.urgency} / ${t.mode}`);
}

// 2. Search: legacy fields used by components/legal-research-demo.tsx + new provenance fields.
const search = await fetch(`${backend}/v1/search`, {
  method: "POST",
  headers: { "content-type": "application/json", "x-pjn-client": "citizen-web" },
  body: JSON.stringify({ query: "inherited property possession dispossessed", limit: 6 })
}).then((r) => r.json());
assert.equal(typeof search.mode, "string");
assert.ok(Array.isArray(search.results) && search.results.length > 0, "search returned no results");
for (const r of search.results) {
  for (const key of ["document_id", "title", "jurisdiction", "authority", "court", "bench", "evidence_level", "snippet",
                     "section_or_article", "citation", "source_url"]) {
    assert.ok(key in r, `search result missing ${key}`);
  }
  assert.ok(["chunk", "metadata"].includes(r.evidence_level));
  if (r.evidence_level === "chunk") {
    assert.ok(Number.isInteger(r.page_start) && r.provenance?.page_url?.includes("#page="), "chunk without page reference");
  }
}
console.log(`PASS search contract → mode=${search.mode}, top=${search.results[0].document_id} ${search.results[0].section_or_article} ${search.results[0].page_reference ?? ""}`);

// 3. Optional: through the real Next.js API routes.
if (nextApp) {
  const triage = await fetch(`${nextApp}/api/triage`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify(cases[0])
  });
  assert.equal(triage.status, 200, `Next /api/triage HTTP ${triage.status}`);
  const tBody = await triage.json();
  assert.ok(["backend", "backend-fallback"].includes(tBody.mode), `Next /api/triage did not use the backend (mode=${tBody.mode})`);
  console.log(`PASS Next.js /api/triage → backend (${tBody.mode}, ${tBody.category})`);

  const ls = await fetch(`${nextApp}/api/legal-search`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ query: "bail non-bailable offence", limit: 4 })
  });
  assert.equal(ls.status, 200);
  const lsBody = await ls.json();
  assert.ok(!["metadata-only", "metadata-fallback"].includes(lsBody.mode), `Next /api/legal-search fell back (mode=${lsBody.mode})`);
  assert.equal(lsBody.results[0].evidence_level, "chunk");
  console.log(`PASS Next.js /api/legal-search → backend (${lsBody.mode}, ${lsBody.results[0].section_or_article})`);
}

console.log("PASS frontend ↔ backend integration");
