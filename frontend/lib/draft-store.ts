"use client";

import { dataRequest } from "./case-store";

const KEY = "pjn:drafts:v1";

export type SavedDraft = {
  id: string;
  templateId: string;
  title: string;
  body: string;
  reviewed: boolean;
  updatedAt: string;
};

/** Where a save landed: the signed-in account (Supabase, RLS-scoped) or only this browser. */
export type DraftSaveTarget = "account" | "local";

type DraftRow = { draft_id: string; template_id: string; title: string; body: string; reviewed: boolean; updated_at: string };

function readLocal(): SavedDraft[] {
  if (typeof window === "undefined") return [];
  try {
    const parsed = JSON.parse(window.localStorage.getItem(KEY) ?? "[]");
    return Array.isArray(parsed) ? (parsed as SavedDraft[]) : [];
  } catch {
    return [];
  }
}

function writeLocal(drafts: SavedDraft[]) {
  try {
    window.localStorage.setItem(KEY, JSON.stringify(drafts));
  } catch {
    /* storage full or blocked — the account copy (if signed in) is still saved */
  }
}

function fromRow(row: DraftRow): SavedDraft {
  return { id: row.draft_id, templateId: row.template_id, title: row.title, body: row.body, reviewed: row.reviewed, updatedAt: row.updated_at };
}

function sortNewest(drafts: SavedDraft[]) {
  return drafts.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

/** Drafts cached in this browser (instant, works signed out). */
export function listDrafts(): SavedDraft[] {
  return readLocal();
}

/**
 * Drafts from the account merged with this browser's copies (newest version of each wins). Browser-only drafts made
 * before signing in are uploaded so they are not lost. Falls back to the browser copy when signed out or offline.
 */
export async function loadDrafts(): Promise<SavedDraft[]> {
  const local = readLocal();
  try {
    const response = await dataRequest("user_drafts?select=draft_id,template_id,title,body,reviewed,updated_at&order=updated_at.desc&limit=100");
    if (!response) return local;
    const remote = ((await response.json()) as DraftRow[]).map(fromRow);
    const merged = new Map(remote.map((draft) => [draft.id, draft]));
    const toUpload: SavedDraft[] = [];
    for (const draft of local) {
      const existing = merged.get(draft.id);
      if (!existing || draft.updatedAt > existing.updatedAt) {
        merged.set(draft.id, draft);
        toUpload.push(draft);
      }
    }
    await Promise.all(toUpload.map((draft) => upsertRemote(draft).catch(() => undefined)));
    const all = sortNewest([...merged.values()]);
    writeLocal(all);
    return all;
  } catch {
    return local;
  }
}

async function upsertRemote(draft: SavedDraft): Promise<boolean> {
  const response = await dataRequest("user_drafts?on_conflict=user_id,draft_id", {
    method: "POST",
    headers: { "content-type": "application/json", Prefer: "resolution=merge-duplicates,return=minimal" },
    body: JSON.stringify({
      draft_id: draft.id, template_id: draft.templateId, title: draft.title, body: draft.body,
      reviewed: draft.reviewed, updated_at: draft.updatedAt
    })
  });
  return response !== null;
}

export async function saveDraft(draft: Omit<SavedDraft, "updatedAt">): Promise<{ drafts: SavedDraft[]; savedTo: DraftSaveTarget }> {
  const next: SavedDraft = { ...draft, updatedAt: new Date().toISOString() };
  const all = [next, ...readLocal().filter((item) => item.id !== draft.id)];
  writeLocal(all);
  let savedTo: DraftSaveTarget = "local";
  try {
    if (await upsertRemote(next)) savedTo = "account";
  } catch {
    /* offline, or migration 006 not applied yet — kept in this browser */
  }
  return { drafts: all, savedTo };
}

export async function deleteDraft(id: string): Promise<SavedDraft[]> {
  const all = readLocal().filter((item) => item.id !== id);
  writeLocal(all);
  try {
    await dataRequest(`user_drafts?draft_id=eq.${encodeURIComponent(id)}`, { method: "DELETE" });
  } catch {
    /* removed locally; the account copy can be deleted next time */
  }
  return all;
}
