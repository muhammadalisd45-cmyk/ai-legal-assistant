"use client";

import { useEffect, useState } from "react";
import type { User } from "@supabase/supabase-js";
import { getSupabaseBrowserClient } from "./supabase/client";

// Browser caches that belong to whoever is signed in. Wiped on sign-out so a shared computer doesn't leak them.
const USER_SCOPED_KEYS = ["pjn:cases:v2", "pjn:intake:v2", "pjn:drafts:v1", "pjn:demo-user:v1", "pjn:supabase-session:v1"];

export function clearUserLocalData() {
  try { USER_SCOPED_KEYS.forEach((key) => window.localStorage.removeItem(key)); } catch { /* storage unavailable */ }
}

export async function signOut() {
  await getSupabaseBrowserClient().auth.signOut();
  clearUserLocalData();
}

export function displayName(user: User | null) {
  const meta = (user?.user_metadata ?? {}) as { full_name?: string };
  return meta.full_name?.trim() || user?.email?.split("@")[0] || "";
}

export function useCurrentUser() {
  const [user, setUser] = useState<User | null>(null);
  useEffect(() => {
    const supabase = getSupabaseBrowserClient();
    void supabase.auth.getUser().then(({ data }) => setUser(data.user));
    const { data } = supabase.auth.onAuthStateChange((_event, session) => setUser(session?.user ?? null));
    return () => data.subscription.unsubscribe();
  }, []);
  return user;
}
