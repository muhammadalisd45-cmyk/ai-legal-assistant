// Browser-safe Supabase settings. The anon/publishable key is designed to be public; RLS protects the data.
export function supabaseConfig() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.replace(/\/$/, "");
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !key) {
    throw new Error("Supabase is not configured. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY.");
  }
  return { url, key };
}

// Routes that require a signed-in account. Public reference pages (research, sources, map, learn) stay open.
export const PROTECTED_PREFIXES = ["/dashboard", "/case", "/briefs", "/drafting", "/saved", "/settings"];
// API routes that spend AI credits or touch user data.
export const PROTECTED_API_PREFIXES = ["/api/triage"];

export function matchesPrefix(pathname: string, prefixes: string[]) {
  return prefixes.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`));
}

// Only allow same-site relative redirects after login (blocks open-redirects like ?next=//evil.com).
export function safeNext(value: string | null | undefined, fallback = "/dashboard") {
  if (!value || !value.startsWith("/") || value.startsWith("//") || value.startsWith("/\\")) return fallback;
  return value;
}
