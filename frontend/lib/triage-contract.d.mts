import type { ClarificationAnswer, Language, TriageResult } from "./types";

export type ClientTriageRequest = { description: string; language: Language; answers?: ClarificationAnswer[] };
export type BackendTriageRequest = {
  message: string;
  language: "english" | "roman_urdu" | "urdu";
  answers?: { question_id: string; question: string; answer: string }[];
};

export function parseClientTriageRequest(value: unknown): { ok: true; value: ClientTriageRequest } | { ok: false; error: string };
export function toBackendTriageRequest(request: ClientTriageRequest): BackendTriageRequest;
export function adaptBackendTriageResponse(value: unknown): TriageResult | null;
export function requestBackendTriage(options: {
  backendUrl: string;
  request: ClientTriageRequest;
  fetchImpl?: typeof fetch;
  timeoutMs?: number;
}): Promise<{ ok: true; result: TriageResult } | { ok: false; reason: string }>;
