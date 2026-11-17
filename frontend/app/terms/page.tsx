import type { Metadata } from "next";
import Link from "next/link";
import { LegalPage, SupportContact } from "@/components/legal-page";

export const metadata: Metadata = {
  title: "Terms of Service — Pakistan Justice Navigator",
  description: "The terms that apply when you use Pakistan Justice Navigator."
};

export default function TermsPage() {
  return (
    <LegalPage current="/terms" title="Terms of Service" lede="Please read these terms before using Pakistan Justice Navigator. By creating an account or using the service, you agree to them.">
      <h2>1. What this service is — and is not</h2>
      <p>Pakistan Justice Navigator (“the service”, “we”) helps you describe a legal situation in your own words, organise facts, find potentially relevant Pakistani laws from official sources, and prepare questions and documents for a qualified legal professional.</p>
      <p><strong>The service provides legal information and case-preparation support only. It is not legal advice, it does not create a lawyer–client relationship, and it is not a substitute for a qualified lawyer.</strong> Laws change, and every situation is different. Verify important facts, deadlines and legal sources with a qualified lawyer before acting on them.</p>
      <p>If you or someone else is in immediate danger, contact the police (15) or emergency services first.</p>

      <h2>2. AI-generated content</h2>
      <p>Parts of the service use artificial intelligence. AI output can be incomplete, out of date or wrong, even when it cites a source. Summaries, categories, review priorities, suggested next steps and drafted documents are starting points that you must check. Always read the cited official source yourself before relying on it.</p>

      <h2>3. Your account</h2>
      <ul>
        <li>You must give accurate sign-up information and keep your password secure.</li>
        <li>You are responsible for activity on your account. Tell us promptly if you suspect unauthorised use.</li>
        <li>You must be at least 18 years old, or use the service with the involvement of a parent or guardian.</li>
      </ul>

      <h2>4. Acceptable use</h2>
      <p>You agree not to:</p>
      <ul>
        <li>use the service for anything unlawful, or to harass, defame, threaten or impersonate anyone;</li>
        <li>upload content you have no right to share, or other people’s private information beyond what your matter requires;</li>
        <li>attempt to break, overload, scrape, reverse-engineer or bypass the security of the service;</li>
        <li>present output from the service as advice from a lawyer, or file drafted documents without reviewing them.</li>
      </ul>

      <h2>5. Your content</h2>
      <p>You keep ownership of what you write and upload. You give us permission to store and process it only as needed to provide the service to you, as described in our <Link href="/privacy">Privacy Policy</Link>.</p>

      <h2>6. Paid features</h2>
      <p>The service is currently free. If paid plans are introduced, prices, what is included, and billing terms will be shown clearly before you pay, and our <Link href="/refunds">Refund Policy</Link> will apply.</p>

      <h2>7. Availability and changes</h2>
      <p>We work to keep the service available but do not guarantee it will be uninterrupted or error-free. We may change, suspend or discontinue features. If we change these terms materially, we will update the effective date and, where appropriate, tell you in the app.</p>

      <h2>8. Limitation of liability</h2>
      <p>To the extent permitted by law, the service is provided “as is”, and we are not liable for any loss arising from reliance on information or documents produced by the service, from missed deadlines, or from decisions made without professional legal advice. Nothing in these terms limits liability that cannot be limited under the laws of Pakistan.</p>

      <h2>9. Ending your use</h2>
      <p>You may stop using the service at any time and ask us to delete your account. We may suspend or close accounts that break these terms.</p>

      <h2>10. Governing law</h2>
      <p>These terms are governed by the laws of the Islamic Republic of Pakistan.</p>

      <h2>11. Contact</h2>
      <p>Questions about these terms: <SupportContact />.</p>
    </LegalPage>
  );
}
