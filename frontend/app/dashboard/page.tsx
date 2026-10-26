import { DashboardClient } from "@/components/dashboard-client";
import { DashboardSidebar } from "@/components/dashboard-sidebar";

export default function DashboardPage() {
  return (
    <div className="pjn-dashboard-layout">
      <DashboardSidebar />
      <div className="pjn-dashboard-content">
        <DashboardClient />
      </div>
    </div>
  );
}
