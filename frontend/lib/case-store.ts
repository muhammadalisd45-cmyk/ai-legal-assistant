"use client";

import type { CaseDraft, IntakeDraft } from "./types";
import { getSupabaseBrowserClient } from "./supabase/client";
import { supabaseConfig } from "./supabase/config";

const INTAKE_KEY = "pjn:intake:v2";
const CASES_KEY = "pjn:cases:v2";
function browser() { return typeof window !== "undefined"; }

// Uses the signed-in account's session (cookie-based, see lib/supabase). No anonymous sign-ups:
// if nobody is signed in, cases stay in this browser only. RLS limits rows to the owning user.
async function ensureSession(): Promise<{ accessToken: string; userId: string; url: string; key: string } | null> {
  if (!browser()) return null;
  let url: string, key: string;
  try { ({ url, key } = supabaseConfig()); } catch { return null; }
  const { data } = await getSupabaseBrowserClient().auth.getSession();
  const session = data.session;
  if (!session || session.user.is_anonymous) return null;
  return { accessToken: session.access_token, userId: session.user.id, url, key };
}

async function dataRequest(path: string, options: RequestInit = {}) {
  const auth = await ensureSession();
  if (!auth) return null;
  const response = await fetch(`${auth.url}/rest/v1/${path}`, {
    ...options,
    headers: {
      apikey: auth.key,
      Authorization: `Bearer ${auth.accessToken}`,
      ...(options.headers ?? {})
    }
  });
  if (!response.ok) throw new Error(`Supabase data request failed (${response.status})`);
  return response;
}

export function saveIntakeDraft(draft: IntakeDraft) {
  if (browser()) window.localStorage.setItem(INTAKE_KEY, JSON.stringify(draft));
}
export function loadIntakeDraft(): IntakeDraft | null {
  if (!browser()) return null;
  try {
    const parsed = JSON.parse(window.localStorage.getItem(INTAKE_KEY) ?? "null") as IntakeDraft | null;
    return parsed?.version === 2 ? parsed : null;
  } catch { return null; }
}
export function clearIntakeDraft() { if (browser()) window.localStorage.removeItem(INTAKE_KEY); }

function readLocalCases(): CaseDraft[] {
  if (!browser()) return [];
  try { return JSON.parse(window.localStorage.getItem(CASES_KEY) ?? "[]") as CaseDraft[]; } catch { return []; }
}
function writeLocalCases(cases: CaseDraft[]) { if (browser()) window.localStorage.setItem(CASES_KEY, JSON.stringify(cases.slice(0, 20))); }

export async function saveCase(draft: CaseDraft): Promise<"supabase" | "local"> {
  writeLocalCases([draft, ...readLocalCases().filter((item) => item.caseId !== draft.caseId)]);
  try {
    const auth = await ensureSession();
    if (!auth) return "local";
    await dataRequest("cases?on_conflict=public_case_id", {
      method: "POST",
      headers: { "content-type": "application/json", Prefer: "resolution=merge-duplicates,return=minimal" },
      body: JSON.stringify({
        user_id: auth.userId,
        public_case_id: draft.caseId,
        language: draft.language,
        category: draft.triage.category,
        summary: draft.triage.summary,
        urgency: draft.triage.urgency,
        status: "analysis",
        raw_description: draft.description,
        structured_payload: draft,
        updated_at: draft.updatedAt
      })
    });
    return "supabase";
  } catch { return "local"; }
}

export async function loadCase(caseId: string): Promise<CaseDraft | null> {
  const local = readLocalCases().find((item) => item.caseId === caseId);
  if (local) return local;
  try {
    const response = await dataRequest(`cases?public_case_id=eq.${encodeURIComponent(caseId)}&select=structured_payload&limit=1`);
    if (!response) return null;
    const rows = (await response.json()) as { structured_payload: CaseDraft }[];
    return rows[0]?.structured_payload ?? null;
  } catch { return null; }
}

export async function listCases(): Promise<CaseDraft[]> {
  const local = readLocalCases();
  try {
    const response = await dataRequest("cases?select=structured_payload&order=updated_at.desc&limit=20");
    if (!response) return local;
    const rows = (await response.json()) as { structured_payload: CaseDraft }[];
    const merged = new Map<string, CaseDraft>();
    [...rows.map((row) => row.structured_payload), ...local].filter(Boolean).forEach((item) => merged.set(item.caseId, item));
    return [...merged.values()].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
  } catch { return local; }
}
