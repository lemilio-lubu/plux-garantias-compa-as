"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  FileText,
  Package,
  ClipboardCheck,
  Activity,
  Users,
  LogOut,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";
import { ROLE_LABELS, CONCESIONARIA_LABELS, type UserRole } from "@/types/auth";

interface NavItem {
  href: string;
  label: string;
  icon: React.ElementType;
  roles: UserRole[];
}

const NAV_ITEMS: NavItem[] = [
  {
    href: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
    roles: ["SUPER_ADMIN", "JEFE_TALLER"],
  },
  {
    href: "/srgs",
    label: "SRGs",
    icon: FileText,
    roles: ["SUPER_ADMIN", "JEFE_TALLER", "ASESOR", "BODEGUERO", "AUDITOR"],
  },
  {
    href: "/catalog",
    label: "Catálogo",
    icon: Package,
    roles: ["SUPER_ADMIN", "JEFE_TALLER", "ASESOR"],
  },
  {
    href: "/audits",
    label: "Auditorías",
    icon: ClipboardCheck,
    roles: ["SUPER_ADMIN", "JEFE_TALLER", "AUDITOR"],
  },
  {
    href: "/events",
    label: "Trazabilidad",
    icon: Activity,
    roles: ["SUPER_ADMIN", "JEFE_TALLER", "AUDITOR"],
  },
  {
    href: "/users",
    label: "Usuarios",
    icon: Users,
    roles: ["SUPER_ADMIN", "JEFE_TALLER"],
  },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuthStore();

  const visibleItems = NAV_ITEMS.filter((item) =>
    user ? item.roles.includes(user.role) : false
  );

  const dealer = user?.concesionaria
    ? CONCESIONARIA_LABELS[user.concesionaria as keyof typeof CONCESIONARIA_LABELS] ?? user.concesionaria
    : "Consolidado";

  return (
    <aside className="flex h-screen w-[248px] flex-col bg-ink text-white shadow-rail">
      {/* Wordmark — instrument plate */}
      <div className="flex h-[68px] items-center gap-2.5 px-5">
        <span className="h-2.5 w-2.5 rounded-full bg-amber shadow-[0_0_10px_rgba(245,179,1,0.6)]" />
        <span className="font-display text-[22px] font-bold tracking-tight text-white">
          Plux
        </span>
        <span className="ml-auto eyebrow text-amber/80">{dealer}</span>
      </div>

      <div className="hazard-strip h-[3px] w-full opacity-90" />

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <p className="eyebrow px-3 pb-2 text-white/35">Operación</p>
        {visibleItems.map((item) => {
          const isActive =
            pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "group relative flex items-center gap-3 rounded-md pl-4 pr-3 h-11",
                "text-small font-medium transition-colors duration-150",
                isActive
                  ? "bg-white/[0.06] text-white"
                  : "text-white/55 hover:bg-white/[0.04] hover:text-white/90"
              )}
            >
              {/* Lit indicator bar */}
              <span
                className={cn(
                  "absolute left-0 top-1/2 h-5 w-[3px] -translate-y-1/2 rounded-full transition-all duration-150",
                  isActive ? "bg-amber shadow-[0_0_8px_rgba(245,179,1,0.7)]" : "bg-transparent group-hover:bg-white/20"
                )}
                aria-hidden
              />
              <item.icon
                size={17}
                className={cn("flex-shrink-0", isActive ? "text-amber" : "text-white/45")}
              />
              <span>{item.label}</span>
              {isActive && (
                <ChevronRight size={13} className="ml-auto text-white/30" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* User info + logout */}
      <div className="border-t border-white/[0.07] p-3">
        {user && (
          <div className="flex items-center gap-3 rounded-md px-2 py-2.5">
            <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-md bg-white/[0.08] font-display text-small font-semibold text-amber">
              {user.full_name.split(" ").map((n) => n[0]).slice(0, 2).join("")}
            </span>
            <div className="min-w-0">
              <p className="truncate text-small font-medium text-white">{user.full_name}</p>
              <p className="eyebrow text-white/45">{ROLE_LABELS[user.role]}</p>
            </div>
          </div>
        )}
        <button
          onClick={logout}
          className={cn(
            "mt-1 flex w-full items-center gap-3 rounded-md px-3 h-10",
            "text-small font-medium text-white/55",
            "transition-colors duration-150 hover:bg-white/[0.05] hover:text-white"
          )}
        >
          <LogOut size={16} className="flex-shrink-0" />
          Cerrar sesión
        </button>
      </div>
    </aside>
  );
}
