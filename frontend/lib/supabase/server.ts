import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { createServerClient } from "@supabase/ssr";
import { supabaseConfig } from "./config";

export async function getSupabaseServerClient() {
  const cookieStore = await cookies();
  const { url, key } = supabaseConfig();
  return createServerClient(url, key, {
    cookies: {
      getAll() {
        return cookieStore.getAll();
      },
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options));
        } catch {
          // Called from a Server Component, where cookies are read-only. The proxy refreshes sessions instead.
        }
      }
    }
  });
}

// Verified current user (checked with Supabase Auth, not just read from the cookie). Anonymous users don't count.
export async function getCurrentUser() {
  const supabase = await getSupabaseServerClient();
  const { data, error } = await supabase.auth.getUser();
  if (error || !data.user || data.user.is_anonymous) return null;
  return data.user;
}

// Second line of defence behind proxy.ts: call from protected pages/layouts.
export async function requireUser(nextPath: string) {
  const user = await getCurrentUser();
  if (!user) redirect(`/login?next=${encodeURIComponent(nextPath)}`);
  return user;
}
