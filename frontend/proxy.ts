import { NextResponse, type NextRequest } from "next/server";
import { createServerClient } from "@supabase/ssr";
import { PROTECTED_API_PREFIXES, PROTECTED_PREFIXES, matchesPrefix, supabaseConfig } from "@/lib/supabase/config";

// Next.js 16 "proxy" (formerly middleware): refreshes the Supabase session cookie on every request and
// blocks signed-out visitors from the workspace before any page renders.
export async function proxy(request: NextRequest) {
  let response = NextResponse.next({ request });
  const { url, key } = supabaseConfig();

  const supabase = createServerClient(url, key, {
    cookies: {
      getAll() {
        return request.cookies.getAll();
      },
      setAll(cookiesToSet, headers) {
        cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value));
        response = NextResponse.next({ request });
        cookiesToSet.forEach(({ name, value, options }) => response.cookies.set(name, value, options));
        Object.entries(headers ?? {}).forEach(([header, value]) => response.headers.set(header, value));
      }
    }
  });

  // getUser() validates the token with Supabase Auth, so a forged or expired cookie is rejected.
  const { data } = await supabase.auth.getUser();
  const user = data.user && !data.user.is_anonymous ? data.user : null;
  const { pathname, search } = request.nextUrl;

  if (!user && matchesPrefix(pathname, PROTECTED_API_PREFIXES)) {
    return NextResponse.json({ error: "Please sign in to continue." }, { status: 401 });
  }

  if (!user && matchesPrefix(pathname, PROTECTED_PREFIXES)) {
    const loginUrl = request.nextUrl.clone();
    loginUrl.pathname = "/login";
    loginUrl.search = `?next=${encodeURIComponent(pathname + search)}`;
    const redirect = NextResponse.redirect(loginUrl);
    response.cookies.getAll().forEach((cookie) => redirect.cookies.set(cookie));
    return redirect;
  }

  if (user && pathname === "/login") {
    const dashboardUrl = request.nextUrl.clone();
    dashboardUrl.pathname = "/dashboard";
    dashboardUrl.search = "";
    return NextResponse.redirect(dashboardUrl);
  }

  return response;
}

export const config = {
  // Skip static assets and images; run everywhere else so sessions stay fresh.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|references/|video/|.*\\.(?:svg|png|jpg|jpeg|gif|webp|mp4|pdf)$).*)"]
};
