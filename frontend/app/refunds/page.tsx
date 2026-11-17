import type { Metadata } from "next";
import { LegalPage, SupportContact } from "@/components/legal-page";

export const metadata: Metadata = {
  title: "Refund Policy — Pakistan Justice Navigator",
  description: "How refunds work for Pakistan Justice Navigator."
};

export default function RefundsPage() {
  return (
    <LegalPage current="/refunds" title="Refund Policy" lede="Pakistan Justice Navigator is currently free to use. This page explains how refunds will work if paid plans are introduced.">
      <h2>1. Current status</h2>
      <p>There are no paid plans at the moment, and we do not take payments. If anyone asks you to pay for Pakistan Justice Navigator outside this website, do not pay and let us know.</p>

      <h2>2. Before any paid plan launches</h2>
      <p>Before we charge for anything, we will update this policy with the exact refund terms for each plan. You will see the price, what is included, how billing works, and how to cancel before you pay.</p>

      <h2>3. What you can expect</h2>
      <ul>
        <li>You will be able to cancel a subscription at any time; cancelling stops future charges.</li>
        <li>If you are charged twice, charged in error, or charged for a service that could not be delivered because of a fault on our side, we will refund that charge.</li>
        <li>Refunds will be returned to the original payment method.</li>
      </ul>
      <p>Refunds cannot depend on the outcome of a legal matter. The service provides information and preparation support, not legal representation or a guaranteed result.</p>

      <h2>4. Contact</h2>
      <p>Billing questions: <SupportContact />.</p>
    </LegalPage>
  );
}
