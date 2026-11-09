import { DashboardClient } from "@/components/dashboard-client";

// The app sidebar comes from <SiteChrome> in the root layout (every app route), so the page renders content only.
export default function DashboardPage() {
  return <DashboardClient />;
}
