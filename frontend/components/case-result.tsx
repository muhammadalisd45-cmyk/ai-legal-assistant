"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { loadCase } from "@/lib/case-store";
import type { CaseDraft, ClarificationAnswer, LegalDocumentMeta } from "@/lib/types";
import { Icon } from "./icons";
import { Reveal } from "./reveal";

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-PK", { day: "numeric", month: "long", year: "numeric" }).format(new Date(value));
}

const PRIORITY_LABEL: Record<CaseDraft["triage"]["urgency"], string> = {
  low: "Low", medium: "Medium", high: "High", critical: "Critical", unknown: "Not assessed"
};

/** A provision returned by the legal search (only the fields the brief uses). */
type Provision = {
  key: string;
  title: string;
  section: string;
  heading: string;
  page: string;
  url: string;
  excerpt: string;
};

type SearchHit = {
  document_id: string;
  title: string;
  section_or_article?: string;
  section_heading?: string;
  page_reference?: string;
  page_start?: number | null;
  source_url?: string;
  snippet?: string;
  evidence_level?: string;
  relevance?: { strong_match?: boolean } | null;
};

function clarificationsOf(draft: CaseDraft): ClarificationAnswer[] {
  if (draft.clarifications?.length) return draft.clarifications;
  // Older cases stored only id → answer; recover the question text where the triage still has it.
  const prompts = new Map(draft.triage.followUpQuestions.map((q) => [q.id, q.prompt]));
  return Object.entries(draft.answers)
    .filter(([, answer]) => answer?.trim())
    .map(([id, answer]) => ({ id, question: prompts.get(id) ?? "", answer }));
}

function excerpt(text: string, max = 170) {
  const clean = text.replace(/\s+/g, " ").trim();
  return clean.length > max ? `${clean.slice(0, max).replace(/\s+\S*$/, "")}…` : clean;
}

/** Official provisions for the brief: strong chunk-level matches only — never metadata guesses. */
function useRelatedProvisions(draft: CaseDraft | null | undefined) {
  const [state, setState] = useState<{ status: "idle" | "loading" | "done" | "error"; items: Provision[] }>({ status: "idle", items: [] });

  useEffect(() => {
    // Without an identified issue the query is just the raw story, which is too noisy to show provisions for.
    if (!draft || draft.triage.legalIssues.length === 0) {
      setState({ status: "done", items: [] });
      return;
    }
    const general = draft.triage.category === "General legal matter";
    const query = [general ? "" : draft.triage.category, ...draft.triage.legalIssues, draft.description.slice(0, 700)]
      .filter(Boolean)
      .join(". ")
      .slice(0, 1100);
    let cancelled = false;
    setState({ status: "loading", items: [] });
    fetch("/api/legal-search", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ query, limit: 6 }) })
      .then((response) => (response.ok ? response.json() : Promise.reject(new Error(String(response.status)))))
      .then((payload: { results?: SearchHit[] }) => {
        if (cancelled) return;
        const seen = new Set<string>();
        const items: Provision[] = [];
        for (const hit of payload.results ?? []) {
          if (hit.evidence_level !== "chunk" || !hit.relevance?.strong_match || !hit.section_or_article) continue;
          const key = `${hit.document_id}|${hit.section_or_article}`;
          if (seen.has(key)) continue;
          seen.add(key);
          const url = hit.source_url ? `${hit.source_url}${hit.page_start ? `#page=${hit.page_start}` : ""}` : "";
          items.push({
            key,
            title: hit.title,
            section: hit.section_or_article,
            heading: hit.section_heading ?? "",
            page: hit.page_reference ?? "",
            url,
            excerpt: excerpt(hit.snippet ?? "")
          });
          if (items.length === 4) break;
        }
        setState({ status: "done", items });
      })
      .catch(() => !cancelled && setState({ status: "error", items: [] }));
    return () => {
      cancelled = true;
    };
  }, [draft]);

  return state;
}

export function CaseResult({ sourceMap, caseId }: { sourceMap: Record<string, LegalDocumentMeta>; caseId: string }) {
  const [draft, setDraft] = useState<CaseDraft | null | undefined>(undefined);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    void loadCase(caseId).then(setDraft);
  }, [caseId]);

  const sources = useMemo(() => {
    if (!draft) return [];
    return draft.triage.sourceIds.map((id) => sourceMap[id]).filter((source): source is LegalDocumentMeta => Boolean(source) && !source.title.toLowerCase().includes("placeholder"));
  }, [draft, sourceMap]);
  const provisions = useRelatedProvisions(draft);

  async function copyReference() {
    if (!draft) return;
    await navigator.clipboard.writeText(draft.caseId);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  if (draft === undefined) return <div className="loading-card surface-card"><span className="loading-line" /> <span className="loading-line short" /> <p>Preparing your saved brief —</p></div>;

  if (draft === null) {
    return (
      <div className="missing-case depth-card">
        <span className="empty-icon"><Icon name="document" size={30} /></span>
        <span className="eyebrow">CASE NOT FOUND —</span>
        <h1>We couldn’t find this case in your saved drafts.</h1>
        <p>No example case has been substituted. Start a new case or return to your case list.</p>
        <div className="hero-actions"><Link href="/case/new" className="button button-accent">Start new case</Link><Link href="/dashboard" className="button button-quiet">My cases</Link></div>
      </div>
    );
  }

  const analyzedDocuments = draft.documents.filter((file) => file.status === "analyzed").length;
  const clarifications = clarificationsOf(draft);
  const pathways = draft.triage.pathways ?? [];
  const urgency = draft.triage.urgency;

  return (
    <div className="result-shell">
      <Reveal className="result-heading">
        <div>
          <span className="eyebrow">CASE {draft.caseId} — PREPARED {formatDate(draft.createdAt)}</span>
          <h1>{draft.triage.category}</h1>
          <p className="lede">A reviewable brief that keeps your statements, AI organization, document status and source context visibly separate.</p>
        </div>
        <div className="result-actions"><button className="button button-quiet" type="button" onClick={copyReference}>{copied ? "Copied" : "Copy case reference"}</button><button className="button button-dark" type="button" onClick={() => window.print()}>Print / save brief</button></div>
      </Reveal>

      <Reveal className="brief-summary" delay={50}>
        <div className="summary-mark"><Icon name="scale" size={25} /></div>
        <div><span className="section-kicker">— WHAT WE UNDERSTOOD</span><p className="summary-text">{draft.triage.summary}</p><p>This is a preliminary organization of the information provided. It is not a final legal conclusion.</p></div>
        <div className={`review-priority priority-${urgency}`}><strong>{PRIORITY_LABEL[urgency] ?? urgency}</strong><span>review priority</span><small>{urgency === "unknown" ? "Not enough detail yet to set a review priority." : "Workflow signal — not a verified legal urgency."}</small></div>
      </Reveal>

      <div className="provenance-key" aria-label="Information status legend">
        <span className="provenance-pill reported">YOU REPORTED</span>
        <span className="provenance-pill review">AI ORGANIZED</span>
        <span className="provenance-pill source">SOURCE TO VERIFY</span>
        <span className="provenance-pill verified">VERIFIED EVIDENCE</span>
      </div>

      <div className="result-grid">
        <section className="result-main">
          <Reveal>
            <article className="surface-card result-card">
              <span className="section-kicker">— 01 / YOUR ACCOUNT</span>
              <span className="provenance-pill reported">YOU REPORTED</span>
              <p className="quote-story">{draft.description}</p>
              <div className="fact-row"><span><Icon name="message" size={17} /> Citizen statement</span><span>{clarifications.length} clarification{clarifications.length === 1 ? "" : "s"}</span><span>{draft.documents.length} file{draft.documents.length === 1 ? "" : "s"} selected</span></div>
            </article>
          </Reveal>

          {clarifications.length > 0 && <Reveal><article className="surface-card result-card"><span className="section-kicker">— 02 / CLARIFICATIONS</span><span className="provenance-pill reported">YOU REPORTED</span><div className="answer-ledger">{clarifications.map((item, index) => <div key={item.id}><span>{String(index + 1).padStart(2, "0")}</span><div>{item.question && <small className="answer-question">{item.question}</small>}<strong>{item.answer}</strong></div></div>)}</div></article></Reveal>}

          <Reveal>
            <article className="surface-card result-card">
              <span className="section-kicker">— 03 / POINTS TO REVIEW</span>
              <span className="provenance-pill review">AI ORGANIZED</span>
              {draft.triage.legalIssues.length > 0
                ? <div className="issue-list">{draft.triage.legalIssues.map((issue, index) => <div className="issue" key={issue}><span>{String(index + 1).padStart(2, "0")}</span><strong>{issue}</strong></div>)}</div>
                : <div className="empty-inline review-empty">No specific legal topic could be identified from the description yet. Adding what happened, when, and what you want to achieve will help.</div>}
              <p className="card-footnote">These are review topics, not findings that a law definitely applies.</p>
            </article>
          </Reveal>

          <Reveal>
            <article className="surface-card result-card">
              <span className="section-kicker">— 04 / WHAT STILL NEEDS CHECKING</span>
              {draft.triage.missingInformation.length > 0
                ? <ul className="checklist">{draft.triage.missingInformation.map((item) => <li key={item}><span>○</span>{item}</li>)}</ul>
                : <div className="empty-inline review-empty">Nothing specific was flagged — still verify dates, documents and sources before relying on this brief.</div>}
            </article>
          </Reveal>

          <Reveal>
            <article className="surface-card result-card">
              <span className="section-kicker">— 05 / DOCUMENT STATUS</span>
              {draft.documents.length === 0 ? <div className="empty-inline">No documents were attached. You can still use this brief to collect the right material later.</div> : <div className="file-list">{draft.documents.map((file) => <div className="file-row" key={`${file.name}-${file.size}`}><span className="file-icon"><Icon name="document" size={18} /></span><div><strong>{file.name}</strong><small>{file.status === "analyzed" ? "Document analysis confirmed" : "File listed in the case — content not yet verified"}</small></div><span className={file.status === "analyzed" ? "status" : "status status-neutral"}>{file.status === "analyzed" ? "Analyzed" : "Not analyzed"}</span></div>)}</div>}
              {analyzedDocuments === 0 && draft.documents.length > 0 && <p className="card-footnote">No document-derived fact is treated as verified yet.</p>}
            </article>
          </Reveal>

          <Reveal>
            <article className="next-steps-card depth-card">
              <span className="section-kicker">— 06 / PRACTICAL NEXT STEPS</span>
              <h2>Use this brief to make the next conversation more focused.</h2>
              {pathways.length > 0 ? (
                <ol>
                  {pathways.map((pathway, index) => <li key={pathway.title}><span>{String(index + 1).padStart(2, "0")}</span><div><strong>{pathway.title}</strong><p>{pathway.description}</p>{pathway.caution && <p className="pathway-caution">{pathway.caution}</p>}</div></li>)}
                  <li><span>{String(pathways.length + 1).padStart(2, "0")}</span><div><strong>Fill the missing information</strong><p>Collect the facts listed above before relying on the brief.</p></div></li>
                </ol>
              ) : (
                <ol>
                  <li><span>01</span><div><strong>Fill the missing information</strong><p>Collect the facts listed above before relying on the brief.</p></div></li>
                  <li><span>02</span><div><strong>Verify important documents and dates</strong><p>Especially any receipts, notices, orders or records connected to the matter, and any possible deadline.</p></div></li>
                  <li><span>03</span><div><strong>Inspect the original sources</strong><p>Provisions are linked separately and should not be treated as case-specific citations until verified.</p></div></li>
                  <li><span>04</span><div><strong>Take the brief to a qualified professional where needed</strong><p>The organized chronology and questions can reduce time spent re-explaining the matter.</p></div></li>
                </ol>
              )}
            </article>
          </Reveal>
        </section>

        <aside className="result-aside">
          <Reveal>
            <article className="source-stack depth-card">
              <span className="section-kicker">POSSIBLE OFFICIAL SOURCES —</span>
              <p>Official provisions found by searching the legal library for this matter. They are starting points to read — whether they apply to your facts has not been verified.</p>
              {provisions.items.map((item) => (
                <a className="source-mini" href={item.url || undefined} target="_blank" rel="noreferrer" key={item.key}>
                  <span className="source-code"><Icon name="book" size={17} /></span>
                  <div>
                    <strong>{item.section}{item.heading ? ` — ${item.heading}` : ""}</strong>
                    <small>{item.title}{item.page ? ` · ${item.page}` : ""}</small>
                    {item.excerpt && <q className="provision-excerpt">{item.excerpt}</q>}
                    <em>Official text · applicability not verified</em>
                  </div>
                  <Icon name="external" size={16} />
                </a>
              ))}
              {sources.map((source) => <a className="source-mini" href={source.source_url} target="_blank" rel="noreferrer" key={source.document_id}><span className="source-code"><Icon name="book" size={17} /></span><div><strong>{source.title}</strong><small>{source.authority} — {source.jurisdiction}</small><em>Official title linked · relevance pending</em></div><Icon name="external" size={16} /></a>)}
              {provisions.status === "loading" && <div className="empty-inline dark">Searching the official legal library…</div>}
              {provisions.status !== "loading" && provisions.items.length === 0 && sources.length === 0 && (
                <div className="empty-inline dark">{provisions.status === "error" ? "The legal library could not be searched right now. Try reloading, or browse the source directory." : "No official provision matched this matter closely enough to show. Browse the source directory or ask a lawyer which law applies."}</div>
              )}
              <Link className="text-link" href="/sources">Browse official source directory <Icon name="arrow" size={16} /></Link>
            </article>
          </Reveal>

          <Reveal>
            <article className="guardrail-card surface-card"><Icon name="shield" size={27} /><div><strong>Important boundary —</strong><p>{draft.triage.guardrail}</p></div></article>
          </Reveal>

          <Reveal>
            <article className="consult-card">
              <span>READY FOR REVIEW —</span>
              <h3>Take a cleaner story into a legal consultation.</h3>
              <p>Print or save this brief together with the original documents. Keep the original source links available for verification.</p>
              <button className="button button-accent full" type="button" onClick={() => window.print()}>Prepare consultation copy <Icon name="arrow" size={18} /></button>
            </article>
          </Reveal>
        </aside>
      </div>
    </div>
  );
}
