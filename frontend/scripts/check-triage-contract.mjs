import assert from "node:assert/strict";
import test from "node:test";
import {
  adaptBackendTriageResponse,
  parseClientTriageRequest,
  requestBackendTriage,
  toBackendTriageRequest
} from "../lib/triage-contract.mjs";

const backendPayload = {
  category: "Property / Inheritance",
  summary: "More facts are needed before identifying a reliable legal pathway.",
  urgency: "unknown",
  facts: ["A relative occupies inherited property."],
  issues: [{ issue: "property/possession/inheritance", explanation: "Potential property issue.", confidence: 0.55 }],
  missing_facts: ["Relevant dates"],
  follow_up_questions: [{ id: "property_owner", question: "Who is shown as the owner?", reason: "Ownership records matter.", priority: "high" }],
  possible_pathways: [],
  warnings: [],
  source_ids_used: ["PK-009"],
  disclaimer: "This is not legal advice.",
  mode: "live"
};

test("maps the public request onto the FastAPI endpoint and language contract", async () => {
  const parsed = parseClientTriageRequest({ description: "My uncle occupies inherited property and sent a notice.", language: "roman-ur" });
  assert.equal(parsed.ok, true);
  assert.deepEqual(toBackendTriageRequest(parsed.value), {
    message: "My uncle occupies inherited property and sent a notice.",
    language: "roman_urdu"
  });
  let call;
  const result = await requestBackendTriage({
    backendUrl: "https://triage.example/",
    request: parsed.value,
    fetchImpl: async (url, options) => {
      call = { url, options };
      return new Response(JSON.stringify(backendPayload), { status: 200, headers: { "content-type": "application/json" } });
    }
  });
  assert.equal(call.url, "https://triage.example/api/v1/triage");
  assert.deepEqual(JSON.parse(call.options.body), {
    message: "My uncle occupies inherited property and sent a notice.",
    language: "roman_urdu"
  });
  assert.equal(result.ok, true);
  assert.deepEqual(result.result.followUpQuestions, [{ id: "property_owner", prompt: "Who is shown as the owner?", type: "text" }]);
});

test("forwards clarification answers and drops blank ones", () => {
  const parsed = parseClientTriageRequest({
    description: "Someone robbed my laptop and now it is gone.",
    language: "en",
    answers: [
      { id: "location", question: "In which city?", answer: " islamabad " },
      { id: "fir_status", question: "Has an FIR been registered?", answer: "   " }
    ]
  });
  assert.equal(parsed.ok, true);
  assert.deepEqual(toBackendTriageRequest(parsed.value), {
    message: "Someone robbed my laptop and now it is gone.",
    language: "english",
    answers: [{ question_id: "location", question: "In which city?", answer: "islamabad" }]
  });
  assert.equal(parseClientTriageRequest({ description: "Someone robbed my laptop and now it is gone.", language: "en", answers: "islamabad" }).ok, false);
  assert.equal(parseClientTriageRequest({ description: "Someone robbed my laptop and now it is gone.", language: "en", answers: [{ answer: "x" }] }).ok, false);
});

test("adapts practical pathways from the backend", () => {
  const result = adaptBackendTriageResponse({
    ...backendPayload,
    possible_pathways: [{ title: "Report it to the police", description: "Ask for an FIR.", prerequisites: [], caution: "Keep a copy." }, { title: "" }]
  });
  assert.deepEqual(result.pathways, [{ title: "Report it to the police", description: "Ask for an FIR.", caution: "Keep a copy." }]);
});

test("adapts backend fields without inventing document recommendations", () => {
  const result = adaptBackendTriageResponse(backendPayload);
  assert.deepEqual(result.legalIssues, ["property/possession/inheritance"]);
  assert.deepEqual(result.missingInformation, ["Relevant dates"]);
  assert.deepEqual(result.suggestedDocuments, []);
  assert.deepEqual(result.sourceIds, ["PK-009"]);
  assert.equal(result.mode, "backend");
});

test("labels a deterministic backend fallback instead of presenting it as live", () => {
  const result = adaptBackendTriageResponse({ ...backendPayload, mode: "deterministic_fallback" });
  assert.equal(result.mode, "backend-fallback");
  assert.match(result.notice, /not a live AI assessment/i);
});

test("rejects invalid client requests and invalid backend responses", async () => {
  assert.equal(parseClientTriageRequest({ description: "This story is long enough but language is invalid.", language: "fr" }).ok, false);
  assert.equal(adaptBackendTriageResponse({ ...backendPayload, mode: "unexpected" }), null);
  const request = { description: "My uncle occupies inherited property and sent a notice.", language: "en" };
  const result = await requestBackendTriage({
    backendUrl: "https://triage.example",
    request,
    fetchImpl: async () => new Response("not json", { status: 200 })
  });
  assert.deepEqual(result, { ok: false, reason: "upstream_invalid_json" });
});

test("treats HTTP errors and network failures as observable backend failures", async () => {
  const request = { description: "My uncle occupies inherited property and sent a notice.", language: "en" };
  const httpResult = await requestBackendTriage({
    backendUrl: "https://triage.example",
    request,
    fetchImpl: async () => new Response("", { status: 503 })
  });
  assert.deepEqual(httpResult, { ok: false, reason: "upstream_http_error" });
  const networkResult = await requestBackendTriage({
    backendUrl: "https://triage.example",
    request,
    fetchImpl: async () => { throw new Error("unreachable"); }
  });
  assert.deepEqual(networkResult, { ok: false, reason: "upstream_unavailable" });
});
