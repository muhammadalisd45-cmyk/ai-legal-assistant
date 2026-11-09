"use client";

import { createBrowserClient } from "@supabase/ssr";
import type { SupabaseClient } from "@supabase/supabase-js";
import { supabaseConfig } from "./config";

let client: SupabaseClient | null = null;

// Session is kept in cookies (not localStorage) so the server/proxy can verify it before rendering protected pages.
export function getSupabaseBrowserClient() {
  if (!client) {
    const { url, key } = supabaseConfig();
    client = createBrowserClient(url, key);
  }
  return client;
}
