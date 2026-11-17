import type { Metadata } from "next";
import { LegalPage, SupportContact } from "@/components/legal-page";

export const metadata: Metadata = {
  title: "Privacy Policy — Pakistan Justice Navigator",
  description: "What information Pakistan Justice Navigator collects, how it is used, and your choices."
};

export default function PrivacyPage() {
  return (
    <LegalPage current="/privacy" title="Privacy Policy" lede="Legal matters are personal. This policy explains what we collect, why, who processes it, and the choices you have.">
      <h2>1. What we collect</h2>
      <ul>
        <li><strong>Account details</strong> — your email address, name if you give one, and sign-in records.</li>
        <li><strong>Case information</strong> — the description of your situation, your answers to follow-up questions, the case brief, messages, and saved document drafts.</li>
        <li><strong>Documents you upload</strong> — files you choose to attach to a case, and information extracted from them.</li>
        <li><strong>Technical data</strong> — basic request logs (time, request ID, error codes) used for security and reliability. Logs are designed to leave out the text of your case.</li>
      </ul>
      <p>Share only what your matter needs. Never enter passwords, banking PINs or card numbers.</p>

      <h2>2. How we use it</h2>
      <ul>
        <li>to organise your situation, find relevant official legal sources, and produce your brief and drafts;</li>
        <li>to save your work to your account so you can return to it on any device;</li>
        <li>to keep the service secure, prevent abuse, and fix problems.</li>
      </ul>
      <p>We do not sell your information and do not use it for advertising.</p>

      <h2>3. Who processes your information</h2>
      <ul>
        <li><strong>Supabase</strong> stores accounts, cases, drafts and uploaded files. Access rules ensure each account can only read its own records.</li>
        <li><strong>AI model providers.</strong> To organise your situation and answer questions, the relevant text is sent through OpenRouter to third-party AI models. Some of these providers may keep or use submitted text under their own terms. Do not include information you are not comfortable sharing with them.</li>
        <li><strong>Voice typing.</strong> If you use the microphone button, your browser’s own speech service (for example Google in Chrome or Microsoft in Edge) turns speech into text. This website does not record or store audio — only the resulting text, when you choose to save it.</li>
      </ul>

      <h2>4. Information kept in your browser</h2>
      <p>Your browser keeps a working copy of your intake draft, cases and document drafts so the app is fast and works if your connection drops. This copy is cleared when you sign out.</p>

      <h2>5. How long we keep it</h2>
      <p>We keep your information while your account is active. When you ask us to delete your account, we delete your cases, drafts and uploaded files, except where we must keep something to meet a legal obligation or resolve a dispute.</p>

      <h2>6. Security</h2>
      <p>Data is encrypted in transit. Uploaded files are kept in private storage, and database access rules limit each account to its own records. No online service is completely secure, so please share only what is necessary.</p>

      <h2>7. Your choices</h2>
      <ul>
        <li>see and update your cases and drafts in the app, or ask us for a copy of the information we hold about you;</li>
        <li>delete individual drafts in the app, or ask us to delete your whole account;</li>
        <li>use the service without voice typing or document upload.</li>
      </ul>

      <h2>8. Children</h2>
      <p>The service is intended for adults. A person under 18 should use it with a parent or guardian.</p>

      <h2>9. Changes</h2>
      <p>If we change this policy materially, we will update the effective date and, where appropriate, tell you in the app.</p>

      <h2>10. Contact</h2>
      <p>Privacy questions or requests: <SupportContact />.</p>
    </LegalPage>
  );
}
