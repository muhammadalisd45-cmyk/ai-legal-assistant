import { ResetPasswordForm } from "@/components/reset-password-form";
import { requireUser } from "@/lib/supabase/server";

// Reached from the reset email: /auth/callback signs the user in with a recovery session, then sends them here.
export default async function ResetPasswordPage() {
  await requireUser("/reset-password");
  return <div className="page-shell login-page"><ResetPasswordForm /></div>;
}
