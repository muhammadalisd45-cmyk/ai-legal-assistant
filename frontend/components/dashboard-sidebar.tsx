
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Icon } from "./icons";

const navigation = [
  { label: "Dashboard", href: "/dashboard", icon: "document" },
  { label: "New Query", href: "/case/new", icon: "plus" },
  { label: "Legal Research", href: "/research", icon: "search" },
  { label: "Source Library", href: "/sources", icon: "book" },
  { label: "Sign In", href: "/login", icon: "shield" },
] as const;

export function DashboardSidebar() {
  const pathname = usePathname();

  return (
    <aside className="pjn-sidebar" aria-label="Dashboard navigation">
      <Link href="/dashboard" className="pjn-sidebar-brand">
        <span className="pjn-sidebar-brand-icon">
          <Icon name="scale" size={25} />
        </span>
        <span>
          <strong>JUSTICE</strong>
          <small>PAKISTAN NAVIGATOR</small>
        </span>
      </Link>

      <p className="pjn-sidebar-label">WORKSPACE</p>

      <nav className="pjn-sidebar-nav">
        {navigation.map((item) => {
          const active =
            item.href === "/dashboard"
              ? pathname === "/dashboard"
              : pathname === item.href ||
                pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`pjn-sidebar-link${active ? " active" : ""}`}
              aria-current={active ? "page" : undefined}
            >
              <Icon name={item.icon} size={19} />
              <span>{item.label}</span>
              {active && <span className="pjn-sidebar-indicator" />}
            </Link>
          );
        })}
      </nav>

      <div className="pjn-sidebar-bottom">
        <Icon name="shield" size={19} />
        <div>
          <strong>Privacy first</strong>
          <p>Your legal information deserves care.</p>
        </div>
      </div>
    </aside>
  );
}

