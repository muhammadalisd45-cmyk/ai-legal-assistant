import { NextResponse } from "next/server";
import { runDemoTriage } from "@/lib/demo-triage";
import type { Language, TriageResult } from "@/lib/types";

export const runtime = "nodejs";

function isLanguage(value: unknown): value is Language {
  return value === "en" || value === "roman-ur" || value === "ur";
}

export async function POST(request: Request) {
  const body = (await request.json()) as { description?: unknown; language?: unknown };
  const description = typeof body.description === "string" ? body.description.trim() : "";
  const language: Language = isLanguage(body.language) ? body.language : "en";

  if (description.length < 20) {
    return NextResponse.json(
      { error: "Please provide at least 20 characters describing the legal problem." },
      { status: 400 }
    );
  }

  const backendUrl = process.env.BACKEND_API_URL?.replace(/\/$/, "");

  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/v1/triage`, {
        method: "POST",
        headers: { "content-type": "application/json", "x-pjn-client": "citizen-web" },
        body: JSON.stringify({ description, language }),
        cache: "no-store",
        signal: AbortSignal.timeout(12000)
      });

      if (upstream.ok) {
        const result = (await upstream.json()) as TriageResult;
        return NextResponse.json({ ...result, mode: "backend" });
      }
    } catch {
      // Resilience fallback: keep intake usable if the external triage service is temporarily unavailable.
    }
  }

  const demo = runDemoTriage(description, language);
  return NextResponse.json({ ...demo, mode: backendUrl ? "demo-fallback" : "demo" });
}
