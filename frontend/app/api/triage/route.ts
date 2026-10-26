import { NextResponse } from "next/server";
import { runDemoTriage } from "@/lib/demo-triage";
import { parseClientTriageRequest, requestBackendTriage } from "@/lib/triage-contract.mjs";

export const runtime = "nodejs";

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Send a valid JSON triage request." }, { status: 400 });
  }
  const parsed = parseClientTriageRequest(body);
  if (!parsed.ok) return NextResponse.json({ error: parsed.error }, { status: 400 });

  const backendUrl = process.env.BACKEND_API_URL?.replace(/\/$/, "");

  if (backendUrl) {
    const upstream = await requestBackendTriage({ backendUrl, request: parsed.value });
    if (upstream.ok) return NextResponse.json(upstream.result);
    // Deliberately do not substitute demo output when a configured backend is unavailable.
    return NextResponse.json(
      { error: "The triage service is temporarily unavailable. Please retry; your draft remains saved." },
      { status: 502 }
    );
  }

  const demo = runDemoTriage(parsed.value.description, parsed.value.language);
  return NextResponse.json({
    ...demo,
    notice: "Demo triage is active because no triage backend is configured. This is not a live AI assessment."
  });
}
