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
  const answers = parseAnswers(value.answers);
  if (!answers) return { ok: false, error: "Clarification answers must be a list of { id, question, answer }." };
  return { ok: true, value: answers.length ? { description, language: value.language, answers } : { description, language: value.language } };
}

/** Optional answers to earlier follow-up questions; blank answers are dropped. Returns null when malformed. */
function parseAnswers(value) {
  if (value === undefined || value === null) return [];
  if (!Array.isArray(value) || value.length > 20) return null;
  const answers = [];
  for (const item of value) {
    if (!item || typeof item !== "object" || typeof item.id !== "string" || !item.id.trim() || item.id.length > 80) return null;
    if (typeof item.answer !== "string" || (item.question !== undefined && typeof item.question !== "string")) return null;
    const answer = item.answer.trim().slice(0, 2000);
    if (answer) answers.push({ id: item.id.trim(), question: (item.question ?? "").trim().slice(0, 500), answer });
  }
  return answers;
}

export function toBackendTriageRequest(request) {
  const body = { message: request.description, language: BACKEND_LANGUAGES[request.language] };
  if (request.answers?.length) {
    body.answers = request.answers.map((item) => ({ question_id: item.id, question: item.question, answer: item.answer }));
  }
  return body;
}

function adaptPathways(value) {
  if (!Array.isArray(value)) return [];
  return value
    .filter((item) => item && typeof item === "object" && typeof item.title === "string" && item.title.trim() && typeof item.description === "string")
    .map((item) => ({ title: item.title, description: item.description, caution: typeof item.caution === "string" ? item.caution : "" }));
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
    pathways: adaptPathways(value.possible_pathways),
    sourceIds: value.source_ids_used,
    guardrail: value.disclaimer,
    notice: usedFallback
      ? "The triage service used its limited fallback. This is not a live AI assessment; verify important facts and sources with a qualified lawyer or relevant authority."
      : undefined
  };
}

export async function requestBackendTriage({ backendUrl, request, fetchImpl = fetch, timeoutMs = 45000 }) {
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
