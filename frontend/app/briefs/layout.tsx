import type { ReactNode } from "react";
import { requireUser } from "@/lib/supabase/server";

// Server-side account check (backs up proxy.ts): no signed-in account, no page.
export default async function ProtectedLayout({ children }: { children: ReactNode }) {
  await requireUser("/briefs");
  return children;
}
