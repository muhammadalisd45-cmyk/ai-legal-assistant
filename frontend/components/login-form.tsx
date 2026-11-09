"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getSupabaseBrowserClient } from "@/lib/supabase/client";
import { Icon } from "./icons";

type Mode = "signin" | "signup" | "forgot";

const COPY: Record<Mode, { head: string; title: string; lede: string; button: string }> = {
  signin: { head: "SIGN IN", title: "Welcome back.", lede: "Sign in to open your dashboard and saved cases.", button: "Sign in" },
  signup: { head: "CREATE ACCOUNT", title: "Create your account.", lede: "Your cases are saved to your account and visible only to you.", button: "Create account" },
  forgot: { head: "RESET PASSWORD", title: "Forgot your password?", lede: "We'll email you a link to set a new one.", button: "Send reset link" }
};

function friendlyError(message: string) {
  const m = message.toLowerCase();
  if (m.includes("invalid login credentials")) return "Email or password is incorrect.";
  if (m.includes("email not confirmed")) return "Please confirm your email first — check your inbox for the link.";
  if (m.includes("already registered")) return "An account with this email already exists. Sign in instead.";
  if (m.includes("rate limit")) return "Too many attempts. Please wait a few minutes and try again.";
  return message;
}

export function LoginForm({ next, linkError }: { next: string; linkError: boolean }) {
  const router = useRouter();
  const [mode, setMode] = useState<Mode>("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(linkError ? "That email link is invalid or has expired. Please try again." : "");
  const [info, setInfo] = useState("");
  const [busy, setBusy] = useState(false);

  function switchMode(value: Mode) {
    setMode(value);
    setError("");
    setInfo("");
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setInfo("");
    const cleanEmail = email.trim();
    if (!/^\S+@\S+\.\S+$/.test(cleanEmail)) return setError("Enter a valid email address.");
    if (mode !== "forgot" && password.length < 8) return setError("Password must be at least 8 characters.");

    const supabase = getSupabaseBrowserClient();
    const callback = (target: string) => `${window.location.origin}/auth/callback?next=${encodeURIComponent(target)}`;
    setBusy(true);
    try {
      if (mode === "signin") {
        const { error: authError } = await supabase.auth.signInWithPassword({ email: cleanEmail, password });
        if (authError) return setError(friendlyError(authError.message));
        router.replace(next);
        router.refresh();
      } else if (mode === "signup") {
        const { data, error: authError } = await supabase.auth.signUp({
          email: cleanEmail,
          password,
          options: { data: { full_name: name.trim() }, emailRedirectTo: callback(next) }
        });
        if (authError) return setError(friendlyError(authError.message));
        // With email confirmation on, Supabase returns no session and (for an existing email) an empty identities list.
        if (data.user && data.user.identities?.length === 0) return setError(friendlyError("already registered"));
        if (data.session) {
          router.replace(next);
          router.refresh();
          return;
        }
        setPassword("");
        setInfo(`We sent a confirmation link to ${cleanEmail}. Open it to activate your account, then sign in.`);
        setMode("signin");
      } else {
        const { error: authError } = await supabase.auth.resetPasswordForEmail(cleanEmail, { redirectTo: callback("/reset-password") });
        if (authError) return setError(friendlyError(authError.message));
        setInfo(`If an account exists for ${cleanEmail}, a reset link is on its way.`);
      }
    } catch {
      setError("Could not reach the sign-in service. Check your connection and try again.");
    } finally {
      setBusy(false);
    }
  }

  const copy = COPY[mode];

  return (
    <div className="login-stage">
      <div className="login-architecture" aria-hidden="true"><span /><span /><span /></div>
      <section className="login-copy">
        <span className="cinema-kicker">RETURN TO YOUR CASE —</span>
        <h1>Your legal story stays <em>organized.</em></h1>
        <p>Sign in to your account to keep your cases, briefs and drafts in one private workspace.</p>
        <div className="login-proof">
          <div><Icon name="shield" size={18} /><span><strong>Private by design</strong><small>Your cases are visible only to your account.</small></span></div>
          <div><Icon name="book" size={18} /><span><strong>Source-aware</strong><small>Official provenance remains visible.</small></span></div>
          <div><Icon name="document" size={18} /><span><strong>Case continuity</strong><small>Continue drafts and briefs.</small></span></div>
        </div>
      </section>
      <form className="login-panel" onSubmit={submit} noValidate>
        <div className="login-panel-head"><Icon name="scale" size={24} /><span>{copy.head}</span></div>
        <h2>{copy.title}</h2>
        <p>{copy.lede}</p>
        {mode === "signup" && (
          <label><span>Name</span><input value={name} onChange={(event) => setName(event.target.value)} placeholder="Your name" autoComplete="name" maxLength={60} /></label>
        )}
        <label><span>Email</span><input value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" type="email" autoComplete="email" required /></label>
        {mode !== "forgot" && (
          <label><span>Password</span><input value={password} onChange={(event) => setPassword(event.target.value)} placeholder={mode === "signup" ? "At least 8 characters" : "Your password"} type="password" autoComplete={mode === "signup" ? "new-password" : "current-password"} minLength={8} required /></label>
        )}
        {error ? <div className="inline-form-error" role="alert">{error}</div> : null}
        {info ? <div className="login-info" role="status">{info}</div> : null}
        <button type="submit" className="cinema-button primary full" disabled={busy}>{busy ? "Please wait…" : copy.button} <Icon name="arrow" size={18} /></button>
        <div className="login-switch">
          {mode === "signin" && <>
            <button type="button" onClick={() => switchMode("forgot")}>Forgot password?</button>
            <button type="button" onClick={() => switchMode("signup")}>New here? Create an account</button>
          </>}
          {mode !== "signin" && <button type="button" onClick={() => switchMode("signin")}>Already have an account? Sign in</button>}
        </div>
        <Link href="/" className="quiet-back">← Back to experience</Link>
      </form>
    </div>
  );
}
