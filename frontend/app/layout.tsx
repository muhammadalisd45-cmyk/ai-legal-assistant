import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";
import "./globals.css";
import { TopNav } from "@/components/top-nav";
import { Icon } from "@/components/icons";

export const metadata: Metadata = {
  title: "Pakistan Justice Navigator",
  description: "AI-assisted case preparation grounded in Pakistani official legal sources."
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <TopNav />
        <main>{children}</main>
        <footer className="footer footer-v3">
          <div className="footer-brand-block">
            <div className="footer-brand"><span><Icon name="scale" size={24} /></span><strong>Pakistan Justice<br />Navigator</strong></div>
            <p>Clearer legal information. Better-prepared conversations.</p>
          </div>
          <div className="footer-links"><div><strong>Product</strong><Link href="/#story">How it works</Link><Link href="/dashboard">Dashboard</Link><Link href="/case/new">Start case</Link></div><div><strong>Research</strong><Link href="/sources">Official sources</Link><Link href="/research">Official legal research</Link></div><div><strong>Access</strong><Link href="/login">Sign in</Link><Link href="/case/new">Citizen intake</Link></div></div>
          <div className="footer-legal"><span>© 2026 Pakistan Justice Navigator. All rights reserved.</span><p>Information and case-preparation support only — not legal representation or professional legal advice.</p></div>
        </footer>
      </body>
    </html>
  );
}
