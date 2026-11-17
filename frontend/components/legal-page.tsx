import Link from "next/link";
import type { ReactNode } from "react";

export const LEGAL_EFFECTIVE_DATE = "17 November 2026";

/** Support contact shown on the legal pages. Set NEXT_PUBLIC_SUPPORT_EMAIL before launch. */
export function SupportContact() {
  const email = process.env.NEXT_PUBLIC_SUPPORT_EMAIL?.trim();
  return email ? <a href={`mailto:${email}`}>{email}</a> : <span>the support contact published on this website</span>;
}

const PAGES = [
  { href: "/terms", label: "Terms of Service" },
  { href: "/privacy", label: "Privacy Policy" },
  { href: "/refunds", label: "Refund Policy" }
];

export function LegalPage({ title, lede, current, children }: { title: string; lede: string; current: string; children: ReactNode }) {
  return (
    <article className="legal-doc">
      <header className="legal-doc-head">
        <span className="eyebrow">LEGAL —</span>
        <h1>{title}</h1>
        <p className="lede">{lede}</p>
        <p className="legal-doc-date">Effective {LEGAL_EFFECTIVE_DATE}</p>
        <nav aria-label="Legal documents" className="legal-doc-nav">
          {PAGES.map((page) => (
            <Link key={page.href} href={page.href} aria-current={page.href === current ? "page" : undefined}>{page.label}</Link>
          ))}
        </nav>
      </header>
      <div className="legal-doc-body">{children}</div>
    </article>
  );
}
