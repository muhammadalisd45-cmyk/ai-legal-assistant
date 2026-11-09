"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { getSupabaseBrowserClient } from "@/lib/supabase/client";
import { Icon } from "./icons";

export function ResetPasswordForm() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    if (password.length < 8) return setError("Password must be at least 8 characters.");
    if (password !== confirm) return setError("The two passwords don't match.");
    setBusy(true);
    const { error: authError } = await getSupabaseBrowserClient().auth.updateUser({ password });
    setBusy(false);
    if (authError) return setError(authError.message);
    router.replace("/dashboard");
    router.refresh();
  }

  return (
    <div className="login-stage">
      <form className="login-panel" onSubmit={submit} noValidate>
        <div className="login-panel-head"><Icon name="scale" size={24} /><span>NEW PASSWORD</span></div>
        <h2>Set a new password.</h2>
        <p>Choose a password of at least 8 characters.</p>
        <label><span>New password</span><input type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="new-password" required /></label>
        <label><span>Confirm password</span><input type="password" value={confirm} onChange={(event) => setConfirm(event.target.value)} autoComplete="new-password" required /></label>
        {error ? <div className="inline-form-error" role="alert">{error}</div> : null}
        <button type="submit" className="cinema-button primary full" disabled={busy}>{busy ? "Saving…" : "Save password"} <Icon name="arrow" size={18} /></button>
      </form>
    </div>
  );
}
