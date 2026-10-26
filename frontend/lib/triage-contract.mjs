const CLIENT_LANGUAGES = new Set(["en", "roman-ur", "ur"]);
const BACKEND_LANGUAGES = {
  en: "english",
  "roman-ur": "roman_urdu",
  ur: "urdu"
};
const BACKEND_URGENCIES = new Set(["low", "medium", "high", "critical", "unknown"]);
const BACKEND_MODES = new Set(["live", "deterministic_fallback"]);

export function parseClientTriageRequest(value) {
  if (!value || typeof value !== "object") return { ok: false, error: "Send a JSON object with a legal-problem description and language." };
  const description = typeof value.description === "string" ? value.description.trim() : "";
  if (description.length < 20 || description.length > 12000) {
    return { ok: false, error: "Provide between 20 and 12,000 characters describing the legal problem." };
  }
  if (!CLIENT_LANGUAGES.has(value.language)) {
    return { ok: false, error: "Choose English, Roman Urdu, or Urdu." };
  }
  return { ok: true, value: { description, language: value.language } };
}

export function toBackendTriageRequest(request) {
  return { message: request.description, language: BACKEND_LANGUAGES[request.language] };
}

function isStringArray(value) {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

function adaptQuestions(value) {
  if (!Array.isArray(value)) return null;
  const questions = [];
  for (const item of value) {
    if (!item || typeof item !== "object" || typeof item.id !== "string" || !item.id || typeof item.question !== "string" || !item.question.trim()) return null;
    // The backend does not assign input widgets; text is the neutral existing UI control.
    questions.push({ id: item.id, prompt: item.question, type: "text" });
  }
  return questions;
}

export function adaptBackendTriageResponse(value) {
  if (!value || typeof value !== "object") return null;
  if (typeof value.category !== "string" || !value.category.trim() || typeof value.summary !== "string" || !value.summary.trim()) return null;
  if (!BACKEND_URGENCIES.has(value.urgency) || !BACKEND_MODES.has(value.mode)) return null;
  if (!isStringArray(value.facts) || !isStringArray(value.missing_facts) || !isStringArray(value.source_ids_used) || typeof value.disclaimer !== "string" || !value.disclaimer.trim()) return null;
  if (!Array.isArray(value.issues)) return null;
  const legalIssues = [];
  for (const issue of value.issues) {
    if (!issue || typeof issue !== "object" || typeof issue.issue !== "string" || !issue.issue.trim()) return null;
    legalIssues.push(issue.issue);
  }
  const followUpQuestions = adaptQuestions(value.follow_up_questions);
  if (!followUpQuestions) return null;

  const usedFallback = value.mode === "deterministic_fallback";
  return {
    mode: usedFallback ? "backend-fallback" : "backend",
    category: value.category,
    summary: value.summary,
    urgency: value.urgency,
    facts: value.facts,
    legalIssues,
    missingInformation: value.missing_facts,
    // The backend does not return document recommendations, so do not infer them.
    suggestedDocuments: [],
    followUpQuestions,
    sourceIds: value.source_ids_used,
    guardrail: value.disclaimer,
    notice: usedFallback
      ? "The triage service used its limited fallback. This is not a live AI assessment; verify important facts and sources with a qualified lawyer or relevant authority."
      : undefined
  };
}

export async function requestBackendTriage({ backendUrl, request, fetchImpl = fetch, timeoutMs = 12000 }) {
  try {
    const response = await fetchImpl(`${backendUrl.replace(/\/$/, "")}/api/v1/triage`, {
      method: "POST",
      headers: { "content-type": "application/json", "x-pjn-client": "citizen-web" },
      body: JSON.stringify(toBackendTriageRequest(request)),
      cache: "no-store",
      signal: AbortSignal.timeout(timeoutMs)
    });
    if (!response.ok) return { ok: false, reason: "upstream_http_error" };
    let payload;
    try {
      payload = await response.json();
    } catch {
      return { ok: false, reason: "upstream_invalid_json" };
    }
    const result = adaptBackendTriageResponse(payload);
    return result ? { ok: true, result } : { ok: false, reason: "upstream_invalid_contract" };
  } catch {
    return { ok: false, reason: "upstream_unavailable" };
  }
}
