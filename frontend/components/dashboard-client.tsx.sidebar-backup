"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { listCases } from "@/lib/case-store";
import type { CaseDraft } from "@/lib/types";
import { Icon } from "./icons";

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en-PK", { day: "numeric", month: "short", year: "numeric" }).format(new Date(value));
}

type DemoUser = { name: string; email: string; mode: "demo" };

export function DashboardClient() {
  const [cases, setCases] = useState<CaseDraft[] | null>(null);
  const [user, setUser] = useState<DemoUser | null>(null);

  useEffect(() => {
    void listCases().then(setCases);
    try {
      setUser(JSON.parse(window.localStorage.getItem("pjn:demo-user:v1") ?? "null") as DemoUser | null);
    } catch {
      setUser(null);
    }
  }, []);

  const stats = useMemo(() => {
    const list = cases ?? [];
    const docs = list.reduce((sum, item) => sum + item.documents.length, 0);
    const ready = list.filter((item) => item.consentAcknowledged).length;
    return { total: list.length, docs, ready };
  }, [cases]);

  return (
    <div className="page-shell dashboard dashboard-v3">
      <section className="dashboard-hero">
        <div>
          <span className="cinema-kicker dark">CITIZEN DASHBOARD —</span>
          <h1>{user?.name ? `Good to see you, ${user.name}.` : "Your cases, without the clutter."}</h1>
          <p>Continue an existing matter, start a new one, or inspect the official-source layer behind your brief.</p>
        </div>
        <Link href="/case/new" className="cinema-button primary"><Icon name="plus" size={18} /> Start a new case</Link>
      </section>

      <section className="dashboard-grid">
        <div className="dashboard-main">
          <div className="dashboard-section-head"><div><span>ACTIVE WORK</span><h2>Your cases</h2></div><Link href="/sources">Official sources →</Link></div>
          {cases === null ? (
            <div className="dashboard-skeleton"><div /><div /></div>
          ) : cases.length === 0 ? (
            <div className="dashboard-empty">
              <span className="dashboard-empty-mark"><Icon name="scale" size={30} /></span>
              <h3>Start with the story — not the legal terminology.</h3>
              <p>Your first case will appear here after the guided intake.</p>
              <Link href="/case/new" className="cinema-button secondary dark-border">Start your first case</Link>
            </div>
          ) : (
            <div className="dashboard-case-list">
              {cases.map((item, index) => (
                <Link href={`/case/${item.caseId}`} className="dashboard-case" key={item.caseId}>
                  <span className="dashboard-case-index">{String(index + 1).padStart(2, "0")}</span>
                  <div className="dashboard-case-copy"><small>{item.caseId} — {formatDate(item.updatedAt)}</small><strong>{item.triage.category}</strong><p>{item.triage.summary}</p></div>
                  <div className="dashboard-case-meta"><span>{item.documents.length} docs</span><Icon name="arrow" size={18} /></div>
                </Link>
              ))}
            </div>
          )}
        </div>

        <aside className="dashboard-rail">
          <div className="metric-panel"><span>CASE RECORDS</span><strong>{stats.total}</strong><small>saved in this experience</small></div>
          <div className="metric-panel"><span>DOCUMENTS</span><strong>{stats.docs}</strong><small>attached across cases</small></div>
          <div className="metric-panel"><span>BRIEFS</span><strong>{stats.ready}</strong><small>acknowledged for review</small></div>
          <Link href="/research" className="research-callout"><Icon name="search" size={24} /><span><strong>Official Legal Research</strong><small>Search official sources and review what has been verified.</small></span><Icon name="arrow" size={18} /></Link>
        </aside>
      </section>

      <section className="dashboard-bottom-strip">
        <div><Icon name="shield" size={18} /><span><strong>Privacy</strong><small>Only add information needed for the matter.</small></span></div>
        <div><Icon name="book" size={18} /><span><strong>Provenance</strong><small>Official source identity remains attached.</small></span></div>
        <div><Icon name="message" size={18} /><span><strong>Language</strong><small>English, Urdu and Roman Urdu intake.</small></span></div>
      </section>
    </div>
  );
}
