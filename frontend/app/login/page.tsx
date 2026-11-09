import { LoginForm } from "@/components/login-form";
import { safeNext } from "@/lib/supabase/config";

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ next?: string; error?: string }> }) {
  const params = await searchParams;
  return <div className="page-shell login-page"><LoginForm next={safeNext(params.next)} linkError={params.error === "link"} /></div>;
}
